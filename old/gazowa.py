#!/usr/bin/env python3
#coding:utf-8
# pip install Pillow

# アップデート日 : 2019/11/24
# Interfaceから削除をPictureに移してメソッド化
# コンストラクタで画像をロードする
# つまりPictureクラスのインスタンス作成=画像のインスタンスにする

# 追記 : gtkがpipからインストール出来ないためパッケージからのインストールが必要
# apt install ./python-gtk2_2.24.0-5.1ubuntu2_amd64.deb

import WxInterface
import pygtk
import subprocess

# 3つ以上の起動を防止する
cmd = "ps ax | grep 'gazowa_v2.py'"
script_name = 'python gazowa.py'
ret = subprocess.check_output( cmd , shell=True)
number = ret.count( script_name ) - 2
if( number >= 3 ):
    sys.exit()

WxInterface.WxInterface()
gtk.main()
