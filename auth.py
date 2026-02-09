import bcrypt
from firebase_config import db

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(email: str, password: str, full_name: str, is_admin: bool = False) -> str:
    """Create a new user in Firestore"""
    from datetime import datetime
    
    hashed_pw = hash_password(password)
    
    user_data = {
        'email': email,
        'hashed_password': hashed_pw,
        'full_name': full_name,
        'is_admin': is_admin,
        'created_at': datetime.now(),
        'deleted': False
    }
    
    doc_ref = db.collection('users').document()
    doc_ref.set(user_data)
    return doc_ref.id

def get_user_by_email(email: str) -> dict:
    """Get user by email"""
    users = db.collection('users').where('email', '==', email).where('deleted', '==', False).stream()
    
    for user in users:
        user_data = user.to_dict()
        user_data['id'] = user.id
        return user_data
    
    return None

def login_user(email: str, password: str) -> dict:
    """Login user - returns user dict if successful, None otherwise"""
    user = get_user_by_email(email)
    
    if user and verify_password(password, user['hashed_password']):
        # Remove password from returned data for security
        user.pop('hashed_password', None)
        return user
    
    return None

def get_user_by_id(user_id: str) -> dict:
    """Get user by ID"""
    user = db.collection('users').document(user_id).get()
    
    if user.exists:
        user_data = user.to_dict()
        user_data['id'] = user.id
        return user_data
    
    return None