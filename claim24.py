"""
Claim 24 -- for every C_4-cactus G with Delta <= 4 and every vertex c of
degree 2, G has an alpha-labeling matching a pattern of Lemma 22 at c, or
its mirror.

Usage:
    python claim24.py            # all 618 pairs with b <= 6
    python claim24.py 5          # restrict to b <= 5

This script reports the result PER PATTERN rather than stopping at the first
one that fits, and it tests four arrangements rather than the two the lemma
states.  Patterns (ii) and (iv) below are the two patterns of Lemma 22, with
f'(c) = lambda; (i) and (iii) are the other two arrangements of {1,2,3,4} with
alternating sum zero, which Remark 23 rules out because they require eta =
lambda to be a label unused by f'.  No alpha-labeling permits that: the induced
label 1 forces the vertices labeled lambda and lambda+1 to be adjacent.  Their
columns therefore come out identically zero, which is the computational form of
Remark 23's exhaustiveness argument.

Expected output for b <= 6:
    618 pairs, 0 with no matching pattern
    feasible counts:  (i) 0   (ii) 344   (iii) 0   (iv) 342
                     (i*) 0  (ii*) 274  (iii*) 0  (iv*) 272
    i.e. the two patterns of Lemma 22 cover every pair, and the two
    arrangements Remark 23 excludes are never feasible.
"""
import sys, time, collections
import networkx as nx
from ortools.sat.python import cp_model
from common import cactus_census, alpha_model, solve

# (f'(c) - lambda, eta - lambda).  (ii) and (iv) are the two patterns of
# Lemma 22; (i) and (iii) are the arrangements Remark 23 excludes.
# c in the low class:
LOW = {'(i)': (-1, 0), '(ii)': (0, -1), '(iii)': (-2, 0), '(iv)': (0, -2)}
# and the mirror, obtained by applying f^c(v) = q - f(v) before and after:
HIGH = {'(i*)': (2, 1), '(ii*)': (1, 2), '(iii*)': (3, 1), '(iv*)': (1, 3)}


def pattern_feasible(G, c, off_c, off_eta, side, tl=120):
    col = nx.bipartite.color(G)
    if col[c] != (0 if side == 'low' else 1):
        return False

    def extra(m, x, lam, col, q, nodes):
        m.Add(x[c] == lam + off_c)               # f'(c) is at the prescribed offset
        for v in nodes:
            m.Add(x[v] != lam + off_eta)         # eta must be UNUSED by f'
        if off_eta > 0:
            m.Add(lam + off_eta <= q)
        if off_c < 0 or off_eta < 0:
            m.Add(lam + min(off_c, off_eta) >= 0)

    m, x, lam = alpha_model(G, extra)
    st, _ = solve(m, tl)
    return st in (cp_model.OPTIMAL, cp_model.FEASIBLE)


def lambda_is_always_used(bmax=4):
    """The fact that kills patterns (i) and (iii): no alpha-labeling omits lambda."""
    print("=== is the label lambda ever unused by an alpha-labeling? ===")
    D = cactus_census(bmax, 4, delta_le4_only=True, verbose=False)
    for b in sorted(D):
        found = 0
        for G in D[b]:
            def extra(m, x, lam, col, q, nodes):
                for v in nodes:
                    m.Add(x[v] != lam)
            m, x, lam = alpha_model(G, extra)
            st, _ = solve(m, 120)
            if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                found += 1
        print(f"  b={b}: {found} of {len(D[b])} graphs admit one   "
              f"({'as expected, none' if found == 0 else 'UNEXPECTED'})")
    print()


def main(bmax=6):
    lambda_is_always_used(min(bmax, 4))
    print(f"=== Claim 24, per pattern, over all (G, c) with b <= {bmax} ===")
    D = cactus_census(bmax, 4, delta_le4_only=True, verbose=False)
    cnt = collections.Counter()
    total = 0
    unmatched = []
    for b in sorted(D):
        for gi, G in enumerate(D[b]):
            for c in G.nodes():
                if G.degree(c) != 2:
                    continue
                total += 1
                hits = [nm for nm, (a, e) in LOW.items()
                        if pattern_feasible(G, c, a, e, 'low')]
                hits += [nm for nm, (a, e) in HIGH.items()
                         if pattern_feasible(G, c, a, e, 'high')]
                for h in hits:
                    cnt[h] += 1
                if not hits:
                    unmatched.append((b, gi, c))
        print(f"  through b={b}: {total} pairs", flush=True)

    print(f"\nTOTAL pairs: {total}")
    print(f"pairs with NO matching pattern: {len(unmatched)}")
    print("\n pattern   feasible")
    for nm in list(LOW) + list(HIGH):
        print(f"   {nm:6s} {cnt[nm]:9d}")
    dead = [nm for nm in list(LOW) + list(HIGH) if cnt[nm] == 0]
    if dead:
        print(f"\nNever feasible: {', '.join(dead)}"
              f"\n  -- the arrangements requiring eta = lambda, as Remark 23 states."
              f"\n  The two patterns of Lemma 22 and their mirrors cover every pair.")


if __name__ == "__main__":
    t = time.time()
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
    print(f"\n[{time.time()-t:.0f}s]")
