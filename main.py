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
        self.tabs = QTabWidget(
            self, 
            movable=True, 
            tabShape=QTabWidget.TabShape.Rounded,
            tabPosition=QTabWidget.TabPosition.North
        )

        self.vornameLine = QLineEdit(self)
        self.nachnameLine = QLineEdit(self)
        self.strasseLine = QLineEdit(self)
        self.plzLine = QLineEdit(self)
        self.ortLine = QLineEdit(self)
        self.handyLine = QLineEdit(self)
        self.emailLine = QLineEdit(self)
        self.websiteLine = QLineEdit(self)

        generateBtn = QPushButton('Generate')
        generateBtn.clicked.connect(self.get_tab_index)
        cancelBtn = QPushButton('Cancel')

        # personal page
        vcard_page = QWidget(self)
        layout = QFormLayout()
        vcard_page.setLayout(layout)
        layout.addRow('Vorname:', self.vornameLine)
        layout.addRow('Nachname:', self.nachnameLine)
        layout.addRow('Strasse', self.strasseLine)
        layout.addRow('PLZ:', self.plzLine)
        layout.addRow('Ort:', self.ortLine)
        layout.addRow('Handy:', self.handyLine)
        layout.addRow('E-Mail:', self.emailLine)
        layout.addRow('Website:', self.websiteLine)

        # contact page
        contact_page = QWidget(self)
        layout = QFormLayout()
        contact_page.setLayout(layout)
        #layout.addRow('Handy:', self.handyLine)
        #layout.addRow('E-Mail:', self.emailLine)

        # add page to the tab widget
        self.tabs.addTab(vcard_page, 'VCARD')
        self.tabs.addTab(contact_page, 'Contact Info')

        main_layout.addWidget(self.tabs, 0, 0, 2, 1)
        main_layout.addWidget(generateBtn, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(cancelBtn, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.show()

    def get_tab_index(self):
        tabIndex = self.tabs.currentIndex()
        if(tabIndex == 0):
            self.make_vcard_qr_code(
                name = str(self.vornameLine.text() + " " + self.nachnameLine.text()),
                street = self.strasseLine.text(),
                code = self.plzLine.text(),
                city = self.ortLine.text(),
                phone = self.handyLine.text(),
                email = self.emailLine.text(),
                website = self.websiteLine.text(),
            )

    def make_vcard_qr_code(self, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        street = kwargs.get('street')
        city = kwargs.get('city')
        code = kwargs.get('code')

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