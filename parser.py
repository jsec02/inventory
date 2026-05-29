#!/usr/bin/env python

# ================================================================================
# =                                    PARSER                                    =
# ================================================================================

import argparse
import sys
from pathlib import Path

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("machines")

    paths = subparsers.add_parser("paths")
    paths.add_argument("machine")

    links = subparsers.add_parser("links")
    links.add_argument("machine")

    packages = subparsers.add_parser("packages")
    packages.add_argument("machine")
    packages.add_argument("package_manager")

    package_managers = subparsers.add_parser("package_managers")
    package_managers.add_argument("machine")

    subparsers.add_parser("all_package_managers")

    return parser.parse_args()


def load_inventory() -> dict:
    with open(Path.home() / "inventory" / "inventory.yaml") as f:
        return yaml.safe_load(f)


def get_machines(inventory: dict) -> None:
    print(*inventory["machines"].keys())


def get_paths(inventory: dict, machine: str) -> None:
    if machine not in inventory["machines"]:
        print(f"Unknown machine: {machine}", file=sys.stderr)
        sys.exit(1)

    for key, value in inventory.items():
        if "paths" in value and machine in value["machines"]:
            print(key, *value["paths"])


def get_links(inventory: dict, machine: str) -> None:
    if machine not in inventory["machines"]:
        print(f"Unknown machine: {machine}", file=sys.stderr)
        sys.exit(1)

    for value in inventory.values():
        if "links" in value and machine in value["machines"]:
            for source, target in value["links"].items():
                print(source, target)


def get_packages(inventory: dict, machine: str, package_manager: str) -> None:
    if machine not in inventory["machines"]:
        print(f"Unknown machine: {machine}", file=sys.stderr)
        sys.exit(1)

    if package_manager not in inventory["machines"][machine]["package_managers"]:
        print(
            f"Invalid package manager for {machine}: {package_manager}", file=sys.stderr
        )
        sys.exit(1)

    print(*inventory["machines"][machine]["package_managers"][package_manager])


def get_package_managers(inventory: dict, machine: str) -> None:
    if machine not in inventory["machines"]:
        print(f"Unknown machine: {machine}", file=sys.stderr)
        sys.exit(1)

    print(*inventory["machines"][machine]["package_managers"].keys())


def main() -> None:
    inventory = load_inventory()

    args = parse_args()

    if args.command == "machines":
        get_machines(inventory)

    elif args.command == "paths":
        get_paths(inventory, args.machine)

    elif args.command == "links":
        get_links(inventory, args.machine)

    elif args.command == "packages":
        get_packages(inventory, args.machine, args.package_manager)

    elif args.command == "package_managers":
        get_package_managers(inventory, args.machine)


if __name__ == "__main__":
    main()
