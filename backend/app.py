from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import logging
from dotenv import load_dotenv
import requests
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure API keys
CEREBRAS_API_KEY = os.getenv('CEREBRAS_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Check which AI service to use (priority order)
if CEREBRAS_API_KEY:
    logger.info("Using Cerebras API")
    AI_SERVICE = 'cerebras'
    try:
        from cerebras.cloud.sdk import Cerebras
        cerebras_client = Cerebras(api_key=CEREBRAS_API_KEY)
    except ImportError:
        logger.warning(
            "Cerebras SDK not installed, falling back to next option")
        AI_SERVICE = None
elif OPENROUTER_API_KEY:
    logger.info("Using OpenRouter API")
    AI_SERVICE = 'openrouter'
elif GEMINI_API_KEY:
    logger.info("Using Gemini API")
    AI_SERVICE = 'gemini'
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
    except ImportError:
        logger.warning("Gemini SDK not installed")
        AI_SERVICE = None
else:
    logger.warning("No AI API key found, will use sample data")
    AI_SERVICE = None

# Create temp folder
AUDIO_FOLDER = 'temp_audio'
os.makedirs(AUDIO_FOLDER, exist_ok=True)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'ai_service': AI_SERVICE or 'sample_data',
        'cerebras_configured': bool(CEREBRAS_API_KEY),
        'openrouter_configured': bool(OPENROUTER_API_KEY),
        'gemini_configured': bool(GEMINI_API_KEY),
        'elevenlabs_configured': bool(ELEVENLABS_API_KEY),
        'maps_configured': bool(GOOGLE_MAPS_API_KEY)
    })


def call_cerebras_api(prompt):
    """Call Cerebras API"""
    try:
        completion = cerebras_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful travel planning assistant. Always respond with valid JSON when asked."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3.1-70b",  # Fast and capable model
            temperature=0.7,
            top_p=0.8,
            max_completion_tokens=4000
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Cerebras API error: {str(e)}")
        raise


def call_openrouter_api(prompt):
    """Call OpenRouter API"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "TripTeller"
    }

    payload = {
        "model": "meta-llama/llama-3.2-3b-instruct:free",  # Free model
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return result['choices'][0]['message']['content']


@app.route('/api/generate-itinerary', methods=['POST'])
def generate_itinerary():
    """Generate travel itinerary"""
    try:
        data = request.get_json()
        city = data.get('city', '')
        days = data.get('days', 3)

        if not city:
            return jsonify({'error': 'Please provide city name'}), 400

        if not AI_SERVICE:
            # Return sample data for testing
            return jsonify({
                'itinerary': get_sample_itinerary(city, days)
            })

        # Build prompt
        prompt = f"""
Create a {days}-day travel itinerary for {city}.

Requirements:
1. Recommend 3-5 attractions per day
2. Include attraction name, description, suggested duration, category (historical, natural, food, etc.)
3. Provide practical travel tips

Return in JSON format with the following structure:
{{
    "city": "{city}",
    "days": {days},
    "schedule": [
        {{
            "day": 1,
            "places": [
                {{
                    "name": "Attraction Name",
                    "description": "Detailed description (100-150 words)",
                    "duration": "Suggested duration",
                    "category": "Category"
                }}
            ]
        }}
    ],
    "tips": ["Tip 1", "Tip 2", "Tip 3"]
}}

Return only JSON, no additional text.
"""

        # Call appropriate AI service
        if AI_SERVICE == 'cerebras':
            response_text = call_cerebras_api(prompt)
        elif AI_SERVICE == 'openrouter':
            response_text = call_openrouter_api(prompt)
        elif AI_SERVICE == 'gemini':
            response = model.generate_content(prompt)
            response_text = response.text.strip()
        else:
            return jsonify({
                'itinerary': get_sample_itinerary(city, days)
            })

        # Clean response text
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        # Parse JSON
        itinerary = json.loads(response_text)

        # Flatten places list for map display
        all_places = []
        for day in itinerary.get('schedule', []):
            all_places.extend(day.get('places', []))

        itinerary['places'] = all_places

        logger.info(
            f"Successfully generated itinerary for {city} using {AI_SERVICE}")
        return jsonify({'itinerary': itinerary})

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        # Return sample data
        return jsonify({
            'itinerary': get_sample_itinerary(city, days)
        })
    except Exception as e:
        logger.error(f"Error generating itinerary: {str(e)}")
        return jsonify({'error': f'Failed to generate itinerary: {str(e)}'}), 500


@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    """Generate attraction audio narration"""
    try:
        data = request.get_json()
        place_name = data.get('place_name', '')
        description = data.get('description', '')

        if not place_name:
            return jsonify({'error': 'Please provide place name'}), 400

        if not ELEVENLABS_API_KEY:
            # Return sample audio URL
            return jsonify({
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
                'message': 'ElevenLabs API not configured, returning sample audio'
            })

        # Generate narration text
        text = f"{place_name}. {description}"

        # Use ElevenLabs to generate voice
        try:
            from elevenlabs import generate, save
            audio = generate(
                text=text,
                voice="Bella",  # Can choose different voices
                api_key=ELEVENLABS_API_KEY
            )

            # Save audio file
            audio_filename = f"{place_name.replace(' ', '_')}.mp3"
            audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
            save(audio, audio_path)

            logger.info(f"Successfully generated audio for {place_name}")

            # Return audio URL
            return jsonify({
                'audio_url': f'/api/audio/{audio_filename}'
            })
        except ImportError:
            return jsonify({
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
                'message': 'ElevenLabs library not installed, returning sample audio'
            })

    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        return jsonify({'error': f'Failed to generate audio: {str(e)}'}), 500


@app.route('/api/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    """Serve audio files"""
    try:
        audio_path = os.path.join(AUDIO_FOLDER, filename)
        return send_file(audio_path, mimetype='audio/mpeg')
    except Exception as e:
        logger.error(f"Error serving audio: {str(e)}")
        return jsonify({'error': 'Audio file not found'}), 404


@app.route('/api/generate-poster', methods=['POST'])
def generate_poster():
    """Generate destination poster (optional feature)"""
    try:
        data = request.get_json()
        city = data.get('city', '')

        if not city:
            return jsonify({'error': 'Please provide city name'}), 400

        # Use Gemini or other API to generate image
        # Return placeholder here
        poster_url = f"https://source.unsplash.com/800x600/?{city},travel"

        return jsonify({
            'poster_url': poster_url
        })

    except Exception as e:
        logger.error(f"Error generating poster: {str(e)}")
        return jsonify({'error': f'Failed to generate poster: {str(e)}'}), 500


def get_sample_itinerary(city, days):
    """Return sample itinerary data"""
    return {
        "city": city,
        "days": days,
        "schedule": [
            {
                "day": 1,
                "places": [
                    {
                        "name": f"{city} Central Square",
                        "description": f"The iconic square located in the heart of {city}, a must-visit destination for tourists. Here you'll find a blend of the city's history and modern culture, surrounded by important historical buildings and contemporary commercial areas. The square regularly hosts various cultural events and festivals.",
                        "duration": "1-2 hours",
                        "category": "Historical & Cultural"
                    },
                    {
                        "name": f"{city} Museum",
                        "description": f"Home to a rich collection of historical artifacts and art treasures, showcasing the historical development and cultural evolution of {city} and the surrounding region. The museum building itself is a work of art, combining traditional and modern design elements.",
                        "duration": "2-3 hours",
                        "category": "Culture & Education"
                    },
                    {
                        "name": f"{city} Old Town",
                        "description": f"A well-preserved historic district where you can experience the traditional charm of {city}. Narrow streets are lined with specialty shops, traditional restaurants, and cafes, making it a great place to experience local life.",
                        "duration": "2-3 hours",
                        "category": "Historical & Cultural"
                    }
                ]
            },
            {
                "day": 2,
                "places": [
                    {
                        "name": f"{city} Park",
                        "description": f"The largest city park in {city}, featuring lush greenery and scenic waterfront views. A popular spot for locals to relax and one of the best places to view the city skyline. The scenery is especially beautiful in spring and fall.",
                        "duration": "2-3 hours",
                        "category": "Nature & Scenery"
                    },
                    {
                        "name": f"{city} Food Street",
                        "description": f"A district that brings together various specialty foods of {city}, from traditional snacks to modern dining. The food street comes alive at night with bright lights and bustling crowds, making it the perfect place to taste authentic local cuisine.",
                        "duration": "2-3 hours",
                        "category": "Food & Shopping"
                    },
                    {
                        "name": f"{city} Observation Deck",
                        "description": f"Located at the city's highest point, this viewing platform offers a 360-degree panoramic view of {city}. Visit at sunset to enjoy the most spectacular city nightscape.",
                        "duration": "1-2 hours",
                        "category": "Sightseeing"
                    }
                ]
            },
            {
                "day": 3,
                "places": [
                    {
                        "name": f"{city} Market",
                        "description": f"The most distinctive traditional market in the area, selling fresh ingredients, handicrafts, and souvenirs. Here you can get close to the daily life of locals and it's a great place to buy unique gifts.",
                        "duration": "1-2 hours",
                        "category": "Shopping Experience"
                    },
                    {
                        "name": f"{city} Arts District",
                        "description": f"A creative arts district filled with galleries, studios, independent bookstores, and cafes. Street art murals and live performances add a unique cultural atmosphere to the area.",
                        "duration": "2-3 hours",
                        "category": "Arts & Culture"
                    }
                ]
            }
        ],
        "tips": [
            f"Check {city}'s weather forecast in advance and prepare appropriate clothing",
            "Consider purchasing a local transportation card to save on costs",
            "Respect local culture and customs, be mindful of your behavior",
            "Keep your personal belongings safe and stay aware of your surroundings",
            "Download translation apps and offline maps in case you need them"
        ],
        "places": []  # Will be filled later
    }


if __name__ == '__main__':
    logger.info("Starting TripTeller Backend Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
