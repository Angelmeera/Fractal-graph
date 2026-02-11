# Fractal Graphs and Graceful Labeling: A Computational Framework

## Overview

This repository presents a computational framework for investigating fractal constructions and graph labeling problems, with particular emphasis on **Iterated Function Systems (IFS)** and **graceful labeling techniques**. The work explores the intersection of fractal geometry and graph theory, providing implementations that bridge theoretical constructs with practical applications in communication networks and graph-theoretic optimization.

## Research Context

Fractal structures exhibit self-similarity across scales and have proven valuable in modeling complex systems. The Vicsek fractal, introduced by Vicsek (1983) [1], provides a deterministic model for diffusion-controlled aggregation, while the Heighway Dragon curve, analyzed comprehensively by Ngai and Nguyen (2003) [2], demonstrates intricate space-filling properties. This repository extends these classical fractals into the domain of graph theory through graceful labeling—a fundamental problem in graph theory with applications in communication network design, frequency assignment, and channel allocation.

## Repository Contents

### 1. `Graceful_labeling_of_Viscek_fractal.ipynb`

This notebook investigates the application of graceful and odd graceful labeling techniques to the Vicsek fractal graph structure.

**Key Features:**
- Recursive construction of the Vicsek fractal graph through iterative subdivision
- Implementation of graceful labeling algorithms
- Extension to odd graceful labeling schemes
- Applications to communication network design, including potential extensions for frequency assignment and channel allocation problems

**Theoretical Significance:**  
Graceful labeling of fractal graphs provides structured approaches to resource allocation in hierarchical network topologies, leveraging the self-similar properties of fractals for efficient design patterns.

### 2. `Heighway_Dragon.ipynb`

This notebook implements the Heighway Dragon curve using L-system formalism, exploring its properties as both a fractal object and a potential graph structure.

**Key Features:**
- L-system based generation of the Heighway Dragon curve
- Iterative fractal construction with visualization at multiple depths
- Graph-theoretic representation of the dragon curve
- Exploration of graceful labeling applicability to non-uniform fractal structures

**Research Direction:**  
The dragon curve presents unique challenges for graceful labeling due to its non-lattice structure, offering opportunities for developing novel labeling strategies for irregular fractal graphs.

### 3. `Viscek_Fractal.ipynb`

This notebook provides a foundational treatment of the Vicsek fractal using Iterated Function Systems.

**Key Features:**
- Mathematical formulation of the IFS defining the Vicsek fractal
- Computational generation with multi-scale visualizations
- Geometric and topological analysis
- Foundation for subsequent graph labeling experiments

**Mathematical Foundation:**  
The Vicsek fractal serves as an exemplar for studying how deterministic fractal rules translate into graph-theoretic properties, providing insights into the relationship between geometric self-similarity and combinatorial structure.

**###4. Fibonacci_Word_Fractal_Odd_Graceful.ipynb**

This notebook explores the Fibonacci word fractal and establishes an odd graceful labeling for the induced path graph.

**Key Features:**

-Generation of Fibonacci words using symbolic substitution rules
-Construction of the Fibonacci word fractal via deterministic turning rules
-Graph interpretation of the fractal curve as a path graph
-Explicit odd graceful vertex labeling and induced edge labeling
-Visualization with non-overlapping, scale-invariant labels

**Mathematical Significance:**
The Fibonacci word fractal provides a bridge between symbolic dynamics and graph labeling theory. Its recursive structure enables inductive proofs of odd graceful labeling and offers insight into labeling problems on self-similar path graphs.

**Research Relevance:** 
This construction is particularly relevant for:

-labeled path decompositions
-fractal graph limits
-recursive network topologies
-extensions to graceful, odd graceful, and α-labelings
 
## Dependencies

The computational framework requires the following Python packages:

```bash
pip install numpy matplotlib networkx ortools
```

**Package Descriptions:**
- `numpy`: Numerical computations and array operations
- `matplotlib`: Visualization of fractals and graph structures
- `networkx`: Graph construction and analysis
- `ortools`: Constraint programming and optimization (for labeling algorithms)

## References

[1] Vicsek, T. (1983). Fractal models for diffusion controlled aggregation. *Journal of Physics A: Mathematical and General*, 16(17), L647. https://doi.org/10.1088/0305-4470/16/17/003

[2] Ngai, S.-M., & Nguyen, N. T. (2003). The Heighway Dragon Revisited. *Discrete & Computational Geometry*, 29, 603-623. https://api.semanticscholar.org/CorpusID:8236024

[3] Monnerot-Dumaine, A. (2009). The Fibonacci Word Fractal. HAL Open Science. hal-00367972. https://hal.science/hal-00367972

## Author

**Angel Meera**  
Indian Institute of Information Technology, Lucknow  
[Scholar Profile](https://iiitl.ac.in/index.php/personnel/angel-meera/)

## Citation

If you use this code in your research, please cite this repository and acknowledge the foundational works referenced above.


*This repository is part of ongoing research in fractal geometry, graph theory, and their applications to network optimization problems.*
