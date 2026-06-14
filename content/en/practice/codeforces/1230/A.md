---
title: "CF 1230A - Dawid and Bags of Candies"
description: "We are given four separate bags, each containing some number of candies. Each bag is indivisible and must be given entirely to exactly one of two friends."
date: "2026-06-15T05:04:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1230
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 588 (Div. 2)"
rating: 800
weight: 1230
solve_time_s: 213
verified: true
draft: false
---

[CF 1230A - Dawid and Bags of Candies](https://codeforces.com/problemset/problem/1230/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 3m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four separate bags, each containing some number of candies. Each bag is indivisible and must be given entirely to exactly one of two friends. The task is to determine whether we can assign each of the four bags to either friend such that both friends end up with exactly the same total number of candies.

In other words, we are partitioning a multiset of four integers into two groups, and we want the sums of the two groups to be equal.

The constraints are extremely small: each value is at most 100 and there are only four bags. This immediately rules out any concern about efficiency. Any solution that even tries all assignments or subsets is easily fast enough since the total number of possibilities is fixed at $2^4 = 16$.

Because there are only four items, the main subtlety is not performance but correctness in handling all partitions consistently.

A common mistake is to assume greedy pairing works, such as matching smallest with largest or checking only a few combinations. That fails because the structure is not ordered and optimal partitions can mix extremes in non-obvious ways.

For example, consider:

```
1 2 3 4
```

A greedy attempt might pair (1,4) and (2,3), which works, but if a heuristic instead pairs (1,2) and (3,4), it fails even though a valid partition exists. This shows that partial reasoning about pairs is unreliable unless all partitions are considered.

Another failure case arises when total sum is odd. For instance:

```
1 1 1 2
```

Total is 5, so equal partition is impossible regardless of assignment. Any correct solution must implicitly reject such cases.

## Approaches

The brute-force idea is to try every possible way to assign each of the four bags to either friend. Since each bag has two choices, this leads to $2^4 = 16$ assignments. For each assignment, we compute the sum of candies for friend A and friend B and check whether they match.

This is already optimal for such a tiny input size. The correctness comes from exhaustiveness: every valid partition corresponds to exactly one binary assignment of the four bags.

The only observation that simplifies reasoning is that we do not actually need to enumerate assignments explicitly if we instead think in terms of subsets: choosing a subset of bags for the first friend automatically determines the second.

A slightly more conceptual shortcut is to observe that the total sum must be even, and we are looking for a subset of bags summing to half of the total. With four elements, subset enumeration is trivial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all assignments) | O(2^4) | O(1) | Accepted |
| Subset Check (optimized view) | O(2^4) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of the four bag values. If the sum is odd, immediately conclude that equal splitting is impossible because two equal integers must sum to an even total.
2. Define the target sum as half of the total. This is the amount each friend must receive.
3. Iterate over all subsets of the four bags. Represent each subset using a bitmask from 0 to 15, where each bit indicates whether a bag is assigned to the first friend.
4. For each subset, compute the sum of selected bags. This represents the candies given to the first friend.
5. If this subset sum equals the target, we have implicitly assigned the remaining bags to the second friend, and both sums match. Return YES immediately.
6. If no subset achieves the target sum, return NO.

### Why it works

Every valid distribution corresponds exactly to one subset of bags assigned to the first friend. The remaining bags form the complement subset. Since we test all subsets, we necessarily test every possible partition. The correctness reduces to the fact that equality of totals is equivalent to finding a subset with sum equal to half of the total.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = list(map(int, input().split()))
    total = sum(a)
    
    if total % 2 != 0:
        print("NO")
        return
    
    target = total // 2
    
    # try all subsets of 4 elements
    for mask in range(1 << 4):
        s = 0
        for i in range(4):
            if mask & (1 << i):
                s += a[i]
        if s == target:
            print("YES")
            return
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The code first reads the four values and computes their total. The parity check prevents unnecessary subset enumeration when equality is impossible.

The bitmask loop enumerates all possible assignments of bags to the first friend. The inner loop accumulates the subset sum. The moment a valid subset is found, the function exits early, since existence is sufficient.

A subtle implementation detail is that we do not need to explicitly compute the second friend’s sum. Once the first sum matches half of the total, the complement automatically matches as well.

## Worked Examples

### Example 1

Input:

```
1 7 11 5
```

Total is 24, target is 12.

| mask | subset | subset sum |
| --- | --- | --- |
| 0001 | [1] | 1 |
| 0010 | [7] | 7 |
| 0011 | [1,7] | 8 |
| 0100 | [11] | 11 |
| 0101 | [1,11] | 12 |

At mask 0101, we reach the target sum 12, so the answer is YES.

This confirms that a valid partition exists where the chosen subset and its complement both sum to 12.

### Example 2

Input:

```
1 1 1 2
```

Total is 5, which is odd.

| step | total | parity check | decision |
| --- | --- | --- | --- |
| 1 | 5 | odd | NO |

Since the total cannot be split evenly, we immediately conclude no valid partition exists without enumerating subsets.

This demonstrates that the parity check correctly prunes impossible cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only 16 subsets are checked, each over 4 elements |
| Space | O(1) | No auxiliary structures beyond a few variables |

The constant upper bound makes this solution trivially within limits. Even in a multi-test scenario, the workload remains negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    a = list(map(int, input().split()))
    total = sum(a)
    if total % 2 != 0:
        return "NO"
    target = total // 2
    for mask in range(1 << 4):
        s = 0
        for i in range(4):
            if mask & (1 << i):
                s += a[i]
        if s == target:
            return "YES"
    return "NO"

# provided samples
assert run("1 7 11 5") == "YES"
assert run("1 1 1 2") == "NO"

# custom cases
assert run("2 2 2 2") == "YES", "all equal"
assert run("1 2 3 6") == "YES", "exact partition exists"
assert run("1 2 4 8") == "NO", "no subset sum match"
assert run("100 1 1 98") == "YES", "boundary values"

print("ok")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 2 2 | YES | symmetric distribution |
| 1 2 3 6 | YES | non-trivial subset match |
| 1 2 4 8 | NO | no valid partition |
| 100 1 1 98 | YES | boundary and extreme values |

## Edge Cases

The parity edge case is handled at the very beginning. For an input like:

```
1 1 1 2
```

the algorithm computes total 5 and immediately returns NO. This prevents unnecessary subset enumeration.

For symmetric inputs like:

```
2 2 2 2
```

the algorithm will still work through subsets, but it finds multiple valid masks quickly, such as selecting any two bags summing to 4.

For cases with a single valid split hidden among many invalid ones, such as:

```
100 1 1 98
```

the subset search ensures that even non-intuitive combinations are tested, and the mask selecting {100, 1} is enough to reach 101, matching the target 101.
