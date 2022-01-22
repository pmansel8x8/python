import click
from data.clusters import CLUSTERS
from lib.tenant_list import ldap_tenant_list
from lib.schedule_list import ldap_schedule_list


@click.group()
@click.option(
    "--cluster",
    required=False,
    type=click.Choice(CLUSTERS.keys()),
    help="cluster name. omit for all clusters",
    default=None,
)
@click.option(
    "--display",
    required=False,
    type=click.Choice(["rich", "raw"]),
    help="display mode (rich or raw)",
    default="rich",
)
@click.pass_context
def cli(ctx, cluster, display):
    ctx.ensure_object(dict)
    ctx.obj["CLUSTER"] = cluster
    ctx.obj["DISPLAY"] = display


@click.command()
@click.pass_context
def tenant(ctx):
    """Get list of tenants for a cluster, or all clusters"""
    scope = ctx.obj["CLUSTER"] if ctx.obj["CLUSTER"] else "all"
    display = ctx.obj["DISPLAY"]
    ldap_tenant_list(scope, display)


@click.command()
@click.pass_context
def schedule(ctx):
    """Get list of schedules for a cluster, or all clusters"""
    scope = ctx.obj["CLUSTER"] if ctx.obj["CLUSTER"] else "all"
    display = ctx.obj["DISPLAY"]
    ldap_schedule_list(scope, display)


cli.add_command(tenant)
cli.add_command(schedule)
