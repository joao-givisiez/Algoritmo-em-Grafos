import os
import time
import sys
from leitura import ler_instancia_completa
from construtivo import gerar_solucao_viavel
from melhoria import aprimorar_solucao_vns

def escrever_solucao_formato(nome_arquivo, rotas_info, custo_total, clocks_heuristica_secs):
    """
    Escreve a solução no formato sol- nomeInstacia.dat
    """
    clocks_heuristica = int(round(clocks_heuristica_secs * 1_000_000))
    clocks_referencia = clocks_heuristica

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"{int(round(custo_total))}\n")
        f.write(f"{len(rotas_info)}\n")
        f.write(f"{clocks_heuristica}\n")
        f.write(f"{clocks_referencia}\n")

        route_id = 1
        for rota in rotas_info:
            servicos_str = rota["servicos_str"]
            custo_rota = rota["custo"]
            demanda_rota = rota["demanda"]
            total_visits = len(servicos_str) + 2

            f.write(f"0 1 {route_id} {demanda_rota} {int(round(custo_rota))} {total_visits} ")
            f.write("(D 0,1,1) ")
            f.write(" ".join(servicos_str))
            f.write(" (D 0,1,1)\n")
            route_id += 1

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_ins = os.path.join(base_dir, "Ins")
    pasta_saida = os.path.join(base_dir, "SolucoesFinais")

    if not os.path.exists(pasta_ins):
        print(f"ERRO: Pasta 'Ins' não encontrada em {pasta_ins}")
        return
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    arquivos = sorted([f for f in os.listdir(pasta_ins) if f.endswith(".dat")])
    if not arquivos:
        print(f"ERRO: Nenhum arquivo .dat encontrado na pasta 'Ins'.")
        return

    total_arquivos = len(arquivos)
    print(f"Encontradas {total_arquivos} instâncias. Iniciando processamento...")
    start_time_total = time.time()

    max_tempo_segundos = 200  # Tempo máximo por instância

    for idx, fname in enumerate(arquivos):
        path = os.path.join(pasta_ins, fname)
        print(f"[{idx + 1}/{total_arquivos}] Resolvendo: {fname}...")

        # Suprimir prints internos durante o processamento
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

        try:
            dados = ler_instancia_completa(path)
            t0 = time.time()

            # Etapa 1: Construtivo
            rotas_info, grafo_obj = gerar_solucao_viavel(dados)

            # Etapa 2: Melhoria
            aprimorar_solucao_vns(rotas_info, dados, grafo_obj, t0, max_tempo_segundos)

            # Remove rotas vazias que possam ter sido geradas pelo VNS
            rotas_info = [r for r in rotas_info if r.get("servicos_str")]

            t1 = time.time()
            clocks_heuristica_secs = t1 - t0
            custo_total = sum(r["custo"] for r in rotas_info)
            saida = os.path.join(pasta_saida, f"sol-{fname}")

            # Restaurar stdout para mostrar o resumo final
            sys.stdout.close()
            sys.stdout = original_stdout

            escrever_solucao_formato(saida, rotas_info, custo_total, clocks_heuristica_secs)
            print(f"    -> Concluído. Custo={int(round(custo_total))}, Rotas={len(rotas_info)}, Tempo={clocks_heuristica_secs:.4f}s.")

        except Exception as e:
            sys.stdout.close()
            sys.stdout = original_stdout
            print(f"    ERRO FATAL ao processar '{fname}': {e}")
            import traceback
            traceback.print_exc()
            continue
            
    end_time_total = time.time()
    print(f"\n Processamento concluído em {end_time_total - start_time_total:.2f} segundos.")
    print(f"Todas as {total_arquivos} soluções foram geradas em: {pasta_saida}")

if __name__ == "__main__":
    main()