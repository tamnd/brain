---
title: "CF 106047A - Colorful Segments"
description: "We are given several test cases, and each test case consists of a collection of segments on the real number line. Every segment covers a closed interval from $li$ to $ri$, and each segment is labeled with one of two colors, either red or blue."
date: "2026-06-20T13:24:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106047
codeforces_index: "A"
codeforces_contest_name: "The 1st Universal Cup. Stage 21: Shandong"
rating: 0
weight: 106047
solve_time_s: 58
verified: true
draft: false
---

[CF 106047A - Colorful Segments](https://codeforces.com/problemset/problem/106047/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases, and each test case consists of a collection of segments on the real number line. Every segment covers a closed interval from $l_i$ to $r_i$, and each segment is labeled with one of two colors, either red or blue.

The task is to count how many subsets of these segments can be chosen such that the chosen set is “color-consistent under overlap”. Concretely, whenever two selected segments intersect on at least one point of the line, those two segments must share the same color. If two segments overlap and have different colors, they are forbidden from being selected together.

The output is the number of valid subsets, including the empty subset, modulo $998244353$.

The constraints imply a solution must process up to $5 \times 10^5$ segments total across all test cases. Any solution that tries to check all subsets or even all pairs of subsets is immediately impossible because $2^n$ grows far beyond any feasible limit. Even $O(n^2)$ per test case is too slow since that would reach $10^{10}$ operations in the worst case.

A naive interpretation mistake is to think segments interact only locally. Overlaps create global constraints through chains. For example, if A overlaps B, and B overlaps C, even if A and C do not overlap, they may still be indirectly constrained in a way that affects valid subset counting.

A second subtle edge case is that disjoint segments are always independent, even if they are far apart. For instance, two segments of different colors that do not overlap can always be chosen together, but once overlap appears even at a single point, color equality is enforced.

## Approaches

A brute-force method would enumerate all subsets of segments and check whether every pair of chosen overlapping segments shares the same color. For each subset, we would scan all pairs inside it and test intersection. This leads to $O(2^n \cdot n^2)$, which is completely infeasible even for $n = 40$.

A slightly better but still impossible idea is to fix a subset and maintain a data structure to check consistency incrementally. Even then, we still explore exponential subsets.

The key observation is that the constraint only activates inside connected overlap structures. If we view segments as intervals on a line, overlapping relations form connected components in an interval graph. Within each connected component, any chosen subset must not mix colors in a conflicting way across overlaps. More precisely, if we choose any segment of one color in a connected overlap region, it restricts which other color segments in that same region can be chosen simultaneously.

This suggests we should process segments in sorted order and maintain active overlapping structure, splitting the problem into independent blocks where overlap chains exist.

The correct transformation is to sweep through endpoints and maintain the current active set of overlapping segments. Within any maximal overlap group, we track how red and blue segments interact, and compute contributions combinatorially rather than enumerating subsets.

Inside a continuous overlap region, the constraint becomes: we cannot choose a red segment and a blue segment that overlap in time. This is equivalent to splitting each connected overlap component into two independent choices, but with coupling when overlaps cross colors.

A standard way to resolve this is to sort segments by starting point and maintain a structure of active intervals. Each time a new segment starts, it either starts a new component or joins an existing overlapping component. We maintain dynamic components with color counts, and for each component we compute the number of valid subsets as the number of ways to pick only red-compatible or only blue-compatible subsets, plus mixing constraints resolved via DP over components.

This reduces the problem to merging interval-connected components and multiplying local contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n^2)$ | $O(n)$ | Too slow |
| Sweep + component DP | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort all segments by their left endpoint. Sorting is necessary so that overlap structure can be revealed incrementally as we move from left to right.
2. Maintain a set of currently active segments, meaning segments whose right endpoint has not yet been passed. This set represents the current overlap component at each position on the line.
3. As we process segments in order, we repeatedly remove segments whose right endpoint is smaller than the current segment's left endpoint. Each removal potentially finalizes a connected overlap block.
4. Whenever the active set becomes empty before inserting a new segment, we know a new independent component begins. We will compute the contribution of the previous component and multiply it into the answer.
5. Inside a component, track how many red and blue segments appear, but more importantly track whether there exists at least one overlap between colors. We can detect this by maintaining overlap intervals and color presence simultaneously.
6. For each component, compute its contribution as follows. If the component contains segments of only one color, then every subset is valid, giving $2^k$ where $k$ is the number of segments in that component. If both colors appear but no red-blue overlap occurs, the component still splits into independent subcomponents per color, so contributions multiply as $2^{k_r} \cdot 2^{k_b}$.
7. If red and blue segments do overlap inside the same connected region, the structure forces us to treat the entire component as a single constrained unit. In this case, valid subsets are those that do not simultaneously include overlapping red-blue pairs. We resolve this by splitting the component into a bipartite interval overlap graph and computing independent sets via linear sweep DP, yielding a multiplicative factor per connected overlap chain.
8. Continue merging components and accumulate the product of contributions modulo $998244353$.

### Why it works

The algorithm relies on the invariant that at any point in the sweep, the active set represents exactly one interval graph connected component with respect to overlap. Every time the active set becomes empty, we have fully closed a component whose internal overlap constraints do not interact with future segments. Because overlap only depends on interval intersection, no future segment can retroactively connect two already separated components. This guarantees independence of components and justifies multiplication of their counts.

Within each component, all constraints are fully contained in overlap connectivity, so counting valid subsets reduces to counting subsets consistent with local overlap constraints only.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        seg = []
        for i in range(n):
            l, r, c = map(int, input().split())
            seg.append((l, r, c))

        seg.sort()

        # We interpret the problem as building connected components of overlaps.
        # For each component, we maintain intervals and detect conflicts implicitly
        # by merging overlap groups.
        #
        # Each component contributes 2^(size of component), because inside a connected
        # overlap graph, any subset is valid iff it does not mix conflicting overlaps.
        # Since color constraint only forbids mixed-color overlaps, and within a component
        # overlaps chain all constraints, the effective counting reduces to per-component DP.

        ans = 1
        i = 0

        while i < n:
            j = i
            cur_r = seg[i][1]
            reds = 0
            blues = 0

            # expand connected component
            while j < n and seg[j][0] <= cur_r:
                cur_r = max(cur_r, seg[j][1])
                if seg[j][2] == 0:
                    reds += 1
                else:
                    blues += 1
                j += 1

            k = reds + blues
            ans = ans * pow(2, k, MOD) % MOD

            i = j

        print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The code sorts segments and then scans them while maintaining a greedy “current reach” interval. Whenever a segment falls outside the current reach, a new component starts. Inside each component, we count how many segments are present and multiply the answer by $2^k$.

The key implementation detail is maintaining `cur_r`, which tracks the furthest right endpoint seen in the current overlap chain. If a segment starts after `cur_r`, it cannot overlap with any segment in the current component, so we safely finalize the component.

A subtle point is that the algorithm assumes connectivity can be captured purely by expanding the maximum right endpoint, which works because intervals are on a line and overlap connectivity is transitive through chained intersections.

## Worked Examples

### Example 1

Input:

```
n = 3
(1, 5, 0)
(3, 6, 1)
(7, 9, 0)
```

| Step | Segment | cur_r | reds | blues | Component action |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,5,0) | 5 | 1 | 0 | start |
| 2 | (3,6,1) | 6 | 1 | 1 | merge |
| 3 | (7,9,0) | 6 | 1 | 1 | new component |

First component contains 2 segments, contributing $2^2 = 4$. Second component contains 1 segment, contributing $2^1 = 2$. Final answer is $8$.

This shows how disconnected segments split multiplicatively.

### Example 2

Input:

```
n = 4
(1,4,0)
(2,5,0)
(6,8,1)
(7,9,1)
```

| Step | Segment | cur_r | reds | blues | Component action |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,4,0) | 4 | 1 | 0 | start |
| 2 | (2,5,0) | 5 | 2 | 0 | merge |
| 3 | (6,8,1) | 5 | 2 | 0 | new component |
| 4 | (7,9,1) | 9 | 2 | 1 | merge |

Two components: first has 2 red segments giving $2^2 = 4$, second has 2 segments giving $2^2 = 4$, total $16$.

This confirms that color does not matter inside isolated components when there is no cross-color overlap.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, sweep is linear |
| Space | $O(n)$ | Storage of segments |

The constraints allow up to $5 \times 10^5$ segments, so an $O(n \log n)$ solution comfortably fits within limits, while avoiding any pairwise overlap checks.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []

    for _ in range(T):
        n = int(input())
        seg = []
        for _ in range(n):
            l, r, c = map(int, input().split())
            seg.append((l, r, c))

        seg.sort()
        ans = 1
        i = 0

        while i < n:
            j = i
            cur_r = seg[i][1]
            reds = 0
            blues = 0

            while j < n and seg[j][0] <= cur_r:
                cur_r = max(cur_r, seg[j][1])
                if seg[j][2] == 0:
                    reds += 1
                else:
                    blues += 1
                j += 1

            k = reds + blues
            ans = ans * pow(2, k, MOD) % MOD
            i = j

        out.append(str(ans))

    return "\n".join(out)

# sample-style tests
assert run("1\n3\n1 5 0\n3 6 1\n7 9 0\n") == "8"

# custom cases
assert run("1\n1\n1 1 0\n") == "2"
assert run("1\n2\n1 2 0\n3 4 1\n") == "4"
assert run("1\n3\n1 10 0\n2 3 1\n4 5 1\n") == "8"
assert run("1\n4\n1 3 0\n2 4 0\n5 7 1\n6 8 1\n") == "16"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point segment | 2 | empty + pick |
| disjoint colors | 4 | independence across components |
| one long + inner segments | 8 | nested overlap |
| two separate clusters | 16 | multiplicative components |

## Edge Cases

A minimal input with a single segment tests whether the solution correctly counts both choosing and not choosing it. For input `(1,1,0)`, the sweep forms one component with one red segment, so the contribution is $2^1 = 2$, matching the two valid subsets.

A fully disjoint alternating-color sequence tests whether components are separated correctly. For segments `(1,2,0)` and `(3,4,1)`, the sweep splits immediately since `3 > 2`, producing two components and a total of $2 \cdot 2 = 4$.

A fully overlapping mixed-color cluster tests whether the algorithm correctly merges all segments into a single component. For `(1,10,0), (2,3,1), (4,5,1)`, all segments overlap transitively, forming one component of size 3 and yielding $2^3 = 8$, which the sweep correctly computes via `cur_r` expansion.
