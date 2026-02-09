import streamlit as st
from firebase_config import db
from auth import login_user, create_user, get_user_by_email
from database import get_all_products, get_all_categories

#PAGE CONFIG 
st.set_page_config(
    page_title="E-Commerce Store Project",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SESSION STATE INITIALIZATION
if 'user' not in st.session_state:
    st.session_state.user = None

if 'cart' not in st.session_state:
    st.session_state.cart = {}

if 'proceed_to_checkout' not in st.session_state:
    st.session_state['proceed_to_checkout'] = False

if 'checkout_items' not in st.session_state:
    st.session_state['checkout_items'] = []

if 'checkout_total' not in st.session_state:
    st.session_state['checkout_total'] = 0

#LOGIN PAGE
def login_page():
    """Login and Signup page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("E-Commerce Store")
        
        # Tabs for login and signup
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        # LOGIN TAB 
        with tab1:
            st.subheader("Login to Your Account")
            
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                submit_btn = st.form_submit_button("Login", use_container_width=True)
            
            if submit_btn:
                if not email or not password:
                    st.error("Please enter email and password")
                else:
                    user = login_user(email, password)
                    
                    if user:
                        st.session_state.user = user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
            
            st.info("📝 Demo credentials:\n- Email: `admin@example.com`\n- Password: `admin123`")
        
        # SIGNUP TAB
        with tab2:
            st.subheader("Create a New Account")
            
            with st.form("signup_form"):
                full_name = st.text_input("Full Name", placeholder="Enter your full name")
                email = st.text_input("Email", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Create a password")
                password_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                
                submit_btn = st.form_submit_button("Sign Up", use_container_width=True)
            
            if submit_btn:
                if not full_name or not email or not password or not password_confirm:
                    st.error("Please fill in all fields")
                elif password != password_confirm:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    # Check if email already exists
                    existing_user = get_user_by_email(email)
                    
                    if existing_user:
                        st.error("Email already exists. Please login or use a different email.")
                    else:
                        try:
                            user_id = create_user(email, password, full_name, is_admin=False)
                            st.success("Account created! Please login.")
                            st.info("You can now login with your credentials.")
                        except Exception as e:
                            st.error(f"Error creating account: {str(e)}")

#MAIN page(AFTER LOGIN)
def main_app():
   
    with st.sidebar:
        st.write(f"👤 **{st.session_state.user['full_name']}**")
        st.write(f"📧 {st.session_state.user['email']}")
        
        if st.session_state.user['is_admin']:
            st.write("🔑 **Admin Account**")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.cart = {}
            st.session_state['proceed_to_checkout'] = False
            st.rerun()
        
        st.divider()
    
    #CHECKOUT FLOW
    if st.session_state.get('proceed_to_checkout', False):
        checkout_page()
        return
    
    # NORMAL NAVIGATION 
    if st.session_state.user['is_admin']:
        # Admin tabs
        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["Products", "Categories", "User Accounts"])
        
        with admin_tab1:
            admin_products_page()
        
        with admin_tab2:
            admin_categories_page()
        
        with admin_tab3:
            admin_users_page()
    
    else:
        # Customer tabs
        customer_tab1, customer_tab2, customer_tab3 = st.tabs(["Store", "Cart", "My Purchases"])
        
        with customer_tab1:
            customer_store_page()
        
        with customer_tab2:
            customer_cart_page()
        
        with customer_tab3:
            customer_purchases_page()

#PPAGES
def admin_categories_page():
    """Admin categories management"""
    st.subheader("🏷️ Manage Categories")

    from database import get_all_categories, create_category, update_category, delete_category

    categories = get_all_categories()

    # Initialize all session_state keys BEFORE creating widgets
    for category in categories:
        if f"modal_edit_cat_{category['id']}" not in st.session_state:
            st.session_state[f"modal_edit_cat_{category['id']}"] = False
        if f"modal_delete_cat_{category['id']}" not in st.session_state:
            st.session_state[f"modal_delete_cat_{category['id']}"] = False

    #Add categories
    st.write("➕ Add New Category")
    with st.form("add_category_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cat_name = st.text_input("Category Name", placeholder="e.g., Electronics")
        
        with col2:
            cat_description = st.text_input("Description", placeholder="e.g., Electronic devices")
        
        submit_btn = st.form_submit_button("Add Category", use_container_width=True)
    
    if submit_btn:
        if not cat_name or not cat_description:
            st.error("Please fill in all fields")
        else:
            try:
                create_category(cat_name, cat_description)
                st.success(f"✅ Category '{cat_name}' added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error adding category: {str(e)}")
    
    st.divider()

    #edit categories
    st.write("📋 All Categories")
    
    if not categories:
        st.info("No categories yet")
    else:
        for category in categories:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{category['name']}**")
                st.caption(category['description'])
            
            with col2:
                if st.button("✏️ Edit", key=f"btn_edit_cat_{category['id']}"):
                    st.session_state[f"modal_edit_cat_{category['id']}"] = True
            
            with col3:
                if st.button("Delete", key=f"btn_delete_cat_{category['id']}"):
                    st.session_state[f"modal_delete_cat_{category['id']}"] = True
            
            #edit modal
            if st.session_state.get(f"modal_edit_cat_{category['id']}", False):
                st.write("Edit Category")
                
                with st.form(f"edit_cat_form_{category['id']}"):
                    new_name = st.text_input("Category Name", value=category['name'])
                    new_description = st.text_input("Description", value=category['description'])
                    
                    col_save, col_cancel = st.columns(2)
                    
                    with col_save:
                        save_btn = st.form_submit_button("Save Changes", use_container_width=True)
                    
                    with col_cancel:
                        cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
                
                if save_btn:
                    if not new_name or not new_description:
                        st.error("Please fill in all fields")
                    else:
                        try:
                            update_category(category['id'], new_name, new_description)
                            st.success(f"Category updated!")
                            st.session_state[f"modal_edit_cat_{category['id']}"] = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error updating category: {str(e)}")
                
                if cancel_btn:
                    st.session_state[f"modal_edit_cat_{category['id']}"] = False
                    st.rerun()


            if st.session_state.get(f"modal_delete_cat_{category['id']}", False):
                st.warning(f"⚠️ Are you sure you want to delete '{category['name']}'?")
                
                col_yes, col_no = st.columns(2)
                
                with col_yes:
                    if st.button("Yes, Delete", key=f"btn_confirm_delete_cat_{category['id']}", use_container_width=True):
                        try:
                            delete_category(category['id'])
                            st.success(f"Category deleted!")
                            st.session_state[f"modal_delete_cat_{category['id']}"] = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting category: {str(e)}")
                
                with col_no:
                    if st.button("No, Keep It", key=f"btn_cancel_delete_cat_{category['id']}", use_container_width=True):
                        st.session_state[f"modal_delete_cat_{category['id']}"] = False
                        st.rerun()
            
            st.divider()


def admin_products_page():
    st.subheader("📦 Manage Products")
    
    from database import (get_all_products, get_all_categories, create_product, 
                         update_product, delete_product)
    
    # Get all products and categories
    products = get_all_products()
    categories = get_all_categories()
    
    if not categories:
        st.error("❌ Please create categories first before adding products")
        return
    
    # Create category name lookup
    category_dict = {cat['id']: cat['name'] for cat in categories}
    
    # Initialize all session_state keys BEFORE creating widgets
    for product in products:
        if f"modal_edit_prod_{product['id']}" not in st.session_state:
            st.session_state[f"modal_edit_prod_{product['id']}"] = False
        if f"modal_delete_prod_{product['id']}" not in st.session_state:
            st.session_state[f"modal_delete_prod_{product['id']}"] = False
    
    #ADD NEW PRODUCt
    st.write("➕ Add New Product")
    
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            prod_name = st.text_input("Product Name", placeholder="e.g., Wireless Headphones")
            prod_price = st.number_input("Price ($)", min_value=0.01, step=0.01)
            prod_stock = st.number_input("Stock Quantity", min_value=1, step=1, value=10)
        
        with col2:
            # Category dropdown
            category_options = [cat['name'] for cat in categories]
            selected_category = st.selectbox("Category", category_options)
            selected_cat_id = [cat['id'] for cat in categories if cat['name'] == selected_category][0]
            
            prod_description = st.text_input("Description", placeholder="Brief description")
            prod_image = st.text_input("Image URL", placeholder="https://example.com/image.jpg")
        
        submit_btn = st.form_submit_button("Add Product", use_container_width=True)
    
    if submit_btn:
        if not prod_name or not prod_description or not prod_image:
            st.error("Please fill in all fields")
        else:
            try:
                create_product(
                    name=prod_name,
                    category_id=selected_cat_id,
                    price=prod_price,
                    description=prod_description,
                    image_url=prod_image,
                    stock=prod_stock
                )
                st.success(f"Product '{prod_name}' added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error adding product: {str(e)}")
    
    st.divider()
    
    #FILTER BY CATEGORY
    st.write("📋 All Products")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"] + [cat['name'] for cat in categories]
        )
    
    # Filter products
    if filter_category == "All":
        filtered_products = products
    else:
        cat_id = [cat['id'] for cat in categories if cat['name'] == filter_category][0]
        filtered_products = [p for p in products if p['category_id'] == cat_id]
    
    if not filtered_products:
        st.info("No products in this category")
    else:
        for product in filtered_products:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"**{product['name']}**")
                    st.caption(product['description'])
                    st.write(f"Category: {category_dict.get(product['category_id'], 'Unknown')}")
                
                with col2:
                    st.metric("Price", f"${product['price']:.2f}")
                    st.metric("Stock", product['stock'])
                
                with col3:
                    if st.button("✏️ Edit", key=f"btn_edit_prod_{product['id']}"):
                        st.session_state[f"modal_edit_prod_{product['id']}"] = True
                
                with col4:
                    if st.button("Delete", key=f"btn_delete_prod_{product['id']}"):
                        st.session_state[f"modal_delete_prod_{product['id']}"] = True
                
                # EDIT MODAL
                if st.session_state.get(f"modal_edit_prod_{product['id']}", False):
                    st.write("Edit Product")
                    
                    with st.form(f"edit_prod_form_{product['id']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_name = st.text_input("Product Name", value=product['name'])
                            new_price = st.number_input("Price ($)", value=product['price'], min_value=0.01, step=0.01)
                            new_stock = st.number_input("Stock", value=product['stock'], min_value=1, step=1)
                        
                        with col2:
                            # Category dropdown for edit
                            cat_options = [cat['name'] for cat in categories]
                            current_cat_name = category_dict.get(product['category_id'], cat_options[0])
                            new_category = st.selectbox("Category", cat_options, index=cat_options.index(current_cat_name), key=f"edit_cat_select_{product['id']}")
                            new_cat_id = [cat['id'] for cat in categories if cat['name'] == new_category][0]
                            
                            new_description = st.text_input("Description", value=product['description'])
                            new_image = st.text_input("Image URL", value=product['image_url'])
                        
                        col_save, col_cancel = st.columns(2)
                        
                        with col_save:
                            save_btn = st.form_submit_button("Save Changes", use_container_width=True)
                        
                        with col_cancel:
                            cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
                    
                    if save_btn:
                        if not new_name or not new_description or not new_image:
                            st.error("Please fill in all fields")
                        else:
                            try:
                                update_product(
                                    product_id=product['id'],
                                    name=new_name,
                                    category_id=new_cat_id,
                                    price=new_price,
                                    description=new_description,
                                    image_url=new_image,
                                    stock=new_stock
                                )
                                st.success(f"Product updated!")
                                st.session_state[f"modal_edit_prod_{product['id']}"] = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error updating product: {str(e)}")
                    
                    if cancel_btn:
                        st.session_state[f"modal_edit_prod_{product['id']}"] = False
                        st.rerun()
                
                # DELETE CONFIRMATION
                if st.session_state.get(f"modal_delete_prod_{product['id']}", False):
                    st.warning(f"⚠️ Are you sure you want to delete '{product['name']}'?")
                    
                    col_yes, col_no = st.columns(2)
                    
                    with col_yes:
                        if st.button("Yes, Delete", key=f"btn_confirm_delete_prod_{product['id']}", use_container_width=True):
                            try:
                                delete_product(product['id'])
                                st.success(f"Product deleted!")
                                st.session_state[f"modal_delete_prod_{product['id']}"] = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting product: {str(e)}")
                    
                    with col_no:
                        if st.button("No, Keep It", key=f"btn_cancel_delete_prod_{product['id']}", use_container_width=True):
                            st.session_state[f"modal_delete_prod_{product['id']}"] = False
                            st.rerun()
                
                st.divider()



def admin_users_page():
    st.subheader("👥 User Accounts")
    
    from database import get_all_users, soft_delete_user
    
    # Get all users
    users = get_all_users()
    
    # Initialize all session_state keys BEFORE creating widgets
    for user in users:
        if f"modal_delete_user_{user['id']}" not in st.session_state:
            st.session_state[f"modal_delete_user_{user['id']}"] = False
    
    st.write(f"**Total Users:** {len(users)}")
    st.divider()
    
    if not users:
        st.info("No user accounts yet")
    else:
        for user in users:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                admin_badge = " 🔑 ADMIN" if user['is_admin'] else ""
                st.write(f"**{user['full_name']}**{admin_badge}")
                st.caption(f"{user['email']}")
            
            with col2:
                created_date = user['created_at'].strftime("%Y-%m-%d") if hasattr(user['created_at'], 'strftime') else str(user['created_at'])
                st.caption(f"Joined: {created_date}")
            
            with col3:
                if user['is_admin']:
                    st.write("🔒 Admin")
                else:
                    st.write("👤 Customer")
            
            with col4:
                # Only allow deleting non-admin users
                if not user['is_admin']:
                    if st.button("Delete", key=f"btn_delete_user_{user['id']}"):
                        st.session_state[f"modal_delete_user_{user['id']}"] = True
                else:
                    st.caption("(Cannot delete admin)")
            
            # DELETE
            if st.session_state.get(f"modal_delete_user_{user['id']}", False):
                st.warning(f"⚠️ Are you sure you want to delete user '{user['full_name']}'?")
                st.caption("Note: This will mark the user as deleted. Their purchase history will be preserved.")
                
                col_yes, col_no = st.columns(2)
                
                with col_yes:
                    if st.button("Yes, Delete", key=f"btn_confirm_delete_user_{user['id']}", use_container_width=True):
                        try:
                            soft_delete_user(user['id'])
                            st.success(f"User deleted!")
                            st.session_state[f"modal_delete_user_{user['id']}"] = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting user: {str(e)}")
                
                with col_no:
                    if st.button("No, Keep User", key=f"btn_cancel_delete_user_{user['id']}", use_container_width=True):
                        st.session_state[f"modal_delete_user_{user['id']}"] = False
                        st.rerun()
            
            st.divider()


def customer_store_page():
    st.subheader("🛒 Browse Products")
    
    from database import get_all_categories, get_products_by_category, get_all_products
    
    # Get categories and products
    categories = get_all_categories()
    all_products = get_all_products()
    
    if not categories or not all_products:
        st.info("No products available yet")
        return
    
    # Create category name lookup
    category_dict = {cat['id']: cat['name'] for cat in categories}
    
    #  FILTER BY CATEGORY 
    col1, col2 = st.columns([1, 4])
    
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"] + [cat['name'] for cat in categories],
            key="store_category_filter"
        )
    
    # Filter products
    if filter_category == "All":
        filtered_products = all_products
    else:
        cat_id = [cat['id'] for cat in categories if cat['name'] == filter_category][0]
        filtered_products = [p for p in all_products if p['category_id'] == cat_id]
    
    if not filtered_products:
        st.info("No products in this category")
        return
    
    #  DISPLAY PRODUCTS IN GRID 
    st.write(f"Found {len(filtered_products)} product(s)")
    st.divider()
    
    # Create grid layout (3 products per row)
    cols = st.columns(3)
    col_idx = 0
    
    for product in filtered_products:
        with cols[col_idx % 3]:
            # Product card
            with st.container(border=True):
                # Image
                st.image(product['image_url'], use_container_width=True)
                
                # Product info
                st.write(f"**{product['name']}**")
                st.caption(category_dict.get(product['category_id'], 'Unknown'))
                st.caption(product['description'])
                
                # Price and stock
                col_price, col_stock = st.columns(2)
                with col_price:
                    st.metric("Price", f"${product['price']:.2f}")
                with col_stock:
                    if product['stock'] > 0:
                        st.metric("Stock", product['stock'])
                    else:
                        st.metric("Stock", "Out")
                
                # Add to cart button
                if product['stock'] > 0:
                    qty = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=product['stock'],
                        value=1,
                        key=f"store_qty_{product['id']}" 
                    )
                    
                    if st.button(
                        "🛒 Add to Cart",
                        key=f"store_btn_add_cart_{product['id']}", 
                        use_container_width=True
                    ):
                        # Add to session state cart
                        cart_item = {
                            'product_id': product['id'],
                            'product_name': product['name'],
                            'price': product['price'],
                            'quantity': int(qty)
                        }
                        
                        # If product already in cart, update quantity
                        if product['id'] in st.session_state.cart:
                            st.session_state.cart[product['id']]['quantity'] += int(qty)
                            st.success(f"Updated {product['name']} in cart!")
                        else:
                            st.session_state.cart[product['id']] = cart_item
                            st.success(f"Added {product['name']} to cart!")
                        
                        st.rerun()
                else:
                    st.error("Out of Stock")
            
            col_idx += 1

    st.write("🛍️ Cart Summary")
    
    if not st.session_state.cart:
        st.info("Your cart is empty")
    else:
        total = 0
        for item_id, item in st.session_state.cart.items():
            item_total = item['price'] * item['quantity']
            total += item_total
            st.write(f"• {item['product_name']} x{item['quantity']} = ${item_total:.2f}")
        
        st.divider()
        st.write(f"Total: ${total:.2f}")
        st.info(f"{len(st.session_state.cart)} item(s) in cart")


     
def customer_cart_page():
    st.subheader("🛍️ Your Shopping Cart")
    
    from database import get_all_products
    
    # Get all products for reference
    all_products = {p['id']: p for p in get_all_products()}
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Go to Store tab to add products!")
        return
    
    st.write(f"Items in cart: {len(st.session_state.cart)}")
    st.divider()
    
    #  DISPLAY CART ITEMS 
    total_amount = 0
    items_to_checkout = []
    
    for product_id, item in st.session_state.cart.items():
        product = all_products.get(product_id)
        
        if product:
            item_total = item['price'] * item['quantity']
            total_amount += item_total
            
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{item['product_name']}**")
                st.caption(f"Price: ${item['price']:.2f} each")
            
            with col2:
                st.metric("Qty", item['quantity'])
            
            with col3:
                st.metric("Subtotal", f"${item_total:.2f}")
            
            with col4:
                # Update quantity button
                new_qty = st.number_input(
                    "New Qty",
                    min_value=1,
                    max_value=product['stock'],
                    value=item['quantity'],
                    key=f"cart_qty_update_{product_id}"
                )
                
                if new_qty != item['quantity']:
                    if st.button("✏️ Update", key=f"cart_btn_update_qty_{product_id}", use_container_width=True):
                        st.session_state.cart[product_id]['quantity'] = new_qty
                        st.success("Quantity updated!")
                        st.rerun()
            
            with col5:
                # Remove from cart button
                if st.button("Remove", key=f"cart_btn_remove_{product_id}", use_container_width=True):
                    del st.session_state.cart[product_id]
                    st.success("Item removed from cart!")
                    st.rerun()
            
            # Prepare item for checkout
            items_to_checkout.append({
                'product_id': product_id,
                'product_name': item['product_name'],
                'quantity': item['quantity'],
                'price': item['price']
            })
            
            st.divider()
    
    #  CART SUMMARY 
    st.write("Order Summary")
    st.metric("Total Amount", f"${total_amount:.2f}")
    
    st.divider()
    
    #  CHECKOUT SECTION 
    st.write("Proceed to Checkout")
    
    if st.button("Complete Purchase (Mock)", use_container_width=True, type="primary"):
        # This will trigger checkout in the main app
        st.session_state['proceed_to_checkout'] = True
        st.session_state['checkout_items'] = items_to_checkout
        st.session_state['checkout_total'] = total_amount
        st.success("Proceeding to checkout...")
        st.rerun()




def customer_purchases_page():
    st.subheader("📋 My Purchases")
    
    from database import get_user_purchases
    
    # Get user's purchases
    user_id = st.session_state.user['id']
    purchases = get_user_purchases(user_id)
    
    if not purchases:
        st.info("You haven't made any purchases yet. Go to Store tab to shop!")
        return
    
    st.write(f"**Total Purchases: {len(purchases)}**")
    st.divider()
    
    # DISPLAY PURCHASES
    for purchase in purchases:
        with st.container(border=True):
            # Purchase header
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                purchase_date = purchase['purchase_date'].strftime("%Y-%m-%d %H:%M") if hasattr(purchase['purchase_date'], 'strftime') else str(purchase['purchase_date'])
                st.write(f"**Purchase #{purchase['id'][:8]}**")
                st.caption(f"{purchase_date}")
            
            with col2:
                st.metric("Total", f"${purchase['total_amount']:.2f}")
            
            with col3:
                status_emoji = "✅" if purchase['status'] == 'completed' else "⏳"
                st.write(f"{status_emoji} {purchase['status'].upper()}")
            
            st.divider()
            
            # Purchase items
            st.write("**Items:**")
            for item in purchase['items']:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"• {item['product_name']}")
                
                with col2:
                    st.caption(f"${item['price']:.2f} each")
                
                with col3:
                    st.caption(f"Qty: {item['quantity']}")
                
                with col4:
                    item_total = item['price'] * item['quantity']
                    st.caption(f"${item_total:.2f}")
            
            
#CHECKOUT PAGE
def checkout_page():
    st.subheader("🎯 Checkout")
    
    from database import create_purchase, reduce_stock
    
    items = st.session_state.get('checkout_items', [])
    total = st.session_state.get('checkout_total', 0)
    
    if not items:
        st.error("No items to checkout")
        if st.button("← Back to Cart"):
            st.session_state['proceed_to_checkout'] = False
            st.rerun()
        return
    
    #ORDER SUMMARY
    st.write("📋 Order Summary")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("Items:")
        for item in items:
            item_total = item['price'] * item['quantity']
            st.write(f"• {item['product_name']} x{item['quantity']} = ${item_total:.2f}")
    
    with col2:
        st.metric("Total", f"${total:.2f}")
    
    st.divider()
    
    # SHIPPING INFO
    st.write("📦 Shipping Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name", value=st.session_state.user['full_name'])
    
    with col2:
        email = st.text_input("Email", value=st.session_state.user['email'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        address = st.text_input("Address", placeholder="123 Main St")
    
    with col2:
        city = st.text_input("City", placeholder="Your City")
    
    col1, col2 = st.columns(2)
    
    with col1:
        state = st.text_input("State/Province", placeholder="CA")
    
    with col2:
        zip_code = st.text_input("ZIP Code", placeholder="12345")
    
    st.divider()
    
    #PAYMENT INFO (MOCK)
    st.write("💳 Payment Information (Just mock)")
    st.info("This is a mock purchase. No real payment processing.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456", type="password")
    
    with col2:
        st.write("")
        st.write("")
        expiry = st.text_input("Expiry (MM/YY)", placeholder="12/25")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cvv = st.text_input("CVV", placeholder="123", type="password")
    
    st.divider()
    
    #COMPLETE PURCHASE BUTTON
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Complete Purchase", use_container_width=True, type="primary"):
            # Validation
            if not all([full_name, email, address, city, state, zip_code, card_number, expiry, cvv]):
                st.error("Please fill in all fields")
            else:
                try:
                    #purchase record
                    purchase_id = create_purchase(
                        user_id=st.session_state.user['id'],
                        items=items,
                        total_amount=total
                    )
                    
                    # Reduce product qty
                    for item in items:
                        reduce_stock(item['product_id'], item['quantity'])
                    
                    # Clear cart and checkout state
                    st.session_state.cart = {}
                    st.session_state['proceed_to_checkout'] = False
                    st.session_state['checkout_items'] = []
                    st.session_state['checkout_total'] = 0
                    
                    st.success("Purchase completed successfully!")
                    
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Purchase ID", purchase_id[:8])
                    with col2:
                        st.metric("Total Amount", f"${total:.2f}")
                    
                    st.info(f"Thank you for your purchase! Your order has been confirmed.")
                    
                    if st.button("← Go to My Purchases"):
                        st.rerun()
                
                except Exception as e:
                    st.error(f"Error processing purchase: {str(e)}")
    
    with col2:
        if st.button("← Back to Cart", use_container_width=True):
            st.session_state['proceed_to_checkout'] = False
            st.rerun()



#RUN APP
if st.session_state.user is None:
    login_page()
else:
    main_app()