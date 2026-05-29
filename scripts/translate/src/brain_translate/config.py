from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel


class Config(BaseModel):
    openai_api_key: str = ""
    deepl_api_key: str = ""
    source_repo: Path
    state_base: Path
    provider: Literal["openai", "deepl", "chatgpt"] = "chatgpt"
    model: str = "gpt-4o"
    request_timeout: int = 120
    max_retries: int = 3

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
            deepl_api_key=os.environ.get("DEEPL_API_KEY", ""),
            source_repo=Path(
                os.environ.get(
                    "BRAIN_SOURCE_REPO",
                    str(Path.home() / "github" / "tamnd" / "brain"),
                )
            ),
            state_base=Path(
                os.environ.get(
                    "BRAIN_STATE_BASE",
                    str(Path.home() / "data" / "brain"),
                )
            ),
            provider=os.environ.get("BRAIN_TRANSLATE_PROVIDER", "chatgpt"),  # type: ignore[arg-type]
            model=os.environ.get("BRAIN_TRANSLATE_MODEL", "gpt-4o"),
        )

    def state_dir(self, lang: str) -> Path:
        return self.state_base / lang

    def repo_dir(self, lang: str) -> Path:
        return self.state_base / lang / "repo"

    def log_dir(self, lang: str) -> Path:
        return self.state_base / lang / "logs"

    def validate_provider(self) -> None:
        if self.provider == "openai" and not self.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY required for provider=openai")
        if self.provider == "deepl" and not self.deepl_api_key:
            raise RuntimeError("DEEPL_API_KEY required for provider=deepl")
        if self.provider == "chatgpt":
            chatgpt_bin = Path.home() / "bin" / "chatgpt-tool"
            if not chatgpt_bin.exists():
                raise RuntimeError(f"chatgpt-tool not found at {chatgpt_bin}")
