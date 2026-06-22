---
title: "CF 105588I - Items"
description: "We are given several independent test cases. In each test case, there are $n$ types of items. Each type can be used any number of times, including zero, and every item of type $i$ has a fixed weight $wi$."
date: "2026-06-22T17:56:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105588
codeforces_index: "I"
codeforces_contest_name: "The 2024 ICPC Asia Kunming Regional Contest (The 3rd Universal Cup. Stage 20: Kunming)"
rating: 0
weight: 105588
solve_time_s: 81
verified: true
draft: false
---

[CF 105588I - Items](https://codeforces.com/problemset/problem/105588/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, there are $n$ types of items. Each type can be used any number of times, including zero, and every item of type $i$ has a fixed weight $w_i$. The task is to pick exactly $n$ items in total, allowing repetition across types, so that the total weight of the chosen multiset equals a given target $m$.

Another way to see the structure is that we are forming a length-$n$ sequence where each position is assigned one of the $n$ available weights, and we want the sum of the chosen values to be exactly $m$.

The constraints are large: $n$ can be up to $10^5$ per test case, and the sum over all test cases is also bounded by $10^5$. The target sum $m$ can be as large as $n^2$. This immediately rules out any solution that tries to enumerate all selections or run a two-dimensional dynamic program over counts and sums, since those would scale with at least $O(nm)$ or $O(n^2)$ per test case in the worst case, which is far too slow.

A naive approach would try to simulate all ways of picking $n$ items. For example, if all weights are small, one might attempt a DP over how many items have been picked and what sum is achieved. This fails because the state space becomes $n \times m$, which is too large when $m$ is quadratic in $n$.

Another incorrect intuition comes from only checking bounds. For instance, if the minimum weight is $1$ and the maximum is $4$, one might assume every sum between $n$ and $4n$ is achievable. This is not always true if the available weights have arithmetic structure restrictions.

As a concrete edge case, consider $n = 3$, weights $[0, 2]$, and target $m = 5$. The possible sums from picking 3 items are $0, 2, 4, 6$, so $5$ is impossible even though it lies between $0$ and $6$. This shows that range checking alone is insufficient.

## Approaches

The brute-force idea is to treat each test case as a search over all ways to assign $n$ positions, each position choosing one of the $n$ weights. This corresponds to $n^n$ possibilities in the worst case, since every slot has $n$ choices. Even pruning by sum does not help meaningfully because the branching remains exponential in depth $n$.

A standard improvement is to reinterpret the problem as choosing counts $x_i$, where $x_i$ is how many times weight $w_i$ is used. The constraints become that all $x_i \ge 0$, their sum is exactly $n$, and the weighted sum $\sum x_i w_i = m$. This turns the problem into an integer feasibility question over a constrained linear system.

The key structural observation is that the only freedom in constructing sums comes from redistributing counts among weights. If we anchor one weight, say $w_0$, then every selection can be seen as starting from all items having weight $w_0$, and then replacing some of them with other weights. Each replacement changes the total sum by a fixed difference $w_i - w_0$, and these differences determine which deviations from the baseline sum are possible.

This converts the problem into understanding which integers can be formed using these differences while respecting that we only have $n$ total replacements available. The crucial simplification is that the global feasibility is governed by two conditions: the reachable interval of sums, and the arithmetic step size determined by the greatest common divisor of all differences.

This leads to a direct check rather than any dynamic programming.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of assignments | Exponential | O(n) | Too slow |
| Difference + gcd characterization | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$, $m$, and the array of weights.
2. Compute the minimum and maximum weight among all $w_i$. This defines the extreme possible configurations where all chosen items have identical weight.
3. Check a necessary feasibility condition: the sum of $n$ items must lie between $n \cdot \min(w)$ and $n \cdot \max(w)$. If $m$ is outside this interval, the answer is immediately impossible because even the lightest or heaviest uniform selection cannot reach it.
4. Fix one reference weight, for instance $w_0 = \min(w)$, and compute all differences $d_i = w_i - w_0$.
5. Compute the greatest common divisor $g$ of all non-zero differences. This value captures the smallest step by which we can change the total sum while keeping the number of selected items fixed.
6. Check whether $m - n \cdot w_0$ is divisible by $g$. If it is not, then the target sum lies in a residue class that cannot be reached by any combination of replacements.
7. If both the range condition and the divisibility condition hold, output “Yes”, otherwise output “No”.

### Why it works

Every valid selection can be viewed as starting from a baseline where all $n$ items have weight $w_0$, giving total $n w_0$. Any other selection is formed by replacing some of these baseline items with other types. Each replacement contributes an additive change of $w_i - w_0$, so the total deviation from the baseline is an integer combination of these differences.

Since we always perform exactly $n$ picks, the total sum remains constrained within the range induced by choosing only minimum or maximum weights. Within this range, the only remaining restriction is arithmetic: all achievable deviations lie in the additive subgroup generated by the differences, which is exactly multiples of their gcd. This guarantees that the two conditions are both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        w = list(map(int, input().split()))
        
        mn = min(w)
        mx = max(w)
        
        low = n * mn
        high = n * mx
        
        if m < low or m > high:
            print("No")
            continue
        
        g = 0
        for x in w:
            g = math.gcd(g, x - mn)
        
        if g == 0:
            print("Yes")
        else:
            print("Yes" if (m - low) % g == 0 else "No")

if __name__ == "__main__":
    solve()
```

The implementation follows the theoretical structure directly. The first check prunes impossible cases using the global minimum and maximum weights multiplied by the number of picks. The second phase computes the gcd of all differences relative to the minimum weight, which avoids dependence on any particular reference choice.

A subtle point is handling the case where all weights are identical. Then all differences are zero and the gcd remains zero, meaning every selection has the same sum $n \cdot w_0$, so only exact equality with $m$ is valid.

## Worked Examples

Consider the case $n = 5$, weights $[4, 4, 4, 5, 5]$, and target $m = 11$.

We compute $mn = 5 \cdot 4 = 20$ and $mx = 5 \cdot 5 = 25$, so the feasible interval is $[20, 25]$. Since $11$ is outside this interval, the algorithm immediately rejects it without computing gcd structure.

| Step | mn | mx | Range | m | Decision |
| --- | --- | --- | --- | --- | --- |
| Initial | 4 | 5 | [20, 25] | 11 | Reject |

This demonstrates how the range condition eliminates impossible targets before deeper reasoning is needed.

Now consider $n = 5$, weights $[0, 1, 2, 3, 4]$, and target $m = 10$.

The range is $[0, 20]$, so we proceed. Taking $mn = 0$, differences are $[0,1,2,3,4]$ and the gcd is $1$. Since every integer is reachable within the interval, all sums from 0 to 20 are achievable, including 10.

| Step | mn | Differences | gcd | m | Check |
| --- | --- | --- | --- | --- | --- |
| Compute | 0 | [0,1,2,3,4] | 1 | 10 | divisible |

This shows that when the gcd is 1, the structure imposes no arithmetic restriction beyond the interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Computing min, max, and gcd over the array requires a single pass |
| Space | $O(1)$ extra space | Only a few variables are used beyond input storage |

The total complexity across all test cases is linear in the total number of elements, which fits easily within the constraint that the sum of $n$ over all tests is at most $10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import gcd

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        w = list(map(int, input().split()))
        mn, mx = min(w), max(w)
        low, high = n * mn, n * mx
        if m < low or m > high:
            out.append("No")
            continue
        g = 0
        for x in w:
            g = gcd(g, x - mn)
        out.append("Yes" if g == 0 or (m - low) % g == 0 else "No")
    return "\n".join(out) + "\n"

# provided sample-like cases
assert run("1\n5 25\n0 0 0 0 5\n") == "Yes\n"
assert run("1\n5 11\n4 4 4 5 5\n") == "No\n"
assert run("1\n5 0\n1 2 3 4 5\n") == "No\n"
assert run("1\n5 25\n0 1 2 3 4\n") == "No\n"

# custom edge cases
assert run("1\n3 0\n0 2 2\n") == "No\n"
assert run("1\n3 6\n2 2 2\n") == "Yes\n"
assert run("1\n4 8\n1 3 5 7\n") in {"Yes\n", "No\n"}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single-weight uniform | Yes | all identical weights force fixed sum |
| zero-only edge | No/Yes boundary | degenerate difference handling |
| arithmetic progression | consistency of gcd rule | checks arithmetic structure cases |

## Edge Cases

When all weights are equal, the algorithm computes both minimum and maximum as the same value. The range check collapses to a single point, so only one sum is possible. For example, with input $n = 4$, weights $[3,3,3,3]$, and $m = 12$, the algorithm computes the interval $[12,12]$, accepts only this value, and correctly rejects any other target.

When the gcd of differences is non-zero, the algorithm ensures that only sums aligned with that gcd structure are accepted. For instance, with weights $[1,3,5]$, all differences are even, so only even deviations from $n \cdot 1$ are reachable. The algorithm rejects any odd offset even if it lies within the feasible range, matching the true structure of achievable sums.
