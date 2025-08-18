from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv
from zodiac_data import get_zodiac_sign, get_zodiac_info

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Google Generative AI
GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY')
if not GOOGLE_AI_API_KEY:
    print("Warning: GOOGLE_AI_API_KEY not found in environment variables")
    print("Please create a .env file with your Google AI API key")

genai.configure(api_key=GOOGLE_AI_API_KEY)

# Initialize Gemini model
try:
    model = genai.GenerativeModel('gemini-2.5-pro')
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    model = None

@app.route('/')
def home():
    """Home endpoint with API information."""
    return jsonify({
        "message": "AI Astrologer API",
        "version": "1.0.0",
        "endpoints": {
            "/horoscope": "POST - Generate horoscope based on birth details",
            "/ask": "POST - Ask custom astrology questions using AI"
        }
    })

@app.route('/horoscope', methods=['POST'])
def generate_horoscope():
    """
    Generate horoscope based on birth details.
    
    Expected JSON payload:
    {
        "name": "John Doe",
        "dateOfBirth": "1990-05-15",
        "timeOfBirth": "14:30",
        "placeOfBirth": "New York, NY"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'dateOfBirth', 'timeOfBirth', 'placeOfBirth']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Parse birth date
        try:
            birth_date = datetime.strptime(data['dateOfBirth'], '%Y-%m-%d')
            month = birth_date.month
            day = birth_date.day
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        # Get zodiac sign
        zodiac_sign = get_zodiac_sign(month, day)
        if zodiac_sign == "Unknown":
            return jsonify({"error": "Could not determine zodiac sign"}), 400
        
        # Get basic zodiac info
        zodiac_info = get_zodiac_info(zodiac_sign)
        
        # Generate AI-powered horoscope
        horoscope_prompt = f"""Generate a personalized horoscope for {data['name']} based on their zodiac sign {zodiac_sign}.

Birth Details:
- Date: {data['dateOfBirth']}
- Time: {data['timeOfBirth']}
- Place: {data['placeOfBirth']}
- Zodiac: {zodiac_sign} ({zodiac_info.get('element', '')} element)

Provide:
1. 5 key personality traits (comma-separated)
2. A brief yearly forecast (2-3 sentences)

Format your response exactly like this:
TRAITS: trait1, trait2, trait3, trait4, trait5
FORECAST: Your forecast text here..."""
        
        try:
            # Generate AI horoscope
            horoscope_response = model.generate_content(horoscope_prompt)
            horoscope_text = horoscope_response.text.strip()
            
            # Parse AI response
            traits_line = [line for line in horoscope_text.split('\n') if line.startswith('TRAITS:')]
            forecast_line = [line for line in horoscope_text.split('\n') if line.startswith('FORECAST:')]
            
            if traits_line and forecast_line:
                traits = [trait.strip() for trait in traits_line[0].replace('TRAITS:', '').split(',')]
                forecast = forecast_line[0].replace('FORECAST:', '').strip()
            else:
                # Fallback to hardcoded data if AI parsing fails
                traits = zodiac_info.get("personality_traits", [])[:5]
                forecast = zodiac_info.get("predictions", "")
            
            # Prepare response
            response = {
                "zodiacSign": zodiac_sign,
                "element": zodiac_info.get("element", ""),
                "personalityTraits": traits,
                "predictions": forecast,
                "birthDetails": {
                    "name": data['name'],
                    "dateOfBirth": data['dateOfBirth'],
                    "timeOfBirth": data['timeOfBirth'],
                    "placeOfBirth": data['placeOfBirth']
                }
            }
            
        except Exception as ai_error:
            # Fallback to hardcoded data if AI fails
            response = {
                "zodiacSign": zodiac_sign,
                "element": zodiac_info.get("element", ""),
                "personalityTraits": zodiac_info.get("personality_traits", [])[:5],
                "predictions": zodiac_info.get("predictions", ""),
                "birthDetails": {
                    "name": data['name'],
                    "dateOfBirth": data['dateOfBirth'],
                    "timeOfBirth": data['timeOfBirth'],
                    "placeOfBirth": data['placeOfBirth']
                }
            }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/ask', methods=['POST'])
def ask_astrology_question():
    """
    Answer custom astrology questions using Gemini 2.5 Pro.
    
    Expected JSON payload:
    {
        "question": "What does my love life look like this year?",
        "birthDetails": {
            "name": "John Doe",
            "dateOfBirth": "1990-05-15",
            "timeOfBirth": "14:30",
            "placeOfBirth": "New York, NY"
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'question' not in data:
            return jsonify({"error": "Missing required field: question"}), 400
        if 'birthDetails' not in data:
            return jsonify({"error": "Missing required field: birthDetails"}), 400
        
        birth_details = data['birthDetails']
        required_birth_fields = ['name', 'dateOfBirth', 'timeOfBirth', 'placeOfBirth']
        for field in required_birth_fields:
            if field not in birth_details:
                return jsonify({"error": f"Missing required birth detail: {field}"}), 400
        
        # Check if Gemini model is available
        if not model:
            return jsonify({"error": "AI model not available. Please check API key configuration."}), 500
        
        # Parse birth date to get zodiac sign
        try:
            birth_date = datetime.strptime(birth_details['dateOfBirth'], '%Y-%m-%d')
            month = birth_date.month
            day = birth_date.day
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        zodiac_sign = get_zodiac_sign(month, day)
        if zodiac_sign == "Unknown":
            return jsonify({"error": "Could not determine zodiac sign"}), 400
        
        # Get zodiac information for context
        zodiac_info = get_zodiac_info(zodiac_sign)
        
        # Create prompt for Gemini
        prompt = f"""You are a friendly AI astrologer. Answer the user's astrology question in a simple, concise way (2-4 sentences maximum).

User Details:
- Name: {birth_details['name']}
- Zodiac Sign: {zodiac_sign}
- Element: {zodiac_info.get('element', '')}
- Key Traits: {', '.join(zodiac_info.get('personality_traits', [])[:3])}

Question: {data['question']}

Give a brief, encouraging astrological insight based on their zodiac sign. Keep it simple, positive, and under 100 words."""

        try:
            # Generate response using Gemini
            response = model.generate_content(prompt)
            answer = response.text.strip()
            
            return jsonify({
                "answer": answer,
                "zodiacSign": zodiac_sign,
                "question": data['question']
            })
            
        except Exception as ai_error:
            return jsonify({"error": f"AI service error: {str(ai_error)}"}), 500
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ai_model_available": model is not None
    })

if __name__ == '__main__':
    print("Starting AI Astrologer Backend...")
    print(f"AI Model Available: {model is not None}")
    if not GOOGLE_AI_API_KEY:
        print("Warning: GOOGLE_AI_API_KEY not configured")
    app.run(debug=True, host='0.0.0.0', port=8002) 