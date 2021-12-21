import sys
import ldap
import ldap.asyncsearch
from datetime import datetime
from rich import box
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from data.clusters import CLUSTERS
from data.filters_attrs import LDAP_FILTERS, LDAP_OBJ_ATTRS
from data.constants import LDAP_BASE_DN, LDAP_USER, LDAP_PWD


class Header:
    def __init__(self, tenant: str, cluster: str) -> None:
        self._title = f"[b]{tenant}[/b] (cluster: {cluster})"

    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            self._title,
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")


def get_pbx_id_and_mode(data: dict) -> tuple[str, str]:
    tenant_pbx_id = "NOT_SET"
    tenant_mode = "1"
    if "wpj-pbx-id" in data and data["wpj-pbx-id"][0].decode():
        tenant_pbx_id = data["wpj-pbx-id"][0].decode()
        if "wpj-vcc-only" in data:
            if data["wpj-vcc-only"][0].decode() == "yes":
                tenant_mode = "3"
            else:
                tenant_mode = "2"
    return tenant_pbx_id, tenant_mode


def get_tenant_email_service(data: dict) -> str:
    tenant_email_service = "FETCHMAIL"
    if "wpj-tenant-email-serviced" in data and data["wpj-tenant-email-service"][0].decode():
        tenant_email_service = data["wpj-tenant-email-service"][0].decode()
    return tenant_email_service


def format_status(data: dict) -> str:
    if data["wpj-enabled"][0].decode() == "yes":
        style = "[green bold]"
    elif data["wpj-enabled"][0].decode() == "no":
        style = "[red strike]"
    else:
        style = "[pink italic]"

    return f'{style}{data["wpj-enabled"][0].decode()}'


def display_tenant_info(data: dict) -> Panel:
    """Display the tenant attributes in the tenantbox layout"""
    tenant_attrs = Table.grid(padding=1)
    tenant_attrs.add_column(style="blue", justify="left")
    tenant_attrs.add_column(no_wrap=True, justify="left")
    tenant_attrs.add_row(
        "Tenant ID:",
        data["wpj-tenant-obj-id"][0].decode(),
    )
    tenant_attrs.add_row(
        "ACD #:",
        data["wpj-acd-num"][0].decode(),
    )
    tenant_attrs.add_row(
        "Status:",
        format_status(data),
    )
    tenant_attrs.add_row(
        "Timezone:",
        data["wpj-tenant-timezone"][0].decode(),
    )
    tenant_attrs.add_row(
        "Language:",
        data["wpj-language-id"][0].decode(),
    )
    tenant_attrs.add_row(
        "OEM:",
        data["wpj-oem-name"][0].decode(),
    )

    tenant_pbx_id, tenant_mode = get_pbx_id_and_mode(data)

    tenant_attrs.add_row(
        "PBX ID:",
        tenant_pbx_id,
    )
    tenant_attrs.add_row(
        "Mode #:",
        tenant_mode,
    )
    tenant_attrs.add_row(
        "Email Service:",
        get_tenant_email_service(data),
    )
    tenant_attrs.add_row(
        "Creation Timestamp:",
        data["createTimestamp"][0].decode(),
    )
    tenant_attrs.add_row(
        "Last Modification Timestamp:",
        data["modifyTimestamp"][0].decode(),
    )

    grid = Table.grid(padding=1)
    grid.add_column()
    grid.add_column(no_wrap=True)
    grid.add_row(tenant_attrs)

    panel = Panel(
        Align.center(tenant_attrs, vertical="middle"),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Tenant attributes",
        border_style="bright_blue",
    )
    return panel


def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=7),
    )
    layout["main"].split_row(
        Layout(name="side", ratio=2),
        Layout(name="body", ratio=5, minimum_size=60),
    )
    layout["side"].split(Layout(name="tenant", ratio=3), Layout(name="db", ratio=1))

    layout["body"].split_row(
        Layout(name="agentgroup"),
        Layout(name="queuechannel"),
    )
    layout["agentgroup"].split(Layout(name="agent"), Layout(name="group"))

    layout["queuechannel"].split(Layout(name="queue"), Layout(name="channel"))

    return layout


def display_results(tenant: str, cluster: str, results: list):

    layout = make_layout()
    layout["header"].update(Header(tenant, cluster))
    layout["tenant"].update(display_tenant_info(results))

    console = Console()
    console.print(layout)
    return


def ldap_tenant_info(tenant: str, cluster: str) -> None:
    ldap_uri = f"ldap://{CLUSTERS[cluster]}:{ldap.PORT}"
    l = ldap.initialize(ldap_uri)
    l.simple_bind_s(LDAP_USER, LDAP_PWD)
    s = ldap.asyncsearch.List(
        l,
    )

    dn = f"wpj-tenant-obj-id={tenant},{LDAP_BASE_DN}"
    s.startSearch(dn, ldap.SCOPE_BASE, LDAP_FILTERS["tenant"], LDAP_OBJ_ATTRS["tenant-info"])

    try:
        partial = s.processResults()
    except ldap.SIZELIMIT_EXCEEDED:
        sys.stderr.write("Warning: Server-side size limit exceeded.\n")
    else:
        if partial:
            sys.stderr.write("Warning: Only partial results received.\n")

    # sys.stdout.write("%d results received.\n" % (len(s.allResults)))
    if len(s.allResults) == 1:
        _, res_data = s.allResults[0]
        _, entry = res_data
        display_results(tenant, cluster, entry)

    return
