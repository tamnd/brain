---
title: "Auto Diff"
description: "Auto Diff book notes exported from ChatGPT, organized into 22 chapters."
tags: ["autodiff", "book"]
draft: false
---

# Auto Diff

| Chapter | Title | Description |
|---|---|---|
| Index | [Index](00/) | Automatic differentiation works naturally on pure mathematical functions: |
| 1 | [Chapter 1. AutoDiff - Chapter 1](01/) | Derivative computation is not only a mathematical problem. It is also a numerical and systems problem. A derivative method must answer three questions simultaneously: |
| 2 | [Chapter 2. AutoDiff - Chapter 2](02/) | Automatic differentiation begins with a simple object: a function. |
| 3 | [Chapter 3. AutoDiff - Chapter 3](03/) | Automatic differentiation reduces a program to elementary operations. An elementary operation is a primitive computation whose derivative rule is known locally. |
| 4 | [Chapter 4. AD as Program Transformation](04/) | Automatic differentiation can be understood as a transformation from one program into another program. |
| 5 | [Chapter 5. AutoDiff - Chapter 5](05/) | Forward mode automatic differentiation appears in many numerical systems where directional derivatives, local sensitivities, or small parameter sets are important. This... |
| 6 | [Chapter 6. AutoDiff - Chapter 6](06/) | Checkpointing is a technique for reducing the memory cost of reverse mode automatic differentiation by selectively storing intermediate states and recomputing missing values... |
| 7 | [Chapter 7. AutoDiff - Chapter 7](07/) | Automatic differentiation is deeply connected to functional programming and lambda calculus. Programs can be viewed as mathematical functions, and differentiation can be... |
| 8 | [Chapter 8. AutoDiff - Chapter 8](08/) | Nested automatic differentiation means applying automatic differentiation inside another automatic differentiation computation. |
| 9 | [Chapter 9. AutoDiff - Chapter 9](09/) | A conditional is a program construct that chooses one computation among several possible computations. In ordinary code, this is written as if, else, switch, case, pattern... |
| 10 | [Chapter 10. AutoDiff - Chapter 10](10/) | Linear algebra primitives are tensor operations with algebraic structure: matrix multiplication, triangular solves, factorizations, inverses, determinants, norms, and spectral... |
| 11 | [Chapter 11. AutoDiff - Chapter 11](11/) | Kernel fusion combines several small operations into one larger executable unit. |
| 12 | [Chapter 12. AutoDiff - Chapter 12](12/) | Differentiable programming treats differentiation as a general programming-language feature. A program can contain numerical kernels, control flow, data structures, solvers,... |
| 13 | [Chapter 13. AutoDiff - Chapter 13](13/) | Neural network training is the repeated application of three operations: evaluate a model, differentiate a scalar loss, and update parameters. Automatic differentiation... |
| 14 | [Chapter 14. AutoDiff - Chapter 14](14/) | An end-to-end differentiable pipeline is a computational system where gradients propagate through the entire chain of computation, from raw inputs to final objectives. |
| 15 | [Chapter 15. AutoDiff - Chapter 15](15/) | A differentiable physics engine computes gradients of physical simulation outputs with respect to inputs, parameters, or control signals. Instead of treating simulation as a... |
| 16 | [Chapter 16](16/) | A differentiable physics engine computes gradients of physical simulation outputs with respect to inputs, parameters, or control signals. Instead of treating simulation as a... |
| 17 | [Chapter 17. AutoDiff - Chapter 17](17/) | Automatic differentiation systems are often assumed to be deterministic. Given identical inputs, identical parameters, and identical code, many users expect identical... |
| 18 | [Chapter 18. AutoDiff - Chapter 18](18/) | Automatic differentiation began as a transformation applied to numerical programs. A differentiable programming language instead treats differentiation as a native semantic... |
| 19 | [Chapter 19. AutoDiff - Chapter 19](19/) | Automatic differentiation systems are trusted infrastructure. Scientific computing, machine learning, optimization, simulation, and control systems depend on gradients being... |
| 20 | [Chapter 20. AutoDiff - Chapter 20](20/) | A minimal automatic differentiation engine can compute correct gradients on small programs. A production system must survive long-running workloads, large tensors, distributed... |
| 21 | [Chapter 21. Differentiation of Large Stateful Systems](21/) | Automatic differentiation works naturally on pure mathematical functions: |
| 22 | [Chapter 22. Differentiation of Large Stateful Systems](22/) | Automatic differentiation works naturally on pure mathematical functions: |
| Appendix | [Appendix](app/) | Automatic differentiation works naturally on pure mathematical functions: |
