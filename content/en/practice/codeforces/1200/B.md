---
title: "CF 1200B - Block Adventure"
description: "In Block Adventure, we have a row of columns with different heights. The player starts on the first column and must reach the last one."
date: "2026-06-11T23:53:21+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1200
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 578 (Div. 2)"
rating: 1200
weight: 1200
solve_time_s: 110
verified: true
draft: false
---

[CF 1200B - Block Adventure](https://codeforces.com/problemset/problem/1200/B)

**Rating:** 1200  
**Tags:** dp, greedy  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

In Block Adventure, we have a row of columns with different heights. The player starts on the first column and must reach the last one. The character can carry blocks in a bag and modify column heights by either removing a block from the current column or placing a block from the bag onto it. Movement to the next column is only possible if the height difference does not exceed a given limit, `k`. The goal is to determine whether the player can traverse from the first to the last column under these rules.

The input gives the number of columns, the initial number of blocks in the bag, the tolerance `k`, and an array of column heights. The output is "YES" if the player can reach the last column and "NO" otherwise.

The constraints indicate that `n` is at most 100, which is small enough to process each column in a simple loop. The bag and column heights can go up to $10^6$, which means we cannot simulate every possible block transfer. Instead, we need a greedy approach that updates the number of blocks in the bag dynamically as we move forward. A careless approach might, for instance, attempt to simulate every possible rearrangement of blocks or fail when `k=0` or the player has exactly enough blocks to make a jump.

An edge case arises when a column is already lower than the next one, but the bag does not have enough blocks to fill the gap. For example, with `h = [3, 7]`, `m = 3`, and `k = 0`, we cannot reach the next column because the gap exceeds the tolerance, and using all blocks from the bag would still leave a deficit. A naive check of just `|h_i - h_{i+1}| <= k` would incorrectly suggest movement is impossible without considering the blocks that can be added.

## Approaches

The brute-force approach would simulate every possible combination of adding or removing blocks at each column, tracking the bag contents. While this is correct, it explodes combinatorially because at each column we can add or remove multiple blocks, creating a massive number of states. With `n=100` and `m` potentially up to $10^6$, the number of operations becomes completely impractical.

The key observation is that we do not need to simulate every action. The only thing that matters at each step is whether we can satisfy the next column's height within the tolerance `k`. If the current column is taller than needed, we remove the excess blocks into the bag. If it is shorter, we use blocks from the bag to reach the minimum allowable height. This greedy approach works because the bag is unlimited in capacity, and we only care about reaching the next column, not the exact sequence of add/remove operations.

We maintain the number of blocks in the bag dynamically and check for each transition whether the next column is reachable. This reduces the problem to a linear scan through the columns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `n` | O(n + m) | Too slow |
| Greedy / Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `n`, `m`, `k`, and the array of column heights `h`.
2. Initialize the number of blocks in the bag as `m`.
3. Loop through columns from the first to the second-to-last. For each column `i`, calculate the maximum height we can safely leave at column `i` so that moving to column `i+1` is possible. This is `max(0, h[i+1] - k)`.
4. If `h[i]` is greater than or equal to this minimum required height, add the excess blocks to the bag. The excess is `h[i] - min_required`.
5. If `h[i]` is less than the minimum required height, calculate how many blocks we need from the bag. If the bag contains fewer blocks than needed, movement is impossible; break and return "NO". Otherwise, subtract the required blocks from the bag.
6. After processing all transitions, if we never ran out of blocks, print "YES".

Why it works: At each step, we ensure the column height is within the tolerance for the next move. By greedily using or collecting blocks, we maintain an invariant that the bag always contains exactly the surplus blocks available from previous columns. This guarantees that if we cannot satisfy a column with the current bag, it is impossible to proceed further.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    h = list(map(int, input().split()))
    bag = m
    possible = True
    for i in range(n - 1):
        min_required = max(0, h[i+1] - k)
        if h[i] >= min_required:
            bag += h[i] - min_required
        else:
            need = min_required - h[i]
            if bag < need:
                possible = False
                break
            bag -= need
    print("YES" if possible else "NO")
```

This code follows the greedy strategy. We compute the minimum height needed to move forward and adjust the bag accordingly. The `max(0, h[i+1] - k)` ensures we never try to leave a negative height. The loop stops immediately when the bag cannot cover the deficit, saving unnecessary computation.

## Worked Examples

**Example 1**:

Input: `3 0 1` and heights `4 3 5`.

| i | h[i] | h[i+1] | min_required | bag | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | 3 | 2 | 0 | 4 >= 2 → bag += 2 → bag = 2 |
| 1 | 3 | 5 | 4 | 2 | 3 < 4 → need = 1 → bag -= 1 → bag = 1 |

The loop finishes and `bag >= 0`, so output is "YES".

**Example 2**:

Input: `3 1 2` and heights `1 4 7`.

| i | h[i] | h[i+1] | min_required | bag | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 4 | 2 | 1 | 1 < 2 → need = 1 → bag = 0 |
| 1 | 4 | 7 | 5 | 0 | 4 < 5 → need = 1 → bag < need → impossible |

Output is "NO".

These traces show the algorithm maintains the bag invariant and correctly determines reachability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * t) | We process each column exactly once per test case |
| Space | O(n) | We store the column heights array for each test case |

Given `n ≤ 100` and `t ≤ 1000`, the total operations are at most 100,000, well within the 1-second limit. The bag and height calculations are integer operations, so no performance bottleneck arises.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        h = list(map(int, input().split()))
        bag = m
        possible = True
        for i in range(n - 1):
            min_required = max(0, h[i+1] - k)
            if h[i] >= min_required:
                bag += h[i] - min_required
            else:
                need = min_required - h[i]
                if bag < need:
                    possible = False
                    break
                bag -= need
        output.append("YES" if possible else "NO")
    return "\n".join(output)

# provided samples
assert run("5\n3 0 1\n4 3 5\n3 1 2\n1 4 7\n4 10 0\n10 20 10 20\n2 5 5\n0 11\n1 9 9\n99\n") == "YES\nNO\nYES\nNO\nYES"

# custom cases
assert run("1\n1 0 0\n0\n") == "YES", "single column"
assert run("1\n2 0 0\n5 5\n") == "YES", "exactly equal columns, k=0"
assert run("1\n2 1 0\n5 6\n") == "YES", "need one block from bag"
assert run("1\n2 0 0\n5 6\n") == "NO", "cannot reach next column"
assert run("1\n3 1000000 1000000\n1000000 0 1000000\n") == "YES", "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1 0 0\n0\n` | YES | Single-column edge case |
| `1\n2 0 0\n5 5\n` | YES | Equal heights, k=0 |
| `1\n2 1 0\n5 6 |  |  |
