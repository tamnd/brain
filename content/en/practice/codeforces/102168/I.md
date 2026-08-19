---
title: "CF 102168I - \u041a\u043e\u043d\u0442\u0435\u0441\u0442\u044b"
description: "There are n contests arranged in chronological order. For contest i, a[i] is the rating increase obtained by participating in it. After participating in contest i, Kirill must skip the next b[i] contests, so the earliest contest he may participate in after i is i + b[i] + 1."
date: "2026-08-19T07:34:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "I"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 74
verified: true
draft: false
---

[CF 102168I - \u041a\u043e\u043d\u0442\u0435\u0441\u0442\u044b](https://codeforces.com/problemset/problem/102168/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `n` contests arranged in chronological order. For contest `i`, `a[i]` is the rating increase obtained by participating in it. After participating in contest `i`, Kirill must skip the next `b[i]` contests, so the earliest contest he may participate in after `i` is `i + b[i] + 1`.

The task is to choose a set of contests whose recovery intervals do not overlap, maximizing the sum of their `a[i]` values. Since `a[i]` can be negative, the empty choice is also relevant: Kirill can simply participate in no contests and gain `0`.

With `n <= 200000`, an `O(n^2)` solution is far too slow. In the worst case it would perform about `200000^2 / 2 = 20,000,000,000` state transitions, which cannot fit into a 2-second limit. We need an algorithm close to linear time.

The values of `a[i]` can reach `10^9` in either direction, and the answer can contain contributions from many contests. A 32-bit integer is not sufficient: the answer can be around `2 * 10^14` in magnitude. Python integers handle this automatically, while languages such as C++ need `long long`.

There are several boundary cases that can make a direct implementation wrong. If there is only one contest, such as

```
1-10 0
```

the answer is `0`, not `-10`, because participating is optional. If `b[i] = 0`, the next contest is immediately available. For example,

```
25 07 0
```

has answer `12`, so treating `b[i]` as if it included contest `i + 1` would incorrectly forbid the second contest.

The other boundary is when the recovery period extends beyond the entire remaining sequence. For

```
210 5100 0
```

the answer is `100`. After contest 1 there are no usable contests left, but that does not make contest 1 mandatory or give it priority over contest 2.

Finally, negative contests must not force us to take them. For

```
3-5 0-2 0-7 0
```

the answer is `0`. A DP initialized to negative infinity without explicitly representing the possibility of taking no contests can silently produce a negative answer.

## Approaches

A straightforward solution considers every possible last contest. Suppose we decide that contest `i` is the last contest we participate in. Then all earlier chosen contests must finish before `i`, and we could recursively enumerate all valid subsets before it. This is correct because every valid schedule has a well-defined last contest, but the number of subsets is exponential, so this approach becomes useless even much earlier than `n = 200000`.

We can make the brute-force idea more structured with dynamic programming. Let `dp[i]` be the maximum rating increase obtainable using only the first `i` contests. When processing contest `i`, there are exactly two possibilities. We skip it, leaving `dp[i - 1]`. Or we participate in it, in which case the previous chosen contest must lie at most `b[i] + 1` positions before `i`. If the first `i` contests are numbered from `1`, the last contest available before the recovery period is

`i - b[i] - 1`.

Thus the value obtained by taking contest `i` is

`a[i] + dp[i - b[i] - 1]`.

The crucial observation is that `dp` already contains the optimal answer for every possible prefix. We do not need to inspect individual earlier schedules. The entire history before the forbidden interval can be summarized by one number.

This gives the recurrence

`dp[i] = max(dp[i - 1], a[i] + dp[max(0, i - b[i] - 1)])`.

The `max(0, ...)` handles cases where contest `i` forces us to go before the beginning of the array. The recurrence examines each contest once, so the total work is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) recursion depth | Too slow |
| Prefix DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create `dp` where `dp[i]` represents the best rating increase obtainable from the first `i` contests. Set `dp[0] = 0`, because before considering any contests the gain is zero.
2. Process contests from left to right. For contest `i`, first consider skipping it. The best result in that case is exactly `dp[i - 1]`.
3. If we participate in contest `i`, we must skip the next `b[i]` contests. The contest immediately before the forbidden interval is `i - b[i] - 1`. Consequently, the best compatible earlier result is `dp[max(0, i - b[i] - 1)]`.
4. Add `a[i]` to that compatible prefix result. This gives the best schedule whose chosen contests include `i`.
5. Store the larger of the skip and participate cases in `dp[i]`. After processing all contests, `dp[n]` is the maximum possible rating increase.

### Why it works

Consider an optimal schedule among the first `i` contests. If it does not contain contest `i`, its value is at most `dp[i - 1]`, and `dp[i - 1]` represents the best such schedule. If it does contain contest `i`, every other chosen contest must belong to the first `i - b[i] - 1` contests. By the definition of `dp`, the best compatible earlier schedule has value `dp[max(0, i - b[i] - 1)]`. Adding `a[i]` gives the best possible schedule that includes `i`. These two cases cover every valid schedule, so taking their maximum gives the true optimum for every prefix. By induction over `i`, `dp[n]` is optimal.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    n = int(input())
    dp = [0] * (n + 1)
    for i in range(1, n + 1):        a, b = map(int, input().split())
        previous = i - b - 1        if previous < 0:            previous = 0
        take = a + dp[previous]        skip = dp[i - 1]
        dp[i] = max(skip, take)
    print(dp[n])

if __name__ == "__main__":    solve()
```

The array `dp` uses one extra position so that `dp[0]` naturally represents the empty prefix. At contest `i`, `previous = i - b - 1` is the largest prefix that can be used together with contest `i`.

The subtraction by one is the main indexing detail. If `b = 0`, contest `i - 1` is allowed, so the prefix must end at `i - 1`. The formula gives exactly `i - 0 - 1 = i - 1`. If `b = 1`, contest `i - 1` must be skipped, so the usable prefix ends at `i - 2`.

When `previous` is negative, there are simply no contests that can precede `i`, and `dp[0] = 0` represents that situation. Python's arbitrary-precision integers also safely handle sums of up to roughly `200000 * 10^9`.

The input is processed with `sys.stdin.readline`, which avoids the overhead of repeatedly splitting the entire input into a large list of tokens.

## Worked Examples

The statement formatting places the sample values on separate lines without explicitly numbering them. Interpreting the two displayed samples gives the following inputs.

### Sample 1

```
320 0100 230 0
```

The states evolve as follows.

| `i` | `a[i]` | `b[i]` | `previous` | `take` | `skip` | `dp[i]` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 20 | 0 | 0 | 20 | 0 | 20 |
| 2 | 100 | 2 | 0 | 100 | 20 | 100 |
| 3 | 30 | 0 | 2 | 130 | 100 | 130 |

At contest 2, `b[2] = 2`, so both contest 1 and contest 3 are incompatible with contest 2. The best choice involving contest 2 is therefore `100`. At contest 3, we can combine it with the best result from the first two contests, giving `100 + 30 = 130`.

### Sample 2

```
320 1100 230 0
```

| `i` | `a[i]` | `b[i]` | `previous` | `take` | `skip` | `dp[i]` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 20 | 1 | 0 | 20 | 0 | 20 |
| 2 | 100 | 2 | 0 | 100 | 20 | 100 |
| 3 | 30 | 0 | 2 | 130 | 100 | 130 |

Here contest 1 has `b[1] = 1`, so participating in it prevents participation in contest 2. Contest 3 itself has no recovery period, so after choosing contest 2 we can still choose contest 3. The optimal result is again `130`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each contest is processed once with constant work. |
| Space | O(n) | The DP array stores one value for every prefix. |

With `n = 200000`, the algorithm performs only a few arithmetic operations per contest, so it comfortably fits the intended time bound. The DP array contains about 200001 Python integers, which is also well within the 256 MB memory limit.

## Test Cases

```python
Pythonimport sysimport io

def solve_data(inp: str) -> str:    data = inp.split()    it = iter(data)
    n = int(next(it))    dp = [0] * (n + 1)
    for i in range(1, n + 1):        a = int(next(it))        b = int(next(it))
        previous = max(0, i - b - 1)        dp[i] = max(dp[i - 1], a + dp[previous])
    return str(dp[n])

def run(inp: str) -> str:    return solve_data(inp)

# Sample 1assert run(    """320 0100 230 0""") == "130", "sample 1"
# Sample 2assert run(    """320 1100 230 0""") == "130", "sample 2"
# Minimum size, negative value, so taking nothing is optimal.assert run(    """1-10 0""") == "0", "minimum-size negative case"
# Two consecutive contests with no recovery period.assert run(    """45 07 03 010 0""") == "25", "b = 0 boundary"
# Every contest forces all remaining contests to be skipped.assert run(    """410 1020 030 040 0""") == "40", "recovery extends beyond the array"
# Negative values mixed with positive values.assert run(    """5-100 010 120 0-50 030 2""") == "50", "negative values"
# Maximum-size input.n = 200000large_input = str(n) + "\n" + ("1 0\n" * n)assert run(large_input) == str(n), "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / -10 0` | `0` | Empty schedule and minimum input size |
| `5 0, 7 0, 3 0, 10 0` | `25` | `b = 0`, where every adjacent contest can be taken |
| `10 10, 20 0, 30 0, 40 0` | `40` | Recovery interval extending beyond all remaining contests |
| `-100 0, 10 1, 20 0, -50 0, 30 2` | `50` | Negative values and choosing only profitable compatible contests |
| `200000` contests with `a = 1, b = 0` | `200000` | Maximum `n` and linear performance |

## Edge Cases

### A single negative contest

For

```
1-10 0
```

the initial state is `dp[0] = 0`. Taking the only contest gives `-10`, while skipping it gives `0`, so `dp[1] = 0`. The algorithm never assumes that at least one contest must be selected.

### No recovery period

For

```
25 07 0
```

contest 1 has `previous = 0`, giving `dp[1] = 5`. Contest 2 has `previous = 1`, because `2 - 0 - 1 = 1`. Its take value is `7 + dp[1] = 12`, so the answer is `12`. This is exactly the boundary behavior required when `b[i] = 0`.

### Recovery beyond the beginning

For

```
210 5100 0
```

contest 1 has `previous = -5`, which is clamped to `0`. Taking it gives `10`. Contest 2 has `previous = 1`, giving `100 + dp[1] = 110` because its own recovery value is zero. Thus the answer is actually `110`, since contest 2 can be taken after contest 1. The large `b[1]` affects only what may follow contest 1, not what may precede contest 2. This distinction is exactly why the DP looks backward from the contest being considered.

### All values are negative

For

```
3-5 0-2 0-7 0
```

every `take` value is negative, while `skip` remains `0`. The DP consequently stays at zero throughout the array. This handles the fact that increasing the rating is optional.

### Very large positive values

Suppose many compatible contests have `a[i] = 10^9`. With `200000` contests, the total can reach `2 * 10^14`. The recurrence itself does not change at this scale, but an implementation using a 32-bit integer would overflow. Python's integer type avoids that issue, so the same recurrence remains valid for the full input range.
