from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()


from pyfiglet import Figlet

LOGO = Figlet(font="standard", width=100).renderText("PHISHGUARD").strip()

def show_banner():
    console.print(
        Panel(
            Align.center(Text(LOGO, style="bold bright_green")),
            border_style="bright_green",
            box=box.DOUBLE,
            subtitle="[bold cyan]PHISHING EMAIL DETECTION[/]",
            padding=(1, 2),
        )
    )
    console.print(
        Align.center(
            Text("PHISHGUARD | LOCAL EMAIL SECURITY TOOL", style="bold cyan")
        )
    )
    console.print(
        Align.center(
            Text(
                "Machine Learning • Header Forensics • URL Analysis",
                style="dim white",
            )
        )
    )

if __name__ == "__main__":
    show_banner()
