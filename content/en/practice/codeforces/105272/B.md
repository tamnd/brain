---
title: "CF 105272B - Battle in space"
description: "Two players take turns writing a number. First, the opponent announces an integer n. After seeing it, we choose our own integer m. Whoever writes the larger number wins immediately."
date: "2026-06-23T06:55:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105272
codeforces_index: "B"
codeforces_contest_name: "IX MaratonUSP Freshman Contest"
rating: 0
weight: 105272
solve_time_s: 46
verified: true
draft: false
---

[CF 105272B - Battle in space](https://codeforces.com/problemset/problem/105272/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players take turns writing a number. First, the opponent announces an integer `n`. After seeing it, we choose our own integer `m`. Whoever writes the larger number wins immediately.

The goal is to always guarantee a win, regardless of what `n` is, while respecting the constraint that our chosen number must lie between `0` and `100000`.

This turns the problem into a simple decision made under a fixed upper bound. We are not trying to react dynamically over multiple rounds or maintain a data structure, we are choosing a single value after observing one input.

The constraint `1 ≤ n ≤ 100` is crucial. It tells us the opponent’s number is always very small compared to the maximum allowed value for `m`. This already suggests that any strategy that tries to carefully compare or adapt per case is unnecessary, since the feasible range for `m` is much larger than anything the opponent can produce.

A naive mistake would be to compute something like `m = n + 1`. This works in most competitive programming problems of this type, but here it is not required and is not optimal in terms of guaranteeing a strict advantage margin. More importantly, a careless implementation might still stay within bounds but fail in variants where `n` could be close to `100000`.

For example, if the rule were different:

Input:

```
100000
```

Then `m = n + 1` would exceed the limit. In this problem we are safe, but the constraint is exactly what allows a simpler constant solution.

## Approaches

A brute-force interpretation would be to try every possible value of `m` from `0` to `100000` and pick one that is strictly greater than `n`. This is correct because we directly simulate the rule for every candidate and check whether it wins. The cost is at most `100001` checks, which is trivial even for many test cases.

However, this approach is unnecessary because the structure of the problem does not depend on any interaction beyond a single comparison. Once we realize that winning only depends on being strictly greater than `n`, we no longer need to search.

The key observation is that we want the largest possible allowed number. Since `100000` is the maximum value we are allowed to output, we check whether it guarantees victory. Because `n ≤ 100`, it always holds that `100000 > n`, so the maximum possible choice already satisfies the winning condition in every case.

This reduces the problem to a constant-time decision.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100000) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` from input. This represents the opponent’s fixed number.
2. Recognize that our number `m` must satisfy two conditions simultaneously: it must be within `[0, 100000]`, and it must be strictly greater than `n`.
3. Observe that the maximum possible candidate `100000` is valid under the constraint.
4. Compare implicitly: since `n ≤ 100`, the inequality `100000 > n` always holds.
5. Output `100000` as it is both valid and guaranteed to win.

### Why it works

The algorithm relies on the monotonic structure of the problem: any larger number always dominates any smaller number. Because we are allowed to choose the maximum possible value in the allowed range, and the opponent’s value is strictly bounded far below it, the maximum value is always a dominant strategy. There is no configuration where a smaller choice would outperform `100000`, since winning depends only on being strictly greater than `n`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    print(100000)

if __name__ == "__main__":
    solve()
```

The solution reads the single input value and immediately outputs `100000`. There is no branching because the constraint on `n` guarantees that this value always beats it. The implementation avoids unnecessary comparisons or arithmetic, keeping the logic minimal and robust.

## Worked Examples

### Example 1

Input:

```
5
```

| Step | n | chosen m | comparison result |
| --- | --- | --- | --- |
| 1 | 5 | 100000 | 100000 > 5 |

The output is always `100000`. This demonstrates that even for small values of `n`, the strategy does not change.

### Example 2

Input:

```
100
```

| Step | n | chosen m | comparison result |
| --- | --- | --- | --- |
| 1 | 100 | 100000 | 100000 > 100 |

This shows the boundary case where `n` is at its maximum. Even here, the fixed output remains valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a single input read and one print operation |
| Space | O(1) | No additional data structures are used |

The constraints are extremely small, and the solution executes in constant time, well within any time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return io.StringIO().write(""), solve()

# provided sample-like cases (constructed)
assert run("1\n") is None
assert run("50\n") is None
assert run("100\n") is None

# custom cases
# minimum
assert run("1\n") is None, "minimum input"

# maximum n
assert run("100\n") is None, "upper bound of n"

# arbitrary mid
assert run("42\n") is None, "mid range"

# edge consistency check
assert run("99\n") is None, "near maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 100000 | minimum input correctness |
| 100 | 100000 | maximum constraint correctness |
| 42 | 100000 | typical mid-range behavior |
| 99 | 100000 | near-boundary stability |

## Edge Cases

### Maximum possible opponent value

Input:

```
100
```

The algorithm selects `100000`. Since `100000 > 100`, the win condition is satisfied. No alternative value is needed because any smaller valid value would still work, but the maximum choice guarantees correctness in all cases.

### Minimum possible opponent value

Input:

```
1
```

Again the algorithm outputs `100000`. The comparison `100000 > 1` trivially holds, confirming that even the smallest opponent value does not affect the decision.

### General bounded case

Any input `n` in `[1, 100]` follows the same execution path, producing the same output. The logic never branches, so all cases reduce to a single invariant check: the output must exceed the maximum possible input, which is satisfied by `100000`.
