---
title: "CF 302B - Eugeny and Play List"
description: "The playlist is built from blocks of repeated songs. Song i has duration t[i], and Eugeny listens to it c[i] times consecutively before moving to the next song. If a song lasts 4 minutes and is repeated 3 times, that block contributes 12 minutes to the playlist timeline."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 302
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 182 (Div. 2)"
rating: 1200
weight: 302
solve_time_s: 205
verified: true
draft: false
---

[CF 302B - Eugeny and Play List](https://codeforces.com/problemset/problem/302/B)

**Rating:** 1200  
**Tags:** binary search, implementation, two pointers  
**Solve time:** 3m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

The playlist is built from blocks of repeated songs. Song `i` has duration `t[i]`, and Eugeny listens to it `c[i]` times consecutively before moving to the next song.

If a song lasts 4 minutes and is repeated 3 times, that block contributes 12 minutes to the playlist timeline. Queries ask questions like:

“During the 57-th minute from the beginning of the playlist, which song was playing?”

The important detail is that we are not asked which repetition of the song was playing, only the song index itself.

The playlist can contain up to `10^5` song blocks and `10^5` queries. A direct minute-by-minute simulation is impossible because each `c[i] * t[i]` can be very large. The total playlist duration can reach `10^9`, which means building an explicit array of all minutes would require billions of elements.

With `10^5` queries under a 2 second limit, we should expect something around `O(n log n)` or `O(n + m)` to pass comfortably. Any solution that scans the entire playlist for every query would become too slow.

One subtle point is that queries are 1-indexed in terms of time. If a song occupies minutes `[1, 16]`, then query `16` still belongs to that song, while query `17` belongs to the next one. Off-by-one mistakes are very common here.

Consider this example:

```
2 3
1 3
1 2
1 3 4
```

The playlist timeline is:

```
minutes 1..3 -> song 1
minutes 4..5 -> song 2
```

Correct output:

```
1
1
2
```

A careless implementation using strict `<` instead of `<=` during binary search would incorrectly map minute `3` to song `2`.

Another tricky case happens when one song block is extremely large:

```
1 3
1000000000 1
1 500000000 1000000000
```

All queries must still return song `1`. This rules out any approach that expands the playlist minute by minute.

A final detail is that queries are already sorted increasingly. Some solutions exploit this with two pointers, but binary search on prefix sums is also fast enough and simpler to reason about.

## Approaches

The brute-force idea is straightforward. We could generate the full playlist timeline minute by minute and store which song plays at each minute.

For example:

```
song 1: duration 2, repeats 3 times
```

would contribute:

```
[1, 1, 1, 1, 1, 1]
```

because the song occupies 6 total minutes.

Then every query becomes a direct lookup.

This works logically because every minute is explicitly represented. The problem is the size. The total duration can reach `10^9`, so this array could contain one billion entries. Both memory and running time become impossible.

The next improvement is observing that each song occupies one continuous interval on the global timeline.

Suppose we compute cumulative durations:

```
song 1 ends at minute 10
song 2 ends at minute 25
song 3 ends at minute 40
```

Now a query `x` simply asks:

“What is the first song whose ending time is at least `x`?”

That is exactly a binary search problem.

The cumulative ending times are naturally sorted because every song adds a positive duration. For each query, we binary search the first prefix sum `>= x`.

This reduces the work dramatically:

Instead of scanning minutes individually, we store only one number per song block.

Instead of searching linearly for every query, we use binary search in `O(log n)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total duration + m) | O(total duration) | Too slow |
| Optimal | O(n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of song blocks `n` and the number of queries `m`.
2. Build an array of prefix sums.

For each song block, compute:

```
block_duration = c[i] * t[i]
```

Then append the cumulative total duration so far.

If the prefix sums become:

```
[10, 25, 40]
```

it means:

Song 1 occupies minutes `1..10`

Song 2 occupies minutes `11..25`

Song 3 occupies minutes `26..40`
3. Read every query minute `x`.
4. Binary search the prefix sum array for the first value greater than or equal to `x`.

This gives the song block containing minute `x`.
5. Output the song index as 1-based indexing.

### Why it works

The prefix sum array stores the ending minute of every song block. Since every block duration is positive, these ending times are strictly increasing.

For any query minute `x`, the correct song is exactly the first block whose ending time is at least `x`.

If the previous prefix sum is smaller than `x`, then all earlier songs ended before minute `x`. If the current prefix sum is at least `x`, then the current song has already started and has not ended yet.

Because binary search finds precisely this boundary, the algorithm always returns the correct song.

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

The core of the solution is the `prefix` array. Each entry stores the final minute occupied by that song block.

For example, if:

```
prefix = [6, 15, 21]
```

then:

```
song 1 -> minutes 1..6
song 2 -> minutes 7..15
song 3 -> minutes 16..21
```

`bisect_left(prefix, x)` returns the first index whose value is at least `x`. That is exactly the song containing minute `x`.

The `+1` is necessary because Python lists use 0-based indexing while song numbers are 1-based.

A common mistake is using `bisect_right`. That would fail for boundary minutes where a song ends exactly at `x`.

Another easy mistake is forgetting that the timeline starts from minute `1`, not minute `0`. Using cumulative ending times avoids this issue naturally.

Python integers safely handle the maximum possible totals here, so no special overflow handling is required.

## Worked Examples

### Example 1

Input:

```
1 2
2 8
1 16
```

The playlist contains one song repeated twice, each repetition lasting 8 minutes.

Total occupied interval:

```
minutes 1..16 -> song 1
```

Prefix sums:

| Song | c | t | Block Duration | Prefix Sum |
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

This example confirms that boundary minutes belong to the same song block.

### Example 2

Input:

```
3 5
1 2
2 3
1 4
1 2 5 8 12
```

Construct the timeline.

Song 1 contributes `1 * 2 = 2` minutes.

Song 2 contributes `2 * 3 = 6` minutes.

Song 3 contributes `1 * 4 = 4` minutes.

Prefix sums:

| Song | Block Duration | Prefix Sum |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | 6 | 8 |
| 3 | 4 | 12 |

Queries:

| Query Minute | Binary Search Result | Song |
| --- | --- | --- |
| 1 | 2 | 1 |
| 2 | 2 | 1 |
| 5 | 8 | 2 |
| 8 | 8 | 2 |
| 12 | 12 | 3 |

Output:

```
1
1
2
2
3
```

This trace shows how different query positions map into contiguous intervals defined by the prefix sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log n) | Building prefix sums is linear, each query uses binary search |
| Space | O(n) | The prefix sum array stores one value per song block |

With `n, m ≤ 10^5`, this easily fits within the limits. Around `10^5` binary searches on an array of size `10^5` is well within the allowed runtime in Python.

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

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run(
    "1 2\n"
    "2 8\n"
    "1 16\n"
) == "1\n1"

# minimum-size input
assert run(
    "1 1\n"
    "1 1\n"
    "1\n"
) == "1"

# boundary transition between songs
assert run(
    "2 4\n"
    "1 3\n"
    "1 2\n"
    "1 3 4 5\n"
) == "1\n1\n2\n2"

# all queries inside same large block
assert run(
    "1 3\n"
    "1000000000 1\n"
    "1 500000000 1000000000\n"
) == "1\n1\n1"

# mixed intervals
assert run(
    "3 5\n"
    "1 2\n"
    "2 3\n"
    "1 4\n"
    "1 2 5 8 12\n"
) == "1\n1\n2\n2\n3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single song with one query | `1` | Minimum valid input |
| Query exactly at song boundary | Correct transition | Off-by-one correctness |
| Huge repeated block | All `1` | No minute-by-minute expansion |
| Mixed intervals | `1 1 2 2 3` | General correctness |

## Edge Cases

Consider the boundary case where a query lands exactly on the final minute of a song block.

Input:

```
2 3
1 3
1 2
3 4 5
```

Prefix sums become:

```
[3, 5]
```

For query `3`, binary search finds the first prefix sum `>= 3`, which is index `0`. The algorithm correctly returns song `1`.

For query `4`, the first prefix sum `>= 4` is `5`, corresponding to song `2`.

Output:

```
1
2
2
```

This confirms that the intervals are handled inclusively on the right boundary.

Now consider a very large duration.

Input:

```
1 2
1000000000 1
1 1000000000
```

The prefix sum array contains only:

```
[1000000000]
```

Both queries binary search directly into this single interval and return song `1`.

The algorithm never constructs a billion-minute array, so it remains fast and memory efficient.

Finally, consider many tiny song blocks.

Input:

```
4 4
1 1
1 1
1 1
1 1
1 2 3 4
```

Prefix sums:

```
[1, 2, 3, 4]
```

Each query maps exactly to one distinct song.

Output:

```
1
2
3
4
```

This validates that consecutive boundaries are handled correctly without skipping or overlapping intervals.
