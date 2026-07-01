---
title: "CF 104012A - Absolutely Flat"
description: "We are given four numbers representing the current lengths of the legs of a table. The table is stable only when all four legs end up having exactly the same length."
date: "2026-07-02T05:06:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104012
codeforces_index: "A"
codeforces_contest_name: "2022-2023 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104012
solve_time_s: 39
verified: true
draft: false
---

[CF 104012A - Absolutely Flat](https://codeforces.com/problemset/problem/104012/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four numbers representing the current lengths of the legs of a table. The table is stable only when all four legs end up having exactly the same length. There is also a single pad of fixed length that can be attached to at most one leg, increasing that leg’s length by that amount, or it can be ignored entirely.

The task is to determine whether, after optionally applying this pad once to exactly one of the four legs, it is possible for all four leg lengths to become equal.

The constraints are very small, with each value at most 100. This immediately rules out any need for heavy computation. Even checking all possibilities directly is trivial since there are only five meaningful states: no operation, or applying the pad to one of four legs.

There are no hidden performance concerns. The main difficulty is logical completeness, ensuring we correctly consider both the “already flat” case and the “needs one adjustment” case.

A subtle edge case appears when multiple legs already share the maximum value and the pad is used incorrectly to overshoot. For example, if the legs are already equal, any unnecessary use of the pad breaks equality, but since we are allowed to not use it, the correct answer remains possible.

Another corner situation is when applying the pad creates equality even if no subset of original values was equal before. For instance, transforming a smaller leg to match the current maximum.

## Approaches

The brute-force approach tries every possible action explicitly. We either do nothing, or we choose one of the four legs and add the pad length to it. For each resulting configuration, we check whether all four values are equal. Since there are only five configurations total, this is constant time work.

The correctness of brute force comes from exhaustiveness. Every valid solution must correspond to exactly one of these five states.

However, thinking in terms of “try all operations” is slightly indirect. A cleaner observation is that after the operation, the final value must be some common target value. That target is either the original maximum (if we do not increase anything beyond it), or a value formed by increasing one of the smaller legs to match a higher one.

So instead of enumerating actions, we can reason about feasibility of reaching a single uniform value. The only candidates worth checking are the current maximum and values formed by increasing each leg by b.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all operations) | O(1) | O(1) | Accepted |
| Target checking (optimal reasoning) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We simplify the problem into checking whether we can make all four numbers equal after at most one increment operation applied to a single element.

1. Read the four leg lengths and the pad length. We keep them as a small list for convenience.
2. Compute the maximum value among the four legs. If all legs are already equal, this maximum is the final target, and we can immediately return success without using the pad.
3. Try the “no operation” case first. If all four values are already equal, we return success immediately. This avoids unnecessary reasoning about modifications.
4. Now consider using the pad on each of the four legs one by one. For each index, temporarily add the pad length to that leg and check whether all four values become equal.
5. If any of these four modifications produces equality across all legs, we can return success.
6. If none of the five configurations works, conclude that making the table flat is impossible.

### Why it works

Any valid final configuration must come from either doing nothing or applying the pad to exactly one leg. There is no other transformation allowed, so the solution space is completely covered by these five states. Since we explicitly check each state, we cannot miss a valid construction, and since we directly verify equality each time, we cannot accept an invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok(a):
    return a[0] == a[1] == a[2] == a[3]

a = [int(input()) for _ in range(4)]
b = int(input())

if ok(a):
    print(1)
    sys.exit(0)

for i in range(4):
    brr = a[:]
    brr[i] += b
    if ok(brr):
        print(1)
        sys.exit(0)

print(0)
```

The implementation mirrors the direct state enumeration. The helper function checks equality across all four legs, which is the only condition required for success.

We explicitly test the unchanged configuration first, which is necessary because using the pad is optional. Then we simulate applying the pad to each leg independently. Copying the array each time ensures we do not accidentally accumulate multiple applications, which would violate the “single pad” constraint.

Since the input size is constant, simplicity is more valuable than micro-optimizations.

## Worked Examples

### Example 1

Input:

```
1 1 1 1
2
```

| Step | Array state | Action | All equal? |
| --- | --- | --- | --- |
| 1 | [1,1,1,1] | no operation | yes |

This shows the simplest case where no modification is needed. The algorithm immediately succeeds in the first check.

### Example 2

Input:

```
1 2 2 2
1
```

| Step | Array state | Action | All equal? |
| --- | --- | --- | --- |
| 1 | [1,2,2,2] | no operation | no |
| 2 | [2,2,2,2] | add pad to first leg | yes |

This demonstrates the key intended transformation: one smaller leg is increased exactly to match the others, producing a uniform configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only five configurations are checked, each requiring constant comparisons |
| Space | O(1) | Only a fixed-size array of four elements is stored |

The constraints are extremely small, so constant-time simulation is sufficient with large safety margin.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a = [int(input()) for _ in range(4)]
    b = int(input())

    def ok(a):
        return a[0] == a[1] == a[2] == a[3]

    if ok(a):
        return "1"

    for i in range(4):
        brr = a[:]
        brr[i] += b
        if ok(brr):
            return "1"

    return "0"

# provided samples (illustrative since exact samples not given)
assert run("1\n1\n1\n1\n2\n") == "1", "already equal"
assert run("1\n2\n2\n2\n1\n") == "1", "one pad fixes mismatch"

# custom cases
assert run("1\n2\n3\n4\n10\n") == "0", "no possible equalization"
assert run("5\n5\n5\n4\n1\n") == "1", "pad fixes last leg"
assert run("10\n10\n10\n10\n1\n") == "1", "already flat dominates"
assert run("1\n1\n1\n2\n1\n") == "1", "pad on second case works"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 1 | already-flat detection |
| mixed, fixable | 1 | single-leg correction |
| no solution | 0 | impossible configurations |
| near-uniform | 1 | boundary adjustment cases |

## Edge Cases

One edge case is when the table is already flat. For input like `3 3 3 3`, the algorithm returns success immediately without trying unnecessary modifications. The equality check catches this before any simulation.

Another case is when applying the pad would overshoot equality if applied to the wrong leg. For `2 2 2 2` with `b = 1`, applying the pad to any leg produces a mismatch, but since we also check the “do nothing” case first, we still correctly return success.

A third case is when only one leg is smaller and exactly matches the others after adding the pad, such as `4 4 4 1` with `b = 3`. The loop correctly tests each index and finds the valid transformation when applying to the last leg, confirming that single-operation coverage is sufficient.
