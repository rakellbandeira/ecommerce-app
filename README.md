# Overview
E-Commerce Store with Admin Dashboard - A simple full-stack e-commerce application built with Streamlit and Firebase, with customer shopping and admin management.
## Customer Features
- Browse products by category, Shopping cart, Mock checkout and purchase, Purchase history tracking
## Admin Features
- Manage products and categories (add, edit, delete), View and manage user accounts and all purchases

## Default Admin Credentials
Email: admin@example.com
Password: admin123

# Software Demo Video
[Youtube Video](http://youtube.link.goes.here)

# Cloud Database
- FireStore Database

## Database structure: Collections
**users**
- `email` (string) - User email
- `hashed_password` (string) - Bcrypt hashed password
- `full_name` (string) 
- `is_admin` (boolean) 
- `created_at` - Account creation date
- `deleted` (boolean) 

**categories**
- `name` (string) - Category name
- `description` - Category description
- `created_at`
- `updated_at`

**products**
- `name` (string) - Product name
- `category_id` 
- `price` (number) - Product price
- `description` (string) - Product description
- `image_url` (string) - Product image URL
- `stock` (number) - Quantity in stock
- `created_at`
- `updated_at`

**purchases**
- `user_id`
- `items` (array) - Products purchased with quantities and prices
- `total_amount` (number) - Purchase total
- `purchase_date` 
- `status` (string) - Purchase status


# Development Environment
- Streamlit in the front-end, Python in the back-end, Google Firestore database and Firebase Auth 

# Future Work
- This app still has a long way tto go in terms of interface, for now is pretty simple. In the future, I also wouldlike to isert ral purchase funcionality with a payment gateway.





