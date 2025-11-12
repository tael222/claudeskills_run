"""Create command for project generation."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def run(
    project_type: str = typer.Argument(..., help="Project type (nextjs, flutter, python, etc.)"),
    name: str = typer.Option(..., "--name", "-n", help="Project name"),
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Output directory"),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Template name"),
) -> None:
    """
    새 프로젝트 생성.

    지원되는 프로젝트 타입:
    - nextjs: Next.js 프로젝트
    - flutter: Flutter 프로젝트
    - python: Python 프로젝트
    - react: React 프로젝트
    """
    console.print(f"[bold blue]Creating {project_type} project: {name}[/bold blue]")

    # TODO: Implement project creation logic
    console.print("[yellow]⚠ Project creation not yet implemented[/yellow]")
    console.print(f"Project type: {project_type}")
    console.print(f"Name: {name}")
    if output_dir:
        console.print(f"Output: {output_dir}")
    if template:
        console.print(f"Template: {template}")
