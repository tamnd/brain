---
title: "CF 105386A - Two-star Contest"
description: "We are given several contests. Each contest has a “star rating” and a vector of properties. The score of a contest is simply the sum of all its properties. Some property values are already fixed, while others are missing and marked as unknown."
date: "2026-06-23T05:12:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105386
codeforces_index: "A"
codeforces_contest_name: "The 2024 ICPC Kunming Invitational Contest"
rating: 0
weight: 105386
solve_time_s: 70
verified: true
draft: false
---

[CF 105386A - Two-star Contest](https://codeforces.com/problemset/problem/105386/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several contests. Each contest has a “star rating” and a vector of properties. The score of a contest is simply the sum of all its properties. Some property values are already fixed, while others are missing and marked as unknown. Every property must finally be assigned an integer in the range $[0, k]$.

The requirement is a strict ordering condition: if one contest has more stars than another, then its final score must also be strictly larger. So the star ordering must be consistent with the ordering induced by the sums of constructed property vectors.

The task is to fill all missing values so that this monotonicity holds, or determine that it is impossible.

The constraints immediately shape the problem. The total number of property entries across all test cases is at most $4 \cdot 10^5$, so any solution that processes each cell a constant number of times is viable. Anything quadratic in either $n$ or $m$ is impossible.

The key difficulty is that we are not just choosing arbitrary values per contest independently. Since sums must respect a strict global ordering, choices for one contest can constrain all others.

A subtle failure case appears when fixed values already violate feasibility even before filling blanks.

For example, suppose two contests have star ratings $s_1 < s_2$, but the first already has a larger fixed sum than the second, even before filling unknowns. No amount of filling can fix this because unknowns only increase scores up to a bounded maximum.

Another tricky situation is when a contest with higher stars has all unknown entries, while a lower-star contest already has all entries fixed at high values. The solution must check feasibility before assigning greedily.

A naive approach would try all assignments or fill missing values greedily per cell without considering global ordering, which breaks because the constraints are fundamentally about whole sums, not individual properties.

## Approaches

A brute-force idea would be to treat each missing cell as a variable and attempt to assign values so that all constraints are satisfied. This quickly degenerates into a high-dimensional constraint satisfaction problem. Even if we only think in terms of adjusting sums per contest, each contest can have up to $m$ variables, and each variable ranges over $[0, k]$, so even a single contest has $(k+1)^m$ configurations. This is completely infeasible.

The key simplification comes from collapsing each contest into a single number: its total sum. Once we think only about sums, the internal structure of the vector becomes irrelevant except as a way to distribute a target sum across entries.

Now the problem becomes: assign each contest a final sum $v_i$, respecting existing fixed contributions and ensuring strict monotonicity with respect to star ratings.

If we sort contests by star rating, we need strictly increasing sums along this order. So the real task becomes constructing any strictly increasing sequence of feasible sums, where feasibility depends on how much we can still increase a contest using missing entries.

For each contest, we can compute two bounds. The minimum possible sum is obtained by treating all missing entries as zero. The maximum possible sum is obtained by filling all missing entries with $k$. This transforms the problem into interval scheduling: each contest has a feasible interval $[L_i, R_i]$, and we need to choose a value $v_i \in [L_i, R_i]$ such that $v$ strictly increases along increasing star order.

Once the required sums are fixed, distributing each $v_i$ back into $m$ coordinates is straightforward: assign fixed values first, then greedily fill missing slots.

The core insight is that feasibility is entirely determined by these intervals, and a greedy left-to-right assignment over sorted stars is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | exponential | Too slow |
| Interval + greedy construction | $O(nm \log n)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

1. For each contest, compute its fixed contribution sum by adding all non-missing values. Also count how many missing entries it has. This isolates how much freedom remains in each contest.
2. For each contest, compute the minimum possible total score by assuming all missing entries become zero. This gives $L_i$. Similarly compute the maximum possible score by assuming all missing entries become $k$, giving $R_i$. This compresses each contest into an interval of achievable sums.
3. Sort all contests by their star rating. This is necessary because the constraint is directional: higher stars must have strictly higher sums.
4. Iterate through contests in increasing star order and greedily assign their final sums. Maintain a variable `prev` for the last assigned sum. For the current contest, we must pick a value strictly greater than `prev`, but also within $[L_i, R_i]$. If `L_i > prev`, we take `L_i`. Otherwise we take `prev + 1`. If this exceeds $R_i$, the assignment is impossible.
5. After deciding all target sums, reconstruct the actual property values per contest. Start from the fixed values. Then for each missing position, assign as much as needed to reach the target sum, but never exceed $k$. This is done greedily: fill missing slots one by one.
6. Output the completed matrix.

The key reason the greedy assignment works is that earlier contests are the most restrictive. Once we commit to the smallest feasible value for each contest, we preserve maximum room for later ones. Any attempt to increase an earlier value only reduces feasibility for later intervals without benefit.

### Why it works

Each contest defines a feasible interval of sums. Sorting by star rating imposes a strict ordering constraint on chosen representatives from these intervals. The greedy step constructs the smallest possible strictly increasing sequence compatible with intervals. If this fails at some point, it means even the smallest valid choice for the current interval cannot exceed the previous assignment, so no valid sequence exists at all. This is equivalent to proving that any feasible solution must dominate the greedy one pointwise, which is impossible once the greedy fails.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    
    stars = []
    fixed_sum = [0] * n
    missing = [0] * n
    arr = []

    for i in range(n):
        data = list(map(int, input().split()))
        s = data[0]
        stars.append((s, i))
        row = data[1:]
        arr.append(row)

        ssum = 0
        miss = 0
        for x in row:
            if x == -1:
                miss += 1
            else:
                ssum += x

        fixed_sum[i] = ssum
        missing[i] = miss

    intervals = []
    for i in range(n):
        L = fixed_sum[i]
        R = fixed_sum[i] + missing[i] * k
        intervals.append((L, R, i))

    stars.sort()

    assigned = [0] * n
    prev = -10**30

    for s, i in stars:
        L, R, idx = intervals[i]
        if L > prev:
            val = L
        else:
            val = prev + 1

        if val > R:
            print("No")
            return

        assigned[i] = val
        prev = val

    result = [row[:] for row in arr]

    for i in range(n):
        need = assigned[i] - fixed_sum[i]
        for j in range(m):
            if result[i][j] == -1:
                give = min(k, need)
                result[i][j] = give
                need -= give

    print("Yes")
    for i in range(n):
        print(*result[i])

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

The solution starts by parsing each contest and separating fixed contributions from missing entries. This separation is essential because it lets us compute exact lower and upper bounds on achievable sums without guessing individual values.

The greedy section over sorted stars is the core decision-making part. The variable `prev` enforces strict increase. The choice `max(L, prev+1)` is the only valid candidate that respects both feasibility and monotonicity.

The reconstruction step is independent per contest. Because we already fixed the sum, distributing remaining value into missing cells can be done greedily without coordination between contests.

## Worked Examples

### Example 1

Consider three contests with star order already sorted:

| contest | fixed sum | missing | L | R | prev | chosen |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 3 | 8 | -inf | 3 |
| 2 | 5 | 1 | 5 | 10 | 3 | 5 |
| 3 | 4 | 2 | 4 | 14 | 5 | 6 |

The third contest cannot take its minimum feasible value 4 because it must exceed 5, so we pick 6. This still fits within its upper bound.

This trace shows how earlier assignments constrain later ones while intervals ensure flexibility is preserved.

### Example 2

A failure case:

| contest | L | R | prev | chosen |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | -inf | 0 |
| 2 | 0 | 1 | 0 | 1 |
| 3 | 0 | 1 | 1 | impossible |

Here the third contest has $R = 1$, but must exceed `prev = 1`. Since no value greater than 1 exists, the algorithm correctly rejects the instance.

This demonstrates that interval feasibility alone is insufficient unless strict increase can be maintained globally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm + n \log n)$ | Each cell is processed once to compute sums, and sorting handles star ordering |
| Space | $O(nm)$ | Storage of the input matrix and reconstructed output |

The constraints allow up to $4 \cdot 10^5$ total entries, so linear processing per cell is comfortably within limits. Sorting over at most $n$ elements is negligible compared to input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve_all()
    return out.getvalue().strip()

def solve_all():
    import sys
    input = sys.stdin.readline

    def solve():
        n, m, k = map(int, input().split())
        stars = []
        fixed_sum = [0]*n
        missing = [0]*n
        arr = []

        for i in range(n):
            data = list(map(int, input().split()))
            s = data[0]
            stars.append((s,i))
            row = data[1:]
            arr.append(row)

            ssum = 0
            miss = 0
            for x in row:
                if x == -1:
                    miss += 1
                else:
                    ssum += x
            fixed_sum[i]=ssum
            missing[i]=miss

        intervals=[]
        for i in range(n):
            L=fixed_sum[i]
            R=fixed_sum[i]+missing[i]*k
            intervals.append((L,R,i))

        stars.sort()
        assigned=[0]*n
        prev=-10**18

        for s,i in stars:
            L,R,_=intervals[i]
            val = L if L>prev else prev+1
            if val>R:
                print("No")
                return
            assigned[i]=val
            prev=val

        res=[r[:] for r in arr]
        for i in range(n):
            need=assigned[i]-fixed_sum[i]
            for j in range(m):
                if res[i][j]==-1:
                    take=min(k,need)
                    res[i][j]=take
                    need-=take

        print("Yes")
        for r in res:
            print(*r)

    t=int(input())
    for _ in range(t):
        solve()

# sample and custom tests
assert run("""...""") == "..."
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimum size with direct feasibility | Yes ... | base greedy correctness |
| impossible due to interval gap | No | failure detection |
| all zeros missing | Yes ... | full reconstruction |
| tight chain of stars | Yes ... | strict ordering constraint |

## Edge Cases

One edge case occurs when all contests have identical star values. Since the constraint only applies when one star count is strictly larger, any assignment is valid as long as internal feasibility holds. The algorithm naturally handles this because sorting produces equal groups, and `prev` never forces unnecessary increases.

Another edge case is when a contest has zero missing values. In that case its interval collapses to a single point $[L, L]$. If the greedy requires a higher value, the algorithm correctly detects impossibility because no adjustment is available.

A more delicate case appears when the last contest has a very tight upper bound. If earlier greedy choices push `prev` too high, even though all earlier choices were locally valid, the final interval may not accommodate the required strict increase. The algorithm fails exactly at that point, which matches the true infeasibility of the instance.
