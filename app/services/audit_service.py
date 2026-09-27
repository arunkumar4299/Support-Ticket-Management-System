from app.models.audit_log import AuditLog
def log_action(db, user_id, action, entity, entity_id=None, ip_address=None, metadata=None):
    log = AuditLog(user_id=user_id, action=action, entity=entity, entity_id=entity_id,
                   ip_address=ip_address, metadata_json=metadata)
    db.add(log)
    return log
