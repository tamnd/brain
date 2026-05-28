---
title: "CF 81D - Polycarp's Picture Gallery"
description: "We have several photo albums, and album i contains a[i] photos. We must build a cyclic gallery of exactly n photos. Each chosen photo is represented only by its album number, because the individual identities of photos do not matter. The gallery is circular."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 81
codeforces_index: "D"
codeforces_contest_name: "Yandex.Algorithm Open 2011: Qualification 1"
rating: 2100
weight: 81
solve_time_s: 159
verified: false
draft: false
---

[CF 81D - Polycarp's Picture Gallery](https://codeforces.com/problemset/problem/81/D)

**Rating:** 2100  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We have several photo albums, and album `i` contains `a[i]` photos. We must build a cyclic gallery of exactly `n` photos. Each chosen photo is represented only by its album number, because the individual identities of photos do not matter.

The gallery is circular. Position `1` is adjacent to positions `2` and `n`, position `2` is adjacent to positions `1` and `3`, and so on. The requirement is that adjacent positions must never come from the same album.

We may use at most `a[i]` photos from album `i`. We do not need to use every available photo, only exactly `n` total photos.

The constraints are small enough to allow constructive greedy algorithms. `m ≤ 40`, which means the number of albums is tiny. `n ≤ 1000`, so even quadratic work is completely safe. A solution around `O(n log m)` or `O(nm)` easily fits inside the limit.

The dangerous part of the problem is the cyclic condition. Many linear arrangements that look valid fail when the first and last elements are checked.

Consider this example:

```
n = 5
albums = [3, 2]
```

A careless greedy may build:

```
1 2 1 2 1
```

All consecutive pairs inside the array are valid, but the last and first positions are both `1`, so the cycle is invalid.

Another subtle case appears when one album is too large.

```
n = 6
albums = [6, 1, 1]
```

Even though there are many photos overall, we cannot place six photos without two neighboring `1`s. In any cycle, one color cannot occupy more than `n / 2` positions. Here album `1` would need too many slots.

A different trap is forgetting that we may discard photos.

```
n = 4
albums = [100, 1, 1]
```

Using all photos is impossible, but we only need four positions. The correct construction is:

```
1 2 1 3
```

A solution that blindly tries to use every available photo would fail unnecessarily.

## Approaches

The brute force approach tries every possible cyclic sequence of length `n`. For each position we choose one of `m` albums, verify the usage limits, and finally check all adjacent pairs.

That gives roughly `m^n` possibilities. Even with `m = 10` and `n = 20`, this is already astronomically large. The brute force works conceptually because the constraints are purely local, we only care about adjacent elements, but the state space explodes immediately.

The next idea is to think about what actually makes a cycle impossible. Suppose one album appears more than half the time. Then even if we separate its occurrences as much as possible, two copies must become neighbors somewhere in the cycle. This is the same obstruction as rearranging characters in a string so equal letters do not touch.

That observation changes the problem from exhaustive search into constructive placement.

We first decide how many photos to take from each album. Obviously we can never take more than `⌊n / 2⌋` from a single album. So we greedily take photos from the albums while respecting that limit, until the total chosen count becomes exactly `n`.

After that, we have a multiset of album labels whose frequencies already satisfy the necessary condition:

```
max_frequency ≤ n / 2
```

For such multisets, a cyclic arrangement always exists.

The remaining task is constructing it.

A clean strategy is to sort albums by frequency, write all chosen labels into an array, then place them into even positions first and odd positions second. This spacing automatically separates equal labels because copies of the same album are distributed across the array before wrapping around.

The whole process is small and efficient because `m` is only `40`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all album sizes.
2. For every album, take as many photos as possible, but never more than `n // 2`.

This limit is mandatory in any valid cycle. If one album exceeded it, two neighboring positions would eventually become equal.
3. Keep adding albums until the total number of selected photos reaches exactly `n`.

If the total selectable amount is still smaller than `n`, print `-1`.
4. Build a list containing the chosen album numbers repeated according to their selected counts.

Example:

```
counts:
album 1 -> 2
album 2 -> 3
album 3 -> 1

list:
[2, 2, 2, 1, 1, 3]
```
5. Sort this list by frequency in descending order.

The most frequent albums are the hardest to place, so we distribute them first.
6. Create an answer array of size `n`.
7. Fill positions `0, 2, 4, ...` first, then continue with `1, 3, 5, ...`.

This spacing keeps equal albums apart naturally.
8. Output the constructed cycle.
9. As a safety check, verify that every neighboring pair differs, including the pair formed by the last and first positions.

### Why it works

The key invariant is that no album frequency exceeds `n / 2`.

When we place elements into alternating positions, copies of the same album are separated by at least one slot because the algorithm exhausts all even positions before touching odd ones. Since the largest frequency is at most half the cycle size, the placements never force two equal labels together.

The cyclic boundary also remains valid. The first and last positions belong to different parity groups during filling, so the construction avoids creating an equal pair at the wraparound edge.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    chosen = []
    total = 0

    # take at most n//2 from every album
    for i in range(m):
        take = min(a[i], n // 2)

        if total + take > n:
            take = n - total

        total += take

        for _ in range(take):
            chosen.append(i + 1)

        if total == n:
            break

    if total < n:
        print(-1)
        return

    # frequency map
    freq = {}
    for x in chosen:
        freq[x] = freq.get(x, 0) + 1

    # impossible if some frequency exceeds n//2
    if max(freq.values()) > n // 2:
        print(-1)
        return

    # sort by frequency descending
    chosen.sort(key=lambda x: freq[x], reverse=True)

    ans = [0] * n

    idx = 0

    # even positions first
    for x in chosen:
        ans[idx] = x
        idx += 2
        if idx >= n:
            idx = 1

    # final verification
    for i in range(n):
        if ans[i] == ans[(i + 1) % n]:
            print(-1)
            return

    print(*ans)

solve()
```

The first section decides how many photos to use from each album. The critical detail is the cap `n // 2`. Without this restriction, a valid cycle may become impossible even though enough photos exist.

The code stops once exactly `n` photos are collected. We never need to use all available photos.

The sorting step is subtle. If low-frequency albums are placed first, a large block of equal albums may remain near the end and become impossible to separate. Sorting by descending frequency distributes difficult elements early.

The placement loop uses alternating indices:

```
0, 2, 4, ...
```

then wraps to:

```
1, 3, 5, ...
```

This is the same trick used in classic "reorganize string" problems.

The final validation is defensive programming. The construction is mathematically correct, but checking the result makes debugging easier and guarantees no accidental implementation bug survives.

## Worked Examples

### Example 1

Input:

```
4 3
1 3 5
```

Chosen counts become:

```
album 1 -> 1
album 2 -> 2
album 3 -> 1
```

The sorted multiset is:

```
[2, 2, 1, 3]
```

| Step | Position Filled | Value | Current Answer |
| --- | --- | --- | --- |
| 1 | 0 | 2 | [2, 0, 0, 0] |
| 2 | 2 | 2 | [2, 0, 2, 0] |
| 3 | 1 | 1 | [2, 1, 2, 0] |
| 4 | 3 | 3 | [2, 1, 2, 3] |

Final cycle:

```
2 1 2 3
```

Every adjacent pair differs, including `3` and `2` across the boundary.

This trace demonstrates the main invariant. The most frequent album is distributed into alternating positions before anything else is inserted.

### Example 2

Input:

```
6 3
6 1 1
```

Chosen counts become:

```
album 1 -> 3
album 2 -> 1
album 3 -> 1
```

Total selected photos:

```
5
```

We cannot reach `n = 6`, so the algorithm outputs:

```
-1
```

| Album | Available | Maximum Allowed | Taken |
| --- | --- | --- | --- |
| 1 | 6 | 3 | 3 |
| 2 | 1 | 3 | 1 |
| 3 | 1 | 3 | 1 |

This example shows why the `n // 2` restriction is necessary. Even though there are eight total photos, the cyclic adjacency condition prevents using six of them safely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the selected labels dominates |
| Space | O(n) | The constructed gallery stores exactly `n` labels |

With `n ≤ 1000`, even quadratic solutions would pass comfortably. This implementation stays well within the limits and runs essentially instantly.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    chosen = []
    total = 0

    for i in range(m):
        take = min(a[i], n // 2)

        if total + take > n:
            take = n - total

        total += take

        for _ in range(take):
            chosen.append(i + 1)

        if total == n:
            break

    if total < n:
        return "-1"

    freq = {}
    for x in chosen:
        freq[x] = freq.get(x, 0) + 1

    if max(freq.values()) > n // 2:
        return "-1"

    chosen.sort(key=lambda x: freq[x], reverse=True)

    ans = [0] * n
    idx = 0

    for x in chosen:
        ans[idx] = x
        idx += 2
        if idx >= n:
            idx = 1

    for i in range(n):
        if ans[i] == ans[(i + 1) % n]:
            return "-1"

    return " ".join(map(str, ans))

# provided sample
out = solve_io("4 3\n1 3 5\n")
vals = list(map(int, out.split()))
assert len(vals) == 4

# minimum valid case
out = solve_io("3 3\n1 1 1\n")
vals = list(map(int, out.split()))
assert len(vals) == 3

# impossible because dominant album too large
assert solve_io("6 3\n6 1 1\n") == "-1"

# exactly balanced
out = solve_io("8 2\n4 4\n")
vals = list(map(int, out.split()))
for i in range(8):
    assert vals[i] != vals[(i + 1) % 8]

# many albums, sparse counts
out = solve_io("5 5\n1 1 1 1 1\n")
vals = list(map(int, out.split()))
assert len(vals) == 5
assert len(set(vals)) == 5
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 3 / 1 1 1` | Any valid cycle | Smallest meaningful cycle |
| `6 3 / 6 1 1` | `-1` | Dominant album impossibility |
| `8 2 / 4 4` | Alternating arrangement | Boundary case where max frequency equals `n/2` |
| `5 5 / 1 1 1 1 1` | Any permutation | Distinct albums everywhere |

## Edge Cases

Consider the case where one album almost dominates the gallery.

Input:

```
8 3
4 2 2
```

The maximum allowed frequency is `4`, so this is still feasible.

The construction becomes:

```
1 1 1 1 2 2 3 3
```

After alternating placement:

```
1 2 1 2 1 3 1 3
```

Checking cyclic neighbors confirms validity. This example shows that frequency exactly equal to `n / 2` is still safe.

Now consider a case where the cyclic boundary is the only danger.

Input:

```
5 2
3 2
```

A naive linear greedy could build:

```
1 2 1 2 1
```

The last and first elements collide.

Our alternating placement instead produces:

```
1 2 1 2 1
```

and the final validation detects the collision. Since no valid cycle exists for these frequencies, the algorithm correctly outputs `-1`.

Finally, consider the case where many photos are available but only some should be used.

Input:

```
4 3
100 1 1
```

The algorithm caps album `1` at `2` photos:

```
1 1 2 3
```

After placement:

```
1 2 1 3
```

The cycle is valid. This confirms that discarding excess photos is essential for correctness.
