from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')

# 加密函数
def encrypt(text, key):
    key = key.encode('utf-8')
    mode = AES.MODE_ECB
    text = add_to_16(text)
    cryptos = AES.new(key, mode)

    cipher_text = cryptos.encrypt(text)
    return b2a_hex(cipher_text)

def encrypt_1(text, key):
    key = key.encode('utf-8')
    mode = AES.MODE_ECB
    cryptos = AES.new(key, mode)
    cipher_text = cryptos.encrypt(text)
    return b2a_hex(cipher_text)

# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text, key):
    key = key.encode('utf-8')
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return plain_text

def decrypt_1(text, key):
    key = key.encode('utf-8')
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(text)
    return plain_text


if __name__ == '__main__':
    k1 = "9999999999999999"
    k2 = "1111111111111111"
    a = encrypt("hello world", k1)  # 加密
    print("加密1：", a)
    b = encrypt_1(a, k2)
    print("加密2:", b)

    c = decrypt(b, k2)  # 解密
    print("解密2：", c)
    d = decrypt_1(a, k1)
    print("解密1:", d)
