#!/usr/bin/env python3
"""Mock manage.py for testing django-migration-fixer action."""
import sys

def main():
    args = sys.argv[1:]
    print(f"manage.py called with args: {args}")

    if not args:
        print("No command provided")
        sys.exit(1)

    command = args[0]
    if command != "makemigrations":
        print(f"Unknown command: {command}")
        sys.exit(1)

    # Parse flags
    if "--fix" not in args:
        print("ERROR: --fix flag not provided")
        sys.exit(1)

    if "-b" not in args:
        print("ERROR: -b flag not provided")
        sys.exit(1)

    branch_idx = args.index("-b")
    if branch_idx + 1 >= len(args):
        print("ERROR: -b flag requires a branch name")
        sys.exit(1)

    branch = args[branch_idx + 1]
    print(f"Branch: {branch}")

    force_update = "-f" in args
    skip_update = "-s" in args

    print(f"Force update: {force_update}")
    print(f"Skip default branch update: {skip_update}")
    print("Migration fix completed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
