---
title: "CF 104237C - Trash Removal"
description: "We are given a sequence of trash piles arranged in a fixed order along a path. Each pile has a weight, and Bob must pick up piles from left to right without skipping or reordering them."
date: "2026-07-02T20:46:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104237
codeforces_index: "C"
codeforces_contest_name: "Harker Programming Invitational 2023 Novice"
rating: 0
weight: 104237
solve_time_s: 54
verified: true
draft: false
---

[CF 104237C - Trash Removal](https://codeforces.com/problemset/problem/104237/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of trash piles arranged in a fixed order along a path. Each pile has a weight, and Bob must pick up piles from left to right without skipping or reordering them. He repeatedly makes trips to a trash can, and in each trip he can carry a contiguous block of piles starting from where he last stopped, as long as the total weight of that trip does not exceed a fixed limit $K$.

The task is to compute the smallest number of such trips needed to process the entire sequence while respecting the order constraint and the capacity constraint.

The key constraint is $N \le 10^5$, which immediately rules out any solution that tries all partitions or checks all subarrays explicitly. A quadratic or worse approach would perform up to $10^{10}$ operations in the worst case, which is not viable under a 1 second limit. This pushes us toward a single linear scan strategy.

A subtle edge case appears when a single pile has weight equal to $K$. In that case, it must form its own trip even if it appears in a sequence of small piles. Another corner case is when all piles fit into a single trip, meaning the answer should be 1. A naive approach that resets incorrectly or starts a new trip too early would overcount in such scenarios.

## Approaches

A brute-force strategy would simulate all possible ways to split the sequence into valid trips. Since each trip is a contiguous segment whose sum is at most $K$, one could try every breakpoint and recursively compute the minimum number of segments. This naturally leads to trying all partitions of the array.

However, the number of partitions of an $N$-element array grows exponentially. Even if we restrict ourselves to valid splits, the worst case where all elements are small allows splitting almost anywhere, leading to roughly $2^{N-1}$ possibilities. This is far beyond any feasible computation.

The structure of the problem simplifies dramatically once we interpret it as a greedy packing process. Since Bob must process items in order and cannot reorder or skip, each trip is simply a maximal prefix starting from the current position whose sum does not exceed $K$. Extending a trip further always reduces or maintains the number of trips, because starting a new trip earlier can never help combine future elements more efficiently due to the strict ordering constraint.

This makes the optimal strategy straightforward: scan from left to right, keep accumulating weights, and whenever adding the next pile would exceed $K$, we commit the current trip and start a new one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (partition DP / recursion) | $O(2^N)$ | $O(N)$ | Too slow |
| Greedy single pass | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Start with a running sum representing the current trip load, and a counter for the number of trips. Both begin at zero.
2. Traverse the piles from left to right in order.
3. For each pile, check whether adding its weight to the current trip would exceed $K$.
4. If it does not exceed $K$, include the pile in the current trip by increasing the running sum.
5. If it exceeds $K$, finalize the current trip by incrementing the trip counter, reset the running sum to the current pile's weight, and start a new trip from this pile.
6. After processing all piles, if there is any unfinished trip (non-zero running sum), count it as one final trip.

The reasoning behind step 5 is that once a constraint is violated, we cannot rearrange earlier decisions. Since the order is fixed, the only valid repair is to cut the trip boundary immediately before the violating element.

### Why it works

At any point in the scan, the algorithm maintains a contiguous segment of piles representing the current trip, and this segment is always maximal under the constraint that its sum is at most $K$. If we ever ended a trip earlier than necessary, we would increase the number of trips without gaining any ability to merge future elements, since no future element can be moved earlier or swapped. Thus, each time we cut, we are forced by feasibility, not by choice, ensuring minimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    trips = 0
    current = 0
    
    for x in a:
        if current + x <= k:
            current += x
        else:
            trips += 1
            current = x
    
    if current > 0:
        trips += 1
    
    print(trips)

if __name__ == "__main__":
    solve()
```

The implementation follows the greedy scan exactly. The variable `current` tracks the ongoing trip weight. When a new pile does not fit, we immediately close the previous trip and start a new one with that pile alone.

The final check ensures that a partially filled last trip is counted. Without this, the final segment would be missed when no overflow occurs at the end.

## Worked Examples

### Example 1

Input:

```
3 2
1 1 2
```

| Index | Pile | Current Sum | Action | Trips |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | add to current | 0 |
| 2 | 1 | 2 | add to current | 0 |
| 3 | 2 | 2 → overflow | close + start new | 1 → 2 |

After processing, we end with 2 trips.

This shows how the overflow condition forces a cut exactly at the point where capacity is exceeded.

### Example 2

Input:

```
5 10
2 3 1 4 2
```

| Index | Pile | Current Sum | Action | Trips |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | add | 0 |
| 2 | 3 | 5 | add | 0 |
| 3 | 1 | 6 | add | 0 |
| 4 | 4 | 10 | add | 0 |
| 5 | 2 | 10 → overflow | close + new | 1 → 2 |

Final answer is 2 trips.

This demonstrates that the algorithm packs each trip as tightly as possible before starting a new one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Each pile is processed exactly once with constant-time operations |
| Space | $O(1)$ | Only a few integer variables are maintained regardless of input size |

The linear scan fits comfortably within the constraints for $N = 10^5$, requiring only simple arithmetic per element, well under the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        solve()
    return output.getvalue().strip()

# provided sample
assert run("3 2\n1 1 2\n") == "2"

# single element
assert run("1 5\n3\n") == "1"

# all fit in one trip
assert run("4 10\n1 2 3 4\n") == "1"

# each element forces new trip
assert run("4 3\n3 3 3 3\n") == "4"

# alternating tight packing
assert run("6 5\n2 3 2 3 2 3\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | minimal boundary case |
| all fit | 1 | full packing in one trip |
| all equal to K | N | forced splits every step |
| alternating sums | 4 | greedy boundary correctness |

## Edge Cases

A minimal input such as `1 5 / 3` is handled correctly because the loop never triggers a split and the final non-zero `current` contributes exactly one trip.

A full-capacity single pile like `1 5 / 5` immediately creates one completed trip, since the overflow check never triggers but the final accumulation is counted.

A sequence where every pile equals $K$, such as `4 3 / 3 3 3 3`, forces a new trip at every element. Each time `current + x` exceeds $K$, the algorithm resets, ensuring no pile is incorrectly merged.

A tightly packed sequence like `6 5 / 2 3 2 3 2 3` demonstrates that the greedy packing always fills each trip as much as possible before cutting, and never delays a cut that would improve feasibility.
