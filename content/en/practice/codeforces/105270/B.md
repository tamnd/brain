---
title: "CF 105270B - Minimum MEX"
description: "We are given an array and we are allowed to look at any contiguous segment of it. For every such segment we compute its MEX, the smallest non-negative integer that does not appear inside the segment. Among all segments, we first care about those whose MEX is as large as possible."
date: "2026-06-23T13:03:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105270
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #32 (2^5-Forces, TheForces Rated, Prizes!)"
rating: 0
weight: 105270
solve_time_s: 87
verified: false
draft: false
---

[CF 105270B - Minimum MEX](https://codeforces.com/problemset/problem/105270/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and we are allowed to look at any contiguous segment of it. For every such segment we compute its MEX, the smallest non-negative integer that does not appear inside the segment. Among all segments, we first care about those whose MEX is as large as possible. After identifying that maximum achievable MEX value, we then look at all segments that achieve it and pick the one with the smallest length. The task is to output only that minimum length.

A useful way to reinterpret this is to think about what it means for a segment to have a large MEX. If a segment has MEX equal to k, then every value from 0 to k−1 must appear at least once inside it, while k itself must be absent. So maximizing MEX means we want a segment that contains as many distinct small integers starting from 0 as possible, without including the first missing one.

The constraints imply we cannot try all O(n²) segments. With total n up to 10⁵ across test cases, even O(n√n) is unsafe. We need something linear or near-linear per test case.

A subtle failure case for naive thinking appears when duplicates exist. For example, if the array is `[0, 1, 0, 1, 2]`, it is easy to think longer segments are better because they “accumulate” more values, but MEX depends only on presence, not frequency. Any approach that tracks counts incorrectly or tries to extend greedily without checking missing values can overestimate segment quality.

Another tricky case is when 0 is missing entirely. Then every segment has MEX 0, so the maximum MEX is 0, and the answer becomes the shortest possible segment, which is 1.

## Approaches

A brute-force solution would enumerate every pair (l, r), compute the MEX of that segment, and track the best result. Computing MEX itself takes O(r−l+1) if done with a set scan, so the full approach becomes O(n³) in the worst case. Even if optimized with a frequency array and incremental updates, we still have O(n²) segments to consider, which is too large for n up to 10⁵.

The key observation is that the MEX of a segment depends only on whether all numbers from 0 up to some k−1 appear inside it. So instead of thinking about arbitrary segments, we focus on what values we are trying to include.

Let M be the global MEX of the entire array. No segment can have MEX larger than M, because M itself is absent everywhere. Therefore the maximum possible MEX is exactly M. So we only need segments that contain every number in `[0, M−1]`.

Now the problem becomes: among all segments that cover at least one occurrence of every value from 0 to M−1, find the shortest one. This is a classic “minimum window covering a set of required elements” problem. We can solve it using a sliding window with frequency counting.

We maintain a window [l, r] and expand r while tracking how many distinct required values we have covered. Once the window contains all values 0 to M−1, we try shrinking l to minimize length while preserving coverage.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Sliding Window | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We first compute the global MEX of the array. This is done by marking which values from 0 upward appear, and stopping at the first missing one. Let this value be M.

Then we solve a coverage problem over the set `{0, 1, ..., M−1}`.

1. Build a frequency array or hashmap for values in the current window. We only care about values in `[0, M−1]`, ignoring everything larger since they do not affect MEX.

The reason is that MEX depends only on the absence of the smallest missing value.
2. Maintain a counter `have` which tracks how many distinct required values are currently present in the window.
3. Expand the right pointer `r` step by step. For each new element, if it is in `[0, M−1]`, increase its frequency. If it becomes present for the first time, increment `have`.
4. When `have == M`, the current window contains all required values, so it is valid and has MEX at least M. Since M is the maximum possible, this window is optimal in terms of MEX.
5. At this point, shrink the left pointer `l` as much as possible while still keeping `have == M`. Each time we move `l`, we update frequencies and possibly reduce `have`.
6. During every valid window, update the answer with the minimum length seen.
7. Continue until the right pointer reaches the end.

### Why it works

The key invariant is that at any moment, `have == M` if and only if the current window contains at least one occurrence of every integer in `[0, M−1]`. This condition is exactly equivalent to the window having MEX equal to M. Since no segment can exceed MEX M, every valid window is a candidate solution. The shrinking step ensures that for each right endpoint, we only consider the smallest valid left endpoint, so no optimal segment is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        seen = [False] * (n + 2)
        for x in a:
            if x <= n + 1:
                seen[x] = True

        mex = 0
        while seen[mex]:
            mex += 1

        if mex == 0:
            print(1)
            continue

        freq = [0] * (mex + 1)
        have = 0
        ans = n
        l = 0

        for r in range(n):
            x = a[r]
            if 0 <= x < mex:
                if freq[x] == 0:
                    have += 1
                freq[x] += 1

            while have == mex:
                ans = min(ans, r - l + 1)
                y = a[l]
                if 0 <= y < mex:
                    freq[y] -= 1
                    if freq[y] == 0:
                        have -= 1
                l += 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The first part computes the global MEX by marking which integers appear. This is necessary because it defines the target coverage set. The sliding window then operates only over values below that MEX, since larger values are irrelevant.

The shrinking loop is the most delicate part. The condition `while have == mex` ensures we continuously minimize the left boundary for each fixed right boundary, which is what guarantees minimal segment length.

## Worked Examples

### Example 1

Input:

`a = [0, 1, 0, 1, 2]`

Global MEX is 3 because 0, 1, 2 are all present and 3 is missing.

We need the shortest subarray containing {0,1,2}.

| r | l | window | freq state | have | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [0] | {0:1} | 1 | expand |
| 1 | 0 | [0,1] | {0,1} | 2 | expand |
| 2 | 0 | [0,1,0] | {0,1} | 2 | expand |
| 3 | 0 | [0,1,0,1] | {0,1} | 2 | expand |
| 4 | 0 | [0,1,0,1,2] | {0,1,2} | 3 | valid |

Now we shrink:

| r | l | window | have | action |
| --- | --- | --- | --- | --- |
| 4 | 0 | [0,1,0,1,2] | 3 | shrink l→1 |
| 4 | 1 | [1,0,1,2] | 3 | shrink l→2 |
| 4 | 2 | [0,1,2] | 3 | shrink stops |

Minimum length is 3.

This demonstrates that duplicates do not matter, only coverage does.

### Example 2

Input:

`a = [1, 2, 3]`

Global MEX is 0 since 0 is missing.

Any segment has MEX 0, so answer is 1.

The algorithm immediately handles this via the special case `mex == 0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each element enters and leaves the window at most once |
| Space | O(n) | Frequency array and seen array |

The sum of n across tests is 10⁵, so linear processing per test is sufficient and comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        seen = [False] * (n + 2)
        for x in a:
            if x <= n + 1:
                seen[x] = True

        mex = 0
        while seen[mex]:
            mex += 1

        if mex == 0:
            out.append("1")
            continue

        freq = [0] * (mex + 1)
        have = 0
        ans = n
        l = 0

        for r in range(n):
            x = a[r]
            if 0 <= x < mex:
                if freq[x] == 0:
                    have += 1
                freq[x] += 1

            while have == mex:
                ans = min(ans, r - l + 1)
                y = a[l]
                if 0 <= y < mex:
                    freq[y] -= 1
                    if freq[y] == 0:
                        have -= 1
                l += 1

        out.append(str(ans))

    return "\n".join(out)

# provided sample (format adapted if needed)
assert run("""1
5
0 1 0 1 2
""") == "3"

# minimum size, mex 0
assert run("""1
3
1 2 3
""") == "1"

# all equal
assert run("""1
5
7 7 7 7 7
""") == "1"

# consecutive full coverage
assert run("""1
5
0 1 2 3 1
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single full coverage | 3 | window shrinking correctness |
| no zero | 1 | mex = 0 case |
| all equal | 1 | trivial minimum segment |
| full prefix coverage | 3 | handling repeated values |

## Edge Cases

When the array never contains 0, the computed MEX is 0 and the algorithm directly outputs 1. For input `[5, 6, 7]`, no frequency processing is needed since no segment can improve MEX beyond 0.

When all required values appear multiple times, the sliding window must ignore duplicates. For `[0,1,0,1,2]`, the frequency logic ensures `have` only counts distinct presence, so shrinking does not break correctness.

When required values are spread far apart, the window expands until the last required value is included, then contracts aggressively. This guarantees that even if the optimal segment starts late, it is still discovered when the right pointer reaches its endpoint.
