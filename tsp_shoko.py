# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
import math

#from common import print_path, read_input

def read_input(filename):#各都市のx,yを読み込む関数
    with open(filename) as f:
        cities = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1])))
        return cities
#cities[(x0,y0),(x1,y1),・・・（）]

def distance(city1, city2):#2点間の都市の距離を計算する関数
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def distance_dic(cities):#全都市の距離を計算して多次元配列に入れる関数
    N = len(cities) #Nは都市の数
    dist = [[0] * N for i in range(N)] #各都市間の経路を保存する配列を定義
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j]) #関数distanceを使って各都市間の経路を算出
    return dist,N

def path_length(path,dist):#入力：ある都市の回り方の組み合わせと、各都市間の距離格納した多次元リスト
                            #出力：ある経路の合計距離
    d= 0
    for i in range(1, len(path)):
        d+= dist[path[i - 1]][path[i]]
    d+= dist[path[0]][path[-1]]
    return d

#N = len(cities)のじゅず順列の考え方、深さ優先探索
#ただし、cities[0]のcityを基準とし、最後のcityを2番目のcityと重複避ける大小比較するために
# 配列[0]にもってくる
#[最後の都市、基準の都市、二番目の都市、・・・]
#pathはあらゆる経路の順列格納する配列、#Nは最終的に並べたい全部の都市の数、nは選択した並べる数、combiは順列を格納する配列
def dfs(N,dist):
    def dfs_sub(n, path, dist):
        global min_length, min_path#再帰するので関数内でmin_length,min_path更新できるように
        if N == n:
            new_len = path_length(path,dist)
            if new_len < min_length:
                min_length = new_len
                min_path = path[:]
        else:
            for x in range(1, N):
                if x not in path:
                    if n != 2 or path[0] > x:#n=2では最後のcityと2番目のcityの大小比較、n!=2では普通に追加
                        path.append(x)
                        dfs_sub(n + 1, path,dist)#4番目以外の順列は再帰で決まる
                        path.pop()

    global min_length, min_path
    min_length = 1e100
    min_path = []
    for x in range(1, N):
        dfs_sub(2, [x, 0],dist)#xが最後のcity,0がスタートとゴールの基準のcity
    return min_length, min_path


#出力
def format_path(path):
    return 'index\n' + '\n'.join(map(str, path))



def print_path(path):
    print(format_path(path))


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities=read_input(sys.argv[1])
    dist, N = distance_dic(cities)
    min_length, min_path= dfs(N,dist)
    print_path(min_path)    #tourはインデックスの順が入ったリスト




input_0 = read_input("input_0.csv")
print(input_0)
