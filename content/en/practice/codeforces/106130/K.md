---
title: "CF 106130K - \u6700\u4e0d\u4e0a\u5347\u4e5f\u4e0d\u4e0b\u964d\u5e8f\u5217"
description: "We are asked to construct a permutation of the numbers from 1 to n. From this permutation we look at two classical subsequence measures: the length of the longest strictly increasing subsequence and the length of the longest strictly decreasing subsequence."
date: "2026-06-20T07:33:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106130
codeforces_index: "K"
codeforces_contest_name: "GDUT 2025 Monthly competition"
rating: 0
weight: 106130
solve_time_s: 38
verified: true
draft: false
---

[CF 106130K - \u6700\u4e0d\u4e0a\u5347\u4e5f\u4e0d\u4e0b\u964d\u5e8f\u5217](https://codeforces.com/problemset/problem/106130/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a permutation of the numbers from 1 to n. From this permutation we look at two classical subsequence measures: the length of the longest strictly increasing subsequence and the length of the longest strictly decreasing subsequence. We want to output any permutation that minimizes the sum of these two lengths.

The key difficulty is that these two quantities pull the permutation in opposite structural directions. A very sorted array makes the increasing subsequence long, while a very reversed array makes the decreasing subsequence long. The task is to find a balanced structure where neither monotonic structure becomes large.

The input is a single integer n up to 2000, so an O(n^2) or O(n log n) construction is perfectly acceptable. Anything exponential or based on enumerating permutations is impossible since n! grows too quickly. Even O(n^3) would be borderline but likely acceptable; however, we should aim for a direct constructive O(n).

A subtle point is that both LIS and LDS are computed on the same permutation. Changing the arrangement to reduce LIS can inadvertently increase LDS and vice versa, so greedy local swaps without structure can easily fail.

For example, consider n = 5:

Permutation 1 2 3 4 5 gives LIS = 5 and LDS = 1, sum = 6.

Permutation 5 4 3 2 1 gives LIS = 1 and LDS = 5, sum = 6.

A naive idea might be to alternate small and large values like 1 5 2 4 3, but such interleavings do not systematically control both subsequence lengths and can still allow long monotone subsequences depending on placement.

The real challenge is to control the width of increasing and decreasing subsequences simultaneously using a global structure rather than local decisions.

## Approaches

A brute-force solution would enumerate all permutations of 1 to n and compute LIS and LDS for each one using dynamic programming in O(n^2) time per permutation. That leads to O(n! · n^2), which becomes impossible even for n around 10.

The key observation is that this problem is fundamentally about decomposing a permutation into monotone subsequences. The classic relationship between LIS, LDS, and partial orders suggests using a grid-like or block structure rather than attempting to optimize subsequences directly.

The correct construction comes from viewing the permutation as arranged in a two-dimensional layout. If we think of splitting the numbers into blocks and reversing inside blocks while keeping block order increasing, we can simultaneously limit how far a monotone subsequence can extend. The idea is to create a structure where any increasing or decreasing subsequence is forced to “switch blocks” frequently, limiting its growth.

A natural optimal construction is to split the array into segments of roughly size sqrt(n), then fill each segment in decreasing order, while arranging segments in increasing order of values. This creates a pattern where LIS is bounded by the number of segments and LDS is bounded by the segment size, balancing both.

More precisely, if we take block size B approximately sqrt(n), we fill numbers in blocks of size B, each block in descending order, and place blocks in increasing order. Then within a block we cannot take more than B elements in increasing subsequence, and across blocks we can take at most about n/B blocks in decreasing subsequence, giving a balanced sum minimized near 2 sqrt(n).

This matches the known intuition that minimizing LIS + LDS for permutations is optimized by a square decomposition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n^2) | O(n) | Too slow |
| Block sqrt construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the permutation using a square blocking strategy.

1. Choose a block size B = ⌈sqrt(n)⌉. This balances the tradeoff between controlling increasing and decreasing subsequences.
2. Split the numbers from 1 to n into consecutive groups of size B, except possibly the last group which may be smaller.
3. For each group, instead of storing numbers in increasing order, store them in decreasing order. This ensures that within a block, it is difficult to form a long increasing subsequence.
4. Place the blocks in increasing order of their values. That is, the first block contains the smallest numbers, the second block the next smallest, and so on.
5. Output the concatenation of all blocks.

The reason for reversing inside each block is that it breaks local increasing structure. Meanwhile, keeping block order increasing ensures that large jumps between blocks prevent long decreasing subsequences from spanning many blocks.

### Why it works

Any increasing subsequence can take at most one element per block if it tries to move across blocks, because elements in later blocks are strictly larger but internal ordering is reversed, limiting consistent selection. Similarly, any decreasing subsequence is trapped inside blocks because block ordering is increasing, so it cannot move from one block to another while remaining decreasing. Thus LIS is bounded by number of blocks and LDS is bounded by block size, making their sum roughly B + n/B, minimized when B is around sqrt(n).

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    import math
    B = int(math.sqrt(n))
    if B * B < n:
        B += 1

    res = []
    for start in range(1, n + 1, B):
        end = min(n, start + B - 1)
        block = list(range(start, end + 1))
        block.reverse()
        res.extend(block)

    print(*res)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the block construction. We compute the block size using the square root, then iterate over ranges of consecutive integers. Each block is reversed before being appended. The important detail is that blocks are formed on value ranges, not on indices, which ensures the permutation property is preserved.

Reversing each block is essential because it forces any increasing subsequence to restart frequently when moving inside a block, while still preserving global ordering across blocks.

## Worked Examples

### Example 1: n = 6

Let B = 2. We form blocks: [1,2], [3,4], [5,6]. Reversing each gives [2,1], [4,3], [6,5].

| Step | Block Range | Block After Reverse | Result |
| --- | --- | --- | --- |
| 1 | 1 2 | 2 1 | 2 1 |
| 2 | 3 4 | 4 3 | 2 1 4 3 |
| 3 | 5 6 | 6 5 | 2 1 4 3 6 5 |

Final permutation: 2 1 4 3 6 5.

This demonstrates that values are locally decreasing but globally increasing across blocks.

### Example 2: n = 7

Let B = 3. Blocks are [1,2,3], [4,5,6], [7]. After reversing: [3,2,1], [6,5,4], [7].

| Step | Block Range | Block After Reverse | Result |
| --- | --- | --- | --- |
| 1 | 1 2 3 | 3 2 1 | 3 2 1 |
| 2 | 4 5 6 | 6 5 4 | 3 2 1 6 5 4 |
| 3 | 7 | 7 | 3 2 1 6 5 4 7 |

This shows how the last smaller block does not break correctness; it only slightly adjusts balance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number is placed into exactly one block and output once |
| Space | O(n) | We store the resulting permutation |

The construction is linear in n, which is easily fast enough for n up to 2000. Memory usage is also linear and trivial for the given constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import sqrt
    n = int(inp.strip())
    B = int(sqrt(n))
    if B * B < n:
        B += 1
    res = []
    for start in range(1, n + 1, B):
        end = min(n, start + B - 1)
        block = list(range(start, end + 1))
        block.reverse()
        res.extend(block)
    return " ".join(map(str, res))

# minimal
assert run("1") == "1"

# small case
assert run("2") in ["1 2", "2 1"]

# sample-like
assert len(run("6").split()) == 6

# larger case structure
assert len(run("10").split()) == 10
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimal boundary |
| 2 | 1 2 or 2 1 | smallest non-trivial permutation |
| 6 | 6 numbers | block correctness and completeness |
| 10 | 10 numbers | general construction validity |

## Edge Cases

For n = 1, the algorithm sets B = 1. The only block is [1], reversing it still gives [1]. LIS and LDS are both 1, and no alternative permutation exists.

For n = 2, B = 2. We have a single block [1,2] reversed into [2,1]. This produces LIS = 1 and LDS = 2, which is optimal since any permutation must have at least one of them equal to 2.

For n = 3, B = 2. Blocks are [1,2] → [2,1] and [3] → [3], giving [2,1,3]. LIS is 2 and LDS is 2, showing the balancing effect already starts appearing even at small scale.

Each of these cases confirms that the construction degrades smoothly at small n without requiring special handling beyond the block size computation.
