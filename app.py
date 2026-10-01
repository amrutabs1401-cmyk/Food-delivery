import streamlit as st
from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem

st.set_page_config(page_title="Food Delivery", page_icon="🍔")
st.title("🍔 Food Delivery App")

# ---------- Session state (keeps objects alive between reruns) ----------
if "customers" not in st.session_state:
    st.session_state.customers = {}   # name -> Customer
if "partners" not in st.session_state:
    st.session_state.partners = {}    # name -> DeliveryPartner
if "orders" not in st.session_state:
    st.session_state.orders = {}      # order_id -> Order
if "restaurants" not in st.session_state:
    # Sample restaurants so the menu section has something to show
    r1 = Restaurant("Spice Hub", "Aurangabad")
    r1.add_item(MenuItem("Paneer Tikka", 220, True))
    r1.add_item(MenuItem("Chicken Biryani", 280, False))
    r1.add_item(MenuItem("Veg Thali", 180, True))

    r2 = Restaurant("Pizza Point", "Aurangabad")
    r2.add_item(MenuItem("Margherita Pizza", 250, True))
    r2.add_item(MenuItem("Chicken Pizza", 320, False))
    r2.add_item(MenuItem("Garlic Bread", 120, True))

    st.session_state.restaurants = {r1.name: r1, r2.name: r2}

customers = st.session_state.customers
partners = st.session_state.partners
orders = st.session_state.orders
restaurants = st.session_state.restaurants

tabs = st.tabs([
    "1. Create Customer",
    "2. Add Wallet",
    "3. Restaurant Menu",
    "4. Place Order",
    "5. Create Partner",
    "6. Accept Order",
    "7. Deliver (OTP)",
])

# ---------- 1. Create customer ----------
with tabs[0]:
    st.subheader("Create Customer")
    name = st.text_input("Name", key="c_name")
    phone = st.text_input("Phone", key="c_phone")
    address = st.text_input("Address", key="c_address")
    if st.button("Create Customer"):
        if not name or not phone or not address:
            st.warning("Please fill all fields.")
        elif name in customers:
            st.error("A customer with this name already exists.")
        else:
            customers[name] = Customer(name, phone, address)
            st.success(f"Customer '{name}' created!")

    if customers:
        st.markdown("**Existing customers**")
        for c in customers.values():
            st.write(f"👤 {c._name} | 📞 {c._phone} | 🏠 {c.address} | 💰 ₹{c._wallet_balance}")

# ---------- 2. Add wallet balance ----------
with tabs[1]:
    st.subheader("Add Wallet Balance")
    if not customers:
        st.info("Create a customer first.")
    else:
        who = st.selectbox("Customer", list(customers), key="w_cust")
        amount = st.number_input("Amount (₹)", min_value=0, step=50, key="w_amt")
        if st.button("Add Money"):
            customers[who].add_to_wallet(amount)
            st.success(f"Added ₹{amount}. New balance: ₹{customers[who]._wallet_balance}")

# ---------- 3. Show restaurant menu ----------
with tabs[2]:
    st.subheader("Restaurant Menu")
    rname = st.selectbox("Restaurant", list(restaurants), key="m_rest")
    rest = restaurants[rname]
    st.caption(f"📍 {rest.location} | {'Open' if rest.is_open() else 'Closed'}")
    st.table([
        {"Item": i.name, "Price (₹)": i.price, "Type": "Veg 🟢" if i.is_veg else "Non-veg 🔴"}
        for i in rest.get_menu()
    ])

# ---------- 4. Place order ----------
with tabs[3]:
    st.subheader("Place an Order")
    if not customers:
        st.info("Create a customer first.")
    else:
        who = st.selectbox("Customer", list(customers), key="o_cust")
        rname = st.selectbox("Restaurant", list(restaurants), key="o_rest")
        rest = restaurants[rname]
        menu = {f"{i.name} (₹{i.price})": i for i in rest.get_menu()}
        chosen = st.multiselect("Select items", list(menu), key="o_items")

        if st.button("Place Order"):
            if not rest.is_open():
                st.error("Restaurant is closed.")
            elif not chosen:
                st.warning("Select at least one item.")
            else:
                items = [menu[c] for c in chosen]
                order = customers[who].place_order(rest, items)
                orders[order._order_id] = order
                st.success(f"Order #{order._order_id} placed!")
                st.info(f"🔐 Your delivery OTP: **{order._otp}**")
                st.write(f"Bill (incl. 5% GST + ₹20 packaging): **₹{order.calculate_bill():.2f}**")
                st.write(f"Estimated time: {order.estimated_time()} minutes")

    if orders:
        st.markdown("**All orders**")
        st.table([
            {"Order ID": o._order_id, "Items": ", ".join(i.name for i in o._items),
             "Status": o._status, "Bill (₹)": round(o.calculate_bill(), 2)}
            for o in orders.values()
        ])

# ---------- 5. Create delivery partner ----------
with tabs[4]:
    st.subheader("Create Delivery Partner")
    pname = st.text_input("Name", key="p_name")
    pphone = st.text_input("Phone", key="p_phone")
    vehicle = st.selectbox("Vehicle", ["Bike", "Scooter", "Bicycle"], key="p_vehicle")
    if st.button("Create Partner"):
        if not pname or not pphone:
            st.warning("Please fill all fields.")
        elif pname in partners:
            st.error("A partner with this name already exists.")
        else:
            partners[pname] = DeliveryPartner(pname, pphone, vehicle)
            st.success(f"Delivery partner '{pname}' created!")

    if partners:
        st.markdown("**Existing partners**")
        for p in partners.values():
            st.write(f"🛵 {p._name} | 📞 {p._phone} | {p.vehicle} | "
                     f"{'Available ✅' if p.is_available else 'Busy ⛔'}")

# ---------- 6. Accept order ----------
with tabs[5]:
    st.subheader("Accept an Order")
    pending = {oid: o for oid, o in orders.items() if o._status == "Placed"}
    if not partners:
        st.info("Create a delivery partner first.")
    elif not pending:
        st.info("No orders waiting for a partner.")
    else:
        who = st.selectbox("Delivery partner", list(partners), key="a_partner")
        oid = st.selectbox("Order", list(pending), key="a_order",
                           format_func=lambda x: f"Order #{x}")
        if st.button("Accept Order"):
            partner = partners[who]
            if not partner.is_available:
                st.error("This partner is busy with another order.")
            else:
                partner.accept_order(pending[oid])
                partner.notify(f"Order #{oid} accepted")
                st.session_state.assigned = st.session_state.get("assigned", {})
                st.session_state.assigned[oid] = who
                st.success(f"{who} accepted Order #{oid}. Status: {pending[oid]._status}")

# ---------- 7. Enter OTP & complete delivery ----------
with tabs[6]:
    st.subheader("Enter OTP & Complete Delivery")
    assigned = st.session_state.get("assigned", {})
    active = {oid: p for oid, p in assigned.items() if orders[oid]._status != "Delivered"}
    if not active:
        st.info("No orders out for delivery.")
    else:
        oid = st.selectbox("Order", list(active), key="d_order",
                           format_func=lambda x: f"Order #{x} (partner: {active[x]})")
        otp = st.number_input("Customer OTP", min_value=0, max_value=9999, step=1, key="d_otp")
        if st.button("Complete Delivery"):
            order = orders[oid]
            partner = partners[active[oid]]
            partner.deliver(order, int(otp))
            if order._status == "Delivered":
                st.success(f"✅ Order #{oid} delivered! {partner._name} is available again.")
                st.balloons()
            else:
                st.error("❌ Wrong OTP. Delivery not completed.")
