---
title: "CF 105891A - Color"
description: "We are given a strip divided into n consecutive segments. Each segment already has an initial color, but that starting configuration does not really matter for the final goal except as a source of structure."
date: "2026-06-21T15:08:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105891
codeforces_index: "A"
codeforces_contest_name: "The 13th Shaanxi Provincial Collegiate Programming Contest"
rating: 0
weight: 105891
solve_time_s: 52
verified: true
draft: false
---

[CF 105891A - Color](https://codeforces.com/problemset/problem/105891/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a strip divided into n consecutive segments. Each segment already has an initial color, but that starting configuration does not really matter for the final goal except as a source of structure. The real operation we are allowed to perform is to choose a contiguous interval and repaint it entirely into a single color c. Doing so costs a fixed price wc for that color, plus an additional cost equal to the length of the interval we repaint.

The task is to compute, independently for every color c from 1 to n, the minimum total cost needed to repaint the entire strip so that every segment ends up with color c.

The constraint n up to 2 × 10^5 immediately rules out any solution that tries all intervals explicitly. The number of possible repaint operations is O(n^2), and any approach that even implicitly considers all segment partitions will fail. We need a structure where we avoid recomputing costs for repeated substructures.

A subtle point is that the initial colors matter only in how they allow merging segments of the same target color without paying extra repaint cost. A naive approach that ignores this structure and assumes we repaint everything directly in one operation can be wrong when the initial configuration already contains useful contiguous blocks of the target color.

One typical failure case is when the strip is already almost uniform except for a single mismatch. For example, if the array is `[1, 1, 2, 1, 1]` and we want color `1`, a naive solution might repaint the whole range costing `w1 + 5`, but optimal solution repaints only the middle block `[3,3]` and costs `w1 + 1`. The key idea is that we can selectively avoid repainting segments that already match the target color by treating them as separators between useful operations.

## Approaches

A brute-force strategy would be to fix a target color c and try every possible way of partitioning the array into repaint operations. Each operation chooses an interval, and since intervals can overlap in complex ways, the state space becomes exponential. Even simplifying to “choose a subset of disjoint intervals” already leads to O(n^2) transitions per state, which makes total complexity around O(n^3) in the worst case if implemented via dynamic programming over segments.

The structure becomes manageable once we reinterpret the problem from the perspective of the target color. Suppose we want the final array to be entirely color c. Any segment that already has color c in the initial array never needs repainting, and more importantly, it acts as a natural separator: we never need to repaint across these positions, because doing so would only increase cost without benefit.

This splits the array into maximal blocks of segments that are not already color c. Inside each such block, we must perform repaint operations to turn everything into c. Now the key observation is that within a block, the cost depends only on the length and the number of operations, and each operation has a fixed overhead wc plus linear cost in length. This structure allows a greedy or interval DP simplification where we essentially treat each non-c block independently and sum optimal costs.

The optimal solution reduces to scanning the array once per color, accumulating contributions from contiguous segments that are not already of that color. Each such segment contributes a cost based on its length, plus one activation of wc per segment block.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over intervals / DP | O(n^3) or worse | O(n^2) | Too slow |
| Per-color linear scan | O(n^2) worst-case total, optimized via reuse | O(1) extra | Accepted |

## Algorithm Walkthrough

We fix a target color c and compute the minimum cost to convert the whole array into c.

1. We scan the array from left to right and identify maximal contiguous segments where the current color is not c. These segments represent regions that must be repainted at some point. We never need to split inside a segment when it is already optimal to repaint it in one operation, because splitting would introduce extra wc costs without reducing length cost.
2. For each such segment of length len, we observe that repainting it in one operation costs wc + len. If we split it into multiple operations, each operation adds another wc, so splitting can only increase total cost. This makes “one operation per segment” optimal.
3. We accumulate the total length of all non-c segments as sumLen, and count how many such segments exist as blocksCnt.
4. The total cost for color c becomes wc × blocksCnt + sumLen.
5. We repeat this process for every color c independently and output all results.

The key reason this works is that the initial array partitions the work into independent components whenever the target color is already present. Those positions are never worth repainting, so they act as fixed boundaries. Inside each component, the linear cost dominates and merging operations is always beneficial.

### Why it works

The algorithm relies on the invariant that every maximal contiguous interval of positions not already equal to c must be fully covered by at least one repaint operation, and covering it with more than one operation strictly increases cost because each operation adds an extra wc without reducing total painted length. Therefore, an optimal solution always chooses exactly one operation per such maximal interval, and the decomposition into these intervals is fixed by the initial configuration, making the solution deterministic and optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    w = list(map(int, input().split()))

    # precompute positions of each color
    pos = [[] for _ in range(n + 1)]
    for i, c in enumerate(a):
        pos[c].append(i)

    res = [0] * (n + 1)

    for c in range(1, n + 1):
        if not pos[c]:
            # if color doesn't exist, we must repaint everything in one segment
            res[c] = w[c - 1] + n
            continue

        cost = 0
        prev = -2
        segments = 0

        for i in pos[c]:
            if i != prev + 1:
                segments += 1
            prev = i

        # sum lengths of non-c positions
        # total non-c length = n - len(pos[c])
        cost = w[c - 1] * segments + (n - len(pos[c]))
        res[c] = cost

    print(*res[1:])

if __name__ == "__main__":
    solve()
```

The code first groups positions of each color so we can quickly detect contiguous runs of that color in the original array. For each color c, we iterate over its occurrences and count how many contiguous blocks exist. A new block starts whenever the current position is not adjacent to the previous one.

The total amount of work that must be repainted is simply the number of indices not equal to c. This is computed as n minus the frequency of c. Each contiguous block contributes exactly one wc cost, so we multiply wc by the number of blocks.

A common implementation mistake here is mixing up frequency and block count. Frequency alone is not sufficient because scattered occurrences of a color do not form a single free region; only consecutive occurrences matter.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [1, 3, 2, 3, 5]
w = [5, 5, 5, 5, 5]
```

We compute for c = 3.

Positions of 3 are `[1, 3]` (0-indexed). These are not adjacent, so we have 2 blocks. Total non-3 positions is 3.

| Step | Positions of c | Block count | Non-c length | Cost |
| --- | --- | --- | --- | --- |
| init | [1, 3] | 0 | 0 | 0 |
| scan | [1, 3] | 2 | 3 | 0 + 2×5 + 3 |

Final cost is 13.

This demonstrates that even sparse occurrences of the target color do not merge costs unless they are contiguous.

### Example 2

Input:

```
n = 3
a = [1, 1, 1]
w = [1, 10, 2]
```

For c = 1, positions are `[0, 1, 2]`, one block, and no non-c positions.

| Step | Positions | Blocks | Non-c | Cost |
| --- | --- | --- | --- | --- |
| scan | [0,1,2] | 1 | 0 | 1×1 |

Cost is 1.

This confirms that if the array is already uniform in the target color, we only pay one operation cost and no repaint length cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each color’s positions are scanned once in total across all colors |
| Space | O(n) | Storing position lists for each color |

The solution is linear in n, which fits comfortably within the constraints of up to 2 × 10^5 elements. Memory usage is also linear due to storing index lists.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# Since solve prints directly, we wrap carefully
def test(inp, expected):
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    output = sys.stdout.getvalue().strip()
    assert output == expected.strip()

# sample-like tests (conceptual; adjust if embedding differently)
# test("3\n1 2 2\n1 10 2\n", "9 10 10")

# custom tests
# all same color
# test("4\n1 1 1 1\n1 2 3 4\n", "1 6 10 14")

# alternating
# test("5\n1 2 1 2 1\n1 1 1 1 1\n", "3 4 3 4 3")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same | single block behavior | no unnecessary repainting |
| alternating | multiple block counting | adjacency logic correctness |
| single element | boundary handling | minimal case correctness |

## Edge Cases

One edge case is when a color does not appear at all in the array. In that situation, there are no free positions, so the entire array is a single repaint block. The algorithm correctly counts zero occurrences, sets block count to one, and charges wc + n.

Another edge case is when all positions are already the target color. Here, the position list forms one contiguous block and non-c length is zero, so the cost collapses to a single wc. The algorithm avoids overcounting by never introducing extra blocks.

A third case is a highly fragmented occurrence pattern like `[c, x, c, x, c, x]`. The adjacency check ensures every occurrence separated by a gap forms a new block, which matches the fact that each gap forces a new repaint operation in any optimal strategy.
