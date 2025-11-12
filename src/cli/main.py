"""Claude Skills Run CLI application."""

import typer
from rich.console import Console

from src.cli.commands import create, init, server, skills, workflow
from src.core.config import settings

# Create Typer app
app = typer.Typer(
    name="claudeskills",
    help="Claude Skills 자동화 워크플로우 추적 및 테스트 플랫폼",
    add_completion=True,
    rich_markup_mode="rich",
)

# Console for rich output
console = Console()

# Add subcommands
app.add_typer(init.app, name="init", help="프로젝트 초기화")
app.add_typer(create.app, name="create", help="프로젝트 생성")
app.add_typer(workflow.app, name="workflow", help="워크플로우 관리")
app.add_typer(skills.app, name="skills", help="스킬 관리")
app.add_typer(server.app, name="server", help="웹 서버 관리")


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"[bold blue]{settings.app_name}[/bold blue] v{settings.app_version}")


@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """
    Claude Skills Run - 자동화 워크플로우 추적 및 테스트 플랫폼.

    Claude Code의 커스텀 스킬을 테스트하고 다양한 자동화 워크플로우를 관리합니다.
    """
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")


if __name__ == "__main__":
    app()
