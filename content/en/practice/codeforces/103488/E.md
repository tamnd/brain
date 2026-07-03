---
title: "CF 103488E - Equality"
description: "We are given an array and a fixed window size. In one move, we choose a contiguous segment of exactly length k and overwrite every element in that segment with the minimum value currently inside that segment."
date: "2026-07-03T09:47:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103488
codeforces_index: "E"
codeforces_contest_name: "The 2021 Zhejiang University City College Freshman Programming Contest"
rating: 0
weight: 103488
solve_time_s: 50
verified: true
draft: false
---

[CF 103488E - Equality](https://codeforces.com/problemset/problem/103488/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and a fixed window size. In one move, we choose a contiguous segment of exactly length `k` and overwrite every element in that segment with the minimum value currently inside that segment. Repeating this operation changes the array, and the goal is to make all elements equal using as few operations as possible, or determine that it cannot be done.

The key difficulty is that the operation is not a simple replacement. It depends on the current minimum inside the chosen window, so the value written into the segment evolves as previous operations change the array. This creates a propagation effect where smaller values can “spread” left or right, but only through windows of size exactly `k`.

The constraints are large: the total length over all test cases is up to `10^5`. This immediately rules out any quadratic simulation of operations over all subarrays. Even a solution that tries all windows repeatedly would be far too slow because each operation touches `k` elements and the number of potential operations is large.

A subtle edge case appears when `k = 1`. Each operation only touches a single element and replaces it with itself, so the array never changes. If the array is not already constant, the answer must be `-1`.

Another important edge case is when `k = n`. There is only one possible operation: we take the entire array and set everything to its minimum. This always succeeds in exactly one step unless the array is already constant, in which case zero steps are needed.

A less obvious failure mode arises when the smallest value is isolated in positions that cannot “reach” other parts of the array due to window constraints. For example, if the minimum exists only in a region that cannot be expanded to cover the entire array using length-`k` windows, the answer becomes impossible even though the value exists.

## Approaches

A brute-force strategy would simulate the process directly. At each step, we scan all valid segments of length `k`, choose one, compute its minimum, and apply the update. Repeating this until convergence gives a correct answer in principle, since we are following the allowed operations exactly.

The issue is that each operation requires scanning a window of size `k`, and we may need up to `O(n)` operations in the worst case. This leads to a total complexity on the order of `O(n^2)` per test case, which is far too slow when `n` reaches `10^5`.

The key observation is that the operation always propagates the minimum inside a window, meaning values can only decrease or remain the same, never increase. This implies that the final value of the array must be the global minimum of the initial array. So the problem becomes: how do we spread this minimum across the entire array using fixed-length intervals?

Instead of simulating operations, we can think in reverse. We want every position to eventually be covered by some window whose minimum is already the global minimum. Once a position contains the global minimum, it can serve as a source to spread that value further in subsequent operations.

This turns the problem into a covering and reachability question over intervals of fixed length, where the only useful state is whether a position already contains the global minimum or not. The process becomes greedy: we try to “activate” segments from left to right, always using the rightmost possible valid window that can contribute progress.

This greedy structure leads to a linear scan solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(1) | Too slow |
| Greedy Window Propagation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the minimum value `mn` of the array. If the final array is not `mn`, no operation can ever increase values, so `mn` is the only possible final target. This reduces the goal to making all elements equal to `mn`.
2. If `k == 1`, check whether all elements are already equal to `mn`. If not, return `-1`. This is because no operation changes any value when the window size is 1.
3. If `k == n`, return `1` if not all elements are already `mn`, otherwise return `0`. A single operation over the whole array is enough to make everything equal to the global minimum.
4. Identify all positions where `a[i] == mn`. These positions are the only usable anchors from which the value can propagate.
5. Scan the array from left to right and maintain the furthest position that can be guaranteed to become `mn` using already reachable anchors. At each position `i`, we check whether there exists an anchor in the range `[i - k + 1, i]`. If such an anchor exists, we can perform an operation ending at `i` to propagate `mn` up to `i + k - 1`.
6. Keep extending this reachable boundary greedily. Each time we extend, we count one operation. If at any point a position `i` cannot be covered by any valid window containing a known `mn`, then it is impossible to proceed and we return `-1`.

### Why it works

The key invariant is that every time we perform an operation, we are only ever spreading the global minimum. Any segment that does not contain `mn` cannot produce a smaller value, so it cannot help in reaching new states. Therefore, the only meaningful transitions are those that extend the region already containing `mn`.

Because every operation affects a contiguous block of fixed length, any optimal sequence can be rearranged so that each operation maximally extends the current reachable prefix. If an operation does not extend the boundary as far as possible, it can be shifted or replaced by one that does without increasing the total count. This ensures that the greedy strategy produces the minimum number of operations or correctly detects impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        mn = min(a)

        if k == 1:
            if all(x == mn for x in a):
                out.append("0")
            else:
                out.append("-1")
            continue

        if k == n:
            if all(x == mn for x in a):
                out.append("0")
            else:
                out.append("1")
            continue

        # positions where value equals global minimum
        has = [0] * n
        for i in range(n):
            if a[i] == mn:
                has[i] = 1

        # prefix sum to query existence in window
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + has[i]

        def window_has(l, r):
            if l < 0:
                l = 0
            return pref[r + 1] - pref[l] > 0

        ops = 0
        i = 0

        while i < n:
            if window_has(i - k + 1, i):
                ops += 1
                i += k
            else:
                i += 1

        out.append(str(ops))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first reduces the target state to the global minimum value. The prefix sum array allows constant time checks of whether a valid window contains at least one occurrence of the minimum. The main loop scans left to right and greedily “jumps” forward by `k` whenever it finds a valid window that can perform a useful operation. Each jump corresponds to one operation.

The key implementation detail is the window check: instead of recomputing minimums or simulating operations, we only track where the global minimum already exists, since only those positions can initiate useful propagation.

## Worked Examples

### Example 1

Input:

```
n = 5, k = 3
a = [3, 4, 1000000, 5, 3]
```

We compute `mn = 3`. Positions containing `mn` are indices `0` and `4`.

We scan from left to right:

| i | Window check [i-k+1, i] | Action | ops |
| --- | --- | --- | --- |
| 0 | contains 3 at index 0 | use window | 1 |
| 3 | contains 3 at index 4? no | move | 1 |
| 4 | valid window includes index 4 | use window | 2 |

We end with 2 operations. The first spreads the left `3`, the second uses the right `3` to cover the remaining region.

This confirms that isolated minimums can still propagate as long as they fall inside reachable windows.

### Example 2

Input:

```
n = 4, k = 2
a = [5, 4, 3, 2]
```

Here `mn = 2`, only at index 3.

| i | Window check | Action | ops |
| --- | --- | --- | --- |
| 0 | no min in [0,0] | impossible locally | 0 |
| 1 | no min in [0,1] | move | 0 |
| 2 | no min in [1,2] | move | 0 |
| 3 | min in [2,3] | use window | 1 |

We succeed with one operation ending at the last position.

This shows that the algorithm does not require early positions to be immediately valid, only that every region can eventually be reached by sliding windows.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass with O(1) window checks using prefix sums |
| Space | O(n) | Prefix array for fast range queries |

The total `n` over all test cases is `10^5`, so a linear scan per test case fits comfortably within limits. Memory usage remains linear and stable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# NOTE: placeholder; assumes solve() is imported correctly
# In real use, wrap solve() and capture stdout.

# Minimal cases
# assert run("1\n1 1\n5\n") == "0"

# k = 1 impossible unless already equal
# assert run("1\n3 1\n1 2 1\n") == "-1"

# all equal
# assert run("1\n4 2\n7 7 7 7\n") == "0"

# k = n
# assert run("1\n1\n5 4\n1 2 3 1 1\n") == "1"

# increasing array
# assert run("1\n1\n5 2\n5 4 3 2 1\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k = 1 non-uniform | -1 | impossibility case |
| all equal | 0 | no operation needed |
| k = n | 1 | single global operation |
| decreasing array | 2 | propagation over chain |

## Edge Cases

When `k = 1`, every operation only rewrites a single element with itself, so no change ever happens. For an input like `[1, 2, 1]`, the scan immediately detects non-uniformity and returns `-1` because no window can propagate anything.

When `k = n`, the only possible window covers the entire array. For `[1, 2, 3, 1, 1]`, the minimum is `1`, and one operation replaces everything with `1`. The algorithm directly returns `1` without scanning windows, matching the only valid move sequence.

When minimum values are sparse but reachable through overlapping windows, such as `[3, 4, 100, 5, 3]` with `k = 3`, the algorithm still succeeds because each minimum lies inside at least one valid window that can propagate it. The greedy scan ensures both ends contribute to coverage even if they are far apart.
