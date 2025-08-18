import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    dateOfBirth: '',
    timeOfBirth: '',
    placeOfBirth: ''
  });

  const [horoscope, setHoroscope] = useState(null);
  const [aiQuestion, setAiQuestion] = useState('');
  const [aiResponse, setAiResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const generateHoroscope = async () => {
    // Validate form data
    if (!formData.name || !formData.dateOfBirth || !formData.timeOfBirth || !formData.placeOfBirth) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/horoscope', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate horoscope');
      }

      setHoroscope(data);
      setError('');
    } catch (err) {
      setError(err.message);
      setHoroscope(null);
    } finally {
      setLoading(false);
    }
  };

  const askAIQuestion = async () => {
    if (!aiQuestion.trim()) {
      setError('Please enter a question');
      return;
    }

    if (!horoscope) {
      setError('Please generate your horoscope first');
      return;
    }

    setAiLoading(true);
    setError('');

    try {
      const response = await fetch('/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: aiQuestion,
          birthDetails: formData
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get AI response');
      }

      setAiResponse(data);
      setError('');
    } catch (err) {
      setError(err.message);
      setAiResponse(null);
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="header">
        <h1>🌟 AI Astrologer</h1>
        <p>Discover your destiny with the power of AI and ancient wisdom</p>
      </div>

      <div className="main-container">
        {/* Birth Details Form */}
        <div className="form-section">
          <h2>Enter Your Birth Details</h2>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="name">Full Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Enter your full name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="dateOfBirth">Date of Birth</label>
              <input
                type="date"
                id="dateOfBirth"
                name="dateOfBirth"
                value={formData.dateOfBirth}
                onChange={handleInputChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="timeOfBirth">Time of Birth</label>
              <input
                type="time"
                id="timeOfBirth"
                name="timeOfBirth"
                value={formData.timeOfBirth}
                onChange={handleInputChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="placeOfBirth">Place of Birth</label>
              <input
                type="text"
                id="placeOfBirth"
                name="placeOfBirth"
                value={formData.placeOfBirth}
                onChange={handleInputChange}
                placeholder="City, Country"
              />
            </div>
          </div>

          <button 
            className="btn" 
            onClick={generateHoroscope}
            disabled={loading}
          >
            {loading ? 'Generating Horoscope...' : 'Generate Horoscope'}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="error fade-in">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="loading fade-in">
            <div className="spinner"></div>
            <p>Consulting the stars...</p>
          </div>
        )}

        {/* Horoscope Results */}
        {horoscope && !loading && (
          <div className="results-section fade-in">
            <h2>Your Astrological Profile</h2>
            
            <div className="zodiac-card">
              <div className="zodiac-sign">{horoscope.zodiacSign}</div>
              <div className="element">Element: {horoscope.element}</div>
              
              <div className="traits-section">
                <h3>Your Personality Traits</h3>
                <div className="traits-list">
                  {horoscope.personalityTraits.map((trait, index) => (
                    <span key={index} className="trait-tag">{trait}</span>
                  ))}
                </div>
              </div>

              <div className="predictions">
                <h3>Your Yearly Forecast</h3>
                <p>{horoscope.predictions}</p>
              </div>
            </div>
          </div>
        )}

        {/* AI Question Section */}
        {horoscope && (
          <div className="ai-question-section fade-in">
            <h2>Ask Your Personal AI Astrologer</h2>
            <p style={{ textAlign: 'center', marginBottom: '20px', color: '#666' }}>
              Have a specific question about your life, relationships, career, or future? 
              Ask our AI astrologer for personalized insights!
            </p>
            
            <textarea
              className="question-input"
              placeholder="Ask anything about your astrology, relationships, career, or future... (e.g., 'What does my love life look like this year?' or 'Will I get a promotion soon?')"
              value={aiQuestion}
              onChange={(e) => setAiQuestion(e.target.value)}
              rows="4"
            />

            <button 
              className="btn" 
              onClick={askAIQuestion}
              disabled={aiLoading}
            >
              {aiLoading ? 'Consulting AI...' : 'Ask AI Astrologer'}
            </button>

            {/* AI Loading State */}
            {aiLoading && (
              <div className="loading fade-in">
                <div className="spinner"></div>
                <p>Your AI astrologer is analyzing the cosmic energies...</p>
              </div>
            )}

            {/* AI Response */}
            {aiResponse && !aiLoading && (
              <div className="ai-response fade-in">
                <h3>🌟 AI Astrological Insight</h3>
                <p>{aiResponse.answer}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App; 