---
title: "CF 1382A - Common Subsequence"
description: "We are given two sequences of integers and asked to extract a third sequence that appears inside both of them in order. “In order” here means we are allowed to delete elements, but we cannot reorder what remains."
date: "2026-06-11T10:51:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1382
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 658 (Div. 2)"
rating: 800
weight: 1382
solve_time_s: 83
verified: false
draft: false
---

[CF 1382A - Common Subsequence](https://codeforces.com/problemset/problem/1382/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two sequences of integers and asked to extract a third sequence that appears inside both of them in order. “In order” here means we are allowed to delete elements, but we cannot reorder what remains.

The task is to find any sequence that is common to both arrays, with the additional requirement that its length must be as small as possible but still non-empty. Since we are minimizing length, the real question becomes whether there exists a common element at all. If there is, a sequence of length one is always optimal, because any single shared value is already a valid subsequence of both arrays and no shorter non-empty sequence exists.

So the entire problem reduces to checking whether the two arrays share at least one integer value. If they do, we output any such value. If they do not, we report that no solution exists.

The constraints are very small: the total number of elements across all test cases is at most 1000. This immediately rules out any need for heavy preprocessing or advanced data structures. Even a direct nested scan would be fast enough, but we can do better conceptually by using membership checks.

A subtle edge case appears when one array has repeated values and the other has none of them. For example, if one array is `[3, 3, 3]` and the other is `[2]`, a careless attempt that assumes “common subsequence” might try to align positions or build longer matches, but the correct answer is simply “NO” because no single value is shared.

Another potential misunderstanding is thinking we need to compute a longest common subsequence or any structured alignment. That would be unnecessary overkill and would also risk incorrect complexity reasoning.

## Approaches

A brute-force way to solve the problem is to try every possible subsequence of the first array and check whether it appears in the second array. Since each array of size up to 1000 has exponentially many subsequences, this approach is completely infeasible. Even generating all single-element subsequences is fine, but extending beyond that explodes combinatorially.

However, we notice something crucial: we are minimizing the length of the subsequence, and any valid solution must have length at least one. If there is any overlap in values between the two arrays, a length-one subsequence is already optimal. If there is no overlap, no longer subsequence can exist either, because any subsequence is composed of elements that must individually appear in both arrays.

This reduces the entire problem to a simple intersection test between two sets of values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(1)-O(n) | Too slow |
| Optimal (set intersection) | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read both arrays.
2. Convert the first array into a set for fast membership queries. This allows O(1) average-time checks for whether a value exists in the first array.
3. Scan through the second array from left to right and check whether each element exists in the set built from the first array.
4. As soon as we find a common element, we output it immediately as a sequence of length one.
5. If we finish scanning without finding any shared value, we output that no solution exists.

The key design choice is stopping immediately on the first match. Since all valid answers of length one are equivalent in optimality, there is no reason to continue searching after finding one.

### Why it works

Any valid common subsequence must consist of elements that appear in both arrays. If there exists any solution, it must contain at least one value that exists in both sequences. Therefore, detecting a single shared value is both necessary and sufficient for feasibility, and choosing it gives the optimal length by definition.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    sa = set(a)
    
    ans = None
    for x in b:
        if x in sa:
            ans = x
            break
    
    if ans is None:
        print("NO")
    else:
        print("YES")
        print(1, ans)
```

The solution relies on converting the first array into a hash set, which enables constant-time membership checks. The second array is scanned in order, and we stop at the first element that appears in the set.

A common mistake is trying to build an explicit subsequence alignment or thinking order constraints matter beyond existence. Here, order only matters for defining subsequences, but since a single element is always order-independent, we never need to reason about positions.

## Worked Examples

### Example 1

Input:

```
a = [10, 8, 6, 4]
b = [1, 2, 3, 4, 5]
```

| Step | Current b element | Set(a) contains? | Action |
| --- | --- | --- | --- |
| 1 | 1 | No | continue |
| 2 | 2 | No | continue |
| 3 | 3 | No | continue |
| 4 | 4 | Yes | stop, output 4 |

We find the first shared element at value 4, so the answer is `[4]`. This confirms that the algorithm does not need to consider deeper structure in the arrays.

### Example 2

Input:

```
a = [3]
b = [2]
```

| Step | Current b element | Set(a) contains? | Action |
| --- | --- | --- | --- |
| 1 | 2 | No | continue |
| end | - | - | no match found |

No element is shared, so the correct output is “NO”. This demonstrates that absence of intersection implies impossibility of any common subsequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | each array is scanned once, set lookup is O(1) average |
| Space | O(n) | storage for the set of first array elements |

Given that total input size across all test cases is at most 1000, this is comfortably within limits. Even with Python overhead, the solution runs in negligible time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        sa = set(a)
        ans = None
        for x in b:
            if x in sa:
                ans = x
                break
        if ans is None:
            out.append("NO")
        else:
            out.append("YES")
            out.append(f"1 {ans}")
    return "\n".join(out)

# provided samples
assert run("""5
4 5
10 8 6 4
1 2 3 4 5
1 1
3
3
1 1
3
2
5 3
1000 2 2 2 3
3 1 5
5 5
1 2 3 4 5
1 2 3 4 5
""") == """YES
1 4
YES
1 3
NO
YES
1 3
YES
1 1"""

# custom cases
assert run("""3
1 1
1
2
1 3
5
5 6 7
2 2
1 2
2 1
""") == """NO
YES
1 5
YES
1 2"""

assert run("""1
5 5
1 2 3 4 5
6 7 8 9 10
""") == """NO"""

assert run("""1
4 4
9 9 9 9
9 1 2 3
""") == """YES
1 9"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no overlap small | NO / YES cases | basic correctness of intersection |
| disjoint full | NO | handles complete separation |
| repeated values | YES 9 | duplicates do not affect logic |

## Edge Cases

A typical corner case is when both arrays contain repeated values but share only one distinct element. For example, `a = [9, 9, 9, 9]` and `b = [9, 1, 2, 3]`. The algorithm converts `a` into `{9}` and immediately finds `9` while scanning `b`, returning `[9]`. This shows that multiplicity is irrelevant since subsequences depend only on existence, not frequency.

Another case is when arrays are disjoint. For `a = [1, 2]` and `b = [3, 4]`, the set lookup never succeeds, so the scan completes without finding a match and correctly outputs “NO”. This confirms that no hidden longer structure can compensate for the absence of shared elements.
