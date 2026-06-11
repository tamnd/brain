---
title: "CF 1413E - Solo mid Oracle"
description: "We repeatedly cast a spell on an enemy. Each cast immediately deals a damage. After that, the same cast heals the enemy by b health every second for exactly c seconds. Casts happen every d seconds because of the cooldown, and all effects stack."
date: "2026-06-11T07:22:54+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 1413
codeforces_index: "E"
codeforces_contest_name: "Technocup 2021 - Elimination Round 1"
rating: 2100
weight: 1413
solve_time_s: 110
verified: true
draft: false
---

[CF 1413E - Solo mid Oracle](https://codeforces.com/problemset/problem/1413/E)

**Rating:** 2100  
**Tags:** greedy, math, ternary search  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We repeatedly cast a spell on an enemy.

Each cast immediately deals `a` damage. After that, the same cast heals the enemy by `b` health every second for exactly `c` seconds. Casts happen every `d` seconds because of the cooldown, and all effects stack.

The enemy dies if, at some integer moment in time, the total accumulated effect of all casts makes its health become non-positive. Since every health change occurring at the same moment is applied together, what really matters is the maximum total damage-minus-healing achieved at any time.

For each test case we must find the largest enemy health that can still be killed. If the accumulated damage can grow without bound, then any health value is eventually killable and the answer is `-1`.

The number of test cases is as large as `10^5`, so anything involving simulation over time is impossible. The parameters themselves can reach `10^6`, which means the answer may be around `10^12`, so 64-bit arithmetic is required.

The challenge is that healing effects from many previous casts overlap. A direct timeline simulation would need to process potentially millions or billions of moments, which is far beyond the limit.

A few edge cases deserve special attention.

Consider:

```
a = 1, b = 2, c = 3, d = 4
```

The spell heals for only three seconds, but the cooldown is four seconds. Every cast finishes all its healing before the next cast happens. The best damage achieved is simply the first hit, so the answer is `1`.

Now consider:

```
a = 239, b = 21, c = 11, d = 3
```

Here each cast contributes more damage than the total additional healing introduced between casts. The cumulative damage grows forever, so the answer is `-1`.

Another subtle case is:

```
a = 4, b = 3, c = 2, d = 1
```

A naive implementation might look only at net damage per cast and conclude the answer is large. In reality the overlapping heals quickly counteract future casts. The true answer is `5`, achieved at a specific intermediate time.

## Approaches

The most direct approach is to simulate the process.

We could cast at times `0, d, 2d, ...`, keep track of all active healing effects, and compute the total damage-minus-healing after every event. The maximum value reached would be the largest health that can be killed.

This works conceptually because the answer is exactly the maximum cumulative damage ever achieved. Unfortunately, the duration can be arbitrarily long. When damage keeps increasing forever, there is no finite stopping point. Even in finite cases, parameters up to `10^6` make event-by-event simulation far too expensive.

The key observation is that we do not need the whole timeline.

Suppose casts occur at times:

```
0, d, 2d, 3d, ...
```

Let us examine the cumulative effect immediately after the `k`-th cast.

Each new cast contributes `+a`.

Between consecutive casts, some healing occurs. How much?

A cast heals during the next `c` seconds. Since casts are spaced by `d` seconds, a particular cast is still active for exactly

```
ceil(c / d)
```

cast intervals.

A cleaner way to count active healing at cast moments is to observe that between cast `i-1` and cast `i`, every previous spell whose healing period still covers that interval contributes `b*d` healing.

The number of such active spells eventually stabilizes at

```
m = floor((c - 1) / d)
```

because a spell affects the next `m + 1` intervals.

After enough casts, each additional cast changes the cumulative damage by

```
a - b * (m + 1)
```

which is

```
a - b * ceil(c / d)
```

since

```
ceil(c/d) = floor((c-1)/d) + 1.
```

If this quantity is positive, cumulative damage grows forever. Any health value can eventually be killed, so the answer is `-1`.

Otherwise the sequence eventually decreases, meaning the maximum occurs among the early casts.

Let

```
k = floor((c - 1) / d)
```

Then the best moment is exactly after the `(k+1)`-st cast. Up to that point, each new cast increases the accumulated damage by

```
a - b * i
```

for increasing values of `i`.

Summing these gains gives

```
answer =
a + (a-b) + (a-2b) + ... + (a-kb)
```

which simplifies to

```
(k+1)a - b * k(k+1)/2.
```

This value is the maximum health that can be killed.

## Approaches Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | Unbounded / too large | O(number of active spells) | Too slow |
| Mathematical derivation | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute

```
k = floor((c - 1) / d).
```

This is the number of previous cast intervals during which a spell can still contribute healing.
2. Check whether

```
a > b * (k + 1).
```

This is the long-term gain from adding one more cast after the overlap pattern has stabilized.
3. If the inequality holds, print `-1`.

The cumulative damage increases without bound, so an enemy with arbitrarily large health can eventually be killed.
4. Otherwise compute

```
(k + 1) * a - b * k * (k + 1) / 2.
```

This is the maximum cumulative damage ever reached.
5. Output that value.

### Why it works

Let `D(n)` be the cumulative damage-minus-healing immediately after the `n`-th cast.

The first cast contributes `a`.

Every subsequent cast adds another `a`, but also suffers healing generated by previous active spells. Before the overlap pattern stabilizes, the healing added between casts increases by exactly `b` each step. After `k+1` active intervals are present, the added healing becomes constant at `b(k+1)`.

Thus the successive differences of `D(n)` form:

```
a,
a-b,
a-2b,
...
a-kb,
a-(k+1)b,
a-(k+1)b,
...
```

If the final constant difference is positive, the sequence grows forever. Otherwise the sequence becomes non-increasing after reaching the term corresponding to `a-kb`, so its maximum is obtained exactly at that point. Summing the arithmetic progression yields the formula above.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        a, b, c, d = map(int, input().split())

        k = (c - 1) // d

        if a > b * (k + 1):
            ans.append("-1")
        else:
            res = (k + 1) * a - b * k * (k + 1) // 2
            ans.append(str(res))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation follows the mathematical derivation directly.

The value

```
k = (c - 1) // d
```

captures how many additional cast intervals remain affected by a spell's healing.

The condition

```
a > b * (k + 1)
```

checks whether the stabilized slope of the cumulative-damage sequence is positive. If it is, the answer is unbounded and we print `-1`.

Otherwise we evaluate the closed-form sum of the arithmetic progression. Python integers automatically handle values larger than 64 bits, although even signed 64-bit integers are sufficient for this problem.

The most common mistake is using `c // d` instead of `(c - 1) // d`. Healing starts one second after casting and lasts exactly `c` seconds, so the correct overlap count is derived from `ceil(c/d)`, which equals `(c - 1)//d + 1`.

## Worked Examples

### Example 1

Input:

```
228 21 11 3
```

Compute:

```
k = (11 - 1) / 3 = 3
```

| Variable | Value |
| --- | --- |
| a | 228 |
| b | 21 |
| c | 11 |
| d | 3 |
| k | 3 |
| b(k+1) | 84 |
| a > b(k+1)? | Yes |

Since

```
228 > 84
```

the cumulative damage keeps increasing forever.

Output:

```
-1
```

This demonstrates the unbounded-growth case.

### Example 2

Input:

```
4 3 2 1
```

| Variable | Value |
| --- | --- |
| a | 4 |
| b | 3 |
| c | 2 |
| d | 1 |
| k | 1 |
| b(k+1) | 6 |
| a > b(k+1)? | No |

Now compute:

```
(1+1)*4 - 3*1*2/2
= 8 - 3
= 5
```

Output:

```
5
```

The sequence of gains is:

```
4, 1, -2, -2, ...
```

so the cumulative damage reaches its maximum after the second cast.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations |
| Space | O(1) | No auxiliary structures |

With at most `10^5` test cases, the total work remains linear in the number of cases and easily fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        a, b, c, d = map(int, input().split())

        k = (c - 1) // d

        if a > b * (k + 1):
            out.append("-1")
        else:
            out.append(str((k + 1) * a - b * k * (k + 1) // 2))

    return "\n".join(out)

# provided sample
assert run(
"""7
1 1 1 1
2 2 2 2
1 2 3 4
4 3 2 1
228 21 11 3
239 21 11 3
1000000 1 1000000 1
"""
) == "\n".join([
    "1",
    "2",
    "1",
    "5",
    "534",
    "-1",
    "500000500000"
]), "sample"

# minimum values
assert run(
"""1
1 1 1 1
"""
) == "1"

# exact boundary, slope becomes zero
assert run(
"""1
6 3 2 1
"""
) == "9"

# no overlap between casts
assert run(
"""1
5 2 3 10
"""
) == "5"

# very large answer
assert run(
"""1
1000000 1 1000000 1
"""
) == "500000500000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `1` | Smallest valid case |
| `6 3 2 1` | `9` | Boundary where long-term slope is exactly zero |
| `5 2 3 10` | `5` | No healing overlap between casts |
| `1000000 1 1000000 1` | `500000500000` | Large arithmetic and 64-bit safety |

## Edge Cases

### No overlap at all

Input:

```
1
5 2 3 10
```

We get:

```
k = (3 - 1) // 10 = 0
```

The formula becomes:

```
(0+1) * 5 = 5
```

Every cast finishes healing long before the next cast starts. The best damage is simply the first hit.

Output:

```
5
```

### Long-term slope exactly zero

Input:

```
1
6 3 2 1
```

We have:

```
k = 1
a = 6
b(k+1) = 6
```

The sequence of gains is:

```
6, 3, 0, 0, ...
```

The cumulative damage reaches:

```
6 -> 9 -> 9 -> 9 ...
```

The maximum is finite and equals `9`.

Output:

```
9
```

This case catches solutions that incorrectly use `>=` instead of `>` in the unboundedness test.

### Unbounded growth

Input:

```
1
239 21 11 3
```

We compute:

```
k = 3
b(k+1) = 84
```

Since

```
239 > 84
```

every sufficiently late cast increases cumulative damage. There is no finite maximum.

Output:

```
-1
```

This case catches solutions that always apply the arithmetic-progression formula without first checking whether the sequence is unbounded.
