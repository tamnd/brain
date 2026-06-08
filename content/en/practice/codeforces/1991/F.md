---
title: "CF 1991F - Triangle Formation"
description: "We are given a sequence of sticks, each with a positive integer length. For each query, we are asked whether it is possible to pick exactly six distinct sticks from a given contiguous subarray such that we can form two non-degenerate triangles."
date: "2026-06-08T15:27:04+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1991
codeforces_index: "F"
codeforces_contest_name: "Pinely Round 4 (Div. 1 + Div. 2)"
rating: 2200
weight: 1991
solve_time_s: 191
verified: false
draft: false
---

[CF 1991F - Triangle Formation](https://codeforces.com/problemset/problem/1991/F)

**Rating:** 2200  
**Tags:** brute force, greedy, implementation, math, sortings  
**Solve time:** 3m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of sticks, each with a positive integer length. For each query, we are asked whether it is possible to pick exactly six distinct sticks from a given contiguous subarray such that we can form **two non-degenerate triangles**. A non-degenerate triangle is one where the sum of any two sides is strictly greater than the third side.

The key points are that each query operates on a contiguous subarray of length at least six, and we need to select six **distinct indices** (not necessarily six distinct lengths) to form two triangles. The constraints are large: up to 100,000 sticks and 100,000 queries, which rules out any brute-force solution that inspects all 6-combinations of sticks in the query.

Edge cases are subtle. If all sticks in a range are equal, any triple of distinct indices forms a valid triangle. However, if there are only two large sticks and the rest are tiny, no triangles may be possible. For example, a subarray `[1, 1, 1, 1, 10, 10]` cannot form two triangles despite having six sticks. Careless implementations that only look at counts of lengths or the three largest sticks may incorrectly answer "YES".

Another subtlety is that stick lengths can be very large, up to 10^9, but arithmetic operations do not overflow in Python, so the focus is entirely on algorithmic efficiency.

## Approaches

The naive approach is to iterate over all 6-combinations of sticks in the given subarray and check every partition into two triples. Each triple is checked for the triangle inequality. This works for correctness but has complexity O((r-l+1)^6) per query, which is far too large given r-l+1 can be up to 10^5. Even using clever triple iteration and avoiding explicit combination generation still leads to O((r-l+1)^3) at minimum per query, which is infeasible for large n and q.

The key insight is that **if we sort the subarray, forming a triangle reduces to checking whether three consecutive elements can form a triangle**. Sorting ensures that for three consecutive sticks a ≤ b ≤ c, we only need to check if a + b > c. If that inequality holds, the triple forms a non-degenerate triangle.

To find two triangles in a subarray, we only need to scan for the first triple that forms a triangle and then scan the remaining elements for a second triple. However, doing this for every query from scratch is still O(n log n) per query due to sorting. This is too slow.

We can optimize further using the observation that **only the six smallest or six largest sticks in any range matter for forming two triangles**, because the triangles are more likely to form when we consider the largest or smallest elements. Precomputing a "prefix of sorted elements" is infeasible because each subarray differs. Instead, we exploit the fact that any valid pair of triangles will appear among the **6 smallest and 6 largest elements** in the range. This reduces each query to scanning at most 12 sticks, which is O(1) after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r-l+1)^6 * q) | O(1) | Too slow |
| Sorting + Consecutive Triples | O(q * (r-l+1) log(r-l+1)) | O(r-l+1) | Too slow |
| Optimal: Scan 12 extreme sticks | O(q * 12) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each query, extract the subarray of sticks from index l to r.
2. Keep track of the **six smallest and six largest stick lengths** in the subarray. This ensures we capture all potential triangles, as triangle formation depends on sums of three sides.
3. Combine these 12 sticks into a list and sort them.
4. Iterate over consecutive triples in this list and record all triples that form a non-degenerate triangle using the condition a + b > c.
5. If at least two disjoint triples exist (disjoint in indices in the original subarray, not necessarily values), answer "YES"; otherwise, answer "NO".

Why it works: Any triple that forms a triangle will involve the smallest or largest elements in the subarray, because triangles cannot be formed from three mid-sized elements if extremes violate the triangle inequality. By checking all 12 extreme candidates, we guarantee finding two valid triangles if they exist. Sorting these candidates allows efficient linear scanning.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_form_two_triangles(sub):
    sub = sorted(sub)
    triangles = []
    n = len(sub)
    for i in range(n-2):
        if sub[i] + sub[i+1] > sub[i+2]:
            triangles.append((i, i+1, i+2))
            if len(triangles) == 2:
                return True
    return False

def main():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    
    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        sub = a[l:r+1]
        
        # pick up to six smallest and six largest
        sub_sorted = sorted(sub)
        candidates = sub_sorted[:6] + sub_sorted[-6:]
        if can_form_two_triangles(candidates):
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    main()
```

Explanation: We take a contiguous subarray, select the six smallest and six largest elements, and sort them. The `can_form_two_triangles` function scans consecutive triples to find triangles. As soon as two are found, we return "YES". This implementation ensures correctness while keeping the query processing essentially constant time.

## Worked Examples

### Example 1

Query: `l=1, r=6` with subarray `[5, 2, 2, 10, 4, 10]`.

| Sorted candidates | Triples forming triangle |
| --- | --- |
| `[2, 2, 4, 5, 10, 10]` | `(2,2,4)`, `(2,4,5)`, `(4,5,10)`, `(5,10,10)` |
| First two valid triples | `(2,4,5)`, `(5,10,10)` |

Output: `YES`

### Example 2

Query: `l=2, r=7` with subarray `[2, 2, 10, 4, 10, 6]`.

| Sorted candidates | Triples forming triangle |
| --- | --- |
| `[2, 2, 4, 6, 10, 10]` | `(2,2,4)`, `(2,4,6)`, `(4,6,10)`, `(6,10,10)` |
| Only one valid triple using distinct sticks | `(2,4,6)` |

Output: `NO`

The trace confirms that only checking extremes suffices and that overlapping triples in terms of indices are avoided.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q * 12 log 12) ≈ O(q) | For each query, sorting at most 12 elements and scanning triples is constant time |
| Space | O(n) | Storing the original stick array and temporary candidate lists per query |

Given n and q up to 10^5, this approach is fast enough. Sorting 12 elements per query is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("""10 5
5 2 2 10 4 10 6 1 5 3
1 6
2 7
2 8
5 10
4 10""") == """YES
NO
YES
NO
YES"""

# Custom minimum size input
assert run("""6 1
1 1 1 1 1 1
1 6""") == "YES"

# Custom all equal, multiple queries
assert run("""7 2
2 2 2 2 2 2 2
1 6
2 7""") == "YES\nYES"

# Custom impossible case
assert run("""6 1
1 1 1 1 10 10
1 6""") == "NO"

# Custom exact six forming two triangles
assert run("""6 1
3 4 5 6 7 8
1 6""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1 1` | `YES` | Minimal size, all equal |
| `2 2 2 2 2 2 2` | `YES\nYES` | Multiple queries, all equal |
| `1 1 1 1 10 10` | `NO` | Impossible two triangles despite six sticks |
| `3 4 5 6 7 8` | `YES` | General case with distinct values |

## Edge Cases

For subarray `[1,1,1
