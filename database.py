from firebase_config import db
from datetime import datetime

# CATEGORIES 

def create_category(name: str, description: str) -> str:
    category_data = {
        'name': name,
        'description': description,
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    
    doc_ref = db.collection('categories').document()
    doc_ref.set(category_data)
    return doc_ref.id

def get_all_categories() -> list:
    categories = db.collection('categories').stream()
    
    result = []
    for cat in categories:
        cat_data = cat.to_dict()
        cat_data['id'] = cat.id
        result.append(cat_data)
    
    return result

def get_category(category_id: str) -> dict:
    cat = db.collection('categories').document(category_id).get()
    
    if cat.exists:
        cat_data = cat.to_dict()
        cat_data['id'] = cat.id
        return cat_data
    
    return None

def update_category(category_id: str, name: str, description: str) -> bool:
    try:
        db.collection('categories').document(category_id).update({
            'name': name,
            'description': description,
            'updated_at': datetime.now()
        })
        return True
    except:
        return False

def delete_category(category_id: str) -> bool:
    try:
        db.collection('categories').document(category_id).delete()
        return True
    except:
        return False


# PRODUCTS 

def create_product(name: str, category_id: str, price: float, description: str, image_url: str, stock: int) -> str:
    product_data = {
        'name': name,
        'category_id': category_id,
        'price': price,
        'description': description,
        'image_url': image_url,
        'stock': stock,
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    
    doc_ref = db.collection('products').document()
    doc_ref.set(product_data)
    return doc_ref.id

def get_all_products() -> list:
    products = db.collection('products').stream()
    
    result = []
    for prod in products:
        prod_data = prod.to_dict()
        prod_data['id'] = prod.id
        result.append(prod_data)
    
    return result

def get_products_by_category(category_id: str) -> list:
    products = db.collection('products').where('category_id', '==', category_id).stream()
    
    result = []
    for prod in products:
        prod_data = prod.to_dict()
        prod_data['id'] = prod.id
        result.append(prod_data)
    
    return result

def get_product(product_id: str) -> dict:
    prod = db.collection('products').document(product_id).get()
    
    if prod.exists:
        prod_data = prod.to_dict()
        prod_data['id'] = prod.id
        return prod_data
    
    return None

def update_product(product_id: str, name: str, category_id: str, price: float, description: str, image_url: str, stock: int) -> bool:
    try:
        db.collection('products').document(product_id).update({
            'name': name,
            'category_id': category_id,
            'price': price,
            'description': description,
            'image_url': image_url,
            'stock': stock,
            'updated_at': datetime.now()
        })
        return True
    except:
        return False

def delete_product(product_id: str) -> bool:
    try:
        db.collection('products').document(product_id).delete()
        return True
    except:
        return False

def reduce_stock(product_id: str, quantity: int) -> bool:
    try:
        product = get_product(product_id)
        new_stock = product['stock'] - quantity
        
        db.collection('products').document(product_id).update({
            'stock': new_stock
        })
        return True
    except:
        return False


# USERS

def get_all_users() -> list:
    users = db.collection('users').where('deleted', '==', False).stream()
    
    result = []
    for user in users:
        user_data = user.to_dict()
        user_data['id'] = user.id
        # Remove password hash from response
        user_data.pop('hashed_password', None)
        result.append(user_data)
    
    return result

def soft_delete_user(user_id: str) -> bool:
    try:
        db.collection('users').document(user_id).update({
            'deleted': True
        })
        return True
    except:
        return False

# PURCHASES 

def create_purchase(user_id: str, items: list, total_amount: float) -> str:
    """    
    items format: [{'product_id': '...', 'product_name': '...', 'quantity': 5, 'price': 29.99}, ...]
    """
    purchase_data = {
        'user_id': user_id,
        'items': items,
        'total_amount': total_amount,
        'purchase_date': datetime.now(),
        'status': 'completed'
    }
    
    doc_ref = db.collection('purchases').document()
    doc_ref.set(purchase_data)
    return doc_ref.id


def get_user_purchases(user_id: str) -> list:
    purchases = db.collection('purchases').where('user_id', '==', user_id).stream()
    
    result = []
    for purchase in purchases:
        purchase_data = purchase.to_dict()
        purchase_data['id'] = purchase.id
        
        if 'items' in purchase_data and purchase_data['items']:
            enriched_items = []
            for item in purchase_data['items']:
                product_doc = db.collection('products').document(item['product_id']).get()
                if product_doc.exists:
                    product = product_doc.to_dict()
                    enriched_item = {
                        'product_id': item['product_id'],
                        'product_name': product.get('name', 'Unknown Product'),
                        'price': item.get('price', 0),
                        'quantity': item.get('quantity', 0)
                    }
                    enriched_items.append(enriched_item)
                else:
                    # Fallback 
                    enriched_item = {
                        'product_id': item['product_id'],
                        'product_name': item.get('product_name', 'Deleted Product'),
                        'price': item.get('price', 0),
                        'quantity': item.get('quantity', 0)
                    }
                    enriched_items.append(enriched_item)
            
            purchase_data['items'] = enriched_items
        
        result.append(purchase_data)
    
    return result

def get_all_purchases() -> list:
    purchases = db.collection('purchases').stream()
    
    result = []
    for purchase in purchases:
        purchase_data = purchase.to_dict()
        purchase_data['id'] = purchase.id
        result.append(purchase_data)
    
    return result