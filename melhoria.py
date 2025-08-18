import math
import time
from grafo import calcular_custo_rota

def aprimorar_solucao_vns(rotas_info, dados, grafo, start_time_global, max_time_global_seconds):
    """
    Solução completa usando uma abordagem parecida com VNS, com controle de tempo.
    """
    while True:
        # Critério de parada global por tempo
        if time.time() - start_time_global > max_time_global_seconds:
            break

        custo_antes_iteracao = sum(r['custo'] for r in rotas_info)
        
        # Passa o controle de tempo para as funções de busca
        if find_best_relocate(rotas_info, dados, grafo, start_time_global, max_time_global_seconds):
            continue

        if time.time() - start_time_global > max_time_global_seconds: break
        if find_best_swap(rotas_info, dados, grafo, start_time_global, max_time_global_seconds):
            continue

        if time.time() - start_time_global > max_time_global_seconds: break
        if find_best_2opt(rotas_info, dados, grafo, start_time_global, max_time_global_seconds):
            continue
        
        # Se nenhum movimento melhorou, para.
        if sum(r['custo'] for r in rotas_info) >= custo_antes_iteracao:
            break

def find_best_relocate(rotas_info, dados, grafo, start_time, max_time):
    """ Tenta encontrar o melhor movimento de realocação e o aplica. """
    deposito = dados["deposito"]
    capacidade = dados["capacidade"]
    melhor_ganho = 0
    melhor_movimento = None

    for r1_idx, rota1 in enumerate(rotas_info):
        # Verificação de tempo no laço externo
        if time.time() - start_time > max_time: return False

        for s1_idx in range(len(rota1["servicos"])):
            servico_para_mover = rota1["servicos"][s1_idx]
            
            for r2_idx, rota2 in enumerate(rotas_info):
                if r1_idx == r2_idx: continue

                # Verifica se a capacidade da rota de destino permite a realocação
                if rota2["demanda"] + servico_para_mover[3] > capacidade:
                    continue

                custo_original = rota1["custo"] + rota2["custo"]
                
                # Cria uma cópia temporária da rota de origem sem o serviço
                rota1_temp = rota1["servicos"][:s1_idx] + rota1["servicos"][s1_idx+1:]
                custo1_novo = calcular_custo_rota(rota1_temp, grafo, deposito)

                # Tenta inserir o serviço em todas as posições da rota de destino
                for s2_idx in range(len(rota2["servicos"]) + 1):
                    rota2_temp = rota2["servicos"][:s2_idx] + [servico_para_mover] + rota2["servicos"][s2_idx:]
                    custo2_novo = calcular_custo_rota(rota2_temp, grafo, deposito)
                    
                    custo_novo_total = custo1_novo + custo2_novo
                    ganho = custo_original - custo_novo_total

                    if ganho > melhor_ganho:
                        melhor_ganho = ganho
                        melhor_movimento = (r1_idx, s1_idx, r2_idx, s2_idx)
    
    if melhor_movimento:
        r1_idx, s1_idx, r2_idx, s2_idx = melhor_movimento
        
        servico_movido = rotas_info[r1_idx]["servicos"].pop(s1_idx)
        rotas_info[r2_idx]["servicos"].insert(s2_idx, servico_movido)
        
        # Atualiza informações das rotas modificadas
        for idx in [r1_idx, r2_idx]:
            rotas_info[idx]["custo"] = calcular_custo_rota(rotas_info[idx]["servicos"], grafo, deposito)
            rotas_info[idx]["demanda"] = sum(s[3] for s in rotas_info[idx]["servicos"])
            rotas_info[idx]["servicos_str"] = [f"(S {s[0]},{s[1]},{s[2]})" for s in rotas_info[idx]["servicos"]]

        return True # Indica que uma melhoria foi feita
    return False


def find_best_swap(rotas_info, dados, grafo, start_time, max_time):
    """ Tenta encontrar o melhor movimento de troca entre duas rotas e o aplica. """
    deposito = dados["deposito"]
    capacidade = dados["capacidade"]
    melhor_ganho = 0
    melhor_movimento = None

    for r1_idx in range(len(rotas_info)):
        # Verificação de tempo no laço externo
        if time.time() - start_time > max_time: return False

        for r2_idx in range(r1_idx + 1, len(rotas_info)):
            rota1 = rotas_info[r1_idx]
            rota2 = rotas_info[r2_idx]
            
            for s1_idx, servico1 in enumerate(rota1["servicos"]):
                for s2_idx, servico2 in enumerate(rota2["servicos"]):
                    
                    # Verifica viabilidade da capacidade
                    if (rota1["demanda"] - servico1[3] + servico2[3] > capacidade) or \
                       (rota2["demanda"] - servico2[3] + servico1[3] > capacidade):
                        continue

                    custo_original = rota1["custo"] + rota2["custo"]
                    
                    # Cria rotas temporárias com a troca
                    rota1_temp_servicos = rota1["servicos"][:s1_idx] + [servico2] + rota1["servicos"][s1_idx+1:]
                    rota2_temp_servicos = rota2["servicos"][:s2_idx] + [servico1] + rota2["servicos"][s2_idx+1:]

                    custo_novo_total = calcular_custo_rota(rota1_temp_servicos, grafo, deposito) + \
                                       calcular_custo_rota(rota2_temp_servicos, grafo, deposito)

                    ganho = custo_original - custo_novo_total
                    if ganho > melhor_ganho:
                        melhor_ganho = ganho
                        melhor_movimento = (r1_idx, s1_idx, r2_idx, s2_idx)

    if melhor_movimento:
        r1_idx, s1_idx, r2_idx, s2_idx = melhor_movimento
        
        # Realiza a troca
        servico1 = rotas_info[r1_idx]["servicos"][s1_idx]
        servico2 = rotas_info[r2_idx]["servicos"][s2_idx]
        rotas_info[r1_idx]["servicos"][s1_idx] = servico2
        rotas_info[r2_idx]["servicos"][s2_idx] = servico1

        # Atualiza informações das rotas modificadas
        for idx in [r1_idx, r2_idx]:
            rotas_info[idx]["custo"] = calcular_custo_rota(rotas_info[idx]["servicos"], grafo, deposito)
            rotas_info[idx]["demanda"] = sum(s[3] for s in rotas_info[idx]["servicos"])
            rotas_info[idx]["servicos_str"] = [f"(S {s[0]},{s[1]},{s[2]})" for s in rotas_info[idx]["servicos"]]
            
        return True
    return False

def find_best_2opt(rotas_info, dados, grafo, start_time, max_time):
    """ Aplica a melhoria 2-Opt intra-rota. """
    deposito = dados["deposito"]
    houve_melhoria_geral = False

    for rota in rotas_info:
        # Verificação de tempo no laço externo
        if time.time() - start_time > max_time: return False

        if len(rota["servicos"]) < 2: continue
        
        custo_inicial_rota = rota["custo"]
        
        melhoria_na_rota = True
        while melhoria_na_rota:
            melhoria_na_rota = False
            custo_atual = calcular_custo_rota(rota["servicos"], grafo, deposito)
            
            for j in range(len(rota["servicos"]) - 1):
                for k in range(j + 1, len(rota["servicos"])):
                    nova_sequencia = rota["servicos"][:j] + rota["servicos"][j:k+1][::-1] + rota["servicos"][k+1:]
                    novo_custo = calcular_custo_rota(nova_sequencia, grafo, deposito)
                    if novo_custo < custo_atual:
                        rota["servicos"] = nova_sequencia
                        custo_atual = novo_custo
                        melhoria_na_rota = True
                        break
                if melhoria_na_rota: break
        
        rota["custo"] = calcular_custo_rota(rota["servicos"], grafo, deposito)
        rota["servicos_str"] = [f"(S {s[0]},{s[1]},{s[2]})" for s in rota["servicos"]]
        if rota["custo"] < custo_inicial_rota:
            houve_melhoria_geral = True
            
    return houve_melhoria_geral