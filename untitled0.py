alphabet = "abcçdefgğhiıjklmnoöprsştuüvyz"


print("give a text to encrypt")
text = input()
def encryption(text):
    x=""
    for char in text:
        x += "+"
        for z in alphabet:
           if char == z:
             x += str(alphabet.index(char))
             
    return x
       