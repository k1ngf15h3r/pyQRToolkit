import sys

from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import QApplication, QWidget, QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton, QLabel, QMenu, QMessageBox, QCalendarWidget, QCheckBox
from PyQt6.QtCore import Qt

import datetime
import segno
import segno.helpers
import vobject
from dotenv import load_dotenv, find_dotenv, dotenv_values, set_key

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

        self.firmaLine = QLineEdit(self)
        self.positionLine = QLineEdit(self)
        self.vornameLine = QLineEdit(self)
        self.nachnameLine = QLineEdit(self)
        self.strasseLine = QLineEdit(self)
        self.plzLine = QLineEdit(self)
        self.ortLine = QLineEdit(self)
        self.telefonLine = QLineEdit(self)
        self.faxLine = QLineEdit(self)
        self.handyLine = QLineEdit(self)
        self.emailLine = QLineEdit(self)
        self.websiteLine = QLineEdit(self)

        # personal page
        vcard_page = QWidget(self)
        layout = QFormLayout()
        vcard_page.setLayout(layout)
        layout.addRow('Firma:', self.firmaLine)
        layout.addRow('Position:', self.positionLine)
        layout.addRow('Vorname:', self.vornameLine)
        layout.addRow('Nachname:', self.nachnameLine)
        layout.addRow('Strasse', self.strasseLine)
        layout.addRow('PLZ:', self.plzLine)
        layout.addRow('Ort:', self.ortLine)
        layout.addRow('Telefon:', self.telefonLine)
        layout.addRow('Fax:', self.faxLine)
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

        self.save_env = QCheckBox(self)
        self.save_env.setText("Werte speichern")
        self.save_env.setChecked(False)

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
        self.main_layout.addWidget(self.save_env, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(generateBtn, 4, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(cancelBtn, 4, 0, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.label, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        self.check_env()

        self.show()

    def check_env(self):
        env_values = dotenv_values('.env')
        if(env_values):
            try:
                self.firmaLine.setText(env_values['VCARD_FIRMA'])
                self.positionLine.setText(env_values['VCARD_POSITION'])
                self.vornameLine.setText(env_values['VCARD_VORNAME'])
                self.nachnameLine.setText(env_values['VCARD_NACHNAME'])
                self.strasseLine.setText(env_values['VCARD_STREET'])
                self.plzLine.setText(env_values['VCARD_CODE'])
                self.ortLine.setText(env_values['VCARD_CITY'])
                self.telefonLine.setText(env_values['VCARD_TELEFON'])
                self.faxLine.setText(env_values['VCARD_FAX'])
                self.handyLine.setText(env_values['VCARD_PHONE'])
                self.emailLine.setText(env_values['VCARD_EMAIL'])
                self.websiteLine.setText(env_values['VCARD_WEBSITE'])
                self.empfaenger.setText(env_values['INVOICE_EMPFAENGER'])
                self.iban.setText(env_values['INVOICE_IBAN'])
                self.betrag.setText(env_values['INVOICE_BETRAG'])
                self.verwendungszweck.setText(env_values['INVOICE_VERWENDUNGSZWECK'])
            except KeyError as e:
                print(f"KeyError: {e}")

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
                    firma = self.firmaLine.text(),
                    position = self.positionLine.text(),
                    name = str(self.vornameLine.text() + " " + self.nachnameLine.text()),
                    street = self.strasseLine.text(),
                    code = self.plzLine.text(),
                    city = self.ortLine.text(),
                    phone = self.telefonLine.text(),
                    fax = self.faxLine.text(),
                    mobile = self.handyLine.text(),
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
        if(self.save_env.isChecked()):
            set_key('.env', 'VCARD_FIRMA', self.firmaLine.text())
            set_key('.env', 'VCARD_POSITION', self.positionLine.text())
            set_key('.env', 'VCARD_VORNAME', self.vornameLine.text())
            set_key('.env', 'VCARD_NACHNAME', self.nachnameLine.text())
            set_key('.env', 'VCARD_STREET', self.strasseLine.text())
            set_key('.env', 'VCARD_CODE', self.plzLine.text())
            set_key('.env', 'VCARD_CITY', self.ortLine.text())
            set_key('.env', 'VCARD_TELEFON', self.telefonLine.text())
            set_key('.env', 'VCARD_FAX', self.faxLine.text())
            set_key('.env', 'VCARD_PHONE', self.handyLine.text())
            set_key('.env', 'VCARD_EMAIL', self.emailLine.text())
            set_key('.env', 'VCARD_WEBSITE', self.websiteLine.text())

        firma = kwargs.get('firma')
        position = kwargs.get('position')
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        fax = kwargs.get('fax')
        mobile = kwargs.get('mobile')
        street = kwargs.get('street')
        city = kwargs.get('city')
        code = kwargs.get('code')
        website = kwargs.get('website')

        # Create a vCard
        vcard = vobject.vCard()
        if(firma):
            vcard.add('org').value = firma
        if(position):
            vcard.add('title').value = position
        if(name):
            vcard.add('fn').value = name
        if(street and city and code):
            vcard.add('adr').value = vobject.vcard.Address(street=street , code=code, city=city)
        if(phone):
            vcard.add('tel').value = phone
            vcard.tel.type_param = 'work'
        if(fax):
            vcard.add('tel').value = fax
            vcard.tel.type_param = 'fax'
        if(mobile):
            vcard.add('tel').value = phone
            vcard.tel.type_param = 'cell'
        if(email):
            vcard.add('email').value = email
        if(website):
            vcard.add('url').value = "https://"+website
        

        # Convert vCard to string
        vcard_string = vcard.serialize()

        # Generate a segno QR code
        qrcode = segno.make(vcard_string)
        qrcode.save("vcard_qrcode.png", scale=3)

        pixmap = QPixmap('vcard_qrcode.png')
        self.label.setPixmap(pixmap)

        print("Vcard QR Code generated successfully!")
        self.label.customContextMenuRequested.connect(self.on_qr_code_context_menu)

    def make_invoice_qr_code(self, **kwargs):
        if(self.save_env.isChecked()):
            set_key('.env', 'INVOICE_EMPFAENGER', self.empfaenger.text())
            set_key('.env', 'INVOICE_IBAN', self.iban.text())
            set_key('.env', 'INVOICE_BETRAG', self.betrag.text())
            set_key('.env', 'INVOICE_VERWENDUNGSZWECK', self.verwendungszweck.text())

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