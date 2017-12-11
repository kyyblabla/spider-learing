from PIL import Image

im = Image.open("captcha.jpg")
im.show()
im.close()
