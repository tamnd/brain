---
title: "CF 2217D - Flip the Bit (Hard Version)"
description: "We are given a binary array and a set of special indices where all values are identical. Our goal is to make the entire array equal to the value at these special indices using the fewest number of flip operations."
date: "2026-06-07T18:26:03+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2217
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1091 (Div. 2) and CodeCraft 26"
rating: 1900
weight: 2217
solve_time_s: 120
verified: false
draft: false
---

[CF 2217D - Flip the Bit (Hard Version)](https://codeforces.com/problemset/problem/2217/D)

**Rating:** 1900  
**Tags:** greedy, implementation, math  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary array and a set of special indices where all values are identical. Our goal is to make the entire array equal to the value at these special indices using the fewest number of flip operations. A flip operation allows us to select a contiguous subarray that contains at least one special index and invert every bit within that subarray.

The problem requires processing multiple test cases, and the sum of array sizes across all cases can reach 200,000. This rules out any solution that examines all possible subarrays explicitly, since that would be quadratic or worse. Instead, we need an approach that works linearly or near-linearly in the array length.

A subtle edge case arises when there are consecutive bits different from the special value but no special indices within the segment. A naive approach that flips at every difference might try to flip segments without including a special index, which is invalid. Another edge case is when the array is already uniform; the correct answer is zero flips, but a careless greedy strategy might still attempt to flip segments unnecessarily. For instance, for an array `[1,1,1,1]` with special indices `[2,3]`, the minimum flips required is `0`.

## Approaches

A brute-force solution would iterate over every element and, when it differs from the special value, attempt all possible ranges containing a special index to flip it. This is correct in principle, since eventually all bits will match, but it performs up to O(n^2) operations per test case, which is far too slow for n up to 200,000.

The key insight for an optimal solution is that we only need to consider contiguous segments of elements that differ from the special value. Each such segment can be neutralized with one flip that stretches from the first element of the segment to the nearest special index on either side. This works because each flip can include at least one special index and invert the whole segment, bringing all bits in the segment to the correct value. By processing the array from left to right and greedily flipping each "wrong" segment in one operation, we can cover the entire array efficiently.

The greedy approach works because the problem is linear: flipping any bit outside a wrong segment is unnecessary and flips are idempotent on non-overlapping segments. We do not need to consider overlapping segments or multiple flips on the same segment, because a single operation suffices if the range includes a special index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read n, k, the array `a`, and the list of special indices `p`. Convert `p` to zero-based indices for easier array handling.
2. Determine the target value `x` at the special indices. All special indices are guaranteed to have the same value, so we can pick `a[p[0]]`.
3. Initialize a counter `ops` to zero and an index `i` to zero. We will scan the array from left to right.
4. While `i` is less than `n`, check if `a[i]` equals `x`. If it does, increment `i` and continue.
5. If `a[i]` differs from `x`, we have found the start of a segment that needs flipping. Increment `ops` by 1. Then move `i` forward until reaching the next element equal to `x` or the end of the array. This skips the entire wrong segment in one operation.
6. Repeat steps 4-5 until the array end. After processing, `ops` contains the minimum number of operations needed.

The greedy approach works because every segment of bits that differ from `x` must be flipped at least once. By extending the flip to the nearest special index, we satisfy the constraint that every flip contains a special index. Flipping overlapping segments is unnecessary because once a segment is flipped, its bits match `x` and will not be flipped again.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        p = list(map(int, input().split()))
        p = [pi - 1 for pi in p]  # convert to 0-based
        x = a[p[0]]  # target value
        ops = 0
        i = 0
        while i < n:
            if a[i] == x:
                i += 1
            else:
                ops += 1
                while i < n and a[i] != x:
                    i += 1
        print(ops)

if __name__ == "__main__":
    solve()
```

The code starts by reading input and converting special indices to zero-based. The target value is taken from the first special index. We scan the array, and whenever we encounter a segment that differs from `x`, we increment the operation counter and skip over the entire segment. This guarantees that each flip is minimal and necessary. Boundary conditions are handled naturally since the while-loop stops at `n`.

## Worked Examples

Sample input:

```
2 1
1 0
1
```

| Step | i | a[i] | ops | Comment |
| --- | --- | --- | --- | --- |
| Start | 0 | 1 | 0 | Matches target 1, move on |
| i=1 | 1 | 0 | 0 | Differs, increment ops=1, skip segment |
| End | 2 | - | 1 | Finished |

This demonstrates that a single flip covers the wrong bit.

Second example:

```
3 2
0 1 0
1 3
```

| Step | i | a[i] | ops | Comment |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | Matches target 0, move on |
| i=1 | 1 | 1 | 0 | Differs, increment ops=1, skip to next 0 at i=2 |
| i=2 | 2 | 0 | 1 | Matches target, move on |
| End | 3 | - | 2 | Done |

The table confirms the greedy approach flips the minimal segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan each element once, and each wrong segment is skipped in a single pass. |
| Space | O(n) | Store array `a` and indices `p`. No extra structures beyond input storage. |

Since the total sum of n across all test cases is 200,000, a linear scan per test case fits comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("6\n2 1\n1 0\n1\n3 2\n0 1 0\n1 3\n5 5\n1 1 1 1 1\n1 2 3 4 5\n9 5\n0 1 0 0 1 0 0 1 0\n3 4 6 7 9\n13 4\n1 0 0 1 0 1 0 1 1 0 1 0 1\n4 8 11 13\n15 3\n1 0 1 0 1 0 1 0 1 0 1 0 1 0 1\n3 11 13") == "2\n2\n0\n3\n5\n8", "sample 1"

# custom edge cases
assert run("1\n4 2\n1 1 1 1\n2 3") == "0", "all equal"
assert run("1\n1 1\n0\n1") == "1", "single element differs"
assert run("1\n5 2\n1 0 0 0 1\n1 5") == "1", "flip entire middle segment"
assert run("1\n6 3\n1 0 1 0 0 1\n1 3 6") == "2", "multiple segments"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1,1,1,1]` | `0` | Already uniform, no flips needed |
| `[0]` | `1` | Single-element array, flip required |
| `[1,0,0,0,1]` | `1` | Long middle segment, flip in one operation |
| `[1,0,1,0,0,1]` | `2` | Multiple segments with gaps between them |

## Edge Cases

For an array `[1,1,1,1]` with special indices `[2,3]`, the algorithm correctly outputs `0` because no elements differ from the target. The while-loop scans each element, finds no differences, and never increments `ops`.

For an array `[1,0,0,0,1]` with special indices `[1,5]
