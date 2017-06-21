"""
This is a mini API demo, all data are taken from the merged.csv file and filtered with pandas.
To launch it, install Flask (pip install flask), go into the folder where the app.py file is,
run 'python app.py' and go to http://localhos:5000
"""
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

#loading data
df = pd.read_csv('./merged.csv')
# removing the index column
df = df.drop('Index',axis=1)

# Create a regions endpoint to see available regions and their insee code
@app.route('/api/regions', methods=['GET'])
def get_regions():
    data = df[['Région','insee_region']].drop_duplicates()
    return data.to_json(orient='records')

# Region endpoint to the the detail of a region. Needs an argument to get the searched region.
@app.route('/api/regions/<int:region_id>', methods=['GET'])
def get_region(region_id):
    data = df[df['insee_region'] == region_id]
    return data.to_json(orient='records')

#Check available years
@app.route('/api/years', methods=['GET'])
def get_years():
    data = df.groupby('Année').sum().reset_index()
    return data.to_json(orient='records')

#Check a particular year
@app.route('/api/years/<int:year_id>', methods=['GET'])
def get_year(year_id):
    data = df[df['Année'] == year_id]
    return data.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
