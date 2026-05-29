from __future__ import annotations

import subprocess
from pathlib import Path

from .models import LANG_META
from .config import Config


class Publisher:
    def __init__(self, cfg: Config, lang: str):
        self.cfg = cfg
        self.lang = lang
        self.repo_dir = cfg.repo_dir(lang)
        meta = LANG_META[lang]
        self.github_repo = f"tamnd/{meta['repo']}"
        self.remote_url = f"git@github.com:{self.github_repo}.git"

    def _git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def ensure_repo(self) -> None:
        """Clone target repo if absent, otherwise pull latest."""
        if (self.repo_dir / ".git").exists():
            try:
                self._git("pull", "--rebase", "--autostash")
            except subprocess.CalledProcessError:
                pass  # diverged branches — let commit handle it
        else:
            self.repo_dir.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "clone", self.remote_url, str(self.repo_dir)],
                check=True,
            )

    def write_file(self, dest_rel: str, content: str) -> None:
        target = self.repo_dir / dest_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def commit_and_push(
        self,
        files: list[str],
        batch: int,
        source_sha: str,
        provider: str,
        model: str,
    ) -> bool:
        """Stage files, commit, push. Returns True if a commit was made."""
        if not files:
            return False

        try:
            self._git("add", "--", *files)
        except subprocess.CalledProcessError:
            # Fall back to add-all if explicit paths fail (path length issues)
            self._git("add", "--all")

        status = self._git("status", "--porcelain")
        if not status:
            return False

        n = len(files)
        msg = (
            f"translate: batch {batch:04d} ({n} file{'s' if n != 1 else ''})\n\n"
            f"Source: tamnd/brain@{source_sha[:12]}\n"
            f"Provider: {provider}\n"
            f"Model: {model}"
        )
        self._git("commit", "-m", msg)
        self._git("push", "origin", "HEAD")
        return True

    def source_sha(self, source_repo: Path) -> str:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=source_repo,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
