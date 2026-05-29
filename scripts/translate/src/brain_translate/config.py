from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel


class Config(BaseModel):
    source_repo: Path
    state_base: Path
    # chatgpt | google | bing | yandex | baidu | google_dt | any translators_pool name
    provider: str = "chatgpt"
    model: str = "gpt-4o"
    max_retries: int = 3

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
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
            provider=os.environ.get("BRAIN_TRANSLATE_PROVIDER", "chatgpt"),
            model=os.environ.get("BRAIN_TRANSLATE_MODEL", "gpt-4o"),
        )

    def state_dir(self, lang: str) -> Path:
        return self.state_base / lang

    def repo_dir(self, lang: str) -> Path:
        return self.state_base / lang / "repo"

    def log_dir(self, lang: str) -> Path:
        return self.state_base / lang / "logs"

    def validate_provider(self) -> None:
        if self.provider == "chatgpt":
            chatgpt_bin = Path.home() / "bin" / "chatgpt-tool"
            if not chatgpt_bin.exists():
                raise RuntimeError(f"chatgpt-tool not found at {chatgpt_bin}")
