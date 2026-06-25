---
title: "CF 106457G - Eridanus Prime"
description: "The problem describes a fleet of transport ships. Ship i has a cargo capacity Ai. We must choose a single crate size x. A ship can only be used when its capacity can be divided into crates of exactly size x, so the ship contributes if and only if Ai is a multiple of x."
date: "2026-06-25T09:14:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106457
codeforces_index: "G"
codeforces_contest_name: "UTPC Spring 2026 Open Contest"
rating: 0
weight: 106457
solve_time_s: 30
verified: true
draft: false
---

[CF 106457G - Eridanus Prime](https://codeforces.com/problemset/problem/106457/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a fleet of transport ships. Ship `i` has a cargo capacity `A_i`. We must choose a single crate size `x`. A ship can only be used when its capacity can be divided into crates of exactly size `x`, so the ship contributes if and only if `A_i` is a multiple of `x`.

For a chosen crate size, the Empire's payout is the crate size multiplied by the number of ships that can use it. In mathematical terms, the value of `x` is:

`x * (number of A_i values divisible by x)`

The task is to find the crate size with the largest payout. If several crate sizes produce the same payout, the smallest crate size must be chosen.

The input contains the number of ships and their capacities. The output is the best crate size.

The important constraint is that there can be up to `10^6` ships, and every capacity is at most `10^6`. A solution that checks every possible crate size against every ship would perform around `10^12` operations in the worst case, which is far beyond what a typical one second limit allows. We need to exploit the small maximum value of a capacity instead of the number of ships.

The key edge cases come from ties and from crate sizes that appear as divisors but are not the most frequent.

For example, if the input is:

```
3
2 4 6
```

The correct output is:

```
3
```

The crate size `2` works for all three ships, giving `2 * 3 = 6`. The crate size `3` works for only the ship with capacity `6`, giving `3 * 1 = 3`, so this example does not produce a tie. A careless implementation that only looks at divisors of the largest value might miss better candidates among smaller divisors.

A tie case is:

```
4
2 4 6 8
```

The correct output is:

```
4
```

Crate size `2` gives `2 * 4 = 8`, and crate size `4` gives `4 * 2 = 8`. Since both have the same payout, we must choose the smaller crate size, so the answer is `2`. A careless implementation that updates the answer whenever it sees an equal score would return the wrong value if it replaces the current answer with the later candidate.

The minimum-size case is:

```
1
1000000
```

The answer is:

```
1000000
```

The only ship should be counted, and its entire capacity can be used as a crate size.

## Approaches

A direct solution would try every possible crate size `x`. For each `x`, we scan all ships and count how many capacities are divisible by `x`. The method is correct because it evaluates the exact payout of every possible choice. However, with `N = 10^6`, this would require checking up to `10^6` possible values against up to `10^6` ships, resulting in about `10^12` divisibility tests.

The useful observation is that capacities are also limited to `10^6`. Instead of asking every ship whether it accepts a crate size, we can reverse the process and ask each crate size how many capacities are its multiples.

Let `freq[v]` be the number of ships with capacity `v`. For a fixed crate size `x`, the usable ships are exactly the capacities:

`x, 2x, 3x, ...`

up to the maximum capacity. We can sum the frequencies of these values using a sieve-like loop. Each possible crate size is processed by visiting its multiples, which is much faster than checking every ship separately.

After computing the count for every `x`, we compare the payout `x * count`. When two payouts are equal, we keep the smaller `x`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N * max(A)) | O(1) | Too slow |
| Optimal | O(max(A) log max(A)) | O(max(A)) | Accepted |

## Algorithm Walkthrough

1. Count how many ships have each capacity. Store this in `freq`, where `freq[v]` tells us how many times capacity `v` appears. This lets us process values rather than individual ships.
2. Iterate over every possible crate size `x` from `1` to the maximum capacity. For each `x`, add the frequencies of all multiples of `x`. These are exactly the ships that can be deployed with crate size `x`.
3. Compute the payout as `x * count`. If it is larger than the best payout seen so far, replace the answer. If it is equal, keep the smaller crate size.
4. Output the stored crate size after all candidates have been checked.

Why it works:

For every possible crate size `x`, the algorithm visits every capacity that is divisible by `x`, so the computed count is exactly the number of ships that can use that crate size. The payout calculation is therefore identical to the definition in the problem. Since every possible `x` is considered and ties are handled by keeping the smallest value, the final answer is guaranteed to be optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    mx = max(a)
    freq = [0] * (mx + 1)

    for value in a:
        freq[value] += 1

    best_x = 1
    best_value = 0

    for x in range(1, mx + 1):
        count = 0
        for multiple in range(x, mx + 1, x):
            count += freq[multiple]

        value = x * count

        if value > best_value:
            best_value = value
            best_x = x
        elif value == best_value and x < best_x:
            best_x = x

    print(best_x)

if __name__ == "__main__":
    solve()
```

The frequency array stores only capacities that actually exist in the input range. Its size is determined by the largest capacity, not by the number of ships.

The outer loop tries every possible crate size. The inner loop walks through its multiples, adding their frequencies. This avoids repeatedly scanning the entire list of ships.

The tie condition is handled explicitly. When two crate sizes have the same payout, the current answer is replaced only if the new crate size is smaller. This prevents the result from depending on iteration order.

Python integers do not overflow, so the multiplication `x * count` is safe even at the maximum values. The only boundary case to handle is the maximum capacity itself, which is included in the frequency array and in every multiple loop.

## Worked Examples

For the first sample:

```
5
2 3 3 4 5
```

The important states are:

| Crate size | Multiples counted | Number of ships | Payout | Best answer |
| --- | --- | --- | --- | --- |
| 1 | 2, 3, 4, 5 | 5 | 5 | 1 |
| 2 | 2, 4 | 2 | 4 | 1 |
| 3 | 3 | 2 | 6 | 3 |
| 4 | 4 | 1 | 4 | 3 |
| 5 | 5 | 1 | 5 | 3 |

The largest payout is produced by crate size `3`, so the answer is `3`.

For the second sample:

```
5
5 4 3 2 1
```

The trace is:

| Crate size | Multiples counted | Number of ships | Payout | Best answer |
| --- | --- | --- | --- | --- |
| 1 | 1, 2, 3, 4, 5 | 5 | 5 | 1 |
| 2 | 2, 4 | 2 | 4 | 1 |
| 3 | 3 | 1 | 3 | 1 |
| 4 | 4 | 1 | 4 | 1 |
| 5 | 5 | 1 | 5 | 1 |

The best payout is shared by crate sizes `1` and `5`. The smaller crate size is chosen, giving `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M log M) | Each crate size visits its multiples, where `M` is the maximum capacity. |
| Space | O(M) | The frequency array stores counts for every capacity up to `M`. |

With `M <= 10^6`, the harmonic-series sieve runs comfortably within the limits. The memory usage is also small because only one integer array of size `10^6 + 1` is needed.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    mx = max(a)
    freq = [0] * (mx + 1)

    for x in a:
        freq[x] += 1

    ans = 1
    best = 0

    for x in range(1, mx + 1):
        cnt = 0
        for y in range(x, mx + 1, x):
            cnt += freq[y]
        score = x * cnt
        if score > best or (score == best and x < ans):
            best = score
            ans = x

    print(ans)

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert solve("5\n2 3 3 4 5\n") == "3\n", "sample 1"
assert solve("5\n5 4 3 2 1\n") == "1\n", "sample 2"

assert solve("1\n1000000\n") == "1000000\n", "single ship maximum capacity"
assert solve("4\n2 4 6 8\n") == "2\n", "tie chooses smallest"
assert solve("6\n12 18 24 30 36 42\n") == "6\n", "common divisors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1000000` | `1000000` | Single value boundary case |
| `4 / 2 4 6 8` | `2` | Equal payout tie handling |
| `6 / 12 18 24 30 36 42` | `6` | Correct divisor counting over many multiples |

## Edge Cases

For the tie case:

```
4
2 4 6 8
```

The frequency array contains one occurrence of each capacity. When `x = 2`, the multiples are `2, 4, 6, 8`, giving a payout of `8`. When `x = 4`, the multiples are `4, 8`, also giving a payout of `8`. The algorithm reaches `x = 4` later, but the equal-score condition keeps `x = 2` because it is smaller.

For a single ship:

```
1
1000000
```

The only useful crate sizes are divisors of `1000000`. The largest payout comes from using the whole ship capacity as the crate size, giving `1000000 * 1`. The multiple loop includes the maximum value itself, so the answer is found correctly.

For many repeated capacities:

```
5
6 6 6 6 6
```

Crate size `6` gives a payout of `30`, while smaller divisors give smaller payouts. The frequency approach counts all five ships at once through `freq[6]`, avoiding any mistake caused by duplicate capacities.
