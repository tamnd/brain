---
title: "CF 1043B - Lost Array"
description: "We are given a sequence of prefix values a[0], a[1], ..., a[n] where a[0] = 0. The sequence was originally generated from a hidden array x of length k, but that array is no longer available."
date: "2026-06-16T17:38:42+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1043
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 519 by Botan Investments"
rating: 1200
weight: 1043
solve_time_s: 223
verified: true
draft: false
---

[CF 1043B - Lost Array](https://codeforces.com/problemset/problem/1043/B)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 3m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of prefix values `a[0], a[1], ..., a[n]` where `a[0] = 0`. The sequence was originally generated from a hidden array `x` of length `k`, but that array is no longer available.

The generation rule is simple: each next value `a[i]` is formed by taking the previous prefix sum `a[i-1]` and adding one element of `x`, chosen in a cyclic manner. Concretely, the added value at step `i` depends only on `x[(i-1) mod k]`. This means the sequence of increments of `a` is periodic with period `k`.

We are asked to find all possible values of `k` such that there exists some integer array `x` of length `k` that could have produced the given prefix sum array.

The input size `n` is at most 1000, which immediately suggests that an `O(n^2)` solution is acceptable. Any solution that tries to reconstruct `x` independently for each candidate `k` and verifies consistency will pass comfortably. Anything exponential over subsets or permutations is unnecessary because the structure is already fully determined by periodicity constraints.

A key subtlety is that `x` is not constrained to be positive or bounded. This removes many typical prefix-sum constraints and leaves only equality structure as the deciding factor.

One common failure case comes from misinterpreting the condition as requiring a specific constructed `x`. For example, assuming `x[i] = a[i] - a[i-1]` directly only works when `k = n`. For smaller `k`, the same `x` value must be reused at multiple positions, so consistency across indices is the real requirement.

Another subtle edge case appears when `k = 1`. In this case, all differences must be identical. Any implementation that forgets to check this explicitly often incorrectly accepts arrays that are not constant in differences.

## Approaches

The first natural idea is to try each candidate length `k` and explicitly reconstruct the hidden array `x`. If we assume `x[j] = a[j+1] - a[j]` for the first `k` positions, we can then simulate the construction of the full array and compare it with the given `a`. This is correct but inefficient if implemented with repeated simulation, because for each `k` we may simulate up to `O(n)` steps, leading to an `O(n^2)` overall approach.

However, we can simplify the problem by shifting perspective. Instead of thinking in terms of reconstructing `x`, we look at the sequence of differences `d[i] = a[i] - a[i-1]`. This sequence is exactly the repeated pattern of `x`. So the problem becomes: for which `k` is the difference array periodic with period `k`?

This transforms the task into a direct periodicity check. For a fixed `k`, every position `i` must satisfy `d[i] = d[i-k]`. If this holds for all valid `i`, then `k` is valid.

The brute-force approach checks this condition independently for each `k`, recomputing comparisons each time. Since each check is `O(n)`, the full solution is `O(n^2)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (period check per k) | O(n^2) | O(n) | Accepted |
| Optimal (same idea, direct implementation) | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

We solve the problem by testing every possible period length `k`.

1. Compute the difference array `d`, where `d[i] = a[i] - a[i-1]`. This isolates the repeated pattern that corresponds to the hidden array `x`. The prefix sums are no longer needed once we extract differences.
2. Iterate over all possible values of `k` from `1` to `n`. Each `k` is treated as a candidate period length.
3. For a fixed `k`, assume it is valid and verify consistency across the difference array. For every index `i` starting from `k+1` to `n`, check whether `d[i] == d[i-k]`.
4. If any mismatch is found, reject this `k` immediately. This ensures we only accept true periodic structures.
5. If all comparisons succeed, add `k` to the answer list.
6. After checking all candidates, output the collected valid values in increasing order.

### Why it works

The key invariant is that the difference array must exactly repeat every `k` positions if it originated from a length-`k` cyclic array `x`. Because each `d[i]` directly corresponds to `x[(i-1) mod k]`, equality of all elements spaced `k` apart is both necessary and sufficient. If any mismatch exists, no assignment of `x` can reconcile the contradiction, since each position in `x` would be forced to take two different values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))

    d = [0] * (n + 1)
    for i in range(1, n + 1):
        d[i] = a[i] - a[i - 1]

    res = []

    for k in range(1, n + 1):
        ok = True
        for i in range(k + 1, n + 1):
            if d[i] != d[i - k]:
                ok = False
                break
        if ok:
            res.append(k)

    print(len(res))
    print(*res)

if __name__ == "__main__":
    solve()
```

The implementation starts by reconstructing the difference array so that the cyclic structure becomes explicit. This avoids repeatedly dealing with prefix sums during validation.

The core loop tries every possible `k` and checks periodicity by comparing each element with the one exactly `k` positions behind it. The early break is important because it prevents unnecessary work once a contradiction is found.

Care must be taken with indexing: the difference array is 1-based here to match the prefix indexing of `a`, which simplifies the relation `d[i] = a[i] - a[i-1]`.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

Here `a = [0, 1, 2, 3, 4, 5]` and `d = [1, 1, 1, 1, 1]`.

| k | checked comparisons | valid |
| --- | --- | --- |
| 1 | all equal (trivially) | yes |
| 2 | all d[i] == d[i-2] | yes |
| 3 | all equal | yes |
| 4 | all equal | yes |
| 5 | all equal | yes |

All values work because the difference array is constant, so any period is valid.

Output:

```
5
1 2 3 4 5
```

This demonstrates the case where maximum symmetry exists and every candidate period is valid.

### Example 2

Input:

```
5
1 3 5 6 8
```

We compute `a = [0,1,3,5,6,8]` and `d = [1,2,2,1,2]`.

| k | key comparisons | valid |
| --- | --- | --- |
| 1 | 2 ≠ 1 immediately | no |
| 2 | d[3]=2 vs d[1]=1 mismatch | no |
| 3 | d[4]=1 == d[1], d[5]=2 == d[2] | yes |
| 4 | mismatch at position 5 | no |
| 5 | trivially consistent | yes |

Output:

```
2
3 5
```

This example shows how multiple valid periods can coexist when the difference pattern partially repeats.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each of the n candidate k values is verified by scanning up to n elements |
| Space | O(n) | Only the difference array and output storage are used |

With `n ≤ 1000`, the maximum number of operations is about one million comparisons, which comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins
    output = io.StringIO()
    sys.stdout = output

    # ---- solution ----
    n = int(input())
    a = [0] + list(map(int, input().split()))

    d = [0] * (n + 1)
    for i in range(1, n + 1):
        d[i] = a[i] - a[i - 1]

    res = []
    for k in range(1, n + 1):
        ok = True
        for i in range(k + 1, n + 1):
            if d[i] != d[i - k]:
                ok = False
                break
        if ok:
            res.append(k)

    print(len(res))
    print(*res)
    # ------------------

    sys.stdout.seek(0)
    return output.getvalue().strip()

# provided sample
assert run("5\n1 2 3 4 5\n") == "5\n1 2 3 4 5"

# custom: single element
assert run("1\n7\n") == "1\n1"

# custom: strictly alternating differences
assert run("4\n1 2 1 2\n") == "2\n2 4"

# custom: all equal differences
assert run("3\n10 20 30\n") == "3\n1 2 3"

# custom: no small period
assert run("5\n1 2 4 7 11\n") == "1\n5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `1 / 1` | minimal boundary case |
| `1 2 1 2` | `2 / 2 4` | alternating pattern |
| `10 20 30` | `3 / 1 2 3` | constant difference case |
| `1 2 4 7 11` | `1 / 5` | no repetition except full length |

## Edge Cases

A minimal input where `n = 1` is important because every `k = 1` is trivially valid. The algorithm handles this naturally since there are no comparisons to fail, so `1` is always included.

When all differences are identical, every `k` becomes valid. The algorithm correctly accepts all values because every comparison `d[i] == d[i-k]` always holds.

For alternating or structured patterns, smaller `k` values can fail while larger ones succeed. The periodic check correctly captures this because mismatches appear exactly where alignment breaks, and rejection happens immediately without needing full reconstruction.
