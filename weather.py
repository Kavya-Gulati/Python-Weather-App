#Python weather app
import sys
from PySide6.QtWidgets import QLabel,QApplication,QWidget,QVBoxLayout,QLineEdit,QPushButton
from PySide6.QtCore import Qt
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel('Enter City Name:',self)
        self.get_weather_button=QPushButton('GET WEATHER',self)
        self.city_input=QLineEdit(self)
        self.temp_label=QLabel()
        self.emoji_label=QLabel()
        self.description_label=QLabel()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WEATHER APP")
        vbox=QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        
        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.temp_label.setObjectName('temp_label')
        self.description_label.setObjectName('description_label')
        self.emoji_label.setObjectName('emoji_label')
        self.get_weather_button.setObjectName('get_weather_button')

        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family:calibri;
                           }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
                           }
            QLineEdit#city_input{
                font-size:40px;
                min-height:60px;                                      
                           }
            QPushButton#get_weather_button{
                font-size:25px;
                font-weight:bold;              
                           }
            QLabel#temp_label{
                font-size:70px;
                           }
            QLabel#emoji_label{
                font-size:100px;
                font-family: Segoe UI emoji;          
                           }
            QLabel#description_label{
                font-size:50px;
                           }
                           """)
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api = 'a0f7e8a99699ad6b1a0f30914afcee43'
        city = self.city_input.text()
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}'

        try:
            response = requests.get(url)
            response.raise_for_status()             
            data=response.json()
            if data['cod']==200:
                self.display_weather(data)
            
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error('Bad Request\nPlease check your input.')
                case 401:
                    self.display_error('Unauthorized\nInvalid API Key.')
                case 403:
                    self.display_error('Forbidden\nAccess Denied.')
                case 404:
                    self.display_error('Not Found\nCity Not Found.')
                case 500:
                    self.display_error('Internal Server Error\nPlease Try Again Later.')
                case 502:
                    self.display_error('Bad Gateway\nInvalid Response From the Server.')
                case 503:
                    self.display_error('Service Unavailable\nServer is down.')
                case 504:
                    self.display_error('Gateway Timeout\nNo response from the server.')   
                case _:
                    self.display_error(f'HTTP error occured\n{http_error}')  

        except requests.exceptions.ConnectionError:
            self.display_error('Connection Error\nPlease Check your Internet Connection.')

        except requests.exceptions.Timeout:
            self.display_error('Timeout Error\nThe Request timed out.')

        except requests.exceptions.TooManyRedirects:
            self.display_error('Too Many Redirects\nPlease Check the URL.')

        except requests.exceptions.RequestException as req_error:
            self.display_error(f'Request Error\n{req_error}')
        

    def display_error(self,message):
        self.temp_label.setStyleSheet('font-size: 30px;')
        self.temp_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        self.temp_label.setStyleSheet('font-size: 75px;')
        temp_k=data['main']['temp']
        temp_c = temp_k - 273.15
        weather_id = data['weather'][0]['id']
        weather_desc = data['weather'][0]['description']
        
        self.description_label.setText(weather_desc)
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.temp_label.setText(f'{temp_c:.0f}°C')  
        
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200<= weather_id <=232:
            return '⛈️'
        elif 300<= weather_id <= 321:
            return '🌦️'
        elif 500<= weather_id <= 531:
            return '🌧️'
        elif 600<= weather_id <= 622:
            return '🌨️'
        elif 701<= weather_id <= 741:
            return '🌁'
        elif weather_id == 762:
            return '🌋'
        elif weather_id == 771:
            return '💨'
        elif weather_id == 781:
            return '🌪️'
        elif weather_id == 800:
            return '🌇'
        elif 801<= weather_id <= 804:
            return '☁️'

if __name__=='__main__':
    app=QApplication(sys.argv)
    weather=WeatherApp()
    weather.show()
    sys.exit(app.exec())
