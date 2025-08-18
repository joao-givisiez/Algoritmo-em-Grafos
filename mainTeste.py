import os
import time
from leitura import ler_instancia_completa
from construtivo import gerar_solucao_viavel
from melhoria import aprimorar_solucao_2opt

def main():
    # Altere o nome do arquivo aqui para testar a instância desejada
    inst = "mgval_0.25_5C.dat" 

    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "Ins", inst)

    if not os.path.exists(path):
        print(f"ERRO: Arquivo de instância não encontrado em '{path}'")
        return

    print(f"--- Resolvendo instância: {inst} ---")
    dados = ler_instancia_completa(path)

    t_inicio = time.time()

    print("1. Gerando solução construtiva inicial...")
    
    rotas_info, grafo_obj = gerar_solucao_viavel(dados)
    custo_inicial = sum(r["custo"] for r in rotas_info)
    print(f"   -> Custo inicial: {int(round(custo_inicial))}, Rotas: {len(rotas_info)}")

    print("\n2. Aprimorando solução com 2-Opt...")
    
    aprimorar_solucao_2opt(rotas_info, dados, grafo_obj)

    t_fim = time.time()
    tempo_total_secs = t_fim - t_inicio
    
    custo_final = sum(r["custo"] for r in rotas_info)

    print("\n--- Resultado Final ---")
    print(f"Custo Inicial:      {int(round(custo_inicial))}")
    print(f"Custo Final (após 2-Opt): {int(round(custo_final))}")
    print(f"Número de Rotas:    {len(rotas_info)}")
    print(f"Tempo de Execução:  {tempo_total_secs:.4f} segundos")
    print("-----------------------\n")

if __name__ == "__main__":
    main()