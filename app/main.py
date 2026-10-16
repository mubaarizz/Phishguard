from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.ui.banner import show_banner
from app.core.email_parser import parse_email
from app.core.header_analyzer import analyze_headers
from app.core.url_analyzer import analyze_url
from app.core.ml_analyzer import analyze_email_text

console = Console()


def scan_email(file_path):
    try:
        email = parse_email(file_path)
    except (OSError, ValueError) as error:
        console.print(f"[bold red]Error:[/] {error}")
        return

    console.print(
        Panel(
            "[bold cyan]EMAIL ANALYSIS REPORT[/]",
            border_style="cyan",
        )
    )

    details = Table(show_header=False, expand=True)
    details.add_column("Field", style="bold cyan", width=20)
    details.add_column("Value", overflow="fold")

    details.add_row("File", email["file_name"])
    details.add_row("Subject", email["subject"] or "(missing)")
    details.add_row(
        "Sender",
        f'{email["sender_name"]} <{email["sender_email"]}>',
    )
    details.add_row("Reply-To", email["reply_to"] or "(not provided)")
    details.add_row("Recipient", email["recipient"] or "(not provided)")
    details.add_row("Date", email["date"] or "(not provided)")

    console.print(details)

    try:
        ml_result = analyze_email_text(
            email["subject"],
            email["body"],
        )

        ml_table = Table(title="Machine Learning Analysis", expand=True)
        ml_table.add_column("Field", style="cyan")
        ml_table.add_column("Result", overflow="fold")

        ml_table.add_row(
            "Predicted classification",
            {"0": "Legitimate", "1": "Phishing (Malicious)"}.get(str(ml_result["predicted_label"]), "Unknown"),
        )
        ml_table.add_row(
            "Legitimate probability",
            f'{ml_result["label_0_probability"]:.2%}',
        )
        ml_table.add_row(
            "Phishing (Malicious) probability",
            f'{ml_result["label_1_probability"]:.2%}',
        )

        console.print(ml_table)
        console.print(f'[dim]{ml_result["note"]}[/]')
    except (OSError, ValueError, ImportError) as error:
        console.print(f"[yellow]ML analysis unavailable:[/] {error}")

    console.print(
        Panel(
            email["body"][:4000] or "(No readable email body found)",
            title="Email Body",
            border_style="blue",
        )
    )

    url_table = Table(title="Extracted URLs", expand=True)
    url_table.add_column("#", style="cyan", width=4)
    url_table.add_column("URL", overflow="fold")
    url_table.add_column("Hostname", overflow="fold")

    for index, item in enumerate(email["urls"], start=1):
        url_table.add_row(
            str(index),
            item["url"],
            item["hostname"] or "(unavailable)",
        )

    if not email["urls"]:
        url_table.add_row("-", "No URLs found", "-")

    console.print(url_table)

    header_analysis = email["header_analysis"]
    header_table = Table(title="Header Forensics Findings", expand=True)
    header_table.add_column("Indicator", style="cyan", overflow="fold")
    header_table.add_column("Severity", width=16)
    header_table.add_column("Details", overflow="fold")

    for finding in header_analysis["findings"]:
        header_table.add_row(
            finding["indicator"],
            finding["severity"],
            finding["details"],
        )

    console.print(header_table)


    risk_table = Table(title="URL Risk Indicators", expand=True)
    risk_table.add_column("URL", overflow="fold")
    risk_table.add_column("Risk", width=12)
    risk_table.add_column("Findings", overflow="fold")

    for item in email["urls"]:
        result = analyze_url(item["url"])
        risk_table.add_row(
            result["url"],
            result["risk_level"],
            "; ".join(result["findings"]),
        )

    if not email["urls"]:
        risk_table.add_row("-", "N/A", "No URLs to analyze")

    console.print(risk_table)

    headers = email["headers"]
    console.print(
        Panel(
            f'Authentication-Results: {headers["authentication_results"] or "Not present"}\n'
            f'Received-SPF: {headers["received_spf"] or "Not present"}\n'
            f'DKIM signature header: {"Present" if headers["dkim_signature_present"] else "Not present"}',
            title="Available Header Evidence",
            border_style="yellow",
        )
    )

    console.print(
        "[dim]Note: ML predicts the dataset's original label, not confirmed phishing. "
        "Header results use supplied email headers; URL checks are heuristic only. "
        "Links are not opened.[/]"
    )


def main():
    show_banner()

    # Preserve the existing command-line usage.
    if len(sys.argv) == 2:
        scan_email(sys.argv[1])
        return

    if len(sys.argv) > 2:
        console.print(
            "[yellow]Usage:[/] python -m app.main [path/to/email.eml]"
        )
        return

    console.print("[bold cyan]Interactive Email Analysis[/]")
    console.print("[dim]Press Enter to choose an email, or type 'q' to quit.[/]")

    while True:
        try:
            choice = console.input("[bold cyan]Enter or q: [/]").strip().lower()

            if choice in {"q", "quit", "exit"}:
                console.print("[dim]Exiting PHISHGUARD. Goodbye![/]")
                break

            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            try:
                file_path = filedialog.askopenfilename(
                    parent=root,
                    title="Select an email for PhishGuard",
                    filetypes=[
                        ("Email files", "*.eml"),
                        ("All files", "*.*"),
                    ],
                )
            finally:
                root.destroy()

            if isinstance(file_path, tuple):
                file_path = file_path[0] if file_path else ""
            file_path = file_path.strip()

        except (EOFError, KeyboardInterrupt):
            console.print("\\n[dim]PHISHGUARD session ended.[/]")
            break

        if not file_path:
            console.print("[dim]File selection cancelled. PHISHGUARD session ended.[/]")
            break

        # Accept paths pasted with surrounding quotes.
        if (
            len(file_path) >= 2
            and file_path[0] == file_path[-1]
            and file_path[0] in {"\\'", '"'}
        ):
            file_path = file_path[1:-1]

        email_path = Path(file_path).expanduser()

        if not email_path.is_file():
            console.print(
                f"[bold red]Error:[/] File not found: {email_path}"
            )
            continue

        if email_path.suffix.lower() != ".eml":
            console.print(
                "[yellow]Please select a file with the .eml extension.[/]"
            )
            continue

        scan_email(str(email_path))

        try:
            again = console.input(
                "\\n[bold cyan]Analyse another email?[/] [Y/n]: "
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            console.print("\\n[dim]PHISHGUARD session ended.[/]")
            break

        if again in {"n", "no", "q", "quit", "exit"}:
            console.print("[dim]Exiting PHISHGUARD. Goodbye![/]")
            break


if __name__ == "__main__":
    main()
