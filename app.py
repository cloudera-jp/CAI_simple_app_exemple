from flask import Flask, render_template, request
import pandas as pd
import os

from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
from pyspark.sql.types import *

app = Flask(__name__)

# KERBEROSレルムの取得
CDSW_DOMAIN = os.environ.get('CDSW_DOMAIN')
if CDSW_DOMAIN:
    parts = CDSW_DOMAIN.split('.')
    realm_low = '.'.join(parts[1:])
    realm = realm_low.upper()

# YARNプリンシパル文字列の生成
yarn_realm = "yarn/_HOST@" + realm

# Sparkセッションの初期化
spark = SparkSession.builder.appName("PythonSQL").master("local[*]").config("yarn.resourcemanager.principal",yarn_realm).getOrCreate()

# 初期表示データの読み込み
df = spark.sql("SELECT * FROM simple_external")
# df.createOrReplaceTempView("simple_external")

@app.route("/", methods=["GET", "POST"])
def index():
    filtered_results = []
    filter_value = ""

    if request.method == "POST":
        filter_value = request.form.get("city_filter", "")
        if filter_value:
            # Spark SQLを使ってデータをフィルタリング
            sql_query = f"SELECT * FROM simple_external WHERE col3 = '{filter_value}'"
            filtered_df = spark.sql(sql_query)
    else:
        filtered_df = df
            
    # Pandas DataFrameに変換してWeb表示用に整形
    filtered_results = filtered_df.toPandas().to_dict('records')
    
    return render_template("index.html", results=filtered_results, filter_value=filter_value)

# メイン
if __name__ == '__main__':

    try:
        app.run(host = '127.0.0.1', port = int(os.environ['CDSW_APP_PORT']))
    except Exception as e:
        print(f"ERROR: unable to run application:\n {str(e)}")
