---
title: "CF 1712B - Woeful Permutation"
description: "We are given a single integer $n$, and we must arrange the numbers from $1$ to $n$ into a permutation so that a particular score is as large as possible."
date: "2026-06-15T00:45:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1712
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 813 (Div. 2)"
rating: 800
weight: 1712
solve_time_s: 223
verified: true
draft: false
---

[CF 1712B - Woeful Permutation](https://codeforces.com/problemset/problem/1712/B)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, number theory  
**Solve time:** 3m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $n$, and we must arrange the numbers from $1$ to $n$ into a permutation so that a particular score is as large as possible. The score is computed position by position: at index $i$, we take the LCM of $i$ and the value placed at that index, and then sum all these contributions.

So we are not free to change the indices, only the values assigned to each position. Each number from $1$ to $n$ must be used exactly once, and the goal is to maximize how large the LCM values become across all positions.

The constraints allow up to $10^5$ per test case and also up to $10^5$ total across all test cases. This rules out any solution that tries all permutations, since $n!$ grows extremely fast. Even a quadratic approach per test case would be too slow when $n$ is large, since $10^5$ squared is already $10^{10}$, far beyond what a 1 second limit allows. This pushes us toward a linear or near-linear construction.

A subtle edge case appears when $n$ is small. For example, when $n=1$, there is only one permutation, so the answer is forced. When $n=2$, swapping the elements changes the LCM contributions in a non-obvious way, and a naive intuition like “put large numbers in large positions” can already fail if not carefully checked against the LCM structure.

## Approaches

A brute-force approach would try every permutation, compute the sum of LCMs for each, and pick the best. This is correct because it evaluates all possible assignments. However, it requires evaluating $n!$ permutations, and each evaluation costs $O(n)$, leading to $O(n \cdot n!)$, which is completely infeasible even for $n = 10$.

The key observation is that the LCM of two numbers $i$ and $p_i$ is maximized when their product is large and their greatest common divisor is small. Since $\mathrm{lcm}(i, p_i) = \frac{i \cdot p_i}{\gcd(i, p_i)}$, we want pairs where the gcd is as small as possible while also keeping both values large when possible.

This suggests pairing numbers in a way that avoids shared factors. The simplest way to guarantee $\gcd(i, p_i) = 1$ as often as possible is to swap elements in pairs. If we pair $i$ with $i+1$, then $\gcd(i, i+1)=1$, and the LCM becomes $i \cdot (i+1)$, which is large compared to any arrangement involving smaller numbers.

So instead of optimizing globally in a complicated way, we can construct a permutation greedily by swapping adjacent elements. This ensures that every pair contributes a large product-like LCM, and we avoid wasting large values on small indices.

For odd $n$, the last element cannot be paired, so it remains in place.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot n!)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Start with the list $[1, 2, 3, \dots, n]$. This is the baseline permutation before optimization.
2. Traverse the array from left to right in steps of 2.
3. For each pair $(i, i+1)$, swap the two values. This creates pairs $(2,1), (4,3), (6,5), \dots$.
4. If $n$ is odd, leave the last element unchanged since it has no partner.
5. Output the resulting array.

The reason we process in pairs is that adjacent integers are guaranteed to be coprime, which maximizes LCM compared to leaving them in order.

### Why it works

Each swapped pair $(i, i+1)$ produces two LCM terms:

$$\mathrm{lcm}(i, i+1) = i(i+1), \quad \mathrm{lcm}(i+1, i) = i(i+1)$$

in some order depending on position. This is strictly better than keeping them aligned as $\mathrm{lcm}(i,i)=i$ and $\mathrm{lcm}(i+1,i+1)=i+1$, since $2i(i+1)$ grows quadratically while $2i+1$ is linear.

Because each pair is independent and swapping does not affect other positions, we can maximize contribution locally for every adjacent block, and the sum of optimal local choices gives a global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    p = list(range(1, n + 1))

    for i in range(0, n - 1, 2):
        p[i], p[i + 1] = p[i + 1], p[i]

    print(*p)
```

The solution constructs the permutation in linear time by initializing the identity permutation and then swapping every adjacent pair. The loop `range(0, n - 1, 2)` ensures that we only swap valid pairs and naturally handles odd lengths by leaving the last element untouched.

A common mistake is attempting more complex gcd-based logic, but none is needed since adjacency already guarantees maximal benefit locally.

## Worked Examples

### Example 1

Input: $n = 5$

Initial array:

| i | p[i] before | action | p[i] after |
| --- | --- | --- | --- |
| 1 | 1 | swap with 2 | 2 |
| 2 | 2 | swap with 1 | 1 |
| 3 | 3 | swap with 4 | 4 |
| 4 | 4 | swap with 3 | 3 |
| 5 | 5 | none | 5 |

Result: $[2, 1, 4, 3, 5]$

This shows how odd positions remain stable at the end while earlier elements are grouped into optimal pairs.

### Example 2

Input: $n = 6$

| i | p[i] before | action | p[i] after |
| --- | --- | --- | --- |
| 1 | 1 | swap with 2 | 2 |
| 2 | 2 | swap with 1 | 1 |
| 3 | 3 | swap with 4 | 4 |
| 4 | 4 | swap with 3 | 3 |
| 5 | 5 | swap with 6 | 6 |
| 6 | 6 | swap with 5 | 5 |

Result: $[2,1,4,3,6,5]$

This confirms the full pairing structure across the entire array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | We build the permutation once and swap each element at most once |
| Space | $O(n)$ | We store the permutation array |

The solution fits easily within constraints since total $n$ across test cases is at most $10^5$, making the total work linear in input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        p = list(range(1, n + 1))
        for i in range(0, n - 1, 2):
            p[i], p[i + 1] = p[i + 1], p[i]
        out.append(" ".join(map(str, p)))
    return "\n".join(out)

# provided samples
assert run("2\n1\n2\n") == "1\n2 1"

# custom cases
assert run("1\n3\n") == "2 1 3", "odd length"
assert run("1\n4\n") == "2 1 4 3", "basic pairing"
assert run("1\n5\n") == "2 1 4 3 5", "odd tail behavior"
assert run("1\n6\n") == "2 1 4 3 6 5", "full pairing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=3 | 2 1 3 | odd tail handling |
| n=4 | 2 1 4 3 | basic greedy pairing |
| n=5 | 2 1 4 3 5 | mixed odd structure |
| n=6 | 2 1 4 3 6 5 | full coverage consistency |

## Edge Cases

For $n=1$, the algorithm produces $[1]$ since the swap loop does not execute. This matches the only valid permutation, so correctness is immediate.

For $n=2$, the swap produces $[2,1]$. Here the alternative $[1,2]$ gives a smaller score because it wastes the large LCM gain from cross pairing, confirming that even the smallest non-trivial case is handled optimally.

For odd $n$, such as $n=5$, the last element remains untouched. The construction still pairs all earlier elements optimally, and the unpaired element contributes the only possible value at its position, so no improvement is possible by moving it elsewhere without breaking a better pair.
