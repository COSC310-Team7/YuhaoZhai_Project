# # Google Translate API

# pip install googletrans==3.1.0a0


from googletrans import Translator

translator = Translator()
result = translator.translate('What is your name', src='en', dest='ur')

print(result.src)
print(result.dest)
print(result.origin)
print(result.text)


detector = Translator()
dec = detector.detect('آپ کا نام کیا ہے')
print(dec)
