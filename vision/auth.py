# A means by authenticating Vision users using LDAP/AD, checking
# to make sure that the user is a member of the Vision user group
from ldap3 import Connection, Server, ALL
# from ldap3.core import LDAPException, LDAPBindError
from config import LDAP_HOST
from os import urandom
from functools import wraps

ad_server = Server(LDAP_HOST, get_info=ALL)
ad_base_dn = 'DC=domain3,DC=local'
ad_vision_group = 'CN=vision_users,OU=Groups,' + ad_base_dn

def authenticate_user(username, password):
    try:
        with Connection(ad_server, user=f'CN={username},OU=users,{ad_base_dn}', password=password) as conn:
            if conn.bind():
                if conn.search(ad_vision_group, '(member={})'.format(conn.user), attributes=['member']):
                    return True
                else:
                    return False
            else:
                return False # Successful authenticate, but not member of group
    except Exception as e:
        # app.logger.error(f"LDAP authentication error: {str(e)}")
        return False
