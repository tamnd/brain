---
title: "CF 102565A - Artifact"
description: "We can view the artifacts as vertices of a directed graph. A pair x - y means that artifact x can be followed by artifact y when constructing a spell. A spell is simply a directed path containing at least two different vertices."
date: "2026-08-06T20:42:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102565
codeforces_index: "A"
codeforces_contest_name: "AGM 2020, Final Round, Day 2"
rating: 0
weight: 102565
solve_time_s: 58
verified: false
draft: false
---

[CF 102565A - Artifact](https://codeforces.com/problemset/problem/102565/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** no  

## Solution
## Problem Understanding

We can view the artifacts as vertices of a directed graph. A pair `x -> y` means that artifact `x` can be followed by artifact `y` when constructing a spell. A spell is simply a directed path containing at least two different vertices.

The key observation is that the friend does not need to own the entire path. If two artifacts appear anywhere on the same directed path, owning those two artifacts is enough for the friend to recreate the complete spell. In graph terms, two vertices cannot both be given away if one of them can reach the other.

The task is to find the largest possible set of vertices such that no two chosen vertices are connected by reachability in either direction. This is the largest antichain of the reachability relation.

The graph contains at most 3000 vertices and 20000 directed edges. A solution that checks every subset of artifacts is impossible because there are 2 3000 possible choices. Even algorithms that examine every pair of vertices repeatedly must be designed carefully, because the reachability relation is global and not just based on the original edges. With 3000 vertices, cubic preprocessing is near the practical limit, while anything exponential is completely ruled out.

Several details can break a simpler solution. First, direct edges are not enough. A pair of artifacts may not have an edge between them but still conflict through a longer path.

For example:

```
3 2
1 2
2 3
```

The correct answer is `1`. A careless solution that only checks direct edges might choose artifacts `1` and `3`, but artifact `1` reaches artifact `3`, so those two artifacts cannot coexist.

Second, cycles require special handling. Consider:

```
3 3
1 2
2 3
3 1
```

The correct answer is `1`. Every artifact can reach every other artifact, so at most one artifact can be selected. Treating the graph as a normal DAG without compressing strongly connected components would miss this.

Third, isolated artifacts are always valid choices. For example:

```
4 1
1 2
```

The correct answer is `3`. Artifacts `3` and `4` do not participate in any spell and can both be given away together with one endpoint of the edge if chosen carefully. A solution that counts only vertices appearing in edges would underestimate the answer.

## Approaches

A direct approach would try every possible set of artifacts and verify whether it contains a conflicting pair. This is correct because a valid answer is exactly a subset with no pair of vertices related by reachability. However, the number of subsets grows exponentially, so it cannot handle even a few dozen artifacts.

A less extreme brute force would first compute reachability and then greedily add artifacts while avoiding conflicts. The problem with this idea is that the largest valid set is not necessarily obtainable by a greedy ordering. The structure is that of a partially ordered set, where local choices can block a larger final solution.

The useful transformation comes from looking at the graph structure. First, vertices inside the same strongly connected component are mutually reachable, so we can keep at most one artifact from each component. After contracting every strongly connected component, the remaining graph is a DAG. Reachability in this DAG defines a partial order.

Now the problem becomes finding the largest antichain in a DAG. Dilworth's theorem gives an equivalent formulation: the size of the maximum antichain equals the minimum number of chains needed to cover all vertices. For a DAG, this can be computed as:

answer=C−maximum matching

where `C` is the number of nodes after SCC compression. The matching is built on a bipartite graph containing two copies of every DAG node. We add an edge from the left copy of `u` to the right copy of `v` whenever `u` can reach `v`.

The brute force fails because it tries to reason about all possible independent sets. The observation that the conflicts form a partial order lets us replace the problem with a standard maximum matching computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2 N ⋅N 2 ) | O(N 2 ) | Too slow |
| SCC + Transitive Closure + Matching | O(N 3 +V 2 V ​ ) | O(N 2 ) | Accepted |

## Algorithm Walkthrough

1. Compute the strongly connected components of the directed graph using Tarjan's algorithm.

Every pair of vertices inside one strongly connected component can reach each other, so the friend can never receive two artifacts from the same component. After compression, each component represents one possible choice.
2. Build the condensed DAG.

Each strongly connected component becomes a single node. If there is an original edge between two different components, add an edge between the corresponding DAG nodes.

The condensed graph has no cycles, which makes reachability easier to process.
3. Compute reachability between every pair of components.

Because the number of components is at most 3000, a bitset-based DAG traversal is enough. Process components in reverse topological order and merge the reachable sets of outgoing neighbors.

After this step, we know exactly which pairs of components cannot both be selected.
4. Create the bipartite graph used by Dilworth's theorem.

Create a left and right copy of every component. For every pair `(u, v)` where `u` can reach `v`, add an edge from the left copy of `u` to the right copy of `v`.

The matching represents how many nodes can be merged into chains.
5. Run Hopcroft-Karp maximum matching on this bipartite graph.

The number of unmatched components after applying the theorem is the size of the largest antichain.
6. Output the value:

number of components−maximum matching size

Why it works:

After SCC compression, every remaining node represents a set where choosing more than one vertex is impossible, so each component contributes at most one artifact. The condensed graph is a DAG, and reachability defines a partial order. A valid answer is exactly an antichain of this partial order because no chosen component may reach another chosen component.

Dilworth's theorem states that the largest antichain size equals the minimum chain decomposition size. For a DAG, the minimum chain decomposition is computed by taking the number of nodes and subtracting the maximum matching in the reachability bipartite graph. Therefore the algorithm returns exactly the maximum number of artifacts that can be given away safely.
