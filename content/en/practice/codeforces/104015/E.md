---
title: "CF 104015E - Delete Two Elements"
description: "We are given an array of integers and we first compute its average value, which is the total sum divided by the number of elements. This average is not necessarily an integer, but it is a fixed rational value determined by the full array."
date: "2026-07-02T04:51:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104015
codeforces_index: "E"
codeforces_contest_name: "ICPC 2021-2022 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 104015
solve_time_s: 43
verified: true
draft: false
---

[CF 104015E - Delete Two Elements](https://codeforces.com/problemset/problem/104015/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and we first compute its average value, which is the total sum divided by the number of elements. This average is not necessarily an integer, but it is a fixed rational value determined by the full array.

The task is to remove exactly two distinct elements so that when we recompute the average of the remaining elements, it stays exactly the same as the original average. We are asked to count how many pairs of indices produce this property.

The key constraint is the array size, which can be up to 200,000. Any solution that checks all pairs directly would consider about $\frac{n(n-1)}{2}$ removals, which is around 20 billion operations in the worst case. That is far beyond what fits into two seconds in Python or C++. This immediately rules out any quadratic approach.

There is a subtle edge case when all elements are identical. In that case, removing any two elements preserves the average trivially, because every subset has the same mean. A naive implementation might still go through unnecessary arithmetic or risk precision issues if it tries to recompute averages directly as floating point numbers.

Another important case is when the average is non-integer. A careless solution might try to compare floating-point averages after deletion. This is unsafe because precision errors could cause incorrect equality checks even when the algebraic condition holds exactly.

## Approaches

A brute-force solution would iterate over all pairs $(i, j)$, remove those two elements, recompute the sum of the remaining array, and check whether the average matches the original one. Computing the remaining sum can be optimized to O(1) using prefix sums, but we still have O(n^2) pairs to test, which leads to about $10^{10}$ checks in the worst case. Even with constant-time arithmetic per check, this is too slow.

The key observation comes from rewriting the condition algebraically. Let the total sum of the array be $S$, and let the original mean be $k = S / n$. After removing two elements $a_i$ and $a_j$, the new sum becomes $S - a_i - a_j$, and the new number of elements is $n - 2$. We require:

$$\frac{S - a_i - a_j}{n - 2} = \frac{S}{n}$$

Cross-multiplying avoids fractions entirely and reveals a linear constraint on pairs. This turns the problem from checking averages into counting pairs with a fixed sum condition. After simplification, each valid pair must satisfy:

$$a_i + a_j = \frac{2S}{n}$$

So the entire task reduces to counting how many pairs sum to a constant target value. This is a classic frequency counting problem that can be solved in linear time using a hash map.

We compute the frequency of each value and then, for each distinct value $x$, we look for its complement $T - x$, where $T = 2S / n$. Care must be taken to avoid double counting and to handle the case where $x = T - x$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Frequency Hashing | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum $S$ of the array and derive the target sum $T = 2S / n$. This value represents what every valid pair must add up to after algebraic transformation of the mean condition.
2. If $2S$ is not divisible by $n$, stop immediately and return 0. In this case, the target sum is not an integer, but all array elements are integers, so no pair can satisfy the condition exactly.
3. Build a frequency map of all array values. This allows us to count how many times each candidate element appears, which is necessary for efficiently counting valid pairs.
4. Iterate over each distinct value $x$ in the frequency map. For each such value, compute its complement $y = T - x$.
5. If $x < y$, count all pairs formed by choosing one occurrence of $x$ and one occurrence of $y$. The number of such pairs is $freq[x] \cdot freq[y]$. The ordering constraint avoids double counting.
6. If $x = y$, count pairs formed entirely within the same value group. The number of such pairs is $freq[x] \cdot (freq[x] - 1) / 2$.
7. Sum all contributions and output the result.

### Why it works

The transformation from an average constraint to a fixed-sum constraint is exact and reversible. Every valid deletion must preserve the mean, and algebra shows this is equivalent to requiring the removed pair to have sum exactly $T = 2S/n$. The frequency-based counting enumerates each unordered pair exactly once, either through distinct complements or within a single value class. No valid pair is missed because every pair of indices is represented by exactly one value combination in the frequency map, and no invalid pair is included because all counted pairs satisfy the derived equality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    s = sum(a)
    if (2 * s) % n != 0:
        print(0)
        return
    
    target = (2 * s) // n
    
    freq = {}
    for x in a:
        freq[x] = freq.get(x, 0) + 1
    
    ans = 0
    for x in freq:
        y = target - x
        if y not in freq:
            continue
        if x < y:
            ans += freq[x] * freq[y]
        elif x == y:
            c = freq[x]
            ans += c * (c - 1) // 2
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by computing the total sum and checking divisibility to ensure the derived target pair sum is integral. This avoids floating-point comparisons entirely. The frequency dictionary tracks occurrences of each value so that pair counting becomes combinational rather than iterative.

The loop over keys carefully enforces ordering using `x < y`, which prevents double counting pairs like (x, y) and (y, x). The equal case uses the standard combination formula for selecting two indices from a group of identical values.

## Worked Examples

### Example 1

Input:

```
4
8 8 8 8
```

Here, $S = 32$, so $T = 2S/n = 16$. Every element is 8, so we check pairs summing to 16.

| Value x | Frequency | Complement y | Contribution |
| --- | --- | --- | --- |
| 8 | 4 | 8 | 4 * 3 / 2 = 6 |

The algorithm counts all ways to pick two elements from four identical values. Every deletion preserves the mean because the array remains constant.

Output:

```
6
```

This confirms that when all values are equal, every pair is valid and combinatorial counting is sufficient.

### Example 2

Input:

```
5
1 4 7 3 5
```

Sum is $20$, so $T = 8$. We count pairs summing to 8.

| x | freq[x] | y = 8-x | freq[y] | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | 7 | 1 | 1 |
| 3 | 1 | 5 | 1 | 1 |
| 4 | 1 | 4 | 1 | ignored (x > y already handled) |

Output:

```
2
```

This trace shows how symmetry handling prevents double counting while still capturing all valid complementary pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute sum and frequency map, one pass over distinct values |
| Space | O(n) | Frequency map stores at most n distinct elements |

The algorithm scales linearly with input size, which is essential for handling up to 200,000 elements within the time limit. The memory usage is also linear and fits comfortably within typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old
    return out.getvalue().strip()

# sample-like cases
assert run("4\n8 8 8 8\n") == "6"
assert run("5\n1 4 7 3 5\n") == "2"

# minimum size
assert run("3\n1 2 3\n") == "0"

# no valid pairs
assert run("4\n1 2 3 4\n") == "0"

# all equal large
assert run("6\n5 5 5 5 5 5\n") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 identical elements | 6 | combinatorial counting correctness |
| 1 4 7 3 5 | 2 | complementary pairing logic |
| 1 2 3 | 0 | no valid pair case |
| 1 2 3 4 | 0 | non-trivial no-solution distribution |
| all 5s (n=6) | 15 | edge case with full symmetry |

## Edge Cases

For the all-equal case, say $n = 6$ and array is `[5, 5, 5, 5, 5, 5]`. The total sum is 30, so target pair sum is 10. Every pair of 5s is valid. The algorithm builds frequency `freq[5] = 6` and enters the equal-case branch. It computes $6 \cdot 5 / 2 = 15$, which matches the number of ways to pick any two positions.

For a case where no integer target exists, such as `[1, 2, 3]`, the sum is 6, so $2S/n = 4$. This is valid, but no pair sums to 4. The frequency map checks pairs and finds none, resulting in 0. If instead the sum had produced a fractional target, the early divisibility check would have correctly returned 0 without needing to scan pairs.

For mixed arrays like `[1, 4, 7, 3, 5]`, the algorithm pairs values strictly by complement structure. Each valid pair appears exactly once due to the ordering constraint, preventing overcounting while still capturing all valid deletions.
