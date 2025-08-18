from leitura import ler_instancia_completa

dados = ler_instancia_completa(r"C:\Users\rafae\OneDrive\Área de Trabalho\GCC218(atualizadoFase2)\GCC218\Fase 2\Ins\BHW10.dat")
print("Resumo da leitura:")
print("Nomes dos blocos: ")
print(f"  Nos requeridos    : {len(dados['requisitos']['nos'])}")
print(f"  Arestas requeridas: {len(dados['requisitos']['arestas'])}")
print(f"  Arcos requeridos  : {len(dados['requisitos']['arcos'])}")
print(f"  Total conexões    : {len(dados['conexoes'])}")
print(f"  Capacidade: {dados['capacidade']}  Deposito: {dados['deposito']}  Num vértices: {dados['num_vertices']}")
print(f"Primeiras 10 conexões: {dados['conexoes'][:10]}")
