"""Translation backends: chatgpt-tool (free), OpenAI API, DeepL."""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path
from typing import Protocol

from tenacity import retry, stop_after_attempt, wait_exponential

from .config import Config


# ---------------------------------------------------------------------------
# Markdown protection (shared logic — keeps code/math intact)
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
# Provider protocol
# ---------------------------------------------------------------------------

class TranslatorBackend(Protocol):
    def translate_doc(self, raw: str, lang: str) -> tuple[str, int]:
        """Return (translated_markdown, tokens_used)."""
        ...


# ---------------------------------------------------------------------------
# chatgpt-tool backend (free, browser-automated ChatGPT)
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

        out_path = src_path.with_suffix(f".{lang}.md")
        try:
            subprocess.run(
                [
                    str(_CHATGPT_TOOL_BIN),
                    "translate",
                    str(src_path),
                    lang,
                    "--output", str(out_path),
                    "--quiet",
                ],
                check=True,
                timeout=1200,
            )
            translated = out_path.read_text(encoding="utf-8")
            return translated, 0
        finally:
            src_path.unlink(missing_ok=True)
            out_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# OpenAI API backend
# ---------------------------------------------------------------------------

_LANG_NAMES = {
    "vi": "Vietnamese",
    "zh_CN": "Simplified Chinese",
    "ja": "Japanese",
}

_FM_TRANSLATABLE = frozenset({"title", "description", "summary"})
_FM_RE = re.compile(r"\A---\s*\n([\s\S]*?)\n---\s*\n?")

_SYSTEM = """\
You are a professional technical translator specializing in mathematics, computer science, \
and programming documentation. Translate from English to {lang_name}.

RULES:
- Output ONLY the translated document. No preamble or closing remarks.
- Preserve every ⟦PROTECT_N⟧ placeholder character-for-character.
- Preserve all Markdown formatting and blank lines exactly.
- Keep proper nouns, code identifiers, and URLs unchanged.
- Technical terms with standard {lang_name} equivalents: use the standard form.\
"""


class OpenAIBackend:
    def __init__(self, cfg: Config):
        from openai import OpenAI

        self._client = OpenAI(api_key=cfg.openai_api_key, timeout=cfg.request_timeout)
        self._model = cfg.model

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
    def _call(self, system: str, user: str) -> tuple[str, int]:
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.1,
        )
        text = resp.choices[0].message.content or ""
        tokens = resp.usage.total_tokens if resp.usage else 0
        return text, tokens

    def translate_doc(self, raw: str, lang: str) -> tuple[str, int]:
        lang_name = _LANG_NAMES.get(lang, lang)
        system = _SYSTEM.format(lang_name=lang_name)
        total = 0

        # Translate front matter fields
        m = _FM_RE.match(raw)
        fm_block = m.group(0) if m else ""
        body = raw[m.end():] if m else raw
        updated_fm = fm_block

        if fm_block:
            inner = fm_block.strip().lstrip("-").rstrip("-").strip()
            fields: dict[str, str] = {}
            for field in _FM_TRANSLATABLE:
                fm = re.search(
                    rf"^{re.escape(field)}\s*:\s*"
                    rf"(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|[^\n]+)",
                    inner, re.MULTILINE,
                )
                if fm:
                    v = fm.group(1).strip().strip('"\'')
                    if v:
                        fields[field] = v

            if fields:
                block = "\n".join(f"{k}: {v}" for k, v in fields.items())
                translated_fields, t = self._call(
                    f"Translate each value to {lang_name}. Output ONLY key: value lines.",
                    block,
                )
                total += t
                for line in translated_fields.strip().splitlines():
                    mm = re.match(r"^(\w+)\s*:\s*(.+)", line.strip())
                    if mm and mm.group(1) in _FM_TRANSLATABLE:
                        updated_fm = re.sub(
                            rf"^({re.escape(mm.group(1))}\s*:\s*)"
                            rf"(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|[^\n]+)",
                            lambda mo, tv=mm.group(2).strip(): f'{mo.group(1)}"{tv}"',
                            updated_fm, count=1, flags=re.MULTILINE,
                        )

        # Protect and translate body
        protected, regions = protect(body)
        translated_body, t = self._call(system, protected)
        total += t
        translated_body = restore(translated_body.strip(), regions)

        return (updated_fm + translated_body).rstrip() + "\n", total


# ---------------------------------------------------------------------------
# DeepL backend
# ---------------------------------------------------------------------------

_DEEPL_LANG_MAP = {
    "vi": "VI",
    "zh_CN": "ZH-HANS",
    "ja": "JA",
}


class DeepLBackend:
    def __init__(self, cfg: Config):
        import deepl

        self._translator = deepl.Translator(cfg.deepl_api_key)

    def translate_doc(self, raw: str, lang: str) -> tuple[str, int]:
        target = _DEEPL_LANG_MAP.get(lang, lang.upper())

        m = _FM_RE.match(raw)
        fm_block = m.group(0) if m else ""
        body = raw[m.end():] if m else raw
        updated_fm = fm_block

        # Translate front matter fields
        if fm_block:
            inner = fm_block.strip().lstrip("-").rstrip("-").strip()
            for field in _FM_TRANSLATABLE:
                fm = re.search(
                    rf"^{re.escape(field)}\s*:\s*"
                    rf"(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|[^\n]+)",
                    inner, re.MULTILINE,
                )
                if fm:
                    v = fm.group(1).strip().strip('"\'')
                    if v:
                        result = self._translator.translate_text(v, target_lang=target)
                        updated_fm = re.sub(
                            rf"^({re.escape(field)}\s*:\s*)"
                            rf"(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|[^\n]+)",
                            lambda mo, tv=result.text: f'{mo.group(1)}"{tv}"',
                            updated_fm, count=1, flags=re.MULTILINE,
                        )

        # Protect code/math, translate body via DeepL (HTML tag-ignore mode)
        protected, regions = protect(body)
        # DeepL handles plain text; wrap placeholders as ignored XML tags
        # Use translate_text with tag_handling="html" and ignore_tags for placeholders
        result = self._translator.translate_text(
            protected,
            target_lang=target,
            tag_handling="xml",
            ignore_tags=["protect"],
        )
        translated_body = restore(result.text.strip(), regions)

        return (updated_fm + translated_body).rstrip() + "\n", 0


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def make_backend(cfg: Config) -> TranslatorBackend:
    cfg.validate_provider()
    if cfg.provider == "chatgpt":
        return ChatGPTToolBackend()
    if cfg.provider == "openai":
        return OpenAIBackend(cfg)
    if cfg.provider == "deepl":
        return DeepLBackend(cfg)
    raise ValueError(f"Unknown provider: {cfg.provider!r}")
