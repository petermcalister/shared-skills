"""CLI tool for memory operations — thin argparse wrappers over src/memory/."""

import argparse
import inspect
import json
import logging
import sys

logger = logging.getLogger(__name__)


def _get_conn():
    """Get a memory DB connection."""
    from src.memory.db import get_connection
    return get_connection()


def _print_json(data):
    """Print data as formatted JSON."""
    json.dump(data, sys.stdout, indent=2, default=str)
    print()


# ── Entry points for CLI shortcuts ──────────────────────────────────


def add_event() -> None:
    """Add an episodic event. Entry point for memory-add-event shortcut."""
    parser = argparse.ArgumentParser(prog="memory-add-event", description="Add an episodic event")
    parser.add_argument("content", help="Event description")
    parser.add_argument("--source", default="manual", help="Event source")
    parser.add_argument("--category", default="general", help="Category")
    parser.add_argument("--importance", type=int, default=5, help="Importance 1-10")
    parser.add_argument("--expires", default=None, help="Expiry date (ISO 8601)")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.episodic import add_event as _add
        conn = _get_conn()
        result = _add(conn, args.content, source=args.source, category=args.category,
                       importance=args.importance, expires=args.expires)
        if args.as_json:
            _print_json(result)
        else:
            print(f"Event added (id={result['id']}): {result['content']}")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def add_task() -> None:
    """Add a task. Entry point for memory-add-task shortcut."""
    parser = argparse.ArgumentParser(prog="memory-add-task", description="Add a task")
    parser.add_argument("title", help="Task title")
    parser.add_argument("--description", default=None, help="Task description")
    parser.add_argument("--priority", default="medium", choices=["low", "medium", "high", "critical"])
    parser.add_argument("--due", default=None, help="Due date (YYYY-MM-DD)")
    parser.add_argument("--source", default="manual")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.tasks import add_task as _add
        conn = _get_conn()
        result = _add(conn, args.title, description=args.description,
                       priority=args.priority, due_date=args.due, source=args.source)
        if args.as_json:
            _print_json(result)
        else:
            print(f"Task added (id={result['id']}): {result['title']}")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def add_fact() -> None:
    """Add a semantic fact. Entry point for memory-add-fact shortcut."""
    parser = argparse.ArgumentParser(prog="memory-add-fact", description="Add a semantic fact")
    parser.add_argument("subject", help="Fact subject")
    parser.add_argument("predicate", help="Fact predicate")
    parser.add_argument("object", help="Fact object/value")
    parser.add_argument("--confidence", type=float, default=0.8)
    parser.add_argument("--source", default="manual")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.semantic import add_fact as _add
        conn = _get_conn()
        result = _add(conn, args.subject, args.predicate, args.object,
                       confidence=args.confidence, source=args.source)
        if args.as_json:
            _print_json(result)
        else:
            print(f"Fact added (id={result['id']}): {args.subject} {args.predicate} {args.object}")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def list_tasks() -> None:
    """List open/overdue tasks. Entry point for memory-tasks shortcut."""
    parser = argparse.ArgumentParser(prog="memory-tasks", description="List open tasks")
    parser.add_argument("--priority", default=None, choices=["low", "medium", "high", "critical"])
    parser.add_argument("--overdue", action="store_true", help="Show only overdue tasks")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.tasks import get_open_tasks, get_overdue_tasks
        conn = _get_conn()
        if args.overdue:
            results = get_overdue_tasks(conn)
        else:
            results = get_open_tasks(conn, priority=args.priority)
        if args.as_json:
            _print_json(results)
        else:
            if not results:
                print("No tasks found.")
                return
            for t in results:
                due = f" (due: {t['due_date']})" if t.get("due_date") else ""
                status = f" [{t['status']}]" if t["status"] != "open" else ""
                print(f"  [{t['priority'].upper()}] #{t['id']}: {t['title']}{due}{status}")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def done() -> None:
    """Complete a task by ID. Entry point for memory-done shortcut."""
    parser = argparse.ArgumentParser(prog="memory-done", description="Complete a task")
    parser.add_argument("task_id", type=int, help="Task ID to complete")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.tasks import complete_task
        conn = _get_conn()
        result = complete_task(conn, args.task_id)
        if args.as_json:
            _print_json(result)
        elif result:
            print(f"Task #{args.task_id} completed: {result['title']}")
        else:
            print(f"Task #{args.task_id} not found.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def recent() -> None:
    """Show recent episodic events. Entry point for memory-recent shortcut."""
    parser = argparse.ArgumentParser(prog="memory-recent", description="Recent episodic events")
    parser.add_argument("--days", type=int, default=7, help="Look back N days")
    parser.add_argument("--min-importance", type=int, default=1)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.episodic import get_recent_events
        conn = _get_conn()
        results = get_recent_events(conn, days=args.days, min_importance=args.min_importance, limit=args.limit)
        if args.as_json:
            _print_json(results)
        else:
            if not results:
                print("No recent events.")
                return
            for e in results:
                print(f"  [{e['category']}] {e['timestamp']}: {e['content']} (importance: {e['importance']})")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def search() -> None:
    """Search across all memory tiers. Entry point for memory-search shortcut."""
    parser = argparse.ArgumentParser(prog="memory-search", description="Search memory")
    parser.add_argument("query", help="Search text")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.query import search_memory
        conn = _get_conn()
        results = search_memory(conn, args.query, limit=args.limit)
        if args.as_json:
            _print_json(results)
        else:
            for tier, items in results.items():
                if items:
                    print(f"\n{tier.upper()} ({len(items)} results):")
                    for item in items:
                        if tier == "episodic":
                            print(f"  {item['timestamp']}: {item['content']}")
                        elif tier == "semantic":
                            print(f"  {item['subject']} {item['predicate']} {item['object']}")
                        elif tier == "tasks":
                            print(f"  #{item['id']}: {item['title']}")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def context() -> None:
    """Show full briefing context. Entry point for memory-context shortcut."""
    parser = argparse.ArgumentParser(prog="memory-context", description="Show briefing context")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.query import build_briefing_context
        conn = _get_conn()
        ctx = build_briefing_context(conn)
        if args.as_json:
            _print_json(ctx)
        else:
            print("=== Always-On Context ===")
            print(ctx["always_on"] or "(empty)")
            print(f"\n=== Recent Events ({len(ctx['episodic_events'])}) ===")
            for e in ctx["episodic_events"]:
                print(f"  {e['timestamp']}: {e['content']}")
            print(f"\n=== Open Tasks ({len(ctx['open_tasks'])}) ===")
            for t in ctx["open_tasks"]:
                print(f"  [{t['priority']}] #{t['id']}: {t['title']}")
            if ctx["overdue_tasks"]:
                print(f"\n=== OVERDUE ({len(ctx['overdue_tasks'])}) ===")
                for t in ctx["overdue_tasks"]:
                    print(f"  #{t['id']}: {t['title']} (due: {t['due_date']})")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def distill() -> None:
    """Extract memories from conversation text. Entry point for memory-distill shortcut."""
    parser = argparse.ArgumentParser(prog="memory-distill", description="Extract memories from text")
    parser.add_argument("--input", required=True, help="Input text or file path")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.distill import distill_text
        from pathlib import Path

        # Read input from file or use as text
        input_path = Path(args.input)
        if input_path.exists():
            text = input_path.read_text(encoding="utf-8")
        else:
            text = args.input

        conn = _get_conn() if not args.dry_run else None
        results = distill_text(text, conn=conn, dry_run=args.dry_run)
        if args.as_json:
            _print_json(results)
        else:
            print(f"Extracted: {len(results.get('events', []))} events, "
                  f"{len(results.get('tasks', []))} tasks, "
                  f"{len(results.get('facts', []))} facts")
            if args.dry_run:
                print("(dry run — nothing written)")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def maintain() -> None:
    """Run decay, expiry, archival, dedup. Entry point for memory-maintain shortcut."""
    parser = argparse.ArgumentParser(prog="memory-maintain", description="Run memory maintenance")
    parser.add_argument("--decay", action="store_true", help="Run importance decay")
    parser.add_argument("--expire", action="store_true", help="Delete expired events")
    parser.add_argument("--archive", action="store_true", help="Archive old completed tasks")
    parser.add_argument("--all", action="store_true", help="Run all maintenance")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.maintain import run_maintenance
        conn = _get_conn()
        run_all = args.all or not (args.decay or args.expire or args.archive)
        results = run_maintenance(
            conn,
            decay=args.decay or run_all,
            expire=args.expire or run_all,
            archive=args.archive or run_all,
        )
        if args.as_json:
            _print_json(results)
        else:
            for action, count in results.items():
                print(f"  {action}: {count} records affected")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def curate() -> None:
    """LLM-driven weekly fact curation. Entry point for memory-curate shortcut."""
    parser = argparse.ArgumentParser(prog="memory-curate", description="Curate semantic facts")
    parser.add_argument("--dry-run", action="store_true", help="Preview without applying")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.curate import curate_facts
        conn = _get_conn()
        results = curate_facts(conn, dry_run=args.dry_run)
        if args.as_json:
            _print_json(results)
        else:
            for action in results.get("actions", []):
                print(f"  {action['type']}: {action['description']}")
            if args.dry_run:
                print("(dry run — nothing applied)")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def brief_action() -> None:
    """Act on morning brief items. Entry point for memory-brief-action shortcut."""
    parser = argparse.ArgumentParser(prog="memory-brief-action", description="Act on brief items")
    parser.add_argument("--action", required=True, choices=["done", "ignore", "snooze", "note"])
    parser.add_argument("--item-id", required=True, type=int, help="Item ID")
    parser.add_argument("--until", default=None, help="Snooze until date (YYYY-MM-DD)")
    parser.add_argument("--text", default=None, help="Note text")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        conn = _get_conn()
        if args.action == "done":
            from src.memory.tasks import complete_task
            result = complete_task(conn, args.item_id)
            msg = f"Task #{args.item_id} completed"
        elif args.action == "ignore":
            from src.utils.db_util import DatabaseManager
            # Lower importance of episodic event
            DatabaseManager.execute(
                conn,
                "UPDATE episodic_event SET importance = MAX(1, importance - 2) WHERE id = ?",
                (args.item_id,),
            )
            result = DatabaseManager.fetch_one(conn, "SELECT * FROM episodic_event WHERE id = ?", (args.item_id,))
            msg = f"Event #{args.item_id} importance lowered"
        elif args.action == "snooze":
            from src.memory.tasks import update_task
            result = update_task(conn, args.item_id, due_date=args.until)
            msg = f"Task #{args.item_id} snoozed until {args.until}"
        elif args.action == "note":
            from src.memory.episodic import add_event
            result = add_event(conn, args.text or "", source="brief-note",
                               category="note", metadata=str(args.item_id))
            msg = f"Note added for item #{args.item_id}"

        if args.as_json:
            _print_json(result)
        else:
            print(msg)
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


# ── WhatsApp command channel ─────────────────────────────────────────


def wa_poll() -> None:
    """Poll cowork-pa for pa: commands. Entry point for wa-poll shortcut."""
    parser = argparse.ArgumentParser(prog="wa-poll", description="Poll WhatsApp for commands")
    parser.add_argument("--force", action="store_true", help="Run even outside 7am-10pm")
    parser.add_argument("--mark-processed", dest="mark_ids", nargs="*", help="Mark message IDs as processed")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.wa_poll import poll_cowork_pa, mark_processed
        conn = _get_conn()

        # If marking messages as processed
        if args.mark_ids:
            for mid in args.mark_ids:
                mark_processed(conn, mid)
            if args.as_json:
                _print_json({"marked": args.mark_ids})
            else:
                print(f"Marked {len(args.mark_ids)} messages as processed")
            return

        result = poll_cowork_pa(conn, force=args.force)
        if args.as_json:
            _print_json(result)
        else:
            if result.get("skipped"):
                print(f"Skipped: {result.get('reason', '')}")
                return
            if result.get("error"):
                print(f"Error: {result['error']}")
                return

            commands = result.get("commands", [])
            if commands:
                print(f"Found {len(commands)} pa: command(s):\n")
                for cmd in commands:
                    print(f"  [{cmd['timestamp']}] {cmd['sender']}: {cmd['text']}")
                    print(f"  Message ID: {cmd['message_id']}")
                    print()
            else:
                print("No new pa: commands.")

            pending = result.get("pending_action")
            if pending:
                print(f"Pending confirmation: {pending}")

            for task in result.get("scheduled_tasks", []):
                print(f"SCHEDULED: {task}")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


# ── Hygiene entry points ─────────────────────────────────────────────


def hygiene_add() -> None:
    """Add a hygiene rule. Entry point for hygiene-add shortcut."""
    parser = argparse.ArgumentParser(prog="hygiene-add", description="Add a hygiene rule")
    parser.add_argument("rule_type", choices=["bulk_move_trash", "bulk_move_junk", "archive",
                                               "ignore_sender", "summarize_sender",
                                               "whatsapp_time_window", "memory_purge"])
    parser.add_argument("source", choices=["gmail", "outlook", "email", "whatsapp", "memory"])
    parser.add_argument("--sender", default=None, help="Sender pattern (LIKE syntax, e.g. %%quora%%)")
    parser.add_argument("--age-days", type=int, default=None, help="Only affect items older than N days")
    parser.add_argument("--threshold", type=float, default=None, help="Importance threshold (memory_purge)")
    parser.add_argument("--description", default=None, help="Human-readable description")
    parser.add_argument("--activate", action="store_true", help="Set status to active immediately")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.hygiene import add_rule, activate_rule
        conn = _get_conn()
        status = "active" if args.activate else "pending"
        result = add_rule(conn, args.rule_type, args.source,
                          sender_pattern=args.sender, age_days=args.age_days,
                          threshold=args.threshold, status=status,
                          description=args.description)
        if args.as_json:
            _print_json(result)
        else:
            print(f"Rule added (id={result['id']}, status={result['status']}): {result.get('description', '')}")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def hygiene_list() -> None:
    """List hygiene rules. Entry point for hygiene-list shortcut."""
    parser = argparse.ArgumentParser(prog="hygiene-list", description="List hygiene rules")
    parser.add_argument("--all", dest="include_revoked", action="store_true", help="Include revoked rules")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.hygiene import get_all_rules
        conn = _get_conn()
        results = get_all_rules(conn, include_revoked=args.include_revoked)
        if args.as_json:
            _print_json(results)
        else:
            if not results:
                print("No hygiene rules.")
                return
            for r in results:
                runs = f" (runs: {r['total_runs']}, affected: {r['total_affected']})" if r["total_runs"] else ""
                print(f"  #{r['id']} [{r['status'].upper()}] {r['rule_type']} on {r['source']}: "
                      f"{r.get('description', '')}{runs}")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def hygiene_revoke() -> None:
    """Revoke a hygiene rule. Entry point for hygiene-revoke shortcut."""
    parser = argparse.ArgumentParser(prog="hygiene-revoke", description="Revoke a hygiene rule")
    parser.add_argument("rule_id", type=int, help="Rule ID to revoke")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.hygiene import revoke_rule
        conn = _get_conn()
        result = revoke_rule(conn, args.rule_id)
        if args.as_json:
            _print_json(result)
        elif result:
            print(f"Rule #{args.rule_id} revoked: {result.get('description', '')}")
        else:
            print(f"Rule #{args.rule_id} not found.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def hygiene_dry_run() -> None:
    """Preview what rules would affect. Entry point for hygiene-dry-run shortcut."""
    parser = argparse.ArgumentParser(prog="hygiene-dry-run", description="Dry-run hygiene rules")
    parser.add_argument("--rule-id", type=int, default=None, help="Specific rule ID (default: all active)")
    parser.add_argument("--report", choices=["whatsapp", "stdout"], default="stdout")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.hygiene_dry_run import dry_run_rule, dry_run_all, send_dry_run_report
        conn = _get_conn()
        if args.report == "whatsapp":
            result = send_dry_run_report(conn, rule_id=args.rule_id)
            if args.as_json:
                _print_json(result)
            else:
                print(f"Dry-run report sent to WhatsApp ({result.get('whatsapp', 'unknown')})")
        else:
            if args.rule_id:
                results = [dry_run_rule(conn, args.rule_id)]
            else:
                results = dry_run_all(conn)
            if args.as_json:
                _print_json(results)
            else:
                for r in results:
                    if "error" in r:
                        print(f"  Rule #{r.get('rule_id', '?')}: {r['error']}")
                    else:
                        print(f"  Rule #{r['rule_id']}: {r['description']}")
                        print(f"    Would affect: {r['would_affect']} items")
                        if r.get("sample_subjects"):
                            for s in r["sample_subjects"][:3]:
                                print(f"    - {s}")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def hygiene_execute() -> None:
    """Execute active hygiene rules. Entry point for hygiene-execute shortcut."""
    parser = argparse.ArgumentParser(prog="hygiene-execute", description="Execute hygiene rules")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout in minutes (default: 60)")
    parser.add_argument("--report", choices=["whatsapp", "stdout"], default="stdout")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.hygiene_executor import execute_rules
        conn = _get_conn()
        results = execute_rules(conn, timeout_minutes=args.timeout,
                                report_whatsapp=(args.report == "whatsapp"))
        if args.as_json:
            _print_json(results)
        else:
            for rule_id, info in results.items():
                print(f"  Rule #{rule_id}: {info['status']} — {info['processed']} items processed")
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


def hygiene_analyse() -> None:
    """Analyse accounts for hygiene opportunities. Entry point for hygiene-analyse shortcut."""
    parser = argparse.ArgumentParser(prog="hygiene-analyse", description="Analyse hygiene opportunities")
    parser.add_argument("--top", type=int, default=5, help="Top N recommendations")
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    try:
        from src.memory.hygiene_analyser import analyse_hygiene, format_recommendations
        results = analyse_hygiene(top_n=args.top)
        if args.as_json:
            _print_json(results)
        else:
            print(format_recommendations(results))
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"Error in {current_function}: {e}", file=sys.stderr)
        logger.warning(f"Error in {current_function}: {e}")
        sys.exit(1)


# ── Main entry point ────────────────────────────────────────────────


def main() -> None:
    """CLI entry point for python -m tools memory."""
    parser = argparse.ArgumentParser(
        prog="python -m tools memory",
        description="Memory system CLI",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("add-event", help="Add an episodic event")
    sub.add_parser("add-task", help="Add a task")
    sub.add_parser("add-fact", help="Add a semantic fact")
    sub.add_parser("tasks", help="List open/overdue tasks")
    sub.add_parser("done", help="Complete a task by ID")
    sub.add_parser("recent", help="Show recent events")
    sub.add_parser("search", help="Search across all tiers")
    sub.add_parser("context", help="Show full briefing context")
    sub.add_parser("distill", help="Extract memories from text")
    sub.add_parser("maintain", help="Run maintenance")
    sub.add_parser("curate", help="Curate semantic facts")
    sub.add_parser("brief-action", help="Act on brief items")
    sub.add_parser("wa-poll", help="Poll WhatsApp for pa: commands")
    sub.add_parser("hygiene-add", help="Add a hygiene rule")
    sub.add_parser("hygiene-list", help="List hygiene rules")
    sub.add_parser("hygiene-revoke", help="Revoke a hygiene rule")
    sub.add_parser("hygiene-dry-run", help="Preview rule effects")
    sub.add_parser("hygiene-execute", help="Execute active rules")
    sub.add_parser("hygiene-analyse", help="Analyse hygiene opportunities")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Map subcommands to entry points
    dispatch = {
        "add-event": add_event,
        "add-task": add_task,
        "add-fact": add_fact,
        "tasks": list_tasks,
        "done": done,
        "recent": recent,
        "search": search,
        "context": context,
        "distill": distill,
        "maintain": maintain,
        "curate": curate,
        "brief-action": brief_action,
        "wa-poll": wa_poll,
        "hygiene-add": hygiene_add,
        "hygiene-list": hygiene_list,
        "hygiene-revoke": hygiene_revoke,
        "hygiene-dry-run": hygiene_dry_run,
        "hygiene-execute": hygiene_execute,
        "hygiene-analyse": hygiene_analyse,
    }

    fn = dispatch[args.command]
    sys.argv = [f"memory-{args.command}"] + sys.argv[2:]
    fn()


if __name__ == "__main__":
    main()
