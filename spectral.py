"""
Corollary 8  -- multiplicity of the eigenvalue 2 in the ordinary L(V_d).
Remark 10    -- |Aut(V_0)| and |Aut(V_1)|.
Proposition 29 -- the two pairs of spectral identities for L_f.
Remark 30    -- the range of rho(A_f) and lambda_2(L_f) over graceful
                labelings; Laplacian integrality; and rho^-(P_{q+1}).

Usage:
    python spectral.py cor8
    python spectral.py aut
    python spectral.py prop29
    python spectral.py remark30 [N]     # N labelings of V_1, default 100000
    python spectral.py integrality
    python spectral.py rhominus

Note on Remark 30: the interval depends on WHICH labelings are sampled.  The
first N returned by the solution callback depend on solver version, seed and
thread count, so a small sample is not reproducible to the printed digits.
This script enumerates as many as the time limit allows with a single worker
and reports the count alongside the interval, so the number quoted in the
paper can be stated with its sample size.
"""
import sys, time, itertools
import numpy as np
import networkx as nx
from ortools.sat.python import cp_model
from common import (vicsek_graph, graceful_model, weighted_matrices,
                    check_graceful)


def cor8(dmax=3):
    print("=== Corollary 8: multiplicity of eigenvalue 2 in L(V_d) ===")
    print("  d     p     q   mult(2)   4*5^(d-1)   5^d")
    for d in range(1, dmax + 1):
        G = vicsek_graph(d)
        L = nx.laplacian_matrix(G).todense().astype(float)
        ev = np.linalg.eigvalsh(L)
        mult = int(np.sum(np.abs(ev - 2) < 1e-8))
        print(f" {d:2d} {G.number_of_nodes():5d} {G.number_of_edges():5d}"
              f" {mult:9d} {4*5**(d-1):11d} {5**d:5d}", flush=True)
    print("\nThe bound of Corollary 8 is 4*5^(d-1); it is attained for d >= 2,")
    print("and the multiplicity is 5 rather than 4 at d = 1.")


def aut(dmax=1):
    print("=== Remark 10: automorphism counts ===")
    from networkx.algorithms.isomorphism import GraphMatcher
    for d in range(0, dmax + 1):
        G = vicsek_graph(d)
        n = sum(1 for _ in GraphMatcher(G, G).isomorphisms_iter())
        e = 5 ** d + 2
        print(f"  |Aut(V_{d})| = {n} = 2^{n.bit_length()-1}   "
              f"(e_d = 5^{d} + 2 = {e}; bound 2^(4*5^(d-1)+3) for d >= 1)")


def prop29(d=1, trials=5):
    print("=== Proposition 29: the spectral identities for L_f ===")
    G = vicsek_graph(d)
    q = G.number_of_edges()
    for f in _sample(G, trials, tl=30):
        A, L = weighted_matrices(G, f)
        ev = np.linalg.eigvalsh(L)
        s = A.sum(1)
        lhs1, rhs1 = ev.sum(), q * (q + 1)
        lhs2 = (ev ** 2).sum()
        rhs2 = (s ** 2).sum() + q * (q + 1) * (2 * q + 1) / 3
        print(f"  sum lambda_i = {lhs1:14.6f}   q(q+1) = {rhs1:14.6f}   "
              f"ok={abs(lhs1-rhs1) < 1e-6}")
        print(f"  sum lambda_i^2 = {lhs2:14.6f}   rhs = {rhs2:14.6f}   "
              f"ok={abs(lhs2-rhs2) < 1e-6}")


class _Cb(cp_model.CpSolverSolutionCallback):
    def __init__(self, x, nodes, cap, sink):
        super().__init__()
        self.x, self.nodes, self.cap, self.sink = x, nodes, cap, sink
        self.n = 0

    def on_solution_callback(self):
        self.n += 1
        self.sink({v: self.Value(self.x[v]) for v in self.nodes})
        if self.n >= self.cap:
            self.StopSearch()


def _sample(G, cap, tl=600, seed=0):
    out = []
    m, x = graceful_model(G)
    s = cp_model.CpSolver()
    s.parameters.enumerate_all_solutions = True
    s.parameters.num_search_workers = 1     # required for exhaustive enumeration
    s.parameters.max_time_in_seconds = tl
    s.parameters.random_seed = seed
    cb = _Cb(x, list(G.nodes()), cap, out.append)
    s.Solve(m, cb)
    return out


def remark30(cap=100000, tl=900):
    G = vicsek_graph(1)
    print(f"=== Remark 30: V_1, p={G.number_of_nodes()}, q={G.number_of_edges()} ===")
    t = time.time()
    S = _sample(G, cap, tl)
    rho = []
    l2 = []
    for f in S:
        A, L = weighted_matrices(G, f)
        rho.append(max(abs(np.linalg.eigvalsh(A))))
        l2.append(sorted(np.linalg.eigvalsh(L))[1])
    print(f"  labelings enumerated: {len(S)}   ({time.time()-t:.0f}s)")
    print(f"  rho(A_f)        in [{min(rho):.4f}, {max(rho):.4f}]")
    print(f"  lambda_2(L_f)   in [{min(l2):.4f}, {max(l2):.4f}]"
          f"   (ratio {max(l2)/min(l2):.2f})")
    print("\n  These are bounds observed on this sample, not the true extremes.")
    print("  Quote them together with the sample size printed above.")


def integrality():
    print("=== Remark 30: is any L_f spectrum integral? ===")
    cases = [("P_5", nx.path_graph(5)), ("P_6", nx.path_graph(6)),
             ("C_4", nx.cycle_graph(4)), ("C_8", nx.cycle_graph(8))]
    for name, G in cases:
        S = _sample(G, 10 ** 7, tl=300)
        bad = 0
        for f in S:
            _, L = weighted_matrices(G, f)
            ev = np.linalg.eigvalsh(L)
            if np.all(np.abs(ev - np.round(ev)) < 1e-7):
                bad += 1
        print(f"  {name:4s}: {len(S):6d} graceful labelings, "
              f"{bad} with integral L_f spectrum")


def rhominus(qmax=8):
    print("=== Remark 30: is the Lemma 1 labeling of P_{q+1} extremal for rho^-? ===")
    print("   q   Lemma 1 rho     true rho^-    extremal?   attaining labeling")
    for q in range(3, qmax + 1):
        p = q + 1
        G = nx.path_graph(p)
        # Lemma 1's zig-zag labeling 0, q, 1, q-1, 2, ...
        lab = []
        lo, hi = 0, q
        while len(lab) < p:
            lab.append(lo); lo += 1
            if len(lab) < p:
                lab.append(hi); hi -= 1
        f1 = {i: lab[i] for i in range(p)}
        A, _ = weighted_matrices(G, f1)
        r1 = max(abs(np.linalg.eigvalsh(A)))
        best, bestf = None, None
        for perm in itertools.permutations(range(q + 1), p):
            f = {i: perm[i] for i in range(p)}
            if sorted(abs(f[i] - f[i + 1]) for i in range(p - 1)) != list(range(1, q + 1)):
                continue
            A, _ = weighted_matrices(G, f)
            r = max(abs(np.linalg.eigvalsh(A)))
            if best is None or r < best - 1e-12:
                best, bestf = r, [f[i] for i in range(p)]
        ok = abs(r1 - best) < 1e-9
        print(f"  {q:2d} {r1:13.6f} {best:13.6f}   {'yes' if ok else 'NO ':9s}"
              f"  {'' if ok else bestf}")


if __name__ == "__main__":
    job = sys.argv[1] if len(sys.argv) > 1 else "cor8"
    t = time.time()
    if job == "remark30":
        remark30(int(sys.argv[2]) if len(sys.argv) > 2 else 100000)
    else:
        {"cor8": cor8, "aut": aut, "prop29": prop29,
         "integrality": integrality, "rhominus": rhominus}[job]()
    print(f"\n[{time.time()-t:.0f}s]")
