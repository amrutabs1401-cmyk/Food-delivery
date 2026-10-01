from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem

# 1. Register customer Priya
priya = Customer("Priya", "9876543210", "Bangalore")
print("--- Customer registered ---")
priya.display_profile()

# 2. Register delivery partner Rajesh
rajesh = DeliveryPartner("Rajesh", "9123456780", "Bike")
print("\n--- Delivery partner registered ---")
rajesh.display_profile()

# 3. Create restaurant Bawarchi and add menu items
bawarchi = Restaurant("Bawarchi", "MG Road")
biryani = MenuItem("Biryani", 250, False)
kebab = MenuItem("Kebab", 150, False)
bawarchi.add_item(biryani)
bawarchi.add_item(kebab)
print("\n--- Menu at", bawarchi.name, "(" + bawarchi.location + ") ---")
for item in bawarchi.get_menu():
    print(f"{item.name}: Rs.{item.price}")

# 4. Wallet top-up (valid and invalid)
print("\n--- Wallet ---")
priya.add_to_wallet(500)
print("After +500:", priya._wallet_balance)
priya.add_to_wallet(-100)
print("After -100 (should be ignored):", priya._wallet_balance)

# 5. Priya places an order for Biryani and Kebab
print("\n--- Placing order ---")
order = priya.place_order(bawarchi, [biryani, kebab])

# Fix the OTP at 1234 so the demo is repeatable
# (normally it is random, so 1234 would only match by chance)
order._otp = 1234

# 6. Bill breakdown and estimated time
subtotal = sum(item.price for item in order._items)
gst = subtotal * 0.05
packaging_fee = 20
total = order.calculate_bill()

print("\n--- Bill ---")
print("Subtotal       :", subtotal)
print("GST (5%)       :", gst)
print("Packaging fee  :", packaging_fee)
print("Total          :", total)
print("Estimated time :", order.estimated_time(), "minutes")

# 7. Rajesh accepts the order, wrong OTP, then correct OTP
print("\n--- Delivery ---")
rajesh.accept_order(order)
print("Status after accept:", order._status)

rajesh.deliver(order, 9999)
print("Status after wrong OTP (9999):", order._status)

rajesh.deliver(order, 1234)
print("Status after correct OTP (1234):", order._status)
print("Rajesh available again:", rajesh.is_available)

# 8. Notifications
print("\n--- Notifications ---")
priya.notify("Order delivered")
rajesh.notify("Order delivered")
