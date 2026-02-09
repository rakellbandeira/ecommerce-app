from auth import create_user
from database import create_category, create_product

def seed_admin():
    print("Creating admin user...")
    admin_id = create_user(
        email="admin@example.com",
        password="admin123",
        full_name="Admin User",
        is_admin=True
    )
    print(f"Admin user created: {admin_id}")

def seed_categories():
    print("\nCreating categories...")
    
    cat1_id = create_category(
        name="Electronics",
        description="Electronic devices and gadgets"
    )
    print(f"Category 1 created: {cat1_id}")
    
    cat2_id = create_category(
        name="Books",
        description="Books and educational materials"
    )
    print(f"Category 2 created: {cat2_id}")
    
    return cat1_id, cat2_id

def seed_products(cat1_id, cat2_id):
    print("\nCreating products...")
    
    # Electronics products
    products_electronics = [
        {
            'name': 'Wireless Headphones',
            'price': 49.99,
            'description': 'High-quality wireless headphones with noise cancellation',
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
            'stock': 10
        },
        {
            'name': 'USB-C Cable',
            'price': 15.99,
            'description': 'Durable USB-C charging and data cable, 2 meters',
            'image_url': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400',
            'stock': 25
        },
        {
            'name': 'Phone Stand',
            'price': 12.99,
            'description': 'Adjustable phone stand for desk, supports all sizes',
            'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400',
            'stock': 15
        }
    ]
    
    # Books products
    products_books = [
        {
            'name': 'Python Guide',
            'price': 29.99,
            'description': 'Complete guide to learning Python programming',
            'image_url': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400',
            'stock': 8
        },
        {
            'name': 'Web Development',
            'price': 34.99,
            'description': 'Master HTML, CSS, and JavaScript for web development',
            'image_url': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400',
            'stock': 12
        },
        {
            'name': 'Data Science',
            'price': 39.99,
            'description': 'Learn data science with Python and machine learning',
            'image_url': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400',
            'stock': 6
        }
    ]
    
    # Create electronics products
    for prod in products_electronics:
        prod_id = create_product(
            name=prod['name'],
            category_id=cat1_id,
            price=prod['price'],
            description=prod['description'],
            image_url=prod['image_url'],
            stock=prod['stock']
        )
        print(f"Product created: {prod['name']}")
    
    # Create book products
    for prod in products_books:
        prod_id = create_product(
            name=prod['name'],
            category_id=cat2_id,
            price=prod['price'],
            description=prod['description'],
            image_url=prod['image_url'],
            stock=prod['stock']
        )
        print(f"Product created: {prod['name']}")

def main():
    print("Starting data seed...\n")
    
    seed_admin()
    cat1_id, cat2_id = seed_categories()
    seed_products(cat1_id, cat2_id)
    
    print("\n All data seeded successfully!")
    print("\nAdmin credentials:")
    print("Email: admin@example.com")
    print("Password: admin123")

if __name__ == '__main__':
    main()