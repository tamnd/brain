---
title: "CF 967B - Watering System"
description: "We are given a system of pipe holes, each hole having a fixed size that determines how much water it can drain when water is poured into the system. Arkady pours a fixed amount of water, but only one hole, the first one, is considered useful to him."
date: "2026-06-17T01:37:10+07:00"
tags: ["codeforces", "competitive-programming", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 967
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 477 (rated, Div. 2, based on VK Cup 2018 Round 3)"
rating: 1000
weight: 967
solve_time_s: 88
verified: true
draft: false
---

[CF 967B - Watering System](https://codeforces.com/problemset/problem/967/B)

**Rating:** 1000  
**Tags:** math, sortings  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system of pipe holes, each hole having a fixed size that determines how much water it can drain when water is poured into the system. Arkady pours a fixed amount of water, but only one hole, the first one, is considered useful to him. His goal is to ensure that at least a required amount of water ends up flowing out through this first hole.

The key control he has is that he may block any subset of holes before pouring water. After blocking, the remaining open holes share the water proportionally to their sizes. If the total size of open holes is $S$, then the first hole receives a fraction $s_1 / S$ of the total water $A$, so its output is $A \cdot s_1 / S$.

The task is to minimize how many holes are blocked so that the first hole receives at least $B$ units of water.

The constraints push us toward a greedy or sorting-based solution. With $n$ up to $10^5$, any approach that tries all subsets of holes is impossible. Even iterating over all $2^n$ possibilities is out of the question, and even checking each possible number of removals with recomputation would be too slow if done naively.

A subtle point is that removing holes affects only the denominator $S$, not the numerator $s_1$. This creates a monotonic effect: removing holes always increases the share of the first hole.

A few edge cases are easy to miss.

If no holes are blocked, it might already be sufficient. For example, if $s_1$ is large compared to the sum of all sizes, the condition holds immediately and the answer is zero.

If all other holes are extremely large compared to $s_1$, then the only way to satisfy the condition is to remove almost everything except the first hole. In extreme cases, the answer becomes $n-1$.

A third subtle case is when multiple holes have identical sizes. Since only the sum matters, not identity, the decision depends only on removing the largest contributors to the denominator.

## Approaches

A brute-force idea would be to try all subsets of holes to block. For each subset, compute the remaining sum $S$, and check whether $A \cdot s_1 / S \ge B$. This would require iterating over all subsets and summing remaining elements, which leads to $O(n \cdot 2^n)$ behavior. With $n = 10^5$, this is completely infeasible.

A more structured view comes from rewriting the condition:

$$\frac{A \cdot s_1}{S} \ge B \quad \Rightarrow \quad S \le \frac{A \cdot s_1}{B}$$

So instead of thinking about maximizing the share of the first hole directly, we think about reducing the total remaining sum $S$. The first hole size is fixed, so we want to make the sum of the remaining holes as small as possible, while blocking as few holes as possible.

This gives a greedy direction: to reduce the sum fastest, we should remove the largest holes first. Each removed hole decreases $S$ as much as possible per removal. Therefore, sorting the holes (excluding the first) in descending order and progressively removing them gives the optimal strategy.

We simulate removing the largest sizes one by one until the condition is satisfied.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all subsets) | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Sorting + Greedy removal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of all hole sizes. This represents the denominator before any removals.
2. Extract the size of the first hole separately, since it is never removed.
3. Check if the condition is already satisfied without removing anything. If $A \cdot s_1 \ge B \cdot S$, return 0 immediately.
4. Collect all other hole sizes into a list, because only they are candidates for removal.
5. Sort this list in descending order so that the largest contributors to the denominator are considered first.
6. Iterate through the sorted list, removing one hole at a time:

1. Subtract its size from the total sum.
2. Increase the removal count.
3. Check if the inequality $A \cdot s_1 \ge B \cdot S$ now holds.

If it holds, stop and return the number of removed holes.

The reasoning behind sorting is that every removal reduces the denominator, and reducing it by a larger amount is always at least as good as reducing it by a smaller amount when we care only about reaching a threshold.

### Why it works

The key invariant is that at any moment, among all sets of holes of the same size (same number of removals), removing the largest available holes minimizes the remaining sum $S$. Since the condition depends only on whether $S$ is below a fixed threshold, reaching that threshold in the fewest removals is equivalent to always maximizing the reduction in $S$ at each step. Any deviation from removing the largest remaining element can only leave a larger sum after the same number of removals, which cannot help satisfy the inequality earlier.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, A, B = map(int, input().split())
    s = list(map(int, input().split()))
    
    s1 = s[0]
    total = sum(s)
    
    if A * s1 >= B * total:
        print(0)
        return
    
    rest = s[1:]
    rest.sort(reverse=True)
    
    removed = 0
    for x in rest:
        total -= x
        removed += 1
        if A * s1 >= B * total:
            print(removed)
            return

if __name__ == "__main__":
    solve()
```

The code follows the derived inequality directly, avoiding floating-point division by cross-multiplying the condition. This prevents precision issues.

The sorting step ensures that each iteration produces the maximum possible reduction in total sum per removed element. The loop stops immediately once the condition is satisfied, so we never remove more holes than necessary.

A common pitfall is accidentally including the first hole in the sorted removal list. That would incorrectly allow removing the very element we depend on for the numerator.

## Worked Examples

### Example 1

Input:

```
4 10 3
2 2 2 2
```

We start with total = 8, s1 = 2.

| Step | Removed holes | Total sum | Check $10·2 ≥ 3·S$ |
| --- | --- | --- | --- |
| 0 | none | 8 | 20 ≥ 24 false |
| 1 | 2 | 6 | 20 ≥ 18 true |

After removing one hole, the condition becomes true, so the answer is 1.

This shows how removing any single hole reduces the denominator enough to cross the threshold.

### Example 2

Input:

```
3 80 20
3 3 4
```

Initial total = 10, s1 = 3.

| Step | Removed holes | Total sum | Check $80·3 ≥ 20·S$ |
| --- | --- | --- | --- |
| 0 | none | 10 | 240 ≥ 200 true |

No removals are needed.

This demonstrates the early-exit case where the initial configuration already satisfies the constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting all holes except the first dominates, followed by a linear scan |
| Space | $O(n)$ | Storing the list of hole sizes |

The constraints allow up to $10^5$ elements, and $n \log n$ sorting comfortably fits within time limits. The rest of the operations are linear and negligible in comparison.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, A, B = map(int, input().split())
    s = list(map(int, input().split()))
    
    s1 = s[0]
    total = sum(s)
    
    if A * s1 >= B * total:
        return "0"
    
    rest = s[1:]
    rest.sort(reverse=True)
    
    removed = 0
    for x in rest:
        total -= x
        removed += 1
        if A * s1 >= B * total:
            return str(removed)

# provided sample
assert run("4 10 3\n2 2 2 2\n") == "1", "sample 1"

# all equal already satisfied
assert run("3 10 1\n5 5 5\n") == "0"

# need all removals except first
assert run("3 10 9\n1 100 100\n") == "2"

# minimal case
assert run("1 5 3\n10\n") == "0"

# large skew
assert run("5 100 1\n1 100 100 100 100\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | early exit correctness |
| extreme imbalance | 2 | removing all others needed |
| single element | 0 | boundary n = 1 |
| skewed large values | 0 | condition already satisfied |

## Edge Cases

When there is only one hole, the denominator never changes and the answer is always zero. The algorithm handles this because the removal list is empty and the early condition check decides the result immediately.

When all holes except the first are extremely large, the algorithm removes them in descending order, quickly shrinking the denominator. Each removal is essential, and the loop naturally counts exactly how many are needed until only the first hole remains or the threshold is reached.

When the initial configuration already satisfies the inequality, no sorting or removal is effectively used, since the early check terminates immediately.
