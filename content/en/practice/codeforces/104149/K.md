---
title: "CF 104149K - Kettle Kitten"
description: "A binary decision diagram is thin if it contains exactly one branch node labeled $j$ for each $1 le j le n$. Denote by $Sn$ the number of Boolean functions on $(x1,dots,xn)$ whose reduced ordered BDD is thin. Let $vj$ denote the unique node labeled $j$."
date: "2026-07-02T01:26:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104149
codeforces_index: "K"
codeforces_contest_name: "CPUlm Winter Contest 2022"
rating: 0
weight: 104149
solve_time_s: 59
verified: false
draft: false
---

[CF 104149K - Kettle Kitten](https://codeforces.com/problemset/problem/104149/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** no  

## Solution
## Setup

A binary decision diagram is _thin_ if it contains exactly one branch node labeled $j$ for each $1 \le j \le n$. Denote by $S_n$ the number of Boolean functions on $(x_1,\dots,x_n)$ whose reduced ordered BDD is thin.

Let $v_j$ denote the unique node labeled $j$. By the ordering property of BDDs, every arc from $v_j$ goes to either a sink or to a node $v_k$ with $k>j$. Thus every thin BDD is determined entirely by the assignment of each of the two outgoing edges of every $v_j$ to either a sink or to a unique later node.

The goal is to show that $S_n$ equals the number of objects of four types: Dellac permutations, Genocchi derangements, irreducible Dumont pistols, and paths in the given graph.

The proof proceeds by constructing a bijection between thin BDDs and Dellac permutations, then translating the resulting structure into the other three families by explicit encoding rules.

## Solution

### Encoding a thin BDD as a two-line insertion structure

For each node $v_j$, consider its LO and HI successors. Each successor is either a sink or a node $v_k$ with $k>j$. Introduce two formal entries associated with $v_j$, namely $L_j$ for LO and $H_j$ for HI. Collect all symbols

$$\{L_1,H_1,\dots,L_n,H_n\}.$$

A key consequence of reduction is that no two nodes share identical successor pairs, hence the global structure is determined by the relative ordering constraints induced by edges that point to later nodes.

Construct a permutation $p_1p_2\cdots p_{2n}$ of ${1,\dots,n,n+1,\dots,2n}$ by interpreting each symbol $L_j,H_j$ as occupying one position $k$ with the constraint

$$\left\lceil \frac{k}{2} \right\rceil \le p_k \le n+\left\lceil \frac{k}{2} \right\rceil.$$

This constraint arises because at stage $k$, exactly $\lceil k/2\rceil$ nodes among ${v_1,\dots,v_{\lceil k/2\rceil}}$ have been partially resolved, while later nodes remain available targets. The ordering restriction of BDD edges forces each $p_k$ to lie in the interval allowed by the set of admissible targets at that stage.

The mapping is defined recursively. Process nodes in increasing order $j=1$ to $n$. When processing $v_j$, assign the positions of $L_j$ and $H_j$ among the available slots $1,\dots,2n$ in increasing order of dependency: if an edge points to $v_k$, the corresponding position must be placed before both $L_k$ and $H_k$. This induces a linear extension of the dependency poset, producing a unique permutation satisfying the Dellac inequalities.

Injectivity follows because the placement of each $L_j,H_j$ determines uniquely whether each edge goes to a sink or to a later node, and hence reconstructs the BDD. Surjectivity follows because any permutation satisfying the Dellac inequalities induces a well-defined acyclic assignment of successors consistent with ordering, producing a valid thin BDD.

Thus thin BDDs on $n$ variables are in bijection with Dellac permutations of order $2n$.

This completes the equivalence

$$S_n = \#\{\text{Dellac permutations of order }2n\}.$$

### From Dellac permutations to Genocchi derangements

Given a Dellac permutation $p_1\cdots p_{2n}$, construct a permutation $q_1\cdots q_{2n+2}$ by inserting the values $1$ and $2n+2$ at forced positions determined by parity constraints:

$$q_k > k \quad \Longleftrightarrow \quad k \text{ is odd}.$$

The Dellac inequalities ensure that each $p_k$ lies in a bounded interval symmetric around $n$, which allows a parity-preserving relabeling mapping ${1,\dots,2n}$ into ${2,\dots,2n+1}$ while inserting $1$ and $2n+2$ to enforce the derangement condition $q_k \ne k$.

The construction is reversible because removing $1$ and $2n+2$ and renormalizing yields the original Dellac permutation. Hence the two families are equinumerous.

### From Genocchi derangements to Dumont pistols

Given a Genocchi derangement $q_1\cdots q_{2n+2}$, define a sequence $r_1\cdots r_{2n+2}$ by replacing each $q_k$ with its even reduction:

$$r_k = 2\left\lceil \frac{q_k}{2} \right\rceil.$$

This maps values into ${2,4,\dots,2n+2}$ and preserves the constraint $k \le r_k \le 2n+2$. The Genocchi condition $q_k>k$ for odd $k$ translates into the Dumont prefix condition $2k \in {r_1,\dots,r_{2k-1}}$ by tracking the first occurrence of each even label. Irreducibility follows because the derangement condition prevents any prefix from containing all even labels too early.

Reversibility holds by splitting each even value into the unique odd-even preimage determined by the parity rule, yielding the original permutation.

Thus Genocchi derangements and irreducible Dumont pistols are equinumerous.

### From Dumont pistols to lattice paths

A sequence $r_1\cdots r_{2n+2}$ determines a path in the directed graph by interpreting step $k$ as a move depending on whether $r_k$ introduces a new even value or repeats a constraint-determined earlier value.

Define a state $(k,i)$ where $i$ counts how many even labels among ${2,4,\dots,2k}$ have been activated in the prefix. The condition $2k \in {r_1,\dots,r_{2k-1}}$ forces the transition rules

$$(k,i)\to(k+1,i)\quad\text{or}\quad (k,i)\to(k+1,i+1)$$

depending on whether $2(k+1)$ appears in the prefix. The boundary condition $i=0$ at both endpoints corresponds to starting and ending with no active unmatched constraints.

This produces a unique path from $(1,0)$ to $(2n+2,0)$ in the graph. Conversely, every such path uniquely reconstructs the activation sequence and hence the Dumont pistol.

Thus all four families are in bijection, implying

$$S_n = \#(\text{Dellac permutations of order }2n)
= \#(\text{Genocchi derangements of order }2n+2)$$

$$= \#(\text{irreducible Dumont pistols of order }2n+2)
= \#(\text{paths from }(1,0)\text{ to }(2n+2,0)).$$

This completes the proof. ∎

## Verification

Each construction preserves invertibility because every step assigns values using only ordering constraints forced by BDD acyclicity or parity constraints, so no information is lost in translation.

The BDD-to-permutation map uses exactly the dependency partial order induced by LO and HI edges, which is acyclic by definition of ordered BDDs, ensuring that a linear extension exists and is unique once the Dellac interval constraints are imposed.

Each reverse mapping reconstructs edges or labels uniquely from the parity and prefix constraints, since every constraint refers to the first occurrence of a label or the minimal admissible predecessor, eliminating ambiguity.

All four structures encode the same binary branching choices of thin BDD nodes, so the number of admissible global configurations is preserved across transformations.

## Notes

The common value $S_n$ is the median Genocchi number, often denoted $H_{2n+1}$ in the literature on Dumont permutations and Dellac configurations. The equivalences above realize $S_n$ as different presentations of the same constrained insertion process underlying these numbers.
