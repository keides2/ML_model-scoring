<!-- TOC -->

- [1. Jenkins の設定](#1-jenkins-の設定)
  - [1.1. Jenkinsの管理](#11-jenkinsの管理)
    - [1.1.1. システムの設定](#111-システムの設定)
    - [1.1.2. プラグインの管理](#112-プラグインの管理)
    - [1.1.3. Manage Credentials(認証情報)](#113-manage-credentials認証情報)
    - [1.1.4. Jenkins ユーザーの変更](#114-jenkins-ユーザーの変更)
  - [1.2. プロジェクト QC_AI_PROJECT](#12-プロジェクト-qc_ai_project)
    - [1.2.1 設定](#121-設定)
  - [1.3. ログ](#13-ログ)
    - [1.3.1. Jenkins ログ](#131-jenkins-ログ)
    - [1.3.2. SCM ポーリング失敗時のログ](#132-scm-ポーリング失敗時のログ)
    - [1.3.3. パラメータ付きビルド時のログ(図は#95, ログは#102の例)](#133-パラメータ付きビルド時のログ図は95-ログは102の例)
    - [1.3.4. 採点結果](#134-採点結果)
- [2. GitLab](#2-gitlab)
  - [2.1. .git > config](#21-git--config)
- [3. 実行ファイル、CSVデータファイルの配置（Ubuntu16.04LTS）](#3-実行ファイルcsvデータファイルの配置ubuntu1604lts)
  - [3.1.  実行ファイル](#31--実行ファイル)
  - [3.2. サブミッション・ファイル submission_name.csv](#32-サブミッションファイル-submission_namecsv)
  - [3.3. CSVファイル](#33-csvファイル)
  - [3.3. Echo](#33-echo)
- [4. 採点結果グラフ表示ページ](#4-採点結果グラフ表示ページ)
  - [4.1. HTML](#41-html)
  - [4.2. JavaScript](#42-javascript)

<!-- /TOC -->

# 1. Jenkins の設定

- `Jenkins`の設定や情報などを記録しておく
- サーバーは、`Ubuntu16.04LTS`
- URLは、http://xxx.xxx.xxx.xxx:9999/
- `Jenkins`のバージョンは、`2.231`
- ジョブ名は、`QC_AI_PROJECT`
- スクリプトなどのソースファイル保存場所は、`GitLab`
- `GitLab`のクローン用アドレスは、https://abcd.com/gitlab/deviceai/qc_ai_project.git
- ブランチは、`submit`
- 稼働時期： 2020年10月1日～

## 1.1. Jenkinsの管理

### 1.1.1. システムの設定

![1-1-1](./images/jenkins/1-1-1.jpg)

![1-1-2](./images/Jenkins/1-1-2.jpg)

![1-1-3](./images/Jenkins/1-1-3.jpg)

![1-1-4](./images/Jenkins/1-1-4.jpg)

- `Gitlab host URL`は、`http://`ではなく、`https://`
- `Global host URL`に`mr.d:Gitlabのトークン`を入れない。入れると`Test Connection`が失敗する

![1-1-5](./images/Jenkins/1-1-5.jpg)

![1-1-6](./images/Jenkins/1-1-6.jpg)

### 1.1.2. プラグインの管理

- インストール済み

![1-2-1](./images/Jenkins/1-2-1.jpg)

### 1.1.3. Manage Credentials(認証情報)

![1-3-1](./images/jenkins/1-3-1.jpg)

### 1.1.4. Jenkins ユーザーの変更

- `Ubuntu`上のWebサーバー`Echo`の実行ユーザーが`kei`なので、`Jenkins`が作ったファイルなどを`kei`のフォルダーにコピーする際に、アクセス権がない場合がある
- よってジョブのシェルスクリプトをデフォルトのユーザー`jenkins`ではなく、別のユーザ`kei`で実行したい
- コマンド単位で別ユーザーに変更することができるが、色々面倒な設定や変更が必要なため、`Jenkins`実行ユーザーを`Ubuntu`のユーザー`kei`に変更する
- このために実行したコマンドは次の通り

     ```bash
     $ sudo -iu root
     $ vi /etc/default/jenkins 
     - JENKINS_USER=$NAME
     + JENKINS_USER=kei
     $ chown -R kei: /var/lib/jenkins /var/log/jenkins /var/cache/jenkins
     $ systemctl restart jenkins
     ```

## 1.2. プロジェクト QC_AI_PROJECT

### 1.2.1 設定

- General

![2-1-1](./images/jenkins/2-1-1.jpg)

![2-1-2](./images/jenkins/2-1-2.jpg)

- ソースコード管理

![2-1-3](./images/jenkins/2-1-3.jpg)

- ビルド・トリガ
  - テスト用
  
![2-1-4](./images/jenkins/2-1-4.jpg)

- ビルド・トリガ
  - 本番

![2-1-5](./images/jenkins/2-1-5.jpg)

- ビルド環境
- ビルド
  - シェルの実行

![2-1-6](./images/Jenkins/2-1-6.jpg)

```bash
#!/bin/bash
# QC_AI_PROJECT Jenkins script 2020-09

echo "●Who am I? I am "`whoami`"."
# Who am I? I am kei.
echo "●Current directory is: "`pwd`
# Current directory is: /var/lib/jenkins/workspace/QC_AI_PROJECT
echo "●Python --version is: "`python --version`
# Python 2.7.12
echo "●Python full-path is: "`which python`
# Python full-path is: /usr/bin/python
echo "●Python3 --version is: "`python3 --version`
# Python3 --version is: Python 3.5.2
echo "●Python3 full-path is: "`which python3`
# Python3 full-path is: /usr/bin/python3
echo

# 環境変数
# echo $http_proxy
# echo $https_proxy

# export http_proxy="http://proxy.abcd.com:3128/"
# export https_proxy='http://proxy.abcd.com:3128/'

# Git
# git config --global http.proxy http://proxy.abcd.com:3128/
# git config --global https.proxy http://proxy.abcd.com:3128/

# git config --global user.name "mr.d"
# git config --global user.email "mr.d@abcd.com"

echo "●git remote -v"
git remote -v
echo
# origin	https://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git (fetch)
# origin	https://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git (push)

# git remote add origin https://mr.d@abcd.com/gitlab/deviceai/qc_ai_project.git
# fatal: remote origin already exists.

echo "●git config --list"
git config --list
echo
# http.proxy=http://proxy.abcd.com:3128/
# https.proxy=http://proxy.abcd.com:3128/
# user.name=mr.d
# user.email=mr.d@abcd.com
# core.repositoryformatversion=0
# core.filemode=true
# core.bare=false
# core.logallrefupdates=true
# remote.origin.url=https://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git
# remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*

echo "●git branch"
git branch
echo
# * (HEAD detached at d5f2a69)

echo "●git branch -r"
git branch -r
echo
# origin/15-baseline-ai
# origin/28-baseline
# origin/42-visdom
# origin/54-
# origin/NG-rpm
# origin/mr.b_0721_baseline_rpm
# origin/master
# origin/submit

# ブランチ変更
# git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
# git fetch --all
# Fetching origin

echo "●git checkout submit"
git checkout submit
echo
# Previous HEAD position was d5f2a69... Merge branch 'score-0903' into 'master'
# Switched to a new branch 'submit'
# Branch submit set up to track remote branch submit from origin.

echo "●追加/変更されたファイルの確認"
for file in `git diff --name-only HEAD..origin/submit`
do
    echo "File name: "$file
    name=`echo $file | sed -r 's/.*submission_(.*).csv/\1/'`
    echo "Submissioner's name: "$name

    # submission_name.csv, test.csv プル
    git pull origin submit:submit

    echo "●submission_name.csv を Echo へコピー"
    cp ./submissions/submission_$name.csv /home/kei/go/echo/submissions
    echo

    # 採点開始
    /home/kei/.pyenv/shims/python3 /home/kei/go/echo/score.py $name linux > /home/kei/go/echo/score.log 2>&1

done

echo "Done!"
```

- ビルド後の処理

![2-1-7](./images/Jenkins/2-1-7.jpg)

## 1.3. ログ

### 1.3.1. Jenkins ログ

```bash
/var/lib/jenkins/logs/tasks/*.log
```

- あまり見ない
- オーナーを `kei` に変更済み

![log](./images/Jenkins/var-lib-jenkins-logs-tasks-20200928-1.jpg)

### 1.3.2. SCM ポーリング失敗時のログ

```bash
/var/lib/jenkins/jobs/QC_AI_PROJECT/scm-polling.log
```

- オーナーを kei に変更済み

![job](./images/Jenkins/var-lib-jenkins-jobs-QC_AI_PROJECT-20200928-1.jpg)

```LOG
Started on 2020/09/28 16:00:00
Polling SCM changes on master
Using strategy: Default
[poll] Last Built Revision: Revision d0cffdc32b0e1307d36469542ba4100575b2356c (origin/submit)
using credential bcbbab18-d851-4587-a60e-fdfe30dff125
 > git rev-parse --is-inside-work-tree # timeout=10
Fetching changes from the remote Git repositories
 > git config remote.origin.url http://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git # timeout=10
Fetching upstream changes from http://mr.d@abcd.com/gitlab/deviceai/qc_ai_project.git
 > git --version # timeout=10
using GIT_ASKPASS to set credentials GitLab用
Setting http proxy: proxy.abcd.com:3128
 > git fetch --tags --progress http://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git +refs/heads/*:refs/remotes/origin/* # timeout=10
Polling for changes in
Seen branch in repository origin/15-baseline-ai
Seen branch in repository origin/28-baseline
Seen branch in repository origin/42-visdom
Seen branch in repository origin/54-
Seen branch in repository origin/NG-rpm
Seen branch in repository origin/mr.b_0721_baseline_rpm
Seen branch in repository origin/master
Seen branch in repository origin/submit
Seen 8 remote branches
 > git show-ref --tags -d # timeout=10
 > git log --full-history --no-abbrev --format=raw -M -m d0cffdc32b0e1307d36469542ba4100575b2356c..6c650f3a6ba29e8041c27eb671db3ca68960dbe5 # timeout=10
Done. Took 0.9 秒
Changes found
```

### 1.3.3. パラメータ付きビルド時のログ(図は#95, ログは#102の例)

```bash
/var/lib/jenkins/jobs/QC_AI_PROJECT/builds/95/log
```

- オーナーを kei に変更済み

![build](./images/Jenkins/var-lib-jenkins-jobs-QC_AI_PROJECT-builds-95-20200928-1.jpg)

```LOG
ユーザー[8mha:////4NNaEK7UA5/uwadFvls0zOmxpcFhv6mKpwn3ezeoz3gFAAAAmx+LCAAAAAAAAP9b85aBtbiIQTGjNKU4P08vOT+vOD8nVc83PyU1x6OyILUoJzMv2y+/JJUBAhiZGBgqihhk0NSjKDWzXb3RdlLBUSYGJk8GtpzUvPSSDB8G5tKinBIGIZ+sxLJE/ZzEvHT94JKizLx0a6BxUmjGOUNodHsLgAzBEgZ+/dLi1CL94ozM3MSSxLxMAE8qu6DEAAAA[mr.dが実行
Running as SYSTEM
masterでビルドします。 ワークスペース: /var/lib/jenkins/workspace/QC_AI_PROJECT
using credential bcbbab18-d851-4587-a60e-fdfe30dff125
 > git rev-parse --is-inside-work-tree # timeout=10
Fetching changes from the remote Git repository
 > git config remote.origin.url http://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git # timeout=10
Fetching upstream changes from http://mr.d@abcd.com/gitlab/deviceai/qc_ai_project.git
 > git --version # timeout=10
using GIT_ASKPASS to set credentials GitLab用
Setting http proxy: proxy.abcd.com:3128
 > git fetch --tags --progress http://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git rev-parse origin/submit^{commit} # timeout=10
Checking out Revision cc996a516b05eef3e1a43d187c6e92bfd570fddc (origin/submit)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f cc996a516b05eef3e1a43d187c6e92bfd570fddc # timeout=10
Commit message: "retry"
 > git rev-list --no-walk 006fc66feca64abbcdc1fd9c330a98ed92eec445 # timeout=10
[QC_AI_PROJECT] $ /bin/bash /tmp/jenkins4817663175319379484.sh
/home/kei/GitLab/qc_ai_project
Who am I? I am kei.
Current directory is: /home/kei/GitLab/qc_ai_project
Python 2.7.12
Python --version is: 
Python full-path is: /usr/bin/python
Python3 --version is: Python 3.5.2
Python3 full-path is: /usr/bin/python3
origin	http://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git (fetch)
origin	http://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git (push)
user.name=mr.d
user.email=mr.d@abcd.com
http.http://abcd.com/gitlab/.proxy=http://proxy.abcd.com:3128/
https.http://abcd.com/gitlab/.proxy=http://proxy.abcd.com:3128/
https.https://github.com/.proxy=http://proxy2.abcd.com:3128/
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
remote.origin.url=http://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
branch.master.remote=origin
branch.master.merge=refs/heads/master
branch.submit.remote=origin
branch.submit.merge=refs/heads/submit
  master
* submit
  origin/15-baseline-ai
  origin/28-baseline
  origin/42-visdom
  origin/54-
  origin/HEAD -> origin/master
  origin/NG-rpm
  origin/mr.b_0721_baseline_rpm
  origin/master
  origin/submit
Fetching origin
From http://abcd.com/gitlab/deviceai/qc_ai_project
   006fc66..cc996a5  submit     -> origin/submit
Already on 'submit'
このブランチは 'origin/submit' に比べて1コミット遅れています。fast-forwardすることができます。
  (use "git pull" to update your local branch)
追加/変更されたファイルの確認
File name: submissions/submission_mr.d.csv
Submissioner's name: mr.d
From http://abcd.com/gitlab/deviceai/qc_ai_project
   006fc66..cc996a5  submit     -> submit
warning: fetch updated the current branch head.
fast-forwarding your working tree from
commit 006fc66feca64abbcdc1fd9c330a98ed92eec445.
Already up-to-date.
Echoへコピー
Done!
Finished: SUCCESS
```

### 1.3.4. 採点結果

```bash
/var/lib/jenkins/workspace/QC_AI_PROJECT/src/go/score.log
```

- オーナーを kei に変更済み

![score](./images/Jenkins/var-lib-jenkins-jobs-QC_AI_PROJECT-src-go-20200928-1.jpg)

```LOG
Name of submissioner (args[1]) is mr.a
prediction File is /home/kei/go/echo/submissions/submission_mr.a.csv
Truth File name is /home/kei/go/echo/pub/data/test.csv
Score File name is /home/kei/go/echo/pub/data/combined.csv


Pandas read CSV file : /home/kei/go/echo/submissions/submission_mr.a.csv
Pandas DataFrame: 
             prediction
id                     
iuvw_000001           0
iuvw_000002           1
iuvw_000003           1
iuvw_000004           1
iuvw_000005           1
iuvw_000006           0
iuvw_100001           0
iuvw_100002           1
iuvw_100003           0
iuvw_100004           0
iuvw_100005           0
iuvw_100006           0
iuvw_100007           0
iuvw_100008           1
iuvw_100009           1
iuvw_100010           1
iuvw_100011           1
iuvw_100012           1
iuvw_100013           1
iuvw_100014           1
iuvw_100015           1
iuvw_100016           0
iuvw_100017           0
iuvw_100018           0
iuvw_100019           0
iuvw_100020           0
iuvw_100021           0 

Pandas read CSV file : /home/kei/go/echo/pub/data/test.csv
Pandas DataFrame: 
             truth
id                
iuvw_000001      1
iuvw_000002      1
iuvw_000003      1
iuvw_000004      1
iuvw_000005      1
iuvw_000006      1
iuvw_100001      0
iuvw_100002      0
iuvw_100003      0
iuvw_100004      0
iuvw_100005      0
iuvw_100006      0
iuvw_100007      0
iuvw_100008      0
iuvw_100009      0
iuvw_100010      0
iuvw_100011      0
iuvw_100012      0
iuvw_100013      0
iuvw_100014      0
iuvw_100015      0
iuvw_100016      0
iuvw_100017      0
iuvw_100018      0
iuvw_100019      0
iuvw_100020      0
iuvw_100021      0 

Score DataFrame: 
             prediction  truth
id                            
iuvw_000001           0      1
iuvw_000002           1      1
iuvw_000003           1      1
iuvw_000004           1      1
iuvw_000005           1      1
iuvw_000006           0      1
iuvw_100001           0      0
iuvw_100002           1      0
iuvw_100003           0      0
iuvw_100004           0      0
iuvw_100005           0      0
iuvw_100006           0      0
iuvw_100007           0      0
iuvw_100008           1      0
iuvw_100009           1      0
iuvw_100010           1      0
iuvw_100011           1      0
iuvw_100012           1      0
iuvw_100013           1      0
iuvw_100014           1      0
iuvw_100015           1      0
iuvw_100016           0      0
iuvw_100017           0      0
iuvw_100018           0      0
iuvw_100019           0      0
iuvw_100020           0      0
iuvw_100021           0      0 

Saved /home/kei/go/echo/pub/data/combined.csv .
Confusion Matrix: 
[[12  9]
 [ 2  4]] 

Heat map: -> See the file './images/confusion_matrix.png'
Accuracy: 59.259259 [%]
Precision: 30.769231 [%]
Recall: 66.666667 [%]
F1-score: 42.105263 [%]

Today is:  2020-09-28
Latest file: /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_15-39-51.csv
Before /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_15-39-51.csv: 
         name        date  trial  accuracy  precision  recall     f1
0  mr.d  2020-09-28     14     81.48      57.14      66  61.54
After: /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_15-39-51.csv: 
         name        date  trial  accuracy  precision  recall     f1
0  mr.d  2020-09-28     15     59.26      30.77      66  42.11 

This file : /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv
Saved /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv 

--- Metrix: accuracy ---

Latest file: /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv
Pandas read CSV file : /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv
Pandas DataFrame: 
                 date  trial  accuracy  precision  recall     f1
name                                                            
mr.d  2020-09-28     15     59.26      30.77      66  42.11 

Metrix 'accuracy' DataFrame tail: 
     trial  mr.a  mr.b  mr.c  mr.d
17     18    81.48      7.2    77.78      74.07 

Copied new_line from tail: 
     trial  mr.a  mr.b  mr.c  mr.d
17     18    81.48      7.2    77.78      74.07 

Before trial: 18 

New_line: 
     trial  mr.a  mr.b  mr.c  mr.d
17     19    59.26      7.2    77.78      74.07 

New 'accuracy' DataFrame: 
     trial  mr.a  mr.b  mr.c  mr.d
0       1    12.40      4.6    11.70       8.20
1       2    14.30      4.9    13.70       9.30
2       3    16.10      4.9    14.50       6.70
3       4    15.30      3.6    11.30       2.50
4       5    15.00      4.4    11.40       4.90
5       6    18.10      5.5    13.80       1.80
6       7    18.50      5.2    13.20       3.70
7       8    21.00      5.5    13.40       2.90
8       9    24.20      6.1    13.90       9.70
9      10    28.50      7.2    15.20       6.90
10     11    92.59      7.2    15.20       6.90
11     12    92.59      7.2    15.20      66.67
12     13    92.59      7.2    15.20      74.07
13     14    92.59      7.2    15.20      62.96
14     15    92.59      7.2    77.78      62.96
15     16    81.48      7.2    77.78      62.96
16     17    81.48      7.2    77.78      66.67
17     18    81.48      7.2    77.78      74.07
17     19    59.26      7.2    77.78      74.07
Saved /home/kei/go/echo/pub/data/accuracy.csv .

--- Metrix: precision ---

Latest file: /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv
Pandas read CSV file : /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv
Pandas DataFrame: 
                 date  trial  accuracy  precision  recall     f1
name                                                            
mr.d  2020-09-28     15     59.26      30.77      66  42.11 

Metrix 'precision' DataFrame tail: 
     trial  mr.a  mr.b  mr.c  mr.d
17     18    57.14     97.2     50.0      42.86 

Copied new_line from tail: 
     trial  mr.a  mr.b  mr.c  mr.d
17     18    57.14     97.2     50.0      42.86 

Before trial: 18 

New_line: 
     trial  mr.a  mr.b  mr.c  mr.d
17     19    30.77     97.2     50.0      42.86 

New 'precision' DataFrame: 
     trial  mr.a  mr.b  mr.c  mr.d
0       1    42.40     14.6      1.7      54.50
1       2    54.30     24.9      3.7      56.30
2       3    26.10     34.9      4.5      34.20
3       4    65.30     43.6     11.3      76.10
4       5    75.00     54.4     21.4       5.90
5       6    18.10     65.5     33.8      12.60
6       7    48.50     75.2     13.2      47.30
7       8    21.00     85.5     63.4      63.60
8       9    74.20     96.1     76.9      35.90
9      10    88.50     97.2     85.2      46.20
10     11    83.33     97.2     85.2      46.20
11     12    83.33     97.2     85.2      33.33
12     13    83.33     97.2     85.2      42.86
13     14    83.33     97.2     85.2      30.00
14     15    83.33     97.2     50.0      30.00
15     16    57.14     97.2     50.0      30.00
16     17    57.14     97.2     50.0      33.33
17     18    57.14     97.2     50.0      42.86
17     19    30.77     97.2     50.0      42.86
Saved /home/kei/go/echo/pub/data/precision.csv .

--- Metrix: recall ---

Latest file: /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv
Pandas read CSV file : /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv
Pandas DataFrame: 
                 date  trial  accuracy  precision  recall     f1
name                                                            
mr.d  2020-09-28     15     59.26      30.77      66  42.11 

Metrix 'recall' DataFrame tail: 
     trial  mr.a  mr.b  mr.c  mr.d
17     18     66.0     87.2     66.0       50.0 

Copied new_line from tail: 
     trial  mr.a  mr.b  mr.c  mr.d
17     18     66.0     87.2     66.0       50.0 

Before trial: 18 

New_line: 
     trial  mr.a  mr.b  mr.c  mr.d
17     19     66.0     87.2     66.0       50.0 

New 'recall' DataFrame: 
     trial  mr.a  mr.b  mr.c  mr.d
0       1     32.4     84.6     11.7        8.2
1       2     14.3     74.9     43.7        9.3
2       3     66.1     64.9     24.5        6.7
3       4     15.3     53.6     11.3        2.5
4       5     85.0     34.4     61.4        4.9
5       6     18.1     75.5     73.8        1.8
6       7     78.5     45.2     83.2        3.7
7       8     21.0     85.5     13.4        2.9
8       9     24.2     96.1     83.9        9.7
9      10     28.5     87.2     85.2        8.2
10     11     83.0     87.2     85.2        8.2
11     12     83.0     87.2     85.2       50.0
12     13     83.0     87.2     85.2       50.0
13     14     83.0     87.2     85.2       50.0
14     15     83.0     87.2     66.0       50.0
15     16     66.0     87.2     66.0       50.0
16     17     66.0     87.2     66.0       50.0
17     18     66.0     87.2     66.0       50.0
17     19     66.0     87.2     66.0       50.0
Saved /home/kei/go/echo/pub/data/recall.csv .

--- Metrix: f1 ---

Latest file: /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv
Pandas read CSV file : /home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv
Pandas DataFrame: 
                 date  trial  accuracy  precision  recall     f1
name                                                            
mr.d  2020-09-28     15     59.26      30.77      66  42.11 

Metrix 'f1' DataFrame tail: 
     trial  mr.a  mr.b  mr.c  mr.d
17     18    61.54     97.2    57.14      46.15 

Copied new_line from tail: 
     trial  mr.a  mr.b  mr.c  mr.d
17     18    61.54     97.2    57.14      46.15 

Before trial: 18 

New_line: 
     trial  mr.a  mr.b  mr.c  mr.d
17     19    42.11     97.2    57.14      46.15 

New 'f1' DataFrame: 
     trial  mr.a  mr.b  mr.c  mr.d
0       1    52.40     84.6    11.70       6.50
1       2    34.30     64.9    23.70       3.70
2       3    36.10     44.9    34.50       8.90
3       4    25.30     34.6    61.30      90.20
4       5    15.00     46.4    91.40      30.40
5       6    48.10     59.5    13.80      25.60
6       7    78.50     65.2    43.20      67.30
7       8    21.00     75.5    53.40      78.10
8       9    14.20     86.1    83.90      45.40
9      10    28.50     97.2    75.20      61.80
10     11    83.33     97.2    75.20      61.80
11     12    83.33     97.2    75.20      40.00
12     13    83.33     97.2    75.20      46.15
13     14    83.33     97.2    75.20      37.50
14     15    83.33     97.2    57.14      37.50
15     16    61.54     97.2    57.14      37.50
16     17    61.54     97.2    57.14      40.00
17     18    61.54     97.2    57.14      46.15
17     19    42.11     97.2    57.14      46.15
Saved /home/kei/go/echo/pub/data/f1.csv .

--- Rank : accuracy ---

Read metrix 'accuracy' file: 
     trial  mr.a  mr.b  mr.c  mr.d
0       1    12.40      4.6    11.70       8.20
1       2    14.30      4.9    13.70       9.30
2       3    16.10      4.9    14.50       6.70
3       4    15.30      3.6    11.30       2.50
4       5    15.00      4.4    11.40       4.90
5       6    18.10      5.5    13.80       1.80
6       7    18.50      5.2    13.20       3.70
7       8    21.00      5.5    13.40       2.90
8       9    24.20      6.1    13.90       9.70
9      10    28.50      7.2    15.20       6.90
10     11    92.59      7.2    15.20       6.90
11     12    92.59      7.2    15.20      66.67
12     13    92.59      7.2    15.20      74.07
13     14    92.59      7.2    15.20      62.96
14     15    92.59      7.2    77.78      62.96
15     16    81.48      7.2    77.78      62.96
16     17    81.48      7.2    77.78      66.67
17     18    81.48      7.2    77.78      74.07
18     19    59.26      7.2    77.78      74.07 

'trial' 
     trial
0       1
1       2
2       3
3       4
4       5
5       6
6       7
7       8
8       9
9      10
10     11
11     12
12     13
13     14
14     15
15     16
16     17
17     18
18     19 

Deleted 'trial' column from accuracy DataFrame:
     mr.a  mr.b  mr.c  mr.d
0     12.40      4.6    11.70       8.20
1     14.30      4.9    13.70       9.30
2     16.10      4.9    14.50       6.70
3     15.30      3.6    11.30       2.50
4     15.00      4.4    11.40       4.90
5     18.10      5.5    13.80       1.80
6     18.50      5.2    13.20       3.70
7     21.00      5.5    13.40       2.90
8     24.20      6.1    13.90       9.70
9     28.50      7.2    15.20       6.90
10    92.59      7.2    15.20       6.90
11    92.59      7.2    15.20      66.67
12    92.59      7.2    15.20      74.07
13    92.59      7.2    15.20      62.96
14    92.59      7.2    77.78      62.96
15    81.48      7.2    77.78      62.96
16    81.48      7.2    77.78      66.67
17    81.48      7.2    77.78      74.07
18    59.26      7.2    77.78      74.07 

Rank : accuracy
     mr.a  mr.b  mr.c  mr.d
0       1.0      4.0      2.0        3.0
1       1.0      4.0      2.0        3.0
2       1.0      4.0      2.0        3.0
3       1.0      3.0      2.0        4.0
4       1.0      4.0      2.0        3.0
5       1.0      3.0      2.0        4.0
6       1.0      3.0      2.0        4.0
7       1.0      3.0      2.0        4.0
8       1.0      4.0      2.0        3.0
9       1.0      3.0      2.0        4.0
10      1.0      3.0      2.0        4.0
11      1.0      4.0      3.0        2.0
12      1.0      4.0      3.0        2.0
13      1.0      4.0      3.0        2.0
14      1.0      4.0      2.0        3.0
15      1.0      4.0      2.0        3.0
16      1.0      4.0      2.0        3.0
17      1.0      4.0      2.0        3.0
18      3.0      4.0      1.0        2.0 

'trial' added Rank : accuracy
     trial  mr.a  mr.b  mr.c  mr.d
0       1      1.0      4.0      2.0        3.0
1       2      1.0      4.0      2.0        3.0
2       3      1.0      4.0      2.0        3.0
3       4      1.0      3.0      2.0        4.0
4       5      1.0      4.0      2.0        3.0
5       6      1.0      3.0      2.0        4.0
6       7      1.0      3.0      2.0        4.0
7       8      1.0      3.0      2.0        4.0
8       9      1.0      4.0      2.0        3.0
9      10      1.0      3.0      2.0        4.0
10     11      1.0      3.0      2.0        4.0
11     12      1.0      4.0      3.0        2.0
12     13      1.0      4.0      3.0        2.0
13     14      1.0      4.0      3.0        2.0
14     15      1.0      4.0      2.0        3.0
15     16      1.0      4.0      2.0        3.0
16     17      1.0      4.0      2.0        3.0
17     18      1.0      4.0      2.0        3.0
18     19      3.0      4.0      1.0        2.0
Saved /home/kei/go/echo/pub/data/rank_accuracy.csv .

--- Rank : precision ---

Read metrix 'precision' file: 
     trial  mr.a  mr.b  mr.c  mr.d
0       1    42.40     14.6      1.7      54.50
1       2    54.30     24.9      3.7      56.30
2       3    26.10     34.9      4.5      34.20
3       4    65.30     43.6     11.3      76.10
4       5    75.00     54.4     21.4       5.90
5       6    18.10     65.5     33.8      12.60
6       7    48.50     75.2     13.2      47.30
7       8    21.00     85.5     63.4      63.60
8       9    74.20     96.1     76.9      35.90
9      10    88.50     97.2     85.2      46.20
10     11    83.33     97.2     85.2      46.20
11     12    83.33     97.2     85.2      33.33
12     13    83.33     97.2     85.2      42.86
13     14    83.33     97.2     85.2      30.00
14     15    83.33     97.2     50.0      30.00
15     16    57.14     97.2     50.0      30.00
16     17    57.14     97.2     50.0      33.33
17     18    57.14     97.2     50.0      42.86
18     19    30.77     97.2     50.0      42.86 

'trial' 
     trial
0       1
1       2
2       3
3       4
4       5
5       6
6       7
7       8
8       9
9      10
10     11
11     12
12     13
13     14
14     15
15     16
16     17
17     18
18     19 

Deleted 'trial' column from precision DataFrame:
     mr.a  mr.b  mr.c  mr.d
0     42.40     14.6      1.7      54.50
1     54.30     24.9      3.7      56.30
2     26.10     34.9      4.5      34.20
3     65.30     43.6     11.3      76.10
4     75.00     54.4     21.4       5.90
5     18.10     65.5     33.8      12.60
6     48.50     75.2     13.2      47.30
7     21.00     85.5     63.4      63.60
8     74.20     96.1     76.9      35.90
9     88.50     97.2     85.2      46.20
10    83.33     97.2     85.2      46.20
11    83.33     97.2     85.2      33.33
12    83.33     97.2     85.2      42.86
13    83.33     97.2     85.2      30.00
14    83.33     97.2     50.0      30.00
15    57.14     97.2     50.0      30.00
16    57.14     97.2     50.0      33.33
17    57.14     97.2     50.0      42.86
18    30.77     97.2     50.0      42.86 

Rank : precision
     mr.a  mr.b  mr.c  mr.d
0       2.0      3.0      4.0        1.0
1       2.0      3.0      4.0        1.0
2       3.0      1.0      4.0        2.0
3       2.0      3.0      4.0        1.0
4       1.0      2.0      3.0        4.0
5       3.0      1.0      2.0        4.0
6       2.0      1.0      4.0        3.0
7       4.0      1.0      3.0        2.0
8       3.0      1.0      2.0        4.0
9       2.0      1.0      3.0        4.0
10      3.0      1.0      2.0        4.0
11      3.0      1.0      2.0        4.0
12      3.0      1.0      2.0        4.0
13      3.0      1.0      2.0        4.0
14      2.0      1.0      3.0        4.0
15      2.0      1.0      3.0        4.0
16      2.0      1.0      3.0        4.0
17      2.0      1.0      3.0        4.0
18      4.0      1.0      2.0        3.0 

'trial' added Rank : precision
     trial  mr.a  mr.b  mr.c  mr.d
0       1      2.0      3.0      4.0        1.0
1       2      2.0      3.0      4.0        1.0
2       3      3.0      1.0      4.0        2.0
3       4      2.0      3.0      4.0        1.0
4       5      1.0      2.0      3.0        4.0
5       6      3.0      1.0      2.0        4.0
6       7      2.0      1.0      4.0        3.0
7       8      4.0      1.0      3.0        2.0
8       9      3.0      1.0      2.0        4.0
9      10      2.0      1.0      3.0        4.0
10     11      3.0      1.0      2.0        4.0
11     12      3.0      1.0      2.0        4.0
12     13      3.0      1.0      2.0        4.0
13     14      3.0      1.0      2.0        4.0
14     15      2.0      1.0      3.0        4.0
15     16      2.0      1.0      3.0        4.0
16     17      2.0      1.0      3.0        4.0
17     18      2.0      1.0      3.0        4.0
18     19      4.0      1.0      2.0        3.0
Saved /home/kei/go/echo/pub/data/rank_precision.csv .

--- Rank : recall ---

Read metrix 'recall' file: 
     trial  mr.a  mr.b  mr.c  mr.d
0       1     32.4     84.6     11.7        8.2
1       2     14.3     74.9     43.7        9.3
2       3     66.1     64.9     24.5        6.7
3       4     15.3     53.6     11.3        2.5
4       5     85.0     34.4     61.4        4.9
5       6     18.1     75.5     73.8        1.8
6       7     78.5     45.2     83.2        3.7
7       8     21.0     85.5     13.4        2.9
8       9     24.2     96.1     83.9        9.7
9      10     28.5     87.2     85.2        8.2
10     11     83.0     87.2     85.2        8.2
11     12     83.0     87.2     85.2       50.0
12     13     83.0     87.2     85.2       50.0
13     14     83.0     87.2     85.2       50.0
14     15     83.0     87.2     66.0       50.0
15     16     66.0     87.2     66.0       50.0
16     17     66.0     87.2     66.0       50.0
17     18     66.0     87.2     66.0       50.0
18     19     66.0     87.2     66.0       50.0 

'trial' 
     trial
0       1
1       2
2       3
3       4
4       5
5       6
6       7
7       8
8       9
9      10
10     11
11     12
12     13
13     14
14     15
15     16
16     17
17     18
18     19 

Deleted 'trial' column from recall DataFrame:
     mr.a  mr.b  mr.c  mr.d
0      32.4     84.6     11.7        8.2
1      14.3     74.9     43.7        9.3
2      66.1     64.9     24.5        6.7
3      15.3     53.6     11.3        2.5
4      85.0     34.4     61.4        4.9
5      18.1     75.5     73.8        1.8
6      78.5     45.2     83.2        3.7
7      21.0     85.5     13.4        2.9
8      24.2     96.1     83.9        9.7
9      28.5     87.2     85.2        8.2
10     83.0     87.2     85.2        8.2
11     83.0     87.2     85.2       50.0
12     83.0     87.2     85.2       50.0
13     83.0     87.2     85.2       50.0
14     83.0     87.2     66.0       50.0
15     66.0     87.2     66.0       50.0
16     66.0     87.2     66.0       50.0
17     66.0     87.2     66.0       50.0
18     66.0     87.2     66.0       50.0 

Rank : recall
     mr.a  mr.b  mr.c  mr.d
0       2.0      1.0      3.0        4.0
1       3.0      1.0      2.0        4.0
2       1.0      2.0      3.0        4.0
3       2.0      1.0      3.0        4.0
4       1.0      3.0      2.0        4.0
5       3.0      1.0      2.0        4.0
6       2.0      3.0      1.0        4.0
7       2.0      1.0      3.0        4.0
8       3.0      1.0      2.0        4.0
9       3.0      1.0      2.0        4.0
10      3.0      1.0      2.0        4.0
11      3.0      1.0      2.0        4.0
12      3.0      1.0      2.0        4.0
13      3.0      1.0      2.0        4.0
14      2.0      1.0      3.0        4.0
15      2.5      1.0      2.5        4.0
16      2.5      1.0      2.5        4.0
17      2.5      1.0      2.5        4.0
18      2.5      1.0      2.5        4.0 

'trial' added Rank : recall
     trial  mr.a  mr.b  mr.c  mr.d
0       1      2.0      1.0      3.0        4.0
1       2      3.0      1.0      2.0        4.0
2       3      1.0      2.0      3.0        4.0
3       4      2.0      1.0      3.0        4.0
4       5      1.0      3.0      2.0        4.0
5       6      3.0      1.0      2.0        4.0
6       7      2.0      3.0      1.0        4.0
7       8      2.0      1.0      3.0        4.0
8       9      3.0      1.0      2.0        4.0
9      10      3.0      1.0      2.0        4.0
10     11      3.0      1.0      2.0        4.0
11     12      3.0      1.0      2.0        4.0
12     13      3.0      1.0      2.0        4.0
13     14      3.0      1.0      2.0        4.0
14     15      2.0      1.0      3.0        4.0
15     16      2.5      1.0      2.5        4.0
16     17      2.5      1.0      2.5        4.0
17     18      2.5      1.0      2.5        4.0
18     19      2.5      1.0      2.5        4.0
Saved /home/kei/go/echo/pub/data/rank_recall.csv .

--- Rank : f1 ---

Read metrix 'f1' file: 
     trial  mr.a  mr.b  mr.c  mr.d
0       1    52.40     84.6    11.70       6.50
1       2    34.30     64.9    23.70       3.70
2       3    36.10     44.9    34.50       8.90
3       4    25.30     34.6    61.30      90.20
4       5    15.00     46.4    91.40      30.40
5       6    48.10     59.5    13.80      25.60
6       7    78.50     65.2    43.20      67.30
7       8    21.00     75.5    53.40      78.10
8       9    14.20     86.1    83.90      45.40
9      10    28.50     97.2    75.20      61.80
10     11    83.33     97.2    75.20      61.80
11     12    83.33     97.2    75.20      40.00
12     13    83.33     97.2    75.20      46.15
13     14    83.33     97.2    75.20      37.50
14     15    83.33     97.2    57.14      37.50
15     16    61.54     97.2    57.14      37.50
16     17    61.54     97.2    57.14      40.00
17     18    61.54     97.2    57.14      46.15
18     19    42.11     97.2    57.14      46.15 

'trial' 
     trial
0       1
1       2
2       3
3       4
4       5
5       6
6       7
7       8
8       9
9      10
10     11
11     12
12     13
13     14
14     15
15     16
16     17
17     18
18     19 

Deleted 'trial' column from f1 DataFrame:
     mr.a  mr.b  mr.c  mr.d
0     52.40     84.6    11.70       6.50
1     34.30     64.9    23.70       3.70
2     36.10     44.9    34.50       8.90
3     25.30     34.6    61.30      90.20
4     15.00     46.4    91.40      30.40
5     48.10     59.5    13.80      25.60
6     78.50     65.2    43.20      67.30
7     21.00     75.5    53.40      78.10
8     14.20     86.1    83.90      45.40
9     28.50     97.2    75.20      61.80
10    83.33     97.2    75.20      61.80
11    83.33     97.2    75.20      40.00
12    83.33     97.2    75.20      46.15
13    83.33     97.2    75.20      37.50
14    83.33     97.2    57.14      37.50
15    61.54     97.2    57.14      37.50
16    61.54     97.2    57.14      40.00
17    61.54     97.2    57.14      46.15
18    42.11     97.2    57.14      46.15 

Rank : f1
     mr.a  mr.b  mr.c  mr.d
0       2.0      1.0      3.0        4.0
1       2.0      1.0      3.0        4.0
2       2.0      1.0      3.0        4.0
3       4.0      3.0      2.0        1.0
4       4.0      2.0      1.0        3.0
5       2.0      1.0      4.0        3.0
6       1.0      3.0      4.0        2.0
7       4.0      2.0      3.0        1.0
8       4.0      1.0      2.0        3.0
9       4.0      1.0      2.0        3.0
10      2.0      1.0      3.0        4.0
11      2.0      1.0      3.0        4.0
12      2.0      1.0      3.0        4.0
13      2.0      1.0      3.0        4.0
14      2.0      1.0      3.0        4.0
15      2.0      1.0      3.0        4.0
16      2.0      1.0      3.0        4.0
17      2.0      1.0      3.0        4.0
18      4.0      1.0      2.0        3.0 

'trial' added Rank : f1
     trial  mr.a  mr.b  mr.c  mr.d
0       1      2.0      1.0      3.0        4.0
1       2      2.0      1.0      3.0        4.0
2       3      2.0      1.0      3.0        4.0
3       4      4.0      3.0      2.0        1.0
4       5      4.0      2.0      1.0        3.0
5       6      2.0      1.0      4.0        3.0
6       7      1.0      3.0      4.0        2.0
7       8      4.0      2.0      3.0        1.0
8       9      4.0      1.0      2.0        3.0
9      10      4.0      1.0      2.0        3.0
10     11      2.0      1.0      3.0        4.0
11     12      2.0      1.0      3.0        4.0
12     13      2.0      1.0      3.0        4.0
13     14      2.0      1.0      3.0        4.0
14     15      2.0      1.0      3.0        4.0
15     16      2.0      1.0      3.0        4.0
16     17      2.0      1.0      3.0        4.0
17     18      2.0      1.0      3.0        4.0
18     19      4.0      1.0      2.0        3.0
Saved /home/kei/go/echo/pub/data/rank_f1.csv .

Done! /home/kei/go/echo/score.py
```

# 2. GitLab

## 2.1. .git > config

```bash
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
[remote "origin"]
#	url = http://abcd.com/gitlab/deviceai/qc_ai_project.git
	url = http://mr.d:TjBQVrMRneoRRRxSuHno@abcd.com/gitlab/deviceai/qc_ai_project.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
	remote = origin
	merge = refs/heads/master
[branch "submit"]
	remote = origin
	merge = refs/heads/submit
```

- `GitLab`のリポジトリ接続`URL`にトークンが必要なため、ユーザー`kei`にも、ユーザー`mr.d`と、トークンを付加する

# 3. 実行ファイル、CSVデータファイルの配置（Ubuntu16.04LTS）

- `Jenkins`のビルドやSCMポーリングを実施する前に、以下のファイルが配置されていること

## 3.1.  実行ファイル

- 採点ファイル
  - `/home/kei/go/echo/score.py`
- 採点ファイルが呼び出すモジュール・ファイル
  - `/home/kei/go/echo/update_metrix.py`
- ![echo-tree](./images/echo-tree.jpg)

## 3.2. サブミッション・ファイル submission_name.csv

- `Jenkins`が、ビルド＞シェルの実行において、`GitLab`からプルしたファイルを以下にコピーする
  - `/home/kei/go/echo/submissions/submission_mr.a.csv`
  - `/home/kei/go/echo/submissions/submission_mr.c.csv`
  - `/home/kei/go/echo/submissions/submission_mr.b.csv`
  - `/home/kei/go/echo/submissions/submission_mr.d.csv`

## 3.3. CSVファイル

- Metrix
  - 各種混合行列の指標、過去の結果を保持
    - `/home/kei/go/echo/pub/data/accuracy.csv`
    - `/home/kei/go/echo/pub/data/precision.csv`
    - `/home/kei/go/echo/pub/data/recall.csv`
    - `/home/kei/go/echo/pub/data/f1.csv`

- Rank
  - 正解率をもとにした順位、過去の結果を保持
    - `/home/kei/go/echo/pub/data/rank_accuracy.csv`
  - 以下のファイルは他の指標をもとに順位付けをする場合に使用する
    - `/home/kei/go/echo/pub/data/rank_precision.csv`
    - `/home/kei/go/echo/pub/data/rank_recall.csv`
    - `/home/kei/go/echo/pub/data/rank_f1.csv`

- Score
  - サブミッショナーの採点結果、最新の結果のみ保持し、古いファイルは`Jenkins`が削除する
    - `/home/kei/go/echo/pub/data/score_mr.a_2020-09-28_17-00-13.csv`
    - `/home/kei/go/echo/pub/data/score_mr.c_2020-09-28_15-39-49.csv`
    - `/home/kei/go/echo/pub/data/score_mr.b_2020-09-29_16-01-28.csv`
    - `/home/kei/go/echo/pub/data/score_mr.d_2020-09-29_12-00-58.csv`

- その他
  - 正解ファイル
    - `/home/kei/go/echo/pub/data/test.csv`

  - `submission`ファイルと、正解ファイル（`test.csv`）を結合したファイル
    - `/home/kei/go/echo/pub/data/combined.csv`
  
## 3.3. Echo

- `Go`言語で記述されたWebサーバー
- `Ubuntu`上で稼働
- server.go


# 4. 採点結果グラフ表示ページ

- `URL`アドレスは、http://xxx.xxx.xxx.xxx:1323/confusion.html
- 記述言語は、`HTML`と`JavaScript`、および`Google Chart`

## 4.1. HTML

- ファイル名は、`confusion.html`
- ファイルの位置は、`/home/kei/go/echo/pub`
- `GitLab`のローカルリポジトリ上では、`C:\gitlab\qc_ai_project\src\go\pub`

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>順位と混合行列をグラフ化</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- AJAX API のロード -->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
        // Visualization API と折れ線グラフ用のパッケージのロード
        google.charts.load('current', {'packages':['corechart']});
    
        // Google Visualization API ロード時のコールバック関数の設定
        google.charts.setOnLoadCallback(drawChart_rank);
        google.charts.setOnLoadCallback(drawChart_accuracy);
        google.charts.setOnLoadCallback(drawChart_precision);
        google.charts.setOnLoadCallback(drawChart_recall);
        google.charts.setOnLoadCallback(drawChart_f1);

        var ma_rank = new Array();
        var ma_acc = new Array();
        var ma_pre = new Array();
        var ma_rec = new Array();
        var ma_f1 = new Array();
        var data = new Array();
        var res = new Array();

        // 1) CSVファイルを読み込む. onload 時実行
        function getValue(){
            /*-- 順位 -------------------------------------------------------------------------------------------- */
            var fname = 'data/rank_accuracy.csv';   // 正解率による順位
            console.log(fname);

            // 2) 該当 csvファイルから chartデータに変換
            ma_rank = getCsv(fname);
            console.log(ma_f1);

            /*-- 正解率 -------------------------------------------------------------------------------------------- */
            var fname = 'data/accuracy.csv';
            console.log(fname);

            // 2) 該当 csvファイルから chartデータに変換
            ma_acc = getCsv(fname);
            console.log(ma_acc);

            /*-- 適合率 -------------------------------------------------------------------------------------------- */
            var fname = 'data/precision.csv';
            console.log(fname);

            // 2) 該当 csvファイルから chartデータに変換
            ma_pre = getCsv(fname);
            console.log(ma_pre);

            /*-- 再現率 -------------------------------------------------------------------------------------------- */
            var fname = 'data/recall.csv';
            console.log(fname);

            // 2) 該当 csvファイルから chartデータに変換
            ma_rec = getCsv(fname);
            console.log(ma_rec);

            /*-- F1 ----------------------------------------------------------------------------------------------- */
            var fname = 'data/f1.csv';
            console.log(fname);

            // 2) 該当 csvファイルから chartデータに変換
            ma_f1 = getCsv(fname);
            console.log(ma_f1);

        };
  
        // 2) csvファイルをchartデータに整形
        function getCsv(url){
            var req = new XMLHttpRequest();         // HTTPでファイルを読み込むためのXMLHttpRrequestオブジェクトを生成
            req.open('get', url, false);            // アクセスするファイルを指定
            req.send(null);                         // HTTPリクエストの発行

            // 改行ごとに配列化
            var arr = req.responseText.split('\n');

            // 1次元配列を2次元配列に変換
            res = [];
            res[0] = arr[0].split(',');
            for(var i = 1; i < arr.length; i++){
                // 空白行が出てきた時点で終了
                if(arr[i] == '') break;
                // ","ごとに配列化
                res[i] = arr[i].split(',');
                for(var i2 = 1; i2 < res[i].length; i2++){
                    // 数字の場合は「' "」を削除 ･･･ 2列目以降に適用
                    if(res[i][i2].match(/\-?\d+(.\d+)?(e[\+\-]d+)?/)){
                        res[i][i2] = parseFloat(res[i][i2].replace(/'?"?/g, ""));
                    }
                }
            }
            return res;
        }

        // google.chartsでグラフを表示
        // 3) ma_rank 順位
        function drawChart_rank() {
            // データテーブルの作成
            data = google.visualization.arrayToDataTable( ma_rank );

            // グラフのオプションを設定
            var options = {
                title : '順位（正解率）',
                titleTextStyle : { color: '#333', fontSize: 20 },
                vAxis: {
                    title: '順位',
                    direction: -1,
                    minValue: 1,
                    maxValue: 3,
                    ticks: [1,2,3],
                    viewWindow: {
                        min: 1
                    }
                },
                hAxis: {title: ma_rank[0][0]},
                seriesType: 'line',             // 全体は棒グラフ(default='line')
                legendTextStyle : { color: '#333', fontSize: 12 },
            };
            // 折れ線グラフ： LineChart のオブジェクトの作成
            var chart = new google.visualization.LineChart(document.getElementById('chart_rank'));
            // // データテーブルとオプションを渡してグラフを描画
            chart.draw(data, options);
        };

        // 3) ma_acc 正解率
        function drawChart_accuracy() {
            // データテーブルの作成
            data = google.visualization.arrayToDataTable( ma_acc );

            // グラフのオプションを設定
            var options = {
                title : '正解率 Accuracy',
                titleTextStyle : { color: '#333', fontSize: 20 },
                vAxis: {title: '正解率 [%]'},
                hAxis: {title: ma_acc[0][0]},
                seriesType: 'line',             // 全体は棒グラフ(default='line')
                legendTextStyle : { color: '#333', fontSize: 12 },
            };
            // 折れ線グラフ： LineChart のオブジェクトの作成
            var chart = new google.visualization.LineChart(document.getElementById('chart_accuracy'));
            // // データテーブルとオプションを渡してグラフを描画
            chart.draw(data, options);
        };

        // 3) ma_pre 適合率
        function drawChart_precision() {
            // データテーブルの作成
            data = google.visualization.arrayToDataTable( ma_pre );

            // グラフのオプションを設定
            var options = {
                title : '適合率 Precision',
                titleTextStyle : { color: '#333', fontSize: 20 },
                vAxis: {title: '適合率 [%]'},
                hAxis: {title: ma_pre[0][0]},
                seriesType: 'line',             // 全体は棒グラフ(default='line')
                legendTextStyle : { color: '#333', fontSize: 12 },
            };
            // 折れ線グラフ： LineChart のオブジェクトの作成
            var chart = new google.visualization.LineChart(document.getElementById('chart_precision'));
            // // データテーブルとオプションを渡してグラフを描画
            chart.draw(data, options);
        };

        // 3) ma_rec 再現率
        function drawChart_recall() {
            // データテーブルの作成
            data = google.visualization.arrayToDataTable( ma_rec );

            // グラフのオプションを設定
            var options = {
                title : '再現率 Recall',
                titleTextStyle : { color: '#333', fontSize: 20 },
                vAxis: {title: '再現率 [%]'},
                hAxis: {title: ma_rec[0][0]},
                seriesType: 'line',             // 全体は棒グラフ(default='line')
                legendTextStyle : { color: '#333', fontSize: 12 },
            };
            // 折れ線グラフ： LineChart のオブジェクトの作成
            var chart = new google.visualization.LineChart(document.getElementById('chart_recall'));
            // // データテーブルとオプションを渡してグラフを描画
            chart.draw(data, options);
        };

        // 3) ma_f1 F1
        function drawChart_f1() {
            // データテーブルの作成
            data = google.visualization.arrayToDataTable( ma_f1 );

            // グラフのオプションを設定
            var options = {
                title : 'F1',
                titleTextStyle : { color: '#333', fontSize: 20 },
                vAxis: {title: 'F1 [%]'},
                hAxis: {title: ma_f1[0][0]},
                seriesType: 'line',             // 全体は棒グラフ(default='line')
                legendTextStyle : { color: '#333', fontSize: 12 },
            };
            // 折れ線グラフ： LineChart のオブジェクトの作成
            var chart = new google.visualization.LineChart(document.getElementById('chart_f1'));
            // // データテーブルとオプションを渡してグラフを描画
            chart.draw(data, options);
        };

</script>

</head>
<body onload="getValue();">
    <!-- グラフを描く div 要素 -->
    <div class="waku1">
        <h3>正解率による順位と混合行列</h3>
        <div id="chart_rank" style="width: 100%; height: 350px"></div>
        <div id="chart_accuracy" style="width: 100%; height: 350px"></div>
        <div id="chart_precision" style="width: 100%; height: 350px"></div>
        <div id="chart_recall" style="width: 100%; height: 350px"></div>
        <div id="chart_f1" style="width: 100%; height: 350px"></div>
    </div>
</body>
</html>
```

## 4.2. JavaScript

- ファイルは、`confusion.html`の中の`<script type="text/javascript"></script>`タグの中に記述
