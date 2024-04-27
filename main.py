from graph import *
# алгоритм взят отсюда
# https://skillbox.ru/media/code/algoritm-deykstry-chto-eto-takoe-kak-rabotaet-i-gde-ispolzuetsya/
# весь код писал сам с нуля

# определение графа
gr = Graph()
# добавление вершин графа
gr.add_vertex(Vertex("A"))
gr.add_vertex(Vertex("B"))
gr.add_vertex(Vertex("C"))
gr.add_vertex(Vertex("D"))
gr.add_vertex(Vertex("E"))
gr.add_vertex(Vertex("F"))

# добавление ребер графа (метка исходящей вершины, метка входящей вершины, расстояние ребра
gr.add_path_by_labels("A", "B", 7)
gr.add_path_by_labels("A", "E", 4)
gr.add_path_by_labels("B", "F", 2)
gr.add_path_by_labels("B", "C", 5)
gr.add_path_by_labels("C", "F", 6)
gr.add_path_by_labels("C", "D", 11)
gr.add_path_by_labels("D", "F", 9)
gr.add_path_by_labels("D", "E", 8)
gr.add_path_by_labels("E", "F", 3)

# запуск нахождения пути (метка начальной вершины, метка конечной вершины
gr.start_search_path("A", "C")
