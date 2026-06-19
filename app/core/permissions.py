from app.models.enums import UserRole


def is_admin(user):
    return str(user.role).upper() == "ADMIN"


def is_manager(user):
    return str(user.role).upper() == "MANAGER"


def is_employee(user):
    return str(user.role).upper() == "EMPLOYEE"


def is_admin_or_manager(user):
    return str(user.role).upper() in [
        "ADMIN",
        "MANAGER"
    ]