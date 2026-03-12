import os
import re

class FileProtector:
    """
    Sensitive File Protection Module (#813)
    Intercepts attempts to read sensitive files like .env, config.json, 
    or files containing 'key' or 'secret' in their names.
    """
    
    SENSITIVE_FILENAMES = {'.env', 'config.json'}
    SENSITIVE_KEYWORDS = {'key', 'secret'}
    
    def __init__(self, authorized_paths=None):
        self.authorized_paths = set(authorized_paths or [])

    def is_authorized(self, file_path):
        """
        Check if the file path is explicitly authorized.
        """
        abs_path = os.path.abspath(file_path)
        return any(abs_path == os.path.abspath(auth_path) for auth_path in self.authorized_paths)

    def validate_access(self, file_path):
        """
        Validate if the file access is allowed.
        Returns (is_allowed, reason)
        """
        filename = os.path.basename(file_path).lower()
        
        # 1. Check explicit filenames
        if filename in self.SENSITIVE_FILENAMES:
            if not self.is_authorized(file_path):
                return False, f"Access to sensitive file '{filename}' is blocked."
        
        # 2. Check keywords in filename
        if any(keyword in filename for keyword in self.SENSITIVE_KEYWORDS):
            if not self.is_authorized(file_path):
                return False, f"Access to file '{filename}' containing sensitive keywords is blocked."
        
        return True, "Access allowed."

    def secure_open(self, file_path, mode='r', **kwargs):
        """
        A wrapper around open() that validates access before opening.
        """
        allowed, reason = self.validate_access(file_path)
        if not allowed:
            raise PermissionError(f"Security Kit Blocked Access: {reason}")
        return open(file_path, mode, **kwargs)

if __name__ == "__main__":
    # Quick test
    protector = FileProtector(authorized_paths=["authorized_key.txt"])
    
    test_files = [
        ".env",
        "config.json",
        "my_secret.txt",
        "api_key.py",
        "normal_file.txt",
        "authorized_key.txt"
    ]
    
    print("--- File Access Validation Test ---")
    for f in test_files:
        allowed, reason = protector.validate_access(f)
        print(f"File: {f:20} | Allowed: {str(allowed):5} | Reason: {reason}")
