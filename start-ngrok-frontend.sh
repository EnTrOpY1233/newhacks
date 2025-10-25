#!/bin/bash

# Start ngrok with fixed domain for frontend
# Domain: tonisha-chiropodical-sharonda.ngrok-free.dev

echo "🌐 Starting ngrok with fixed domain"
echo "========================================"
echo ""
echo "Domain: tonisha-chiropodical-sharonda.ngrok-free.dev"
echo "Port: 5173 (Frontend)"
echo ""
echo "📡 Checking if frontend is running..."

if ! curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "⚠️  Frontend is not running on port 5173"
    echo ""
    echo "Please start frontend first:"
    echo "  cd vue-project && npm run dev"
    echo ""
    read -p "Press Enter to continue anyway, or Ctrl+C to cancel..."
fi

echo ""
echo "🚀 Starting ngrok tunnel..."
echo ""
echo "Your app will be available at:"
echo "  https://tonisha-chiropodical-sharonda.ngrok-free.dev"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

# Start ngrok with fixed domain
ngrok http --url=tonisha-chiropodical-sharonda.ngrok-free.dev 5173


