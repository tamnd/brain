"""Translation backends.

Free providers (no API keys required):
  chatgpt  — chatgpt-tool translate (browser-automated ChatGPT, AI quality)
  google   — translators package, Google Translate
  bing     — translators package, Microsoft Bing Translator
  yandex   — translators package, Yandex Translate
  baidu    — translators package, Baidu Fanyi (good for CJK)

Usage: set BRAIN_TRANSLATE_PROVIDER to any of the above.
"""
from __future__ import annotations

import re
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path

from tenacity import retry, stop_after_attempt, wait_exponential

from .config import Config

# ---------------------------------------------------------------------------
# Markdown protection
# ---------------------------------------------------------------------------

_PLACEHOLDER = "⟦PROTECT_{i}⟧"

_PROTECT_PATTERNS = [
    re.compile(r"```[\s\S]*?```", re.MULTILINE),
    re.compile(r"~~~[\s\S]*?~~~", re.MULTILINE),
    re.compile(r"\$\$[\s\S]*?\$\$", re.DOTALL),
    re.compile(r"\\\[[\s\S]*?\\\]", re.DOTALL),
    re.compile(r"(?<!\$)\$(?!\$)[^\$\n]+?\$(?!\$)"),
    re.compile(r"\\\([^\)]+\\\)"),
    re.compile(r"{{<[\s\S]*?>}}"),
    re.compile(r"`[^`\n]+`"),
]


def protect(text: str) -> tuple[str, dict[str, str]]:
    regions: dict[str, str] = {}
    n = 0
    for pat in _PROTECT_PATTERNS:
        def _sub(m: re.Match, _n: list[int] = [n]) -> str:
            key = _PLACEHOLDER.format(i=_n[0])
            regions[key] = m.group(0)
            _n[0] += 1
            return key
        text = pat.sub(_sub, text)
        n = len(regions)
    return text, regions


def restore(text: str, regions: dict[str, str]) -> str:
    for k, v in regions.items():
        text = text.replace(k, v)
    return text


# ---------------------------------------------------------------------------
# Front matter helpers (shared by all backends)
# ---------------------------------------------------------------------------

_TRANSLATABLE_FM: frozenset[str] = frozenset({"title", "description", "summary"})
_FM_RE = re.compile(r"\A---\s*\n([\s\S]*?)\n---\s*\n?")


def _split_frontmatter(raw: str) -> tuple[str, str]:
    m = _FM_RE.match(raw)
    return (m.group(0), raw[m.end():]) if m else ("", raw)


def _patch_fm(fm_block: str, field: str, new_val: str) -> str:
    return re.sub(
        rf"^({re.escape(field)}\s*:\s*)(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|[^\n]+)",
        lambda mo: f'{mo.group(1)}"{new_val}"',
        fm_block, count=1, flags=re.MULTILINE,
    )


def _extract_fm_fields(fm_block: str) -> dict[str, str]:
    inner = fm_block.strip().strip("-").strip()
    out: dict[str, str] = {}
    for field in _TRANSLATABLE_FM:
        m = re.search(
            rf"^{re.escape(field)}\s*:\s*(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|[^\n]+)",
            inner, re.MULTILINE,
        )
        if m:
            v = m.group(1).strip().strip("\"'")
            if v:
                out[field] = v
    return out


# ---------------------------------------------------------------------------
# Segment-based translation (MT backends)
# MT APIs translate any text, including placeholder words like "PROTECT".
# Solution: split protected text on placeholder tokens, translate only the
# plain-text segments, then reassemble — placeholders are never sent to the API.
# ---------------------------------------------------------------------------

_PLACEHOLDER_RE = re.compile(r"⟦PROTECT_\d+⟧")


def _translate_protected(
    protected_text: str,
    translate_fn: Callable[[str], str],
) -> str:
    """Translate text between ⟦PROTECT_N⟧ placeholders, leaving them intact."""

    parts: list[tuple[str, bool]] = []  # (content, is_placeholder)
    last = 0
    for m in _PLACEHOLDER_RE.finditer(protected_text):
        segment = protected_text[last : m.start()]
        if segment:
            parts.append((segment, False))
        parts.append((m.group(0), True))
        last = m.end()
    remainder = protected_text[last:]
    if remainder:
        parts.append((remainder, False))

    out: list[str] = []
    for content, is_ph in parts:
        if is_ph:
            out.append(content)
        elif content.strip():
            # Translate in chunks to respect API limits
            chunks = _chunk_paragraphs(content)
            translated_chunks: list[str] = []
            for chunk in chunks:
                if chunk.strip():
                    try:
                        translated_chunks.append(translate_fn(chunk))
                    except Exception:
                        translated_chunks.append(chunk)
                else:
                    translated_chunks.append(chunk)
            out.append("\n\n".join(translated_chunks))
        else:
            out.append(content)  # whitespace-only — keep as-is
    return "".join(out)


# ---------------------------------------------------------------------------
# Text chunking (MT APIs have ~5000-char limits)
# ---------------------------------------------------------------------------

_CHUNK_MAX = 4000


def _chunk_paragraphs(text: str) -> list[str]:
    """Split text into ≤ CHUNK_MAX chunks at paragraph boundaries."""
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        if current_len + len(para) + 2 > _CHUNK_MAX and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = len(para)
        else:
            current.append(para)
            current_len += len(para) + 2

    if current:
        chunks.append("\n\n".join(current))
    return chunks


# ---------------------------------------------------------------------------
# chatgpt-tool backend (free, AI quality)
# ---------------------------------------------------------------------------

_CHATGPT_TOOL_BIN = Path.home() / "bin" / "chatgpt-tool"


class ChatGPTToolBackend:
    """Calls chatgpt-tool translate FILE LANG --output OUT as a subprocess."""

    def translate_doc(self, raw: str, lang: str) -> tuple[str, int]:
        with tempfile.NamedTemporaryFile(
            suffix=".md", mode="w", encoding="utf-8", delete=False
        ) as src_f:
            src_f.write(raw)
            src_path = Path(src_f.name)

        out_path = src_path.with_suffix(f".{lang}.out.md")
        try:
            subprocess.run(
                [
                    str(_CHATGPT_TOOL_BIN), "translate",
                    str(src_path), lang,
                    "--output", str(out_path),
                    "--quiet",
                ],
                check=True,
                timeout=1200,
            )
            return out_path.read_text(encoding="utf-8"), 0
        finally:
            src_path.unlink(missing_ok=True)
            out_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# MT backend via `translators` package (google, bing, yandex, baidu, …)
# ---------------------------------------------------------------------------

# Language codes expected by translators package
_TS_LANG: dict[str, str] = {
    "vi": "vi",
    "zh_CN": "zh",
    "ja": "ja",
    "ko": "ko",
    "fr": "fr",
    "de": "de",
    "es": "es",
    "pt": "pt",
    "ru": "ru",
    "ar": "ar",
}


class MTBackend:
    """Free machine-translation via the `translators` package.

    provider: one of 'google', 'bing', 'yandex', 'baidu', or any name in
    translators.translators_pool.
    """

    def __init__(self, provider: str = "google"):
        self.provider = provider
        import translators as _ts
        self._ts = _ts

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=3, max=20))
    def _translate_chunk(self, chunk: str, to_lang: str) -> str:
        return self._ts.translate_text(  # type: ignore[no-any-return]
            chunk,
            translator=self.provider,
            to_language=to_lang,
            from_language="en",
        )

    def _translate_field(self, text: str, to_lang: str) -> str:
        return self._translate_chunk(text, to_lang)

    def translate_doc(self, raw: str, lang: str) -> tuple[str, int]:
        to_lang = _TS_LANG.get(lang, lang)
        fm_block, body = _split_frontmatter(raw)
        updated_fm = fm_block

        # Translate front matter fields
        if fm_block:
            for field, val in _extract_fm_fields(fm_block).items():
                try:
                    translated = self._translate_field(val, to_lang)
                    updated_fm = _patch_fm(updated_fm, field, translated)
                except Exception:
                    pass  # leave original if translation fails

        # Protect code/math, translate only the text segments between placeholders
        protected, regions = protect(body)
        translated_body = restore(
            _translate_protected(protected, lambda c: self._translate_chunk(c, to_lang)),
            regions,
        )
        return (updated_fm + translated_body).rstrip() + "\n", 0


# ---------------------------------------------------------------------------
# deep-translator backend (alternative Google interface, cleaner API)
# ---------------------------------------------------------------------------

# deep-translator language codes
_DT_LANG: dict[str, str] = {
    "vi": "vi",
    "zh_CN": "zh-CN",
    "ja": "ja",
    "ko": "ko",
    "fr": "fr",
    "de": "de",
    "es": "es",
    "pt": "pt",
    "ru": "ru",
    "ar": "ar",
}

# deep-translator chunk limit
_DT_CHUNK_MAX = 4500


class DeepTranslatorBackend:
    """deep-translator GoogleTranslator — simple, reliable free MT."""

    def __init__(self) -> None:
        from deep_translator import GoogleTranslator
        self._GoogleTranslator = GoogleTranslator

    def _make(self, to_lang: str) -> object:
        return self._GoogleTranslator(source="en", target=to_lang)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=3, max=20))
    def _translate_text(self, text: str, to_lang: str) -> str:
        translator = self._make(to_lang)
        result = translator.translate(text)  # type: ignore[union-attr]
        return result or text

    def translate_doc(self, raw: str, lang: str) -> tuple[str, int]:
        to_lang = _DT_LANG.get(lang, lang)
        fm_block, body = _split_frontmatter(raw)
        updated_fm = fm_block

        if fm_block:
            for field, val in _extract_fm_fields(fm_block).items():
                try:
                    updated_fm = _patch_fm(updated_fm, field, self._translate_text(val, to_lang))
                except Exception:
                    pass

        protected, regions = protect(body)
        translated_body = restore(
            _translate_protected(protected, lambda c: self._translate_text(c, to_lang)),
            regions,
        )
        return (updated_fm + translated_body).rstrip() + "\n", 0


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_MT_PROVIDERS = {"google", "bing", "yandex", "baidu", "reverso", "lingvanex"}


def make_backend(cfg: Config) -> "object":
    cfg.validate_provider()
    if cfg.provider == "chatgpt":
        return ChatGPTToolBackend()
    if cfg.provider == "google_dt":
        return DeepTranslatorBackend()
    if cfg.provider in _MT_PROVIDERS or cfg.provider in _get_ts_pool():
        return MTBackend(cfg.provider)
    raise ValueError(
        f"Unknown provider: {cfg.provider!r}. "
        f"Use: chatgpt, google, bing, yandex, baidu, google_dt, or any name in translators_pool."
    )


def _get_ts_pool() -> list[str]:
    try:
        import translators as ts
        return ts.translators_pool  # type: ignore[no-any-return]
    except Exception:
        return []
