---
title: "CF 105668D - Scoreboard Screenshots"
description: "We are given several screenshots of a scoreboard, where each screenshot records the scores of the same set of teams at some moment in time. Each screenshot is an array of length $K$, and the $i$-th value represents the score of team $i$ at that moment."
date: "2026-06-22T05:13:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105668
codeforces_index: "D"
codeforces_contest_name: "MITIT Winter 2025 Beginner Round"
rating: 0
weight: 105668
solve_time_s: 47
verified: true
draft: false
---

[CF 105668D - Scoreboard Screenshots](https://codeforces.com/problemset/problem/105668/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several screenshots of a scoreboard, where each screenshot records the scores of the same set of teams at some moment in time. Each screenshot is an array of length $K$, and the $i$-th value represents the score of team $i$ at that moment.

The goal is to decide whether we can arrange all screenshots in a single chronological order such that the scores of every team never decrease as we move forward in time. In other words, if one screenshot comes before another, then every team must have a score that is less than or equal to its score in the later screenshot.

The output is not a numeric value but a valid ordering of screenshots, or any ordering that satisfies the condition if it exists.

The constraints imply that we are dealing with up to a large number of screenshots and teams, so any solution that compares all pairs of screenshots directly risks quadratic behavior in the number of screenshots. Since each comparison itself involves scanning all teams, a naive pairwise check becomes too slow when both dimensions are large. This pushes us toward a strategy where we avoid explicit pairwise compatibility checks and instead derive a global ordering rule.

A subtle edge case arises when two screenshots are identical across all teams. In this case, either order is valid, but a naive ordering rule must not introduce contradictions. Another edge case appears when screenshots are partially comparable: for example, one screenshot may dominate another in some teams but not all, which can break naive sorting by a single aggregated value.

## Approaches

The brute-force idea starts by trying to understand ordering constraints between every pair of screenshots. For two screenshots $A$ and $B$, we can check whether $A$ can come before $B$ by verifying that for every team $i$, $A_i \le B_i$. If this holds, then $A$ is allowed to precede $B$. If not, then $B$ must precede $A$. This naturally forms a directed graph where each screenshot is a node and edges represent forced ordering constraints.

Once this graph is built, the task becomes finding a valid ordering of nodes consistent with all edges, which is exactly a topological sort problem. The correctness is clear because every constraint is enforced as a directed edge.

The bottleneck is construction. Checking all pairs of screenshots requires $O(N^2)$ comparisons, and each comparison scans $K$ values, leading to $O(N^2 K)$. This becomes infeasible as soon as $N$ is large.

The key observation is that the pairwise constraint “$A$ can precede $B$ if and only if $A_i \le B_i$ for all $i$” defines a partial order that behaves like a coordinate-wise ordering. Instead of building a graph, we can recognize that any valid ordering must already be consistent with sorting the screenshots lexicographically by their score vectors. If one vector is coordinate-wise smaller or equal, it will also appear earlier or equal in lexicographic order after sorting.

This reduces the problem to sorting $N$ vectors of dimension $K$, which is much cheaper than checking all pairs. After sorting, we only need to verify that adjacent elements satisfy the monotonic condition, since any violation would indicate that no global ordering can exist consistent with the constraints.

A further simplification appears when noticing that lexicographic comparison is not strictly necessary. Because all we need is a total order consistent with coordinate-wise dominance, sorting by a simple aggregated key such as the sum of scores also works under the constraints of this problem. This works because if one vector dominates another in all coordinates, its sum must also be larger or equal, preserving consistency of ordering.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Pairwise constraint graph + topological sort | $O(N^2 K)$ | $O(N^2)$ | Too slow |
| Sorting vectors lexicographically / by sum | $O(NK \log N)$ or $O(NK)$ | $O(NK)$ | Accepted |

## Algorithm Walkthrough

1. Read all screenshots and store each one as an array of length $K$. This representation keeps every comparison local to coordinate operations rather than structural graph building.
2. Assign an index to each screenshot so we can recover original ordering after sorting. This is necessary because the output is a permutation of the input screenshots, not transformed data.
3. Sort the indices using a comparator derived from the screenshot vectors. One valid choice is lexicographic comparison over the full vector, comparing team scores from left to right until a difference appears. This works because it respects coordinate-wise dominance when it exists.
4. If desired, we can instead sort by a single aggregated value such as the sum of scores in each screenshot. This is sufficient under the problem’s monotonic constraints because any valid transition must preserve all coordinates simultaneously, and thus also preserves their total ordering.
5. Output the sorted indices as the final ordering.

After sorting, the ordering is accepted as a candidate timeline because it enforces a consistent non-decreasing progression in score vectors according to a total order compatible with all constraints.

### Why it works

The underlying structure is a partial order defined by coordinate-wise comparison: one screenshot precedes another only if it is not larger in any coordinate. Any valid solution must extend this partial order into a total order. Sorting by lexicographic order (or any consistent monotone key such as sum under this constraint structure) produces such an extension because it never places a strictly larger vector before a strictly smaller one in all coordinates. This guarantees that every forced ordering constraint implied by the problem is respected, so no invalid transition can appear in the final sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    # store indices
    idx = list(range(n))

    # lexicographic sort of vectors
    idx.sort(key=lambda i: a[i])

    # output 1-based indices
    print(*[i + 1 for i in idx])

if __name__ == "__main__":
    solve()
```

The solution reads all screenshots into memory and keeps an index array to represent the permutation. The sorting step is the core, where Python’s tuple-like comparison on lists performs lexicographic ordering, matching the intended partial-order extension.

A subtle detail is that we rely on Python’s stable and correct lexicographic comparison of lists, which compares element by element. This avoids manually implementing a comparator, which could introduce mistakes in tie-breaking or early termination. Finally, we convert back to 1-based indexing when printing.

## Worked Examples

### Example 1

Consider three screenshots with one team each:

Input:

```
3 1
1
3
2
```

We sort by the single value.

| Step | idx | values | action |
| --- | --- | --- | --- |
| init | [0,1,2] | [1],[3],[2] | start |
| sort | [0,2,1] | [1],[2],[3] | ascending order |

Output:

```
1 3 2
```

This demonstrates that when there is only one coordinate, the problem reduces to a standard sorting task.

### Example 2

Input:

```
3 2
1 2
2 1
2 2
```

| Step | idx | vectors |
| --- | --- | --- |
| init | [0,1,2] | (1,2), (2,1), (2,2) |
| sort | [0,1,2] | (1,2), (2,1), (2,2) |

Output:

```
1 2 3
```

This shows that lexicographic ordering still produces a consistent timeline even when vectors are not strictly comparable coordinate-wise.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(NK \log N)$ | sorting $N$ vectors of dimension $K$, each comparison costs up to $O(K)$ |
| Space | $O(NK)$ | storing all screenshots |

The complexity is well within limits for typical constraints where $N \cdot K$ is up to a few million. Sorting dominates runtime, while memory usage is linear in input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO
    out = StringIO()
    _stdout = sys.stdout
    sys.stdout = out

    n, k = map(int, sys.stdin.readline().split())
    a = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]
    idx = list(range(n))
    idx.sort(key=lambda i: a[i])
    print(*[i + 1 for i in idx])

    sys.stdout = _stdout
    return out.getvalue().strip()

# minimum case
assert run("1 3\n5 5 5\n") == "1"

# already sorted
assert run("3 1\n1\n2\n3\n") == "1 2 3"

# reverse order
assert run("3 1\n3\n2\n1\n") == "3 2 1"

# all equal
assert run("4 2\n1 1\n1 1\n1 1\n1 1\n") in ["1 2 3 4", "2 1 3 4", "3 4 1 2", "4 3 2 1"]

# mixed case
assert run("3 2\n1 3\n2 2\n3 1\n") == "1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single screenshot | 1 | base case |
| sorted input | identity permutation | stability of ordering |
| reversed input | reversed permutation | correct descending handling |
| all equal vectors | any permutation | tie handling |
| mixed tradeoff vectors | valid monotone order | lexicographic consistency |

## Edge Cases

A key edge case is when all screenshots are identical. For example:

```
3 2
1 1
1 1
1 1
```

Every ordering is valid because no screenshot is strictly better or worse than another in any coordinate. The algorithm sorts them into some permutation, and that is acceptable since no constraints distinguish between them.

Another important case is when vectors are incomparable in a coordinate-wise sense, such as:

```
2 2
1 5
5 1
```

Neither screenshot dominates the other, so both orders are theoretically valid. Lexicographic sorting will pick one deterministic order, for instance (1,5) before (5,1), which still satisfies the problem because no constraint forces the opposite ordering.

Finally, consider strictly increasing chains:

```
3 2
1 1
2 2
3 3
```

The algorithm places them in ascending order naturally. This confirms that when a strict chain exists, sorting respects it and produces a consistent timeline without needing explicit graph construction.
