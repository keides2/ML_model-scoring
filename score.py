# Usage: $ Python score.py submissioner's-name　[linux]
# 
import glob
import os
import sys
import csv
import pprint
import datetime
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import seaborn as sns
import matplotlib
# matplotlib.use('Agg')     # サーバー側 RuntimeError: Invalid DISPLAY variable 対策
import matplotlib.pyplot as plt
plt.switch_backend('Agg')   # サーバー側 RuntimeError: Invalid DISPLAY variable 対策
import update_metrix as mx  # update_metrix.py

# 混合行列、正解率、適合率、再現率、F1
def confusion(name, y_pred, y_truth):
    # y_truth = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    # y_pred = [0, 1, 1, 1, 1, 0, 0, 0, 1, 1]
    
    # 混合行列 Confusion Matrix
    cm = confusion_matrix(y_truth, y_pred)    
    print("Confusion Matrix: ")
    print(cm, "\n")

    # ヒートマップ
    plt.figure()
    sns.heatmap(cm, annot=True)
    print("Heat map: -> See the file 'img/confusion_matrix.png'")

    plt.savefig(img_dir + 'confusion_matrix.png')
    plt.close('all')
    
    # 正解率
    sc_acc = accuracy_score(y_truth, y_pred)
    sc_acc *= 100   # 単位[%]
    print("Accuracy: %f [%%]" % sc_acc)

    # 適合率
    sc_pre = precision_score(y_truth, y_pred)
    sc_pre *= 100   # 単位[%]
    print("Precision: %f [%%]" % sc_pre)

    # 再現率
    sc_rec = recall_score(y_truth, y_pred)
    sc_rec *= 100   # 単位[%]
    print("Recall: %f [%%]" % sc_rec)

    # F1
    sc_f1 = f1_score(y_truth, y_pred)
    sc_f1 *= 100   # 単位[%]
    print("F1-score: %f [%%]" % sc_f1)

    # カレントディレクトリは？
    # path = os.getcwd()
    # print("Current directory path: %s \n" % path)

    # ファイル名を都度更新する
    # 最新のファイル名取得
    list_of_files = glob.glob(base_dir + 'score_' + name + '*.csv')
    latest_sc_file = max(list_of_files, key=os.path.getctime)
    print("Latest file: %s" % latest_sc_file)

    # 前の結果から'trial'を読みだしてインクリメント、メトリックス更新
    # sc_file = base_dir + 'score_' + name + '.csv'
    # 0行目は header、0列目はインデックス
    # df = pd.read_csv(sc_file, header = 0, index_col=0)
    # 0行目は header、インデックスなし
    # 結果をファイルに保存
    df = pd.read_csv(latest_sc_file, header = 0)
    print("Before %s: \n" % latest_sc_file, df)
    # 最新ファイルを消す
    os.remove(latest_sc_file)

    '''
    # 今日の日付取得
    d_today = datetime.date.today()
    print("\nToday is: ", d_today)

    df.at[name, 'date'] = d_today   # 日付の更新
    trial = df.at[name, 'trial']    # 試行回数の取得
    trial += 1                      # 試行回数インクリメントして代入
    df.at[name, 'trial'] = trial
    df.at[name, 'accuracy'] = sc_acc.round(2)      # 小数点以下2桁に丸め
    df.at[name, 'precision'] = sc_pre.round(2)     # 小数点以下2桁に丸め
    df.at[name, 'recall'] = sc_rec.round(2)        # 小数点以下2桁に丸め
    df.at[name, 'f1'] = sc_f1.round(2)             # 小数点以下2桁に丸め
    '''
    # 今日の日時取得
    dt_now = datetime.datetime.now()
    d_todaytime = dt_now.strftime('%m-%d_%H-%M-%S')  # 09-28_18-31-13

    df.at[0, 'date'] = d_todaytime   # 日付時刻の更新
    trial = df.at[0, 'trial']        # 試行回数の取得（未使用）
    trial += 1                       # 試行回数インクリメントして代入
    df.at[0, 'trial'] = trial
    df.at[0, 'accuracy'] = sc_acc.round(2)      # 小数点以下2桁に丸め
    df.at[0, 'precision'] = sc_pre.round(2)     # 小数点以下2桁に丸め
    df.at[0, 'recall'] = sc_rec.round(2)        # 小数点以下2桁に丸め
    df.at[0, 'f1'] = sc_f1.round(2)             # 小数点以下2桁に丸め
    print("After: %s: \n" % latest_sc_file, df, "\n")

    # 新規保存
    # 今回作成するファイル
    suffix = dt_now.strftime('_%Y-%m-%d_%H-%M-%S')  # _2020-09-28_18-31-13
    this_file = base_dir + 'score_' + name + suffix +'.csv'
    print("This file : %s" % this_file)

    # ヘッダーあり（デフォルト）、インデックスあり（デフォルト）
    # df.to_csv(sc_file, header = True, index = True)
    # ヘッダーあり（デフォルト）、インデックスなし
    df.to_csv(this_file, header = True, index = False)
    print("Saved %s \n" % this_file)

# CSVファイルの読み込み
def read_csv(file_pred, file_truth):
    print("File name: %s" % file_pred)
    with open(file_pred,encoding="utf-8_sig") as f_p:
        pred = csv.reader(f_p)
        for row in pred:
            print(row)
    print("\n")

    print("File name: %s" % file_truth)
    with open(file_truth,encoding="utf-8_sig") as f_t:
        pred = csv.reader(f_t)
        for row in pred:
            print(row)
    print("\n")

# Pandas で CSVファイルの読み込み、インデックスあり用
def read_csv_pandas(file):
    print("Pandas read CSV file : %s" % file)
    try:
        # header あり（headerの行番号は0：デフォルト）
        # index あり（index_colを指定しないとindex列は認識しない）
        # index_col=0 は、indexとして使いたい列番号=0
        '''
        trial    mr.a      mr.b     mr.c     mr.d
            1    52.40     84.6     11.7     6.5
            2    34.30     64.9     23.7     3.7
            3    36.10     44.9     34.5     8.9
        '''
        # index_col=0 がないと
        '''
            trial    mr.a      mr.b     mr.c     mr.d
        0       1    52.40     84.6     11.7     6.5
        1       2    34.30     64.9     23.7     3.7
        2       3    36.10     44.9     34.5     8.9
        '''
        df = pd.read_csv(file, header = 0, index_col=0)
        print("Pandas DataFrame: ")
        print(df, "\n")
        return df
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    
# 採点用CSVファイルの生成
def make_combined(df_pred, df_truth, file_combined):
    # DataFrame から'正解'列抽出
    correct_col = df_truth[['truth']]

    # DataFrame 予測に、'正解'列を横方向に連結
    score = pd.concat([df_pred, correct_col], axis=1)
    print("Score DataFrame: ")
    print(score, "\n")

    # ファイル保存
    # ヘッダーあり（デフォルト）、インデックスあり（デフォルト）
    score.to_csv(file_combined, header = True, index = True)
    print("Saved %s ." % file_combined)


# メイン
def main():
    # 基底ディレクトリ
    global base_dir
    global submit_dir
    global img_dir

    # 引数チェック
    args = sys.argv
    if (len(args) < 2 or len(args) > 3):
        print("Usage: $ python " + args[0] + " name" + " [linux]")
        sys.exit(1)

    # Windows / Linux server
    if (len(args) == 2):
        # windows
        # Current dir: C:\gitlab\qc_ai_project\
        base_dir = 'src/go/pub/data/'
        submit_dir = 'submissions/'
        img_dir = 'src/go/img/'
    else:
        # Linux server
        # Current dir: /var/lib/jenkins/workspace/QC_AI_FAN/
        base_dir = '/home/kei/go/echo/pub/data/'
        submit_dir = '/home/kei/go/echo/submissions/'
        img_dir = '/home/kei/go/echo/img/'

    # 提出者名取得
    name = args[1]
    print("Name of submissioner (args[1]) is %s" % name)

    # 提出ファイル名を作成
    file_pred = submit_dir + "submission_" + name + ".csv"
    print("Prediction File is %s" % file_pred)

    # 正解ファイル名を作成
    file_truth = base_dir + "test.csv"
    print("Truth File name is %s" % file_truth)

    # 提出（予測）ファイルと正解ファイルを結合したファイル名を作成
    file_combined = base_dir + "combined.csv"
    print("Score File name is %s" % file_combined)
    print("\n")

    # 予測ファイル、正解ファイルの読み込み Pandas
    f_p = read_csv_pandas(file_pred)
    f_t = read_csv_pandas(file_truth)

    # 予測と正解の結合ファイル作成
    make_combined(f_p, f_t, file_combined)

    # 推測結果列と正解列抽出
    y_pred = f_p[['prediction']]
    y_truth = f_t[['truth']]

    # 混合行列、正解率、適合率、再現率、F1 を
    # 計算して成績ファイルの更新・保存まで
    confusion(name, y_pred, y_truth)

    # メトリックス・リスト
    metrix_list = ['accuracy', 'precision', 'recall', 'f1']
    
    # メトリックスの代入
    for metrix in metrix_list:
        print("--- Metrix: %s ---\n" % metrix)
        mx.insert_metrix(name, metrix, base_dir)

    # 順位付け
    for metrix in metrix_list:
        print("--- Rank : %s ---\n" % metrix)
        mx.rank(metrix, base_dir)

    # 終了
    print("Done! %s" % args[0])

# break

if __name__ == '__main__':
	main()
