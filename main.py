import sys

from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import QApplication, QWidget, QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton, QLabel, QMenu, QMessageBox
from PyQt6.QtCore import Qt

import segno
import segno.helpers
import vobject

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("QR Code Generator")

        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)

        # create a tab widget
        self.tabs = QTabWidget(
            self, 
            movable=True, 
            tabShape=QTabWidget.TabShape.Rounded,
            tabPosition=QTabWidget.TabPosition.North
        )

        self.vornameLine = QLineEdit(self)
        self.nachnameLine = QLineEdit(self)
        self.dateofbirth = QDateEdit(self)
        self.dateofbirth.setDate(self.dateofbirth.date().addYears(-18))
        self.strasseLine = QLineEdit(self)
        self.plzLine = QLineEdit(self)
        self.ortLine = QLineEdit(self)
        self.handyLine = QLineEdit(self)
        self.emailLine = QLineEdit(self)
        self.websiteLine = QLineEdit(self)

        # personal page
        vcard_page = QWidget(self)
        layout = QFormLayout()
        vcard_page.setLayout(layout)
        layout.addRow('Vorname:', self.vornameLine)
        layout.addRow('Nachname:', self.nachnameLine)
        layout.addRow('Geburtsdatum:', self.dateofbirth)
        layout.addRow('Strasse', self.strasseLine)
        layout.addRow('PLZ:', self.plzLine)
        layout.addRow('Ort:', self.ortLine)
        layout.addRow('Handy:', self.handyLine)
        layout.addRow('E-Mail:', self.emailLine)
        layout.addRow('Website:', self.websiteLine)

        self.empfaenger = QLineEdit(self)
        self.iban = QLineEdit(self)
        self.betrag = QLineEdit(self)
        self.verwendungszweck = QLineEdit(self)

        # invoice page
        invoice_page = QWidget(self)
        layout = QFormLayout()
        invoice_page.setLayout(layout)
        layout.addRow('Name:', self.empfaenger)
        layout.addRow('IBAN:', self.iban)
        layout.addRow('Betrag:', self.betrag)
        layout.addRow('Verwendungszweck:', self.verwendungszweck)

        self.label = QLabel(self)
        self.label.setBaseSize(300, 300)
        self.label.setText("QR Code")
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        generateBtn = QPushButton('Generate')
        generateBtn.clicked.connect(self.get_tab_index)
        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(sys.exit)

        # add page to the tab widget
        self.tabs.addTab(vcard_page, 'VCARD')
        self.tabs.addTab(invoice_page, 'Invoice')

        self.main_layout.addWidget(self.tabs, 0, 0, 2, 1)
        self.main_layout.addWidget(generateBtn, 3, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(cancelBtn, 3, 0, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.label, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        self.show()

    def on_qr_code_context_menu(self):
        menu = QMenu(self)
        copy_action = menu.addAction("Copy to Clipboard")
        save_action = menu.addAction("Save As")
        
        menu.popup(QCursor.pos())
        action = menu.exec()

        if action == copy_action:
            self.copy_to_clipboard()
        elif action == save_action:
            self.save_as()

    def copy_to_clipboard(self):
        QApplication.clipboard().setPixmap(self.label.pixmap())
        print("Copy to clipboard")
        pass

    def save_as(self):
        print("Save as")
        pass

    def get_tab_index(self):
        tabIndex = self.tabs.currentIndex()
        if(tabIndex == 0):
            if(self.vornameLine.text() == "" or self.nachnameLine.text() == ""):
                msgBox = QMessageBox(self)
                msgBox.setText("Vorname und Nachname sind mindestens erforderlich!")
                msgBox.setWindowTitle("Warnung")
                msgBox.setIcon(QMessageBox.Icon.Warning)
                msgBox.exec()
                print("Please fill all the required fields!")
            else:
                self.make_vcard_qr_code(
                    name = str(self.vornameLine.text() + " " + self.nachnameLine.text()),
                    dob = self.dateofbirth.date().toString("yyyy-MM-dd"),
                    street = self.strasseLine.text(),
                    code = self.plzLine.text(),
                    city = self.ortLine.text(),
                    phone = self.handyLine.text(),
                    email = self.emailLine.text(),
                    website = self.websiteLine.text(),
                )
        if(tabIndex == 1):
            if(self.empfaenger.text() == "" or self.iban.text() == "" or self.betrag.text() == "" or self.verwendungszweck.text() == ""):
                msgBox = QMessageBox(self)
                msgBox.setText("Alle Felder müssen ausgefüllt sein!")
                msgBox.setWindowTitle("Warnung")
                msgBox.setIcon(QMessageBox.Icon.Warning)
                msgBox.exec()
                print("Please fill all the required fields!")
            else:
                self.make_invoice_qr_code(
                    empfaenger = self.empfaenger.text(),
                    iban = self.iban.text(),
                    betrag = self.betrag.text(),
                    verwendungszweck = self.verwendungszweck.text()
                )

    def make_vcard_qr_code(self, **kwargs):
        name = kwargs.get('name')
        dob = kwargs.get('dob')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        street = kwargs.get('street')
        city = kwargs.get('city')
        code = kwargs.get('code')
        website = kwargs.get('website')

        # Create a vCard
        vcard = vobject.vCard()
        if(name):
            vcard.add('fn').value = name
        if(dob):
            vcard.add('bday').value = dob
        if(street and city and code):
            vcard.add('adr').value = vobject.vcard.Address(street=street , code=code, city=city)
        if(phone):
            vcard.add('tel')
            vcard.tel.type_param = 'cell'
            vcard.tel.value = phone
        if(email):
            vcard.add('email').value = email
        if(website):
            vcard.add('url').value = "https://"+website
        

        # Convert vCard to string
        vcard_string = vcard.serialize()

        # Generate a segno QR code
        qrcode = segno.make(vcard_string)
        qrcode.save("vcard_qrcode.png", scale=10)

        pixmap = QPixmap('vcard_qrcode.png')
        self.label.setPixmap(pixmap)

        print("Vcard QR Code generated successfully!")
        self.label.customContextMenuRequested.connect(self.on_qr_code_context_menu)

    def make_invoice_qr_code(self, **kwargs):
        empfaenger = kwargs.get('empfaenger')
        iban = kwargs.get('iban')
        betrag = kwargs.get('betrag')
        verwendungszweck = kwargs.get('verwendungszweck')

        # Create a invoice qr code
        qrcode = segno.helpers.make_epc_qr(
            name=empfaenger,
            iban=iban,
            amount=betrag,
            text=verwendungszweck
        )

        qrcode.save("invoice_qrcode.png", scale=3)

        pixmap = QPixmap('invoice_qrcode.png')
        self.label.setPixmap(pixmap)

        print("Invoice QR Code generated successfully!")
        self.label.customContextMenuRequested.connect(self.on_qr_code_context_menu)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())