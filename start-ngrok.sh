#!/bin/bash

# Start ngrok tunnels for TripTeller
# This creates public URLs for both frontend and backend

echo "🌐 Starting ngrok tunnels for TripTeller"
echo "========================================"
echo ""

# Check if services are running
echo "📡 Checking if services are running..."
if ! curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "⚠️  Backend is not running on port 5000"
    echo "   Please start backend first: cd backend && python app.py"
    echo ""
fi

if ! curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "⚠️  Frontend is not running on port 5173"
    echo "   Please start frontend first: cd vue-project && npm run dev"
    echo ""
fi

echo "🚀 Starting ngrok tunnels..."
echo ""
echo "This will create public URLs for:"
echo "  - Frontend (port 5173)"
echo "  - Backend (port 5000)"
echo ""
echo "Press Ctrl+C to stop tunnels"
echo "========================================"
echo ""

# Start ngrok with the config file
ngrok start --all --config=ngrok.yml


