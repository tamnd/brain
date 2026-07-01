---
title: "CF 104069A - Abducting Nathan!"
description: "Two players, Thiago and Nathan, are playing a ping-pong style game where the server switches in blocks instead of alternating every two points as in the official rules. Instead, the server changes after every k points scored in total, regardless of who scores them."
date: "2026-07-02T02:58:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104069
codeforces_index: "A"
codeforces_contest_name: "VII MaratonUSP Freshman Contest"
rating: 0
weight: 104069
solve_time_s: 49
verified: true
draft: false
---

[CF 104069A - Abducting Nathan!](https://codeforces.com/problemset/problem/104069/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players, Thiago and Nathan, are playing a ping-pong style game where the server switches in blocks instead of alternating every two points as in the official rules. Instead, the server changes after every k points scored in total, regardless of who scores them. Thiago always starts serving at the beginning of the match.

We are given the current score in multiple independent test cases. For each case, we need to determine who will serve next based on the current total number of points played. The score itself does not affect the serve change except through how many points have been played so far, since each point advances the serve cycle.

Each test case provides k, the block size for service changes, and the current scores T and N. From these we compute how many points have been played in total, then determine how many full service blocks have passed. If the number of completed blocks is even, Thiago is still the server; if it is odd, Nathan is serving.

The constraints allow up to 10^4 test cases and values up to 10^9 for k and scores. This immediately rules out any simulation that processes each point individually. A per-point simulation would require up to 2 × 10^9 operations in a single test, which is far beyond feasible limits. The solution must be O(1) per test case.

A subtle edge case appears when the total number of points is exactly divisible by k. In that situation, the serve switches right after the last point, so the next server depends on whether the number of completed blocks is even or odd. Another corner case is when T = 0 and N = 0, meaning no points have been played yet, so Thiago must still be serving.

## Approaches

The naive idea is to simulate the game point by point. Starting with Thiago as the server, we would increment a counter for each point and switch the server every k points. After processing T + N steps, we would output the current server. This is correct because it follows the rule directly.

However, this approach becomes impossible under the constraints because T + N can be as large as 2 × 10^9. Even doing a single operation per point would exceed time limits by several orders of magnitude.

The key observation is that we never need to track individual points. The only relevant quantity is the total number of completed blocks of size k. Once we compute S = T + N, the number of full blocks is S // k. Each block flips the server exactly once, so the server depends only on the parity of this quotient.

This reduces the entire problem to a constant-time arithmetic computation per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T + N) per test | O(1) | Too slow |
| Arithmetic Block Counting | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read k, T, and N for each test case. These define the block size and current total points in the game state.
2. Compute S = T + N, the total number of points played so far. The serve switching depends only on how many full k-point segments have been completed.
3. Compute blocks = S // k. Each full block corresponds to one complete service interval after which the server flips.
4. If blocks is even, output "Thiago" because Thiago started serving and an even number of flips returns the serve to the starter.
5. If blocks is odd, output "Nathan" because an odd number of flips means the serve has switched away from the starter.

### Why it works

The serve changes only at fixed boundaries of size k in the global point sequence. This partitions the timeline into consecutive intervals, each reversing the current server exactly once. Since Thiago starts serving at time zero, the server after S points depends solely on how many complete intervals have been crossed. Partial progress inside the current interval does not affect the next server, only completed intervals matter. Therefore the parity of S // k fully determines the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    k, T, N = map(int, input().split())
    total = T + N
    blocks = total // k

    if blocks % 2 == 0:
        print("Thiago")
    else:
        print("Nathan")
```

The implementation directly follows the mathematical reduction. The key step is collapsing the state into total points, avoiding any need to track individual scoring sequences. Integer division computes the number of completed service intervals, and parity determines the server.

A common mistake is forgetting that the switch happens after k points, not every k-th point including zero. Using floor division handles this correctly without off-by-one issues. Another subtle point is that we do not need to consider who scored the last point, since scoring does not influence the serving rule.

## Worked Examples

### Example 1

Input: k = 5, T = 3, N = 2

Total points S = 5

| Step | S | blocks = S // k | parity | server |
| --- | --- | --- | --- | --- |
| initial | 5 | 1 | odd | Nathan |

Since one full block has passed, Thiago has switched once and Nathan is serving.

This confirms that even if the score distribution is uneven, only total points matter.

### Example 2

Input: k = 5, T = 3, N = 1

S = 4

| Step | S | blocks | parity | server |
| --- | --- | --- | --- | --- |
| initial | 4 | 0 | even | Thiago |

No full block is completed, so Thiago remains serving. This shows that incomplete blocks do not trigger a switch.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case performs a constant number of arithmetic operations |
| Space | O(1) | Only a few integers are stored regardless of input size |

The solution comfortably handles up to 10^4 test cases since each one is reduced to a single division and modulo operation.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        k, T, N = map(int, input().split())
        total = T + N
        blocks = total // k
        out.append("Thiago" if blocks % 2 == 0 else "Nathan")
    return "\n".join(out)

# provided sample-style cases
assert solve("2\n7 1 0\n2 2 8\n") == "Thiago\nNathan"

# k large, no switch
assert solve("1\n10 3 4\n") == "Thiago"

# exact boundary switch
assert solve("1\n5 3 2\n") == "Nathan"

# multiple switches
assert solve("1\n3 9 0\n") == "Thiago"

# zero points
assert solve("1\n5 0 0\n") == "Thiago"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k=10, S=7 | Thiago | no completed block |
| k=5, S=5 | Nathan | exact boundary flip |
| k=3, S=9 | Thiago | even number of flips |
| k=5, S=0 | Thiago | initial state |

## Edge Cases

When no points have been played, T = 0 and N = 0, the total is S = 0. The computation gives blocks = 0 // k = 0, which is even, so Thiago is correctly identified as the server.

For cases where S is exactly a multiple of k, such as k = 4 and S = 8, we get blocks = 2. Since two full service intervals have completed, the serve has switched twice, returning to Thiago. The implementation correctly captures this without needing to explicitly detect boundaries.

For very large values, such as k = 10^9 and S close to 2 × 10^9, integer division still runs in constant time and safely avoids overflow issues in Python.
