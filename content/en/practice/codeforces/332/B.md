---
title: "CF 332B - Maximum Absurdity"
description: "We are given a list of numbers placed on a line, where each position represents a law and its value represents how “useful” or “valuable” it is. We must select exactly two contiguous blocks of fixed length k."
date: "2026-06-06T10:03:04+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 332
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 193 (Div. 2)"
rating: 1500
weight: 332
solve_time_s: 76
verified: true
draft: false
---

[CF 332B - Maximum Absurdity](https://codeforces.com/problemset/problem/332/B)

**Rating:** 1500  
**Tags:** data structures, dp, implementation  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of numbers placed on a line, where each position represents a law and its value represents how “useful” or “valuable” it is. We must select exactly two contiguous blocks of fixed length `k`. These two blocks cannot overlap, and we want the sum of all values inside both blocks to be as large as possible.

Another way to see it is that we are sliding a window of size `k` across the array and computing its sum at every valid starting position. From these window sums, we must choose two windows such that their indices do not overlap and the total of their sums is maximized. The output is not the value but the starting indices of these two windows, with a tie-breaking rule that prefers smaller starting indices first.

The constraints are large, with up to 200,000 elements. Any solution that tries all pairs of windows would require checking roughly $O(n^2)$ combinations, which is far too slow. Even $O(nk)$ solutions that recompute window sums repeatedly would also fail in the worst case. This forces us toward a linear or near-linear solution, typically $O(n)$ or $O(n \log n)$.

A few edge cases are easy to miss. If all values are identical, any pair of valid segments is optimal, but the tie-breaking rule forces us to pick the earliest possible first segment and then the earliest compatible second segment. Another subtle case happens when the best two segments are adjacent versus slightly separated; a naive greedy choice might pick a locally best second segment that blocks a globally better pairing.

For example, consider:

```
n = 5, k = 2
values = [5, 1, 5, 1, 5]
```

The best choice is segments starting at 1 and 3 (or 3 and 5), but picking the best single segment first greedily can block the optimal pair.

The key difficulty is that the best second segment depends on where the first segment ends, so we need a structure that allows us to efficiently combine best prefix choices with suffix scanning.

## Approaches

The brute-force idea is straightforward: compute the sum of every subarray of length `k`, store them, and then try every pair of non-overlapping subarrays. If there are about `n` possible subarrays, then checking all pairs is $O(n^2)$, and each check is $O(1)$, so total complexity is $O(n^2)$, which is too large for 200,000.

We can improve this by observing that once we know the sum of every window of size `k`, the problem reduces to selecting two indices `i < j - k + 1` maximizing `sum[i] + sum[j]`. Instead of trying all pairs, we can precompute the best possible first segment for every position `j` where the second segment starts.

For each position `j`, we want to know the best `i` to the left of it. That naturally suggests maintaining a prefix maximum over window sums. Then for each `j`, we pair it with the best valid `i` before it and compute the answer.

This reduces the problem from quadratic pairing to a single pass with precomputed window sums and prefix best positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Prefix optimization | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We first convert the array into an array of window sums, where each index represents the sum of a subarray of length `k`.

1. Compute prefix sums of the input array so that any window sum can be computed in constant time. This avoids recomputing sums repeatedly and ensures we stay linear overall.
2. Build an array `w`, where `w[i]` is the sum of the segment starting at `i` (1-indexed). Each value represents the “score” of choosing a segment at that position.
3. Create an array `best_left`, where `best_left[i]` stores the index of the best window among all windows starting from `1` to `i`. The “best” means largest sum; if equal, we keep the smaller index. This prefix structure allows us to instantly know the optimal first segment for any second segment position.
4. Iterate over all valid starting positions of the second segment. For a second segment starting at `i`, the first segment must end before it starts, so the last valid start is `i - k`.
5. For each valid `i`, compute total value as `w[i] + w[best_left[i - k]]` and track the maximum. Apply tie-breaking by preferring smaller first index, then smaller second index.
6. Output the two stored starting positions.

The key idea is that when we fix the second segment, the best first segment is already known in constant time via prefix maximum.

Why it works: at every position `i`, `best_left[i]` stores the optimal first segment among all valid candidates. Any optimal pair must have its first segment within that range, and pairing it with a fixed second segment does not affect its internal optimality. This reduces the global optimization problem into independent local decisions over a prefix and suffix split.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

# prefix sums
pref = [0] * (n + 1)
for i in range(n):
    pref[i + 1] = pref[i] + a[i]

# window sums
w = [0] * (n - k + 1)
for i in range(n - k + 1):
    w[i] = pref[i + k] - pref[i]

# best position to the left
best_left = [0] * len(w)
best_left[0] = 0

for i in range(1, len(w)):
    if w[i] > w[best_left[i - 1]]:
        best_left[i] = i
    else:
        best_left[i] = best_left[i - 1]

best_i = 0
best_j = k
best_val = -1

for j in range(k, len(w)):
    i = best_left[j - k]
    val = w[i] + w[j]
    if val > best_val:
        best_val = val
        best_i = i
        best_j = j
    elif val == best_val and (i < best_i or (i == best_i and j < best_j)):
        best_i = i
        best_j = j

print(best_i + 1, best_j + 1)
```

The prefix array is standard and ensures each window sum is computed in constant time. The array `w` compresses the problem into selecting two elements instead of two segments.

The `best_left` array is the critical structure: it ensures that for every possible second segment, we can instantly retrieve the best valid first segment without scanning.

Tie-breaking is handled explicitly in the final loop by comparing indices after matching sums.

## Worked Examples

### Example 1

Input:

```
5 2
3 6 1 1 6
```

Window sums:

| i | window | sum |
| --- | --- | --- |
| 0 | [3,6] | 9 |
| 1 | [6,1] | 7 |
| 2 | [1,1] | 2 |
| 3 | [1,6] | 7 |

Now build `best_left`:

| i | w[i] | best_left[i] |
| --- | --- | --- |
| 0 | 9 | 0 |
| 1 | 7 | 0 |
| 2 | 2 | 0 |
| 3 | 7 | 0 |

For each second segment:

- j = 2: best i in [0..0] → i=0, total = 9 + 2 = 11
- j = 3: best i in [0..1] → i=0, total = 9 + 7 = 16

Best pair is (0, 3) in 0-indexed form → (1, 4).

This shows how prefix selection ensures we never miss the globally optimal first segment when evaluating later positions.

### Example 2

Input:

```
6 2
1 2 3 1 2 3
```

Window sums:

```
[3, 5, 4, 3, 5]
```

We compare:

- Best pair occurs with windows at 1 and 4 (0-indexed 1 and 4), giving 5 + 5 = 10.

| j | best i | pair sum |
| --- | --- | --- |
| 2 | 0 | 8 |
| 3 | 1 | 8 |
| 4 | 1 | 10 |

This demonstrates how the algorithm correctly waits for a better second segment even if earlier ones look promising.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | prefix sums, window sums, and two linear scans |
| Space | O(n) | arrays for prefix sums and window sums |

The solution runs comfortably within limits because every element is processed a constant number of times, and no nested iteration over segments exists.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    w = [0] * (n - k + 1)
    for i in range(n - k + 1):
        w[i] = pref[i + k] - pref[i]

    best_left = [0] * len(w)
    for i in range(1, len(w)):
        if w[i] > w[best_left[i - 1]]:
            best_left[i] = i
        else:
            best_left[i] = best_left[i - 1]

    best_i = best_j = 0
    best_val = -1

    for j in range(k, len(w)):
        i = best_left[j - k]
        val = w[i] + w[j]
        if val > best_val or (val == best_val and (i < best_i or (i == best_i and j < best_j))):
            best_val = val
            best_i, best_j = i, j

    return f"{best_i + 1} {best_j + 1}"

# provided sample
assert run("5 2\n3 6 1 1 6\n") == "1 4"

# minimum case
assert run("2 1\n5 6\n") == "1 2"

# all equal
assert run("6 2\n1 1 1 1 1 1\n") == "1 3"

# clear separated peaks
assert run("6 2\n1 100 1 1 100 1\n") == "1 4"

# adjacent best vs later best
assert run("7 2\n5 1 5 1 5 1 5\n") == "1 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 2 ...` | `1 4` | sample correctness |
| `2 1 ...` | `1 2` | minimum size behavior |
| all equal | `1 3` | tie-breaking stability |
| two peaks | `1 4` | non-overlapping optimal pairing |
| alternating peaks | `1 3` | correct global pairing over greedy |

## Edge Cases

When all values are identical, every window has the same score. The prefix maximum array always keeps the earliest index, so the first segment is fixed as early as possible, and the second segment becomes the earliest valid position after it. This matches the tie-breaking requirement exactly.

When the best two windows are adjacent versus slightly farther apart, the algorithm still behaves correctly because adjacency is enforced only through index separation, not through preference. Even if a later window is locally optimal, it will not replace a globally optimal earlier prefix when constructing `best_left`.

For small inputs like `n = 2k`, there is exactly one valid pair of segments, and the algorithm reduces correctly to selecting that pair without any ambiguity.
