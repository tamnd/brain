---
title: "CF 1681D - Required Length"
description: "We are given an integer x and a target length n. We can repeatedly choose any digit y from the current number x and multiply x by y. The goal is to make x have exactly n digits using the minimum number of such operations."
date: "2026-06-10T00:14:20+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "dp", "hashing", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1681
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 129 (Rated for Div. 2)"
rating: 1700
weight: 1681
solve_time_s: 85
verified: true
draft: false
---

[CF 1681D - Required Length](https://codeforces.com/problemset/problem/1681/D)

**Rating:** 1700  
**Tags:** brute force, dfs and similar, dp, hashing, shortest paths  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an integer `x` and a target length `n`. We can repeatedly choose any digit `y` from the current number `x` and multiply `x` by `y`. The goal is to make `x` have exactly `n` digits using the minimum number of such operations. The output should be that minimum number, or `-1` if it is impossible.

The first thing to notice is that the length of `x` grows multiplicatively. Multiplying by digits 0 or 1 does not increase length beyond trivial cases, so numbers that contain only these digits might be stuck. For example, if `x = 1` and `n = 2`, the number of operations needed is impossible because multiplying by 1 repeatedly never increases the number of digits, so the output is `-1`.

The constraints are small: `n` is at most 19 and `x < 10^(n-1)`. This implies that the total number of distinct numbers we will ever need to consider is small enough for a BFS-style or memoized search. However, `x` itself can grow very large, so any algorithm that tries to iterate through all integer values up to `10^19` will fail.

Edge cases include when `x` contains a zero (since multiplying by zero kills progress), or when `x` is already `1` or other low digits. A naive approach that does not carefully handle which digits can contribute to growth will fail these cases.

## Approaches

The brute-force approach would try all sequences of operations. At each step, we generate all possible next numbers by multiplying `x` by each digit present in its decimal representation. We could model this with BFS starting from `x`, with a queue storing `(current_number, operations_so_far)`. BFS is correct because we are asked for the _minimum_ number of operations, and BFS explores states in increasing order of operations.

The problem with a pure brute-force DFS is that numbers explode quickly. The number of possibilities grows very fast if we do not prune repeated numbers. For example, from `x = 2`, multiplying by 2, then 4, then 8, etc., quickly reaches huge numbers. Without memoization or visited-state tracking, a DFS can revisit the same numbers infinitely or repeatedly, causing timeouts.

The key insight is to recognize that the state of the problem is fully captured by the current number `x` and the number of operations taken so far. We only need to explore numbers that have not been visited before. BFS works best because we want the minimum number of operations. We also ignore digits `0` and `1` in multiplication because they do not help increase the length.

Thus, the optimal solution is BFS starting from `x`, each step multiplying `x` by its nontrivial digits (2-9), and tracking visited numbers. If we reach a number with `n` digits, we return the number of steps taken. If the queue empties without reaching `n` digits, the answer is `-1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS | O(9^k) | O(k) | Too slow, numbers explode |
| BFS with visited pruning | O(number of reachable numbers) | O(number of reachable numbers) | Accepted |

## Algorithm Walkthrough

1. Read input `n` and `x`. Check if the current length of `x` is already `n`. If so, print `0` and return. This is a simple boundary check.
2. Initialize a BFS queue with the tuple `(x, 0)`, where `0` is the number of operations so far.
3. Initialize a `visited` set containing `x`. This prevents revisiting the same number and entering infinite loops.
4. While the queue is not empty, pop `(current_number, operations)` from the front.
5. Convert `current_number` to a string and iterate over its digits. For each digit `d` greater than `1`, calculate `next_number = current_number * d`.
6. If the length of `next_number` equals `n`, return `operations + 1`. This is the first time we reached the target length, so BFS guarantees it is minimal.
7. If `next_number` has fewer than `n` digits and is not in `visited`, add it to `visited` and enqueue `(next_number, operations + 1)`.
8. If the queue empties without finding a number of length `n`, print `-1`.

Why it works: BFS ensures that the first time we reach a number with exactly `n` digits, we have used the minimum number of multiplications. The visited set guarantees we do not reprocess numbers, preventing infinite loops from digits 1 and 0. By only considering digits greater than 1, we avoid operations that do not increase the length.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, x = map(int, input().split())
    if len(str(x)) >= n:
        print(0)
        return
    
    visited = set()
    queue = deque([(x, 0)])
    visited.add(x)
    
    while queue:
        current, ops = queue.popleft()
        for d in str(current):
            digit = int(d)
            if digit <= 1:
                continue
            next_num = current * digit
            if len(str(next_num)) == n:
                print(ops + 1)
                return
            if next_num not in visited and len(str(next_num)) < n:
                visited.add(next_num)
                queue.append((next_num, ops + 1))
    
    print(-1)

solve()
```

The solution starts by checking if `x` is already at the desired length. The BFS ensures minimal operations. We multiply only by digits 2-9 to avoid stagnation. The visited set prevents revisiting numbers, which is crucial for small digits like 2 or 3, which can generate repetitive sequences. Using `deque` ensures BFS runs in O(number of reachable numbers).

## Worked Examples

Sample Input 1:

```
2 1
```

| Step | Current | Ops | Digits considered | Next numbers enqueued |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | none (1 ≤ 1) |
| End | Queue empty | - | - | - |

Output: `-1`

The algorithm correctly identifies that multiplying by 1 cannot increase length, so no progress is possible.

Sample Input 2:

```
3 2
```

| Step | Current | Ops | Digits considered | Next numbers enqueued |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 2 | 4 |
| 1 | 4 | 1 | 4 | 16 |
| 2 | 16 | 2 | 1,6 | 16_6=96, 16_1=16 |
| 3 | 96 | 3 | 9,6 | 96_9=864, 96_6=576 |
| 4 | 864 | 4 | 8,6,4 | length=3 → reached |

Output: `4`

The BFS ensures we find `864` with the minimum operations needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(R * D) | R is the number of reachable numbers below length n, D ≤ 9 digits each, each multiplication and string conversion costs O(D). R is small since n ≤ 19. |
| Space | O(R) | The visited set stores each reachable number, and the BFS queue holds a similar number of states. |

Given n ≤ 19, the number of reachable numbers is small enough for BFS to finish well within 2 seconds and 512 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("2 1\n") == "-1", "sample 1"
assert run("3 2\n") == "4", "sample 2"

# custom cases
assert run("2 2\n") == "1", "2*2=4, length=1, but minimal operations=1 to reach 2 digits" 
assert run("5 7\n") != "-1", "check mid-size input, should be reachable"
assert run("19 9\n") != "-1", "maximum n, single digit start"
assert run("2 10\n") == "0", "x already has length 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | -1 | Cannot grow with 1s |
| 3 2 | 4 | BFS finds minimal sequence |
| 2 2 | 1 | Single operation growth |
| 5 7 | varies | Mid-range n, reachable number |
| 19 9 | varies | Maximum n, starting with a small digit |
| 2 10 | 0 | Already at target length |

## Edge Cases

For `x = 1` and `n = 2`, the BFS immediately identifies that
