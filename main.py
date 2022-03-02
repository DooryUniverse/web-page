from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/corona')
def corona():
    
    corona_df = pd.read_csv('corona.csv')
    corona_df.columns=["인덱스", "등록일시","사망자", "확진자", "게시글 번호", "기준일", "기준시간", "수정일시", "누적 의심자", "누적확진률"]
    corona_df.sort_values("등록일시", inplace=True)
    corona_df["일일 확진자"]=(corona_df["확진자"] - corona_df["확진자"].shift()).fillna(0)
    corona_df["일일 사망자"]=corona_df["사망자"].diff().fillna(0)
    corona_df.drop(['인덱스', '기준일', '게시글 번호', '기준시간','수정일시'], axis=1, inplace = True)
    corona_df.reset_index(drop=True, inplace=True)
    return corona_df.to_html()

@app.route("/img")
def img():
    corona_df = pd.read_csv('corona.csv')
    corona_df.columns=["인덱스", "등록일시","사망자", "확진자", "게시글 번호", "기준일", "기준시간", "수정일시", "누적 의심자", "누적확진률"]
    corona_df.sort_values("등록일시", inplace=True)
    corona_df["일일 확진자"]=(corona_df["확진자"] - corona_df["확진자"].shift()).fillna(0)
    corona_df["일일 사망자"]=corona_df["사망자"].diff().fillna(0)
    corona_df.drop(['인덱스', '기준일', '게시글 번호', '기준시간','수정일시'], axis=1, inplace = True)
    corona_df.reset_index(drop=True, inplace=True)
    decide_cnt=corona_df["일일 확진자"].values.tolist()
    state_dt = corona_df["등록일시"].values.tolist()
    plt.plot(state_dt, decide_cnt)
    plt.xlabel("date")
    plt.ylabel("corona")
    plt.title("Corona data")
    
    img_1=BytesIO()
    plt.savefig(img_1, format="png", dpi=1000)
    img_1.seek(0)
   
    
    return send_file(img_1, mimetype='image/png')
app.run