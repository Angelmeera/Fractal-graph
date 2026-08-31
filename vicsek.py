"""
The Vicsek-specific computations: all three labeling models of Algorithm 1
applied to V_d, and the alpha-verification behind Corollary 21.

Usage:
    python vicsek.py alpha        # V_d is an alpha-graph, d = 0, 1, 2
    python vicsek.py labelings    # graceful, odd graceful and alpha, d = 0, 1, 2
    python vicsek.py d3 [SECS]    # the honest negative at d = 3 (p=376, q=500)
    python vicsek.py prop6        # Proposition 6's structural claims, d = 0..3
    python vicsek.py boundaries   # the boundaries lambda attained, d = 0, 1, 2

Reproduces:
    V_0 (= C_4), V_1 and V_2 admit alpha-labelings, hence (Lemma 11) odd
    graceful ones; d = 3 returns UNKNOWN on modest hardware, which is what
    the paper records.
"""
import sys, time
import networkx as nx
from ortools.sat.python import cp_model
from common import (vicsek_graph, alpha_model, graceful_model,
                    odd_graceful_model, solve, check_graceful,
                    check_odd_graceful, has_alpha, is_snake)


def _run(model_fn, G, tl, checker):
    m, x = model_fn(G)[:2]
    st, s = solve(m, tl)
    name = s.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        checker(G, {v: s.Value(x[v]) for v in G.nodes()})
    return name


def alpha(dmax=2, tl=900):
    print("=== V_d is an alpha-graph (the basis of Corollary 21) ===")
    print("  d      p      q   status        time")
    for d in range(dmax + 1):
        G = vicsek_graph(d)
        t = time.time()
        m, x, lam = alpha_model(G)
        st, s = solve(m, tl)
        name = s.StatusName(st)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            check_graceful(G, {v: s.Value(x[v]) for v in G.nodes()})
        print(f" {d:2d} {G.number_of_nodes():6d} {G.number_of_edges():6d}"
              f"   {name:12s} {time.time()-t:6.1f}s", flush=True)


def labelings(dmax=2, tl=900):
    print("=== all three models of Algorithm 1 on V_d ===")
    print("  d      p      q   graceful    odd graceful   alpha")
    for d in range(dmax + 1):
        G = vicsek_graph(d)
        a = _run(graceful_model, G, tl, check_graceful)
        b = _run(odd_graceful_model, G, tl, check_odd_graceful)
        c = _run(alpha_model, G, tl, check_graceful)
        print(f" {d:2d} {G.number_of_nodes():6d} {G.number_of_edges():6d}"
              f"   {a:11s} {b:14s} {c}", flush=True)
    print("\nEvery labeling returned was re-checked independently for injectivity,")
    print("range and induced-label set (Algorithm 1, line 21).")


def boundaries(dmax=2, tl=600):
    """
    p. 24: V_0, V_1, V_2 are alpha-graphs with boundary lambda = 2, 9, 37, and
    for V_1 every lambda permitted by (2) is attained.

    Inequality (2) gives |A| - 1 <= lambda <= q - |B| for A the low class, so
    the admissible window depends on which stable set is taken low; both
    orientations are tested here, since f^c(v) = q - f(v) maps one to the other.
    """
    import networkx as nx
    from ortools.sat.python import cp_model as cpm
    print("=== boundaries attained by alpha-labelings of V_d ===")
    for d in range(dmax + 1):
        G = vicsek_graph(d)
        q = G.number_of_edges()
        col = nx.bipartite.color(G)
        A = [v for v in G if col[v] == 0]
        B = [v for v in G if col[v] == 1]
        attained = []
        for low, high in ((A, B), (B, A)):
            lo_bound, hi_bound = len(low) - 1, q - len(high)
            for target in range(max(0, lo_bound), hi_bound + 1):
                if target in attained:
                    continue
                m = cpm.CpModel()
                x = {v: m.NewIntVar(0, q, f"x{v}") for v in G}
                for v in low:
                    m.Add(x[v] <= target)
                for v in high:
                    m.Add(x[v] > target)
                m.AddAllDifferent(list(x.values()))
                dd = []
                for u, v in G.edges():
                    e = m.NewIntVar(1, q, "d")
                    m.AddAbsEquality(e, x[u] - x[v])
                    dd.append(e)
                m.AddAllDifferent(dd)
                st, sol = solve(m, tl)
                if st in (cpm.OPTIMAL, cpm.FEASIBLE):
                    check_graceful(G, {v: sol.Value(x[v]) for v in G})
                    attained.append(target)
        attained.sort()
        window = f"[{len(A)-1}, {q-len(B)}]"
        print(f"  V_{d}: p={G.number_of_nodes():4d} q={q:4d} |A|={len(A)} |B|={len(B)}"
              f"  window from (2): {window}")
        print(f"        boundaries attained: {attained}", flush=True)
    print("\n  The paper reports lambda = 2, 9, 37 for V_0, V_1, V_2, and that for")
    print("  V_1 every lambda permitted by (2) is attained.")


def d3(secs=1800):
    G = vicsek_graph(3)
    print(f"=== V_3: p={G.number_of_nodes()}, q={G.number_of_edges()}, "
          f"time limit {secs}s ===")
    t = time.time()
    m, x, lam = alpha_model(G)
    st, s = solve(m, secs)
    print(f"  status: {s.StatusName(st)}   ({time.time()-t:.0f}s)")
    print("  The paper records UNKNOWN here: neither a labeling found nor the")
    print("  space exhausted.  Reported as an honest negative, not a claim.")


def prop6(dmax=3):
    print("=== Proposition 6: structure of V_d ===")
    print("  d      p      q  blocks  all C_4  cycle rank  Delta  bipartite  5^d")
    for d in range(dmax + 1):
        G = vicsek_graph(d)
        p, q = G.number_of_nodes(), G.number_of_edges()
        blocks = list(nx.biconnected_component_edges(G))
        allc4 = all(len(b) == 4 for b in blocks)
        rank = q - p + 1
        delta = max(dict(G.degree()).values())
        print(f" {d:2d} {p:6d} {q:6d} {len(blocks):7d}  {str(allc4):7s} {rank:11d}"
              f" {delta:6d}  {str(nx.is_bipartite(G)):9s} {5**d:5d}", flush=True)
        assert p == 3 * 5 ** d + 1 and q == 4 * 5 ** d and len(blocks) == 5 ** d
        assert allc4 and rank == 5 ** d and nx.is_bipartite(G)
    print("\n  Note: Delta(V_0) = 2, not 4 -- V_0 = C_4 has no cut vertex.")
    print("  Proposition 6's 'maximum degree 4' holds for d >= 1.")


if __name__ == "__main__":
    job = sys.argv[1] if len(sys.argv) > 1 else "alpha"
    arg = int(sys.argv[2]) if len(sys.argv) > 2 else None
    t = time.time()
    if job == "d3":
        d3(arg or 1800)
    else:
        {"alpha": alpha, "labelings": labelings, "prop6": prop6,
         "boundaries": boundaries}[job]()
    print(f"\n[{time.time()-t:.0f}s]")
