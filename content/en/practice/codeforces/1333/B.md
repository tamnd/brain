---
title: "CF 1333B - Kind Anton"
description: "We are given two integer arrays of the same length. The first array starts with very restricted values, each position being either negative one, zero, or positive one. The second array can contain arbitrary integers, potentially very large in magnitude."
date: "2026-06-16T08:38:58+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1333
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 632 (Div. 2)"
rating: 1100
weight: 1333
solve_time_s: 317
verified: false
draft: false
---

[CF 1333B - Kind Anton](https://codeforces.com/problemset/problem/1333/B)

**Rating:** 1100  
**Tags:** greedy, implementation  
**Solve time:** 5m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two integer arrays of the same length. The first array starts with very restricted values, each position being either negative one, zero, or positive one. The second array can contain arbitrary integers, potentially very large in magnitude. The task is to decide whether we can transform the first array into the second using a specific operation that repeatedly modifies elements.

The allowed operation picks two indices with the first strictly before the second, then adds the value of the earlier position into the later position. Importantly, the source position does not change, and the operation can be repeated any number of times, including reusing the same pair.

The key constraint is that influence only flows from left to right. Earlier elements can affect later ones, but never the reverse. This creates a directional propagation system across the array.

The input size allows up to one hundred thousand elements total across all test cases. This immediately rules out any quadratic simulation of operations between pairs of indices, since even a single naive attempt to simulate repeated updates per position would explode far beyond the time limit.

A subtle difficulty appears in understanding what the repeated operation actually enables. Since the same pair can be chosen multiple times, a single nonzero value can be applied repeatedly to later positions, which means the operation is not a one time transfer but a reusable source of influence.

Edge cases that tend to break naive reasoning include situations where a required increase appears early but the only positive source occurs later, for example an array like `[0, 1]` trying to become `[1, 0]`. This is impossible because the positive value is too far right to help the first position. Another failure case is assuming total sums matter. For instance, matching total sums does not guarantee feasibility because operations are directional and do not allow rearranging mass backward.

## Approaches

A brute force interpretation would simulate operations directly. We would repeatedly scan all pairs `(i, j)` and apply updates whenever it seems helpful until no further changes occur or the array matches the target. This approach is correct in principle because it mimics the allowed operations exactly, but each operation can be applied indefinitely and there are O(n^2) pairs, leading to an unbounded or extremely large number of iterations. Even restricting ourselves to a reasonable cap would still not scale to n up to 100000.

The key observation is that the structure of the operation is extremely coarse. Each position in the initial array is either a permanent source of positive influence, negative influence, or neutrality. A value of one means we can repeatedly add one to any later position. A value of minus one means we can repeatedly subtract one from any later position. A zero does nothing.

This turns the entire process into a reachability condition rather than a simulation problem. For each position in the target array, we only need to know whether we have already encountered at least one positive source and at least one negative source in the prefix up to that position. If we ever need to increase a value relative to its initial state, we require access to a positive source in the left prefix. If we need to decrease it, we require a negative source in the left prefix. Once such a source exists, it can be reused infinitely many times, so we never need more than one.

This reduces the problem to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) or worse | O(n) | Too slow |
| Prefix source tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently, scanning from left to right while tracking whether we have seen a positive one or a negative one so far in the original array.

1. Initialize two boolean flags, one indicating whether a positive one has appeared in the prefix and another indicating whether a negative one has appeared.
2. Iterate through each index from left to right. At each position, first update the flags using the value from the original array. If the current element is one, the positive flag becomes true. If it is minus one, the negative flag becomes true. Zero does not change anything.
3. Compare the current values of the two arrays at this position. If the target value is greater than the original value, then we need to increase this position using additions of one, which requires that a positive source already exists in the prefix. If no such source exists, the transformation is impossible.
4. If the target value is smaller than the original value, then we need to decrease it using minus one operations, which requires that a negative source exists in the prefix. If none exists, the transformation is impossible.
5. If neither condition is violated for any index, the transformation is possible.

The crucial point is that we never need to track how many times a source is used, only whether it exists at all in the reachable prefix.

### Why it works

The operation structure makes each nonzero entry in the original array a reusable generator of unit increments or decrements for all later positions. Once a value of one appears at some index i, every position j greater than i can receive arbitrarily many increments from i by repeating the operation. The same holds for minus one as a source of unlimited decrements. Because sources are never consumed, only introduced into the prefix, the only meaningful state is whether at least one source exists on each side.

This reduces all feasibility questions to prefix existence checks, which remain consistent throughout the scan.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        has_pos = False
        has_neg = False
        ok = True
        
        for i in range(n):
            if a[i] == 1:
                has_pos = True
            elif a[i] == -1:
                has_neg = True
            
            if b[i] > a[i]:
                if not has_pos:
                    ok = False
                    break
            elif b[i] < a[i]:
                if not has_neg:
                    ok = False
                    break
        
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The implementation follows the scan described in the algorithm. The flags are updated before checking the feasibility at each index because the current position itself can serve as a source for later indices if it is nonzero.

A common subtle mistake is updating the flags after checking the condition. That would incorrectly prevent a value at position i from being used to satisfy constraints at position i itself when allowed.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [1, -1, 0]
b = [1, 1, -2]
```

We track prefix sources and feasibility step by step.

| i | a[i] | b[i] | has_pos | has_neg | Condition |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | True | False | ok |
| 1 | -1 | 1 | True | True | increase allowed |
| 2 | 0 | -2 | True | True | decrease allowed |

At index 1, the target is larger than the original value, so we need a positive source, which already exists from index 0. At index 2, the target is smaller, so we need a negative source, which appears at index 1. Every requirement is satisfied.

### Example 2

Input:

```
n = 2
a = [1, 0]
b = [1, 41]
```

| i | a[i] | b[i] | has_pos | has_neg | Condition |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | True | False | ok |
| 1 | 0 | 41 | True | False | increase allowed |

Even though the increase is large, the presence of a single positive source is sufficient because it can be applied repeatedly to the second index.

This demonstrates that magnitude does not matter, only the existence of a source does.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | each element is processed once with constant work |
| Space | O(1) extra | only two boolean flags are maintained |

The total complexity across all test cases is linear in the total input size, which fits easily within the constraints of up to one hundred thousand elements.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        has_pos = False
        has_neg = False
        ok = True
        
        for i in range(n):
            if a[i] == 1:
                has_pos = True
            elif a[i] == -1:
                has_neg = True
            
            if b[i] > a[i] and not has_pos:
                ok = False
                break
            if b[i] < a[i] and not has_neg:
                ok = False
                break
        
        print("YES" if ok else "NO")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    sys.stdin = old_stdin
    return out.getvalue().strip()

# provided samples
assert run("""5
3
1 -1 0
1 1 -2
3
0 1 1
0 2 2
2
1 0
1 41
2
-1 0
-1 -41
5
0 1 -1 1 -1
1 1 -1 1 -1
""") == """YES
NO
YES
YES
NO"""

# custom cases
assert run("""1
1
0
5
""") == "NO", "no source cannot increase"

assert run("""1
3
1 0 0
1 100 100
""") == "YES", "single positive enables unlimited increases"

assert run("""1
3
0 -1 0
0 -5 -5
""") == "YES", "negative source enables decreases"

assert run("""1
3
0 1 0
-1 1 0
""") == "NO", "negative needed before it appears"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero target increase | NO | no source available |
| single positive source large increase | YES | unbounded reuse of +1 |
| negative propagation | YES | -1 enables arbitrary decreases |
| ordering dependency failure | NO | prefix constraint enforcement |

## Edge Cases

A common edge case is when a required operation depends on a source that appears later in the array. For example, if the first position requires a decrease but the first minus one appears only after it, the transformation fails even though a global negative exists. The algorithm correctly rejects this because the prefix flag is still false at the time of evaluation.

Another subtle case is when all elements of the initial array are zero. Since zeros cannot generate any change, any target array different from the initial one immediately fails, which is correctly captured by the absence of both flags throughout the scan.

A third case is when only one type of source exists. If the array contains only ones, any required decrease is impossible regardless of future structure, and the scan immediately detects this when a negative requirement appears without a prefix negative.
