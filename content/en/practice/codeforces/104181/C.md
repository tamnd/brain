---
title: "CF 104181C - Brownie Baking"
description: "We are given a set of friends, each of whom wants a brownie of at least a certain minimum size. We are also given a collection of baking tins, each tin producing exactly one brownie of a fixed size."
date: "2026-07-02T00:37:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104181
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 02-10-23 Div. 1 (Advanced)"
rating: 0
weight: 104181
solve_time_s: 58
verified: true
draft: false
---

[CF 104181C - Brownie Baking](https://codeforces.com/problemset/problem/104181/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of friends, each of whom wants a brownie of at least a certain minimum size. We are also given a collection of baking tins, each tin producing exactly one brownie of a fixed size. Each tin can be used at most once, and each friend can receive at most one brownie. A friend is satisfied if the brownie they receive is strictly larger than their requested size.

The task is to match tins to friends in a way that maximizes the number of satisfied friends.

The input consists of two arrays. The first describes the minimum acceptable brownie size for each friend. The second describes the available brownie sizes produced by tins. The output is a single integer: the maximum number of valid pairings where a tin size is strictly greater than the friend’s requirement.

The constraints go up to 200,000 elements in both arrays. Any solution that is quadratic in the worst case would require on the order of 4 × 10^10 comparisons, which is far beyond what can be executed in two seconds in Python. This immediately rules out brute force pairing or checking every possible assignment.

A subtle point in the problem is the strict inequality condition. A tin of exactly the requested size does not satisfy the friend. This changes how we search for matches, because equality is not acceptable and must be skipped carefully during matching.

A second subtle issue is that optimal assignments are not obvious locally. Giving a large tin to a small request can sometimes block a better future match, so greedy choices must be justified carefully.

## Approaches

A brute-force interpretation is to consider every possible assignment of tins to friends and choose the best matching. Even restricting ourselves to trying each friend against every tin yields N × M comparisons. With both up to 2 × 10^5, this becomes infeasible.

Another slightly improved but still too slow approach is to sort both arrays and, for each friend, scan forward in the tins array to find the first valid tin. Even with sorting, the nested scan still degrades to quadratic behavior when many tins are too small, because each tin may be examined multiple times.

The key observation is that both arrays are independent sets of sizes, and we only care about matching them under a monotone condition. Once sorted, the structure becomes linear: if we process the smallest unmet requirement and always try to satisfy it with the smallest possible tin that still works, we avoid wasting large tins.

This leads naturally to a greedy strategy: sort both arrays and move through them with two pointers. We attempt to pair the smallest remaining requirement with the smallest tin that can satisfy it. If the tin is too small, we discard it and move on, because it cannot help any larger requirement that we have not yet reached. If it is large enough, we match them and advance both pointers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force pairing | O(NM) | O(1) | Too slow |
| Sort + greedy two pointers | O(N log N + M log M) | O(1) extra | Accepted |

## Algorithm Walkthrough

We sort both the friend requirements and the tin sizes in ascending order. This aligns the problem so that we always deal with the smallest remaining unsatisfied demand first.

We maintain two indices, one for friends and one for tins, and we also maintain a counter for successful matches.

1. Sort the array of friend requirements in increasing order and sort the array of tin sizes in increasing order. This ensures we can reason greedily from smallest to largest without missing optimal pairings.
2. Initialize two pointers, i for friends and j for tins, both starting at 0. Also initialize a variable matched to 0. The pointer i represents the smallest unmet requirement, and j represents the smallest unused tin.
3. While both pointers are within bounds, compare s[i] and t[j]. If t[j] is greater than s[i], we assign this tin to this friend, increment matched by 1, and advance both pointers. This is safe because t[j] is the smallest tin that can satisfy s[i], so any other choice would only waste larger tins.
4. If t[j] is less than or equal to s[i], we discard this tin by incrementing j. It cannot satisfy the current friend, and since all future friends have equal or larger requirements, it cannot satisfy them either, so it is permanently useless.
5. Continue until either array is exhausted. The value of matched is the maximum number of satisfied friends.

Why it works comes down to a dominance argument over sorted arrays. At any step, pairing the smallest unsatisfied friend with the smallest possible usable tin preserves future flexibility. If we were to use a larger tin instead, we would only reduce the number of options available for later, larger requirements, without improving the current match. The algorithm maintains the invariant that all tins before j are either used or too small to be useful, and all friends before i are already satisfied.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    s = list(map(int, input().split()))
    t = list(map(int, input().split()))
    
    s.sort()
    t.sort()
    
    i = j = 0
    matched = 0
    
    while i < n and j < m:
        if t[j] > s[i]:
            matched += 1
            i += 1
            j += 1
        else:
            j += 1
    
    print(matched)

if __name__ == "__main__":
    solve()
```

The core of the implementation is the two-pointer sweep after sorting. Sorting is necessary because the greedy decision only holds when both sequences are monotonic. Without sorting, local decisions have no global guarantee.

The strict inequality is handled directly in the comparison `t[j] > s[i]`. Using `>=` here would incorrectly count equal-sized tins as valid, which violates the problem condition.

The pointers advance in a controlled way: i only moves when a friend is satisfied, j always moves forward and never revisits tins, ensuring linear scan after sorting.

## Worked Examples

### Sample 1

Input:

```
5 3
8 12 25 3 10
1 8 20
```

Sorted:

s = [3, 8, 10, 12, 25]

t = [1, 8, 20]

| i | j | s[i] | t[j] | Action | matched |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 3 | 1 | 1 ≤ 3, discard tin | 0 |
| 0 | 1 | 3 | 8 | 8 > 3, match | 1 |
| 1 | 2 | 8 | 20 | 20 > 8, match | 2 |

Output is 2.

This trace shows that small tins are safely discarded even if they might seem usable later, because larger requirements exist that still preserve feasibility.

### Custom Example

Input:

```
4 4
5 6 7 8
4 5 6 10
```

Sorted:

s = [5, 6, 7, 8]

t = [4, 5, 6, 10]

| i | j | s[i] | t[j] | Action | matched |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 5 | 4 | discard | 0 |
| 0 | 1 | 5 | 5 | discard (not strictly greater) | 0 |
| 0 | 2 | 5 | 6 | match | 1 |
| 1 | 3 | 6 | 10 | match | 2 |

This demonstrates the strict inequality behavior clearly, where equality still requires skipping tins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N + M log M) | Sorting both arrays dominates, two-pointer scan is linear |
| Space | O(1) extra | Sorting is in-place aside from input storage |

The constraints allow up to 2 × 10^5 elements, so sorting at this scale is well within limits in Python, and the linear scan adds negligible overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import sys as _sys
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    n, m = map(int, input().split())
    s = list(map(int, input().split()))
    t = list(map(int, input().split()))
    s.sort()
    t.sort()
    i = j = 0
    matched = 0
    while i < n and j < m:
        if t[j] > s[i]:
            matched += 1
            i += 1
            j += 1
        else:
            j += 1
    print(matched)

# provided sample
assert run("""5 3
8 12 25 3 10
1 8 20
""") == "2"

# all tins too small
assert run("""3 3
10 20 30
1 2 3
""") == "0"

# all tins large enough
assert run("""3 3
1 2 3
10 10 10
""") == "3"

# equality edge case
assert run("""3 3
5 5 5
5 6 7
""") == "2"

# mixed case
assert run("""5 4
2 4 6 8 10
1 3 5 9
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all tins too small | 0 | no accidental matches |
| all tins large | 3 | full matching possible |
| equality case | 2 | strict inequality handling |
| mixed case | 3 | greedy pairing correctness |

## Edge Cases

A critical edge case is when many tins are exactly equal to requirements. For example:

Input:

```
3 3
5 5 5
5 6 7
```

After sorting, the algorithm compares 5 with 5 first. Since the condition is strict, it discards the tin. This repeats until it reaches 6, producing only two matches. A buggy implementation that uses `>=` instead of `>` would incorrectly count the first pair and return 3, violating the problem constraint.

Another edge case occurs when all tins are smaller than all requirements:

```
3 3
10 20 30
1 2 3
```

The pointer over tins advances until exhaustion without any matches. The algorithm correctly returns 0 because no tin ever satisfies the strict inequality condition, and every discard is justified by monotonicity after sorting.
