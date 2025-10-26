# 🚀 Quick Start Guide - Date & Weather Feature

## ⚡ 3-Minute Setup

### Step 1: Get OpenWeather API Key (2 minutes)

1. Go to: https://openweathermap.org/api
2. Click "Sign Up" → Create free account
3. Verify email → Get API key
4. Copy your API key

### Step 2: Configure Backend (30 seconds)

Open `backend/.env` and add:
```env
OPENWEATHER_API_KEY=paste_your_key_here
```

### Step 3: Start Services (30 seconds)

**Terminal 1 - Backend**:
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend**:
```bash
cd vue-project
npm run dev
```

## ✅ Test It!

1. Open browser: http://localhost:5173
2. Enter city: "Tokyo"
3. Select date: Tomorrow
4. Click "Search"
5. See weather ☀️ and events 🎉!

## 📋 API Key Summary

| Service | Required? | Cost | Link |
|---------|-----------|------|------|
| OpenWeather | **YES** for weather | **FREE** | [Get Key](https://openweathermap.org/api) |
| Google Maps | Already configured | Varies | - |
| Cerebras/Gemini | Already configured | Varies | - |

## 🎯 What You Get

✅ Real-time weather information  
✅ Temperature, humidity, wind speed  
✅ Special events and festivals  
✅ International & local holidays  
✅ Smart date-aware itineraries  
✅ Beautiful weather icons  

## 🆘 Quick Troubleshooting

**Weather not showing?**
- Check `.env` file has `OPENWEATHER_API_KEY`
- Restart backend server
- Check browser console (F12)

**Can't select date?**
- Refresh page
- Try different browser
- Check if date picker is visible

**Events not showing?**
- Events database is limited
- Try major cities (Tokyo, Paris, New York)
- Try known holiday dates (Dec 25, Jan 1)

## 📚 Full Documentation

See `DATE_WEATHER_FEATURE_GUIDE.md` for complete details!

---

**That's it! You're ready to go! 🎉**

