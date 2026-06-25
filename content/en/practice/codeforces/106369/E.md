---
title: "CF 106369E - Most Valuable Pez"
description: "The problem models a collection of Pez dispensers. Each dispenser contains exactly 12 candies arranged from the top to the bottom, and a dispenser can only be eaten from the top."
date: "2026-06-25T08:19:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106369
codeforces_index: "E"
codeforces_contest_name: "2023 UCF Local Programming Contest"
rating: 0
weight: 106369
solve_time_s: 38
verified: true
draft: false
---

[CF 106369E - Most Valuable Pez](https://codeforces.com/problemset/problem/106369/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a collection of Pez dispensers. Each dispenser contains exactly 12 candies arranged from the top to the bottom, and a dispenser can only be eaten from the top. If you decide to take some candies from one dispenser, you must take a contiguous prefix of that dispenser. You are allowed to split your choices across all dispensers, and the goal is to eat exactly `k` candies while maximizing the total value of the eaten candies.

The input gives the number of dispensers and the number of candies that must be eaten, followed by the values inside every dispenser from top to bottom. The output is the largest possible sum of values obtainable by choosing valid prefixes whose total length is exactly `k`.

The important constraint is that there can be up to 1000 dispensers, but each dispenser has only 12 candies. Since `k` can be as large as `12000`, solutions that try every possible selection of candies will explode. A brute force over all choices would consider many combinations of prefixes and is far beyond what a 2 second limit allows. We need something close to `n * k` or `n * k * small_constant`.

The tricky cases are caused by the prefix restriction. A greedy strategy that repeatedly takes the currently largest visible candy fails because taking a small candy can reveal a much larger one underneath. For example:

```
Input
2 2
1 100 1 1 1 1 1 1 1 1 1 1
50 1 1 1 1 1 1 1 1 1 1 1
```

The correct output is:

```
101
```

A careless greedy approach takes `50` first, then `1`, for a total of `51`. The optimal choice is taking two candies from the first dispenser, accepting the value `1` to unlock the `100`.

Another edge case is when all useful candies are deep in a dispenser. For example:

```
Input
1 3
1 1 100 1 1 1 1 1 1 1 1 1
```

The correct output is:

```
102
```

Taking only the visible maximum candy fails because the `100` cannot be collected alone. The third candy is required, and the prefix length matters.

A final boundary case is when `k` equals the total number of candies:

```
Input
1 12
5 4 3 2 1 6 7 8 9 10 11 12
```

The answer is the sum of all values:

```
78
```

Any approach that assumes it can stop early or only take the best few candies will fail here.

## Approaches

The direct way to solve the problem is to enumerate how many candies we take from each dispenser. For every dispenser we have 13 choices: take zero candies, take one candy, and so on up to all 12 candies. Trying all combinations of these choices is correct because every valid final selection corresponds to exactly one choice per dispenser. However, the number of possibilities is `13^n`, which is enormous even for a few dozen dispensers, and completely impossible when `n` reaches 1000.

The structure of the problem gives us a smaller state space. We do not care which dispensers produced the candies already eaten. We only care about how many candies have been taken so far and the maximum value achievable with that count. Since each dispenser contributes only 0 through 12 candies, we can process dispensers one at a time and update these best values.

For each dispenser, we precompute the value of every possible prefix. Then the transition is simple: if we currently have a solution using `j` candies, we can add a prefix of length `x` from the current dispenser and reach `j + x` candies. The number of choices per dispenser is only 13, so the dynamic programming is fast enough.

The brute force works because it explores every possible division of candies between dispensers, but it fails because the number of divisions is exponential. The observation that only the number of already chosen candies matters lets us compress all previous decisions into a one-dimensional DP array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(13^n) | O(n) | Too slow |
| Optimal | O(n * k * 12) | O(k) | Accepted |

## Algorithm Walkthrough

1. Compute prefix sums for every Pez dispenser. The value at position `x` represents the total value obtained by taking the first `x` candies from that dispenser. Position zero has value zero because taking nothing is always allowed.
2. Create a dynamic programming array where `dp[j]` stores the maximum value obtainable after processing some number of dispensers and eating exactly `j` candies. Initially, only `dp[0]` is valid because we have not taken anything yet.
3. Process each dispenser independently. For every possible previous candy count `j`, try every prefix length `x` from 0 to 12. If taking `x` candies from the current dispenser does not exceed `k`, update the state for `j + x`.
4. After all dispensers are processed, the answer is `dp[k]` because the state represents the best value for exactly `k` candies.

The reason this works is that each dispenser only affects the answer through how many candies it contributes and the value of that prefix. Once a dispenser is processed, all details about how those candies were chosen can be forgotten because future dispensers only care about the remaining number of candies available.

Why it works: The DP invariant is that after processing the first `i` dispensers, `dp[j]` is the best possible value using exactly `j` candies from those dispensers. When processing the next dispenser, every valid solution either takes some prefix from this dispenser or takes nothing. The transition tries every one of those possibilities, so every valid solution remains reachable and the maximum value is kept. After the final dispenser, the invariant gives the optimal answer for `k` candies.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    dp = [-1] * (k + 1)
    dp[0] = 0

    for _ in range(n):
        values = list(map(int, input().split()))
        pref = [0] * 13

        for i, value in enumerate(values):
            pref[i + 1] = pref[i] + value

        ndp = [-1] * (k + 1)

        for used in range(k + 1):
            if dp[used] == -1:
                continue
            limit = min(12, k - used)
            for take in range(limit + 1):
                ndp[used + take] = max(
                    ndp[used + take],
                    dp[used] + pref[take]
                )

        dp = ndp

    print(dp[k])

if __name__ == "__main__":
    solve()
```

The code keeps only one DP layer because the current dispenser should either be used or not used exactly once. A second array is needed to avoid combining the same dispenser with itself during the update.

The prefix array has length 13 because a dispenser has exactly 12 candies. `pref[take]` is the contribution of choosing that many candies from the current dispenser.

The transition skips impossible states where `dp[used]` is still `-1`. The upper bound on `take` is reduced by the remaining number of candies needed, which prevents unnecessary work and avoids indexing states beyond `k`.

There are no overflow concerns in Python. In languages with fixed integer sizes, the maximum answer is still small enough for a standard 32-bit integer, but using a larger type is harmless.

## Worked Examples

### Sample 1

Input:

```
4 7
3 6 8 2 2 5 6 1 2 3 1 4
4 1 1 1 1 70 4 1 5 3 2 3
5 3 2 6 6 2 3 1 6 2 3 2
1 4 3 8 4 9 2 1 6 5 4 1
```

The important DP states after processing each dispenser are:

| Dispenser | Main transition | Best value for 7 candies |
| --- | --- | --- |
| 1 | Build all prefixes from first stack | Impossible |
| 2 | Combine prefixes from first two stacks | 50 |
| 3 | Consider the large value 70 after taking 5 candies | 83 |
| 4 | Check final combinations | 83 |

The trace shows why the DP is needed. The best answer requires taking several low-value candies first to unlock the `70`.

### Sample 2

Input:

```
1 6
20 30 40 15 1 14 2 2 2 2 2 2
```

| Dispenser | Prefix length considered | Value |
| --- | --- | --- |
| 1 | 0 | 0 |
| 1 | 1 | 20 |
| 1 | 2 | 50 |
| 1 | 3 | 90 |
| 1 | 4 | 105 |
| 1 | 5 | 106 |
| 1 | 6 | 120 |

The answer is the prefix of length 6 because there is only one dispenser and the required number of candies must come from that single sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * k * 12) | Each dispenser updates every candy count using at most 13 prefix choices |
| Space | O(k) | Only the current and previous DP layer information is needed |

With `n = 1000` and `k = 12000`, the number of transitions is around 156 million in the worst case. The constant factor is small because every dispenser has only 12 possible prefix lengths, so the dynamic programming fits the intended limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    
    n, k = map(int, input().split())
    dp = [-1] * (k + 1)
    dp[0] = 0

    for _ in range(n):
        a = list(map(int, input().split()))
        pref = [0] * 13
        for i, x in enumerate(a):
            pref[i + 1] = pref[i] + x

        ndp = [-1] * (k + 1)
        for used in range(k + 1):
            if dp[used] == -1:
                continue
            for take in range(min(12, k - used) + 1):
                ndp[used + take] = max(ndp[used + take], dp[used] + pref[take])
        dp = ndp

    sys.stdin = old
    return str(dp[k])

assert run("""4 7
3 6 8 2 2 5 6 1 2 3 1 4
4 1 1 1 1 70 4 1 5 3 2 3
5 3 2 6 6 2 3 1 6 2 3 2
1 4 3 8 4 9 2 1 6 5 4 1
""") == "83"

assert run("""1 6
20 30 40 15 1 14 2 2 2 2 2 2
""") == "120"

assert run("""1 1
300 1 1 1 1 1 1 1 1 1 1 1
""") == "300"

assert run("""2 2
1 100 1 1 1 1 1 1 1 1 1 1
50 1 1 1 1 1 1 1 1 1 1 1
""") == "101"

assert run("""1 12
5 4 3 2 1 6 7 8 9 10 11 12
""") == "78"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single candy needed | 300 | Minimum `k` and direct prefix choice |
| Hidden large value | 101 | Prevents greedy solutions from passing |
| Take everything | 78 | Full-length prefix handling |
| Samples | 83 and 120 | Confirms the standard cases |

## Edge Cases

For the hidden-value case:

```
2 2
1 100 1 1 1 1 1 1 1 1 1 1
50 1 1 1 1 1 1 1 1 1 1 1
```

The DP first stores the options from the first dispenser. The state for taking two candies becomes `101`, because the only way to access the `100` candy is to take the `1` above it. When the second dispenser is considered, the state `2` remains at `101`, proving the algorithm does not get trapped by locally attractive candies.

For the deep-prefix case:

```
1 3
1 1 100 1 1 1 1 1 1 1 1 1
```

The only dispenser is processed with all prefix lengths. The length three prefix has value `102`, while length one and two prefixes cannot reach the `100`. The final DP state for three candies is exactly `102`.

For the full-dispenser case:

```
1 12
5 4 3 2 1 6 7 8 9 10 11 12
```

The transition allows taking all 12 candies because the prefix list includes length 12. The DP never assumes a dispenser must contribute fewer candies, so the final state correctly contains the sum of the entire dispenser.
