import sys
import requests
from requests.auth import HTTPBasicAuth
from PySide.QtCore import *
from PySide.QtGui import *
import os
import random
import string
from Crypto.Hash import MD5
from Crypto.Hash import SHA256
from Crypto.Cipher import DES

GFolders = []
authentication = ""

class Login(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("SecureShare Login")
        self.inLabel = QLabel(self)
        self.inLabel.setText("Login to SecureShare")
        self.inLabel.setAlignment(4)
        self.textName = QLineEdit(self)
        self.textName.setPlaceholderText("Username")
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.textPass.setPlaceholderText("Password")
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QVBoxLayout(self)
        layout.addWidget(self.inLabel)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        global authentication
        authentication = HTTPBasicAuth(self.textName.text(), self.textPass.text())
        r = requests.get('https://guarded-mesa-1337.herokuapp.com/reports/api_available_reports', auth=authentication)
        print(r.text)
        folders = r.json()
        if 'detail' in folders:
            errmsg = folders['detail']
            QMessageBox.warning(self, 'Error', errmsg)
        else:
            global GFolders
            GFolders = folders
            self.accept()

class UploadDialog(QDialog):
    def __init__(self, report_id):
        QDialog.__init__(self)
        self.setWindowTitle("SecureShare")
        self.reportId = report_id
        self.textName = QLineEdit(self)
        self.buttonFile = QPushButton('Choose File', self)
        self.buttonFile.clicked.connect(self.handleFile)
        self.pathLabel = QLabel(self)
        font = self.pathLabel.font();
        font.setPointSize(10)
        self.pathLabel.setFont(font)
        self.pathLabel.setText("")
        self.encryptedBox = QCheckBox("Encrypted")
        self.buttonSubmit = QPushButton('Add Attachment', self)
        self.buttonSubmit.clicked.connect(self.handleSubmit)
        layout = QFormLayout(self)
        layout.addRow("Attachment Name:", self.textName)
        layout.addRow("File: ", self.buttonFile)
        layout.addRow(self.pathLabel)
        layout.addRow("File Encryption: ", self.encryptedBox)
        layout.addRow(self.buttonSubmit)
        self.setFixedSize(250, 150)
        self.setLayout(layout)

    def handleFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", os.getcwd())
        self.pathLabel.setText(path)

    def handleSubmit(self):
        #find hash
        h = MD5.new()
        chunk_size = 8192
        with open(self.pathLabel.text(), 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if len(chunk) == 0:
                    break
                h.update(chunk)

        #encrypt if checked
        if self.pathLabel.text() == "":
            QMessageBox.warning(self, 'Error', "You must choose a file to upload!")
            return

        f
        if self.encryptedBox.isChecked():
            random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            print(encrypt_file(self.pathLabel.text(), random_string.encode()))
            QMessageBox.information(self, 'Key', "Your decryption key is " + random_string)
            encfilename = self.pathLabel.text()+".enc"
            print(encfilename)
            f = open(encfilename, 'rb')
        else:
            f = open(self.pathLabel.text(), 'rb')

        files = {'upload': f}
        post_data = {"name": self.textName.text(), "key":h.hexdigest(), "encrypted": self.encryptedBox.isChecked(), "report": self.reportId}
        global authentication
        r = requests.post('https://guarded-mesa-1337.herokuapp.com/reports/api_add_report/', files=files, data=post_data, auth=authentication)
        resp = r.json()
        if self.textName.text() not in resp.values():
            errmsg = ""
            for key in resp.keys():
                errmsg = errmsg + (key + ": " + resp[key][0] + "\n")
            QMessageBox.warning(self, 'Error', errmsg)
        else:
            self.r = resp
            self.done(0)

    def getR(self):
        return self.r


class Window(QWidget):

    def __init__(self):

        QWidget.__init__(self)
        self.setWindowTitle("SecureShare")
        ########### DATA PARSE
        global GFolders
        print(GFolders)
        self.data = []
        for folder in GFolders:
            newfolder = QTreeWidgetItem()
            newfolder.setText(0, "Folder: " + folder['label'])
            self.data.append(newfolder)
            for report in folder['reports']:
                newreport = QTreeWidgetItem()
                newreport.setText(0, "Report: " + report['title'])
                newreport.setText(1, "Created: " + report['create_date'])
                newreport.setText(2, report['description'])
                newreport.setText(3, str(report['id']))
                newfolder.addChild(newreport)
                for attachment in report['attachment_set']:
                    newattach = QTreeWidgetItem()
                    newattach.setText(0, "Attachment: " + attachment['name'])
                    newattach.setText(1, "Encrypted: " + str(attachment['encrypted']))
                    newattach.setText(2, "Checksum: " + attachment['key'])
                    newattach.setText(3, attachment['upload'])
                    newattach.setText(4, str(attachment['id']))
                    newreport.addChild(newattach)
        self.publicreportitem = QTreeWidgetItem()
        self.publicreportitem.setText(0, "PUBLIC REPORTS")
        self.data.append(self.publicreportitem)



        self.treeView = QTreeWidget()
        self.treeView.clicked.connect(self.itemClicked)
        self.treeView.addTopLevelItems(self.data)

        self.layoutside = QVBoxLayout()
        self.titlelabel = QLabel()
        self.titlelabel.setText("")
        font = self.titlelabel.font();
        font.setPointSize(20)
        font.setBold(True)
        self.titlelabel.setFont(font)
        self.detaillabel = QLabel()
        self.detaillabel.setText("")
        self.descriptionlabel = QLabel()
        self.descriptionlabel.setWordWrap(True)
        self.descriptionlabel.setText("")
        self.buttonDownload = QPushButton('Download', self)
        self.buttonDownload.setEnabled(False)
        self.buttonDownload.clicked.connect(self.downloadClicked)
        self.buttonUpload = QPushButton('Add Attachment to Report', self)
        self.buttonUpload.setEnabled(False)
        #self.buttonUpload.setEnabled(False)
        self.buttonUpload.clicked.connect(self.uploadClicked)
        self.layoutside.addWidget(self.titlelabel)
        self.layoutside.addWidget(self.detaillabel)
        self.layoutside.addWidget(self.descriptionlabel)
        self.layoutside.addWidget(self.buttonUpload)
        self.layoutside.addWidget(self.buttonDownload)

        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        layout.addSpacing(5)
        layout.addLayout(self.layoutside)

        self.setLayout(layout)
        self.decryptkey = ""

    def itemClicked(self):
        self.titlelabel.setText(self.treeView.currentItem().text(0))
        self.detaillabel.setText(self.treeView.currentItem().text(1))
        self.descriptionlabel.setText(self.treeView.currentItem().text(2))
        if self.treeView.currentItem().text(0).startswith("Attachment"):
            self.buttonDownload.setEnabled(True)
        else:
            self.buttonDownload.setEnabled(False)
        if self.treeView.currentItem().text(0).startswith("Report"):
            self.buttonUpload.setEnabled(True)
        else:
            self.buttonUpload.setEnabled(False)

        if self.treeView.currentItem().text(0) == "PUBLIC REPORTS":
            if self.treeView.currentItem().childCount() == 0:
                self.treeView.setEnabled(False)
                r = requests.get('https://guarded-mesa-1337.herokuapp.com/reports/api_public_reports')
                publicreports = r.json()
                for report in publicreports:
                    newreport = QTreeWidgetItem()
                    newreport.setText(0, "Report: " + report['title'])
                    newreport.setText(1, "Created: " + report['create_date'])
                    newreport.setText(2, report['description'])
                    self.publicreportitem.addChild(newreport)
                    for attachment in report['attachment_set']:
                        newattach = QTreeWidgetItem()
                        newattach.setText(0, "Attachment: " + attachment['name'])
                        newattach.setText(1, "Encrypted: " + str(attachment['encrypted']))
                        newattach.setText(2, "Download Attachment Below")
                        newattach.setText(3, attachment['upload'])
                        newreport.addChild(newattach)
                self.treeView.setEnabled(True)
                self.publicreportitem.setExpanded(True)



    def downloadClicked(self):
        #download file
        global authentication
        downloadurl = 'https://guarded-mesa-1337.herokuapp.com/reports/'+self.treeView.currentItem().text(4)+'/download_attachment'
        print(downloadurl)
        r = requests.get(downloadurl, auth=authentication)
        if r.text == "denied":
            QMessageBox.warning(self, 'Error', "You do not have access to this file")

        if self.treeView.currentItem().text(1) == "Encrypted: True":
            file_extension = "*."+self.treeView.currentItem().text(3).split(".")[1]
            print(file_extension)
            path, _ = QFileDialog.getSaveFileName(self, "Save File", os.getcwd(), file_extension, file_extension)
            self.showKeyDialog()
            decrypt_file(r.content, self.decryptkey.encode(), path)
        else:
            file_extension = "*"+os.path.splitext(self.treeView.currentItem().text(3))[1]
            print(os.path.splitext(self.treeView.currentItem().text(3)))
            path, _ = QFileDialog.getSaveFileName(self, "Save File", os.getcwd(), file_extension, file_extension)
            with open(path, 'wb') as f:
                f.write(r.content)



    def showKeyDialog(self):
        text, ok = QInputDialog.getText(self, 'Key Input', 'Enter Decryption Key:')
        if ok:
            self.decryptkey = str(text)

    def uploadClicked(self):
        upload_dialog = UploadDialog(self.treeView.currentItem().text(3))
        upload_dialog.exec_()
        # after dialog...
        newattach = QTreeWidgetItem()
        attachment = upload_dialog.getR()
        newattach.setText(0, "Attachment: " + attachment['name'])
        newattach.setText(1, "Encrypted: " + str(attachment['encrypted']))
        newattach.setText(2, "Checksum: " + attachment['key'])
        newattach.setText(3, attachment['upload'])
        newattach.setText(4, str(attachment['id']))
        self.treeView.currentItem().addChild(newattach)


def secret_sym_string(text, key):
    thehash = SHA256.new(key)
    des = DES.new(thehash.digest()[0:8], DES.MODE_ECB)
    while len(text) % 8 != 0:
        text += b'\0'
    return des.encrypt(text)

def unsecret_sym_string(text, key):
    thehash = SHA256.new(key)
    des = DES.new(thehash.digest()[0:8], DES.MODE_ECB)
    return des.decrypt(text).rstrip(b"/0")

def encrypt_file(filename, key):
    """
    Encrypts a file given the filename and key bytes
    """
    #try:
    with open(filename, "rb") as f:
        writefilename = f.name + ".enc"
        with open(writefilename, "wb") as wf:
            wf.write(secret_sym_string(f.read(), key))
    #except:
    #    return False
    #return True

def decrypt_file(content, key, writefilename):
    """
    Decrypts a file given the filename and key bytes
    """
    #try:
    with open(writefilename, "wb") as wf:
        wf.write(unsecret_sym_string(content, key))
    #except:
    #    return False
    #return True


if __name__ == '__main__':

    app = QApplication(sys.argv)

    if Login().exec_() == QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())
