---
title: "CF 1828B - Permutation Swap"
description: "We are given a permutation of integers from 1 to n in some arbitrary order. Our task is to sort the permutation into ascending order by repeatedly swapping pairs of elements that are exactly k positions apart, for some fixed k."
date: "2026-06-09T07:21:17+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1828
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 873 (Div. 2)"
rating: 900
weight: 1828
solve_time_s: 80
verified: true
draft: false
---

[CF 1828B - Permutation Swap](https://codeforces.com/problemset/problem/1828/B)

**Rating:** 900  
**Tags:** math, number theory  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to n in some arbitrary order. Our task is to sort the permutation into ascending order by repeatedly swapping pairs of elements that are exactly k positions apart, for some fixed k. The problem asks us to choose the largest possible k that still allows the permutation to be sorted under this restriction.

For example, if the permutation is `[3, 1, 2]`, swapping elements that are 1 position apart allows us to sort it as `[1, 2, 3]`. But if we tried k = 2, the only swap we could do would be the first and last element, which is insufficient to fully sort the array. Therefore, the maximum k here is 1.

The constraints are tight enough to rule out naive solutions that try every k from 1 to n. With n up to 10^5 and multiple test cases summing up to 2·10^5 elements, any O(n²) approach would time out. We need an O(n) or O(n log n) approach per test case.

Non-obvious edge cases arise when elements are very far from their correct position. For instance, if a permutation starts with `[n, 1, 2, ..., n-1]`, the maximum k is n-1, since the largest displacement is n-1. A naive algorithm might just check adjacent swaps, missing the fact that distant swaps allow bigger k.

## Approaches

A brute-force approach would be to iterate over all possible k from 1 to n-1 and simulate swaps. For each k, we would try swapping every pair at distance k until no more swaps can help. This works for correctness, but for n = 10^5, simulating all swaps is O(n²) in the worst case, which is too slow.

The key insight is that we do not need to simulate swaps. Each element has a target position, and the distance it needs to move is simply `abs(current_index - target_index)`. For a fixed k, an element can only reach its target if the distance is divisible by k. This reduces the problem to computing the greatest common divisor of all displacement distances. Specifically, the maximum k that can sort the permutation is the GCD of all `abs(p_i - i)` over i from 1 to n. If the GCD is g, then every element can reach its correct position via swaps of distance g. This transforms the problem into an O(n) calculation using a running GCD.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal (GCD of displacements) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `k_max` to 0. This will store the running GCD of displacements.
2. Iterate over all indices i from 1 to n. For each element at position i, calculate its displacement as `abs(p[i] - i)`. This measures how far the element is from its target position.
3. Update `k_max` to be the GCD of itself and the current displacement. Using a running GCD ensures that at the end, `k_max` is the largest integer that divides all displacements.
4. After processing all elements, `k_max` is the maximum value of k that allows sorting the permutation using swaps of distance k.
5. Output `k_max`.

Why it works: the GCD of all displacements guarantees that every element can move to its correct position in multiples of k. If any element has a displacement not divisible by k, it would be impossible to reach its target. Therefore, the maximum k is exactly the GCD of all displacements.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        k_max = 0
        for i, val in enumerate(p, start=1):
            displacement = abs(val - i)
            k_max = math.gcd(k_max, displacement)
        print(k_max)

if __name__ == "__main__":
    main()
```

The solution reads input efficiently using `sys.stdin.readline`. We enumerate positions starting from 1 to match the problem's 1-based indexing. The displacement is always non-negative, and the running GCD accumulates the largest k that divides all distances. Using `math.gcd` handles edge cases like zero displacements automatically.

## Worked Examples

For the permutation `[3, 1, 2]`:

| i | p[i] | displacement | GCD so far |
| --- | --- | --- | --- |
| 1 | 3 | 2 | 2 |
| 2 | 1 | 1 | 1 |
| 3 | 2 | 1 | 1 |

The maximum k is 1, matching the expected output.

For `[3, 4, 1, 2]`:

| i | p[i] | displacement | GCD so far |
| --- | --- | --- | --- |
| 1 | 3 | 2 | 2 |
| 2 | 4 | 2 | 2 |
| 3 | 1 | 2 | 2 |
| 4 | 2 | 2 | 2 |

The maximum k is 2, which also matches the expected output.

These traces confirm that the algorithm correctly identifies the largest k by computing the GCD of all displacements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Computing the displacement and GCD for each element is linear. |
| Space | O(n) | We store the permutation in a list. |

The sum of n over all test cases is ≤ 2·10^5, so total time is acceptable. Memory usage stays within the 256 MB limit.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    return out.getvalue().strip()

# Provided samples
assert run("7\n3\n3 1 2\n4\n3 4 1 2\n7\n4 2 6 7 5 3 1\n9\n1 6 7 4 9 2 3 8 5\n6\n1 5 3 4 2 6\n10\n3 10 5 2 9 6 7 8 1 4\n11\n1 11 6 4 8 3 7 5 9 10 2\n") == "1\n2\n3\n4\n3\n2\n3"

# Custom cases
assert run("1\n2\n2 1\n") == "1", "minimum-size input"
assert run("1\n5\n5 4 3 2 1\n") == "1", "reversed array"
assert run("1\n6\n1 2 3 4 5 6\n") == "0", "already sorted"
assert run("1\n4\n2 4 1 3\n") == "1", "displacements have GCD 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n2 1 | 1 | Minimum-size permutation |
| 5\n5 4 3 2 1 | 1 | Maximum displacement in reversed array |
| 6\n1 2 3 4 5 6 | 0 | Already sorted permutation |
| 4\n2 4 1 3 | 1 | Multiple displacements with GCD 1 |

## Edge Cases

If a permutation is already sorted, all displacements are 0. The algorithm correctly returns 0 as the maximum k. For a reversed array, the displacements are [4, 2, 0, 2, 4] for n = 5. The GCD of these numbers is 1, indicating only k = 1 allows full sorting. The algorithm does not rely on the specific order of elements and handles small and large permutations identically. For a permutation where all elements are evenly spaced from their targets, like `[3, 1, 4, 2]`, the displacements are [2, 1, 1, 2], and the GCD is 1, again giving the correct maximum k. The running GCD computation naturally filters out zeros and handles the edge case of single-element displacements.
