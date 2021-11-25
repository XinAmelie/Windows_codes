# coding=utf-8
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Hash import SHA
import base64
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto import Random
from Crypto.PublicKey import RSA



# key的长度2048

random_generator = Random.new().read
rsa = RSA.generate(2048, random_generator)

# 初始化的密钥和公钥，得到文件
# 执行一次就行，得到private_a.rsa  得到public_a.rsa 信息数据
'''
random_generator = Random.new().read
rsa = RSA.generate(2048, random_generator)
# 生成私钥
private_key = rsa.exportKey()
print(private_key.decode('utf-8'))
print("-" * 30 + "分割线" + "-" * 30)
# 生成公钥
public_key = rsa.publickey().exportKey()
print(public_key.decode('utf-8'))

'''



class Unlock_Pwd():
    '''公钥加密，私钥解密'''
    def ecreate_keys(self):
            '''导入密钥和公钥,生成文件'''
            private_key = rsa.exportKey()
            with open("private_a.rsa", 'wb') as f:
                f.write(private_key)

            public_key = rsa.publickey().exportKey()
            with open("public_a.rsa", 'wb') as f:
                f.write(public_key)

        # 使用公钥对内容进行rsa加密
    def encrypt(self,message):
            with open('public_a.rsa') as f:
                key = f.read()
                pub_key = RSA.importKey(str(key))
                cipher = PKCS1_cipher.new(pub_key)
                rsa_text = base64.b64encode(cipher.encrypt(bytes(message.encode("utf8"))))
                print(rsa_text.decode('utf-8'))
                return rsa_text

        # 使用私钥对内容进行rsa解密
    def  decrypt(self,rsa_text):
            with open('private_a.rsa') as f:
                key = f.read()
                pri_key = RSA.importKey(key)
                cipher = PKCS1_cipher.new(pri_key)
                back_text = cipher.decrypt(base64.b64decode(rsa_text), 0)
                print(back_text.decode('utf-8'))


class verify_key():
    '''私钥签名，公钥验证'''
    def prikey_sigin(self):
        '''使用私钥生成签名'''
        # message = "需要加密的信息"
        with open('private_a.rsa') as f:
            key = f.read()
            pri_key = RSA.importKey(key)
            signer = PKCS1_signature.new(pri_key)
            digest = SHA.new()
            digest.update(message.encode("utf8"))
            sign = signer.sign(digest)
            signature = base64.b64encode(sign)
            print(signature.decode('utf-8'))
            return signature

    def pubkey_verify(self, signature):
        # 使用公钥验证签名
        with open('public_a.rsa') as f:
            key = f.read()
            pub_key = RSA.importKey(key)
            verifier = PKCS1_signature.new(pub_key)
            digest = SHA.new()
            digest.update(message.encode("utf8"))
            res = verifier.verify(digest, base64.b64decode(signature))
            print(res)
            return res


if __name__ == '__main__':


    # # 传入公钥加密的内容，利用私钥进行解密

    Un = Unlock_Pwd()
    # rsa_text = "A0GlUvX7XxzIaMA6JuTKS6PWQkLP+oNlJIW6FcP9sK/qdg08r0+xG6+D7p29rUoJcQz6OCqjToElddHHRKytvu7CCyGv+baPyncAI6EF8OTFuGoAqJ3kVC6e7FOezn/n9maCVdQSu4eMdairM/1wWPbGh/B6SfKB4fgUwEvKVPt1xBE0UJnm+Z8Z+Ir8tdFGv0iLxPjXIN+Ewx0apbeAj5P8aH9Lchhmbztq1VKnXLfaO4ethnEEH8+puuvNg6a52hMyPIxwnFp47UTXNyQkXkRe1oKavhSbHn7O5HJLKF3coFItubiuOM5s7KmlqD9VFMc8rXj4OQAVyC0HOaF7BA=="
    # message1 = rsa_text
    # Un.encrypt(message1)

    # Un.decrypt(rsa_text)
    #
    # print('---------分割线--------')
    #
    # # 先加密参数，再解密
    message = 'https://files.hrloo.com/www/uploadfile/2021/0908/585ea8df308f927ea2ab537ad4cb2a42.jpg'
    rsa_text1 =Un.encrypt(message)
    lase_text1 = Un.decrypt(rsa_text1)

    print('---------分割线--------')
    #
    # # 传入私钥签名的message,利用公钥验证签名
    # message = "300"
    # Var = verify_key()
    # res_tex = Var.prikey_sigin()
    # Var.pubkey_verify(res_tex)


