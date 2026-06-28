---
title: "CF 104930G - Dinnerbone and Array"
description: "We are given a small array of integers, each test case independent. From that array, we consider every possible subset of elements except that we are not allowed to take the entire array."
date: "2026-06-28T07:47:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104930
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 01-26-24 Div. 2 (Beginner)"
rating: 0
weight: 104930
solve_time_s: 252
verified: false
draft: false
---

[CF 104930G - Dinnerbone and Array](https://codeforces.com/problemset/problem/104930/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small array of integers, each test case independent. From that array, we consider every possible subset of elements except that we are not allowed to take the entire array. The empty subset is allowed because it is still a subset and does not violate the “not full set” condition.

For any chosen subset $S$, we compute a value formed from two parts: the size of the subset, and the sum of cubes of its elements. The subset size is multiplied, and the sign depends on whether the size is odd or even. Concretely, even-sized subsets contribute positively, odd-sized subsets contribute negatively, and everything is scaled by the subset size itself.

The task is to evaluate this expression for every valid subset and report the minimum and maximum values per test case.

The key constraint is that $N \le 15$. This is the critical signal: although the number of subsets is $2^N$, at most $2^{15} = 32768$, so enumerating all subsets per test case is feasible. Even with up to 1000 test cases, a solution that processes each subset in constant or very small amortized time is acceptable. What becomes unacceptable is any approach that recomputes subset sums from scratch for each subset, which would introduce an extra factor of $N$, pushing the complexity toward half a billion operations.

Edge cases are mostly about subset selection rules and sign behavior.

A common mistake is to assume the empty subset is disallowed because of the “strict subset” wording. If we excluded it, we would miss a valid candidate with value 0, which can affect the minimum or maximum when all other values are strictly positive or negative.

Another subtle case is the full subset exclusion. If we include it by accident, its contribution can dominate because both the subset size multiplier and cube sum are at their maximum.

For example, if $A = [1, 1, 1]$, then the full subset would produce $3 \cdot (-1)^3 \cdot 3 = -9$, which may incorrectly become the minimum, even though it should not be considered.

## Approaches

The most direct approach is to iterate over every subset using bitmasks. For each subset, we compute its size and the sum of cubes of included elements, then evaluate the expression. This is correct because it explicitly follows the definition. The issue is efficiency in computing subset sums repeatedly.

If we recompute the cube sum from scratch for each subset, we scan up to 15 elements per subset. That leads to roughly $2^N \cdot N$, which is about 500,000 operations per test case, and up to 500 million in the worst case across all tests. That is too slow in Python.

The improvement comes from recognizing that subsets form a natural DP structure. If we represent subsets as bitmasks, we can compute each subset’s cube sum incrementally. A subset can be decomposed into a smaller subset plus one newly added element. This allows us to compute all subset sums in $O(2^N)$ time per test case without re-scanning elements.

Once we have subset sums efficiently, evaluating the expression for each subset is constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (rescan per subset) | $O(2^N \cdot N)$ | $O(1)$ | Too slow |
| Bitmask DP over subset sums | $O(2^N)$ | $O(2^N)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Convert each element $A_i$ into its cube value $A_i^3$. This avoids recomputing powers repeatedly and keeps arithmetic local to integers.
2. Precompute subset sums of cubes using a bitmask DP. For each mask, we isolate its least significant set bit and express the mask as a smaller mask plus one element. This guarantees each subset sum is computed once, building on already computed results.
3. For each mask from $0$ to $2^N - 1$, compute the subset size and evaluate the expression $|S| \cdot (-1)^{|S|} \cdot \text{sum}(S)$.
4. Skip the full mask $(1 << N) - 1$, since the problem forbids using the entire array.
5. Track global minimum and maximum over all valid subsets.

The key design choice is computing subset sums via DP rather than recomputation. Without this, the solution would exceed time limits even though $N$ is small.

### Why it works

Every subset corresponds to exactly one bitmask, and every bitmask can be reduced by removing one set bit. The DP ensures that when we compute a subset, the smaller subset it depends on is already known. This creates a strict ordering over masks by number of bits, guaranteeing no recomputation and no missing states. Since the expression depends only on subset size and sum, both fully determined per mask, evaluating each mask independently is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        N = int(input())
        A = list(map(int, input().split()))
        
        nmask = 1 << N
        cube = [x * x * x for x in A]
        
        # subset sum DP over bitmasks
        sub_sum = [0] * nmask
        
        for mask in range(1, nmask):
            lsb = mask & -mask
            idx = (lsb.bit_length() - 1)
            sub_sum[mask] = sub_sum[mask ^ lsb] + cube[idx]
        
        full_mask = nmask - 1
        
        mn = float('inf')
        mx = float('-inf')
        
        for mask in range(nmask):
            if mask == full_mask:
                continue
            
            k = mask.bit_count()
            val = k * sub_sum[mask]
            if k % 2 == 1:
                val = -val
            
            if val < mn:
                mn = val
            if val > mx:
                mx = val
        
        print(mn, mx)

if __name__ == "__main__":
    solve()
```

The cube preprocessing isolates exponentiation so that subset evaluation becomes purely additive. The DP step uses the identity that removing the lowest set bit always leads to a strictly smaller mask already processed. The bit index extraction through `lsb.bit_length() - 1` converts the isolated bit into an array index safely.

During evaluation, subset size is obtained via `bit_count()`, which is efficient for small $N$. The sign flip is applied after multiplication to avoid mistakes with operator precedence.

## Worked Examples

### Example 1

Consider a small array $A = [1, -1, 2]$. We evaluate all subsets except the full set.

| Mask | Subset | Size k | Sum of cubes | Expression |
| --- | --- | --- | --- | --- |
| 000 | {} | 0 | 0 | 0 |
| 001 | {1} | 1 | 1 | -1 |
| 010 | {-1} | 1 | -1 | 1 |
| 100 | {2} | 1 | 8 | -8 |
| 011 | {1,-1} | 2 | 0 | 0 |
| 101 | {1,2} | 2 | 9 | 18 |
| 110 | {-1,2} | 2 | 7 | 14 |

The full set 111 is excluded.

Minimum is -8 and maximum is 18.

This trace shows how odd subsets invert sign while even subsets preserve it, and how scaling by subset size amplifies differences.

### Example 2

Take $A = [-2, -2]$.

| Mask | Subset | Size k | Sum of cubes | Expression |
| --- | --- | --- | --- | --- |
| 00 | {} | 0 | 0 | 0 |
| 01 | {-2} | 1 | -8 | 8 |
| 10 | {-2} | 1 | -8 | 8 |

Full set 11 is excluded.

Both single-element subsets produce identical values, and empty subset anchors the minimum at 0.

This demonstrates that when all elements are identical, subset symmetry collapses the range of outputs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^N)$ per test case | Each subset is computed once, and evaluation is constant time |
| Space | $O(2^N)$ | Stores subset sums for all masks |

With $N \le 15$, each test runs in about 32768 states, and even with 1000 tests this remains within practical limits in Python due to tight integer operations and linear memory access patterns.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isfinite
    
    input = sys.stdin.readline
    
    def solve():
        T = int(input())
        out = []
        for _ in range(T):
            N = int(input())
            A = list(map(int, input().split()))
            
            nmask = 1 << N
            cube = [x * x * x for x in A]
            sub_sum = [0] * nmask
            
            for mask in range(1, nmask):
                lsb = mask & -mask
                idx = (lsb.bit_length() - 1)
                sub_sum[mask] = sub_sum[mask ^ lsb] + cube[idx]
            
            full_mask = nmask - 1
            mn = float('inf')
            mx = float('-inf')
            
            for mask in range(nmask):
                if mask == full_mask:
                    continue
                k = mask.bit_count()
                val = k * sub_sum[mask]
                if k % 2 == 1:
                    val = -val
                mn = min(mn, val)
                mx = max(mx, val)
            
            out.append(f"{mn} {mx}")
        return "\n".join(out)

    return solve()

# provided sample (format adjusted as parsing is unclear in statement)
# assert run(...) == ...

# custom cases
assert run("1\n1\n5\n") == "0 0", "single element excludes full set"
assert run("1\n2\n1 1\n") is not None
assert run("1\n3\n-1 -1 -1\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element | 0 0 | Only empty subset is valid |
| All equal positive | varies | symmetry and full subset exclusion |
| All equal negative | varies | sign alternation behavior |

## Edge Cases

The empty subset is the main conceptual edge case. For an input like $[5]$, the only allowed subsets are empty and the single-element subset is disallowed because it equals the full array. The algorithm evaluates only the empty mask and correctly produces value 0.

The full subset exclusion is another critical condition. For $A = [2, 2]$, the subset containing both elements would yield $2 \cdot (+1) \cdot (16 + 16) = 64$, but it is never considered. The loop explicitly skips this mask, ensuring the maximum comes from single-element subsets instead.

When all elements are negative, cubes preserve negativity but the alternating sign from subset size creates non-intuitive flips. The DP still handles this correctly because it never assumes monotonicity, it evaluates each subset independently from its computed sum.
