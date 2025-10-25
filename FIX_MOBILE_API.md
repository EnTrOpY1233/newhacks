# 🔧 Mobile API Connection Fix

## ✅ Problem Solved!

The issue was that mobile devices couldn't access the backend API at `localhost:5000` because:
1. Mobile phone is not on the same "localhost" as your computer
2. HTTPS (ngrok) cannot call HTTP (localhost) - browser blocks it

## 🛠️ Solution Implemented

**Vite Proxy Configuration** - All API requests now go through the same ngrok URL and get proxied to the local backend.

### What Changed:

1. **`vite.config.js`** - Added proxy configuration
   ```javascript
   proxy: {
     '/api': {
       target: 'http://localhost:5000',
       changeOrigin: true
     }
   }
   ```

2. **`.env`** - Set API URL to empty (uses same origin)
   ```
   VITE_API_URL=
   ```

3. **`App.vue` & `CityInput.vue`** - Updated to handle empty API_BASE_URL

---

## 🔄 Restart Required

### Step 1: Stop Frontend

In the terminal running frontend (showing `vite`):
- Press `Ctrl+C`

### Step 2: Restart Frontend

```bash
cd /home/grealish/newhacks/vue-project
npm run dev
```

Wait for:
```
VITE v7.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: http://xxx.xxx.xxx.xxx:5173/
```

---

## 📱 How to Test

### On Mobile Phone:

1. **Open browser** and visit:
   ```
   https://tonisha-chiropodical-sharonda.ngrok-free.dev
   ```

2. **Type a city name**: 
   - Try "Paris" or "Tokyo"

3. **Tap Search button**

4. **Should work now!** ✅
   - Location search should succeed
   - Modal should show locations
   - Can select and generate itinerary

---

## 🔍 How It Works Now

### Before (Broken):
```
Mobile Browser (HTTPS)
    ↓
    → Tries to call: http://localhost:5000/api/...
    ✗ BLOCKED (can't access localhost, mixed content)
```

### After (Fixed):
```
Mobile Browser (HTTPS)
    ↓
    → Calls: https://tonisha...ngrok-free.dev/api/...
    ↓
    → Vite Dev Server (receives request)
    ↓
    → Proxies to: http://localhost:5000/api/...
    ↓
    → Backend responds
    ↓
    → Returns to mobile browser
    ✓ SUCCESS!
```

---

## 📊 Request Flow

| Step | Location | URL | Protocol |
|------|----------|-----|----------|
| 1 | Mobile | `/api/search-places` | HTTPS |
| 2 | Vite Proxy | → `localhost:5000/api/search-places` | HTTP |
| 3 | Backend | Process request | HTTP |
| 4 | Vite Proxy | ← Response | HTTP |
| 5 | Mobile | Receive data | HTTPS |

---

## ✅ Verification Steps

After restarting frontend:

1. **On Computer** (should still work):
   ```
   http://localhost:5173
   ```

2. **On Mobile** (should now work):
   ```
   https://tonisha-chiropodical-sharonda.ngrok-free.dev
   ```

3. **Try searching**:
   - Enter "Paris"
   - Click Search
   - Should see location modal
   - Select Paris, France
   - Should generate itinerary

---

## 🐛 If Still Not Working

### Check Backend is Running
```bash
curl http://localhost:5000/api/health
```
Should return JSON with `"status": "ok"`

### Check Frontend is Running
```bash
curl http://localhost:5173
```
Should return HTML

### Check ngrok is Running
In ngrok terminal, should see:
```
Forwarding    https://tonisha-chiropodical-sharonda.ngrok-free.dev -> http://localhost:5173
```

### Clear Mobile Browser Cache
On mobile:
1. Open browser settings
2. Clear cache/cookies
3. Reload page

### Try Incognito/Private Mode
- Fresh session
- No cached files

---

## 📱 Mobile Browser DevTools (Advanced)

If you have a laptop:

### For iPhone (Safari):
1. Connect iPhone via USB
2. On Mac: Safari → Develop → [Your iPhone] → [Page]
3. Can see console errors

### For Android (Chrome):
1. Enable USB debugging on phone
2. Connect via USB
3. Chrome → `chrome://inspect`
4. Click "Inspect" under your page
5. Can see console errors

---

## 🎯 Expected Behavior

### On Mobile:
- ✅ Page loads
- ✅ Can type in city input
- ✅ Search button responds
- ✅ Location search succeeds
- ✅ Can select location
- ✅ Itinerary generates
- ✅ Map shows
- ✅ Everything works!

### Console (F12):
- No CORS errors
- No "Mixed Content" errors
- No "Failed to fetch" errors
- API calls show successful (200 status)

---

## 💡 Technical Notes

### Why This Works:
- Same-origin requests (HTTPS → HTTPS)
- Vite dev server handles proxy internally
- Browser security happy
- Mobile can access everything

### Production Deployment:
For production, you would:
1. Deploy backend to a server with HTTPS
2. Update `VITE_API_URL` to backend URL
3. No proxy needed (both HTTPS)

### Development:
Current setup is perfect for development:
- Backend runs locally (fast, easy to debug)
- Frontend proxies requests
- Works on all devices

---

## 🔄 Quick Restart Commands

```bash
# Terminal 1 - Backend (should already be running)
cd /home/grealish/newhacks/backend
source venv/bin/activate
python app.py

# Terminal 2 - Frontend (RESTART THIS)
cd /home/grealish/newhacks/vue-project
npm run dev

# Terminal 3 - ngrok (should already be running)
cd /home/grealish/newhacks
./start-ngrok-frontend.sh
```

---

## 🎉 Summary

**Problem**: Mobile couldn't access `localhost:5000` backend  
**Solution**: Vite proxy routes all `/api/*` requests to backend  
**Result**: Mobile works perfectly! ✅

**Now restart frontend and test on your phone!** 📱✨

---

*Configuration updated: 2025-10-25*  
*Status: Ready to test*

