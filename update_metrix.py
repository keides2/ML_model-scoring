# Usage: $ Python update_metrix.py submissioner's-name [linux]
# 
import glob
import os
import sys
import datetime
import numpy as np
import pandas as pd

# 代入
def insert_metrix(name, metrix, base_dir):
    # 代入先メトリックスファイルの読み込み
    f_metrix = base_dir + metrix + '.csv'

    # ヘッダありCSVの読み込み。0行目がヘッダ、インデックス無し
    df_metrix = pd.read_csv(f_metrix, header = 0)

    # 採点結果ファイルの読み込み
    # 最新のファイル名取得
    list_of_files = glob.glob(base_dir + 'score_' + name + '*.csv')
    latest_sc_file = max(list_of_files, key=os.path.getctime)
    print("Latest file: %s" % latest_sc_file)

    # ヘッダありCSVの読み込み。0行目がヘッダ
    df_score = read_csv_pandas(latest_sc_file)

    # メトリックス・データフレームの最後の行を取得
    df_tail = df_metrix.tail(1)
    print("Metrix '%s' DataFrame tail: \n" % metrix, df_tail, "\n")

    # 行末に追加する行を作成
    new_line = df_tail.copy()
    print("Copied new_line from tail: \n", new_line, "\n")

    # 動作確認
    '''
    print(df_score.index.values)    # ['mr.d']
    print(df_score.at[df_score.index.values[0], 'recall'])  # 50.0
    print(new_line.index.values[0]) # 10 as index
    print(new_line.at[new_line.index.values[0], 'mr.d'])   # 6.9 as mr.d's metrix
    '''

    # メトリックス代入
    # new_line.iat[1, name_column] = df_score.iat[1, metrix_column]
    new_line.at[new_line.index.values[0], name] = df_score.at[df_score.index.values[0], metrix]

    # 今日の日時取得
    dt_now = datetime.datetime.now()    # 2回目の取得なのでずれがある
    d_todaytime = dt_now.strftime('%m-%d_%H-%M-%S')  # 09-28_18-31-13

    # trial → date に変更、日時更新
    print("Before date: %s \n" % new_line.iat[0, 0])
    # new_line.iat[0, 0] += 1
    new_line.iat[0, 0] = d_todaytime
    print("New_line: \n", new_line, "\n")
    
    # 追加して上書き保存
    df_new = df_metrix.append(new_line)
    print("New '%s' DataFrame: \n" % metrix, df_new)
    
    # ファイル保存
    # ヘッダーあり（デフォルト）、インデックスなし
    f_metrix = base_dir + metrix + '.csv'
    df_new.to_csv(f_metrix, header = True, index = False)
    print("Saved %s .\n" % f_metrix)

# 順位付け
def rank(metrix, base_dir):
    # メトリックスファイルの読み込み
    f_metrix = base_dir + metrix + '.csv'

    # ヘッダありCSVの読み込み。0行目がヘッダ、インデックス無し
    df_metrix = pd.read_csv(f_metrix, header = 0)
    print("Read metrix '%s' file: \n" % metrix, df_metrix, '\n')

    # ランク
    # 'trial' → 'date' 列保存
    df_trial = df_metrix[['date']]
    print("'date' \n", df_trial, '\n')
    # 'trial' → 'date' 列削除
    df_metrix_no_trial = df_metrix.loc[:, 'mr.a':]   # 行は全部、列は'mr.a'から右全部
    print("Deleted 'date' column from %s DataFrame:\n" % metrix, df_metrix_no_trial, '\n')

    # 行ごとに順位付け、降順
    df_rank = df_metrix_no_trial.rank(axis=1, ascending=False)
    print("Rank : %s\n" % metrix, df_rank, '\n')

    # 'trial' → 'date' 列復帰
    df_rank = df_trial.join(df_rank)
    print("'date' added Rank : %s\n" % metrix, df_rank)

    # ファイル保存
    # ヘッダーあり（デフォルト）、インデックスなし
    f_rank = base_dir + 'rank_' + metrix + '.csv'
    df_rank.to_csv(f_rank, header = True, index = False)
    print("Saved %s .\n" % f_rank)

# Pandas で CSVファイルの読み込み
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
        # index_col=0 ないとき
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

# メイン
def main():
    # 基底ディレクトリ
    global base_dir

    # 引数チェック
    args = sys.argv
    if (len(args) < 2 or len(args) > 3):
        print("Usage: $ python " + args[0] + " name" + " [linux]")
        sys.exit(1)

    # Windows / Linux server
    if (len(args) == 2):
        # windows
        base_dir = 'src/go/pub/data/'
    else:
        # Linux server
        base_dir = '/home/kei/go/echo/pub/data/'

    # 提出者名取得
    name = args[1]
    print("Name (args[1]) is %s \n" % name)

    # メトリックス・リスト
    metrix_list = ['accuracy', 'precision', 'recall', 'f1']
    
    # メトリックスの代入
    for metrix in metrix_list:
        insert_metrix(name, metrix, base_dir)

    # 順位付け
    for metrix in metrix_list:
        rank(metrix, base_dir)
    
    # 終了
    print("Done! %s" % args[0])

# break

if __name__ == '__main__':
	main()
