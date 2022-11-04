
import flask
import pickle
import os

# Use pickle to load in the pre-trained model.
with open(f'../webapp/model/crop_data.pkl', 'rb') as f:
    model = pickle.load(f)
app = flask.Flask(__name__, template_folder='templates')
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))
    if flask.request.method == 'POST':
        average_rain_fall_mm_per_year = flask.request.form['average_rain_fall_mm_per_year']
        pesticides_tonnes = flask.request.form['pesticides_tonnes']
        avg_temp = flask.request.form['avg_temp']
        input_variables = pd.DataFrame([[average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp]],
                                       columns=['average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp'],
                                       dtype=float)
        prediction = model.predict(input_variables)[0]
        return flask.render_template('main.html',
                                     original_input={'Average_rain_fall_mm_per_year':average_rain_fall_mm_per_year,
                                                     'Pesticides_tonnes':pesticides_tonnes,
                                                     'Avg_temp':avg_temp},
                                     result=prediction,
                                     )
    if __name__=="__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=False,host='0.0.0.0', port=port)
