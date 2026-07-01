---
title: "CF 104287C - No Sweep"
description: "We are looking at a sequence of $n$ independent rounds of a game. In each round exactly one player wins. One special player is Thomas, and there are $k$ other competitors, so every round has $k+1$ possible winners."
date: "2026-07-01T20:44:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104287
codeforces_index: "C"
codeforces_contest_name: "Teamscode Spring 2023 Contest"
rating: 0
weight: 104287
solve_time_s: 60
verified: true
draft: false
---

[CF 104287C - No Sweep](https://codeforces.com/problemset/problem/104287/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking at a sequence of $n$ independent rounds of a game. In each round exactly one player wins. One special player is Thomas, and there are $k$ other competitors, so every round has $k+1$ possible winners.

A full outcome of the game is simply a length-$n$ sequence where each position chooses one of these $k+1$ players as the winner of that round. Among all such sequences, we want to count those in which Thomas does not win every single round. In other words, we exclude the single degenerate case where every entry in the sequence is Thomas.

The total number of possible sequences is $(k+1)^n$, since each round has $k+1$ independent choices. The only forbidden configuration is the one where Thomas is chosen in all $n$ positions.

The constraints are extremely small: $n \le 10$ and $k \le 4$. This immediately tells us that even a naive enumeration of all outcomes is feasible, since the maximum number of sequences is $5^{10} \approx 9.7 \times 10^6$, which is borderline but still manageable in optimized Python if done carefully. However, the structure is simple enough that enumeration is unnecessary.

A subtle edge case is when $n = 1$. In that case, “Thomas gets a sweep” means Thomas wins the only round. So the answer should be all players except that single configuration. That becomes $k$, since there are $k+1$ total choices and we exclude exactly one.

Another edge case is when $k = 0$, meaning Thomas is the only player. The only possible outcome is a sweep, so the answer must be zero for any $n \ge 1$. The formula must naturally handle this.

## Approaches

The most direct way to think about the problem is to generate all possible sequences of winners. For each round we pick one of $k+1$ players, forming a tree of depth $n$ with branching factor $k+1$. This produces exactly $(k+1)^n$ leaves. For each leaf, we check whether every position is Thomas, and subtract that single invalid case.

This works correctly because it explicitly constructs all outcomes. The failure point is efficiency: even at the upper bound $n = 10$, $k = 4$, the search space grows to nearly ten million sequences, and any additional overhead inside recursion or string construction makes it fragile in Python under strict limits.

The key observation is that the structure is entirely uniform across rounds. Every round is independent, and the condition “Thomas wins all rounds” corresponds to exactly one sequence. Therefore, we do not need to enumerate anything; we only need to subtract that single configuration from the total count.

So the answer is simply:

$$(k+1)^n - 1$$

The brute force explicitly counts both parts, while the optimized solution directly counts the full space and removes the only forbidden case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | $O((k+1)^n \cdot n)$ | $O(n)$ | Too slow |
| Direct Formula | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read integers $n$ and $k$. These define the number of rounds and the number of non-Thomas players.
2. Compute the total number of possible outcomes as $(k+1)^n$, since each round independently chooses one winner among $k+1$ competitors.
3. Subtract 1 from this total to remove the single invalid outcome where Thomas wins every round.
4. Output the resulting value.

The only reasoning step that matters is recognizing that the invalid condition corresponds to exactly one configuration, not a range or subset. That is what allows subtraction instead of inclusion-exclusion or dynamic programming.

### Why it works

Every valid game outcome corresponds uniquely to a length-$n$ sequence over an alphabet of size $k+1$. This mapping is bijective: each sequence defines exactly one outcome and each outcome defines exactly one sequence.

The “sweep” condition corresponds to the single sequence where every position is Thomas. Since no other sequence shares this property, removing exactly one from the total count produces the correct answer. There is no overlap or interaction between rounds that could create additional forbidden cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())

total = pow(k + 1, n)
print(total - 1)
```

The implementation mirrors the mathematical reduction directly. The built-in `pow` is used for fast exponentiation, which is unnecessary for such small constraints but keeps the code clean and safe.

The subtraction of 1 is safe for all valid inputs because when $k \ge 0$ and $n \ge 1$, we always have $(k+1)^n \ge 1$, and equality happens only at $k = 0$, where the result correctly becomes zero.

## Worked Examples

### Example 1: $n = 2, k = 1$

Players are Thomas and one opponent.

Total outcomes are $2^2 = 4$.

| Round 1 | Round 2 | Valid? |
| --- | --- | --- |
| T | T | No |
| T | O | Yes |
| O | T | Yes |
| O | O | Yes |

We subtract the single invalid case $TT$, leaving 3 valid outcomes.

This confirms the idea that only one configuration is excluded.

### Example 2: $n = 10, k = 3$

Total outcomes are $4^{10} = 1048576$.

The only invalid outcome is Thomas winning all 10 rounds, so we subtract 1.

Result is $1048575$.

No structure beyond uniform counting is involved, which demonstrates that the solution scales purely through exponentiation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | One exponentiation and one subtraction |
| Space | $O(1)$ | Only a few integer variables |

The constraints are small, but the solution is already optimal for any reasonable input size. Even if $n$ were large, Python’s built-in exponentiation would handle it efficiently, and the logic would remain unchanged.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    return str(pow(k + 1, n) - 1)

# provided samples
assert run("2 1\n") == "3"
assert run("10 3\n") == "1048575"

# minimum n, k = 0 (only Thomas exists, always sweep)
assert run("1 0\n") == "0"

# single round with multiple opponents
assert run("1 3\n") == "3"

# all equal edge: k = 1, n = 1
assert run("1 1\n") == "1"

# slightly larger sanity check
assert run("3 2\n") == str(3**3 - 1)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 0 | Only Thomas exists, sweep is unavoidable |
| 1 3 | 3 | Single round excludes only Thomas |
| 3 2 | 26 | General correctness of formula |

## Edge Cases

The most important edge case is when $k = 0$. The input describes a situation where only Thomas exists. For any $n$, every round must be won by Thomas, so there is exactly one outcome and it is always a sweep. The formula gives $(0+1)^n - 1 = 0$, which matches the reasoning directly.

For $n = 1$, the problem reduces to choosing a single winner among $k+1$ players. Exactly one of these choices is invalid (Thomas), so the result should be $k$. The formula gives $(k+1)^1 - 1 = k$, which aligns exactly.

For larger $n$, no new structural cases appear because independence across rounds ensures no interaction effects. Each additional round only multiplies the total space, and the forbidden configuration remains singular.
