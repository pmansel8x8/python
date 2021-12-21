LDAP_FILTERS: dict[str, str] = {
    "tenant": "(objectClass=wpj-tenant)",
    "all_queues": "(objectClass=wpj-phone-queue)|(objectClass=wpj-email-queue)|(objectClass=wpj-chat-queue)|(objectClass=wpj-vmail-queue)",
}

LDAP_OBJ_ATTRS: dict[str, list] = {
    "tenant-list": [
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
    "tenant-info": [
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
}
