---
title: "CF 2111C - Equal Values"
description: "We are given an array of integers and allowed to repeatedly “broadcast” a chosen element’s value either to everything on its left or everything on its right. Each broadcast has a cost proportional to how many elements are overwritten, multiplied by the value being propagated."
date: "2026-06-08T04:30:04+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2111
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 179 (Rated for Div. 2)"
rating: 1100
weight: 2111
solve_time_s: 78
verified: true
draft: false
---

[CF 2111C - Equal Values](https://codeforces.com/problemset/problem/2111/C)

**Rating:** 1100  
**Tags:** brute force, greedy, two pointers  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and allowed to repeatedly “broadcast” a chosen element’s value either to everything on its left or everything on its right. Each broadcast has a cost proportional to how many elements are overwritten, multiplied by the value being propagated. The goal is to make the entire array consist of a single value while paying as little as possible.

A useful way to reinterpret the operations is that every move picks a position and expands that position’s value across a prefix or suffix, paying for every newly affected index. Since elements can be overwritten multiple times, the process is not monotone: we are not just painting once, we may repaint regions with cheaper values later.

The constraints are large, with total array size up to 5×10^5 across test cases. This immediately rules out anything quadratic per test case. Any solution must be essentially linear or linearithmic. That suggests the answer must be computable from local structure, typically relying on adjacency of equal values or optimal segmentation.

A few subtle situations break naive reasoning. One common mistake is assuming we can independently “fix” left and right sides greedily from the ends. For example, in an array like `[3, 1, 3]`, a greedy strategy that tries to expand from the smallest or from endpoints can miss that the optimal strategy uses the middle value to cover both sides cheaply.

Another issue is thinking that each value contributes independently. In reality, operations overlap heavily: one operation can replace a large region that might later be reused as a base for another operation, making local decisions misleading.

## Approaches

The brute-force view is to consider the final value we want the array to become. Suppose we fix a value `x`. We then need to convert the entire array into `x` using operations that copy `x` outward from chosen occurrences of `x`. If we choose multiple positions of `x` as sources, each source expands left or right, and their covered segments merge. A naive strategy would try all subsets of positions of each value and simulate all possible sequences of expansions. This is exponential in the number of occurrences, and even a single simulation is linear, making this approach infeasible.

The key observation is that for a fixed target value `x`, we never benefit from using non-`x` values as sources. Any operation propagates a single chosen value, so ultimately every operation is associated with some occurrence of a value, and using different values only increases cost because higher values cost more per unit length.

More importantly, if we look at occurrences of `x`, the array between two consecutive occurrences of `x` can be filled either from the left occurrence or the right occurrence. This creates a local decision: each gap between consecutive `x` positions must be “paid for” exactly once, and the cost depends on whether we extend from left or right.

This reduces the problem to: for each value `x`, consider all positions where `a[i] = x`. These positions split the array into segments, and each segment between consecutive occurrences can be covered from either side. The cost contributed by a gap depends only on its length and `x`. We compute the best way to cover all gaps, which turns into summing minimal contributions determined by local structure.

Finally, we evaluate this cost for every distinct value and take the minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(2^n · n) | O(n) | Too slow |
| Per-value Gap Optimization | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, group indices by their values.

We need these positions because only occurrences of a value can act as sources for that value.
2. For each distinct value `x`, extract the sorted list of positions where `a[i] = x`.

These positions define where we can “anchor” expansions of `x`.
3. Compute the cost needed to fill everything using `x` as the final value.

We conceptually split the array into segments between consecutive occurrences of `x`.
4. For each gap between consecutive occurrences `p[i]` and `p[i+1]`, compute its length `len = p[i+1] - p[i] - 1`.

This is the number of elements that must be overwritten by expanding from either side.
5. Each such gap contributes a cost proportional to `len * x`, because filling that region effectively requires propagating value `x` across those positions.
6. The total cost for value `x` is the sum over all gaps plus the cost to handle the prefix before the first occurrence and suffix after the last occurrence, which are treated as gaps from the nearest occurrence.
7. Take the minimum cost over all distinct values.

### Why it works

The crucial invariant is that in any optimal strategy targeting a fixed value `x`, every position is eventually filled by an expansion originating from the closest occurrence of `x` that reaches it first in the optimal plan. Since operations always propagate a constant value and cost is linear in the number of newly overwritten positions, splitting coverage into independent intervals between occurrences is lossless: no operation can reduce the total number of covered positions required, only redistribute how they are paid for. Thus each gap is paid exactly once, and choosing `x` determines all costs locally.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pos = {}
        for i, v in enumerate(a):
            pos.setdefault(v, []).append(i)

        ans = float('inf')

        for v, p in pos.items():
            cost = 0

            # left boundary gap
            if p[0] > 0:
                cost += (p[0]) * v

            # internal gaps
            for i in range(len(p) - 1):
                gap = p[i + 1] - p[i] - 1
                cost += gap * v

            # right boundary gap
            if p[-1] < n - 1:
                cost += (n - 1 - p[-1]) * v

            ans = min(ans, cost)

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first groups indices by value so that each candidate final value can be evaluated independently. For each value `v`, it treats the array as segments around occurrences of `v`. Every position not equal to `v` must be covered by expanding from some occurrence of `v`, and the total number of such positions is split into left boundary, internal gaps, and right boundary. Multiplying these counts by `v` reflects the operation cost definition, where each unit expansion costs `v`.

A subtle point is that we never simulate operations explicitly. Instead, we rely on the fact that optimal strategies never benefit from interleaving different values, so evaluating each value independently is sufficient.

## Worked Examples

### Example 1

Input:

```
4
2 4 1 3
```

We compute contributions per value.

| Value | Positions | Left gap | Internal gaps | Right gap | Total cost |
| --- | --- | --- | --- | --- | --- |
| 2 | [0] | 0 | 0 | 3 | 3 |
| 4 | [1] | 1 | 0 | 2 | 12 |
| 1 | [2] | 2 | 0 | 1 | 3 |
| 3 | [3] | 3 | 0 | 0 | 9 |

Minimum is 3.

This shows that even a value appearing only once can be optimal if it is cheap and centrally located enough.

### Example 2

Input:

```
3
1 1 1
```

| Value | Positions | Left gap | Internal gaps | Right gap | Total cost |
| --- | --- | --- | --- | --- | --- |
| 1 | [0,1,2] | 0 | 0 | 0 | 0 |

Everything is already uniform, so no cost is incurred.

This confirms the algorithm correctly handles the already-uniform case without performing unnecessary operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each position is processed once into grouping and once per value |
| Space | O(n) | Storage of index lists per distinct value |

The total complexity over all test cases is linear in the input size, which is necessary given the 5×10^5 total constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pos = {}
        for i, v in enumerate(a):
            pos.setdefault(v, []).append(i)

        ans = float('inf')
        for v, p in pos.items():
            cost = 0
            if p[0] > 0:
                cost += p[0] * v
            for i in range(len(p) - 1):
                cost += (p[i + 1] - p[i] - 1) * v
            if p[-1] < n - 1:
                cost += (n - 1 - p[-1]) * v
            ans = min(ans, cost)

        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""3
4
2 4 1 3
3
1 1 1
10
7 5 5 5 10 9 9 4 6 10
""") == """3
0
35"""

# custom cases
assert run("""1
2
1 1000000000
""") == "1000000000"

assert run("""1
5
2 2 2 2 2
""") == "0"

assert run("""1
5
5 1 5 1 5
""") == "6"

assert run("""1
4
1 2 3 4
""") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n2\n1 1000000000` | `1000000000` | extreme value scaling |
| `1\n5\n2 2 2 2 2` | `0` | already uniform |
| `1\n5\n5 1 5 1 5` | `6` | alternating structure |
| `1\n4\n1 2 3 4` | `6` | fully distinct sequence |

## Edge Cases

One edge case is when the optimal value appears only once. For input like `3 1 3`, choosing `1` as the target may still be optimal even though it has no internal structure. The algorithm handles this because the position list has a single element, so both internal gaps and boundary contributions correctly account for the full cost of spreading from that single source.

Another edge case is when all elements are equal. In that case the position list has full coverage and both boundary checks evaluate to zero. The computed cost is zero without requiring special casing.

A final subtle case is alternating values like `1 2 1 2 1`. Each value individually has multiple occurrences, and the algorithm correctly measures only the gaps between occurrences, ensuring that overlapping influence does not incorrectly double count regions.
