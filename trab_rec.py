import networkx as nx
import copy


def rcsp(graph=nx.DiGraph()):
    graph_aux = copy.deepcopy(graph)
    node_at = 1
    node_dest = graph_aux.number_of_nodes()
    path = []
    possible_paths = {}
    for nodes in range(1, node_dest+1):
        possible_paths_aux = []
        for node_iter in G.successors(nodes):
            possible_paths_aux.append(node_iter)

        possible_paths[nodes] = possible_paths_aux
        print(possible_paths[nodes])

    # print(possible_paths[node_at])
    return graph_aux

    # while node_at != node_dest:
    #     possible_paths_aux = []
    #     for nodes_suc in G.successors(node_at):
    #         possible_paths_aux.append(nodes_suc)
    #
    #     possible_paths[node_at] = possible_paths_aux
    #     break


arq = 'rcsp6.txt'
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

rcsp(G)

# for x in G.successors(1):
#     print(x)
# print(qtd_nodes, qtd_edges, qtd_resources, qtd_min_res, qtd_max_res, G.number_of_nodes())
# print(G.get_edge_data(100, 99))
