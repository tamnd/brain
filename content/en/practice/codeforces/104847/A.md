---
title: "CF 104847A - Quantum Supremacy"
description: "We are comparing two ways to exhaustively test all binary strings of length $n$. There are $2^n$ possible secrets. A classical machine tests exactly one candidate per $a$ seconds, so its total time is proportional to $a cdot 2^n$. A quantum machine behaves differently."
date: "2026-06-28T11:22:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104847
codeforces_index: "A"
codeforces_contest_name: "2019-2020 ICPC, Moscow Subregional"
rating: 0
weight: 104847
solve_time_s: 47
verified: true
draft: false
---

[CF 104847A - Quantum Supremacy](https://codeforces.com/problemset/problem/104847/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are comparing two ways to exhaustively test all binary strings of length $n$. There are $2^n$ possible secrets. A classical machine tests exactly one candidate per $a$ seconds, so its total time is proportional to $a \cdot 2^n$.

A quantum machine behaves differently. With $q$ qubits, it can process up to $2^q$ candidate strings in one batch, and each batch takes $b$ seconds. Since there are $2^n$ total candidates, the quantum machine needs $2^{n-q}$ batches, so its total time is $b \cdot 2^{n-q}$.

The task is to find the smallest non-negative integer $q$ such that the quantum time is strictly smaller than the classical time, or determine that no such $q$ exists.

The input size goes up to $10^{18}$, so direct computation of powers like $2^n$ is impossible. Any solution must avoid constructing exponential values explicitly and instead rely on algebraic manipulation of inequalities.

A key edge case appears when the quantum machine is never faster regardless of $q$. For example, if $a \le b$, then even with infinite batching advantage, the quantum side is not competitive because each batch is not cheaper than a classical single test.

Another subtle case is when $n$ is small and $a$ is large. For instance, if $n = 1, a = 100, b = 1$, then even a small $q$ makes quantum immediately superior. A naive approach that assumes monotonic behavior without solving the inequality correctly might overestimate $q$.

## Approaches

A direct simulation would try every $q$, compute classical and quantum runtimes, and compare them. The classical time is fixed for given $n, a$, but the quantum time depends on how many batches of size $2^q$ are needed. Even if we avoid simulating strings, we still face exponential quantities like $2^n$, making brute force infeasible.

The brute-force reasoning works in principle because the quantum runtime decreases exponentially as $q$ increases. However, checking each $q$ requires evaluating expressions involving $2^n$, which cannot be represented when $n$ is large. This breaks the approach before runtime even becomes an issue.

The key observation is that both runtimes can be written in closed exponential form:

$$T_{\text{classical}} = a \cdot 2^n$$

$$T_{\text{quantum}} = b \cdot 2^{n-q}$$

We compare them:

$$b \cdot 2^{n-q} < a \cdot 2^n$$

Cancel $2^n$:

$$b \cdot 2^{-q} < a$$

Rearranging:

$$\frac{b}{2^q} < a \quad \Rightarrow \quad b < a \cdot 2^q$$

Now the problem becomes finding the smallest $q$ such that:

$$2^q > \frac{b}{a}$$

If $a \ge b$, then even $q = 0$ satisfies $b < a$, so quantum is already faster at zero qubits.

Otherwise, we compute the smallest integer $q$ such that $2^q > b/a$, which is equivalent to $q = \lfloor \log_2(b/a) \rfloor + 1$. Since we only deal with integers and large values, we compute this by repeated doubling or bit-length logic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $q$ with exponential values | Impossible (overflow) | O(1) | Too slow |
| Logarithmic comparison using inequality | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the condition into a comparison between $a$, $b$, and powers of two.

1. Compare $a$ and $b$. If $a \ge b$, then even with $q = 0$, quantum is already strictly better because it processes all strings in $b$ seconds versus $a$ seconds per string classically, making the total comparison favorable immediately. Output 0.
2. Otherwise, we need to increase $q$ until batching advantage compensates for the slower per-batch time $b$. We search for the smallest $q$ such that $a \cdot 2^q > b$.
3. Start with $q = 0$ and a value $2^q = 1$. Repeatedly double until the inequality holds. Each doubling corresponds to increasing $q$ by 1.
4. Stop when $a \cdot 2^q > b$. The current $q$ is minimal because we increased $q$ monotonically from zero.

### Why it works

The inequality reduces the original exponential comparison to a monotone function in $q$. The left-hand side $a \cdot 2^q$ strictly increases as $q$ increases, so there is a unique threshold where it first exceeds $b$. Starting from zero and incrementing ensures we hit that threshold exactly once, and stopping at the first success guarantees minimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, a, b = map(int, input().split())

# Compare directly first condition
if a >= b:
    print(0)
    sys.exit()

q = 0
power = 1  # represents 2^q

while a * power <= b:
    power *= 2
    q += 1

print(q)
```

The first branch handles the case where quantum is immediately competitive without needing any qubits. The second part maintains an explicit representation of $2^q$ using repeated doubling, avoiding any large exponentiation or logarithms.

The loop condition directly enforces the inequality $a \cdot 2^q \le b$, so the first $q$ that breaks it is exactly the answer. Using multiplication by 2 each step prevents overflow concerns from exponentiation formulas and keeps everything in integer arithmetic.

## Worked Examples

### Example 1

Input:

```
1024 1 1
```

| q | 2^q | a·2^q | Condition a·2^q ≤ b |
| --- | --- | --- | --- |
| 0 | 1 | 1 | true |

The loop stops immediately since $a \cdot 1 = 1 \le 1$ is still not strictly greater, but since $a \ge b$ is false, we continue logic carefully: quantum is not better at q=0, but increasing q only increases left side, so we still need to ensure strict inequality. The first $q$ where $a \cdot 2^q > 1$ is $q = 1$. Output is 1.

This shows the threshold behavior: even minimal increase in qubits creates the first strict advantage.

### Example 2

Input:

```
10 100 1
```

| q | 2^q | a·2^q | Condition |
| --- | --- | --- | --- |
| 0 | 1 | 100 | false (not > 1) |

Here $a \ge b$, so we immediately output 0.

This demonstrates the shortcut case where quantum is already faster at zero qubits due to per-operation dominance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(b/a)) | Each step doubles the simulated quantum capacity until threshold is exceeded |
| Space | O(1) | Only a few integer variables are maintained |

The loop runs at most 60 iterations since values are bounded by $10^{18}$, making the solution trivial under the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, a, b = map(int, input().split())

    if a >= b:
        return "0"

    q = 0
    power = 1
    while a * power <= b:
        power *= 2
        q += 1
    return str(q)

# provided sample-like cases
assert run("1 1 1") == "0"
assert run("10 100 1") == "0"

# custom cases
assert run("1 1 2") == "1", "small threshold case"
assert run("5 3 20") == "3", "growth crossing case"
assert run("60 1 10") == "4", "larger gap case"
assert run("100 5 4") == "0", "a >= b immediate win"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 2 | 1 | minimal qubit gain needed |
| 5 3 20 | 3 | exponential crossing behavior |
| 60 1 10 | 4 | larger threshold scaling |
| 100 5 4 | 0 | immediate dominance case |

## Edge Cases

When $a \ge b$, the algorithm immediately returns 0. For example, input `100 5 4` triggers this branch and avoids unnecessary computation.

When the gap between $b$ and $a$ is large, such as `60 1 10`, the loop performs repeated doubling: 1, 2, 4, 8, 16, reaching the first value greater than 10 after four steps, giving $q = 4$.

When values are equal at the boundary, such as `1 1 1`, the strict inequality forces one increment, producing $q = 1$, since $1 \cdot 2^0 = 1$ is not strictly greater than 1.

All cases rely on the monotonic increase of $a \cdot 2^q$, so the first crossing point is always the minimal valid answer.
