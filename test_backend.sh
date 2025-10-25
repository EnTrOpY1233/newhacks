#!/bin/bash

echo "🧪 Testing TripTeller Backend..."
echo "================================"

# Test health endpoint
echo ""
echo "1️⃣ Testing /api/health..."
curl -s http://localhost:5000/api/health | python3 -m json.tool

# Test itinerary generation
echo ""
echo ""
echo "2️⃣ Testing /api/generate-itinerary for Paris..."
curl -s -X POST http://localhost:5000/api/generate-itinerary \
  -H "Content-Type: application/json" \
  -d '{"city": "Paris", "days": 3}' | python3 -m json.tool | head -50

echo ""
echo "================================"
echo "✅ Backend test complete!"

