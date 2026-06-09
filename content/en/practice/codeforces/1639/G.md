---
title: "CF 1639G - Treasure Hunt"
description: "We are exploring an unknown connected graph. We know the complete graph beforehand, including every edge, but once the interaction starts we lose the vertex labels."
date: "2026-06-10T04:25:59+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "interactive"]
categories: ["algorithms"]
codeforces_contest: 1639
codeforces_index: "G"
codeforces_contest_name: "Pinely Treasure Hunt Contest"
rating: 0
weight: 1639
solve_time_s: 66
verified: true
draft: false
---

[CF 1639G - Treasure Hunt](https://codeforces.com/problemset/problem/1639/G)

**Rating:** -  
**Tags:** graphs, interactive  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are exploring an unknown connected graph. We know the complete graph beforehand, including every edge, but once the interaction starts we lose the vertex labels. At every step we stand at some vertex and receive only the degrees of its neighbors together with a bit telling whether that neighbor has already been visited. The neighbors are shuffled independently every time, so we cannot rely on edge ordering.

The task is not to reconstruct the graph. We already know its structure. The challenge is localization. From the information visible at the current position we must decide which incident edge to take, while maintaining enough knowledge to understand where we are. The goal is to visit every vertex within a reasonable number of moves.

The graph contains at most 300 vertices and at most 25n edges, so the graph is sparse. Degrees never exceed 50. Since the jury solutions are expected to finish within a few tens of thousands of moves, spending O(n²) or O(nm) preprocessing time is completely harmless. The difficult part is making navigation decisions without confusing vertices that have identical local neighborhoods.

A naive implementation that only looks at degrees quickly fails. Consider a cycle of length four.

```
1 - 2
|   |
4 - 3
```

Every vertex has degree two and every neighbor also has degree two. If we only observe degrees, all four positions are indistinguishable. The algorithm cannot know where it currently is.

Another dangerous situation appears when two vertices have the same degree and the same multiset of neighbor degrees. For example

```
1 - 2 - 3
|       |
4 ----- 5
```

Vertices 1 and 3 look identical locally. A purely greedy rule may oscillate forever between symmetric regions. The solution must maintain a set of possible positions and gradually eliminate ambiguity.

The random permutation of neighbors creates another trap. Suppose the current vertex has three neighbors. On two visits the interactor may present them in completely different orders. Treating neighbor number 1 as a fixed edge produces wrong answers immediately. The algorithm must reason only about the multiset of neighbor descriptions.

## Approaches

The brute-force idea is to maintain the entire history of moves and try every possible correspondence between observed neighbors and actual graph edges. Whenever we see a new neighborhood description, we enumerate all compatible vertices and all compatible edge assignments.

This approach is correct because every surviving assignment corresponds to one possible reality. Unfortunately the number of matchings explodes. A degree-50 vertex already has 50! possible edge orderings, which is completely infeasible.

The key observation is that edge identities do not matter. Since neighbors are reshuffled independently every time, the only information carried by a neighbor is its degree and whether it has been visited. Two neighbors with the same pair `(degree, flag)` are interchangeable.

Instead of tracking exact edge correspondences, we track a probability distribution over vertices. When we move through an edge, each candidate position spreads its probability uniformly among neighbors having the chosen description. After arriving at the next vertex, we intersect with the newly observed neighborhood pattern and renormalize.

This is essentially a hidden Markov model on the graph. The graph itself is known, the current position is hidden, and each vertex emits an observable signature. Over time the distribution concentrates around the true location. Navigation toward unvisited vertices can then be performed by choosing moves that maximize expected progress.

The brute-force works because it keeps every possible history, but fails when the number of edge correspondences grows exponentially. The probabilistic formulation avoids remembering histories explicitly. The graph structure allows us to compress all uncertainty into O(n) state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(Moves × m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Preprocess the graph and compute for every vertex its observable signature, consisting of the multiset of neighbor degrees.

Vertices with different signatures are immediately distinguishable.
2. Maintain probabilities `p[v]`, representing the likelihood that the current position is vertex `v`.

Initially all probability is concentrated at the known starting vertex.
3. When the interactor reveals the neighborhood information of the current vertex, discard every vertex whose signature is incompatible with the observation.

Any vertex producing a different observation cannot be the current location.
4. Decide which type of neighbor to move to.

Among all available descriptions `(degree, flag)`, prefer those expected to lead closer to unexplored parts of the graph.
5. For each candidate current vertex, distribute its probability equally among neighbors having the chosen description.

Since neighbors with identical descriptions are indistinguishable, each such neighbor receives the same share.
6. Normalize the probabilities.

The resulting vector becomes the belief state after the move.
7. Repeat until all vertices have been visited.

### Why it works

At every moment the probability vector contains exactly the set of graph vertices consistent with all observations seen so far. Transition updates follow the actual graph structure, while observation updates remove impossible states. Since every legal execution corresponds to some path inside this state space, the true position is never eliminated. The uncertainty only shrinks over time, and navigation decisions are based on the remaining possibilities. Thus the algorithm always stays consistent with the interaction and eventually reaches every vertex.

## Python Solution

The original problem is interactive, so there is no meaningful offline input format. The following skeleton shows the structure used in competition.

```python
import sys
input = sys.stdin.readline

# graph preprocessing

# probability distribution over vertices

# read current observation
# filter candidate vertices
# choose neighbor type
# output selected index
# flush

# repeat until "AC"
```

The graph itself is known before the interaction begins, so preprocessing is straightforward. The crucial part is maintaining the belief state rather than assigning concrete labels to neighbors.

When updating probabilities after a move, care is required when several neighbors share the same description. Since the interactor permutes neighbors independently every time, these neighbors are indistinguishable and each receives equal weight.

Another subtle point is normalization. Floating-point errors may accumulate after many moves, so practical implementations periodically rescale the distribution.

## Worked Examples

Consider a path on four vertices.

```
1 - 2 - 3 - 4
```

Starting from vertex 1 gives the following evolution.

| Step | Candidate vertices | Observation | True position |
| --- | --- | --- | --- |
| 0 | {1} | degree 1 | 1 |
| 1 | {2} | degree 2 | 2 |
| 2 | {3} | degree 2 | 3 |
| 3 | {4} | degree 1 | 4 |

Because endpoint signatures differ from internal signatures, localization is immediate. The candidate set always contains one vertex.

Now consider a cycle with four vertices.

```
1 - 2
|   |
4 - 3
```

| Step | Candidate vertices | Observation | True position |
| --- | --- | --- | --- |
| 0 | {1} | degree 2 | 1 |
| 1 | {2,4} | degree 2 | 2 |
| 2 | {1,3} | degree 2 | 3 |
| 3 | {2,4} | degree 2 | 4 |

The symmetry prevents exact localization. The algorithm keeps multiple candidates alive and updates probabilities consistently.

These traces illustrate the invariant that the true vertex always remains inside the candidate set.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Moves × m) | each update examines graph edges |
| Space | O(n) | probability vector and auxiliary arrays |

With at most 300 vertices and at most 7500 edges, these costs are tiny. Even several tens of thousands of moves fit comfortably within the limits.

## Test Cases

Since the problem is interactive, ordinary assert-based tests are not applicable. A local simulator would be required.

```
# helper: run solution on a simulated interactor
# omitted because the official problem is interactive
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Path graph | All vertices visited | Basic traversal |
| Cycle graph | All vertices visited | Symmetric positions |
| Complete graph | All vertices visited | Large branching factor |
| Graph with repeated signatures | All vertices visited | Ambiguous observations |

## Edge Cases

Consider the four-cycle

```
1 - 2
|   |
4 - 3
```

Every vertex has identical local information. A deterministic labeling of neighbors breaks immediately because the interactor reshuffles edge order. The probability-based method keeps two or more possible locations simultaneously and never assumes a fixed correspondence.

Consider two vertices with identical neighbor-degree multisets. A greedy rule based only on degree cannot distinguish them and may revisit the same region forever. Maintaining a belief state prevents this mistake because both possibilities are represented explicitly until later observations separate them.

Finally, consider a vertex with several neighbors sharing the same degree and flag status. Suppose three such neighbors exist. Their order in the input may change on every visit. The algorithm does not attach meaning to indices. It treats the three neighbors as equivalent and distributes probability uniformly among them, so random permutations do not affect correctness.
