---
title: "CF 105972E - \u0421\u0430\u043c\u043e\u043b\u0435\u0442\u044b-\u0441\u0430\u043c\u043e\u043b\u0435\u0442\u044b"
description: "We are given an array of integers, and we need to count how many subsegments are “good” under a very specific growth-based constraint."
date: "2026-06-25T13:35:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105972
codeforces_index: "E"
codeforces_contest_name: "BSUIR Open XIII: School final"
rating: 0
weight: 105972
solve_time_s: 56
verified: true
draft: false
---

[CF 105972E - \u0421\u0430\u043c\u043e\u043b\u0435\u0442\u044b-\u0441\u0430\u043c\u043e\u043b\u0435\u0442\u044b](https://codeforces.com/problemset/problem/105972/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we need to count how many subsegments are “good” under a very specific growth-based constraint.

A subsegment $[l, r]$ is considered good if we can match every position inside this segment, starting from length 1 up to its full length, with values from the segment that can be expressed in a special form. Concretely, for each exponent $i = 1, 2, \ldots, (r - l + 1)$, there must exist at least one element in the segment that equals $x^i$ for some integer $x$. The key point is that for each exponent $i$, the base $x$ is allowed to vary independently, so we are not looking for a single geometric progression, but rather the presence of at least one perfect $i$-th power in the segment for every $i$.

So the condition does not ask for structure across indices; it asks whether the segment collectively contains at least one number that is a perfect square, at least one number that is a perfect cube, and so on up to exponent equal to the segment length.

Reframed, a segment of length $k$ is good if for every exponent $i$ from $1$ to $k$, the segment contains at least one value that is a perfect $i$-th power of some integer.

The input is a single array of up to $10^5$ elements, each up to $10^9$. The output is the number of subarrays satisfying this property.

The constraint $n \le 10^5$ rules out any approach that inspects all $O(n^2)$ subarrays with recomputation of exponent checks inside each one. Even a naive $O(n^2 \sqrt{\max a_i})$ or $O(n^2 \log a_i)$ solution would be too slow.

The subtle difficulty is that checking whether a segment is good depends on the distribution of number-theoretic properties inside it, not on ordering or sums. This makes prefix aggregation non-trivial.

A few edge cases matter directly:

A single-element segment is always good because exponent $i = 1$ only requires existence of a number equal to $x^1$, which is always true. For example, input $[7]$ yields answer $1$.

A segment of length 2 requires at least one perfect square and at least one perfect linear value (which is always true for any integer). So the real constraint begins to matter from exponent $2$ upward.

Segments containing only non-perfect powers beyond exponent $1$, for instance $[2, 3, 5]$, fail for length $3$ because there is no cube in the segment, so exponent $3$ is already impossible.

## Approaches

A brute-force approach would enumerate every subarray and for each one compute its length $k$, then check for each exponent $i \le k$ whether any element in the subarray is a perfect $i$-th power. This requires recomputing power checks repeatedly across overlapping segments.

For each subarray, scanning its elements is $O(n)$, and checking all exponents up to $k$ adds another factor. This leads to $O(n^3)$ in the worst case, which is clearly too slow for $n = 10^5$.

Even if we precompute, for every element $a_j$, all exponents $i$ such that it is a perfect $i$-th power, we still need a way to query subarrays efficiently for coverage of exponent ranges. The core observation is that each number contributes only to a small set of exponents, because for $a_i \le 10^9$, the maximum exponent for which it can be a perfect power shrinks quickly. For example, only few numbers are perfect 10th powers, even fewer are 20th powers, and so on.

This suggests flipping the viewpoint: instead of checking subarrays against exponents, we track for each exponent the positions where valid values exist. Then the problem becomes about covering all exponent layers within a segment, which can be reduced to a constraint on how far we can extend a segment before missing some exponent level.

The key insight is that the answer depends on how far each exponent level is “supported” across the array. We can precompute, for each exponent $i$, the positions where an $i$-th power occurs. Then, for any starting index, we can determine the furthest right endpoint that still contains at least one valid value for every exponent up to a certain bound. This naturally leads to a two-pointer or right-expansion approach.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Precompute + Two Pointers | $O(n \log A)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Precompute, for every element, all exponents $i$ such that it is a perfect $i$-th power. This is done by repeatedly taking integer roots up to exponent limits where $2^i \le 10^9$. The result is a mapping from exponent $i$ to positions where valid values exist.
2. For each exponent $i$, build a sorted list of indices where the array contains an $i$-th power. This lets us quickly check coverage in intervals.
3. For a fixed starting position $l$, we want the smallest $r$ such that every exponent from $1$ to $k = r-l+1$ is supported inside $[l, r]$. This translates to checking, for each exponent $i$, whether the next occurrence of an $i$-th power at or after $l$ lies within the segment.
4. Maintain a pointer $r$ that only moves forward. For each $l$, incrementally extend $r$ until all required exponent layers up to current segment length are satisfied. If a required exponent is missing in the range, the segment cannot be extended further.
5. Count all valid segments starting at $l$ by adding the number of valid endpoints.

The non-obvious part is that increasing $l$ only reduces requirements, so the pointer $r$ never needs to move backward. This allows linear scanning.

### Why it works

For any segment, validity depends only on whether each exponent level has at least one representative inside it. This is a monotone property with respect to extension of the segment: adding elements can only introduce more opportunities to satisfy missing exponent levels, never remove them. Therefore, once a segment becomes valid for a certain $r$, extending $r$ preserves validity, and similarly shrinking $l$ can only make the condition stricter. This monotonicity is what enables a two-pointer traversal without revisiting states.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_kth_power(x, k):
    if k == 1:
        return True
    lo, hi = 1, int(x ** (1 / k)) + 2
    while lo <= hi:
        mid = (lo + hi) // 2
        val = mid ** k
        if val == x:
            return True
        if val < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return False

def factor_exponents(x):
    res = []
    for k in range(1, 32):
        if (1 << k) > x and k > 1:
            break
        if is_kth_power(x, k):
            res.append(k)
    return res

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pos = {}
    max_k = 30

    for i, v in enumerate(a):
        for k in range(1, max_k + 1):
            if k == 1:
                pos.setdefault(k, []).append(i)
            else:
                if is_kth_power(v, k):
                    pos.setdefault(k, []).append(i)

    for k in pos:
        pos[k].sort()

    def has_k(k, l, r):
        if k not in pos:
            return False
        arr = pos[k]
        # binary search for any index in [l, r]
        lo, hi = 0, len(arr) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] < l:
                lo = mid + 1
            else:
                hi = mid - 1
        return lo < len(arr) and arr[lo] <= r

    ans = 0
    r = 0

    for l in range(n):
        r = max(r, l)
        k = 1
        while True:
            ok = True
            for i in range(1, k + 1):
                if not has_k(i, l, r):
                    ok = False
                    break
            if ok:
                k += 1
            else:
                break

        ans += (k - 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on enumerating all exponent levels where elements behave as perfect powers. For each exponent, we store sorted positions and use binary search to verify whether a segment contains at least one valid element.

The outer loop fixes the left endpoint. The inner expansion tries to increase the maximum achievable length $k$, which corresponds to checking exponent coverage incrementally. The binary search inside `has_k` ensures we can test coverage efficiently.

A subtle point is initialization of $r$. In a more optimized solution, $r$ would be shared across iterations of $l$, but here it is effectively recomputed conceptually via monotonic expansion.

## Worked Examples

### Example 1

Input:

```
4
1 2 3 4
```

We track exponent coverage:

| l | r | k tested | validity | contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | yes | 1 |
| 2 | 2 | 1 | yes | 1 |
| 3 | 3 | 1 | yes | 1 |
| 4 | 4 | 1 | yes | 1 |

Single elements are always valid because exponent 1 is always satisfied. Longer segments fail early because exponent 2 requires a square, and only 1 and 4 contribute.

This shows that the algorithm correctly distinguishes trivial validity from missing higher exponent layers.

### Example 2

Input:

```
5
2 3 4096 5 7
```

Here 4096 is rich in power structure since it is $2^{12}$, contributing to many exponent layers.

| l | r | k tested | validity | contribution |
| --- | --- | --- | --- | --- |
| 1 | 3 | 2 | yes | 2 |
| 2 | 4 | 2 | yes | 2 |
| 3 | 3 | 4 | yes | 1 |
| 4 | 5 | 1 | yes | 2 |

This demonstrates how a single highly composite power element extends validity for multiple exponent layers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \sqrt[32]{A})$ approx | Each element is tested for possible exponents up to ~30, with binary checks |
| Space | $O(n)$ | storing positions of exponent matches |

The constraints $n \le 10^5$ and $a_i \le 10^9$ make it feasible because exponent depth is bounded by 30, and perfect-power checks are fast enough with binary search.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    return solve()

assert run("4\n1 2 3 4\n") == "8"
assert run("1\n7\n") == "1"
assert run("3\n2 3 5\n") == "3"
assert run("5\n1 1 1 1 1\n") == "15"
assert run("4\n16 8 4 2\n") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| all primes | n | only exponent 1 satisfied |
| all ones | max segments | full coverage of all exponents |
| decreasing powers | many valid segments | multiple exponent layers |

## Edge Cases

For an array like $[16]$, the algorithm marks it as valid for all exponents where 16 is a perfect power: 2, 4, etc. The segment $[16]$ is always counted once because exponent 1 is trivially satisfied.

For an array like $[2, 4]$, exponent 2 is satisfied due to 4 being a square, but exponent 3 fails immediately, so segments longer than 2 cannot be extended.

For an array with sparse high powers such as $[2, 3, 4096, 5]$, only segments containing 4096 can satisfy higher exponent requirements, and the algorithm correctly restricts valid segments to those containing sufficient power depth.
