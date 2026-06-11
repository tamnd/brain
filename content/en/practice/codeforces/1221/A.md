---
title: "CF 1221A - 2048 Game"
description: "We are given several independent game states. Each state consists of tiles whose values are powers of two. In one move, we may pick two tiles with the same value and merge them into a single tile whose value is their sum."
date: "2026-06-11T22:36:51+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1221
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 73 (Rated for Div. 2)"
rating: 1000
weight: 1221
solve_time_s: 96
verified: true
draft: false
---

[CF 1221A - 2048 Game](https://codeforces.com/problemset/problem/1221/A)

**Rating:** 1000  
**Tags:** brute force, greedy, math  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent game states. Each state consists of tiles whose values are powers of two. In one move, we may pick two tiles with the same value and merge them into a single tile whose value is their sum.

The question is whether it is possible to obtain a tile with value `2048` after performing any number of merges.

The operation is exactly the same as in the game 2048. Two equal powers of two combine into the next larger power of two. Since every value is already a power of two, every merge also produces a power of two.

The constraints are very small. There are at most 100 queries, and each query contains at most 100 numbers. Even a simulation using frequency counts of powers of two would be easily fast enough. We do not need any sophisticated data structure.

The key observation comes from understanding which tiles can contribute to a future `2048`.

Any tile larger than `2048` is useless. Since merges only increase values, a tile such as `4096` can never become `2048`. It also cannot merge with smaller tiles to create `2048`, because merging is only allowed between equal values.

Another subtle case is when the total sum of all usable tiles reaches `2048`, even though no individual tile starts near that value.

For example:

```
1
11
1 1 2 2 4 4 8 8 16 16 1024
```

The usable sum is:

```
1+1+2+2+4+4+8+8+16+16+1024 = 1086
```

which is not enough, so the answer is `NO`.

A different example:

```
1
2
1024 1024
```

The answer is `YES` because the two `1024` tiles merge directly into `2048`.

A common mistake is to include values larger than `2048` in the sum:

```
1
2
4096 4
```

The correct answer is `NO`.

A careless solution might compute total sum `4100 ≥ 2048` and incorrectly answer `YES`, even though the `4096` tile can never help produce `2048`.

## Approaches

The most direct approach is to simulate the game. We can count how many tiles of each power of two exist. Whenever there are at least two copies of some value `x`, we merge pairs of them into value `2x`. Repeating this process eventually produces every tile that can possibly be created.

This simulation is correct because every legal sequence of merges produces exactly the same final carry propagation. The problem is that it is more machinery than we actually need.

The crucial observation is that every tile with value at most `2048` can always be merged as much as necessary. Powers of two behave exactly like binary carries.

Suppose we take all values not exceeding `2048` and add them together. If their total sum is at least `2048`, then we can always perform merges until a `2048` tile appears. The reason is that repeated merges simply convert this total mass into larger and larger powers of two.

If the total sum of all tiles not exceeding `2048` is less than `2048`, then creating a `2048` tile is impossible because merges never increase the total sum.

This reduces the entire problem to a simple sum.

For each query, ignore every number greater than `2048`, add the remaining numbers, and check whether the sum is at least `2048`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n + log V) | O(log V) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

Here `V` is the largest power of two that may appear during simulation.

## Algorithm Walkthrough

1. Read the number of queries.
2. For each query, read all tile values.
3. Initialize a running sum equal to zero.
4. For every tile, check whether its value is at most `2048`.
5. If the value is at most `2048`, add it to the running sum.

Values larger than `2048` can never contribute to creating a `2048` tile, so they are ignored.
6. After processing all tiles, compare the sum with `2048`.
7. If the sum is at least `2048`, print `"YES"`.
8. Otherwise, print `"NO"`.

### Why it works

The total sum of all tiles is preserved by every merge operation. Two equal tiles `x + x` become a single tile `2x`, so no value is lost or gained.

Every tile larger than `2048` is irrelevant because merges never decrease values. Such a tile can never become `2048`, nor can it merge with smaller values to create `2048`.

Among tiles whose values do not exceed `2048`, repeated merges act exactly like carrying in binary addition. If their total sum is at least `2048`, those carries eventually produce a `2048` tile. If their total sum is less than `2048`, no sequence of merges can create a tile whose value exceeds the available total mass.

Thus the condition

```
sum(all values ≤ 2048) ≥ 2048
```

is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())

    for _ in range(q):
        n = int(input())
        arr = list(map(int, input().split()))

        total = 0
        for x in arr:
            if x <= 2048:
                total += x

        print("YES" if total >= 2048 else "NO")

solve()
```

The implementation follows the proof directly.

The variable `total` stores the sum of every tile that could possibly contribute to a future `2048`. Any value larger than `2048` is skipped immediately.

After processing one query, a single comparison determines the answer.

There are no overflow concerns in Python. Even in the worst case, the sum is far below Python's integer limits.

The most common implementation mistake is forgetting to ignore values greater than `2048`. Doing so would incorrectly treat tiles such as `4096` as useful contributors.

## Worked Examples

### Example 1

Input:

```
4
1024 512 64 512
```

| Tile | Included? | Running Sum |
| --- | --- | --- |
| 1024 | Yes | 1024 |
| 512 | Yes | 1536 |
| 64 | Yes | 1600 |
| 512 | Yes | 2112 |

Final sum = 2112.

Since `2112 ≥ 2048`, the answer is:

```
YES
```

This demonstrates that we do not need to explicitly simulate the merges. The available mass already exceeds `2048`, so a `2048` tile can be formed.

### Example 2

Input:

```
2
4096 4
```

| Tile | Included? | Running Sum |
| --- | --- | --- |
| 4096 | No | 0 |
| 4 | Yes | 4 |

Final sum = 4.

Since `4 < 2048`, the answer is:

```
NO
```

This example shows why values larger than `2048` must be ignored. The `4096` tile cannot help create a `2048` tile.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each tile is processed exactly once |
| Space | O(1) | Only a few variables are stored |

For each query we perform a single linear scan through at most 100 numbers. Even across all test cases, the amount of work is tiny compared to the limits, so the solution easily fits within both the time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    q = int(input())
    ans = []

    for _ in range(q):
        n = int(input())
        arr = list(map(int, input().split()))

        total = sum(x for x in arr if x <= 2048)
        ans.append("YES" if total >= 2048 else "NO")

    return "\n".join(ans)

# provided sample
assert run(
"""6
4
1024 512 64 512
1
2048
3
64 512 2
2
4096 4
7
2048 2 2048 2048 2048 2048 2048
2
2048 4096
"""
) == """YES
YES
NO
NO
YES
YES"""

# minimum size
assert run(
"""1
1
1
"""
) == "NO", "single small tile"

# exact boundary
assert run(
"""1
2
1024 1024
"""
) == "YES", "two tiles merge into 2048"

# large value should be ignored
assert run(
"""1
2
4096 1024
"""
) == "NO", "4096 cannot help create 2048"

# many small values
assert run(
"""1
11
1 1 2 2 4 4 8 8 16 16 1986
"""
) == "YES", "sum of usable tiles reaches 2048"

# all equal values
assert run(
"""1
100
32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32
"""
) == "YES", "100 * 32 = 3200"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `NO` | Minimum-size query |
| `1024 1024` | `YES` | Exact merge into 2048 |
| `4096 1024` | `NO` | Larger values must be ignored |
| Small powers summing to 2048+ | `YES` | Binary-carry behavior |
| 100 copies of 32 | `YES` | Large multiplicities |

## Edge Cases

Consider:

```
1
1
2048
```

The algorithm adds `2048` to the running sum, obtaining `2048`. Since the sum is already at least `2048`, it outputs `YES`. No merges are required because the target tile already exists.

Now consider:

```
1
2
4096 4
```

The algorithm ignores `4096` and keeps only `4`. The resulting sum is `4`, so it outputs `NO`. This matches the game rules because values never decrease.

Finally, consider:

```
1
4
512 512 512 512
```

The running sum becomes `2048`. The algorithm outputs `YES`.

Tracing the actual merges:

```
512 + 512 -> 1024
512 + 512 -> 1024
1024 + 1024 -> 2048
```

This confirms the key invariant behind the solution: all usable tiles contribute their total mass toward building a `2048` tile, and only the sum matters.
