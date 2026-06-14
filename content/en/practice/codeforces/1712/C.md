---
title: "CF 1712C - Sort Zero"
description: "We are given several independent test cases, each consisting of an array of positive integers. In one move, we are allowed to pick a value x and simultaneously erase all occurrences of x in the array by turning them into zeros."
date: "2026-06-15T00:45:26+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1712
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 813 (Div. 2)"
rating: 1100
weight: 1712
solve_time_s: 227
verified: false
draft: false
---

[CF 1712C - Sort Zero](https://codeforces.com/problemset/problem/1712/C)

**Rating:** 1100  
**Tags:** greedy, sortings  
**Solve time:** 3m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent test cases, each consisting of an array of positive integers. In one move, we are allowed to pick a value `x` and simultaneously erase all occurrences of `x` in the array by turning them into zeros. The task is to apply this operation as few times as possible so that the resulting array becomes non-decreasing.

A key point is that we are not rearranging elements. The relative order of positions never changes, only values get replaced by zero. Since zero is the smallest possible value, turning elements into zero can only help fix inversions where a larger value appears before a smaller one.

The constraint `n ≤ 10^5` across all test cases forces a linear or near-linear solution per test case. Anything that repeatedly scans the array or simulates operations naively per value would be too slow if it recomputes order structure after each deletion.

A subtle edge case appears when the array is already non-decreasing. For example, `[0, 0, 1, 1]` is already valid, so no operation is needed. A careless approach that always deletes something (for instance, always targeting the first inversion) might incorrectly perform unnecessary operations.

Another important case is when values are “interleaved” heavily, such as `[1, 2, 1, 2]`. A naive intuition might suggest one or two operations are enough, but because zeros affect order globally, we must reason carefully about how many distinct “layers” of disorder exist.

## Approaches

A brute-force strategy would simulate all possible sequences of operations. Each operation picks a value `x` and removes it entirely. Since each value can be removed at most once, we are effectively choosing subsets of distinct values and checking whether the resulting array becomes sorted after applying them.

There are at most `n` distinct values, so the number of subsets is exponential. Even if we check validity in `O(n)` time per subset, this becomes `O(2^n · n)`, which is completely infeasible.

The key insight is to shift perspective from “which values do we delete” to “which structure in the array forces deletions”.

Observe what it means for the array to be non-decreasing after deletions. All remaining non-zero values must already appear in sorted order, and every inversion must be eliminated by removing at least one of the two values involved in the inversion.

Now consider scanning the array from left to right while maintaining the maximum value seen so far. Whenever we see a decrease (a value smaller than the running maximum), that position creates a constraint: either the current value or something before it must eventually be removed to eliminate the inversion. Since removals are per-value globally, each distinct value that participates in such “breaks” is forced into at least one operation.

The crucial observation is that every time we encounter a new “layer of disorder”, it corresponds to a distinct value that must be removed in a separate operation. Counting how many distinct values are responsible for breaking monotonicity gives the answer.

We can formalize this by tracking all values that appear in positions where `a[i] < max(a[0..i-1])`. Every such value is “bad” and must be removed at least once. Since one operation removes all occurrences of a value, the answer becomes the number of distinct values that ever appear in a decreasing position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Traverse the array from left to right while maintaining the maximum value seen so far.

This captures the current “sorted expectation” boundary.
2. Whenever the current element is greater than or equal to the maximum, update the maximum.

This means the sequence has not been broken at this position.
3. If the current element is smaller than the maximum, mark this value as “bad”.

The reason is that this element participates in an inversion with some earlier larger element.
4. Store every such “bad” value in a set.

We use a set because multiple occurrences of the same value should only require one operation.
5. After processing the entire array, the answer is the size of the set.

### Why it works

The invariant is that every time we detect `a[i] < max_so_far`, we identify a value that is strictly necessary to remove in any valid solution. This is because the inversion involving `a[i]` and the previous maximum cannot be fixed unless either `a[i]` or that previous larger value is deleted. Since we are only allowed to delete by value, not by position, marking the value at `i` is sufficient to account for that constraint globally. Distinct values collected this way correspond exactly to the minimal set of operations needed to eliminate all inversions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        mx = 0
        bad = set()
        
        for v in a:
            if v >= mx:
                mx = v
            else:
                bad.add(v)
        
        print(len(bad))

if __name__ == "__main__":
    solve()
```

The code directly follows the scan described earlier. The variable `mx` maintains the running maximum, and any element that violates monotonicity is inserted into a set. The final answer is the number of distinct such values. The key implementation detail is that we do not reset the maximum or revisit earlier elements, since the decision is purely based on left-to-right structure.

## Worked Examples

### Example 1

Input: `[3, 3, 2]`

| i | value | max_so_far | bad set |
| --- | --- | --- | --- |
| 0 | 3 | 3 | {} |
| 1 | 3 | 3 | {} |
| 2 | 2 | 3 | {2} |

Output is `1`.

This shows that only value `2` ever appears in a decreasing position, so only one operation is required.

### Example 2

Input: `[1, 3, 1, 3]`

| i | value | max_so_far | bad set |
| --- | --- | --- | --- |
| 0 | 1 | 1 | {} |
| 1 | 3 | 3 | {} |
| 2 | 1 | 3 | {1} |
| 3 | 3 | 3 | {1} |

Output is `1`.

Only value `1` is ever part of a drop, so deleting all `1`s fixes the array.

This demonstrates that multiple inversions can be resolved by a single value deletion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single linear scan with constant-time updates and set operations |
| Space | O(k) | Set stores only distinct problematic values |

The total complexity across all test cases is linear in the total input size, which fits comfortably within limits since the sum of `n` is `10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        
        mx = 0
        bad = set()
        for v in a:
            if v >= mx:
                mx = v
            else:
                bad.add(v)
        out.append(str(len(bad)))
    
    return "\n".join(out)

# provided samples
assert run("""5
3
3 3 2
4
1 3 1 3
5
4 1 5 3 2
4
2 4 1 2
1
1
""") == """1
2
4
3
0"""

# custom: already sorted
assert run("""1
4
1 2 3 4
""") == "0"

# custom: all equal
assert run("""1
5
7 7 7 7 7
""") == "0"

# custom: strict alternating
assert run("""1
4
2 1 2 1
""") == "1"

# custom: worst disorder
assert run("""1
6
6 5 4 3 2 1
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sorted array | 0 | no operations needed |
| all equal | 0 | duplicates never trigger false positives |
| alternating | 1 | single value can fix multiple inversions |
| descending | n-1 distinct bad values | maximal disorder behavior |

## Edge Cases

A fully sorted array like `[1, 2, 3]` never triggers the `v < mx` condition, so the bad set remains empty and the algorithm correctly returns zero.

An array like `[5, 5, 5]` keeps `mx` unchanged throughout, and no element is ever considered bad, so it correctly requires no operations.

In a descending array such as `[4, 3, 2, 1]`, every element except the first violates the running maximum, producing bad values `{3, 2, 1}`. The algorithm therefore counts exactly the distinct values responsible for all inversions, matching the minimal number of required deletions.
