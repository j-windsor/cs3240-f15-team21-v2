import sys
import requests
from requests.auth import HTTPBasicAuth
from PySide.QtCore import *
from PySide.QtGui import *
import os

GFolders = []
authentication = ""

class Login(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.textName = QLineEdit(self)
        self.textName.setPlaceholderText("Username")
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.textPass.setPlaceholderText("Password")
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        global authentication
        authentication = HTTPBasicAuth(self.textName.text(), self.textPass.text())
        r = requests.get('https://guarded-mesa-1337.herokuapp.com/reports/api_available_reports', auth=authentication)
        print(r.cookies)
        #self.token = r.cookies['sessionid']
        #authentication = {'sessionid': token}
        folders = r.json()
        if 'detail' in folders:
            errmsg = folders['detail']
            QMessageBox.warning(self, 'Error', errmsg)
        else:
            global GFolders
            GFolders = folders
            self.accept()

class Window(QWidget):

    def __init__(self):

        QWidget.__init__(self)

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
                newfolder.addChild(newreport)
                for attachment in report['attachment_set']:
                    newattach = QTreeWidgetItem()
                    newattach.setText(0, "Attachment: " + attachment['name'])
                    newattach.setText(1, "Encrypted: " + str(attachment['encrypted']))
                    newattach.setText(2, "Download Attachment Below")
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
        self.layoutside.addWidget(self.titlelabel)
        self.layoutside.addWidget(self.detaillabel)
        self.layoutside.addWidget(self.descriptionlabel)
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
        if self.treeView.currentItem().childCount() == 0:
            self.buttonDownload.setEnabled(True)
        else:
            self.buttonDownload.setEnabled(False)

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
        print(authentication)
        r = requests.get(downloadurl, auth=authentication)
        if r.text == "denied":
            QMessageBox.warning(self, 'Error', "You do not have access to this file")

        if self.treeView.currentItem().text(1) == "Encrypted: True":
            self.showKeyDialog()
            ## decrypt file
        file_extension = "*"+os.path.splitext(self.treeView.currentItem().text(3))[1]
        path, _ = QFileDialog.getSaveFileName(self, "Save File", os.getcwd(), file_extension, file_extension)
        print(r.content)
        with open(path, 'wb') as f:
            f.write(r.content)



    def showKeyDialog(self):
        text, ok = QInputDialog.getText(self, 'Key Input',
            'Enter Decryption Key:')
        if ok:
            self.decryptkey = str(text)



if __name__ == '__main__':

    app = QApplication(sys.argv)

    if Login().exec_() == QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())
