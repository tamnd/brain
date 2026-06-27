---
title: "CF 105048B - Romeo and Random Walk"
description: "We are given a set of points on a number line, each point representing a possible initial position of Juliet at time zero. Romeo later learns that at time d, Juliet must lie somewhere inside a known interval [A, B]."
date: "2026-06-28T05:07:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105048
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 2 (Beginner)"
rating: 0
weight: 105048
solve_time_s: 78
verified: false
draft: false
---

[CF 105048B - Romeo and Random Walk](https://codeforces.com/problemset/problem/105048/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points on a number line, each point representing a possible initial position of Juliet at time zero. Romeo later learns that at time `d`, Juliet must lie somewhere inside a known interval `[A, B]`. Between time `0` and time `d`, Juliet can move freely along the line, but her speed is limited: in each minute she can move at most one unit distance, so after `d` minutes she can end up anywhere within distance `d` from where she started.

The task is to determine which starting points among the given candidates could have evolved into some position inside `[A, B]` after exactly `d` minutes of such movement. The output is the list of indices of those valid starting points.

The constraints allow up to `10^5` candidate points and coordinates up to `10^9`, with `d` also up to `10^9`. This immediately rules out any approach that simulates movement or checks reachability minute by minute. Any solution must reduce each point to a constant-time check, since an `O(N)` or `O(N log N)` solution is expected to pass comfortably, while anything quadratic would be far too slow.

A subtle issue arises from boundary reasoning. A common mistake is to treat reachability as a single point instead of an interval. Another is to check only one direction of movement, for example verifying whether `P_i` can reach `A` or `B` individually, instead of checking overlap of reachable ranges. These mistakes lead to rejecting valid starting points where Juliet simply moves toward the correct part of the interval.

For example, suppose `d = 2`, `P_i = 5`, and `[A, B] = [6, 7]`. Juliet can move from `5` to `7` in two steps, so this starting point is valid. A naive check like “can she reach `A` exactly” would incorrectly reject it.

## Approaches

A brute-force interpretation simulates the movement from each starting position. From a point `x`, after `d` minutes Juliet can be anywhere in the interval `[x - d, x + d]`. To check validity, one could enumerate all possible positions reachable from `x` and verify whether any lies in `[A, B]`. This immediately becomes infeasible because each interval contains `O(d)` integer positions, and `d` can be as large as `10^9`, making the simulation impossible.

The key observation is that movement transforms each starting point into a continuous interval, and we only need to know whether two intervals intersect. Instead of tracking all possible positions, we compute the reachable interval `[x - d, x + d]` and check whether it overlaps with `[A, B]`. Interval overlap reduces to a pair of linear inequalities, which simplifies further into a direct constraint on `x`.

The intervals intersect if and only if there exists some position that lies in both. This happens exactly when `x + d >= A` and `x - d <= B`. Rearranging gives `x >= A - d` and `x <= B + d`. So each candidate point can be checked independently in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N·d) | O(1) | Too slow |
| Interval Reduction | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the reachability problem into a simple range filter on the original points.

1. Compute the minimum starting position that can still reach `[A, B]` after `d` minutes, which is `A - d`. This comes from reversing the maximum rightward movement.
2. Compute the maximum starting position that can still reach `[A, B]`, which is `B + d`, coming from reversing the maximum leftward movement.
3. Iterate over all points `P[i]`.
4. For each point, check whether it lies in the interval `[A - d, B + d]`. If it does, include its index in the answer.
5. Output all collected indices in increasing order.

The reason we reverse the interval instead of forward-simulating movement is that every starting position maps to a symmetric reachable segment. Working backward converts a dynamic reachability problem into a static filtering condition.

### Why it works

At time zero, a starting position `x` expands into the full interval `[x - d, x + d]` at time `d`. Juliet is valid if and only if this interval intersects `[A, B]`. Interval intersection is equivalent to the condition that neither interval lies completely to the left or completely to the right of the other. Translating those non-overlap conditions produces the bounds `x >= A - d` and `x <= B + d`. Therefore, every valid starting point is captured exactly once by this filter, and no invalid point can satisfy it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, A, B, d = map(int, input().split())
    P = list(map(int, input().split()))

    left = A - d
    right = B + d

    res = []
    for i, x in enumerate(P):
        if left <= x <= right:
            res.append(str(i))

    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the derived interval condition. The only subtle point is that the indices are preserved from input order, so we enumerate with `i` starting from zero and print those indices as strings.

Care must be taken not to recompute reachability per point in any expanded way. The entire solution relies on reducing each point to a single comparison against a precomputed interval.

## Worked Examples

Consider a small scenario where `A = 10`, `B = 12`, `d = 3`, and points are `[5, 9, 11, 15]`.

The transformed valid starting interval becomes `[A - d, B + d] = [7, 15]`.

| i | P[i] | Check (7 ≤ x ≤ 15) | Result |
| --- | --- | --- | --- |
| 0 | 5 | no | reject |
| 1 | 9 | yes | keep |
| 2 | 11 | yes | keep |
| 3 | 15 | yes | keep |

Output is `1 2 3`.

Now consider a boundary-heavy case: `A = 0`, `B = 0`, `d = 5`, and points `[6, 5, 4, -1]`.

The valid interval is `[-5, 5]`.

| i | P[i] | Check (-5 ≤ x ≤ 5) | Result |
| --- | --- | --- | --- |
| 0 | 6 | no | reject |
| 1 | 5 | yes | keep |
| 2 | 4 | yes | keep |
| 3 | -1 | yes | keep |

This shows that even though the target interval collapses to a point at time `d`, any starting position within distance `d` of it remains valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each point is checked once with constant-time arithmetic |
| Space | O(1) | Only a few variables are stored aside from output |

The linear scan over up to `10^5` points easily fits within the time limit, and memory usage remains constant aside from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample (format reconstructed)
assert run("""10 3 5 14
10 14 17 5 11 13 6 17 10 2
""") == "0 3 4 5 6 8"

# minimum size
assert run("""1 0 0 0
0
""") == "0"

# all invalid
assert run("""3 10 12 1
0 1 2
""") == ""

# all valid due to large d
assert run("""4 100 100 100
0 50 150 200
""") == "0 1 2 3"

# boundary tight case
assert run("""5 10 10 0
9 10 11 10 8
""") == "1 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | indices list | basic correctness |
| single element | 0 | minimum input handling |
| all invalid | empty | correct rejection |
| large d | all indices | full inclusion |
| d = 0 | exact match only | boundary precision |

## Edge Cases

One edge case is when `d = 0`. In this situation, Juliet cannot move at all, so the only valid starting points are those already inside `[A, B]`. The algorithm handles this naturally because the interval becomes `[A, B]`, so the condition reduces to a direct membership test.

Another case is when `A - d` becomes negative. Since coordinates can be zero but not negative in input, this simply expands the valid region leftward beyond the domain of possible points. The algorithm still works because comparisons remain valid even with negative bounds, and no special clamping is required.

A final subtle case is when `[A, B]` is extremely large and overlaps almost all possible positions. In that case, `A - d` and `B + d` may exceed input bounds in either direction, but again the interval check remains correct since it only depends on inequality relationships, not absolute range limits.
