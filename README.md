# CLI Password Manager 🔐

A secure, lightweight Command-Line Interface (CLI) password manager built in **Python**. This application uses symmetric encryption to store your passwords safely in a local "vault" file, ensuring that only the person who possesses the master key can read or manage them.

## ✨ Features

* 🔑 **Secure Key Generation:** Generates a highly secure encryption key using the Fernet symmetric encryption standard (AES).
* 📁 **Encrypted Local Vault:** Passwords are saved in a local text file. The entire contents are encrypted, making them completely unreadable to unauthorized users.
* 🛡️ **Overwrite Protection:** Built-in safeguards prevent you from accidentally overwriting or deleting an existing master key or password vault.
* ⚙️ **Graceful Error Handling:** Provides clear, user-friendly error messages if dependencies are missing, if files aren't found, or if incorrect keys are used.
* ➕ **Easy Management:** * Add or update passwords.
  * Retrieve stored passwords securely.
  * Delete existing passwords from the vault.
  * List all currently saved site names.

## 🛠️ Prerequisites

This project requires **Python 3.x** and the `cryptography` library. 

To install the required dependency, run the following command in your terminal:
```bash
pip install cryptography
