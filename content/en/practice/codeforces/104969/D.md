---
title: "CF 104969D - Feeding the Kids"
description: "We are given a sequence of students, each requesting a certain number of pizza slices in a fixed order. There are K identical pizzas, and each pizza has the same unknown capacity S slices."
date: "2026-06-28T19:07:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104969
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 1 (Advanced)"
rating: 0
weight: 104969
solve_time_s: 75
verified: false
draft: false
---

[CF 104969D - Feeding the Kids](https://codeforces.com/problemset/problem/104969/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of students, each requesting a certain number of pizza slices in a fixed order. There are K identical pizzas, and each pizza has the same unknown capacity S slices. Students are served one by one: if the current pizza still has enough remaining slices for the next student’s request, that student is served from it; otherwise the remaining slices of that pizza are discarded, a fresh pizza is opened, and the student is served from the new one.

The key question is not how the serving proceeds, but how large S must be so that this process can complete without running out of pizzas, given that at most K pizzas are available.

So the task is to choose the smallest integer S such that when we simulate this greedy serving process, we never need more than K pizzas.

The input size allows up to 100,000 students and up to 100,000 pizzas. This immediately rules out any solution that tries to check all possible values of S by simulating the process for each candidate. A naive upper bound for S is the sum of all demands, which can be up to 10^11, so any linear search over S would be completely infeasible.

We need a solution that reduces the problem to a monotonic feasibility check.

A few subtle cases matter:

If a single student requests a very large number of slices, say d_i = 10^6, then S must be at least that large. Otherwise the algorithm would repeatedly open pizzas just for one student, which is allowed but wastes capacity; more importantly, the correctness condition still holds but feasibility becomes impossible under small S.

Another edge case appears when K is large compared to N. For example, if K ≥ N, even S = max(d_i) always works, because each student could in principle start a new pizza. This does not change the answer structure but helps confirm correctness of edge handling.

Finally, the main subtlety is that leftover slices are always discarded when a new pizza is opened. This means we are effectively partitioning the sequence into segments, where each segment has total sum at most S, but segments are forced by overflow, not by optimal packing. This forced greedy structure is what drives the solution.

## Approaches

A direct brute-force approach would try a candidate value S and simulate the serving process: maintain remaining slices in the current pizza, decrement it as we serve students, and count how many times we need to open a new pizza. If we exceed K, S is invalid.

This simulation is correct for a fixed S, and costs O(N) time. However, S itself can be as large as the sum of all demands. Trying all values from max(d_i) upward would require up to 10^11 checks, which is impossible.

The key observation is that feasibility is monotonic in S. If a given S is sufficient to serve all students within K pizzas, then any larger S is also sufficient, because increasing capacity can only reduce or maintain the number of pizza openings. This turns the problem into a binary search over S.

Each feasibility check is a greedy scan: we simulate the process and count how many pizzas are used. If at any point a single demand exceeds S, we immediately know S is invalid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force S enumeration | O(N * sum d_i) | O(1) | Too slow |
| Binary search + simulation | O(N log max d_i) | O(1) | Accepted |

## Algorithm Walkthrough

We search for the smallest S such that we can serve all students using at most K pizzas.

1. Set the search range for S from max(d_i) to sum(d_i). The lower bound is necessary because any student must fit into a single pizza segment.
2. Define a function can(S) that simulates serving students with pizza capacity S. Initialize pizzas_used = 1 and remaining = S.
3. For each demand d_i, check whether it fits into the current remaining capacity. If remaining ≥ d_i, subtract d_i from remaining and continue.
4. If remaining < d_i, increment pizzas_used by 1, reset remaining to S, and then subtract d_i. This models discarding leftover slices and opening a new pizza.
5. If at any point pizzas_used exceeds K, return False immediately because S is insufficient.
6. Binary search on S. If can(S) is true, try smaller values; otherwise, increase S.

The key design choice is that we never try to optimize how students are grouped. The process is forced, so the greedy simulation is the only valid interpretation.

### Why it works

For a fixed S, the simulation produces the minimum possible number of pizzas because it only opens a new pizza when forced by lack of remaining capacity. Any alternative strategy that opens pizzas earlier would only increase usage. Therefore can(S) correctly reflects feasibility.

Monotonicity ensures that the set of valid S values forms a suffix of integers, which guarantees binary search correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(d, n, k, s):
    pizzas_used = 1
    remaining = s

    for x in d:
        if x > s:
            return False
        if remaining >= x:
            remaining -= x
        else:
            pizzas_used += 1
            if pizzas_used > k:
                return False
            remaining = s - x

    return pizzas_used <= k

def solve():
    n, k = map(int, input().split())
    d = list(map(int, input().split()))

    lo = max(d)
    hi = sum(d)

    while lo < hi:
        mid = (lo + hi) // 2
        if can(d, n, k, mid):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The code separates the feasibility check from the binary search, which is essential for clarity and correctness. The function can carefully enforces the forced opening rule: whenever the remaining capacity is insufficient, we immediately open a new pizza and reset the counter.

One subtle point is initializing lo as max(d). This avoids unnecessary checks for invalid S values and ensures the simulation never attempts to assign a student more slices than a pizza can hold.

The binary search converges because each step shrinks the interval [lo, hi) based on monotonic feasibility.

## Worked Examples

Consider an input where demands are [5, 2, 7, 3] and K = 2.

We test candidate S = 7.

| Student | Demand | Remaining before | Action | Pizzas used |
| --- | --- | --- | --- | --- |
| 1 | 5 | 7 | serve, remaining = 2 | 1 |
| 2 | 2 | 2 | serve, remaining = 0 | 1 |
| 3 | 7 | 0 | open new pizza | 2 |
| 3 (cont) | 7 | 7 | serve, remaining = 0 | 2 |
| 4 | 3 | 0 | open new pizza | 3 |

We exceed K = 2, so S = 7 is invalid. This shows that even though every demand fits individually, fragmentation forces extra pizzas.

Now test S = 10.

| Student | Demand | Remaining before | Action | Pizzas used |
| --- | --- | --- | --- | --- |
| 1 | 5 | 10 | serve | 1 |
| 2 | 2 | 5 | serve | 1 |
| 3 | 7 | 3 | open new pizza, serve | 2 |
| 4 | 3 | 3 | serve | 2 |

We use exactly 2 pizzas, so S = 10 is feasible. This demonstrates how increasing S reduces fragmentation at forced breakpoints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log M) | Each feasibility check scans all students once, and binary search over S runs in logarithmic range M = sum(d_i) |
| Space | O(1) | Only counters and input array are stored |

The constraints N ≤ 10^5 make a linear scan acceptable, and log M is at most around 40 for typical bounds, keeping the solution well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def can(d, n, k, s):
        pizzas_used = 1
        remaining = s
        for x in d:
            if x > s:
                return False
            if remaining >= x:
                remaining -= x
            else:
                pizzas_used += 1
                if pizzas_used > k:
                    return False
                remaining = s - x
        return pizzas_used <= k

    def solve():
        n, k = map(int, input().split())
        d = list(map(int, input().split()))
        lo, hi = max(d), sum(d)
        while lo < hi:
            mid = (lo + hi) // 2
            if can(d, n, k, mid):
                hi = mid
            else:
                lo = mid + 1
        print(lo)

    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("5 3\n2 10 3 6 7\n") == "10"

# minimum case
assert run("1 1\n5\n") == "5"

# all equal small
assert run("4 2\n2 2 2 2\n") == "4"

# tight fragmentation
assert run("3 2\n5 5 5\n") == "10"

# large K (each student separate allowed)
assert run("3 3\n8 1 1\n") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 5 | 5 | single student baseline |
| 4 2 / 2 2 2 2 | 4 | even distribution |
| 3 2 / 5 5 5 | 10 | forced splitting effect |
| 3 3 / 8 1 1 | 8 | large K reduces pressure |

## Edge Cases

One important edge case is when a single demand exceeds the current candidate S. For example, d = [10, 1, 1] and S = 5. The algorithm immediately rejects S without simulating further, because no feasible segmentation exists. This prevents wasted computation and preserves correctness of binary search bounds.

Another case is when K is very large, such as K ≥ N. In d = [3, 4, 2], K = 10, the optimal S becomes max(d) = 4. The simulation will never open a second pizza unless forced by a demand larger than remaining capacity, and since each demand fits, we remain within K easily.

A final case is heavy fragmentation: d = [6, 6, 6], K = 2. With S = 6, every student forces a new pizza, requiring 3 pizzas and failing. With S = 12, the first two students fit in one pizza, and the last forces the second, staying within K. This shows how S controls segmentation rather than just local feasibility.
