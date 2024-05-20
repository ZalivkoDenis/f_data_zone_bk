## JSON Web Tokens (aka JWT)   
Проверку  токена можно выполнить здесь: [jwt.io](https://jwt.io)

### Генерация RSA ключей для реализации авторизации по JWT-токену.
#### после выполнения команд ключи, ключи необходимо переместить в папку ../certs/

```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem    
```

---

## Шифрование паролей.

### Генерация RSA ключей для реализации шифрования.
#### после выполнения команд ключи, ключи необходимо переместить в папку ../certs/

```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out rsa_local_secret.key 2048
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in rsa_local_secret.key -outform PEM -pubout -out rsa_public_local_secret.key    
```

