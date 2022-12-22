import xmlrpc.client

PORT = 8069
URL = f"http://localhost:{PORT}"
DB = "dev01"
COMMON = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')


def connect(login, password):
    return COMMON.authenticate(DB, login, password, {})
