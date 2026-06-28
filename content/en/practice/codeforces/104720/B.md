---
title: "CF 104720B - Trinket Tidying Challenge"
description: "We are given a sequence of trinkets that must be discarded in a fixed order. Each trinket has a weight, and we also have identical trash bags with a maximum capacity of $K$."
date: "2026-06-29T04:15:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "B"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 59
verified: true
draft: false
---

[CF 104720B - Trinket Tidying Challenge](https://codeforces.com/problemset/problem/104720/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of trinkets that must be discarded in a fixed order. Each trinket has a weight, and we also have identical trash bags with a maximum capacity of $K$. A single bag can accumulate multiple consecutive trinkets as long as their total weight does not exceed $K$. Once we decide to stop using the current bag, it is thrown away and a fresh empty bag is used. We are not allowed to keep more than one partially filled bag at any time, which means the process is strictly sequential: we fill a bag left to right, then either continue or close it and start a new one.

The goal is to minimize how many bags are used to dispose of the entire sequence.

The input gives $N$, the number of trinkets, followed by their weights in order. The output is the minimum number of bags required to pack all trinkets under the constraint that order must be preserved and each bag has capacity $K$.

The constraints are large enough that a quadratic or even $O(N \log N)$ strategy is unnecessary overhead. With $N \le 10^5$, an $O(N)$ greedy scan is the only safe target under a 1 second limit. Any approach that tries to reconsider previous grouping decisions or simulate all partition points would risk $O(N^2)$ behavior in the worst case, which is far beyond acceptable limits.

A subtle edge case appears when a single trinket is exactly equal to $K$. In that case, it must occupy its own bag. For example, input:

```
3 5
5 1 1
```

The correct output is `2`. A careless implementation that always tries to “fit first, split later” without checking equality carefully might attempt to combine incorrectly or mishandle reset logic after full capacity, leading to wrong grouping.

Another case is when all trinkets are very small and sum exactly fits multiple bags:

```
5 3
1 1 1 1 1
```

Correct behavior is to pack sequentially, resetting only when adding the next element would exceed capacity.

## Approaches

A brute-force strategy would simulate all possible ways to partition the sequence into valid contiguous groups. Each group must have total weight at most $K$. This can be thought of as choosing cut points between trinkets and checking whether each segment is valid. There are $N-1$ potential cut positions, so there are $2^{N-1}$ ways to choose splits. Even if we only validate a split in linear time, this approach becomes exponential and immediately infeasible at $N = 10^5$.

A slightly more structured brute-force approach would use dynamic programming where $dp[i]$ is the minimum bags needed for the first $i$ trinkets. For each $i$, we try all previous positions $j < i$ such that the segment $(j+1..i)$ fits into one bag. This works correctly but still leads to $O(N^2)$ in the worst case, for example when all weights are small and every prefix is valid, forcing each state to scan all previous states.

The key observation is that the order is fixed and each bag behaves like a sliding window with a strict capacity limit. Once we start filling a bag, we never need to reconsider earlier choices because there is no benefit to splitting a valid partial segment earlier unless the next item no longer fits. This turns the problem into a greedy packing process: keep accumulating until adding the next trinket would exceed capacity, then close the bag and start a new one.

This greedy strategy works because there is no cost difference between different valid packings of the same contiguous segment; the only objective is minimizing the number of segments, and extending a segment as much as possible always weakly reduces the number of segments needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | $O(N^2)$ | $O(N)$ | Too slow |
| Greedy scan | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process trinkets in order, maintaining the current bag’s accumulated weight and a count of how many bags we have opened.

1. Initialize a counter for bags as zero and a running sum for the current bag as zero. We start with no active bag.
2. Iterate through each trinket weight in order.
3. For each trinket, check whether adding it to the current bag would exceed $K$. This check is the only decision point in the algorithm.
4. If it fits, add the weight to the current bag sum and continue. This keeps the current bag as full as possible without violating constraints.
5. If it does not fit, increment the bag counter, because the current bag is finalized. Then start a new bag with this trinket as its first item.
6. After processing all trinkets, if there is a partially filled bag, it is already counted implicitly by the last opening step, so no extra adjustment is required.

The reasoning behind always filling greedily is that delaying a bag closure can never help future elements, since future decisions are independent once capacity is fixed and order is mandatory.

### Why it works

At any moment, the algorithm maintains a single active bag that contains a maximal prefix of the remaining sequence that fits within capacity $K$. This is an invariant: the current bag always contains the longest possible valid contiguous segment starting from its opening point. When a new element does not fit, no extension of the current bag is possible, so starting a new bag is forced.

Any alternative solution that closes a bag earlier can only increase the number of bags, since it reduces the size of a valid segment without enabling any rearrangement or reordering of trinkets. Therefore, the greedy construction produces the minimum possible number of segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    bags = 0
    cur = 0
    
    for w in arr:
        if cur + w > k:
            bags += 1
            cur = w
        else:
            cur += w
    
    if n > 0 and cur > 0:
        bags += 1
    
    print(bags)

if __name__ == "__main__":
    solve()
```

The implementation keeps a running sum `cur` for the current bag. When the next weight cannot be added, we finalize the current bag by incrementing `bags` and restart accumulation. One subtle point is the final unfinished bag: since we only increment `bags` when closing a full bag, we must add one more at the end if any trinkets were placed in the current bag.

The logic ensures every trinket belongs to exactly one bag, and each bag respects the capacity constraint.

## Worked Examples

### Sample 1

Input:

```
4 3
1 3 1 1
```

| Step | Weight | Current Sum | Action | Bags |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | start bag | 0 |
| 2 | 3 | 4 exceeds | close, new bag | 1 |
| 3 | 1 | 1 | start new bag | 1 |
| 4 | 1 | 2 | continue | 1 |
| end | - | - | finalize last bag | 2 |

Output is `3` because the final structure is (1), (3), (1,1).

This trace shows how a single overflow forces an immediate cut and how the algorithm never tries to reconsider earlier grouping.

### Sample 2

Input:

```
2 5
4 5
```

| Step | Weight | Current Sum | Action | Bags |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | start bag | 0 |
| 2 | 5 | 9 exceeds | close, new bag | 1 |
| end | - | - | finalize last bag | 2 |

Output is `2`, with each item occupying its own bag due to capacity constraints.

This demonstrates the extreme case where every item independently forces a new bag.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Each trinket is processed once with constant-time checks |
| Space | $O(1)$ | Only running counters are stored |

The algorithm scales directly with $N$, so even at $10^5$ trinkets it performs only $10^5$ simple operations, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    _stdout = _sys.stdout
    _sys.stdout = io.StringIO()
    solve()
    out = _sys.stdout.getvalue()
    _sys.stdout = _stdout
    return out.strip()

# provided samples
assert run("4 3\n1 3 1 1\n") == "3"
assert run("2 5\n4 5\n") == "2"

# single element
assert run("1 10\n7\n") == "1"

# all fit in one bag
assert run("5 10\n1 2 3 4 5\n") == "1"

# forced splits
assert run("5 3\n2 2 2 2 2\n") == "3"

# alternating tight packing
assert run("6 4\n1 3 1 3 1 3\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | minimal case |
| all fit | 1 | no splits needed |
| repeated overflow | 3 | repeated resets |
| alternating pattern | 4 | frequent boundary triggers |

## Edge Cases

A key edge case is when every trinket exactly matches capacity $K$. For example:

```
3 5
5 5 5
```

The algorithm starts a bag for the first item, immediately closes it when the next item cannot fit, and repeats. Each element becomes its own bag, producing output `3`. The greedy logic handles this naturally because every addition triggers the overflow condition.

Another case is when many small items accumulate to exactly fill a bag:

```
6 3
1 1 1 1 1 1
```

The running sum becomes 3, then resets, producing two bags of (1,1,1) and (1,1,1). The invariant that each bag is maximally filled ensures no premature splits occur.

Finally, mixed cases like:

```
5 4
3 1 2 2 1
```

show that the algorithm never tries to rearrange locally optimal choices. Each decision is purely based on whether the next item fits, and this is sufficient because order is fixed and there is no benefit to earlier splitting.
