import requests
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


class City(db.Model):
    ''' Database Class

    Notes:
        Class where the name of the
        objects inside the Database
        is called.
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    ''' Requests Used

    Notes:
        The requests used are GET and POST, where
        the page returns the database elements with
        GET and Creates a New element inserted in the Input.
    '''
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_ = City(name=new_city)
            db.session.add(new_city_)
            db.session.commit()

    cities = City.query.all()

    try:
        ''' Handling Exceptions

        Notes:
            Exception Handling where an invalid
            name is requested by the user.
        '''
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=f7d3986218f3c9e12e6502dfa599d080'  # noqa: E501
        city = 'Maracanaú'

        weather_data = []

        for city in cities:
            ''' Accessing the Database

            Notes:
                Here the database is accessed by listing
                the objects and making the get request on
                the url listed.
            '''

            response = requests.get(url.format(city.name)).json()

            weather = {
                'name': city.name,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
            }

            weather_data.append(weather)
        return render_template(['weather.html'], weather_data=weather_data)
    except IndexError:
        message = 'City Don\'t Found'
        return jsonify({'status': 'Error', 'message': message})
    except Exception:
        message = 'Unknown Error'
        return jsonify({'status': 'Error', 'message': message})


if __name__ == '__main__':
    app.run(debug=True)
