---
title: "CF 105364A - Pairs"
description: "We are given several independent test cases. In each one, we receive an even-length list of integers, and we must decide whether it is possible to partition the numbers into pairs such that every pair has the same sum."
date: "2026-06-23T16:00:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105364
codeforces_index: "A"
codeforces_contest_name: "XXV Spain Olympiad in Informatics, Online Qualifier 2"
rating: 0
weight: 105364
solve_time_s: 75
verified: true
draft: false
---

[CF 105364A - Pairs](https://codeforces.com/problemset/problem/105364/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each one, we receive an even-length list of integers, and we must decide whether it is possible to partition the numbers into pairs such that every pair has the same sum. Each element must be used exactly once, and all formed pairs must share a single common target sum.

Another way to think about the task is that we are trying to rearrange the array into disjoint pairs, and every pair must "balance" to the same value. The challenge is not to construct the pairs explicitly, but only to determine whether such a pairing exists.

The constraints are large enough that any approach trying to test pairings explicitly will fail. With up to $5 \cdot 10^5$ numbers across all test cases, a solution that considers even a quadratic number of pairings per case is immediately impossible. This forces us toward a strategy where each test case is handled in linear or near-linear time, typically $O(n \log n)$ or better.

A subtle issue appears when all values are identical or when values repeat in uneven distributions. For example, if all numbers are the same, pairing is always possible because every pair has the same sum. On the other hand, if the multiset is skewed so that only one candidate sum could work for one pair but not consistently for all pairs, a naive greedy pairing might incorrectly assume feasibility or fail depending on pairing order.

Consider a misleading case like:

```
4
1 2 3 4
```

If we greedily pair adjacent elements, we get sums 3 and 7, which immediately fails. But even alternative pairings like (1,4) and (2,3) give sums 5 and 5, so this case is actually valid. This shows that pairing order matters for naive strategies, and we need a global invariant rather than local decisions.

## Approaches

A brute-force strategy would attempt to form all possible pairings of the array and check whether any full pairing produces equal sums across all pairs. This is equivalent to exploring all perfect matchings in a complete graph with $n$ vertices, which grows super-exponentially. Even with pruning, the number of pairings is on the order of $(n-1)!!$, which becomes infeasible even for $n = 20$.

The key observation is that if such a pairing exists, the target sum must be uniquely determined. Suppose we sort the array. If we pair the smallest element with the largest element, that already fixes the required sum. Every other pair must conform to this same sum, which forces a strict structure: second smallest pairs with second largest, and so on. If any mismatch occurs, no alternative pairing can rescue the situation, because changing any pairing would break the global sum consistency.

This reduces the problem from searching over all pairings to verifying a single deterministic pairing pattern after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Sorting + Two Pointers | O(n log n) | O(1) / O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the array and sort it in non-decreasing order. Sorting is necessary because the optimal pairing structure depends on matching extremes, and sorting exposes these extremes cleanly.
2. Compute a candidate target sum using the first and last elements, specifically $a[0] + a[n-1]$. This value is forced if a valid solution exists, because the smallest and largest elements must be paired in any valid configuration; otherwise, replacing them with any other pairing would only reduce the range and break consistency.
3. Use two pointers, one starting at the beginning and one at the end, and move inward. At each step, form a conceptual pair from the current smallest remaining and largest remaining elements.
4. For each such pair, verify that their sum equals the previously computed target sum. If any pair deviates, immediately conclude that no valid pairing exists.
5. If all pairs match the target sum, then a valid partition exists.

The key idea is that once the outermost elements are fixed, the remaining structure is fully determined. There is no flexibility left for rearrangement without breaking consistency.

### Why it works

After sorting, assume a valid solution exists. Let the minimum element be paired with some element other than the maximum. If that happens, the maximum must pair with something smaller than or equal to the second largest. That would force a second pair whose sum exceeds or falls short of the original target depending on ordering, contradicting the requirement that all pairs share the same sum.

This creates a rigid pairing structure: the sorted array must pair symmetrically from the ends inward. Since the target sum is fixed by the extreme elements, every pair is forced, and any deviation invalidates the configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()

        target = a[0] + a[-1]

        ok = True
        i, j = 0, n - 1

        while i < j:
            if a[i] + a[j] != target:
                ok = False
                break
            i += 1
            j -= 1

        out.append("SI" if ok else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the array so that the smallest and largest values become the natural first candidate pair. The target sum is fixed immediately from these extremes, since any valid solution must include some pairing structure consistent with that value.

The two-pointer loop enforces that every symmetric pair matches the same sum. The loop only runs $n/2$ iterations, so the verification step is linear. The only subtle requirement is that the target must be computed before the loop begins; recomputing it dynamically would be incorrect because it would allow inconsistent local adjustments.

## Worked Examples

### Example 1

Input:

```
4
-2 1 -1 2
```

Sorted array: `[-2, -1, 1, 2]`, target = 0

| i | j | a[i] | a[j] | sum | valid so far |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | -2 | 2 | 0 | yes |
| 1 | 2 | -1 | 1 | 0 | yes |

All pairs match, so output is `SI`.

This confirms that symmetric pairing correctly captures a valid structure even when negatives are present.

### Example 2

Input:

```
6
2 4 0 6 3 5
```

Sorted array: `[0, 2, 3, 4, 5, 6]`, target = 6

| i | j | a[i] | a[j] | sum | valid so far |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | 0 | 6 | 6 | yes |
| 1 | 4 | 2 | 5 | 7 | no |

Mismatch occurs immediately, so output is `NO`.

This shows that even though some pairs could match the target individually, the global structure cannot be satisfied simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates each test case |
| Space | $O(1)$ extra | only pointers and fixed variables, aside from input storage |

The total input size across test cases is bounded by $5 \cdot 10^5$, so sorting each case independently still fits comfortably within limits. The linear scan afterward ensures that verification does not add overhead beyond sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        target = a[0] + a[-1]
        ok = True
        i, j = 0, n - 1
        while i < j:
            if a[i] + a[j] != target:
                ok = False
                break
            i += 1
            j -= 1
        res.append("SI" if ok else "NO")
    return "\n".join(res)

# provided samples
assert run("""3
4
-2 1 -1 2
6
2 4 0 6 3 5
8
1 1 1 1 1 1 1 1
""") == """SI
NO
SI"""

# all equal values
assert run("""1
6
5 5 5 5 5 5
""") == "SI"

# already valid symmetric structure
assert run("""1
4
1 3 2 2
""") == "SI"

# impossible due to imbalance
assert run("""1
4
1 1 2 3
""") == "NO"

# negative values
assert run("""1
4
-1 -2 2 1
""") == "SI"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | SI | uniform multiset always works |
| symmetric hidden pairing | SI | correctness beyond trivial order |
| imbalance case | NO | detects impossible distributions |
| negatives | SI | correctness with sign changes |

## Edge Cases

One important edge case is when all values are identical. For input:

```
6
7 7 7 7 7 7
```

sorting gives the same array and the target is 14. Every pair sums to 14, so the algorithm accepts. The pointer scan never finds a mismatch, confirming correctness in degenerate uniform distributions.

Another edge case involves negative numbers where the optimal pairing is not obvious without sorting:

```
4
-3 -1 2 4
```

Sorting gives `[-3, -1, 2, 4]`, target = 1. The pairs are (-3,4) and (-1,2), both summing to 1. The algorithm correctly identifies feasibility even though naive adjacent pairing would incorrectly suggest failure.

A third edge case is when only one pair violates the constraint:

```
6
0 1 2 3 4 10
```

Sorted array leads to target 10, but pairing reveals a mismatch early. The algorithm rejects immediately without exploring alternative pairings, which is essential for efficiency on large inputs.
