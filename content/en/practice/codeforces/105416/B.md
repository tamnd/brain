---
title: "CF 105416B - Hard Boiled"
description: "We are given a collection of eggs, where each egg requires a specific amount of time to be fully cooked. Jacob has a fixed total time budget and a single pot, which means he can only cook one egg at a time without overlap."
date: "2026-06-23T04:41:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105416
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 10-11-24 Div. 2 (Beginner)"
rating: 0
weight: 105416
solve_time_s: 96
verified: false
draft: false
---

[CF 105416B - Hard Boiled](https://codeforces.com/problemset/problem/105416/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of eggs, where each egg requires a specific amount of time to be fully cooked. Jacob has a fixed total time budget and a single pot, which means he can only cook one egg at a time without overlap. Once he starts cooking an egg, he must spend its full cooking time on it before moving to another egg.

The task is to determine how many eggs he can fully cook if he schedules them in the best possible way. The key freedom he has is the order in which he cooks the eggs, and the goal is to maximize the number of completed eggs within the total available time.

The constraint on the number of eggs is up to 100,000, while time values and total time can be as large as 2 billion. This immediately rules out any approach that tries all permutations or simulates all subsets explicitly. Even an $O(n^2)$ approach would be too slow if it involves repeated scanning or selection.

The natural pitfall appears when one assumes that taking eggs in input order is sufficient. For example, if the input is:

```
t = 10
c = [9, 1, 1]
```

Cooking in order yields only 1 egg, since 9 consumes almost all time. But the optimal choice is to take the two small eggs first, giving 2 eggs total. This shows ordering is essential.

Another subtle edge case is when total time exactly matches a combination:

```
t = 6
c = [4, 2, 2]
```

A correct strategy can cook all three, but a naive greedy-by-order approach might fail if the 4 is taken first.

So the real issue is selecting a subset of cooking times whose sum is as large as possible without exceeding $t$, while maximizing the number of chosen elements.

## Approaches

The most direct idea is to try every subset of eggs, compute its total cooking time, and track the largest subset that fits in time. This is correct because it explicitly evaluates all possibilities. However, the number of subsets grows exponentially as $2^n$, and even for $n = 100000$, this is completely infeasible. Even restricting to combinations of size $k$ does not help, since iterating all combinations still explodes.

A more structured observation comes from noticing what actually determines whether a set of eggs is feasible: only the sum of their cooking times matters, not their order. Since each egg contributes positively to total time, the best way to fit as many eggs as possible is to minimize the total cost of each chosen egg set size. That naturally suggests picking the smallest cooking times first.

If we sort the cooking times in non-decreasing order, then taking eggs from smallest upward ensures that for any prefix, we are maximizing the number of eggs for the smallest possible total time. Any deviation from this ordering replaces a smaller or equal cost with a larger one, which can only reduce the number of eggs that fit within the time limit.

Once sorted, we simply accumulate times from left to right until adding another egg would exceed the budget. The prefix length reached at that point is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | $O(2^n)$ | $O(n)$ | Too slow |
| Sort + greedy prefix sum | $O(n \log n)$ | $O(1)$ or $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of eggs $n$ and total available time $t$, then read the list of cooking times. This establishes the resource constraint and individual costs.
2. Sort the cooking times in ascending order. This step ensures that we always consider the cheapest available egg first, which is necessary to maximize how many can fit into the budget.
3. Initialize two variables: a running sum for total cooking time used so far, and a counter for how many eggs have been cooked.
4. Iterate through the sorted list of cooking times from smallest to largest.
5. For each egg, check whether adding its cooking time would exceed the total time $t$. If it does not, include it in the schedule by adding its time to the running sum and incrementing the counter.
6. If adding the current egg would exceed the limit, stop immediately. Any further eggs are even larger or equal, so they cannot be included without violating the constraint.
7. Output the counter as the maximum number of eggs that can be cooked.

The key idea is that we never reconsider earlier decisions because sorting ensures that once a larger egg cannot fit, no later egg can fit either.

### Why it works

The correctness relies on the fact that all egg costs are independent and additive, and we are maximizing cardinality under a single sum constraint. In any optimal solution, if a larger-cost egg is chosen while a smaller-cost unused egg exists, swapping them cannot increase total time and never reduces the number of eggs. Repeated application of this swap argument transforms any optimal solution into one that picks a prefix of the sorted list. That prefix is exactly what the greedy scan constructs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, t = map(int, input().split())
    c = list(map(int, input().split()))
    
    c.sort()
    
    total = 0
    count = 0
    
    for x in c:
        if total + x <= t:
            total += x
            count += 1
        else:
            break
    
    print(count)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the cooking times so that we always process the smallest remaining cost first. This is the structural transformation that makes the greedy approach valid. The loop then accumulates time until the constraint is violated. The early break is important because once we exceed the budget, all subsequent values are at least as large due to sorting.

A common mistake is forgetting to sort, which breaks correctness immediately because the greedy assumption depends entirely on increasing order. Another issue is not stopping early, which is unnecessary for correctness but can degrade performance slightly.

## Worked Examples

### Example 1

Input:

```
n = 3, t = 10
c = [9, 1, 1]
```

After sorting:

```
[1, 1, 9]
```

| Step | Egg | Running Sum | Count | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | take |
| 2 | 1 | 2 | 2 | take |
| 3 | 9 | 2 | 2 | stop |

The third egg cannot be added because it exceeds the remaining budget. The result confirms that prioritizing small values yields the maximum count.

### Example 2

Input:

```
n = 5, t = 10
c = [2, 2, 2, 2, 2]
```

After sorting:

```
[2, 2, 2, 2, 2]
```

| Step | Egg | Running Sum | Count | Action |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 1 | take |
| 2 | 2 | 4 | 2 | take |
| 3 | 2 | 6 | 3 | take |
| 4 | 2 | 8 | 4 | take |
| 5 | 2 | 10 | 5 | take |

All eggs fit exactly, demonstrating that the algorithm correctly handles tight equality cases without prematurely stopping.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, followed by a single linear scan |
| Space | $O(1)$ or $O(n)$ | Depends on in-place sort implementation |

The constraints allow up to 100,000 eggs, so an $O(n \log n)$ sorting approach comfortably fits within time limits, while linear scanning remains trivial in cost.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, t = map(int, input().split())
    c = list(map(int, input().split()))
    c.sort()
    total = 0
    count = 0
    for x in c:
        if total + x <= t:
            total += x
            count += 1
        else:
            break
    return str(count)

# provided samples
assert run("3 10\n9 1 1\n") == "2", "sample 1"
assert run("5 10\n2 2 2 2 2\n") == "5", "sample 2"

# custom cases
assert run("1 5\n10\n") == "0", "cannot cook any egg"
assert run("4 100\n1 2 3 4\n") == "4", "all fit easily"
assert run("4 5\n4 4 4 4\n") == "1", "only one fits"
assert run("6 7\n5 1 1 1 1 1\n") == "4", "prefix selection after sorting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 / 10 | 0 | no feasible selection |
| 4 100 / 1 2 3 4 | 4 | full consumption case |
| 4 5 / 4 4 4 4 | 1 | tight budget boundary |
| 6 7 / 5 1 1 1 1 1 | 4 | greedy prefix correctness |

## Edge Cases

A critical edge case is when no egg can be cooked at all. For input:

```
n = 1, t = 3
c = [10]
```

After sorting, the first element already exceeds the budget. The loop immediately breaks without incrementing the counter, producing 0. This confirms that the algorithm correctly handles complete infeasibility.

Another edge case is when all eggs are identical and exactly fit the budget in multiples. For:

```
n = 3, t = 6
c = [2, 2, 2]
```

Sorting leaves the list unchanged. The algorithm adds each egg sequentially, reaching exactly 6. Since equality is allowed, it includes all three eggs. This demonstrates correct handling of boundary equality conditions where the sum matches the limit exactly without overflow or premature stopping.
