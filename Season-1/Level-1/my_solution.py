from collections import namedtuple
from decimal import Decimal
#Inspired from solution
# Define data structures using namedtuples
Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

# Define constants for acceptable ranges
MAX_ITEM_AMOUNT = 100000
MAX_QUANTITY = 100
MIN_QUANTITY = 0
MAX_TOTAL = Decimal('1e6')

# Function to validate an order
def validorder(order):
    # Initialize variables to track payments and expenses
    payments = Decimal('0')
    expenses = Decimal('0')

    # Iterate through items in the order
    for item in order.items:
        if item.type == 'payment':
            # Check if payment amount is within a reasonable range
            if -MAX_ITEM_AMOUNT <= item.amount <= MAX_ITEM_AMOUNT:
                payments += Decimal(str(item.amount))
        elif item.type == 'product':
            # Check if quantity and amount are within reasonable ranges
            if isinstance(item.quantity, int) and MIN_QUANTITY < item.quantity <= MAX_QUANTITY and MIN_QUANTITY < item.amount <= MAX_ITEM_AMOUNT:
                expenses += Decimal(str(item.amount)) * item.quantity
            else:
                return "Invalid quantity or amount for product"
        else:
            return "Invalid item type: %s" % item.type

    # Check if total payments or expenses exceed the maximum allowed
    if abs(payments) > MAX_TOTAL or expenses > MAX_TOTAL:
        return "Total amount payable for an order exceeded"

    # Check if payments and expenses match
    if payments != expenses:
        return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, payments - expenses)
    else:
        return "Order ID: %s - Full payment received!" % order.id
