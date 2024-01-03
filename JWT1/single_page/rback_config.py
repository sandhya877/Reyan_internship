from enum import Enum

class ROLES(str,Enum):
    END_USER = "END_USER",
    MODERATOR = "MODERATOR",
    ADMIN = "ADMIN",
    ROOT = "ROOT"


class FastApiRBACMaster:
    def RBAC(self,allowed_roles,incoming_role):
        allowed_roles_values = [role.value.lower() for role in allowed_roles]
        print(allowed_roles_values)
        print(incoming_role)
        if incoming_role == ROLES.ROOT:
            return True
        else:
            return incoming_role in allowed_roles_values