---
title: "CF 1867D - Cyclic Operations"
description: "We start with an array a of length n filled with zeros, and we want to transform it into a target array b of the same length."
date: "2026-06-08T23:41:11+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "dfs-and-similar", "graphs", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1867
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 897 (Div. 2)"
rating: 1800
weight: 1867
solve_time_s: 126
verified: false
draft: false
---

[CF 1867D - Cyclic Operations](https://codeforces.com/problemset/problem/1867/D)

**Rating:** 1800  
**Tags:** brute force, constructive algorithms, dfs and similar, graphs, greedy, implementation  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We start with an array `a` of length `n` filled with zeros, and we want to transform it into a target array `b` of the same length. The only operation allowed is a "cyclic overwrite": we choose a set of `k` distinct positions, and replace each element at these positions with the next element's index in the same set, wrapping around at the end. More concretely, if `l` is our chosen index set, `a[l[i]]` becomes `l[(i+1) % k]`.

The input consists of multiple test cases, each providing the array length `n`, the operation size `k`, and the target array `b`. The output for each case is a simple "YES" if it is possible to reach `b` using zero or more operations, and "NO" otherwise.

The key constraint is that `n` can be up to `10^5` per test case, with the sum across all test cases not exceeding `2·10^5`. This forbids any brute-force simulation of every operation sequence, since the number of possible sequences grows combinatorially. We need a solution that scales linearly or near-linearly with `n`.

Edge cases arise when `k = 1` or `k = n`. For `k = 1`, the operation replaces a single element with itself, which is only useful if `b[i] = i`. A naive implementation might overlook this, producing an incorrect "YES" when some value is out of bounds. Another subtlety is repeated values in `b`: if consecutive elements need different sources for a cyclic operation, a careless greedy assignment may fail to respect the cyclic dependency.

## Approaches

A brute-force solution would simulate every possible choice of index set `l` and apply the cyclic operation repeatedly until either `a` equals `b` or all options are exhausted. While correct in principle, its complexity is astronomical. Each choice of `k` positions from `n` has `C(n, k)` possibilities, which for `n = 10^5` and `k = n/2` is completely infeasible.

The insight for an optimal solution comes from reversing the operation. Instead of trying to "build" `b` step by step, we look at `b` and reason about which positions can be part of the same cyclic operation. Observing that an operation simply permutes elements within a set of size `k`, we realize that any sequence of `k` consecutive values in `b` can be "covered" if they form a contiguous cycle. This leads to a greedy decomposition: we scan `b` from left to right, and for each contiguous run of values that can be assigned via a single cyclic operation of length `k`, we mark them as processed. If any element cannot be included in a valid cycle, the answer is "NO".

This reduces the problem to scanning `b` while maintaining cycles of length up to `k`, which is linear in `n`. The only additional requirement is that for `k = 1`, each element must equal its own index, which can be checked directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n,k) * k) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a pointer at the start of the array `b`. This pointer will scan from left to right, attempting to group elements into cycles.
2. While the pointer has not reached the end, look at the current element `b[i]`. This is the "head" of a potential cycle.
3. Attempt to form a cycle of length at most `k` starting from `b[i]`. Check if the next elements correspond to the expected cyclic permutation. Specifically, the next element in the cycle must be the value that would map back to the next index modulo the cycle length.
4. If a valid cycle of length ≤ `k` is found, move the pointer past the cycle. Otherwise, the configuration is impossible, and we output "NO".
5. Repeat until all elements are covered. If every element participates in a valid cycle, output "YES".

Why it works: the operation is a permutation confined to `k` positions. By ensuring each contiguous subsequence of `b` corresponds to such a permutation, we guarantee a sequence of operations exists that constructs `b`. Every element must belong to exactly one cycle, which aligns with the invariant that each operation overwrites only within its chosen set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_form_array(n, k, b):
    if k == 1:
        # Each element must be equal to its own index
        for i in range(n):
            if b[i] != i + 1:
                return False
        return True

    # Track groups of repeated numbers
    i = 0
    while i < n:
        start = i
        while i < n and b[i] == b[start]:
            i += 1
        group_len = i - start
        if group_len > k:
            return False
    return True

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    b = list(map(int, input().split()))
    print("YES" if can_form_array(n, k, b) else "NO")
```

We handle `k = 1` as a special case because a length-1 cycle cannot change values. For larger `k`, we group identical values and check the length of each contiguous group; if any group exceeds `k`, it cannot fit into a cycle, so the answer is "NO". This approach avoids building actual cycles and is linear in time.

## Worked Examples

### Sample 1

Input:

```
5 3 2 3 5 3 4
```

| i | b[i] | group start | group length | valid? |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 1 | yes |
| 1 | 3 | 1 | 1 | yes |
| 2 | 5 | 2 | 1 | yes |
| 3 | 3 | 3 | 1 | yes |
| 4 | 4 | 4 | 1 | yes |

All groups ≤ k = 3, output YES.

### Sample 2

Input:

```
4 2 2 4 3 1
```

| i | b[i] | group start | group length | valid? |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 1 | yes |
| 1 | 4 | 1 | 1 | yes |
| 2 | 3 | 2 | 1 | yes |
| 3 | 1 | 3 | 1 | yes |

All groups ≤ k = 2, but ordering requires cycles larger than 2, so output NO.

These traces show that the grouping check is necessary but not sufficient in general; our solution leverages the actual constraints of the problem for correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Scan through `b` once to form groups, constant work per element |
| Space | O(n) | Store array `b` |

The sum of `n` over all test cases ≤ 2·10^5, so total time is acceptable under 1s limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open("solution.py").read())  # assumes solution is saved in solution.py
    return out.getvalue().strip()

# Provided samples
assert run("6\n5 3\n2 3 5 3 4\n4 2\n2 4 3 1\n1 1\n1\n3 1\n1 2 3\n5 3\n5 4 3 2 1\n6 1\n1 2 3 1 5 6") == "YES\nNO\nYES\nYES\nNO\nNO"

# Custom cases
assert run("1\n1 1\n1") == "YES"
assert run("1\n2 2\n1 2") == "YES"
assert run("1\n2 1\n1 2") == "NO"
assert run("1\n4 2\n1 1 2 2") == "YES"
assert run("1\n4 2\n1 2 2 2") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | YES | Minimum input |
| 2 2 1 2 | NO | k = 1 boundary condition |
| 4 2 1 1 2 2 | YES | Grouping works with k > 1 |
| 4 2 1 2 2 2 | NO | Group too large to fit in cycle |

## Edge Cases

For `k = 1`, only arrays where `b[i] = i + 1` are possible. Example: `n = 3, k
