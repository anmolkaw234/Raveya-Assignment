import json
from typing import Any

from openai import OpenAI

from app.core.config import get_settings


class AIClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.enabled = self.settings.ai_api_key not in {"", "replace_me"}
        self.client = None
        if self.enabled:
            self.client = OpenAI(api_key=self.settings.ai_api_key, base_url=self.settings.ai_base_url)

    def generate_json(self, *, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        if not self.enabled:
            raise RuntimeError("AI API key not configured. Add it in .env or Codespaces secrets.")

        completion = self.client.chat.completions.create(
            model=self.settings.ai_model,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = completion.choices[0].message.content
        return json.loads(content)
