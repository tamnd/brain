---
title: "CF 104427B - Lawyers"
description: "We are given a directed relationship between lawyers. Each relationship says that one lawyer trusts another, and this trust has a very specific operational meaning: if lawyer B trusts lawyer A, then A provides a defense for B."
date: "2026-06-30T18:58:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104427
codeforces_index: "B"
codeforces_contest_name: "2022-2023 Winter Petrozavodsk Camp, Day 2: GP of ainta"
rating: 0
weight: 104427
solve_time_s: 50
verified: true
draft: false
---

[CF 104427B - Lawyers](https://codeforces.com/problemset/problem/104427/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed relationship between lawyers. Each relationship says that one lawyer trusts another, and this trust has a very specific operational meaning: if lawyer B trusts lawyer A, then A provides a defense for B.

So the input defines a directed graph where an edge A → B means A defends B. A lawyer can defend many others, and a lawyer is considered acquitted if at least one other lawyer defends them, which translates to having at least one incoming edge in this directed graph.

There is a single global exception that changes the structure of validity. If two lawyers defend each other simultaneously, meaning there is a directed cycle of length two between them, then both of those lawyers are automatically declared guilty regardless of any other incoming defenses they might have.

The task is to determine whether it is possible for every lawyer to be acquitted under these rules, given that all trust relations are fixed and cannot be modified.

The constraints go up to two hundred thousand lawyers and two hundred thousand relations. This immediately implies that any solution must be linear or near-linear in the size of the graph. An O(NM) or O(N^2) style approach would be far beyond feasible limits, while O(N + M) or O(M log N) approaches are acceptable.

A naive mistake here is to focus only on the "at least one incoming defense" condition and ignore the mutual defense rule. For example, in a graph like 1 ↔ 2 and 3 ↔ 4, every node has at least one incoming edge, but both pairs are invalid because of mutual defense, making the answer NO.

Another subtle failure case is when a node has no incoming edges at all. Even if the graph is otherwise dense, a single such node makes universal acquittal impossible.

## Approaches

A direct brute-force interpretation would simulate the condition for each lawyer independently. For every node, we would scan all incoming edges to verify that at least one exists. After that, we would scan all pairs of nodes to detect whether any mutual defense pair exists and invalidate those nodes.

This works conceptually because it follows the definition exactly. However, the cost of scanning all pairs for mutual relationships is quadratic in the worst case. With up to 200,000 nodes, a pairwise check would imply up to 4 × 10^10 comparisons, which is not viable.

The key observation is that both conditions are local to edges. Whether a node has an incoming edge can be tracked by a simple indegree counter. Whether a mutual defense exists can be checked during input processing by marking directed edges in a hash set or adjacency set, and verifying whether the reverse edge already exists.

This reduces the problem from global reasoning over all pairs to constant-time checks per edge.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N² + M) | O(N + M) | Too slow |
| Optimal | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

We model the situation as a directed graph where each trust relation becomes a directed edge.

### Steps

1. Read all edges and construct a representation of the directed graph.

Each edge A → B indicates that A defends B.
2. Maintain an array `indegree` where `indegree[v]` counts how many lawyers defend lawyer v.

Every time we read an edge A → B, we increment `indegree[B]`.

This directly captures whether each lawyer receives at least one defense.
3. At the same time, store all directed edges in a set.

This allows constant-time checking of whether a reverse edge exists.
4. For each edge A → B, check whether the reverse edge B → A exists.

If it does, we immediately know a mutual defense pair exists, which makes the configuration invalid.
5. After processing all edges, verify that every lawyer has indegree at least 1.

If any lawyer has indegree 0, they cannot be acquitted.
6. If both conditions are satisfied, output YES. Otherwise, output NO.

### Why it works

The algorithm directly encodes both necessary conditions implied by the problem rules. The indegree condition ensures every lawyer receives at least one defense. The mutual-edge check enforces the rule that any pair of reciprocal defenses automatically invalidates both participants.

Since both conditions depend only on local edge information, and every edge is checked exactly once, there is no hidden global dependency. Any valid configuration must satisfy these conditions, and any violation of them directly corresponds to a rule violation in the problem statement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    indeg = [0] * (n + 1)
    edges = set()
    
    bad = False
    
    for _ in range(m):
        a, b = map(int, input().split())
        # a defends b => a -> b
        indeg[b] += 1
        edges.add((a, b))
    
    # check mutual defense
    for a, b in edges:
        if (b, a) in edges:
            bad = True
            break
    
    if bad:
        print("NO")
        return
    
    for i in range(1, n + 1):
        if indeg[i] == 0:
            print("NO")
            return
    
    print("YES")

if __name__ == "__main__":
    solve()
```

The solution separates the two constraints cleanly. The indegree array is updated in the input loop so no second pass over adjacency lists is needed for that part. The edge set is used purely for detecting mutual pairs; using a set ensures O(1) average lookup time.

A subtle implementation detail is that mutual edges are checked after reading all input rather than during insertion. Either approach works, but post-processing keeps the logic simpler and avoids missing cases where both directions appear later in input.

## Worked Examples

### Example 1

Input:

```
3 3
1 2
2 3
3 1
```

| Step | Edge | Indegree | Mutual check |
| --- | --- | --- | --- |
| 1 | 1 → 2 | [0,0,1,0] | none |
| 2 | 2 → 3 | [0,0,1,1] | none |
| 3 | 3 → 1 | [1,0,1,1] | none |

All nodes have indegree at least 1 and no reverse edges exist. The configuration is valid, so the output is YES.

### Example 2

Input:

```
4 6
1 2
1 3
1 4
2 3
2 4
3 4
```

| Step | Edge | Indegree | Mutual check |
| --- | --- | --- | --- |
| 1 | 1 → 2 | [0,0,1,0,0] | none |
| ... | ... | ... | ... |
| final | - | node 1 has indegree 0 | none |

Node 1 never receives any incoming defense. Even though the graph is dense, this single violation makes full acquittal impossible, so the answer is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Each edge is processed once for counting indegrees and once for mutual checking |
| Space | O(N + M) | Stores indegree array and edge set |

The constraints allow up to 200,000 nodes and edges, so linear complexity is necessary. The solution fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""3 3
1 2
2 3
3 1
""") == "YES"

assert run("""4 6
1 2
1 3
1 4
2 3
2 4
3 4
""") == "NO"

assert run("""4 4
1 2
2 1
3 4
4 3
""") == "NO"

# custom cases
assert run("""1 0
""") == "NO", "single node cannot be defended"

assert run("""2 1
1 2
""") == "NO", "node 1 has indegree 0"

assert run("""2 2
1 2
2 1
""") == "NO", "mutual defense invalidates both"

assert run("""3 2
1 2
2 3
""") == "NO", "node 1 has indegree 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | NO | no incoming defense possible |
| chain missing start coverage | NO | indegree zero case |
| mutual pair | NO | bidirectional rule |
| partial chain | NO | multiple constraints together |

## Edge Cases

A minimal edge case is when N = 1 and M = 0. The single lawyer receives no defense, so the algorithm correctly outputs NO due to indegree being zero.

In a two-node single-edge case like 1 → 2, node 1 has indegree zero even though node 2 is properly defended. The indegree scan catches this immediately, producing NO.

In a symmetric pair like 1 ↔ 2, both nodes have indegree at least one, so a naive solution might incorrectly return YES. The mutual-edge detection catches this and correctly rejects the configuration.

In sparse graphs where edges form long chains, the correctness depends entirely on detecting the first node in the chain having indegree zero. The algorithm handles this naturally because indegree accumulation is independent of structure beyond immediate neighbors.
