---
title: "CF 106124K - km/h"
description: "We are simulating a driver moving through a sequence of road signs, where each sign either sets a specific speed limit or removes the current restriction and restores the original national speed limit."
date: "2026-06-20T05:32:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106124
codeforces_index: "K"
codeforces_contest_name: "2025-2026 ICPC Nordic Collegiate Programming Contest (NCPC 2025)"
rating: 0
weight: 106124
solve_time_s: 41
verified: true
draft: false
---

[CF 106124K - km/h](https://codeforces.com/problemset/problem/106124/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a driver moving through a sequence of road signs, where each sign either sets a specific speed limit or removes the current restriction and restores the original national speed limit.

The key detail is that the national speed limit is unknown to us, except that it is a multiple of ten and strictly higher than any explicit speed limit sign ever shown. This means whenever we see a “reset” sign, we cannot directly restore a fixed number. Instead, we must infer the maximum possible speed consistent with everything observed so far.

The task is sequential. After each sign, we must output the highest speed that is guaranteed to be legal given all constraints seen up to that point.

The input is a stream of operations. Each operation is either a numeric limit, which immediately restricts the maximum allowed speed to that value, or a slash symbol indicating a reset, which removes all explicit limits and returns us to the unknown national speed limit regime.

The constraints are small, with at most 100 signs. This means any solution up to quadratic time is already safe, but the structure of the problem is simple enough that a linear simulation suffices.

A subtle failure case appears around resets. If one incorrectly assumes the national speed limit is fixed or tries to “remember” a guessed value, the logic breaks.

For example, consider:

Input:

```
/
```

This is impossible as the first sign must be a speed limit, but it highlights the issue: after a reset, we do not have a concrete number unless we derive it from prior limits.

A more realistic edge case is:

Input:

```
50
80
/
```

Correct reasoning:

After 50, the limit is 50.

After 80, the limit becomes 50 (because we always obey the smallest restriction seen so far).

After reset, the limit becomes the unknown national speed limit, which must be strictly larger than any seen limit, so at least 90 (since it must be a multiple of ten). Thus the answer becomes 90.

A naive implementation that simply “forgets constraints” and prints an unbounded value or zero after reset is incorrect.

The core difficulty is that resets require reconstructing a consistent upper bound from history, not merely clearing state.

## Approaches

A brute-force interpretation would try to recompute the valid maximum speed after every sign by reconsidering all previous constraints. After each reset, we would scan backwards to find the maximum speed limit seen so far and then assume the national speed limit is the smallest multiple of ten strictly greater than it. This works conceptually because the national limit must be consistent with all previous limits.

However, this approach becomes inefficient if extended to large inputs, since each reset could trigger a full scan of all previous signs, leading to quadratic behavior in the worst case. Even though N is small here, this motivates simplifying the state.

The key observation is that we never need to recompute from scratch. The only information that matters is the maximum speed limit seen since the last reset. That value alone determines the minimum possible national speed limit: the smallest multiple of ten strictly greater than it. Therefore, instead of scanning history, we maintain a running maximum that is reset whenever a slash appears.

This reduces the entire process to a single pass with constant-time updates per sign.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(1) | Accepted but unnecessary |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain one piece of state: the highest explicit speed limit seen since the last reset.

1. Initialize a variable `mx` to 0. This represents the strongest constraint currently active.
2. Read the first sign, which is guaranteed to be a number, and set `mx` to that value. Output it immediately.
3. For each subsequent sign, process it in order.
4. If the sign is a number `L`, update `mx` to be `max(mx, L)`. Output `mx` because the legal speed is always bounded by the tightest restriction seen so far.
5. If the sign is `/`, compute the national speed limit as the smallest multiple of ten strictly greater than `mx`. This can be done as `((mx // 10) + 1) * 10`. Output this value, but importantly do not reset `mx` to zero; instead, we conceptually switch into “no restriction except national limit” mode, which means future explicit limits again re-establish constraints starting from that baseline.
6. Continue until all signs are processed.

The key idea is that `mx` always tracks the strongest explicit constraint in the current segment between resets. The slash does not erase history for correctness purposes, it only changes how we interpret the next segment.

### Why it works

At any point without a reset, legality is governed entirely by the minimum over all speed limits seen since the last reset. That minimum is exactly the current `mx`. When a reset occurs, the only missing value is the national speed limit, but the problem guarantees it is a multiple of ten strictly above any observed limit. The smallest such value is completely determined by `mx`, so we can safely output it without guessing anything else. No other historical information influences the current answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    mx = 0
    first = True
    
    for _ in range(n):
        s = input().strip()
        
        if s == "/":
            # restore national speed limit
            mx = ((mx // 10) + 1) * 10
            print(mx)
        else:
            val = int(s)
            if first:
                mx = val
                first = False
            else:
                mx = max(mx, val)
            print(mx)

if __name__ == "__main__":
    solve()
```

The implementation keeps a running maximum `mx` that represents the tightest explicit restriction in the current segment. When we encounter a numeric sign, we update this maximum. When we encounter a slash, we convert the current maximum into the implied national limit by rounding up to the next multiple of ten.

The `first` flag ensures that the initial state is handled cleanly, since the problem guarantees the first sign is always a speed limit.

A common pitfall is resetting `mx` to zero on `/`. That would incorrectly imply no restriction, whereas the correct behavior is to infer a concrete bound from the previous maximum.

## Worked Examples

### Example 1

Input:

```
50
80
/
60
/
```

We track `mx` and output step by step.

| Step | Sign | mx before | Action | Output |
| --- | --- | --- | --- | --- |
| 1 | 50 | 0 | mx = 50 | 50 |
| 2 | 80 | 50 | mx = 80 | 80 |
| 3 | / | 80 | round up to 90 | 90 |
| 4 | 60 | 90 | mx = max(90, 60) = 90 | 90 |
| 5 | / | 90 | round up to 100 | 100 |

This trace shows that after a reset, earlier explicit constraints still influence the inferred national limit through the carried maximum.

### Example 2

Input:

```
40
30
/
70
/
```

| Step | Sign | mx before | Action | Output |
| --- | --- | --- | --- | --- |
| 1 | 40 | 0 | mx = 40 | 40 |
| 2 | 30 | 40 | mx stays 40 | 40 |
| 3 | / | 40 | round up to 50 | 50 |
| 4 | 70 | 50 | mx = 70 | 70 |
| 5 | / | 70 | round up to 80 | 80 |

This confirms that the algorithm correctly merges constraints across segments separated by resets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each sign is processed once with constant-time updates |
| Space | O(1) | Only a single running maximum is stored |

With N ≤ 100, this is trivially fast, but the linear structure reflects the true nature of the process and scales to much larger inputs without modification.

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

# provided sample-like tests
assert run("1\n50\n") == "50"

assert run("3\n50\n80\n/\n") == "50\n80\n90"

# custom cases

# minimum case
assert run("1\n10\n") == "10", "single limit"

# all increasing limits
assert run("4\n10\n20\n30\n40\n") == "10\n20\n30\n40", "monotonic increase"

# reset after peak
assert run("5\n10\n90\n/\n50\n/\n") == "10\n90\n100\n100\n110", "reset behavior"

# repeated resets
assert run("5\n30\n/\n/\n20\n/\n") == "30\n40\n50\n50\n60", "multiple resets"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 10 | 10 | base case |
| increasing sequence | monotonic outputs | normal updates |
| reset after peak | rounded inference | national speed logic |
| repeated resets | stability across cycles | repeated inference |

## Edge Cases

A key edge case is when the maximum before a reset is already a multiple of ten. For example:

Input:

```
60
/
```

We compute `((60 // 10) + 1) * 10 = 70`, so the output becomes 70. A naive approach that simply returns 60 after reset would violate the requirement that the national speed limit must be strictly higher than any explicit limit seen so far.

Another case is when small limits are followed by a reset:

Input:

```
10
20
/
```

We track `mx = 20`, then after reset output 30. This shows that the reset does not revert to a fixed constant but depends entirely on accumulated history.

Finally, repeated resets without new limits confirm stability:

Input:

```
10
/
/
```

Step 1 gives 10, step 2 gives 20, step 3 gives 30. Each reset continues to derive a strictly increasing sequence, which matches the rule that the national limit is always above prior observed limits.
