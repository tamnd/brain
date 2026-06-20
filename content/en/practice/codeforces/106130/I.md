---
title: "CF 106130I - \u8fd0\u52a8\u4e16\u754c\u6821\u56ed"
description: "We are given a single probability value p, describing the success rate of one independent attempt to obtain a required result. A student has exactly three independent attempts. Each attempt either succeeds with probability p or fails with probability 1 - p."
date: "2026-06-20T08:22:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106130
codeforces_index: "I"
codeforces_contest_name: "GDUT 2025 Monthly competition"
rating: 0
weight: 106130
solve_time_s: 53
verified: true
draft: false
---

[CF 106130I - \u8fd0\u52a8\u4e16\u754c\u6821\u56ed](https://codeforces.com/problemset/problem/106130/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single probability value `p`, describing the success rate of one independent attempt to obtain a required result. A student has exactly three independent attempts. Each attempt either succeeds with probability `p` or fails with probability `1 - p`. The process stops being relevant once at least one success happens, because that already guarantees overall success.

The task is to compute the probability that at least one of the three attempts succeeds.

The input is a floating-point number between `0` and `1`. The output is a single floating-point number representing the probability of success within three tries, with a tolerance of `1e-4` in either relative or absolute error.

Even though the statement is short, the key modeling choice is recognizing that this is a classic “at least one success in repeated independent Bernoulli trials” problem.

No large constraints are involved, so performance is irrelevant, but numerical stability matters slightly because we are dealing with floating-point arithmetic. The only subtle edge cases appear at the boundaries `p = 0` and `p = 1`.

If `p = 0`, every attempt fails, so the answer must be `0`. A naive computation like `1 - (1 - p)^3` still works here, but only if floating-point precision does not introduce negative zero or tiny noise.

If `p = 1`, every attempt succeeds, so the answer is exactly `1`.

A common mistake is trying to enumerate sequences manually and accidentally double-counting outcomes where multiple successes occur. That leads to incorrect combinatorial reasoning unless carefully structured.

## Approaches

A brute-force interpretation would explicitly enumerate all possible outcomes of the three independent trials. Each trial has two states, success or failure, so there are `2^3 = 8` total outcome patterns. We could compute the probability of each pattern and sum those that contain at least one success.

This approach is correct because it directly follows the definition of probability over independent events. However, it is unnecessarily verbose and scales poorly if the number of trials grows, because `n` trials would require `2^n` combinations.

The key observation is that counting “at least one success” is easier via its complement. Instead of summing all favorable cases, we compute the probability that all attempts fail and subtract from `1`.

The probability that a single attempt fails is `(1 - p)`. Since the attempts are independent, the probability that all three fail is `(1 - p)^3`. Therefore, the desired probability is:

`1 - (1 - p)^3`

This reduces the problem from enumerating outcomes to a single arithmetic expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(2^3) | O(1) | Works but unnecessary |
| Complement Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the probability `p` from input. This value represents success probability per attempt.
2. Compute the failure probability `q = 1 - p`. This transforms the problem into reasoning about the single “bad event” rather than the “good event”.
3. Compute the probability that all three attempts fail as `q^3`. Independence allows multiplication across attempts.
4. Subtract this value from `1` to obtain the probability that at least one attempt succeeds.
5. Print the result as a floating-point number.

The only real computation is a constant number of arithmetic operations, so the implementation is straightforward.

### Why it works

The events “at least one success” and “all failures” are complementary and mutually exclusive, covering the entire probability space. Since independence allows exact computation of the “all fail” event as a product of identical probabilities, the complement gives the exact target without approximation beyond floating-point arithmetic.

## Python Solution

```python
import sys
input = sys.stdin.readline

p = float(input().strip())

q = 1.0 - p
ans = 1.0 - q * q * q

print(ans)
```

The code reads the probability as a float, computes the complement failure probability, and raises it to the third power by repeated multiplication. This avoids any potential overhead of calling `pow` and keeps the computation explicit.

The subtraction from `1.0` is done last to minimize floating-point error accumulation. Since the expression involves only a few operations, precision is well within the required tolerance.

## Worked Examples

### Example 1

Input:

```
0.5
```

We compute `q = 0.5`.

| Step | Value |
| --- | --- |
| p | 0.5 |
| q | 0.5 |
| q^3 | 0.125 |
| 1 - q^3 | 0.875 |

Output:

```
0.875
```

This matches the probability that at least one success occurs in three fair independent coin flips.

### Example 2

Input:

```
0.2
```

| Step | Value |
| --- | --- |
| p | 0.2 |
| q | 0.8 |
| q^3 | 0.512 |
| 1 - q^3 | 0.488 |

Output:

```
0.488
```

This confirms that even with a low success rate, three attempts significantly increase the chance of success.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The computation is constant-time regardless of input size, which trivially satisfies any reasonable constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    p = float(input().strip())
    q = 1.0 - p
    ans = 1.0 - q**3
    return str(ans)

# provided sample
assert abs(float(run("0.5")) - 0.875) < 1e-9

# edge: always fail
assert abs(float(run("0")) - 0.0) < 1e-9

# edge: always succeed
assert abs(float(run("1")) - 1.0) < 1e-9

# small probability
assert abs(float(run("0.1")) - (1 - 0.9**3)) < 1e-9

# high probability
assert abs(float(run("0.9")) - (1 - 0.1**3)) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0.5 | 0.875 | standard case |
| 0 | 0 | all failures |
| 1 | 1 | guaranteed success |
| 0.1 | 0.271 | low probability regime |
| 0.9 | 0.999 | high probability regime |

## Edge Cases

For `p = 0`, we get `q = 1`, so `q^3 = 1` and the result is `0`. The algorithm correctly captures that every attempt fails, so no success is possible.

For `p = 1`, we get `q = 0`, so `q^3 = 0` and the result is `1`. This reflects guaranteed success on the first attempt, and subsequent attempts are irrelevant.

For extreme floating-point inputs close to `0` or `1`, the subtraction remains stable because the expression involves only one subtraction and two multiplications, which stay within the required error tolerance.
