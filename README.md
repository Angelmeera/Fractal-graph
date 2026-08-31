# Fractal Graphs and Graceful Labeling: A Computational Framework

## Overview

This repository presents a computational framework for investigating fractal constructions and graph labeling problems, with particular emphasis on **Iterated Function Systems (IFS)** and **graceful labeling techniques**. The work explores the intersection of fractal geometry and graph theory, providing implementations that bridge theoretical constructs with practical applications in communication networks and graph-theoretic optimization.

It accompanies the paper *On Graceful Labeling of Finite Approximation of Fractal Graphs*. The notebooks in Part 1 build and illustrate the fractal graphs and their labelings; the scripts in Part 2 reproduce the exhaustive computations behind the paper's tables and claims, each printing the numbers that appear in the text so that any result can be checked directly.

## Research Context

Fractal structures exhibit self-similarity across scales and have proven valuable in modeling complex systems. The Vicsek fractal, introduced by Vicsek (1983) [1], provides a deterministic model for diffusion-controlled aggregation, while the Heighway Dragon curve, analyzed comprehensively by Ngai and Nguyen (2003) [2], demonstrates intricate space-filling properties. This repository extends these classical fractals into the domain of graph theory through graceful labeling — a fundamental problem in graph theory with applications in communication network design, frequency assignment, and channel allocation.

---

# Part 1 — Construction and labeling notebooks

### 1. `Graceful_labeling_of_Viscek_fractal.ipynb`

Application of graceful and odd graceful labeling techniques to the Vicsek fractal graph.

- Recursive construction of the Vicsek fractal graph through iterative subdivision
- Implementation of graceful labeling algorithms via constraint programming
- Extension to odd graceful labeling schemes
- Applications to communication network design, including frequency assignment and channel allocation

**Theoretical significance.** Graceful labeling of fractal graphs provides structured approaches to resource allocation in hierarchical network topologies, leveraging the self-similar properties of fractals for efficient design patterns.

### 2. `Heighway_Dragon.ipynb`

The Heighway Dragon curve via L-system formalism, as both a fractal object and a graph.

- L-system generation of the Heighway Dragon curve
- Iterative fractal construction with visualization at multiple depths
- Graph-theoretic representation of the dragon curve
- Graceful labeling of the coordinate-identified dragon graph

**Research direction.** The dragon curve presents unique challenges for graceful labeling due to its non-lattice structure, offering opportunities for developing labeling strategies for irregular fractal graphs.

### 3. `Viscek_Fractal.ipynb`

Foundational treatment of the Vicsek fractal using Iterated Function Systems.

- Mathematical formulation of the IFS defining the Vicsek fractal (saltire form)
- Computational generation with multi-scale visualizations
- Geometric and topological analysis

### 4. `Fibonacci_word_fractal.ipynb`

Generation and visualization of the Fibonacci word fractal.

- Fibonacci words *W_n* by symbolic substitution
- Construction of the curve by the odd–even turning rule
- Visualization at successive orders

The odd graceful labeling of the induced path, and the self-avoidance verification the paper relies on, are implemented in `fibonacci.py` (Part 2).

---

# Part 2 — Verification scripts

These reproduce the computations in Sections 3.5 and 3.6 and the Fibonacci self-avoidance sweep cited in Proposition 3 and Remark 4.

| script | reproduces |
|---|---|
| `vicsek.py alpha` | V₀, V₁ and V₂ admit α-labelings — the verified base of Corollary 21 |
| `vicsek.py labelings` | all three labeling models of Algorithm 1 (graceful, odd graceful, α) on V_d, *d* ≤ 2 |
| `vicsek.py d3` | the honest negative at *d* = 3 (*p* = 376, *q* = 500): CP-SAT returns UNKNOWN, as the paper records |
| `vicsek.py prop6` | Proposition 6's structural claims for *d* = 0…3: 5^d blocks all C₄, *p* = 3·5^d + 1, *q* = 4·5^d, cycle rank 5^d, bipartite |
| `vicsek.py boundaries` | p. 24: the boundaries λ attained by α-labelings of V₀, V₁, V₂ — including that for V₁ every λ permitted by (2) is attained |
| `census.py table6` | Table 6: all C₄-cacti *b* = 1…7 (1, 1, 3, 7, 25, 88, 366) with α-counts (…, 24, 87, 365), Δ ≤ 4 counts to *b* = 9, and a check that every non-α graph found really is C₄⁽ᵇ⁾ |
| `census.py remark28` | Remark 28: C₈- and C₁₂-cacti with Δ ≤ 4 and at most 4 blocks (1, 1, 4, 15 and 1, 1, 6, 33), all α |
| `census.py snakes` | last column of Table 6, against Theorem 4.1 of Barrientos, *Alpha labeling of amalgamated cycles* [59] |
| `alpha_search.py table4` | Table 4: Amal(K₂,ᵣ, *h*, *m*) for *r* = 2, 3, 4 — prints the CP-SAT status, so the negatives can be seen to be completed INFEASIBLE proofs rather than time-outs |
| `alpha_search.py table5` | Table 5: α-labelings of C₄⁽ᵏ⁾ for *k* ≤ 4 with λ, *f*(*h*), λ − *f*(*h*), and the INFEASIBLE result at *k* = 5 — the computational content of Corollaries 15 and 16 |
| `alpha_search.py remark18` | Remarks 17 and 18: the α ranges for C₈⁽ᵏ⁾ and C₁₂⁽ᵏ⁾ |
| `claim24.py` | Claim 24 over all 618 pairs (*G*, *c*) with *b* ≤ 6, reported **per pattern**; also the exhaustiveness argument of Remark 23 |
| `spectral.py cor8` | Corollary 8: multiplicity of eigenvalue 2 in *L*(*V_d*) — 5, 20, 100 at *d* = 1, 2, 3 |
| `spectral.py aut` | Remark 10: \|Aut(*V_d*)\| = 2^(5^d + 2) for *d* = 0…4, i.e. 2³, 2⁷, 2²⁷, 2¹²⁷, 2⁶²⁷ |
| `spectral.py prop29` | Proposition 29: both pairs of spectral identities, checked numerically |
| `spectral.py remark30 N` | Remark 30: range of ρ(*A_f*) and λ₂(*L_f*) over *N* graceful labelings of *V*₁ |
| `spectral.py ks1` | Remark 30: ρ(*A_f*) over the graceful labelings of KS₁ = C₁₂ |
| `spectral.py integrality` | Remark 30: no graceful labeling of *P*₅, *P*₆, *C*₄, *C*₈ gives an integral *L_f* spectrum |
| `spectral.py rhominus` | Remark 30: the Lemma 1 labeling attains ρ⁻(*P*_{q+1}) for *q* = 3…7 but not *q* = 8 |
| `paths.py all` | Proposition 3's control sweeps in exact integer arithmetic: von Koch to 4⁹, arrowhead to 3¹³, Hilbert to 4¹⁰ − 1 edges |
| `fibonacci.py selfavoiding N` | Proposition 3 / Remark 4: self-avoidance of the curve of the Fibonacci word *W_n* for every *n* ≤ *N* |
| `fibonacci.py oddgraceful N` | odd graceful labeling of the Fibonacci word fractal, e.g. order 11, where \|*W*₁₁\| = *F*₁₁ = 89 edges and the induced labels are {1, 3, …, 177} |
| `ifs.py` | renders and audits all six IFS displays: ratio, rotation and translation of every map, the attractor, and its box-counting dimension |

`common.py` holds the shared constructions (V_d, the coordinate-identified Heighway dragon, vertex amalgamation, the cactus censuses) and all three CP-SAT models of Algorithm 1 — graceful, odd graceful, and α. Every labeling a solver returns is re-checked independently for injectivity, range and induced-label set, as Algorithm 1 line 21 requires: `check_graceful` against {1, …, q} and `check_odd_graceful` against {1, 3, …, 2q − 1}.

## Notes on reproducibility

**Censuses are exact.** Isomorphism rejection buckets candidates by Weisfeiler–Lehman hash and then runs an exact `networkx.is_isomorphic` test inside each bucket, so the hash only narrows the comparison and never decides it.

**Negative results are proofs, not time-outs.** `alpha_search.py` prints the CP-SAT status for every instance; `INFEASIBLE` means the search space was exhausted. Where the solver genuinely does not finish, the status is `UNKNOWN` and the script says so rather than reporting a negative — `vicsek.py d3` is the one case in the paper where that happens.

**Δ(V₀) = 2, not 4.** `vicsek.py prop6` prints the maximum degree at each order and notes this: V₀ = C₄ has no cut vertex, so Proposition 6's maximum-degree claim holds for *d* ≥ 1. Every other clause of the proposition is asserted by the script for *d* = 0…3.

**`claim24.py` reports each pattern separately** rather than stopping at the first that fits, and it tests four arrangements rather than the two Lemma 22 states. The two extra ones are the arrangements Remark 23 excludes, which require η = λ to be a label unused by *f*′; the script also verifies directly that no α-labeling of a C₄-cactus omits λ, so those two columns come out zero. That is Remark 23's exhaustiveness argument in computational form.

**Exact arithmetic for the lattice sweeps.** `paths.py` puts the von Koch and arrowhead curves on the triangular lattice as Eisenstein integers *a* + *b*ω, ω = exp(iπ/3), and the Hilbert curve on the square lattice, so deciding whether two vertices coincide involves no floating-point tolerance at all. `fibonacci.py` does the same on the square lattice.

**`spectral.py remark30` is sample-dependent by nature.** The set of labelings returned by the solver depends on version, seed and thread count, so any interval quoted from it should be reported together with the sample size the script prints. A single worker is used, which is required for exhaustive enumeration.

**`ifs.py` is the audit that catches a mistyped coefficient.** A wrong contraction ratio turns the attractor into a disconnected dust, visible both in the render and in the box-counting dimension. Expected dimensions: Sierpiński arrowhead ln 3 / ln 2 ≈ 1.585, Vicsek ln 5 / ln 3 ≈ 1.465, von Koch curve ln 4 / ln 3 ≈ 1.262, dragon and Hilbert 2, and the seven-map system of [40] 2 — that last one is the *filled* Koch snowflake region, whereas the graph KSₙ that is labeled is its boundary cycle C₃·₄ⁿ. The third arrowhead map is stated with ratio 1/3 in [51]; `ifs.py` uses the corrected 1/2, as the dimension ln 3 / ln 2 and the vertex count 3ⁿ + 1 recorded there require.

## Approximate running times

Single modern core, `ortools` 9.x:

    vicsek.py prop6               ~1 s
    vicsek.py boundaries          ~10 min (V_2 dominates)
    paths.py all                  ~3 s
    vicsek.py alpha               ~20 s
    vicsek.py labelings           ~35 s
    vicsek.py d3                  its own time limit (UNKNOWN expected)
    census.py snakes              ~10 s
    census.py table6              ~10 min  (b = 7 dominates)
    census.py remark28            ~5 min
    alpha_search.py table5        ~1 s
    alpha_search.py table4        ~2 min
    alpha_search.py remark18      ~45 min (the slowest job; C_8^(7) alone takes ~6 min)
    claim24.py 4                  ~10 s
    claim24.py 6                  ~25 min
    spectral.py cor8              ~1 s
    spectral.py aut               ~2 s (with nauty)
    spectral.py ks1               ~40 s
    spectral.py rhominus          ~1 s
    spectral.py remark30          bounded by its own time limit
    fibonacci.py selfavoiding 30  ~5 s
    ifs.py                        ~1 min

## Dependencies

```bash
pip install numpy matplotlib networkx ortools
```

`spectral.py aut` additionally needs **nauty** for the automorphism orders, since |Aut(V₄)| = 2⁶²⁷ cannot be reached by enumerating group elements:

```bash
apt-get install nauty     # or: brew install nauty
```

Without it that one check falls back to enumeration and reports only *d* ≤ 1; everything else runs on the pip packages alone.

- `numpy` — numerical computations and array operations
- `matplotlib` — visualization of fractals and graph structures
- `networkx` — graph construction and analysis
- `ortools` — constraint programming (CP-SAT) for the labeling searches

## References

[1] Vicsek, T. (1983). Fractal models for diffusion controlled aggregation. *Journal of Physics A: Mathematical and General*, 16(17), L647. https://doi.org/10.1088/0305-4470/16/17/003

[2] Ngai, S.-M., & Nguyen, N. T. (2003). The Heighway Dragon Revisited. *Discrete & Computational Geometry*, 29, 603–623. https://api.semanticscholar.org/CorpusID:8236024

[3] Monnerot-Dumaine, A. (2009). The Fibonacci Word Fractal. HAL Open Science, hal-00367972. https://hal.science/hal-00367972

## Author

**Angel Meera**
Indian Institute of Information Technology, Lucknow
[Scholar Profile](https://iiitl.ac.in/index.php/personnel/angel-meera/)

## Citation

If you use this code in your research, please cite this repository and acknowledge the foundational works referenced above.

---

*This repository is part of ongoing research in fractal geometry, graph theory, and their applications to network optimization problems.*
