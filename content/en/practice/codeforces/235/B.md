---
title: "CF 235B - Let's Play Osu!"
description: "Each click in the game independently becomes either a successful hit (O) or a miss (X). For a completed sequence, we split it into maximal consecutive blocks of O. If a block has length L, it contributes L² to the score. The total score is the sum of these squared block lengths."
date: "2026-06-04T10:08:22+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 235
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 146 (Div. 1)"
rating: 2000
weight: 235
solve_time_s: 93
verified: true
draft: false
---

[CF 235B - Let's Play Osu!](https://codeforces.com/problemset/problem/235/B)

**Rating:** 2000  
**Tags:** dp, math, probabilities  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

Each click in the game independently becomes either a successful hit (`O`) or a miss (`X`).

For a completed sequence, we split it into maximal consecutive blocks of `O`. If a block has length `L`, it contributes `L²` to the score. The total score is the sum of these squared block lengths.

We are not given a concrete sequence. Instead, for every position `i`, we know the probability `p[i]` that the click is successful. All clicks are independent. We must compute the expected value of the final score.

The first instinct is to think about all possible outcomes. A sequence of length `n` has `2^n` possible realizations, and each realization has its own score. Computing the expectation by enumerating them is impossible. With `n` up to `100000`, even storing all outcomes would be absurd.

The constraint `n ≤ 100000` immediately suggests that we need something close to linear time. Quadratic dynamic programming is already too expensive because `10^10` operations are far beyond the time limit. Any accepted solution must process each probability only a constant number of times.

The tricky part is that the score depends on entire runs of consecutive successes. A run ending at position `i` may have started arbitrarily far earlier, so a local transition is not obvious.

Several edge cases are easy to mishandle.

Consider:

```
1
1.0
```

The only possible sequence is `"O"`, whose score is `1`. Any recurrence must correctly initialize the first position.

Consider:

```
2
1.0 1.0
```

The only possible sequence is `"OO"`, whose score is `4`, not `2`. A method that simply sums expected contributions of individual positions would miss the interaction between consecutive successes.

Consider:

```
3
0 1 0
```

The middle click always forms a run of length `1`, so the answer is exactly `1`. Any recurrence that accidentally carries state through a position with probability `0` will produce an incorrect result.

Another subtle case is:

```
3
0.5 0.5 0.5
```

A run can extend across multiple positions, so the contribution of position `i` depends on the expected length of the run ending at `i-1`. This dependence is exactly what the solution must capture.

## Approaches

Suppose we try brute force.

For every one of the `2^n` possible sequences, we could compute its probability and score, then add `probability × score` to the answer. This is mathematically correct because expectation is defined that way.

The problem is the number of outcomes. Even for `n = 50`, there are already more than one quadrillion sequences. For `n = 100000`, the approach is completely infeasible.

The key observation is that we do not actually need the full distribution of runs. We only need enough information to update the expected score when processing one more position.

Imagine a run of successes ending at the current position. Let its length be `L`.

If the current click succeeds, extending a run from length `L-1` to length `L`, the score contribution of that run changes from

`(L-1)²`

to

`L²`.

The increase is

`L² - (L-1)² = 2L - 1`.

This incremental form is the crucial simplification.

Instead of tracking complete runs, we track the expected length of the current suffix of consecutive successes. When a new successful click arrives, the score increases by `2L-1`. Since expectation is linear, we only need the expected value of `L`.

This leads to a simple linear DP maintaining:

`len`, the expected length of the consecutive-success suffix ending at the current position.

`ans`, the expected score accumulated so far.

Each probability is processed once, giving an `O(n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### State Definitions

Let:

`f` = expected length of the consecutive `O` suffix ending at the current position.

`ans` = expected score after processing the current position.

### Transition Derivation

Assume we are processing probability `p`.

If the click is a miss, the suffix length becomes `0`.

If the click is successful, the suffix length becomes the previous suffix length plus `1`.

Hence:

$$f' = p(f+1)$$

because with probability `p` we obtain `f+1`, and with probability `1-p` we obtain `0`.

Now consider the score increase.

When a successful click extends a run whose new length is `L`, the run score increases by:

$$L^2-(L-1)^2 = 2L-1$$

The new length equals `f+1` in expectation-conditioned form.

Therefore the expected increase contributed by this position is:

$$p \cdot (2(f+1)-1)
=
p(2f+1)$$

So:

$$ans' = ans + p(2f+1)$$

Notice that the old value of `f` must be used here, before updating it.

### Numbered Steps

1. Initialize `f = 0` and `ans = 0`.
2. Process probabilities from left to right.
3. For the current probability `p`, add

$$p(2f+1)$$

to `ans`.

This is the expected score increase caused by extending the current run if the click succeeds.
4. Update the expected suffix length:

$$f = p(f+1)$$

If the click misses, the suffix becomes zero. If it succeeds, the suffix length increases by one.
5. After all probabilities are processed, output `ans`.

### Why it works

Let `L_i` denote the random length of the consecutive-success suffix ending at position `i`.

The maintained variable `f` is exactly `E[L_i]`.

When position `i` succeeds, the run ending there changes from length `L_i-1` to `L_i`. The score increment is always:

$$L_i^2-(L_i-1)^2 = 2L_i-1$$

Taking expectation and using linearity of expectation gives:

$$E[\Delta]
=
p_i(2E[L_{i-1}]+1)$$

which is exactly the update added to `ans`.

Since every score increase is accounted for once, and `f` always equals the expected suffix length after processing the current position, the accumulated value `ans` equals the expected total score.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(float, input().split()))

    f = 0.0
    ans = 0.0

    for prob in p:
        ans += prob * (2.0 * f + 1.0)
        f = prob * (f + 1.0)

    print("{:.15f}".format(ans))

solve()
```

The variable `f` stores the expected length of the current consecutive-success suffix. Before updating it, we use its old value to compute the expected score increase contributed by the current click.

The order is important. The formula

$$ans += p(2f+1)$$

uses the suffix length ending at the previous position. Updating `f` first would incorrectly use the new suffix length and double count part of the contribution.

All calculations use floating point numbers. The recurrence performs only additions and multiplications, so standard double precision is more than sufficient for the required `10^{-6}` accuracy.

The memory usage stays constant because only two floating point variables are maintained regardless of `n`.

## Worked Examples

### Example 1

Input:

```
3
0.5 0.5 0.5
```

| Position | p | f before | Score increase | ans after | f after |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.5 | 0.0 | 0.5 | 0.5 | 0.5 |
| 2 | 0.5 | 0.5 | 1.0 | 1.5 | 0.75 |
| 3 | 0.5 | 0.75 | 1.25 | 2.75 | 0.875 |

Final answer:

```
2.750000000000000
```

This example shows how the expected suffix length grows gradually. Even though no specific run length is known, the expectation is enough to compute the expected score increase.

### Example 2

Input:

```
3
1 1 1
```

| Position | p | f before | Score increase | ans after | f after |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 2 | 1 | 1 | 3 | 4 | 2 |
| 3 | 1 | 2 | 5 | 9 | 3 |

Final answer:

```
9.000000000000000
```

The only possible sequence is `"OOO"`. The run length grows from `1` to `2` to `3`, producing score increments `1`, `3`, and `5`, whose sum is `9`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each probability is processed once |
| Space | O(1) | Only two floating point variables are maintained |

With `n = 100000`, the algorithm performs roughly one hundred thousand iterations and a handful of arithmetic operations per iteration. This comfortably fits within the time limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    p = list(map(float, input().split()))

    f = 0.0
    ans = 0.0

    for prob in p:
        ans += prob * (2.0 * f + 1.0)
        f = prob * (f + 1.0)

    return "{:.15f}".format(ans)

# provided sample
assert abs(float(run("3\n0.5 0.5 0.5\n")) - 2.75) < 1e-9

# minimum size, always miss
assert abs(float(run("1\n0\n")) - 0.0) < 1e-9

# minimum size, always hit
assert abs(float(run("1\n1\n")) - 1.0) < 1e-9

# all hits, score = 3^2
assert abs(float(run("3\n1 1 1\n")) - 9.0) < 1e-9

# isolated guaranteed hit
assert abs(float(run("3\n0 1 0\n")) - 1.0) < 1e-9

# two guaranteed hits form one block of length 2
assert abs(float(run("2\n1 1\n")) - 4.0) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `0` | Smallest instance, no successful clicks |
| `1 / 1` | `1` | Correct initialization |
| `3 / 1 1 1` | `9` | Single run spanning entire array |
| `3 / 0 1 0` | `1` | Proper reset after misses |
| `2 / 1 1` | `4` | Consecutive hits must merge into one block |

## Edge Cases

Consider:

```
1
0
```

Initially `f = 0`. The update adds `0 * (2*0 + 1) = 0` to the answer, and `f` remains `0`. The final result is `0`, matching the fact that every click is a miss.

Consider:

```
2
1 1
```

After the first click, `ans = 1` and `f = 1`. After the second click, the added contribution is `1 * (2*1 + 1) = 3`, giving a final answer of `4`. This correctly represents a single run of length `2`, whose score is `2²`.

Consider:

```
3
0 1 0
```

The first click contributes nothing and leaves `f = 0`. The second click contributes `1`, producing `f = 1`. The third click contributes nothing and resets the suffix. The answer is exactly `1`, corresponding to one isolated successful click.

Consider:

```
4
1 0 1 1
```

The sequence is deterministic. The runs are `"O"` and `"OO"`, giving score `1² + 2² = 5`.

The algorithm produces:

| Position | p | f before | ans after |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 1 |
| 2 | 0 | 1 | 1 |
| 3 | 1 | 0 | 2 |
| 4 | 1 | 1 | 5 |

The reset at position two prevents the later run from incorrectly merging with the first one.
