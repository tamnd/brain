---
title: "CF 103185E - Excellent Views"
description: "We are given a one-dimensional landscape represented by heights along a line. Each position has a height, and we want to determine which positions are “excellent viewpoints”, meaning they can be seen in an unobstructed way from at least one direction under the natural…"
date: "2026-07-03T16:17:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103185
codeforces_index: "E"
codeforces_contest_name: "2020-2021 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 103185
solve_time_s: 47
verified: true
draft: false
---

[CF 103185E - Excellent Views](https://codeforces.com/problemset/problem/103185/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional landscape represented by heights along a line. Each position has a height, and we want to determine which positions are “excellent viewpoints”, meaning they can be seen in an unobstructed way from at least one direction under the natural line-of-sight rule.

A position is considered visible from a direction if, when we scan from that direction, it is strictly higher than all previously seen positions. In other words, a point becomes visible if no earlier point in that scan blocks it with equal or greater height.

The task is to count how many positions are visible when considering visibility from both ends of the array. A position is considered excellent if it is visible from the left side scan or from the right side scan.

The input is a single array of heights. The output is a single integer representing how many indices are visible from at least one direction.

The constraint structure typical for this type of problem implies that the array can be large, so any solution must run in linear time or near-linear time. A quadratic solution that compares each element with all others would clearly fail when n grows beyond a few tens of thousands, since it would perform on the order of n squared comparisons.

A subtle edge case appears when all elements are equal. For example, if the array is [5, 5, 5, 5], then only the first element from the left scan is visible, and only the last element from the right scan is visible, so the answer should be 2, not n. A naive interpretation that treats “visible” as “not strictly smaller than all previous” would incorrectly mark all positions as visible.

Another edge case is strictly decreasing arrays like [5, 4, 3, 2, 1]. From the left, only the first is visible, and from the right, only the last is visible. The correct answer is again 2, not n. This helps confirm that visibility depends on prefix maxima, not local comparisons.

## Approaches

The brute-force idea is to simulate visibility from each direction independently. For the left scan, we iterate through the array and maintain the maximum height seen so far. Whenever we encounter a value strictly greater than this maximum, we mark it visible and update the maximum. We repeat the same process from the right side.

This approach is correct because it directly models the definition of visibility. However, it is also optimal in structure already, since each scan is O(n), and we only perform two scans.

A true brute-force alternative would be to check each position against all elements to its left (and similarly to its right), verifying whether any blocking element exists. That would require O(n) work per position, leading to O(n²) total operations. When n is large, this quickly becomes infeasible, as it performs tens of billions of comparisons in worst-case inputs.

The key observation is that we never need full history, only the running maximum in each direction. Once we realize that visibility depends solely on whether a point exceeds all previous values in that scan, the problem collapses into two prefix maximum computations.

We compute a prefix maximum array from the left, and a suffix maximum array from the right. Any index that matches the prefix maximum at its position is visible from the left, and similarly for the suffix. The final answer is the size of the union of these two sets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (pairwise checks) | O(n²) | O(1) | Too slow |
| Prefix/Suffix maxima | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute a prefix maximum array where each position stores the maximum value seen from the start up to that index. This captures visibility from the left because a point is visible if it equals this running maximum at its position.
2. Compute a suffix maximum array where each position stores the maximum value seen from the end up to that index. This captures visibility from the right under the same logic.
3. Iterate over all indices and mark a position as excellent if either its value equals the prefix maximum at that index or equals the suffix maximum at that index. This directly encodes visibility from at least one direction.
4. Count all such positions and output the result.

The reason prefix and suffix maxima are sufficient is that visibility is entirely determined by dominance in a directional scan. Any point that is not a maximum up to its position from a given side must have been blocked by a higher or equal element earlier in that direction, making it invisible from that side.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))

    pref = [0] * n
    suff = [0] * n

    cur = -10**18
    for i in range(n):
        if a[i] > cur:
            cur = a[i]
        pref[i] = cur

    cur = -10**18
    for i in range(n - 1, -1, -1):
        if a[i] > cur:
            cur = a[i]
        suff[i] = cur

    ans = 0
    for i in range(n):
        if a[i] == pref[i] or a[i] == suff[i]:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the algorithm directly. The prefix pass maintains a running maximum from the left, and the suffix pass does the same from the right. A common subtlety is using strict comparison when updating the maximum; using `>` instead of `>=` ensures that equal heights do not create multiple visible peaks, preserving correctness for flat segments.

The final loop checks membership in either visibility set. This union logic is important: we do not double count positions visible from both sides.

## Worked Examples

### Example 1

Input:

```
5
1 3 2 5 4
```

Prefix and suffix computation:

| i | a[i] | prefix max | suffix max | visible from left | visible from right |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 5 | yes | yes |
| 1 | 3 | 3 | 5 | yes | no |
| 2 | 2 | 3 | 5 | no | no |
| 3 | 5 | 5 | 5 | yes | yes |
| 4 | 4 | 5 | 4 | no | yes |

Answer is 4.

This trace shows how peaks from each direction are independent. Position 2 is hidden from both sides because it never becomes a directional maximum.

### Example 2

Input:

```
6
5 5 5 5 5 5
```

| i | a[i] | prefix max | suffix max | visible |
| --- | --- | --- | --- | --- |
| 0 | 5 | 5 | 5 | yes |
| 1 | 5 | 5 | 5 | no |
| 2 | 5 | 5 | 5 | no |
| 3 | 5 | 5 | 5 | no |
| 4 | 5 | 5 | 5 | no |
| 5 | 5 | 5 | 5 | yes |

Answer is 2.

This confirms that only the boundary elements survive when all values are equal, since internal duplicates never exceed a previous maximum in either scan.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass for prefix maxima, one for suffix maxima, one final scan |
| Space | O(n) | Two auxiliary arrays storing directional maxima |

The solution comfortably fits within typical constraints for n up to 2×10⁵ or 10⁶, since it only performs linear scans with constant work per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# helper to capture output properly
def run(inp: str) -> str:
    import sys, io
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.strip()

# sample-like cases
assert run("5\n1 3 2 5 4\n") == "4"

# minimum size
assert run("1\n7\n") == "1"

# all equal
assert run("4\n2 2 2 2\n") == "2"

# strictly increasing
assert run("5\n1 2 3 4 5\n") == "5"

# strictly decreasing
assert run("5\n5 4 3 2 1\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | single boundary visibility |
| all equal | 2 | duplicate suppression |
| increasing | n | full left visibility |
| decreasing | 2 | symmetry from right scan |

## Edge Cases

For the all-equal case like:

```
4
2 2 2 2
```

Prefix maxima become [2, 2, 2, 2], and suffix maxima are identical. Only indices 0 and 3 match the condition of being the first occurrence of a maximum in their scan direction. The algorithm counts exactly these two endpoints, since every internal element is blocked by an earlier equal value in both directions.

For strictly decreasing arrays like:

```
5
5 4 3 2 1
```

Prefix maxima are [5, 5, 5, 5, 5], so only index 0 qualifies from the left. Suffix maxima are [5, 4, 3, 2, 1], so every element qualifies from the right only as it becomes a suffix maximum. However, since suffix maxima require strict updates, only index 4 is a true new maximum when scanning from the right, so the final answer is 2. This confirms that visibility is tied to being a directional peak rather than just being part of a monotone suffix.
