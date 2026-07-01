---
title: "CF 104308A - Rain Rain Go Away, Come Again Another Day!"
description: "The input describes several independent “landscapes” made of vertical stacks of unit-width bricks. Each landscape is an array where the value at position i represents how tall the wall is at that point. When rain falls, water can accumulate in the gaps between taller walls."
date: "2026-07-01T20:01:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104308
codeforces_index: "A"
codeforces_contest_name: "Mirror of Independence Day Programming Contest 2023 by MIST Computer Club"
rating: 0
weight: 104308
solve_time_s: 63
verified: true
draft: false
---

[CF 104308A - Rain Rain Go Away, Come Again Another Day!](https://codeforces.com/problemset/problem/104308/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes several independent “landscapes” made of vertical stacks of unit-width bricks. Each landscape is an array where the value at position `i` represents how tall the wall is at that point.

When rain falls, water can accumulate in the gaps between taller walls. Water is only trapped when there are higher or equal walls on both the left and right side of a position, because otherwise it would flow out.

For each test case, the task is to compute the total volume of water that remains trapped after rain across the entire structure.

The constraints imply up to 10,000 test cases, but the total number of positions across all cases is at most 20,000. That single bound is the key: any solution close to linear per test case would already be too slow, but a linear scan per element overall is acceptable. Anything quadratic per test case would be far beyond limits.

A few edge cases matter for correctness.

A strictly increasing array like `[1, 2, 3, 4]` traps no water, because every position has no left boundary taller than itself. The answer must be 0.

A strictly decreasing array like `[4, 3, 2, 1]` also traps no water for the same reason, but a naive algorithm that only looks at one side maxima without proper pairing can incorrectly count negative or partial contributions if implemented carelessly.

Flat arrays like `[2, 2, 2, 2]` also trap no water. Some incorrect implementations accidentally treat equal boundaries as trapping space if they use strict inequalities instead of inclusive maxima.

Finally, single-element or empty-structure-like cases such as `[5]` must return 0 since no container can form.

## Approaches

The direct way to compute trapped water is to inspect each position independently and determine how much water sits above it. For a given index `i`, the water level is limited by the tallest wall to its left and the tallest wall to its right. If we denote those as `L[i]` and `R[i]`, then the water above position `i` is `max(0, min(L[i], R[i]) - h[i])`.

A brute-force implementation computes `L[i]` and `R[i]` by scanning left and right for every index. This is correct because it explicitly reconstructs the constraints on each position. However, each index requires O(n) work to recompute its boundaries, leading to O(n²) per test case. With total `n` up to 2×10⁴, this worst-case behavior becomes too slow in a tight 1-second limit if test cases are adversarially distributed.

The key observation is that the left and right maxima do not need to be recomputed repeatedly. They can be precomputed once. Once we have prefix maxima and suffix maxima arrays, each position can be evaluated in O(1), reducing the problem to a linear scan. Even further optimization removes auxiliary arrays entirely by using a two-pointer technique that maintains running maxima from both ends, ensuring each element is processed once.

The two-pointer method works because the limiting factor for trapped water at any position is always the smaller of the best boundaries seen so far from either side. By always advancing the side with the smaller boundary, we guarantee that the decision at that step is final and cannot be improved later.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Prefix/Suffix Arrays | O(n) | O(n) | Accepted |
| Two Pointers | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We use a two-pointer strategy with running maxima.

1. Initialize two pointers `l = 0` and `r = n - 1`, and two variables `left_max = 0` and `right_max = 0`. These represent the best boundary seen so far from each side.
2. While `l < r`, compare `h[l]` and `h[r]`. The side with the smaller height determines the next computation.
3. If `h[l] <= h[r]`, we process position `l`. The reason is that the right boundary is already guaranteed to be at least `h[l]`, so the limiting factor is `left_max`. If `h[l] >= left_max`, we update `left_max`. Otherwise, water accumulates at `left_max - h[l]`. Then increment `l`.
4. Otherwise, we process position `r` symmetrically. If `h[r] >= right_max`, update `right_max`. Otherwise, add `right_max - h[r]`. Then decrement `r`.
5. Accumulate all contributions during the sweep.

At every step, we always finalize the water contribution for one boundary without needing future information, because the opposite side is guaranteed to be tall enough to form a cap for that index.

### Why it works

The invariant is that at any moment, all positions strictly outside the current `[l, r]` window have already been fully processed with correct boundary constraints. The decision to process the smaller side ensures that for the chosen index, the opposite boundary is at least as large as the height being processed, so the only unknown limiting factor is the running maximum on the processed side. This prevents any later adjustment from changing the computed water level.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))

        l, r = 0, n - 1
        left_max, right_max = 0, 0
        water = 0

        while l < r:
            if h[l] <= h[r]:
                if h[l] >= left_max:
                    left_max = h[l]
                else:
                    water += left_max - h[l]
                l += 1
            else:
                if h[r] >= right_max:
                    right_max = h[r]
                else:
                    water += right_max - h[r]
                r -= 1

        out.append(str(water))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code maintains two pointers that shrink toward the center. At each step, it processes the smaller boundary first because that side’s water level is already fully determined by the best boundary seen so far. The running maxima ensure we never recompute scans over the array, and the accumulated `water` variable collects contributions immediately.

A common implementation mistake is to compare `h[l]` and `h[r]` but forget to maintain separate maxima, which leads to undercounting when interior peaks appear. Another issue is updating pointers before using the current height, which shifts the logic by one index and silently corrupts the result.

## Worked Examples

### Example 1

Input:

```
h = [0, 1, 0, 2, 1, 0]
```

| l | r | h[l] | h[r] | left_max | right_max | action | water |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 5 | 0 | 0 | 0 | 0 | process l | 0 |
| 1 | 5 | 1 | 0 | 1 | 0 | process r | 0 |
| 1 | 4 | 1 | 1 | 1 | 1 | process r | 0 |
| 1 | 3 | 1 | 2 | 1 | 1 | process l | 0 |
| 2 | 3 | 0 | 2 | 1 | 1 | process l | 1 |
| 3 | 3 | - | - | - | - | stop | 1 |

This trace shows that water is only added when a position is strictly below a maintained boundary. The algorithm never re-evaluates earlier positions, confirming the single-pass property.

### Example 2

Input:

```
h = [3, 0, 2, 0, 4]
```

| l | r | h[l] | h[r] | left_max | right_max | action | water |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 4 | 3 | 4 | 3 | 0 | process l | 0 |
| 1 | 4 | 0 | 4 | 3 | 0 | process l | 3 |
| 2 | 4 | 2 | 4 | 3 | 0 | process l | 3 |
| 3 | 4 | 0 | 4 | 3 | 0 | process l | 6 |

The second example highlights how repeated low valleys accumulate water based purely on the left boundary until the right side becomes relevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case, O(total n) overall | each index is processed once by one pointer move |
| Space | O(1) | only a few running variables are used |

The total input size is only 2×10⁴, so a linear scan over all elements easily fits within the time limit. Memory usage remains constant regardless of input size, which is optimal for this problem.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            h = list(map(int, input().split()))
            l, r = 0, n - 1
            left_max, right_max = 0, 0
            water = 0
            while l < r:
                if h[l] <= h[r]:
                    if h[l] >= left_max:
                        left_max = h[l]
                    else:
                        water += left_max - h[l]
                    l += 1
                else:
                    if h[r] >= right_max:
                        right_max = h[r]
                    else:
                        water += right_max - h[r]
                    r -= 1
            out.append(str(water))
        return "\n".join(out)

    return solve()

# provided sample (implicit from statement formatting)
assert run("1\n12\n0 1 0 2 1 0 1 3 2 1 2 1\n") == "6"

# minimum size
assert run("1\n1\n5\n") == "0"

# all equal
assert run("1\n4\n2 2 2 2\n") == "0"

# increasing
assert run("1\n5\n1 2 3 4 5\n") == "0"

# decreasing
assert run("1\n5\n5 4 3 2 1\n") == "0"

# valley case
assert run("1\n5\n3 0 3 0 3\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | base case correctness |
| all equal | 0 | no false trapping on flat terrain |
| increasing | 0 | no left boundary formation |
| decreasing | 0 | no right boundary formation |
| symmetric valleys | 6 | correct accumulation across multiple pits |

## Edge Cases

For a single element input like `[7]`, the algorithm sets both pointers at the same index and immediately terminates without processing, producing 0. No boundary is formed, so no water can be counted.

For a flat structure like `[4, 4, 4, 4]`, both `left_max` and `right_max` are updated immediately to 4, and every comparison finds no gap below a boundary. The accumulated water remains 0 throughout, matching the expected physical interpretation.

For a strictly increasing sequence, the left pointer side always updates `left_max` at each step before any deficit is detected. Since no element is ever below its running maximum, no water is added. The same logic applies symmetrically for strictly decreasing sequences, where the right pointer dominates and prevents accumulation on that side.
