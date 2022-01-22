import click
from data.clusters import CLUSTERS
from lib.tenant_info import ldap_tenant_info


@click.group()
def cli():
    pass


@click.command()
@click.option("--tenant", required=True, help="tenant name")
@click.option("--cluster", required=True, type=click.Choice(CLUSTERS.keys()), help="cluster name")
def tenant(tenant, cluster):
    ldap_tenant_info(tenant, cluster)
