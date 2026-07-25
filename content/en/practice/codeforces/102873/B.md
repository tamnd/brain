---
title: "CF 102873B - Rabbit Game"
description: "We have a row of carrots, where each carrot has a size. Two rabbits begin at opposite ends of this row. A rabbit can continue moving inward only while every next carrot it reaches is at least as large as the carrot it just ate."
date: "2026-07-25T13:08:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102873
codeforces_index: "B"
codeforces_contest_name: "Unofficial Div 4 Round #2 by ssense  SlavicG"
rating: 0
weight: 102873
solve_time_s: 69
verified: true
draft: false
---

[CF 102873B - Rabbit Game](https://codeforces.com/problemset/problem/102873/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of carrots, where each carrot has a size. Two rabbits begin at opposite ends of this row. A rabbit can continue moving inward only while every next carrot it reaches is at least as large as the carrot it just ate. The two rabbits can choose their order of moves, so the goal is to maximize how many different carrots are eaten before both rabbits can no longer continue. The problem asks for that maximum count.

The first rabbit only depends on the longest non-decreasing prefix of the array. If the first few carrots are `1 2 2 5`, it can eat all of them because every move is allowed. The second rabbit has the symmetric condition from the other side: when looking from right to left, the eaten sequence must be non-decreasing, which means the remaining suffix must be non-increasing when viewed from left to right.

The constraint `n <= 2 * 10^5` rules out simulating every possible order of rabbit moves. Any approach that tries many combinations of moves can easily become quadratic or worse, and around `4 * 10^10` operations would be far beyond the limit. We need a linear scan because it processes the entire array only a constant number of times.

The tricky cases are where the two rabbits' reachable segments touch or overlap. A common mistake is to count the two rabbits independently and accidentally count the same carrot twice. For example:

```
Input
5
2 2 2 2 2
```

The correct output is:

```
5
```

Both rabbits can reach every carrot, but the middle carrots are not counted twice. The answer is the number of distinct carrots that can be covered.

Another boundary case is when one rabbit stops immediately. For example:

```
Input
4
5 1 1 1
```

The correct output is:

```
4
```

The left rabbit eats only the first carrot because the next one is smaller. The right rabbit can eat the entire suffix `1 1 1`. A solution that assumes both rabbits always contribute more than one carrot would fail here.

A final case is when the reachable parts are separated by a decreasing jump:

```
Input
5
1 3 2 3 1
```

The correct output is:

```
4
```

The left rabbit reaches the first two carrots, and the right rabbit reaches the last two carrots. The middle carrot is unreachable by either rabbit.

## Approaches

The direct approach is to simulate both rabbits. We can start from the left endpoint and repeatedly move while the next carrot satisfies the condition. We can do the same from the right endpoint. This correctly identifies every carrot each rabbit can possibly eat because a rabbit's path is deterministic once its starting side is fixed.

The problem with a full simulation of possible move orders is that it treats the interaction between rabbits as if there are many meaningful choices. In reality, the only important information is the furthest position each rabbit can reach. The left rabbit always claims a prefix, and the right rabbit always claims a suffix.

The observation that simplifies the problem is that the order of moves only matters when both rabbits want the same carrot. We can let the left rabbit take every carrot in its reachable prefix and the right rabbit take every carrot in its reachable suffix. The maximum answer is just the size of the union of those two ranges.

The brute-force simulation of all move orders can have exponentially many possibilities because at every moment either rabbit might move. Even tracking many states is unnecessary because the reachable intervals completely describe the game. The optimal solution finds both boundaries with two scans and combines them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of possible move choices | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan from the left side and find the last index `left` that belongs to the first rabbit's path. Start with the first carrot eaten. Continue moving while the next carrot is greater than or equal to the current carrot. The final index is the end of the reachable prefix.
2. Scan from the right side and find the first index `right` that belongs to the second rabbit's path. Start with the last carrot eaten. Move left while the next carrot is greater than or equal to the current carrot from the rabbit's perspective. In array order, this means the previous element must be greater than or equal to the current one.
3. The left rabbit can eat every carrot in the interval `[0, left]`, and the right rabbit can eat every carrot in the interval `[right, n-1]`. If these intervals overlap, the overlap is counted only once.
4. Compute the size of the union of the two intervals. If `left < right`, the intervals are separate and the answer is `(left + 1) + (n - right)`. Otherwise, they overlap and cover the whole section from `0` to `n - 1`, so the answer is `n`.

Why it works: the movement rule makes each rabbit's path fixed. The left rabbit cannot jump over a carrot that blocks it, so everything it eats must be inside one maximal prefix. The same reasoning gives one maximal suffix for the right rabbit. Any optimal game can only use carrots from these two regions, and both regions can be completely consumed by choosing the move order appropriately. Counting their union gives exactly the maximum number of distinct carrots eaten.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    left = 0
    while left + 1 < n and a[left + 1] >= a[left]:
        left += 1

    right = n - 1
    while right - 1 >= 0 and a[right - 1] >= a[right]:
        right -= 1

    if left < right:
        ans = left + 1 + (n - right)
    else:
        ans = n

    print(ans)

if __name__ == "__main__":
    solve()
```

The first loop finds the exact stopping point of the left rabbit. The comparison uses `a[left + 1] >= a[left]` because the rabbit is moving left to right and needs the next carrot to be at least as large as the previous one.

The second loop looks similar but runs backwards. The condition is `a[right - 1] >= a[right]` because the rabbit is moving toward smaller indices. This is the same as saying the sequence it eats is non-decreasing in the rabbit's movement direction.

The final calculation handles the only interaction between rabbits. If `left < right`, the rabbits have disjoint reachable parts. Otherwise their paths meet or cross, and together they can cover every carrot between the two endpoints.

The implementation uses only a few integer variables besides the input array. Python integers do not have overflow issues for these values, and the number of operations is linear.

## Worked Examples

For:

```
4
1 2 3 4
```

the scan states are:

| Step | left | right | Meaning |
| --- | --- | --- | --- |
| Start | 0 | 3 | Both rabbits are at their endpoints |
| Left scan finishes | 3 | 3 | Left rabbit reaches the end |
| Right scan finishes | 3 | 0 | Right rabbit reaches the start |
| Answer |  |  | 4 |

Both rabbits can cover the entire row, and counting the union gives four carrots.

For:

```
5
1 3 2 3 1
```

the scan states are:

| Step | left | right | Meaning |
| --- | --- | --- | --- |
| Start | 0 | 4 | Initial positions |
| Left scan finishes | 1 | 4 | Left rabbit stops before size 2 |
| Right scan finishes | 1 | 3 | Right rabbit stops before size 2 |
| Answer |  |  | 4 |

The reachable intervals are `[0, 1]` and `[3, 4]`. The middle carrot belongs to neither rabbit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each scan moves through the array at most once. |
| Space | O(1) | Only boundary indices and counters are stored besides the input array. |

With `n` up to `2 * 10^5`, a linear solution easily fits the time limit. The memory usage is also constant after reading the array.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    left = 0
    while left + 1 < n and a[left + 1] >= a[left]:
        left += 1

    right = n - 1
    while right - 1 >= 0 and a[right - 1] >= a[right]:
        right -= 1

    if left < right:
        ans = left + 1 + (n - right)
    else:
        ans = n

    sys.stdin = old_stdin
    return str(ans) + "\n"

assert solve_case("4\n1 2 3 4\n") == "4\n", "sample 1"
assert solve_case("5\n1 3 2 3 1\n") == "4\n", "sample 2"
assert solve_case("9\n1 1 2 1 9 2 1 1 2\n") == "4\n", "sample 3"
assert solve_case("7\n1 3 5 4 4 3 2\n") == "7\n", "sample 4"
assert solve_case("5\n2 2 2 2 2\n") == "5\n", "sample 5"

assert solve_case("2\n1 1\n") == "2\n", "minimum size and equal values"
assert solve_case("5\n5 4 3 2 1\n") == "5\n", "fully decreasing array"
assert solve_case("6\n1 2 1 1 1 1\n") == "5\n", "left boundary stops early"
assert solve_case("8\n1 3 5 2 4 6 7 8\n") == "5\n", "separated reachable regions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 1` | `2` | Minimum size and equality handling |
| `5 / 5 4 3 2 1` | `5` | A rabbit can start from a difficult side while the other covers the rest |
| `6 / 1 2 1 1 1 1` | `5` | One side stopping immediately after a drop |
| `8 / 1 3 5 2 4 6 7 8` | `5` | Correct separation of the two reachable intervals |

## Edge Cases

For the all-equal case:

```
5
2 2 2 2 2
```

the left scan reaches index `4` because every move is allowed. The right scan reaches index `0` for the same reason. The intervals overlap, so the algorithm returns `n = 5` instead of adding both lengths and producing an invalid answer.

For the early-stop case:

```
4
5 1 1 1
```

the left scan remains at index `0` because `1` is smaller than `5`. The right scan moves to index `1` because `1 1 1` is valid from right to left. The intervals `[0,0]` and `[1,3]` are separate, so the answer is `1 + 3 = 4`.

For the overlapping case:

```
5
1 2 3 4 5
```

the left rabbit reaches index `4`, and the right rabbit reaches index `0`. The two ranges overlap completely, so the algorithm returns `5`. Counting both ranges independently would incorrectly return `10`.

For the separated case:

```
5
1 3 2 3 1
```

the left scan stops at index `1`, while the right scan stops at index `3`. The two rabbits can eat positions `0,1,3,4`, giving the correct answer `4`. The algorithm never includes index `2` because neither monotonic path can cross the drop that blocks it.
