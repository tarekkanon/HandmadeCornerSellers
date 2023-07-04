from flask_login import UserMixin

class Seller(UserMixin):
    id = 0
    email = ''
    password = ''

    def __init__(self, sellerObj):
        self.id = sellerObj['SellerId']
        self.email = sellerObj['SellerEmail']
        self.password = sellerObj['SellerPassword']
        self._authenticated = True
        self._active = True

    @property
    def is_active(self):
        return self._active

    @property
    def is_authenticated(self):
        return self._authenticated

    @is_authenticated.setter
    def is_authenticated(self, value):
        if value:
            self._authenticated = True
        else:
            self._authenticated = False

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id