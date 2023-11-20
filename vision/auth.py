# A means by authenticating Vision users using LDAP/AD, checking
# to make sure that the user is a member of the Vision user group
from ldap3 import Connection, Server, ALL
from config import LDAP_HOST, LDAP_BASE_DN, LDAP_VISION_GROUP, LDAP_USER_OU

ad_server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
ad_vision_group = f"{LDAP_VISION_GROUP},{LDAP_BASE_DN}"


def authenticate_user(username, password):
    try:
        with Connection(
            ad_server,
            user=f"CN={username},OU={LDAP_USER_OU},{LDAP_BASE_DN}",
            password=password,
        ) as conn:
            if conn.bind():
                if conn.search(
                    ad_vision_group,
                    "(member={})".format(conn.user),
                    attributes=["member"],
                ):
                    return True
                else:
                    return False
            else:
                return False  # Successful authenticate, but not member of group
    except Exception as e:
        return False
