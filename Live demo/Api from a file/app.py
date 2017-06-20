import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

df = pd.read_csv('./merged.csv')
df = df.drop('Index',axis=1)

@app.route('/api/regions', methods=['GET'])
def get_regions():
    data = df[['Région','insee_region']].drop_duplicates()
    return data.to_json(orient='records')

@app.route('/api/regions/<int:region_id>', methods=['GET'])
def get_region(region_id):
    data = df[df['insee_region'] == region_id]
    return data.to_json(orient='records')

@app.route('/api/years', methods=['GET'])
def get_years():
    data = df.groupby('Année').sum().reset_index()
    return data.to_json(orient='records')

@app.route('/api/years/<int:year_id>', methods=['GET'])
def get_year(year_id):
    data = df[df['Année'] == year_id]
    return data.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
