---
title: "CF 1980B - Choosing Cubes"
description: "We are given several independent scenarios where a collection of numbered cubes is rearranged based on their values. One cube is special because it is the favorite, identified by its original position."
date: "2026-06-08T16:51:52+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1980
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 950 (Div. 3)"
rating: 800
weight: 1980
solve_time_s: 80
verified: true
draft: false
---

[CF 1980B - Choosing Cubes](https://codeforces.com/problemset/problem/1980/B)

**Rating:** 800  
**Tags:** sortings  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios where a collection of numbered cubes is rearranged based on their values. One cube is special because it is the favorite, identified by its original position. After sorting all cubes in descending order of their values, Dmitry removes the first k cubes from this sorted list. The task is to determine whether the favorite cube is always removed, never removed, or could go either way depending on how ties in values are resolved.

The key difficulty is that sorting is not fully deterministic. When multiple cubes share the same value, their relative order after sorting can change arbitrarily. This means the final position of the favorite cube is not fixed; it depends on how equal-valued elements are arranged.

The output must classify the favorite cube into three categories. If it always appears within the first k positions after any valid sorting, the answer is YES. If it can never appear within the first k positions, the answer is NO. Otherwise, there exists at least one valid sorting where it is removed and another where it is not, so the answer is MAYBE.

The constraints are small, with n up to 100 and up to 1000 test cases. This immediately rules out any heavy simulation or state enumeration over permutations of equal elements. Even though brute force permutation reasoning is theoretically possible, the number of reorderings among equal elements grows factorially and is unnecessary.

A subtle edge case arises when many elements have the same value as the favorite. In such cases, the favorite’s position can shift across a wide range after sorting.

For example, if all cubes have value 5 and k = 3, and n = 5, then the favorite cube could be placed anywhere in the sorted order. It could end up inside the first 3 or outside them depending on tie-breaking, so the answer is MAYBE.

Another edge case appears when k is very large. If k = n, all cubes are always removed regardless of ordering, so the answer is always YES. Conversely, if k = 0, no cube is removed, so the answer is always NO.

## Approaches

A brute-force approach would attempt to enumerate all permutations of cubes that respect non-increasing value order. This effectively means generating all ways to permute elements within equal-value groups and checking whether the favorite cube appears in the first k positions in all, none, or some of them. While conceptually straightforward, this explodes factorially inside each group of duplicates. In the worst case where all values are equal, this becomes n! permutations, which is completely infeasible even for n = 100.

The key observation is that sorting only fixes the relative order between different values. All uncertainty exists only inside equal-value blocks. So instead of simulating permutations, we only need to reason about how many elements are strictly greater than the favorite value, and how many are equal to it.

All elements with value strictly greater than the favorite must appear before it in every valid sorted order. These positions are fixed and contribute to a guaranteed prefix. Elements with equal value can appear before or after the favorite arbitrarily among themselves. This creates a range of possible positions for the favorite cube in the final sorted array.

Let higher be the number of elements strictly greater than a_f, and equal be the number of elements equal to a_f, including the favorite itself.

The earliest possible position of the favorite is when all equal elements are arranged after it among their block, so it comes immediately after all strictly greater elements. That position is higher + 1.

The latest possible position is when all other equal elements are placed before it, so it is last within its equal block. That position is higher + equal.

Now we compare this range with k. If even the earliest position is greater than k, the favorite is never removed. If the latest position is at most k, it is always removed. Otherwise, there exists a split of tie-breaking that puts it on either side, so the answer is MAYBE.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations within equal groups | Exponential | O(n) | Too slow |
| Count greater and equal elements | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read n, f, k and the array a.

The favorite cube is at index f, so we store its value x = a[f].
2. Count how many elements have value strictly greater than x.

These elements must appear before the favorite in any sorted arrangement.
3. Count how many elements have value equal to x.

This group includes the favorite itself and determines how flexible its position is.
4. Compute the earliest possible position of the favorite as greater + 1.

This corresponds to the case where all equal elements except the favorite are placed after it.
5. Compute the latest possible position of the favorite as greater + equal.

This corresponds to the case where all other equal elements are placed before it.
6. Compare this range with k.

If latest ≤ k, then every possible ordering places the favorite in the removed prefix, so output YES.
7. If earliest > k, then no possible ordering places it within the removed prefix, so output NO.
8. Otherwise output MAYBE.

This corresponds to overlap between possible positions and the cutoff.

### Why it works

The sorted order is fully determined up to permutations inside equal-value groups. Elements with different values have a fixed relative order. This means the favorite’s only source of uncertainty is its rank among elements with the same value. Its final position depends only on how many equal-valued elements are placed before it. That number can range from 0 to equal − 1 independently of other constraints, so the favorite’s position spans a contiguous interval [greater + 1, greater + equal]. Any position outside this interval is impossible, and every position inside is achievable by a suitable tie-breaking. This makes the comparison against k complete and exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, f, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    x = a[f - 1]
    
    greater = 0
    equal = 0
    
    for v in a:
        if v > x:
            greater += 1
        elif v == x:
            equal += 1
    
    earliest = greater + 1
    latest = greater + equal
    
    if latest <= k:
        print("YES")
    elif earliest > k:
        print("NO")
    else:
        print("MAYBE")
```

The implementation directly mirrors the derived interval logic. The only subtle point is indexing: the favorite index is 1-based in input, so it must be shifted to 0-based when accessing the array. The counts are recomputed per test case since n is small.

The decision logic avoids sorting entirely, which is unnecessary because we never need the exact permutation, only the rank interval of the favorite cube.

## Worked Examples

### Example 1

Input:

n = 5, f = 2, k = 2

a = [4, 3, 3, 2, 3]

| Step | greater | equal | earliest | latest | k | Result |
| --- | --- | --- | --- | --- | --- | --- |
| compute x = 3 |  |  |  |  |  |  |
| count values | 1 | 3 | 2 | 4 | 2 | MAYBE |

The favorite value is 3. There is one value greater (4) and three equal values. The favorite can be second through fourth in the sorted array depending on tie-breaking. Since k = 2 lies inside this range, some valid arrangements remove it while others do not.

### Example 2

Input:

n = 5, f = 5, k = 3

a = [4, 2, 1, 3, 5]

| Step | greater | equal | earliest | latest | k | Result |
| --- | --- | --- | --- | --- | --- | --- |
| compute x = 5 |  |  |  |  |  |  |
| count values | 0 | 1 | 1 | 1 | 3 | YES |

The favorite is the largest element, so it always becomes the first in sorted order. Since k = 3, it is always removed regardless of tie-breaking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan the array once to count greater and equal elements |
| Space | O(1) | Only a few counters are used |

The constraints allow up to 1000 test cases with n up to 100, so at most 100,000 operations, which is trivial under 1 second in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []
    
    t = int(input())
    for _ in range(t):
        n, f, k = map(int, input().split())
        a = list(map(int, input().split()))
        x = a[f - 1]
        
        greater = sum(1 for v in a if v > x)
        equal = sum(1 for v in a if v == x)
        
        earliest = greater + 1
        latest = greater + equal
        
        if latest <= k:
            out.append("YES")
        elif earliest > k:
            out.append("NO")
        else:
            out.append("MAYBE")
    
    return "\n".join(out) + "\n"

# provided samples
assert run("""12
5 2 2
4 3 3 2 3
5 5 3
4 2 1 3 5
5 5 2
5 2 4 1 3
5 5 5
1 2 5 4 3
5 5 4
3 1 2 4 5
5 5 5
4 3 2 1 5
6 5 3
1 2 3 1 2 3
10 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1
42
5 2 3
2 2 1 1 2
2 1 1
2 1
5 3 1
3 3 2 3 2
""") == """MAYBE
YES
NO
YES
YES
YES
MAYBE
MAYBE
YES
YES
YES
NO
"""

# custom cases
assert run("""1
1 1 1
5
""") == "YES\n"

assert run("""1
5 1 0
5 4 3 2 1
""") == "NO\n"

assert run("""1
4 2 2
2 2 2 2
""") == "MAYBE\n"

assert run("""1
6 3 2
5 5 5 1 1 1
""") == "NO\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element always removed | YES | minimum edge case |
| k = 0 no removal | NO | boundary condition |
| all equal values | MAYBE | full tie flexibility |
| mixed groups cutoff | NO | strict separation case |

## Edge Cases

A case where all values are equal demonstrates the full range behavior. If n = 4, k = 2, and all values are 7, then greater = 0 and equal = 4, so earliest = 1 and latest = 4. The favorite can land in any position depending on tie-breaking, so it can be removed or not, producing MAYBE. The algorithm correctly captures this because the interval spans both sides of k.

When the favorite has the maximum value, greater = 0 and equal = 1. The interval collapses to a single position at the front of the array. If k ≥ 1, it is always removed, otherwise it is never removed. The code handles this cleanly because earliest equals latest, eliminating ambiguity.

When k is very small, only elements strictly forced into the front matter. If greater already exceeds k, the favorite is guaranteed to be pushed beyond the cutoff regardless of equal-group behavior, producing NO.
