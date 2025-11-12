"""Skills management commands."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from src.core.config import settings

app = typer.Typer()
console = Console()


@app.command()
def list(
    custom: bool = typer.Option(False, "--custom", "-c", help="Show custom skills only"),
) -> None:
    """스킬 목록 조회."""
    table = Table(title="Available Skills")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Type", style="green")

    # TODO: Scan skills directories
    skills_data = [
        ("flutter-init", "Flutter 프로젝트 생성", "Built-in"),
        ("nextjs-init", "Next.js 프로젝트 생성", "Built-in"),
        ("code-changelog", "코드 변경사항 문서화", "Built-in"),
        ("ai-verifier", "AI 검증 루프", "Built-in"),
    ]

    for name, desc, skill_type in skills_data:
        if custom and skill_type != "Custom":
            continue
        table.add_row(name, desc, skill_type)

    console.print(table)


@app.command()
def info(
    name: str = typer.Argument(..., help="Skill name"),
) -> None:
    """스킬 상세 정보 조회."""
    console.print(f"[bold blue]Skill: {name}[/bold blue]")

    # TODO: Load skill metadata
    console.print("[yellow]⚠ Skill info not yet implemented[/yellow]")


@app.command()
def install(
    source: str = typer.Argument(..., help="Skill source (path or URL)"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Custom skill name"),
) -> None:
    """스킬 설치."""
    console.print(f"[bold blue]Installing skill from: {source}[/bold blue]")

    # TODO: Implement skill installation
    console.print("[yellow]⚠ Skill installation not yet implemented[/yellow]")
