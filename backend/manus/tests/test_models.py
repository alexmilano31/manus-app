import unittest
from src.models.user import User, ApiKey
from datetime import datetime

class TestUserModel(unittest.TestCase):
    def test_user_creation(self):
        """Test la création d'un utilisateur et ses propriétés par défaut"""
        user = User(
            username="testuser",
            email="test@example.com",
            password="hashed_password"
        )
        
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "hashed_password")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)
        self.assertFalse(user.two_factor_enabled)
        self.assertIsNone(user.two_factor_secret)
        self.assertIsNone(user.recovery_codes)
    
    def test_user_to_dict(self):
        """Test la méthode to_dict de l'utilisateur"""
        user = User(
            username="testuser",
            email="test@example.com",
            password="hashed_password"
        )
        
        user_dict = user.to_dict()
        
        self.assertEqual(user_dict['username'], "testuser")
        self.assertEqual(user_dict['email'], "test@example.com")
        self.assertTrue(user_dict['is_active'])
        self.assertFalse(user_dict['is_verified'])
        self.assertFalse(user_dict['two_factor_enabled'])
        self.assertNotIn('password', user_dict)
    
    def test_recovery_codes(self):
        """Test la gestion des codes de récupération"""
        user = User(
            username="testuser",
            email="test@example.com",
            password="hashed_password"
        )
        
        # Test avec des codes de récupération
        codes = ["code1", "code2", "code3"]
        user.set_recovery_codes(codes)
        
        retrieved_codes = user.get_recovery_codes()
        self.assertEqual(retrieved_codes, codes)
        
        # Test sans codes de récupération
        user.recovery_codes = None
        self.assertEqual(user.get_recovery_codes(), [])

class TestApiKeyModel(unittest.TestCase):
    def test_api_key_creation(self):
        """Test la création d'une clé API et ses propriétés par défaut"""
        api_key = ApiKey(
            user_id=1,
            platform="binance",
            api_key="encrypted_api_key",
            api_secret="encrypted_api_secret",
            label="My Binance Account"
        )
        
        self.assertEqual(api_key.user_id, 1)
        self.assertEqual(api_key.platform, "binance")
        self.assertEqual(api_key.api_key, "encrypted_api_key")
        self.assertEqual(api_key.api_secret, "encrypted_api_secret")
        self.assertEqual(api_key.label, "My Binance Account")
        self.assertIsNone(api_key.passphrase)
        self.assertTrue(api_key.is_active)
        self.assertIsNone(api_key.last_used)
    
    def test_api_key_to_dict(self):
        """Test la méthode to_dict de la clé API"""
        api_key = ApiKey(
            user_id=1,
            platform="binance",
            api_key="encrypted_api_key",
            api_secret="encrypted_api_secret",
            label="My Binance Account"
        )
        
        api_key_dict = api_key.to_dict()
        
        self.assertEqual(api_key_dict['platform'], "binance")
        self.assertEqual(api_key_dict['label'], "My Binance Account")
        self.assertTrue(api_key_dict['is_active'])
        self.assertIsNone(api_key_dict['last_used'])
        self.assertNotIn('api_key', api_key_dict)
        self.assertNotIn('api_secret', api_key_dict)

if __name__ == '__main__':
    unittest.main()
