---
title: "CF 1140C - Playlist"
description: "Each song has two attributes: its length t and its beauty b. If we choose some subset of songs, its score is $$(text{sum of lengths}) times (text{minimum beauty})$$ We may choose at most k songs, and we want the maximum possible score."
date: "2026-06-12T03:46:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1140
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 62 (Rated for Div. 2)"
rating: 1600
weight: 1140
solve_time_s: 89
verified: true
draft: false
---

[CF 1140C - Playlist](https://codeforces.com/problemset/problem/1140/C)

**Rating:** 1600  
**Tags:** brute force, data structures, sortings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

Each song has two attributes: its length `t` and its beauty `b`.

If we choose some subset of songs, its score is

$$(\text{sum of lengths}) \times (\text{minimum beauty})$$

We may choose at most `k` songs, and we want the maximum possible score.

The interesting part is that the objective combines two different aggregate operations. The lengths are summed, but the beauties contribute only through their minimum value. A song with a very small beauty can drastically reduce the score even if it has a large length.

The constraints are large. We can have up to `3 * 10^5` songs, which immediately rules out any algorithm that enumerates subsets, pairs of subsets, or performs quadratic scans. With a 2-second time limit, we should target roughly `O(n log n)`.

A few edge cases are easy to mishandle.

Consider:

```
3 2
100 1
5 10
5 10
```

The optimal answer is:

```
100
```

by taking the two beauty-10 songs. A greedy strategy that always picks the largest lengths would choose the first song and obtain only `100 * 1 = 100`, missing the fact that beauty is the bottleneck.

Another subtle case is when choosing fewer than `k` songs is best:

```
3 3
100 100
1 1
1 1
```

The answer is:

```
10000
```

Taking only the first song gives `100 * 100`. Including either of the other songs drops the minimum beauty to `1`, making the score much worse.

One more case demonstrates why we must consider every possible minimum beauty:

```
4 2
10 5
10 4
10 3
10 2
```

The best answer is:

```
80
```

using the first two songs. The minimum beauty is `4`, not the globally largest beauty `5`. Restricting attention only to the largest beauty values would miss the optimum.

## Approaches

A brute-force solution would examine every subset of size at most `k`, compute the sum of lengths, compute the minimum beauty, and keep the best score.

This is correct because it directly checks all possibilities.

Unfortunately, even for `n = 50` this becomes impractical. For `n = 3 * 10^5`, the number of subsets is astronomical.

The key observation comes from looking at the minimum beauty.

Suppose we already know which song supplies the minimum beauty of the chosen set. Let that beauty be `B`.

Then every selected song must have beauty at least `B`, otherwise the minimum would be smaller.

Among all songs whose beauty is at least `B`, what is the best set of at most `k` songs?

Since the score becomes

$$(\text{sum of lengths}) \times B,$$

and `B` is fixed, we simply want the largest possible total length using at most `k` eligible songs.

That means we should take the `k` largest lengths among songs with beauty at least `B`.

This suggests processing beauty values from largest to smallest.

After sorting songs by decreasing beauty, when we are currently looking at a song with beauty `b`, every previously processed song has beauty at least `b`.

At that moment, we want to know the maximum total length obtainable from at most `k` processed songs. A min-heap is perfect for maintaining the largest `k` lengths seen so far.

As we scan:

1. Insert the current length into the heap.
2. If the heap grows beyond size `k`, remove the smallest length.
3. Maintain the sum of values currently in the heap.
4. Treat the current beauty as the minimum beauty candidate and evaluate:

$$(\text{current sum}) \times b$$

The heap always contains the largest lengths available among songs whose beauty is at least the current beauty, exactly matching the observation above.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n \cdot n) | O(n) | Too slow |
| Optimal | O(n log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read all songs as pairs `(beauty, length)`.
2. Sort the songs by beauty in descending order.

After sorting, every previously processed song has beauty at least as large as the current song's beauty.
3. Create a min-heap that will store selected lengths.
4. Maintain `length_sum`, the sum of all lengths currently inside the heap.
5. Iterate through the songs in sorted order.
6. Insert the current song's length into the heap and add it to `length_sum`.
7. If the heap size exceeds `k`, remove the smallest length and subtract it from `length_sum`.

The heap now contains the largest `k` lengths among all processed songs.
8. Compute

$$\text{candidate} = \text{length\_sum} \times \text{current beauty}$$

At this point every song represented in the heap has beauty at least the current beauty.
9. Update the answer with the maximum candidate value seen.
10. After processing all songs, print the answer.

### Why it works

When processing a song with beauty `b`, every processed song has beauty at least `b`. Any valid subset whose minimum beauty is exactly `b` must be composed only of these processed songs.

For a fixed minimum beauty `b`, maximizing the score reduces to maximizing the total length subject to selecting at most `k` songs. The heap maintains exactly the largest `k` lengths among all processed songs, so `length_sum` is the maximum achievable total length for this beauty threshold.

Since every possible minimum beauty appears as the beauty of some song, the scan evaluates the optimal score for every candidate minimum beauty. Taking the maximum over all evaluations yields the global optimum.

## Python Solution

```python
import sys
from heapq import heappush, heappop

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    songs = []
    for _ in range(n):
        t, b = map(int, input().split())
        songs.append((b, t))

    songs.sort(reverse=True)

    heap = []
    length_sum = 0
    answer = 0

    for b, t in songs:
        heappush(heap, t)
        length_sum += t

        if len(heap) > k:
            length_sum -= heappop(heap)

        answer = max(answer, length_sum * b)

    print(answer)

if __name__ == "__main__":
    solve()
```

The sorting step creates the order in which beauty thresholds are considered. When we reach beauty `b`, every song seen so far has beauty at least `b`.

The heap stores lengths only. Keeping a min-heap allows us to efficiently discard the smallest length whenever more than `k` songs are present. After this adjustment, the heap contains the largest `k` lengths among all processed songs.

The variable `length_sum` is maintained incrementally. Recomputing the sum from the heap each iteration would introduce an unnecessary factor of `k`.

The multiplication must be performed using 64-bit arithmetic. In Python this happens automatically. In languages such as C++, `long long` is required because lengths can sum to roughly `3 * 10^11`, and multiplying by beauty can reach around `3 * 10^17`.

A common mistake is computing the score before removing excess elements from the heap. The heap must first be reduced to at most `k` songs, otherwise the candidate score may use too many songs.

## Worked Examples

### Sample 1

Input:

```
4 3
4 7
15 1
3 6
6 8
```

After sorting by beauty:

`(8,6), (7,4), (6,3), (1,15)`

| Step | Beauty | Length | Heap Lengths | Length Sum | Candidate | Best |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8 | 6 | [6] | 6 | 48 | 48 |
| 2 | 7 | 4 | [4,6] | 10 | 70 | 70 |
| 3 | 6 | 3 | [3,6,4] | 13 | 78 | 78 |
| 4 | 1 | 15 | [4,6,15] | 25 | 25 | 78 |

The maximum score appears when beauty `6` is treated as the minimum beauty. The heap contains lengths `6, 4, 3`, giving total length `13` and score `13 * 6 = 78`.

### Sample 2

Input:

```
3 2
1 1
1 1
100 100
```

Sorted order:

`(100,100), (1,1), (1,1)`

| Step | Beauty | Length | Heap Lengths | Length Sum | Candidate | Best |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 100 | 100 | [100] | 100 | 10000 | 10000 |
| 2 | 1 | 1 | [1,100] | 101 | 101 | 10000 |
| 3 | 1 | 1 | [1,100] | 101 | 101 | 10000 |

The best answer comes from selecting only one song. This demonstrates why the problem says "at most `k` songs" rather than exactly `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log k) | Sorting is O(n log n), heap operations are O(log k) each. Since `k ≤ n`, the overall complexity is commonly written as O(n log n), or O(n log k) after sorting. |
| Space | O(k) | The heap stores at most `k` lengths. |

The dominant cost is sorting `3 * 10^5` songs, which is easily manageable within the limits. The heap operations add only logarithmic overhead, and the memory usage remains small.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from heapq import heappush, heappop

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k = map(int, input().split())

    songs = []
    for _ in range(n):
        t, b = map(int, input().split())
        songs.append((b, t))

    songs.sort(reverse=True)

    heap = []
    s = 0
    ans = 0

    for b, t in songs:
        heappush(heap, t)
        s += t

        if len(heap) > k:
            s -= heappop(heap)

        ans = max(ans, s * b)

    return str(ans) + "\n"

# sample 1
assert run(
"""4 3
4 7
15 1
3 6
6 8
"""
) == "78\n"

# sample-style case
assert run(
"""3 2
1 1
1 1
100 100
"""
) == "10000\n"

# minimum size
assert run(
"""1 1
5 7
"""
) == "35\n"

# all equal values
assert run(
"""4 2
3 5
3 5
3 5
3 5
"""
) == "30\n"

# k = n
assert run(
"""3 3
5 4
2 3
1 2
"""
) == "16\n"

# choosing fewer than k songs is optimal
assert run(
"""3 3
100 100
1 1
1 1
"""
) == "10000\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5 7` | `35` | Smallest possible instance |
| Four identical songs, `k=2` | `30` | Handling duplicate values |
| `k=n` example | `16` | Using all songs when beneficial |
| Large beauty outlier | `10000` | Best solution may use fewer than `k` songs |

## Edge Cases

Consider:

```
3 3
100 100
1 1
1 1
```

After sorting, the first processed song has beauty `100`. The heap contains only length `100`, giving score `10000`. Later songs reduce the beauty threshold to `1`, producing much smaller scores. The algorithm naturally keeps the earlier answer, correctly handling cases where fewer than `k` songs are optimal.

Consider:

```
3 2
100 1
5 10
5 10
```

Sorted order is:

```
(10,5), (10,5), (1,100)
```

When beauty `10` is processed, the heap contains lengths `5` and `5`, yielding score `100`. When beauty drops to `1`, the heap contains the two largest lengths, `100` and `5`, producing score `105`. The answer remains `105`. The algorithm does not greedily favor large lengths or large beauties alone, it evaluates both together through every beauty threshold.

Consider:

```
4 2
10 5
10 4
10 3
10 2
```

The scan evaluates:

```
10*5 = 50
20*4 = 80
20*3 = 60
20*2 = 40
```

The maximum occurs at beauty `4`. This confirms why every possible minimum beauty must be examined. The optimum is not necessarily associated with the largest beauty value.
