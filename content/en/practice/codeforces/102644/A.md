---
title: "CF 102644A - Random Mood"
description: "The problem describes a person whose mood has only two possible states: happy and sad. Every second, the current mood may change with probability p, or stay the same with probability 1 - p."
date: "2026-08-01T10:10:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102644
codeforces_index: "A"
codeforces_contest_name: "Matrix Exponentiation"
rating: 0
weight: 102644
solve_time_s: 227
verified: true
draft: false
---

[CF 102644A - Random Mood](https://codeforces.com/problemset/problem/102644/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a person whose mood has only two possible states: happy and sad. Every second, the current mood may change with probability `p`, or stay the same with probability `1 - p`. We start at the happy state and need to find the probability that the person is happy again after exactly `n` seconds.

The input contains the number of seconds to simulate and the probability of changing mood during one second. The required output is the final probability of being happy after those `n` transitions.

The value of `n` can reach `10^9`, which immediately rules out simulating each second. A direct simulation would require one operation per second, and even a linear solution would need one billion updates in the worst case. The probability has a simple two-state structure, so the solution must use a method that handles repeated transitions efficiently, reducing the number of operations from proportional to `n` to proportional to the number of bits in `n`.

The main implementation pitfalls come from large values of `n` and from handling probabilities correctly. For example, with input `1 0.7`, the answer is `0.3` because the only way to still be happy after one second is not changing mood. A careless implementation might return `0.7` by treating the switch probability as the final happy probability.

Another common mistake appears when `n` is even. For input `2 0.1`, the answer is `0.82`, because the mood is happy if it switches twice or does not switch at all. A solution that only considers the probability of remaining unchanged during every second would calculate `0.81` and miss the paths that return to happiness after an even number of switches.

## Approaches

The straightforward approach is to keep track of the probability of being happy and sad after every second. Initially, the happy probability is `1` and the sad probability is `0`. Each second, we update both values using the transition rules. If the current happy probability is `h` and sad probability is `s`, then the next happy probability is `h * (1 - p) + s * p`, while the next sad probability is `h * p + s * (1 - p)`.

This method is correct because it directly follows the probability transitions. The problem is the number of transitions. When `n` is `10^9`, this requires one billion updates, which is far beyond the available time.

The key observation is that every second applies the same transformation to the pair of probabilities. Repeating the same transformation many times is exactly the situation where matrix exponentiation is useful. We can represent one transition as a 2 by 2 matrix and raise that matrix to the power `n` using binary exponentiation.

The brute-force works because each second is an independent application of the same transition rule, but fails when the number of seconds becomes too large. The observation that the transition itself can be represented as a matrix lets us apply all `n` transitions in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Build the transition matrix that describes one second of mood changes.

If the current state is represented as a column vector `[happy, sad]`, one transition changes it into:

```
[1-p  p] [happy]
[ p  1-p] [sad]
```

The matrix contains every possible transition probability between the two states.
2. Raise this transition matrix to the power `n` using binary exponentiation.

Instead of multiplying the matrix by the state vector `n` times, we repeatedly square the matrix. When a bit of `n` is set, that squared matrix contributes to the final answer.
3. Apply the resulting matrix to the initial state.

The initial state is `[1, 0]` because the person starts happy. After multiplying by the matrix raised to the `n`th power, the first component of the resulting vector is the probability of being happy.

Why it works:

The transition matrix exactly represents one second of the process. Matrix multiplication combines transitions, so multiplying the matrix by itself `n` times represents performing the transition `n` times. Binary exponentiation computes the same matrix power using repeated squaring, which preserves the exact mathematical meaning while reducing the number of operations. Since the initial state vector is known, the final multiplication extracts the exact probability of being happy after all transitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def multiply(a, b):
    return [
        [
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ],
        [
            a[1][0] * b[0][0] + a[1][1] * b[1][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ],
    ]

def power(matrix, n):
    result = [[1.0, 0.0], [0.0, 1.0]]
    while n > 0:
        if n & 1:
            result = multiply(result, matrix)
        matrix = multiply(matrix, matrix)
        n >>= 1
    return result

def solve():
    n, p = input().split()
    n = int(n)
    p = float(p)

    transition = [
        [1.0 - p, p],
        [p, 1.0 - p],
    ]

    result = power(transition, n)

    answer = result[0][0]
    print("{:.10f}".format(answer))

solve()
```

The `multiply` function performs multiplication of two 2 by 2 matrices. Since the matrices are always this small, writing the four expressions directly avoids unnecessary loops.

The `power` function starts with the identity matrix because it represents applying zero transitions. During binary exponentiation, every set bit of `n` adds the corresponding power of the transition matrix to the answer. Squaring the matrix after each bit lets us skip large ranges of transitions.

The final matrix represents all `n` seconds of movement. Because the initial state is `[1, 0]`, only the first column of the resulting matrix matters, and the value at position `[0][0]` is the probability of ending happy.

Floating point precision is sufficient because the required error is only `10^-6`. Python integers are not involved in the exponentiation result, so there is no overflow concern.

## Worked Examples

For Sample 1:

Input:

```
1 0.7
```

The transition matrix is:

```
[0.3 0.7]
[0.7 0.3]
```

| Variable | Initial | After processing bit |
| --- | --- | --- |
| n | 1 | 0 |
| result[0][0] | 1.0 | 0.3 |
| matrix[0][0] | 0.3 | 0.58 |

The only set bit is the first bit of `n`, so the transition matrix itself becomes the answer matrix. The top-left value is `0.3`, matching the probability of staying happy for one second.

For Sample 2:

Input:

```
2 0.1
```

The transition matrix is:

```
[0.9 0.1]
[0.1 0.9]
```

| Variable | Initial | After first square |
| --- | --- | --- |
| n | 2 | 1 |
| result[0][0] | 1.0 | 1.0 |
| matrix[0][0] | 0.9 | 0.82 |

The binary representation of `2` is `10`, so the first transition matrix is squared before being applied. The resulting top-left value is `0.82`, representing the probability of either no switches or two switches.

These examples show why the matrix approach naturally handles both odd and even numbers of mood changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Binary exponentiation performs a constant amount of 2 by 2 matrix work for each bit of `n`. |
| Space | O(1) | Only a few fixed-size matrices are stored. |

The largest possible value of `n` has only about 30 bits, so the algorithm performs a very small number of matrix multiplications even in the worst case. It easily fits the time and memory limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def multiply(a, b):
        return [
            [
                a[0][0] * b[0][0] + a[0][1] * b[1][0],
                a[0][0] * b[0][1] + a[0][1] * b[1][1],
            ],
            [
                a[1][0] * b[0][0] + a[1][1] * b[1][0],
                a[1][0] * b[0][1] + a[1][1] * b[1][1],
            ],
        ]

    def power(matrix, n):
        result = [[1.0, 0.0], [0.0, 1.0]]
        while n:
            if n & 1:
                result = multiply(result, matrix)
            matrix = multiply(matrix, matrix)
            n >>= 1
        return result

    n, p = sys.stdin.readline().split()
    n = int(n)
    p = float(p)
    m = [[1 - p, p], [p, 1 - p]]
    ans = power(m, n)[0][0]

    sys.stdin = old_stdin
    return "{:.10f}".format(ans)

assert run("1 0.7\n") == "0.3000000000", "sample 1"
assert run("2 0.1\n") == "0.8200000000", "sample 2"
assert run("11 0.06\n") == "0.6225404294", "sample 3"

assert run("1 0.5\n") == "0.5000000000", "single step with equal switching chance"
assert run("1000000000 0.5\n") == "0.5000000000", "large n precision case"
assert run("10 0.000001\n") == "0.9999900001", "small probability case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0.5` | `0.5000000000` | Checks the symmetric transition case. |
| `1000000000 0.5` | `0.5000000000` | Checks that huge `n` is handled logarithmically. |
| `10 0.000001` | `0.9999900001` | Checks precision with a very small switching probability. |

## Edge Cases

For the one-second case `1 0.7`, the algorithm creates the matrix:

```
[0.3 0.7]
[0.7 0.3]
```

The exponent is one, so the matrix is not squared. The answer is the top-left value, `0.3`, which correctly represents staying happy after one transition.

For the two-second case `2 0.1`, the algorithm squares the transition matrix because the exponent is represented by the binary value `10`. The squared matrix contains the combined probability of all two-step paths, including switching twice and not switching at all. Its top-left value becomes `0.82`.

For a very large value such as `1000000000 0.5`, every transition has equal probability of changing or staying. After any positive number of seconds, the probability of being happy is exactly `0.5`. Binary exponentiation reaches this answer without iterating through the seconds one by one.

For very small probabilities such as `10 0.000001`, repeated multiplication could lose accuracy if implemented carelessly. The matrix method keeps the calculation in standard floating point arithmetic and avoids subtracting large nearly equal values, producing a result within the required tolerance.

You can adjust the editorial’s depth or wording if you want it closer to an official Codeforces tutorial style or a shorter contest blog format.
