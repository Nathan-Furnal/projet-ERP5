import xmlrpc.client
import itertools

PORT = 8069
URL = f"http://localhost:{PORT}"
DB = "dev01"
COMMON = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
MODELS = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')


def connect(login, password):
    return COMMON.authenticate(DB, login, password, {})


def db_interact(uid, password, table, mode, fields=None):
    return MODELS.execute_kw(
        DB, uid, password, table, mode, [],
        {'fields': fields})


def get_apartments(uid, password):
    products = db_interact(uid, password, 'product.product', 'search_read', ['apart_id', 'qty_available'])
    apartments = db_interact(uid, password, 'realtor.apartment', 'search_read',
                             ['name', 'img', 'availability_date', 'expected_price', 'apartment_area',
                              'terrace_area', 'total_area', 'user_id', 'best_price'])
    offers = db_interact(uid, password, 'realtor.offer', 'search_read', ['price', 'partner_id', 'property_id'])

    # Align apartments and products and the same ids since 'apart_id' and 'property_id' refers to 'id'
    # they have the same number of elements
    apartments = sorted(apartments, key=lambda x: x['id']) # id is an int
    products = sorted(products, key=lambda x: x['apart_id'][0])  # apart_id is a list like [1, 'Apartment']
    # Offers keeps track of all the offers, but we want only the latest offer, which is the greatest in value
    offers = sorted(offers, key=lambda x: x['property_id'][0])   # property_id is a list like [1, 'Apartment']
    # Since the offers are sorted, group by property id and get the first element (the greatest) of each group
    offers = [next(g) for _, g in itertools.groupby(offers, lambda x: x['property_id'][0])]
    for apart, prod, offer in zip(apartments, products, offers):
        apart['quantity'] = prod['qty_available']
        apart['user_id'] = apart['user_id'][1]  # Keep the seller's name but not the ID, format is [1, "name"] otherwise
        # offer['partner_id'] is like [1, 'name'] so grab the first element
        # the output of execute is a list of dict, same logic and grab the only element
        apart['partner_id'] = \
            MODELS.execute_kw(DB, uid, password, 'res.partner', 'search_read', [[['id', '=', offer['partner_id'][0]]]],
                              {'fields': ['id', 'name']})[0]['name']

    return apartments


def create_offer(uid, password, partner_name, offer_amt, apart_id):
    partner = MODELS.execute_kw(DB, uid, password, 'res.partner', 'search_read', [
        [['name', '=', partner_name]]], {'fields': ['id', 'name']})
    if not partner:
        partner_id = MODELS.execute_kw(DB, uid, password, 'res.partner', 'create', [{'name': partner_name}])
    else:
        partner_id = partner[0]['id']  # Same issue with the result of a search_read query

    MODELS.execute_kw(DB, uid, password, 'realtor.offer', 'create', [{'price': offer_amt,
                                                                      'partner_id': partner_id,
                                                                      'property_id': apart_id}])
