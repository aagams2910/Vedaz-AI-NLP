
# AI Astrologer

Full-stack astrology app using React (frontend) and Flask (backend) with Gemini 2.5 Pro for all astrological answers.

## Setup

**Backend:**
1. `cd backend`
2. `pip install -r requirements.txt`
3. Add your Google AI API key to `.env`:
    ```
    GOOGLE_AI_API_KEY=your_api_key_here
    ```
4. `python app.py` (runs at `http://localhost:8002`)

**Frontend:**
1. `cd frontend`
2. `npm install`
3. `npm start` (runs at `http://localhost:3000`)

## API

### POST /horoscope
Request:
```
{
   "name": "John Doe",
   "dateOfBirth": "YYYY-MM-DD",
   "timeOfBirth": "HH:MM",
   "placeOfBirth": "City, Country"
}
```
Response:
```
{
   "zodiacSign": "...",
   "element": "...",
   "personalityTraits": ["...", "...", ...],
   "predictions": "...",
   "birthDetails": {...}
}
```

### POST /ask
Request:
```
{
   "question": "...",
   "birthDetails": { ... }
}
```
Response:
```
{
   "answer": "..."
}
```
