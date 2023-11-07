import pytest

from docopt import docopt

from ezd.cli import main


def test_cli_api():
    cli_interface = main.__doc__
    parsing = docopt(cli_interface, "dashboard")
    assert "dashboard" in parsing and parsing["dashboard"]

    parsing = docopt(cli_interface, "dashboard -d 42")
    assert "dashboard" in parsing and parsing["dashboard"]
    assert "--dashboard-id" in parsing
    assert parsing["--dashboard-id"] == "42"

    parsing = docopt(cli_interface, "dashboard distribute -d 42")
    assert "dashboard" in parsing and parsing["dashboard"]
    assert "distribute" in parsing and parsing["distribute"]
    assert "--dashboard-id" in parsing
    assert parsing["--dashboard-id"] == "42"

    result = docopt(cli_interface, "dashboard -u mock://server.api -k azerty")
    partial_except = {
        "dashboard": True,
        "--api-url": "mock://server.api",
        "--api-key": "azerty",
    }
    assert set(partial_except.items()).issubset(set(result.items()))


def test_arguments_interpretation():
    client, command, arguments = main.interpret_command({"dashboard": True})
    assert command.__name__ == "list_dashboard"

    client, command, arguments = main.interpret_command(
        {"dashboard": True, "--dashboard-id": "42"}
    )
    assert command.__name__ == "show_dashboard"
    assert arguments == ["42"]

    client, command, arguments = main.interpret_command(
        {"dashboard": True, "distribute": True, "--dashboard-id": "42"}
    )
    assert command.__name__ == "distribute_dashboard"
    assert arguments == ["42"]

    client, command, arguments = main.interpret_command(
        {"dashboard": True, "--api-url": "mock://server.api", "--api-key": "azerty"}
    )
    assert client.api_key == "azerty"
    assert client.base_url == "mock://server.api"
