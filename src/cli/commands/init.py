"""Initialize command."""

from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Confirm

from src.core.database import init_db_sync
from src.core.logger import logger

app = typer.Typer()
console = Console()


@app.command()
def run(
    force: bool = typer.Option(False, "--force", "-f", help="Force re-initialization"),
) -> None:
    """
    프로젝트 초기화.

    데이터베이스를 생성하고 필요한 디렉토리를 설정합니다.
    """
    try:
        console.print("[bold blue]Initializing Claude Skills Run...[/bold blue]")

        # Create logs directory
        logs_dir = Path("logs")
        if not logs_dir.exists():
            logs_dir.mkdir(parents=True)
            console.print(f"✓ Created {logs_dir}")

        # Create skills directory
        skills_dir = Path("skills")
        if not skills_dir.exists():
            skills_dir.mkdir(parents=True)
            console.print(f"✓ Created {skills_dir}")

        # Initialize database
        db_file = Path("claudeskills.db")
        if db_file.exists() and not force:
            if not Confirm.ask(
                f"[yellow]Database {db_file} already exists. Overwrite?[/yellow]"
            ):
                console.print("[yellow]Skipped database initialization[/yellow]")
                return

        init_db_sync()
        console.print("✓ Database initialized")

        console.print("\n[bold green]✓ Initialization completed successfully![/bold green]")
        console.print("\n[dim]Next steps:[/dim]")
        console.print("  1. Configure .env file with your ANTHROPIC_API_KEY")
        console.print("  2. Run [bold]claudeskills server start[/bold] to start the web server")
        console.print("  3. Run [bold]claudeskills --help[/bold] to see available commands")

    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        console.print(f"[bold red]✗ Initialization failed: {e}[/bold red]")
        raise typer.Exit(code=1)
