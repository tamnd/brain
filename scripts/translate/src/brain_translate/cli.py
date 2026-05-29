"""brain-translate CLI — incremental translation pipeline for tamnd/brain."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from .config import Config
from .detect import dest_path, file_hash, scan_source
from .models import LANG_META, SUPPORTED_LANGS, QueueItem
from .publisher import Publisher
from .state import StateManager
from .translator import make_backend

app = typer.Typer(
    name="brain-translate",
    help="Incremental translation pipeline for tamnd/brain.",
    no_args_is_help=True,
)
console = Console()
err = Console(stderr=True)


def _validate_lang(lang: str) -> str:
    if lang not in SUPPORTED_LANGS:
        err.print(
            f"[red]Unknown language {lang!r}.[/] "
            f"Supported: {', '.join(sorted(SUPPORTED_LANGS))}"
        )
        raise typer.Exit(1)
    return lang


def _make_sm(cfg: Config, lang: str) -> StateManager:
    return StateManager(
        cfg.state_dir(lang),
        lang,
        cfg.source_repo,
        cfg.repo_dir(lang),
        provider=cfg.provider,
        model=cfg.model,
    )


# ---------------------------------------------------------------------------
# setup
# ---------------------------------------------------------------------------

@app.command()
def setup(
    lang: Annotated[str, typer.Argument(help="Language code: vi, zh_CN, ja")],
) -> None:
    """Initialize state directory for a language."""
    lang = _validate_lang(lang)
    cfg = Config.from_env()
    sm = _make_sm(cfg, lang)
    state = sm.load_state()
    sm.save_state(state)
    queue = sm.load_queue()
    sm.save_queue(queue)
    meta = LANG_META[lang]
    err.print(f"[green]Ready:[/] {cfg.state_dir(lang)}")
    err.print(f"  lang:     {lang} ({meta['name']})")
    err.print(f"  repo:     {cfg.repo_dir(lang)}")
    err.print(f"  provider: {cfg.provider}")


# ---------------------------------------------------------------------------
# scan
# ---------------------------------------------------------------------------

@app.command()
def scan(
    lang: Annotated[str, typer.Argument(help="Language code")],
) -> None:
    """Scan content/en for new/changed files and add them to the queue."""
    lang = _validate_lang(lang)
    cfg = Config.from_env()
    sm = _make_sm(cfg, lang)
    state = sm.load_state()
    queue = sm.load_queue()

    new_files, changed = scan_source(cfg.source_repo, state, queue)
    sm.save_queue(queue)

    err.print(f"[green]New:[/green] {len(new_files)}")
    err.print(f"[yellow]Changed:[/yellow] {len(changed)}")
    err.print(f"[blue]Total pending:[/blue] {len(queue.pending)}")


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

@app.command()
def status(
    lang: Annotated[str, typer.Argument(help="Language code")],
) -> None:
    """Show translation progress for a language."""
    lang = _validate_lang(lang)
    cfg = Config.from_env()
    sm = _make_sm(cfg, lang)
    state = sm.load_state()
    queue = sm.load_queue()

    done = sum(1 for f in state.files.values() if f.status == "done")
    failed = sum(1 for f in state.files.values() if f.status == "failed")
    total_tokens = sum(f.tokens_used for f in state.files.values())

    t = Table(title=f"brain-translate: {lang} ({LANG_META[lang]['name']})")
    t.add_column("Metric", style="dim")
    t.add_column("Value")
    t.add_row("Translated (done)", str(done))
    t.add_row("Failed", str(failed))
    t.add_row("Queue pending", str(len(queue.pending)))
    t.add_row("Queue failed", str(len(queue.failed)))
    t.add_row("Batch", str(state.batch))
    t.add_row("Tokens used", f"{total_tokens:,}")
    t.add_row("Last run", str(state.last_run or "never"))
    t.add_row("Provider", state.translator.provider)
    console.print(t)


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------

@app.command()
def run(
    lang: Annotated[str, typer.Argument(help="Language code")],
    limit: int = typer.Option(20, "--limit", "-n", help="Max files to translate per run"),
    provider: Optional[str] = typer.Option(
        None, "--provider", "-p",
        help="chatgpt | google | bing | yandex | baidu | google_dt (overrides env)",
    ),
    push: bool = typer.Option(False, "--push", help="Commit + push after translating"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Translate one specific file"),
) -> None:
    """Translate pending files from the queue.

    Examples:
      brain-translate run vi --limit 50 --push
      brain-translate run vi --provider chatgpt --push
      brain-translate run vi --file content/en/practice/maths/imo/1974/2.md
    """
    lang = _validate_lang(lang)
    cfg = Config.from_env()
    if provider:
        cfg = cfg.model_copy(update={"provider": provider})

    sm = _make_sm(cfg, lang)
    state = sm.load_state()
    queue = sm.load_queue()
    backend = make_backend(cfg)
    pub = Publisher(cfg, lang)

    # Build work list
    if file:
        items = [it for it in queue.pending if it.source_path == file]
        if not items:
            err.print(f"[yellow]{file} not in queue; adding now[/]")
            items = [QueueItem(source_path=file)]
    else:
        items = queue.pending[:limit]

    if not items:
        err.print("[yellow]Nothing to translate. Run 'scan' first.[/]")
        raise typer.Exit(0)

    pub.ensure_repo()
    translated_dest: list[str] = []

    for item in items:
        src_abs = cfg.source_repo / item.source_path
        if not src_abs.exists():
            err.print(f"[yellow]skip (missing):[/] {item.source_path}")
            queue.pending = [x for x in queue.pending if x.source_path != item.source_path]
            sm.save_queue(queue)
            continue

        src_hash = file_hash(src_abs)
        dp = dest_path(item.source_path)
        err.print(f"[dim]translating:[/] {item.source_path}")

        try:
            raw = src_abs.read_text(encoding="utf-8")
            translated, tokens = backend.translate_doc(raw, lang)
            pub.write_file(dp, translated)
            sm.mark_done(state, item.source_path, src_hash, dp, tokens, cfg.provider)
            sm.save_state(state)
            translated_dest.append(dp)
            queue.pending = [x for x in queue.pending if x.source_path != item.source_path]
            sm.save_queue(queue)
            err.print(f"[green]done:[/] {dp}")
        except Exception as exc:
            # escape brackets so Rich doesn't strip them as markup tags
            msg = str(exc).replace("[", "\\[")
            err.print(f"[red]error:[/] {item.source_path}: {msg}")
            sm.mark_failed(state, item.source_path, src_hash, dp, cfg.provider)
            sm.save_state(state)
            item.retries += 1

    err.print(f"Translated {len(translated_dest)} file(s).")

    if translated_dest and push:
        sha = pub.source_sha(cfg.source_repo)
        state.batch += 1
        if pub.commit_and_push(
            translated_dest, state.batch, sha, cfg.provider, cfg.model
        ):
            err.print(f"[green]Pushed batch {state.batch:04d}[/]")
        sm.save_state(state)
    elif translated_dest:
        err.print("[dim]Run 'push <lang>' to publish.[/]")


# ---------------------------------------------------------------------------
# push
# ---------------------------------------------------------------------------

@app.command("push")
def push_cmd(
    lang: Annotated[str, typer.Argument(help="Language code")],
) -> None:
    """Commit all staged translations in the local repo and push."""
    lang = _validate_lang(lang)
    cfg = Config.from_env()
    sm = _make_sm(cfg, lang)
    state = sm.load_state()
    pub = Publisher(cfg, lang)

    pub.ensure_repo()
    sha = pub.source_sha(cfg.source_repo)
    state.batch += 1

    # Stage everything new/modified in the repo
    subprocess.run(["git", "add", "--all"], cwd=pub.repo_dir, check=True)
    if pub.commit_and_push(
        ["."], state.batch, sha, cfg.provider, cfg.model
    ):
        err.print(f"[green]Pushed batch {state.batch:04d}[/]")
        sm.save_state(state)
    else:
        err.print("[yellow]Nothing to push.[/]")


# ---------------------------------------------------------------------------
# compare
# ---------------------------------------------------------------------------

@app.command()
def compare(
    lang: Annotated[str, typer.Argument(help="Language code")],
    file: str = typer.Option(..., "--file", "-f", help="Source file to compare"),
    out_dir: Optional[Path] = typer.Option(
        None, "--out-dir", help="Directory to write comparison files (default: /tmp)"
    ),
) -> None:
    """Translate one file with all available providers and write side-by-side outputs.

    Example:
      brain-translate compare vi --file content/en/practice/maths/imo/1974/2.md
    """
    lang = _validate_lang(lang)
    cfg = Config.from_env()
    src_abs = cfg.source_repo / file
    if not src_abs.exists():
        err.print(f"[red]Not found:[/] {src_abs}")
        raise typer.Exit(1)

    raw = src_abs.read_text(encoding="utf-8")
    stem = Path(file).stem
    out_base = out_dir or Path("/tmp")
    out_base.mkdir(parents=True, exist_ok=True)

    providers = ["chatgpt", "openai", "deepl"]
    for prov in providers:
        try:
            pcfg = cfg.model_copy(update={"provider": prov})
            pcfg.validate_provider()
        except RuntimeError as e:
            err.print(f"[yellow]skip {prov}:[/] {e}")
            continue

        err.print(f"[dim]translating with {prov}...[/]")
        try:
            backend = make_backend(pcfg)
            translated, _ = backend.translate_doc(raw, lang)
            out_path = out_base / f"{stem}.{lang}.{prov}.md"
            out_path.write_text(translated, encoding="utf-8")
            err.print(f"[green]{prov}:[/] {out_path}")
        except Exception as exc:
            err.print(f"[red]{prov} error:[/] {exc}")

    err.print(f"\nCompare outputs in: {out_base}")
    err.print(f"  diff: diff {out_base}/{stem}.{lang}.chatgpt.md {out_base}/{stem}.{lang}.openai.md")
