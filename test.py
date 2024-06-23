import binascii, os

print(str(binascii.hexlify(os.urandom(16)))[2:-1])