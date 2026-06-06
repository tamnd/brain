---
title: "CF 268E - Playlist"
description: "Each song has two attributes. Its length is l, and independently Manao likes it with probability p. When a song is played for the first time, one of two things happens. If he likes it, the song is added to a collection of remembered songs."
date: "2026-06-05T01:10:50+07:00"
tags: ["codeforces", "competitive-programming", "math", "probabilities", "sortings"]
categories: ["algorithms"]
codeforces_contest: 268
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 164 (Div. 2)"
rating: 2100
weight: 268
solve_time_s: 160
verified: true
draft: false
---

[CF 268E - Playlist](https://codeforces.com/problemset/problem/268/E)

**Rating:** 2100  
**Tags:** math, probabilities, sortings  
**Solve time:** 2m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

Each song has two attributes. Its length is `l`, and independently Manao likes it with probability `p`.

When a song is played for the first time, one of two things happens.

If he likes it, the song is added to a collection of remembered songs.

If he dislikes it, he immediately replays every remembered song once.

The remembered songs are exactly the songs that were liked among all songs processed earlier. Once a song is liked, it stays liked forever.

We may arrange the songs in any order. Among all permutations, we must maximize the expected total listening time.

The input contains up to 50,000 songs. A quadratic algorithm would require roughly 2.5 billion pair interactions, which is far beyond the limit. The solution must be close to `O(n log n)`.

The main difficulty is that the contribution of a song depends on which songs appear before it. A song can be replayed many times because of future disliked songs, so local greedy choices are not immediately obvious.

Several edge cases are easy to mishandle.

Consider a song that is never liked:

```
1
100 0
```

The expected listening time is exactly `100`. There are no remembered songs, so no replays occur. Any formula that blindly multiplies by probabilities without handling `p = 0` correctly can produce wrong extra contributions.

Consider a song that is always liked:

```
1
100 100
```

The answer is also `100`. The song is played once and never replayed because there are no later songs. Some derivations accidentally count self-interactions and obtain a larger value.

Another subtle case is when one probability is zero:

```
2
100 100
200 0
```

If the first song is placed before the second, the total listening time is

```
100 + 200 + 100 = 400
```

because the second song is certainly disliked and triggers a replay of the first song.

If the order is reversed, the total is only

```
200 + 100 = 300
```

So the ordering matters even when one probability is deterministic.

## Approaches

A brute-force solution would try every permutation of songs, compute its expected listening time, and keep the maximum.

For a fixed permutation, expectation can be computed from probability formulas. Unfortunately there are `n!` permutations. Even for `n = 15` this is already hopeless, while the actual limit is `50,000`.

The key observation is that expectation is linear. Instead of thinking about complete executions, we can compute the expected contribution of each interaction between pairs of songs.

Suppose song `i` appears before song `j`.

Song `i` is replayed when song `j` is disliked, but only if song `i` was liked earlier.

The probability of that event is

$$P(i\text{ liked}) \cdot P(j\text{ disliked})$$

which equals

$$\frac{p_i}{100}\left(1-\frac{p_j}{100}\right).$$

Whenever it happens, an additional `l_i` seconds are listened to.

So every ordered pair `(i,j)` with `i` before `j` contributes

$$l_i \cdot \frac{p_i}{100}\left(1-\frac{p_j}{100}\right)$$

to the expectation.

The expected duration of the first play of every song is always counted exactly once, regardless of order:

$$\sum l_i.$$

Thus the optimization problem becomes:

$$\sum l_i + \sum_{i<j} l_i \cdot \frac{p_i}{100} \left(1-\frac{p_j}{100}\right).$$

The constant term does not depend on the permutation. Only the pairwise term matters.

Whenever an objective can be written as a sum of pairwise contributions, an exchange argument is often the right tool. We compare two adjacent songs and determine which order is better. This produces a sorting criterion and reduces the problem to sorting once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n! · n)` | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

### Deriving the ordering rule

Consider two songs `A` and `B`.

Let

$$a=l_A,\quad x=\frac{p_A}{100}$$

and

$$b=l_B,\quad y=\frac{p_B}{100}.$$

Only their mutual interaction changes when we swap them.

If `A` comes before `B`, the pair contributes

$$a x (1-y).$$

If `B` comes before `A`, the pair contributes

$$b y (1-x).$$

We want `A` before `B` when

$$a x (1-y) > b y (1-x).$$

Multiplying by `100^2` to avoid fractions gives

$$a p_A (100-p_B) > b p_B (100-p_A).$$

This is a complete comparison rule between two songs.

### Steps

1. Read all songs.
2. Sort songs using the comparator

$$l_i p_i (100-p_j) > l_j p_j (100-p_i).$$

If this inequality holds, song `i` must appear before song `j`.

1. After sorting, compute the expectation.
2. Maintain

$$S=\sum_{\text{processed}} l_i \cdot \frac{p_i}{100}.$$

`S` represents the expected total length of remembered songs after all previously processed songs.

1. Process songs from left to right.
2. Add the song's own first play, namely `l_i`, to the answer.
3. The current song is disliked with probability

$$1-\frac{p_i}{100}.$$

If that happens, all remembered songs are replayed. Their expected total length is exactly `S`.

Add

$$S\left(1-\frac{p_i}{100}\right)$$

to the answer.

1. Update

$$S \leftarrow S + l_i\frac{p_i}{100}.$$

1. Output the final expectation.

### Why it works

The pairwise objective is additive. For any two neighboring songs, the contribution difference between the two possible orders depends only on those two songs:

$$a p_A (100-p_B) - b p_B (100-p_A).$$

Whenever this value is positive, placing `A` before `B` increases the expectation. This defines a valid pairwise ordering relation. Sorting according to that relation guarantees that every adjacent inversion has been removed. By the standard exchange argument, no further swap can improve the arrangement, so the resulting permutation is optimal.

The expectation computation is also correct because linearity of expectation allows us to replace the random set of remembered songs by its expected total length `S`. Each song independently contributes `l_i p_i/100` to that expected remembered length.

## Python Solution

```python
import sys
from functools import cmp_to_key

input = sys.stdin.readline

def solve():
    n = int(input())
    songs = []

    for _ in range(n):
        l, p = map(int, input().split())
        songs.append((l, p))

    def cmp(a, b):
        l1, p1 = a
        l2, p2 = b

        left = l1 * p1 * (100 - p2)
        right = l2 * p2 * (100 - p1)

        if left > right:
            return -1
        if left < right:
            return 1
        return 0

    songs.sort(key=cmp_to_key(cmp))

    ans = 0.0
    remembered = 0.0

    for l, p in songs:
        prob = p / 100.0

        ans += l
        ans += remembered * (1.0 - prob)

        remembered += l * prob

    print("{:.12f}".format(ans))

if __name__ == "__main__":
    solve()
```

The comparator is the heart of the solution. It comes directly from comparing the two possible orders of a pair of songs. Using cross multiplication avoids floating-point precision issues during sorting.

The variable `remembered` stores the expected total length of songs already remembered. It is not the actual random length during one execution. By linearity of expectation, tracking only the expected value is sufficient.

The answer is accumulated incrementally. Every song contributes its own initial playback length. Then, with probability `1 - p/100`, it causes all remembered songs to be replayed. The expected length of those songs is exactly `remembered`.

All arithmetic inside the comparator uses integers. The largest value is approximately

$$1000 \cdot 100 \cdot 100 = 10^7,$$

which is tiny compared to Python's integer range.

## Worked Examples

### Sample 1

Input:

```
3
150 20
150 50
100 50
```

The comparator orders the songs as:

```
(150,50), (100,50), (150,20)
```

| Step | Song `(l,p)` | remembered before | Added replay expectation | Answer after |
| --- | --- | --- | --- | --- |
| 1 | (150,50) | 0 | 0 | 150 |
| 2 | (100,50) | 75 | 37.5 | 287.5 |
| 3 | (150,20) | 125 | 100 | 537.5 |

Final answer:

```
537.500000000
```

This trace shows how `remembered` represents the expected remembered length. After the first song it equals `150 × 0.5 = 75`. After the second song it becomes `125`.

### Custom Example

Input:

```
2
100 100
200 0
```

Optimal order is already shown by the comparator.

| Step | Song `(l,p)` | remembered before | Added replay expectation | Answer after |
| --- | --- | --- | --- | --- |
| 1 | (100,100) | 0 | 0 | 100 |
| 2 | (200,0) | 100 | 100 | 400 |

Final answer:

```
400.000000000
```

This example demonstrates why high-probability songs tend to move earlier. A certain dislike later in the playlist repeatedly triggers the remembered songs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting dominates the running time |
| Space | `O(n)` | Storage of all songs |

With `n = 50,000`, an `O(n log n)` sort performs roughly a few hundred thousand comparisons, which comfortably fits within the time limit. Memory usage is also small.

## Test Cases

```python
import sys
import io
from functools import cmp_to_key

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    songs = [tuple(map(int, input().split())) for _ in range(n)]

    def cmp(a, b):
        l1, p1 = a
        l2, p2 = b

        x = l1 * p1 * (100 - p2)
        y = l2 * p2 * (100 - p1)

        if x > y:
            return -1
        if x < y:
            return 1
        return 0

    songs.sort(key=cmp_to_key(cmp))

    ans = 0.0
    remembered = 0.0

    for l, p in songs:
        prob = p / 100.0
        ans += l
        ans += remembered * (1.0 - prob)
        remembered += l * prob

    return f"{ans:.12f}"

# provided sample
assert run(
"""3
150 20
150 50
100 50
"""
) == "537.500000000000", "sample 1"

# minimum size
assert run(
"""1
100 0
"""
) == "100.000000000000", "single song, never liked"

# always liked then always disliked
assert run(
"""2
100 100
200 0
"""
) == "400.000000000000", "replay triggered once"

# all probabilities zero
assert run(
"""3
50 0
60 0
70 0
"""
) == "180.000000000000", "no remembered songs ever"

# all probabilities one hundred
assert run(
"""3
50 100
60 100
70 100
"""
) == "180.000000000000", "no replay events"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One song, probability 0 | 100 | Base case |
| `(100,100)` and `(200,0)` | 400 | Ordering effect |
| All probabilities 0 | Sum of lengths | No remembered songs |
| All probabilities 100 | Sum of lengths | No dislikes occur |

## Edge Cases

### Song never liked

Input:

```
1
100 0
```

The sorted order is unchanged. Initially `remembered = 0`.

The song contributes `100` for its first play. Since `remembered` is zero, the replay term is also zero. The answer is exactly `100`.

### Song always liked

Input:

```
1
100 100
```

The song contributes `100`. The replay probability is zero, so nothing extra is added. Afterwards `remembered` becomes `100`, but there are no later songs. The result remains `100`.

### Deterministic dislike after deterministic like

Input:

```
2
100 100
200 0
```

The comparator prefers the first song before the second because

$$100 \cdot 100 \cdot 100 > 200 \cdot 0 \cdot 0.$$

After processing the first song, `remembered = 100`.

The second song is certainly disliked, so its replay contribution is exactly `100`.

The final answer is

$$100 + 200 + 100 = 400.$$

This confirms that the algorithm correctly handles probabilities at both extremes and correctly exploits replay opportunities through the sorting rule.
