import random

def gerar_trace(nome_arquivo="trace.in", quantidade=500, limite=10000):
    """Gera um arquivo texto com endereços aleatórios simulando acessos de memória."""
    with open(nome_arquivo, "w") as f:
        for _ in range(quantidade):
            numero = random.randint(0, limite - 1)
            f.write(f"{numero}\n")

    print(f"Arquivo '{nome_arquivo}' gerado com {quantidade} números aleatórios.")

if __name__ == "__main__":
	for i in range(1, 6):
		nome_arquivo = f"trace_{i}.in"
		gerar_trace(nome_arquivo=nome_arquivo, quantidade=500 * i, limite=10000 * i)
