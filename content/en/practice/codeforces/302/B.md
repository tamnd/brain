---
title: "CF 302B - Eugeny and Play List"
description: "Eugeny has a playlist made of several songs. Song i lasts t[i] minutes, and he repeats that same song c[i] times before moving to the next one. The playlist order never changes."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 302
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 182 (Div. 2)"
rating: 1200
weight: 302
solve_time_s: 118
verified: true
draft: false
---

[CF 302B - Eugeny and Play List](https://codeforces.com/problemset/problem/302/B)

**Rating:** 1200  
**Tags:** binary search, implementation, two pointers  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

Eugeny has a playlist made of several songs. Song `i` lasts `t[i]` minutes, and he repeats that same song `c[i]` times before moving to the next one. The playlist order never changes.

If a song has duration 4 and is repeated 3 times, that song occupies 12 consecutive minutes in the global timeline of the playlist. After all songs are expanded this way, Eugeny writes down several moments in time, and for each moment we must determine which song was playing during that minute.

The core difficulty is that the playlist can become extremely large if we expand every repeated song explicitly. A song may repeat up to `10^9` times, and each repeat may last up to `10^9` minutes. Even though the total playlist duration is capped at `10^9`, explicitly constructing a minute-by-minute array would still be far too expensive.

The number of songs and queries can both reach `10^5`. That immediately rules out any solution that scans all songs for every query, because `10^5 × 10^5 = 10^10` operations, far beyond what fits into a 2 second limit. We need something closer to `O(n log n)` or `O((n + m) log n)`.

A subtle detail is that the queries ask for the song playing during the `x`-th minute, using 1-based indexing. Off-by-one mistakes are common here. For example:

```
1 3
2 5
1 5 10
```

The song occupies minutes `[1, 10]`, not `[0, 9]`. Every query should return song `1`.

Another easy mistake appears at segment boundaries. Consider:

```
2 3
1 2
1 3
2 3 5
```

Song 1 occupies minutes `[1, 2]`.

Song 2 occupies minutes `[3, 5]`.

Correct answers:

```
1
2
2
```

A careless binary search that uses `<` instead of `<=` may incorrectly assign minute `2` to song `2`.

Large values also matter. Suppose:

```
1 1
1000000000 1000000000
1000000000
```

The cumulative durations can become very large, so the implementation must avoid fixed-width integer overflow in languages like C++. Python handles this naturally, but the editorial logic should still treat cumulative sums carefully.

## Approaches

The brute-force idea is straightforward. We can build the full expanded playlist minute by minute. For each song, repeat its index `c[i] * t[i]` times in an array. Then every query becomes a direct lookup.

This works because the playlist timeline is linear and every minute belongs to exactly one song. If the playlist were small, direct expansion would be simple and correct.

The problem is scale. The total duration can reach `10^9` minutes. Constructing an array of one billion elements already exceeds reasonable memory limits, and iterating through it would also be too slow.

The next idea is to avoid storing every minute separately. Each song occupies one continuous interval on the global timeline.

Suppose we compute cumulative ending times:

```
Song 1 ends at minute 10
Song 2 ends at minute 25
Song 3 ends at minute 40
```

Now consider query minute `17`. We want the first cumulative ending time that is at least `17`. That song must contain minute `17`.

This transforms the problem into repeated searches on a sorted array. Since cumulative end times are strictly increasing, binary search becomes the natural tool.

The observation that each song corresponds to one continuous interval lets us compress potentially billions of minutes into only `n` prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total duration + m) | O(total duration) | Too slow |
| Optimal | O(n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all songs and queries.
2. For every song, compute how many total minutes it contributes.

The contribution is `c[i] * t[i]` because the song lasts `t[i]` minutes and is repeated `c[i]` times.
3. Build a prefix sum array of cumulative ending times.

If the first song contributes 10 minutes and the second contributes 15 minutes, the prefix array becomes:

```
[10, 25]
```

This means:

Song 1 occupies minutes `[1, 10]`

Song 2 occupies minutes `[11, 25]`
4. For each query minute `x`, binary search the prefix array for the first value greater than or equal to `x`.

That index corresponds to the song playing during minute `x`.
5. Output the song index using 1-based numbering.

### Why it works

The prefix array partitions the entire playlist timeline into consecutive ranges.

If `prefix[i]` is the ending minute of song `i`, then song `i` occupies:

```
(prefix[i-1] + 1) to prefix[i]
```

For a query minute `x`, the first prefix value satisfying:

```
prefix[i] >= x
```

must be the segment containing `x`. Any earlier song ends before `x`, and any later song starts after `x`.

Binary search correctly finds this boundary because the prefix sums are strictly increasing.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    prefix = []
    total = 0

    for _ in range(n):
        c, t = map(int, input().split())
        total += c * t
        prefix.append(total)

    queries = list(map(int, input().split()))

    ans = []

    for x in queries:
        idx = bisect_left(prefix, x)
        ans.append(str(idx + 1))

    sys.stdout.write("\n".join(ans))

solve()
```

The solution starts by constructing cumulative ending times for every song. The variable `total` tracks the total number of minutes processed so far.

For each song, the contribution is `c * t`. After adding that contribution, we append the new cumulative total to `prefix`.

The `prefix` array stays sorted because every contribution is positive. That property is what makes binary search possible.

The query handling uses `bisect_left`. This function returns the first index where `x` could be inserted while preserving sorted order. In other words, it finds the first position where:

```
prefix[idx] >= x
```

That exactly matches the song interval containing minute `x`.

The `+1` during output converts the zero-based Python index into the one-based song numbering required by the problem.

One subtle detail is boundary handling. If a query equals a cumulative ending time exactly, the answer should still be the current song, not the next one. `bisect_left` handles this correctly because it returns the leftmost valid position.

## Worked Examples

### Example 1

Input:

```
1 2
2 8
1 16
```

The single song lasts 8 minutes and repeats twice.

| Song | c | t | Contribution | Prefix Total |
| --- | --- | --- | --- | --- |
| 1 | 2 | 8 | 16 | 16 |

Queries:

| Query Minute | First Prefix ≥ Query | Song |
| --- | --- | --- |
| 1 | 16 | 1 |
| 16 | 16 | 1 |

Output:

```
1
1
```

This example confirms that exact boundary values belong to the same song interval.

### Example 2

Input:

```
3 5
1 3
2 2
1 4
1 3 4 7 11
```

The playlist structure becomes:

Song 1: 3 minutes

Song 2: 4 minutes

Song 3: 4 minutes

Cumulative endings:

| Song | Contribution | Prefix Total |
| --- | --- | --- |
| 1 | 3 | 3 |
| 2 | 4 | 7 |
| 3 | 4 | 11 |

Queries:

| Query Minute | First Prefix ≥ Query | Song |
| --- | --- | --- |
| 1 | 3 | 1 |
| 3 | 3 | 1 |
| 4 | 7 | 2 |
| 7 | 7 | 2 |
| 11 | 11 | 3 |

Output:

```
1
1
2
2
3
```

This trace demonstrates how the binary search transitions correctly at song boundaries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log n) | Building prefix sums is linear, each query uses binary search |
| Space | O(n) | The prefix array stores one value per song |

With `n, m ≤ 10^5`, this complexity easily fits the limits. Around `10^5` binary searches on a `10^5` sized array is well within acceptable runtime in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    prefix = []
    total = 0

    for _ in range(n):
        c, t = map(int, input().split())
        total += c * t
        prefix.append(total)

    queries = list(map(int, input().split()))

    ans = []

    for x in queries:
        ans.append(str(bisect_left(prefix, x) + 1))

    return "\n".join(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
    "1 2\n"
    "2 8\n"
    "1 16\n"
) == "1\n1", "sample 1"

# minimum size
assert run(
    "1 1\n"
    "1 1\n"
    "1\n"
) == "1", "minimum input"

# boundary transitions
assert run(
    "2 4\n"
    "1 2\n"
    "1 3\n"
    "1 2 3 5\n"
) == "1\n1\n2\n2", "boundary minutes"

# repeated long segment
assert run(
    "3 3\n"
    "2 2\n"
    "3 1\n"
    "1 5\n"
    "1 5 10\n"
) == "1\n2\n3", "multiple segments"

# large values
assert run(
    "1 2\n"
    "1000000000 1\n"
    "1 1000000000\n"
) == "1\n1", "large cumulative values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single song, single query | `1` | Minimum valid input |
| Queries on exact boundaries | `1 1 2 2` | Off-by-one correctness |
| Multiple song ranges | `1 2 3` | Correct interval transitions |
| Large repetition counts | `1 1` | Large cumulative sums |

## Edge Cases

Consider the boundary case where a query lands exactly at the final minute of a song.

Input:

```
2 2
1 2
1 3
2 3
```

The prefix array becomes:

```
[2, 5]
```

For query `2`, binary search finds the first prefix value greater than or equal to `2`, which is index `0`. The answer is song `1`.

For query `3`, binary search finds index `1`, which corresponds to song `2`.

Output:

```
1
2
```

This confirms that the algorithm handles segment endpoints correctly.

Now consider extremely large durations.

Input:

```
1 1
1000000000 1000000000
1000000000
```

The song contributes `10^18` total minutes. Python integers safely store this value, and the prefix array becomes:

```
[1000000000000000000]
```

The query minute `1000000000` still maps correctly to song `1`.

Finally, consider the smallest possible playlist.

Input:

```
1 1
1 1
1
```

The prefix array is `[1]`. Binary search immediately returns index `0`, so the output is:

```
1
```

This verifies that the implementation handles single-element arrays without special cases.
