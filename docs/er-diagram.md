# ER Diagram

USER (1) ----< TICKET >---- (1) CATEGORY
USER (1) ----< COMMENT >---- (1) TICKET
USER (1) ----< ATTACHMENT >- (1) TICKET
USER (1) ----< NOTIFICATION
USER (1) ----< AUDIT_LOG
USER (1) ----< REFRESH_TOKEN
TICKET (1) ----< STATUS_HISTORY

Ticket.customer_id -> users.id
Ticket.assigned_agent_id -> users.id
Ticket.category_id -> ticket_categories.id
