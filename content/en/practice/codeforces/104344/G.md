---
title: "CF 104344G - Presentes de P\u00e1scoa"
description: "Fred has a list of chocolate eggs, each with a known price in cents, and a fixed amount of money. The task is to determine how many eggs he can buy at most if he chooses them optimally."
date: "2026-07-01T18:29:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104344
codeforces_index: "G"
codeforces_contest_name: "Maratona dos Bixes 2023 - UNICAMP"
rating: 0
weight: 104344
solve_time_s: 64
verified: true
draft: false
---

[CF 104344G - Presentes de P\u00e1scoa](https://codeforces.com/problemset/problem/104344/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

Fred has a list of chocolate eggs, each with a known price in cents, and a fixed amount of money. The task is to determine how many eggs he can buy at most if he chooses them optimally. Each egg can be bought at most once, and he is free to choose any subset of the available eggs.

The input gives the number of available eggs, the amount of money, and a list of prices. The output is a single integer representing the maximum number of items whose total cost does not exceed the budget.

The key constraint is that the number of eggs can be as large as 100000. Any solution that tries to consider all subsets or even all combinations is immediately infeasible. A quadratic approach would require around 10^10 operations in the worst case, which is far beyond the time limit.

The only non-trivial edge case arises when prices vary widely. For example, if all items are expensive except one cheap item, a naive strategy that does not prioritize small values could waste the budget early. Another failure mode appears when the list is unsorted and a greedy approach assumes order matters without explicitly sorting.

A simple example where ordering matters:

Input:

```
3
5
5 4 1
```

The correct answer is `1`, because buying the item costing 1 is optimal. A careless approach that picks the first affordable prefix without sorting might incorrectly behave unpredictably depending on input order.

Another edge case:

Input:

```
4
10
8 7 6 5
```

Correct output is `1`. Any strategy that tries combinations without ordering will fail to maximize count efficiently.

## Approaches

A brute-force interpretation is to try all subsets of eggs, compute their total cost, and track the largest subset whose sum does not exceed the budget. This is correct because it explicitly evaluates every possible selection, but it grows exponentially as 2^N subsets, and even checking each subset costs O(N), leading to O(N·2^N) time. With N up to 100000, this is impossible.

A better observation comes from reframing the objective. We are not trying to maximize value or minimize cost; we are maximizing the number of items, which suggests that each item contributes equally to the objective. Since every item gives +1 to the answer regardless of its price, the optimal strategy is to buy the cheapest items first.

Once we sort the prices in increasing order, we can greedily take items one by one until the budget runs out. This works because any solution that includes a more expensive item while excluding a cheaper one can be improved by swapping them, reducing or preserving total cost while not decreasing the count.

This reduces the problem to sorting plus a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N·2^N) | O(N) | Too slow |
| Sort + Greedy | O(N log N) | O(1) or O(N) | Accepted |

## Algorithm Walkthrough

1. Read N, the number of eggs, and C, the available budget.
2. Read the list of prices.
3. Sort the list in non-decreasing order so that cheaper items come first.

Sorting is necessary because local decisions depend on global ordering of costs.
4. Initialize a counter for purchased items and a running sum of spent money.
5. Iterate through the sorted prices.
6. For each price, check whether adding it to the current spent amount stays within the budget.

If it does, include it and update the spent amount and counter.

If it does not, stop immediately since all remaining items are at least as expensive.
7. Output the counter.

Why it works:

At any point in the process, we have chosen the cheapest possible subset of a given size. If there existed a better solution with more items, it would necessarily replace some chosen expensive item with a cheaper unused one, which contradicts the fact that we always process items in increasing order. The greedy choice maintains the invariant that after k steps, we have the minimum possible cost among all subsets of size k.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    c = int(input())
    p = list(map(int, input().split()))
    
    p.sort()
    
    used = 0
    total = 0
    
    for price in p:
        if total + price <= c:
            total += price
            used += 1
        else:
            break
    
    print(used)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the prices so that we always consider cheaper eggs first. The variable `total` tracks the money spent so far, and `used` counts how many eggs have been selected. The loop maintains the invariant that we always take the next cheapest feasible item. The early stopping condition is safe because once a price exceeds the remaining budget, all subsequent prices are at least as large.

A subtle detail is the use of a strict budget check `total + price <= c`. This ensures we never exceed the limit even on boundary cases where the remaining budget exactly matches a price.

## Worked Examples

### Sample 1

Input:

```
4
15
1 2 3 5
```

Sorted prices remain `[1, 2, 3, 5]`.

| Step | Price | Total Before | Take? | Total After | Count |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | yes | 1 | 1 |
| 2 | 2 | 1 | yes | 3 | 2 |
| 3 | 3 | 3 | yes | 6 | 3 |
| 4 | 5 | 6 | yes | 11 | 4 |

All items fit within budget 15, so the answer is 4.

This confirms that when the total sum of all items is within budget, the algorithm correctly consumes everything.

### Sample 2

Input:

```
5
10
1 9 4 6 3
```

Sorted prices: `[1, 3, 4, 6, 9]`

| Step | Price | Total Before | Take? | Total After | Count |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | yes | 1 | 1 |
| 2 | 3 | 1 | yes | 4 | 2 |
| 3 | 4 | 4 | yes | 8 | 3 |
| 4 | 6 | 8 | no | 8 | 3 |

We stop when the next item cannot be included. This shows that greedily taking smallest items maximizes count before budget exhaustion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates; single linear pass afterward |
| Space | O(1) extra (or O(N) depending on sort implementation) | Only counters are used beyond input storage |

The constraints allow up to 100000 items, and O(N log N) sorting is well within limits. The linear scan is negligible in comparison, so the solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(input())
    c = int(input())
    p = list(map(int, input().split()))
    
    p.sort()
    
    used = 0
    total = 0
    
    for price in p:
        if total + price <= c:
            total += price
            used += 1
        else:
            break
    
    return str(used).strip()

# provided samples
assert run("4\n15\n1 2 3 5\n") == "4", "sample 1"
assert run("5\n10\n1 9 4 6 3\n") == "3", "sample 2"

# custom cases
assert run("1\n5\n10\n") == "0", "cannot buy anything"
assert run("3\n10\n5 5 5\n") == "2", "boundary exact fit"
assert run("6\n21\n4 4 4 4 4 4\n") == "5", "repeated small values"
assert run("5\n100\n1 2 3 4 5\n") == "5", "all fit easily"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 item too expensive | 0 | handles zero purchases |
| repeated equal values | 2 | exact budget boundary correctness |
| many small equal values | 5 | greedy accumulation stability |
| all items fit | 5 | full consumption case |

## Edge Cases

One edge case occurs when all items are more expensive than the budget. After sorting, the first item already violates the constraint, so the loop terminates immediately and the output remains zero. For example:

Input:

```
3
2
5 6 7
```

After sorting `[5, 6, 7]`, the first comparison fails and no updates happen, producing output `0`.

Another case is when multiple items have identical prices equal to the remaining budget at different stages. The condition `total + price <= c` ensures that equality is accepted correctly. For example:

Input:

```
4
10
2 2 2 4
```

Execution:

First three 2s are taken, reaching total 6, then 4 is taken to reach exactly 10. The algorithm correctly allows equality at each step, ensuring maximal count is achieved.
