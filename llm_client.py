"""
EcoPantry AI - Course LLM Client (OpenAI SDK + HTTP Fallback)
Connects to the course proxy endpoint:
  Base URL: https://aiki-labs.up.railway.app/api/v1
  Model: gpt-6-luna
  Key: Course-provided key
"""
import json
import requests

COURSE_API_KEY = "sk-cal-4ab4d3034d58994974f50c4a19ff8ce240a2a4d538af5868"
COURSE_BASE_URL = "https://aiki-labs.up.railway.app/api/v1"
COURSE_MODEL = "gpt-6-luna"

def get_openai_client():
    """Attempts to load the OpenAI official client if installed."""
    try:
        from openai import OpenAI
        return OpenAI(
            api_key=COURSE_API_KEY,
            base_url=COURSE_BASE_URL
        )
    except ImportError:
        return None

def call_course_llm(messages: list, system_prompt: str = None, max_tokens: int = 400) -> str:
    """
    Sends chat completion request to the course endpoint.
    Uses openai SDK if available; otherwise falls back to direct REST API via requests.
    """
    # Prepare message list with system prompt
    formatted_messages = []
    if system_prompt:
        formatted_messages.append({"role": "system", "content": system_prompt})
    
    for m in messages:
        # Avoid duplicate consecutive roles if needed
        formatted_messages.append({"role": m["role"], "content": m["content"]})

    # Strategy 1: Use official OpenAI SDK if installed
    client = get_openai_client()
    if client is not None:
        try:
            response = client.chat.completions.create(
                model=COURSE_MODEL,
                messages=formatted_messages,
                max_completion_tokens=min(max_tokens, 800)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI SDK call failed: {str(e)}")

    # Strategy 2: Direct HTTP POST via requests (zero-dependency fallback)
    url = f"{COURSE_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {COURSE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": COURSE_MODEL,
        "messages": formatted_messages,
        "max_completion_tokens": min(max_tokens, 800)
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Direct REST API call to course endpoint failed: {str(e)}")
