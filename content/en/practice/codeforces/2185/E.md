---
title: "CF 2185E - The Robotic Rush"
description: "Every robot receives exactly the same sequence of moves. After the first instruction, all robots shift by the same displacement. After the second instruction, all robots shift by another common displacement, and so on."
date: "2026-06-07T21:31:20+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2185
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1074 (Div. 4)"
rating: 1500
weight: 2185
solve_time_s: 166
verified: true
draft: false
---

[CF 2185E - The Robotic Rush](https://codeforces.com/problemset/problem/2185/E)

**Rating:** 1500  
**Tags:** binary search, greedy, implementation, two pointers  
**Solve time:** 2m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

Every robot receives exactly the same sequence of moves. After the first instruction, all robots shift by the same displacement. After the second instruction, all robots shift by another common displacement, and so on.

Let $p_i$ be the cumulative displacement after the first $i$ instructions. A robot that started at position $a$ will be at position $a + p_i$ after step $i$.

A robot dies the first time it lands on a spike. We must output, for every prefix of instructions, how many robots are still alive.

The first observation is that robots never interact with each other. Whether one robot survives depends only on its own starting position and the spike locations. This lets us compute an independent death time for each robot.

The constraints are the real challenge. Across all test cases, the sums of $n$, $m$, and $k$ are each at most $2 \cdot 10^5$. Any solution that simulates every robot for every instruction would require $O(nk)$ work, which can reach $4 \cdot 10^{10}$ operations and is completely infeasible. We need something close to $O((n+m+k)\log k)$.

A subtle edge case appears when a robot never reaches any spike. For example:

```
1
1 1 3
10
100
LRL
```

The robot only moves near position 10 while the spike is at 100. The correct answers are:

```
1 1 1
```

A solution that only looks at the final position would incorrectly conclude that some earlier collision occurred.

Another easy mistake is forgetting that touching a spike at any intermediate time kills the robot immediately. Consider:

```
1
1 1 2
1
2
RL
```

The robot moves $1 \to 2 \to 1$. It dies after the first move, so the answer is:

```
0 0
```

Checking only the position after all instructions would miss this collision.

The final non-obvious case is that a robot can die because of a spike on either side. For example:

```
robot = 10
spikes = {7, 20}
moves = LLL
```

The robot reaches 7 on the third move and dies. Looking only at the nearest spike to the right would be incorrect.

## Approaches

The brute-force idea is straightforward. For every robot, simulate the instruction sequence step by step, update its position, and check whether it stands on a spike. The first step where this happens is its death time.

This is correct because it exactly follows the process described in the statement. Unfortunately, it performs $O(nk)$ updates. With both values near $2 \cdot 10^5$, the running time becomes far too large.

The key observation is that all robots share the same displacement sequence.

Let

$$p_i$$

be the cumulative displacement after $i$ instructions.

For a robot starting at position $a$, its position after step $i$ is

$$a+p_i.$$

A robot dies if some spike position lies among all positions it has visited.

Suppose we know the minimum and maximum cumulative displacement reached during the first $i$ instructions:

$$L_i=\min_{1\le j\le i} p_j,
\qquad
R_i=\max_{1\le j\le i} p_j.$$

Because every move changes the position by exactly one unit, the walk visits every integer point between its minimum and maximum displacement. Thus, during the first $i$ instructions, a robot starting at $a$ visits exactly the interval

$$[a+L_i,\; a+R_i].$$

So the robot is alive after $i$ steps if and only if no spike lies inside this interval. The only spikes that matter are the nearest spike to the left and the nearest spike to the right of the robot's starting position.

For each robot, we can binary search the largest prefix length for which the interval still avoids both neighboring spikes. That gives the last step where the robot is alive. After computing this value for every robot, we only need to count how many robots survive each prefix length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nk)$ | $O(m)$ | Too slow |
| Optimal | $O((m+k)\log m + n(\log m+\log k))$ | $O(m+k+n)$ | Accepted |

## Algorithm Walkthrough

### 1. Compute cumulative displacement extremes

Process the instruction string once.

Maintain the current displacement $p$.

For every prefix $i$, store:

$$L_i=\min(L_{i-1},p),$$

and

$$R_i=\max(R_{i-1},p).$$

These values describe the leftmost and rightmost displacement reached during the first $i$ instructions.

### 2. Sort spike positions

Sort all spike coordinates.

For each robot position $a$, find:

- the nearest spike strictly to the left,
- the nearest spike strictly to the right.

This is done with binary search in the sorted spike array.

### 3. Binary search the survival length of each robot

For a fixed robot at position $a$, let:

- $left$ be its nearest left spike,
- $right$ be its nearest right spike.

For a prefix length $mid$, the robot remains alive exactly when

$$left < a+L_{mid}$$

and

$$a+R_{mid} < right.$$

The first inequality means the explored interval has not reached the left spike. The second means it has not reached the right spike.

These conditions are monotone. Once a robot dies, it can never become alive again. Hence we binary search the largest prefix length satisfying both inequalities.

Call this value $c$. The robot is alive after steps $1,2,\dots,c$ and dead afterwards.

### 4. Count survivors for every step

Store all values $c$.

Sort them.

For each instruction count $i$, we need the number of robots with

$$c \ge i.$$

A two-pointer sweep over the sorted array gives all answers in linear time.

### Why it works

For any prefix of instructions, every robot follows the same displacement walk. The set of displacements visited during that walk is exactly the interval between the minimum and maximum displacement reached so far.

A robot starting at position $a$ therefore visits exactly the interval $[a+L_i,a+R_i]$. The robot survives if and only if no spike lies inside that interval.

The nearest left and right spikes completely determine whether the interval contains a spike. If the interval stays strictly between them, all other spikes are even farther away and cannot be reached. If either neighboring spike enters the interval, the robot dies immediately.

The survival condition is monotone with respect to the prefix length, so binary search correctly finds the last surviving prefix. Counting robots whose survival length is at least $i$ yields the number alive after $i$ instructions.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, m, k = map(int, input().split())
        robots = list(map(int, input().split()))
        spikes = sorted(map(int, input().split()))
        s = input().strip()

        min_disp = [0] * (k + 1)
        max_disp = [0] * (k + 1)

        cur = 0
        for i, ch in enumerate(s, 1):
            if ch == 'L':
                cur -= 1
            else:
                cur += 1

            min_disp[i] = min(min_disp[i - 1], cur)
            max_disp[i] = max(max_disp[i - 1], cur)

        NEG_INF = -10**18
        POS_INF = 10**18

        survive = []

        for a in robots:
            pos = bisect_left(spikes, a)

            left_spike = spikes[pos - 1] if pos > 0 else NEG_INF
            right_spike = spikes[pos] if pos < m else POS_INF

            lo, hi = 1, k
            best = 0

            while lo <= hi:
                mid = (lo + hi) // 2

                alive = (
                    left_spike < a + min_disp[mid]
                    and a + max_disp[mid] < right_spike
                )

                if alive:
                    best = mid
                    lo = mid + 1
                else:
                    hi = mid - 1

            survive.append(best)

        survive.sort()

        ans = []
        ptr = 0

        for step in range(1, k + 1):
            while ptr < n and survive[ptr] < step:
                ptr += 1
            ans.append(str(n - ptr))

        print(*ans)

solve()
```

The first section computes the cumulative displacement extrema. `min_disp[i]` and `max_disp[i]` describe the entire range explored by the movement sequence up to step `i`.

For each robot, we locate the neighboring spikes using binary search on the sorted spike array. Infinite sentinels are used when a spike does not exist on one side. This avoids special-case logic later.

The binary search over instruction prefixes relies on monotonicity. If a robot survives a longer prefix, it also survives every shorter prefix. Conversely, once a spike enters the explored interval, every larger prefix remains invalid.

The final counting phase is easy to get wrong. `survive[i]` stores the largest step index for which a robot is still alive. A robot contributes to answer `step` exactly when `survive[i] >= step`. Sorting these values allows a single pointer sweep.

## Worked Examples

### Sample 1

Input:

```
2 1 3
0 1
2
LRR
```

The displacement prefixes are:

| Step | Move | Displacement | Min | Max |
| --- | --- | --- | --- | --- |
| 1 | L | -1 | -1 | 0 |
| 2 | R | 0 | -1 | 0 |
| 3 | R | 1 | -1 | 1 |

Robot at 0:

| Step | Interval Visited | Spike 2 reached? |
| --- | --- | --- |
| 1 | [-1,0] | No |
| 2 | [-1,0] | No |
| 3 | [-1,1] | No |

Robot at 1:

| Step | Interval Visited | Spike 2 reached? |
| --- | --- | --- |
| 1 | [0,1] | No |
| 2 | [0,1] | No |
| 3 | [0,2] | Yes |

The survival lengths are `[3, 2]`.

Answers:

```
2 2 1
```

This example shows why the interval interpretation works. The second robot dies exactly when the right endpoint reaches the spike.

### Sample 3

Input:

```
3 2 3
1 3 7
9 6
RRL
```

Prefix statistics:

| Step | Displacement | Min | Max |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 1 |
| 2 | 2 | 0 | 2 |
| 3 | 1 | 0 | 2 |

Robot at 7 has a spike at 9 on its right.

| Step | Interval |
| --- | --- |
| 1 | [7,8] |
| 2 | [7,9] |
| 3 | [7,9] |

It dies at step 2.

Robot at 1 and robot at 3 never reach either spike.

Answers:

```
3 2 2
```

This demonstrates that only the maximum and minimum displacement matter. The exact path between them is irrelevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((m+k)\log m + n(\log m+\log k))$ | sorting spikes, locating neighbors, and binary searching survival length |
| Space | $O(n+m+k)$ | spike array, prefix extrema, and survival lengths |

Since the total sums of $n$, $m$, and $k$ across all test cases are at most $2 \cdot 10^5$, this complexity easily fits within the limits.

## Test Cases

```python
import sys, io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    out = []

    t = int(input())

    for _ in range(t):
        n, m, k = map(int, input().split())
        robots = list(map(int, input().split()))
        spikes = sorted(map(int, input().split()))
        s = input().strip()

        mn = [0] * (k + 1)
        mx = [0] * (k + 1)

        cur = 0
        for i, ch in enumerate(s, 1):
            cur += -1 if ch == 'L' else 1
            mn[i] = min(mn[i - 1], cur)
            mx[i] = max(mx[i - 1], cur)

        surv = []

        for a in robots:
            p = bisect_left(spikes, a)

            left = spikes[p - 1] if p else -10**18
            right = spikes[p] if p < m else 10**18

            lo, hi = 1, k
            best = 0

            while lo <= hi:
                mid = (lo + hi) // 2

                if left < a + mn[mid] and a + mx[mid] < right:
                    best = mid
                    lo = mid + 1
                else:
                    hi = mid - 1

            surv.append(best)

        surv.sort()

        ptr = 0
        ans = []
        for step in range(1, k + 1):
            while ptr < n and surv[ptr] < step:
                ptr += 1
            ans.append(str(n - ptr))

        out.append(" ".join(ans))

    return "\n".join(out)

# provided sample
assert run("""3
2 1 3
0 1
2
LRR
2 3 3
2 4
1 3 5
LRL
3 2 3
1 3 7
9 6
RRL
""") == """2 2 1
0 0 0
3 2 2"""

# minimum size
assert run("""1
1 1 1
0
10
L
""") == "1"

# dies immediately
assert run("""1
1 1 2
1
2
RL
""") == "0 0"

# no spike ever reached
assert run("""1
1 1 3
10
100
LRL
""") == "1 1 1"

# left-side collision
assert run("""1
1 1 3
10
7
LLL
""") == "1 1 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single robot, distant spike | `1` | Minimum sizes |
| `1 -> 2` collision | `0 0` | Immediate death |
| Spike far away | `1 1 1` | Robot survives forever |
| Left spike at distance 3 | `1 1 0` | Left-side collision handling |

## Edge Cases

### Robot never reaches any spike

Input:

```
1
1 1 3
10
100
LRL
```

The displacement range after every prefix remains inside $[-1,0]$. The visited intervals are:

```
[9,10]
[9,10]
[9,10]
```

The spike at 100 never enters the interval, so the binary search returns survival length 3. The answers are:

```
1 1 1
```

### Immediate collision

Input:

```
1
1 1 2
1
2
RL
```

After the first move, the robot stands on 2. The interval after step 1 is:

```
[1,2]
```

which already contains the spike. The largest surviving prefix is 0, producing:

```
0 0
```

### Collision from the left side

Input:

```
1
1 1 3
10
7
LLL
```

The displacement minima become:

```
-1, -2, -3
```

After step 3, the visited interval is:

```
[7,10]
```

which reaches the spike at 7. The robot survives exactly two steps, giving:

```
1 1 0
```

This case confirms that checking only spikes to the right would be incorrect. The nearest spike on either side must be considered.
