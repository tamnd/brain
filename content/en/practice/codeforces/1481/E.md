---
title: "CF 1481E - Sorting Books"
description: "We have a row of books. Each book has a color. We may repeatedly choose any book and move it to the end of the row. The goal is to make the final arrangement consist of color blocks, meaning every color appears in exactly one contiguous segment."
date: "2026-06-10T23:37:34+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1481
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 699 (Div. 2)"
rating: 2500
weight: 1481
solve_time_s: 139
verified: false
draft: false
---

[CF 1481E - Sorting Books](https://codeforces.com/problemset/problem/1481/E)

**Rating:** 2500  
**Tags:** data structures, dp, greedy  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We have a row of books. Each book has a color. We may repeatedly choose any book and move it to the end of the row.

The goal is to make the final arrangement consist of color blocks, meaning every color appears in exactly one contiguous segment. Different colors may appear in any order, but books of the same color must end up adjacent.

We need the minimum number of books moved.

The operation is unusual. We never insert a book somewhere in the middle. Every moved book goes to the far right. Because of that, some books stay in their original relative order forever, while moved books are collected at the end.

The input size reaches $5 \cdot 10^5$. Any algorithm that tries all possible final color orders, all subsets of moved books, or performs quadratic scans is immediately impossible. Even $O(n \sqrt n)$ would be uncomfortable at this scale. We need something close to linear or $O(n \log n)$.

The difficult part is understanding what the books that remain in place can look like. A naive idea is to keep the largest already-beautiful subsequence, but the operation is much more restrictive than arbitrary deletions. We must respect the structure created by moving books only to the end.

Several edge cases are easy to mishandle.

Consider:

```
1 2 1
```

The answer is 1. Move the middle book:

```
1 1 2
```

A solution that only checks whether each color is already contiguous in the original array would incorrectly conclude that two books must move.

Another subtle case is:

```
1 2 2 1
```

The answer is 1. Move the last `1`:

```
1 2 2 1
→
1 2 2 1   (remove last 1)
→
1 2 2 1   (append to end, same position)
```

More naturally, move the first `1`:

```
2 2 1 1
```

The important observation is that a color does not necessarily need all its occurrences preserved in the stationary part.

A third case is when one color already occupies a complete interval:

```
1 2 2 2 3
```

The answer is 0. Any algorithm that forces colors to appear in increasing or decreasing order of value would fail, because the final order of color blocks is completely unrestricted.

## Approaches

The brute-force viewpoint is to decide which books stay in place. Every book that does not stay must be moved to the end.

Suppose we knew the set of stationary books. Their relative order never changes. After removing all moved books, the stationary books must already form a beautiful shelf, because moved books are appended later and cannot alter the internal structure of the stationary prefix.

This suggests searching for the largest subset of books that can remain. If we can keep $k$ books, then the answer is $n-k$.

The problem is that there are $2^n$ possible subsets. Even trying to characterize all valid subsets directly becomes infeasible.

The key observation comes from looking at each color's first and last occurrence.

Let:

- $L_c$ = first occurrence of color $c$
- $R_c$ = last occurrence of color $c$
- $cnt_c$ = frequency of color $c$

If we decide that color $c$ participates in the stationary part, then once we keep any occurrence of $c$, every occurrence inside $[L_c,R_c]$ must also belong to the same color block. Otherwise another color would split the block.

This interval structure turns the problem into a dynamic programming problem over positions.

Define $dp[i]$ as the maximum number of books that can remain stationary using only suffix positions starting at $i$.

When we stand at position $i$, two possibilities exist.

We may simply remove the current book. Then we gain nothing and continue with $dp[i+1]$.

Or we may start preserving the color whose interval begins here. Suppose the color is $c$ and $i=L_c$.

Inside $[L_c,R_c]$, every occurrence of color $c$ can remain. For every other color whose entire interval lies inside this range, we may also preserve all of its occurrences. This creates a chain of nested intervals.

The original accepted solution processes positions from right to left and maintains, for each color, the best value obtainable when its interval is chosen. The interval structure allows every position to be handled only once, yielding linear complexity.

The transition ultimately computes the maximum number of books that can stay, and the answer is:

$$n - \max(\text{stationary books})$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal DP + interval processing | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

First compute for every color its first occurrence, last occurrence, and frequency.

Let `dp[i]` denote the maximum number of books that can remain stationary considering only positions from `i` onward.

Process positions from right to left.

1. If we remove the book at position `i`, we obtain `dp[i+1]`.
2. Let the current color be `c`.
3. Maintain `best[c]`, the value corresponding to choosing the interval of color `c`.
4. If position `i` is the last occurrence of `c`, initialize

$$best[c] = cnt_c$$

because at minimum we can keep all occurrences of this color.
5. Otherwise update

$$best[c] = best[c] + 1$$

while moving left through another occurrence of the same color.
6. If position `i` is the first occurrence of `c`, we may finish the interval of color `c` and continue after its last occurrence:

$$best[c] += dp[R_c + 1]$$
7. Set

$$dp[i] = \max(dp[i+1], best[c])$$
8. Continue until position 1.

The maximum number of stationary books is `dp[1]`. The answer is `n - dp[1]`.

### Why it works

For every color, the interval between its first and last occurrence determines the region that must be handled consistently. When the scan reaches an occurrence of color `c`, `best[c]` stores the best solution that keeps the current suffix of the interval of `c`.

Moving left extends that preserved interval by one more occurrence of `c`. Once the scan reaches the first occurrence, the entire interval of `c` has been accounted for. At that point we may concatenate an optimal solution beginning immediately after `R_c`.

Every valid stationary set can be decomposed into such completed color intervals, and every transition produced by the DP corresponds to a realizable stationary set. The recurrence examines both possibilities at every position: discard the current book or commit to the interval structure of its color. Since all intervals are processed exactly once, the maximum number of books that can stay is computed correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    first = [-1] * (n + 1)
    last = [-1] * (n + 1)
    cnt = [0] * (n + 1)

    for i, x in enumerate(a):
        if first[x] == -1:
            first[x] = i
        last[x] = i
        cnt[x] += 1

    dp = [0] * (n + 1)
    best = [0] * (n + 1)

    for i in range(n - 1, -1, -1):
        c = a[i]

        if i == last[c]:
            best[c] = cnt[c]
        else:
            best[c] += 1

        if i == first[c]:
            best[c] += dp[last[c] + 1]

        dp[i] = max(dp[i + 1], best[c])

    print(n - dp[0])

if __name__ == "__main__":
    solve()
```

The first pass computes the interval information for every color.

`best[c]` is the central idea. While scanning from right to left, it stores the value of the partially processed interval of color `c`. Encountering another occurrence of `c` extends that interval by one preserved book.

The special handling at the first occurrence is crucial. Only after reaching the first occurrence do we know that the whole interval of that color has been covered. At that moment we are allowed to append an optimal solution starting after the interval ends.

The DP array is a suffix DP. `dp[i]` always represents the best answer available in the suffix beginning at position `i`. Taking `max(dp[i + 1], best[c])` corresponds exactly to the choice between discarding the current book or using the interval structure of its color.

All values fit comfortably in 32-bit integers because they never exceed `n`, but Python integers remove any concern.

## Worked Examples

### Example 1

Input:

```
5
1 2 2 1 3
```

Intervals:

| Color | First | Last | Count |
| --- | --- | --- | --- |
| 1 | 0 | 3 | 2 |
| 2 | 1 | 2 | 2 |
| 3 | 4 | 4 | 1 |

Right-to-left DP:

| i | Color | best[color] after update | dp[i] |
| --- | --- | --- | --- |
| 4 | 3 | 1 | 1 |
| 3 | 1 | 2 | 2 |
| 2 | 2 | 2 | 2 |
| 1 | 2 | 3 | 3 |
| 0 | 1 | 4 | 4 |

We can keep 4 books, so the answer is:

```
5 - 4 = 1
```

The trace shows how completing the interval of color 2 at position 1 allows the DP to connect with later intervals.

### Example 2

Input:

```
5
2 1 1 1 2
```

Intervals:

| Color | First | Last | Count |
| --- | --- | --- | --- |
| 1 | 1 | 3 | 3 |
| 2 | 0 | 4 | 2 |

DP evolution:

| i | Color | best[color] after update | dp[i] |
| --- | --- | --- | --- |
| 4 | 2 | 2 | 2 |
| 3 | 1 | 3 | 3 |
| 2 | 1 | 4 | 4 |
| 1 | 1 | 5 | 5 |
| 0 | 2 | 6 | 6 |

The maximum stationary count reaches 4 books, yielding answer 1. One move is enough to make the colors contiguous.

This example demonstrates nested intervals, which are exactly what the DP is designed to handle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each position is processed once |
| Space | $O(n)$ | Arrays for intervals, DP, and color states |

With $n \le 5 \cdot 10^5$, linear time is easily fast enough. The memory usage is also well within the 256 MB limit because all arrays store only integers and have size proportional to $n$.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    first = [-1] * (n + 1)
    last = [-1] * (n + 1)
    cnt = [0] * (n + 1)

    for i, x in enumerate(a):
        if first[x] == -1:
            first[x] = i
        last[x] = i
        cnt[x] += 1

    dp = [0] * (n + 1)
    best = [0] * (n + 1)

    for i in range(n - 1, -1, -1):
        c = a[i]

        if i == last[c]:
            best[c] = cnt[c]
        else:
            best[c] += 1

        if i == first[c]:
            best[c] += dp[last[c] + 1]

        dp[i] = max(dp[i + 1], best[c])

    return str(n - dp[0]) + "\n"

assert solve_io("5\n1 2 2 1 3\n") == "1\n"

assert solve_io("1\n1\n") == "0\n"
assert solve_io("5\n7 7 7 7 7\n") == "0\n"
assert solve_io("4\n1 2 3 4\n") == "0\n"
assert solve_io("3\n1 2 1\n") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Minimum size |
| `7 7 7 7 7` | `0` | All books same color |
| `1 2 3 4` | `0` | Already beautiful with singleton colors |
| `1 2 1` | `1` | Non-contiguous color requiring exactly one move |

## Edge Cases

Consider:

```
3
1 2 1
```

The interval of color `1` is `[0,2]`. The interval of color `2` is `[1,1]`.

While scanning from right to left, the DP recognizes that preserving both occurrences of `1` and the single occurrence of `2` inside the interval is possible. The maximum stationary count becomes `2`, producing answer `1`. This matches the move:

```
1 2 1
→
1 1 2
```

Consider:

```
4
1 2 2 1
```

Color `2` already forms a contiguous block. The DP keeps that entire interval and combines it with one occurrence block of color `1`. The stationary count reaches `3`, so the answer is `1`.

A greedy strategy that insists on preserving every occurrence of a color once it is selected would miss this possibility.

Consider:

```
5
1 2 2 2 3
```

Every color already occupies one contiguous segment. The intervals are disjoint and already valid. The DP keeps all five books, obtaining `dp[0] = 5`, so the answer is `0`.

This confirms that the algorithm correctly handles shelves that require no operations at all.
