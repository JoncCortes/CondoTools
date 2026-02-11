from django.db import OperationalError, ProgrammingError, connection
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from apps.common.current_user import get_current_user

from .models import AuditLog

_PREVIOUS_VALUES = {}
_ALLOWED_APP_LABELS = {
    "accounts",
    "condominiums",
    "units",
    "residents",
    "staff",
    "visitors",
    "packages",
    "announcements",
    "incidents",
    "common_areas",
    "reservations",
    "visit_logs",
    "settings_menu",
}


def _key(sender, instance):
    return f"{sender.__name__}:{instance.pk}"


def _should_audit(sender) -> bool:
    if sender is AuditLog:
        return False
    return sender._meta.app_label in _ALLOWED_APP_LABELS


def _audit_table_exists() -> bool:
    try:
        return AuditLog._meta.db_table in connection.introspection.table_names()
    except Exception:
        return False


def _safe_create_audit(**kwargs):
    try:
        AuditLog.objects.create(**kwargs)
    except (ProgrammingError, OperationalError):
        # During initial migrate/deploy the audit table may not exist yet.
        return


@receiver(pre_save)
def cache_previous_state(sender, instance, **kwargs):
    if not _should_audit(sender) or not instance.pk or not _audit_table_exists():
        return
    try:
        old = sender.objects.get(pk=instance.pk)
    except Exception:
        return
    _PREVIOUS_VALUES[_key(sender, instance)] = {
        field.name: getattr(old, field.name)
        for field in sender._meta.fields
        if field.name not in {"id", "created_at", "updated_at"}
    }


@receiver(post_save)
def create_or_update_audit(sender, instance, created, raw=False, **kwargs):
    if raw or not _should_audit(sender):
        return

    user = get_current_user()
    previous = _PREVIOUS_VALUES.pop(_key(sender, instance), {})
    changes = {}
    if not created and previous:
        for field, old_val in previous.items():
            new_val = getattr(instance, field)
            if str(old_val) != str(new_val):
                changes[field] = {"old": str(old_val), "new": str(new_val)}

    if not _audit_table_exists():
        return

    _safe_create_audit(
        user=user,
        action="CREATE" if created else "UPDATE",
        model=sender.__name__,
        object_id=str(instance.pk),
        condominium=getattr(instance, "condominium", None),
        changes=changes,
    )


@receiver(post_delete)
def delete_audit(sender, instance, **kwargs):
    if not _should_audit(sender) or not _audit_table_exists():
        return

    user = get_current_user()
    _safe_create_audit(
        user=user,
        action="DELETE",
        model=sender.__name__,
        object_id=str(instance.pk),
        condominium=getattr(instance, "condominium", None),
        changes={},
    )
