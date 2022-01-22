import ldap

LDAP_PARAMS: dict[str, dict] = {
    "list-tenant": {
        "scope": ldap.SCOPE_ONELEVEL,
        "filter": "(objectClass=wpj-tenant)",
        "attributes": [
            "wpj-tenant-obj-id",
            "wpj-acd-num",
            "wpj-enabled",
            "wpj-tenant-email-service",
            "wpj-tenant-timezone",
            "wpj-pbx-id",
            "wpj-vcc-only",
            "wpj-oem-name",
            "wpj-language-id",
            "createTimestamp",
            "modifyTimestamp",
        ],
    },
    "list-schedule": {
        "scope": ldap.SCOPE_SUBTREE,
        "filter": "(objectClass=wpj-schedule)",
        "attributes": [
            "wpj-schedule-name",
            "wpj-schedule-timezone",
            "wpj-schedule-weekdays",
            "createTimestamp",
            "modifyTimestamp",
        ],
    },
}


LDAP_FILTERS: dict[str, str] = {
    "tenant": "(objectClass=wpj-tenant)",
    "schedule": "(objectClass=wpj-schedule)",
    "all_queues": "(objectClass=wpj-phone-queue)|(objectClass=wpj-email-queue)|(objectClass=wpj-chat-queue)|(objectClass=wpj-vmail-queue)",
}

LDAP_OBJ_ATTRS: dict[str, dict[str, list]] = {
    "list": {
        "tenant": [
            "wpj-tenant-obj-id",
            "wpj-acd-num",
            "wpj-enabled",
            "wpj-tenant-email-service",
            "wpj-tenant-timezone",
            "wpj-pbx-id",
            "wpj-vcc-only",
            "wpj-oem-name",
            "wpj-language-id",
            "createTimestamp",
            "modifyTimestamp",
        ],
        "schedule": [
            "wpj-schedule-name",
            "wpj-schedule-timezone",
            "wpj-schedule-weekdays",
            "createTimestamp",
            "modifyTimestamp",
        ],
    },
    "info": {
        "tenant": [
            "wpj-tenant-obj-id",
            "wpj-acd-num",
            "wpj-fetchmail-instance",
            "wpj-enabled",
            "wpj-current-platform-id",
            "wpj-tenant-email-service",
            "wpj-tenant-timezone",
            "wpj-pbx-id",
            "wpj-vcc-only",
            "wpj-oem-name",
            "wpj-language-id",
            "createTimestamp",
            "modifyTimestamp",
        ],
    },
}
