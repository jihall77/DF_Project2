cipher = "3wzf8RYd5zzPh5icWk3YAhnqZ4Rr4y3azeMSGpJc49s4utBMjUyAkeHhTGvzTCZ5gfDmEHLYrXqdVVxuB"
key = "BESURETODRINKYOUROVALTINE"

hex_cipher = list()
hex_key = list()

hex_decode = list()

for c_text in cipher:
    hex_cipher.append(ord(c_text))

#print(hex_cipher)

for k_text in key:
    hex_key.append(ord(k_text))


i = 0
for c_hex in hex_cipher:
    d_text = c_hex + hex_key[i]
    if d_text > 0x7f:
        d_text = d_text - 0x7f
    hex_decode.append(d_text)
    i += 1
    if i >= len(hex_key):
        i = 0

print(hex_decode)

d_string = ""

for d_text in hex_decode:
    d_string += chr(d_text)

print(d_string)