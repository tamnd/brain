from __future__ import annotations

import json
from pathlib import Path

from .models import FileState, TranslationQueue, TranslationState, TranslatorConfig, utcnow


class StateManager:
    def __init__(
        self,
        state_dir: Path,
        lang: str,
        source_repo: Path,
        target_repo: Path,
        provider: str = "chatgpt",
        model: str = "gpt-4o",
    ):
        self.state_dir = state_dir
        self.lang = lang
        self._state_file = state_dir / "state.json"
        self._queue_file = state_dir / "queue.json"
        self._source_repo = str(source_repo)
        self._target_repo = str(target_repo)
        self._provider = provider
        self._model = model
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "logs").mkdir(exist_ok=True)

    # ── state ────────────────────────────────────────────────────────────────

    def load_state(self) -> TranslationState:
        if self._state_file.exists():
            return TranslationState.model_validate(
                json.loads(self._state_file.read_text())
            )
        return TranslationState(
            lang=self.lang,
            source_repo=self._source_repo,
            target_repo=self._target_repo,
            translator=TranslatorConfig(provider=self._provider, model=self._model),  # type: ignore[arg-type]
        )

    def save_state(self, state: TranslationState) -> None:
        self._state_file.write_text(state.model_dump_json(indent=2))

    # ── queue ─────────────────────────────────────────────────────────────────

    def load_queue(self) -> TranslationQueue:
        if self._queue_file.exists():
            return TranslationQueue.model_validate(
                json.loads(self._queue_file.read_text())
            )
        return TranslationQueue()

    def save_queue(self, queue: TranslationQueue) -> None:
        self._queue_file.write_text(queue.model_dump_json(indent=2))

    # ── helpers ───────────────────────────────────────────────────────────────

    def mark_done(
        self,
        state: TranslationState,
        source_path: str,
        source_hash: str,
        dest_path: str,
        tokens: int = 0,
        provider: str = "chatgpt",
    ) -> None:
        state.files[source_path] = FileState(
            source_hash=source_hash,
            translated_at=utcnow(),
            dest_path=dest_path,
            status="done",
            tokens_used=tokens,
            provider=provider,
        )
        state.last_run = utcnow()

    def mark_failed(
        self,
        state: TranslationState,
        source_path: str,
        source_hash: str,
        dest_path: str,
        provider: str = "chatgpt",
    ) -> None:
        state.files[source_path] = FileState(
            source_hash=source_hash,
            translated_at=utcnow(),
            dest_path=dest_path,
            status="failed",
            provider=provider,
        )
