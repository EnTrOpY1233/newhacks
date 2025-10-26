# TripTeller - AI Voice Tour Guide + Smart Travel Recommendations

An AI-powered smart travel planning application that generates travel itineraries, attraction recommendations, and provides voice narration simply by entering a city name.

![Theme](https://img.shields.io/badge/Theme-Travel%20%26%20Tourism-blue)
![Frontend](https://img.shields.io/badge/Frontend-Vue.js-green)
![Backend](https://img.shields.io/badge/Backend-Flask-lightgrey)
![AI](https://img.shields.io/badge/AI-Gemini-orange)

## Core Features

| Feature | Description |
|---------|-------------|
| **Smart City Input** | Google Place Picker autocomplete, intelligent location search (New) |
| **Location Confirmation** | Verify city existence, handle duplicate place names, confirm country/state (Latest) |
| **AI-Generated Routes** | Gemini AI automatically generates 1-7 day itineraries (JSON structure) |
| **Map Display** | Google Maps API shows attraction locations and routes |
| **Voice Narration** | ElevenLabs voice narration for attraction descriptions |
| **Image Generation** | Automatically generates "destination posters" (optional) |

## Project Highlights

- **Quick Demo**: Enter "Paris", get complete itinerary, map display, and voice narration in seconds
- **Modern UI**: Beautiful gradient design, responsive layout, excellent user experience
- **AI-Driven**: Fully powered by Gemini AI for intelligent itinerary planning
- **Smart Search**: Google Place Picker provides real-time location autocomplete (New)
- **Location Verification**: Automatically verify city existence, intelligently handle duplicate city names (e.g., Paris, France vs Paris, Texas) (Latest)
- **Multi-language Support**: Frontend supports multiple languages, easily extensible

## UI Preview

```
+------------------------------------------+
|  TripTeller - AI Tour Guide              |
|  Smart Recommendations · Voice · Routes  |
+------------------------------------------+
|  [Enter city name...]     [Search]       |
|  Popular: Tokyo Paris Toronto...        |
+------------------------------------------+
|  Itinerary        |    Map               |
|  Day 1            |    [Google Maps]     |
|  • Place 1 [Play] |                      |
|  • Place 2 [Play] |                      |
|  Day 2...         |                      |
+------------------------------------------+
```

## Tech Stack

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Fast frontend build tool
- **Google Maps API** - Map display

### Backend
- **Flask** - Python web framework
- **Gemini API** - Google's generative AI
- **ElevenLabs** - AI voice synthesis
- **CORS** - Cross-origin resource sharing

## Quick Start

### Prerequisites

- Node.js >= 20.19.0
- Python >= 3.8
- The following API keys:
  - Google Gemini API Key
  - Google Maps API Key
  - ElevenLabs API Key

### 1. Clone the Project

```bash
git clone <your-repo-url>
cd newhacks
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp env.example .env
# Edit the .env file and add your API keys

# Run backend server
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd vue-project

# Install dependencies
npm install

# Configure environment variables
cp env.example .env
# Edit the .env file and add your Google Maps API Key

# Run development server
npm run dev
```

The frontend will run on `http://localhost:5173`

### 4. Public Access (Optional - using ngrok)

If you need external users to access your application (remote demos, mobile device testing, etc.):

```bash
# Start ngrok in a new terminal
./start-ngrok.sh

# Get public URLs and update configuration in another terminal
./get-ngrok-urls.sh
./update-frontend-url.sh

# Restart frontend for changes to take effect
```

For detailed instructions, see [NGROK_SETUP.md](./NGROK_SETUP.md) or [Quick Start Guide](./NGROK_QUICK_START.md)

## Getting API Keys

### 1. Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in and create an API key
3. Copy the key to your backend `.env` file

### 2. Google Maps API
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable the following APIs:
   - Maps JavaScript API
   - Geocoding API
3. Create credentials and copy the API key
4. Paste into both frontend and backend `.env` files

### 3. ElevenLabs API
1. Visit [ElevenLabs](https://elevenlabs.io/)
2. Sign up for an account (free tier available)
3. Get your API key from settings
4. Copy to backend `.env` file

## Project Structure

```
newhacks/
├── backend/                 # Flask backend
│   ├── app.py              # Main application file
│   ├── requirements.txt    # Python dependencies
│   ├── env.example         # Environment variables example
│   └── README.md           # Backend documentation
│
├── vue-project/            # Vue frontend
│   ├── src/
│   │   ├── App.vue         # Main app component
│   │   ├── components/     # Vue components
│   │   │   ├── CityInput.vue        # City input
│   │   │   ├── ItineraryDisplay.vue # Itinerary display
│   │   │   ├── MapView.vue          # Map view
│   │   │   └── AudioPlayer.vue      # Audio player
│   │   └── main.js
│   ├── package.json
│   └── env.example         # Environment variables example
│
└── README.md               # Project documentation
```

## How to Use

1. **Enter City**: Type any city name in the search box (e.g., Tokyo, Paris, Toronto)
2. **Confirm Location**: After clicking search, the system verifies the location
   - If only one match is found, it's automatically confirmed
   - If multiple cities with the same name exist, select the correct country/state
3. **Generate Itinerary**: Choose travel duration (1/3/5/7 days) and intensity (relaxed/moderate/intensive)
4. **View Itinerary**: AI automatically generates a customized itinerary
5. **View Map**: The map on the right automatically marks all attraction locations
6. **Listen to Narration**: Click the "Play Narration" button for any attraction
7. **Enjoy Your Trip**: Use the AI-generated itinerary to plan your travel!

## Configuration Options

### Modify Trip Duration

Edit in `App.vue`:

```javascript
body: JSON.stringify({ city, days: 3 })  // Change to your desired number of days
```

### Customize Map Style

Modify the `styles` parameter in the `initMap` function in `MapView.vue`.

### Change Voice

Modify in the `generate_audio` function in `app.py`:

```python
voice="Bella"  # Options: Rachel, Domi, Bella, Antoni, etc.
```

## Troubleshooting

### Frontend Cannot Connect to Backend
- Check that the backend is running on `http://localhost:5000`
- Verify that `VITE_API_URL` in `.env` is configured correctly

### Map Not Displaying
- Confirm that the Google Maps API Key is properly configured
- Check that the APIs are enabled (Maps JavaScript API and Geocoding API)

### Voice Generation Failed
- Verify that the ElevenLabs API key is correct
- Ensure your account has sufficient free credits

### AI-Generated JSON Parsing Failed
- The backend will automatically fall back to sample data
- Check if the Gemini API key is valid

## Development Roadmap

- [ ] Add user account system
- [ ] Save and share itineraries
- [ ] Multi-language interface support
- [ ] Real-time weather integration
- [ ] Hotel and restaurant recommendations
- [ ] Mobile app version

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License
## Contributors


## Acknowledgments

- [Google Gemini](https://ai.google.dev/) - AI itinerary generation
- [ElevenLabs](https://elevenlabs.io/) - Voice synthesis
- [Google Maps](https://developers.google.com/maps) - Map services
- [Vue.js](https://vuejs.org/) - Frontend framework
- [Flask](https://flask.palletsprojects.com/) - Backend framework

---

**Built for NewHacks 2025 - Let AI be your personal travel advisor!**
