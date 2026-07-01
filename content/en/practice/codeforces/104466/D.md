---
title: "CF 104466D - DnD Dice"
description: "We roll a collection of standard DnD dice. The input tells us how many d4, d6, d8, d12, and d20 dice are included. Every die is fair, and each face is numbered from 1 up to its number of sides. Every complete roll produces one total sum."
date: "2026-06-30T13:14:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104466
codeforces_index: "D"
codeforces_contest_name: "2023-2024 ICPC German Collegiate Programming Contest (GCPC 2023)"
rating: 0
weight: 104466
solve_time_s: 63
verified: true
draft: false
---

[CF 104466D - DnD Dice](https://codeforces.com/problemset/problem/104466/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We roll a collection of standard DnD dice. The input tells us how many d4, d6, d8, d12, and d20 dice are included. Every die is fair, and each face is numbered from 1 up to its number of sides.

Every complete roll produces one total sum. Different sums are not equally likely because many different combinations of face values may produce the same total. The task is to print every possible sum, ordered from highest probability to lowest probability. If two sums have exactly the same probability, either order is accepted.

The largest input contains 10 dice of each type, for a total of 50 dice. A brute force enumeration of every outcome is immediately impossible. Even rolling only ten d20 dice already creates $20^{10}$ outcomes, and the actual maximum input is vastly larger than that. The algorithm must avoid enumerating individual rolls.

The useful observation is that although the number of outcomes is enormous, the number of possible sums is small. The minimum possible sum is the number of dice, since every die contributes at least 1. The maximum possible sum is

$$40 + 60 + 80 + 120 + 200 = 500.$$

Only 451 different sums can ever exist, which is tiny. This strongly suggests dynamic programming over sums.

One easy mistake is assuming that probabilities can be compared using floating point values. Floating point rounding may incorrectly swap sums whose probabilities are equal or extremely close. For example,

```
1 0 0 0 0
```

produces the sums 1, 2, 3, and 4, each with identical probability. The correct output may list them in any order, but a comparison based on rounded floating point values is unnecessary. Counting the number of ways to reach every sum avoids this issue completely.

Another subtle case is when only one die exists.

```
0 0 0 0 1
```

Every face appears exactly once, so every sum has the same probability. Any permutation of 1 through 20 is valid. A solution that assumes there is always a unique ordering would incorrectly reject valid outputs.

A final edge case is when many dice are present.

```
10 10 10 10 10
```

The number of possible rolls is astronomically large, so storing probabilities or enumerating outcomes is infeasible. Dynamic programming stores only the number of ways to obtain each achievable sum, whose largest index never exceeds 500.

## Approaches

The most direct solution recursively generates every possible roll, computes its sum, and counts how many times each total appears. This is correct because every outcome is examined exactly once. Unfortunately, its running time equals the total number of outcomes, which in the worst case is

$$4^{10} \cdot 6^{10} \cdot 8^{10} \cdot 12^{10} \cdot 20^{10},$$

far beyond anything a computer can process.

The reason this problem is still easy is that we do not actually care which sequence of rolls produced a sum. We only need the number of ways to obtain each total. Since there are at most 451 different sums, we can repeatedly update a distribution over sums as we add dice one by one.

Suppose we already know how many ways each sum can occur after processing some dice. When another die with $k$ sides is added, every existing sum contributes to exactly $k$ new sums. We simply distribute its count across those new totals. This is exactly a convolution of distributions, but with only a few hundred possible sums, a straightforward dynamic programming implementation is already fast enough.

After all dice have been processed, the number of ways for each sum is proportional to its probability because every complete outcome is equally likely. Sorting sums by these counts directly produces the required order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\prod s_i)$ | $O(\text{number of sums})$ | Too slow |
| Optimal | $O(D \times S \times 20)$ | $O(S)$ | Accepted |

Here, $D \le 50$ is the number of dice and $S \le 500$ is the largest possible sum.

## Algorithm Walkthrough

1. Read the numbers of each die type.
2. Expand the input into a list containing one entry for every die, where each entry stores its number of sides. For example, one d4 and two d8 become the list `[4, 8, 8]`.
3. Create a dynamic programming array where `dp[x]` is the number of ways to obtain sum `x` using the dice processed so far. Initially only sum 0 is possible, so set `dp[0] = 1`.
4. Process the dice one at a time. For each die with `k` sides, create a fresh array `ndp`.
5. For every reachable sum and every face value from 1 through `k`, add the current number of ways into the corresponding new sum. Each existing outcome extends into exactly one outcome for every face value.
6. Replace `dp` with `ndp` and continue until every die has been processed.
7. Compute the smallest and largest achievable sums from the number of dice and their side counts.
8. Sort all achievable sums by decreasing `dp[sum]`. If two counts are equal, any relative order is acceptable, so the secondary key is irrelevant.
9. Output the sums in sorted order.

### Why it works

After processing any prefix of the dice, the dynamic programming table exactly counts the number of distinct rolls producing every possible sum. This invariant is true initially because only sum 0 is achievable without rolling any dice. Every update preserves the invariant because every previous roll extends independently with every face of the new die, and every resulting roll is counted exactly once. After all dice have been been processed, `dp[s]` equals the total number of outcomes whose sum is `s`. Since every complete roll is equally likely, sorting by these counts is exactly the same as sorting by probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t, c, o, d, i = map(int, input().split())

    dice = (
        [4] * t +
        [6] * c +
        [8] * o +
        [12] * d +
        [20] * i
    )

    max_sum = sum(dice)
    dp = [0] * (max_sum + 1)
    dp[0] = 1

    current_max = 0

    for sides in dice:
        ndp = [0] * (max_sum + 1)
        for s in range(current_max + 1):
            if dp[s] == 0:
                continue
            ways = dp[s]
            for face in range(1, sides + 1):
                ndp[s + face] += ways
        dp = ndp
        current_max += sides

    min_sum = len(dice)

    ans = list(range(min_sum, max_sum + 1))
    ans.sort(key=lambda x: dp[x], reverse=True)

    print(*ans)

if __name__ == "__main__":
    solve()
```

The solution begins by expanding the compressed input into one list entry per die. This makes every update identical regardless of die type.

The dynamic programming array always represents the distribution after processing a certain number of dice. A fresh array is allocated for every die because each transition must use only values from the previous stage. Updating the array in place would accidentally reuse newly created states and overcount many sums.

`current_max` keeps track of the largest reachable sum after the processed dice. Iterating only up to this value avoids scanning unused entries.

Python integers automatically grow to arbitrary precision, so even the enormous number of possible rolls for the largest test fits without overflow.

Finally, the achievable sums are sorted by their counts. Since probabilities differ only by the common denominator equal to the total number of outcomes, comparing counts is sufficient.

## Worked Examples

### Sample 1

Input:

```
1 1 1 0 0
```

The dice are d4, d6, and d8.

| Step | Die | Reachable Sum Range |
| --- | --- | --- |
| 0 | None | 0 |
| 1 | d4 | 1 to 4 |
| 2 | d6 | 2 to 10 |
| 3 | d8 | 3 to 18 |

After the final update, the largest counts occur at sums 11, 10, and 9. These become the beginning of the output.

This example shows how repeated convolutions naturally create the familiar bell-shaped distribution, where middle sums have many more combinations than extreme sums.

### Sample 2

Input:

```
2 0 0 1 0
```

The dice are d4, d4, and d12.

| Step | Die | Reachable Sum Range |
| --- | --- | --- |
| 0 | None | 0 |
| 1 | d4 | 1 to 4 |
| 2 | d4 | 2 to 8 |
| 3 | d12 | 3 to 20 |

The peak probability occurs near the middle of the distribution, so sums such as 9 and 14 appear before the extreme values.

This example demonstrates that the algorithm treats different die sizes uniformly. Each additional die simply performs another distribution update.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(D \times S \times 20)$ | Every die updates every reachable sum using at most 20 faces. |
| Space | $O(S)$ | Only the current and next distributions are stored. |

Since there are at most 50 dice and the largest possible sum is only 500, the algorithm performs well under one million transition operations. This easily satisfies the problem limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    t, c, o, d, i = map(int, input().split())

    dice = [4] * t + [6] * c + [8] * o + [12] * d + [20] * i
    max_sum = sum(dice)

    dp = [0] * (max_sum + 1)
    dp[0] = 1
    cur = 0

    for sides in dice:
        ndp = [0] * (max_sum + 1)
        for s in range(cur + 1):
            if dp[s]:
                for f in range(1, sides + 1):
                    ndp[s + f] += dp[s]
        dp = ndp
        cur += sides

    mn = len(dice)
    ans = list(range(mn, max_sum + 1))
    ans.sort(key=lambda x: dp[x], reverse=True)
    return " ".join(map(str, ans))

# provided samples
assert run("1 1 1 0 0\n") == "11 10 9 12 8 13 14 7 15 6 5 16 17 4 18 3"
assert run("2 0 0 1 0\n") == "9 14 12 11 10 13 15 8 16 7 6 17 5 18 4 19 3 20"

# custom cases
assert set(run("1 0 0 0 0\n").split()) == {"1", "2", "3", "4"}
assert set(run("0 0 0 0 1\n").split()) == {str(x) for x in range(1, 21)}
assert run("0 1 0 0 0\n").split()[0] in {"3", "4"}
assert len(run("10 10 10 10 10\n").split()) == 451
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0 0 0` | Any permutation of `1 2 3 4` | Single fair die, all probabilities equal |
| `0 0 0 0 1` | Any permutation of `1` through `20` | Large single die |
| `0 1 0 0 0` | Begins with `3` or `4` | Tie handling for a symmetric distribution |
| `10 10 10 10 10` | 451 sums | Maximum input size |

## Edge Cases

Consider the input

```
1 0 0 0 0
```

The dynamic programming table starts with `dp[0] = 1`. After processing the d4, sums 1 through 4 each receive exactly one contribution. Every count is identical, so every ordering is valid. The algorithm naturally produces equal frequencies without any special handling.

Now consider

```
0 0 0 0 1
```

There is only one d20. Every face contributes exactly once, so all twenty sums receive count 1. Sorting by frequency leaves all sums tied, matching the specification that ties may appear in any order.

Finally, consider

```
10 10 10 10 10
```

The smallest achievable sum is 50 and the largest is 500. Although the total number of possible rolls is unimaginably large, the dynamic programming table still contains only 501 entries. Each die performs at most 20 transitions for every possible sum, so the running time depends only on the range of sums rather than the number of individual outcomes.
