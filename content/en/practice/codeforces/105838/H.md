---
title: "CF 105838H - Defense Deployment"
description: "We are given multiple independent test cases. Each test case describes a set of points on an infinite 2D grid. Every point represents a tower placed at integer coordinates."
date: "2026-06-21T22:40:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105838
codeforces_index: "H"
codeforces_contest_name: "The 14th Huazhong Agricultural University Programming Contest"
rating: 0
weight: 105838
solve_time_s: 46
verified: true
draft: false
---

[CF 105838H - Defense Deployment](https://codeforces.com/problemset/problem/105838/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent test cases. Each test case describes a set of points on an infinite 2D grid. Every point represents a tower placed at integer coordinates. From each tower, four rays are constantly emitted along the positive and negative directions of the x-axis and y-axis, extending infinitely and covering every point they pass through.

Two towers are considered to “attack each other” if each one lies on at least one of the other’s rays. Since rays go only along axis-parallel lines, this condition translates into a very rigid geometric structure: a tower at $(a_i, b_i)$ attacks another tower at $(a_j, b_j)$ if and only if they share either the same x-coordinate or the same y-coordinate.

The task is to count the number of unordered pairs $(i, j)$, $i < j$, such that either $a_i = a_j$ or $b_i = b_j$.

The constraints are large. The total number of points across all test cases is up to $10^5$, so any solution that checks all pairs directly, which would be $O(n^2)$, is immediately too slow. We need something close to linear or linearithmic time per test case.

A subtle but important edge case is handling duplicates in counts carefully. If multiple towers share both the same x and y coordinates, they would be identical points, but the problem guarantees coordinates are distinct, so we avoid that ambiguity. However, we still must avoid double counting pairs that share both coordinates in intermediate reasoning, even though it cannot happen here due to uniqueness.

## Approaches

A direct approach is straightforward: check every pair of towers and verify whether their x-coordinates match or their y-coordinates match. This is correct because it directly implements the definition of mutual attack. However, with up to $10^5$ points, this requires about $5 \times 10^9$ comparisons in the worst case, which is not feasible.

The key observation is that the condition decomposes cleanly into two independent equivalence relations. A pair is valid if it belongs to the same x-group or the same y-group. This suggests counting contributions per group rather than per pair.

If we fix an x-coordinate $a$, all towers with that x-coordinate form a group. Any pair inside this group is valid, contributing $\binom{k}{2}$ if there are $k$ towers with that x-value. Similarly, for each y-coordinate $b$, all towers with that y-coordinate also contribute $\binom{k}{2}$.

The subtle issue is that this union-of-conditions approach may double count pairs that share both x and y. However, since all points are distinct, no two towers share both coordinates, so there is no intersection to subtract.

Thus, the problem reduces to counting frequencies of x-values and y-values separately and summing combinatorial contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Frequency counting | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read all x-coordinates and y-coordinates and store frequency counts for each distinct value. We maintain two hash maps or arrays: one for x-values and one for y-values. This is necessary because the answer depends only on how many points share each coordinate, not their identities.
2. For every distinct x-coordinate value, let its frequency be $k$. We add $k \cdot (k - 1) / 2$ to the answer. This counts all unordered pairs of towers aligned vertically on that x-line.
3. For every distinct y-coordinate value, let its frequency be $k$. We again add $k \cdot (k - 1) / 2$ to the answer. This counts all unordered pairs of towers aligned horizontally on that y-line.
4. Output the accumulated sum for the test case.

The key reasoning step is that each valid pair is uniquely determined by being aligned either vertically or horizontally. Since we are counting all pairs inside each coordinate class independently, every valid interaction is captured exactly once.

### Why it works

Consider any valid pair of towers. If they attack each other, they must share x or share y. If they share x, they are included in exactly one x-group contribution via $\binom{k}{2}$. If they share y, they are included in exactly one y-group contribution. Because coordinates are distinct, a pair cannot simultaneously share both x and y, so there is no overlap between the two counting processes. This establishes a one-to-one correspondence between valid pairs and the contributions summed by the algorithm.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        xs = list(map(int, input().split()))
        ys = list(map(int, input().split()))

        cx = {}
        cy = {}

        for x in xs:
            cx[x] = cx.get(x, 0) + 1
        for y in ys:
            cy[y] = cy.get(y, 0) + 1

        ans = 0

        for v in cx.values():
            ans += v * (v - 1) // 2
        for v in cy.values():
            ans += v * (v - 1) // 2

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution separates counting into two independent frequency accumulations. The first loop builds counts of how many towers lie on each vertical line, and the second builds counts for horizontal lines. The final loops convert these frequencies into pair counts using the standard combination formula.

A common implementation mistake is attempting to increment the answer during input parsing without fully separating x and y counts, which risks mixing logic and makes debugging harder. Another pitfall is forgetting integer division in the combination formula, but Python’s `//` ensures correctness.

## Worked Examples

Consider a small configuration:

Input:

```
n = 4
x = [1, 1, 2, 3]
y = [1, 2, 2, 2]
```

We compute frequencies.

For x-values:

| x | count |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 3 | 1 |

For y-values:

| y | count |
| --- | --- |
| 1 | 1 |
| 2 | 3 |

Now we compute contributions.

| Source | Value | Contribution |
| --- | --- | --- |
| x=1 | 2 | 1 |
| x=2 | 1 | 0 |
| x=3 | 1 | 0 |
| y=1 | 1 | 0 |
| y=2 | 3 | 3 |

Final answer is 4.

This trace shows that each axis-aligned group contributes independently and that pairs are naturally partitioned by coordinate equality.

Now consider a case where all points lie on a single horizontal line:

Input:

```
n = 5
x = [1, 2, 3, 4, 5]
y = [7, 7, 7, 7, 7]
```

| y | count | contribution |
| --- | --- | --- |
| 7 | 5 | 10 |

All x counts are 1 so they contribute nothing. The result is 10, matching all pairs among five points.

This demonstrates that the y-grouping alone fully captures all interactions when alignment is purely horizontal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each point is processed once for x and once for y, and frequency aggregation is linear |
| Space | O(n) | Hash maps store at most n distinct coordinate values |

The total complexity across all test cases remains linear in the total number of points, which fits comfortably within limits of $10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import Counter

    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        xs = list(map(int, input().split()))
        ys = list(map(int, input().split()))
        cx = Counter(xs)
        cy = Counter(ys)

        ans = 0
        for v in cx.values():
            ans += v * (v - 1) // 2
        for v in cy.values():
            ans += v * (v - 1) // 2
        out.append(str(ans))
    return "\n".join(out)

# provided sample (as interpreted from statement)
assert run("""1
4
1 2 3 1
2 3 1 3
""") == "2"

# all on same x
assert run("""1
3
5 5 5
1 2 3
""") == "3"

# all on same y
assert run("""1
4
1 2 3 4
7 7 7 7
""") == "6"

# no shared coordinates
assert run("""1
3
1 2 3
4 5 6
""") == "0"

# mixed case
assert run("""1
5
1 1 2 2 3
1 2 2 3 3
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same x | 3 | vertical grouping correctness |
| all same y | 6 | horizontal grouping correctness |
| no overlap | 0 | no false positives |
| mixed | 4 | combined counting correctness |

## Edge Cases

A subtle edge case is when all points share the same x-coordinate. The algorithm handles this by putting all points into a single x-frequency bucket, producing $\binom{n}{2}$, while all y-frequencies are isolated and contribute zero. The trace in the worked examples already confirms that the x-group alone produces the correct full answer.

Another case is when all points share the same y-coordinate. Symmetrically, the y-frequency dominates and the x-side contributes nothing. Since the algorithm treats x and y independently, there is no interaction term that could distort the result.

A final edge case is when all coordinates are distinct in both dimensions. Both frequency maps consist entirely of ones, so every $\binom{1}{2}$ term vanishes. The algorithm correctly outputs zero, matching the fact that no two towers share a line of attack.
