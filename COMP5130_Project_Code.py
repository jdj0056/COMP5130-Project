import random
from collections import defaultdict
from collections import Counter

def load_graph(file):
    a = defaultdict(lambda: defaultdict(float))
    with open(file, 'r') as f:
        for l in f:
            if l.startswith('#'):
                continue
            p = l.strip().split()
            if len(p) < 2:
                continue
            u, v = int(p[0]), int(p[1])
            if u == v:
                continue
            a[u][v] += 1.0
            a[v][u] += 1.0
    return a

def louvain(a):
    m = sum(sum(neighbor.values()) for neighbor in a.values()) / 2
    cur = a
    original = list(a.keys())
    n_map = {n: [n] for n in original}
    while True:
        # Phase 1
        n = list(cur.keys())
        n_community ={p: p for p in n}
        com_weight = {p: sum(cur[p].values()) for p in n}
        improved = True
        while improved:
            for u in n:
                original_community = n_community[u]
                u_degree = sum(cur[u].values())
                neighbor_weight = defaultdict(float)
                for v, weight in cur[u].items():
                    neighbor_weight[n_community[v]] += weight
                best_gain = 0
                best_community = original_community
                com_weight[original_community] -= u_degree
                for c, c_weight in neighbor_weight.items():
                    g = (c_weight / m) - (com_weight[c] *u_degree / (2 * m**2))
                    if g > best_gain:
                        best_gain = g
                        best_community = c
                    n_community[u] = best_community
                    com_weight[best_community] += u_degree
                    if best_community == original_community:
                        improved = False
                    else:
                        improved = True
        # Phase 2
        new_coms = defaultdict(list)
        for n2, c2 in n_community.items():
            new_coms[c2].append(n2)
        if len(new_coms) == len(cur):
            break
        new_a = defaultdict(lambda: defaultdict(float))
        new_map = {}
        for c_id, m_node in new_coms.items():
            combined = []
            for n2 in m_node:
                combined.extend(n_map[n2])
            new_map[c_id] = combined
            for i in m_node:
                for j, weight in cur[i].items():
                    new_a[c_id][n_community[j]] += weight
        cur = new_a
        n_map = new_map
    return list(n_map.values())

def label_propogation(a):
    nodes = list(a.keys())
    labels = {n: n for n in nodes}
    for i in range(100):
        random.shuffle(nodes)
        changed = False
        for u in nodes:
            if not a[u]:
                continue
            neighbor_labels = Counter()
            for v, weight in a[u].items():
                neighbor_labels[labels[v]] += weight
            most_common = Counter(neighbor_labels).most_common(1)[0][0]
            if labels[u] == most_common:
                changed = False
            else:
                labels[u] = most_common
                changed = True
        if not changed:
            break
    coms = defaultdict(list)
    for n, l in labels.items():
        coms[l].append(n)
    return list(coms.values())


if __name__ == "__main__":
    file = 'CA-GrQc.txt'
    graph = load_graph(file)
    print(f"\nRunning Louvain on {file}.")
    louvain_test = louvain(graph)
    print(f"\nResult of the Louvain test: {len(louvain_test)} communities found.")
    print(f"\nRunning Label Propogation on {file}.")
    label_prop_test = label_propogation(graph)
    print(f"\nResult of the Label Propogation test: {len(label_prop_test)} communities found.")
