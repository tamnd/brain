---
title: "CF 105380A - Who Hates Abhishek?"
description: "We are asked to construct a special kind of permutation of size n. A permutation here means we arrange the numbers from 1 to n exactly once each. The twist is that the permutation must behave like an involution without fixed points."
date: "2026-06-23T16:05:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105380
codeforces_index: "A"
codeforces_contest_name: "TSEC Round 1 (Div. 4)"
rating: 0
weight: 105380
solve_time_s: 64
verified: true
draft: false
---

[CF 105380A - Who Hates Abhishek?](https://codeforces.com/problemset/problem/105380/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a special kind of permutation of size `n`. A permutation here means we arrange the numbers from `1` to `n` exactly once each.

The twist is that the permutation must behave like an involution without fixed points. In other words, if we look at the value at position `j`, call it `a[j]`, then applying the same mapping again brings us back: `a[a[j]] = j`. At the same time, no position is allowed to map to itself, so `a[j] != j` for every `j`.

This structure forces every index to be paired with exactly one other index. If `a[x] = y`, then automatically `a[y] = x`, and neither `x` nor `y` can be equal. So the permutation is entirely made of disjoint 2-cycles.

The input size `n` can be as large as `100000`, so any solution must run in linear time. A quadratic or even $O(n \log n)$ construction is fine, but anything involving repeated searching or matching would be unnecessary and risky.

A key edge case appears when `n` is odd. If every element must belong to a pair, an odd number of elements leaves one index unpaired. That makes the condition impossible to satisfy.

For example, when `n = 3`, we would need pairs like `(1, 2)` and `(3, ?)`, but there is no partner left for `3`. Any attempt will force a fixed point or break the bijection requirement.

So the real difficulty is not constructing the permutation when possible, but recognizing when the structure is impossible.

## Approaches

A naive attempt would be to try building the permutation by tracking which positions are already used. We could iterate through indices from `1` to `n`, and for each unused index `i`, search for another unused index `j` and set `a[i] = j`, `a[j] = i`. This guarantees correctness because we explicitly enforce the conditions.

The issue is performance. For each index, we may scan through the remaining unused indices to find a partner. In the worst case, this becomes approximately $n + (n-1) + (n-2) + \cdots$, which is $O(n^2)$. With `n = 100000`, this is far beyond feasible limits.

The key observation is that the condition `a[a[j]] = j` and `a[j] != j` forces the permutation to be a perfect matching over indices. We do not need to search for partners dynamically. We only need to ensure every element is paired with exactly one other element.

Once we accept that interpretation, the construction becomes immediate: if we list numbers in order and swap adjacent pairs, we automatically create valid 2-cycles. Each pair `(1,2)`, `(3,4)`, `(5,6)`, and so on satisfies both conditions. The mapping is symmetric, and no element maps to itself.

If `n` is odd, one element is left unpaired, so no valid construction exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching | O(n²) | O(n) | Too slow |
| Adjacent Swapping | O(n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Check whether `n` is odd. If it is, immediately output `-1`. This is because pairing requires groups of size exactly 2, and an odd count makes full pairing impossible.
2. Initialize an array `a` of size `n + 1` (using 1-based indexing for convenience).
3. Iterate over indices `i` from `1` to `n` in steps of `2`.
4. For each pair `(i, i+1)`, assign `a[i] = i+1` and `a[i+1] = i`. This creates a mutual mapping between adjacent elements.
5. After processing all indices, output the array from `1` to `n`.

The reason we step by 2 is that each operation consumes exactly two unused indices, and we guarantee no overlap between pairs.

### Why it works

The constructed permutation is a disjoint union of 2-cycles. Each index `i` is assigned exactly one partner `i+1` or `i-1`, so the mapping is bijective. Applying the permutation twice returns to the original index because swapping twice restores the original position: `a[a[i]] = i`. Since no element is ever mapped to itself, the fixed-point condition is also satisfied. There is no interaction between different pairs, so the property holds globally.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    if n % 2 == 1:
        print(-1)
        return
    
    a = list(range(n + 1))
    
    for i in range(1, n + 1, 2):
        a[i], a[i + 1] = i + 1, i
    
    print(*a[1:])

if __name__ == "__main__":
    solve()
```

The solution first handles the impossibility condition by checking parity. This is the only case where we can fail.

The array is initialized with a dummy zero index so that 1-based indexing matches the problem definition. This avoids repeated index adjustments and reduces off-by-one risk.

The loop swaps adjacent indices in constant time per pair. Each iteration finalizes two positions permanently, so no additional bookkeeping is needed.

Finally, printing `a[1:]` removes the dummy slot and outputs the permutation.

## Worked Examples

### Example 1: `n = 6`

We start with an array `[1, 2, 3, 4, 5, 6]`.

| i | Operation | Array state |
| --- | --- | --- |
| 1 | swap (1,2) | [2, 1, 3, 4, 5, 6] |
| 3 | swap (3,4) | [2, 1, 4, 3, 5, 6] |
| 5 | swap (5,6) | [2, 1, 4, 3, 6, 5] |

The final permutation satisfies `a[a[i]] = i` because each pair is symmetric, and no element remains fixed.

### Example 2: `n = 4`

Start `[1, 2, 3, 4]`.

| i | Operation | Array state |
| --- | --- | --- |
| 1 | swap (1,2) | [2, 1, 3, 4] |
| 3 | swap (3,4) | [2, 1, 4, 3] |

Each element is paired exactly once, confirming the structure works for even `n`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each index is visited once and swapped once |
| Space | O(1) extra | aside from output array, only a few variables are used |

The construction is linear, so it comfortably handles `n = 100000`. Memory usage is also minimal since we only store the permutation itself.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    # embedded solution
    def solve():
        n = int(sys.stdin.readline().strip())
        if n % 2 == 1:
            print(-1)
            return
        a = list(range(n + 1))
        for i in range(1, n + 1, 2):
            a[i], a[i + 1] = i + 1, i
        print(*a[1:])

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided samples
assert run("6\n") == "2 1 4 3 6 5", "sample 1"
assert run("4\n") == "2 1 4 3", "sample 2"

# custom cases
assert run("1\n") == "-1", "minimum odd case"
assert run("2\n") == "2 1", "minimum even case"
assert run("3\n") == "-1", "small odd impossibility"
assert run("10\n") == "2 1 4 3 6 5 8 7 10 9", "larger even case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | -1 | smallest impossible case |
| 2 | 2 1 | smallest valid swap |
| 3 | -1 | odd-length failure |
| 10 | paired swaps | correctness on larger even input |

## Edge Cases

When `n = 1`, there is no possible partner for the single element. The algorithm immediately returns `-1`, matching the requirement that no fixed points are allowed.

When `n = 2`, the loop runs once and swaps positions `1` and `2`, producing `[2, 1]`. Checking manually, `a[a[1]] = a[2] = 1` and similarly for index `2`, confirming correctness.

When `n` is any odd number like `5`, the algorithm detects the parity before any construction begins. For `n = 5`, returning `-1` avoids attempting a partial pairing like `(1,2)`, `(3,4)` which would leave index `5` unpaired and force a fixed point or invalid mapping.
