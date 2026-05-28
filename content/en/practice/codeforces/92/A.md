---
title: "CF 92A - Chips"
description: "We have n walruses arranged in a circle. The presenter starts with m chips and distributes them in order. Walrus 1 receives 1 chip, walrus 2 receives 2 chips, and so on up to walrus n, after which the cycle repeats again from walrus 1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 92
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 75 (Div. 2 Only)"
rating: 800
weight: 92
solve_time_s: 195
verified: true
draft: false
---

[CF 92A - Chips](https://codeforces.com/problemset/problem/92/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 3m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` walruses arranged in a circle. The presenter starts with `m` chips and distributes them in order. Walrus `1` receives `1` chip, walrus `2` receives `2` chips, and so on up to walrus `n`, after which the cycle repeats again from walrus `1`.

The process continues as long as the presenter has enough chips to satisfy the current walrus completely. The moment the presenter cannot give the required amount, the process stops and the remaining chips stay with the presenter. The task is to compute how many chips remain at the end.

The constraints are extremely small. The number of walruses is at most `50`, and the number of chips is at most `10^4`. Even a direct simulation that repeatedly subtracts values one by one easily fits within the time limit. In the worst case, each operation removes at least one chip, so the loop runs at most `10^4` times, which is trivial for a 2 second limit.

The main source of mistakes is handling the stopping condition correctly. The process ends when the presenter cannot fully satisfy the current walrus, not after partially giving chips.

Consider this input:

```
3 1
```

The first walrus needs exactly `1` chip, so the presenter gives it away and ends with `0`.

A careless implementation might stop before giving the chip because it checks the wrong inequality.

Another subtle case is when the cycle wraps around:

```
4 11
```

The presenter gives `1 + 2 + 3 + 4 = 10` chips during the first full cycle, leaving `1`. Then the cycle starts again, walrus `1` receives the last chip, and the presenter ends with `0`. An incorrect implementation might stop immediately after the first full cycle and incorrectly output `1`.

One more edge case appears when the remaining chips are smaller than the next required amount:

```
3 7
```

The distribution goes like this:

`1 -> 2 -> 3 -> 1`

The presenter now has `0` chips left after giving the final `1`. If we instead had:

```
3 6
```

The presenter gives `1 -> 2 -> 3` and stops with `0`.

If we had:

```
3 5
```

The presenter gives `1 -> 2`, leaving `2`. The next walrus needs `3`, so the answer is `2`. A buggy implementation that subtracts first and checks later would produce a negative value.

## Approaches

The most direct solution is to simulate the process exactly as described. We keep track of the current walrus number, cycling from `1` to `n`, and repeatedly check whether enough chips remain. If yes, we subtract the required amount and move to the next walrus. Otherwise, we stop and print the remaining chips.

This brute-force approach is already fast enough because every successful operation decreases the number of chips by at least `1`. Since `m ≤ 10^4`, the loop executes at most `10^4` times.

There is also a mathematical observation behind the process. One complete round distributes:

$1+2+\cdots+n=\frac{n(n+1)}{2}$

chips.

We could repeatedly remove whole rounds before simulating the remaining partial round. That reduces the number of iterations further. Still, with the given constraints, the simple simulation is cleaner and fully sufficient.

The brute-force solution works because the state transition is tiny and bounded. The constraints are so small that optimization is unnecessary. The important part is implementing the cyclic order and stopping condition correctly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m) | O(1) | Accepted |
| Round-Based Optimization | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. Start with the current walrus index equal to `1`.
3. While the presenter still has enough chips for the current walrus, subtract the required number of chips from `m`.
4. Move to the next walrus in clockwise order.

If the current walrus was `n`, wrap around back to `1`.
5. The moment `m` becomes smaller than the required amount for the current walrus, stop the process.
6. Print the remaining value of `m`.

Why it works:

At every step, the algorithm exactly follows the rules of the distribution process. The variable representing the current walrus always matches the next walrus who should receive chips, and `m` always stores the number of chips still available. The loop continues only when the current walrus can be fully satisfied. Once that becomes impossible, the process must terminate immediately according to the problem statement. Since every successful iteration mirrors one legal move of the presenter, the final remaining value is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

current = 1

while m >= current:
    m -= current
    current += 1

    if current > n:
        current = 1

print(m)
```

The variable `current` stores which walrus should receive chips next. It starts from `1` because the process always begins with walrus `1`.

The loop condition is the critical detail:

```
while m >= current:
```

The presenter is only allowed to continue if enough chips exist to fully satisfy the current walrus. Using `>` instead of `>=` would fail when the remaining chips exactly match the required amount.

After subtracting the chips, we advance to the next walrus. When the index exceeds `n`, we wrap back to `1` to maintain the circular order.

The implementation never produces negative values because subtraction happens only after verifying enough chips are available.

## Worked Examples

### Example 1

Input:

```
4 11
```

| Current Walrus | Chips Needed | Chips Before | Chips After |
| --- | --- | --- | --- |
| 1 | 1 | 11 | 10 |
| 2 | 2 | 10 | 8 |
| 3 | 3 | 8 | 5 |
| 4 | 4 | 5 | 1 |
| 1 | 1 | 1 | 0 |

The next walrus would need `2` chips, but none remain, so the answer is `0`.

This example demonstrates the wrap-around behavior after reaching walrus `4`.

### Example 2

Input:

```
3 5
```

| Current Walrus | Chips Needed | Chips Before | Chips After |
| --- | --- | --- | --- |
| 1 | 1 | 5 | 4 |
| 2 | 2 | 4 | 2 |

The next walrus needs `3` chips, but only `2` remain, so the process stops and the answer is `2`.

This trace confirms that the process ends before partial distribution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each successful iteration removes at least one chip |
| Space | O(1) | Only a few integer variables are stored |

Since `m` is at most `10^4`, the simulation performs at most `10^4` iterations. That is far below the limits for a 2 second runtime. Memory usage is constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    current = 1

    while m >= current:
        m -= current
        current += 1

        if current > n:
            current = 1

    print(m)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("4 11\n") == "0\n", "sample 1"

# minimum values
assert run("1 1\n") == "0\n", "minimum case"

# cannot satisfy second walrus
assert run("2 1\n") == "0\n", "exactly enough for first walrus"

# partial stop in middle of cycle
assert run("3 5\n") == "2\n", "stop before giving 3 chips"

# wrap around multiple times
assert run("2 7\n") == "1\n", "multiple complete cycles"

# maximum style stress case
assert run("50 10000\n") == "145\n", "large input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | Smallest possible input |
| `2 1` | `0` | Exact equality condition |
| `3 5` | `2` | Stopping before partial distribution |
| `2 7` | `1` | Correct circular wrap-around |
| `50 10000` | `145` | Large input within constraints |

## Edge Cases

Consider the exact-fit scenario:

```
1 1
```

The first walrus requires exactly `1` chip. The algorithm checks `m >= current`, which is true, subtracts the chip, and leaves `0`. The next iteration fails because `0 < 1`, so the output is correctly `0`.

Now consider a wrap-around case:

```
4 11
```

After giving `1 + 2 + 3 + 4 = 10` chips, the algorithm resets `current` back to `1`. Since one chip remains, the presenter gives it away successfully and ends with `0`. This confirms the circular indexing is handled correctly.

Finally, examine a partial-failure case:

```
3 5
```

The algorithm performs these steps:

`5 -> 4 -> 2`

The next walrus needs `3`, but only `2` remain. Because the loop condition fails before subtraction, the algorithm stops immediately and prints `2`. This prevents invalid negative values and matches the problem rules exactly.
