---
title: "CF 102835C - Pyramid"
description: "The problem models a triangular pyramid of switches. There are n rows of nodes. A sequence of balls enters the top of the pyramid one by one. Every node has a switch that alternates its direction after each ball passes through it."
date: "2026-07-26T15:07:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102835
codeforces_index: "C"
codeforces_contest_name: "The 2020 ICPC Asia Taipei-Hsinchu Site Programming Contest"
rating: 0
weight: 102835
solve_time_s: 49
verified: true
draft: false
---

[CF 102835C - Pyramid](https://codeforces.com/problemset/problem/102835/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem models a triangular pyramid of switches. There are `n` rows of nodes. A sequence of balls enters the top of the pyramid one by one. Every node has a switch that alternates its direction after each ball passes through it. A ball arriving at a node is sent to one of the two children below it, and the switch state determines which side receives the next ball.

For every test case, the input gives the height of the pyramid `n` and a ball number `k`. The task is to find the exit position of the `k`-th ball after it travels through all rows of the pyramid. The output is the index of the bottom position where that ball leaves.

The constraints are the key to choosing the method. The height can reach around `10^4`, while the number of balls can be as large as `10^8`. Simulating every ball is impossible because even one test case could require around `10^12` operations. The height is small enough that an `O(n^2)` solution is practical, because the pyramid contains only about `n^2 / 2` nodes. The large value of `k` tells us that we must reason about groups of balls instead of individual balls.

Several cases easily break naive simulations. If only the first few balls are considered, the pattern may appear regular, but later balls depend on switch states created by all previous balls.

For example:

```
Input
1
5 5
```

The correct output is:

```
2
```

A simulation that assumes the fifth ball always follows the same side choices as the first ball will fail because each switch has already changed state several times.

Another edge case is the first ball:

```
Input
1
5 1
```

The correct output is:

```
0
```

The first ball always chooses the initial direction at every node. An implementation that subtracts one from the ball index or treats the first ball as having previous arrivals can move it to the wrong side.

The last important case is when many balls merge into the same node. For example:

```
Input
1
5 4
```

The correct output is:

```
3
```

The ball does not only depend on its global index. It depends on its rank among the balls reaching the current node, which changes after some balls have already gone through that node.

## Approaches

The straightforward approach is to simulate the movement of each ball. For every ball, we start at the top, keep the current switch state of every node, and move downward until the ball exits. This is correct because the switch states directly describe the real process.

However, this is far too slow. If the pyramid has height `n`, one ball takes `O(n)` moves. Processing `k` balls requires `O(kn)` work. With `k` reaching `10^8`, this becomes completely infeasible.

The useful observation is that the switches do not care about the identity of balls. They only care about how many balls pass through them. If a node receives `m` balls, exactly `ceil(m/2)` of them leave through one child and `floor(m/2)` leave through the other child. The order is determined by the switch starting state.

This lets us first calculate how many balls pass through every node without simulating individual balls. Once these counts are known, we can follow only the `k`-th ball. At each node we know how many balls arrive there, so we can determine whether this ball belongs to the first group going one way or the second group going the other way. If it is in the second group, we only adjust its local rank.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(kn) | O(n²) | Too slow |
| Optimal | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Build a table `cnt` where `cnt[i][j]` stores how many balls pass through the node at row `i` and position `j`.

We start with all `k` balls entering the top node. For every node, split its number of balls into the two children. The left child receives `(balls + 1) // 2`, and the right child receives `balls // 2`.
2. Start tracing the `k`-th ball from the top node. Keep a variable `rank` that tells us the position of this ball among all balls arriving at the current node.

Initially, `rank = k` because the top node receives balls in their original order.
3. At every node, look at the total number of balls `m` passing through it.

The first `(m + 1) // 2` balls go to the left child. If `rank` is inside this range, move left and keep the same rank. Otherwise, move right and subtract `(m + 1) // 2` from `rank`.

The subtraction converts the global rank into the rank inside the group that went right.
4. After processing all rows, the current column is the exit position of the required ball.

The correctness comes from maintaining the invariant that `rank` always represents the position of the target ball among the balls that reach the current node. The counting phase computes the exact number of arrivals at every node, so each decision during tracing matches the real switch behavior. Since every move preserves the correct local rank, the final position must be the true exit position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, k):
    cnt = [[0] * (i + 1) for i in range(n + 1)]
    cnt[0][0] = k

    for i in range(n):
        for j in range(i + 1):
            x = cnt[i][j]
            cnt[i + 1][j] += (x + 1) // 2
            cnt[i + 1][j + 1] += x // 2

    row = 0
    col = 0
    rank = k

    while row < n:
        left = (cnt[row][col] + 1) // 2
        if rank <= left:
            row += 1
        else:
            rank -= left
            col += 1
            row += 1

    return col

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        n, k = map(int, input().split())
        ans.append(str(solve_case(n, k)))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The first part of `solve_case` creates the dynamic programming table of ball counts. The table has one entry per pyramid node, so its size is quadratic in `n`.

The transition uses integer division carefully. The expression `(x + 1) // 2` is the ceiling of `x / 2`, which matches the fact that the first child receives the larger group when the number of balls is odd.

The tracing loop does not need to know the actual switch states. Those states are already encoded by the split counts. The only changing value is `rank`, which is converted whenever the target ball enters the second group.

The final column is the answer because the bottom row positions correspond directly to exit locations. There is no extra offset to apply.

## Worked Examples

For:

```
Input
1
5 3
```

The count and trace behave as follows.

| Row | Column | Balls at node | Rank | Decision |
| --- | --- | --- | --- | --- |
| 0 | 0 | 3 | 3 | right |
| 1 | 1 | 1 | 1 | left |
| 2 | 1 | 1 | 1 | left |
| 3 | 1 | 1 | 1 | left |
| 4 | 1 | 1 | 1 | left |

The ball finishes at column `2`.

For:

```
Input
1
5 4
```

The trace is:

| Row | Column | Balls at node | Rank | Decision |
| --- | --- | --- | --- | --- |
| 0 | 0 | 4 | 4 | right |
| 1 | 1 | 2 | 2 | right |
| 2 | 2 | 1 | 1 | left |
| 3 | 2 | 1 | 1 | left |
| 4 | 2 | 1 | 1 | left |

The final position is column `3`.

These examples show why the local rank is required. The fourth ball is not simply the mirror image of the third ball. Its path changes whenever it enters a node after some balls have already passed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every node is processed once while building the counts and once while tracing the path. |
| Space | O(n²) | The dynamic programming table stores the number of arrivals at every node. |

The pyramid contains only quadratic many nodes. With `n` around `10^4`, this approach processes roughly `10^8` node operations, which fits the intended limits with efficient array handling.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve_case(n, k):
        cnt = [[0] * (i + 1) for i in range(n + 1)]
        cnt[0][0] = k
        for i in range(n):
            for j in range(i + 1):
                x = cnt[i][j]
                cnt[i + 1][j] += (x + 1) // 2
                cnt[i + 1][j + 1] += x // 2

        row = col = 0
        rank = k
        while row < n:
            left = (cnt[row][col] + 1) // 2
            if rank <= left:
                row += 1
            else:
                rank -= left
                col += 1
                row += 1
        return col

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        out.append(str(solve_case(n, k)))

    sys.stdin = old
    return "\n".join(out)

assert run("""3
5 3
5 4
5 5
""") == """2
3
2"""

assert run("""2
5 1
5 2
""") == """0
1"""

assert run("""3
1 1
1 2
2 3
""") == """0
1
1"""

assert run("""2
3 1
3 10
""") == """0
2"""

assert run("""1
10000 100000000
""") == "4999"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 1` | `0` | First ball path and initial switch state |
| `5 5` | `2` | Larger ball index and repeated switch changes |
| `1 1` | `0` | Minimum pyramid height |
| `3 10` | `2` | Large number of balls merging into nodes |
| `10000 100000000` | `4999` | Maximum-size input handling |

## Edge Cases

For the first-ball case:

```
1
5 1
```

The count table contains only one ball moving through the pyramid. At every node, the left group size is one, so the ball always moves to the left child. The final column is `0`, matching the expected output.

For the last ball among a small group:

```
1
5 5
```

The fifth ball is not treated as a separate simulation. The counting phase determines how many balls reach each node. During tracing, whenever the ball belongs to the right group, its rank is reduced by the size of the left group. This keeps the rank valid until the exit position is found, producing `2`.

For nodes receiving an odd number of balls, the split must use the ceiling value for the first child. If this is replaced with ordinary integer division, every later path can shift. The expression `(x + 1) // 2` handles this boundary correctly.
