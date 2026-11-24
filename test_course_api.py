"""
Quick standalone tester for the course OpenAI endpoint.
Run with: python test_course_api.py
"""
import sys
from llm_client import call_course_llm, COURSE_MODEL, COURSE_BASE_URL

print(f"Testing Course Endpoint: {COURSE_BASE_URL}")
print(f"Target Model: {COURSE_MODEL}\n")

test_messages = [
    {"role": "user", "content": "Hello from EcoPantry AI! Give me a 1-sentence cooking tip."}
]

try:
    response = call_course_llm(test_messages, max_tokens=100)
    print("✅ SUCCESS! Response from course endpoint:")
    print("-" * 50)
    print(response)
    print("-" * 50)
except Exception as e:
    print(f"❌ Connection Error: {e}")
    print("\nNote: Ensure your internet connection is active and railway.app is accessible.")
