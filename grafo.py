
import math
from dijkstra import dijkstra

class Grafo:
    def __init__(self, dados):
        n_header = dados["num_vertices"]
        self.n = n_header
        # Garante que o número de vértices seja o maior índice encontrado
        max_node_in_conns = 0
        if dados["conexoes"]:
            max_node_in_conns = max(max(u, v) for u, v, _, _ in dados["conexoes"])
        
        self.n = max(self.n, max_node_in_conns)
        
        self.adj = {} # Usaremos um dicionário para a lista de adjacência
        for u, v, custo, tipo in dados["conexoes"]:
            if u not in self.adj: self.adj[u] = []
            if v not in self.adj: self.adj[v] = []
            
            self.adj[u].append((v, custo))
            # Para arestas não direcionadas (NE e E), adicionamos o caminho de volta
            if tipo in ("NE", "E"):
                self.adj[v].append((u, custo))
        
        # Cache para armazenar os resultados do Dijkstra
        self.cache_distancias = {}

    def obter_distancias(self, no_origem):
        """
        Retorna um dicionário com as distâncias de 'no_origem' para todos os outros.
        Usa o cache para evitar recalcular.
        """
        if no_origem in self.cache_distancias:
            return self.cache_distancias[no_origem]
        
        # Se não está no cache, calcula com Dijkstra e armazena
        distancias = dijkstra(self.n, self.adj, no_origem)
        self.cache_distancias[no_origem] = distancias
        return distancias

def calcular_custo_rota(sequencia_servicos, grafo, deposito):
    """
    Calcula o custo de uma rota usando o objeto grafo para obter as distâncias.
    """
    if not sequencia_servicos:
        return 0.0

    custo_total = 0.0
    pos_atual = deposito

    for servico in sequencia_servicos:
        _, p1, p2, _, s_custo, t_custo = servico
        
        distancias_do_ponto_atual = grafo.obter_distancias(pos_atual)
        custo_viagem = distancias_do_ponto_atual.get(p1, math.inf)

        if custo_viagem == math.inf: return math.inf

        custo_total += custo_viagem
        custo_total += t_custo
        custo_total += s_custo
        pos_atual = p2

    distancias_finais = grafo.obter_distancias(pos_atual)
    custo_volta = distancias_finais.get(deposito, math.inf)

    if custo_volta == math.inf: return math.inf

    custo_total += custo_volta
    return custo_total