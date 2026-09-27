from fastapi import APIRouter

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get("/")
def get_notifications():
    return {
        "message": "Notifications retrieved successfully",
        "notifications": []
    }


@router.get("/{notification_id}")
def get_notification(notification_id: int):
    return {
        "id": notification_id,
        "message": "Notification retrieved successfully"
    }


@router.patch("/{notification_id}/read")
def mark_notification_as_read(notification_id: int):
    return {
        "id": notification_id,
        "message": "Notification marked as read"
    }