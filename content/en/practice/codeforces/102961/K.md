---
title: "CF 102961K - Collecting Numbers"
description: "We are given a sequence of integers representing a permutation-like arrangement of distinct numbers. The task is to determine how many “rounds” it takes to process all numbers in increasing order, where each round consists of scanning the sequence from left to right and picking…"
date: "2026-07-04T06:52:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "K"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 38
verified: true
draft: false
---

[CF 102961K - Collecting Numbers](https://codeforces.com/problemset/problem/102961/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers representing a permutation-like arrangement of distinct numbers. The task is to determine how many “rounds” it takes to process all numbers in increasing order, where each round consists of scanning the sequence from left to right and picking off numbers whenever they appear in the next required order position.

A more concrete way to think about it is that we want to read the values 1 through n in order, but we are forced to traverse the array from left to right repeatedly. Each time we traverse, we pick as many next-in-order values as we can without going backwards in the array. Once we can no longer continue in the current pass, we start a new pass.

The input gives n followed by an array of length n containing each integer from 1 to n exactly once. The output is a single integer, the number of full left-to-right passes required to consume the sequence in increasing order.

The constraint structure implies n can be large, typically up to 200,000 or similar in Codeforces-style problems. That immediately rules out any approach that simulates full passes over the array repeatedly. A naive simulation that scans the array once per number would behave like O(n²) in the worst case, which would be too slow.

A subtle edge case appears when the array is already sorted. In that case, everything is consumed in a single pass. The opposite extreme is a reverse-sorted array, where each element forces a new pass because every next required number appears earlier in the array than the previous one.

For example, if n = 5 and the array is [5, 4, 3, 2, 1], we cannot pick 1 until a full pass is done, so every number requires its own pass, leading to output 5. A naive scan-per-pass approach might accidentally recompute progress incorrectly if it does not carefully reset state between passes.

## Approaches

The brute-force idea is to literally simulate the process. We maintain the current target value we are trying to pick, starting from 1. We repeatedly scan the array from left to right. Whenever we encounter the current target, we increment the target. Once we reach the end of the array, we count one pass and restart scanning until all numbers are consumed.

This works because it faithfully follows the definition of the process. The problem is the cost. In the worst case, each pass might only consume one element, so we scan the entire array for each of n values. That leads to about n passes, each taking O(n), producing O(n²) total operations.

The key observation is that what matters is not the scanning itself, but where consecutive numbers appear relative to each other in the array. If number x+1 appears to the left of x, then we cannot continue the current pass when reaching x, because we already passed x+1 in this scan. Each time this happens, we are forced to start a new pass.

So instead of simulating passes, we track positions of each value in the array. We walk through values from 1 to n and compare positions. Whenever the position of the current value is smaller than the position of the previous value, it means the order breaks within a single scan, and a new pass is required.

This reduces the problem to counting how many times the position sequence decreases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an array `pos` where `pos[x]` stores the index of value `x` in the given permutation. This converts the problem from working on the array itself to working on positions, which makes comparisons constant time.
2. Initialize a counter `rounds = 1` because at least one pass is always needed to start processing the sequence.
3. Iterate `x` from 2 to n, comparing `pos[x]` with `pos[x-1]`. Each comparison checks whether we can continue the current increasing sequence within the same scan.
4. If `pos[x] < pos[x-1]`, increment `rounds` by 1. This means value `x` appears before `x-1` in the array, so in a left-to-right scan we would encounter `x-1` first, and thus cannot process `x` in the same pass.
5. After finishing the loop, output `rounds`.

### Why it works

The algorithm relies on the invariant that a single scan can only process values whose indices appear in increasing order. Each time we detect a decrease in the index sequence of consecutive values, we identify a boundary between two scans. Since values are consumed strictly in increasing numerical order, every inversion between `pos[x]` and `pos[x-1]` forces a new traversal. The count of such breaks exactly matches the number of required passes.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
a = list(map(int, input().split()))

pos = [0] * (n + 1)
for i, v in enumerate(a):
    pos[v] = i

rounds = 1
for x in range(2, n + 1):
    if pos[x] < pos[x - 1]:
        rounds += 1

print(rounds)
```

The first loop builds the position map so that each value knows its location in O(1) time. This is crucial because it transforms repeated scanning into simple comparisons.

The second loop implements the core observation: we only care about whether consecutive values appear in increasing index order. The initialization to 1 reflects the fact that even a perfectly ordered array requires at least one pass.

A common mistake is initializing `rounds` to 0 and trying to increment only on breaks, which undercounts by one. Another subtle issue is confusing values with indices, the comparison must be between positions of values, not the values themselves.

## Worked Examples

### Example 1

Input:

```
5
3 1 2 5 4
```

We compute positions:

| x | pos[x] |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 0 |
| 4 | 4 |
| 5 | 3 |

Now we compare consecutive values:

| x | pos[x-1] | pos[x] | Break? | rounds |
| --- | --- | --- | --- | --- |
| 2 | 1 | 2 | No | 1 |
| 3 | 2 | 0 | Yes | 2 |
| 4 | 0 | 4 | No | 2 |
| 5 | 4 | 3 | Yes | 3 |

Output is 3.

This trace shows that every time the position order decreases, a new pass becomes necessary, confirming the mapping between inversions and scan resets.

### Example 2

Input:

```
4
1 2 3 4
```

| x | pos[x-1] | pos[x] | Break? | rounds |
| --- | --- | --- | --- | --- |
| 2 | 0 | 1 | No | 1 |
| 3 | 1 | 2 | No | 1 |
| 4 | 2 | 3 | No | 1 |

Output is 1.

This demonstrates the best-case scenario where the permutation is already aligned with the required order, so a single scan suffices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to build positions and one linear scan over values |
| Space | O(n) | Array storing position of each value |

The solution fits comfortably within typical constraints up to 200,000 elements. Both time and memory usage scale linearly, which is optimal given that every element must be read at least once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input().strip())
    a = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, v in enumerate(a):
        pos[v] = i

    rounds = 1
    for x in range(2, n + 1):
        if pos[x] < pos[x - 1]:
            rounds += 1

    return str(rounds)

# provided samples
assert run("5\n3 1 2 5 4\n") == "3"

# minimum size
assert run("1\n1\n") == "1"

# already sorted
assert run("4\n1 2 3 4\n") == "1"

# reverse sorted
assert run("4\n4 3 2 1\n") == "4"

# random permutation
assert run("6\n4 1 3 2 6 5\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | minimal boundary case |
| sorted array | 1 | no breaks case |
| reverse array | n | worst fragmentation |
| mixed permutation | 4 | general correctness |

## Edge Cases

A single-element array such as `[1]` is the simplest possible scenario. The position array contains only one value, and the loop over consecutive pairs never runs, leaving `rounds = 1`. The algorithm correctly handles this without special casing.

A reverse sorted array like `[4, 3, 2, 1]` produces positions where each `pos[x] < pos[x-1]` holds true. The loop increments `rounds` at every step, resulting in 4 passes. This matches the intuition that each number must be processed in a separate traversal because every next required value appears earlier in the array.

A partially ordered case such as `[3, 1, 2, 4]` produces a single break when moving from 2 to 3 in position order. The algorithm detects exactly one decrease and outputs 2, correctly splitting the sequence into two scans.
