# -*- coding: utf-8 -*-

# Created by ItsMatriX

# Discord: 404 - Not Found#3020
# Guild: https://discord.gg/veVcKK6NZJ

import json
from ctypes import WinDLL
from os import _exit, listdir, mkdir, remove
from os.path import expanduser, isdir, isfile, sep, split
from sys import argv
from threading import Thread
from time import sleep

import requests
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets

AppDataRoaming = expanduser(
    '~') + sep + 'AppData' + sep + 'Roaming' + sep + 'Anicord 2.0'

if not isdir(AppDataRoaming):
    mkdir(AppDataRoaming)


class WindowsDLLs:
    WindowsUser32DLL = WinDLL('user32.dll')

class Colors:
    pass


try:
    try:
        exec(open(AppDataRoaming + sep + 'style.py', 'r').read())
    except:
        class AnicordColors:
            MainColor = (95, 237, 207)
            HoverOnMainColor = (74, 186, 162)
            FormBGColor = (22, 35, 69)
            MainBGColor = (33, 46, 78)
            OnTranspHoverColor = (49, 68, 116)

    AnicordColors.MainColor = tuple(AnicordColors.MainColor)
    AnicordColors.HoverOnMainColor = tuple(AnicordColors.HoverOnMainColor)
    AnicordColors.FormBGColor = tuple(AnicordColors.FormBGColor)
    AnicordColors.MainBGColor = tuple(AnicordColors.MainBGColor)
    AnicordColors.OnTranspHoverColor = tuple(AnicordColors.OnTranspHoverColor)

    class DefaultAnicordColors:
        MainColor = (95, 237, 207)
        HoverOnMainColor = (74, 186, 162)
        FormBGColor = (22, 35, 69)
        MainBGColor = (33, 46, 78)
        OnTranspHoverColor = (49, 68, 116)

    RequiredImages = [
        'Animation.png', 'Authorization.png', 'Close.png', 'Minus.png',
        'Pin.png', 'PinDark.png', 'Run.png', 'Starting.png', 'Stop.png',
        'Timer.png'
    ]

    Matches = 0

    for file in listdir('./WhiteIcons'):
        if file in RequiredImages:
            Matches += 1

    if Matches != len(RequiredImages):
        print('No all images at WhiteIcons/.')
        exit(1)

    Recolored = []

    def RecolorImage(ImageLocation, r, g, b, name):
        ImagePIL = Image.open(ImageLocation)
        Pixels = ImagePIL.load()
        for i in range(0, ImagePIL.size[0]):
            for j in range(0, ImagePIL.size[1]):
                Pixels[i, j] = (r, g, b, Pixels[i, j][3])
                ImagePIL.putpixel((i, j), Pixels[i, j])
        Recolored.append(ImageLocation)
        ImagePIL.save(f"{name}")
        print(f'Redrawed {ImageLocation}')

    def recolorImages():
        # MainColor:
        # Animation.png
        # Authorization.png
        # Minus.png
        # Pin.png
        # Starting.png
        # Timer.png

        # FormBGColor:
        # Run.png
        # Stop.png

        # MainBGColor:
        # Close.png
        # PinDark.png

        for file in listdir('./WhiteIcons'):
            if file in [
                    'Animation.png', 'Authorization.png', 'Minus.png',
                    'Pin.png', 'Starting.png', 'Timer.png'
            ]:
                color = AnicordColors.MainColor
            elif file in ['Close.png', 'PinDark.png']:
                color = AnicordColors.MainBGColor
            elif file in ['Run.png', 'Stop.png']:
                color = AnicordColors.FormBGColor

            Thread(target=lambda: RecolorImage(f'WhiteIcons/{file}', color[
                0], color[1], color[2], AppDataRoaming + sep + file)).start()

        open(AppDataRoaming + sep + 'image_colors.py',
             'w').write('class Colors:\n'
                        f'    MainColor = {AnicordColors.MainColor}\n'
                        f'    MainBGColor = {AnicordColors.MainBGColor}\n'
                        f'    FormBGColor = {AnicordColors.FormBGColor}')

        while len(Recolored) != len(RequiredImages):
            pass

    try:
        exec(open(AppDataRoaming + sep + 'image_colors.py', 'r').read())
    except:
        recolorImages()
        exec(open(AppDataRoaming + sep + 'image_colors.py', 'r').read())

    try:
        if (Colors.MainColor != AnicordColors.MainColor) or (
                Colors.MainBGColor != AnicordColors.MainBGColor) or (
                    Colors.FormBGColor != AnicordColors.FormBGColor):
            recolorImages()
    except:
        pass

    ImCount = 0

    for file in listdir(AppDataRoaming + sep + './'):
        if file in RequiredImages:
            ImCount += 1

    if ImCount != len(RequiredImages):
        print('Recolor: At line 141')
        recolorImages()
except:
    Reply = WindowsDLLs.WindowsUser32DLL.MessageBoxW(
        0, '????????????????, ?????? ?????????????????? ????-???? ?????????? ??????????. ???? ???????????? ?????????????? ???????',
        '???? ?????????????? ??????????????????????', 4)
    if Reply == 6:
        remove(AppDataRoaming + sep + 'style.py')

    _exit(0)


def SetPresence(HttpAuthorization, StatusText=None, StatusIcon=None):
    if StatusText:
        if StatusIcon:
            HTTPRequestBody = {
                'custom_status': {
                    'text': StatusText
                },
                'status': StatusIcon
            }
        else:
            HTTPRequestBody = {'custom_status': {'text': StatusText}}
    else:
        if StatusIcon:
            HTTPRequestBody = {'status': StatusIcon}
        else:
            return None

    HTTPRequestHeaders = {'Authorization': HttpAuthorization}

    HTTPResponse = requests.patch(
        'https://discord.com/api/v9/users/@me/settings',
        json=HTTPRequestBody,
        headers=HTTPRequestHeaders)

    return HTTPResponse.status_code


def CheckToken(HttpAuthorization):
    HTTPResponse = requests.get('https://discord.com/api/v9/channels/@me',
                                headers={'Authorization': HttpAuthorization})

    HTTPResponseStatusCode = HTTPResponse.status_code

    if HTTPResponseStatusCode == 401:
        return False
    else:
        return True


def HasNoVoidLnes(Statuses):
    Statuses = Statuses.split('\n')

    line = 1

    for Status in Statuses:
        if Status == '':
            return line
        line += 1
    return True


class ApplicationState:
    AllowMainWindowMove = False


class PYQTHoverButton(QtWidgets.QPushButton):
    HoverSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(PYQTHoverButton, self).__init__(parent)

    def enterEvent(self, event):
        self.HoverSignal.emit('enterEvent')

    def leaveEvent(self, event):
        self.HoverSignal.emit('leaveEvent')


class PYQTHoverLabel(QtWidgets.QLabel):
    HoverSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(PYQTHoverLabel, self).__init__(parent)

    def enterEvent(self, event):
        self.HoverSignal.emit('enterEvent')

    def leaveEvent(self, event):
        self.HoverSignal.emit('leaveEvent')


class Ui_Application(QtWidgets.QMainWindow):

    IsPinned = False
    IsWorking = False
    IsStarting = False
    RunnerButtonChangeSignal = QtCore.pyqtSignal(dict)

    def InitWindow(self, Application):
        Application.setObjectName('Application')
        Application.resize(246, 266)
        Application.setMinimumSize(QtCore.QSize(246, 266))
        Application.setMaximumSize(QtCore.QSize(246, 266))
        Application.setStyleSheet(
            'QScrollBar:vertical {\n'
            '    border: none;\n'
            f'    background: rgb{AnicordColors.MainBGColor};\n'
            '    width: 5px;\n'
            '    margin: 12px 0 12px 0;\n'
            '}\n'
            'QScrollBar::handle:vertical {    \n'
            f'    background-color: rgb{AnicordColors.MainColor};\n'
            '    min-height: 15px;\n'
            '    border-radius: 2px;\n'
            '}\n'
            'QScrollBar::handle:vertical:hover {    \n'
            f'    background-color: rgb{AnicordColors.HoverOnMainColor};\n'
            '    min-height: 15px;\n'
            '    border-radius: 2px;\n'
            '}\n'
            'QScrollBar::handle:vertical:pressed {    \n'
            '    background-color: rgb(53, 134, 117);\n'
            '    min-height: 15px;\n'
            '    border-radius: 2px;\n'
            '}\n'
            'QScrollBar::sub-line:vertical {\n'
            '    border: none;\n'
            f'    background-color: rgb{AnicordColors.MainColor};\n'
            '    height: 10px;\n'
            '    border-radius: 2px;\n'
            '    subcontrol-position: top;\n'
            '    subcontrol-origin: margin;\n'
            '}\n'
            'QScrollBar::sub-line:vertical:hover {    \n'
            f'    background-color: rgb{AnicordColors.HoverOnMainColor};\n'
            '}\n'
            'QScrollBar::sub-line:vertical:pressed {    \n'
            '    background-color: rgb(53, 134, 117);\n'
            '}\n'
            'QScrollBar::add-line:vertical {\n'
            '    border: none;\n'
            f'    background-color: rgb{AnicordColors.MainColor};\n'
            '    height: 10px;\n'
            '    border-radius: 2px;\n'
            '    subcontrol-position: bottom;\n'
            '    subcontrol-origin: margin;\n'
            '}\n'
            'QScrollBar::add-line:vertical:hover {    \n'
            f'    background-color: rgb{AnicordColors.HoverOnMainColor};\n'
            '}\n'
            'QScrollBar::add-line:vertical:pressed {    \n'
            '    background-color: rgb(53, 134, 117);\n'
            '}\n'
            'QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n'
            '    background: none;\n'
            '}\n'
            'QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n'
            '    background: none;\n'
            '}\n'
            'QLineEdit {\n'
            '    color: rgb(255, 255, 255);\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            f'    border-color: rgb{AnicordColors.MainColor};\n'
            '    border-radius: 5;\n'
            '    border-width: 1;\n'
            '    padding-left: 3;\n'
            '    padding-right: 20;\n'
            '    border-style: solid;\n'
            '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
            '}\n'
            'QLineEdit:focus {\n'
            '    color: rgb(255, 255, 255);\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            f'    border-color: rgb{AnicordColors.MainColor};\n'
            '    border-radius: 5;\n'
            '    border-width: 2;\n'
            '    padding-left: 3;\n'
            '    padding-right: 20;\n'
            '    border-style: solid;\n'
            '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
            '}\n'
            'QPlainTextEdit {\n'
            '    color: rgb(255, 255, 255);\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            f'    border-color: rgb{AnicordColors.MainColor};\n'
            '    border-radius: 5;\n'
            '    border-width: 1;\n'
            '    padding-left: 1;\n'
            '    padding-right: 25;\n'
            '    border-style: solid;\n'
            '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
            '}\n'
            'QPlainTextEdit:focus {\n'
            '    color: rgb(255, 255, 255);\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            f'    border-color: rgb{AnicordColors.MainColor};\n'
            '    border-radius: 5;\n'
            '    border-width: 2;\n'
            '    padding-left: 1;\n'
            '    padding-right: 25;\n'
            '    border-style: solid;\n'
            '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
            '}\n'
            'QDoubleSpinBox {\n'
            '    color: rgb(255, 255, 255);\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            f'    border-color: rgb{AnicordColors.MainColor};\n'
            '    border-radius: 5;\n'
            '    border-width: 1;\n'
            '    padding-left: 3;\n'
            '    padding-right: 20;\n'
            '    border-style: solid;\n'
            '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
            '}\n'
            'QDoubleSpinBox:focus {\n'
            '    color: rgb(255, 255, 255);\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            f'    border-color: rgb{AnicordColors.MainColor};\n'
            '    border-radius: 5;\n'
            '    border-width: 2;\n'
            '    padding-left: 3;\n'
            '    padding-right: 20;\n'
            '    border-style: solid;\n'
            '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
            '}\n'
            'QToolTip {\n'
            '    font: 87 9pt \'Segoe UI Black\';\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            f'    color: rgb{AnicordColors.MainColor};\n'
            '    border-style: solid;\n'
            '    border-width: 1;\n'
            f'    border-color: rgb{AnicordColors.MainColor};\n'
            '}')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.CentralWidget = QtWidgets.QWidget(Application)
        self.CentralWidget.setObjectName('CentralWidget')
        self.FormBG = PYQTHoverLabel(self.CentralWidget)
        self.FormBG.setGeometry(QtCore.QRect(5, 30, 236, 191))
        self.FormBG.setStyleSheet(
            f'background-color: rgb{AnicordColors.FormBGColor};\n'
            'border-radius: 10')
        self.FormBG.setObjectName('FormBG')
        self.Authorization = QtWidgets.QLineEdit(self.CentralWidget)
        self.Authorization.setGeometry(QtCore.QRect(20, 45, 206, 26))
        self.Authorization.setObjectName('Authorization')
        self.IconAuthorization = PYQTHoverLabel(self.CentralWidget)
        self.IconAuthorization.setGeometry(QtCore.QRect(205, 50, 16, 16))
        self.IconAuthorization.setPixmap(QtGui.QPixmap(AppDataRoaming + sep + 'Authorization.png'))
        self.IconAuthorization.setScaledContents(True)
        self.IconAuthorization.setToolTip('?????????? ?????????????? ???????????? Discord.')
        self.IconAuthorization.setObjectName('IconAuthorization')
        self.Frames = QtWidgets.QPlainTextEdit(self.CentralWidget)
        self.Frames.setGeometry(QtCore.QRect(20, 90, 206, 71))
        self.Frames.setObjectName('Frames')
        self.IconFrames = PYQTHoverLabel(self.CentralWidget)
        self.IconFrames.setGeometry(QtCore.QRect(205, 95, 16, 16))
        self.IconFrames.setPixmap(
            QtGui.QPixmap(AppDataRoaming + sep + 'Animation.png'))
        self.IconFrames.setScaledContents(True)
        self.IconFrames.setToolTip(
            '??????????????:\n'
            '   Idle;;????????????! - ?????????? ???????????????????? ???????????? '
            '"??????????????????" ?? ???????????? "????????????!"\n'
            '   ????????????! - ?????????? ?????????????????? ???????????? "????????????!", ???????????? ???????????????? ???? ??????????.\n'
            '   idle - ?????????? ???????????????????? ???????????? "??????????????????", ???????????? ?????????????? ???? ??????????.\n\n'
            '????????????:\n'
            '    online - ?? ????????\n'
            '    idle - ??????????????????\n'
            '    dnd - ???? ????????????????????\n'
            '    invisible - ??????????????????')
        self.IconFrames.setObjectName('IconFrames')
        self.MainBG = PYQTHoverLabel(self.CentralWidget)
        self.MainBG.setGeometry(QtCore.QRect(0, 0, 246, 266))
        self.MainBG.setStyleSheet(
            f'background-color: rgb{AnicordColors.MainBGColor};\n'
            'border-radius: 10')
        self.MainBG.setObjectName('MainBG')
        self.WindowTitle = PYQTHoverLabel(self.CentralWidget)
        self.WindowTitle.setGeometry(QtCore.QRect(11, 6, 131, 21))
        self.WindowTitle.setStyleSheet('font: 87 10pt \'Segoe UI Black\';\n'
                                       f'color: rgb{AnicordColors.MainColor};')
        self.WindowTitle.setAlignment(QtCore.Qt.AlignLeft)
        self.WindowTitle.setObjectName('WindowTitle')
        self.DelayHint = PYQTHoverLabel(self.CentralWidget)
        self.DelayHint.setGeometry(QtCore.QRect(20, 180, 141, 26))
        self.DelayHint.setStyleSheet(
            'font: 63 10pt \'Segoe UI Variable Small Semibol\';\n'
            f'color: rgb{AnicordColors.MainColor};')
        self.DelayHint.setAlignment(QtCore.Qt.AlignLeading
                                    | QtCore.Qt.AlignLeft
                                    | QtCore.Qt.AlignVCenter)
        self.DelayHint.setObjectName('DelayHint')
        self.StatusChangeDelay = QtWidgets.QDoubleSpinBox(self.CentralWidget)
        self.StatusChangeDelay.setGeometry(QtCore.QRect(165, 180, 61, 26))
        self.StatusChangeDelay.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons)
        self.StatusChangeDelay.setMinimum(0.2)
        self.StatusChangeDelay.setMaximum(999.9)
        self.StatusChangeDelay.setSingleStep(0.2)
        self.StatusChangeDelay.setDecimals(1)
        self.StatusChangeDelay.setValue(2)
        self.StatusChangeDelay.setObjectName('StatusChangeDelay')
        self.IconTimer = PYQTHoverLabel(self.CentralWidget)
        self.IconTimer.setGeometry(QtCore.QRect(205, 185, 16, 16))
        self.IconTimer.setPixmap(
            QtGui.QPixmap(AppDataRoaming + sep + 'Timer.png'))
        self.IconTimer.setScaledContents(True)
        self.IconTimer.setToolTip(
            '???????????????? ?????????? ?????????????????????? ???????????????? (?? ????????????????)')
        self.IconTimer.setObjectName('IconTimer')
        self.Runner = PYQTHoverButton(self.CentralWidget)
        self.Runner.setGeometry(QtCore.QRect(145, 231, 90, 23))
        self.Runner.setStyleSheet(
            'QPushButton {\n'
            f'    color: rgb{AnicordColors.FormBGColor};\n'
            f'    background-color: rgb{AnicordColors.MainColor};\n'
            '    border-radius: 5;\n'
            '    padding-left: 1;\n'
            '    padding-right: 1;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '}')
        ObjectIcon = QtGui.QIcon()
        ObjectIcon.addPixmap(QtGui.QPixmap(AppDataRoaming + sep + 'Run.png'),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Runner.setIcon(ObjectIcon)
        self.Runner.setIconSize(QtCore.QSize(13, 13))
        self.Runner.setObjectName('Runner')
        self.SetStyle = PYQTHoverButton(self.CentralWidget)
        self.SetStyle.setGeometry(QtCore.QRect(91, 231, 40, 23))
        self.SetStyle.setStyleSheet(
            'QPushButton {\n'
            f'    color: rgb{AnicordColors.MainColor};\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            '    border-radius: 5;\n'
            '    padding-left: 1;\n'
            '    padding-right: 1;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '}')
        self.SetStyle.setObjectName('SetStyle')
        self.PanelClose = PYQTHoverButton(self.CentralWidget)
        self.PanelClose.setGeometry(QtCore.QRect(215, 5, 26, 21))
        self.PanelClose.setStyleSheet(
            'QPushButton {\n'
            f'    color: rgb{AnicordColors.FormBGColor};\n'
            f'    background-color: rgb{AnicordColors.MainColor};\n'
            '    border-radius: 5;\n'
            '    padding-left: 1;\n'
            '    padding-right: 1;\n'
            '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
            '}')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(AppDataRoaming + sep + 'Close.png'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PanelClose.setIcon(icon)
        self.PanelClose.setIconSize(QtCore.QSize(13, 13))
        self.PanelClose.setObjectName('PanelClose')
        self.PanelPin = PYQTHoverButton(self.CentralWidget)
        self.PanelPin.setGeometry(QtCore.QRect(185, 5, 26, 21))
        self.PanelPin.setStyleSheet(
            'QPushButton {\n'
            f'    color: rgb{AnicordColors.FormBGColor};\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            '    border-radius: 5;\n'
            '    padding-left: 1;\n'
            '    padding-right: 1;\n'
            '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
            '}')
        ObjectIcon = QtGui.QIcon()
        ObjectIcon.addPixmap(QtGui.QPixmap(AppDataRoaming + sep + 'Pin.png'),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PanelPin.setIcon(ObjectIcon)
        self.PanelPin.setIconSize(QtCore.QSize(16, 16))
        self.PanelPin.setObjectName('PanelPin')
        self.PanelHide = PYQTHoverButton(self.CentralWidget)
        self.PanelHide.setGeometry(QtCore.QRect(155, 5, 26, 21))
        self.PanelHide.setStyleSheet(
            'QPushButton {\n'
            f'    color: rgb{AnicordColors.FormBGColor};\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            '    border-radius: 5;\n'
            '    padding-left: 1;\n'
            '    padding-right: 1;\n'
            '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
            '}')
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(AppDataRoaming + sep + 'Minus.png'),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PanelHide.setIcon(icon2)
        self.PanelHide.setIconSize(QtCore.QSize(16, 16))
        self.PanelHide.setObjectName('PanelHide')
        self.MainBG.raise_()
        self.FormBG.raise_()
        self.Authorization.raise_()
        self.IconAuthorization.raise_()
        self.Frames.raise_()
        self.IconFrames.raise_()
        self.WindowTitle.raise_()
        self.DelayHint.raise_()
        self.StatusChangeDelay.raise_()
        self.IconTimer.raise_()
        self.Runner.raise_()
        self.SetStyle.raise_()
        self.PanelClose.raise_()
        self.PanelPin.raise_()
        self.PanelHide.raise_()
        Application.setCentralWidget(self.CentralWidget)

        QtCore.QMetaObject.connectSlotsByName(Application)

        Application.setWindowTitle('Anicord 2.0 - Neon Version')
        self.Authorization.setPlaceholderText('?????????? ?????????????? ????????????')
        self.Frames.setPlaceholderText('??????????????')
        self.WindowTitle.setText('Anicord 2.0')
        self.DelayHint.setText('????????????????:')
        self.Runner.setText('????????')
        self.SetStyle.setText('??????????')

        self.WindowTitle.HoverSignal.connect(self.PanelBackgroundHover)
        self.MainBG.HoverSignal.connect(self.PanelBackgroundHover)

        self.PanelHide.HoverSignal.connect(self.PanelHideHover)
        self.PanelClose.HoverSignal.connect(self.PanelCloseHover)
        self.PanelPin.HoverSignal.connect(self.PanelPinHover)
        self.Runner.HoverSignal.connect(self.RunnerButtonHover)

        self.Runner.clicked.connect(lambda: Thread(target=self.Run).start())

        self.PanelClose.clicked.connect(self.close)
        self.PanelHide.clicked.connect(self.showMinimized)
        self.PanelPin.clicked.connect(self.PinWindow)
        self.SetStyle.clicked.connect(self.SetAppStyle)

        self.RunnerButtonChangeSignal.connect(self.RunnerButtonChangeEvent)

    def LoadStyle(self):
        Reply = WindowsDLLs.WindowsUser32DLL.MessageBoxW(
            0, '?????????????? ?????????? ?? ?????????????????? ?????? ???????????? ???????????', '?????????? ??????????', 4)

        if Reply == 6:
            DefaultLocation = split(__file__)[0] + sep + 'Examples'
        else:
            DefaultLocation = expanduser('~')

        QFileDialog = QtWidgets.QFileDialog

        file = QFileDialog.getOpenFileName(self, '???????????????? ??????????',
                                           DefaultLocation,
                                           'JSON style (*.json)')[0]

        if not file:
            return

        try:
            fileContent = json.loads(open(file, 'r').read())
        except Exception as e:
            WindowsDLLs.WindowsUser32DLL.MessageBoxW(0, f'{type(e)} -> {e}',
                                       '???????????? JSON ??????????????????????????', 0x10)
            return

        keys = fileContent.keys()

        components = [
            'MainColor', 'HoverOnMainColor', 'FormBGColor', 'MainBGColor',
            'OnTranspHoverColor'
        ]

        for key in keys:
            if key not in components:
                WindowsDLLs.WindowsUser32DLL.MessageBoxW(0, f'???????? {key} ???? ????????????.',
                                           '????????????', 0x10)
                return

        build = 'class AnicordColors:\n' +\
                f'    MainColor = {fileContent["MainColor"]}\n' +\
                f'    HoverOnMainColor = {fileContent["HoverOnMainColor"]}\n' +\
                f'    MainBGColor = {fileContent["MainBGColor"]}\n' +\
                f'    FormBGColor = {fileContent["FormBGColor"]}\n' +\
                f'    OnTranspHoverColor = {fileContent["OnTranspHoverColor"]}\n'

        open(AppDataRoaming + sep + 'style.py', 'w').write(build)

        WindowsDLLs.WindowsUser32DLL.MessageBoxW(
            0, '?????????????????? ?????????????????? ????????????????, ?????????? ?????????????????? ??????????.',
            '?????????? ?????????????? ????????????????', 64)
        _exit(0)

    def SetAppStyle(self):
        if isfile(AppDataRoaming + sep + 'style.py'):
            Reply = WindowsDLLs.WindowsUser32DLL.MessageBoxW(0, '?????????????? ???????????',
                                               '?????????? ??????????', 4)
            if Reply == 6:
                remove(AppDataRoaming + sep + 'style.py')
                _exit(0)

            else:
                self.LoadStyle()
        else:
            self.LoadStyle()

    def Run(self):
        if self.IsWorking:
            self.IsWorking = False

            self.RunnerButtonChangeSignal.emit({
                'text':
                '????????',
                'style':
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.MainColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 87 8pt \'Segoe UI Black\';\n'
                '}',
                'icon':
                AppDataRoaming + sep + 'Run.png'
            })

            return

        self.RunnerButtonChangeSignal.emit({
            'text':
            '????????',
            'style':
            'QPushButton {\n'
            f'    color: rgb{AnicordColors.FormBGColor};\n'
            f'    background-color: rgb{AnicordColors.MainColor};\n'
            '    border-radius: 5;\n'
            '    padding-left: 1;\n'
            '    padding-right: 1;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '}',
            'icon':
            AppDataRoaming + sep + 'Run.png'
        })

        self.IsStarting = True

        self.RunnerButtonChangeSignal.emit({
            'text':
            '????????????????',
            'style':
            'QPushButton {\n'
            f'    color: rgb{AnicordColors.MainColor};\n'
            f'    background-color: rgb{AnicordColors.MainBGColor};\n'
            '    border-radius: 5;\n'
            '    padding-left: 1;\n'
            '    padding-right: 1;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '}',
            'icon':
            AppDataRoaming + sep + 'Starting.png'
        })

        Token = self.Authorization.text()
        Delay = self.StatusChangeDelay.value()
        Statuses = self.Frames.toPlainText()

        if Token == '':
            self.RunnerButtonChangeSignal.emit({
                'text':
                '????????',
                'style':
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.MainColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 87 8pt \'Segoe UI Black\';\n'
                '}',
                'icon':
                AppDataRoaming + sep + 'Run.png'
            })

            WindowsDLLs.WindowsUser32DLL.MessageBoxW(0, '?????????? ????????.', '?????????????????? ????????????',
                                       0x10)

            return

        if Statuses == '':
            self.RunnerButtonChangeSignal.emit({
                'text':
                '????????',
                'style':
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.MainColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 87 8pt \'Segoe UI Black\';\n'
                '}',
                'icon':
                AppDataRoaming + sep + 'Run.png'
            })

            WindowsDLLs.WindowsUser32DLL.MessageBoxW(0, '?????????????? ??????????????.',
                                       '?????????????????? ????????????', 0x10)

            return

        if '\n' not in Statuses:
            self.RunnerButtonChangeSignal.emit({
                'text':
                '????????',
                'style':
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.MainColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 87 8pt \'Segoe UI Black\';\n'
                '}',
                'icon':
                AppDataRoaming + sep + 'Run.png'
            })

            WindowsDLLs.WindowsUser32DLL.MessageBoxW(
                0, '?????????????? ?????????????? 2 ??????????????, ???????????????? ???? ?????????? ??????????????.',
                '?????????????????? ????????????', 0x10)

            return

        if HasNoVoidLnes(Statuses) != True:
            self.RunnerButtonChangeSignal.emit({
                'text':
                '????????',
                'style':
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.MainColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 87 8pt \'Segoe UI Black\';\n'
                '}',
                'icon':
                AppDataRoaming + sep + 'Run.png'
            })

            WindowsDLLs.WindowsUser32DLL.MessageBoxW(
                0, f'???????????? ?????????? ???? ???????????? {HasNoVoidLnes(Statuses)}.',
                '?????????????????? ????????????', 0x10)

            return

        TokenIsValid = CheckToken(Token)

        if not TokenIsValid:
            self.RunnerButtonChangeSignal.emit({
                'text':
                '????????',
                'style':
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.MainColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 87 8pt \'Segoe UI Black\';\n'
                '}',
                'icon':
                AppDataRoaming + sep + 'Run.png'
            })

            WindowsDLLs.WindowsUser32DLL.MessageBoxW(0, '?????????? ??????????????.', '?????????????????? ????????????',
                                       0x10)

            return

        self.IsStarting = False
        self.IsWorking = True

        self.RunnerButtonChangeSignal.emit({
            'text':
            '????????',
            'style':
            'QPushButton {\n'
            f'    color: rgb{AnicordColors.FormBGColor};\n'
            f'    background-color: rgb{AnicordColors.MainColor};\n'
            '    border-radius: 5;\n'
            '    padding-left: 1;\n'
            '    padding-right: 1;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '}',
            'icon':
            AppDataRoaming + sep + 'Stop.png'
        })

        Statuses = Statuses.split('\n')

        while self.IsWorking:
            for Status in Statuses:
                if not self.IsWorking:
                    return
                StatusIcon = None
                StatusText = None
                if Status.lower() in ['online', 'idle', 'dnd', 'invisible']:
                    StatusIcon = Status.lower()
                else:
                    if ';;' in Status:
                        Status = Status.split(';;', 1)
                        if Status[0].lower() in [
                                'online', 'idle', 'dnd', 'invisible'
                        ]:
                            StatusIcon = Status[0].lower()
                            StatusText = Status[1]
                        else:
                            StatusText = Status[0] + ';;' + Status[1]
                    else:
                        StatusText = Status

                Thread(target=lambda: SetPresence(Token, StatusText, StatusIcon
                                                  )).start()
                sleep(Delay)

    def RunnerButtonChangeEvent(self, data):
        self.Runner.setStyleSheet(data['style'])
        self.Runner.setText(data['text'])
        ObjectIcon = QtGui.QIcon()
        ObjectIcon.addPixmap(QtGui.QPixmap(data['icon']), QtGui.QIcon.Normal,
                             QtGui.QIcon.Off)
        self.Runner.setIcon(ObjectIcon)

    def RunnerButtonHover(self, event):
        if not self.IsStarting:
            if event == 'enterEvent':
                self.Runner.setStyleSheet(
                    'QPushButton {\n'
                    f'    color: rgb{AnicordColors.FormBGColor};\n'
                    f'    background-color: rgb{AnicordColors.HoverOnMainColor};\n'
                    '    border-radius: 5;\n'
                    '    padding-left: 1;\n'
                    '    padding-right: 1;\n'
                    '    font: 87 8pt \'Segoe UI Black\';\n'
                    '}')
            else:
                self.Runner.setStyleSheet(
                    'QPushButton {\n'
                    f'    color: rgb{AnicordColors.FormBGColor};\n'
                    f'    background-color: rgb{AnicordColors.MainColor};\n'
                    '    border-radius: 5;\n'
                    '    padding-left: 1;\n'
                    '    padding-right: 1;\n'
                    '    font: 87 8pt \'Segoe UI Black\';\n'
                    '}')

    def PanelPinHover(self, event):
        if self.IsPinned:
            if event == 'enterEvent':
                self.PanelPin.setStyleSheet(
                    'QPushButton {\n'
                    f'    color: rgb{AnicordColors.FormBGColor};\n'
                    f'    background-color: rgb{AnicordColors.HoverOnMainColor};\n'
                    '    border-radius: 5;\n'
                    '    padding-left: 1;\n'
                    '    padding-right: 1;\n'
                    '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
                    '}')
            else:
                self.PanelPin.setStyleSheet(
                    'QPushButton {\n'
                    f'    color: rgb{AnicordColors.FormBGColor};\n'
                    f'    background-color: rgb{AnicordColors.MainColor};\n'
                    '    border-radius: 5;\n'
                    '    padding-left: 1;\n'
                    '    padding-right: 1;\n'
                    '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
                    '}')
        else:
            if event == 'enterEvent':
                self.PanelPin.setStyleSheet(
                    'QPushButton {\n'
                    f'    color: rgb{AnicordColors.FormBGColor};\n'
                    f'    background-color: rgb{AnicordColors.OnTranspHoverColor};\n'
                    '    border-radius: 5;\n'
                    '    padding-left: 1;\n'
                    '    padding-right: 1;\n'
                    '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
                    '}')
            else:
                self.PanelPin.setStyleSheet(
                    'QPushButton {\n'
                    f'    color: rgb{AnicordColors.FormBGColor};\n'
                    f'    background-color: rgb{AnicordColors.MainBGColor};\n'
                    '    border-radius: 5;\n'
                    '    padding-left: 1;\n'
                    '    padding-right: 1;\n'
                    '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
                    '}')

    def PanelCloseHover(self, event):
        if event == 'enterEvent':
            self.PanelClose.setStyleSheet(
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.HoverOnMainColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
                '}')
        else:
            self.PanelClose.setStyleSheet(
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.MainColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
                '}')

    def PanelHideHover(self, event):
        if event == 'enterEvent':
            self.PanelHide.setStyleSheet(
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.OnTranspHoverColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
                '}')
        else:
            self.PanelHide.setStyleSheet(
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.MainBGColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
                '}')

    def PinWindow(self):
        self.IsPinned = not self.IsPinned

        if not self.IsPinned:
            self.PanelPin.setStyleSheet(
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.MainBGColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
                '}')
            ObjectIcon = QtGui.QIcon()
            ObjectIcon.addPixmap(
                QtGui.QPixmap(AppDataRoaming + sep + 'Pin.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.PanelPin.setIcon(ObjectIcon)
        else:
            self.PanelPin.setStyleSheet(
                'QPushButton {\n'
                f'    color: rgb{AnicordColors.FormBGColor};\n'
                f'    background-color: rgb{AnicordColors.MainColor};\n'
                '    border-radius: 5;\n'
                '    padding-left: 1;\n'
                '    padding-right: 1;\n'
                '    font: 63 8pt \'Segoe UI Variable Small Semibol\';\n'
                '}')
            ObjectIcon = QtGui.QIcon()
            ObjectIcon.addPixmap(
                QtGui.QPixmap(AppDataRoaming + sep + 'PinDark.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.PanelPin.setIcon(ObjectIcon)

        if self.IsPinned:
            self.setWindowFlags(self.windowFlags()
                                | QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags()
                                & ~QtCore.Qt.WindowStaysOnTopHint)
            self.show()

    def PanelBackgroundHover(self, event):
        if event == 'enterEvent':
            ApplicationState.AllowMainWindowMove = True
        else:
            ApplicationState.AllowMainWindowMove = False


class ApplicationWindow(Ui_Application):

    def __init__(self):
        super().__init__()
        self.InitWindow(self)

    def closeEvent(self, *args):
        _exit(0)

    def mousePressEvent(self, event):
        if ApplicationState.AllowMainWindowMove:
            try:
                if event.button() == QtCore.Qt.LeftButton:
                    self.old_pos = event.pos()
            except:
                pass

    def mouseReleaseEvent(self, event):
        if ApplicationState.AllowMainWindowMove:
            try:
                if event.button() == QtCore.Qt.LeftButton:
                    self.old_pos = None
            except:
                pass

    def mouseMoveEvent(self, event):
        if ApplicationState.AllowMainWindowMove:
            try:
                if not self.old_pos:
                    return
                delta = event.pos() - self.old_pos
                self.move(self.pos() + delta)
            except:
                pass


if __name__ == '__main__':
    Application = QtWidgets.QApplication(argv)
    Window = ApplicationWindow()
    Window.show()
    _exit(Application.exec_())
else:
    pass
