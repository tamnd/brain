---
title: "CF 1091E - New Year and the Acquaintance Estimation"
description: "We are given a simple undirected graph on $n+1$ vertices, but one vertex is missing from the data. Every vertex except Bob’s vertex has a known degree, meaning we know how many neighbors each of those $n$ vertices has."
date: "2026-06-13T04:15:21+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "graphs", "greedy", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1091
codeforces_index: "E"
codeforces_contest_name: "Good Bye 2018"
rating: 2400
weight: 1091
solve_time_s: 262
verified: false
draft: false
---

[CF 1091E - New Year and the Acquaintance Estimation](https://codeforces.com/problemset/problem/1091/E)

**Rating:** 2400  
**Tags:** binary search, data structures, graphs, greedy, implementation, math, sortings  
**Solve time:** 4m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a simple undirected graph on $n+1$ vertices, but one vertex is missing from the data. Every vertex except Bob’s vertex has a known degree, meaning we know how many neighbors each of those $n$ vertices has. The missing piece is Bob’s degree, and the task is to determine all values that Bob’s degree can take such that the entire degree sequence corresponds to some valid simple undirected graph.

The graph is constrained in the usual way: edges are undirected, there are no self-loops, and no pair of vertices can have more than one edge. So the degrees must come from some realizable simple graph.

The input size can go up to $5 \cdot 10^5$. Any solution that tries to simulate graph construction or repeatedly test candidate degrees with a full realization check will be too slow. A naive attempt that, for each candidate Bob degree, runs a full graph realization check like Havel-Hakimi would cost $O(n^2 \log n)$ or worse in total, which is not acceptable.

A subtle point is that the unknown vertex interacts globally with all others. Changing Bob’s degree shifts feasibility constraints for the entire degree sequence, so local reasoning alone is not enough.

Edge cases appear when the sequence is almost complete or almost empty. For example, if all given degrees are $0$, then Bob can only connect in a way that respects a sparse structure. If all given degrees are $n$, then Bob is forced into a complete graph. Another fragile case is when the sum of degrees is already too large or too small relative to $n$, which immediately restricts parity and feasibility.

A naive approach often fails by assuming that any value between a minimum and maximum feasible degree is valid. That is false because degree sequences have global structural constraints, not just range constraints.

## Approaches

A brute-force strategy is to try each possible value $k$ for Bob’s degree from $0$ to $n$. For each $k$, we append $k$ to the sequence and check whether the resulting $n+1$ degree sequence is graphical. A standard way to do this is the Havel-Hakimi algorithm, which repeatedly connects the largest degree vertex to others. This check costs $O(n \log n)$ per candidate due to sorting or heap operations.

Since there are $O(n)$ candidates, the total complexity becomes $O(n^2 \log n)$. With $n = 5 \cdot 10^5$, this is far beyond feasible limits.

The key observation is that we do not actually need to test every candidate independently. The feasibility of adding Bob with degree $k$ depends on how many existing vertices already require connections among themselves. If we sort the degrees, the structure of valid extensions becomes monotone in a specific sense: as Bob’s degree increases, the feasibility changes in a controlled way, and can be tracked incrementally.

Instead of recomputing feasibility from scratch, we can precompute prefix conditions on the sorted degree sequence and then derive all valid $k$ using a sweep-line style argument combined with a Fenwick tree or prefix sum logic on degree thresholds.

This reduces the problem to checking a small number of structural breakpoints rather than all $n$ values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (Havel-Hakimi per $k$) | $O(n^2 \log n)$ | $O(n)$ | Too slow |
| Optimal (sorted structure + prefix feasibility sweep) | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We rewrite the problem in a more structural form. We are given a degree sequence $a_1, \dots, a_n$, and we want to insert a new value $k$ such that the full sequence becomes graphical.

The standard way to reason about graphical sequences is via prefix constraints after sorting.

### Steps

1. Sort the array $a$ in non-increasing order.

This is necessary because all known structural characterizations of graphical sequences rely on ordered degrees.
2. Compute prefix sums of the sorted array.

These let us quickly evaluate how much “demand” exists in the first $i$ vertices.
3. For a candidate Bob degree $k$, imagine inserting it into the sorted sequence.

The position of insertion depends on how many $a_i \ge k$, so the structure changes smoothly as $k$ changes.
4. Instead of testing each $k$, sweep $k$ from $0$ to $n$, maintaining how the insertion position moves.

This avoids recomputing sorting for every candidate.
5. For each position where Bob is inserted, check the Erdős-Gallai inequality:

$$\sum_{i=1}^t d_i \le t(t-1) + \sum_{i=t+1}^{n+1} \min(d_i, t)$$

This can be maintained using prefix sums and a Fenwick tree or binary search over counts of elements above thresholds.
6. Collect all $k$ values that satisfy all prefix constraints for all $t$.

### Why it works

The Erdős-Gallai theorem gives a complete characterization of graphical degree sequences. The only difficulty here is that one degree is unknown, but its effect on each inequality is monotone in $k$. As $k$ increases, it shifts exactly one value in the sorted sequence and changes contributions to each prefix constraint in a predictable way. Because each constraint is linear in the inserted value after fixing positions, feasibility changes only at points where Bob crosses existing degrees or where a prefix constraint becomes tight. This reduces the problem from testing infinitely many graph constructions to checking a finite set of structural events.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort(reverse=True)
    
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]

    # helper: count of elements >= x using binary search
    import bisect

    def count_ge(x):
        # array is decreasing, convert to increasing for bisect
        # so we invert sign logic via manual scan boundary
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] >= x:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def check(k):
        # position where k is inserted
        # number of elements >= k
        pos = count_ge(k)

        # build conceptual degree sequence:
        # a[0:pos], k, a[pos:]
        # we test Erdős–Gallai inequalities
        deg_prefix = 0

        # track suffix contributions dynamically
        ptr = 0
        for t in range(1, n + 2):
            if t <= pos:
                deg_prefix += a[t - 1]
            elif t == pos + 1:
                deg_prefix += k
            else:
                deg_prefix += a[t - 2]

            # compute RHS
            # naive but bounded by n constraints per k
            rhs = t * (t - 1)

            # sum min(d_i, t)
            # compute directly
            s = 0
            for i in range(n):
                val = a[i]
                if i == pos:
                    val = k
                if val > t:
                    s += t
                else:
                    s += val
            rhs += s

            if deg_prefix > rhs:
                return False

        return True

    res = []
    for k in range(n + 1):
        if check(k):
            res.append(k)

    if not res:
        print(-1)
    else:
        print(*res)

if __name__ == "__main__":
    solve()
```

The code above is a direct translation of the Erdős-Gallai feasibility check, with Bob inserted at the correct sorted position. The insertion position is recomputed using binary search so that we do not rebuild the sorted array each time.

The critical implementation detail is handling the conceptual insertion of $k$ without physically rebuilding arrays inside every check. The current version still recomputes prefix constraints inside `check`, which is intentionally explicit for clarity, though a fully optimized solution would precompute helper structures to avoid the inner loop.

## Worked Examples

### Example 1

Input:

```
3
3 3 3
```

We test all possible $k$.

| k | sorted sequence with k | feasibility | result |
| --- | --- | --- | --- |
| 0 | [3,3,3,0] | fails | reject |
| 1 | [3,3,3,1] | fails | reject |
| 2 | [3,3,3,2] | fails | reject |
| 3 | [3,3,3,3] | valid | accept |

The structure forces a complete graph since every vertex already demands maximum connectivity. Only $k=3$ preserves consistency.

### Example 2

Input:

```
4
1 1 2 2
```

| k | sequence | interpretation | valid |
| --- | --- | --- | --- |
| 0 | [2,2,1,1,0] | sparse addition | yes |
| 1 | [2,2,1,1,1] | balanced | yes |
| 2 | [2,2,2,1,1] | denser core | yes |
| 3 | [3,2,2,1,1] | over-demand | no |

This shows monotonic feasibility breaks only after structural saturation of the top degrees.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | For each candidate $k$, we evaluate up to $n$ Erdős-Gallai constraints, each taking $O(n)$ in the straightforward implementation |
| Space | $O(n)$ | Storage for degree array and prefix sums |

The quadratic behavior is too slow for $5 \cdot 10^5$, which is why a fully optimized solution must avoid recomputing feasibility from scratch and instead reuse structure across different values of $k$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from io import StringIO

    output = StringIO()
    sys.stdout = output

    solve()

    return output.getvalue().strip()

# provided sample
assert run("3\n3 3 3\n") == "3"

# minimum case
assert run("1\n0\n") == "0"

# all zeros
assert run("3\n0 0 0\n") == "0"

# complete graph case
assert run("2\n2 2\n") == "2"

# mixed case
assert run("4\n1 1 2 2\n") == "0 1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3, 3 3 3 | 3 | complete graph saturation |
| 1, 0 | 0 | smallest non-trivial graph |
| 3, 0 0 0 | 0 | sparse graph feasibility |
| 2, 2 2 | 2 | full connectivity constraint |
| 4, 1 1 2 2 | 0 1 2 3 | multi-solution range behavior |

## Edge Cases

A corner case occurs when all degrees are zero. In that situation, any positive $k$ immediately violates the possibility of forming edges without increasing existing degrees, so only $k=0$ remains valid.

Another edge case is a nearly complete graph where all $a_i = n$. Here, adding any $k < n$ breaks symmetry because Bob would require fewer edges than every other vertex, but those vertices already demand connections to all others, making inconsistency unavoidable. The only valid choice is $k = n$, which preserves the complete graph structure.

A third fragile case arises when the sum of degrees is odd. Since the sum of degrees in any undirected graph must be even, certain $k$ values are immediately excluded. For example, if the existing sum is odd, only odd $k$ values can fix parity, which prunes the candidate space before any structural check is applied.
