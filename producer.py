"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

        """
        Fiecare producator are un id propriu.
        """
        self.producer_id = self.marketplace.register_producer()

    def run(self):
        """
        Producatorul parcurge lista de produse pe care trebuie sa le produca
        si le publica in marketplace in cantitatea ceruta.
        """
        while True:
            for current_product in self.products:
                product = current_product[0]
                quantity = current_product[1]
                sleep_time = current_product[2]

                for _ in range(quantity):
                    if self.marketplace.publish(self.producer_id, product) is False:
                        time.sleep(self.republish_wait_time)
                    else:
                        time.sleep(sleep_time)
