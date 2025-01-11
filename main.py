import qrcode
import vobject

name = input("Enter your name: ")
email = input("Enter your email: ")
phone = input("Enter your mobile phone number: ")
street = input("Enter your street: ")
city = input("Enter your city: ")
code = input("Enter your code: ")

# Create a vCard
vcard = vobject.vCard()
vcard.add('fn').value = name
vcard.add('email').value = email
vcard.add('tel').value = vobject.vcard.Telephone(phone=phone, type='cell')
vcard.add('adr').value = vobject.vcard.Address(street=street , code=code, city=city)

# Convert vCard to string
vcard_string = vcard.serialize()

# Generate a QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(vcard_string)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill='black', back_color='white')

# Save the image to a file
img.save("qrcode.png")