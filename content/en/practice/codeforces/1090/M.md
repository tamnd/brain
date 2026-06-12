---
title: "CF 1090M - The Pleasant Walk"
description: "We are given a line of houses, each painted with an integer color. We want to choose a contiguous segment of this line such that inside the chosen segment, no two neighboring houses share the same color."
date: "2026-06-13T04:03:49+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1090
codeforces_index: "M"
codeforces_contest_name: "2018-2019 Russia Open High School Programming Contest (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1000
weight: 1090
solve_time_s: 256
verified: true
draft: false
---

[CF 1090M - The Pleasant Walk](https://codeforces.com/problemset/problem/1090/M)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 4m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of houses, each painted with an integer color. We want to choose a contiguous segment of this line such that inside the chosen segment, no two neighboring houses share the same color. Among all such valid segments, we are asked to maximize the number of houses in the segment.

The input is simply an array of colors. The output is the length of the longest contiguous subarray where every adjacent pair of elements differs.

The constraints immediately guide the design space. With up to 100,000 houses, any solution that tries all subarrays and checks validity from scratch would involve on the order of $n^2$ segments and potentially $O(n)$ verification per segment, which is far beyond what fits in a one second limit. We are therefore looking for a linear scan or a two-pointer style solution that processes each element a constant number of times.

A subtle edge case appears when the array alternates perfectly, such as `1 2 1 2 1`. The correct answer is the full length. A naive approach that restarts too aggressively might incorrectly truncate the segment. Another edge case is a fully uniform array like `5 5 5 5`, where every valid segment has length 1. Any solution must correctly reset on every violation.

## Approaches

A brute-force strategy would enumerate every possible starting position and extend the segment to the right while maintaining the constraint that adjacent elements differ. For each starting index $i$, we scan forward until we find an index $j$ such that $a[j] = a[j-1]$, then record the length $j - i$.

This is correct because it directly constructs all maximal valid segments. However, in the worst case where all elements are distinct or alternating, each starting position runs nearly to the end, giving roughly $n + (n-1) + \dots + 1 = O(n^2)$ operations. With $n = 100000$, this is on the order of $10^{10}$, which is not feasible.

The key observation is that validity depends only on local adjacency. Once we encounter a pair of equal neighbors, any segment crossing that boundary becomes invalid. This means the array is naturally partitioned into maximal blocks where adjacent elements are always different. Inside each block, the entire block is valid, so we only need the maximum block length.

This reduces the problem to a single linear scan where we track the current streak length of valid adjacency and reset it whenever we encounter equality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a running length of the current valid segment ending at each position.

1. Start with the first house. The current valid segment length is 1 because a single element is always valid.
2. Iterate through the array from left to right starting at index 1. At each position, compare the current color with the previous one.
3. If the current color differs from the previous color, we can extend the current valid segment by 1. This is safe because the only condition is adjacency, and we have just verified the new adjacency is valid.
4. If the current color is the same as the previous one, the valid segment is broken at this point. We reset the current segment length to 1 because a new segment can start from this position.
5. Keep track of the maximum segment length seen during the scan.

The answer is the maximum value reached by this running length.

### Why it works

At any position, the algorithm maintains the length of the longest valid segment ending exactly at that position. This works because the only constraint involves adjacent elements. As long as the last adjacent pair is valid, all earlier pairs in the current window were already validated when the window was extended. When a violation occurs, no valid segment can cross it, so restarting at that index preserves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    best = 1
    cur = 1

    for i in range(1, n):
        if a[i] != a[i - 1]:
            cur += 1
        else:
            cur = 1
        if cur > best:
            best = cur

    print(best)

if __name__ == "__main__":
    solve()
```

The solution reads the array and maintains two variables. The variable `cur` tracks the length of the current valid segment ending at index `i`. The variable `best` stores the maximum such value across all positions.

The transition is straightforward. When consecutive elements differ, we extend `cur`. When they match, we reset. The important implementation detail is that the reset must set `cur` to 1, not 0, because a single element always forms a valid segment by itself.

The answer is updated after every step to ensure we capture the best segment anywhere in the array.

## Worked Examples

### Example 1

Input:

```
8
1 2 3 3 2 1 2 2
```

| i | a[i] | a[i-1] | cur | best |
| --- | --- | --- | --- | --- |
| 0 | 1 | - | 1 | 1 |
| 1 | 2 | 1 | 2 | 2 |
| 2 | 3 | 2 | 3 | 3 |
| 3 | 3 | 3 | 1 | 3 |
| 4 | 2 | 3 | 2 | 3 |
| 5 | 1 | 2 | 3 | 3 |
| 6 | 2 | 1 | 4 | 4 |
| 7 | 2 | 2 | 1 | 4 |

This trace shows how the segment is continuously extended until a repetition breaks it at index 3, after which a new segment begins. The longest valid stretch occurs just before the final repetition.

### Example 2

Input:

```
5
5 5 5 5 5
```

| i | a[i] | a[i-1] | cur | best |
| --- | --- | --- | --- | --- |
| 0 | 5 | - | 1 | 1 |
| 1 | 5 | 5 | 1 | 1 |
| 2 | 5 | 5 | 1 | 1 |
| 3 | 5 | 5 | 1 | 1 |
| 4 | 5 | 5 | 1 | 1 |

Every adjacency breaks immediately, so the best segment never exceeds length 1. This confirms the reset logic behaves correctly on uniform arrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant-time comparison and update |
| Space | O(1) | Only a few counters are used regardless of input size |

The linear scan fits comfortably within the constraints for 100,000 elements, and constant memory usage avoids any overhead concerns.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("8 3\n1 2 3 3 2 1 2 2\n") == "4"

# all distinct
assert run("5 5\n1 2 3 4 5\n") == "5"

# all equal
assert run("4 2\n7 7 7 7\n") == "1"

# alternating
assert run("6 2\n1 2 1 2 1 2\n") == "6"

# single element
assert run("1 10\n5\n") == "1"

# break in middle
assert run("7 3\n1 2 2 3 4 4 5\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4 5 | 5 | strictly increasing validity |
| 7 7 7 7 | 1 | full reset behavior |
| 1 2 1 2 1 2 | 6 | full alternating valid segment |
| 1-element case | 1 | boundary condition correctness |
| 2 2 split cases | 3 | handling multiple breaks |

## Edge Cases

A fully uniform array such as `5 5 5 5` causes a reset at every step. The algorithm processes it as a sequence of independent length-1 segments, always updating `best` to 1 and never incorrectly merging across invalid boundaries.

An alternating array such as `1 2 1 2 1 2` never triggers a reset. The running length grows continuously to 6, confirming that repeated valid transitions are accumulated correctly without artificial truncation.

A case with clustered duplicates like `1 2 2 3 4 4 5` demonstrates alternating growth and resets. The scan produces segment lengths `2`, then reset, then `3`, showing that the algorithm correctly isolates maximal valid stretches without needing explicit segmentation logic.
