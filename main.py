from mem_sim import MemorySimulator

mem_simulator = MemorySimulator(page_size=4096, num_tlb_entries=16, num_frames=64, rep_policy='LRU')

arq_test = open("tests/trace.in", "r")

# Simula acessos de memória a partir do arquivo trace.in
for addr in arq_test:
    mem_simulator.access_memory(int(addr))
print("Simulação trace.in concluída.")
mem_simulator.print_statistics()

# Simula acessos de memória a partir dos arquivos trace_1.in a trace_5.in
for i in range(1, 6):
    mem_simulator = MemorySimulator(page_size=4096, num_tlb_entries=16, num_frames=64, rep_policy='LRU')
    trace_file = f"tests/trace_{i}.in"
    arq_test = open(trace_file, "r")

    for addr in arq_test:
        mem_simulator.access_memory(int(addr))
    print(f"Simulação {trace_file} concluída.")
    mem_simulator.print_statistics()

