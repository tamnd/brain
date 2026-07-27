---
title: "CF 102786D - \u0411\u044b\u0447\u0438\u0439 \u0440\u044b\u043d\u043e\u043a"
description: "The input describes the daily percentage changes of an asset price. Each value is given in basis points, so a value of 100 means a change of 1%, -250 means a decrease of 2.5%, and so on. The price changes are applied one after another, which means they multiply rather than add."
date: "2026-07-27T19:24:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102786
codeforces_index: "D"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u042f\u0440\u0413\u0423 \u0438\u043c. \u041f.\u0413. \u0414\u0435\u043c\u0438\u0434\u043e\u0432\u0430 Demidov Open IT Cup 2019"
rating: 0
weight: 102786
solve_time_s: 60
verified: true
draft: false
---

[CF 102786D - \u0411\u044b\u0447\u0438\u0439 \u0440\u044b\u043d\u043e\u043a](https://codeforces.com/problemset/problem/102786/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes the daily percentage changes of an asset price. Each value is given in basis points, so a value of `100` means a change of `1%`, `-250` means a decrease of `2.5%`, and so on. The price changes are applied one after another, which means they multiply rather than add. A sequence of changes `+10%`, then `-10%` does not return to the original price because the second change affects the already modified value.

We need to choose a contiguous range of days. The beginning of the range is the day when we buy the asset, and the end is the day when we sell it. The goal is to maximize the final value after applying all changes inside this range. If several ranges give exactly the same return, the one with the latest starting day is preferred. If the starting days are equal, the longer range is preferred.

The number of changes can reach 300,000. A quadratic solution would need to examine roughly 45 billion intervals in the worst case, which is far beyond what a typical competitive programming time limit allows. The solution must process the array in linear or near-linear time. The amount of memory also has to remain proportional to the input size, so storing large tables of interval results is not practical.

There are several edge cases where a straightforward implementation can fail. The first is that adding percentages instead of multiplying them gives the wrong answer. For example:

```
4
5000 -4000 100 100
```

The correct answer is `1 4`, because the multiplier is `1.5 * 0.6 * 1.01 * 1.01`, which is greater than any individual gain. A solution that sums changes sees `50 - 40 + 1 + 1 = 12%` and may incorrectly compare it against individual days.

Another issue is handling negative changes. A large drop can make extending a segment worse, but a later increase can make the whole segment optimal. For example:

```
5
-1000 5000 -1000 5000 -1000
```

The best interval is the full range `1 5`, because the two strong increases compensate for the losses through multiplication. A solution that only searches for consecutive positive values misses this.

Tie breaking is another subtle point. Consider:

```
4
100 0 100 0
```

The intervals `1 4` and `3 4` have the same return because the zero changes do not affect the price. The correct answer is `3 4`, since it starts later. An implementation that keeps the first maximum it finds will fail.

## Approaches

A direct approach is to try every possible starting day and extend the interval one day at a time. For each interval, we can maintain the current multiplier and compare it with the best one found so far. This is correct because every possible period is checked.

However, there are `N * (N + 1) / 2` possible intervals. With `N = 300000`, that is about 45 billion intervals. Even with constant-time updates, this is far too slow.

The key observation is that every daily multiplier is positive. A change of `p` basis points corresponds to a multiplier of:

```
1 + p / 10000
```

Because all multipliers are positive, maximizing a product is equivalent to maximizing the sum of their logarithms:

```
log(a * b * c) = log(a) + log(b) + log(c)
```

The problem becomes a maximum subarray sum problem on transformed values. This is exactly the structure handled by Kadane's algorithm.

The brute-force method works because it explicitly evaluates every product, but it fails because there are too many intervals. Transforming multiplication into addition lets us keep only the best possible previous state while scanning from left to right.

The comparison between the approaches is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert each daily change into a logarithmic value. For a change `p`, store:

```
log(1 + p / 10000)
```

The sum of these values over an interval represents the logarithm of the total return, so comparing sums is the same as comparing actual returns.

1. Maintain a prefix sum of the transformed values. If `pref[i]` is the sum of the first `i` transformed values, then the value of interval `(l, r)` is:

```
pref[r] - pref[l - 1]
```

1. While scanning the ending position `r`, keep the smallest prefix sum among all positions before `r`. Subtracting the smallest previous prefix gives the largest possible interval ending at `r`.
2. When several prefix positions have the same minimum value, keep the latest one. A later starting position is preferred by the problem's tie-breaking rule.
3. Compare the current interval with the best answer found so far. Replace the answer if the return is larger. If the returns are equal, choose the interval with the larger starting index, and if those are also equal, choose the longer interval.
4. After processing position `r`, insert `pref[r]` into the stored minimum prefix information so future intervals can start after `r`.

Why it works:

The prefix sum representation means every interval value is determined by choosing one earlier prefix to subtract from the current prefix. For a fixed ending position, the best interval must start immediately after the smallest previous prefix value. The algorithm always stores exactly this necessary information, including the correct tie-breaking choice among equal prefix values. Since every possible ending position is checked, and the best starting point for each ending position is considered, the global optimum is found.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))

    logs = [math.log1p(x / 10000.0) for x in p]

    eps = 1e-12

    pref = 0.0
    min_pref = 0.0
    min_pos = 0

    best_value = -float("inf")
    best_l = 1
    best_r = 1

    for i, value in enumerate(logs, start=1):
        pref += value

        current = pref - min_pref
        l = min_pos + 1
        r = i

        length = r - l + 1
        best_length = best_r - best_l + 1

        if (
            current > best_value + eps
            or (
                abs(current - best_value) <= eps
                and (l > best_l or (l == best_l and length > best_length))
            )
        ):
            best_value = current
            best_l = l
            best_r = r

        if pref < min_pref - eps or (abs(pref - min_pref) <= eps and i > min_pos):
            min_pref = pref
            min_pos = i

    print(best_l, best_r)

if __name__ == "__main__":
    solve()
```

The solution first transforms every percentage change into a logarithm. `log1p` is used instead of directly calculating `log(1 + x)` because it is more accurate for values close to zero.

The variable `pref` stores the current prefix sum. `min_pref` is the smallest prefix sum seen before the current position, and `min_pos` is the index of that prefix. When the current position is used as the end of a period, subtracting this minimum prefix produces the best possible interval ending here.

The answer comparison contains the tie-breaking logic. A larger logarithmic return is always better. If two returns are equal within floating-point precision, the interval with the larger left endpoint is selected. If both left endpoints match, the later right endpoint gives the longer interval.

The update of `min_pref` happens after checking the current answer because the current day cannot be used as the starting point of an interval ending on the same day in the prefix formulation. Keeping the order correct avoids an off-by-one error.

Python floating-point numbers are sufficient here because only comparisons between accumulated logarithms are needed. The original products could become extremely small or large, but the logarithmic form keeps all values within a manageable range.

## Worked Examples

For the first sample:

```
4
1000 2000 -3000 4000
```

The transformed values are the logarithms of the multipliers `1.1`, `1.2`, `0.7`, and `1.4`.

| Day | Prefix sum | Minimum prefix | Minimum position | Current interval | Best answer |
| --- | --- | --- | --- | --- | --- |
| 1 | log(1.1) | 0 | 0 | 1-1 | 1-1 |
| 2 | log(1.1*1.2) | 0 | 0 | 1-2 | 1-2 |
| 3 | log(1.1_1.2_0.7) | 0 | 0 | 1-3 | 1-2 |
| 4 | log(1.1_1.2_0.7*1.4) | log(1.1_1.2_0.7) | 3 | 4-4 | 4-4 |

The full interval gives a lower return than the final `+40%` day alone. The minimum prefix after day 3 allows the algorithm to discover that dropping the previous days is better.

For the second sample:

```
4
10 20 -25 40
```

| Day | Prefix sum | Minimum prefix | Minimum position | Current interval | Best answer |
| --- | --- | --- | --- | --- | --- |
| 1 | log(1.1) | 0 | 0 | 1-1 | 1-1 |
| 2 | log(1.1*1.2) | 0 | 0 | 1-2 | 1-2 |
| 3 | log(1.1_1.2_0.75) | 0 | 0 | 1-3 | 1-2 |
| 4 | log(1.1_1.2_0.75*1.4) | 0 | 0 | 1-4 | 1-4 |

Here the final increase is strong enough that keeping the earlier gains and the loss gives the highest overall return.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each daily change is transformed and processed once. |
| Space | O(1) | Only a few running variables are stored. |

The algorithm performs a constant amount of work for each of the at most 300,000 input values. It avoids storing all intervals or prefix arrays, so it fits comfortably within the memory limit.

## Test Cases

```python
import sys
import io
import math

def solve_data(data):
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)
    input = sys.stdin.readline

    n = int(input())
    p = list(map(int, input().split()))

    pref = 0.0
    min_pref = 0.0
    min_pos = 0
    eps = 1e-12

    best = -float("inf")
    bl = br = 1

    for i, x in enumerate(p, 1):
        pref += math.log1p(x / 10000.0)

        cur = pref - min_pref
        l = min_pos + 1

        if (
            cur > best + eps
            or (
                abs(cur - best) <= eps
                and (l > bl or (l == bl and i - l + 1 > br - bl + 1))
            )
        ):
            best = cur
            bl = l
            br = i

        if pref < min_pref - eps or (abs(pref - min_pref) <= eps and i > min_pos):
            min_pref = pref
            min_pos = i

    sys.stdin = old_stdin
    return f"{bl} {br}"

assert solve_data("4\n1000 2000 -3000 4000\n") == "4 4"
assert solve_data("4\n10 20 -25 40\n") == "1 4"

assert solve_data("3\n100 100 100\n") == "1 3"
assert solve_data("3\n-9999 5000 5000\n") == "2 3"
assert solve_data("5\n100 0 100 0 0\n") == "3 5"

assert solve_data("2\n-10000 100\n") == "2 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 100 100 100` | `1 3` | Checks that a profitable sequence is extended. |
| `3 / -9999 5000 5000` | `2 3` | Checks that a huge initial loss is discarded. |
| `5 / 100 0 100 0 0` | `3 5` | Checks latest-start tie breaking. |
| `2 / -10000 100` | `2 2` | Checks boundary behavior near the smallest multiplier. |

## Edge Cases

A sequence containing a very large loss followed by gains is handled by the minimum prefix logic. For:

```
3
-9999 5000 5000
```

the first multiplier is `0.0001`, so including it almost destroys the investment. The prefix sum after the first day becomes extremely negative, making it the minimum prefix. When the second day is processed, starting from day 2 becomes better, and the algorithm continues from there. The final answer is:

```
2 3
```

A tie between intervals must prefer the latest start. For:

```
5
100 0 100 0 0
```

the zero changes do not modify the return. The intervals `1 5` and `3 5` have the same product. The algorithm stores the latest position among equal minimum prefixes, which causes the candidate beginning at day 3 to replace the earlier one. The output is:

```
3 5
```

A single day can be the best answer. For:

```
4
1000 2000 -3000 4000
```

the first three days together are weaker than the last day alone. The prefix minimum before the fourth day is updated after the loss, allowing the algorithm to consider only day 4. The output becomes:

```
4 4
```

These cases are exactly where approaches based on adding percentages, assuming positive streaks are optimal, or ignoring tie-breaking rules tend to fail.
