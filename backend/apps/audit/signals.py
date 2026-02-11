from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from apps.common.current_user import get_current_user

from .models import AuditLog

_PREVIOUS_VALUES = {}


def _key(sender, instance):
    return f"{sender.__name__}:{instance.pk}"


@receiver(pre_save)
def cache_previous_state(sender, instance, **kwargs):
    if sender is AuditLog or not instance.pk:
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
def create_or_update_audit(sender, instance, created, **kwargs):
    if sender is AuditLog or sender._meta.app_label in {"sessions", "admin", "contenttypes"}:
        return
    user = get_current_user()
    previous = _PREVIOUS_VALUES.pop(_key(sender, instance), {})
    changes = {}
    if not created and previous:
        for field, old_val in previous.items():
            new_val = getattr(instance, field)
            if str(old_val) != str(new_val):
                changes[field] = {"old": str(old_val), "new": str(new_val)}
    AuditLog.objects.create(
        user=user,
        action="CREATE" if created else "UPDATE",
        model=sender.__name__,
        object_id=str(instance.pk),
        condominium=getattr(instance, "condominium", None),
        changes=changes,
    )


@receiver(post_delete)
def delete_audit(sender, instance, **kwargs):
    if sender is AuditLog or sender._meta.app_label in {"sessions", "admin", "contenttypes"}:
        return
    user = get_current_user()
    AuditLog.objects.create(
        user=user,
        action="DELETE",
        model=sender.__name__,
        object_id=str(instance.pk),
        condominium=getattr(instance, "condominium", None),
        changes={},
    )
