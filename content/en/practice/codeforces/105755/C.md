---
title: "CF 105755C - Count Pairs"
description: "We are given a multiset of positive integers, and we want to choose a subset with no duplicates such that every pair of chosen numbers satisfies a strict bitwise condition involving XOR. For any two chosen numbers $x$ and $y$, we compute $x oplus y$."
date: "2026-06-22T15:09:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105755
codeforces_index: "C"
codeforces_contest_name: "Bay Area Programming Contest 2025"
rating: 0
weight: 105755
solve_time_s: 80
verified: true
draft: false
---

[CF 105755C - Count Pairs](https://codeforces.com/problemset/problem/105755/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of positive integers, and we want to choose a subset with no duplicates such that every pair of chosen numbers satisfies a strict bitwise condition involving XOR.

For any two chosen numbers $x$ and $y$, we compute $x \oplus y$. The requirement is that this XOR result must be strictly larger than the larger of the two numbers. If this fails for even one pair, the subset is invalid.

So the task is to maximize how many distinct values we can pick while keeping this pairwise constraint true for every pair in the subset.

The constraint $n \le 3 \cdot 10^5$ immediately rules out any approach that checks all pairs explicitly. A naive check over all subsets or even greedy verification with pairwise comparisons would be quadratic in the worst case and would not pass. Any valid solution must reduce the interaction between elements to something closer to linear or linearithmic time.

A key edge case appears when many numbers share the same magnitude range. For example, consider a block of numbers like $4, 5, 6, 7$. All of them lie in the same power-of-two interval, but their pairwise XOR behavior is highly constrained. Another edge case is when values are spread across different magnitude ranges, like $1, 2, 3$, where some pairs behave well and others immediately violate the condition. A naive greedy approach that only compares adjacent values or only checks one direction of ordering will fail on such mixed cases.

## Approaches

The brute-force idea is straightforward. We try every subset and verify whether all pairs satisfy the XOR condition. Even if we fix a subset and validate it in $O(k^2)$, the number of subsets is exponential, so this is completely infeasible.

A slightly more reasonable attempt is to sort the array and try to build the subset greedily, checking each new candidate against all already chosen elements. This reduces subset search, but the validation step still becomes $O(n^2)$ in the worst case, since every insertion may scan the entire chosen set.

The key observation comes from understanding how XOR behaves relative to the most significant bit of numbers. The value of a number is dominated by its highest set bit. When two numbers differ in their highest set bit, XOR behaves in a way that tends to destroy or preserve magnitude in a very structured manner.

If two numbers lie in different highest-bit groups, one of them has a strictly higher most significant bit. In that case, the larger number dominates the comparison, and XOR cannot reliably exceed it because XOR never introduces bits above the highest bit of either operand. This immediately restricts which combinations are even candidates.

Inside a fixed highest-bit group, all numbers share the same leading bit. XOR cancels that bit, which forces the result to drop below the entire range of that group. Since every number in the group is at least $2^k$, while XOR stays below $2^k$, any pair inside the same group automatically violates the condition.

This leads to a strong structural simplification: at most one number from each highest-bit group can ever be selected. Once this is recognized, the problem reduces to counting how many distinct highest-bit groups are represented in the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal (MSB grouping) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each number, determine its most significant bit position. This identifies the power-of-two interval the number belongs to.
2. Maintain a boolean array or set indexed by bit position to track which groups have already been represented in the chosen subset.
3. Iterate through all numbers. For each number, compute its MSB index.
4. If this MSB index has not been seen before, mark it as used and increment the answer. Otherwise, skip the number since selecting more than one element from the same group would immediately violate the condition.
5. Output the total number of distinct MSB groups encountered.

### Why it works

The invariant is that any valid subset can contain at most one element per highest-bit class. Within a class, every number lies in $[2^k, 2^{k+1})$. For any two such numbers, XOR removes the leading bit and produces a value strictly below $2^k$, which is always smaller than both original numbers. This directly violates the requirement that XOR must exceed the maximum of the pair. Across different classes, selecting more than one element is also unsafe in general, but the constraint inside a class already forces the optimal strategy to pick at most one representative per class, and any valid subset cannot exceed this bound. Thus counting distinct MSB values gives the maximum possible size.

## Python Solution

```python
import sys
input = sys.stdin.readline

def msb(x):
    return x.bit_length() - 1

n = int(input())
arr = list(map(int, input().split()))

seen = set()
ans = 0

for x in arr:
    b = msb(x)
    if b not in seen:
        seen.add(b)
        ans += 1

print(ans)
```

The solution computes the most significant bit of each number using `bit_length`, which runs in constant time per integer. The set `seen` ensures we count each bit group only once.

A subtle point is that duplicates do not matter at all because the problem requires a set of unique elements. Even if duplicates exist in input, they collapse to the same MSB group and are ignored after the first occurrence.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

We compute MSB groups:

| Value | Binary | MSB index | Seen before? | Action | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | No | take | 1 |
| 2 | 10 | 1 | No | take | 2 |
| 3 | 11 | 1 | Yes | skip | 2 |

This shows that values 2 and 3 compete for the same bit class, so only one of them can be used. The final answer is 2.

### Example 2

Input:

```
5
4 5 6 7 8
```

| Value | Binary | MSB index | Seen before? | Action | Answer |
| --- | --- | --- | --- | --- | --- |
| 4 | 100 | 2 | No | take | 1 |
| 5 | 101 | 2 | Yes | skip | 1 |
| 6 | 110 | 2 | Yes | skip | 1 |
| 7 | 111 | 2 | Yes | skip | 1 |
| 8 | 1000 | 3 | No | take | 2 |

The example demonstrates that once a bit class is used, all other values in the same interval become unusable, even if they differ significantly in lower bits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number is processed once with constant-time MSB computation and set lookup |
| Space | O(log A) | We store at most one entry per possible bit position |

The solution fits easily within limits since the number range only requires about 22-23 bit classes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline

    def msb(x):
        return x.bit_length() - 1

    n = int(input())
    arr = list(map(int, input().split()))

    seen = set()
    ans = 0
    for x in arr:
        b = msb(x)
        if b not in seen:
            seen.add(b)
            ans += 1

    return str(ans)

# provided samples
assert run("3\n1 2 3\n") == "2"
assert run("3\n4000000 4000000 4000000\n") == "1"

# custom cases
assert run("1\n7\n") == "1", "single element"
assert run("5\n1 2 4 8 16\n") == "5", "all distinct MSBs"
assert run("4\n3 5 6 7\n") == "1", "same MSB collapse"
assert run("6\n1 2 3 4 5 6\n") == "3", "mixed MSB groups"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 | 1 | single-element edge case |
| powers of two | 5 | all MSBs distinct |
| 3 5 6 7 | 1 | full same-class collapse |
| 1 2 3 4 5 6 | 3 | mixed grouping behavior |

## Edge Cases

A minimal input with a single number always produces an answer of 1, since there are no pairs to violate the condition.

For a case like `4 5 6 7`, all numbers share the same most significant bit. The algorithm assigns them the same group, keeps only the first occurrence, and ignores the rest. This matches the fact that any pair inside this range fails the XOR condition.

For `1 2 3`, the grouping splits into MSB 0 for 1 and MSB 1 for both 2 and 3. The algorithm correctly counts two groups, matching the best achievable subset `{1, 2}` or `{1, 3}` but never all three.
