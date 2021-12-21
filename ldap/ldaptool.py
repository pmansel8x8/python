import click
from data.clusters import CLUSTERS
from commands.tenant_list import ldap_tenant_list
from commands.tenant_info import ldap_tenant_info

# from rich.style import Style


@click.group()
def cli():
    pass


@click.command()
@click.option("--cluster", required=True, type=click.Choice(CLUSTERS.keys()), help="cluster name")
def tenant_list(cluster):
    ldap_tenant_list(cluster)


@click.command()
@click.option("--tenant", required=True, help="tenant name")
@click.option("--cluster", required=True, type=click.Choice(CLUSTERS.keys()), help="cluster name")
def tenant_info(tenant, cluster):
    ldap_tenant_info(tenant, cluster)


cli.add_command(tenant_list)
cli.add_command(tenant_info)

if __name__ == "__main__":
    cli()
