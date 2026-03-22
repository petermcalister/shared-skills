"""CLI tool for searching Outlook emails and calendar."""

import argparse
import inspect
import io
import json
import logging
import sys

logger = logging.getLogger(__name__)

# Fix Windows console encoding for Unicode characters
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def _get_client():
    """Get connected OutlookClient or exit with error."""
    from src.outlook.outlook_client import OutlookClient, OutlookConnectionError
    try:
        client = OutlookClient()
        client.connect()
        return client
    except OutlookConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _print_emails(emails: list[dict], as_json: bool = False) -> None:
    """Format and print email results."""
    if as_json:
        json.dump(emails, sys.stdout, indent=2, default=str)
        print()
        return
    if not emails:
        print("No emails found.")
        return
    if len(emails) == 1 and "error" in emails[0]:
        print(f"Error: {emails[0]['error']}")
        return
    for i, email in enumerate(emails, 1):
        unread = " [UNREAD]" if email.get("unread") else ""
        print(f"{i:3}. {email['received']}  {email['sender']}")
        print(f"     {email['subject']}{unread}")
        print(f"     ID: {email['entry_id']}")
        print()


def _print_events(events: list[dict], as_json: bool = False) -> None:
    """Format and print calendar results."""
    if as_json:
        json.dump(events, sys.stdout, indent=2, default=str)
        print()
        return
    if not events:
        print("No events found.")
        return
    if len(events) == 1 and "error" in events[0]:
        print(f"Error: {events[0]['error']}")
        return
    for i, event in enumerate(events, 1):
        all_day = " [ALL DAY]" if event.get("all_day") else ""
        recurring = " [recurring]" if event.get("recurring") else ""
        location = f" @ {event['location']}" if event.get("location") else ""
        print(f"{i:3}. {event['start']} — {event['end']}{all_day}{recurring}")
        print(f"     {event['subject']}{location}")
        print()


def _print_folders(folders: list[dict], as_json: bool = False) -> None:
    """Format and print folder listing."""
    if as_json:
        json.dump(folders, sys.stdout, indent=2, default=str)
        print()
        return
    if not folders:
        print("No folders found.")
        return
    for f in folders:
        unread = f" ({f['unread_count']} unread)" if f["unread_count"] else ""
        print(f"  {f['path']}  [{f['item_count']} items]{unread}")


def _print_full_email(result: dict, as_json: bool = False) -> None:
    """Format and print a full email."""
    if as_json:
        json.dump(result, sys.stdout, indent=2, default=str)
        print()
        return
    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    print(f"From: {result['sender']} <{result.get('sender_email', '')}>")
    print(f"To: {result.get('to', '')}")
    if result.get("cc"):
        print(f"CC: {result['cc']}")
    print(f"Date: {result['received']}")
    print(f"Subject: {result['subject']}")
    if result.get("attachments"):
        print(f"Attachments: {', '.join(result['attachments'])}")
    print(f"\n{result.get('body', '')}")


# --- Individual entry points for poetry shortcuts ---

def search() -> None:
    """Search Outlook emails. Entry point for outlook-search shortcut."""
    parser = argparse.ArgumentParser(prog="outlook-search", description="Search Outlook emails")
    parser.add_argument("query", help="Search keyword")
    parser.add_argument("--weeks", type=int, default=None)
    parser.add_argument("--months", type=int, default=None)
    parser.add_argument("--folder", type=str, default=None)
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        client = _get_client()
        results = client.search_emails(
            query=args.query, weeks=args.weeks, months=args.months, folder=args.folder
        )
        if not args.as_json:
            print(f"Search: '{args.query}'\n")
        _print_emails(results, args.as_json)
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def recent() -> None:
    """List recent Outlook emails. Entry point for outlook-recent shortcut."""
    parser = argparse.ArgumentParser(prog="outlook-recent", description="List recent Outlook emails")
    parser.add_argument("--weeks", type=int, default=None)
    parser.add_argument("--months", type=int, default=None)
    parser.add_argument("--folder", type=str, default=None)
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        client = _get_client()
        results = client.list_recent(
            weeks=args.weeks, months=args.months, folder=args.folder
        )
        _print_emails(results, args.as_json)
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def read() -> None:
    """Read a full Outlook email. Entry point for outlook-read shortcut."""
    parser = argparse.ArgumentParser(prog="outlook-read", description="Read Outlook email by EntryID")
    parser.add_argument("email_id", help="Outlook EntryID")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        client = _get_client()
        result = client.read_email(args.email_id)
        _print_full_email(result, args.as_json)
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def folders() -> None:
    """List Outlook mail folders. Entry point for outlook-folders shortcut."""
    parser = argparse.ArgumentParser(prog="outlook-folders", description="List Outlook mail folders")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        client = _get_client()
        results = client.list_folders()
        _print_folders(results, args.as_json)
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def calendar() -> None:
    """Search or list Outlook calendar events. Entry point for outlook-calendar shortcut."""
    parser = argparse.ArgumentParser(prog="outlook-calendar", description="Outlook calendar events")
    parser.add_argument("query", nargs="?", default=None, help="Search keyword (optional)")
    parser.add_argument("--weeks", type=int, default=None)
    parser.add_argument("--months", type=int, default=None)
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        client = _get_client()
        if args.query:
            results = client.search_calendar(
                query=args.query, weeks=args.weeks, months=args.months
            )
            if not args.as_json:
                print(f"Calendar search: '{args.query}'\n")
        else:
            results = client.list_calendar_events(
                weeks=args.weeks, months=args.months
            )
        _print_events(results, args.as_json)
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def send() -> None:
    """Send an email via Outlook. Entry point for outlook-send shortcut."""
    parser = argparse.ArgumentParser(prog="outlook-send", description="Send an email via Outlook")
    parser.add_argument("to", help="Recipient email address(es), semicolon-separated")
    parser.add_argument("subject", help="Email subject")
    parser.add_argument("body", help="Email body text")
    parser.add_argument("--cc", default=None, help="CC recipients")
    parser.add_argument("--bcc", default=None, help="BCC recipients")
    parser.add_argument("--html", action="store_true", help="Treat body as HTML")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        client = _get_client()
        result = client.send_email(
            to=args.to,
            subject=args.subject,
            body=args.body,
            cc=args.cc,
            bcc=args.bcc,
            html=args.html,
        )
        if args.as_json:
            json.dump(result, sys.stdout, indent=2, default=str)
            print()
        elif "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Email sent to {args.to}: {args.subject}")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


# --- Main entry point for python -m tools outlook ---

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m tools outlook",
        description="Search Outlook emails and calendar",
    )
    sub = parser.add_subparsers(dest="command")

    p_search = sub.add_parser("search", help="Search emails by keyword")
    p_search.add_argument("query", help="Search keyword")
    p_search.add_argument("--weeks", type=int, default=None)
    p_search.add_argument("--months", type=int, default=None)
    p_search.add_argument("--folder", type=str, default=None)
    p_search.add_argument("--json", dest="as_json", action="store_true")

    p_recent = sub.add_parser("recent", help="List recent emails")
    p_recent.add_argument("--weeks", type=int, default=None)
    p_recent.add_argument("--months", type=int, default=None)
    p_recent.add_argument("--folder", type=str, default=None)
    p_recent.add_argument("--json", dest="as_json", action="store_true")

    p_folders = sub.add_parser("folders", help="List mail folders")
    p_folders.add_argument("--json", dest="as_json", action="store_true")

    p_cal = sub.add_parser("calendar", help="Search or list calendar events")
    p_cal.add_argument("query", nargs="?", default=None, help="Search keyword (optional)")
    p_cal.add_argument("--weeks", type=int, default=None)
    p_cal.add_argument("--months", type=int, default=None)
    p_cal.add_argument("--json", dest="as_json", action="store_true")

    p_read = sub.add_parser("read", help="Read full email by EntryID")
    p_read.add_argument("email_id", help="Outlook EntryID")
    p_read.add_argument("--json", dest="as_json", action="store_true")

    p_send = sub.add_parser("send", help="Send an email")
    p_send.add_argument("to", help="Recipient email(s)")
    p_send.add_argument("subject", help="Subject line")
    p_send.add_argument("body", help="Body text")
    p_send.add_argument("--cc", default=None)
    p_send.add_argument("--bcc", default=None)
    p_send.add_argument("--html", action="store_true")
    p_send.add_argument("--json", dest="as_json", action="store_true")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "search":
        sys.argv = ["outlook-search", args.query]
        if args.weeks:
            sys.argv += ["--weeks", str(args.weeks)]
        if args.months:
            sys.argv += ["--months", str(args.months)]
        if args.folder:
            sys.argv += ["--folder", args.folder]
        if args.as_json:
            sys.argv.append("--json")
        search()
    elif args.command == "recent":
        sys.argv = ["outlook-recent"]
        if args.weeks:
            sys.argv += ["--weeks", str(args.weeks)]
        if args.months:
            sys.argv += ["--months", str(args.months)]
        if args.folder:
            sys.argv += ["--folder", args.folder]
        if args.as_json:
            sys.argv.append("--json")
        recent()
    elif args.command == "folders":
        sys.argv = ["outlook-folders"]
        if args.as_json:
            sys.argv.append("--json")
        folders()
    elif args.command == "calendar":
        sys.argv = ["outlook-calendar"]
        if args.query:
            sys.argv.insert(1, args.query)
        if args.weeks:
            sys.argv += ["--weeks", str(args.weeks)]
        if args.months:
            sys.argv += ["--months", str(args.months)]
        if args.as_json:
            sys.argv.append("--json")
        calendar()
    elif args.command == "read":
        sys.argv = ["outlook-read", args.email_id]
        if args.as_json:
            sys.argv.append("--json")
        read()
    elif args.command == "send":
        sys.argv = ["outlook-send", args.to, args.subject, args.body]
        if args.cc:
            sys.argv += ["--cc", args.cc]
        if args.bcc:
            sys.argv += ["--bcc", args.bcc]
        if args.html:
            sys.argv.append("--html")
        if args.as_json:
            sys.argv.append("--json")
        send()


if __name__ == "__main__":
    main()
