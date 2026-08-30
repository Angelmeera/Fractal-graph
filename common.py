"""
Shared constructions and solvers for the computations reported in
"On Graceful Labeling of Finite Approximation of Fractal Graphs".

Requires: networkx, numpy, ortools   (pip install networkx numpy ortools)
"""
import collections, itertools, math, warnings
warnings.filterwarnings('ignore', category=UserWarning, module='networkx')
import networkx as nx
import numpy as np
from ortools.sat.python import cp_model

# ----------------------------------------------------------------- graphs

def vicsek_graph(d):
    """V_d of Algorithm 1, line 2: saltire form (four corners + centre)."""
    squares = {(0, 0)}
    for _ in range(d):
        squares = {(3 * x + dx, 3 * y + dy) for (x, y) in squares
                   for dx, dy in [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]}
    G = nx.Graph()
    for (x, y) in squares:
        c = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
        for i in range(4):
            G.add_edge(c[i], c[(i + 1) % 4])
    return nx.convert_node_labels_to_integers(G)


def dragon_graph(n):
    """Coordinate-identified Heighway dragon D_n of Algorithm 1, line 3."""
    s = "FX"
    for _ in range(n):
        out = []
        for ch in s:
            out.append({'X': "X+YF+", 'Y': "-FX-Y"}.get(ch, ch))
        s = "".join(out)
    x = y = 0
    dx, dy = 1, 0
    G = nx.Graph()
    G.add_node((0, 0))
    for ch in s:
        if ch == 'F':
            nx_, ny_ = x + dx, y + dy
            G.add_edge((x, y), (nx_, ny_))
            x, y = nx_, ny_
        elif ch == '+':
            dx, dy = -dy, dx
        elif ch == '-':
            dx, dy = dy, -dx
    return G


def amal(H, h, k):
    """Amal(H, h, k): vertex amalgamation of k copies of H at the vertex h."""
    G = nx.Graph()
    G.add_node('h')
    nxt = 0
    for _ in range(k):
        mp = {}
        for v in H.nodes():
            if v == h:
                mp[v] = 'h'
            else:
                mp[v] = nxt
                nxt += 1
        for u, v in H.edges():
            G.add_edge(mp[u], mp[v])
    return G


def C4k(k):
    """C_4^(k) = Amal(C_4, v, k)."""
    return amal(nx.cycle_graph(4), 0, k)


# ------------------------------------------------------- cactus censuses

def _attach(G, v, n, cycle_len):
    H = G.copy()
    new = list(range(n, n + cycle_len - 1))
    path = [v] + new + [v]
    H.add_edges_from(zip(path, path[1:]))
    return H


def cactus_census(bmax, cycle_len=4, delta_le4_only=False, verbose=True):
    """
    All C_m-cacti with 1..bmax blocks, up to isomorphism, built by attaching
    one block at a time.  Returns {b: [graphs]}.

    Isomorphism rejection uses Weisfeiler-Lehman hashing to bucket, then an
    exact nx.is_isomorphic test inside each bucket, so the counts are exact.
    """
    level = [nx.cycle_graph(cycle_len)]
    out = {1: level}
    for b in range(2, bmax + 1):
        buckets = collections.defaultdict(list)
        for G in level:
            n = G.number_of_nodes()
            for v in list(G.nodes()):
                if delta_le4_only and G.degree(v) >= 4:
                    continue
                H = nx.convert_node_labels_to_integers(_attach(G, v, n, cycle_len))
                key = nx.weisfeiler_lehman_graph_hash(H, iterations=5)
                if not any(nx.is_isomorphic(H, K) for K in buckets[key]):
                    buckets[key].append(H)
        level = [G for lst in buckets.values() for G in lst]
        out[b] = level
        if verbose:
            print(f"    b={b}: {len(level)}", flush=True)
    return out


def is_snake(G):
    """True iff the block-adjacency tree of G is a path."""
    blocks = [frozenset().union(*[set(e) for e in bb])
              for bb in nx.biconnected_component_edges(G)]
    B = nx.Graph()
    B.add_nodes_from(range(len(blocks)))
    for i, j in itertools.combinations(range(len(blocks)), 2):
        if blocks[i] & blocks[j]:
            B.add_edge(i, j)
    if B.number_of_nodes() == 1:
        return True
    return nx.is_tree(B) and all(d <= 2 for _, d in B.degree())


# ------------------------------------------------------ labeling models

def alpha_model(G, extra=None):
    """
    CP-SAT model for an alpha-labeling (Algorithm 1, Phase 2, with the
    bipartition constraint of line 14).  Colour class 0 is the low class;
    the complementary choice is reached by f^c(v) = q - f(v).
    """
    q = G.number_of_edges()
    nodes = list(G.nodes())
    col = nx.bipartite.color(G)
    m = cp_model.CpModel()
    x = {v: m.NewIntVar(0, q, f"x{v}") for v in nodes}
    lam = m.NewIntVar(0, q, "lam")
    for v in nodes:
        if col[v] == 0:
            m.Add(x[v] <= lam)
        else:
            m.Add(x[v] > lam)
    m.AddAllDifferent(list(x.values()))
    d = []
    for u, v in G.edges():
        dd = m.NewIntVar(1, q, "d")
        if col[u] == 0:
            m.Add(dd == x[v] - x[u])
        else:
            m.Add(dd == x[u] - x[v])
        d.append(dd)
    m.AddAllDifferent(d)
    if extra:
        extra(m, x, lam, col, q, nodes)
    return m, x, lam


def graceful_model(G):
    """CP-SAT model for a graceful labeling (Algorithm 1, Phase 2, lines 5-9)."""
    q = G.number_of_edges()
    nodes = list(G.nodes())
    m = cp_model.CpModel()
    x = {v: m.NewIntVar(0, q, f"x{v}") for v in nodes}
    m.AddAllDifferent(list(x.values()))
    d = []
    for u, v in G.edges():
        dd = m.NewIntVar(1, q, "d")
        m.AddAbsEquality(dd, x[u] - x[v])
        d.append(dd)
    m.AddAllDifferent(d)
    return m, x


def solve(m, tl=300, workers=8, seed=0):
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    s.parameters.max_time_in_seconds = tl
    s.parameters.random_seed = seed
    return s.Solve(m), s


def check_graceful(G, f):
    """Independent re-check of a returned labeling (Algorithm 1, line 21)."""
    q = G.number_of_edges()
    assert len(set(f.values())) == G.number_of_nodes(), "labels not injective"
    assert all(0 <= v <= q for v in f.values()), "label out of range"
    lab = sorted(abs(f[u] - f[v]) for u, v in G.edges())
    assert lab == list(range(1, q + 1)), "induced labels are not 1..q"
    return True


def has_alpha(G, tl=300):
    """True / False / None (None = solver did not finish)."""
    m, x, lam = alpha_model(G)
    st, s = solve(m, tl)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        f = {v: s.Value(x[v]) for v in G.nodes()}
        check_graceful(G, f)
        return True
    if st == cp_model.INFEASIBLE:
        return False
    return None


def has_graceful(G, tl=300):
    m, x = graceful_model(G)
    st, s = solve(m, tl)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        f = {v: s.Value(x[v]) for v in G.nodes()}
        check_graceful(G, f)
        return True
    if st == cp_model.INFEASIBLE:
        return False
    return None


# ------------------------------------------------- label-weighted matrices

def weighted_matrices(G, f):
    """A_f and L_f of Section 2."""
    nodes = list(G.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    p = len(nodes)
    A = np.zeros((p, p))
    for u, v in G.edges():
        w = abs(f[u] - f[v])
        A[idx[u], idx[v]] = w
        A[idx[v], idx[u]] = w
    L = np.diag(A.sum(1)) - A
    return A, L
