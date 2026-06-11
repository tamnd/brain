---
title: "CF 1415B - Repainting Street"
description: "We have a row of houses, each painted with some color. In one day, Tom chooses a contiguous segment of exactly k houses. Inside that segment he may repaint any subset of those houses, and each house can be repainted to any color independently."
date: "2026-06-11T07:11:42+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1415
codeforces_index: "B"
codeforces_contest_name: "Technocup 2021 - Elimination Round 2"
rating: 1100
weight: 1415
solve_time_s: 113
verified: true
draft: false
---

[CF 1415B - Repainting Street](https://codeforces.com/problemset/problem/1415/B)

**Rating:** 1100  
**Tags:** brute force, greedy  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of houses, each painted with some color. In one day, Tom chooses a contiguous segment of exactly `k` houses. Inside that segment he may repaint any subset of those houses, and each house can be repainted to any color independently.

The goal is to make every house end up with the same color while using as few days as possible.

A useful way to think about the operation is that a day allows us to "fix" up to `k` consecutive positions. Since houses inside the chosen segment can be repainted however we want, the only thing that matters is which houses already have the final target color and which do not.

The number of colors is at most 100, while the total number of houses across all test cases is at most `10^5`. This immediately suggests that trying every possible final color is feasible. On the other hand, anything that repeatedly scans large portions of the array for every position would become too expensive. An `O(n * 100)` solution is easily fast enough, while `O(n^2)` is not.

There are a few subtle situations that can cause incorrect reasoning.

Consider:

```
n = 5, k = 2
1 1 1 1 1
```

The answer is `0` because the street is already beautiful. A careless solution that always performs at least one operation for the chosen color would return `1`.

Consider:

```
n = 5, k = 5
1 2 3 4 5
```

The answer is `1`. One segment of length 5 covers the entire street, so every house can be repainted on the same day. A solution that counts mismatched houses individually would incorrectly return `5`.

Consider:

```
n = 7, k = 3
1 2 1 2 1 2 1
```

If the target color is `1`, the mismatches are at positions 2, 4, and 6. One operation starting at position 2 covers positions 2 through 4, fixing two mismatches at once. Another operation starting at position 6 fixes the last one. The answer is `2`, not `3`. Counting mismatches instead of segments would overestimate the result.

## Approaches

The most direct brute-force idea is to choose a target color and simulate all possible repainting strategies. We could model the street state after every operation and search for the minimum number of days. This is correct because it explores all possibilities, but the number of possible segments and repainting choices grows explosively. Even for moderate values of `n`, such a search becomes completely impractical.

The key observation is that the actual colors inside a repaint operation do not matter. Once we decide that the final street color will be `x`, every position is either already correct or needs to become `x`.

Suppose we scan the street from left to right while targeting color `x`.

When we encounter a house that already has color `x`, we do nothing.

When we encounter a house with a different color, that position must eventually be covered by some repaint operation. The best choice is to start an operation here. Since one operation affects a segment of length `k`, we can immediately skip the next `k` positions because they can all be fixed within that same day.

This greedy step is optimal. Any solution must cover that mismatching position somehow, and starting the repaint segment at the first uncovered mismatch covers as many future positions as possible.

Since colors are limited to the range `1..100`, we can try every possible target color and take the minimum answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(100n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the answer to a very large value.
2. For every possible target color `x` from 1 to 100, compute how many days are needed if the entire street must become color `x`.
3. Scan the houses from left to right using index `i`.
4. If house `i` already has color `x`, move to the next position because no repainting is needed there.
5. If house `i` has a different color, one repaint operation is unavoidable. Increase the day count by one.
6. After using that repaint operation, skip the next `k` positions by setting `i += k`.

The operation can cover a segment of length `k` beginning at this mismatch, so every position inside that segment can be fixed during the same day.
7. Continue until the scan reaches the end of the street.
8. Update the global answer with the minimum day count among all target colors.
9. Output the minimum answer.

### Why it works

Fix a target color `x`.

During the left-to-right scan, suppose position `i` is the first mismatch that has not yet been covered by any previous repaint operation. Any valid solution must use some operation covering position `i`, otherwise that house would never become color `x`.

Starting the operation at position `i` is never worse than starting it earlier, because earlier positions have already been handled. Starting at `i` covers position `i` and extends coverage as far to the right as possible, potentially fixing additional future mismatches.

The greedy choice always covers the maximum useful range beginning from the first uncovered mismatch. Repeating this process produces the minimum number of operations for the chosen target color. Since the optimal final color must be one of the colors in the allowed range, checking all colors and taking the minimum yields the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, k = map(int, input().split())
        c = list(map(int, input().split()))

        answer = float('inf')

        for target in range(1, 101):
            days = 0
            i = 0

            while i < n:
                if c[i] == target:
                    i += 1
                else:
                    days += 1
                    i += k

            answer = min(answer, days)

        print(answer)

solve()
```

The outer loop tries every possible final color. Since colors are restricted to at most 100 distinct values, this is very cheap.

For a fixed target color, the variable `i` scans the street. When a position already matches the target, we simply advance by one.

When a mismatch is found, we immediately spend one day and jump ahead by `k` positions. This models placing a repaint segment of length `k` starting at the current mismatch. The segment fixes every house inside its range that needs changing, so revisiting those positions would be redundant.

One easy mistake is jumping by `k - 1` instead of `k`. The current mismatching position is also part of the painted segment, so the entire segment contains exactly `k` positions.

Another common mistake is trying only colors that already appear in the array. That actually works for this problem, but iterating through all colors `1..100` is simpler and still runs comfortably within the limits.

## Worked Examples

### Example 1

Input:

```
n = 10, k = 2
1 1 2 2 1 1 2 2 2 1
```

Try target color `2`.

| Step | Position | Color | Action | Days |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | mismatch, paint | 1 |
| 2 | 3 | 2 | already correct | 1 |
| 3 | 4 | 2 | already correct | 1 |
| 4 | 5 | 1 | mismatch, paint | 2 |
| 5 | 7 | 2 | already correct | 2 |
| 6 | 8 | 2 | already correct | 2 |
| 7 | 9 | 2 | already correct | 2 |
| 8 | 10 | 1 | mismatch, paint | 3 |

The result for target color `2` is 3 days. No other target color does better, so the final answer is `3`.

This trace shows how a single repaint operation can eliminate several future mismatches by skipping an entire block of length `k`.

### Example 2

Input:

```
n = 10, k = 3
1 3 3 3 3 1 2 1 3 3
```

Try target color `3`.

| Step | Position | Color | Action | Days |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | mismatch, paint | 1 |
| 2 | 4 | 3 | already correct | 1 |
| 3 | 5 | 3 | already correct | 1 |
| 4 | 6 | 1 | mismatch, paint | 2 |
| 5 | 9 | 3 | already correct | 2 |
| 6 | 10 | 3 | already correct | 2 |

The answer for color `3` is 2 days, which is optimal.

This example demonstrates why jumping by exactly `k` positions is correct. The operation at position 6 covers positions 6 through 8, fixing all remaining non-3 houses in that region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(100n) | Scan the array once for each possible color |
| Space | O(1) | Only a few counters are stored |

Since the sum of all `n` values is at most `10^5`, the total work is roughly `100 × 10^5 = 10^7` simple operations, which easily fits within the time limit in Python. Memory usage stays constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        c = list(map(int, input().split()))

        ans = 10**9

        for target in range(1, 101):
            days = 0
            i = 0

            while i < n:
                if c[i] == target:
                    i += 1
                else:
                    days += 1
                    i += k

            ans = min(ans, days)

        out.append(str(ans))

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""3
10 2
1 1 2 2 1 1 2 2 2 1
7 1
1 2 3 4 5 6 7
10 3
1 3 3 3 3 1 2 1 3 3
"""
) == "3\n6\n2\n", "sample"

# minimum size
assert run(
"""1
1 1
5
"""
) == "0\n", "single house"

# already beautiful
assert run(
"""1
5 3
7 7 7 7 7
"""
) == "0\n", "all equal"

# k = n
assert run(
"""1
5 5
1 2 3 4 5
"""
) == "1\n", "whole array in one operation"

# off-by-one coverage check
assert run(
"""1
7 3
1 2 1 2 1 2 1
"""
) == "2\n", "segment coverage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5` | `0` | Minimum-size instance |
| `7 7 7 7 7` | `0` | Already beautiful street |
| `1 2 3 4 5` with `k=5` | `1` | Whole street covered in one day |
| `1 2 1 2 1 2 1` with `k=3` | `2` | Correct segment skipping and off-by-one handling |

## Edge Cases

Consider:

```
1
5 5
1 2 3 4 5
```

For target color `1`, the first mismatch appears at position 2. One repaint operation covers positions 2 through 5, so the scan immediately exits. The algorithm returns `1`. This matches the fact that a segment of length `n` covers the entire street.

Consider:

```
1
5 3
4 4 4 4 4
```

Every position already matches the target color `4`. The scan never enters the repaint branch, so the day count remains `0`. The algorithm correctly recognizes that no work is needed.

Consider:

```
1
7 3
1 2 1 2 1 2 1
```

Using target color `1`, the first mismatch is at position 2. One operation covers positions 2 through 4. The next uncovered mismatch is position 6, requiring one more operation. Total days equal `2`. This confirms that the algorithm groups multiple mismatches into a single repaint whenever they lie inside the same length-`k` segment.

Consider:

```
1
7 1
1 2 3 4 5 6 7
```

With `k = 1`, every operation affects exactly one house. For any chosen target color, six houses differ from it, so six repaint operations are required. The algorithm finds each mismatch and advances by one position, producing the correct answer `6`.
