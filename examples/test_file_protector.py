import os
import sys
import unittest

# Add the project root to sys.path to import the core module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.file_protector import FileProtector

class TestFileProtector(unittest.TestCase):
    def setUp(self):
        self.protector = FileProtector(authorized_paths=["authorized_key.txt"])
        # Create dummy files for testing
        self.test_files = [
            ".env",
            "config.json",
            "my_secret.txt",
            "api_key.py",
            "normal_file.txt",
            "authorized_key.txt"
        ]
        for f in self.test_files:
            with open(f, 'w') as f_out:
                f_out.write("dummy content")

    def tearDown(self):
        # Clean up dummy files
        for f in self.test_files:
            if os.path.exists(f):
                os.remove(f)

    def test_sensitive_files_blocked(self):
        # .env should be blocked
        allowed, reason = self.protector.validate_access(".env")
        self.assertFalse(allowed)
        self.assertIn("blocked", reason.lower())

        # config.json should be blocked
        allowed, reason = self.protector.validate_access("config.json")
        self.assertFalse(allowed)
        self.assertIn("blocked", reason.lower())

    def test_keyword_files_blocked(self):
        # my_secret.txt should be blocked
        allowed, reason = self.protector.validate_access("my_secret.txt")
        self.assertFalse(allowed)
        self.assertIn("blocked", reason.lower())

        # api_key.py should be blocked
        allowed, reason = self.protector.validate_access("api_key.py")
        self.assertFalse(allowed)
        self.assertIn("blocked", reason.lower())

    def test_normal_file_allowed(self):
        # normal_file.txt should be allowed
        allowed, reason = self.protector.validate_access("normal_file.txt")
        self.assertTrue(allowed)

    def test_authorized_file_allowed(self):
        # authorized_key.txt should be allowed even if it contains 'key'
        allowed, reason = self.protector.validate_access("authorized_key.txt")
        self.assertTrue(allowed)

    def test_secure_open_exception(self):
        # secure_open should raise PermissionError for blocked files
        with self.assertRaises(PermissionError):
            self.protector.secure_open(".env")

    def test_secure_open_success(self):
        # secure_open should work for allowed files
        with self.protector.secure_open("normal_file.txt") as f:
            content = f.read()
            self.assertEqual(content, "dummy content")

if __name__ == "__main__":
    unittest.main()
