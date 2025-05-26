import unittest
import json
from src.main import app
from src.models.user import db, User, ApiKey
import bcrypt

class TestAuthRoutes(unittest.TestCase):
    def setUp(self):
        """Configuration avant chaque test"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # Création d'un utilisateur de test
            hashed_password = bcrypt.hashpw('TestPassword123!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            test_user = User(
                username='testuser',
                email='test@example.com',
                password=hashed_password
            )
            db.session.add(test_user)
            db.session.commit()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_register_success(self):
        """Test l'enregistrement réussi d'un utilisateur"""
        response = self.app.post('/api/auth/register', 
            json={
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'SecurePassword123!'
            }
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('user_id', data)
        
        # Vérification en base de données
        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'new@example.com')
    
    def test_register_existing_username(self):
        """Test l'enregistrement avec un nom d'utilisateur existant"""
        response = self.app.post('/api/auth/register', 
            json={
                'username': 'testuser',
                'email': 'another@example.com',
                'password': 'SecurePassword123!'
            }
        )
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_register_weak_password(self):
        """Test l'enregistrement avec un mot de passe faible"""
        response = self.app.post('/api/auth/register', 
            json={
                'username': 'weakuser',
                'email': 'weak@example.com',
                'password': 'weak'
            }
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_login_success(self):
        """Test la connexion réussie"""
        response = self.app.post('/api/auth/login', 
            json={
                'username': 'testuser',
                'password': 'TestPassword123!'
            }
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)
        self.assertIn('user', data)
    
    def test_login_invalid_credentials(self):
        """Test la connexion avec des identifiants invalides"""
        response = self.app.post('/api/auth/login', 
            json={
                'username': 'testuser',
                'password': 'WrongPassword123!'
            }
        )
        
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
