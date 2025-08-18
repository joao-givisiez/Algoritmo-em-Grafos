import math
from grafo import Grafo, calcular_custo_rota

def gerar_solucao_viavel(dados):
    capacidade = dados["capacidade"]
    deposito = dados["deposito"]
    reqs = dados["requisitos"]

    g = Grafo(dados)

    servicos = []
    id_global = 1
    for s_type, s_list in [('N', reqs["nos"]), ('E', reqs["arestas"]), ('A', reqs["arcos"])]:
        for s_orig in s_list:
            s = s_orig.copy()
            s['tipo'] = s_type
            s['global_id'] = id_global
            s['atendido'] = False
            servicos.append(s)
            id_global += 1

    total_servicos = len(servicos)
    servicos_atendidos_cont = 0
    rotas_finais = []

    while servicos_atendidos_cont < total_servicos:
        servicos_atendidos_antes = servicos_atendidos_cont
        carga_atual = 0
        seq_serv_rota_obj = []
        pos_atual = deposito

        while True:
            distancias_atuais = g.obter_distancias(pos_atual)
            melhor_indice = -1
            menor_custo_insercao = math.inf
            p1_escolhido, p2_escolhido, prox_pos_escolhida = 0, 0, -1

            for i, s in enumerate(servicos):
                if s['atendido'] or (carga_atual + s['demanda'] > capacidade):
                    continue

                custo_candidato_atual, p1_temp, p2_temp, pos_final_temp = math.inf, 0, 0, 0
                u, v, s_custo, t_custo = s['u'], s['v'], s['s_custo'], s['t_custo']

                if s['tipo'] == 'N':
                    custo_viagem = distancias_atuais.get(u, math.inf)
                    if custo_viagem != math.inf:
                        custo_candidato_atual, p1_temp, p2_temp, pos_final_temp = custo_viagem + s_custo, u, u, u
                elif s['tipo'] == 'E':
                    custo_vu = distancias_atuais.get(u, math.inf)
                    custo1 = (custo_vu + t_custo + s_custo) if custo_vu != math.inf else math.inf
                    custo_vv = distancias_atuais.get(v, math.inf)
                    custo2 = (custo_vv + t_custo + s_custo) if custo_vv != math.inf else math.inf
                    if custo1 <= custo2 and custo1 != math.inf:
                        custo_candidato_atual, p1_temp, p2_temp, pos_final_temp = custo1, u, v, v
                    elif custo2 < custo1 and custo2 != math.inf:
                        custo_candidato_atual, p1_temp, p2_temp, pos_final_temp = custo2, v, u, u
                elif s['tipo'] == 'A':
                    custo_viagem = distancias_atuais.get(u, math.inf)
                    if custo_viagem != math.inf:
                        custo_candidato_atual, p1_temp, p2_temp, pos_final_temp = custo_viagem + t_custo + s_custo, u, v, v

                if custo_candidato_atual < menor_custo_insercao:
                    menor_custo_insercao, melhor_indice = custo_candidato_atual, i
                    p1_escolhido, p2_escolhido, prox_pos_escolhida = p1_temp, p2_temp, pos_final_temp
            
            if melhor_indice != -1:
                servico_escolhido = servicos[melhor_indice]
                servico_escolhido['atendido'] = True
                servicos_atendidos_cont += 1
                carga_atual += servico_escolhido['demanda']
                seq_serv_rota_obj.append((servico_escolhido['global_id'], p1_escolhido, p2_escolhido, servico_escolhido['demanda'], servico_escolhido['s_custo'], servico_escolhido['t_custo']))
                pos_atual = prox_pos_escolhida
            else:
                break
        
        if seq_serv_rota_obj:
            custo_rota_final = calcular_custo_rota(seq_serv_rota_obj, g, deposito)
            if custo_rota_final == math.inf:
                print(f"ERRO ({dados['nome']}): Rota inviável detectada durante construção!")
            rotas_finais.append({"servicos": seq_serv_rota_obj, "servicos_str": [f"(S {s[0]},{s[1]},{s[2]})" for s in seq_serv_rota_obj], "demanda": carga_atual, "custo": custo_rota_final})

        if servicos_atendidos_cont == servicos_atendidos_antes and servicos_atendidos_cont < total_servicos:
            print(f"AVISO CRÍTICO ({dados['nome']}): Loop estagnado. {total_servicos - servicos_atendidos_cont} serviços não atendidos. Parando.")
            break
            
    # Certifique-se de que a solução inicial é válida e não vazia.
    rotas_info = rotas_finais  # Exemplo de inicialização
    if not rotas_info:
        raise ValueError("Solução inicial inválida ou vazia.")
    return rotas_info, g