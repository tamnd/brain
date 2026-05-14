---
title: "Auto Diff"
description: "Auto Diff book notes, into 22 chapters."
tags: ["autodiff", "book"]
draft: false
---

# Auto Diff

| Chapter | Title | Description |
|---|---|---|
| 1 | [Chapter 1. Introduction](01/) | A derivative measures how an output changes when an input changes. That sentence is simple, but it is one of the main ideas behind numerical computing, optimization, machine... |
| 2 | [Chapter 2. Mathematical Foundations](02/) | Automatic differentiation begins with a simple object: a function. |
| 3 | [Chapter 3. Programs as Mathematical Objects](03/) | A straight-line program is the simplest model of computation used in automatic differentiation. It is a program with a fixed sequence of assignments, no branches, no loops,... |
| 4 | [Chapter 4. Core Theory of Automatic Differentiation](04/) | Automatic differentiation is built on a simple observation: a complicated derivative can be computed by composing many small local derivatives. Instead of manipulating a full... |
| 5 | [Chapter 5. Forward Mode Automatic Differentiation](05/) | Forward mode automatic differentiation computes derivatives by carrying two values through a program at the same time: the ordinary value and its tangent. The ordinary value... |
| 6 | [Chapter 6. Reverse Mode Automatic Differentiation](06/) | Reverse mode automatic differentiation computes derivatives by propagating sensitivities backward through a computation. In forward mode, each intermediate value carries a... |
| 7 | [Chapter 7. Dual Numbers and Algebraic Structures](07/) | Dual numbers give the cleanest algebraic model of forward mode automatic differentiation. They extend ordinary real numbers with a formal infinitesimal part. Instead of... |
| 8 | [Chapter 8. Higher-Order Differentiation](08/) | First derivatives describe local rate of change. Second derivatives describe how that rate of change itself changes. In optimization, this is curvature. In dynamics, it is... |
| 9 | [Chapter 9. Differentiation of Control Flow](09/) | A conditional is a program construct that chooses one computation among several possible computations. In ordinary code, this is written as if, else, switch, case, pattern... |
| 10 | [Chapter 10. Matrix and Tensor Differentiation](10/) | Matrix calculus is the notation and rule system used to differentiate functions whose inputs, outputs, or intermediate values are vectors, matrices, or tensors. Automatic... |
| 11 | [Chapter 11. Compiler and Runtime Design](11/) | Source transformation is an implementation strategy for automatic differentiation in which a program that computes a function is rewritten into another program that computes... |
| 12 | [Chapter 12. AD in Modern Programming Languages](12/) | Lisp is one of the natural homes of automatic differentiation. It treats programs as data, has a simple expression syntax, and supports macro systems that can transform code... |
| 13 | [Chapter 13. Optimization and Machine Learning](13/) | Gradient descent is the basic optimization procedure behind much of modern machine learning. It is simple enough to state in one line, but rich enough to expose many of the... |
| 14 | [Chapter 14. Scientific Computing Applications](14/) | Differential equations are one of the main reasons automatic differentiation matters in scientific computing. Many scientific models are not written as closed-form functions.... |
| 15 | [Chapter 15. Differentiable Systems Architecture](15/) | An end-to-end differentiable pipeline is a system whose final objective can send derivative information backward through every trainable or tunable stage of computation.... |
| 16 | [Chapter 16. Sparse and Structured Differentiation](16/) | Sparse and structured differentiation studies how to compute derivatives without materializing dense derivative objects. Many real systems have enormous Jacobians and... |
| 17 | [Chapter 17. Numerical and Systems Concerns](17/) | Automatic differentiation computes derivatives by executing arithmetic. On a real machine, arithmetic uses finite precision. This means AD gives the derivative of the... |
| 18 | [Chapter 18. Advanced Topics](18/) | Many programs do not compute their output by applying a fixed sequence of explicit operations. Instead, they define the output as the solution of another problem. |
| 19 | [Chapter 19. Theory and Foundations](19/) | Automatic differentiation is often described by a simple rule: |
| 20 | [Chapter 20. Building an AD Engine](20/) | A minimal forward mode automatic differentiation engine has one job: evaluate a program while carrying both a value and its derivative. The engine does not build a graph. It... |
| 21 | [Chapter 21. Major AD Systems](21/) | ADIFOR, short for Automatic Differentiation of Fortran, is one of the classical source-transformation systems for automatic differentiation. It was designed for numerical... |
| 22 | [Chapter 22. Open Problems](22/) | Automatic differentiation works naturally on pure mathematical functions: |
| Appendix | [Appendix](app/) | ADIFOR, short for Automatic Differentiation of Fortran, is one of the classical source-transformation systems for automatic differentiation. It was designed for numerical... |
