"""Server management commands."""

import subprocess
import sys

import typer
from rich.console import Console

from src.core.config import settings

app = typer.Typer()
console = Console()


@app.command()
def start(
    host: str = typer.Option(None, "--host", "-h", help="Server host"),
    port: int = typer.Option(None, "--port", "-p", help="Server port"),
    reload: bool = typer.Option(True, "--reload/--no-reload", help="Enable auto-reload"),
) -> None:
    """웹 서버 시작."""
    server_host = host or settings.api_host
    server_port = port or settings.api_port

    console.print(
        f"[bold blue]Starting server at http://{server_host}:{server_port}[/bold blue]"
    )
    console.print(f"[dim]API docs: http://{server_host}:{server_port}/api/docs[/dim]")

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "src.api.app:app",
                "--host",
                server_host,
                "--port",
                str(server_port),
                *(["--reload"] if reload else []),
            ],
            check=True,
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped[/yellow]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]✗ Server failed to start: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def dev() -> None:
    """개발 모드로 서버 시작 (auto-reload 활성화)."""
    start(reload=True)
