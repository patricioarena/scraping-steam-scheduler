class Item(object):
    def __init__(self, name=None, link=None, img=None, discount=None, price_without_discounted=None, price_with_discounted=None):
        self.name = name
        self.link = link
        self.img = img
        self.discount = discount
        self.price_without_discounted = price_without_discounted
        self.price_with_discounted = price_with_discounted

    def set_name(self, name):
        self.name = name

    def set_link(self, link):
        self.link = link

    def set_img(self, img):
        self.img = img

    def set_discount(self, discount):
        self.discount = discount

    def set_price_without_discounted(self, price_without_discounted):
        self.price_without_discounted = price_without_discounted

    def set_price_with_discounted(self, price_with_discounted):
        self.price_with_discounted = price_with_discounted
