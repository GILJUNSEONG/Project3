from flask import Flask, render_template, request
import pickle
import pandas as pd
from myfunction import get_df

app = Flask(__name__)

model = None
with open('model/model.pkl', 'rb') as pickle_file:
    model = pickle.load(pickle_file)

_, df = get_df()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods = ['POST', 'GET'])  # machinelearning page
def predict():
    if request.method == 'POST':

        built_year = int(request.form['건축년도'])
        year = 2021
        dong = request.form['법정동']
        gu = int(request.form['지역코드'])
        pyeong = int(request.form['전용면적'])
        area = float(pyeong) * 3.3
        floor = int(request.form['층'])

        data = [[built_year, year, dong, gu, area, floor]]
        column_name = ['건축년도', '년', '법정동', '지역코드', '전용면적', '층']

        data = pd.DataFrame(data, columns=column_name)
        pred = model.predict(data)

        house_price = int(pred[0])*10000

        house_condition = (df['건축년도'] < built_year + 5) & (df['건축년도'] > built_year - 5) & (df['법정동'] == dong) & (df['지역코드'] == gu) & (df['전용면적'] < area + 20) & (df['전용면적'] > area - 20) & (df['층'] < floor + 5) & (df['층'] > floor - 5)

        house_selected = df[house_condition].sort_values(by=['년','월','일'], ascending=False)
        house_selected['거래금액(천 원)'] = (house_selected['거래금액'] * 10).apply(lambda x : "{:,}".format(x))
        house_selected['평 수'] = (house_selected['전용면적'] / 3.3).astype(int)
        house_selected['거래일자'] = house_selected['년'].astype(str) + '-' + house_selected['월'].astype(str) + '-' + house_selected['일'].astype(str)
        house_selected = house_selected[['건축년도', '법정동', '아파트', '평 수', '층', '거래일자', '거래금액(천 원)']].head(15).reset_index(drop=True)
    return render_template('predict.html', year = built_year, floor=floor, dong=dong, pyeong=pyeong, price=format(house_price,','), tables=[house_selected.to_html(classes='data', header='true')])

if __name__ == "__main__":
    app.run()