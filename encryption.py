import hashlib

def encrypt_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Example usage
if __name__ == "__main__":
    sensitive_info = "UserSecretPassword123"
    print("Encrypted:", encrypt_data(sensitive_info))
