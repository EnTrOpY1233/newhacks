# 📅🌤️ Date Selection & Weather/Events Feature Guide

## Overview

TripTeller now supports **optional travel start date selection** with automatic weather and special events information! This feature helps you plan your trip better by providing:

- 🌤️ **Real-time weather information** for your destination
- 🎉 **Special events, festivals, and holidays** happening during your travel dates
- 📅 **Smart date picker** with intuitive UI
- 🎯 **Date-aware itinerary planning** that considers weather and local events

---

## 🔑 Required API Keys

### OpenWeather API (Free)

**Purpose**: Get real-time weather information for any city worldwide

**How to get it**:
1. Visit [https://openweathermap.org/api](https://openweathermap.org/api)
2. Click "Sign Up" (top right)
3. Create a free account (no credit card required)
4. Verify your email
5. Go to "API keys" section
6. Copy your API key

**Free Tier Limits**:
- ✅ 60 calls/minute
- ✅ 1,000,000 calls/day
- ✅ Current weather data
- ✅ 5-day forecast (optional for future enhancement)

**Cost**: **100% FREE** for basic usage

---

## 🛠️ Setup Instructions

### Step 1: Add OpenWeather API Key

1. Open `backend/.env` file (create it if it doesn't exist)
2. Add your OpenWeather API key:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

**Example `.env` file**:
```env
CEREBRAS_API_KEY=your_cerebras_key
GEMINI_API_KEY=your_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key
GOOGLE_MAPS_API_KEY=your_maps_key
OPENWEATHER_API_KEY=your_openweather_key_here  # Add this line
```

### Step 2: Restart Backend

```bash
cd backend
python app.py
```

### Step 3: Start Frontend

```bash
cd vue-project
npm run dev
```

---

## 🎯 How to Use

### 1. **Select a City**
   - Enter a city name (e.g., "Tokyo", "Paris", "New York")
   - Confirm the location from the search results

### 2. **Choose Travel Start Date (Optional)**
   - Look for the date picker with 📅 icon
   - Click on the date input field
   - Select your travel start date from the calendar
   - The date must be today or in the future

### 3. **Configure Travel Options**
   - Select number of days (1-7)
   - Choose intensity level (Relaxed/Moderate/Intensive)
   - Add preferences (optional)

### 4. **Generate Itinerary**
   - Click "Search" button
   - Wait for the system to:
     - ✅ Fetch weather information
     - ✅ Check for special events/festivals
     - ✅ Generate personalized itinerary

### 5. **View Results**
   - **Weather Card**: Shows temperature, humidity, wind speed, weather description
   - **Events Card**: Lists festivals, holidays, and special events
   - **Itinerary**: Customized based on weather and events

---

## 📊 Features in Detail

### Weather Information

The weather card displays:
- **Temperature**: Current temperature in Celsius
- **Feels Like**: Perceived temperature
- **Humidity**: Air humidity percentage
- **Wind Speed**: Wind speed in m/s
- **Description**: Weather condition (e.g., "clear sky", "light rain")
- **Weather Icon**: Visual representation from OpenWeather

### Events & Festivals

The system checks for:

#### International Holidays
- New Year's Day (Jan 1)
- Valentine's Day (Feb 14)
- International Women's Day (Mar 8)
- April Fools' Day (Apr 1)
- International Workers' Day (May 1)
- International Children's Day (Jun 1)
- Halloween (Oct 31)
- Christmas (Dec 25)
- New Year's Eve (Dec 31)

#### Chinese Holidays
- Chinese New Year (Spring Festival)
- Qingming Festival
- Labor Day
- National Day
- And more...

#### City-Specific Events
- **Tokyo**: Cherry Blossom Festival, Summer Festival, New Year Countdown
- **Paris**: Bastille Day, Christmas celebrations
- **London**: Queen's Birthday, Bonfire Night
- **New York**: Independence Day, Thanksgiving, Times Square Countdown
- And more cities...

### Event Impact Levels

Events are categorized by their impact on travel:
- 🔴 **High Impact**: Major holidays/festivals - expect crowds, higher prices
- 🟡 **Medium Impact**: Moderate events - some areas may be busy
- 🟢 **Low Impact**: Minor events - minimal effect on travel

---

## 🎨 User Interface

### Date Picker Component
```
📅 Travel Start Date (Optional)
[Date Input Field]
Selected: October 26, 2025
```

### Weather Card
```
🌤️ Weather Information
┌─────────────────────────┐
│ [Weather Icon] 25°C     │
│ Clear sky               │
│                         │
│ Feels like: 23°C        │
│ Humidity: 65%           │
│ Wind: 3.5 m/s           │
└─────────────────────────┘
```

### Events Card
```
🎉 Special Events & Festivals
┌─────────────────────────────────┐
│ Cherry Blossom Festival         │
│ Festival · High Impact          │
│ Tokyo cherry blossom season     │
└─────────────────────────────────┘
```

---

## 🔧 Technical Implementation

### Backend API Endpoints

#### 1. `/api/weather` (POST)
**Request**:
```json
{
  "city": "Tokyo",
  "lat": 35.6762,
  "lon": 139.6503,
  "date": "2025-10-26"
}
```

**Response**:
```json
{
  "weather": {
    "temperature": 25.5,
    "feels_like": 23.8,
    "humidity": 65,
    "description": "clear sky",
    "icon": "01d",
    "wind_speed": 3.5,
    "city": "Tokyo",
    "country": "JP"
  }
}
```

#### 2. `/api/events` (POST)
**Request**:
```json
{
  "city": "Tokyo",
  "country": "Japan",
  "date": "2025-03-20"
}
```

**Response**:
```json
{
  "events": [
    {
      "name": "Cherry Blossom Festival",
      "type": "festival",
      "description": "Tokyo cherry blossom season",
      "impact": "high"
    }
  ]
}
```

### Frontend Components

1. **DatePicker.vue**: Date selection component
2. **WeatherInfo.vue**: Weather and events display
3. **CityInput.vue**: Integrated date picker
4. **App.vue**: Main application logic

---

## 🚀 Advanced Features

### Future Enhancements (Planned)

1. **Multi-day Weather Forecast**
   - Show weather for each day of the trip
   - Use OpenWeather 5-day forecast API

2. **More Event Sources**
   - Integrate with event APIs (Eventbrite, Ticketmaster)
   - Add more city-specific events
   - Include concerts, sports events, exhibitions

3. **Smart Recommendations**
   - Suggest indoor activities on rainy days
   - Recommend outdoor activities on sunny days
   - Adjust itinerary based on event crowds

4. **Weather Alerts**
   - Severe weather warnings
   - Travel advisories
   - Safety recommendations

---

## 🐛 Troubleshooting

### Weather Not Showing

**Problem**: Weather information doesn't appear

**Solutions**:
1. Check if OpenWeather API key is configured in `.env`
2. Verify the API key is valid at [openweathermap.org](https://openweathermap.org)
3. Check browser console for errors (F12)
4. Ensure backend is running and accessible

### Date Picker Not Working

**Problem**: Can't select a date

**Solutions**:
1. Check if date input is enabled
2. Verify minimum date is set correctly
3. Try refreshing the page
4. Check browser compatibility (use modern browser)

### Events Not Showing

**Problem**: No events displayed even on known festival dates

**Solutions**:
1. Check if the date matches known events
2. Verify city name is correct
3. Events database is limited - not all events are included
4. Check browser console for API errors

### API Rate Limits

**Problem**: "Too many requests" error

**Solutions**:
1. OpenWeather free tier: 60 calls/minute
2. Wait a minute before trying again
3. Consider upgrading to paid plan if needed
4. Implement caching on backend (future enhancement)

---

## 📝 Example Usage Scenarios

### Scenario 1: Cherry Blossom Season in Tokyo

1. Enter "Tokyo" as destination
2. Select date: March 20, 2025
3. Choose 3 days, moderate intensity
4. Result:
   - Weather: 15°C, partly cloudy
   - Event: Cherry Blossom Festival (High Impact)
   - Itinerary: Includes parks and outdoor viewing spots

### Scenario 2: Christmas in Paris

1. Enter "Paris" as destination
2. Select date: December 25, 2025
3. Choose 5 days, relaxed intensity
4. Result:
   - Weather: 5°C, light rain
   - Event: Christmas (High Impact)
   - Itinerary: Indoor attractions, museums, Christmas markets

### Scenario 3: Summer in New York

1. Enter "New York" as destination
2. Select date: July 4, 2025
3. Choose 4 days, intensive intensity
4. Result:
   - Weather: 28°C, sunny
   - Event: Independence Day (High Impact)
   - Itinerary: Outdoor activities, fireworks viewing, parks

---

## 🎓 Best Practices

### For Users

1. **Plan Ahead**: Select dates early to see weather patterns
2. **Check Events**: Look for festivals that interest you
3. **Be Flexible**: Weather can change, have backup plans
4. **Consider Impact**: High-impact events mean crowds and higher prices

### For Developers

1. **Cache Weather Data**: Reduce API calls by caching for 1 hour
2. **Error Handling**: Gracefully handle API failures
3. **User Feedback**: Show loading states and error messages
4. **Expand Events Database**: Add more cities and events regularly

---

## 📚 Additional Resources

### OpenWeather API Documentation
- [Current Weather API](https://openweathermap.org/current)
- [5 Day Forecast API](https://openweathermap.org/forecast5)
- [Weather Icons](https://openweathermap.org/weather-conditions)

### Event APIs (Future Integration)
- [Eventbrite API](https://www.eventbrite.com/platform/api)
- [Ticketmaster API](https://developer.ticketmaster.com/)
- [Predicthq Events API](https://www.predicthq.com/)

---

## ✅ Checklist

Before using the feature:
- [ ] OpenWeather API key added to `.env`
- [ ] Backend restarted
- [ ] Frontend running
- [ ] Browser console shows no errors
- [ ] Date picker visible in UI
- [ ] Can select future dates
- [ ] Weather card appears after search
- [ ] Events card shows relevant events

---

## 🎉 Success!

You now have a fully functional date-aware travel planning system with weather and events integration! 

**Enjoy planning your perfect trip! 🌍✈️**

---

*Last updated: October 26, 2025*
*Version: 1.0.0*

