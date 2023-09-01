from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

def generate_keys():
    private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public = private.public_key()
    return private, public

def sign(message, private):
    message = bytes(message, 'utf-8')  # Removed redundant conversion
    signature = private.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify(message, sig, public):
    message = bytes(message, 'utf-8')  # Removed redundant conversion
    try:
        public.verify(
            sig,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True  # Signature is valid
    except InvalidSignature:
        print("Error executing public key")
        return False

if __name__ == '__main__':
    pr, pu = generate_keys() #A
    pr1,pu1 = generate_keys() #B
    # Print the keys for reference
    print("Private Key:", pr)
    print("Public Key:", pu)

    message = "Hii I am Avineesh, Blockchain Dev."
    sig = sign(message, pr)
    # Print the signature for reference
    print("Signature:", sig)

    is_valid = verify(message, sig, pu1)
    
    if is_valid:
        print("Signature is valid.")
    else:
        print("Signature is invalid.")
