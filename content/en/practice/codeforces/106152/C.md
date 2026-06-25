---
title: "CF 106152C - Buffet Line"
description: "We have a line of food items, and each item has a desirability value. For every item, we can either take it or skip it. The restriction is that we are not allowed to take two neighboring items. If we choose item i, then item i+1 must be skipped."
date: "2026-06-25T11:25:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106152
codeforces_index: "C"
codeforces_contest_name: "UT 104c Midterm #2"
rating: 0
weight: 106152
solve_time_s: 41
verified: true
draft: false
---

[CF 106152C - Buffet Line](https://codeforces.com/problemset/problem/106152/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of food items, and each item has a desirability value. For every item, we can either take it or skip it.

The restriction is that we are not allowed to take two neighboring items. If we choose item `i`, then item `i+1` must be skipped.

The task is to find the largest possible total desirability obtainable under this rule. The input consists of the number of food items and their desirability values. The output is a single integer, the maximum achievable total desirability.

The constraint `n ≤ 10000` is small enough that an `O(n²)` solution would already perform around 100 million operations in the worst case, which is unnecessarily expensive. Since the problem only asks about adjacent positions, it strongly suggests a dynamic programming solution where each position depends on a constant number of previous positions. An `O(n)` solution is the natural target.

A common mistake is to greedily take the larger value from every adjacent pair. Local choices do not necessarily lead to the best global answer.

Consider:

```
3
2 1 2
```

The correct answer is:

```
4
```

We take the first and third items. A greedy strategy that only looks at neighboring values may miss this combination.

Another edge case is when there is only one item.

```
1
42
```

The answer is:

```
42
```

A DP implementation that blindly accesses `dp[i-2]` without handling small indices can fail here.

A third edge case occurs when many values are zero.

```
5
0 0 0 0 0
```

The answer is:

```
0
```

The algorithm must correctly handle situations where taking nothing is effectively optimal.

## Approaches

The brute-force approach is to examine every subset of food items, check whether it contains adjacent selected positions, and compute its desirability sum. This is correct because it explicitly considers every valid choice.

The problem is that there are `2^n` subsets. Even for `n = 50`, this is already far beyond what can be computed in time, and the actual limit is `n = 10000`.

The key observation is that when we stand at position `i`, there are only two meaningful possibilities.

Either we skip item `i`, in which case the best answer up to `i` is exactly the best answer up to `i-1`.

Or we take item `i`, in which case item `i-1` cannot be taken. The best achievable value becomes the best answer up to `i-2` plus the desirability of item `i`.

This means the decision at position `i` depends only on two previously computed states. That structure is exactly what dynamic programming is designed for.

Let `dp[i]` denote the maximum desirability obtainable using the first `i` items.

Then:

```
dp[i] = max(
    dp[i-1],
    dp[i-2] + value[i]
)
```

Every state is computed once, giving a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(1) | Too slow |
| Optimal DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and the desirability values.
2. Handle the base case `n = 1` by returning the only value.
3. Create a DP array where `dp[i]` stores the maximum desirability obtainable from the first `i` items.
4. Set `dp[0] = 0`, representing an empty prefix.
5. Set `dp[1] = value[0]`, since with only one item the best choice is to take it.
6. For every position `i` from `2` to `n`, compute:

```
dp[i] = max(
    dp[i-1],
    dp[i-2] + value[i-1]
)
```

The first option skips the current item. The second option takes it and combines it with the best valid solution ending at least one position earlier.
7. Output `dp[n]`.

### Why it works

The invariant is that `dp[i]` always stores the optimal answer for the first `i` items.

For the `i`-th item, every valid solution belongs to exactly one of two groups.

Either the item is not chosen, giving value `dp[i-1]`, or it is chosen, forcing item `i-1` to be excluded and giving value `dp[i-2] + value[i]`.

Since these are the only possibilities and we take the larger of them, `dp[i]` is optimal. By induction, every state is correct, including the final answer `dp[n]`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

if n == 1:
    print(a[0])
else:
    dp = [0] * (n + 1)

    dp[0] = 0
    dp[1] = a[0]

    for i in range(2, n + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + a[i - 1])

    print(dp[n])
```

The DP array uses 1-based indexing for convenience. `dp[i]` refers to the first `i` items, while the original array remains 0-based.

The transition uses `a[i - 1]` because the `i`-th DP state corresponds to the element stored at index `i - 1`.

The most common implementation mistake is mixing the array indexing systems and accidentally using `a[i]`, which shifts every value by one position and causes incorrect results or index errors.

The initialization is also important. `dp[0]` represents taking nothing from an empty prefix, while `dp[1]` represents the best answer for the first item.

## Worked Examples

### Example 1

Input:

```
5
3 8 10 2 0
```

| i | Current Value | dp[i-2] + value | dp[i-1] | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 3 | - | - | 3 |
| 2 | 8 | 8 | 3 | 8 |
| 3 | 10 | 13 | 8 | 13 |
| 4 | 2 | 10 | 13 | 13 |
| 5 | 0 | 13 | 13 | 13 |

Final answer:

```
13
```

The optimal choice is taking values `3` and `10`.

### Example 2

Input:

```
7
0 9 10 2 0 0 0
```

| i | Current Value | dp[i-2] + value | dp[i-1] | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 0 | - | - | 0 |
| 2 | 9 | 9 | 0 | 9 |
| 3 | 10 | 10 | 9 | 10 |
| 4 | 2 | 11 | 10 | 11 |
| 5 | 0 | 10 | 11 | 11 |
| 6 | 0 | 11 | 11 | 11 |
| 7 | 0 | 11 | 11 | 11 |

Final answer:

```
11
```

This example shows that sometimes taking a smaller value later creates a better overall combination.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each DP state is computed once |
| Space | O(n) | The DP array stores `n + 1` states |

With `n ≤ 10000`, linear time is extremely comfortable. The memory usage is also tiny, requiring only a few thousand integers.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    if n == 1:
        return str(a[0])

    dp = [0] * (n + 1)
    dp[1] = a[0]

    for i in range(2, n + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + a[i - 1])

    return str(dp[n])

# provided samples
assert run("5\n3 8 10 2 0\n") == "13"
assert run("7\n0 9 10 2 0 0 0\n") == "11"
assert run("1\n42\n") == "42"

# custom cases
assert run("1\n0\n") == "0", "minimum size"
assert run("5\n0 0 0 0 0\n") == "0", "all zeros"
assert run("3\n2 1 2\n") == "4", "take first and third"
assert run("6\n5 5 5 5 5 5\n") == "15", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `0` | Minimum input size |
| `5 / 0 0 0 0 0` | `0` | All values zero |
| `3 / 2 1 2` | `4` | Non-adjacent selection beats greedy choice |
| `6 / 5 5 5 5 5 5` | `15` | Repeated equal values |

## Edge Cases

Consider:

```
1
42
```

The algorithm immediately uses the base case and prints `42`. No DP transition is needed. This avoids invalid access to `dp[-1]` or other out-of-range positions.

Consider:

```
3
2 1 2
```

The DP values become:

```
dp[1] = 2
dp[2] = 2
dp[3] = 4
```

The algorithm correctly combines the first and third items, producing `4`.

Consider:

```
5
0 0 0 0 0
```

The DP table remains all zeros:

```
dp = [0, 0, 0, 0, 0, 0]
```

The output is `0`, which is the maximum achievable desirability.

These cases demonstrate that the recurrence handles small inputs, non-greedy optimal choices, and zero-valued items correctly.
