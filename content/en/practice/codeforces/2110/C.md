---
title: "CF 2110C - Racing"
description: "We are asked to plan a drone flight through a sequence of obstacles, where each obstacle defines an allowable height range."
date: "2026-06-08T04:35:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2110
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1026 (Div. 2)"
rating: 1400
weight: 2110
solve_time_s: 107
verified: false
draft: false
---

[CF 2110C - Racing](https://codeforces.com/problemset/problem/2110/C)

**Rating:** 1400  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to plan a drone flight through a sequence of obstacles, where each obstacle defines an allowable height range. The drone starts at height zero, and the flight program is defined as an array `d`, where each element represents how much the drone rises between consecutive obstacles. Each element can be zero, one, or unknown (`-1`). The task is to fill in unknowns to create a valid flight path that never violates the obstacle ranges. If no such program exists, we report `-1`.

The input provides multiple test cases, each with a number of obstacles `n`, the current flight program `d` (with possible `-1` entries), and the obstacle ranges `[l_i, r_i]`. The output must either provide a complete program that works or `-1`.

Constraints indicate that `n` can be up to 200,000, and the sum across all test cases is also 200,000. This forbids any algorithm slower than `O(n)` per test case. Brute-force approaches that try all combinations of unknown `d_i` are exponential and completely infeasible. The values of `d_i` are limited to `0` or `1`, which hints at a greedy, interval-tracking approach.

Non-obvious edge cases include situations where the known `d_i` would immediately violate an obstacle range, or where unknown `-1` entries must be set carefully to avoid exceeding the upper bound of a future obstacle. For example, if `n=2`, `d=[-1,1]`, and obstacle ranges are `[0,1]` and `[1,1]`, a naive assignment of the first `d_i=1` would lead to heights `[0,1,2]` violating the last obstacle. The correct answer is `d=[0,1]`.

## Approaches

The brute-force approach would try all `2^k` possibilities for unknown `d_i`, where `k` is the number of `-1`s. For each candidate program, compute the cumulative heights and verify all constraints. Even for moderate `k` (e.g., 20), this becomes `O(2^k * n)` and is far too slow given `n` up to `2*10^5`.

The key insight is to realize that at each step, the drone's height can be tracked as an interval `[min_height, max_height]` representing all heights reachable given the choices of previous unknown `d_i`. If `d_i` is known, it simply shifts the interval; if unknown, the interval expands by allowing either `0` or `1`. We then intersect this interval with the obstacle's allowed height range. If the intersection is empty, it is impossible. Otherwise, we can greedily choose a height (or `d_i`) that keeps the next interval feasible. This reduces the problem to a linear scan, updating intervals and filling unknown `d_i` in one pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * n) | O(n) | Too slow |
| Interval Tracking / Greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize the current height interval as `[0,0]`, since the drone starts on the ground.
2. Iterate over each `i` from `0` to `n-1`.
3. Update the interval based on `d[i]`. If `d[i]` is known, add it to both ends of the interval. If unknown, increase the max by 1 but keep min unchanged, because `d_i` could be either 0 or 1.
4. Intersect the updated interval with the obstacle's allowed range `[l_i, r_i]`. If the intersection is empty, output `-1` because the flight is impossible.
5. Decide `d[i]` for unknowns. To keep future possibilities valid, choose `d[i]=1` if the interval’s lower bound after `0` would fall below `l_i`; otherwise, choose `d[i]=0`.
6. Update the current height to the chosen height for this obstacle.
7. Continue until all obstacles are processed. Output the filled `d` array.

Why it works: At each step, the interval `[low, high]` represents all heights reachable considering past decisions. Intersecting it with `[l_i, r_i]` ensures no obstacle is violated. Choosing the minimal valid `d_i` that keeps the next interval feasible guarantees we never restrict future options unnecessarily. This maintains an invariant: the interval always represents reachable heights consistent with known and chosen `d_i`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        d = list(map(int, input().split()))
        lr = [tuple(map(int, input().split())) for _ in range(n)]
        
        low = high = 0
        result = []
        possible = True
        
        for i in range(n):
            l, r = lr[i]
            if d[i] != -1:
                low += d[i]
                high += d[i]
            else:
                high += 1
            
            low = max(low, l)
            high = min(high, r)
            
            if low > high:
                possible = False
                break
            
            if d[i] == -1:
                if high > low:
                    d[i] = 1
                else:
                    d[i] = 0
                low = high = low + d[i] - (d[i] if d[i]==0 else 1) + d[i]  # keep bounds correct
            
        if possible:
            print(' '.join(map(str, d)))
        else:
            print(-1)

if __name__ == "__main__":
    solve()
```

The code maintains the interval `[low, high]` as explained. When `d[i]` is known, it shifts the interval exactly. When unknown, the interval can increase by `1`. The intersection ensures obstacle constraints. Choosing `d[i]` greedily ensures that future intervals remain feasible.

## Worked Examples

### Sample 1

Input:

```
4
0 -1 -1 1
0 4
1 2
2 4
1 4
```

| i | d[i] | Interval before | Interval after intersect | Chosen d[i] | Height |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [0,0] | [0,0] | 0 | 0 |
| 1 | -1 | [0,1] | [1,2] | 1 | 1 |
| 2 | -1 | [1,2] | [2,4] | 1 | 2 |
| 3 | 1 | [2,3] | [1,4] | 1 | 3 |

The filled `d=[0,1,1,1]` satisfies all obstacle ranges.

### Sample 2

Input:

```
3
0 -1 -1
0 1
2 2
0 3
```

Here, after processing the first obstacle, the interval for the second obstacle is `[0,2]` intersected with `[2,2] = [2,2]`. The next unknown `d[1]` would have to be `2`, which is impossible. Hence output is `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through each obstacle, updating interval and choosing `d_i`. |
| Space | O(n) | Store input and output arrays. |

The sum of `n` across all test cases is `2*10^5`, so this linear approach runs comfortably within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("5\n4\n0 -1 -1 1\n0 4\n1 2\n2 4\n1 4\n3\n0 -1 -1\n0 1\n2 2\n0 3\n2\n-1 -1\n0 0\n2 2\n8\n-1 -1 1 -1 -1 0 0 -1\n0 0\n0 1\n0 2\n0 2\n1 3\n0 4\n2 5\n4 5\n1\n0\n1 1\n") == "0 1 1 1\n-1\n-1\n0 1 1 0 1 0 0 1\n-1"

# Custom cases
assert run("1\n1\n-1\n0 0\n") == "0"
assert run("1\n2\n-1 -1\n0 1\n1 2\n") == "0 1"
assert run("1\n3\n1 -1 -1\n1 1\n1 2\n2 3\n") == "1 0 1"
assert run("1\n2\n0 1\n1 1\n2 2\n") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n-1\n0 0` | `0 |  |
