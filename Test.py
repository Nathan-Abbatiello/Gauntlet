import sys, time, serial, re
# from upspackv2 import *
from PyQt5.QtWidgets import QApplication, QScrollArea, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QSlider, QHBoxLayout, QGroupBox 
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer, QTime, QDateTime, Qt, QSize 
import subprocess
# device info
deviceInfo = {
    "Name": "testDevice",
    "Version": "0.1",
    "Started": "01/03/2022",
    "GUI": "PY-QT-5"
}

brightness = "100"

# global widget definitions
widgets={
    "button": [],
    "label": [],
    "image": [],
    "slider": []
}

app = QApplication(sys.argv)
app.setStyleSheet("QPushButton{"+
"border: 4px solid '#007777';"+ 
    "border-radius: 35px;"+
    "font-size: 30px;"+
    "background-color: linear-gradient(to bottom, rgba(0,0,0,0) 70%, rgba(90, 180, 180, 0.5));"+
    "color:white;"+
    "padding: 15px 0;"+
    "margin: 5px;}")
window = QWidget()
window.setWindowTitle("TestApp")
window.setStyleSheet("background: #222222;")
grid = QGridLayout()
# page layout vertical
pageLayout = QVBoxLayout(window)
# horizontal layout for top menu
topBarCon = QHBoxLayout()
# mainpage content container
content = QWidget()
contentLayout = QGridLayout()

pageLayout.addLayout(topBarCon)
pageLayout.addLayout(contentLayout)
content.setMinimumHeight(430)
content.setMaximumHeight(430)


# ################ battery functions
# test = UPS2("/dev/ttyS0")
# cap_var= "empty"
# vin_var =  "empty"
# def reflash_data():
#     version,vin,batcap,vout = test.decode_uart()
# #    loc_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # cur_time = time.time()
    # cur_time = cur_time - load_time
#    print(cur_time)
    # time_var.set("Running: "+str(int(cur_time)) + "s")    
#     batcap_int = int(batcap)
# #    print(type(batcap_int))
#     if vin == "NG":
#         vin_var = "Power NOT connected!"
#     else:
#         vin_var = "Power connected!"
    # if batcap_int< 30:
        # if batcap_int == 1:
            # cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            # stop_time = "\nHalt time :"+cur_time
            # with open("log.txt","a+") as f:
                # f.write(stop_time)
            # os.system("sudo shutdown -t now")
            # sys.exit()            
    # cap_var = "Battery Capacity: "+str(batcap)+"%"
    # vout_var = "Output Voltage: "+vout+" mV"
    # return cap_var


################# operations
def minimise():
    window.showMinimized()

def shutdown():
    subprocess.run("sudo shutdown now", shell = True)

def reboot():
    subprocess.run("sudo reboot", shell = True)

def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget][-1].hide()
            widgets[widget].pop()

def hide_widget(widget):
    widget.hide()

def current_time():
    time = QDateTime.currentDateTime()
    return time.toString("yyyy-MM-dd hh:mm:ss")

def set_brightness(brightness): 
    subprocess.run([ "echo "+str(brightness)+" > /sys/class/backlight/rpi_backlight/brightness"], shell = True)


################### reuseable UI Elements
# button
def button(text, clickFunc=False, parent=contentLayout):
    button = QPushButton(text)
    widgets["button"].append(button)
    # applies onclick function to btn if one has been given
    if clickFunc != False:    
        button.clicked.connect(clickFunc)
    if parent != False:
        parent.addWidget(widgets["button"][-1])

# label
def label(text="", parent=contentLayout, fontSize="20"): 
    label = QLabel(text)
    label.setStyleSheet("font-size: "+fontSize+"px;"+
    "color: white;"+"padding-top: 5px;")
    label.setAlignment(Qt.AlignCenter)
    widgets["label"].append(label)
    if parent != False:
        parent.addWidget(widgets["label"][-1])

def page_title(text="", rowSpan=0, columnSpan=0): 
    label = QLabel(text)
    label.setStyleSheet("font-size: 25px;"+
    "color: white;"+"padding: 5px;"+ "width: 100%;"
    +"background: '#008888';")
    label.setAlignment(Qt.AlignTop)
    label.setAlignment(Qt.AlignHCenter)
    widgets["label"].append(label)
    grid.addWidget(widgets["label"][-1], 0, 0, rowSpan, columnSpan)

def slider(min=0, max=250, int=10):
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min)
    slider.setMaximum(max)
    slider.setTickInterval(int)
    slider.setStyleSheet("QSlider::handle:horizontal {background-color: '#009999'; height: 80px; width: 80px; margin: -2px;}"+
    "QSlider::groove:horizontal {border: 1px solid; height: 40px;}"+
    "QSlider {height: 60px;}")
    slider.valueChanged.connect(set_brightness)
    widgets["slider"].append(slider)
    contentLayout.addWidget(widgets["slider"][-1]) 

# display image
def image(filePath="", row=0, column=0):
    if filePath != "":
        pxMap = QPixmap(filePath)
        lbl = QLabel()
        lbl.setAlignment(Qt.AlignRight)
        lbl.setStyleSheet("margin: 0;")
        lbl.resize(300, 450)
        lbl.setPixmap(pxMap.scaled(lbl.size(), QtCore.Qt.IgnoreAspectRatio))
        widgets["image"].append(lbl)
        grid.addWidget(widgets["image"][-1], row, column)

# test button
def testButton(text="", clickFunc=False, width=50, icon=""):
    if icon != "":
        button = QPushButton(QIcon(icon), text)
        button.setIconSize(QSize(45,45))
    else:
        button = QPushButton(text)
    button.setStyleSheet("QPushButton {border: none;"+
    "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.5 rgba(0,0,0,0), stop: 1 rgba(0,200,200,0.3));"+
    "border-radius: 15px;"+
    "border-bottom: 4px solid '#007777';" 
    "font-size: 30px;"+
    "color: white;"+
    "margin: 0px;}"+
    "QPushButton:pressed{"+
    "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.5 rgba(0,0,0,0), stop: 1 rgba(0,200,200,0.7));"+
    "border-bottom: 4px solid '#00bbbb';}") 
    button.setMaximumWidth(width)
    button.setMaximumHeight(80)
    widgets["button"].append(button)
    # applies onclick function to btn if one has been given
    if clickFunc != False:    
        button.clicked.connect(clickFunc)
    topBarCon.addWidget(widgets["button"][-1])

def pop_up(msg="confirm", accFunc=False, accept="yes", decline="no"):
    popUp = QWidget(window)
    popUp.setObjectName("popUp")
    popUp.setStyleSheet("QWidget#popUp {border: 3px solid #007777;}")
    popUp.setGeometry(0, 100, 800, 380)
    grd = QGridLayout(popUp)
    lbl = label(msg, False, "30")
    btnAccept = QPushButton(accept)
    btnDecline = QPushButton(decline)
    grd.addWidget(widgets["label"][-1],0,0,1,0)
    grd.addWidget(btnAccept,1,0)
    grd.addWidget(btnDecline,1,1)
    if accFunc != False:    
        btnAccept.clicked.connect(accFunc)
    btnDecline.clicked.connect(lambda: hide_widget(popUp))
    btnAccept.clicked.connect(lambda: hide_widget(popUp))
    popUp.show()

############# display functions
def start_up():
    clear_widgets()
    msgStart = label("Device Initialised", 0,0,"30")
    i = 1
    # display device info
    for info in deviceInfo:
        info = label(info+": "+deviceInfo[info],i, 0, "20")
        i+= 1

def top_bar():
    clear_widgets()
    # img1 = image("/home/pi/Documents/RaspberryPi-Code/Gauntlet/testImage.jpeg",0,1)
    btn1 = testButton("Suit", suit,185)
    btn2 = testButton("Devices",devices,185)
    btn3 = testButton("Modes",modes, 185)
    btn4 = testButton("btn",False, 185)
    btn5 = testButton("",settings,60, "/home/pi/Documents/RaspberryPi-Code/Gauntlet/Images/settings.png") 

def suit():
    clear_widgets()
    top_bar()
    title = page_title("Suit")
    text = label("suit menu changed...")
    text = label(current_time())
    text = label(".")
    # text = label(reflash_data())

def devices():
    top_bar()

def modes():
    top_bar()

def settings():
    clear_widgets()
    top_bar()
    text = label("Brightness")
    sldr = slider(0, 250, 10)
    btnMin = button("Desktop", lambda: pop_up("Exit to Desktop", minimise))
    btnShtDwn = button("Shutdown", lambda: pop_up("Shutdown", shutdown))
    btnRbt = button("Reboot", lambda: pop_up("Reboot", reboot))
    text2 = label("test")
    text3 = label("test")
    text4 = label("test")





##################### run sequence
window.setLayout(pageLayout)
window.showFullScreen()
# reflash_data()
# version,vin,batcap,vout = test.decode_uart()

# start_up()
timer = QTimer()
timer.start(2000)
timer.setSingleShot(True)
timer.timeout.connect(suit)

# battery data
# timer2 = QTimer()
# timer2.start(200)
# timer2.timeout.connect(reflash_data)

sys.exit(app.exec())