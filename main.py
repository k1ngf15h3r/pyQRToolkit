import sys

from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt

import segno
import vobject

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("QR Code Generator")

        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        # create a tab widget
        tabs = QTabWidget(
            self, 
            movable=True, 
            tabShape=QTabWidget.TabShape.Rounded,
            tabPosition=QTabWidget.TabPosition.North
        )


        # personal page
        vcard_page = QWidget(self)
        layout = QFormLayout()
        vcard_page.setLayout(layout)
        layout.addRow('Vorname:', QLineEdit(self))
        layout.addRow('Nachname:', QLineEdit(self))
        layout.addRow('Strasse:', QLineEdit(self))
        layout.addRow('PLZ:', QLineEdit(self))
        layout.addRow('Ort:', QLineEdit(self))
        layout.addRow('Handy:', QLineEdit(self))
        layout.addRow('E-Mail:', QLineEdit(self))
        layout.addRow('Website:', QLineEdit(self))

        # contact page
        contact_page = QWidget(self)
        layout = QFormLayout()
        contact_page.setLayout(layout)
        layout.addRow('Phone Number:', QLineEdit(self))
        layout.addRow('Email Address:', QLineEdit(self))

        # add page to the tab widget
        tabs.addTab(vcard_page, 'VCARD')
        tabs.addTab(contact_page, 'Contact Info')

        main_layout.addWidget(tabs, 0, 0, 2, 1)
        main_layout.addWidget(QPushButton('Save'), 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(QPushButton('Cancel'), 2, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.show()

    def make_vcard_qr_code():
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone = input("Enter your mobile phone number: ")
        street = input("Enter your street: ")
        city = input("Enter your city: ")
        code = input("Enter your code: ")

        # Create a vCard
        vcard = vobject.vCard()
        if(name):
            vcard.add('fn').value = name
        if(email):
            vcard.add('email').value = email
        if(phone):
            vcard.add('tel')
            vcard.tel.type_param = 'cell'
            vcard.tel.value = phone
        if(street and city and code):
            vcard.add('adr').value = vobject.vcard.Address(street=street , code=code, city=city)

        # Convert vCard to string
        vcard_string = vcard.serialize()

        # Generate a segno QR code
        qrcode = segno.make(vcard_string)
        qrcode.save("qrcode.png", scale=10)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())