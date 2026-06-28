---
title: "CF 104885E - \u0425\u043e\u0440\u043e\u0448\u0438\u0435-\u0445\u043e\u0440\u043e\u0448\u0438\u0435 \u043f\u043e\u0434\u043e\u0442\u0440\u0435\u0437\u043a\u0438"
description: "We are given an array and we work with its prefix sums. Let pref[i] denote the sum of the first i elements, with pref[0] = 0. A subarray [l, r] is called good when its sum is zero, which is equivalent to pref[r] - pref[l-1] = 0, or pref[r] = pref[l-1]."
date: "2026-06-28T09:08:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104885
codeforces_index: "E"
codeforces_contest_name: "Municipal stage of ROI in Nizhny Novgorod 2023"
rating: 0
weight: 104885
solve_time_s: 41
verified: true
draft: false
---

[CF 104885E - \u0425\u043e\u0440\u043e\u0448\u0438\u0435-\u0445\u043e\u0440\u043e\u0448\u0438\u0435 \u043f\u043e\u0434\u043e\u0442\u0440\u0435\u0437\u043a\u0438](https://codeforces.com/problemset/problem/104885/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and we work with its prefix sums. Let `pref[i]` denote the sum of the first `i` elements, with `pref[0] = 0`. A subarray `[l, r]` is called good when its sum is zero, which is equivalent to `pref[r] - pref[l-1] = 0`, or `pref[r] = pref[l-1]`.

The problem then asks us to count a stronger notion: a subarray is good-good if it contains at least one sub-subarray whose sum is zero. In terms of prefix sums, this means that inside the range `[l-1, r]`, there must exist two indices `i < j` such that `pref[i] = pref[j]`. If all prefix sums in `[l-1, r]` are distinct, then no zero-sum subarray exists, and the segment is considered bad-good.

So the task reduces to counting subarrays `[l, r]` such that the prefix sums in `[l-1, r]` are not all distinct.

The input is an integer array, and we must compute the number of such “good-good” subarrays.

If the array size is up to around `10^5`, any quadratic enumeration of subarrays becomes impossible. A naive `O(n^2)` scan already produces around `5 * 10^9` operations, which is too slow. This immediately suggests that we need a linear or near-linear scan, most likely with a sliding window.

A subtle edge case appears when all prefix sums are distinct globally. For example, if the array is strictly increasing positive numbers like `[1, 2, 3]`, then every prefix sum is distinct, so no zero-sum subarray exists anywhere. The correct answer should be `0`. A naive approach that only checks local subarrays without tracking prefix uniqueness would incorrectly count many segments.

Another edge case is when the array has many repeated prefix sums. For example `[1, -1, 1, -1]` produces repeated prefix sums and many zero-sum subarrays. Here the correct counting depends on detecting first repetition boundaries, not enumerating subarrays.

## Approaches

A brute force strategy fixes `(l, r)` and checks whether there exists a duplicate prefix sum in `[l-1, r]`. This requires scanning the segment or using a set per query. Each check is `O(n)`, and there are `O(n^2)` segments, giving `O(n^3)` or `O(n^2 log n)` depending on implementation. This is far too slow.

The key observation is to flip the condition. Instead of directly counting good-good segments, we consider the complement: segments where all prefix sums are distinct. These are exactly the segments that contain no repeated prefix sum, meaning no zero-sum subarray exists inside them.

We can fix the right endpoint `r` and maintain the longest valid segment ending at `r` such that prefix sums are unique. Let `l` be the smallest index such that `[l, r]` is invalid, meaning there is a repeated prefix sum inside `[l, r]`. Then all starting points `l' < l` produce valid segments `[l', r]` that are good-good, and all `l' >= l` produce invalid ones.

Thus, for each `r`, the contribution is exactly `l`, and we can compute it using a sliding window with a hash map tracking last occurrences of prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal sliding window | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We first convert the array into prefix sums, because the problem is entirely about equality of prefix values.

We then maintain a sliding window over prefix indices `[l, r]` such that all prefix sums inside are distinct.

1. Initialize a hash map `last`, which stores the last index where each prefix sum was seen. Also set `l = 0` and `answer = 0`.
2. Iterate `r` from `0` to `n` over prefix sums. Each step tries to extend the window to include `pref[r]`.
3. If `pref[r]` has been seen before at position `p`, and `p >= l`, then we must move `l` to `p + 1`. This is necessary because keeping `p` inside the window would introduce a duplicate prefix sum, violating uniqueness.
4. After fixing `l`, we add the contribution `l` to the answer. This counts how many starting points produce a bad-good segment ending at `r`, which corresponds to good-good segments in the original formulation.
5. Update `last[pref[r]] = r`.

The reason we use prefix indices rather than array indices is that subarray sums are encoded as equality between two prefix positions.

### Why it works

At any fixed `r`, the window `[l, r]` is the longest suffix ending at `r` with all prefix sums distinct. Any starting point `l' < l` ensures that `[l', r]` must contain a repeated prefix sum, because the repeated occurrence at `l-1` and some earlier position is forced inside the segment. Conversely, any `l' >= l` keeps all prefix sums distinct inside the segment. This creates a clean partition of valid and invalid starting points, making `l` the exact contribution boundary.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    last = {}
    l = 0
    ans = 0

    for r in range(n + 1):
        x = pref[r]

        if x in last and last[x] >= l:
            l = last[x] + 1

        last[x] = r
        ans += l

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the sliding window idea over prefix sums. The critical detail is that we iterate over `pref[0..n]`, not the original array. The map `last` stores positions of prefix sums, and the pointer `l` always jumps forward, never backward, ensuring linear complexity.

The accumulation `ans += l` corresponds to counting all valid starting positions for subarrays ending at each `r`.

## Worked Examples

### Example 1

Input:

```
4
1 -1 1 -1
```

Prefix sums:

`[0, 1, 0, 1, 0]`

| r | pref[r] | last map before | l | action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | {} | 0 | insert 0 | 0 |
| 1 | 1 | {0:0} | 0 | insert 1 | 0 |
| 2 | 0 | {0:0,1:1} | 1 | duplicate 0 forces l=1 | 1 |
| 3 | 1 | {...} | 2 | duplicate 1 forces l=2 | 3 |
| 4 | 0 | {...} | 3 | duplicate 0 forces l=3 | 6 |

The final answer is `6`, showing that many subarrays contain repeated prefix sums, meaning many segments contain a zero-sum subarray.

### Example 2

Input:

```
3
1 2 3
```

Prefix sums:

`[0, 1, 3, 6]` all distinct.

| r | pref[r] | l | ans |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 2 | 3 | 0 | 0 |
| 3 | 6 | 0 | 0 |

No duplicates ever appear, so `l` never moves and every segment is invalid in the original sense, giving answer `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each prefix index is processed once, and each update of `l` is monotonic |
| Space | O(n) | hash map stores at most `n` prefix sums |

The solution fits comfortably within limits for `n` up to `10^5`, since it performs only linear work and constant-time hash operations per step.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    last = {}
    l = 0
    ans = 0

    for r in range(n + 1):
        x = pref[r]
        if x in last and last[x] >= l:
            l = last[x] + 1
        last[x] = r
        ans += l

    return str(ans)

# all-positive distinct prefix sums
assert run("3\n1 2 3\n") == "0"

# alternating sum
assert run("4\n1 -1 1 -1\n") == "6"

# single element zero
assert run("1\n0\n") == "1"

# all zeros
assert run("3\n0 0 0\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n0\n` | `1` | single-element prefix duplicate behavior |
| `3\n0 0 0\n` | `6` | heavy repetition forces frequent l shifts |
| `3\n1 2 3\n` | `0` | no prefix collisions case |
| `4\n1 -1 1 -1\n` | `6` | alternating prefix repetition pattern |

## Edge Cases

When all elements are zero, every prefix sum repeats at every step. The algorithm starts with `l = 0`, and each new `0` forces `l` to jump to the last occurrence plus one. This creates maximal shifting and produces contributions growing as `0 + 1 + 2 + 3`.

When all prefix sums are distinct, the hash map never triggers a reset of `l`. The window remains maximal, but since no repeated prefix sum exists, every segment is invalid in terms of containing a zero-sum subarray, resulting in zero contributions.

When a single value repeats far apart, such as prefix sums `[0, 5, 10, 5, 15]`, the jump in `l` happens exactly when the second `5` appears. The pointer skips over all invalid starts at once, which is the key mechanism preventing quadratic behavior.
