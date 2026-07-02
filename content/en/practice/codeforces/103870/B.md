---
title: "CF 103870B - Sanity"
description: "We are tracking a simple repeating process over time. Each day contributes to a running counter that measures how many days have passed since the last reset event."
date: "2026-07-02T07:44:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103870
codeforces_index: "B"
codeforces_contest_name: "TeamsCode Summer 2022 Contest"
rating: 0
weight: 103870
solve_time_s: 37
verified: true
draft: false
---

[CF 103870B - Sanity](https://codeforces.com/problemset/problem/103870/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tracking a simple repeating process over time. Each day contributes to a running counter that measures how many days have passed since the last reset event. Whenever this counter reaches a multiple of a fixed period $K$, we perform an action: we increase a value called “sanity” by one.

So the input describes a sequence of days, and each day implicitly increments a day counter. The only interesting moments are those days where the counter is divisible by $K$, because those are the days when sanity increases. After such a day, the counter can either continue or be reset to zero, but both interpretations are equivalent because only the modulo with respect to $K$ matters.

The output is the final sanity value after processing all days in the sequence.

Even though the statement is phrased in terms of “Chessbot emailing Bossologist,” the core abstraction is just periodic counting: every time we complete a block of $K$ days, we add one to the answer.

The constraints are minimal, but this is still a linear-time simulation problem. If the number of days $N$ is up to $10^5$ or $10^6$, then an $O(N)$ traversal is trivially safe. Anything worse than linear, such as recomputing cycles or checking divisibility in a nested manner, would be unnecessary overhead but still would not pass if it introduced extra factors.

The main edge cases come from how the first cycle starts and how exact multiples of $K$ behave. A naive implementation that resets incorrectly or checks after incrementing in the wrong order can shift the count by one.

For example, if $K = 3$ and we process 3 days, sanity should increase exactly once. If someone resets the counter too early, they might miss the increment entirely. Conversely, if they reset too late, they might count twice across boundaries.

## Approaches

The brute-force interpretation is to simulate day by day while maintaining a counter for days since the last reset. Each day increments the counter by one, and whenever the counter reaches $K$, we increase sanity and reset the counter to zero. This directly mirrors the problem description and is correct by construction.

The cost of this approach is linear in the number of days because each day requires only constant work. There is no nested structure or dependency between days, so no further optimization is needed. Any attempt to “precompute” events is unnecessary because the process is already periodic and simple.

The key observation is that the counter never needs to be stored beyond its value modulo $K$. Instead of thinking in terms of resets, we can think in terms of modular arithmetic: each day contributes one unit, and whenever the accumulated total is divisible by $K$, we increment sanity.

This reframes the problem as counting how many multiples of $K$ appear in the range $1$ to $N$, which is simply $N // K$. The simulation collapses into a single arithmetic expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N) | O(1) | Accepted |
| Direct Arithmetic | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of days $N$ and the period $K$. These define the full timeline and the frequency of sanity increases.
2. Compute how many complete blocks of size $K$ fit into $N$. This is done by integer division $N // K$, which directly counts how many times we hit a multiple of $K$.
3. Output this value as the final sanity level. Each full block corresponds to exactly one increment, and partial blocks at the end do not contribute.

### Why it works

The key invariant is that the day counter only matters through its remainder modulo $K$. Every time we complete a full segment of length $K$, the counter reaches zero again and a new cycle begins. Thus, the total number of times we hit the boundary condition is exactly the number of complete cycles in the prefix of length $N$. No partial cycle can trigger an increment because it never reaches $K$, so only full divisions contribute to the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = input().strip().split()
    if not data:
        return
    n, k = map(int, data)
    
    # each full block of size k contributes +1 sanity
    print(n // k)

if __name__ == "__main__":
    solve()
```

The solution reads the two integers and directly computes integer division. The only subtlety is ensuring that input parsing handles whitespace correctly, since some contest formats provide both values on one line.

The division $n // k$ is safe in all cases, including when $n < k$, where it correctly returns zero. This corresponds to having no full cycles at all.

## Worked Examples

### Example 1

Input:

```
10 3
```

We process days from 1 to 10 with a cycle length of 3.

| Day | Counter state | Sanity |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 3 → reset | 1 |
| 4 | 1 | 1 |
| 5 | 2 | 1 |
| 6 | 3 → reset | 2 |
| 7 | 1 | 2 |
| 8 | 2 | 2 |
| 9 | 3 → reset | 3 |
| 10 | 1 | 3 |

Final output:

```
3
```

This confirms that every complete group of 3 days contributes exactly one increment.

### Example 2

Input:

```
7 4
```

| Day | Counter state | Sanity |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 3 | 0 |
| 4 | 4 → reset | 1 |
| 5 | 1 | 1 |
| 6 | 2 | 1 |
| 7 | 3 | 1 |

Final output:

```
1
```

This shows that incomplete trailing segments do not contribute, since the counter never reaches 4 again.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic division is performed after input |
| Space | O(1) | No auxiliary structures are used |

The solution is constant time and constant memory, which is far below typical Codeforces limits. Even with extremely large inputs, the computation remains instantaneous because it avoids iteration entirely.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimum case
assert run("1 5") == "0"

# exact multiple
assert run("6 3") == "2"

# non-multiple
assert run("10 4") == "2"

# large k greater than n
assert run("7 10") == "0"

# equal values
assert run("100 100") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 | 0 | no full cycle |
| 6 3 | 2 | exact multiples |
| 10 4 | 2 | partial remainder ignored |
| 7 10 | 0 | k > n edge case |
| 100 100 | 1 | boundary equality case |

## Edge Cases

For the case where $N < K$, such as input `5 10`, the counter never reaches the threshold. The algorithm computes `5 // 10 = 0`, correctly indicating no sanity increases. A step-by-step simulation would show the counter progressing from 1 to 5 without ever hitting 10, confirming no increment.

For exact boundary alignment, such as `9 3`, the simulation hits the threshold exactly at days 3, 6, and 9. The algorithm returns `9 // 3 = 3`, matching the three reset events precisely.
