#!/usr/bin/env python3
"""
Test script for place confirmation feature
Tests the /api/search-places endpoint with various city names
"""

import requests
import json
import sys

# Configuration
API_BASE_URL = "http://localhost:5000"
SEARCH_ENDPOINT = f"{API_BASE_URL}/api/search-places"

# Test cases
TEST_CASES = [
    {
        "name": "Unique city - Tokyo",
        "query": "Tokyo",
        "expected_min_results": 1,
        "expected_country": "Japan"
    },
    {
        "name": "Duplicate city names - Paris",
        "query": "Paris",
        "expected_min_results": 2,
        "expected_countries": ["France", "United States"]
    },
    {
        "name": "Multiple Springfield cities",
        "query": "Springfield",
        "expected_min_results": 3,
        "expected_country": "United States"
    },
    {
        "name": "City with special characters - São Paulo",
        "query": "São Paulo",
        "expected_min_results": 1,
        "expected_country": "Brazil"
    },
    {
        "name": "Non-existent city - Atlantis",
        "query": "Atlantis",
        "expected_results": 0
    },
    {
        "name": "City with state - Portland, Oregon",
        "query": "Portland, Oregon",
        "expected_min_results": 1,
        "expected_state": "Oregon"
    }
]


def print_separator():
    """Print a visual separator"""
    print("\n" + "=" * 80 + "\n")


def test_search_places(test_case):
    """
    Test the search-places endpoint with a specific query
    
    Args:
        test_case: Dictionary containing test case details
    
    Returns:
        bool: True if test passed, False otherwise
    """
    print(f"Test: {test_case['name']}")
    print(f"Query: '{test_case['query']}'")
    
    try:
        # Make API request
        response = requests.post(
            SEARCH_ENDPOINT,
            json={"query": test_case["query"]},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Check response status
        if response.status_code != 200:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        # Parse response
        data = response.json()
        places = data.get("places", [])
        num_results = len(places)
        
        print(f"✓ Found {num_results} place(s)")
        
        # Display results
        for i, place in enumerate(places, 1):
            city = place.get("city", "Unknown")
            state = place.get("state", "")
            country = place.get("country", "Unknown")
            country_code = place.get("country_code", "??")
            
            location_parts = [city]
            if state:
                location_parts.append(state)
            location_parts.append(country)
            
            print(f"  {i}. {', '.join(location_parts)} ({country_code})")
            print(f"     Address: {place.get('formatted_address', 'N/A')}")
        
        # Validate results
        if "expected_results" in test_case:
            # Exact match expected
            if num_results != test_case["expected_results"]:
                print(f"❌ FAILED: Expected {test_case['expected_results']} results, got {num_results}")
                return False
        
        if "expected_min_results" in test_case:
            # Minimum results expected
            if num_results < test_case["expected_min_results"]:
                print(f"❌ FAILED: Expected at least {test_case['expected_min_results']} results, got {num_results}")
                return False
        
        if "expected_country" in test_case and num_results > 0:
            # Check if expected country is in results
            countries = [p.get("country") for p in places]
            if test_case["expected_country"] not in countries:
                print(f"❌ FAILED: Expected country '{test_case['expected_country']}' not found")
                return False
        
        if "expected_countries" in test_case:
            # Check if all expected countries are present
            countries = [p.get("country") for p in places]
            for expected_country in test_case["expected_countries"]:
                if expected_country not in countries:
                    print(f"❌ FAILED: Expected country '{expected_country}' not found")
                    return False
        
        if "expected_state" in test_case and num_results > 0:
            # Check if expected state is in results
            states = [p.get("state") for p in places if p.get("state")]
            if test_case["expected_state"] not in states:
                print(f"❌ FAILED: Expected state '{test_case['expected_state']}' not found")
                return False
        
        print("✅ PASSED")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ FAILED: Cannot connect to backend server")
        print("Make sure the backend is running on http://localhost:5000")
        return False
    except requests.exceptions.Timeout:
        print("❌ FAILED: Request timed out")
        return False
    except Exception as e:
        print(f"❌ FAILED: {type(e).__name__}: {str(e)}")
        return False


def main():
    """Run all test cases"""
    print("🧪 Testing Place Confirmation Feature")
    print("=" * 80)
    
    # Check if backend is running
    try:
        health_response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✓ Backend is running")
            print(f"  AI Service: {health_data.get('ai_service', 'unknown')}")
            print(f"  Google Maps configured: {health_data.get('maps_configured', False)}")
            
            if not health_data.get('maps_configured'):
                print("\n⚠️  WARNING: Google Maps API is not configured!")
                print("Place search will not work without a valid Google Maps API key")
                print("Please configure GOOGLE_MAPS_API_KEY in backend/.env")
                return 1
        else:
            print(f"❌ Backend health check failed: HTTP {health_response.status_code}")
            return 1
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running!")
        print("Please start the backend server first:")
        print("  cd backend && python app.py")
        return 1
    
    print_separator()
    
    # Run test cases
    passed = 0
    failed = 0
    
    for test_case in TEST_CASES:
        result = test_search_places(test_case)
        if result:
            passed += 1
        else:
            failed += 1
        print_separator()
    
    # Summary
    total = passed + failed
    print(f"Test Summary:")
    print(f"  Total: {total}")
    print(f"  ✅ Passed: {passed}")
    print(f"  ❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

