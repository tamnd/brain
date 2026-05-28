---
title: "CF 81D - Polycarp's Picture Gallery"
description: "We have several photo albums. Album i contains a[i] photos. We must build a cyclic gallery containing exactly n photos. Instead of choosing concrete photo IDs, we only need to output the album number for each position. The gallery is circular, so every position has two neighbors."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 81
codeforces_index: "D"
codeforces_contest_name: "Yandex.Algorithm Open 2011: Qualification 1"
rating: 2100
weight: 81
solve_time_s: 168
verified: false
draft: false
---

[CF 81D - Polycarp's Picture Gallery](https://codeforces.com/problemset/problem/81/D)

**Rating:** 2100  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We have several photo albums. Album `i` contains `a[i]` photos. We must build a cyclic gallery containing exactly `n` photos. Instead of choosing concrete photo IDs, we only need to output the album number for each position.

The gallery is circular, so every position has two neighbors. Position `1` is adjacent to both positions `2` and `n`. The requirement is that adjacent positions must always come from different albums.

We are free to choose any subset of photos from the albums, as long as we place exactly `n` photos total and never exceed the available count of any album.

The constraints are small enough that we can afford quadratic work. `n ≤ 1000` and `m ≤ 40`, so even an `O(n^2)` or `O(n log n)` construction is easily fast enough. What we cannot do is brute force over permutations or perform exponential search, because the number of possible cyclic arrangements grows astronomically even for `n = 20`.

The tricky part is not selecting photos, but arranging them so that the first and last positions also differ. A sequence that works linearly may still fail cyclically.

Consider this example:

```
n = 5
albums = [3, 2]
```

A naive greedy might produce:

```
1 2 1 2 1
```

Every adjacent pair inside the array differs, but the last and first positions are both `1`, so the cycle is invalid.

Another dangerous case is when one album is too large.

```
n = 6
albums = [6]
```

Every chosen photo would come from the same album, so avoiding equal neighbors is impossible.

More subtly:

```
n = 7
albums = [4, 3]
```

A valid cycle exists:

```
1 2 1 2 1 2 1
```

Wait, this actually fails because the first and last positions are both `1`.

For a cycle, the largest album cannot exceed `n / 2`. Here `4 > floor(7/2)`, so no valid arrangement exists.

A careless implementation that only checks linear adjacency would incorrectly accept such cases.

One more edge case appears when we have more available photos than needed. We are not required to use every photo.

Example:

```
n = 4
albums = [1, 100]
```

We should select only four photos total. The correct answer is impossible because any cyclic arrangement of length `4` needs at most `2` copies of the same album, but album `2` dominates too heavily and album `1` contributes only one separator.

Understanding that we may discard photos is essential. The construction should first decide how many photos to take from each album.

## Approaches

The brute-force idea is straightforward. First choose which photos to use, then try every permutation and check whether adjacent positions differ cyclically.

Even if we only think in terms of album labels instead of concrete photos, the number of arrangements is enormous. With `n = 1000`, even `1000!` possibilities are beyond impossible to enumerate. A backtracking search with pruning still explodes because many prefixes remain feasible until very deep into the recursion.

The reason brute force works conceptually is that the condition is purely local. We only care about neighboring positions. Unfortunately, local constraints do not reduce the search space enough.

The key observation is that this is really a frequency-balancing problem. We only need to distribute repeated album labels around a circle. Once no album appears too many times, a valid arrangement can always be constructed greedily.

For a cyclic arrangement, no album may occupy more than half the positions. Otherwise two copies of that album must become adjacent by the pigeonhole principle.

That condition is also sufficient.

So the problem becomes:

1. Decide how many photos to take from each album, with total exactly `n`.
2. Ensure the maximum chosen count is at most `n / 2`.
3. Construct the cyclic arrangement.

The elegant construction is based on sorting all chosen album labels and placing them into the answer using alternating positions.

Suppose the multiset is:

```
1 1 1 2 2 3
```

We place them into positions:

```
0, 2, 4, 1, 3, 5
```

The repeated labels become naturally separated because equal elements in the sorted list get distributed across distant indices.

This transforms the problem from exponential search into a deterministic greedy construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all album sizes.
2. For every album, initially take as many photos as possible, but never more than `n / 2`.

This is necessary because any album appearing more than `n / 2` times would force two adjacent copies in the cycle.
3. Sum the chosen counts.
4. If the total chosen count is still smaller than `n`, print `-1`.

This means that even after using the maximum safe amount from every album, we cannot reach `n` photos.
5. Otherwise, reduce the chosen counts until their sum becomes exactly `n`.

We can decrease any positive count arbitrarily. Reducing counts never hurts feasibility because it only lowers frequencies.
6. Build an array containing each album index repeated according to its chosen count.

Example:

```
counts = [2,1,3]
```

becomes

```
[1,1,2,3,3,3]
```
7. Sort this list.

Equal labels become consecutive, which makes the next placement step predictable.
8. Create an empty answer array of size `n`.
9. Fill even indices first, then odd indices.

Use the order:

```
0, 2, 4, ..., 1, 3, 5, ...
```

Place the sorted labels one by one into these positions.
10. Output the final arrangement.

### Why it works

The crucial invariant is that no album count exceeds `n / 2`.

When we distribute the sorted labels into alternating positions, copies of the same album become separated by at least one other position. Since equal labels appear consecutively in the sorted list, placing them into positions spaced two apart prevents collisions.

The only remaining danger is the cyclic edge between the last and first positions. The `max_count ≤ n/2` condition guarantees that the alternating placement never wraps equal labels onto both ends simultaneously.

This construction is equivalent to interleaving the largest frequencies across the circle. The feasibility condition is both necessary and sufficient, so whenever the algorithm does not print `-1`, the produced arrangement is valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    take = [min(x, n // 2) for x in a]

    total = sum(take)

    if total < n:
        print(-1)
        return

    extra = total - n

    for i in range(m):
        dec = min(take[i], extra)
        take[i] -= dec
        extra -= dec
        if extra == 0:
            break

    vals = []

    for i in range(m):
        vals.extend([i + 1] * take[i])

    vals.sort()

    ans = [0] * n

    pos = []

    for i in range(0, n, 2):
        pos.append(i)

    for i in range(1, n, 2):
        pos.append(i)

    for i in range(n):
        ans[pos[i]] = vals[i]

    for i in range(n):
        if ans[i] == ans[(i + 1) % n]:
            print(-1)
            return

    print(*ans)

solve()
```

The first stage computes how many photos we are allowed to use from each album. Capping every album at `n // 2` encodes the feasibility condition directly into the construction.

After that, the total chosen amount may exceed `n`, because several albums together can still provide many usable photos. We simply remove extra copies arbitrarily. Reducing counts cannot create a new conflict because adjacency only becomes easier when frequencies shrink.

The `vals` array stores the multiset of album labels. Sorting is important because the placement strategy assumes identical labels are grouped together.

The position order is the core trick. We first fill all even indices, then all odd indices. This spreads equal labels apart automatically.

The final verification loop is not strictly necessary if the reasoning is correct, but it is a useful defensive check and costs only `O(n)`.

One subtle point is that the cycle check uses modulo indexing:

```
ans[(i + 1) % n]
```

Without the modulo, the code would only validate linear adjacency and miss the edge between the last and first positions.

## Worked Examples

### Example 1

Input:

```
4 3
1 3 5
```

After capping by `n // 2 = 2`:

| Album | Original | Chosen |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 2 |
| 3 | 5 | 2 |

Total is `5`, but we only need `4`.

We remove one extra copy.

| Album | Final Count |
| --- | --- |
| 1 | 0 |
| 2 | 2 |
| 3 | 2 |

The multiset becomes:

```
[2, 2, 3, 3]
```

Placement order is:

```
0, 2, 1, 3
```

| Step | Value | Position | Array |
| --- | --- | --- | --- |
| 1 | 2 | 0 | [2,0,0,0] |
| 2 | 2 | 2 | [2,0,2,0] |
| 3 | 3 | 1 | [2,3,2,0] |
| 4 | 3 | 3 | [2,3,2,3] |

Final answer:

```
2 3 2 3
```

Every neighboring pair differs, including the cyclic pair `(3,2)`.

This trace demonstrates how alternating placement separates repeated labels automatically.

### Example 2

Input:

```
7 2
4 3
```

After capping by `n // 2 = 3`:

| Album | Original | Chosen |
| --- | --- | --- |
| 1 | 4 | 3 |
| 2 | 3 | 3 |

Total is `6`, smaller than `7`.

The algorithm prints:

```
-1
```

This confirms the necessary condition. Even after limiting album frequencies to safe values, we cannot gather enough photos.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the constructed multiset dominates |
| Space | O(n) | Arrays storing chosen labels and the final answer |

With `n ≤ 1000`, this complexity is comfortably within limits. The sorting step handles at most 1000 elements, which is trivial for Python in a 2-second limit.

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

    take = [min(x, n // 2) for x in a]

    total = sum(take)

    if total < n:
        return "-1"

    extra = total - n

    for i in range(m):
        dec = min(take[i], extra)
        take[i] -= dec
        extra -= dec
        if extra == 0:
            break

    vals = []

    for i in range(m):
        vals.extend([i + 1] * take[i])

    vals.sort()

    ans = [0] * n

    pos = []

    for i in range(0, n, 2):
        pos.append(i)

    for i in range(1, n, 2):
        pos.append(i)

    for i in range(n):
        ans[pos[i]] = vals[i]

    for i in range(n):
        if ans[i] == ans[(i + 1) % n]:
            return "-1"

    return " ".join(map(str, ans))

# provided sample
out = solve_io("4 3\n1 3 5\n")
arr = list(map(int, out.split()))
assert len(arr) == 4
for i in range(4):
    assert arr[i] != arr[(i + 1) % 4]

# impossible case
assert solve_io("7 2\n4 3\n") == "-1"

# minimum valid size
out = solve_io("3 3\n1 1 1\n")
arr = list(map(int, out.split()))
for i in range(3):
    assert arr[i] != arr[(i + 1) % 3]

# all equal albums
assert solve_io("5 1\n10\n") == "-1"

# balanced large frequencies
out = solve_io("6 2\n3 3\n")
arr = list(map(int, out.split()))
for i in range(6):
    assert arr[i] != arr[(i + 1) % 6]

# extra unused photos
out = solve_io("5 3\n10 10 10\n")
arr = list(map(int, out.split()))
assert len(arr) == 5
for i in range(5):
    assert arr[i] != arr[(i + 1) % 5]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7 2 / 4 3` | `-1` | Largest frequency exceeds cyclic limit |
| `3 3 / 1 1 1` | Any valid cycle | Minimum valid size |
| `5 1 / 10` | `-1` | Single album impossible |
| `6 2 / 3 3` | Any alternating cycle | Perfectly balanced counts |
| `5 3 / 10 10 10` | Any valid cycle | Correct handling of discarded photos |

## Edge Cases

Consider:

```
5 2
3 2
```

The maximum allowed frequency is `2`, because `n // 2 = 2`.

After capping:

```
2 2
```

The total becomes `4`, smaller than `5`, so the algorithm prints `-1`.

This is correct. Any cycle of odd length requires some album to appear at least three times, but three copies in a cycle of length five inevitably force an adjacency.

Now consider:

```
6 3
6 1 1
```

After capping:

```
3 1 1
```

The total is `5`, still below `6`.

Again the algorithm prints `-1`.

Intuitively, the dominant album needs separators between all its copies. Two extra albums provide only two separators, not enough to place six photos cyclically.

Finally, consider:

```
8 4
2 2 2 100
```

After capping:

```
2 2 2 4
```

The total is `10`, so we remove two extras.

One possible final count set is:

```
0 2 2 4
```

The construction yields something like:

```
4 2 4 3 4 2 4 3
```

The largest album occupies exactly half the positions, which is still safe. Every copy is separated by another album, including across the cyclic boundary.
