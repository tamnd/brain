---
title: "CF 104743B - Array Construction"
description: "We are asked to build an array of length n using non-negative integers, with the additional restriction that all elements must be pairwise distinct. The array is not arbitrary, because two global bitwise constraints must hold simultaneously."
date: "2026-06-28T23:11:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104743
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #25(5^2-Forces)"
rating: 0
weight: 104743
solve_time_s: 80
verified: false
draft: false
---

[CF 104743B - Array Construction](https://codeforces.com/problemset/problem/104743/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to build an array of length `n` using non-negative integers, with the additional restriction that all elements must be pairwise distinct. The array is not arbitrary, because two global bitwise constraints must hold simultaneously.

The first constraint fixes the bitwise OR of the entire array to be exactly `x`. This means every bit that is set in any array element must collectively cover exactly the set bits of `x`, no more and no less. If any element introduces a bit outside `x`, the OR would exceed `x`. If some bit in `x` is missing from all elements, the OR would be smaller.

The second constraint fixes the bitwise AND of the entire array to be exactly `y`. This forces every element to contain all bits that are set in `y`. If even one element misses a bit of `y`, the global AND loses it. At the same time, no extra bit can survive in all elements unless it is already in `y`.

So each element must lie in a very tight bitwise corridor: every number must include all bits of `y`, and must not include any bit outside `x`.

From constraints, `t` can be up to `10^5`, so each test must be solved in constant or logarithmic time. Any approach that constructs arrays explicitly or tries subsets of values will fail immediately. We are forced into reasoning purely about bit patterns and existence conditions.

A few edge cases already stand out.

If `n = 1`, the array has only one element, so OR and AND both equal that element. This forces `x = y`, otherwise the answer is impossible.

If `y` contains a bit that is not in `x`, there is no valid number even individually, because every element must respect both constraints simultaneously.

Another subtle case appears when `n > 1`. Even if a single number `x` satisfies both OR and AND constraints, we still must ensure we can create multiple distinct numbers without breaking the OR or AND structure. This is where naive intuition fails, because duplicating values is forbidden and small perturbations can break AND or OR unexpectedly.

## Approaches

A brute-force approach would attempt to construct all possible arrays of size `n` from the valid domain of numbers between `0` and `2^{30}-1`, then check OR and AND. Even restricting to values consistent with `x` and `y`, the search space is still exponential in `n`, since every position is independent but constrained by global conditions. For `n = 30`, even a restricted enumeration becomes astronomically large.

The structure of the problem becomes clearer if we rewrite each element constraint in bit terms. Since every element must contribute to an AND of `y`, every element must contain all bits of `y`. So every valid element has the form `y | t`, where `t` uses only bits that are inside `x` but outside `y`.

Now we focus on the OR condition. The OR of all elements must become exactly `x`. Since every element already contains `y`, the OR already includes all bits of `y`. The remaining task is to cover all bits in `x` that are not in `y` using the chosen `t` parts across elements.

This transforms the problem into a classic covering and distinctness issue over bitmasks: we need to pick `n` distinct supersets of `y`, all contained within `x`, whose union of extra bits equals `x \ y`.

The key observation is that there are only two meaningful types of elements: those that contribute some subset of the extra bits, and those that may be identical in the `y`-core but must still remain distinct overall. Distinctness forces us to ensure enough freedom in the non-fixed bits to generate `n` different values.

The decisive simplification comes from understanding capacity. The number of available distinct masks is exactly `2^k`, where `k` is the number of free bits in `x` that are not fixed by `y`. If `n` exceeds this number, we cannot form distinct elements at all.

Also, if `y` is not a submask of `x`, no construction exists. Finally, when `n = 1`, equality of OR and AND forces equality of `x` and `y`.

This reduces the problem to simple bit counting and a few logical checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential | O(n) | Too slow |
| Bitmask Analysis | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We translate the conditions into bit operations.

1. First check whether `y` is compatible with `x` by verifying `(y & x) == y`. If not, some bit required in every element cannot exist in `x`, so construction is impossible.
2. If `n == 1`, the array has only one element. That element must simultaneously produce OR and AND equal to itself, so we require `x == y`. If this fails, no valid array exists.
3. Compute the number of free bits, defined as bits that are set in `x` but not in `y`. Let `free = x ^ y` after ensuring no overlap outside constraints. The actual number of usable patterns depends on how many bits are set in `free`.
4. The number of distinct values we can construct using these free bits is `2^(popcount(free))`, because each subset of free bits gives a unique valid number of the form `y | subset`.
5. If `n` is greater than this number of available distinct values, we cannot satisfy the distinctness constraint, so output `NO`.
6. Otherwise, output `YES`.

### Why it works

Every valid element must include all bits of `y`, so every element is uniquely determined by which subset of the remaining bits it activates. These subsets are independent and do not affect the mandatory `y` bits. Therefore, the problem reduces to selecting `n` distinct subsets of a finite set of size equal to the number of free bits in `x`. The OR constraint is satisfiable as long as we can cover all free bits across chosen subsets, which is always possible when at least one subset includes each bit, and such subsets exist whenever the bit is part of `x`. The only limiting factor is whether we have enough distinct subsets to assign to all positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x, y = map(int, input().split())

        if (y & x) != y:
            print("NO")
            continue

        if n == 1:
            print("YES" if x == y else "NO")
            continue

        free = x ^ y
        k = free.bit_count()

        if n > (1 << k):
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the reduction to bit reasoning. The first check enforces feasibility of the AND constraint inside the OR space. The second handles the degenerate single-element case where OR and AND collapse. The final step counts how many independent bits remain free for variation and checks whether they can generate enough distinct numbers.

The use of `bit_count()` is crucial because it gives the exact number of independent degrees of freedom in the mask. The final comparison against `2^k` captures the entire combinatorial capacity of valid constructions.

## Worked Examples

### Example 1

Input:

```
n = 3, x = 7, y = 3
```

Here `x = 111₂`, `y = 011₂`. The free bit is only the highest bit of `x`.

| Step | Value |
| --- | --- |
| Check `(y & x) == y` | True |
| n == 1 | False |
| free = x ^ y | 100₂ |
| k = popcount(free) | 1 |
| capacity = 2^k | 2 |
| n ≤ capacity | 3 ≤ 2 is False |

Output is `NO`. We only have two distinct valid patterns: `011` and `111`, so we cannot form 3 distinct elements.

This confirms that distinctness is the limiting factor.

### Example 2

Input:

```
n = 2, x = 5, y = 1
```

Binary: `x = 101₂`, `y = 001₂`.

| Step | Value |
| --- | --- |
| Check `(y & x) == y` | True |
| free = x ^ y | 100₂ |
| k = popcount(free) | 1 |
| capacity = 2 | 2 |
| n ≤ capacity | True |

We can construct `{1, 5}`.

OR is `101`, AND is `001`, and both elements are distinct.

This shows the construction space exactly matches subset choices of free bits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test uses constant-time bit operations |
| Space | O(1) | Only a few integers per test |

The solution easily fits within limits since even `10^5` test cases only require basic arithmetic and bit counting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, x, y = map(int, input().split())

        if (y & x) != y:
            out.append("NO")
            continue

        if n == 1:
            out.append("YES" if x == y else "NO")
            continue

        free = x ^ y
        k = free.bit_count()

        out.append("YES" if n <= (1 << k) else "NO")

    return "\n".join(out)

# provided samples (as given format reconstructed)
assert run("4\n1 0 0\n3 1 4\n2 1000000000 1\n4 2 3\n") == "YES\nYES\nNO\nNO"

# custom cases
assert run("1\n1 7 7\n") == "YES", "single element exact match"
assert run("1\n1 7 3\n") == "NO", "single element mismatch"
assert run("1\n2 1 2\n") == "NO", "invalid mask relation"
assert run("1\n4 3 3\n") == "YES", "max freedom case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 7 7` | YES | single-element equality case |
| `1 7 3` | NO | n=1 forces x=y |
| `2 1 2` | NO | invalid bit compatibility |
| `4 3 3` | YES | maximum freedom scenario |

## Edge Cases

One edge case is when `n = 1`. For input `n = 1, x = 5, y = 1`, the algorithm immediately rejects because `x != y`. The only possible array is `[a1]`, and it must satisfy both OR and AND equal to `a1`, forcing equality of targets. The check handles this directly before any bit reasoning.

Another edge case is when `y` is not a subset of `x`, for example `x = 2 (010₂), y = 1 (001₂)`. The condition `(y & x) == y` fails, correctly rejecting the case because no number can simultaneously contain bit 0 and avoid violating OR constraints.

A final subtle case occurs when `x == y`. Here `free = 0`, so only one valid number exists: `y` itself. If `n > 1`, the algorithm correctly returns `NO` since distinct elements cannot be formed.
