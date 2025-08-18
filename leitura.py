import os

def ler_instancia_completa(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = [l.strip() for l in f if l.strip()]

    dados = {
        "nome": os.path.basename(caminho),
        "optimal_value": None,
        "capacidade": 0,
        "deposito": 0,
        "num_vertices": 0,
        "requisitos": {
            "nos": [],
            "arestas": [],
            "arcos": []
        },
        "conexoes": []
    }

    def is_header(l):
        h = l.upper()
        return ("DEMAND" in h or "S. COST" in h or "FROM" in h or "TO" in h or "T. COST" in h or "COST" in h)

    def try_parse_connection(line_parts):
        try:
            u = int(line_parts[-3])
            v = int(line_parts[-2])
            custo = int(line_parts[-1])
            return u, v, custo
        except (IndexError, ValueError):
            return None, None, None

    i = 0
    while i < len(linhas):
        linha = linhas[i]
        lstr = linha.strip().upper()

        if "OPTIMAL VALUE" in lstr: i+=1; continue
        elif "CAPACITY" in lstr: dados["capacidade"] = int(linha.split(":")[1].strip()); i+=1; continue
        elif "DEPOT NODE" in lstr: dados["deposito"] = int(linha.split(":")[1].strip()); i+=1; continue
        elif "#NODES" in lstr: dados["num_vertices"] = int(linha.split(":")[1].replace('\t','').strip()); i+=1; continue
        elif "#VEHICLES" in lstr: i+=1; continue
        elif "#EDGES" in lstr: i+=1; continue
        elif "#ARCS" in lstr: i+=1; continue
        elif "#REQUIRED" in lstr: i+=1; continue
        elif "NAME:" in lstr: i+=1; continue

        elif lstr.startswith("REN."):
            i += 1
            while i < len(linhas):
                l = linhas[i]
                if not l or not l.strip().upper().startswith("N") or is_header(l): break
                try:
                    partes = l.split(); sid = int(partes[0][1:]); d = int(partes[1]); sc = int(partes[2])
                    dados["requisitos"]["nos"].append({"id": sid, "u": sid, "v": sid, "demanda": d, "s_custo": sc, "t_custo": 0})
                except Exception as e: pass
                i += 1
            continue
        elif lstr.startswith("REE."):
            i += 1
            while i < len(linhas):
                l = linhas[i]
                if not l or not l.strip().upper().startswith("E") or is_header(l): break
                try:
                    partes = l.split(); sid = int(partes[0][1:]); u = int(partes[1]); v = int(partes[2]); tc = int(partes[3]); d = int(partes[4]); sc = int(partes[5])
                    dados["requisitos"]["arestas"].append({"id": sid, "u": u, "v": v, "demanda": d, "s_custo": sc, "t_custo": tc})
                    dados["conexoes"].append((u, v, tc, "E")); dados["conexoes"].append((v, u, tc, "E"))
                except Exception as e: pass
                i += 1
            continue
        elif lstr.startswith("REA."):
            i += 1
            while i < len(linhas):
                l = linhas[i]
                if not l or not l.strip().upper().startswith("A") or is_header(l): break
                try:
                    partes = l.split(); sid = int(partes[0][1:]); u = int(partes[1]); v = int(partes[2]); tc = int(partes[3]); d = int(partes[4]); sc = int(partes[5])
                    dados["requisitos"]["arcos"].append({"id": sid, "u": u, "v": v, "demanda": d, "s_custo": sc, "t_custo": tc})
                    dados["conexoes"].append((u, v, tc, "A"))
                except Exception as e: pass
                i += 1
            continue

        elif lstr.startswith("EDGE"):
            i += 1
            while i < len(linhas):
                l = linhas[i]
                if not l or is_header(l) or l.upper().startswith("ARC"): break
                partes = l.split()
                u, v, custo = try_parse_connection(partes)
                if u is not None:
                    dados["conexoes"].append((u, v, custo, "NE"))
                    dados["conexoes"].append((v, u, custo, "NE"))
                else: pass # Ignora silenciosamente linhas não parseáveis aqui
                i += 1
            continue

        elif lstr.startswith("ARC"):
            i += 1
            while i < len(linhas):
                l = linhas[i]
                if not l or is_header(l) or l.upper().startswith("END"): break
                partes = l.split()
                u, v, custo = try_parse_connection(partes)
                if u is not None:
                    dados["conexoes"].append((u, v, custo, "NA"))
                else: pass # Ignora silenciosamente linhas não parseáveis aqui
                i += 1
            continue

        i += 1
    return dados