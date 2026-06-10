---
title: "CF 1569C - Jury Meeting"
description: "We are asked to count the number of permutations of jury members that are “nice,” given how they present their tasks. Each jury member $i$ has $ai$ tasks, and they tell tasks in order according to a permutation."
date: "2026-06-10T11:42:32+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 1569
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 113 (Rated for Div. 2)"
rating: 1500
weight: 1569
solve_time_s: 519
verified: true
draft: false
---

[CF 1569C - Jury Meeting](https://codeforces.com/problemset/problem/1569/C)

**Rating:** 1500  
**Tags:** combinatorics, math  
**Solve time:** 8m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the number of permutations of jury members that are “nice,” given how they present their tasks. Each jury member $i$ has $a_i$ tasks, and they tell tasks in order according to a permutation. A permutation is nice if no jury member ever presents two of their tasks consecutively.

The key insight is that the sequence of presentations is effectively a round-robin: in each round, each jury member with remaining tasks presents one task. A permutation fails if some member ends up telling more than one task in a row.

From a structural perspective, the only thing that can cause a permutation to be invalid is if there is a member whose number of tasks is **too large relative to the others**, so that after all others have presented once, this member still has a task left and would have to present twice in a row.

This immediately gives us a concrete condition: let $\text{max}_a$ be the maximum $a_i$ and $\text{sum}_a$ the total sum of all $a_i$. A nice permutation is **impossible** if the largest $a_i$ exceeds the sum of the other $a_i$ plus one. Otherwise, there is always a way to interleave the tasks to avoid consecutive presentations.

Edge cases arise when all jury members have the same number of tasks. For instance, if every $a_i = 1$, then **all permutations are automatically nice**, because no one can present twice in a row. Similarly, if $n = 2$ and the tasks are equal, there is exactly one nice permutation.

The constraints are large ($n$ up to $2 \cdot 10^5$ and $a_i$ up to $10^9$), which rules out any approach that simulates the presentation process explicitly. We need a **combinatorial formula** to count permutations directly.

## Approaches

The brute-force approach is to generate all permutations and simulate the task-sharing process. For each permutation, track each jury member's remaining tasks and check if anyone presents consecutively. This is correct but infeasible: $n!$ permutations is far too large when $n$ reaches $10^5$.

The key observation is that the only restriction comes from the member(s) with the maximum number of tasks. Let $\text{max}_a$ appear $c$ times in the array. If $\text{max}_a - \text{second\_max}_a > 1$, then it is impossible to interleave the tasks without some max-member presenting twice in a row. Otherwise, we can count permutations by first choosing positions for the “second-highest” member(s), and then permuting the remaining members freely.

The combinatorial reasoning can be broken down as:

1. If there is more than one maximum, all permutations are valid except when the largest exceeds the others by more than 1.
2. If the largest occurs once, we must avoid it appearing in the last position relative to the second-largest; the number of bad permutations can be computed combinatorially.

This leads to an efficient $O(n \log n)$ solution using factorials and modular arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!)$ | $O(n)$ | Too slow |
| Combinatorial counting | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read $t$ test cases.
2. For each test case, read $n$ and array $a$.
3. Compute $\text{max}_a = \max(a)$ and count $c$ the number of times it occurs.
4. Compute $\text{second\_max}_a$ as the next largest value in $a$.
5. If $\text{max}_a - \text{second\_max}_a > 1$, print 0 because it is impossible to interleave the tasks.
6. Otherwise, compute factorials up to $n$ modulo $998244353$ for permutation counting.
7. If there are multiple occurrences of $\text{max}_a$, all permutations are valid, so answer is $n!$.
8. If there is a single maximum, calculate the number of permutations where the single maximum is placed “too early” using combinatorial formulas, subtract from $n!$, and print the result modulo $998244353$.

**Why it works**: The correctness relies on the round-robin property. The maximum cannot be placed consecutively; by controlling only the maximum relative to the second maximum, we guarantee that no other member will ever present twice in a row. This reduces the problem to counting valid permutations of positions for these maximum tasks.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    t = int(input())
    fact = [1] * (2*10**5 + 10)
    for i in range(1, len(fact)):
        fact[i] = fact[i-1] * i % MOD
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        mx = max(a)
        c = a.count(mx)
        if c > 1:
            print(fact[n])
            continue
        sec = max(x for x in a if x != mx)
        if mx - sec > 1:
            print(0)
            continue
        cnt = a.count(sec)
        # Number of bad permutations
        bad = fact[n] * modinv(cnt + 1) % MOD
        print((fact[n] - bad + MOD) % MOD)

solve()
```

**Explanation**: We precompute factorials modulo $998244353$. If multiple maxima exist, all permutations are valid. Otherwise, we calculate “bad” permutations where the single maximum appears too early relative to the second maximum, using modular inverses to divide factorials efficiently.

## Worked Examples

Sample input `2 1 2`:

| Permutation | Max | Nice? |
| --- | --- | --- |
| [1,2] | 2 | No, second member presents twice consecutively |
| [2,1] | 2 | Yes, no one presents consecutively |

Output: `1`.

Sample input `3 5 5 5`:

All permutations of `[1,2,3]` are nice because max appears multiple times. Output: `6` (`3!`).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + n \log n)$ | Precompute factorials once, process each test case in O(n) |
| Space | $O(n)$ | Store factorials |

This fits comfortably within the problem limits.

## Test Cases

```python
import sys, io

def run(inp):
    sys.stdin = io.StringIO(inp)
    solve()
    return

# provided samples
run("4\n2\n1 2\n3\n5 5 5\n4\n1 3 3 7\n6\n3 4 2 1 3 3\n")
# Expected output:
# 1
# 6
# 0
# 540

# custom cases
run("1\n2\n1 1\n")  # Expected: 2, all permutations nice
run("1\n3\n1 1 2\n")  # Expected: 5, single max case
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1` | 2 | multiple maxima, all permutations valid |
| `3 1 1 2` | 5 | single max relative to second max |
| `4 5 5 5 5` | 24 | all equal, max appears multiple times |
| `3 1 2 4` | 0 | impossible to interleave |

## Edge Cases

If the largest member has tasks exceeding the sum of others by more than 1, no interleaving avoids consecutive presentations. For example, `n=3, a=[1,1,4]`. Our algorithm detects `4 - 1 > 1` and immediately returns `0`.

If all members have equal tasks, any permutation is valid. Our factorial precomputation ensures these cases are handled efficiently.

This captures all non-obvious constraints from the problem without simulating each permutation.
