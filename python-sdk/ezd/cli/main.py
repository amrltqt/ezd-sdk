"""Ezd CLIent

Usage:
    main.py dashboard distribute --dashboard-id DASHBOARD_ID [-u URL] [-k API_KEY]
    main.py dashboard [--dashboard-id=<dashboard_id>] [-u URL] [-k API_KEY]

Options:
    -h --help                                     Show this screen.
    --version                                     Show version.
    -u URL, --api-url URL                         Url endpoints to the Ezd API
    -k API_KEY, --api-key API_KEY                 Ezd API key
    -d DASHBOARD_ID, --dashboard-id DASHBOARD_ID  Target dashboard id

Commands:
    dashboard             Dashborad manipulation command, if no id list all dashboards
    dashboard distribute  Distribute the dashboard to targets
"""
from docopt import docopt
import json
from typing import Tuple, Callable

from ezd.api.client import EZDClient


def interpret_command(arguments: dict) -> Tuple[EZDClient, Callable, list]:
    client = EZDClient.from_env()

    if arguments.get("--api-url", False):
        client.base_url = arguments["--api-url"]

    if arguments.get("--api-key", False):
        client.api_key = arguments["--api-key"]

    command = lambda x: x
    args = list()

    if arguments.get("dashboard", False) and arguments.get("distribute", False):
        command = distribute_dashboard
        args.append(arguments["--dashboard-id"])
    elif (
        arguments.get("dashboard", False)
        and arguments.get("--dashboard-id", None) is not None
    ):
        command = show_dashboard
        args.append(arguments["--dashboard-id"])
    elif arguments.get("dashboard", False):
        command = list_dashboard

    return (client, command, args)


def list_dashboard(client):
    response = client.list_dashboards()
    print(json.dumps(response, indent=2))


def show_dashboard(client, dashboard_id):
    response = client.get_dashboard(dashboard_id)
    print(json.dumps(response, indent=2))


def distribute_dashboard(client, dashboard_id):
    response = client.distribute_dashboard(dashboard_id)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    arguments = docopt(__doc__, version="Ezd client SDK v1.0.0-beta")
    client, command, arguments = interpret_command(arguments)
    command(client, *arguments)
