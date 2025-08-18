"""
Zodiac data module containing all zodiac sign information, date ranges, and personality traits.
"""

ZODIAC_SIGNS = {
    "Aries": {
        "date_range": (3, 21, 4, 19),
        "element": "Fire",
        "personality_traits": [
            "Courageous", "Energetic", "Willful", "Pioneering", "Independent",
            "Dynamic", "Quick-witted", "Enthusiastic", "Confident", "Optimistic"
        ],
        "predictions": "This year brings new beginnings and exciting opportunities. Your natural leadership qualities will shine, and you'll find yourself taking charge of important projects. Your energy and enthusiasm will attract positive attention and open doors to new possibilities."
    },
    "Taurus": {
        "date_range": (4, 20, 5, 20),
        "element": "Earth",
        "personality_traits": [
            "Patient", "Reliable", "Devoted", "Persistent", "Practical",
            "Stable", "Determined", "Loyal", "Ambitious", "Sensual"
        ],
        "predictions": "Stability and growth are your themes this year. Your practical approach to life will help you build solid foundations in both personal and professional areas. Financial opportunities may arise, and your patience will be rewarded with long-term success."
    },
    "Gemini": {
        "date_range": (5, 21, 6, 20),
        "element": "Air",
        "personality_traits": [
            "Adaptable", "Versatile", "Communicative", "Witty", "Intellectual",
            "Eloquent", "Youthful", "Lively", "Quick-thinking", "Curious"
        ],
        "predictions": "Communication and learning are highlighted this year. Your natural curiosity will lead you to new knowledge and experiences. Networking opportunities abound, and your ability to adapt will help you navigate any challenges that arise."
    },
    "Cancer": {
        "date_range": (6, 21, 7, 22),
        "element": "Water",
        "personality_traits": [
            "Nurturing", "Protective", "Sympathetic", "Moody", "Tenacious",
            "Highly imaginative", "Loyal", "Emotional", "Intuitive", "Caring"
        ],
        "predictions": "Emotional growth and family matters take center stage this year. Your intuitive nature will guide you in making important decisions. Home and family life will bring you great satisfaction, and your nurturing qualities will be appreciated by those around you."
    },
    "Leo": {
        "date_range": (7, 23, 8, 22),
        "element": "Fire",
        "personality_traits": [
            "Creative", "Passionate", "Generous", "Warm-hearted", "Cheerful",
            "Humorous", "Dignified", "Self-confident", "Natural leader", "Dramatic"
        ],
        "predictions": "This is your year to shine! Your natural charisma and leadership abilities will be recognized and rewarded. Creative projects will flourish, and your generous spirit will attract positive relationships. Success in your chosen field is highly likely."
    },
    "Virgo": {
        "date_range": (8, 23, 9, 22),
        "element": "Earth",
        "personality_traits": [
            "Analytical", "Kind", "Hardworking", "Practical", "Modest",
            "Intelligent", "Loyal", "Reliable", "Perfectionist", "Helpful"
        ],
        "predictions": "Your attention to detail and analytical mind will serve you well this year. Professional growth and skill development are highlighted. Your practical approach to problem-solving will earn you respect and recognition in your work environment."
    },
    "Libra": {
        "date_range": (9, 23, 10, 22),
        "element": "Air",
        "personality_traits": [
            "Diplomatic", "Gracious", "Fair-minded", "Social", "Peaceful",
            "Idealistic", "Cooperative", "Romantic", "Charming", "Easy-going"
        ],
        "predictions": "Relationships and harmony are your focus this year. Your diplomatic nature will help resolve conflicts and build stronger connections. Partnership opportunities, both personal and professional, will bring balance and fulfillment to your life."
    },
    "Scorpio": {
        "date_range": (10, 23, 11, 21),
        "element": "Water",
        "personality_traits": [
            "Passionate", "Determined", "Magnetic", "Mysterious", "Strategic",
            "Intense", "Perceptive", "Loyal", "Ambitious", "Transformative"
        ],
        "predictions": "Transformation and deep personal growth are your themes this year. Your intuitive insights will lead to important discoveries about yourself and others. Financial opportunities may arise through your strategic thinking and determination."
    },
    "Sagittarius": {
        "date_range": (11, 22, 12, 21),
        "element": "Fire",
        "personality_traits": [
            "Optimistic", "Adventurous", "Independent", "Honest", "Philosophical",
            "Enthusiastic", "Wanderlust", "Extroverted", "Fun-loving", "Generous"
        ],
        "predictions": "Adventure and expansion are calling you this year. Travel opportunities, both physical and intellectual, will broaden your horizons. Your optimistic outlook will attract positive experiences, and your honesty will strengthen important relationships."
    },
    "Capricorn": {
        "date_range": (12, 22, 1, 19),
        "element": "Earth",
        "personality_traits": [
            "Responsible", "Disciplined", "Self-controlled", "Ambitious", "Patient",
            "Humble", "Hardworking", "Traditional", "Practical", "Wise"
        ],
        "predictions": "Career advancement and long-term goals are your focus this year. Your disciplined approach and patience will pay off with significant achievements. Financial stability and professional recognition are likely outcomes of your hard work."
    },
    "Aquarius": {
        "date_range": (1, 20, 2, 18),
        "element": "Air",
        "personality_traits": [
            "Progressive", "Original", "Independent", "Humanitarian", "Intellectual",
            "Friendly", "Aloof", "Inventive", "Unconventional", "Visionary"
        ],
        "predictions": "Innovation and social change are your themes this year. Your unique perspective and humanitarian instincts will lead to meaningful contributions to society. Networking with like-minded individuals will open doors to exciting opportunities."
    },
    "Pisces": {
        "date_range": (2, 19, 3, 20),
        "element": "Water",
        "personality_traits": [
            "Compassionate", "Artistic", "Intuitive", "Gentle", "Musical",
            "Romantic", "Dreamy", "Mystical", "Selfless", "Adaptable"
        ],
        "predictions": "Spiritual growth and creative expression are highlighted this year. Your intuitive abilities will be heightened, leading to important insights. Artistic projects and spiritual pursuits will bring you deep satisfaction and personal fulfillment."
    }
}

def get_zodiac_sign(month, day):
    """
    Determine zodiac sign based on birth month and day.
    
    Args:
        month (int): Birth month (1-12)
        day (int): Birth day (1-31)
    
    Returns:
        str: Zodiac sign name
    """
    for sign, data in ZODIAC_SIGNS.items():
        start_month, start_day, end_month, end_day = data["date_range"]
        
        # Handle Capricorn (spans across year end)
        if start_month == 12 and end_month == 1:
            if (month == 12 and day >= start_day) or (month == 1 and day <= end_day):
                return sign
        else:
            # Regular date range check
            if (month == start_month and day >= start_day) or \
               (month == end_month and day <= end_day) or \
               (start_month < month < end_month):
                return sign
    
    return "Unknown"

def get_zodiac_info(zodiac_sign):
    """
    Get complete information for a zodiac sign.
    
    Args:
        zodiac_sign (str): Name of the zodiac sign
    
    Returns:
        dict: Complete zodiac sign information
    """
    return ZODIAC_SIGNS.get(zodiac_sign, {}) 