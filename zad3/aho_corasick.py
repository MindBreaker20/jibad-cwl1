class Automaton:  # Klasa reprezentujaca automat
    def __init__(self, goto, fail_links, pattern_nodes, dictionary_links):  # Komponenty automatu
        self.goto = goto
        self.fail_links = fail_links
        self.pattern_nodes = pattern_nodes
        self.dictionary_links = dictionary_links


class AhoCorasick:  # Klasa implementująca automat Aho-Corasick
    def __init__(self):
        self.goto = {}
        self.fail_links = {}
        self.pattern_nodes = {}
        self.dictionary_links = {}
        self.indexes = []

    def build_goto(self, patterns):  # Budowanie Goto - słownika słowników
        tape = '#'.join(patterns)
        parent_node, child_node = 0, 1  # Inicjalizacja pierwszego rodzica i potomka
        for i in range(len(tape)):
            if tape[i] != '#':
                if parent_node not in self.goto:
                    self.goto[parent_node] = {tape[i]: child_node}  # Tworzenie zagnieżdżonego słownika przechowującego potomków rodzica
                    parent_node = child_node
                    child_node += 1
                else:
                    if tape[i] in self.goto[parent_node]:
                        parent_node = self.goto[parent_node][tape[i]]  # Potomek staje się rodzicem dla swoich potomków
                    else:
                        self.goto[parent_node][tape[i]] = child_node  # Aktualizacja słownika potomków danego rodzica
                        parent_node = child_node
                        child_node += 1
            else:
                parent_node = 0

    def build_fail_links(self):  # Budowanie Failure links z użyciem algorytmu Breadth First Search
        visited_nodes, queue = [], []
        root_node = 0
        visited_nodes.append(root_node)
        queue.append(root_node)
        self.fail_links[0] = 0

        while len(queue) > 0:
            node = queue[0]
            queue.pop(0)
            if node in self.goto.keys():
                for label, child_node in self.goto[node].items():
                    if child_node not in visited_nodes:
                        queue.append(child_node)
                        visited_nodes.append(child_node)
                        if node == 0:  # Potomkowie korzenia mają fail linki do korzenia
                            self.fail_links[child_node] = 0
                        else:
                            parent_node = node  # Jedno cofnięcie się do rodzica
                            self.new_fail_link_search(parent_node, label, child_node)

    def new_fail_link_search(self, parent_node, label, child_node):  # Nieustanne poszukiwanie nowego fail linka
        while True:
            parent_node = self.fail_links[parent_node]
            if parent_node == 0:
                if label in self.goto[parent_node]:  # Jeśli z korzenia wychodzi etykieta
                    self.fail_links[child_node] = self.goto[parent_node][label]
                    break
                else:  # Jesli z korzenia nie wychodzi etykieta
                    self.fail_links[child_node] = 0
                    break
            else:
                if parent_node in self.goto.keys():
                    if label in self.goto[parent_node]:  # Fail link do potomka na wyższym szczeblu
                        self.fail_links[child_node] = self.goto[parent_node][label]
                        break

    def build_ending_pattern_nodes(self):  # Budowanie słownika węzłów, gdzie kończą się podane wzorce (klucz to węzeł, wartość to indeks wzorca w liście)
        for pattern in pattern_strings:
            node = 0
            for i in range(len(pattern)):
                if pattern[i] in self.goto[node].keys():  # Jesli litera wzorca pokrywa się z etykietą wchodzącą węzła
                    label = pattern[i]
                    node = self.goto[node][label]
            self.pattern_nodes[node] = pattern_strings.index(pattern)

    def build_dictionary_links(self):  # Budowanie Dictionary links
        for node, linked_node in self.fail_links.items():  # Przeszukiwanie fail linków
            for pattern_node in self.pattern_nodes.keys():  # Przeszukiwanie słownika węzłów, gdzie kończą się podane wzorce
                if linked_node == pattern_node:
                    self.dictionary_links[node] = pattern_node

    def build(self, patterns):  # Funkcja zwracająca zbudowany automat
        self.build_goto(patterns)
        self.build_fail_links()
        self.build_ending_pattern_nodes()
        self.build_dictionary_links()
        return Automaton(self.goto, self.fail_links, self.pattern_nodes, self.dictionary_links)

    def search(self, automaton_object, text):  # Szukanie wzorców w tekście
        node, counter = 0, 0
        text = text + "#"

        while text[counter] != '#':
            label = text[counter]
            if node in automaton_object.goto.keys():
                if label in automaton_object.goto[node].keys():
                    node = automaton_object.goto[node][label]
                else:
                    node = automaton_object.fail_links[node]
                    continue
            else:
                node = automaton_object.fail_links[node]
                continue

            if node in automaton_object.pattern_nodes:  # Sprawdzenie czy sciezka w drzewie zawiera węzły wzorców
                pattern_index = automaton_object.pattern_nodes[node]  # Wydobycie indeksu wzorca w liście wzorców
                pattern = pattern_strings[pattern_index]  # wydobycie subtekstu z listy wzorców za pomocą indeksu
                self.indexes.append(counter - len(pattern) + 1)  # Użycie dlugosci subtekstu do obliczenia indeksu subwzorca

            if node in automaton_object.dictionary_links:  # Sprawdzenie czy sciezka w drzewie ma dictionary links (sub wzorce)
                node_index = automaton_object.dictionary_links[node]  # Wydobycie numeru węzła sub wzorca
                pattern_index = automaton_object.pattern_nodes[node_index]   # Wydobycie indeksu wzorca w liście wzorców
                pattern = pattern_strings[pattern_index]  # wydobycie subtekstu z listy wzorców
                self.indexes.append(counter - len(pattern) + 1)

            counter += 1

        self.indexes = list(set(self.indexes))  # Redukcja ewentualnych powtarzajacych sie indeksów (subwzorce i wzorce)

    def __repr__(self):
        rep = str(self.indexes)
        return rep


if __name__ == '__main__':
    text_string = "aaabc"
    pattern_strings = ["abc", "aab", "cba"]
    ahoCorasick = AhoCorasick()
    automaton = ahoCorasick.build(pattern_strings)
    ahoCorasick.search(automaton, text_string)
    print(repr(ahoCorasick.indexes))

