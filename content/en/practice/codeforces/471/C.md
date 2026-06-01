---
title: "CF 471C - MUH and House of Cards"
description: "A house of cards is built from floors. If a floor contains k rooms, then each room uses two leaning cards, so the rooms themselves consume 2k cards. Between adjacent rooms and above the outermost rooms there is a ceiling made of horizontal cards."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 471
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 269 (Div. 2)"
rating: 1700
weight: 471
solve_time_s: 102
verified: true
draft: false
---

[CF 471C - MUH and House of Cards](https://codeforces.com/problemset/problem/471/C)

**Rating:** 1700  
**Tags:** binary search, brute force, greedy, math  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

A house of cards is built from floors. If a floor contains `k` rooms, then each room uses two leaning cards, so the rooms themselves consume `2k` cards. Between adjacent rooms and above the outermost rooms there is a ceiling made of horizontal cards. A row of `k` rooms needs `k - 1` shared ceiling cards between neighboring rooms and one more ceiling card above each room position, which gives a total of `k - 1 + 1 = k` horizontal cards.

So a floor with `k` rooms uses:

$$2k + (k-1)=3k-1$$

cards.

The number of rooms must strictly decrease as we move upward through the house. If the floors contain

$$a_1 > a_2 > \dots > a_h \ge 1$$

rooms, then the total number of cards is

$$\sum_{i=1}^{h}(3a_i-1) = 3\sum a_i - h.$$

We are given exactly `n` cards and must count how many different heights `h` are possible. A height is valid if there exists a strictly decreasing positive sequence of room counts whose total card consumption is exactly `n`.

The constraint is the interesting part. `n` can be as large as `10^12`. Any approach that enumerates partitions or explores combinations of floor sizes is hopeless. Even `O(n)` is far too large. We need something closer to logarithmic or square-root complexity.

A subtle case occurs when there is no valid house at all. For example:

```
6
```

The smallest one-floor house uses `2` cards, the smallest two-floor house uses `7` cards, and no valid configuration consumes exactly `6`. The answer is `0`.

Another easy mistake is forgetting the strict decrease condition. Consider:

```
13
```

Using room counts `(2,2)` would consume `10` cards, but it is illegal because the floors are not strictly decreasing. Only strictly decreasing sequences are allowed.

A third source of bugs is counting different room distributions separately. The problem asks for the number of possible heights, not the number of houses. If several different floor configurations have the same height, they contribute only once.

## Approaches

A direct brute force interpretation is to generate all strictly decreasing sequences of positive integers, compute their card usage, and check whether it equals `n`. This is correct because every legal house corresponds to exactly one such sequence. Unfortunately, the number of decreasing sequences grows explosively. Even for moderate values of `n`, the search space resembles the number of integer partitions, which is far beyond what can be explored when `n` reaches `10^12`.

The key observation comes from rewriting the card formula:

$$n = 3\sum a_i - h.$$

Rearranging gives

$$\sum a_i = \frac{n+h}{3}.$$

For a fixed height `h`, the problem becomes:

Can we write

$$S=\frac{n+h}{3}$$

as a sum of `h` distinct positive integers?

This is a classic number-theoretic question.

The smallest possible sum of `h` distinct positive integers is obtained from

$$1+2+\cdots+h = \frac{h(h+1)}2.$$

Once we have such a set, increasing the largest element by any nonnegative amount preserves distinctness. Consequently, every integer sum at least

$$\frac{h(h+1)}2$$

is achievable.

So a height `h` is valid exactly when two conditions hold:

$$n+h \equiv 0 \pmod 3$$

and

$$\frac{n+h}{3}\ge \frac{h(h+1)}2.$$

The second inequality becomes

$$h^2+h \le \frac{2(n+h)}3.$$

After simplification:

$$3h^2+h-2n \le 0.$$

This immediately gives an upper bound of roughly

$$h \le \sqrt{\frac{2n}{3}},$$

which is under one million even for `n = 10^{12}`. We can simply test every possible height up to that bound.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(√n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate over all possible heights `h` starting from `1`.
2. Stop when `3h² + h > 2n`. For larger heights, the minimum required number of cards already exceeds `n`, so no further height can be valid.
3. Check whether `n + h` is divisible by `3`. If it is not, then `S = (n+h)/3` is not an integer and no house of height `h` exists.
4. If divisibility holds, verify the minimum-sum condition

$$\frac{n+h}{3} \ge \frac{h(h+1)}2.$$

This is equivalent to the derivation above.
5. If the condition is satisfied, increment the answer.
6. After all feasible heights have been tested, output the count.

### Why it works

For any height `h`, every legal house corresponds to a strictly decreasing sequence of `h` positive room counts. The total card formula transforms the problem into asking whether `(n+h)/3` can be represented as a sum of `h` distinct positive integers.

A sum of `h` distinct positive integers exists exactly when it is at least `1+2+\cdots+h`. Every larger value is obtainable by increasing the largest element while preserving distinctness. Thus the divisibility condition and the minimum-sum condition are both necessary and sufficient. The algorithm checks exactly these conditions for every feasible height, so every valid height is counted once and every invalid height is rejected.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    ans = 0
    h = 1

    while 3 * h * h + h <= 2 * n:
        if (n + h) % 3 == 0:
            s = (n + h) // 3
            if s >= h * (h + 1) // 2:
                ans += 1
        h += 1

    print(ans)

solve()
```

The variable `h` represents the height currently being tested.

The loop condition comes directly from the inequality

$$3h^2+h-2n \le 0.$$

Once it fails, even the minimum possible house of that height requires more cards than available, so no larger height can work either.

The divisibility check is performed before computing `s`. Without it, integer division would silently accept impossible cases.

The comparison against `h(h+1)/2` encodes the existence of a representation as a sum of `h` distinct positive integers. Since Python integers have arbitrary precision, there is no overflow risk even when `n = 10^{12}`.

## Worked Examples

### Example 1

Input:

```
13
```

| h | n+h | Divisible by 3? | S=(n+h)/3 | Minimum Sum h(h+1)/2 | Valid? |
| --- | --- | --- | --- | --- | --- |
| 1 | 14 | No | - | 1 | No |
| 2 | 15 | Yes | 5 | 3 | Yes |

The next height is impossible because `3·3²+3 = 30 > 26`.

Answer:

```
1
```

This demonstrates that only height `2` works, even though multiple floor layouts may exist.

### Example 2

Input:

```
6
```

| h | n+h | Divisible by 3? | S=(n+h)/3 | Minimum Sum h(h+1)/2 | Valid? |
| --- | --- | --- | --- | --- | --- |
| 1 | 7 | No | - | 1 | No |
| 2 | 8 | No | - | 3 | No |

The loop stops because `3·3²+3 = 30 > 12`.

Answer:

```
0
```

This example shows that having enough cards for some structures does not imply a valid house exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) | Heights are checked only up to the positive root of `3h²+h−2n≤0` |
| Space | O(1) | Only a few integer variables are stored |

For `n = 10^12`, the largest tested height is about `8 × 10^5`. A simple loop over that many values is easily within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        n = int(input())

        ans = 0
        h = 1

        while 3 * h * h + h <= 2 * n:
            if (n + h) % 3 == 0:
                s = (n + h) // 3
                if s >= h * (h + 1) // 2:
                    ans += 1
            h += 1

        return str(ans)

    return solve()

# provided sample
assert run("13\n") == "1", "sample 1"

# custom cases
assert run("1\n") == "0", "minimum input"
assert run("2\n") == "1", "single room house"
assert run("6\n") == "0", "no valid house"
assert run("7\n") == "1", "smallest two-floor house"
assert run("1000000000000\n").isdigit(), "large boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Below the minimum cards needed for any house |
| `2` | `1` | Smallest valid one-floor configuration |
| `6` | `0` | No valid representation exists |
| `7` | `1` | Smallest valid height-two house |
| `1000000000000` | Numeric answer | Performance near maximum constraint |

## Edge Cases

Consider the input:

```
1
```

The loop condition `3h²+h≤2n` already fails for `h=1` because `4>2`. No height is examined and the answer remains `0`. This correctly reflects that even a single room requires two cards.

Consider:

```
6
```

For `h=1`, `n+h=7`, which is not divisible by three. For `h=2`, `n+h=8`, which is also not divisible by three. No valid height exists. A careless implementation that only checked the minimum-card inequality would incorrectly accept some height.

Consider:

```
7
```

For `h=2`,

$$S=\frac{7+2}{3}=3.$$

The minimum sum of two distinct positive integers is also `3`, namely `1+2`. The condition is satisfied exactly at the boundary, producing one valid height. This case catches off-by-one mistakes where `>` is used instead of `>=`.

Finally, consider:

```
13
```

For `h=2`, we obtain `S=5`, which is larger than the minimum sum `3`. The representation `1+4` exists, giving a valid two-floor house. The algorithm counts the height once regardless of how many room distributions produce that height, matching the problem requirement.
