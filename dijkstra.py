
import heapq
import math

def dijkstra(num_vertices, adj_list, start_node):
    """
    Executa o algoritmo de Dijkstra a partir de um nó inicial.
    'adj_list' é uma lista de adjacência onde adj[u] = [(v, custo), ...].
    Retorna um dicionário de distâncias do start_node para todos os outros.
    """
    dist = {i: math.inf for i in range(num_vertices + 1)}
    dist[start_node] = 0
    
    # Fila de prioridade armazena (distancia, no)
    pq = [(0, start_node)]

    while pq:
        d, u = heapq.heappop(pq)

        # Se já encontramos um caminho mais curto, ignoramos
        if d > dist[u]:
            continue

        # Para cada vizinho v de u
        if u in adj_list:
            for v, weight in adj_list[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    heapq.heappush(pq, (dist[v], v))
    
    return dist