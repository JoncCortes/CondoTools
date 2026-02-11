from .models import AuditLog


def create_audit_log(*, user, action: str, instance):
    AuditLog.objects.create(
        user=user,
        condominium=getattr(instance, "condominium", None),
        action=action,
        model_name=instance.__class__.__name__,
        object_id=str(instance.pk),
        payload={},
    )
