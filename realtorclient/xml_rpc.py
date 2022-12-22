import xmlrpc.client

PORT = 8069
URL = f"http://localhost:{PORT}"
DB = "dev01"
COMMON = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
MODELS = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')


def connect(login, password):
    return COMMON.authenticate(DB, login, password, {})


def get_apartments(uid, password, table='realtor.apartment', mode='search_read'):
    apartments = MODELS.execute_kw(
        DB, uid, password, table, mode, [],
        {'fields': [
            'name',
            'img',
            'availability_date',
            'expected_price',
            'apartment_area',
            'terrace_area',
            'total_area',
            'user_id',
            'best_price',
        ]})
    products = MODELS.execute_kw(
        DB, uid, password, 'product.product', mode, [],
        {'fields': [
            'apart_id', 'qty_available']})

    # Align apartments and products and the same ids since 'apart_id' refers to 'id'
    apartments = sorted(apartments, key=lambda x: x['id'])
    products = sorted(products, key=lambda x: x['apart_id'])

    for apart, prod in zip(apartments, products):
        apart['quantity'] = prod['qty_available']
        apart['user_id'] = apart['user_id'][1]  # Keep the seller's name but not the ID, format is [1, "name"] otherwise

    return apartments
