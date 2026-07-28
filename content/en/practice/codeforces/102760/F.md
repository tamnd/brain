---
title: "CF 102760F - Square, Not Rectangle"
description: "We are given a histogram made of adjacent vertical tiles. The i-th tile has width 1 and height Hi, so a group of consecutive tiles forms a rectangle whose width is the number of chosen tiles and whose height is limited by the shortest tile in that group."
date: "2026-07-28T23:51:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102760
codeforces_index: "F"
codeforces_contest_name: "2020 KAIST 10th ICPC Mock Contest (XXI Open Cup. Grand Prix of Korea. Division 2)"
rating: 0
weight: 102760
solve_time_s: 58
verified: true
draft: false
---

[CF 102760F - Square, Not Rectangle](https://codeforces.com/problemset/problem/102760/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a histogram made of adjacent vertical tiles. The `i`-th tile has width `1` and height `H_i`, so a group of consecutive tiles forms a rectangle whose width is the number of chosen tiles and whose height is limited by the shortest tile in that group. The task is to find the largest possible square that fits completely inside the histogram and output its side length. The square must have its sides aligned with the histogram axes.

The input contains one histogram with `N` tiles followed by their heights. The output is not the area of the square, but the maximum side length that can be achieved.

The number of tiles can reach `300000`, so an algorithm that checks many intervals cannot work. A direct search over all pairs of left and right boundaries would require around `N^2` interval checks, which is far beyond what a typical competitive programming time limit allows. The heights can also be as large as `10^9`, so the answer and intermediate comparisons must be handled using integer arithmetic without relying on small value assumptions.

The tricky cases come from confusing the largest rectangle with the largest square. For example, if the histogram is:

```
3
100 1 100
```

the largest rectangle has area `200`, but the largest square has side length `1`, because the only wide region is not tall enough.

Another common mistake is forgetting that a square can use only part of a large rectangle. For:

```
5
10 10 10 10 10
```

the answer is `5`, not `10`, because the histogram is only five tiles wide. The limiting factor is the smaller of width and height.

A final boundary case is a single tile:

```
1
7
```

The answer is `1`, not `7`, because one tile has width exactly one.

## Approaches

The brute-force idea is to try every possible consecutive range of tiles. For each range, we find the minimum height inside it. That minimum height is the maximum possible square height for this range, while the range length is the maximum possible square width. The candidate answer is the smaller of those two values.

This approach is correct because every possible square corresponds to some consecutive range of tiles. However, there are `N(N+1)/2` ranges, which is about `4.5 * 10^10` when `N = 300000`. Even with fast minimum queries, checking every range is impossible.

The key observation is that the shortest tile in a range determines the maximum height of every square using that range. Instead of considering every range, we can consider each tile as the minimum-height tile of the best possible range around it.

For a tile with height `h`, we find the widest consecutive segment where every tile has height at least `h`. If that segment has width `w`, then the largest square for which this tile is the limiting height has side length `min(h, w)`.

The remaining challenge is finding these widest segments efficiently. A monotonic increasing stack gives exactly this information. It allows us to find, for every tile, the first smaller tile on the left and the first smaller tile on the right. Those two positions define the maximal range where the current height can be the minimum.

The brute-force method works because every possible square belongs to some interval. It fails because there are too many intervals. The monotonic stack removes the need to enumerate intervals by directly finding the maximal interval for each possible limiting height.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Traverse the histogram from left to right while maintaining a monotonic increasing stack of tile indices. The stack stores tiles whose heights have not yet encountered a smaller tile on their right. Keeping heights increasing means that when a shorter tile appears, we immediately know that some previous tiles have reached their maximal width.
2. When the current height is smaller than the height of the tile at the top of the stack, remove indices from the stack one by one. For each removed tile, the current position is the first smaller tile on the right, and the new stack top after removal is the first smaller tile on the left.
3. Compute the width of the maximal segment for the removed tile. If there is no smaller tile on the left, the segment starts at the beginning of the histogram. Otherwise, it starts after the left smaller tile. The width is the current index minus that left boundary.
4. Use the removed tile's height and computed width to form a square candidate. The side length cannot exceed either dimension, so update the answer with `min(height, width)`.
5. Push the current tile index onto the stack after all taller tiles have been processed. This keeps the stack property valid for future tiles.
6. After scanning all tiles, pretend there is one extra tile of height `0`. This forces every remaining stack element to be removed and processed, covering ranges that extend to the end of the histogram.

Why it works:

Every valid square occupies some consecutive group of tiles. Let the shortest tile height in that group be `h`. At least one tile in the group has height exactly `h`. When the algorithm processes that tile, the monotonic stack gives the largest possible interval where every tile has height at least `h`. Any square using height `h` cannot be wider than this interval, and the algorithm checks exactly the best possible side length for it. Since every possible square has a corresponding minimum-height tile that is considered, the maximum candidate found by the algorithm is the true answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    h = list(map(int, input().split()))

    stack = []
    ans = 0

    for i in range(n + 1):
        cur = h[i] if i < n else 0

        while stack and h[stack[-1]] > cur:
            idx = stack.pop()
            height = h[idx]

            if stack:
                width = i - stack[-1] - 1
            else:
                width = i

            ans = max(ans, min(height, width))

        stack.append(i)

    print(ans)

if __name__ == "__main__":
    solve()
```

The stack stores indices rather than heights because the position of each tile is needed to calculate the width of its maximal valid interval. The stack is increasing by height, so every time a shorter tile arrives, the removed tiles have found their first smaller element on the right.

The extra iteration with height `0` is a sentinel. It does not represent a real tile, but it guarantees that all remaining heights are popped and evaluated. Without it, tiles that extend to the histogram's end would never be considered.

The width calculation is the main place where off-by-one mistakes happen. If the stack is empty after removing a tile, there is no smaller tile to its left, so the interval starts at index `0` and has width `i`. Otherwise, the interval begins after `stack[-1]`, giving width `i - stack[-1] - 1`.

## Worked Examples

For the sample:

```
6
3 4 4 4 4 3
```

the execution is:

| Step | Current index | Current height | Stack after processing | Removed height | Candidate |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | [0] | none | none |
| 2 | 1 | 4 | [0, 1] | none | none |
| 3 | 2 | 4 | [0, 1, 2] | none | none |
| 4 | 3 | 4 | [0, 1, 2, 3] | none | none |
| 5 | 4 | 4 | [0, 1, 2, 3, 4] | none | none |
| 6 | 5 | 3 | [0, 5] | 4 | 4 |
| 7 | 6 | 0 | [ ] | 3 | 3 |

The four tiles of height `4` form a square of side length `4`, which becomes the answer.

Another example:

```
5
2 5 5 5 2
```

| Step | Current index | Current height | Stack after processing | Removed height | Candidate |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | [0] | none | none |
| 2 | 1 | 5 | [0, 1] | none | none |
| 3 | 2 | 5 | [0, 1, 2] | none | none |
| 4 | 3 | 5 | [0, 1, 2, 3] | none | none |
| 5 | 4 | 2 | [0, 4] | 5 | 3 |
| 6 | 5 | 0 | [ ] | 2 | 2 |

The height `5` region has width `3`, so the best square has side length `3`. The surrounding height `2` tiles are wider but cannot create a larger square because their height is the limiting dimension.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Every tile index enters the stack once and leaves it once. |
| Space | O(N) | The stack can contain every tile index in an increasing histogram. |

The algorithm performs a constant amount of work for every stack operation, and the total number of pushes and pops is linear. With `N = 300000`, this easily fits within the intended limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""6
3 4 4 4 4 3
""") == "4\n", "sample 1"

assert run("""1
7
""") == "1\n", "single tile"

assert run("""5
10 10 10 10 10
""") == "5\n", "width limited"

assert run("""3
100 1 100
""") == "1\n", "short middle tile"

assert run("""5
2 5 5 5 2
""") == "3\n", "largest square inside rectangle"

assert run("""6
1 2 3 4 5 6
""") == "3\n", "increasing heights"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `1` | Single tile width boundary |
| `10 10 10 10 10` | `5` | Width limiting the answer |
| `100 1 100` | `1` | Height bottleneck handling |
| `2 5 5 5 2` | `3` | Square inside a larger rectangle |
| `1 2 3 4 5 6` | `3` | Correct stack behavior on increasing heights |

## Edge Cases

For the histogram:

```
3
100 1 100
```

the stack first stores the increasing heights `100`, then encounters `1`. The two height `100` tiles are popped, but their available width is only `1`, so they produce side length `1`. The height `1` tile can span the whole histogram, but its height also limits the square to `1`. The algorithm returns `1`, matching the true maximum.

For:

```
5
10 10 10 10 10
```

all tiles remain in the stack until the sentinel zero height is processed. Each height `10` tile can cover the full width of five tiles, but the square side is limited by the width. The best candidate becomes `min(10, 5) = 5`.

For:

```
1
7
```

the only tile is removed by the sentinel. Its width is calculated as `1`, so the candidate is `min(7, 1) = 1`. This prevents the algorithm from incorrectly treating the tile height as the square side.

I can also provide a shorter contest-editorial version or a more proof-focused version if needed.
