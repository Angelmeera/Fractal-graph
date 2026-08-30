"""
Renders and audits every iterated function system displayed in the paper.

Usage:
    python ifs.py            # audit all six, write PNGs to ./figures/
    python ifs.py arrowhead  # one system only

For each system the script prints the contraction ratio and rotation of every
map, renders the attractor by the chaos game, and (where the attractor should
be a curve) estimates its box-counting dimension.  This is the check that
catches a mistyped coefficient: a wrong ratio turns the attractor into a
disconnected dust, which is obvious in the render and in the dimension.

NOTE on the Koch snowflake: the seven maps of [40] have as attractor the
FILLED snowflake region (box dimension 2), as the paper now states.  The graph
KS_n that is labeled is its BOUNDARY, the cycle C_{3*4^n}, obtained by applying
the four von Koch maps to each of the three sides.
"""
import os, sys, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

S3 = math.sqrt(3)


def R(t):
    c, s = math.cos(t), math.sin(t)
    return np.array([[c, -s], [s, c]])


def M(a, b, c, d, e, f):
    return (np.array([[a, b], [c, d]]), np.array([e, f]))


SYSTEMS = {
    # Sierpinski arrowhead: three similarities of ratio 1/2, rotations -120, 0, +120.
    # The third map is stated with ratio 1/3 in [51]; corrected here to 1/2, as
    # required by the dimension ln3/ln2 and the vertex count 3^n + 1 given there.
    "arrowhead": [
        M(-1/4,  S3/4, -S3/4, -1/4, 1/4, S3/4),
        M( 1/2,  0.0,   0.0,   1/2, 1/4, S3/4),
        M(-1/4, -S3/4,  S3/4, -1/4, 1.0, 0.0),
    ],
    "von_koch_curve": [
        M(1/3, 0, 0, 1/3, 0, 0),
        M(1/6, -S3/6, S3/6, 1/6, 1/3, 0),
        M(1/6,  S3/6, -S3/6, 1/6, 1/2, S3/6),
        M(1/3, 0, 0, 1/3, 2/3, 0),
    ],
    "heighway_dragon": [
        M(1/2, -1/2, 1/2, 1/2, 0, 0),
        M(-1/2, -1/2, 1/2, -1/2, 1, 0),
    ],
    "hilbert": [
        M(0, 1/2, 1/2, 0, -1/4, -1/4),
        M(1/2, 0, 0, 1/2, -1/4, 1/4),
        M(1/2, 0, 0, 1/2, 1/4, 1/4),
        M(0, -1/2, -1/2, 0, 1/4, -1/4),
    ],
    "vicsek": [
        M(1/3, 0, 0, 1/3, 1/3, 1/3),
        M(1/3, 0, 0, 1/3, 0, 2/3),
        M(1/3, 0, 0, 1/3, 0, 0),
        M(1/3, 0, 0, 1/3, 2/3, 0),
        M(1/3, 0, 0, 1/3, 2/3, 2/3),
    ],
    # attractor is the FILLED snowflake region, not the boundary cycle KS_n
    "koch_snowflake_region": [
        (0.5 * R(math.pi / 6) / math.cos(math.pi / 6), np.array([0.0, 0.0])),
    ] + [M(1/3, 0, 0, 1/3, *o) for o in
         [(1/S3, 1/3), (0, 2/3), (-1/S3, 1/3), (-1/S3, -1/3), (0, -2/3), (1/S3, -1/3)]],
}


def attractor(maps, n=250000, seed=1):
    rng = np.random.default_rng(seed)
    p = np.zeros(2)
    for _ in range(500):
        A, t = maps[rng.integers(len(maps))]
        p = A @ p + t
    P = np.empty((n, 2))
    for i in range(n):
        A, t = maps[rng.integers(len(maps))]
        p = A @ p + t
        P[i] = p
    return P


def box_dimension(P):
    span = max(P.max(0) - P.min(0))
    Q = (P - P.min(0)) / span
    out = []
    for k in (4, 5, 6, 7, 8):
        eps = 2.0 ** -k
        boxes = len({tuple(v) for v in np.floor(Q / eps).astype(int)})
        out.append((eps, boxes))
    dims = [math.log(b2 / b1) / math.log(2)
            for (_, b1), (_, b2) in zip(out, out[1:])]
    return dims


def audit(name, maps, outdir="figures"):
    print(f"=== {name} ===")
    for i, (A, t) in enumerate(maps):
        r = math.sqrt(abs(np.linalg.det(A)))
        rot = math.degrees(math.atan2(A[1, 0], A[0, 0]))
        print(f"   w{i}: ratio {r:.6f}  rotation {rot:8.2f} deg  "
              f"translation ({t[0]:+.4f}, {t[1]:+.4f})")
    P = attractor(maps)
    dims = box_dimension(P)
    print("   box-counting dimension estimates: "
          + ", ".join(f"{d:.3f}" for d in dims))
    os.makedirs(outdir, exist_ok=True)
    plt.figure(figsize=(5, 5))
    plt.scatter(P[:, 0], P[:, 1], s=0.05, c="k", linewidths=0)
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.savefig(f"{outdir}/{name}.png", dpi=110, bbox_inches="tight")
    plt.close()
    print(f"   -> {outdir}/{name}.png\n")


if __name__ == "__main__":
    which = sys.argv[1:] or list(SYSTEMS)
    for name in which:
        audit(name, SYSTEMS[name])
