from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserPermission(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE = "manage"

ROLE_PERMISSIONS = {
    UserRole.USER: [UserPermission.READ],
    UserRole.ADMIN: [UserPermission.READ, UserPermission.WRITE, UserPermission.DELETE, UserPermission.MANAGE]
}
