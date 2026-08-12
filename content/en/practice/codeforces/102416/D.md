---
title: "CF 102416D - Calculated risk"
description: "We repeatedly roll a fair die with k faces. A successful roll is one that shows 1, and the game ends as soon as we have seen n successful rolls consecutively."
date: "2026-08-12T20:43:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102416
codeforces_index: "D"
codeforces_contest_name: "Edinburgh Competition 2019"
rating: 0
weight: 102416
solve_time_s: 107
verified: true
draft: false
---

[CF 102416D - Calculated risk](https://codeforces.com/problemset/problem/102416/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We repeatedly roll a fair die with `k` faces. A successful roll is one that shows `1`, and the game ends as soon as we have seen `n` successful rolls consecutively. Every roll costs £1, so the required prize is exactly the expected number of rolls until the first occurrence of `n` consecutive ones.

The input consists of `k`, the number of faces on the die, and `n`, the required length of the consecutive streak. The output is the expected number of rolls, with an absolute or relative error of at most `10^-4`. The official constraints are `3 <= k <= 20` and `1 <= n <= 5`.

The small upper bound on `n` might suggest a simulation or a state-based dynamic program, but the quantity we need is an exact expectation, not one particular random experiment. A simulation would require a potentially large number of rolls and would only approximate the answer. The useful observation is that the probability of success on every roll is fixed at `1/k`, and the only information from the past that affects our future is the current length of the suffix consisting entirely of ones.

There are several boundary cases that are easy to mishandle. For `n = 1`, a single one already finishes the game. For example, with input `3 1`, the expected number of rolls is `3`, because every roll has probability `1/3` of ending the game. A recurrence that assumes there is always a nonempty intermediate streak state can accidentally return the wrong value here.

Another common mistake is counting the number of rolls after the winning roll instead of including it. For `k = 6, n = 2`, the correct answer is `42`, not `41`, because the winning roll itself costs £1. The sample confirms this value.

A third issue is forgetting that a failed attempt at extending a streak resets the current streak completely. With `k = 3, n = 2`, a sequence such as `1, 1` finishes after two rolls, while `1, 2, 1, 1` finishes after four. After the `2`, the earlier `1` cannot contribute to the new streak.

## Approaches

A direct brute-force idea is to generate possible sequences of die rolls and determine when each sequence first contains `n` consecutive ones. This is conceptually correct because every finite sequence has a known probability, and averaging its stopping time over all possible outcomes gives the desired expectation. The problem is that the process has no fixed maximum length. A sequence can avoid the target streak for arbitrarily many rolls, so exhaustive enumeration has no finite worst-case stopping bound. Even if we artificially stop after `L` rolls, there are `k^L` sequences to inspect, which becomes infeasible almost immediately.

We can instead describe the process using its current streak length. Let `E_i` be the expected number of additional rolls needed when the current suffix contains exactly `i` consecutive ones, where `0 <= i < n`. From state `i`, the next roll costs one roll. With probability `1/k`, it is another one and moves us to state `i + 1`. With probability `(k - 1)/k`, it is not one and the streak resets to state `0`.

Thus,

`E_i = 1 + (1/k) E_{i+1} + ((k-1)/k) E_0`

with `E_n = 0`.

The crucial simplification is that we do not actually need to solve all these equations numerically. Starting from the last state and substituting backwards produces a geometric sum. The result is

`E_0 = (1 - (1/k)^n) / ((1 - 1/k)(1/k)^n)`.

Multiplying numerator and denominator by `k^n` gives the much cleaner integer expression

`E_0 = (k^(n+1) - k) / (k - 1)`.

For example, with `k = 6` and `n = 2`, this gives

`(6^3 - 6) / 5 = 210 / 5 = 42`.

The answer is actually an integer for all valid integer values of `k` and `n`, so floating-point arithmetic is unnecessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded, `O(k^L)` for horizon `L` | `O(L)` | Too slow |
| Optimal | `O(1)` | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read `k` and `n`. The probability of rolling a one is `1/k`, while the probability of rolling anything else is `(k-1)/k`.
2. Model the process by the length of the current consecutive-one suffix. If the current suffix has length `i`, a one increases it to `i+1`, while any other value resets it to zero. This captures all information from the past that can affect the remaining waiting time.
3. Let `E_i` denote the expected remaining number of rolls from state `i`. The terminal state is `E_n = 0`, because the required streak has already been obtained.
4. For every nonterminal state, write the one-step expectation

`E_i = 1 + E_{i+1}/k + (k-1)E_0/k`.

The `1` accounts for the roll we are about to make. The two remaining terms describe the two possible next states.
5. Solve the recurrence backwards. Repeated substitution expresses `E_0` in terms of itself and a geometric sequence. The resulting equation simplifies to

`E_0 = (k^(n+1) - k)/(k-1)`.
6. Compute that expression using integer arithmetic and print it. The largest permitted answer is at most `10^9`, so Python's integer arithmetic handles the calculation comfortably.

### Why it works

The state `i` always represents exactly the number of consecutive ones immediately preceding the next roll. This is sufficient because older rolls have no influence on future rolls once the current suffix length is known. From each state, the recurrence considers every possible next outcome and adds exactly one for that next roll. Since `E_n = 0`, solving the recurrence gives the expected stopping time from every state, including the initial state `E_0`. The closed form is simply the exact solution of those expectation equations, so the algorithm returns the required expected number of rolls rather than an estimate based on random simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k, n = map(int, input().split())

    answer = (k ** (n + 1) - k) // (k - 1)
    print(f"{answer:.2f}")

if __name__ == "__main__":
    solve()
```

The program reads the two parameters and directly evaluates the closed form obtained from the recurrence. There is no need to construct the individual streak states because the recurrence has already been algebraically simplified.

The exponent is `n + 1`, not `n`. This is a common off-by-one error. For `n = 1`, the formula becomes `(k^2-k)/(k-1) = k`, which is exactly the expected waiting time for one successful roll.

The subtraction is also `k`, giving `k^(n+1) - k`. Using only `k^(n+1)` would produce an incorrect result even though it might look close for large values.

Integer division is safe because the expression is always an integer. More importantly, it avoids introducing floating-point rounding before formatting. The output uses two decimal places, which is comfortably within the required `10^-4` tolerance.

## Worked Examples

For Sample 1, the input is `k = 6, n = 2`. The formula evaluates as follows.

| Variable | Value |
| --- | --- |
| `k` | 6 |
| `n` | 2 |
| `k^(n+1)` | 216 |
| `k^(n+1) - k` | 210 |
| `k - 1` | 5 |
| `answer` | 42 |

The expected number of rolls is `42.00`. The state interpretation also makes this intuitive: from zero consecutive ones, a one moves us toward the target, while any other face resets the streak. The formula accounts for all such resets exactly.

For a second example, consider `k = 3, n = 1`.

| Variable | Value |
| --- | --- |
| `k` | 3 |
| `n` | 1 |
| `k^(n+1)` | 9 |
| `k^(n+1) - k` | 6 |
| `k - 1` | 2 |
| `answer` | 3 |

A single one is enough to finish, and each roll has probability `1/3` of producing one. The expected waiting time is consequently `3`, confirming that the formula handles the smallest possible streak length correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(1)` | Only one exponentiation and a constant number of arithmetic operations are performed. |
| Space | `O(1)` | The algorithm stores only `k`, `n`, and the resulting value. |

The constraints are tiny, with `n <= 5` and `k <= 20`, so even a state-based dynamic program would be easily fast enough. The closed form is substantially simpler and eliminates all iteration over states. It uses negligible memory and runs comfortably within the one-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys
import io

def solve():
    k, n = map(int, input().split())
    answer = (k ** (n + 1) - k) // (k - 1)
    print(f"{answer:.2f}")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("6 2\n") == "42.00", "sample 1"

# Minimum k and minimum n
assert run("3 1\n") == "3.00", "single one on a 3-sided die"

# Maximum k and maximum n
assert run("20 5\n") == "3368420.00", "maximum constraints"

# Two-sided streak with the smallest possible die
assert run("3 2\n") == "6.00", "short streak"

# Boundary case n = 1 with a larger die
assert run("20 1\n") == "20.00", "single one on a 20-sided die"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 2` | `42.00` | Provided sample and general recurrence |
| `3 1` | `3.00` | Minimum `n`, catches an off-by-one in the exponent |
| `20 5` | `3368420.00` | Maximum values of both parameters |
| `3 2` | `6.00` | Small nontrivial streak and reset behavior |
| `20 1` | `20.00` | Boundary case where one success immediately ends the game |

## Edge Cases

For `3 1`, the target is simply the first roll equal to one. The formula gives `(3^2 - 3)/(3-1) = 3`, so the output is `3.00`. A solution that accidentally uses `k^n` instead of `k^(n+1)` would fail this case immediately.

For `6 2`, the target is two consecutive ones. The formula gives `(6^3 - 6)/5 = 42`, so the output is `42.00`. This case catches the mistake of stopping the count before charging for the successful roll, because the expectation includes the roll that creates the final streak.

For `3 2`, the expected value is `(3^3 - 3)/2 = 12/2 = 6`. A useful manual trace is that the process starts in state zero, moves to state one after a one, reaches the terminal state after another one, and returns to zero after any non-one. The recurrence includes both transitions, so repeated failed attempts are accounted for rather than treating each pair of rolls as an independent trial.

For `20 5`, the answer is `(20^6 - 20)/19 = 3,368,420`. This is the largest corner of the given constraints and demonstrates why simulating individual rolls is a poor way to compute the expectation. The closed form reaches the answer immediately, while the actual random process may require millions of rolls before the desired streak appears.
