#!/usr/bin/env python3
"""
Gemini API Key Test Script
Tests if a Gemini API key is valid and working
"""

import sys
import os

def test_gemini_key(api_key):
    """Test if the Gemini API key is valid"""
    
    print("=" * 60)
    print("Gemini API Key Test".center(60))
    print("=" * 60)
    print()
    
    # Check if API key is provided
    if not api_key:
        print("❌ Error: No API key provided")
        return False
    
    print(f"📝 Testing API Key: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # Try to import the required library
    try:
        from google import genai
        print("✓ google.genai library found")
    except ImportError:
        print("❌ Error: google-genai library not installed")
        print("   Install it with: pip install google-genai")
        return False
    
    print()
    print("-" * 60)
    print("Testing API Connection...")
    print("-" * 60)
    print()
    
    # Configure and test the API
    try:
        # Set API key as environment variable
        os.environ['GOOGLE_API_KEY'] = api_key
        
        # Create client
        client = genai.Client(api_key=api_key)
        print("✓ Client initialized")
        
        # Try to generate content
        print("✓ Model: gemini-2.0-flash-exp")
        print("\nSending test prompt: 'Explain how AI works in a few words'")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Explain how AI works in a few words",
        )
        
        # Check if we got a response
        if response and response.text:
            print(f"✓ Response received:\n  '{response.text.strip()}'")
            print()
            print("=" * 60)
            print("✅ SUCCESS: API Key is VALID and WORKING!".center(60))
            print("=" * 60)
            return True
        else:
            print("❌ Error: No response text received")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print()
        print("=" * 60)
        print("❌ FAILED: API Key is INVALID or NOT WORKING".center(60))
        print("=" * 60)
        
        # Provide helpful error messages
        error_str = str(e).lower()
        print("\nPossible reasons:")
        if "api key not valid" in error_str or "invalid" in error_str or "403" in error_str:
            print("  • The API key is invalid or expired")
            print("  • Get a new key at: https://aistudio.google.com/apikey")
        elif "quota" in error_str or "429" in error_str:
            print("  • API quota exceeded")
            print("  • Check your usage at: https://console.cloud.google.com/")
        elif "permission" in error_str or "404" in error_str:
            print("  • API key doesn't have required permissions")
            print("  • Enable Gemini API in Google Cloud Console")
        else:
            print("  • Network connection issue")
            print("  • API service temporarily unavailable")
        
        return False

def main():
    """Main function"""
    
    # The API key to test
    API_KEY = "AIzaSyCOl5CnAYAfLvBf2LlE9Sdi_LrThI6im-I"
    
    # Allow command line override
    if len(sys.argv) > 1:
        API_KEY = sys.argv[1]
    
    # Test the key
    success = test_gemini_key(API_KEY)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

