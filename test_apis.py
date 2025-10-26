#!/usr/bin/env python3
"""
API Test Script for TripTeller Backend
Tests all API endpoints to ensure they are working correctly
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"
TIMEOUT = 30  # seconds

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_test(name):
    print(f"{Colors.BOLD}Testing: {Colors.RESET}{name}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.RESET}")

def test_health_check():
    """Test the health check endpoint"""
    print_test("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print_success("Health check passed")
            print_info(f"AI Service: {data.get('ai_service', 'Unknown')}")
            print_info(f"Configured Services:")
            for key, value in data.items():
                if key != 'status' and key != 'ai_service' and isinstance(value, bool):
                    status = "✓" if value else "✗"
                    print_info(f"  {status} {key}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Is the backend running?")
        return False
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

def test_search_places():
    """Test the search places endpoint"""
    print_test("Search Places")
    try:
        test_cases = [
            {"query": "Paris"},
            {"query": "Tokyo"},
            {"query": "New York"},
        ]
        
        for case in test_cases:
            response = requests.post(
                f"{BASE_URL}/api/search-places",
                json=case,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                places = data.get('places', [])
                print_success(f"Search for '{case['query']}' returned {len(places)} result(s)")
                if places:
                    place = places[0]
                    print_info(f"  First result: {place.get('city', 'N/A')}, {place.get('country', 'N/A')}")
            else:
                print_error(f"Search failed for '{case['query']}': {response.status_code}")
                return False
        
        return True
    except Exception as e:
        print_error(f"Search places failed: {str(e)}")
        return False

def test_generate_itinerary():
    """Test the generate itinerary endpoint"""
    print_test("Generate Itinerary")
    try:
        test_data = {
            "city": "Tokyo",
            "days": 3,
            "intensity": "moderate",
            "preferences": ["historical", "food"],
            "location_context": {
                "state": "Tokyo",
                "country": "Japan",
                "country_code": "JP"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/generate-itinerary",
            json=test_data,
            timeout=60  # This might take longer
        )
        
        if response.status_code == 200:
            data = response.json()
            itinerary = data.get('itinerary', {})
            schedule = itinerary.get('schedule', [])
            print_success(f"Generated itinerary with {len(schedule)} days")
            if schedule:
                first_day = schedule[0]
                places = first_day.get('places', [])
                print_info(f"  Day 1 has {len(places)} attractions")
            return True
        else:
            print_error(f"Generate itinerary failed: {response.status_code}")
            print_error(f"Response: {response.text[:200]}")
            return False
    except Exception as e:
        print_error(f"Generate itinerary failed: {str(e)}")
        return False

def test_generate_audio():
    """Test the generate audio endpoint"""
    print_test("Generate Audio")
    try:
        test_data = {
            "text": "Welcome to Tokyo! Today we will explore the historic temples and enjoy delicious Japanese cuisine.",
            "voice": "rachel"  # Default voice
        }
        
        response = requests.post(
            f"{BASE_URL}/api/generate-audio",
            json=test_data,
            timeout=60  # This might take longer
        )
        
        if response.status_code == 200:
            data = response.json()
            filename = data.get('filename')
            print_success(f"Audio generated: {filename}")
            # Try to download the file
            download_response = requests.get(f"{BASE_URL}/api/audio/{filename}")
            if download_response.status_code == 200:
                print_success("Audio file is accessible")
            else:
                print_warning(f"Cannot download audio file: {download_response.status_code}")
            return True
        else:
            print_error(f"Generate audio failed: {response.status_code}")
            print_info("This might fail if ElevenLabs API is not configured")
            return False
    except Exception as e:
        print_error(f"Generate audio failed: {str(e)}")
        return False

def test_weather():
    """Test the weather endpoint"""
    print_test("Weather API")
    try:
        # Get tomorrow's date
        tomorrow = datetime.now() + timedelta(days=1)
        test_data = {
            "city": "Tokyo",
            "state": "Tokyo",
            "country": "Japan",
            "date": tomorrow.strftime("%Y-%m-%d")
        }
        
        response = requests.post(
            f"{BASE_URL}/api/weather",
            json=test_data,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            weather = data.get('weather')
            if weather:
                print_success(f"Weather data retrieved for {test_data['city']}")
                temp = weather.get('temperature', {}).get('day', 'N/A')
                print_info(f"  Temperature: {temp}°C")
            else:
                print_warning("No weather data returned")
            return True
        else:
            print_error(f"Weather API failed: {response.status_code}")
            print_info("This might fail if OpenWeather API is not configured")
            return False
    except Exception as e:
        print_error(f"Weather API failed: {str(e)}")
        return False

def test_events():
    """Test the events endpoint"""
    print_test("Events API")
    try:
        # Get next week's date
        next_week = datetime.now() + timedelta(days=7)
        test_data = {
            "city": "Tokyo",
            "country": "Japan",
            "date": next_week.strftime("%Y-%m-%d")
        }
        
        response = requests.post(
            f"{BASE_URL}/api/events",
            json=test_data,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print_success(f"Events API returned {len(events)} event(s)")
            if events:
                print_info(f"  First event: {events[0].get('title', 'N/A')}")
            return True
        else:
            print_error(f"Events API failed: {response.status_code}")
            print_info("This might fail if Eventbrite API is not configured")
            return False
    except Exception as e:
        print_error(f"Events API failed: {str(e)}")
        return False

def test_speech_to_text():
    """Test the speech-to-text endpoint"""
    print_test("Speech to Text")
    print_warning("Skipping - requires audio file upload")
    print_info("You can test this manually by recording audio and posting to /api/speech-to-text")
    return True

def run_all_tests():
    """Run all API tests"""
    print_header("TripTeller API Test Suite")
    print_info(f"Testing API at: {BASE_URL}\n")
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("Search Places", test_search_places()))
    results.append(("Generate Itinerary", test_generate_itinerary()))
    results.append(("Generate Audio", test_generate_audio()))
    results.append(("Weather API", test_weather()))
    results.append(("Events API", test_events()))
    results.append(("Speech to Text", test_speech_to_text()))
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if result else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"{status} - {test_name}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}All tests passed! 🎉{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}Some tests failed. Check the output above for details.{Colors.RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
