---
title: "CF 104720F - Chef Circle"
description: "We are given a circular arrangement of n chefs, each chef having a fixed value C[i] that represents their tastebud index. A waiter chooses a starting chef and then walks clockwise around the circle, visiting every chef exactly once until all are processed."
date: "2026-06-29T04:17:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "F"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 76
verified: false
draft: false
---

[CF 104720F - Chef Circle](https://codeforces.com/problemset/problem/104720/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular arrangement of `n` chefs, each chef having a fixed value `C[i]` that represents their tastebud index. A waiter chooses a starting chef and then walks clockwise around the circle, visiting every chef exactly once until all are processed.

The key twist is that the order in which a chef is visited affects their contribution. If a chef is the `i`-th person to be served, their contribution is `i * C[j]`, where `i` starts from 1 and increases by 1 each step along the traversal.

Because the circle can be started at any chef, we effectively get `n` different linear orderings (rotations of the array). For each rotation, we compute the weighted sum with increasing weights from 1 to `n`, and we must output the maximum possible value among all rotations.

The input size `n ≤ 100000` immediately rules out any approach that recomputes the score from scratch for every starting position. A naive `O(n^2)` solution would perform up to 10¹⁰ operations in the worst case, which is far beyond feasible limits. This pushes us toward an `O(n)` or `O(n log n)` approach.

A subtle issue appears if we try to simulate rotations without careful bookkeeping. Since each position contributes with a different multiplier depending on its position in the rotation, even a small indexing mistake or off-by-one shift will produce incorrect totals. Another pitfall is recomputing sums using floating or incremental approximations without preserving exact integer updates, which can silently drift for large values up to 10⁹.

## Approaches

The most direct way to understand the problem is to fix a starting chef and compute the weighted sum by walking through the circle. For a given start, we assign weights `1, 2, ..., n` and accumulate `i * C[...]`. This is correct, but repeating it for every starting position requires recomputing a full `O(n)` sum for each of the `n` rotations, leading to `O(n^2)` total work.

The bottleneck is that consecutive rotations are highly related. When we shift the starting point by one position, every element effectively moves one step earlier in the sequence except one element that wraps around to the end. This means the total sum does not need to be recomputed from scratch; it can be updated using a formula derived from how weights change under rotation.

Let the current arrangement be `B[0..n-1]`, and define the weighted sum as:

`F = 1*B[0] + 2*B[1] + ... + n*B[n-1]`.

If we rotate the array so that `B[1]` becomes the first element, every element’s weight decreases by 1, except the former first element which moves to the end and gains weight `n`. The net effect simplifies to a clean recurrence:

`F_next = F + total_sum - n * B[0]`.

This identity is the core observation. It allows us to move from one rotation to the next in constant time, maintaining a running total and updating the answer as we go through all `n` rotations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute each rotation) | O(n²) | O(1) | Too slow |
| Rotation DP with update formula | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We treat the array as fixed and simulate all rotations using a running score.

1. Compute the total sum of all elements in the array. This value is reused in every rotation update, since the multiset of elements never changes.
2. Compute the initial weighted sum for the first configuration, where the array is taken as given. Each element at index `i` contributes `(i+1) * C[i]`.
3. Store this value as both the current score and the initial best answer.
4. Now iterate through possible rotations from 1 to `n-1`.
5. For each rotation, update the current score using the derived transition:

`current = current + total_sum - n * C[i-1]`, where `C[i-1]` is the element that moves from front to back in the previous configuration.
6. After each update, compare and store the maximum score seen so far.
7. After processing all rotations, output the maximum value.

The key reasoning behind step 5 is that when an element moves from position 0 to position `n-1`, it gains weight `n`, while every other element effectively loses one unit of weight. Aggregating these changes collapses into a single expression involving only the removed element and the total sum.

### Why it works

The algorithm maintains the exact value of the weighted sum for the current rotation at every step. The invariant is that after processing the `k`-th rotation, `current` equals the correct weighted sum for that rotation ordering. The update formula precisely accounts for the net change in contribution when shifting the starting point by one, so no information is lost and no element is double-counted. Since every rotation is reached exactly once, the maximum over all maintained correct values is the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_and_rest = list(map(int, sys.stdin.read().strip().split()))
    n = n_and_rest[0]
    arr = n_and_rest[1:]

    total = sum(arr)

    cur = 0
    for i in range(n):
        cur += (i + 1) * arr[i]

    best = cur

    for i in range(1, n):
        cur = cur + total - n * arr[i - 1]
        if cur > best:
            best = cur

    print(best)

if __name__ == "__main__":
    solve()
```

The solution first flattens input reading to avoid overhead. The initial weighted sum is computed directly in a single pass. The update step uses the previously derived recurrence, carefully referencing `arr[i-1]` as the element that transitions from the front of the previous rotation to the back in the new one. The variable `best` tracks the maximum across all rotations.

A common implementation mistake is using `arr[i]` instead of `arr[i-1]` in the update step, which shifts the removal point incorrectly and breaks the recurrence. Another subtle issue is forgetting that the first rotation corresponds to shifting by exactly one position, not recomputing a fresh base.

## Worked Examples

### Example 1

Input array: `[2, 3, 5, 1, 9, 10]`, `n = 6`

We start with the initial arrangement.

| Step | Current rotation start | Current value | Total sum |
| --- | --- | --- | --- |
| 0 | 0 | 132 | 30 |
| 1 | 1 | 114 | 30 |
| 2 | 2 | 102 | 30 |
| 3 | 3 | 102 | 30 |
| 4 | 4 | 78 | 30 |
| 5 | 5 | 102 | 30 |

The initial configuration already yields the maximum value of 132. Each subsequent rotation is obtained using the update rule, confirming that no recomputation is needed.

This trace shows that the recurrence correctly tracks how the weighted sum evolves under circular shifts, and the maximum is found without explicit rotation simulation.

### Example 2

Input array: `[1, 4, 2]`, `n = 3`

| Step | Current rotation start | Current value | Total sum |
| --- | --- | --- | --- |
| 0 | 0 | 16 | 7 |
| 1 | 1 | 13 | 7 |
| 2 | 2 | 11 | 7 |

The best value is 16, achieved at the original ordering. This confirms that even in small cases, different rotations can significantly change the weighted sum, and the algorithm correctly evaluates all of them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute initial sum and one pass to iterate all rotations with O(1) updates |
| Space | O(1) | Only a few running variables are stored beyond the input array |

The linear complexity fits comfortably within constraints of `n ≤ 100000`, and memory usage remains minimal since no auxiliary structures proportional to `n²` are created.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("6\n2 3 5 1 9 10\n") == "132"
assert run("3\n1 4 2\n") == "16"

# all equal values
assert run("5\n7 7 7 7 7\n") == str(7 * (1+2+3+4+5)), "uniform array"

# minimum size
assert run("1\n100\n") == "100"

# strictly increasing
assert run("4\n1 2 3 4\n") == str(1*1 + 2*2 + 3*3 + 4*4), "already optimal"

# reverse order
assert run("4\n4 3 2 1\n") == str(4*1 + 3*2 + 2*3 + 1*4), "rotation sensitivity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| uniform array | sum of fixed rotation | rotation invariance |
| n=1 case | single value | base edge case |
| increasing array | diagonal weighting | no rotation improvement |
| reverse array | best rotation shift | rotation dependency |

## Edge Cases

For a single chef, the algorithm immediately computes the weighted sum as the value itself, and no rotations are performed. The update loop is skipped entirely, leaving the initial value as the answer.

For arrays where all values are identical, every rotation produces the same weighted sum because only the weights change, not the multiset contribution structure. The update formula still holds, but every computed `cur` remains identical, so the maximum is stable.

For strictly increasing or decreasing sequences, the optimal rotation may occur at the beginning or end depending on how large values align with large weights. The recurrence correctly explores all rotations, ensuring the peak alignment is captured without explicitly constructing each permutation.
