from collections import OrderedDict, deque

class MemorySimulator:
    def __init__(self, page_size, num_tlb_entries, num_frames, rep_policy):
        self.page_size = page_size
        self.num_tlb_entries = num_tlb_entries
        self.num_frames = num_frames    
        self.rep_policy = rep_policy

        if rep_policy not in ['LRU', 'SecondChance']:
            raise ValueError("Política de substituição inválida. Use 'LRU' ou 'SecondChance'.")

        self.tlb = OrderedDict()  # TLB com política LRU - ordem = mais antigo -> mais recente
        self.page_table = {}  # Tabela de páginas
        self.frames = [None] * num_frames

        # Estruturas auxiliares para substituição
        self.frame_usage = OrderedDict()    # ordem = mais antigo -> mais recente; contém marcadores de uso para LRU
        self.second_chance = deque()    # para política SecondChance
        self.reference_bits = {}    # bits de referência das páginas

        # contadores de estatísticas
        self.tlb_hits = 0
        self.tlb_misses = 0
        self.page_faults = 0

    def access_memory(self, virtual_address):
        """Simula o acesso a um endereço virtual."""
        page_number = virtual_address // self.page_size

        # 1. Tenta acessar a TLB
        if page_number in self.tlb:
            self.tlb_hits += 1
            frame_number = self.tlb[page_number]
            # Atualiza LRU da TLB
            self.tlb.move_to_end(page_number)
        else:
            self.tlb_misses += 1
            frame_number = self.handle_tlb_miss(page_number)

        # 2. Atualiza estruturas da política de substituição
        self.update_replacement_policy(page_number)

        return frame_number

    # Métodos auxiliares
    def handle_tlb_miss(self, page_number):
        """Trata uma falta na TLB (pode gerar page fault)"""

        # tenta acessar a tabela de páginas
        if page_number not in self.page_table:
            # atualiza table de páginas e conta page fault
            self.page_faults += 1
            self.handle_page_fault(page_number)

        # atualiza TLB
        frame_number = self.page_table[page_number]
        self.update_tlb(page_number, frame_number)
        return frame_number

    def handle_page_fault(self, page_number):
        """Trata um page fault com base na política de substituição"""
        # Verifica se há espaço livre na memória física
        if None in self.frames:
            # aloca nova página em um frame livre
            frame_number = self.frames.index(None)
            self.frames[frame_number] = page_number
        else:
            # substitui uma página existente
            if self.rep_policy == "LRU":
                frame_number = self.replace_page_lru(page_number)
            elif self.rep_policy == "SecondChance":
                frame_number = self.replace_page_second_chance(page_number)
            else:
                raise ValueError("Política de substituição inválida")

        # Atualiza tabela de páginas
        self.page_table[page_number] = frame_number

    def update_tlb(self, page_number, frame_number):
        """Atualiza TLB com política LRU"""
        if page_number in self.tlb:
            # reordena o mais recente para o fim do dict
            self.tlb.move_to_end(page_number)
        else:
            if len(self.tlb) >= self.num_tlb_entries:
                self.tlb.popitem(last=False)  # remove LRU
            self.tlb[page_number] = frame_number

    def replace_page_lru(self, new_page):
        """
        Substitui página menos usada (LRU)
        Retorna a posição do frame onde a nova página foi alocada.
        """
        # remove a página menos recentemente usada
        old_page, _ = self.frame_usage.popitem(last=False)
        frame_number = self.page_table[old_page]
        del self.page_table[old_page]

        #substitui a página no frame
        self.frames[frame_number] = new_page
        return frame_number

    def replace_page_second_chance(self, new_page):
        """Implementa algoritmo Second-Chance"""
        while True:
            old_page = self.second_chance[0]
            if self.reference_bits.get(old_page, 0) == 0:
                self.second_chance.popleft()
                frame_number = self.page_table[old_page]
                del self.page_table[old_page]
                self.frames[frame_number] = new_page
                return frame_number
            else:
                # Dá segunda chance
                self.reference_bits[old_page] = 0
                self.second_chance.rotate(-1)

    def update_replacement_policy(self, page_number):
        """Atualiza informações de uso (para LRU ou SecondChance)"""
        if self.rep_policy == "LRU":
            if page_number in self.frame_usage:
                self.frame_usage.move_to_end(page_number)
            else:
                self.frame_usage[page_number] = True
        elif self.rep_policy == "SecondChance":
            if page_number not in self.reference_bits:
                self.reference_bits[page_number] = 1
                self.second_chance.append(page_number)
            else:
                self.reference_bits[page_number] = 1

    def print_statistics(self):
        print("=" * 60)
        print("SIMULADOR DE MEMÓRIA - Estatísticas de Acesso")
        print("=" * 60)
        print(f"Política de Substituição:   {self.rep_policy}")
        print(f"Tamanho da Página:          {self.page_size} bytes")
        print(f"Entradas na TLB:            {self.num_tlb_entries}")
        print(f"Número de Frames:           {self.num_frames}")
        print("-" * 60)
        print(f"TLB Hits:                   {self.tlb_hits:,}")
        print(f"TLB Misses:                 {self.tlb_misses:,}")
        print(f"Page Faults:                {self.page_faults:,}")
        print("=" * 60)
