---
title: "CF 105699M - Meta"
description: "We are given a small set of programming contest problems, and for each problem we know how long each of three teammates would need to implement it if they are the one assigned to it. A value of -1 means that a particular teammate is unable to implement that problem at all."
date: "2026-06-22T04:54:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105699
codeforces_index: "M"
codeforces_contest_name: "OCPC 2024 Winter, Day 8: Borys Minaiev Contest 1 (The 3rd Universal Cup. Stage 27: London)"
rating: 0
weight: 105699
solve_time_s: 45
verified: true
draft: false
---

[CF 105699M - Meta](https://codeforces.com/problemset/problem/105699/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small set of programming contest problems, and for each problem we know how long each of three teammates would need to implement it if they are the one assigned to it. A value of `-1` means that a particular teammate is unable to implement that problem at all.

The team has only one shared computer, so they cannot work in parallel. They also have a fixed contest duration of 300 minutes. Each problem, if chosen, is assigned to exactly one teammate, and the time contribution is the corresponding implementation time of that teammate for that problem. The goal is to select as many distinct problems as possible such that each chosen problem is assigned to a teammate who can solve it and the sum of all chosen implementation times does not exceed 300.

The structure of the input is essentially a collection of up to 14 items, each item being a triple of costs over three “knapsacks”, where each item can either be taken with one of the valid costs or skipped entirely. We are not asked to maximize total value, but instead maximize the number of items selected under a single global time budget.

The constraint `n ≤ 14` is the critical signal. With at most 14 problems, any solution that explores subsets of problems is viable, since `2^14 = 16384`, which is small enough to allow checking every subset explicitly. The additional dimension of three choices per item does not change that feasibility, because it can be resolved inside each subset by a simple decision rule.

The only subtle edge case comes from `-1` values. A naive interpretation might treat `-1` as zero or ignore feasibility incorrectly, which would allow impossible assignments.

For example, if a problem is:

```
A -1 20 10
```

then assigning it to the first teammate is impossible. A wrong greedy approach might still try to “pick the minimum time” and mistakenly treat it as zero, leading to overcounting feasible sets. The correct handling is that this option is excluded entirely.

Another edge case is when all three values are `-1`. In that case, the problem can never be chosen and must always be ignored, even if all other problems are small.

## Approaches

A direct way to think about this problem is to imagine trying all possible ways of selecting and assigning problems. For each subset of problems, we would decide which teammate solves each chosen problem and compute the total time. If the total is at most 300, we update the best answer by the size of that subset.

This brute-force view is correct but has two layers of combinatorics. First, there are `2^n` subsets of problems. For each subset, each chosen problem has up to 3 assignment choices, so a naive expansion would look like `O(3^n)`. Even with `n = 14`, this is already borderline if implemented without care, though still technically feasible in optimized code. However, it is unnecessary to consider all assignments independently.

The key simplification is that for any fixed subset of problems, the optimal assignment is trivial: for each problem in the subset, we only ever care about the minimum valid time among the three teammates. There is no interaction between problems in terms of assignment choices, because each problem consumes the same shared time resource regardless of who solves it. This removes the second combinatorial layer entirely.

So the problem collapses into selecting a subset of items where each item has a single effective cost, defined as the minimum of its valid implementation times. We then want the maximum number of items whose total cost does not exceed 300. This is a classic knapsack variant where the objective is cardinality maximization with a small item count.

We now only need to evaluate all subsets, compute their total cost and size, and track the best feasible size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full assignment enumeration | O(3^n) | O(n) | Too slow |
| Subset enumeration with min-cost reduction | O(2^n · n) | O(n) | Accepted |

## Algorithm Walkthrough

We first preprocess each problem by converting its three time values into a single effective cost. This cost is the smallest among the valid values, ignoring any `-1` entries. If all three values are `-1`, we mark the problem as unusable.

Next we enumerate all subsets of problems using bitmasks. Each subset represents a candidate set of problems we attempt to solve.

1. For each problem, compute its effective cost as the minimum of its available teammate times. If all are `-1`, we treat it as infinite cost and ensure it can never be selected.
2. Iterate over all masks from `0` to `2^n - 1`. Each mask encodes a subset of problems.
3. For a given mask, compute two values: the number of selected problems and the total time required.
4. While computing the total time, if it ever exceeds 300, we stop early for that subset since it cannot be improved by continuing.
5. If the total time is within 300, we update the answer with the maximum number of problems seen so far.

The early stopping inside each subset is important because it avoids unnecessary summation once feasibility is already broken, keeping the solution efficient even in Python.

### Why it works

For each problem, assigning it to a teammate is independent of all other problems because there is no per-person capacity constraint, only a single global time budget. This removes any coupling between assignment decisions. Therefore, replacing each problem with its minimum feasible assignment cost preserves the feasibility of every subset and never increases the cost of a valid assignment. Any optimal solution must correspond to some subset, and within that subset, choosing the minimum cost assignment for each problem is always optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    cost = []

    for _ in range(n):
        parts = input().split()
        name = parts[0]
        t = list(map(int, parts[1:]))

        best = 10**9
        for x in t:
            if x != -1:
                best = min(best, x)

        cost.append(best)

    ans = 0

    for mask in range(1 << n):
        total = 0
        cnt = 0

        for i in range(n):
            if mask & (1 << i):
                if cost[i] == 10**9:
                    total = 10**9
                    break
                total += cost[i]
                cnt += 1
                if total > 300:
                    break

        if total <= 300:
            ans = max(ans, cnt)

    print(ans)

if __name__ == "__main__":
    solve()
```

The preprocessing step compresses each problem into a single scalar cost, which is essential for reducing the search space. The bitmask loop then explores all subsets directly. The early termination conditions inside the subset loop ensure we do not waste time accumulating costs once infeasibility is certain.

A subtle implementation detail is representing impossible problems with a very large number instead of zero. Using zero would incorrectly allow selecting unsolvable problems for free, artificially inflating the answer. Using a sentinel like `10**9` ensures such subsets automatically exceed the budget.

## Worked Examples

Consider a simplified input with three problems:

```
P1: 50 60 70
P2: -1 40 90
P3: 100 20 80
```

After preprocessing, we get costs:

P1 = 50, P2 = 40, P3 = 20

We now enumerate subsets.

| Mask | Chosen | Total Cost | Count | Valid |
| --- | --- | --- | --- | --- |
| 000 | {} | 0 | 0 | yes |
| 001 | P1 | 50 | 1 | yes |
| 010 | P2 | 40 | 1 | yes |
| 011 | P1,P2 | 90 | 2 | yes |
| 100 | P3 | 20 | 1 | yes |
| 101 | P1,P3 | 70 | 2 | yes |
| 110 | P2,P3 | 60 | 2 | yes |
| 111 | all | 110 | 3 | yes |

The best subset is all three problems with total cost 110, giving answer 3. This trace confirms that the reduction to minimum per-problem cost preserves all meaningful tradeoffs.

Now consider a case with an impossible problem:

```
P1: -1 -1 -1
P2: 200 200 200
```

Costs become:

P1 = impossible, P2 = 200

| Mask | Chosen | Total Cost | Valid |
| --- | --- | --- | --- |
| 01 | P1 | invalid | no |
| 10 | P2 | 200 | yes |
| 11 | P1,P2 | invalid | no |

The best answer is 1, since P1 cannot contribute at all despite being present in the input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^n · n) | Each subset is evaluated by scanning up to n items |
| Space | O(n) | Only stores per-problem costs and a few counters |

With `n ≤ 14`, `2^n` is at most 16384, and multiplying by 14 still yields well under a few hundred thousand operations, which comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    input = sys.stdin.readline
    n = int(input())
    cost = []

    for _ in range(n):
        parts = input().split()
        t = list(map(int, parts[1:]))

        best = 10**9
        for x in t:
            if x != -1:
                best = min(best, x)
        cost.append(best)

    ans = 0
    for mask in range(1 << n):
        total = 0
        cnt = 0
        for i in range(n):
            if mask & (1 << i):
                if cost[i] == 10**9:
                    total = 10**9
                    break
                total += cost[i]
                cnt += 1
                if total > 300:
                    break
        if total <= 300:
            ans = max(ans, cnt)

    print(ans)

# sample
assert run("""3
A -1 20 -1
B 80 90 60
C 40 50 30
""") == "3"

# all impossible
assert run("""2
A -1 -1 -1
B -1 -1 -1
""") == "0"

# tight budget
assert run("""3
A 200 200 200
B 200 200 200
C 200 200 200
""") == "1"

# mix
assert run("""4
A 100 1 100
B 100 100 1
C -1 200 200
D 150 150 150
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all impossible | 0 | handling of unusable problems |
| tight budget | 1 | greedy packing under constraint |
| mixed costs | 3 | subset selection correctness |

## Edge Cases

One edge case is when every problem is impossible for at least one teammate but still feasible through another. For instance, a problem might look like `-1 10 200`. The algorithm correctly takes 10 as the cost and ignores the `-1`, ensuring the problem remains usable.

Another edge case is when a problem is impossible for all teammates. In that case, its cost becomes infinite and any subset containing it is automatically rejected. The enumeration still considers such subsets, but they are filtered out immediately once the sentinel cost is detected.

A final subtle case is when many small-cost problems exist and the optimal solution requires taking almost all of them until the budget is exactly saturated. The bitmask enumeration guarantees these combinations are checked explicitly, and the early stopping only affects pruning of infeasible subsets, not skipping valid combinations.
