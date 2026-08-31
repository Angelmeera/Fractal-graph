"""
Table 6  -- exhaustive census of C_4-cacti and their alpha-labelings.
Remark 28 -- the same for C_8- and C_12-cacti with at most 4 blocks.

Usage:
    python census.py table6      # Table 6 (all C_4-cacti to b=7, Delta<=4 to b=9)
    python census.py remark28    # Remark 28 (C_8 and C_12, b<=4)
    python census.py snakes      # the last column of Table 6

Reproduces:
    all C_4-cacti      b = 1..7 :   1,  1,  3,  7, 25, 88, 366
      of which alpha           :   1,  1,  3,  7, 24, 87, 365
      each failure is C_4^(b), the only exception (Corollary 15)
    Delta <= 4         b = 1..9 :   1,  1,  2,  4, 11, 30, 96, 319, 1135
      all alpha (Conjecture 20)
    C_4-snakes         b = 1..9 :   1,  1,  2,  3,  6, 10, 20,  36,   72
      matching  (1/2)(2^(b-2) + 2^floor((b-1)/2))  for b >= 2, which is
      Theorem 4.1 of Barrientos, "Alpha labeling of amalgamated cycles",
      Theory Appl. Graphs 9(2), 11 (2022)  [reference [59] of the paper]
"""
import sys, time
import networkx as nx
from common import cactus_census, has_alpha, is_snake, C4k


def table6(bmax_all=7, bmax_d4=9):
    print("=== Table 6: all C_4-cacti ===")
    A = cactus_census(bmax_all, 4, delta_le4_only=False)
    print("=== Table 6: C_4-cacti with Delta <= 4 ===")
    D = cactus_census(bmax_d4, 4, delta_le4_only=True)

    print("\n b |   all    alpha  not-alpha |  Delta<=4   alpha  not-alpha | snakes")
    for b in range(1, max(bmax_all, bmax_d4) + 1):
        row = [f"{b:2d} |"]
        for coll, bmax in ((A, bmax_all), (D, bmax_d4)):
            if b not in coll:
                row.append(f"{'-':>8} {'-':>7} {'-':>10} |")
                continue
            al = 0
            bad = []
            for G in coll[b]:
                r = has_alpha(G)
                if r is True:
                    al += 1
                else:
                    bad.append((G, r))
            row.append(f"{len(coll[b]):8d} {al:7d} {len(bad):10d} |")
            for G, r in bad:
                assert r is not None, "solver did not finish"
                assert nx.is_isomorphic(G, C4k(b)), "a non-alpha graph is not C_4^(b)"
        row.append(f"{sum(1 for G in D.get(b, []) if is_snake(G)):6d}"
                   if b in D else f"{'-':>6}")
        print(" ".join(row), flush=True)
    print("\nEvery non-alpha graph found was isomorphic to C_4^(b)  (checked, not assumed).")


def remark28():
    for m in (8, 12):
        print(f"=== Remark 28: C_{m}-cacti with Delta <= 4, at most 4 blocks ===")
        D = cactus_census(4, m, delta_le4_only=True)
        for b in sorted(D):
            res = [has_alpha(G, tl=600) for G in D[b]]
            print(f"  b={b}: {len(D[b]):3d} graphs, alpha: {sum(1 for r in res if r is True):3d},"
                  f" not alpha: {sum(1 for r in res if r is False):3d},"
                  f" unfinished: {sum(1 for r in res if r is None):3d}", flush=True)


def snakes(bmax=9):
    print("=== C_4-snake counts vs Barrientos, Alpha labeling of "
          "amalgamated cycles, Thm 4.1 ===")
    D = cactus_census(bmax, 4, delta_le4_only=True, verbose=False)
    print("  b   counted   formula")
    for b in sorted(D):
        c = sum(1 for G in D[b] if is_snake(G))
        f = 1 if b == 1 else (2 ** (b - 2) + 2 ** ((b - 1) // 2)) // 2
        flag = "" if c == f else "   <-- MISMATCH"
        print(f" {b:2d} {c:9d} {f:9d}{flag}")


if __name__ == "__main__":
    job = sys.argv[1] if len(sys.argv) > 1 else "table6"
    t = time.time()
    {"table6": table6, "remark28": remark28, "snakes": snakes}[job]()
    print(f"\n[{time.time() - t:.0f}s]")
