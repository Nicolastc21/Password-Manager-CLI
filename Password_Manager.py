import os

try:
    from cryptography.fernet import Fernet, InvalidToken  # type: ignore[reportMissingImports]
except ModuleNotFoundError:
    Fernet = None
    InvalidToken = None


class PasswordManager:
    def __init__(self):
        self.key = None
        self.cipher = None
        self.password_file = None
        self.password_dict = {}

    def _require_key(self):
        if Fernet is None:
            raise ImportError("Missing dependency: install 'cryptography' to use PasswordManager.")
        if self.cipher is None:
            raise ValueError("No encryption key loaded. Create or load a key first.")

    def create_key(self, path):
        if Fernet is None:
            raise ImportError("Missing dependency: install 'cryptography' to use PasswordManager.")

        if os.path.exists(path):
            raise FileExistsError(f"A file already exists at '{path}'. Choose a different name.")
            
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        with open(path, 'wb') as f:
            f.write(self.key)
            
    def load_key(self, path):
        if Fernet is None:
            raise ImportError("Missing dependency: install 'cryptography' to use PasswordManager.")
        with open(path, 'rb') as f:
            self.key = f.read()

        try:
            self.cipher = Fernet(self.key)
        except ValueError as exc:
            self.key = None
            raise ValueError(f"Invalid key file: {exc}")
            
    def create_password_file(self, path, initial_values=None):
        self._require_key()

        if os.path.exists(path):
            raise FileExistsError(f"A vault already exists at '{path}'. Load it instead of creating a new one.")
            
        self.password_file = path
        self.password_dict = {}
        
        # Write all entries atomically
        with open(path, 'w') as f:
            if initial_values:
                for site, password in initial_values.items():
                    if not site or not password:
                        continue
                    encrypted = self.cipher.encrypt(password.encode()).decode()
                    f.write(site + ":" + encrypted + "\n")
                    self.password_dict[site] = password
    
    def load_password_file(self, path):
        self._require_key()
        self.password_file = path
        self.password_dict = {}
        
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ':' not in line:
                    continue
                site, encrypted = line.split(':', 1)
                try:
                    self.password_dict[site] = self.cipher.decrypt(encrypted.encode()).decode()
                except InvalidToken:
                    raise InvalidToken(f"Failed to decrypt entry for '{site}'. Wrong key?")
    
    def add_password(self, site, password):
        self._require_key()
        
        if self.password_file is None:
            raise ValueError("No password file loaded. Create or load a password file first.")
            
        if not site:
            raise ValueError("Site name cannot be empty.")
        if not password:
            raise ValueError("Password cannot be empty.")
        
        self.password_dict[site] = password

        with open(self.password_file, 'w') as f:
            for s, p in self.password_dict.items():
                encrypted = self.cipher.encrypt(p.encode()).decode()
                f.write(s + ":" + encrypted + "\n")
                
    def get_password(self, site):
        if site not in self.password_dict:
            raise KeyError(f"No password found for '{site}'")
        return self.password_dict[site]


def main():
    pm = PasswordManager()
    print("Welcome to CLI Password Manager!")
    print("--------------------------------")
    
    while True:
        print("\nWhat do you want to do?")
        print("  1. Create a new key")
        print("  2. Load an existing key")
        print("  3. Create a new password file")
        print("  4. Load an existing password file")
        print("  5. Add a new password")
        print("  6. Get a password")
        print("  7. Exit")
        choice = input("\nChoose an option (1-7): ").strip()
        
        if choice == "1":
            path = input("Enter the path to save the new key (e.g., secret.key): ")
            try:
                pm.create_key(path)
                print("Key created and saved successfully!")
            except Exception as exc:
                print(f"Error: {exc}")
        elif choice == "2":
            path = input("Enter the path to load the key (e.g., secret.key): ")
            try:
                pm.load_key(path)
                print("Key loaded successfully!")
            except FileNotFoundError:
                print("Key file not found.")
            except Exception as exc:
                print(f"Error: {exc}")
        elif choice == "3":
            path = input("Enter the path to save the new password file (e.g., vault.txt): ")
            try:
                pm.create_password_file(path)
                print("Password file created and saved successfully!")
            except Exception as exc:
                print(f"Error: {exc}")
        elif choice == "4":
            path = input("Enter the path to load the password file (e.g., vault.txt): ")
            try:
                pm.load_password_file(path)
                print("Password file loaded successfully!")
            except FileNotFoundError:
                print("Password file not found.")
            except Exception as exc:
                print(f"Error: {exc}")
        elif choice == "5":
            site = input("Enter the site name: ")
            new_password = input("Enter the password: ")
            try:
                pm.add_password(site, new_password)
                print(f"Password for '{site}' added/updated successfully!")
            except Exception as exc:
                print(f"Error: {exc}")
        elif choice == "6":
            site = input("Enter the site name: ")
            try:
                stored_password = pm.get_password(site)
                print(f"Password for '{site}': {stored_password}")
            except KeyError:
                print(f"No password found for '{site}'.")
            except Exception as exc:
                print(f"Error: {exc}")
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 7.")


if __name__ == "__main__":
    main()