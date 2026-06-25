---
title: "CF 105790D - Course Deviation"
description: "A spaceship is approaching a landing strip. Between the ship and the landing strip there are $N$ mountains. The ship moves forward at a constant speed of 1 kilometer per second and simultaneously descends at a constant rate of 1 kilometer per second."
date: "2026-06-26T03:49:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105790
codeforces_index: "D"
codeforces_contest_name: "UDESC Selection Contest 2024-1"
rating: 0
weight: 105790
solve_time_s: 34
verified: true
draft: false
---

[CF 105790D - Course Deviation](https://codeforces.com/problemset/problem/105790/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

A spaceship is approaching a landing strip. Between the ship and the landing strip there are $N$ mountains. The ship moves forward at a constant speed of 1 kilometer per second and simultaneously descends at a constant rate of 1 kilometer per second.

If the ship starts its descent from altitude $H$, then after one second it passes the first mountain at altitude $H-1$, after two seconds it passes the second mountain at altitude $H-2$, and in general it passes the $i$-th mountain at altitude $H-(i+1)$ when using zero-based indexing.

Each mountain has height $h_i$. The ship must stay strictly above every mountain it passes. The task is to find the smallest initial altitude $H$ that guarantees no collision.

The input consists of the number of mountains and their heights. The output is a single integer, the minimum safe starting altitude.

The mountain heights can be as large as $10^9$. This immediately rules out any simulation over altitude values or any approach that tries all possible starting heights. The number of mountains can be large enough that the solution should process each mountain only once, which suggests an $O(N)$ scan.

The main source of mistakes is the strict inequality. The ship cannot merely reach the top of a mountain, it must remain above it.

Consider:

```
1
10
```

If the initial altitude is 11, the ship reaches altitude 10 when passing the mountain. That is a collision because the altitude is not strictly greater than the mountain height. The correct answer is:

```
12
```

Another easy mistake is forgetting that the ship loses altitude before reaching the first mountain.

Example:

```
3
2 2 1
```

At altitude 4, the ship reaches the first mountain at altitude 3, the second at altitude 2, and collides with the second mountain. The correct answer is:

```
5
```

A third pitfall is using one-based and zero-based indices inconsistently.

Example:

```
2
1 100
```

For the second mountain, the ship is at altitude $H-2$, not $H-1$. The correct condition becomes $H > 102$, giving answer:

```
103
```

A wrong indexing scheme would produce 102.

## Approaches

The most direct approach is to try candidate starting altitudes one by one. For each altitude $H$, simulate the flight and verify whether every mountain is cleared. This simulation is correct because it checks exactly the conditions described in the problem.

The problem is that the required altitude can exceed $10^9$. Testing every possible altitude up to the answer would require billions of checks, which is completely infeasible.

A slightly smarter version performs binary search on the answer. For a fixed altitude $H$, we can verify safety in $O(N)$ time. Since the answer lies within a range of roughly $10^9$, binary search needs about 31 iterations, giving $O(N \log 10^9)$.

The key observation removes even the binary search.

When passing mountain $i$, the ship's altitude equals:

$$H - (i+1)$$

To avoid collision:

$$H - (i+1) > h_i$$

Rearranging:

$$H > h_i + i + 1$$

Since this must hold for every mountain, $H$ must be strictly larger than the maximum value of $h_i + i + 1$.

The smallest integer satisfying that requirement is:

$$H = \max(h_i + i + 1) + 1$$

which can also be written as:

$$H = \max(h_i + i + 2)$$

Now the answer is obtained by a single scan through the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \cdot A)$ | $O(1)$ | Too slow |
| Binary Search | $O(N \log A)$ | $O(1)$ | Accepted |
| Optimal | $O(N)$ | $O(1)$ | Accepted |

Here $A$ denotes the magnitude of the answer.

## Algorithm Walkthrough

1. Read $N$ and the mountain heights.
2. Initialize `answer = 0`.
3. For every mountain at index `i`:

Compute `h[i] + i + 2`.

This value is exactly the minimum starting altitude required to clear that particular mountain safely.
4. Update `answer` with the maximum value seen so far.

Every mountain imposes a lower bound on the starting altitude. The strongest lower bound determines the final answer.
5. Output `answer`.

### Why it works

For mountain $i$, the ship reaches altitude $H-(i+1)$. Safety requires:

$$H-(i+1) > h_i$$

which is equivalent to:

$$H \ge h_i+i+2$$

because $H$ is an integer.

Every mountain generates one such lower bound. Any altitude smaller than the maximum bound fails for at least one mountain. The maximum bound itself satisfies all inequalities simultaneously. Since it is both sufficient and necessary, it is the minimum valid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
h = list(map(int, input().split()))

ans = 0

for i in range(n):
    ans = max(ans, h[i] + i + 2)

print(ans)
```

The implementation mirrors the mathematical derivation directly.

The expression `h[i] + i + 2` comes from converting the strict inequality into an integer lower bound. Using `+1` instead of `+2` would be incorrect because the ship must remain strictly above the mountain.

The loop computes the requirement imposed by each mountain and keeps only the largest one. No additional storage is needed beyond the input array and the running maximum.

Python integers automatically handle values larger than $10^9$, so overflow is not a concern.

## Worked Examples

### Example 1

Input:

```
3
2 2 1
```

| i | h[i] | h[i] + i + 2 | Current Maximum |
| --- | --- | --- | --- |
| 0 | 2 | 4 | 4 |
| 1 | 2 | 5 | 5 |
| 2 | 1 | 5 | 5 |

Answer:

```
5
```

The second mountain is the limiting factor. Starting at altitude 5 clears every mountain, while altitude 4 collides with the second mountain.

### Example 2

Input:

```
5
4 2 3 1 5
```

| i | h[i] | h[i] + i + 2 | Current Maximum |
| --- | --- | --- | --- |
| 0 | 4 | 6 | 6 |
| 1 | 2 | 5 | 6 |
| 2 | 3 | 7 | 7 |
| 3 | 1 | 6 | 7 |
| 4 | 5 | 11 | 11 |

Answer:

```
11
```

The final mountain forces the highest starting altitude. Any smaller value would place the ship at altitude at most 5 when passing that mountain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | One scan through the mountains |
| Space | $O(1)$ | Only a running maximum is stored |

The algorithm performs a constant amount of work per mountain and never revisits elements. This comfortably fits typical competitive programming limits even when $N$ is very large.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    h = list(map(int, input().split()))

    ans = 0
    for i in range(n):
        ans = max(ans, h[i] + i + 2)

    return str(ans)

# provided samples
assert run("3\n2 2 1\n") == "5", "sample 1"
assert run("1\n10\n") == "12", "sample 2"
assert run("5\n3 4 2 3 1\n") == "8", "sample 3"

# custom cases
assert run("1\n1\n") == "3", "minimum size"
assert run("4\n5 5 5 5\n") == "10", "all equal"
assert run("2\n1 100\n") == "103", "indexing boundary"
assert run("3\n1000000000 1000000000 1000000000\n") == "1000000004", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `3` | Smallest possible instance |
| `4 / 5 5 5 5` | `10` | All heights equal |
| `2 / 1 100` | `103` | Correct altitude loss per mountain |
| `3 / 10^9 10^9 10^9` | `1000000004` | Large values and integer handling |

## Edge Cases

Consider:

```
1
10
```

The algorithm computes:

$$10 + 0 + 2 = 12$$

and outputs 12.

Checking manually, altitude 11 reaches the mountain at altitude 10, which is not strictly above it. The strict inequality is handled correctly.

Consider:

```
3
2 2 1
```

The computed values are:

$$4,\ 5,\ 5$$

so the answer is 5.

At altitude 4, the ship passes the second mountain at altitude 2 and collides. The maximum requirement correctly identifies the minimum safe altitude.

Consider:

```
2
1 100
```

The algorithm computes:

$$1+0+2=3$$

and

$$100+1+2=103$$

giving answer 103.

The second mountain is reached after two seconds, not one. The formula automatically incorporates the correct altitude loss through the index term `i + 1`, avoiding off-by-one mistakes.
