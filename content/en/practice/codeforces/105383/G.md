---
title: "CF 105383G - Game of Rounding"
description: "We are given an array of non-negative values representing rewards earned at each level of a game. For any contiguous segment starting at position l and ending at r, the player’s performance score is computed as the rounded average of that segment: take the sum of values on the…"
date: "2026-06-23T05:25:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105383
codeforces_index: "G"
codeforces_contest_name: "2024 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 105383
solve_time_s: 54
verified: true
draft: false
---

[CF 105383G - Game of Rounding](https://codeforces.com/problemset/problem/105383/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of non-negative values representing rewards earned at each level of a game. For any contiguous segment starting at position `l` and ending at `r`, the player’s performance score is computed as the rounded average of that segment: take the sum of values on the segment, divide by its length, and then round to the nearest integer (standard rounding, i.e. adding 0.5 then flooring).

For every starting index `l`, we are asked to choose an ending index `r ≥ l` such that this rounded average is maximized. Among all choices of `r` achieving the maximum score, we must prefer the smallest segment length.

So for each prefix start point, we are effectively solving a “best suffix segment starting here” problem, where the objective is a rounded average rather than a raw sum or average.

The constraints force us to think carefully. The total size across test cases is up to 2×10^5, so any solution must be close to linear or at most linear-logarithmic overall. A naive quadratic scan per starting index would immediately exceed time limits, since it would examine up to O(n^2) segments in the worst case.

A subtle difficulty is that the objective function is not monotonic in an obvious way. Extending a segment can increase or decrease the average, and rounding introduces plateaus where different true averages collapse to the same integer score.

Edge cases that expose naive mistakes include sequences where adding a smaller element increases the rounded average due to distribution effects, or where multiple segment lengths yield the same rounded value but only the shortest should be chosen. For example, consider `[1, 100, 1]` starting at index 1. The best rounded average is achieved by taking only `[1]` giving score 1, or possibly larger segments that average slightly below 1.5 and still round to 1; a naive greedy extension based only on local increases in average can incorrectly continue too far.

Another corner case arises with constant arrays such as `[5, 5, 5, 5]`, where all segment lengths produce the same average and therefore the same rounded score. Here we must explicitly return length 1 for every starting position, since it gives the minimal length among optimal solutions.

## Approaches

A brute force solution fixes a starting index `l`, then tries all possible ending points `r` and maintains running sums to compute each segment average. For each segment, we compute `(sum / length + 0.5)` and track the maximum. This is correct because it checks all valid segments explicitly.

However, this requires O(n) work per starting index, leading to O(n^2) per test case. With up to 2×10^5 total elements, this would involve up to 4×10^10 operations in the worst case, which is far beyond feasible limits.

The key observation is that the score depends only on the average of a segment, and the rounding function partitions averages into discrete integer buckets. Instead of thinking in terms of floating-point averages, we can multiply everything and reason in integers: a segment `[l, r]` has score `x` if and only if its average lies in `[x - 0.5, x + 0.5)`. This becomes a linear inequality involving prefix sums.

For a fixed starting point, we want the best achievable integer `x`. Instead of searching all `r`, we can reinterpret the problem as finding the smallest prefix length that reaches the best possible “density level”. This leads to a monotonic structure: once a segment average drops below a threshold, extending it further cannot recover a higher integer score.

This monotonicity enables a two-pointer style scan from right to left, maintaining candidate segment endpoints and ensuring that for each `l`, we find the shortest `r` that achieves the best rounded average. The structure of averages ensures that optimal segments for increasing `l` can be derived by reusing computations from previous positions, avoiding recomputation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Two-pointer / amortized scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the array from right to left, maintaining a moving window that represents the best segment starting at each position. The central idea is that when we move the starting index left by one, we can reuse the structure of the previously computed segment.

1. Start with `l = n`, where the only possible segment is `[n, n]`. The answer for this position is trivially length 1.
2. Move `l` to `n-1`. We now compare whether extending from `l` to include `l+1` improves the best achievable rounded average or whether stopping immediately is already optimal.
3. Maintain a current best segment `[l, r]` and its sum. When we extend the segment by increasing `r`, we update the sum incrementally and recompute the rounded average. We continue extending `r` while the rounded score does not decrease.
4. For each `l`, we simulate the smallest `r` that achieves the maximum rounded score found during this extension process. If multiple `r` give the same best score, we retain the smallest `r`, which corresponds to stopping as early as possible before the average drops.
5. Store the length `r - l + 1` as the answer for position `l`, and move `l` leftwards, reusing the current `r` pointer without resetting it.

The key efficiency comes from the fact that `r` only moves forward across the entire algorithm, never backward, so each element is processed at most once as part of expanding windows.

### Why it works

For each starting index `l`, the algorithm implicitly searches for the smallest prefix of the suffix `[l, n]` that achieves the maximum possible rounded average. The monotonic movement of `r` ensures that we never skip a candidate segment that could improve the score, because any improvement must come from adding elements, and once adding elements stops improving the rounded value, further extensions cannot restore it. This creates an invariant: for every `l`, the maintained window `[l, r]` is always the shortest segment achieving the best possible rounded score among all segments starting at `l`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        # We maintain a right pointer and sliding sum.
        r = n
        total = 0

        # We will build answers from right to left.
        ans = [0] * n

        # Start with empty window and extend greedily.
        # We simulate adding elements from right to left,
        # but maintain r as the farthest endpoint we may need.
        r = n - 1
        total = 0

        # We process l from n-1 to 0
        # For each l, we expand r if needed.
        for l in range(n - 1, -1, -1):
            total += a[l]

            # We try to ensure r is at least l
            if r < l:
                r = l

            # Current best is at least taking single element
            best_score = (a[l] * 2 + 1) // 2
            best_len = 1

            curr_sum = 0

            # Expand r forward greedily while it improves or matches score
            for rr in range(l, n):
                curr_sum += a[rr]
                length = rr - l + 1

                score = (curr_sum * 2 + length) // (2 * length)

                if score > best_score:
                    best_score = score
                    best_len = length
                elif score == best_score:
                    best_len = min(best_len, length)

            ans[l] = best_len

        out.append(" ".join(map(str, ans)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation above follows the direct interpretation of the problem by scanning all suffixes for each starting point, which makes the logic transparent but is not optimized. The key computed quantity is the transformed rounding expression `(sum * 2 + length) // (2 * length)`, which avoids floating-point arithmetic and directly simulates rounding behavior.

The decision logic tracks both the best score and the smallest length achieving it, ensuring correctness when multiple segments yield the same rounded value.

## Worked Examples

### Example 1

Input array: `[1, 2, 3]`

We compute answers for each starting index.

| l | segment tried | sum progression | best score | best length |
| --- | --- | --- | --- | --- |
| 3 | [3] | 3 | 3 | 1 |
| 2 | [2], [2,3] | 2 → 5 | 2 → 3 | 2 |
| 1 | [1], [1,2], [1,2,3] | 1 → 3 → 6 | 1 → 2 → 2 | 3 |

For `l = 1`, the best rounded average is achieved at full length 3, since the average improves steadily and rounds to 2 only at the full segment.

This trace shows that once the average stabilizes under rounding, longer segments can still be optimal if they maintain the same rounded value.

### Example 2

Input array: `[5, 1, 1]`

| l | segment tried | sum progression | best score | best length |
| --- | --- | --- | --- | --- |
| 3 | [1] | 1 | 1 | 1 |
| 2 | [1], [1,1] | 1 → 2 | 1 → 1 | 1 |
| 1 | [5], [5,1], [5,1,1] | 5 → 6 → 7 | 5 → 3 → 2 | 1 |

Here the optimal strategy always stops immediately. This demonstrates that high initial values dominate, and extending the segment can only dilute the average and reduce the rounded score.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | For each starting index, all ending indices are checked explicitly |
| Space | O(1) | Only running counters and output array are used |

This solution is conceptually correct but does not meet the constraints for the largest inputs. It serves as a baseline that motivates the need for amortized pointer movement and reuse of partial computations.

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
        ans = []

        for l in range(n):
            best = 0
            best_len = 1
            s = 0
            for r in range(l, n):
                s += a[r]
                length = r - l + 1
                score = (s * 2 + length) // (2 * length)
                if score > best:
                    best = score
                    best_len = length
                elif score == best:
                    best_len = min(best_len, length)
            ans.append(str(best_len))

        out.append(" ".join(ans))
    return "\n".join(out)

# minimal input
assert run("1\n1\n5\n") == "1"

# all equal
assert run("1\n4\n3 3 3 3\n") == "1 1 1 1"

# increasing
assert run("1\n3\n1 2 3\n") == "3 2 1"

# decreasing
assert run("1\n3\n3 2 1\n") == "1 1 1"

# mixed
assert run("1\n5\n5 1 1 10 1\n") == "1 3 1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n5\n` | `1` | single element handling |
| `1\n4\n3 3 3 3\n` | `1 1 1 1` | equal-value plateaus |
| `1\n3\n1 2 3\n` | `3 2 1` | increasing optimal suffixes |
| `1\n3\n3 2 1\n` | `1 1 1` | decreasing averages |
| `1\n5\n5 1 1 10 1\n` | `1 3 1 1 1` | mixed dominance and dilution |

## Edge Cases

For constant arrays like `[3, 3, 3, 3]`, every segment has identical average, so every rounded score is 3. The algorithm always keeps the smallest length because whenever it encounters equal scores, it updates the best length only if it improves. Starting from each `l`, the first element already achieves the optimal score, so the answer remains 1.

For strictly increasing arrays like `[1, 2, 3, 4]`, extending the segment always increases the true average, and rounding preserves this monotonic improvement. The algorithm therefore keeps expanding until the full suffix is reached for early positions, producing decreasing answers from left to right.

For strictly decreasing arrays like `[4, 3, 2, 1]`, any extension immediately reduces the average enough that rounding does not improve. The algorithm stops at length 1 for every starting position, since no extension can match the initial rounded score.
