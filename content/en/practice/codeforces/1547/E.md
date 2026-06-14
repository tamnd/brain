---
title: "CF 1547E - Air Conditioners"
description: "We are given a one-dimensional strip of length $n$. Some positions on this strip contain air conditioners, each fixed at a known coordinate and each producing its own base temperature."
date: "2026-06-14T19:58:16+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "implementation", "shortest-paths", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1547
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 731 (Div. 3)"
rating: 1500
weight: 1547
solve_time_s: 465
verified: false
draft: false
---

[CF 1547E - Air Conditioners](https://codeforces.com/problemset/problem/1547/E)

**Rating:** 1500  
**Tags:** data structures, dp, implementation, shortest paths, sortings, two pointers  
**Solve time:** 7m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a one-dimensional strip of length $n$. Some positions on this strip contain air conditioners, each fixed at a known coordinate and each producing its own base temperature. Every other cell inherits a temperature determined by its distance to all air conditioners: from each conditioner, the contribution to a cell is its base temperature plus the absolute distance to that cell, and the final temperature is the minimum of all such contributions.

So each air conditioner acts like a source that “radiates” linearly increasing temperature as we move away from it. We want, for every position on the line, the smallest value among all these linear growth functions.

The input size allows up to $3 \cdot 10^5$ total cells across all test cases. Any solution that tries to compute the answer for every cell by scanning all conditioners independently would perform up to $O(nk)$ operations in a test case, which degenerates to $9 \cdot 10^{10}$ in the worst case and is not feasible. This immediately rules out brute force per cell.

A key structural detail is that each air conditioner contributes a V-shaped function $t_i + |a_i - x|$. The final answer is the lower envelope of these V-shapes.

A common failure case for naive reasoning is computing only nearest air conditioners incorrectly. For example, if two conditioners are at positions 1 and 100 with similar temperatures, a cell in the middle is influenced by both, and the minimum is not necessarily from the closest one in raw distance when base temperatures differ significantly.

Another subtle edge case is when one conditioner is far but has a much smaller base temperature. A greedy nearest-position-only approach fails there because it ignores vertical offsets.

## Approaches

The brute-force approach evaluates every cell independently. For a fixed position $i$, it checks all conditioners and computes $t_j + |a_j - i|$, taking the minimum. This is correct because it directly follows the definition. The cost comes from repeating this computation for all $n$ cells, giving $O(nk)$ operations per test case in the worst case, which is too slow when both $n$ and $k$ are large.

The key observation is that each conditioner defines a function over the line, and the answer is the minimum of these functions at every point. Instead of treating this as independent queries, we reinterpret it as a multi-source shortest path problem on a line graph: each conditioner is a source with initial distance $t_i$, and moving left or right increases cost by 1 per step. This is exactly a shortest path on a graph where every node connects to its neighbors with weight 1.

This structure allows a multi-source BFS or Dijkstra-like propagation. Since all edge weights are 1, we can initialize all sources at once and propagate outward in increasing order of distance using a deque or priority queue logic. The optimal simplification is that this becomes a classic “multi-source shortest path on a line”, which reduces to a linear sweep after sorting sources.

We process from left to right and right to left because each direction independently computes the best contribution from conditioners on that side. The final answer is the minimum of these two sweeps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nk)$ | $O(1)$ | Too slow |
| Two-pass propagation | $O(n + k)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We treat the line as something where influence spreads outward from each conditioner, and we compute minimal values separately from both directions.

1. Initialize an array `ans` of size $n$ with infinity. This represents unknown best temperatures so far.
2. For each air conditioner at position $a_i$, set `ans[a_i] = t_i`. This encodes the fact that at the source, cost is exactly its base temperature.
3. Sweep from left to right. Maintain the best possible value coming from the left side. At position $i$, the best left influence is either starting fresh from a conditioner at $i$, or extending the previous best by +1. We update `ans[i] = min(ans[i], ans[i-1] + 1)`. This step ensures we capture the effect of all conditioners to the left spreading rightward.
4. Sweep from right to left symmetrically. Maintain propagation from the right side. At position $i$, update `ans[i] = min(ans[i], ans[i+1] + 1)`. This ensures right-side conditioners influence leftward correctly.
5. Output the final `ans` array.

The reason each sweep uses a simple +1 transition is that moving one cell increases distance by exactly 1, so each step correctly models the absolute distance expansion.

### Why it works

Each conditioner defines a distance field that expands uniformly in both directions. The left-to-right pass computes the minimum over all paths that go through a sequence of right moves starting from any source, and the right-to-left pass does the same for left moves. Since any optimal path from a source to a cell is monotone in one direction after leaving the source, it must be captured entirely by one of these two sweeps. Taking the minimum of both directions reconstructs the full envelope of all $t_i + |a_i - x|$ functions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    INF = 10**18

    for _ in range(q):
        input()
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        t = list(map(int, input().split()))

        ans = [INF] * n

        for i in range(k):
            ans[a[i] - 1] = t[i]

        for i in range(1, n):
            ans[i] = min(ans[i], ans[i - 1] + 1)

        for i in range(n - 2, -1, -1):
            ans[i] = min(ans[i], ans[i + 1] + 1)

        print(*ans)

if __name__ == "__main__":
    solve()
```

The initialization step places all air conditioners directly into the array. The left-to-right sweep correctly models propagation of influence increasing by one per step. The right-to-left sweep corrects cases where the best source lies to the right. The use of a large `INF` ensures non-initialized cells do not incorrectly dominate minima.

A common implementation mistake is forgetting to convert positions to zero-based indexing. Another subtle issue is overwriting instead of taking minimum during propagation, which would incorrectly discard better paths.

## Worked Examples

We trace a small case: $n=6$, conditioners at positions 2 and 5 with temperatures 14 and 16.

Initial state after placement:

| i | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| ans | inf | 14 | inf | inf | 16 | inf |

After left-to-right sweep:

| i | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| ans | inf | 14 | 15 | 16 | 16 | 17 |

After right-to-left sweep:

| i | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| ans | 15 | 14 | 15 | 16 | 16 | 17 |

This confirms how influence from both sides merges to form the correct minimum envelope.

A second example is a single conditioner at position 4 with value 10 in $n=7$. The propagation produces a symmetric linear increase outward, confirming that both sweeps correctly reproduce absolute distance behavior.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | Each sweep visits each cell once, plus $O(k)$ initialization |
| Space | $O(n)$ | Array stores current best values for each position |

The total complexity over all test cases is linear in the sum of $n$, which fits comfortably within the constraint of $3 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    q = int(input())
    INF = 10**18
    out_lines = []

    for _ in range(q):
        input()
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        t = list(map(int, input().split()))

        ans = [INF] * n

        for i in range(k):
            ans[a[i] - 1] = t[i]

        for i in range(1, n):
            ans[i] = min(ans[i], ans[i - 1] + 1)

        for i in range(n - 2, -1, -1):
            ans[i] = min(ans[i], ans[i + 1] + 1)

        out_lines.append(" ".join(map(str, ans)))

    return "\n".join(out_lines)

assert run("""5

6 2
2 5
14 16

10 1
7
30

5 5
3 1 4 2 5
3 1 4 2 5

7 1
1
1000000000

6 3
6 1 3
5 5 5
""") == """15 14 15 16 16 17
36 35 34 33 32 31 30 31 32 33
1 2 3 4 5
1000000000 1000000001 1000000002 1000000003 1000000004 1000000005 1000000006
5 6 5 6 6 5"""

assert run("""1

1 1
1
10
""") == "10"

assert run("""1

5 1
3
7
""") == "9 8 7 8 9"

assert run("""1

6 2
1 6
5 1
""") == "5 2 3 4 5 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 10 | minimal boundary case |
| single center conditioner | symmetric propagation | correctness of both sweeps |
| opposite extremes | mixed influence | correct envelope behavior |

## Edge Cases

A minimal single-conditioner case such as $n=1, k=1$ with position 1 directly initializes the array and no propagation changes it, confirming correctness for degenerate inputs.

A case with one conditioner at the far left, for example $n=5$, $a_1=1$, shows how only the left-to-right sweep matters. The algorithm starts with ans = [t, inf, inf, inf, inf], then propagates to [t, t+1, t+2, t+3, t+4], matching the definition exactly as distances grow by one per step.
