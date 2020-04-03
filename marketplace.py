"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the
    implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated
        with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producer_id = -1
        self.cart_id = -1

        """
        Dictionar in care retin lista cu produse pentru fiecare producator.
        """
        self.producers = {}

        """
        Dictionar in care retin ce produse sunt in cosul fiecarui consumator.
        """
        self.costumer_carts = {}

        """
        Id-ul producatorului de unde am luat produsul, pentru a sti unde sa il
        adaug cand consumatorul da remove_from_cart.
        """
        self.last_producer = -1

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producer_id += 1
        return self.producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait
        and then try again.

        Daca id-ul producatorului nu se afla printre chei, atunci creez cheia
        corespunzatoare si initializez cu o lista goala. Dupa aceea, verific
        daca mai este loc pentru a adauga produsele.
        """

        if producer_id not in self.producers:
            self.producers[producer_id] = []

        if len(self.producers[producer_id]) < self.queue_size_per_producer:
            self.producers[producer_id].append(product)
            return True

        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.cart_id += 1
        self.costumer_carts[self.cart_id] = []

        return self.cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again

        Caut produsul dorit in listele tuturor producatorilor. Daca il gasesc,
        il adaug in cosul consumatorului si il sterg din lista producatorului.
        De asemenea, retin id-ul producatorului de unde am luat produsul,
        pentru a sti unde sa-l adaug daca consumatorul apeleaza remove.
        """
        for current_producer in self.producers:
            for current_product in self.producers[current_producer]:
                if current_product == product:
                    self.costumer_carts[cart_id].append(product)
                    self.producers[current_producer].remove(current_product)
                    self.last_producer = current_producer
                    return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart

        Elimin produsul din cosul consumatorului si il adaug in produsele
        producatorului de la care l-a luat.
        """
        self.costumer_carts[cart_id].remove(product)
        self.producers[self.last_producer].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.costumer_carts[cart_id]
