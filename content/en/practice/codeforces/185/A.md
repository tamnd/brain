---
title: "CF 185A - Plant"
description: "We start with exactly one upward-pointing triangle. Every year, each triangle splits into four smaller triangles. Three of them keep the same orientation as the parent, while one flips direction. The input gives the number of years n."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 185
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 118 (Div. 1)"
rating: 1300
weight: 185
solve_time_s: 98
verified: true
draft: false
---

[CF 185A - Plant](https://codeforces.com/problemset/problem/185/A)

**Rating:** 1300  
**Tags:** math  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with exactly one upward-pointing triangle. Every year, each triangle splits into four smaller triangles. Three of them keep the same orientation as the parent, while one flips direction.

The input gives the number of years `n`. After those `n` years of growth, we must compute how many triangles point upward. Since the number grows extremely fast, the answer is required modulo `1000000007`.

The bound on `n` is the real challenge here. It can be as large as `10^18`, which immediately rules out any simulation that processes each triangle individually. Even iterating year by year is suspicious unless each step is constant time. We need something logarithmic in `n`, because `10^18` operations are impossible within any realistic time limit.

The first subtle edge case is `n = 0`.

Input:

```
0
```

Correct output:

```
1
```

No growth has happened yet, so the original upward triangle still exists. A careless recurrence that starts from year `1` without defining the base case properly will fail here.

Another easy mistake is misunderstanding how downward triangles behave. Some implementations incorrectly assume every triangle always creates three upward triangles and one downward triangle. That is only true for upward parents.

Suppose we have one downward triangle. After one year it produces:

- three downward triangles
- one upward triangle

The orientation inheritance matters. Ignoring it gives completely wrong results after the first step.

A third common issue is overflow in languages with fixed-size integers. The number of triangles grows exponentially, roughly like `4^n`. Even for moderate `n`, this exceeds 64-bit integers. Modular arithmetic must be applied throughout the computation.

## Approaches

The most direct approach is to track how many upward and downward triangles exist after each year.

Let:

- `U(n)` be the number of upward triangles after `n` years
- `D(n)` be the number of downward triangles after `n` years

An upward triangle creates:

- `3` upward
- `1` downward

A downward triangle creates:

- `1` upward
- `3` downward

That gives the transitions:

```
U(n+1) = 3U(n) + D(n)
D(n+1) = U(n) + 3D(n)
```

Starting from:

```
U(0) = 1
D(0) = 0
```

This simulation is completely correct. Each year is processed in constant time, so the complexity is `O(n)`.

The problem is the size of `n`. With `n = 10^18`, even one operation per year is far too slow.

The key observation is that the recurrence has a very regular structure. Add the two equations together:

```
U(n+1) + D(n+1)
= 4(U(n) + D(n))
```

Since initially:

```
U(0) + D(0) = 1
```

we get:

```
U(n) + D(n) = 4^n
```

Now subtract the equations:

```
U(n+1) - D(n+1)
= 2(U(n) - D(n))
```

Initially:

```
U(0) - D(0) = 1
```

so:

```
U(n) - D(n) = 2^n
```

Now we have a simple system:

```
U(n) + D(n) = 4^n
U(n) - D(n) = 2^n
```

Adding them:

```
2U(n) = 4^n + 2^n
```

Therefore:

```
U(n) = (4^n + 2^n) / 2
```

The problem is now reduced to modular exponentiation. Fast exponentiation computes powers in `O(log n)` time, which easily handles `10^18`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recurrence simulation | O(n) | O(1) | Too slow |
| Mathematical formula with fast exponentiation | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Compute `2^n mod MOD` using fast modular exponentiation.

Python's built-in `pow(base, exp, mod)` already implements binary exponentiation efficiently.
3. Compute `4^n mod MOD`.

Since `4 = 2^2`, this is also computed efficiently with modular exponentiation.
4. Add the two values modulo `MOD`.

The formula derived earlier is:

```
U(n) = (4^n + 2^n) / 2
```
5. Divide by `2` under modulo arithmetic.

Modular division is not ordinary integer division. We multiply by the modular inverse of `2`.

Because `MOD = 1000000007` is prime:

```
inverse_of_2 = 2^(MOD-2) mod MOD
```

This value equals `500000004`.
6. Print the result.

### Why it works

The recurrence precisely models the growth rules. Every upward triangle contributes three upward and one downward child, while every downward triangle contributes one upward and three downward children.

By analyzing the sum and difference of the two counts, the coupled recurrence separates into two independent geometric sequences:

```
U(n) + D(n) = 4^n
U(n) - D(n) = 2^n
```

Solving this system uniquely determines:

```
U(n) = (4^n + 2^n) / 2
```

Fast exponentiation computes the required powers correctly modulo `1000000007`, so the algorithm always produces the exact number of upward triangles modulo the required value.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007
INV2 = 500000004

n = int(input())

p2 = pow(2, n, MOD)
p4 = pow(4, n, MOD)

ans = (p2 + p4) % MOD
ans = (ans * INV2) % MOD

print(ans)
```

The implementation directly follows the derived formula.

`pow(2, n, MOD)` computes `2^n mod MOD` using binary exponentiation internally. Its complexity is logarithmic in `n`, which is why the solution works even for `10^18`.

The division by `2` is handled carefully. Writing:

```
ans = (p2 + p4) // 2
```

would be incorrect under modulo arithmetic. We must multiply by the modular inverse instead.

The modular inverse of `2` modulo `1000000007` is:

```
500000004
```

because:

```
2 × 500000004 ≡ 1 (mod 1000000007)
```

Another subtle point is applying `% MOD` after addition. Even though Python integers do not overflow, keeping values reduced modulo `MOD` is standard competitive programming practice and avoids unnecessary growth.

## Worked Examples

### Example 1

Input:

```
1
```

| Step | Value |
| --- | --- |
| `2^n mod MOD` | `2` |
| `4^n mod MOD` | `4` |
| Sum | `6` |
| Multiply by inverse of `2` | `3` |

Output:

```
3
```

After one year, the original upward triangle creates three upward triangles and one downward triangle. The answer is `3`.

### Example 2

Input:

```
2
```

| Step | Value |
| --- | --- |
| `2^n mod MOD` | `4` |
| `4^n mod MOD` | `16` |
| Sum | `20` |
| Multiply by inverse of `2` | `10` |

Output:

```
10
```

This trace confirms that the formula continues to match the recurrence after multiple generations.

We can verify manually:

- Year 1: `3` upward, `1` downward
- Year 2:

- upward contribution: `3×3 + 1×1 = 10`
- downward contribution: `3×1 + 1×3 = 6`

So the upward count is indeed `10`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Fast exponentiation processes the bits of `n` |
| Space | O(1) | Only a few integer variables are stored |

With `n` up to `10^18`, logarithmic time is easily fast enough. Binary exponentiation needs only about 60 iterations for numbers of that size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 1000000007
INV2 = 500000004

def solve():
    input = sys.stdin.readline

    n = int(input())

    p2 = pow(2, n, MOD)
    p4 = pow(4, n, MOD)

    ans = (p2 + p4) % MOD
    ans = (ans * INV2) % MOD

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("1\n") == "3\n", "sample 1"

# custom cases
assert run("0\n") == "1\n", "initial state"
assert run("2\n") == "10\n", "second generation"
assert run("3\n") == "36\n", "larger recurrence check"
assert run("1000000000000000000\n").strip().isdigit(), "very large n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1` | Correct handling of the base case |
| `1` | `3` | Single expansion step |
| `2` | `10` | Correct recurrence behavior |
| `3` | `36` | Formula consistency over multiple years |
| `10^18` | valid modular value | Performance on maximum constraint |

## Edge Cases

The first important edge case is the initial configuration.

Input:

```
0
```

Execution:

- `2^0 = 1`
- `4^0 = 1`
- `(1 + 1) / 2 = 1`

Output:

```
1
```

This confirms the algorithm correctly preserves the original upward triangle when no growth occurs.

Another tricky case is verifying that downward triangles are handled correctly.

Input:

```
2
```

The recurrence gives:

- Year 0: `(U, D) = (1, 0)`
- Year 1: `(3, 1)`
- Year 2:

```
U = 3×3 + 1 = 10
D = 3 + 3×1 = 6
```

The formula gives:

```
(4^2 + 2^2)/2 = (16 + 4)/2 = 10
```

Both methods agree exactly, showing that the derivation correctly incorporates the behavior of downward triangles.

The final important edge case is extremely large `n`.

Input:

```
1000000000000000000
```

A linear simulation would require `10^18` iterations, which is impossible. The implemented algorithm performs only logarithmic-time exponentiation, using roughly 60 multiplication steps internally. This is why it remains fast even at the upper limit.
