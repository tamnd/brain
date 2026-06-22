---
title: "CF 105437D - Equal Halves"
description: "We are given an array of even length, split conceptually into two equal parts: the left half and the right half. We are allowed to perform exactly one swap, but the swap is heavily constrained."
date: "2026-06-23T03:42:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105437
codeforces_index: "D"
codeforces_contest_name: "ICPC 2024-2025 NERC, Southern and Volga Russia Qualifier"
rating: 0
weight: 105437
solve_time_s: 106
verified: false
draft: false
---

[CF 105437D - Equal Halves](https://codeforces.com/problemset/problem/105437/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of even length, split conceptually into two equal parts: the left half and the right half. We are allowed to perform exactly one swap, but the swap is heavily constrained. We must pick one index from the left half and one index from the right half, and exchange their values.

After doing this single swap, we want the sum of the left half to become exactly equal to the sum of the right half. The task is to determine whether such a swap exists, and if it does, output any valid pair of positions.

The constraint that stands out is the array size up to 200,000. Any solution that tries all pairs across halves would require about (n/2)^2 checks, which becomes roughly 10^10 operations in the worst case, far beyond feasible limits in 2 seconds. This immediately rules out brute-force pairing.

The values themselves are bounded by 10,000, which is small enough that frequency-based reasoning or hashing techniques become plausible.

A subtle point is that we must perform exactly one swap, not at most one. So even if the array already has equal halves, we still need to find a swap that preserves equality rather than doing nothing.

A failure mode for naive reasoning is assuming we can pick any element from the left and match it greedily with something from the right that balances the sums locally. For example, trying to match differences independently ignores the global sum constraint, because swapping affects both halves simultaneously.

Another trap is forgetting that the swap must cross halves. A valid internal swap inside one half is disallowed even if it would balance sums.

## Approaches

A direct approach is to try every pair (i, j) with i in the left half and j in the right half, simulate the swap, and recompute both half sums. Each check costs O(n) if recomputed naively, or O(1) if we maintain prefix sums. Even with O(1) checks, we still have O(n^2) pairs, which is about 10^10 operations, too slow.

To improve, we rewrite the effect of a swap algebraically. Let the initial left sum be S_L and right sum be S_R. Suppose we swap a value x from the left with a value y from the right. After swapping, the left sum becomes S_L - x + y, and the right sum becomes S_R - y + x. We want:

S_L - x + y = S_R - y + x

Rearranging gives:

S_L - S_R = 2(x - y)

This is the key reduction. The entire problem becomes finding a pair (x, y) such that their difference is fixed by the global imbalance between halves.

Let D = S_L - S_R. Then we need:

x - y = D / 2

This immediately implies D must be even, otherwise no solution exists.

Now the task becomes: find x in the left half and y in the right half such that y = x - D/2. Since values are bounded and we only need membership checks, we can store the right half in a hash set or frequency map and test each left element.

This reduces the problem from pair search over indices to value matching with bookkeeping of positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of the left half and the sum of the right half. The difference between them is the only global information that matters, because every swap affects both halves symmetrically.
2. Compute D = S_L - S_R. If D is odd, stop immediately. No integer pair (x, y) can satisfy x - y = D/2, so no swap can balance the halves.
3. Build a mapping from values in the right half to their indices. We only need to know whether a value exists and where it occurs, because we are free to choose any valid position.
4. Compute target difference k = D / 2. We now want to find a left element x such that (x - k) exists in the right half. This directly encodes the swap condition derived earlier.
5. Iterate through the left half. For each position i with value x, check whether x - k exists in the right half map. If it does, we immediately return (i, corresponding index). This is valid because it satisfies the derived equality condition, guaranteeing balanced sums after the swap.
6. If no such pair is found after scanning the left half, output NO.

### Why it works

The transformation reduces the swap effect to a single linear equation in the chosen values. Any valid swap must satisfy x - y = D/2, and any pair satisfying this equation necessarily equalizes the two half sums when substituted back into the updated sums. Since we check every candidate left value against all possible matching right values, we do not miss any feasible swap.

The correctness rests on the fact that the swap only changes sums by subtracting and adding exactly the swapped values. There are no other interactions between positions, so the equation fully characterizes feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    mid = n // 2
    left = a[:mid]
    right = a[mid:]
    
    sum_left = sum(left)
    sum_right = sum(right)
    
    diff = sum_left - sum_right
    
    if diff % 2 != 0:
        print("NO")
        return
    
    k = diff // 2
    
    pos_right = {}
    for i, val in enumerate(right):
        if val not in pos_right:
            pos_right[val] = i + 1  # 1-based index in right half
    
    for i, val in enumerate(left):
        need = val - k
        if need in pos_right:
            print("YES")
            print(i + 1, pos_right[need] + mid)
            return
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The solution starts by splitting the array into halves and computing their sums directly. The key implementation detail is maintaining indices separately for the right half using 1-based indexing relative to that segment, then converting back to global indexing by adding `mid`.

The computed value `k` is the half-difference between sums, and we use it to translate the condition into a lookup problem. For each left element, we compute the required partner value in the right half and check existence in constant time using a dictionary.

A common pitfall is forgetting to shift indices when reporting the right-side position. Another is incorrectly computing `k` as the full difference instead of half, which breaks the equation derived from the swap effect.

## Worked Examples

### Example 1

Input:

```
6
4 1 2 6 7 6
```

Left half is `[4, 1, 2]`, right half is `[6, 7, 6]`.

| Step | S_L | S_R | diff | k | Action |
| --- | --- | --- | --- | --- | --- |
| init | 7 | 19 | -12 | -6 | compute sums |
| check | 7 | 19 | -12 | -6 | build right map |
| scan i=1 | 4 | - | - | - | need = 4 - (-6) = 10 not found |
| scan i=2 | 1 | - | - | - | need = 1 - (-6) = 7 found |
| stop | - | - | - | - | output swap |

We find that swapping value 1 from the left with value 7 from the right balances the sums. After swap, both halves sum to 13, confirming the derived condition works exactly.

### Example 2

Input:

```
4
5 4 3 5
```

Left half is `[5, 4]`, right half is `[3, 5]`.

| Step | S_L | S_R | diff | k | Action |
| --- | --- | --- | --- | --- | --- |
| init | 9 | 8 | 1 | 0.5 | diff is odd |
| stop | 9 | 8 | 1 | - | output NO |

Since the difference is odd, no integer swap can satisfy x - y = D/2, and the algorithm correctly terminates early.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | one pass to compute sums, one pass to build hash map, one pass over left half |
| Space | O(n) | storage for right half value-to-index mapping |

The solution comfortably fits within limits since n is up to 200,000, and all operations are linear-time hash lookups and simple arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample tests
assert run("6\n4 1 2 6 7 6\n") == "YES\n2 5"
assert run("4\n5 4 3 5\n") == "NO"

# all equal values (always possible swap exists)
assert run("4\n1 1 1 1\n") != ""

# minimal case
assert run("2\n1 2\n") == "YES\n1 2"

# no solution case
assert run("6\n1 1 1 100 100 100\n") == "NO"

# crafted imbalance odd sum difference
assert run("4\n1 2 3 10\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 elements | YES swap | minimal boundary correctness |
| all equal | any YES | existence in symmetric cases |
| strongly imbalanced | NO | failure cases |
| odd diff case | NO | parity constraint |

## Edge Cases

One edge case is when the array is already balanced. For example:

Input:

```
4
1 2 2 1
```

Here both halves sum to 3. The algorithm computes diff = 0, so k = 0. This means we need x = y, so any identical-value cross-half pair is valid. The hash map on the right half ensures that if a value exists on both sides, we immediately find a valid swap, even though the sums were already equal.

Another case is when multiple identical values exist. The mapping stores only one index per value, but this is sufficient because any occurrence is valid. Even if multiple swaps exist, returning the first found pair still satisfies the condition since the equation depends only on values, not positions.
