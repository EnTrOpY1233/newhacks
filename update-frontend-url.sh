#!/bin/bash

# Update frontend to use ngrok backend URL
# This script automatically updates the frontend .env file

echo "🔧 Updating frontend to use ngrok backend..."
echo "========================================"
echo ""

# Get backend URL from ngrok API
BACKEND_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o 'https://[^"]*' | grep -v 'api.ngrok.com' | grep '5000' | head -1)

if [ -z "$BACKEND_URL" ]; then
    echo "❌ Cannot get backend URL from ngrok"
    echo ""
    echo "Make sure ngrok is running:"
    echo "  ./start-ngrok.sh"
    echo ""
    exit 1
fi

echo "📡 Backend ngrok URL: $BACKEND_URL"
echo ""

# Update or create .env file
ENV_FILE="vue-project/.env"

if [ -f "$ENV_FILE" ]; then
    echo "📝 Updating existing $ENV_FILE..."
    # Backup original
    cp "$ENV_FILE" "${ENV_FILE}.backup"
    # Update VITE_API_URL
    if grep -q "VITE_API_URL" "$ENV_FILE"; then
        sed -i "s|VITE_API_URL=.*|VITE_API_URL=${BACKEND_URL}|" "$ENV_FILE"
    else
        echo "VITE_API_URL=${BACKEND_URL}" >> "$ENV_FILE"
    fi
else
    echo "📝 Creating new $ENV_FILE..."
    echo "VITE_API_URL=${BACKEND_URL}" > "$ENV_FILE"
    echo "VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here" >> "$ENV_FILE"
fi

echo "✅ Frontend configuration updated!"
echo ""
echo "Current configuration:"
cat "$ENV_FILE"
echo ""
echo "========================================"
echo ""
echo "⚠️  IMPORTANT: You must restart the frontend for changes to take effect"
echo ""
echo "1. Stop frontend (Ctrl+C in frontend terminal)"
echo "2. Restart: cd vue-project && npm run dev"
echo ""
echo "💡 TIP: The frontend will now connect to the ngrok backend URL"
echo "   This allows external users to access your app!"
echo ""


