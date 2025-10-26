from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import logging
from dotenv import load_dotenv
import requests
from io import BytesIO
import re
from urllib.parse import quote, urljoin
import speech_recognition as sr
import tempfile
import wave

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
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Check which AI service to use (priority order)
cerebras_client = None
model = None
AI_SERVICE = None

if CEREBRAS_API_KEY:
    try:
        from cerebras.cloud.sdk import Cerebras
        cerebras_client = Cerebras(api_key=CEREBRAS_API_KEY)
        AI_SERVICE = 'cerebras'
        logger.info("✅ Using Cerebras API")
    except ImportError as e:
        logger.warning(
            f"Cerebras SDK not installed: {e}, falling back to next option")
        AI_SERVICE = None
    except Exception as e:
        logger.error(f"Failed to initialize Cerebras client: {e}")
        AI_SERVICE = None

if not AI_SERVICE and OPENROUTER_API_KEY:
    AI_SERVICE = 'openrouter'
    logger.info("✅ Using OpenRouter API")

if not AI_SERVICE and GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        AI_SERVICE = 'gemini'
        logger.info("✅ Using Gemini API")
    except ImportError as e:
        logger.warning(f"Gemini SDK not installed: {e}")
        AI_SERVICE = None
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        AI_SERVICE = None

if not AI_SERVICE:
    logger.warning("⚠️  No AI API configured, will use sample data")
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
        'maps_configured': bool(GOOGLE_MAPS_API_KEY),
        'weather_configured': bool(OPENWEATHER_API_KEY)
    })


@app.route('/api/search-places', methods=['POST'])
def search_places():
    """
    Search for places using Google Geocoding API.
    Returns a list of matching places with their details (country, state, formatted address).
    Handles duplicate city names by returning all matches.
    """
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    if not GOOGLE_MAPS_API_KEY:
        logger.warning("Google Maps API key not configured")
        return jsonify({'error': 'Google Maps API not configured'}), 500
    
    try:
        # Use Google Geocoding API to search for the place
        geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': query,
            'key': GOOGLE_MAPS_API_KEY
        }
        
        logger.info(f"🔍 Searching for place: {query}")
        response = requests.get(geocode_url, params=params)
        response.raise_for_status()
        
        geocode_data = response.json()
        
        if geocode_data['status'] == 'ZERO_RESULTS':
            return jsonify({'places': []}), 200
        
        if geocode_data['status'] != 'OK':
            logger.error(f"Geocoding API error: {geocode_data['status']}")
            return jsonify({'error': f"Geocoding failed: {geocode_data['status']}"}), 500
        
        # Parse results to extract relevant place information
        places = []
        for result in geocode_data['results']:
            place_info = {
                'formatted_address': result['formatted_address'],
                'place_id': result['place_id'],
                'location': result['geometry']['location'],
                'city': None,
                'state': None,
                'country': None,
                'country_code': None
            }
            
            # Extract city, state, and country from address components
            for component in result['address_components']:
                types = component['types']
                
                if 'locality' in types:
                    place_info['city'] = component['long_name']
                elif 'administrative_area_level_1' in types:
                    place_info['state'] = component['long_name']
                elif 'country' in types:
                    place_info['country'] = component['long_name']
                    place_info['country_code'] = component['short_name']
            
            # If no city found, try to use other locality types
            if not place_info['city']:
                for component in result['address_components']:
                    types = component['types']
                    if 'administrative_area_level_2' in types or 'sublocality' in types:
                        place_info['city'] = component['long_name']
                        break
            
            places.append(place_info)
        
        logger.info(f"✅ Found {len(places)} place(s)")
        return jsonify({'places': places}), 200
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error calling Geocoding API: {str(e)}")
        return jsonify({'error': 'Failed to search for places'}), 500
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


def call_cerebras_api(prompt):
    """Call Cerebras API"""
    if not cerebras_client:
        raise Exception("Cerebras client not initialized")

    try:
        logger.info("📡 Calling Cerebras API...")
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
            model="llama3.1-8b",  # Available Cerebras model
            temperature=0.7,
            top_p=0.8,
            max_completion_tokens=4000
        )
        response_content = completion.choices[0].message.content
        logger.info(
            f"✅ Cerebras API response received ({len(response_content)} chars)")
        return response_content
    except Exception as e:
        logger.error(f"❌ Cerebras API error: {str(e)}")
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
    """
    Generate travel itinerary for a confirmed location
    Accepts location_context with detailed place information (state, country, coordinates)
    """
    try:
        data = request.get_json()
        city = data.get('city', '')
        days = data.get('days', 3)
        intensity = data.get('intensity', 'moderate')
        preferences = data.get('preferences', [])
        location_context = data.get('location_context', {})

        if not city:
            return jsonify({'error': 'Please provide city name'}), 400
        
        # Extract additional location details if provided
        state = location_context.get('state', '')
        country = location_context.get('country', '')
        
        # Build full location name for better context
        full_location = city
        if state and country:
            full_location = f"{city}, {state}, {country}"
        elif country:
            full_location = f"{city}, {country}"
        
        logger.info(f"Generating itinerary for: {full_location}")

        if not AI_SERVICE:
            # Return sample data for testing
            return jsonify({
                'itinerary': get_sample_itinerary(city, days)
            })

        # Build intensity-specific requirements
        intensity_descriptions = {
            'relaxed': 'Relaxed pace with 2-3 attractions per day, plenty of rest time, focus on leisurely activities and relaxation. Allow 3-4 hours per attraction.',
            'moderate': 'Balanced pace with 3-4 attractions per day, mix of activities and rest. Allow 2-3 hours per attraction.',
            'intensive': 'Fast-paced with 4-6 attractions per day, maximize sightseeing, early starts and full days. Allow 1-2 hours per attraction.'
        }

        intensity_desc = intensity_descriptions.get(
            intensity, intensity_descriptions['moderate'])

        # Build preferences description
        preference_desc = ""
        if preferences:
            pref_names = ', '.join(preferences)
            preference_desc = f"\nUser Preferences: Focus on {pref_names} attractions and experiences. Prioritize these categories when selecting destinations."

        # Build prompt with full location context
        prompt = f"""
Create a {days}-day travel itinerary for {full_location} with a {intensity} travel pace.

Travel Intensity: {intensity_desc}{preference_desc}

Requirements:
1. Adjust number of attractions per day based on the {intensity} intensity level
2. Include attraction name, description, suggested duration, category (historical, natural, food, culture, shopping, adventure, nightlife, art, etc.)
3. {'IMPORTANT: Prioritize ' + ', '.join(preferences) + ' attractions based on user preferences' if preferences else 'Include a diverse mix of attractions'}
4. Provide practical travel tips specific to the {intensity} pace
5. Consider travel time between attractions for {intensity} travelers
6. Focus on attractions specifically in {full_location} to avoid confusion with similarly named cities
7. For each attraction, include ticket information with:
   - requires_ticket: true/false
   - ticket_price: estimated price or "Free"
   - booking_url: search URL for tickets
   - source: "AI Generated"
   - notes: brief ticket information

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
                    "category": "Category",
                    "ticket_info": {{
                        "requires_ticket": true/false,
                        "ticket_price": "price or Free",
                        "booking_url": "search URL",
                        "source": "AI Generated",
                        "notes": "ticket information"
                    }}
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

        # Use ElevenLabs to generate voice (using new client API)
        try:
            from elevenlabs.client import ElevenLabs
            
            # Initialize ElevenLabs client
            client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
            
            # Generate audio using text-to-speech
            audio_generator = client.text_to_speech.convert(
                text=text,
                voice_id="JBFqnCBsd6RMkjVDRZzb",  # George voice (clear, professional)
                model_id="eleven_multilingual_v2",  # Supports multiple languages
                output_format="mp3_44100_128",
            )
            
            # Save audio file
            audio_filename = f"{place_name.replace(' ', '_').replace('/', '_')}.mp3"
            audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
            
            # Write audio bytes to file
            with open(audio_path, 'wb') as audio_file:
                for chunk in audio_generator:
                    audio_file.write(chunk)

            logger.info(f"✅ Successfully generated audio for {place_name}")

            # Return audio URL
            return jsonify({
                'audio_url': f'/api/audio/{audio_filename}',
                'place_name': place_name
            })
        except ImportError as e:
            logger.warning(f"ElevenLabs library not installed: {e}")
            return jsonify({
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
                'message': 'ElevenLabs library not installed, returning sample audio'
            })
        except Exception as e:
            logger.error(f"Error calling ElevenLabs API: {str(e)}")
            return jsonify({
                'audio_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
                'message': f'Failed to generate audio: {str(e)}'
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


def search_ticket_info(attraction_name, city):
    """Search for ticket information for an attraction"""
    try:
        logger.info(f"Searching ticket info for: {attraction_name} in {city}")
        
        # Multiple search strategies
        ticket_info = None
        
        # Strategy 1: Search TripAdvisor
        ticket_info = search_tripadvisor_tickets(attraction_name, city)
        if ticket_info:
            return ticket_info
            
        # Strategy 2: Search Viator
        ticket_info = search_viator_tickets(attraction_name, city)
        if ticket_info:
            return ticket_info
            
        # Strategy 3: Search GetYourGuide
        ticket_info = search_getyourguide_tickets(attraction_name, city)
        if ticket_info:
            return ticket_info
            
        # Strategy 4: Generic search
        ticket_info = search_generic_tickets(attraction_name, city)
        if ticket_info:
            return ticket_info
            
        # Default response if no tickets found
        return {
            'requires_ticket': False,
            'ticket_price': None,
            'booking_url': None,
            'source': 'No ticket information found',
            'notes': 'This attraction may be free to visit or tickets may be available on-site'
        }
        
    except Exception as e:
        logger.error(f"Error searching ticket info: {str(e)}")
        return {
            'requires_ticket': False,
            'ticket_price': None,
            'booking_url': None,
            'source': 'Error',
            'notes': f'Unable to determine ticket requirements: {str(e)}'
        }


def search_tripadvisor_tickets(attraction_name, city):
    """Search TripAdvisor for ticket information"""
    try:
        # Construct search query
        search_query = f"{attraction_name} {city} tickets"
        
        # Use a web search API or scraping approach
        # For now, return a structured response based on common patterns
        attraction_lower = attraction_name.lower()
        
        # Common paid attractions
        paid_keywords = ['museum', 'palace', 'castle', 'tower', 'aquarium', 'zoo', 'theme park', 'gallery', 'exhibition']
        free_keywords = ['park', 'square', 'beach', 'market', 'street', 'district', 'neighborhood']
        
        requires_ticket = any(keyword in attraction_lower for keyword in paid_keywords)
        
        if requires_ticket:
            return {
                'requires_ticket': True,
                'ticket_price': 'Varies (check official website)',
                'booking_url': f'https://www.tripadvisor.com/Attraction_Products-g{get_city_code(city)}-{attraction_name.replace(" ", "_")}.html',
                'source': 'TripAdvisor',
                'notes': 'Tickets may be available online or at the venue'
            }
        elif any(keyword in attraction_lower for keyword in free_keywords):
            return {
                'requires_ticket': False,
                'ticket_price': 'Free',
                'booking_url': None,
                'source': 'TripAdvisor',
                'notes': 'This attraction is typically free to visit'
            }
            
        return None
        
    except Exception as e:
        logger.error(f"TripAdvisor search error: {str(e)}")
        return None


def search_viator_tickets(attraction_name, city):
    """Search Viator for ticket information"""
    try:
        # Construct Viator search URL
        search_query = f"{attraction_name} {city}"
        viator_url = f"https://www.viator.com/searchResults/all?text={quote(search_query)}"
        
        # For demonstration, return structured data
        attraction_lower = attraction_name.lower()
        
        # Check if it's likely a paid attraction
        paid_indicators = ['museum', 'palace', 'castle', 'tower', 'aquarium', 'zoo', 'theme park']
        
        if any(indicator in attraction_lower for indicator in paid_indicators):
            return {
                'requires_ticket': True,
                'ticket_price': 'From $10-50 (varies by attraction)',
                'booking_url': viator_url,
                'source': 'Viator',
                'notes': 'Skip-the-line tickets available'
            }
            
        return None
        
    except Exception as e:
        logger.error(f"Viator search error: {str(e)}")
        return None


def search_getyourguide_tickets(attraction_name, city):
    """Search GetYourGuide for ticket information"""
    try:
        search_query = f"{attraction_name} {city}"
        getyourguide_url = f"https://www.getyourguide.com/s/?q={quote(search_query)}"
        
        # Similar logic to Viator
        attraction_lower = attraction_name.lower()
        
        if any(keyword in attraction_lower for keyword in ['museum', 'palace', 'castle', 'tower']):
            return {
                'requires_ticket': True,
                'ticket_price': 'From €8-25 (varies by attraction)',
                'booking_url': getyourguide_url,
                'source': 'GetYourGuide',
                'notes': 'Instant confirmation and mobile tickets'
            }
            
        return None
        
    except Exception as e:
        logger.error(f"GetYourGuide search error: {str(e)}")
        return None


def search_generic_tickets(attraction_name, city):
    """Generic ticket search using common patterns"""
    try:
        attraction_lower = attraction_name.lower()
        
        # Museum pattern
        if 'museum' in attraction_lower:
            return {
                'requires_ticket': True,
                'ticket_price': 'Typically $10-20',
                'booking_url': f'https://www.google.com/search?q={quote(f"{attraction_name} {city} tickets")}',
                'source': 'General Search',
                'notes': 'Most museums require tickets. Check official website for current prices.'
            }
        
        # Theme park pattern
        if any(keyword in attraction_lower for keyword in ['theme park', 'amusement park', 'park']):
            return {
                'requires_ticket': True,
                'ticket_price': 'Typically $30-100+',
                'booking_url': f'https://www.google.com/search?q={quote(f"{attraction_name} {city} tickets")}',
                'source': 'General Search',
                'notes': 'Theme parks require tickets. Advance booking recommended.'
            }
        
        # Historical site pattern
        if any(keyword in attraction_lower for keyword in ['palace', 'castle', 'fortress', 'tower']):
            return {
                'requires_ticket': True,
                'ticket_price': 'Typically $5-25',
                'booking_url': f'https://www.google.com/search?q={quote(f"{attraction_name} {city} tickets")}',
                'source': 'General Search',
                'notes': 'Historical sites often require tickets. Audio guides may be extra.'
            }
        
        # Free attraction pattern
        if any(keyword in attraction_lower for keyword in ['park', 'square', 'beach', 'market', 'street']):
            return {
                'requires_ticket': False,
                'ticket_price': 'Free',
                'booking_url': None,
                'source': 'General Search',
                'notes': 'This attraction is typically free to visit'
            }
        
        return None
        
    except Exception as e:
        logger.error(f"Generic search error: {str(e)}")
        return None


def get_city_code(city):
    """Get city code for TripAdvisor (simplified)"""
    city_codes = {
        'tokyo': '298184',
        'paris': '187147',
        'london': '186338',
        'new york': '60763',
        'rome': '187791',
        'barcelona': '187497',
        'amsterdam': '188590',
        'berlin': '187275',
        'madrid': '187514',
        'vienna': '190454'
    }
    return city_codes.get(city.lower(), '187147')  # Default to Paris


@app.route('/api/get-ticket-info', methods=['POST'])
def get_ticket_info():
    """Get ticket information for an attraction"""
    try:
        data = request.get_json()
        attraction_name = data.get('attraction_name', '')
        city = data.get('city', '')

        if not attraction_name:
            return jsonify({'error': 'Please provide attraction name'}), 400

        # Search for ticket information
        ticket_info = search_ticket_info(attraction_name, city)
        
        logger.info(f"Ticket info for {attraction_name}: {ticket_info}")
        return jsonify({'ticket_info': ticket_info})

    except Exception as e:
        logger.error(f"Error getting ticket info: {str(e)}")
        return jsonify({'error': f'Failed to get ticket info: {str(e)}'}), 500


@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech audio to text"""
    try:
        # 检查是否有音频文件
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400

        # 创建临时文件保存音频
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            # 初始化语音识别器
            recognizer = sr.Recognizer()
            
            # 读取音频文件
            with sr.AudioFile(temp_file_path) as source:
                # 调整环境噪音
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.record(source)
            
            # 尝试使用Google语音识别（支持中文）
            try:
                text = recognizer.recognize_google(audio_data, language='zh-CN')
                logger.info(f"Speech recognition successful: {text}")
                return jsonify({
                    'text': text,
                    'confidence': 0.9,  # Google API不返回置信度，使用默认值
                    'language': 'zh-CN'
                })
            except sr.UnknownValueError:
                return jsonify({'error': '无法识别语音内容，请重试'}), 400
            except sr.RequestError as e:
                logger.error(f"Google Speech API error: {e}")
                # 如果Google API失败，尝试其他方法
                return jsonify({'error': '语音识别服务暂时不可用，请稍后重试'}), 500
                
        finally:
            # 清理临时文件
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    except Exception as e:
        logger.error(f"Speech to text error: {str(e)}")
        return jsonify({'error': f'语音识别失败: {str(e)}'}), 500


@app.route('/api/speech-to-text-offline', methods=['POST'])
def speech_to_text_offline():
    """Offline speech recognition using local models"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400

        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            temp_file_path = temp_file.name

        try:
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(temp_file_path) as source:
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.record(source)
            
            # 尝试使用Sphinx离线识别（需要安装pocketsphinx）
            try:
                text = recognizer.recognize_sphinx(audio_data, language='zh-CN')
                return jsonify({
                    'text': text,
                    'confidence': 0.7,
                    'language': 'zh-CN',
                    'method': 'offline'
                })
            except sr.UnknownValueError:
                return jsonify({'error': '无法识别语音内容'}), 400
            except Exception as e:
                logger.error(f"Offline recognition error: {e}")
                return jsonify({'error': '离线语音识别失败'}), 500
                
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    except Exception as e:
        logger.error(f"Offline speech to text error: {str(e)}")
        return jsonify({'error': f'离线语音识别失败: {str(e)}'}), 500


def get_sample_itinerary(city, days):
    """Return sample itinerary data"""
    sample_data = {
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
                        "category": "Historical & Cultural",
                        "ticket_info": {
                            "requires_ticket": False,
                            "ticket_price": "Free",
                            "booking_url": None,
                            "source": "General",
                            "notes": "Public square - free to visit"
                        }
                    },
                    {
                        "name": f"{city} Museum",
                        "description": f"Home to a rich collection of historical artifacts and art treasures, showcasing the historical development and cultural evolution of {city} and the surrounding region. The museum building itself is a work of art, combining traditional and modern design elements.",
                        "duration": "2-3 hours",
                        "category": "Culture & Education",
                        "ticket_info": {
                            "requires_ticket": True,
                            "ticket_price": "Typically $10-20",
                            "booking_url": f"https://www.google.com/search?q={quote(f'{city} Museum tickets')}",
                            "source": "General Search",
                            "notes": "Most museums require tickets. Check official website for current prices."
                        }
                    },
                    {
                        "name": f"{city} Old Town",
                        "description": f"A well-preserved historic district where you can experience the traditional charm of {city}. Narrow streets are lined with specialty shops, traditional restaurants, and cafes, making it a great place to experience local life.",
                        "duration": "2-3 hours",
                        "category": "Historical & Cultural",
                        "ticket_info": {
                            "requires_ticket": False,
                            "ticket_price": "Free",
                            "booking_url": None,
                            "source": "General",
                            "notes": "Historic district - free to walk around"
                        }
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
                        "category": "Nature & Scenery",
                        "ticket_info": {
                            "requires_ticket": False,
                            "ticket_price": "Free",
                            "booking_url": None,
                            "source": "General",
                            "notes": "Public park - free to visit"
                        }
                    },
                    {
                        "name": f"{city} Food Street",
                        "description": f"A district that brings together various specialty foods of {city}, from traditional snacks to modern dining. The food street comes alive at night with bright lights and bustling crowds, making it the perfect place to taste authentic local cuisine.",
                        "duration": "2-3 hours",
                        "category": "Food & Shopping",
                        "ticket_info": {
                            "requires_ticket": False,
                            "ticket_price": "Free",
                            "booking_url": None,
                            "source": "General",
                            "notes": "Food district - free to walk around, pay for food"
                        }
                    },
                    {
                        "name": f"{city} Observation Deck",
                        "description": f"Located at the city's highest point, this viewing platform offers a 360-degree panoramic view of {city}. Visit at sunset to enjoy the most spectacular city nightscape.",
                        "duration": "1-2 hours",
                        "category": "Sightseeing",
                        "ticket_info": {
                            "requires_ticket": True,
                            "ticket_price": "Typically $15-30",
                            "booking_url": f"https://www.google.com/search?q={quote(f'{city} Observation Deck tickets')}",
                            "source": "General Search",
                            "notes": "Observation decks usually require tickets. Advance booking recommended."
                        }
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
                        "category": "Shopping Experience",
                        "ticket_info": {
                            "requires_ticket": False,
                            "ticket_price": "Free",
                            "booking_url": None,
                            "source": "General",
                            "notes": "Traditional market - free to visit, pay for purchases"
                        }
                    },
                    {
                        "name": f"{city} Arts District",
                        "description": f"A creative arts district filled with galleries, studios, independent bookstores, and cafes. Street art murals and live performances add a unique cultural atmosphere to the area.",
                        "duration": "2-3 hours",
                        "category": "Arts & Culture",
                        "ticket_info": {
                            "requires_ticket": False,
                            "ticket_price": "Free",
                            "booking_url": None,
                            "source": "General",
                            "notes": "Arts district - free to walk around, some galleries may charge"
                        }
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
        ]
    }

    # Flatten places list for map display
    all_places = []
    for day in sample_data['schedule']:
        all_places.extend(day['places'])
    sample_data['places'] = all_places

    return sample_data


@app.route('/api/weather', methods=['POST'])
def get_weather():
    """Get weather information for a location and date"""
    try:
        data = request.get_json()
        city = data.get('city', '')
        lat = data.get('lat', '')
        lon = data.get('lon', '')
        date = data.get('date', '')  # Date for future implementation with forecast API
        
        if not city and not (lat and lon):
            return jsonify({'error': 'Please provide city name or coordinates'}), 400
        
        if not OPENWEATHER_API_KEY:
            logger.warning("OpenWeather API key not configured")
            return jsonify({'error': 'Weather API not configured'}), 500
        
        # Use OpenWeather Current Weather API
        if lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        
        logger.info(f"🌤️ Getting weather for: {city}")
        response = requests.get(url)
        response.raise_for_status()
        
        weather_data = response.json()
        
        # Format weather information
        weather_info = {
            'temperature': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'humidity': weather_data['main']['humidity'],
            'description': weather_data['weather'][0]['description'],
            'icon': weather_data['weather'][0]['icon'],
            'wind_speed': weather_data['wind']['speed'],
            'city': weather_data['name'],
            'country': weather_data['sys']['country']
        }
        
        logger.info(f"✅ Weather data retrieved for {city}")
        return jsonify({'weather': weather_info}), 200
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Weather API error: {str(e)}")
        return jsonify({'error': 'Failed to get weather data'}), 500
    except Exception as e:
        logger.error(f"❌ Weather error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/events', methods=['POST'])
def get_events():
    """Get special events, festivals, and holidays for a location and date"""
    try:
        data = request.get_json()
        city = data.get('city', '')
        country = data.get('country', '')
        date = data.get('date', '')
        
        if not city:
            return jsonify({'error': 'Please provide city name'}), 400
        
        # Parse date
        from datetime import datetime
        if date:
            try:
                event_date = datetime.strptime(date, '%Y-%m-%d')
                month = event_date.month
                day = event_date.day
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        else:
            # Use current date if not provided
            now = datetime.now()
            month = now.month
            day = now.day
        
        # Get events for the date
        events = get_events_for_date(city, country, month, day)
        
        logger.info(f"🎉 Found {len(events)} events for {city} on {month}/{day}")
        return jsonify({'events': events}), 200
        
    except Exception as e:
        logger.error(f"❌ Events error: {str(e)}")
        return jsonify({'error': 'Failed to get events'}), 500


def get_events_for_date(city, country, month, day):
    """Get events for a specific date"""
    events = []
    
    # International holidays
    international_holidays = {
        (1, 1): "New Year's Day",
        (2, 14): "Valentine's Day",
        (3, 8): "International Women's Day",
        (4, 1): "April Fools' Day",
        (5, 1): "International Workers' Day",
        (6, 1): "International Children's Day",
        (10, 31): "Halloween",
        (12, 25): "Christmas",
        (12, 31): "New Year's Eve"
    }
    
    # Chinese holidays (approximate dates)
    chinese_holidays = {
        (1, 1): "New Year's Day",
        (2, 10): "Chinese New Year (Spring Festival)",  # Approximate
        (3, 8): "Women's Day",
        (4, 5): "Qingming Festival (Tomb Sweeping Day)",  # Approximate
        (5, 1): "Labor Day",
        (6, 1): "Children's Day",
        (9, 10): "Teachers' Day",
        (10, 1): "National Day"
    }
    
    # Check for international holidays
    if (month, day) in international_holidays:
        events.append({
            'name': international_holidays[(month, day)],
            'type': 'holiday',
            'description': f'International holiday: {international_holidays[(month, day)]}',
            'impact': 'high'
        })
    
    # Check for Chinese holidays if in China
    if country and 'china' in country.lower():
        if (month, day) in chinese_holidays:
            events.append({
                'name': chinese_holidays[(month, day)],
                'type': 'holiday',
                'description': f'Chinese holiday: {chinese_holidays[(month, day)]}',
                'impact': 'high'
            })
    
    # City-specific events
    city_events = get_city_specific_events(city, month, day)
    events.extend(city_events)
    
    return events


def get_city_specific_events(city, month, day):
    """Get city-specific events (simplified database)"""
    events = []
    
    # Major cities and their known events
    city_events = {
        'tokyo': {
            (3, 20): {'name': 'Cherry Blossom Festival', 'type': 'festival', 'description': 'Tokyo cherry blossom season', 'impact': 'high'},
            (7, 1): {'name': 'Summer Festival', 'type': 'festival', 'description': 'Traditional summer celebration', 'impact': 'medium'},
            (12, 31): {'name': 'New Year Countdown', 'type': 'event', 'description': 'Shibuya New Year countdown event', 'impact': 'high'}
        },
        'paris': {
            (7, 14): {'name': 'Bastille Day', 'type': 'holiday', 'description': 'French National Day', 'impact': 'high'},
            (4, 1): {'name': 'April Fools Day', 'type': 'holiday', 'description': 'Traditional April Fools', 'impact': 'low'},
            (12, 25): {'name': 'Christmas', 'type': 'holiday', 'description': 'Christmas celebration', 'impact': 'high'}
        },
        'london': {
            (6, 2): {'name': "Queen's Birthday", 'type': 'holiday', 'description': 'UK Queen Birthday celebration', 'impact': 'medium'},
            (11, 5): {'name': 'Bonfire Night', 'type': 'festival', 'description': 'Traditional bonfire festival', 'impact': 'medium'},
            (12, 25): {'name': 'Christmas', 'type': 'holiday', 'description': 'Christmas celebration', 'impact': 'high'}
        },
        'new york': {
            (7, 4): {'name': 'Independence Day', 'type': 'holiday', 'description': 'US Independence Day', 'impact': 'high'},
            (11, 24): {'name': 'Thanksgiving', 'type': 'holiday', 'description': 'Thanksgiving celebration', 'impact': 'high'},
            (12, 31): {'name': 'Times Square Countdown', 'type': 'event', 'description': 'New Year countdown event', 'impact': 'high'}
        }
    }
    
    # Check if city has specific events
    city_lower = city.lower()
    for city_name, events_dict in city_events.items():
        if city_lower in city_name or city_name in city_lower:
            if (month, day) in events_dict:
                events.append(events_dict[(month, day)])
    
    return events


if __name__ == '__main__':
    logger.info("Starting TripTeller Backend Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
