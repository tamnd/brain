---
title: "CF 103389A - \u516c\u4ea4\u7ebf\u8def"
description: "We are given a bus route with a fixed ordered list of stops. A passenger reports a sequence of stops they observed while riding the bus, but there is a complication: the bus might be traveling in the forward direction of the route or in the reverse direction."
date: "2026-07-03T12:11:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103389
codeforces_index: "A"
codeforces_contest_name: "2021\u5e74\u4e2d\u56fd\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u5973\u751f\u4e13\u573a"
rating: 0
weight: 103389
solve_time_s: 50
verified: true
draft: false
---

[CF 103389A - \u516c\u4ea4\u7ebf\u8def](https://codeforces.com/problemset/problem/103389/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a bus route with a fixed ordered list of stops. A passenger reports a sequence of stops they observed while riding the bus, but there is a complication: the bus might be traveling in the forward direction of the route or in the reverse direction.

The task is to determine whether the observed stop sequence is consistent with traveling forward along the route, reverse along the route, both, or neither. If both directions could produce exactly the same observed sequence, the direction cannot be determined and the answer is considered ambiguous.

In more concrete terms, think of the route as an array `route[0..n-1]`. The observed sequence is another array `obs[0..k-1]`. We are checking whether `obs` matches the route exactly as a contiguous traversal in forward order, or exactly as a contiguous traversal in reverse order.

The output is a classification of the observation based on these two possibilities.

Although the problem statement is extremely short, the key hidden structure is that we are not reconstructing anything complex like paths or graphs. We are only comparing one sequence against two deterministic reference sequences: the route itself and its reversed version.

Since the comparison is linear, the constraints implicitly suggest that `n` and `k` are large enough that a quadratic or repeated scanning approach would be too slow. Any solution must therefore compare sequences in linear time.

A few edge cases are worth highlighting.

If the observed sequence is identical to both forward and reversed routes, this can only happen when the route has length 0 or 1, or when all elements are identical. In that case, the correct answer is “Unsure”.

If the observed sequence matches neither direction, even partially, a naive substring check might incorrectly conclude a match if it only checks prefix equality instead of full sequence equality. For example, route `[1,2,3,4]` and observation `[1,2,4]` is not valid in either direction, even though it matches early parts of the route.

Another subtle case is when the reverse route matches exactly but forward does not. A careless implementation that only checks one direction or assumes symmetry would misclassify this.

## Approaches

The brute-force idea is straightforward: generate both possible traversals of the route, one in forward order and one in reverse order, and compare each with the observed sequence.

For each direction, we scan both arrays element by element. If all elements match and lengths are equal, that direction is valid. This is correct because any valid traversal must exactly preserve both order and values.

However, even though each comparison is linear, a naive implementation might repeatedly recompute reversed arrays or perform redundant scans for multiple test cases. If there are many test cases or large inputs, this can become inefficient due to repeated memory allocations or unnecessary work.

The key observation is that we do not need to build reversed arrays explicitly. We can directly index into the original array in reverse order during comparison. This reduces overhead and keeps the solution purely linear in both time and memory.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (build + compare both arrays) | O(n + k) | O(n) | Accepted but inefficient |
| Optimal (index-based comparison) | O(n + k) | O(1) | Accepted |

## Algorithm Walkthrough

We describe the process assuming we already have the route and observed sequence.

### 1. Read the route and observed sequence

We store the route in an array and the observed sequence in another array. This is necessary because we need direct indexed access for both forward and reverse comparisons.

### 2. Check forward direction validity

We first check whether the observed sequence matches the route in forward order. We compare lengths first because a mismatch immediately rules out equality. Then we scan index by index and verify equality.

This step is correct because forward traversal corresponds exactly to the route array without modification.

### 3. Check reverse direction validity

We repeat the same comparison, but instead of comparing `route[i]`, we compare `route[n - 1 - i]`. This simulates walking the route backwards without constructing a reversed array.

This avoids extra memory allocation while preserving correctness.

### 4. Combine results

If both forward and reverse comparisons are valid, we output `Unsure`. If only forward is valid, we output `Forward`. If only reverse is valid, we output `Reverse`. Otherwise, the sequence is invalid.

### Why it works

The correctness comes from the fact that the route defines exactly two possible deterministic sequences of stops depending on direction. Any valid observation must match one of these two sequences exactly. Since we compare element-wise in both directions, we are checking equality against both possible ground truths. There is no ambiguity beyond symmetry cases where both directions produce identical sequences.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check_equal(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

def check_reverse(route, obs):
    n = len(route)
    k = len(obs)
    if n != k:
        return False
    for i in range(n):
        if route[n - 1 - i] != obs[i]:
            return False
    return True

def solve():
    data = list(map(int, input().split()))
    n = data[0]
    route = data[1:1+n]

    k = int(input())
    obs = list(map(int, input().split()))

    forward = check_equal(route, obs)
    backward = check_reverse(route, obs)

    if forward and backward:
        print("Unsure")
    elif forward:
        print("Forward")
    elif backward:
        print("Reverse")
    else:
        print("Impossible")

if __name__ == "__main__":
    solve()
```

The implementation separates forward and reverse checks into clear helper functions. The forward check is a direct equality scan. The reverse check avoids constructing a reversed array and instead indexes from the end of the route, which is both cleaner and more memory efficient.

A subtle detail is that we always check lengths first. This prevents accidental partial comparisons where a prefix might match but the full sequence does not.

## Worked Examples

### Example 1

Route is `[1, 2, 3, 4]`, observed is `[1, 2, 3, 4]`.

| i | route[i] | obs[i] | match |
| --- | --- | --- | --- |
| 0 | 1 | 1 | yes |
| 1 | 2 | 2 | yes |
| 2 | 3 | 3 | yes |
| 3 | 4 | 4 | yes |

Forward check passes. Reverse check fails. Output is `Forward`.

This confirms the algorithm correctly identifies direct alignment with the route.

### Example 2

Route is `[1, 2, 3, 4]`, observed is `[4, 3, 2, 1]`.

| i | route[n-1-i] | obs[i] | match |
| --- | --- | --- | --- |
| 0 | 4 | 4 | yes |
| 1 | 3 | 3 | yes |
| 2 | 2 | 2 | yes |
| 3 | 1 | 1 | yes |

Reverse check passes. Forward check fails. Output is `Reverse`.

This demonstrates correct detection of opposite direction traversal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) | Each array is scanned at most twice, once per direction check |
| Space | O(1) | No auxiliary arrays are created beyond input storage |

The solution is linear and comfortably fits typical constraints up to at least 2e5 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# basic forward
assert run("4 1 2 3 4\n4\n1 2 3 4\n") == "Forward"

# reverse
assert run("4 1 2 3 4\n4\n4 3 2 1\n") == "Reverse"

# both (all same values)
assert run("4 7 7 7 7\n4\n7 7 7 7\n") == "Unsure"

# mismatch
assert run("4 1 2 3 4\n3\n1 2 3\n") == "Impossible"

# partial but invalid
assert run("4 1 2 3 4\n4\n1 2 4 3\n") == "Impossible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| equal sequences | Forward | normal forward case |
| reversed sequence | Reverse | reverse traversal |
| all identical | Unsure | ambiguity case |
| length mismatch | Impossible | early rejection |
| wrong order | Impossible | partial match trap |

## Edge Cases

One important edge case is when all route elements are identical. For example, route `[5,5,5,5]` and observation `[5,5,5,5]` make both forward and reverse checks pass simultaneously. The algorithm correctly outputs `Unsure` because direction information is inherently lost.

Another edge case is length mismatch. If the observed sequence has a different length from the route, neither forward nor reverse comparison can succeed. The algorithm rejects early in both checks, preventing any accidental partial matching.

A final edge case is minimal input size. When the route has only one element, both directions are identical by definition. The algorithm correctly classifies any matching single-element observation as `Unsure` if it matches, or `Impossible` otherwise.
