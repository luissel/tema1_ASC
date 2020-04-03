"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """

        Thread.__init__(self, **kwargs)
        self.kwargs = kwargs
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

        """
        Fiecare consumator are un id pentru cosul sau de cumparaturi.
        """
        self.cart_id = self.marketplace.new_cart()

    def run(self):
        """
        Parcurg listele cu operatiile facute de consumator si le aplic.
        La final, afisez ce produse a cumparat cosnumatorul respectiv.
        """
        for current_list in self.carts:
            for operation in current_list:
                operation_type = operation['type']
                product = operation['product']
                quantity = operation['quantity']

                if operation_type == 'add':
                    for _ in range(quantity):
                        while self.marketplace.add_to_cart(self.cart_id, product) is False:
                            time.sleep(self.retry_wait_time)
                else:
                    for _ in range(quantity):
                        self.marketplace.remove_from_cart(self.cart_id, product)

        products = self.marketplace.place_order(self.cart_id)
        for current_product in products:
            print("%s bought %s" % (self.kwargs['name'], current_product))
