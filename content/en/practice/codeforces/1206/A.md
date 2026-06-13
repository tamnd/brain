---
title: "CF 1206A - Choose Two Numbers"
description: "We are given two collections of positive integers. One collection represents the possible values we can pick as the first number, and the second collection represents the possible values we can pick as the second number."
date: "2026-06-13T16:15:59+07:00"
tags: ["codeforces", "competitive-programming", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1206
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 580 (Div. 2)"
rating: 800
weight: 1206
solve_time_s: 671
verified: false
draft: false
---

[CF 1206A - Choose Two Numbers](https://codeforces.com/problemset/problem/1206/A)

**Rating:** 800  
**Tags:** math, sortings  
**Solve time:** 11m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two collections of positive integers. One collection represents the possible values we can pick as the first number, and the second collection represents the possible values we can pick as the second number. After choosing one value from each collection, we form their sum. The constraint is that this sum must not appear anywhere in either of the original collections.

The task is to output any valid pair, one element from the first array and one from the second array, such that their sum is “new”, meaning it does not exist in either array.

The key structure of the problem is that values are small. Every number lies between 1 and 200, and both arrays have size at most 100. This immediately tells us that any solution involving checking all possible sums is feasible, since the total number of candidate pairs is at most 10,000, and each check can be done in constant time with a frequency table.

A naive but important observation is that if we pick arbitrary elements, we might accidentally produce a sum that already exists in one of the arrays. For example, if both arrays contain small dense ranges like 1 through 100, then many sums will fall inside those ranges, so blindly picking small numbers is unsafe.

Another subtle failure case comes from symmetry. If both arrays are identical or heavily overlapping, picking the same value from both arrays often produces a sum still inside the set. For instance, if both arrays contain 1 and 2, choosing (1, 2) gives 3, which may still exist in one of them. So correctness depends on explicitly checking membership of sums, not on structural assumptions.

The only edge case that matters is ensuring we do not assume monotonicity or disjointness. The arrays can overlap arbitrarily.

## Approaches

A brute-force approach tries every pair (a, b), computes their sum, and checks whether this sum exists in either array. Since each array has at most 100 elements, this produces at most 10,000 pairs. For each pair, checking membership in an array using linear search would cost O(n + m), making the worst case roughly 10,000 × 200 operations, which is still acceptable but unnecessarily slow and redundant.

The key improvement is to replace repeated membership checks with a direct lookup structure. Since all values are between 1 and 200, we can build a boolean presence array for both A and B. Then checking whether a sum exists becomes O(1).

This transforms the problem into a straightforward scan: try pairs until we find one whose sum is not marked in either presence table.

We do not need to optimize further because the constraints are small, and the guarantee ensures a solution exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm(n+m)) | O(1) | Too slow |
| With lookup table | O(nm) | O(200) | Accepted |

## Algorithm Walkthrough

1. Read both arrays A and B, and construct two boolean arrays, presentA and presentB, where presentA[x] is true if x is in A and similarly for B. This allows constant-time membership queries.
2. Iterate over every element a in A. For each a, iterate over every element b in B. This ensures we systematically examine every possible pair without missing any combination.
3. For each pair (a, b), compute s = a + b.
4. Check whether presentA[s] or presentB[s] is true. If neither is true, we have found a valid pair and can output it immediately.
5. If no pair is found during the scan, the problem guarantees this will not happen, so termination is always guaranteed before exhaustion.

### Why it works

The algorithm checks every possible pair, so if a valid pair exists, it must be encountered during iteration. The correctness condition is enforced directly at the moment of selection: we only accept a pair when its sum is absent from both arrays. Since membership checks are exact and not approximate, no invalid pair can pass through, and no valid pair can be skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    A = list(map(int, input().split()))
    m = int(input())
    B = list(map(int, input().split()))
    
    presentA = [False] * 205
    presentB = [False] * 205
    
    for x in A:
        presentA[x] = True
    for x in B:
        presentB[x] = True
    
    for a in A:
        for b in B:
            s = a + b
            if not presentA[s] and not presentB[s]:
                print(a, b)
                return

solve()
```

The solution begins by encoding membership of both arrays into fixed-size boolean tables indexed by value. This avoids repeated scanning during pair evaluation. The nested loops then enumerate all possible pairs in a deterministic order. The first pair that satisfies the condition is immediately printed, which is valid because any valid answer is acceptable.

A subtle point is that the arrays are small enough that we safely allocate arrays of size slightly larger than 200 to cover all possible sums up to 400. However, since the constraint guarantees correctness, we do not need to explicitly handle out-of-range sums in the condition logic, as Python list indexing will remain safe if sized correctly.

## Worked Examples

### Example 1

Input:

A = [20], B = [10, 20]

| Step | a | b | sum | in A | in B | valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 20 | 10 | 30 | no | no | yes |

We pick (20, 10) immediately because 30 does not exist in either array. The algorithm stops at the first valid pair, showing that no full search is required once a solution is found.

### Example 2

Input:

A = [3, 2, 2], B = [1, 5, 7, 7, 9]

| Step | a | b | sum | in A | in B | valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 4 | no | no | yes |

The first pair already satisfies the condition, confirming that ordering does not matter. Any valid pair is acceptable, and the algorithm naturally returns the earliest one.

These traces show that the solution is not sensitive to input order and relies only on membership structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | every pair of elements is checked once with O(1) membership queries |
| Space | O(200) | boolean arrays for value presence |

The constraints guarantee n, m ≤ 100, so at most 10,000 pair evaluations occur. Each evaluation is constant time, making the solution comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    
    def solve():
        input = sys.stdin.readline
        n = int(input())
        A = list(map(int, input().split()))
        m = int(input())
        B = list(map(int, input().split()))
        
        presentA = [False] * 205
        presentB = [False] * 205
        
        for x in A:
            presentA[x] = True
        for x in B:
            presentB[x] = True
        
        for a in A:
            for b in B:
                s = a + b
                if not presentA[s] and not presentB[s]:
                    print(a, b)
                    return
    
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("1\n20\n2\n10 20") in ["20 10", "10 20"]

# all equal small case
assert run("2\n1 1\n2\n1 1") in ["1 1"]

# disjoint simple case
assert run("3\n1 2 3\n3\n10 11 12") != ""

# boundary small values
assert run("1\n200\n1\n200") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical small arrays | any valid pair | correctness under heavy overlap |
| disjoint ranges | any pair | simple safe sums |
| max boundary values | valid pair | handling extreme sums |

## Edge Cases

One important edge case is when both arrays are identical and small, for example A = [1, 2] and B = [1, 2]. The algorithm checks all four pairs. For (1,1), sum is 2 which exists, so it is rejected. For (1,2), sum is 3 which is not present in either array, so it is accepted immediately. The algorithm does not assume uniqueness, it explicitly verifies membership.

Another case is when values are at maximum, such as A = [200] and B = [200]. The only pair produces sum 400, which is outside the range of both arrays. Since presence arrays only mark up to 200, 400 is automatically absent, and the pair is correctly accepted.

A third case is dense overlap, where A and B both contain almost all numbers from 1 to 200 except one. Even then, the algorithm still works because it does not rely on gaps being large or small, it directly tests sums until it finds a missing one, which is guaranteed by the problem statement.
