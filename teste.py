import secrets
from fakepinterest import bcrypt 

print(secrets.token_hex(16))


print(bcrypt.check_password_hash('$2b$12$Sd3ghTxXTHyVJ7oUi2R0NOYgKYuYt6eSoOMZzDstJ4IjAGz94Wthq', '13123'))