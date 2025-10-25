# TripTeller - Changelog

## Latest Update - UI/UX Improvements

### 1. Color Scheme Update
**Old:** Purple gradient (#667eea to #764ba2)
**New:** Clean blue theme (#3B82F6)

#### Changed Elements:
- Background: Light blue gradient (#f0f9ff to #e0f2fe)
- Primary buttons: Solid blue (#3B82F6)
- Hover states: Darker blue (#2563EB)
- Border accents: Blue theme throughout
- Day titles: Blue color
- Place cards: Blue left border

### 2. Removed All Emojis
**Changed:**
- Header: "TripTeller - AI Travel Guide" (removed ✈️)
- Search button: "Search" (removed 🔍)
- Loading: "Generating..." (removed ⏳)
- Itinerary header: "Travel Itinerary" (removed 📅)
- Play Audio: "Play Audio" (removed 🔊)
- Travel Tips: "Travel Tips" (removed 💡)
- Route Map: "Route Map" (removed 🗺️)
- Destination Poster: "Destination Poster" (removed 🎨)
- Audio Player: Title only (removed 🎧)

### 3. New Travel Options Feature

#### Travel Duration
Users can now select trip length:
- 1 Day
- 3 Days (default)
- 5 Days
- 7 Days

#### Travel Intensity
Users can choose their travel pace:
- **Relaxed**: 2-3 attractions/day, 3-4 hours per attraction, plenty of rest
- **Moderate**: 3-4 attractions/day, 2-3 hours per attraction, balanced pace (default)
- **Intensive**: 4-6 attractions/day, 1-2 hours per attraction, maximize sightseeing

### 4. Enhanced AI Prompts
Backend now customizes itineraries based on:
- Selected number of days
- Chosen intensity level
- Specific pacing recommendations
- Travel time considerations

### 5. UI Improvements
- Clean, modern blue color scheme
- Professional appearance without emojis
- Intuitive option selectors with active states
- Responsive design maintained
- Improved hover effects

## Technical Changes

### Frontend (Vue.js)
- `App.vue`: Updated colors, added options handling
- `CityInput.vue`: Added travel options UI, blue theme
- `ItineraryDisplay.vue`: Removed emojis, blue colors
- `MapView.vue`: Removed emoji from header
- `AudioPlayer.vue`: Removed emojis

### Backend (Flask)
- `app.py`: 
  - Added intensity parameter handling
  - Enhanced prompt with intensity-specific descriptions
  - Customized recommendations based on pace
  - Maintained backward compatibility

### User Flow
1. Enter city name
2. Select travel duration (1/3/5/7 days)
3. Choose intensity (Relaxed/Moderate/Intensive)
4. Click Search
5. Receive customized AI itinerary

## Benefits
- More professional appearance
- Customizable travel experience
- Better user control over trip planning
- AI generates appropriate content for each intensity level
- Cleaner, more accessible design





