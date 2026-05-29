from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

SUPPORTED_LANGS: frozenset[str] = frozenset({"vi", "zh_CN", "ja"})

LANG_META: dict[str, dict[str, str]] = {
    "vi": {
        "name": "Vietnamese",
        "label": "Tiếng Việt",
        "locale": "vi",
        "title": "brain (Tiếng Việt)",
        "description": "Ghi chú cá nhân của tamnd",
        "repo": "brain-vi",
        "cf_project": "brain-vi",
        "base_url": "https://brain-vi.tamnd.com/",
        "github_module": "github.com/tamnd/brain-vi",
    },
    "zh_CN": {
        "name": "Simplified Chinese",
        "label": "中文",
        "locale": "zh-CN",
        "title": "brain (中文)",
        "description": "tamnd 的个人知识库",
        "repo": "brain-zh-cn",
        "cf_project": "brain-zh-cn",
        "base_url": "https://brain-zh-cn.tamnd.com/",
        "github_module": "github.com/tamnd/brain-zh-cn",
    },
    "ja": {
        "name": "Japanese",
        "label": "日本語",
        "locale": "ja",
        "title": "brain (日本語)",
        "description": "tamnd の個人知識ベース",
        "repo": "brain-ja",
        "cf_project": "brain-ja",
        "base_url": "https://brain-ja.tamnd.com/",
        "github_module": "github.com/tamnd/brain-ja",
    },
}


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TranslatorConfig(BaseModel):
    provider: Literal["openai", "deepl"] = "openai"
    model: str = "gpt-4o"


class FileState(BaseModel):
    source_hash: str
    translated_at: datetime
    dest_path: str
    status: Literal["done", "failed"] = "done"
    tokens_used: int = 0
    provider: str = "openai"


class TranslationState(BaseModel):
    schema_version: int = 1
    lang: str
    source_repo: str
    target_repo: str
    last_run: datetime | None = None
    batch: int = 0
    translator: TranslatorConfig = Field(default_factory=TranslatorConfig)
    files: dict[str, FileState] = Field(default_factory=dict)


class QueueItem(BaseModel):
    source_path: str
    priority: int = 0
    added_at: datetime = Field(default_factory=utcnow)
    retries: int = 0


class TranslationQueue(BaseModel):
    pending: list[QueueItem] = Field(default_factory=list)
    failed: list[QueueItem] = Field(default_factory=list)
