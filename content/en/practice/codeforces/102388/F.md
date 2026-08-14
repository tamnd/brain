---
title: "CF 102388F - Shopping"
description: "We have n coin denominations, and every denomination can be used any number of times. For a target amount m, a way of making change is determined only by how many coins of each denomination are used, not by the order in which those coins are written."
date: "2026-08-14T13:50:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102388
codeforces_index: "F"
codeforces_contest_name: "SUFE ICPC Team Formation Test"
rating: 0
weight: 102388
solve_time_s: 188
verified: false
draft: false
---

[CF 102388F - Shopping](https://codeforces.com/problemset/problem/102388/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We have `n` coin denominations, and every denomination can be used any number of times. For a target amount `m`, a way of making change is determined only by how many coins of each denomination are used, not by the order in which those coins are written. For example, with denominations `2` and `3`, the amount `6` has two ways: `2 + 2 + 2` and `3 + 3`.

For each test case, the input gives the number of denominations, the target amount, and the denomination values themselves. The required output is the number of distinct combinations whose total value is exactly `m`, reduced modulo `10^9 + 7`.

The constraints point directly toward dynamic programming. There are at most `100` denominations and the target is at most `10000`, so roughly `n * m = 10^6` state transitions per test case are affordable. With at most ten test cases, this is about `10^7` simple operations, which is reasonable in a compiled language and still practical in Python with a compact implementation. Anything exponential in `m` or the number of coin choices is completely out of reach.

The first edge case is a denomination larger than the target. For example,

```
1
2 3
4 5
```

has output `0`. Neither coin can participate in a valid sum, so a DP implementation must not accidentally treat the initial state `dp[0] = 1` as a way to make every target.

The second edge case is when a denomination is exactly equal to the target. For example,

```
1
1 5
5
```

has output `1`. The inner loop must include index `m`; using a range that stops at `m - 1` silently loses this solution.

The third edge case is unlimited reuse of a denomination. For example,

```
1
2 6
2 3
```

has output `2`, corresponding to `2 + 2 + 2` and `3 + 3`. Treating each denomination like a 0/1 item would miss both combinations because neither denomination can be used more than once.

The fourth edge case is that the input order must not affect the answer. For example,

```
1
2 6
3 2
```

also has output `2`. A correct coin-change DP uses an ascending target loop so that the current denomination can be reused during the same pass. A descending target loop would turn the transition into 0/1 knapsack behavior.

The formal statement describes the coin values as different. If duplicate values are nevertheless supplied, processing every input entry as a separate coin type counts them separately. For example, three entries of value `2` and target `6` give `10`, because the three types can contribute counts summing to `3` in `C(5,2) = 10` ways. Such an input is outside the stated constraints, but the implementation has a consistent interpretation of it.

## Approaches

A direct brute-force approach can recursively try every possible next coin and continue until the running sum reaches or exceeds `m`. To avoid counting different orders as different change combinations, it can keep the chosen coin indices nondecreasing, or equivalently generate all ordered sequences and canonicalize each one before inserting it into a set. This works conceptually because every valid combination can be generated and every invalid partial choice can eventually be rejected.

The problem is the number of candidates. Even the ordered-sequence version becomes enormous with just two denominations. For denominations `1` and `2`, the number of ordered sequences whose sum is `10000` is exactly the Fibonacci number `F_10001`, because a sequence ending in `1` comes from a sequence summing to `9999`, while one ending in `2` comes from a sequence summing to `9998`. `F_10001` has roughly `2090` decimal digits, so a brute-force search would need to generate on the order of `10^2089` terminal sequences before it could finish. Canonicalizing those sequences does not help, because the expensive generation has already happened.

The brute force works because every combination can be constructed by choosing coins, but it repeatedly solves the same smaller subproblems. For instance, once we know how many ways can make amount `8` using a certain prefix of the denominations, that result is needed again whenever another solution reaches the same state. The observation that these repeated subproblems are completely described by the amount already formed and the set of denominations allowed lets us store the answers instead of recomputing them.

This gives the standard unbounded coin-change dynamic programming formulation. Let `dp[x]` represent the number of ways to make amount `x` using only the denominations processed so far. When denomination `c` is introduced, every old way to make `x - c` can be extended by adding one `c` coin, giving a way to make `x`. The transition is therefore

`dp[x] += dp[x - c]`.

The direction of the inner loop is the key detail. We process `x` from `c` upward. Because `dp[x - c]` may already have been updated using the same coin, the current denomination can be used again, exactly matching the fact that there are infinitely many coins of each type.

The order of the outer denomination loop also gives us the crucial counting convention. A combination such as `2 + 3 + 5` is generated according to the fixed denomination order, rather than once for every permutation such as `3 + 5 + 2`. Each combination has exactly one representation in the DP state sequence, so it is counted once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `m` and the number of choices | Exponential in the number of generated states | Too slow |
| Optimal | `O(nm)` | `O(m)` | Accepted |

## Algorithm Walkthrough

1. Create an array `dp` of length `m + 1`, where `dp[x]` will eventually mean the number of ways to form amount `x`. Set `dp[0] = 1` and every other entry to zero. The empty selection is exactly one way to make amount zero, and every nonzero amount initially has no known representation.
2. Process the coin denominations one at a time. After processing a denomination, `dp[x]` counts combinations using only the denominations seen so far. This invariant prevents different orders of the same coins from becoming separate answers.
3. For a coin of value `c`, iterate `x` from `c` through `m` in increasing order. For every such amount, add `dp[x - c]` to `dp[x]`.
4. The transition is correct because every combination counted by `dp[x - c]` can receive one additional `c` coin and become a combination for `x`. Since the loop is ascending, `dp[x - c]` may already contain combinations that use `c`, so any number of copies of the current denomination is allowed.
5. Reduce each update modulo `10^9 + 7`. Only the residue is required by the problem, and reducing during the computation keeps the stored integers small.
6. After all denominations have been processed, output `dp[m]`. At this point the invariant says that it contains exactly all combinations of the available denominations whose total value is `m`.

### Why it works

The invariant is that after processing the first `k` denominations, `dp[x]` equals the number of combinations that form `x` using only those `k` denominations. Initially, with no denominations, only amount zero can be formed, giving `dp[0] = 1`. When denomination `c` is processed, every new combination using at least one `c` has a unique decomposition into a combination using the already processed denominations plus one final `c`. The ascending loop allows that preceding combination to contain any number of `c` coins, so every valid combination is added exactly once. Existing combinations that use no `c` remain untouched. Thus the invariant survives every denomination, and `dp[m]` at the end is exactly the required count.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())
        coins = list(map(int, input().split()))

        dp = [0] * (m + 1)
        dp[0] = 1

        for coin in coins:
            if coin > m:
                continue

            for amount in range(coin, m + 1):
                dp[amount] += dp[amount - coin]
                if dp[amount] >= MOD:
                    dp[amount] -= MOD

        print(dp[m])

if __name__ == "__main__":
    solve()
```

The first part reads each test case and creates one DP array for its target amount. The array has `m + 1` entries because amount zero is a real state and the target `m` must also be represented.

Setting `dp[0] = 1` is essential. When processing a coin equal to `x`, the transition uses `dp[x - coin] = dp[0]`, thereby creating the first solution consisting of exactly that coin. Without this initialization, every state would remain zero forever.

The outer loop processes denominations rather than amounts. This is what makes the DP count combinations instead of ordered sequences. Once a denomination has been processed, later denominations can be added, but earlier denominations are never reconsidered in a different order.

The inner loop starts at `coin`, because smaller amounts cannot contain this coin. It ends at `m`, inclusively, because a coin may itself be the complete target.

The inner loop must move upward. Consider `coin = 2` and `amount = 6`. By the time `dp[6]` is calculated, `dp[4]` has already incorporated the current coin, allowing `2 + 2` to be extended to `2 + 2 + 2`. A descending loop would read only the state from before the current coin was introduced and would incorrectly limit each denomination to one use.

Python integers do not overflow, but the modulo operation is still necessary because the required answer is modulo `10^9 + 7`. The conditional subtraction is enough because both operands are already below the modulus, so their sum is less than `2 * MOD`.

## Worked Examples

### Sample testcase 1

Consider the first testcase:

```
1 100
1
```

There is only one denomination, so the only possible representation of `100` is one hundred copies of the coin with value `1`.

| Processed coin | `dp[0]` | `dp[1]` | `dp[100]` |
| --- | --- | --- | --- |
| none | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 |

After processing coin `1`, the ascending loop repeatedly reuses the current denomination. Thus `dp[100] = 1`, and the output is `1`.

This trace demonstrates why the problem is an unbounded knapsack problem rather than a 0/1 knapsack problem. The same denomination must be usable one hundred times.

### Sample testcase 2

Now consider:

```
4 10
5 7 2 3
```

Start with `dp[0] = 1`. The table records selected states after each denomination has been fully processed.

| Processed coins | `dp[2]` | `dp[3]` | `dp[4]` | `dp[5]` | `dp[6]` | `dp[7]` | `dp[8]` | `dp[9]` | `dp[10]` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| 5, 7 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| 5, 7, 2 | 1 | 0 | 1 | 1 | 1 | 2 | 1 | 2 | 2 |
| 5, 7, 2, 3 | 1 | 1 | 1 | 2 | 2 | 3 | 3 | 4 | 5 |

The final value `dp[10] = 5` corresponds to the five combinations `5 + 5`, `7 + 3`, `5 + 3 + 2`, `3 + 3 + 2 + 2`, and five copies of `2`.

The state `dp[7]` after processing coin `3` is especially instructive. It contains `7`, `5 + 2`, and `3 + 2 + 2`. When the transition for amount `10` uses that state, it produces `7 + 3`, `5 + 2 + 3`, and `3 + 2 + 2 + 3`. This demonstrates how the current coin can be reused while still counting each unordered combination only once.

### Sample testcase 3

For:

```
3 100
1 2 3
```

the useful target states are:

| Processed coins | `dp[0]` | `dp[1]` | `dp[2]` | `dp[100]` |
| --- | --- | --- | --- | --- |
| none | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 |
| 1, 2 | 1 | 1 | 2 | 51 |
| 1, 2, 3 | 1 | 1 | 2 | 884 |

After coin `1`, every amount has exactly one representation. Adding coin `2` creates all partitions using only `1` and `2`, giving `51` ways for `100`. Adding coin `3` expands the set again, producing the required `884`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nm)` | Each of the `n` denominations scans amounts from its value through `m`, with at most `m` transitions. |
| Space | `O(m)` | Only the one-dimensional DP array of `m + 1` states is stored. |

With `n <= 100` and `m <= 10000`, one test case performs at most about one million DP updates. Even across ten test cases this is around ten million updates, while the memory usage is only about ten thousand Python integer references plus their integer objects. The solution comfortably avoids the exponential search space of brute force and fits the stated limits.

## Test Cases

```python
import sys
import io
from contextlib import redirect_stdout

MOD = 1000000007
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())
        coins = list(map(int, input().split()))

        dp = [0] * (m + 1)
        dp[0] = 1

        for coin in coins:
            if coin > m:
                continue

            for amount in range(coin, m + 1):
                dp[amount] += dp[amount - coin]
                if dp[amount] >= MOD:
                    dp[amount] -= MOD

        print(dp[m])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_input = globals()["input"]

    sys.stdin = io.StringIO(inp)
    globals()["input"] = sys.stdin.readline

    out = io.StringIO()
    try:
        with redirect_stdout(out):
            solve()
    finally:
        sys.stdin = old_stdin
        globals()["input"] = old_input

    return out.getvalue()

# Provided sample
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
""", "provided sample"

# Minimum-size input
assert run("""\
1
1 1
1
""") == "1\n", "minimum-size case"

# Maximum n and maximum m, with only one denomination able to reach m
max_coins = " ".join(map(str, range(9901, 10001)))
assert run(f"""\
1
100 10000
{max_coins}
""") == "1\n", "maximum-size case"

# Duplicate values, outside the formal distinct-denomination constraint.
# Three separate entries of value 2 give C(3 + 3 - 1, 3 - 1) = 10.
assert run("""\
1
3 6
2 2 2
""") == "10\n", "all-equal robustness case"

# Boundary case: coin value exactly equals the target.
assert run("""\
1
1 10000
10000
""") == "1\n", "coin equal to target"

# Unbounded reuse and coin-order independence.
# 6 can be 2+2+2 or 3+3.
assert run("""\
1
2 6
3 2
""") == "2\n", "unbounded and reversed order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / 1` | `1` | Minimum valid input and the `dp[0]` initialization |
| `100 10000` with denominations `9901..10000` | `1` | Maximum `n`, maximum `m`, and values larger than most of the target |
| `3 6 / 2 2 2` | `10` | Robustness when duplicate values are supplied, although duplicates are outside the formal constraint |
| `1 10000 / 10000` | `1` | Inclusive upper boundary of the inner loop |
| `2 6 / 3 2` | `2` | Unlimited reuse and independence from input denomination order |

## Edge Cases

A denomination larger than the target is handled by the condition `if coin > m: continue`. For the input

```
1
2 3
4 5
```

both denominations are skipped, so the array remains `dp[0] = 1` and `dp[1..3] = 0`. The algorithm prints `0`, correctly recognizing that no positive amount can be formed.

A denomination exactly equal to the target exercises the upper boundary. For

```
1
1 5
5
```

the loop runs with `amount = 5` and performs `dp[5] += dp[0]`. Since `dp[0] = 1`, the resulting `dp[5]` is `1`. The inclusive `m + 1` endpoint in `range(coin, m + 1)` is what makes this solution visible.

Unlimited reuse is handled by the ascending amount loop. For

```
1
2 6
2 3
```

processing coin `2` produces `dp[2] = 1`, then `dp[4] = dp[2] = 1`, then `dp[6] = dp[4] = 1`, representing three copies of `2`. Processing coin `3` subsequently creates `dp[6] += dp[3] = 1`, representing two copies of `3`. The final answer is `2`.

Finally, changing the input order does not change the combinations. For

```
1
2 6
3 2
```

coin `3` is processed first and creates the `3 + 3` solution. Coin `2` is then processed and creates `2 + 2 + 2`. Since each denomination is handled in a fixed outer-loop phase and can be reused only through the ascending inner loop, neither solution is duplicated. The result remains `2`.
