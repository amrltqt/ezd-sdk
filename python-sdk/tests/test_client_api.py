import pytest

from ezd.api.client import EZDClient


def test_constructor():
    client = EZDClient("https://foo.bar", "azerty")
    assert client.base_url == "https://foo.bar"
    assert client.api_key == "azerty"


def test_constructor_from_env(monkeypatch):
    client = EZDClient.from_env()

    assert client.base_url == "https://api.ezd.amrltqt.com"
    assert client.api_key is None

    monkeypatch.setenv("EZD_API_URL", "https://foo.bar")
    monkeypatch.setenv("EZD_API_KEY", "azerty")

    client = EZDClient.from_env()

    assert client.base_url == "https://foo.bar"
    assert client.api_key == "azerty"


def test_get_headers():
    client = EZDClient("https://foo.bar")

    assert client._get_headers() == {"Content-Type": "application/json"}

    client = EZDClient("https://foo.bar", "azerty")
    assert client._get_headers() == {
        "Content-Type": "application/json",
        "Authorization": "Bearer azerty",
    }


def test_list_dashboard(requests_mock):
    base_url = "mock://api_server"
    client = EZDClient(base_url)
    requests_mock.get(f"{base_url}/dashboards", json={"results": ["a", "b", "c"]})
    assert client.list_dashboards() == ["a", "b", "c"]


def test_get_dashboard(requests_mock):
    base_url = "mock://api_server"
    dashboard_id = 42
    client = EZDClient(base_url)
    requests_mock.get(
        f"{base_url}/dashboards/{dashboard_id}", json={"a": 42, "b": "test"}
    )
    assert client.get_dashboard(dashboard_id) == {"a": 42, "b": "test"}
