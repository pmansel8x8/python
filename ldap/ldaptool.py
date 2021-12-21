import sys
import ldap
import ldap.asyncsearch
from rich.console import Console
from rich.table import Table
from rich.style import Style
from data.clusters import EN1_CLUSTERS, PROD_CLUSTERS
from data.filters_attrs import TENANT_ATTRS, TENANT_FILTER


ldap.PORT = 8389

LDAP_BASE_DN = "o=whitepj.net"
LDAP_USER = "cn=Directory Manager,o=whitepj.net"
LDAP_PWD = "ST1013ba"
TENANT_FILTER = "(objectClass=wpj-tenant)"


def get_tenant_list(ldap_uri: str) -> None:
    l = ldap.initialize(ldap_uri)
    l.simple_bind_s(LDAP_USER, LDAP_PWD)
    r = l.search_s(LDAP_BASE_DN, ldap.SCOPE_ONELEVEL, TENANT_FILTER, ["wpj-tenant-obj-id"])
    for dn, entry in r:
        print("Processing", repr(dn))
    return


def get_tenant_list_async(uri: str) -> None:
    ldap_uri = f"ldap://{uri}:{ldap.PORT}"
    l = ldap.initialize(ldap_uri)
    l.simple_bind_s(LDAP_USER, LDAP_PWD)
    s = ldap.asyncsearch.List(
        l,
    )

    s.startSearch(LDAP_BASE_DN, ldap.SCOPE_ONELEVEL, TENANT_FILTER, TENANT_ATTRS)

    try:
        partial = s.processResults()
    except ldap.SIZELIMIT_EXCEEDED:
        sys.stderr.write("Warning: Server-side size limit exceeded.\n")
    else:
        if partial:
            sys.stderr.write("Warning: Only partial results received.\n")

    # sys.stdout.write("%d results received.\n" % (len(s.allResults)))

    table = Table(title=f"Tenant List ({len(s.allResults)})")
    table.add_column("Tenant ID")
    table.add_column("ACD #", justify="center")
    table.add_column("Enabled", justify="center")
    table.add_column("Timezone", justify="center")
    table.add_column("PBX ID")
    table.add_column("Mode #", justify="center")
    table.add_column("OEM", justify="center")
    table.add_column("Language", justify="center")
    table.add_column("Email Service", justify="center")
    table.add_column("Created on", justify="center")
    table.add_column("Last modified on", justify="center")
    for _, res_data in s.allResults:
        _, entry = res_data
        elements = []
        elements.append(entry["wpj-tenant-obj-id"][0].decode())
        elements.append(entry["wpj-acd-num"][0].decode())
        elements.append(entry["wpj-enabled"][0].decode())
        elements.append(entry["wpj-tenant-timezone"][0].decode())
        tenant_mode = "1"
        if "wpj-pbx-id" in entry and entry["wpj-pbx-id"][0].decode():
            tenant_pbx_id = entry["wpj-pbx-id"][0].decode()
            if "wpj-vcc-only" in entry:
                if entry["wpj-vcc-only"][0].decode() == "yes":
                    tenant_mode = "3"
                else:
                    tenant_mode = "2"
        else:
            tenant_pbx_id = "NOT_SET"
        elements.append(tenant_pbx_id)
        elements.append(tenant_mode)
        elements.append(entry["wpj-oem-name"][0].decode())
        elements.append(entry["wpj-language-id"][0].decode())
        if "wpj-tenant-email-serviced" in entry and entry["wpj-tenant-email-service"][0].decode():
            tenant_email_service = entry["wpj-tenant-email-service"][0].decode()
        else:
            tenant_email_service = "FETCHMAIL"
        elements.append(tenant_email_service)
        elements.append(entry["createTimestamp"][0].decode())
        elements.append(entry["modifyTimestamp"][0].decode())
        if entry["wpj-enabled"][0].decode() == "yes":
            style = "[green bold]"
        elif entry["wpj-enabled"][0].decode() == "no":
            style = "[red strike]"
        else:
            style = "[pink italic]"
        elements[0] = f"{style}{elements[0]}"
        table.add_row(*elements)
    console = Console()
    console.print(table)

    # base_style = Style.parse("cyan")
    # console.print("Hello, World", style = base_style + Style(underline=True))

    # style_enabled = Style(color="green", bgcolor="yellow", italic=True)
    # style = Style.parse("italic magenta on yellow")

    return


def main():
    clusters = EN1_CLUSTERS
    # clusters = PROD_CLUSTERS
    get_tenant_list_async(clusters["B50"])


if __name__ == "__main__":
    main()
