---
title: "CF 1486A - Shifting Stacks"
description: "We are given a sequence of stacks, each with some number of blocks. The task is to decide if we can redistribute blocks, moving them only to the right, to make the stack heights strictly increasing."
date: "2026-06-10T23:07:07+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1486
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 703 (Div. 2)"
rating: 900
weight: 1486
solve_time_s: 113
verified: true
draft: false
---

[CF 1486A - Shifting Stacks](https://codeforces.com/problemset/problem/1486/A)

**Rating:** 900  
**Tags:** greedy, implementation  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of stacks, each with some number of blocks. The task is to decide if we can redistribute blocks, moving them only to the right, to make the stack heights strictly increasing. Each move consists of taking one block from stack $i$ and placing it onto stack $i+1$. We do not remove or discard stacks; even empty stacks remain in place.

The input consists of multiple test cases. Each test case gives the number of stacks $n$ and a list of heights. The output is YES if we can achieve a strictly increasing sequence and NO otherwise.

The constraints are modest: $n \le 100$ and the sum of all $n$ across test cases is at most $10^4$. This allows any algorithm that is roughly $O(n)$ per test case, since $10^4$ total operations is feasible under a 1-second time limit. However, a naive brute-force that simulates moving single blocks repeatedly could take up to $10^9$ steps if stack heights are near the upper bound, which is far too slow.

Edge cases that can trip up a naive solution include stacks with zero height, all stacks equal, or very large numbers that require careful accumulation of excess blocks. For example, an input like `[0, 0, 1]` cannot be made strictly increasing because the first two stacks start at zero and we cannot move blocks left. Similarly `[1000000000, 1000000000, 1000000000]` can be adjusted by moving excess blocks gradually to the right to form `[0, 1, 2]` plus offsets, demonstrating that the solution must track cumulative surplus, not just individual pair differences.

## Approaches

The brute-force approach would simulate every possible move, taking one block at a time and shifting it right until no more moves can be made. This is correct in principle, because eventually all excess blocks would be distributed to satisfy the strictly increasing condition if possible. The problem is that a single test case with stacks of height $10^9$ would require billions of moves, which is infeasible.

The key insight is to notice that each stack can contribute a certain "excess" to the next stack. If the first stack has more than zero blocks, it can give as many as $h_0$ blocks to the next stack. More generally, the $i$-th stack must be able to supply enough blocks to ensure that all previous positions can reach the strictly increasing requirement. Formally, after distributing excess blocks from left to right, the $i$-th stack must have at least $i$ blocks in total. This transforms the problem into a simple linear scan, keeping track of the cumulative surplus and checking if each stack can satisfy its required minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(sum of all heights) | O(n) | Too slow for large heights |
| Optimal | O(n) per test case | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$ and the heights array $h$.
2. Initialize a variable `surplus` to zero. This will track the number of blocks we can carry over to the next stack.
3. Iterate through the stacks from left to right using an index $i$ (0-based).
4. For each stack, add the current height $h[i]$ to `surplus`. This represents all blocks available for use, including what has been carried over.
5. Check if `surplus` is at least $i$, the minimum number of blocks needed so far to make the sequence strictly increasing. If `surplus < i`, output NO and stop for this test case.
6. Otherwise, subtract $i$ from `surplus` to account for the blocks used to reach the strictly increasing requirement at this position. Continue to the next stack.
7. If all stacks satisfy the requirement, output YES.

The reason this works is that `surplus` tracks the total number of blocks we can shift to the right. The strictly increasing requirement at index $i$ is that there must be at least $i$ blocks accumulated by that point, because the minimum strictly increasing sequence for index $i$ is `[0, 1, 2, ..., n-1]`. If we can meet this requirement at every step, the final distribution can always be realized by shifting blocks right, making the sequence strictly increasing.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))
        surplus = 0
        possible = True
        for i in range(n):
            surplus += h[i]
            if surplus < i:
                possible = False
                break
            surplus -= i
        print("YES" if possible else "NO")

if __name__ == "__main__":
    solve()
```

The solution reads input efficiently using `sys.stdin.readline`. `surplus` accumulates available blocks. At each stack, we ensure there are enough blocks to satisfy the strictly increasing condition. If not, we terminate early to avoid unnecessary computation. Subtracting `i` from `surplus` accounts for using blocks to meet the minimum required at that position. Off-by-one errors are avoided by using 0-based indexing consistently.

## Worked Examples

Consider the input `[3, 4, 4, 4]`:

| i | h[i] | surplus before check | required i | surplus after check |
| --- | --- | --- | --- | --- |
| 0 | 4 | 0+4=4 | 0 | 4-0=4 |
| 1 | 4 | 4+4=8 | 1 | 8-1=7 |
| 2 | 4 | 7+4=11 | 2 | 11-2=9 |

All stacks satisfy the requirement, output is YES.

Input `[0, 1, 0]`:

| i | h[i] | surplus before check | required i | surplus after check |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 0+1=1 | 1 | 1-1=0 |
| 2 | 0 | 0+0=0 | 2 | 0<2 → NO |

This shows the algorithm correctly detects insufficient blocks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each stack is processed exactly once with simple arithmetic |
| Space | O(1) extra | Only a few integers are used; input array dominates memory, which is required anyway |

Given the sum of $n \le 10^4$ over all test cases, this solution runs comfortably within the 1-second limit.

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

# provided samples
assert run("6\n2\n1 2\n2\n1 0\n3\n4 4 4\n2\n0 0\n3\n0 1 0\n4\n1000000000 1000000000 1000000000 1000000000\n") == \
"YES\nYES\nYES\nNO\nNO\nYES"

# custom cases
assert run("1\n1\n0\n") == "YES", "single stack zero"
assert run("1\n1\n100\n") == "YES", "single stack non-zero"
assert run("1\n3\n0 0 0\n") == "NO", "all zeros"
assert run("1\n3\n0 1 2\n") == "YES", "already strictly increasing"
assert run("1\n3\n2 2 2\n") == "YES", "equal heights that can be adjusted"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n0\n` | YES | Single stack zero height |
| `1\n1\n100\n` | YES | Single stack non-zero height |
| `1\n3\n0 0 0\n` | NO | All zeros, cannot increase |
| `1\n3\n0 1 2\n` | YES | Already strictly increasing |
| `1\n3\n2 2 2\n` | YES | Equal heights, can redistribute |

## Edge Cases

For `[0, 0, 1]`, the algorithm computes `surplus=0` at index 0, `surplus=0` at index 1, and `surplus=1` at index 2. The required minimum is 2 at index 2. Since `surplus < i`, it outputs NO. This correctly handles the case where the first two stacks are empty and there is no way to shift blocks left.

For `[1000000000, 1000000000, 1000000000]`, `surplus` grows rapidly: 1e9 → 2e9-1 → 3e9-3. At each step, `surplus >= i`,
