---
title: "CF 105544H - Bank Deposit Challenge"
description: "We are given a fixed amount of cash and a list of bank deposit opportunities. Each opportunity requires spending a specific amount of money to participate, and in return it yields a fixed amount of interest."
date: "2026-06-22T23:33:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105544
codeforces_index: "H"
codeforces_contest_name: "The 2023 ICPC Asia Taoyuan Regional Programming Contest"
rating: 0
weight: 105544
solve_time_s: 49
verified: true
draft: false
---

[CF 105544H - Bank Deposit Challenge](https://codeforces.com/problemset/problem/105544/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed amount of cash and a list of bank deposit opportunities. Each opportunity requires spending a specific amount of money to participate, and in return it yields a fixed amount of interest. The constraint is that each deposit option can be chosen at most once, and the total money spent across chosen options cannot exceed the available cash. The goal is to select a subset of these deposit options that maximizes the total interest gained.

This is structurally a knapsack problem where each item has a cost and a value, and we want to maximize value under a capacity constraint. The “cost” is the required deposit amount and the “value” is the interest earned.

The constraints are small enough that a quadratic dynamic programming solution is feasible. The number of banks is at most 100, and the cash limit is at most 1000. A straightforward brute-force subset enumeration would consider all $2^N$ subsets, which grows to about $10^{30}$ in the worst case and is completely infeasible. This immediately suggests a dynamic programming approach over the budget dimension.

A subtle edge case occurs when all deposit requirements exceed the available cash. For example, if cash is 10 and all $w_i > 10$, then no selection is possible and the answer must be 0. A naive implementation that initializes DP incorrectly (for example, without properly setting unreachable states) could accidentally propagate invalid values and produce a non-zero answer. Another case is when multiple combinations yield the same cost but different value; the algorithm must ensure it always keeps the maximum value.

## Approaches

The brute-force idea is to try every subset of bank offers. For each subset, we compute total cost and total interest, and keep the best valid one. This works because it directly evaluates all possibilities, but it becomes impossible as soon as $N$ exceeds around 25 due to exponential growth.

The structure of the problem reveals a classic 0/1 knapsack pattern. Each bank offer is an item, the deposit limit is its weight, and the interest is its value. The capacity is the available cash $C$. Instead of tracking subsets explicitly, we can build a dynamic programming array where $dp[c]$ represents the maximum interest achievable using exactly or at most $c$ cash.

The key improvement comes from recognizing that each item is used at most once. This allows us to iterate capacities in descending order for each item, ensuring we do not reuse the same item multiple times. This reduces the complexity from exponential to polynomial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^N \cdot N)$ | $O(N)$ | Too slow |
| 0/1 Knapsack DP | $O(NC)$ | $O(C)$ | Accepted |

## Algorithm Walkthrough

We treat each bank offer as an item with a cost and a value, and we build up the best achievable interest for every possible budget up to $C$.

1. Initialize a DP array of size $C + 1$, where every entry starts at 0. This represents that with zero items, no interest can be earned regardless of budget.
2. Process each bank offer one by one. For a bank $i$, let its cost be $w_i$ and its value be $v_i$.
3. For this bank, iterate the budget backwards from $C$ down to $w_i$. The backward direction ensures that we do not reuse the same bank multiple times within this iteration.
4. For each budget $c$, consider whether taking this bank improves the result: we compare the current value $dp[c]$ with $dp[c - w_i] + v_i$. We update $dp[c]$ if the latter is larger.
5. After processing all banks, the answer is the maximum value in the DP array, which represents the best achievable interest without exceeding the budget.

### Why it works

At any point during processing, the DP array encodes the best possible interest achievable using only the banks processed so far. The backward iteration guarantees that when we update $dp[c]$, the value $dp[c - w_i]$ still refers to a state that does not include the current bank, preserving the 0/1 constraint. This invariant ensures that every valid subset of banks is considered exactly once, and no invalid reuse occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    C = int(input().strip())
    v = list(map(int, input().split()))
    w = list(map(int, input().split()))
    n = len(v)

    dp = [0] * (C + 1)

    for i in range(n):
        cost = w[i]
        val = v[i]
        for c in range(C, cost - 1, -1):
            dp[c] = max(dp[c], dp[c - cost] + val)

    print(max(dp))

if __name__ == "__main__":
    solve()
```

The solution uses a one-dimensional DP array to compress memory. Each iteration updates the array in place, but only in decreasing order of capacity so that previous states remain valid for transition. The final answer is taken as the maximum over all capacities since we are allowed to spend any amount up to $C$, not necessarily exactly $C$.

## Worked Examples

### Example 1

Input:

```
C = 10
v = [5, 15, 7]
w = [20, 30, 50]
```

All costs exceed the capacity, so no item can be chosen.

| Step | Item | dp state (compressed) | Explanation |
| --- | --- | --- | --- |
| Init | - | all zeros | no choices available |
| After all | all items | all zeros | no valid updates |

Output is 0.

This confirms that the algorithm correctly handles the case where no item fits.

### Example 2

Input:

```
C = 72
v = [2, 10, 12, 10, 10, 17, 13, 15]
w = [120, 10, 5, 20, 25, 100, 80, 300]
```

We only consider items with cost ≤ 72.

| Item | cost | value | dp[72] after processing |
| --- | --- | --- | --- |
| 1 | 120 | 2 | 0 |
| 2 | 10 | 10 | 10 |
| 3 | 5 | 12 | 22 |
| 4 | 20 | 10 | 32 |
| 5 | 25 | 10 | 42 |
| 6 | 100 | 17 | 42 |
| 7 | 80 | 13 | 42 |
| 8 | 300 | 15 | 42 |

The final result is 42.

This trace shows how the DP gradually accumulates optimal combinations under the budget constraint while ignoring oversized items.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(NC)$ | each of N items updates up to C states |
| Space | $O(C)$ | single DP array of size C+1 |

With $N \le 100$ and $C \le 1000$, the algorithm performs at most $10^5$ transitions, which easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    C = int(input().strip())
    v = list(map(int, input().split()))
    w = list(map(int, input().split()))
    n = len(v)

    dp = [0] * (C + 1)
    for i in range(n):
        for c in range(C, w[i] - 1, -1):
            dp[c] = max(dp[c], dp[c - w[i]] + v[i])

    return str(max(dp))

# provided samples (approximated formatting)
assert run("10\n5 15 7\n20 30 50\n") == "0"
assert run("72\n2 10 12 10 10 17 13 15\n120 10 5 20 25 100 80 300\n") == "42"

# custom cases
assert run("1\n5\n1\n") == "0", "no item fits"
assert run("5\n10\n5\n") == "10", "exact fit single item"
assert run("10\n1 2 3\n2 3 4\n") == "6", "all items fit"
assert run("10\n5 6\n5 5\n") == "11", "choose best combination"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no item fits | 0 | unreachable states |
| exact fit | 10 | boundary equality |
| all items fit | 6 | full accumulation |
| mixed choice | 11 | optimal subset selection |

## Edge Cases

When every item has cost larger than the budget, the DP array should remain unchanged at zero. For instance, with $C = 3$, $w = [5, 6]$, no transitions are possible because the inner loop never executes. The final answer correctly becomes 0.

When an item exactly matches the budget, such as $C = 10$, $w = [10]$, the DP update sets $dp[10] = v_1$, since $dp[0]$ is 0 and the transition is valid. This confirms that equality boundaries are handled correctly.

When multiple items have overlapping costs, such as $C = 10$, $w = [5, 5]$, the backward iteration ensures that after processing the first item, the second item can still combine with the first without violating the single-use constraint, yielding the correct combined value.
