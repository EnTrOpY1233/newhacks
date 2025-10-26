# Testing Place Confirmation Feature

## Prerequisites

1. **Backend running** on `http://localhost:5000`
2. **Frontend running** on `http://localhost:5173`
3. **Google Maps API key** configured in both backend and frontend `.env` files

## Automated Backend Testing

Run the automated test script:

```bash
cd /home/grealish/newhacks
python3 test_place_confirmation.py
```

This will test:
- Unique city names (Tokyo)
- Duplicate city names (Paris, Springfield)
- Special characters (São Paulo)
- Non-existent locations (Atlantis)
- City with state specification (Portland, Oregon)

## Manual Frontend Testing

### Test Case 1: Unique City Name (Auto-confirm)

**Steps:**
1. Open browser to `http://localhost:5173`
2. Type "Tokyo" in the search box
3. Click "Search" button

**Expected Result:**
- No confirmation modal appears
- Location confirmed banner shows: "✓ Location confirmed: Tokyo, Japan"
- Itinerary generation starts immediately
- Map displays Tokyo attractions

---

### Test Case 2: Duplicate City Names (Manual selection)

**Steps:**
1. Clear previous search
2. Type "Paris" in the search box
3. Click "Search" button

**Expected Result:**
- Confirmation modal appears with title "Confirm Location"
- Modal shows at least 2 options:
  - Paris, Île-de-France, France (FR)
  - Paris, Texas, United States (US)
- Each option shows:
  - City name (bold)
  - State (if applicable)
  - Country name
  - Country code badge (green)
  - Full formatted address
- Hover over options shows green highlight
- Click on "Paris, France" option

**Expected After Selection:**
- Modal closes
- Location confirmed banner shows: "✓ Location confirmed: Paris, Île-de-France, France"
- Itinerary generation starts for Paris, France
- Map shows French attractions

---

### Test Case 3: Multiple Same-Named Cities

**Steps:**
1. Clear previous search
2. Type "Springfield" in the search box
3. Click "Search" button

**Expected Result:**
- Confirmation modal appears
- Shows multiple Springfield options from different US states:
  - Springfield, Illinois, United States
  - Springfield, Massachusetts, United States
  - Springfield, Missouri, United States
  - etc.
- Each clearly labeled with state
- Can select desired Springfield

---

### Test Case 4: Non-existent Location

**Steps:**
1. Clear previous search
2. Type "Atlantis" in the search box
3. Click "Search" button

**Expected Result:**
- Confirmation modal appears
- Shows "No locations found for 'Atlantis'"
- Displays hint: "Please try a different search term"
- Cancel button available to close modal
- No itinerary generation

---

### Test Case 5: Popular Cities Quick Select

**Steps:**
1. Click on "Tokyo" from Popular Cities buttons
2. Input field fills with "Tokyo"
3. Click "Search" button

**Expected Result:**
- Same as Test Case 1
- Auto-confirms and generates itinerary

---

### Test Case 6: Search During Loading

**Steps:**
1. Type "London" and click Search
2. While "Searching..." is displayed, try to click Search again

**Expected Result:**
- Search button is disabled during search
- Input field is disabled
- Button text shows "Searching..."
- Cannot trigger duplicate searches

---

### Test Case 7: Modal Interaction

**Steps:**
1. Search for "Paris"
2. Modal appears with options
3. Click outside the modal (on the dark overlay)

**Expected Result:**
- Modal closes
- No location confirmed
- No itinerary generated
- Can search again

**Alternative:**
1. Search for "Paris"
2. Modal appears
3. Click the "×" close button in top-right

**Expected Result:**
- Same as clicking outside
- Modal closes gracefully

---

### Test Case 8: City with Special Characters

**Steps:**
1. Type "São Paulo" in search box
2. Click "Search" button

**Expected Result:**
- Successfully finds São Paulo, Brazil
- Handles special characters correctly
- Auto-confirms (if single result)
- Generates itinerary for São Paulo

---

### Test Case 9: State-Specific Search

**Steps:**
1. Type "Portland, Oregon"
2. Click "Search" button

**Expected Result:**
- Finds Portland in Oregon specifically
- Shows in results with state clearly marked
- Auto-confirms if specific enough
- Generates Oregon-specific itinerary

---

### Test Case 10: Network Error Handling

**Steps:**
1. Stop the backend server
2. Type "Tokyo" and click Search

**Expected Result:**
- Shows "Searching..." briefly
- Confirmation modal appears with error message
- Error is displayed in red box
- Helpful error message shown
- Can close modal and retry after restarting backend

---

## Visual Checks

### Modal Design
- ✅ Clean white background
- ✅ Rounded corners (12px)
- ✅ Shadow effect for depth
- ✅ Proper spacing and padding
- ✅ Responsive on mobile devices

### Place Items
- ✅ Clear visual separation between items
- ✅ Hover effect (green border, light green background)
- ✅ Smooth transition on hover
- ✅ Country code badge in green
- ✅ City name is bold and prominent

### Confirmed Location Banner
- ✅ Light green background
- ✅ Green checkmark icon in circle
- ✅ Clear text showing city, state (if any), country
- ✅ Positioned below search area, above itinerary

---

## Performance Checks

### Response Time
- Place search should complete in < 2 seconds
- Modal should appear immediately
- No UI lag or freezing

### API Calls
Open browser DevTools (F12) → Network tab:
- ✅ Single `/api/search-places` call per search
- ✅ No duplicate or unnecessary calls
- ✅ Proper error handling for failed requests

---

## Accessibility Checks

### Keyboard Navigation
1. Tab through interface
2. Can focus on input field
3. Can activate search with Enter key
4. Can close modal with Escape key (optional enhancement)

### Screen Readers
- Input has proper placeholder text
- Buttons have descriptive labels
- Error messages are clear and readable

---

## Browser Compatibility

Test on:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari (if available)

Test on mobile:
- ✅ iOS Safari
- ✅ Android Chrome

---

## Common Issues & Solutions

### Issue: Modal doesn't appear
**Solution:** 
- Check browser console for errors
- Verify backend is running
- Check Google Maps API key is configured

### Issue: No results for valid city
**Solution:**
- Check backend logs
- Verify Google Maps API key has Geocoding API enabled
- Check API quota hasn't been exceeded

### Issue: Wrong location selected
**Solution:**
- Feature is working as designed
- Use more specific search (include state/country)
- Select correct option from modal list

### Issue: Modal stuck on screen
**Solution:**
- Click Cancel button
- Click outside modal
- Refresh page if needed

---

## Success Criteria

All of the following should work:
- ✅ Backend endpoint responds correctly
- ✅ Frontend displays modal properly
- ✅ Can search and confirm locations
- ✅ Single results auto-confirm
- ✅ Multiple results show selection UI
- ✅ No results show helpful message
- ✅ Confirmed location displays banner
- ✅ Itinerary generation uses confirmed location
- ✅ All error cases handled gracefully
- ✅ UI is responsive and accessible

---

## Notes

- All code and comments are in English
- Feature uses Google Geocoding API
- Requires valid API key to function
- Free tier has daily quota limits
- Results are not cached (future enhancement)

