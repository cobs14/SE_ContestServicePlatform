import rsa

pubkey, pri = rsa.newkeys(512)
pub = pubkey.save_pkcs1().decode()
# pub = pub[pub.find('\n') + 1:pub.rfind('\n', 0, -1)]
# print(pub)
p = rsa.PublicKey.load_pkcs1(pub.encode())
a = rsa.encrypt('aaaaaa'.encode(), p)
print(rsa.decrypt(a, pri).decode())
