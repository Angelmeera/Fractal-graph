# Computational verification code

Scripts reproducing the computations reported in *On Graceful Labeling of
Finite Approximation of Fractal Graphs*. Each script prints the numbers that
appear in the paper, so a reader can check any table or claim directly.

These cover Sections 3.5 and 3.6, which the existing notebooks in this
repository do not, plus the Fibonacci self-avoidance sweep cited in
Proposition 3 and Remark 4.

## Requirements

    pip install networkx numpy ortools matplotlib

## Script → claim

| script | reproduces |
|---|---|
| `census.py table6` | Table 6: all C₄-cacti *b* = 1…7 (1, 1, 3, 7, 25, 88, 366) with α-counts (…, 24, 87, 365), Δ ≤ 4 counts to *b* = 9, and a check that every non-α graph found really is C₄⁽ᵇ⁾ |
| `census.py remark28` | Remark 28: C₈- and C₁₂-cacti with Δ ≤ 4 and at most 4 blocks (1, 1, 4, 15 and 1, 1, 6, 33), all α |
| `census.py snakes` | last column of Table 6, against Theorem 4.1 of [56] |
| `alpha_search.py table4` | Table 4: Amal(K₂,ᵣ, *h*, *m*) for *r* = 2, 3, 4 — prints the CP-SAT status, so the negatives can be seen to be completed INFEASIBLE proofs rather than time-outs |
| `alpha_search.py table5` | Table 5: α-labelings of C₄⁽ᵏ⁾ for *k* ≤ 4 with λ, *f*(*h*), λ − *f*(*h*), and the INFEASIBLE result at *k* = 5 (Corollary 15) |
| `claim24.py` | Claim 24 over all 618 pairs (*G*, *c*) with *b* ≤ 6, reported **per pattern** |
| `spectral.py cor8` | Corollary 8: multiplicity of eigenvalue 2 in *L*(*V_d*) — 5, 20, 100 at *d* = 1, 2, 3 |
| `spectral.py aut` | Remark 10: \|Aut(*V*₀)\| = 2³, \|Aut(*V*₁)\| = 2⁷ |
| `spectral.py prop29` | Proposition 29: both pairs of spectral identities, checked numerically |
| `spectral.py remark30 N` | Remark 30: range of ρ(*A_f*) and λ₂(*L_f*) over *N* graceful labelings of *V*₁ |
| `spectral.py integrality` | Remark 30: no graceful labeling of *P*₅, *P*₆, *C*₄, *C*₈ gives an integral *L_f* spectrum |
| `spectral.py rhominus` | Remark 30: the Lemma 1 labeling attains ρ⁻(*P*_{q+1}) for *q* = 3…7 but not *q* = 8 |
| `fibonacci.py selfavoiding N` | Proposition 3 / Remark 4: self-avoidance of the Fibonacci word curve for every *n* ≤ *N* |
| `fibonacci.py oddgraceful N` | odd graceful labeling of the Fibonacci word fractal (Lemma 2), e.g. *F*₁₁ with 89 edges and induced labels {1, 3, …, 177} |
| `ifs.py` | renders and audits all six IFS displays: ratio, rotation and translation of every map, the attractor, and its box-counting dimension |

`common.py` holds the shared constructions (V_d, the coordinate-identified
Heighway dragon, vertex amalgamation, the cactus censuses) and the two CP-SAT
models of Algorithm 1. Every labeling a solver returns is re-checked
independently for injectivity, range and induced-label set, as Algorithm 1
line 21 requires.

## Notes on reproducibility

**Censuses are exact.** Isomorphism rejection buckets by Weisfeiler–Lehman
hash and then runs an exact `nx.is_isomorphic` test inside each bucket, so the
hash is only used to narrow the comparison, never to decide it.

**Negative results are proofs, not time-outs.** `alpha_search.py` prints the
CP-SAT status for every instance. `INFEASIBLE` means the search space was
exhausted.

**`claim24.py` reports each pattern separately** rather than stopping at the
first one that fits. Two of the four patterns of Lemma 22 as originally
printed require η = λ to be a label unused by *f*′, which no α-labeling
permits: the induced label 1 forces the vertices labeled λ and λ + 1 to be
adjacent. Those two columns come out identically zero. The script also
verifies directly that no α-labeling of a C₄-cactus omits the label λ.

**`spectral.py remark30` is sample-dependent by nature.** The set of labelings
returned by the solver depends on version, seed and thread count, so any
interval quoted from it should be reported together with the sample size the
script prints. The script uses a single worker, which is required for
exhaustive enumeration.

**`ifs.py` is the audit that catches a mistyped coefficient.** A wrong
contraction ratio turns the attractor into a disconnected dust, which shows up
both in the render and in the box-counting dimension. Expected dimensions:
arrowhead ln 3 / ln 2 ≈ 1.585, Vicsek ln 5 / ln 3 ≈ 1.465, von Koch curve
ln 4 / ln 3 ≈ 1.262, dragon and Hilbert 2, and the seven-map Koch snowflake
system 2 — that last one is the *filled* region, whereas the graph KS_n
labeled in the paper is its boundary cycle C_{3·4ⁿ}.

## Approximate running times

Single modern core, `ortools` 9.x:

    census.py snakes            ~10 s
    census.py table6            ~10 min  (b = 7 dominates)
    census.py remark28          ~5 min
    alpha_search.py table5      ~1 s
    alpha_search.py table4      ~2 min
    claim24.py 4                ~10 s
    claim24.py 6                ~25 min
    spectral.py cor8            ~1 s
    spectral.py rhominus        ~1 s
    spectral.py remark30        bounded by its own time limit
    fibonacci.py selfavoiding 30  ~5 s
    ifs.py                      ~1 min
