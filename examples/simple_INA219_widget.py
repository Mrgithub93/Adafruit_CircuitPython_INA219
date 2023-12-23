#just a simple battery indicator widget i made for my 4s lipo to my robot using the INA219 module
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar, QDesktopWidget
from PyQt5.QtCore import QTimer, Qt
import board
import busio
from adafruit_ina219 import INA219
import adafruit_ina219
import pyttsx3


# Function to calculate percentage, change these values to whatever you have
def calculate_percentage(value):
    lower_bound = 13.8
    upper_bound = 16.8
    if value < lower_bound:
        return 0.0
    elif value > upper_bound:
        return 100.0
    else:
        return ((value - lower_bound) / (upper_bound - lower_bound)) * 100


# PyQt application window
class BatteryMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.label_voltage = QLabel("Voltage: ")
        self.batteryLevel = QProgressBar()
        self.batteryLevel.setMinimumHeight(30)

        self.layout.addWidget(self.label_voltage)
        self.layout.addWidget(self.batteryLevel)
        self.setLayout(self.layout)
        self.setWindowTitle('Robs POWAH')
        self.setGeometry(50, 50, 50, 50)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""
        QWidget{
            color: #b1b1b1;
            background-color: #323232;
        }
        QLabel{
            font-family:Operator Mono Bold;
            font:16px;
        } 
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
        }
#         QProgressBar::chunk {
#             background-color: #d7801a;
#             width: 20px;
#         }
        """)
        self.show()

        # INA219 setup
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ina219 = INA219(i2c)
        self.ina219.bus_adc_resolution = 0x3
        self.ina219.bus_voltage_range = 0x1

        # Update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_values)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)
        screen_width = QDesktopWidget().availableGeometry().width()
        window_width = self.frameGeometry().width()
        x_position = (screen_width - window_width) / 2
        self.move(int(x_position), 10)  # Adjust the vertical position (10) as needed

    def update_values(self):
        bus_voltage = self.ina219.bus_voltage
        percentage = calculate_percentage(bus_voltage)
        self.label_voltage.setText(f"Voltage: {bus_voltage:.1f}V")
        self.batteryLevel.setValue(int(percentage))

        if percentage < 90:
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background: blue;
            width: 2.15px;
            margin: 0.5px;
            }""")

        if percentage < 80:
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background: green;
            width: 2.15px;
            margin: 0.5px;
            }""")
        elif percentage < 50:
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background: orange;
            width: 4px;
            margin: 0.5px;
            }""")
        elif percentage < 25:
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background: red;
            width: 2.15px;
            margin: 0.5px;
            }""")
        elif percentage > 25:
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background: red;
            width: 2.15px;
            margin: 0.5px;
            }""")
            speak("battery low")
        elif percentage == 1:
            self.batteryLevel.setStyleSheet("""QProgressBar::chunk{
            background: red;
            width: 2.15px;
            margin: 0.5px;
            }""")
            speak("voltage critical")


def speak(text):
    engine = pyttsx3.init()  # Initialize the pyttsx3 engine
    engine.say(text)  # Pass the text you want to speak
    engine.runAndWait()  # Process and speak the text


# Main function to run the application
def displaymain():
    app = QApplication(sys.argv)
    ex = BatteryMonitor()
    sys.exit(app.exec_())


if __name__ == '__main__':
    displaymain()

