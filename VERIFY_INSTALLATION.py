#!/usr/bin/env python3
"""
Verification script for web search implementation.
Run this to ensure everything is installed and working.
"""

import sys
import os
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_check(status, message):
    symbol = "✅" if status else "❌"
    print(f"{symbol} {message}")

def check_requests_library():
    """Check if requests library is installed."""
    print_header("1. Checking requests library")
    try:
        import requests
        print_check(True, f"requests library installed: {requests.__version__}")
        return True
    except ImportError:
        print_check(False, "requests library NOT installed")
        print("   Run: pip install requests")
        return False

def check_groq_library():
    """Check if Groq SDK is installed."""
    print_header("2. Checking Groq SDK")
    try:
        import groq
        print_check(True, f"groq library installed")
        return True
    except ImportError:
        print_check(False, "groq library NOT installed")
        print("   Run: pip install groq")
        return False

def check_groq_api_key():
    """Check if GROQ_API_KEY is set."""
    print_header("3. Checking GROQ_API_KEY")
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        masked = api_key[:10] + "..." + api_key[-5:]
        print_check(True, f"GROQ_API_KEY is set: {masked}")
        return True
    else:
        print_check(False, "GROQ_API_KEY NOT set in environment")
        print("   Add to .env file or export as environment variable")
        return False

def check_problem_generator():
    """Check if problem_generator.py has web search code."""
    print_header("4. Checking problem_generator.py")

    problem_gen_path = Path("backend/src/problem_generator.py")
    if not problem_gen_path.exists():
        print_check(False, f"problem_generator.py not found at {problem_gen_path}")
        return False

    with open(problem_gen_path, 'r') as f:
        content = f.read()

    checks = [
        ("_search_case_studies" in content, "Contains _search_case_studies method"),
        ("_parse_duckduckgo_results" in content, "Contains _parse_duckduckgo_results method"),
        ("duckduckgo.com" in content, "Contains DuckDuckGo reference"),
        ("REQUESTS_AVAILABLE" in content, "Contains requests availability check"),
    ]

    all_passed = True
    for check, description in checks:
        print_check(check, description)
        if not check:
            all_passed = False

    return all_passed

def check_frontend_updates():
    """Check if frontend has been updated for case studies display."""
    print_header("5. Checking frontend updates")

    page_tsx = Path("frontend_new/src/app/page.tsx")
    if not page_tsx.exists():
        print_check(False, f"page.tsx not found at {page_tsx}")
        return False

    with open(page_tsx, 'r') as f:
        content = f.read()

    checks = [
        ("Data Analytics Case Studies" in content, "Updated case studies display"),
        ("research.sources.map" in content, "Renders research sources"),
        ("key_insights" in content, "Shows key insights from case studies"),
    ]

    all_passed = True
    for check, description in checks:
        print_check(check, description)
        if not check:
            all_passed = False

    return all_passed

def check_internet_connection():
    """Check if internet connection is available."""
    print_header("6. Checking internet connection")
    try:
        import requests
        response = requests.head("https://www.google.com", timeout=3)
        print_check(True, f"Internet connection available (status: {response.status_code})")
        return True
    except Exception as e:
        print_check(False, f"Internet connection failed: {e}")
        return False

def test_web_search():
    """Test actual web search functionality."""
    print_header("7. Testing web search functionality")

    try:
        import requests
        print("Attempting to search DuckDuckGo...")

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(
            "https://html.duckduckgo.com/",
            params={'q': 'data analytics case study'},
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print_check(True, "DuckDuckGo search request successful")
            if "result" in response.text.lower():
                print_check(True, "Web search returns valid results")
                return True
            else:
                print_check(False, "Web search returns empty results")
                return False
        else:
            print_check(False, f"DuckDuckGo returned status {response.status_code}")
            return False
    except Exception as e:
        print_check(False, f"Web search test failed: {e}")
        return False

def main():
    """Run all checks."""
    print("\n" + "="*60)
    print("  Web Search Implementation Verification")
    print("="*60)

    results = {
        "requests library": check_requests_library(),
        "groq library": check_groq_library(),
        "GROQ_API_KEY": check_groq_api_key(),
        "problem_generator.py": check_problem_generator(),
        "frontend updates": check_frontend_updates(),
        "internet connection": check_internet_connection(),
        "web search": test_web_search(),
    }

    # Summary
    print_header("Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, result in results.items():
        symbol = "✅" if result else "❌"
        print(f"{symbol} {name}")

    print(f"\n{passed}/{total} checks passed")

    if passed == total:
        print("\n✅ ALL CHECKS PASSED! Web search implementation is ready.")
        print("\nNext steps:")
        print("1. Start backend:   cd backend && python src/main.py")
        print("2. Start frontend:  cd frontend_new && npm run dev")
        print("3. Test at:         http://localhost:3000")
        return 0
    else:
        print(f"\n❌ {total - passed} checks failed. Please fix issues above.")
        print("\nCommon fixes:")
        print("• pip install requests")
        print("• pip install groq")
        print("• Set GROQ_API_KEY environment variable")
        print("• Check internet connection")
        return 1

if __name__ == "__main__":
    sys.exit(main())
