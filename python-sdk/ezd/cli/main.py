import click
import json

from ezd.api.client import EZDClient

@click.group()
def main():
    pass

@main.group()
def dashboard():
    pass

@dashboard.command()
def list():
    client = EZDClient.from_env()
    response = client.list_dashboards()

    click.echo(json.dumps(response))

@dashboard.command()
@click.argument('dashboard_id')
def show(dashboard_id):
    client = EZDClient.from_env()
    response = client.get_dashboard(dashboard_id)

    click.echo(json.dumps(response))

@dashboard.command()
@click.argument('dashboard_id')
def distribute(dashboard_id):
    client = EZDClient.from_env()
    response = client.distribute_dashboard(dashboard_id)

    click.echo(json.dumps(response))

if __name__ == '__main__':
    main()
