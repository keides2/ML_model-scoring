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
# origin/hayashi_0721_baseline_rpm
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

# Echoへコピー
#echo "Echoへコピー"
#cp ./src/go/pub/data/rank_accuracy.csv /home/kei/go/echo/pub/data/
#cp ./src/go/pub/data/accuracy.csv /home/kei/go/echo/pub/data/
#cp ./src/go/pub/data/precision.csv /home/kei/go/echo/pub/data/
#cp ./src/go/pub/data/recall.csv /home/kei/go/echo/pub/data/
#cp ./src/go/pub/data/f1.csv /home/kei/go/echo/pub/data/

echo "Done!"