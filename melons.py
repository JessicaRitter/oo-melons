"""Classes for melon orders."""
from random import randint
import datetime

class TooManyMelonsError(ValueError):

    def __init__(self):
        super(TooManyMelonsError, self).__init__("No more than 100 melons, please!")

class AbstractMelonOrder(object):
    """A melon order"""

    def __init__(self, species, qty, order_type, tax):
        """ Initialize melon order"""

        self.species = species
        self.qty = qty
        self.shipped = False
        self.order_type = order_type
        self.tax = tax
        if self.qty >= 100:
            raise TooManyMelonsError()


    def get_base_price(self):
        """Choose a random integer to be the base price"""

        #randint(0,6)--range weekday
        #randint(0,24)
        base_price = randint(5, 9)
        today = datetime.datetime.today()
        weekday = int(today.weekday())
        is_rush_hours = int(today.hour)
        if weekday in range(0, 4) and is_rush_hours in range(8, 11):
            base_price += 4

        return base_price

    def get_total(self):
        """Calculate price, including tax."""

        base_price = self.get_base_price()
        if self.species == "christmas":
            total = (1 + self.tax) * self.qty * (base_price * 1.5)
        else:
            total = (1 + self.tax) * self.qty * base_price

        return total

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True


class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    def __init__(self, species, qty):
        """Initialize melon order attributes."""

        super(DomesticMelonOrder, self).__init__(species, qty,
                                                 order_type='domestic',
                                                 tax=0.08)


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    def __init__(self, species, qty, country_code):
        """Initialize melon order attributes."""

        super(InternationalMelonOrder, self).__init__(species, qty,
                                                      order_type='international',
                                                      tax=0.17)
        self.country_code = country_code

    def get_total(self):
        """Gets total of international orders"""

        total = super(InternationalMelonOrder, self).get_total()

        if self.qty < 10:
            total += 3
        return total

    def get_country_code(self):
        """Return the country code."""

        return self.country_code


class GovernmentMelonOrder(AbstractMelonOrder):
    """Melons for the Government"""

    def __init__(self, species, qty):
        """Initialize Government Melon Order"""

        super(GovernmentMelonOrder, self).__init__(species, qty, order_type='government',
                                                    tax=0)
        self.passed_inspection = False

    def mark_inspection(self, passed):
        """Mark government melon passed inspection"""
        self.passed_inspection = passed
