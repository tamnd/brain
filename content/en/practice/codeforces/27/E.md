---
title: "CF 27E - Number With The Given Amount Of Divisors"
description: "We are given a single integer n, and we need to construct the smallest positive integer whose number of divisors is exac"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 27
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 27 (Codeforces format, Div. 2)"
rating: 2000
weight: 27
solve_time_s: 94
verified: true
draft: false
---

[CF 27E - Number With The Given Amount Of Divisors](https://codeforces.com/problemset/problem/27/E)

**Rating:** 2000  
**Tags:** brute force, dp, number theory  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer `n`, and we need to construct the smallest positive integer whose number of divisors is exactly `n`.

The core mathematical fact behind the problem is the divisor formula. If a number has prime factorization

$$x = p_1^{a_1} p_2^{a_2} \cdots p_k^{a_k}$$

then the number of divisors of `x` equals

$$(a_1 + 1)(a_2 + 1)\cdots(a_k + 1)$$

The task is not to count divisors of some given number. Instead, we must reverse the process. We need to choose exponents so that their product equals `n`, then build the smallest possible number from them.

The constraint `n ≤ 1000` is small enough that we can explore many divisor decompositions recursively. The real challenge comes from the answer itself. The resulting number may be as large as `10^18`, which rules out brute forcing integers and counting divisors one by one. Even checking every number up to `10^18` is obviously impossible.

The search space of exponent combinations is also deceptive. A careless recursive solution can generate huge numbers of states or overflow while multiplying primes repeatedly. The key observation is that minimal numbers with a fixed divisor count always use small primes with non-increasing exponents. That structure shrinks the search dramatically.

Several edge cases are easy to mishandle.

For `n = 1`, the correct answer is `1`.

Input:

```
1
```

Output:

```
1
```

A recursive construction based only on multiplying primes may accidentally skip this case because the empty prime factorization corresponds to `1`.

Another subtle case is when multiple exponent arrangements produce the same divisor count. For `n = 12`, we can build:

$$12 = (3+1)(2+1)$$

which gives

$$2^3 \cdot 3^2 = 72$$

But we can also use

$$12 = (5+1)(1+1)$$

which gives

$$2^5 \cdot 3 = 96$$

Both numbers have 12 divisors, but 72 is smaller. A greedy choice based only on larger exponents fails here.

Another common mistake is assigning larger exponents to larger primes. Suppose we want divisor count `6`.

Using exponents `(2,1)` correctly gives:

$$2^2 \cdot 3 = 12$$

Swapping them gives:

$$2 \cdot 3^2 = 18$$

The second number is larger. Minimal constructions always place larger exponents on smaller primes.

Overflow is also dangerous. Even though the final answer fits in `10^18`, intermediate recursive multiplications can exceed that limit if not checked carefully.

## Approaches

The most direct brute-force idea is to iterate upward from `1`, compute the divisor count for every integer, and stop at the first one whose divisor count equals `n`.

Computing divisors for one number by trial division takes roughly `O(sqrt(x))`. The answer itself may be close to `10^18`, so even checking numbers up to a tiny fraction of that range is hopeless. This approach becomes infeasible almost immediately.

A more mathematical brute-force strategy is better. Since divisor counts come from exponent products, we can try all factorizations of `n` into terms like `(a_i + 1)`, construct the corresponding number, and keep the minimum.

This already uses the right structure, but if we generate exponent combinations carelessly, we create many duplicates and many useless states. The crucial observation is that the smallest valid number always has these properties:

First, primes are used in increasing order: `2, 3, 5, 7, ...`

Second, exponents are non-increasing:

$$a_1 \ge a_2 \ge a_3 \ge \cdots$$

Why must this be true? Suppose we had `a_i < a_j` for `i < j`. Then swapping the exponents places the larger exponent on the smaller prime, producing a smaller number while preserving the divisor count.

This transforms the problem into a bounded DFS over exponent choices.

At each step, we choose an exponent for the current prime. If we choose exponent `e`, then the divisor count multiplier becomes `(e + 1)`. We continue recursively only if `(e + 1)` divides the remaining divisor target.

Because exponents must be non-increasing, each recursive level only considers exponents up to the previous exponent. This restriction cuts the search space dramatically.

The number of states is very manageable because `n ≤ 1000`, and exponents decrease quickly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over integers | Exponential in answer size | O(1) | Too slow |
| DFS over exponent decompositions | Very small practical search, roughly O(number of valid exponent states) | O(depth) | Accepted |

## Algorithm Walkthrough

1. Prepare a small list of prime numbers starting from `2`.

The minimal answer always uses the smallest primes first, so only the first few primes are needed.
2. Start a DFS with these parameters:

`idx` = current prime index,

`last_exp` = maximum exponent allowed,

`remaining` = divisor count still needed,

`current` = current constructed number.

The `last_exp` restriction enforces non-increasing exponents.
3. If `remaining == 1`, we have successfully built a number whose divisor count matches `n`.

Compare `current` against the global minimum answer and update if smaller.
4. Try every exponent `e` from `1` to `last_exp`.

Choosing exponent `e` contributes a factor of `(e + 1)` to the divisor count.
5. Skip any exponent where `(e + 1)` does not divide `remaining`.

Such a choice can never lead to the required divisor count.
6. Multiply the current prime repeatedly to build `p^e`.

Stop immediately if multiplication would exceed the best answer already found.
7. Recurse using:

`idx + 1`,

`e` as the new maximum exponent,

`remaining // (e + 1)`,

`current * p^e`.

Passing `e` forward preserves the non-increasing exponent rule.
8. Continue until all valid exponent assignments are explored.

### Why it works

Every positive integer has a unique prime factorization, and its divisor count depends only on the exponents. The DFS enumerates all possible exponent combinations whose divisor products equal `n`.

The non-increasing exponent restriction does not remove any optimal solution. If a solution violates this order, swapping larger exponents toward smaller primes always produces a smaller number with the same divisor count. Repeated swaps eventually produce a non-increasing arrangement.

Since the DFS explores all such canonical arrangements and tracks the minimum constructed value, the final answer is guaranteed to be the smallest integer with exactly `n` divisors.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 10**18

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

n = int(input())

ans = LIMIT

def dfs(idx, last_exp, remaining, current):
    global ans

    if remaining == 1:
        ans = min(ans, current)
        return

    if idx >= len(primes):
        return

    prime = primes[idx]
    value = 1

    for exp in range(1, last_exp + 1):
        if value > ans // prime:
            break

        value *= prime

        if remaining % (exp + 1) != 0:
            continue

        nxt = current * value

        if nxt >= ans:
            continue

        dfs(idx + 1, exp, remaining // (exp + 1), nxt)

dfs(0, 64, n, 1)

print(ans)
```

The DFS builds the answer prime by prime. The parameter `remaining` stores how many divisor factors are still needed. If we choose exponent `e`, then `(e + 1)` must divide `remaining`, because that exponent contributes exactly `(e + 1)` to the divisor count formula.

The recursion starts with a very large exponent bound like `64`. The exact value is not important as long as it comfortably exceeds all realistic exponents within `10^18`.

The variable `value` incrementally stores powers of the current prime. Instead of recomputing `prime ** exp` repeatedly, we multiply once per loop iteration. This is both faster and safer.

The overflow guard:

```
if value > ans // prime:
```

prevents multiplication beyond the current best answer. This pruning is critical. Without it, intermediate numbers could exceed `10^18` and create unnecessary recursive branches.

Another subtle detail is:

```
dfs(idx + 1, exp, ...)
```

Passing `exp` instead of `last_exp` enforces non-increasing exponents. That single restriction removes huge numbers of redundant states and guarantees we only generate canonical minimal forms.

## Worked Examples

### Example 1

Input:

```
4
```

We want a number with exactly 4 divisors.

| Step | Prime | Exponent | Divisor Product | Current Number |
| --- | --- | --- | --- | --- |
| Start | - | - | 1 | 1 |
| Choose 2² | 2 | 2 | 3 | 4 |
| Cannot finish | - | - | - | - |
| Backtrack | - | - | - | - |
| Choose 2¹ | 2 | 1 | 2 | 2 |
| Choose 3¹ | 3 | 1 | 4 | 6 |

The algorithm first tries exponent `2` on prime `2`, giving divisor multiplier `3`. Since the remaining divisor target becomes impossible, it backtracks.

Then it tries exponents `(1,1)`:

$$(1+1)(1+1)=4$$

which constructs:

$$2^1 \cdot 3^1 = 6$$

This is the smallest valid number.

### Example 2

Input:

```
12
```

| Step | Prime | Exponent | Divisor Product | Current Number |
| --- | --- | --- | --- | --- |
| Start | - | - | 1 | 1 |
| Choose 2³ | 2 | 3 | 4 | 8 |
| Choose 3² | 3 | 2 | 12 | 72 |
| Candidate found | - | - | 12 | 72 |
| Choose 2⁵ | 2 | 5 | 6 | 32 |
| Choose 3¹ | 3 | 1 | 12 | 96 |

The trace shows why exponent ordering matters. Both exponent sets produce 12 divisors:

$$(3+1)(2+1)=12$$

and

$$(5+1)(1+1)=12$$

But the smaller constructed number is 72, so the DFS keeps it as the best answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(number of valid exponent states) | DFS explores only divisor-compatible exponent combinations |
| Space | O(depth of recursion) | Depth is bounded by the number of used primes |

The practical search space is tiny because `n ≤ 1000`, exponents decrease monotonically, and pruning removes large branches quickly. The recursion depth never exceeds a small constant, so both time and memory easily fit within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    LIMIT = 10**18
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

    n = int(input())
    ans = LIMIT

    def dfs(idx, last_exp, remaining, current):
        nonlocal ans

        if remaining == 1:
            ans = min(ans, current)
            return

        if idx >= len(primes):
            return

        prime = primes[idx]
        value = 1

        for exp in range(1, last_exp + 1):
            if value > ans // prime:
                break

            value *= prime

            if remaining % (exp + 1) != 0:
                continue

            nxt = current * value

            if nxt >= ans:
                continue

            dfs(idx + 1, exp, remaining // (exp + 1), nxt)

    dfs(0, 64, n, 1)

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("4\n") == "6", "sample 1"

# custom cases
assert run("1\n") == "1", "minimum case"
assert run("2\n") == "2", "prime divisor count"
assert run("6\n") == "12", "mixed exponents"
assert run("12\n") == "60", "multiple exponent decompositions"
assert run("24\n") == "360", "larger divisor structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Empty prime factorization case |
| `2` | `2` | Single prime exponent |
| `6` | `12` | Combination of exponents `(2,1)` |
| `12` | `60` | Competing exponent decompositions |
| `24` | `360` | Deeper recursive branching |

## Edge Cases

For input:

```
1
```

the DFS starts with `remaining = 1`. The base case triggers immediately, and the algorithm returns `1`.

This corresponds to the empty factorization:

$$1 = 1$$

whose divisor count is also `1`.

For input:

```
6
```

the divisor count can be formed as:

$$6 = (2+1)(1+1)$$

The DFS constructs:

$$2^2 \cdot 3 = 12$$

If exponents were assigned in the opposite order, we would get:

$$2 \cdot 3^2 = 18$$

The non-increasing exponent restriction prevents this larger construction.

For input:

```
12
```

multiple exponent decompositions exist:

$$12 = 12$$

gives:

$$2^{11} = 2048$$

while:

$$12 = (3+1)(2+1)$$

gives:

$$2^3 \cdot 3^2 = 72$$

and:

$$12 = (4+1)(1+1)$$

gives:

$$2^4 \cdot 3 = 48$$

Actually the smallest valid answer is:

$$2^2 \cdot 3 \cdot 5 = 60$$

because:

$$(2+1)(1+1)(1+1)=12$$

The DFS explores every valid exponent decomposition and keeps the minimum.

Overflow pruning becomes important for larger inputs. Suppose a branch already produces a number larger than the current best answer. The condition:

```
if nxt >= ans:
    continue
```

stops exploring that branch immediately. This avoids both useless work and accidental overflow during deeper multiplications.
