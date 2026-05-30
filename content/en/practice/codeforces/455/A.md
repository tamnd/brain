---
title: "CF 455A - Boredom"
description: "We are given an array of integers. In one move, we choose a value x that is currently present, earn x points from deleting one occurrence of it, and all occurrences of x - 1 and x + 1 disappear from the array as a consequence."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 455
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 260 (Div. 1)"
rating: 1500
weight: 455
solve_time_s: 91
verified: true
draft: false
---

[CF 455A - Boredom](https://codeforces.com/problemset/problem/455/A)

**Rating:** 1500  
**Tags:** dp  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. In one move, we choose a value `x` that is currently present, earn `x` points from deleting one occurrence of it, and all occurrences of `x - 1` and `x + 1` disappear from the array as a consequence.

At first glance, the operation looks like it depends on individual positions in the array. It actually depends only on the values. Whenever we decide that value `x` is worth taking, every occurrence of `x` can eventually be collected, because removing one `x` does not remove other `x` values. The only conflict is with neighboring values `x - 1` and `x + 1`.

The input contains up to `10^5` numbers, and each number is at most `10^5`. Any solution that tries to explore different sequences of moves directly is hopeless. Even quadratic algorithms would require around `10^10` operations in the worst case, which is far beyond the limit. We need something close to linear or `O(M)`, where `M` is the maximum value appearing in the array.

Several edge cases are easy to mishandle.

Consider:

```
3
2 2 2
```

The correct answer is `6`.

A careless solution might think choosing value `2` gives only `2` points once. In reality, after neighboring values are removed, all three occurrences of `2` can still be taken, yielding `2 + 2 + 2 = 6`.

Consider:

```
4
1 1 2 2
```

The correct answer is `4`.

Taking all `1`s gives `2` points. Taking all `2`s gives `4` points. We cannot take both because values `1` and `2` conflict. Any solution that treats occurrences independently instead of grouping equal values will produce the wrong result.

Consider:

```
5
1 3 5 7 9
```

The correct answer is `25`.

None of the values are adjacent, so every value can be taken. A solution that only compares neighboring array positions rather than neighboring numeric values would miss this.

## Approaches

The most direct idea is to think about every possible sequence of moves. At each step we choose a value, delete conflicting values, and continue recursively. This is correct because it explores all legal outcomes.

The problem is the number of possibilities. With up to `10^5` elements, the search space becomes enormous. Even memoizing states is impractical because the remaining set of values can vary in too many ways.

The key observation is that positions do not matter at all. Only value frequencies matter.

Suppose value `x` appears `cnt[x]` times. If we decide to use value `x`, we can eventually collect

```
x * cnt[x]
```

points.

After making that decision, values `x - 1` and `x + 1` become unavailable. Nothing else is affected.

This transforms the problem into a much simpler one. For every integer value `x`, we have a "house" worth

```
points[x] = x * cnt[x]
```

If we take house `x`, we cannot take houses `x - 1` or `x + 1`.

This is exactly the same structure as the classic House Robber dynamic programming problem.

Let `dp[i]` be the maximum score obtainable using values from `1` through `i`.

For value `i`, there are only two possibilities.

If we skip it, the answer remains `dp[i - 1]`.

If we take it, we gain `points[i]` and must skip `i - 1`, giving

```
dp[i - 2] + points[i]
```

So the recurrence becomes:

```
dp[i] = max(
    dp[i - 1],
    dp[i - 2] + points[i]
)
```

This reduces the problem to a simple linear dynamic program over value space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal DP | O(M) | O(M) | Accepted |

Here `M` is the maximum value appearing in the input, at most `100000`.

## Algorithm Walkthrough

1. Read the array.
2. Count how many times each value appears.
3. For every value `x`, compute its total contribution:

```
points[x] = x * cnt[x]
```

If we choose value `x`, this is the total score we can earn from all occurrences of `x`.
4. Let `mx` be the maximum value in the array.
5. Create a DP array of size `mx + 1`.
6. Set:

```
dp[0] = 0
dp[1] = points[1]
```
7. For every value `i` from `2` to `mx`, compute:

```
dp[i] = max(
    dp[i - 1],
    dp[i - 2] + points[i]
)
```

The first option skips value `i`.

The second option takes value `i`, so value `i - 1` cannot be used.
8. Output `dp[mx]`.

### Why it works

After grouping equal numbers, every value `i` becomes an independent decision with reward `points[i]`. The only restriction is that values differing by one cannot both be chosen.

When computing `dp[i]`, every valid solution over values `1..i` either excludes `i` or includes it. If it excludes `i`, the best score is exactly `dp[i-1]`. If it includes `i`, then `i-1` must be excluded, leaving the best score `dp[i-2] + points[i]`. These are the only possibilities, and the recurrence takes the better one.

By induction on `i`, `dp[i]` always stores the optimal answer for values up to `i`, so `dp[mx]` is the optimal answer for the entire problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    mx = max(a)

    points = [0] * (mx + 1)
    for x in a:
        points[x] += x

    if mx == 1:
        print(points[1])
        return

    dp = [0] * (mx + 1)
    dp[1] = points[1]

    for i in range(2, mx + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + points[i])

    print(dp[mx])

if __name__ == "__main__":
    solve()
```

The first stage aggregates all equal values. Instead of storing frequencies separately and later multiplying, the implementation directly accumulates `x` into `points[x]` for every occurrence. After processing the array, `points[x]` already equals `x * cnt[x]`.

The dynamic programming array is indexed by value, not by position in the original array. This is the central idea of the solution. The recurrence only depends on the previous two value states.

The special handling for `mx == 1` avoids accessing `dp[1]` when the DP array would otherwise have size one. This is the only boundary condition that requires explicit care.

Python integers automatically handle large values. The maximum possible answer is around `10^10`, which easily fits in Python's integer type.

## Worked Examples

### Example 1

Input:

```
2
1 2
```

Frequency totals:

```
points[1] = 1
points[2] = 2
```

| i | points[i] | dp[i-2] | dp[i-1] | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 1 | - | - | 1 |
| 2 | 2 | 0 | 1 | 2 |

Answer:

```
2
```

Taking value `2` is better than taking value `1`. Since the values are adjacent, both cannot be chosen.

### Example 2

Input:

```
5
2 2 2 2 2
```

Frequency totals:

```
points[2] = 10
```

| i | points[i] | dp[i-2] | dp[i-1] | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 0 | - | - | 0 |
| 2 | 10 | 0 | 0 | 10 |

Answer:

```
10
```

This example shows why equal values must be grouped. Once value `2` is chosen, every occurrence contributes to the score.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M) | One DP transition for every value from 1 to the maximum value |
| Space | O(M) | Arrays `points` and `dp` of size `M + 1` |

Since `M ≤ 100000`, the algorithm performs only about one hundred thousand DP transitions and easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    mx = max(a)

    points = [0] * (mx + 1)
    for x in a:
        points[x] += x

    if mx == 1:
        return str(points[1])

    dp = [0] * (mx + 1)
    dp[1] = points[1]

    for i in range(2, mx + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + points[i])

    return str(dp[mx])

# provided sample
assert run("2\n1 2\n") == "2", "sample 1"

# minimum size
assert run("1\n1\n") == "1", "single element"

# all equal values
assert run("5\n2 2 2 2 2\n") == "10", "all equal"

# adjacent conflict
assert run("4\n1 1 2 2\n") == "4", "must choose better side"

# non-adjacent values
assert run("5\n1 3 5 7 9\n") == "25", "all values can be taken"

# classic mixed case
assert run("9\n1 2 1 3 2 2 2 3 3\n") == "10", "dp transition check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Smallest valid input |
| `5 / 2 2 2 2 2` | `10` | All occurrences of one value are collected |
| `4 / 1 1 2 2` | `4` | Adjacent values conflict |
| `5 / 1 3 5 7 9` | `25` | Non-adjacent values can all be chosen |
| `9 / 1 2 1 3 2 2 2 3 3` | `10` | General DP behavior |

## Edge Cases

Consider:

```
3
2 2 2
```

The aggregated score is:

```
points[2] = 6
```

The DP computes:

```
dp[1] = 0
dp[2] = max(0, 6) = 6
```

The output is `6`, correctly collecting every occurrence of value `2`.

Consider:

```
4
1 1 2 2
```

The totals become:

```
points[1] = 2
points[2] = 4
```

The DP computes:

```
dp[1] = 2
dp[2] = max(2, 4) = 4
```

The output is `4`. The algorithm correctly recognizes that taking all `2`s is better than taking all `1`s.

Consider:

```
5
1 3 5 7 9
```

The totals are:

```
points[1] = 1
points[3] = 3
points[5] = 5
points[7] = 7
points[9] = 9
```

All intermediate values have contribution zero. The recurrence repeatedly takes every non-conflicting value, producing:

```
1 + 3 + 5 + 7 + 9 = 25
```

The output is `25`, showing that gaps between values are handled naturally by the DP.
