"""
Google Gemini AI service client with fast response routing and fallback support.
"""

import os
from typing import Generator

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class GeminiService:
    """Manages Gemini client initialization, prompt routing, and streaming."""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key.strip() or os.environ.get("GEMINI_API_KEY", "")
        self._client = None
        if self.api_key and GEMINI_AVAILABLE:
            try:
                self._client = genai.Client(api_key=self.api_key)
            except Exception:
                self._client = None

    @property
    def is_connected(self) -> bool:
        return self._client is not None

    def ask(self, prompt: str, system: str = "", model: str = "gemini-2.5-flash") -> str:
        """
        Fast synchronous generation with automatic model fallback.
        """
        if not self.is_connected:
            return "⚠️ Please configure your Google Gemini API key to use AI features."

        models_to_try = [model, "gemini-2.5-flash", "gemini-4-hydrogen", "gemini-3.5-flash-lite"]
        last_error = None

        for m in models_to_try:
            try:
                kwargs = {
                    "model": m,
                    "input": prompt,
                    "store": False
                }
                if system:
                    kwargs["system_instruction"] = system
                response = self._client.interactions.create(**kwargs)
                return response.output_text or "(No output generated)"
            except Exception as e:
                last_error = e
                continue

        return f"❌ AI Generation Error: {last_error}"

    def ask_stream(self, prompt: str, system: str = "", model: str = "gemini-2.5-flash") -> Generator[str, None, None]:
        """
        High-speed streaming generator for live typing effect.
        """
        if not self.is_connected:
            yield "⚠️ Please configure your Google Gemini API key to use AI features."
            return

        models_to_try = [model, "gemini-2.5-flash", "gemini-3.5-flash-lite", "gemini-4-hydrogen"]
        full_prompt = f"System: {system}\n\nTask: {prompt}" if system else prompt

        for m in models_to_try:
            try:
                stream = self._client.models.generate_content_stream(
                    model=m,
                    contents=full_prompt
                )
                for chunk in stream:
                    if chunk.text:
                        yield chunk.text
                return
            except Exception:
                continue

        yield "❌ Error: Could not generate streaming response. Please verify your API key."
