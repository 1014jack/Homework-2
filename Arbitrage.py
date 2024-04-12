liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}



from typing import Tuple, List
from math import log

def negate_logarithm_convertor(graph: Tuple[Tuple[float]]) -> List[List[float]]:
    ''' log of each rate in graph and negate it'''
    result = [[-log(edge) for edge in row] for row in graph]
    return result


def arbitrage(currency_tuple: tuple, rates_matrix: Tuple[Tuple[float, ...]]):
    ''' Calculates arbitrage situations and prints out the details of this calculations'''

    trans_graph = negate_logarithm_convertor(rates_matrix)

    # Pick any source vertex -- we can run Bellman-Ford from any vertex and get the right result

    source = 1
    n = len(trans_graph)
    min_dist = [float('inf')] * n

    pre = [-1] * n
    
    min_dist[source] = 0

    # 'Relax edges |V-1| times'
    for _ in range(n-1):
        for source_curr in range(n):
            for dest_curr in range(n):
                if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                    min_dist[dest_curr] = min_dist[source_curr] + trans_graph[source_curr][dest_curr]
                    pre[dest_curr] = source_curr

    # if we can still relax edges, then we have a negative cycle
    for source_curr in range(n):
        for dest_curr in range(n):
            if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                # negative cycle exists, and use the predecessor chain to print the cycle
                print_cycle = [dest_curr, source_curr]
                # Start from the source and go backwards until you see the source vertex again or any vertex that already exists in print_cycle array
                while pre[source_curr] not in  print_cycle:
                    print_cycle.append(pre[source_curr])
                    source_curr = pre[source_curr]
                print_cycle.append(pre[source_curr])
                # print("Arbitrage Opportunity: \n")
                # print(" --> ".join([currencies[p] for p in print_cycle[::-1]]))
                possible_paths.append([currencies[p] for p in print_cycle[::-1]])

def swap_for_exact_token(token_in, token_out, amount_in):
    if (token_in, token_out) in liquidity:
        y, x= liquidity[(token_in, token_out)]
    else:
        x, y = liquidity[(token_out, token_in)]
    return (0.997*x*amount_in)/(y + 0.997*amount_in)

currencies = ('tokenA', 'tokenB', 'tokenC', 'tokenD', 'tokenE')

rates = [[1]*len(currencies) for i in range(len(currencies))]

for i in range(len(currencies)):
    for j in range(i+1, len(currencies)):
        x, y = liquidity[(currencies[i], currencies[j])]
        rates[i][j] = y/x
        rates[j][i] = x/y
        
possible_paths = []
arbitrage(currencies, rates)

for path in possible_paths:
    curr_token = 'tokenB'
    curr_value = 5

    if path[0] == 'tokenA':
        path = ['tokenB'] + path
    elif path[0] == 'tokenC' or path[0] == 'tokenD' or path[0] == 'tokenE':
        path = ['tokenB', 'tokenA'] + path

    extended_path = ['tokenB']

    for i in range(1, len(path)):
        extended_path.append(path[i])
        if path[i] == curr_token:
            break        
        
    for i in range(len(extended_path)-1):
        curr_value = swap_for_exact_token(extended_path[i], extended_path[i+1], curr_value)
        curr_token = extended_path[i+1]
    if curr_value > 20:
        print('path:', '->'.join(extended_path), end=', ')
        print(f'{curr_token} balance={curr_value}')