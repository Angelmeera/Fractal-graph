"""
Table 4 -- sharpness of Theorem 13 / Corollary 14 for Amal(K_{2,r}, h, m).
Table 5 -- alpha-labelings of C_4^(k) for k <= 4, and the failure at k = 5.

Usage:
    python alpha_search.py table4
    python alpha_search.py table5

Reproduces:
    Table 4   r = 2: largest alpha m = 4, smallest non-alpha m = 5
              r = 3:                   6,                       7
              r = 4:                   8,                       9
    Every negative is a COMPLETED infeasibility proof, not a time-out; the
    script prints the CP-SAT status so this can be checked.
    Table 5   the four labelings of C_4^(k), k = 1..4, with boundary lambda,
              f(h), and the induced label set {1,...,4k}; and Corollary 15's
              boundary case k = 5 returning INFEASIBLE.
"""
import sys, time
import networkx as nx
from ortools.sat.python import cp_model
from common import amal, C4k, alpha_model, solve, check_graceful


def _alpha_with_status(G, tl=1800):
    m, x, lam = alpha_model(G)
    st, s = solve(m, tl)
    name = s.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        f = {v: s.Value(x[v]) for v in G.nodes()}
        check_graceful(G, f)
        return name, f, s.Value(lam)
    return name, None, None


def table4(rs=(2, 3, 4)):
    print("=== Table 4: Amal(K_{2,r}, h, m), h a vertex of degree r ===")
    print("  r    m     p     q   CP-SAT status   alpha?")
    for r in rs:
        print(f"  --- r = {r}, bound of Corollary 14 is m <= {2*r} ---")
        for m in range(2, 2 * r + 3):
            K = nx.complete_bipartite_graph(2, r)   # nodes 0,1 have degree r
            G = amal(K, 0, m)
            t = time.time()
            name, f, lam = _alpha_with_status(G)
            print(f" {r:3d} {m:4d} {G.number_of_nodes():5d} {G.number_of_edges():5d}"
                  f"   {name:13s}   {'yes' if f else 'no':4s}  ({time.time()-t:.1f}s)",
                  flush=True)


def table5(kmax=5):
    print("=== Table 5: alpha-labelings of C_4^(k) = Amal(C_4, v, k) ===")
    print("   k    p    q  status        lambda  f(h)  lambda-f(h)")
    for k in range(1, kmax + 1):
        G = C4k(k)
        q = G.number_of_edges()
        name, f, lam = _alpha_with_status(G)
        if f is None:
            print(f" {k:4d} {G.number_of_nodes():4d} {q:4d}  {name:13s}"
                  f"   --  (Corollary 15: not an alpha-graph)")
            continue
        # normalise by f^c(v) = q - f(v) (equation (1)) so that h is in the
        # low class, matching the convention of Table 5
        if f['h'] > lam:
            f = {v: q - val for v, val in f.items()}
            lam = q - lam - 1
        fh = f['h']
        induced = sorted(abs(f[u] - f[v]) for u, v in G.edges())
        assert induced == list(range(1, q + 1))
        print(f" {k:4d} {G.number_of_nodes():4d} {q:4d}  {name:13s} {lam:6d} {fh:5d} {lam-fh:12d}")
        print(f"        labels: {dict(sorted(f.items(), key=lambda kv: str(kv[0])))}")
    print("\nTheorem 13 gives lambda <= 2r with r = 2, i.e. lambda <= 4;")
    print("Corollary 14 then gives k <= 4, and k = 5 is infeasible above.")


def remark18(kmax=9):
    """Remarks 17 and 18: Amal(C_m, v, k) = C_m^(k) for m = 8 and 12."""
    print("=== Remarks 17 and 18: C_8^(k) and C_12^(k) ===")
    for m in (8, 12):
        print(f"  --- C_{m}^(k) ---")
        largest = None
        for k in range(2, kmax + 1):
            G = amal(nx.cycle_graph(m), 0, k)
            t = time.time()
            name, f, lam = _alpha_with_status(G, tl=1800)
            print(f"   k={k:2d}  p={G.number_of_nodes():4d} q={G.number_of_edges():4d}"
                  f"  {name:12s} {'alpha' if f else '-':6s} ({time.time()-t:.1f}s)",
                  flush=True)
            if f:
                largest = k
            elif name == "INFEASIBLE":
                break
        print(f"   -> alpha for 2 <= k <= {largest}")


if __name__ == "__main__":
    job = sys.argv[1] if len(sys.argv) > 1 else "table4"
    t = time.time()
    {"table4": table4, "table5": table5, "remark18": remark18}[job]()
    print(f"\n[{time.time()-t:.0f}s]")
