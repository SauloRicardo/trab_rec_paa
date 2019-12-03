import networkx as nx
import copy
import random
import time


def rcsp(node_beg_f, node_end_f, qtd_max_res_f, k_paths, graph=nx.DiGraph()):
    graph_aux = copy.deepcopy(graph)
    possible_paths = {}
    for nodes in range(1, graph_aux.number_of_nodes()+1):
        possible_paths_aux = []
        it = 0
        for node_iter in graph_aux.successors(nodes):
            if it == 0:
                lower = graph_aux.get_edge_data(nodes, node_iter)['weight']
                it = 1
                possible_paths_aux.append(node_iter)

            elif graph_aux.get_edge_data(nodes, node_iter)['weight'] <= lower:
                lower = graph_aux.get_edge_data(nodes, node_iter)['weight']
                possible_paths_aux.insert(0, node_iter)

            else:
                possible_paths_aux.append(node_iter)

        possible_paths[nodes] = possible_paths_aux

    for j in k_paths:
        ant_aux = node_beg_f
        for i in j:
            if i != node_beg_f:
                possible_paths[ant_aux].remove(i)
                ant_aux = i

    path = []

    node_at = node_beg_f
    path.append(node_at)
    resources_consumed = [0]*len(qtd_max_res_f)
    while node_at != node_end_f:
        # print(path)
        possibilities = len(possible_paths[node_at])
        if possibilities > 0:
            possible_node = possible_paths[node_at].pop(random.randrange(0, possibilities))  # Aleatório
            # possible_node = possible_paths[node_at].pop(0)  # Guloso
            resources_consumed_aux = copy.deepcopy(resources_consumed)
            cont_aux = 0
            for resources in graph.get_edge_data(node_at, possible_node)['resource_consumed']:
                resources_consumed_aux[cont_aux] += resources
                cont_aux += 1

            over = False
            for verify in range(0, len(resources_consumed_aux)):
                if resources_consumed_aux[verify] < qtd_max_res_f[verify]:
                    over = True

            if over:
                node_at = possible_node
                resources_consumed = resources_consumed_aux
                path.append(node_at)

        else:
            node_return = path.pop()
            if len(path) == 0:
                break
            else:
                node_at = path[len(path) - 1]
                cont_aux = 0
                for resources in graph.get_edge_data(node_at, node_return)['resource_consumed']:
                    resources_consumed[cont_aux] -= resources
                    cont_aux += 1

        # print(path)
    return path


def make_tests():
    archives = ['rcsp1.txt', 'rcsp3.txt', 'rcsp6.txt', 'rcsp7.txt', 'rcsp9.txt',
                   'rcsp11.txt', 'rcsp13.txt', 'rcsp15.txt', 'rcsp19.txt', 'rcsp21.txt']

    for arch in archives:
        arq = arch
        inp_txt = open(arq, 'r')

        cont = 1
        qtd_nodes = 0
        qtd_edges = 0
        qtd_resources = 0
        qtd_min_res = []
        qtd_max_res = []
        G = nx.DiGraph()

        for line in inp_txt:
            line_aux = line.split(' ')
            line_aux.pop(0)
            line_aux.pop()

            if cont == 1:
                qtd_nodes, qtd_edges, qtd_resources = line_aux
                qtd_nodes, qtd_edges, qtd_resources = int(qtd_nodes), int(qtd_edges), int(qtd_resources)

            elif cont == 2:
                qtd_min_res = line_aux
                for x in range(0, len(qtd_min_res)):
                    qtd_min_res[x] = int(qtd_min_res[x])

            elif cont == 3:
                qtd_max_res = line_aux
                for x in range(0, len(qtd_max_res)):
                    qtd_max_res[x] = int(qtd_max_res[x])

            elif cont <= (qtd_nodes + 3):
                G.add_node(cont - 3)

            else:
                node_beg = int(line_aux.pop(0))
                node_end = int(line_aux.pop(0))
                weight_aux = int(line_aux.pop(0))
                res_cons_aux = line_aux
                for x in range(0, len(res_cons_aux)):
                    res_cons_aux[x] = int(res_cons_aux[x])
                G.add_edge(node_beg, node_end, weight=weight_aux, resource_consumed=res_cons_aux)
            cont += 1

        iterations = 10
        total_final = 99999999
        known_paths = []
        time_tot = time.time()

        for x in range(0, iterations):
            path = rcsp(1, qtd_nodes, qtd_max_res, known_paths, G)
            # print(path)
            known_paths.append(path)
            if len(path) > 0:
                ant = path[0]
                total = 0
                for y in path:
                    if y != path[0]:
                        total += G.get_edge_data(ant, y)['weight']
                        ant = y

                if total < total_final:
                    total_final = total
                    path_final = path

        time_tot = time.time() - time_tot

        logs.write(arch)
        logs.write("\nCaminho encontrado : " + str(path_final))
        logs.write("\nCusto do caminho : " + str(total_final))
        logs.write("\nTempo Utilizado :" + str(time_tot))
        logs.write("\n\n")

        # print(arch)
        # print("Caminho encontrado : ", path_final)
        # print("Custo do caminho : ", total_final)
        # print("Tempo Utilizado :", time_tot)
        # print()


logs = open('log_rand.txt', 'w')
make_tests()

# arq = 'rcsp21.txt'
# inp_txt = open(arq, 'r')
#
# cont = 1
# qtd_nodes = 0
# qtd_edges = 0
# qtd_resources = 0
# qtd_min_res = []
# qtd_max_res = []
# G = nx.DiGraph()
#
# for line in inp_txt:
#     line_aux = line.split(' ')
#     line_aux.pop(0)
#     line_aux.pop()
#
#     if cont == 1:
#         qtd_nodes, qtd_edges, qtd_resources = line_aux
#         qtd_nodes, qtd_edges, qtd_resources = int(qtd_nodes), int(qtd_edges), int(qtd_resources)
#
#     elif cont == 2:
#         qtd_min_res = line_aux
#         for x in range(0, len(qtd_min_res)):
#             qtd_min_res[x] = int(qtd_min_res[x])
#
#     elif cont == 3:
#         qtd_max_res = line_aux
#         for x in range(0, len(qtd_max_res)):
#             qtd_max_res[x] = int(qtd_max_res[x])
#
#     elif cont <= (qtd_nodes + 3):
#         G.add_node(cont - 3)
#
#     else:
#         node_beg = int(line_aux.pop(0))
#         node_end = int(line_aux.pop(0))
#         weight_aux = int(line_aux.pop(0))
#         res_cons_aux = line_aux
#         for x in range(0, len(res_cons_aux)):
#             res_cons_aux[x] = int(res_cons_aux[x])
#         G.add_edge(node_beg, node_end, weight=weight_aux, resource_consumed=res_cons_aux)
#     cont += 1
#
# iterations = 10
# total_final = 99999999
# known_paths = []
#
# for x in range(0, iterations):
#     path = rcsp(1, 500, qtd_max_res, known_paths, G)
#     # print(path)
#     known_paths.append(path)
#     if len(path) > 0:
#         ant = path.pop(0)
#         total = 0
#         for y in path:
#             total += G.get_edge_data(ant, y)['weight']
#             ant = y
#
#         if total < total_final:
#             total_final = total
#             path_final = path
#
# print(total_final)
