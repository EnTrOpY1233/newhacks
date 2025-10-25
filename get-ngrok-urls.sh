#!/bin/bash

# Get ngrok tunnel URLs
# This script fetches the current ngrok public URLs

echo "🔍 Fetching ngrok tunnel URLs..."
echo "========================================"
echo ""

# Wait a moment for ngrok to start
sleep 2

# Get tunnels info from ngrok API
TUNNELS=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null)

if [ -z "$TUNNELS" ]; then
    echo "❌ Cannot connect to ngrok API"
    echo ""
    echo "Make sure ngrok is running:"
    echo "  ./start-ngrok.sh"
    echo ""
    exit 1
fi

# Parse and display URLs
echo "✅ Active ngrok tunnels:"
echo ""

# Extract frontend URL (port 5173)
FRONTEND_URL=$(echo "$TUNNELS" | grep -o 'https://[^"]*' | grep -v 'api.ngrok.com' | head -1)
if [ ! -z "$FRONTEND_URL" ]; then
    echo "🎨 Frontend URL:"
    echo "   $FRONTEND_URL"
    echo ""
fi

# Extract backend URL (port 5000)
BACKEND_URL=$(echo "$TUNNELS" | grep -o 'https://[^"]*' | grep -v 'api.ngrok.com' | tail -1)
if [ ! -z "$BACKEND_URL" ]; then
    echo "📡 Backend URL:"
    echo "   $BACKEND_URL"
    echo "   Health Check: ${BACKEND_URL}/api/health"
    echo ""
fi

echo "========================================"
echo ""
echo "📋 To update frontend to use ngrok backend:"
echo ""
echo "1. Stop the frontend (Ctrl+C)"
echo "2. Update vue-project/.env:"
echo "   VITE_API_URL=${BACKEND_URL}"
echo "3. Restart frontend: npm run dev"
echo ""
echo "Or use the helper script:"
echo "   ./update-frontend-url.sh"
echo ""
echo "========================================"
echo ""
echo "🌐 ngrok Web Interface:"
echo "   http://localhost:4040"
echo ""


