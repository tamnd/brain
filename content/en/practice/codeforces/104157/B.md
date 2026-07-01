---
title: "CF 104157B - Watch Your Sugar!"
description: "We are given a collection of chocolates, each with a known amount of sugar. Thomas has a daily sugar limit and wants to eat as many whole chocolates as possible without the total sugar exceeding that limit."
date: "2026-07-02T01:14:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104157
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 01-27-23 Div. 2 (Beginner)"
rating: 0
weight: 104157
solve_time_s: 44
verified: true
draft: false
---

[CF 104157B - Watch Your Sugar!](https://codeforces.com/problemset/problem/104157/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of chocolates, each with a known amount of sugar. Thomas has a daily sugar limit and wants to eat as many whole chocolates as possible without the total sugar exceeding that limit. Each chocolate is either fully eaten or not eaten at all, and the goal is to maximize the count of selected chocolates under a total sum constraint.

The input consists of a list of integers representing sugar amounts per chocolate and a single integer representing the maximum allowed total sugar. The output is a single number: the largest number of chocolates whose combined sugar does not exceed the limit.

The constraints are small: at most 100 chocolates and sugar values up to 10,000 total limit. This immediately suggests that even quadratic behavior would be acceptable, since 100² operations is trivial. Anything exponential is unnecessary but still technically feasible at this scale.

The key edge case is when all chocolates exceed the limit individually. For example, if `s = 3` and chocolates are `[5, 6, 7]`, then the correct answer is `0`. A greedy or sorting-based approach must correctly handle the fact that no partial selection is allowed and skipping all items is valid.

Another edge case is when all chocolates are very small and can all be taken. For example, `s = 100` and all values are `1`, where the answer should be `n`.

A subtle failure case arises if someone tries to take chocolates in input order without considering their sizes. For instance, `s = 10` and `[6, 6, 1, 1, 1]`. Taking in order yields `6 + 6` immediately exceeds the limit after the first two picks, producing a suboptimal count, while a better strategy would be to take smaller chocolates first.

## Approaches

The brute-force approach is to try all subsets of chocolates, compute their total sugar, and track the maximum size of any subset whose sum is within the limit. This is correct because it directly explores every possible selection. However, the number of subsets is `2^n`, which for `n = 100` is astronomically large, on the order of `10^30`, which makes it completely infeasible.

The structure of the problem reveals a simpler strategy. Since we only care about maximizing the number of items under a sum constraint, we should prefer smaller items first. Intuitively, each chocolate has equal "value" in terms of contribution to the count, so minimizing cost per item is optimal. Sorting the chocolates by sugar content and then greedily taking the smallest ones ensures that we pack as many items as possible before hitting the limit.

This converts the problem into a simple greedy accumulation over a sorted array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (subset enumeration) | O(2^n · n) | O(n) | Too slow |
| Sort + Greedy | O(n log n) | O(1) extra (excluding sort) | Accepted |

## Algorithm Walkthrough

1. Read the number of chocolates `n`, the sugar limit `s`, and the list of sugar values. Sorting is necessary because order determines how efficiently we can pack small items first.
2. Sort the list in non-decreasing order. This ensures that every prefix of the list represents the cheapest possible way to take that many chocolates.
3. Initialize a running sum `total = 0` and a counter `count = 0`.
4. Iterate through the sorted chocolates from smallest to largest.
5. For each chocolate, check whether adding its sugar to `total` would exceed `s`. If not, include it by updating `total += value` and incrementing `count += 1`.
6. If adding the current chocolate would exceed the limit, stop immediately. Any later chocolates are equal or larger, so none can be added without violating the constraint.
7. Output `count`.

### Why it works

The correctness relies on the fact that replacing any chosen chocolate with a smaller one can only improve feasibility without reducing the count. Since all chocolates contribute equally to the objective (one per chocolate), the optimal strategy always prefers lower-cost items. Sorting ensures that at every step, we are making the locally optimal choice that preserves the maximum possible remaining capacity for future picks. This creates a monotonic process where the number of selected items is maximized greedily without backtracking.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
s = int(input().strip())
a = list(map(int, input().split()))

a.sort()

total = 0
count = 0

for x in a:
    if total + x <= s:
        total += x
        count += 1
    else:
        break

print(count)
```

The solution begins by sorting the array, which is the only non-trivial step. This guarantees that we always consider smaller chocolates first, which is essential for maximizing the number of items. The loop maintains a running sum and ensures we never exceed the limit. The early break is important because once we fail at a given chocolate, all later ones are guaranteed to be too large as well.

A common mistake is forgetting to sort, which leads to incorrect greedy behavior based on input order. Another subtle issue is not breaking early, which is not incorrect but slightly less efficient.

## Worked Examples

### Example 1

Input:

```
n = 5, s = 10
chocolates = [2, 3, 5, 4, 1]
```

Sorted array is `[1, 2, 3, 4, 5]`.

| Step | Chocolate | Running Total | Count |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 3 | 2 |
| 3 | 3 | 6 | 3 |
| 4 | 4 | 10 | 4 |
| 5 | 5 | stop | 4 |

The algorithm selects four chocolates before reaching the limit exactly. This shows that greedy packing achieves a tight fit when possible.

### Example 2

Input:

```
n = 4, s = 6
chocolates = [4, 2, 3, 5]
```

Sorted array is `[2, 3, 4, 5]`.

| Step | Chocolate | Running Total | Count |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 1 |
| 2 | 3 | 5 | 2 |
| 3 | 4 | stop | 2 |

Here the algorithm correctly avoids larger chocolates that would exceed the limit. The optimal answer is 2, achieved by selecting 2 and 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, iteration is linear |
| Space | O(1) extra | Only counters are used beyond input storage |

The constraints allow up to 100 items, so sorting and a single pass are trivial under the time limit. Even a less optimal implementation would pass, but this solution is clean and scalable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    s = int(input().strip())
    a = list(map(int, input().split()))
    a.sort()

    total = 0
    count = 0

    for x in a:
        if total + x <= s:
            total += x
            count += 1
        else:
            break

    return str(count).strip()

# provided samples (conceptual, since not explicitly given)
assert run("5\n10\n2 3 5 4 1\n") == "4"
assert run("4\n6\n4 2 3 5\n") == "2"

# custom cases
assert run("1\n0\n5\n") == "0", "cannot take anything"
assert run("3\n100\n1 1 1\n") == "3", "all fit"
assert run("3\n3\n4 5 6\n") == "0", "all too large"
assert run("5\n7\n6 1 1 1 1\n") == "4", "greedy after sorting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1, 0, 5` | 0 | zero budget edge case |
| `3, 100, all 1s` | 3 | all items included |
| `3, 3, large values` | 0 | no valid picks |
| `5, 7, mixed values` | 4 | sorting necessity and greedy correctness |

## Edge Cases

For the case where no chocolate can be taken, such as `s = 3` and `[5, 6, 7]`, sorting gives the same array. The algorithm checks `5` first and immediately stops since `0 + 5 > 3`. The output remains `0`, which is correct because no subset is feasible.

For the case where all chocolates fit exactly or with slack, such as `s = 10` and `[1, 2, 3, 4]`, sorting produces `[1, 2, 3, 4]`. The algorithm accumulates `1 → 3 → 6 → 10`, successfully taking all items. The stopping condition never triggers early, showing that the algorithm does not prematurely terminate when the full set is valid.
