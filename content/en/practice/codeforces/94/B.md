---
title: "CF 94B - Friends"
description: "We have exactly five people. Some pairs of people know each other, and the input lists all such acquaintance relations. The task is to determine whether there exists either: 1. Three people where every pair knows each other. 2. Three people where no pair knows each other."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 94
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 76 (Div. 2 Only)"
rating: 1300
weight: 94
solve_time_s: 97
verified: true
draft: false
---

[CF 94B - Friends](https://codeforces.com/problemset/problem/94/B)

**Rating:** 1300  
**Tags:** graphs, implementation, math  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have exactly five people. Some pairs of people know each other, and the input lists all such acquaintance relations.

The task is to determine whether there exists either:

1. Three people where every pair knows each other.
2. Three people where no pair knows each other.

This is naturally a graph problem. Each person is a vertex, and an acquaintance relation is an undirected edge. We are looking for either:

1. A triangle in the graph.
2. A triangle in the complement graph.

If at least one of those structures exists, we print `"WIN"`. Otherwise we print `"FAIL"`.

The constraints are extremely small. There are only five vertices, and at most ten edges because an undirected graph on five vertices has `5 * 4 / 2 = 10` possible pairs. Even a brute-force search over all triples is tiny. The total number of triples is only `C(5, 3) = 10`.

The main difficulty is not performance, it is implementing the conditions correctly.

One easy mistake is checking only for triangles of friendships and forgetting independent triples. Consider this input:

```
2
1 2
3 4
```

The correct answer is:

```
WIN
```

People `1, 3, 5` are pairwise unacquainted. A solution that searches only for friendship triangles would incorrectly print `"FAIL"`.

Another common bug is treating the graph as directed. The relation is symmetric, so if `(1, 3)` appears, then `3` also knows `1`. A careless adjacency structure may forget this and miss valid triples.

For example:

```
3
1 2
2 3
1 3
```

The correct answer is:

```
WIN
```

This is a friendship triangle. If the implementation stores only one direction of each edge, the check may fail.

A more subtle edge case is the empty graph:

```
0
```

The correct answer is:

```
WIN
```

Any three people form a triple of pairwise strangers. A solution that assumes at least one edge exists could behave incorrectly here.

## Approaches

The most direct solution is brute force over all triples of people.

There are only five people, so we can enumerate every combination `(a, b, c)` where `a < b < c`. For each triple, we check two conditions:

1. All three pairs are edges.
2. None of the three pairs are edges.

If either condition is true for any triple, we immediately return `"WIN"``.

This brute-force approach is already fast enough. There are only ten triples, and each check examines three pairs, so the total work is constant.

The reason this works so naturally is that the property we care about is entirely local to triples. We never need larger graph structure, shortest paths, connected components, or anything global.

A more naive version of brute force would explicitly build all subsets of people and then test all subsets of size three. That still works because the graph is tiny, but it introduces unnecessary overhead.

The key observation is that the problem reduces exactly to checking every triple once. Since the graph size is fixed at five, this becomes a compact implementation problem rather than an optimization problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| General subset brute force | O(2^5) | O(1) | Accepted |
| Triple enumeration | O(C(5,3)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Create a `5 x 5` adjacency matrix initialized with `False`.

The matrix lets us check whether two people know each other in constant time.
2. Read each acquaintance pair `(a, b)`.

Convert the indices to zero-based indexing and set both `adj[a][b]` and `adj[b][a]` to `True`.

The graph is undirected, so both directions must be stored.
3. Enumerate every triple of distinct people `(i, j, k)` with `i < j < k`.

Using ordered triples avoids duplicates and guarantees every group of three people is checked exactly once.
4. For the current triple, compute whether all three pairs are connected.

The required edges are:

`i-j`, `i-k`, and `j-k`.
5. Compute whether all three pairs are absent.

This means none of the three edges exists.
6. If either condition is true, print `"WIN"` and stop.

We only need one valid triple.
7. If all triples are checked and none satisfies the condition, print `"FAIL"`.

### Why it works

Every valid answer depends only on groups of three people. The algorithm examines every possible triple exactly once. For each triple, it checks both definitions from the problem:

1. Pairwise acquainted.
2. Pairwise unacquainted.

If such a triple exists anywhere in the graph, the enumeration will eventually reach it and return `"WIN"`. If the algorithm finishes without finding one, then no qualifying triple exists, so `"FAIL"` is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution

def solve():
    m = int(input())

    adj = [[False] * 5 for _ in range(5)]

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1

        adj[a][b] = True
        adj[b][a] = True

    for i in range(5):
        for j in range(i + 1, 5):
            for k in range(j + 1, 5):

                ab = adj[i][j]
                ac = adj[i][k]
                bc = adj[j][k]

                all_friends = ab and ac and bc
                all_strangers = (not ab) and (not ac) and (not bc)

                if all_friends or all_strangers:
                    print("WIN")
                    return

    print("FAIL")

solve()
```

The adjacency matrix is the simplest representation here because the graph is tiny and we frequently ask questions of the form "does edge `(u, v)` exist?". Each lookup becomes a single array access.

The loops use `i < j < k` so every triple appears exactly once. This avoids duplicate work and prevents accidental cases where the same person appears multiple times.

The variables `ab`, `ac`, and `bc` make the logic easier to read and reduce repeated indexing operations. Since there are only three relevant edges per triple, explicitly naming them keeps the conditions clear.

The implementation checks both required patterns separately:

```
all_friends = ab and ac and bc
all_strangers = (not ab) and (not ac) and (not bc)
```

Mixing these conditions into one expression often creates logical mistakes, especially with negations.

The program exits immediately after finding a valid triple because one witness is enough to determine the answer.

## Worked Examples

### Example 1

Input:

```
4
1 3
2 3
1 4
5 3
```

Adjacency edges are:

`(1,3), (2,3), (1,4), (3,5)`

The algorithm checks triples in order.

| Triple | Existing Edges | All Friends | All Strangers |
| --- | --- | --- | --- |
| (1,2,3) | 1-3, 2-3 | No | No |
| (1,2,4) | 1-4 | No | No |
| (1,2,5) | none | No | Yes |

The algorithm prints:

```
WIN
```

This trace shows that we do not need a friendship triangle. The triple `(1,2,5)` forms three pairwise strangers, which already satisfies the problem.

### Example 2

Input:

```
5
1 2
2 3
3 4
4 5
5 1
```

This graph is a cycle of length five.

| Triple | Existing Edges | All Friends | All Strangers |
| --- | --- | --- | --- |
| (1,2,3) | 1-2, 2-3 | No | No |
| (1,2,4) | 1-2 | No | No |
| (1,2,5) | 1-2, 1-5 | No | No |
| (1,3,4) | 3-4 | No | No |
| (1,3,5) | 1-5 | No | No |
| (1,4,5) | 4-5, 1-5 | No | No |
| (2,3,4) | 2-3, 3-4 | No | No |
| (2,3,5) | 2-3 | No | No |
| (2,4,5) | 4-5 | No | No |
| (3,4,5) | 3-4, 4-5 | No | No |

No triple satisfies either condition, so the algorithm prints:

```
FAIL
```

This example is the famous counterexample showing that the statement becomes false for five people.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only 10 triples are checked |
| Space | O(1) | The adjacency matrix size is fixed at 5 x 5 |

The running time is effectively constant because the graph size never changes. Even the simplest brute-force approach easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        m = int(input())

        adj = [[False] * 5 for _ in range(5)]

        for _ in range(m):
            a, b = map(int, input().split())
            a -= 1
            b -= 1

            adj[a][b] = True
            adj[b][a] = True

        for i in range(5):
            for j in range(i + 1, 5):
                for k in range(j + 1, 5):

                    ab = adj[i][j]
                    ac = adj[i][k]
                    bc = adj[j][k]

                    all_friends = ab and ac and bc
                    all_strangers = (not ab) and (not ac) and (not bc)

                    if all_friends or all_strangers:
                        return "WIN"

        return "FAIL"

    return solve()

# provided sample
assert run(
"""4
1 3
2 3
1 4
5 3
"""
) == "WIN", "sample 1"

# empty graph
assert run(
"""0
"""
) == "WIN", "all strangers"

# complete graph
assert run(
"""10
1 2
1 3
1 4
1 5
2 3
2 4
2 5
3 4
3 5
4 5
"""
) == "WIN", "all friendship triangles"

# 5-cycle Ramsey counterexample
assert run(
"""5
1 2
2 3
3 4
4 5
5 1
"""
) == "FAIL", "cycle of length 5"

# single friendship triangle
assert run(
"""3
1 2
2 3
1 3
"""
) == "WIN", "friendship triangle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty graph | WIN | Detects independent triples |
| Complete graph | WIN | Detects friendship triangles |
| 5-cycle | FAIL | Famous counterexample |
| Single triangle | WIN | Basic friendship detection |

## Edge Cases

Consider the empty graph:

```
0
```

The adjacency matrix contains only `False` values. The very first triple `(1,2,3)` has no edges at all. The algorithm computes:

```
all_friends = False
all_strangers = True
```

So it correctly prints:

```
WIN
```

This confirms that the algorithm handles graphs with no edges.

Now consider the five-cycle counterexample:

```
5
1 2
2 3
3 4
4 5
5 1
```

Every triple contains either exactly one edge or exactly two edges. None contain zero edges or three edges. The algorithm systematically checks all ten triples and never finds a valid one, so it prints:

```
FAIL
```

This is the critical correctness case because it proves the statement is not universally true for five people.

Finally, consider a pure friendship triangle:

```
3
1 2
2 3
1 3
```

When the algorithm reaches triple `(1,2,3)`, all three required edges exist:

```
1-2 = True
1-3 = True
2-3 = True
```

So `all_friends` becomes `True`, and the algorithm immediately prints:

```
WIN
```

This confirms that the graph is treated as undirected and friendship triangles are detected correctly.
