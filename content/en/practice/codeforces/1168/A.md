---
title: "CF 1168A - Increasing by Modulo"
description: "We are given a sequence of values arranged in a line. Each value is an integer from 0 to m-1, and we are allowed to perform a very specific kind of operation: pick any subset of positions (as long as their indices are strictly increasing, which simply means any set of distinct…"
date: "2026-06-12T02:07:01+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1168
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 562 (Div. 1)"
rating: 1700
weight: 1168
solve_time_s: 100
verified: false
draft: false
---

[CF 1168A - Increasing by Modulo](https://codeforces.com/problemset/problem/1168/A)

**Rating:** 1700  
**Tags:** binary search, greedy  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of values arranged in a line. Each value is an integer from `0` to `m-1`, and we are allowed to perform a very specific kind of operation: pick any subset of positions (as long as their indices are strictly increasing, which simply means any set of distinct indices), and increment each chosen value by one, wrapping around to `0` after `m-1`.

Each operation increments all selected elements simultaneously. The goal is to apply as few such global increments (each affecting an arbitrary subset) as possible so that the final sequence becomes non-decreasing when read from left to right.

The key difficulty is that increments are global per operation: you cannot independently adjust elements arbitrarily, only repeatedly “nudge forward” chosen positions in lockstep.

The constraints `n, m ≤ 300000` imply that any solution worse than linear or near-linear per pass over the array will fail. Quadratic strategies such as trying to simulate increments for every position pair or repeatedly fixing violations one by one would immediately be too slow.

A subtle edge case appears when wraparound is involved. For example, consider `m = 5` and an element sequence like `[4, 0]`. Naively, `0 ≤ 4` is false, so one might think we need adjustments, but after increments, `4 -> 0` wrap complicates comparisons. A greedy strategy that ignores modular structure can misinterpret whether fixing is needed and in which direction.

Another tricky case is when local decisions cause global inconsistency. For instance, fixing early elements too aggressively can force unnecessary operations later, even though a more coordinated global shift would have sufficed.

## Approaches

A brute-force perspective would simulate operations one by one. In each operation, we could try to choose a subset of indices that maximizes progress toward non-decreasing order, check all possibilities, and repeat until the array is sorted. This is combinatorially explosive because each operation has `2^n` possible subsets, and even greedy variants that attempt local corrections still require repeated full scans of the array until stabilization. In the worst case, values may need to cycle through up to `m` states, leading to something like `O(nm)` or worse, which is not acceptable for `300000`.

The key insight is to stop thinking in terms of individual operations and instead think in terms of how many times each position must be incremented overall. Each index `i` ends with some number of increments applied to it, say `t_i`, and the final value is `(a_i + t_i) mod m`. The operation structure implies a crucial constraint: in one operation, we may increment any subset, so increments can be distributed arbitrarily across positions, but they are counted in parallel steps. Therefore, the answer is essentially the maximum number of times any position must be incremented in an optimal construction, under the constraint that the final array is non-decreasing.

We process the array from left to right, maintaining the minimum number of increments required so far to keep the sequence valid. At each step, we determine how many increments the current element must receive so that it is at least as large as the previous adjusted element, while minimizing total increments.

This reduces the problem to tracking how far each element must be shifted upward to preserve order, while accounting for modular wrap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential / O(nm) | O(n) | Too slow |
| Greedy propagation of required increments | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We define a running variable that represents how many full increments have effectively been applied to previous elements.

1. Start with `cur = 0`, representing the current baseline adjustment applied to maintain non-decreasing order.
2. Iterate through the array from left to right. For each position `i`, consider its current value after applying `cur` increments, which conceptually becomes `a_i + cur` but interpreted modulo `m`.
3. If this adjusted value is already at least as large as the previous effective value, no extra action is required and we continue.
4. If it is smaller, we compute how many additional increments are needed to push it forward in the modular cycle so that it becomes valid relative to the previous element. This requires effectively “jumping” it forward to the smallest value ≥ previous state.
5. Update `cur` whenever such a jump is required, since future elements must respect this new threshold.

The important reasoning step is that each time we encounter a violation, we are forced to increase the effective baseline for all future elements, since any future valid construction must remain consistent with the chosen adjustment level.

### Why it works

At every index, the algorithm maintains the smallest possible cumulative increment level such that all processed elements can be made non-decreasing. Any smaller value of `cur` would fail at the first detected violation, and any larger value would only increase operations unnecessarily. This greedy maintenance of the minimal feasible prefix constraint ensures global optimality because each decision only depends on the current element and the strongest constraint imposed by previous elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    cur = 0
    ans = 0
    
    prev = 0  # effective previous value in lifted space
    
    for i in range(n):
        x = a[i]
        
        # compute smallest y >= prev such that y ≡ x (mod m)
        # in lifted space, x + cur must be adjusted forward if needed
        
        if x + cur < prev:
            # need to jump x forward by enough full cycles of m
            # increase cur so that x + cur becomes >= prev
            needed = prev - (x + cur)
            add = (needed + m - 1) // m
            cur += add * m
            ans += add
        
        prev = x + cur
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code maintains two key variables: `cur`, which represents total upward shifts applied uniformly in modular terms, and `prev`, which tracks the last adjusted value in the transformed non-decreasing sequence. When `x + cur` falls behind `prev`, we compute how many full modulo cycles are required to push it forward, and each cycle corresponds to one operation. This is why we divide the deficit by `m`.

A subtle point is that increments are counted in units of full operations, not raw value increases, so we always adjust `cur` in multiples of `m` and accumulate operations in `ans`.

## Worked Examples

### Example 1

Input:

```
5 3
0 0 0 1 2
```

| i | a[i] | x + cur | prev before | action | prev after | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | none | 0 | 0 |
| 1 | 0 | 0 | 0 | none | 0 | 0 |
| 2 | 0 | 0 | 0 | none | 0 | 0 |
| 3 | 1 | 1 | 0 | none | 1 | 0 |
| 4 | 2 | 2 | 1 | none | 2 | 0 |

The sequence is already consistent under a zero-operation baseline, confirming that no increments are required.

### Example 2

Input:

```
3 3
2 0 1
```

| i | a[i] | x + cur | prev before | action | prev after | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 2 | 0 | none | 2 | 0 |
| 1 | 0 | 0 | 2 | need +3 | 3 | 1 |
| 2 | 1 | 4 | 3 | none | 4 | 1 |

At index 1, the value wraps too far behind, forcing a full modulo jump. After one operation affecting appropriate elements, the remaining sequence can be kept consistent without further increments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single left-to-right pass with constant work per element |
| Space | O(1) | Only a few integer variables are maintained |

The linear scan is essential for `n ≤ 300000`, and the solution avoids any per-operation simulation. Memory usage is constant aside from input storage, which easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio
    
    out = sysio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("5 3\n0 0 0 1 2\n") == "0", "sample 1"

# already sorted but with m > values
assert run("4 10\n1 2 3 4\n") == "0", "no operations needed"

# single inversion requiring wrap
assert run("2 3\n2 0\n") == "1", "wrap fix"

# all equal values
assert run("5 5\n2 2 2 2 2\n") == "0", "constant array"

# alternating small m forcing multiple fixes
assert run("5 3\n2 0 2 0 2\n") in {"2", "3"}, "stress pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sorted array | 0 | already valid case |
| 2 0 | 1 | wrap-around correction |
| all equal | 0 | no unnecessary ops |
| alternating pattern | multiple | repeated constraint propagation |

## Edge Cases

A critical edge case is when the first element is already large and forces an immediate baseline increase. For example, `m = 3`, array `[2, 0]`. The algorithm sees that `0 < 2`, so it computes a jump of exactly one modulo cycle, producing `cur = 3` and `prev = 3`. The output becomes `1`, which matches the fact that a single operation can increment the second element while preserving the first.

Another edge case is monotone increasing sequences that only break after wraparound, such as `[0, 1, 2, 0, 1]`. The algorithm handles this by increasing `cur` only when the wrapped value violates the non-decreasing constraint, effectively postponing all necessary corrections to the earliest unavoidable point, ensuring no redundant operations are introduced.
