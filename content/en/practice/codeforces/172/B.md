---
title: "CF 172B - Pseudorandom Sequence Period"
description: "We are given a linear congruential generator, a classic pseudorandom sequence formula: $$ri = (a cdot r{i-1} + b) bmod m$$ The sequence starts from r0, and every next value is computed from the previous one."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 172
codeforces_index: "B"
codeforces_contest_name: "Croc Champ 2012 - Qualification Round"
rating: 1200
weight: 172
solve_time_s: 213
verified: true
draft: false
---

[CF 172B - Pseudorandom Sequence Period](https://codeforces.com/problemset/problem/172/B)

**Rating:** 1200  
**Tags:** *special, implementation, number theory  
**Solve time:** 3m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a linear congruential generator, a classic pseudorandom sequence formula:

$$r_i = (a \cdot r_{i-1} + b) \bmod m$$

The sequence starts from `r0`, and every next value is computed from the previous one. Since every value is taken modulo `m`, there are only `m` possible states: `0` through `m - 1`.

The task is not to find when the sequence first repeats. We specifically need the length of the repeating cycle that eventually appears. A sequence may have some non-repeating prefix before entering the cycle.

For example, with:

```
a = 2
b = 6
m = 12
r0 = 11
```

the sequence becomes:

```
11 -> 4 -> 2 -> 10 -> 2 -> 10 -> ...
```

The value `11` appears only once. After that, the sequence alternates forever between `2` and `10`, so the period is `2`.

The constraint `m ≤ 100000` is the key observation. Since every generated value is between `0` and `m - 1`, the sequence can visit at most `m` distinct states before some value repeats. That immediately rules out any infinite exploration concerns. Even an `O(m)` or `O(m log m)` solution easily fits within the limits.

A naive approach that compares every pair of positions would become quadratic. With `m = 100000`, an `O(m²)` algorithm could require around `10^10` operations, which is far beyond the time limit.

The tricky part is distinguishing the preperiod from the actual cycle.

Consider this input:

```
0 0 10 7
```

The sequence is:

```
7 -> 0 -> 0 -> 0 -> ...
```

The correct answer is `1`, not `2`. A careless implementation that measures distance between the first and second occurrence of any value could incorrectly count part of the preperiod.

Another subtle case is when the cycle starts immediately:

```
1 1 5 0
```

The sequence becomes:

```
0 -> 1 -> 2 -> 3 -> 4 -> 0 -> ...
```

The whole sequence is cyclic from the beginning, so the answer is `5`.

A third edge case happens when the sequence reaches a fixed point:

```
5 3 100 15
```

Suppose the sequence eventually becomes:

```
78 -> 78 -> 78 -> ...
```

The period is still `1`, because a single value repeats forever.

## Approaches

The brute-force idea is straightforward. Generate the sequence step by step and store every produced value. Whenever a value appears again, try to determine the cycle length by comparing future elements.

This works because the sequence is deterministic. Once we revisit a previous state, everything after that point repeats identically. The problem is efficiency. If we repeatedly compare large suffixes to verify candidate periods, the worst-case complexity becomes quadratic.

The important observation is that the generator behaves like a directed graph where every node has exactly one outgoing edge. From any state, there is exactly one next state. Such graphs always consist of a path leading into a cycle.

Since there are only `m` possible states, the first repeated value immediately identifies the start of the cycle.

Suppose value `x` first appears at position `p`, and later appears again at position `q`.

Because the transition function is deterministic:

```
next(x) is always the same
```

the entire suffix after position `p` must match the suffix after position `q`. That means the cycle length is simply:

```
q - p
```

So instead of storing the entire sequence and performing comparisons, we only need to remember the first position where each value appeared.

The algorithm becomes:

1. Generate values one by one.
2. Store the first index where each value appears.
3. When a value repeats, return the difference between current index and first occurrence index.

Since each state is processed at most once before repetition, the algorithm runs in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(m) | Too slow |
| Optimal | O(m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read `a`, `b`, `m`, and `r0`.
2. Create a dictionary or array `first_seen` that stores the first index where each value appears.
3. Mark the starting value `r0` as seen at position `0`.
4. Repeatedly generate the next value using:

$$r = (a \cdot r + b) \bmod m$$
5. Increase the current position counter after generating each new value.
6. Check whether the new value has appeared before.
7. If the value is new, store its first occurrence position and continue.
8. If the value already appeared at position `p`, the sequence has entered a cycle. The cycle length is:

$$\text{current position} - p$$
9. Print that length and stop.

### Why it works

The sequence is completely determined by its current value. If some value `x` appears at two different positions, the future evolution from both positions must be identical.

Suppose:

```
r_p = r_q
```

with `p < q`.

Then:

```
r_{p+1} = r_{q+1}
r_{p+2} = r_{q+2}
...
```

because both positions apply the same transition formula to the same value.

That means the sequence repeats every `q - p` steps starting from position `p`. Since we stop at the first repeated value, this difference is the minimum valid period.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, m, r = map(int, input().split())

first_seen = [-1] * m
first_seen[r] = 0

pos = 0

while True:
    r = (a * r + b) % m
    pos += 1

    if first_seen[r] != -1:
        print(pos - first_seen[r])
        break

    first_seen[r] = pos
```

The array `first_seen` stores the first position where each remainder appears. Since every value is in the range `[0, m - 1]`, using an array is faster and simpler than using a dictionary.

The variable `pos` represents the index of the current value in the sequence. We start with `r0` at position `0`.

Inside the loop, we first generate the next value, then increment the position. The order matters. If we incremented before generating the next state, the stored indices would shift incorrectly and produce off-by-one errors in the cycle length.

The moment we encounter a previously seen value, we subtract its first occurrence position from the current position. That difference is exactly the cycle length.

The loop is guaranteed to terminate because there are only `m` distinct states.

## Worked Examples

### Example 1

Input:

```
2 6 12 11
```

Generated sequence:

```
11 -> 4 -> 2 -> 10 -> 2 -> ...
```

| Position | Current Value | First Seen Before? | Action |
| --- | --- | --- | --- |
| 0 | 11 | No | store 11 at 0 |
| 1 | 4 | No | store 4 at 1 |
| 2 | 2 | No | store 2 at 2 |
| 3 | 10 | No | store 10 at 3 |
| 4 | 2 | Yes, at 2 | answer = 4 - 2 = 2 |

The repeated value is `2`. Its first occurrence was at position `2`, and it appears again at position `4`, so the period is `2`.

### Example 2

Input:

```
1 3 5 2
```

Generated sequence:

```
2 -> 0 -> 3 -> 1 -> 4 -> 2 -> ...
```

| Position | Current Value | First Seen Before? | Action |
| --- | --- | --- | --- |
| 0 | 2 | No | store 2 at 0 |
| 1 | 0 | No | store 0 at 1 |
| 2 | 3 | No | store 3 at 2 |
| 3 | 1 | No | store 1 at 3 |
| 4 | 4 | No | store 4 at 4 |
| 5 | 2 | Yes, at 0 | answer = 5 - 0 = 5 |

This trace shows a cycle that starts immediately. Every value in modulo `5` appears exactly once before repetition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | each state is processed at most once |
| Space | O(m) | stores first occurrence for each possible remainder |

With `m ≤ 100000`, the algorithm performs at most one iteration per possible state. Both the runtime and memory usage comfortably fit within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a, b, m, r = map(int, input().split())

    first_seen = [-1] * m
    first_seen[r] = 0

    pos = 0

    while True:
        r = (a * r + b) % m
        pos += 1

        if first_seen[r] != -1:
            print(pos - first_seen[r])
            return

        first_seen[r] = pos

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run("2 6 12 11\n") == "2", "sample 1"

# minimum-size input
assert run("0 0 1 0\n") == "1", "single state"

# cycle starts immediately
assert run("1 1 5 0\n") == "5", "full modulo cycle"

# fixed point after one step
assert run("0 0 10 7\n") == "1", "constant sequence"

# off-by-one detection
assert run("2 0 7 1\n") == "3", "cycle length should be 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 1 0` | `1` | smallest possible state space |
| `1 1 5 0` | `5` | cycle begins immediately |
| `0 0 10 7` | `1` | fixed-point cycle after preperiod |
| `2 0 7 1` | `3` | catches index-shift mistakes |

## Edge Cases

Consider the input:

```
0 0 10 7
```

The generated sequence is:

```
7 -> 0 -> 0 -> 0 -> ...
```

Trace:

| Position | Value |
| --- | --- |
| 0 | 7 |
| 1 | 0 |
| 2 | 0 |

The value `0` first appears at position `1` and repeats at position `2`. The algorithm returns `2 - 1 = 1`, which is correct. The initial value `7` belongs to the preperiod and is not part of the cycle.

Now consider:

```
1 1 5 0
```

The sequence becomes:

```
0 -> 1 -> 2 -> 3 -> 4 -> 0
```

Trace:

| Position | Value |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 0 |

The repeated value `0` was first seen at position `0`, so the algorithm returns `5`. This confirms that cycles beginning immediately are handled correctly.

Finally, consider:

```
5 3 100 15
```

Suppose the sequence reaches:

```
78 -> 78 -> 78 -> ...
```

The first repetition occurs one step later, so the algorithm computes:

```
current_position - first_seen[78] = 1
```

A self-loop is still a valid cycle, and the algorithm naturally handles it without special cases.
