
from enum import Enum

class EndpointURLs(Enum):
    '''
        Customers endpoint urls
    '''
    CUSTOMERS = 'customers/'

    '''
        Sellers endpoint urls
    '''
    SELLERS_NEW = 'sellers/'
    SELLERS_LOGIN = 'sellers/login'
    SELLERS_LOGIN_SESSION = 'sellers/login_session'
    SELLERS_UPDATE = 'sellers/update'
    SELLERS_UPDATE_PASSWORD = 'sellers/update_password'

    '''
        Orders endpoint urls
    '''
    ORDERS = 'orders/'

    '''
        Products endpoint urls
    '''
    PRODUCTS = 'products/'

    '''
        Reviews endpoint urls
    '''
    REVIEWS = 'reviews/'

    '''
        Shipments endpoint urls
    '''
    SHIPMENTS = 'shipments/'

    '''
        Categories endpoint urls
    '''
    CATEGORIES = 'categories/'

    '''
        Sub categories endpoint urls
    '''
    SUBCATEGORIES = 'subcategories/'

    '''
        Tags endpoint urls
    '''
    TAG = 'tag/'


class EndpointBuilder():
    def __init__(self):
        self.BaseURL = 'http://127.0.0.1:8523/'

    def BuildURL(self, endpoint = EndpointURLs):
        return self.BaseURL + endpoint.value