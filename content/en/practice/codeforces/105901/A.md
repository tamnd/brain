---
title: "CF 105901A - Problem Setting"
description: "We are given a list of numeric attributes, where each attribute starts with an initial value. Alongside this, there are several constraints."
date: "2026-06-21T15:20:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105901
codeforces_index: "A"
codeforces_contest_name: "2025 ICPC Wuhan Invitational Contest (The 3rd Universal Cup. Stage 37: Wuhan)"
rating: 0
weight: 105901
solve_time_s: 57
verified: true
draft: false
---

[CF 105901A - Problem Setting](https://codeforces.com/problemset/problem/105901/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of numeric attributes, where each attribute starts with an initial value. Alongside this, there are several constraints. Each constraint targets a specific attribute index and demands that after modifications, the value at that index must lie inside a given inclusive interval.

We are allowed to adjust any attribute value by repeatedly increasing or decreasing it by 1, and each unit change costs 1 time unit. The task is to modify the initial array so that every constraint is satisfied, while minimizing the total cost across all attributes. If it is impossible to satisfy all constraints simultaneously, the answer must be reported as impossible.

The key observation from the input format is that constraints are independent except for sharing the same attribute index. That means constraints do not interact across different positions; they only intersect within the same index.

The constraints are small in number, at most 100 attributes and 100 constraints per test case. This immediately rules out anything like trying all possible final arrays or doing global search over values. Even iterating over all possible values in the range up to 10^9 is completely infeasible.

A naive approach that tries to adjust each attribute independently while repeatedly checking all constraints would still be acceptable, but anything that simulates step-by-step unit changes is too slow conceptually, even if optimized.

A subtle failure case arises when constraints on the same index are contradictory but not obviously so. For example, if an attribute must lie in [1, 5] according to one constraint and [6, 10] according to another, then no value can satisfy both. A naive solver that only applies the last constraint seen would incorrectly assume feasibility.

Another corner case is when an attribute has no constraints at all. In that case, it should not contribute any cost because it can remain unchanged regardless of its initial value.

## Approaches

A brute-force perspective would attempt to adjust each attribute value by trying all possible final values within a reasonable range, such as scanning from 1 to 10^9 for each index and checking whether it satisfies all constraints. For each candidate value, we would compute its distance from the original value and pick the minimum valid one. This works in principle because we explicitly verify feasibility, but the complexity becomes prohibitive. Even for a single attribute, scanning up to 10^9 values is impossible, and multiplying this by up to 100 attributes makes it entirely infeasible.

The structural simplification comes from realizing that constraints on a fixed index only restrict that index to lie inside an intersection of intervals. Instead of considering many candidate values, we only need the intersection of all ranges affecting that index. Once we have that intersection, the problem for that attribute reduces to choosing the closest point in a segment to a fixed number, which is a standard projection problem on a line.

This transforms the global optimization into independent one-dimensional problems per index. Each attribute contributes independently to the total cost once its feasible interval is known.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 10^9) | O(1) | Too slow |
| Optimal | O(nq) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. For each attribute index, we start by assuming it has no restrictions. We represent its feasible interval as infinitely wide, meaning any value is allowed initially.
2. We iterate over all constraints. For each constraint (p, l, r), we restrict the feasible interval of attribute p by intersecting it with [l, r]. This means we update the lower bound to max(current lower bound, l) and the upper bound to min(current upper bound, r). This step ensures we accumulate all requirements without losing any constraint.
3. After processing all constraints, we check each attribute interval. If for any index the lower bound becomes greater than the upper bound, the intersection is empty and no value can satisfy all constraints. In this case, the answer is immediately -1.
4. If the interval is valid, we compute the minimum cost to move the initial value into this interval. If the initial value is already inside, cost is zero. If it is below the interval, we move it up to the lower bound. If it is above, we move it down to the upper bound. We accumulate this cost over all attributes.
5. Finally, we output the total accumulated cost.

The core idea is that each attribute is reduced to choosing a point in a segment that minimizes distance to a fixed value.

### Why it works

For each index, all constraints only restrict membership in intervals, and membership in multiple intervals is equivalent to membership in their intersection. Any valid final value must lie inside this intersection, and every value inside it is equally valid with respect to constraints. Therefore, minimizing cost reduces to a closest-point problem on a closed interval. Since distance on a line is convex, the closest valid point is always either the original value (if inside), or one of the interval boundaries. This guarantees optimality independently per attribute, and independence across attributes ensures summing these local optima gives the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    L = [-INF] * n
    R = [INF] * n

    for _ in range(q):
        p, l, r = map(int, input().split())
        p -= 1
        if l > L[p]:
            L[p] = l
        if r < R[p]:
            R[p] = r

    ok = True
    for i in range(n):
        if L[i] == -INF:
            L[i] = 1
            R[i] = 10**9

        if L[i] > R[i]:
            ok = False
            break

    if not ok:
        print(-1)
        continue

    ans = 0
    for i in range(n):
        if a[i] < L[i]:
            ans += L[i] - a[i]
        elif a[i] > R[i]:
            ans += a[i] - R[i]

    print(ans)
```

The implementation maintains two arrays representing the feasible range for each attribute. Constraints are applied by tightening these ranges. A subtle point is handling attributes with no constraints; they are treated as fully free by initializing them to a wide interval and later converting untouched ones into the full allowed domain.

The cost computation is done after feasibility is confirmed, since computing distance before checking intersection validity could otherwise waste work or hide impossible cases.

## Worked Examples

Consider a case with three attributes:

Input:

```
n = 3, q = 3
a = [20, 25, 4]
constraints:
1: (3, 5, 7)
2: (1, 10, 15)
3: (3, 2, 6)
```

We track intervals per index.

| Index | Initial Interval | After constraint 1 | After constraint 2 | After constraint 3 | Final Interval |
| --- | --- | --- | --- | --- | --- |
| 1 | [-inf, inf] | unchanged | [10, 15] | unchanged | [10, 15] |
| 2 | [-inf, inf] | unchanged | unchanged | unchanged | [1, 1e9] |
| 3 | [-inf, inf] | [5, 7] | unchanged | [5, 6] | [5, 6] |

Now compute cost:

For index 1, 20 is above [10, 15], so cost is 5.

For index 2, 25 lies inside free range, cost is 0.

For index 3, 4 is below [5, 6], so cost is 1.

Total cost is 6.

This trace shows that constraints compress into intervals and the final adjustment is purely geometric distance.

Now consider a feasibility failure case:

```
n = 1
a = [10]
constraints: [1, 1, 5], [1, 6, 8]
```

| Step | Interval |
| --- | --- |
| start | [-inf, inf] |
| after first | [1, 5] |
| after second | [6, 5] |

The interval becomes invalid since lower bound exceeds upper bound, so the output is -1. This demonstrates that contradiction detection reduces to a simple interval intersection check.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test case | Each constraint updates one interval once, and each index is processed once |
| Space | O(n) | Two arrays store interval bounds per attribute |

Given that both n and q are at most 100 and there are at most 100 test cases, this runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    INF = 10**18

    t = int(input())
    out = []
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))

        L = [-INF] * n
        R = [INF] * n

        for _ in range(q):
            p, l, r = map(int, input().split())
            p -= 1
            L[p] = max(L[p], l)
            R[p] = min(R[p], r)

        ok = True
        for i in range(n):
            if L[i] == -INF:
                L[i], R[i] = 1, 10**9
            if L[i] > R[i]:
                ok = False
                break

        if not ok:
            out.append("-1")
            continue

        ans = 0
        for i in range(n):
            if a[i] < L[i]:
                ans += L[i] - a[i]
            elif a[i] > R[i]:
                ans += a[i] - R[i]

        out.append(str(ans))

    return "\n".join(out)

# minimal feasible
assert run("""1
1 0
10
""") == "0"

# contradiction
assert run("""1
1 2
10
1 1 5
1 6 8
""") == "-1"

# already satisfied
assert run("""1
2 2
5 7
1 1 10
2 6 8
""") == "0"

# needs adjustment both sides
assert run("""1
2 2
0 20
1 5 10
2 0 15
""") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single attribute, no constraints | 0 | free variables cost nothing |
| conflicting constraints | -1 | infeasible intersection detection |
| already satisfied intervals | 0 | no unnecessary movement |
| mixed adjustments | 15 | correct distance-to-interval logic |

## Edge Cases

When an attribute has no constraints at all, the algorithm assigns it a full valid domain. Since the initial value always lies inside that domain, the computed cost remains zero, which matches the fact that no constraint forces any change.

When constraints are contradictory, such as disjoint intervals on the same index, the intersection collapses immediately during processing. The algorithm detects this purely through interval bounds without needing to simulate values, and correctly outputs -1.

When the initial value lies exactly on the boundary of the final interval, both inequality branches avoid adding cost, since movement is only needed when strictly outside. This ensures that boundary-adjacent cases do not introduce off-by-one errors in distance computation.
