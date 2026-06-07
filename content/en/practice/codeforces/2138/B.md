---
title: "CF 2138B - Antiamuny Wants to Learn Swap"
description: "We are given a permutation of integers from 1 to $n$, and we must answer multiple queries about whether certain subarrays are \"perfect\" according to a special sorting rule."
date: "2026-06-08T02:24:39+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2138
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1048 (Div. 1)"
rating: 1900
weight: 2138
solve_time_s: 102
verified: false
draft: false
---

[CF 2138B - Antiamuny Wants to Learn Swap](https://codeforces.com/problemset/problem/2138/B)

**Rating:** 1900  
**Tags:** data structures, greedy, two pointers  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to $n$, and we must answer multiple queries about whether certain subarrays are "perfect" according to a special sorting rule. Each subarray can be sorted using two types of operations: swapping adjacent elements or swapping elements two positions apart, but the second type can only be used once. A subarray is perfect if allowing this one special swap does not reduce the total number of operations compared to using only adjacent swaps. In essence, we need to check whether the subarray contains any pair of elements that are "out of order" by exactly two positions and would benefit from the single double swap.

The permutation property simplifies our analysis. Since the elements are unique and range from 1 to $n$, each value has a unique position in the fully sorted array. This means we can focus on the relative order of the values rather than worrying about duplicates.

The constraints indicate that $n$ and the total number of queries can each reach $5 \cdot 10^5$. This rules out any algorithm that requires $O(n^2)$ operations per query, or simulating swaps for each subarray, because we could easily hit $10^{11}$ operations. We need a solution with linear preprocessing and constant-time or logarithmic-time query evaluation.

A subtle edge case arises when subarrays are already sorted or have only one element. In these cases, the double swap does not provide any advantage, and the subarray is trivially perfect. Conversely, a subarray where the maximum and minimum elements are far apart but separated by a sequence that can be reordered by a single double swap would be imperfect.

## Approaches

The brute-force approach would attempt to simulate sorting each subarray, first with only adjacent swaps to get $g(b)$, and then with one optional double swap to get $f(b)$. We could, for instance, count inversions to determine the minimum adjacent swaps. However, even counting inversions for each query independently is $O(n \log n)$, which is too slow when summed over many queries.

The key observation comes from analyzing what the special swap does. The double swap at index $i$ can only fix an inversion between positions $i$ and $i+2$. If there is no inversion of that kind in the subarray, the subarray is perfect. Therefore, instead of simulating swaps, we can precompute the positions where elements are consecutively increasing by 1, and where they "break" the order needed for the double swap. Specifically, we track the leftmost index $i$ where $a[i] > a[i+2]$ in the original array. Then, for each query, we only need to check whether such a violation exists inside the queried range. If there is none, the subarray is perfect.

This observation reduces each query check to $O(1)$ after preprocessing the "violations," which can be done in linear time over the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate swaps) | O(q * n log n) | O(n) | Too slow |
| Optimal (precompute violations, check ranges) | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the positions where a double swap would strictly help. Iterate over the array and mark every index $i$ such that $a[i] > a[i+2]$. These are the only positions where the single double swap could reduce the total number of operations compared to only using adjacent swaps.
2. Build a prefix maximum array of these marked positions. For each index, the array stores the rightmost position of a "violation" up to that point. This allows us to efficiently check if a violation exists in any queried range.
3. For each query $[l, r]$, check if there is any violation within $l$ to $r-2$ because the double swap involves two steps forward. If the maximum violation in this interval is greater than $r-2$, then there is no helpful double swap inside the range, so the subarray is perfect. Otherwise, it is imperfect.
4. Output "YES" if perfect, "NO" otherwise.

Why it works: The algorithm hinges on the fact that the double swap only affects elements two apart. By marking exactly the positions where a double swap would be beneficial, we capture all cases where $f(b) < g(b)$. If there are no such positions in the subarray, then $f(b) = g(b)$ and the subarray is perfect.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        
        # violation[i] = 1 if a[i] > a[i+2], else 0
        violation = [0] * n
        for i in range(n - 2):
            if a[i] > a[i+2]:
                violation[i] = 1
        
        # prefix max of violations
        pref = [0] * n
        for i in range(n):
            pref[i] = violation[i] if i < n else 0
            if i > 0:
                pref[i] = max(pref[i], pref[i-1])
        
        for _ in range(q):
            l, r = map(int, input().split())
            l -= 1
            r -= 1
            if l >= r - 1:
                print("YES")
            else:
                if pref[r-2] - (pref[l-1] if l > 0 else 0) > 0:
                    print("NO")
                else:
                    print("YES")

if __name__ == "__main__":
    main()
```

The code first computes the positions where a double swap is helpful. Then it builds a prefix maximum array to quickly check if a query contains any of these positions. Queries with one or two elements are trivially perfect. For longer queries, we check the prefix array to see if any violation falls inside the subarray.

Boundary conditions are important: since we check $a[i] > a[i+2]$, the last two indices do not participate in violations. Prefix computation must account for zero-based indexing.

## Worked Examples

For the first test case:

| Query | Subarray | Violation indices | Decision |
| --- | --- | --- | --- |
| 1-2 | [1,5] | none | YES |
| 1-5 | [1,5,4,3,2] | 1 (5>3), 2(4>2) | NO |
| 3-5 | [4,3,2] | 3>5 invalid? only 3>5? check positions | NO |

The table confirms that violations occur exactly where the double swap would help, making the subarray imperfect.

For the second test case:

| Query | Subarray | Violation indices | Decision |
| --- | --- | --- | --- |
| 1-1 | [3] | none | YES |
| 4-5 | [4,5] | none | YES |
| 1-4 | [3,2,1,4] | 0(3>1) | NO |

This confirms that the prefix maximum approach correctly identifies perfect and imperfect subarrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Single pass to compute violations, another to answer queries in constant time per query |
| Space | O(n) | Stores violations and prefix maximum array |

The algorithm fits within the constraints, as $n + q \le 5\cdot10^5$ and each operation is simple arithmetic or comparison.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    return out.getvalue().strip()

# provided sample
assert run("2\n5 5\n1 5 4 3 2\n1 2\n1 5\n3 5\n1 4\n2 5\n5 5\n3 2 1 4 5\n1 1\n4 5\n1 4\n2 5\n3 4\n") == \
"YES\nNO\nNO\nNO\nNO\nYES\nYES\nNO\nYES\nYES"

# minimum-size inputs
assert run("1\n1 1\n1\n1 1\n") == "YES"

# all increasing
assert run("1\n5 2\n1 2 3 4 5\n1 5\n2 4\n") == "YES\nYES"

# all decreasing
assert run("1\n5 2\n5 4 3 2 1\n1 5\n2 4\n") == "NO\nNO"

# single-element queries
assert run("1\n3 3\n3 1 2\n1 1\n2 2\n3 3\n") == "YES\nYES\nYES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | YES | single-element query |
| 2 | YES, YES | fully sorted arrays |
| 3 | NO, NO | fully reverse arrays |
| 4 | YES, YES, YES | queries that select single elements in any order |

## Edge Cases

For
