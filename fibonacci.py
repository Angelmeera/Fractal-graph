"""
Remark 4 / Proposition 3 -- self-avoidance of the Fibonacci word curve,
verified for every n <= 36, and the odd graceful labeling of the resulting
path (Lemma 2).

Usage:
    python fibonacci.py selfavoiding [NMAX]   # default 30; 36 needs ~2 GB
    python fibonacci.py oddgraceful  [N]      # odd graceful labeling of F_n

Drawing rule (Monnerot-Dumaine [35], p.2):
    each digit draws a unit segment FORWARD; after a 0, the heading turns
    left if that digit's index is even and right if it is odd, while a 1
    leaves the heading unchanged.  The turn conditions the NEXT segment.
"""
import sys, time
import numpy as np


def fibonacci_word(n):
    """W_n, with W_1 = 1, W_2 = 0, W_n = W_{n-1} W_{n-2}; |W_n| = F_n."""
    if n == 1:
        return "1"
    if n == 2:
        return "0"
    a, b = "1", "0"
    for _ in range(3, n + 1):
        a, b = b, b + a
    return b


def curve_points(word):
    """Vertices visited, as an (m+1, 2) int array, starting at (0,0) facing up."""
    w = np.frombuffer(word.encode(), dtype=np.uint8) - ord('0')
    m = w.size
    idx = np.arange(1, m + 1)
    # turn AFTER drawing digit i: +1 (left) if digit 0 and i even, -1 if digit 0 and i odd
    turn = np.where(w == 0, np.where(idx % 2 == 0, 1, -1), 0).astype(np.int64)
    head = np.empty(m, dtype=np.int64)
    head[0] = 1                                  # 0:right 1:up 2:left 3:down
    if m > 1:
        head[1:] = (1 + np.cumsum(turn[:-1])) % 4
    head %= 4
    dx = np.array([1, 0, -1, 0])[head]
    dy = np.array([0, 1, 0, -1])[head]
    x = np.concatenate([[0], np.cumsum(dx)])
    y = np.concatenate([[0], np.cumsum(dy)])
    return np.stack([x, y], axis=1)


def selfavoiding(nmax=30):
    print("=== self-avoidance of the Fibonacci word curve ===")
    print("   n     |W_n| = F_n   vertices   distinct   self-avoiding?")
    for n in range(3, nmax + 1):
        w = fibonacci_word(n)
        P = curve_points(w)
        packed = (P[:, 0].astype(np.int64) << 32) ^ (P[:, 1].astype(np.int64) & 0xFFFFFFFF)
        distinct = np.unique(packed).size
        ok = distinct == P.shape[0]
        print(f"  {n:2d} {len(w):10d} {P.shape[0]:10d} {distinct:10d}   "
              f"{'yes' if ok else 'NO'}", flush=True)
        if not ok:
            print("  -> the curve is NOT self-avoiding at this order; the reduction")
            print("     to a path in Proposition 3 fails here.")
            return


def odd_graceful_path(p):
    """
    Odd graceful labeling of P_p by Lemma 2 applied to the zig-zag alpha-
    labeling of Lemma 1:  g(v) = 2f(v) if f(v) <= lambda, else 2f(v) - 1.
    """
    q = p - 1
    lab = []
    lo, hi = 0, q
    while len(lab) < p:
        lab.append(lo); lo += 1
        if len(lab) < p:
            lab.append(hi); hi -= 1
    f = {i: lab[i] for i in range(p)}
    # The zig-zag labeling puts 0, 1, ..., floor(q/2) on the even positions and
    # q, q-1, ... on the odd ones, so its boundary is lambda = floor(q/2).
    lam = q // 2
    assert lam == max(v for v in f.values() if v <= lam)
    assert all(f[i] <= lam for i in range(0, p, 2)) and \
           all(f[i] > lam for i in range(1, p, 2))
    g = {v: (2 * a if a <= lam else 2 * a - 1) for v, a in f.items()}
    return f, g, lam


def oddgraceful(n=11):
    w = fibonacci_word(n)
    P = curve_points(w)
    p = P.shape[0]
    q = p - 1
    packed = (P[:, 0].astype(np.int64) << 32) ^ (P[:, 1].astype(np.int64) & 0xFFFFFFFF)
    assert np.unique(packed).size == p, "curve is not self-avoiding at this order"
    print(f"=== order {n}: |W_{n}| = F_{n} = {len(w)} edges, {p} vertices,"
          f" abstractly P_{p} ===")
    f, g, lam = odd_graceful_path(p)
    induced = sorted(abs(g[i] - g[i + 1]) for i in range(p - 1))
    expect = list(range(1, 2 * q, 2))
    assert induced == expect, "induced labels are not {1,3,...,2q-1}"
    assert len(set(g.values())) == p and max(g.values()) <= 2 * q - 1
    print(f"  odd graceful: induced labels are exactly "
          f"{{1, 3, ..., {2*q-1}}}   verified")
    if p <= 40:
        print("  vertex labels along the path:",
              [g[i] for i in range(p)])
    else:
        print("  first 20 vertex labels:", [g[i] for i in range(20)], "...")


if __name__ == "__main__":
    job = sys.argv[1] if len(sys.argv) > 1 else "selfavoiding"
    arg = int(sys.argv[2]) if len(sys.argv) > 2 else None
    t = time.time()
    if job == "selfavoiding":
        selfavoiding(arg or 30)
    else:
        oddgraceful(arg or 11)
    print(f"\n[{time.time()-t:.0f}s]")
