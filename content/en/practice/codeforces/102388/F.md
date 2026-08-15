---
title: "CF 102388F - Shopping"
description: "We have n coin denominations, and each denomination can be used any number of times. For a target amount m, we need to count how many different multisets of coins sum exactly to m. The order of the coins does not matter, so 2 + 3 and 3 + 2 represent the same way of making change."
date: "2026-08-15T08:29:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102388
codeforces_index: "F"
codeforces_contest_name: "SUFE ICPC Team Formation Test"
rating: 0
weight: 102388
solve_time_s: 512
verified: true
draft: false
---

[CF 102388F - Shopping](https://codeforces.com/problemset/problem/102388/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` coin denominations, and each denomination can be used any number of times. For a target amount `m`, we need to count how many different multisets of coins sum exactly to `m`. The order of the coins does not matter, so `2 + 3` and `3 + 2` represent the same way of making change. The answer is reported modulo `1,000,000,007`.

For example, with denominations `2, 3, 5, 7` and target `10`, the valid combinations are `3 + 7`, `5 + 5`, `2 + 3 + 5`, `2 + 2 + 3 + 3`, and five copies of `2`, giving an answer of `5`.

The target is at most `10,000`, while there can be at most `100` denominations. That strongly suggests a dynamic programming solution around `n * m`, which is at most about one million state updates per test case. With at most ten test cases, this remains practical in Python with a compact one-dimensional DP. A solution that enumerates all possible combinations is not remotely feasible, because even a single denomination can be used up to `m` times and the number of combinations grows rapidly as more denominations are added.

The denomination values can also be as large as `10,000`. Any denomination larger than `m` can never participate in a valid combination, so processing it is unnecessary. The statement describes the denominations as different, but deduplicating them in the implementation makes the algorithm robust if repeated values are supplied. Repeated identical denominations should not create different ways, because a way is determined by the values and multiplicities of the coins, not by which input position supplied a coin.

There are several edge cases where a careless implementation can silently count the wrong thing. With

```
1
1 3
5
```

the answer is `0`, because the only available coin is already larger than the target. A recurrence that blindly indexes `dp[amount - coin]` without checking the boundary can access an invalid state.

With

```
1
2 5
2 3
```

the answer is `1`, from `2 + 3`. A common mistake is to update the DP in the wrong order and accidentally count different permutations of the same coins. The two sequences `2 + 3` and `3 + 2` must not become separate answers.

With

```
1
2 4
2 2
```

the answer is `1` if duplicate denominations are interpreted as the same coin value. Treating the two input entries as independent coin types would count the same monetary combination in multiple ways. The original problem promises different denominations, but deduplication avoids that ambiguity.

Finally, with

```
1
1 1
1
```

the answer is `1`. The empty sum is represented by `dp[0] = 1`, and adding the denomination `1` must turn that into exactly one way to form amount `1`. Initializing the DP array with zero everywhere would lose this fundamental base case.

## Approaches

A direct brute-force approach is to choose how many copies of every denomination are used and test whether the resulting sum is `m`. For denomination `c_i`, its count can range from zero through `floor(m / c_i)`, so the number of combinations examined is

`product(floor(m / c_i) + 1)`.

This is correct because every possible multiset of coins corresponds to exactly one choice of those counts. The problem is the size of that search space. In the worst case, if all denominations are `1`, there are theoretically `10001^100` choices of counts, although duplicate denominations are not allowed by the original statement. Even with distinct small denominations, the search space becomes enormous. A recursive enumeration therefore fails long before reaching `n = 100` and `m = 10000`.

A more subtle brute-force strategy generates every ordered sequence of coins whose sum does not exceed `m`, then keeps only sequences reaching exactly `m`. This is even worse because the same combination appears in many permutations. For instance, `2 + 3 + 5` can be generated in six different orders. The actual problem asks for one answer for that combination, so exploring order creates work that the problem does not need.

The key observation is that the target amount is bounded by `10,000`, so we do not need to remember the entire collection of coins chosen so far. We only need to know how many ways each smaller amount can be formed. Once the denominations have been processed in a fixed order, we can decide whether to append the current denomination to an already counted combination.

Let `dp[x]` be the number of ways to form amount `x` using the denominations processed so far. When processing a coin of value `c`, every way to form `x - c` can be extended by one `c` coin to form `x`. Thus we add `dp[x - c]` to `dp[x]`.

The order of the loops is what makes this count combinations rather than permutations. We process denominations in the outer loop and amounts in increasing order in the inner loop. Once denomination `c` is being processed, `dp[x - c]` already contains ways that may use `c`, which allows unlimited copies. At the same time, every denomination is introduced in one fixed stage, so the same combination cannot be generated again in a different order.

The brute-force works because it explicitly considers every possible multiplicity of every coin, but fails when there are too many such choices. The observation that two partial solutions with the same current amount have identical future possibilities lets us merge them into one DP state. That reduces the problem to `O(nm)` transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(product(m / c_i + 1))` in the worst case | `O(n)` recursion depth | Too slow |
| Optimal | `O(nm)` | `O(m)` | Accepted |

## Algorithm Walkthrough

1. Read the denominations and remove duplicate values if any are present. A denomination represents a coin value, so duplicate copies of the same value do not create distinct ways to make change.
2. Ignore every denomination greater than `m`. Such a coin can never appear in a valid sum equal to `m`, so processing it cannot change the answer.
3. Create a one-dimensional array `dp` of length `m + 1` and initialize every entry to zero. Set `dp[0] = 1`. There is exactly one way to make amount zero, namely to choose no coins. This base case is what allows the first actual coin to start a combination.
4. Process each denomination `c` one at a time. For the current denomination, iterate `x` from `c` through `m` in increasing order and perform `dp[x] += dp[x - c]` modulo `1,000,000,007`.
5. The increasing order of `x` deliberately allows `dp[x - c]` to already include the current denomination. For example, while processing coin `2`, the update for `dp[4]` can use the newly updated `dp[2]`, representing two copies of `2`. If the amounts were processed in decreasing order, each denomination could be used at most once.
6. After all denominations have been processed, `dp[m]` contains the number of different combinations whose total value is exactly `m`. Print that value modulo `1,000,000,007`.

### Why it works

The invariant is that after processing the first `k` denominations, `dp[x]` equals the number of combinations that form exactly `x` using only those `k` denominations. When processing a new denomination `c`, every old combination forming `x` remains available, and every combination that uses at least one `c` can be uniquely obtained by removing one `c`, leaving a combination counted by `dp[x - c]`. Thus the update adds exactly the new combinations introduced by `c`.

Because denominations are processed in a fixed order, a combination has a unique point at which its largest-indexed denomination is introduced. It cannot be counted again through another permutation of the same coins. Because amounts are processed from small to large, the current denomination may be used repeatedly, so all valid multiplicities are included. The invariant consequently holds after every denomination, and `dp[m]` is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        coins = list(map(int, input().split()))

        # The original statement has distinct denominations.
        # Deduplication also makes the implementation robust to repeated values.
        coins = sorted(set(c for c in coins if c <= m))

        dp = [0] * (m + 1)
        dp[0] = 1

        for coin in coins:
            for amount in range(coin, m + 1):
                dp[amount] += dp[amount - coin]
                if dp[amount] >= MOD:
                    dp[amount] -= MOD

        out.append(str(dp[m]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input is read once per test case, and the denominations are filtered and deduplicated before the DP starts. Sorting is not required for correctness, but gives the coin set a deterministic order and makes it easy to process denominations consistently.

The DP array has indices `0` through `m`, so its size is exactly `m + 1`. `dp[0] = 1` represents the unique empty combination. No other initial state should be set to a nonzero value.

For each coin, the inner loop starts at `coin`, because amounts below the coin value cannot use that denomination. It ends at `m`, because amounts larger than the target cannot contribute to `dp[m]`.

The inner loop moves upward. This is the most important implementation detail. Suppose the current coin is `2`. After computing `dp[2]`, the later update for `dp[4]` reads that updated value, so two copies of `2` are allowed. If the loop moved downward, the current coin would not be visible in the same iteration, turning the recurrence into a zero-or-one usage transition.

Python integers do not overflow, but taking every update modulo `MOD` keeps the stored values small and directly implements the required modular arithmetic. Since both operands are already below `MOD`, one subtraction is enough after addition to keep the result in the range `[0, MOD)`.

## Worked Examples

### Sample case: denominations 5, 7, 2, 3, target 10

The denominations can be processed in the input order. The following table shows the relevant DP state after each denomination has been fully processed.

| Processed coins | `dp[0]` | `dp[2]` | `dp[3]` | `dp[4]` | `dp[5]` | `dp[6]` | `dp[7]` | `dp[8]` | `dp[9]` | `dp[10]` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| 5, 7 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| 5, 7, 2 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 2 |
| 5, 7, 2, 3 | 1 | 1 | 1 | 1 | 2 | 2 | 2 | 2 | 3 | 5 |

After processing coin `2`, `dp[10] = 2`, representing `5 + 5` and `2 + 2 + 2 + 2 + 2`. When coin `3` is added, the other three combinations appear: `3 + 7`, `2 + 3 + 5`, and `2 + 2 + 3 + 3`. The final value is `5`, matching the sample.

The trace demonstrates both parts of the invariant. Every state represents combinations rather than ordered sequences, while the upward amount loop permits unlimited copies of each denomination.

### Sample case: denominations 101, 102, 103, 104, target 100

Every denomination is larger than the target, so filtering leaves no usable coins.

| Processed coin | DP initialization | Final `dp[100]` |
| --- | --- | --- |
| none | `dp[0] = 1`, all other states `0` | 0 |
| 101 | ignored | 0 |
| 102 | ignored | 0 |
| 103 | ignored | 0 |
| 104 | ignored | 0 |

The answer is `0`, because no available coin can be placed into a sum of `100`. This exercises the boundary where every denomination exceeds the target and confirms that the DP does not need any special case beyond filtering those coins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nm)` | Each usable denomination updates at most `m` DP states. |
| Space | `O(m)` | Only the current one-dimensional DP array is stored. |

With `n <= 100` and `m <= 10000`, there are at most about one million elementary DP transitions per test case. Even with ten test cases, the total is on the order of ten million transitions, which fits the intended constraints. The memory consumption is about `10,001` Python integers for the largest target, well within the 256 MB limit.

## Test Cases

```python
import sys
import io

MOD = 1_000_000_007

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        coins = list(map(int, input().split()))

        coins = sorted(set(c for c in coins if c <= m))

        dp = [0] * (m + 1)
        dp[0] = 1

        for coin in coins:
            for amount in range(coin, m + 1):
                dp[amount] += dp[amount - coin]
                if dp[amount] >= MOD:
                    dp[amount] -= MOD

        out.append(str(dp[m]))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample = """\
5
1 100
1
4 10
5 7 2 3
3 100
1 2 3
4 100
101 102 103 104
5 10000
5 4 3 2 1
"""

assert run(sample) == """\
1
5
884
0
649632988
""", "provided samples"

assert run("""\
1
1 1
1
""") == "1\n", "minimum target with the only usable coin"

assert run("""\
1
1 10000
9999
""") == "0\n", "coin is smaller than target but cannot divide it"

assert run("""\
1
2 5
2 3
""") == "1\n", "boundary combination 2 + 3"

assert run("""\
1
2 4
2 2
""") == "1\n", "duplicate denominations must not multiply the answer"

assert run("""\
1
100 10000
""" + " ".join(["1"] * 100) + "\n") == "1\n", \
    "maximum n and m with repeated denomination values"

assert run("""\
1
3 10
11 12 13
""") == "0\n", "every coin exceeds the target"

assert run("""\
1
3 6
2 3 6
""") == "3\n", "exact target and multiple combination sizes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / 1` | `1` | Minimum-size input and the `dp[0]` base case |
| `1 / 1 10000 / 9999` | `0` | A usable-looking denomination that cannot actually reach the target |
| `1 / 2 5 / 2 3` | `1` | Exact boundary combination and correct inclusive DP endpoint |
| `1 / 2 4 / 2 2` | `1` | Duplicate denomination handling |
| `1 / 100 10000 / 100 copies of 1` | `1` | Maximum `n` and maximum `m` |
| `1 / 3 10 / 11 12 13` | `0` | All denominations larger than the target |
| `1 / 3 6 / 2 3 6` | `3` | Several different multiplicities reaching the exact target |

## Edge Cases

### A denomination larger than the target

Consider

```
1
1 3
5
```

The coin `5` is discarded because `5 > 3`. The DP remains `[1, 0, 0, 0]`, so `dp[3] = 0`. The algorithm does not attempt to access `dp[3 - 5]`, avoiding a negative-indexing bug in Python.

### Order must not create different combinations

Consider

```
1
2 5
2 3
```

Initially `dp[0] = 1`. Processing coin `2` produces one way for amounts `2` and `4`, corresponding to `2` and `2 + 2`. Processing coin `3` then uses those states, so `dp[5]` receives one contribution from `dp[2]`, representing `2 + 3`. There is no second contribution corresponding to `3 + 2`, because the denomination `2` was already processed before `3`. The output is exactly `1`.

### Repeated denomination values

Consider

```
1
2 4
2 2
```

After deduplication, the coin list is just `[2]`. The DP produces `dp[4] = 1`, corresponding to `2 + 2`. Without deduplication, treating the two equal values as separate coin types would make the same monetary combination appear through different input positions. The statement guarantees distinct denominations, so this case is outside the official input model, but the implementation handles it safely.

### The empty combination as the DP base case

For

```
1
1 1
1
```

the initial state is `dp[0] = 1`. Processing coin `1` updates `dp[1]` from `dp[0]`, giving `dp[1] = 1`. The one way is a single `1` coin. If `dp[0]` were initialized to zero, no amount would ever become reachable, because every transition would depend on an unreachable state.

### Exact boundary at the target

Consider

```
1
3 6
2 3 6
```

Processing `2` gives one way to make `2`, `4`, and `6`. Processing `3` adds `3` and `6`, while the amount `6` also receives the combination `3 + 3`. Finally, coin `6` adds the direct combination `[6]`. The three distinct combinations are `2 + 2 + 2`, `3 + 3`, and `6`, so the answer is `3`.

The loop `range(coin, m + 1)` includes `m` itself. Stopping at `m - 1` would miss every combination whose final update creates the target directly, including the single coin `6` in this example.
