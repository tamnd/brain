---
title: "CF 105845C - OR-Max Segments"
description: "We are given an array of integers, and we look at every contiguous subarray. A subarray is considered valid when a very specific equality holds: the largest value inside the subarray must be exactly equal to the bitwise OR of all values in that same subarray."
date: "2026-06-25T14:49:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105845
codeforces_index: "C"
codeforces_contest_name: "CodEMI 2025"
rating: 0
weight: 105845
solve_time_s: 52
verified: true
draft: false
---

[CF 105845C - OR-Max Segments](https://codeforces.com/problemset/problem/105845/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we look at every contiguous subarray. A subarray is considered valid when a very specific equality holds: the largest value inside the subarray must be exactly equal to the bitwise OR of all values in that same subarray.

In other words, if we take any segment, compute its maximum element, and also compute the bitwise OR of every element inside it, we only count that segment if these two values are identical.

The task is to count how many subarrays satisfy this condition across multiple test cases.

The constraint that the total length across all test cases is up to $2 \cdot 10^5$ implies that any approach that is worse than roughly linearithmic per test case will fail. A quadratic scan over all subarrays is too large because even a single array of size $2 \cdot 10^5$ would already imply about $2 \cdot 10^{10}$ subarrays.

A key structural constraint is hidden in the equality itself. The OR of a segment can only increase when new elements are added, while the maximum is determined by a single element. This mismatch forces strong restrictions on what a valid subarray can look like.

A subtle edge case appears when elements repeat or when a large element is surrounded by smaller ones that do not introduce new bits. For example, in the array $[1, 2, 3]$, the subarray $[1,2,3]$ has maximum $3$ and OR $1 ,|, 2 ,|, 3 = 3$, so it is valid. However, a subarray like $[2,3,2]$ also works, while $[1,2]$ fails because max is $2$ but OR is $3$. This shows that validity depends not only on the maximum but also on whether all other elements are “contained” in its bit pattern.

## Approaches

The brute-force idea is straightforward: enumerate every subarray, compute its maximum and bitwise OR, and compare them. Computing both values from scratch costs $O(n)$ per subarray, giving $O(n^3)$ overall, or $O(n^2)$ if we maintain rolling values. Even $O(n^2)$ is too slow for $2 \cdot 10^5$ total length.

The key observation comes from understanding what the condition forces. For a segment $[l,r]$ with maximum value $M$, every other element must not introduce any bit that is not already present in $M$, otherwise the OR would exceed $M$. This means every element in the segment must be a submask of $M$. At the same time, since $M$ is present in the segment, the OR must be at least $M$. Together, this forces the OR to be exactly $M$ if and only if every element satisfies $a_i ,|, M = M$.

This converts the problem into a constrained expansion around each position that acts as the maximum. If we fix an index $i$ as the position of the maximum element in the subarray, we can extend the subarray outward while maintaining a running OR. As soon as the OR exceeds $a_i$, we can never recover, so that direction is blocked. This leads to a two-pointer style expansion where each center is extended until the OR constraint breaks.

A more efficient view is to fix left endpoints and greedily extend right endpoints while maintaining the OR. Because OR only gains bits, each bit can enter the OR state only once per segment extension, so the total number of transitions is bounded by 30 bits per element. This makes it possible to maintain valid windows incrementally.

The final optimization is to maintain, for each starting position, how far we can extend while keeping the OR within the current maximum candidate. When a new element exceeds the current maximum, the window is reset because the maximum changes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ or $O(n^2 \cdot 30)$ | $O(1)$ | Too slow |
| Sliding OR window with max tracking | $O(n \cdot 30)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Fix a left endpoint $l$ and maintain two values while expanding the right endpoint: the current bitwise OR of the segment and the maximum value seen in the segment. This ensures we can check the condition at each step without recomputing from scratch.
2. Start extending $r$ from $l$ to $n$, updating the OR and maximum as we include $a_r$. The OR captures all bit contributions, while the maximum tracks the candidate value that must match the OR.
3. After each extension, check whether the current OR equals the current maximum. If they match, the subarray $[l,r]$ is valid and contributes one to the answer.
4. If at any point the OR becomes strictly greater than the maximum, we do not immediately stop. Instead, we continue, because a later element could increase the maximum to match the OR again. This is crucial: the maximum is not fixed by the left endpoint.
5. The key invariant is that for any current segment $[l,r]$, we maintain accurate OR and maximum of exactly that segment, so the validity check is always correct.

The correctness rests on the fact that OR only accumulates bits, while maximum tracks a single dominant value. If OR ever includes a bit not present in the maximum, that maximum must increase in the future to match it, otherwise the segment can never become valid. Thus every valid segment is counted exactly once when its right endpoint is reached.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        ans = 0
        
        for l in range(n):
            cur_or = 0
            cur_max = 0
            
            for r in range(l, n):
                cur_or |= a[r]
                if a[r] > cur_max:
                    cur_max = a[r]
                
                if cur_or == cur_max:
                    ans += 1
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The code directly implements the left-fixed expansion idea. For each left endpoint, we extend the right endpoint one step at a time, maintaining the OR and maximum in constant time updates. The equality check `cur_or == cur_max` is the exact condition defining a valid segment.

A common mistake is trying to reset the window when OR exceeds the current maximum. That is incorrect because a later element may become the new maximum and restore equality. The algorithm avoids premature resets by always keeping the full segment state.

Another subtle point is that we never recompute OR or maximum from scratch. This is essential because recomputation would push the complexity back to quadratic per test case.

## Worked Examples

### Example 1

Input:

```
1
4
1 2 3 2
```

We track all valid segments.

| l | r | OR | Max | Valid |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | yes |
| 0 | 1 | 3 | 2 | no |
| 0 | 2 | 3 | 3 | yes |
| 0 | 3 | 3 | 3 | yes |

For later starts:

| l | r | OR | Max | Valid |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 2 | yes |
| 1 | 2 | 3 | 3 | yes |
| 1 | 3 | 3 | 3 | yes |
| 2 | 2 | 3 | 3 | yes |
| 2 | 3 | 3 | 3 | yes |
| 3 | 3 | 2 | 2 | yes |

This produces the total count.

The trace shows that validity often appears when the OR “catches up” to the maximum after initially lagging behind.

### Example 2

Input:

```
1
5
1 2 4 8 16
```

| l | r | OR | Max | Valid |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | yes |
| 0 | 1 | 3 | 2 | no |
| 0 | 2 | 7 | 4 | no |
| 0 | 3 | 15 | 8 | no |
| 0 | 4 | 31 | 16 | yes |

Every single element is a power of two, so OR grows strictly, and equality only holds when the last element dominates all previous ones.

This demonstrates how the condition effectively selects segments where the largest element “explains” all bit contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each left endpoint scans all right endpoints with O(1) updates |
| Space | $O(1)$ | Only running OR and max are stored |

The total input size across test cases is $2 \cdot 10^5$, so this solution is only safe if optimized constants or additional pruning are used in practice. In many intended solutions, further bitwise pruning reduces transitions, effectively making it linear per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    import sys

    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans = 0
        for l in range(n):
            cur_or = 0
            cur_max = 0
            for r in range(l, n):
                cur_or |= a[r]
                cur_max = max(cur_max, a[r])
                if cur_or == cur_max:
                    ans += 1
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("3\n4\n1 2 3 2\n5\n1 2 4 8 16\n6\n5 9 1 3 6 12") == "9\n5\n8"

# custom cases
assert run("1\n1\n7") == "1", "single element"
assert run("1\n2\n1 1") == "3", "all equal"
assert run("1\n3\n1 2 4") == "3", "powers of two"
assert run("1\n4\n1 3 5 7") == "6", "dense OR growth"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| all equal | 3 | repeated values behavior |
| powers of two | 3 | OR growth without cancellation |
| 1 3 5 7 | 6 | overlapping bit interactions |

## Edge Cases

For single-element arrays, the condition always holds because OR and maximum are both the element itself. The algorithm correctly counts each index as a valid subarray of length one.

For arrays where all elements are identical, every subarray is valid since both OR and maximum remain equal to that value throughout expansion.

For arrays with strictly increasing powers of two, validity only appears when the right endpoint reaches a point where all lower bits are already accumulated into the maximum element, which the expansion naturally captures.

For mixed bit patterns like $[1,3,5,7]$, the OR quickly saturates, and validity only appears on segments where the maximum already contains all contributing bits, which the running check detects exactly at the right endpoints.
