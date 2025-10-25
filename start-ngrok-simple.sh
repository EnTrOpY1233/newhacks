#!/bin/bash

# Simple ngrok startup - one tunnel at a time
# Works with free ngrok accounts

echo "🌐 Starting ngrok tunnel for TripTeller"
echo "========================================"
echo ""

# Check authtoken
echo "🔑 Checking ngrok configuration..."
if ! ngrok config check &> /dev/null; then
    echo "⚠️  ngrok configuration issue detected"
    echo ""
    echo "Please visit: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "And verify your authtoken is correct"
    echo ""
fi

echo "ℹ️  Free ngrok accounts can run one tunnel at a time"
echo ""
echo "Choose which service to expose:"
echo "  1) Frontend only (port 5173)"
echo "  2) Backend only (port 5000)"
echo "  3) Try both (may fail on free account)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🎨 Starting frontend tunnel on port 5173..."
        echo "Press Ctrl+C to stop"
        echo "========================================"
        ngrok http 5173
        ;;
    2)
        echo ""
        echo "📡 Starting backend tunnel on port 5000..."
        echo "Press Ctrl+C to stop"
        echo "========================================"
        ngrok http 5000
        ;;
    3)
        echo ""
        echo "🚀 Attempting to start both tunnels..."
        echo "Press Ctrl+C to stop"
        echo "========================================"
        ngrok start --all --config=ngrok.yml
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac


