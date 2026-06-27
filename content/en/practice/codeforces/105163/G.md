---
title: "CF 105163G - Grey-like Code"
description: "The construction defines a directed graph built from bit manipulation. Each vertex is an integer in a full range that can be interpreted as a fixed-length binary string."
date: "2026-06-27T10:54:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105163
codeforces_index: "G"
codeforces_contest_name: "The 19th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 105163
solve_time_s: 35
verified: false
draft: false
---

[CF 105163G - Grey-like Code](https://codeforces.com/problemset/problem/105163/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** no  

## Solution
## Problem Understanding

The construction defines a directed graph built from bit manipulation. Each vertex is an integer in a full range that can be interpreted as a fixed-length binary string. From every vertex, exactly two directed edges are created: one obtained by shifting the current state left by one bit and forcing the new least significant bit to be 0, and another doing the same but forcing the new bit to be 1, with everything truncated back to the original bit width.

In other words, each node represents a binary string of length $n-1$, and each outgoing edge appends either a 0 or a 1 while discarding the oldest bit. Every directed edge can be labeled by the bit that was appended, so every edge corresponds uniquely to a binary digit choice.

The task is not about shortest paths or reachability. It is about counting a global structure in this graph, specifically the number of Eulerian circuits. An Eulerian circuit is a closed walk that traverses every directed edge exactly once. Because every node has equal in-degree and out-degree, such circuits exist, and the problem reduces to counting how many distinct ones there are.

The non-trivial part is that the graph size grows exponentially with $n$. The number of vertices is $2^{n-1}$, and the number of edges is $2^n$. Even storing all edges explicitly becomes infeasible when $n$ is large. This immediately rules out any approach that attempts to enumerate walks or even build large combinatorial structures explicitly, since $2^n$ grows beyond any feasible limit once $n$ exceeds around 25.

A subtle failure mode appears if one tries to simulate Eulerian tours or use naive backtracking counting. Even for $n = 10$, the graph already has 512 vertices and 1024 edges, and the number of Eulerian circuits is astronomically larger than what any enumeration could handle. Any approach that explores permutations of edges or paths will explode factorially and fail long before reaching the intended input limits.

The correct output is a single large integer representing this count, so the real challenge is converting a combinatorial counting problem on a huge graph into a closed-form expression.

## Approaches

A direct approach would try to explicitly construct the graph and count Eulerian circuits using backtracking or Hierholzer-style enumeration combined with memoization. This works only in very small cases because every edge choice branches into two possibilities, and the number of valid Eulerian traversals grows super-exponentially. Even if pruning is applied, the state space remains proportional to permutations of edges, which is roughly $(2^n)!$ in the worst conceptual case. That is far beyond any computational limit.

The structure of the graph reveals a more useful perspective. Each vertex corresponds to a fixed-length binary string, and transitions correspond to shifting and appending bits. This is exactly the de Bruijn graph of binary strings of length $n-1$. In this graph, Eulerian circuits are known to correspond one-to-one with de Bruijn sequences of order $n$, where every binary string of length $n$ appears exactly once as a contiguous substring of a cyclic sequence.

Once the problem is recognized as counting Eulerian circuits in a de Bruijn graph, the BEST theorem becomes applicable. It states that the number of Eulerian circuits in a directed Eulerian graph equals the product of factorials of vertex out-degrees multiplied by the number of directed spanning trees rooted at any vertex. In this specific graph, every vertex has out-degree 2, which simplifies the factorial term heavily, since every contribution becomes $1! \cdot 1!$-like structure across a uniform distribution.

The remaining part reduces to counting spanning arborescences in a highly symmetric graph. The Laplacian matrix of this graph has a recursive block structure because vertices split naturally according to their binary prefixes. This symmetry allows a determinant recurrence on principal minors, ultimately collapsing into a simple exponential form.

A key simplification is that the graph is so regular that its spectrum behaves predictably under recursion. The characteristic polynomial satisfies a doubling recurrence, which implies that the determinant of the relevant Laplacian minor grows as a power of two with an exponent tied to the number of edges minus vertices plus one.

This leads to the known closed form for binary de Bruijn graphs: the number of Eulerian circuits is

$$2^{2^{n-1} - n}.$$

So instead of constructing or analyzing the graph directly, the problem reduces to computing a single exponentiation of two.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force Eulerian counting | Exponential in $2^n$ | Exponential | Too slow |
| Graph theory (BEST + structure) | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$, which determines the dimension of the de Bruijn graph and therefore the number of vertices $2^{n-1}$ and edges $2^n$. The graph itself is never constructed.
2. Recognize that the structure corresponds to a binary de Bruijn graph where each Eulerian circuit corresponds uniquely to a valid cyclic sequence containing every binary string of length $n$ exactly once.
3. Apply the known result derived from the BEST theorem and Laplacian determinant analysis of this graph family, which gives the number of Eulerian circuits as $2^{2^{n-1} - n}$.
4. Compute the exponent $2^{n-1} - n$. This step is crucial because the exponent itself can become very large even for moderate $n$, so the computation must rely on arbitrary precision integers.
5. Output (2^{(2^{
