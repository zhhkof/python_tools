import hashlib
m=hashlib.md5()
m.update(b'test')
print(m.hexdigest())
print(list('test'))
