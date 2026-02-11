PERMISSION_REGISTRY = {
    "dashboard": ["dashboard.view"],
    "settings": [
        "settings.view",
        "settings.manage_condominiums",
        "settings.manage_users",
        "settings.manage_menu_pages",
        "settings.manage_role_permissions",
    ],
    "condominiums": ["condominiums.view", "condominiums.create", "condominiums.update", "condominiums.delete"],
    "units": ["units.view", "units.create", "units.update", "units.delete"],
    "residents": ["residents.view", "residents.create", "residents.update", "residents.delete"],
    "visitors": ["visitors.view", "visitors.create", "visitors.update", "visitors.delete", "visitors.audit_log.view"],
    "visit_logs": ["visit_logs.view", "visit_logs.create", "visit_logs.update", "visit_logs.delete", "visit_logs.checkout"],
    "packages": ["packages.view", "packages.create", "packages.update", "packages.delete", "packages.mark_delivered", "packages.audit_log.view"],
    "announcements": ["announcements.view", "announcements.create", "announcements.update", "announcements.delete"],
    "occurrences": ["occurrences.view", "occurrences.create", "occurrences.update", "occurrences.delete", "occurrences.change_status"],
    "common_areas": ["common_areas.view", "common_areas.create", "common_areas.update", "common_areas.delete"],
    "reservations": ["reservations.view", "reservations.create", "reservations.update", "reservations.delete", "reservations.approve", "reservations.cancel"],
    "profile": ["profile.view", "profile.update"],
    "service_providers": ["service_providers.view", "service_providers.create", "service_providers.update", "service_providers.delete", "service_providers.audit_log.view"],
}

PERMISSION_LABELS = {
    key: key.replace('.', ' · ').replace('_', ' ').title()
    for keys in PERMISSION_REGISTRY.values()
    for key in keys
}

ALL_PERMISSION_KEYS = [p for keys in PERMISSION_REGISTRY.values() for p in keys]

ROLE_DEFAULTS = {
    "PLATFORM_ADMIN": ALL_PERMISSION_KEYS,
    "SINDICO": [
        p for p in ALL_PERMISSION_KEYS
        if p not in {"settings.manage_role_permissions", "condominiums.delete"}
    ],
    "PORTEIRO": [
        "dashboard.view", "units.view", "residents.view",
        "visitors.view", "visitors.create", "visitors.update", "visitors.audit_log.view",
        "visit_logs.view", "visit_logs.create", "visit_logs.checkout",
        "packages.view", "packages.create", "packages.mark_delivered", "packages.audit_log.view",
        "announcements.view",
        "occurrences.view", "occurrences.create",
        "profile.view", "profile.update",
        "service_providers.view", "service_providers.create", "service_providers.update", "service_providers.audit_log.view",
    ],
    "MORADOR": [
        "dashboard.view", "profile.view", "profile.update",
        "announcements.view",
        "packages.view",
        "reservations.view", "reservations.create", "reservations.cancel",
        "occurrences.view", "occurrences.create",
    ],
}
