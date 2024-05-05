#класс вершины
class Vertex:
    def __init__(self, label):
        self.label = label  # метка
        self.path_idx_list = []  # список индексов исходящих ребер
        self.calc_path = -1  # посчитанный "вес пути" для вершины

# добавление индекса исходящего ребра
    def add_path_idx(self, idx):
        if idx in self.path_idx_list:
            return False
        else:
            self.path_idx_list.append(idx)
            return True

# вернуть список индексов исходящих ребер
    def ret_paths(self):
        return self.path_idx_list

# записать "вес пути" до вершины
    def set_calc_path(self, interval):
        self.calc_path = interval

# проверка вес пути бесконечен или нет
    def is_calc_path_infinity(self):
        if self.calc_path == -1:
            return True
        else:
            return False

# класс (структура) ребра
class Path:
    def __init__(self, vert_from_idx, vert_to_idx, interval):
        self.vert_from_idx = vert_from_idx
        self.vert_to_idx = vert_to_idx
        self.interval = interval

# класс графа
class Graph:
    def __init__(self):
        self.v_list = []  # массив вершин
        self.p_list = []  # массив ребер
        self.path_tmp = []  # массив для поиска минимального пути
        self.watched_list = []  # индексы уже просмотренных вершин

    #  поиск индекса вершины в массиве по метке
    def find_vertex_by_label(self, vert_label):
        idx = 0
        for v in self.v_list:
            if v.label == vert_label:
                return idx
            else:
                idx += 1
        return False

    # функция проверки есть ли вершина в графе
    def has_vertex_by_label(self, vert_label):
        for v in self.v_list:
            if v.label == vert_label:
                return True
        return False

    #добавить вершину в граф
    def add_vertex(self, vertex):
        if not self.has_vertex_by_label(vertex.label):
            self.v_list.append(vertex)
            return True
        else:
            return False

    # добавить ребро в граф через экземпляр класса
    def add_path(self, path):
        self.p_list.append(path)
        return len(self.p_list) - 1

    # добавить ребро в граф через описание меток вершин и расстояния между ними
    def add_path_by_labels(self, vert_from_label, vert_to_label, interval):
        vert_from_idx = self.find_vertex_by_label(vert_from_label)
        vert_to_idx = self.find_vertex_by_label(vert_to_label)
        p_idx = self.add_path(Path(vert_from_idx, vert_to_idx, interval))
        self.v_list[vert_from_idx].add_path_idx(p_idx)
        self.v_list[vert_to_idx].add_path_idx(p_idx)

    # поиск минимального расстояния на исходящих рёбрах вершины (не используется)
    def ret_min_path_from_vert(self, v_idx):
        st_idx = self.v_list[v_idx].path_idx_list[0]
        path_min = self.p_list[st_idx].interval
        path_min_idx = 0
        for p_idx in self.v_list[v_idx].path_idx_list:
            if self.p_list[p_idx].interval < path_min:
                path_min = self.p_list[p_idx].interval
                path_min_idx = p_idx
        return self.v_list[v_idx].path_idx_list[path_min_idx]

    # расчет "веса пути" для вершины и поиск ребра для перехода, входные данные - индекс вершины
    def calc_linked_path(self, v_idx):
        path_min = -1
        path_min_idx = -1

        for p_idx in self.v_list[v_idx].path_idx_list:
            if not self.p_list[p_idx].vert_to_idx == v_idx:
                v_to_idx = self.p_list[p_idx].vert_to_idx
            else:
                v_to_idx = self.p_list[p_idx].vert_from_idx

            if v_to_idx in self.watched_list:
                continue

            interval = self.p_list[p_idx].interval
            path_start = self.v_list[v_idx].calc_path

            if path_start + interval < self.v_list[v_to_idx].calc_path or self.v_list[v_to_idx].calc_path == -1:
                self.v_list[v_to_idx].calc_path = path_start + interval

            if path_min_idx == -1:
                path_min_idx = p_idx
                path_min = self.v_list[v_to_idx].calc_path
            elif self.v_list[v_to_idx].calc_path < path_min:
                path_min_idx = p_idx
                path_min = self.v_list[v_to_idx].calc_path

        return path_min_idx

    # определение начального значения веса для стартовой вершины и запуск расчета "весов пути"
    def calc_min_path(self, v_idx):
        if self.v_list[v_idx].is_calc_path_infinity():
            self.v_list[v_idx].set_calc_path(0)

        self.calc_iterative(v_idx)

    # итеративная функция перебора вершин по алгоритму
    def calc_iterative(self, v_idx):
        while True:
            path_min_idx = self.calc_linked_path(v_idx)
            self.watched_list.append(v_idx)
            v_to = self.ret_other_v(v_idx, path_min_idx)
            if v_to in self.watched_list:
                return True
            else:
                #self.calc_recursive(v_to)
                v_idx = v_to

    # вернуть индекс вершины на другой стороне ребра
    def ret_other_v(self, cur_v, p_idx):
        if not self.p_list[p_idx].vert_to_idx == cur_v:
            v_to = self.p_list[p_idx].vert_to_idx
        else:
            v_to = self.p_list[p_idx].vert_from_idx
        return v_to

    # поиск обратного пути по метке конечной вершины
    def find_path_labels(self, v_label_end):
        v_end_idx = self.find_vertex_by_label(v_label_end)
        has_path = False
        for p_idx in self.v_list[v_end_idx].path_idx_list:
            interval = self.p_list[p_idx].interval
            v_to = self.ret_other_v(v_end_idx, p_idx)

            if self.v_list[v_end_idx].calc_path - interval == self.v_list[v_to].calc_path:
                #print(self.v_list[v_to].label)
                label_next = self.v_list[v_to].label
                has_path = True
                self.path_tmp.append(label_next)
                self.find_path_labels(label_next)
        if not has_path:
            #print("Завершено")
            return

    # запуск алгоритмов расчёта "весов путей" и вывода оптимального пути на экран
    def start_search_path(self, v_label_start, v_label_end):
        start_idx = self.find_vertex_by_label(v_label_start)

        self.calc_min_path(start_idx)
        self.path_tmp = [v_label_end]
        self.find_path_labels(v_label_end)
        #var_dump(self.path_tmp)
        self.print_w()
        self.print_path()

    # вывод оптимального пути на экран
    def print_path(self):
        path_str = ""
        el_count = len(self.path_tmp)
        for x in range(0, el_count):
            path_str += self.path_tmp[(el_count-x-1)]
            if x < el_count-1:
                path_str += "-"
        print("= Оптимальный путь =")
        print(path_str)

    # вывод на экран рассчитанных "весов путей" для начальной вершины графа
    def print_w(self):
        print("= Посчитанные минимальные пути =")
        for el in self.v_list:
            print(el.label + ": " + str(el.calc_path))
