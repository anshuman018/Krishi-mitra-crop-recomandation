import joblib
import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Load your model
model = joblib.load('crop_app')

# Function to fetch weather data excluding rainfall
def get_weather_data(city):
    api_key = '1bffeac4e19307fa76afbe3e1af64e11'
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(api_url)
        data = response.json()

        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        
        return temperature, humidity
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None, None

@app.route('/')
def home():
    return render_template('Home_1.html')

@app.route('/Predict')
def prediction():
    return render_template('Index.html')

@app.route('/form', methods=["POST"])
def brain():
    Nitrogen = float(request.form['Nitrogen'])
    Phosphorus = float(request.form['Phosphorus'])
    Potassium = float(request.form['Potassium'])
    Ph = float(request.form['ph'])

    # Get manual rainfall input from the form
    Rainfall = float(request.form['Rainfall'])
       
    # Get weather data (temperature, humidity) from the city
    city = request.form.get('city', 'London')  
    Temperature, Humidity = get_weather_data(city)

    if Temperature is None or Humidity is None:
        return "Error fetching weather data. Please try again."

    # Create the input values for prediction, including manual Rainfall
    values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]
    
    # Validate the inputs
    if 0 < Ph <= 14 and Temperature < 100 and Humidity > 0:
        arr = [values]
        acc = model.predict(arr)[0]  # Extracting the predicted crop from the array

        background_images = {
            "apple": "/static/style/apple.jpg",
            "wheat": "/static/style/wheat.jpeg",
            "corn": "/static/style/corn.jpg",
            "rice": "/static/style/rice.jpg",
            "grapes": "/static/style/grapes.jpg",
            "watermelon": "/static/style/watermelon.jpeg",
            "banana": "/static/style/banana.jpeg",
            "blackgram": "/static/style/black gram.jpeg",
            "chickpea": "/static/style/chickpea.jpeg",
            "coffee": "/static/style/coffee.jpeg",
            "cotton": "/static/style/cotton.jpeg",
            "jute": "/static/style/jute.jpg",
            "kidneybean": "/static/style/kidney bean.jpeg",
            "lentil": "/static/style/lentil.jpeg",
            "moongbean": "/static/style/moong bean.jpeg",
            "mothbean": "/static/style/moth bean.jpeg",
            "muskmelon": "/static/style/muskmelon.jpeg",
            "orange": "/static/style/orange.jpeg",
            "papaya": "/static/style/papaya.jpeg",
            "pigeonp": "/static/style/pigeonp.jpeg",
            "pomegranate": "/static/style/pomegranate.jpeg"
        }

        # Get the background image for the predicted crop or use a default
        background_image = background_images.get(acc, "/static/style/image.jpg")

        # Pass the predicted crop and background image to the template
        return render_template('prediction.html', prediction=acc, background_image=background_image)
    else:
        return "Sorry... Error in entered values in the form. Please check the values and fill it again."

if __name__ == '__main__':
    app.run()
