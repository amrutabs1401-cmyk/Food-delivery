# 🍔 Food Delivery System (OOP in Python)

A small, console-based food delivery simulation built to demonstrate core **Object-Oriented Programming** concepts in Python: abstraction, inheritance, encapsulation, and polymorphism.

## ✨ Features

- Two user types: **Customer** and **Delivery Partner**
- Restaurants with a menu of veg / non-veg items
- Order placement with an auto-generated order ID (`ORD1`, `ORD2`, ...)
- Bill calculation with **5% GST** and a flat **₹20 packaging fee**
- OTP-based delivery verification
- Order status tracking: `Placed → Accepted → Delivered`
- Wallet balance for every user

## 🧱 Class Overview

| Class | Description |
|---|---|
| `User` (abstract) | Base class holding `name`, `phone`, and wallet balance. Declares abstract `notify()` and `display_profile()`. |
| `Customer(User)` | Has an address and order history. Can place orders. |
| `DeliveryPartner(User)` | Has a vehicle, availability, and rating. Can accept and deliver orders. |
| `MenuItem` | A food item with `name`, `price`, and `is_veg`. |
| `Restaurant` | Holds a menu; supports adding items and fetching the menu. |
| `Order` | Holds items, status, and OTP. Calculates bill, estimated time, and verifies OTP. |

## 🎯 OOP Concepts Demonstrated

- **Abstraction** – `User` is an abstract base class (`ABC`) with `@abstractmethod`s.
- **Inheritance** – `Customer` and `DeliveryPartner` extend `User`.
- **Polymorphism** – each subclass implements `notify()` and `display_profile()` differently.
- **Encapsulation** – protected attributes (`_name`, `_wallet_balance`, `_otp`, `_menu`, ...) and controlled updates via methods like `add_to_wallet()` and `update_status()`.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher (no external libraries needed)

### Run

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python main.py
```

> Replace `main.py` with the name of your file.

## 💻 Example Usage

```python
# Create a restaurant and add menu items
restaurant = Restaurant("Spice Hub", "Aurangabad")
restaurant.add_item(MenuItem("Paneer Tikka", 180, True))
restaurant.add_item(MenuItem("Chicken Biryani", 250, False))

# Create users
customer = Customer("Aman", "9876543210", "CIDCO, Aurangabad")
partner = DeliveryPartner("Rahul", "9123456780", "Bike")

customer.add_to_wallet(500)

# Place an order
order = customer.place_order(restaurant, restaurant.get_menu())
# Your OTP is: 1234

print("Total bill:", order.calculate_bill())
print("ETA (mins):", order.estimated_time())

# Delivery flow
partner.accept_order(order)
partner.deliver(order, 1234)

# Notifications & profiles
customer.notify("Order delivered")
customer.display_profile()
partner.display_profile()
```

### Sample Output

```
Your OTP is: 1234
Total bill: 472.5
ETA (mins): 30
Notification: Order delivered for customer: Aman
Name: Aman
Phone: 9876543210
Wallet Balance: 500
Address: CIDCO, Aurangabad
Name: Rahul
Phone: 9123456780
Availability: True
Rating: 0.0
```

## 🧾 Bill Calculation

```
subtotal = sum of item prices
GST      = 5% of subtotal
total    = subtotal + GST + ₹20 packaging fee
```

## 🔮 Future Improvements

- Generate a random OTP per order instead of the fixed `1234`
- Validate that ordered items belong to the chosen restaurant and check `is_open()`
- Deduct the bill from the customer's wallet on order placement
- Assign available delivery partners automatically
- Add order cancellation and more statuses (e.g., `Preparing`, `Out for Delivery`)
- Add ratings and reviews
- Persist data using a database or JSON files
- Add unit tests with `pytest`


