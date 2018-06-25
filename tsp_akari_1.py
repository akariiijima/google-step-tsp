import sys
import math
import random

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour

def score(tour,input_): #順路距離計算
    score = 0
    for i in range(len(tour)-1):
        score = score + math.sqrt((input_[tour[i]][0] - input_[tour[i+1]][0])*(input_[tour[i]][0] - input_[tour[i+1]][0]) + (input_[tour[i]][1] - input_[tour[i+1]][1])*(input_[tour[i]][1] - input_[tour[i+1]][1]))
    score = score + math.sqrt((input_[tour[0]][0] - input_[tour[len(tour)-1]][0])*(input_[tour[0]][0] - input_[tour[len(tour)-1]][0]) + (input_[tour[0]][1] - input_[tour[len(tour)-1]][1])*(input_[tour[0]][1] - input_[tour[len(tour)-1]][1]))
    return score

def simulated_annealing(tour,greedy_score,len_tour,input_): #焼きなまし法
    index = 0
    optimisation_tour = tour
    minimum_score = greedy_score
    swap_pair = set() #乱数の一致を防ぐ
    while(index < 100000): #100000回繰り返し
        pair_match = 0 #乱数が一致した場合の真偽
        while(True):
            swap_1 = int(random.uniform(0, len_tour)) #乱数1を発生させる
            swap_2 = int(random.uniform(0, len_tour)) #乱数2を発生させる
            if swap_1 != swap_2:
                break
        swap_1, swap_2 = min(swap_1,swap_2), max(swap_1,swap_2) #常にswap_1<swap_2となるようにしておく
        if (swap_1,swap_2) not in swap_pair: #乱数ペアが1度も出現しなかったら
            swap_pair.add((swap_1,swap_2))      
        
            tour[swap_1],tour[swap_2] = tour[swap_2],tour[swap_1] #tourの中身を交換
            if score(tour,input_) < minimum_score: #もし交換したindexの順路が最短だと
                minimum_score = score(tour,input_) #スコアを更新
                optimisation_tour = tour #tourを更新
            else:
                tour[swap_1],tour[swap_2] = tour[swap_1],tour[swap_2] #元のtourのならびに戻す
            index = index + 1
        else:
            index = index + 1
            continue

    print(swap_pair)
    return optimisation_tour, minimum_score
    
        

assert len(sys.argv) > 1
tour = solve(read_input(sys.argv[1]))
input_csv = read_input(sys.argv[1])
#print(input_csv)
#print(score(tour,input_csv))
(optimisation_tour, minimum_score) = simulated_annealing(tour,score(tour,input_csv),len(tour),input_csv)

print(minimum_score)
print(len(tour))
