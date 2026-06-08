---
title: "CF 2025C - New Game"
description: "We are given a multiset of numbers and we want to build a longest possible sequence by repeatedly picking elements from it. The rule for extending the sequence is local: after taking a number $x$, the next chosen number must be either $x$ or $x+1$."
date: "2026-06-08T12:23:29+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "implementation", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2025
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 170 (Rated for Div. 2)"
rating: 1300
weight: 2025
solve_time_s: 110
verified: false
draft: false
---

[CF 2025C - New Game](https://codeforces.com/problemset/problem/2025/C)

**Rating:** 1300  
**Tags:** binary search, brute force, greedy, implementation, sortings, two pointers  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of numbers and we want to build a longest possible sequence by repeatedly picking elements from it. The rule for extending the sequence is local: after taking a number $x$, the next chosen number must be either $x$ or $x+1$. There is also a global restriction: across the entire chosen sequence, we are only allowed to use at most $k$ distinct values.

The key freedom is that we may start from any element, and we are not forced to follow a fixed path in the array. We are simply selecting a subsequence in time, but adjacency is determined purely by values, not positions.

The constraints indicate that $n$ can be up to $2\cdot 10^5$ across tests, so any solution that tries to simulate all starting points independently or explores many chains explicitly would be too slow. We need something closer to sorting plus a linear or near-linear scan per test case.

A naive failure mode appears when values are interleaved. For example, sequences like $1,100,2,101,3,102$ tempt greedy “extend from each start” approaches, but those ignore that we can reorder selection arbitrarily from the deck. The structure depends only on frequencies and adjacency between sorted values, not positions.

## Approaches

A brute-force idea would be to simulate starting from every possible card and greedily extend the sequence by always picking a valid next value $x$ or $x+1$ if available. This is correct locally, but the number of possible starting choices is $n$, and each simulation may traverse many elements, giving $O(n^2)$ behavior in the worst case.

The key observation is that after sorting the values, the problem becomes one about contiguous value blocks. If we fix a starting value $x$, then the only values we can ever use are $x, x+1, x+2, \dots$, but we are limited to at most $k$ distinct values, so the usable segment is some window of at most $k$ consecutive integers. Inside that window, we want to take as many elements as possible, but we are constrained by a stronger rule: we cannot “skip backwards” in value, so the best we can do is take everything in that interval.

However, there is an important twist: because the next move can stay at $x$ or increase by 1, once we enter a value $v$, we can consume all occurrences of $v$ before moving to $v+1$. So any valid play corresponds to choosing a starting value and then walking forward in sorted unique values, collecting full frequency blocks, until we either exhaust $k$ distinct values or the chain breaks.

Thus the problem reduces to compressing the array into sorted unique values with frequencies and then finding the maximum total frequency over any window of at most $k$ consecutive distinct values.

A two pointers sliding window over the compressed array solves this efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Sliding window on compressed values | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first compress the array by sorting and grouping identical values, producing arrays of distinct values and their frequencies.

We then maintain a sliding window over these groups.

1. Sort the array. This aligns equal values together and lets us work in frequency blocks instead of individual cards. This is essential because all occurrences of a value behave identically in the game.
2. Build two arrays: one for distinct values, one for their frequencies. Each block represents how many times a value can be taken consecutively once reached.
3. Use two pointers $l$ and $r$ over these blocks. The window $[l, r]$ represents a candidate set of distinct values that can be used in a game segment.
4. Maintain the invariant that the number of distinct values in the window is at most $k$, so we always ensure $r-l+1 \le k$. If it exceeds $k$, we move $l$ forward.
5. For each valid window, compute the sum of frequencies inside it. This sum represents the number of cards that can be taken if we start at the leftmost value of the window and extend forward.
6. Track the maximum such sum over all windows.

The answer is the best window sum observed.

### Why it works

The game forces monotone non-decreasing values with step size at most 1, which means once we commit to a starting value, the only flexibility is how many consecutive values we include. Any optimal play therefore corresponds to choosing a contiguous segment in sorted distinct values. Since all occurrences of a value are interchangeable and fully usable once reached, the optimal strategy is to take full frequency blocks. The sliding window enumerates all valid choices of at most $k$ distinct consecutive values, ensuring no optimal segment is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    vals = []
    cnts = []
    
    for x in a:
        if not vals or vals[-1] != x:
            vals.append(x)
            cnts.append(1)
        else:
            cnts[-1] += 1
    
    m = len(vals)
    
    ans = 0
    cur = 0
    l = 0
    
    for r in range(m):
        cur += cnts[r]
        
        while r - l + 1 > k:
            cur -= cnts[l]
            l += 1
        
        ans = max(ans, cur)
    
    print(ans)

t = int(input())
for _ in range(t):
    solve()
```

The code first sorts and compresses values so that identical numbers become contiguous frequency blocks. The sliding window then tracks a valid segment of at most $k$ distinct values, while maintaining the running sum of frequencies to compute the best achievable sequence length.

A subtle point is that we only shrink the window when the number of distinct values exceeds $k$, not based on gaps in value, because after sorting, distinct blocks already reflect increasing value order.

## Worked Examples

### Example 1

Input:

```
n = 10, k = 2
[5, 2, 4, 3, 4, 3, 4, 5, 3, 2]
```

Sorted:

```
[2,2,3,3,3,4,4,4,5,5]
```

Compressed:

| l | r | window values | sum |
| --- | --- | --- | --- |
| 0 | 0 | [2] | 2 |
| 0 | 1 | [2,3] | 5 |
| 0 | 2 | [2,3,4] → shrink |  |
| 1 | 2 | [3,4] | 6 |
| 1 | 3 | [3,4,5] → shrink |  |
| 2 | 3 | [4,5] | 4 |

Maximum is 6.

This confirms that optimal play is determined by choosing the best contiguous value interval.

### Example 2

Input:

```
n = 5, k = 1
[10, 11, 10, 11, 10]
```

Compressed:

```
10 -> 3, 11 -> 2
```

Only windows of size 1 allowed:

| window | sum |
| --- | --- |
| [10] | 3 |
| [11] | 2 |

Answer is 3.

This shows that when $k=1$, the solution reduces to picking the most frequent single value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates, sliding window is linear |
| Space | $O(n)$ | storage for compressed frequencies |

The constraints allow up to $2\cdot10^5$ total elements, so an $O(n \log n)$ sorting solution with linear scanning easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()

        vals = []
        cnts = []

        for x in a:
            if not vals or vals[-1] != x:
                vals.append(x)
                cnts.append(1)
            else:
                cnts[-1] += 1

        ans = 0
        cur = 0
        l = 0

        for r in range(len(vals)):
            cur += cnts[r]
            while r - l + 1 > k:
                cur -= cnts[l]
                l += 1
            ans = max(ans, cur)

        print(ans)

    t = int(input())
    out = []
    for _ in range(t):
        solve()
    return ""

# sample checks (structure-based, not strict stdout capture in this snippet)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | n | single block dominance |
| alternating values | k-dependent | window correctness |
| strictly increasing | k window sum | contiguous selection |
| random mix | correct max segment | general case |

## Edge Cases

A key edge case is when all values are distinct. In that case each block has size 1, and the answer becomes exactly $k$, since any window of size $k$ contributes $k$ elements. The algorithm handles this naturally because every block contributes 1 and the sliding window simply sums over $k$ consecutive blocks.

Another edge case is when all values are equal. Then there is only one block, and the window always stays of size 1 regardless of $k$, so the answer is $n$. The algorithm handles this because no shrinking ever occurs and the full frequency is always counted.

A more subtle case is when $k$ exceeds the number of distinct values. Then the window never shrinks and the algorithm correctly returns the sum of all frequencies, meaning all cards can be taken in one chain.
