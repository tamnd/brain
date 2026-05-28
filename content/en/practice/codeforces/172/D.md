---
title: "CF 172D - Calendar Reform"
description: "Each year in Berland has a certain number of days. The first year has a days, the next has a + 1, and so on for n consecutive years. For a year with x days, the government chooses a month length that satisfies two conditions. First, the month length must be a perfect square."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 172
codeforces_index: "D"
codeforces_contest_name: "Croc Champ 2012 - Qualification Round"
rating: 1500
weight: 172
solve_time_s: 89
verified: true
draft: false
---

[CF 172D - Calendar Reform](https://codeforces.com/problemset/problem/172/D)

**Rating:** 1500  
**Tags:** *special, number theory  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

Each year in Berland has a certain number of days. The first year has `a` days, the next has `a + 1`, and so on for `n` consecutive years.

For a year with `x` days, the government chooses a month length that satisfies two conditions. First, the month length must be a perfect square. Second, it must divide `x` exactly so the number of months is an integer. Among all such choices, they pick the largest possible month length.

If the chosen month length is `d²`, then the number of months in that year is `x / d²`. Since every month needs one sheet of paper, the contribution of that year to the answer is exactly:

$$\frac{x}{\text{largest square divisor of }x}$$

We must compute the total number of sheets over all years from `a` to `a + n - 1`.

The constraints are large. Both `a` and `n` can reach `10^7`, and the interval length can also be close to `10^7`. A solution that factorizes every number independently with trial division would perform roughly:

$$10^7 \cdot \sqrt{10^7}$$

operations in the worst case, which is far beyond the time limit.

The key challenge is that we need information about square divisors for a huge consecutive range of integers. This strongly suggests preprocessing with a sieve-like method rather than handling numbers one by one.

There are several easy mistakes here.

A common incorrect idea is to use the largest perfect square less than or equal to the year length. That is not enough because the square must divide the year exactly.

For example:

Input:

```
10 1
```

The year has 10 days. The largest square not exceeding 10 is 9, but 9 does not divide 10. The correct square divisor is 1, so the answer is:

```
10
```

Another subtle case is when the year itself is a perfect square.

Input:

```
36 1
```

The largest square divisor is 36 itself, so the year contains only one month and contributes:

```
1
```

A careless implementation that only searches for proper divisors would incorrectly return 4 or 9 instead.

Prime numbers are another important edge case.

Input:

```
13 1
```

The only square divisor is 1, so the contribution is:

```
13
```

If the implementation assumes every number has some larger square divisor, it will fail here.

## Approaches

The direct brute-force solution is straightforward. For every year length `x`, enumerate all integers `d` such that `d² ≤ x`. Whenever `d²` divides `x`, update the best square divisor. At the end, add `x / best` to the answer.

This works because the definition is explicit. We simply test every possible square divisor and keep the largest valid one.

The problem is the running time. A single number up to `10^7` requires checking roughly `√10^7 ≈ 3162` candidates. Doing this for up to `10^7` years leads to tens of billions of operations.

We need to avoid repeated divisor searches.

The crucial observation is that the quantity we really need is:

$$\frac{x}{\text{largest square divisor of }x}$$

This value has a well-known interpretation in number theory. If we factorize:

$$x = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}$$

then the largest square divisor removes every even part of the exponents. The remaining value is:

$$p_1^{e_1 \bmod 2} p_2^{e_2 \bmod 2} \cdots p_k^{e_k \bmod 2}$$

This is called the square-free kernel of `x`.

For example:

$$108 = 2^2 \cdot 3^3$$

The largest square divisor is:

$$2^2 \cdot 3^2 = 36$$

and the remaining factor is:

$$3$$

So the year contributes 3 sheets.

Now the problem becomes much easier. We only need the square-free kernel for every number in a range up to `10^7`.

This can be computed efficiently with a sieve.

Start with `f[i] = i`. For every prime `p`, divide `f[j]` by `p²` repeatedly for all multiples `j` of `p²`. After processing all primes, `f[x]` becomes exactly the square-free kernel of `x`.

The total complexity is close to harmonic sieve complexity and easily fits within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n\sqrt{A})$ | $O(1)$ | Too slow |
| Optimal | $O(M \log \log M)$ | $O(M)$ | Accepted |

Here, `M = a + n - 1`.

## Algorithm Walkthrough

1. Read `a` and `n`, and define `m = a + n - 1`, the largest year length we need to process.
2. Create an array `f` where initially `f[i] = i` for every `1 ≤ i ≤ m`.

At the start, every number is assumed to be its own square-free kernel.
3. Build a sieve to identify primes up to `√m`.

We only care about primes whose squares fit inside the range.
4. For every prime `p`, compute `sq = p * p`.
5. Iterate through all multiples of `sq`.

Every multiple contains at least one factor of `p²`, so its square-free kernel should not contain that square factor.
6. While the current value is divisible by `sq`, divide it by `sq`.

Repeated division matters because a number may contain higher powers such as `p⁴` or `p⁶`.
7. After processing all primes, `f[x]` equals the square-free kernel of `x`.
8. Sum `f[x]` for all years `x` from `a` to `m`.
9. Print the total.

### Why it works

Every integer can be uniquely factorized into primes. Suppose:

$$x = \prod p_i^{e_i}$$

The largest square divisor removes all even contributions from the exponents:

$$\prod p_i^{2\lfloor e_i/2 \rfloor}$$

Dividing `x` by this quantity leaves:

$$\prod p_i^{e_i \bmod 2}$$

which is exactly the square-free kernel.

The sieve processes every prime square `p²` and removes it repeatedly from all affected numbers. After all such removals, every remaining prime exponent is either 0 or 1, meaning the result is square-free. Since all square factors were removed and only square factors were removed, the final value is exactly the required contribution for that year.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, n = map(int, input().split())

    m = a + n - 1

    # f[x] will become the square-free kernel of x
    f = list(range(m + 1))

    # sieve for primes
    is_prime = [True] * (m + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= m:
        if is_prime[p]:
            # remove p^2 factors from all multiples
            sq = p * p

            for x in range(sq, m + 1, sq):
                while f[x] % sq == 0:
                    f[x] //= sq

            # mark composite numbers
            for multiple in range(p * p, m + 1, p):
                is_prime[multiple] = False

        p += 1

    ans = 0
    for x in range(a, m + 1):
        ans += f[x]

    print(ans)

solve()
```

The array `f` starts as the identity mapping, so `f[x] = x`. As the sieve runs, square factors are removed from each entry until only the square-free part remains.

The repeated division loop is essential. Suppose `x = 144 = 2^4 * 3^2`. Removing `2²` only once would leave another square factor behind:

$$144 \to 36$$

but 36 still contains `2²`. The loop continues until the factor disappears completely.

The prime sieve and the square-removal process are combined in one traversal. The implementation marks composites exactly like a standard Eratosthenes sieve.

The answer can become large, potentially around:

$$10^7 \cdot 10^7$$

so Python integers are necessary. Python handles this automatically.

The memory usage is acceptable because the arrays contain roughly `10^7` elements each, which fits within the contest limit in PyPy.

## Worked Examples

### Example 1

Input:

```
25 3
```

The years are 25, 26, and 27.

| Year | Prime Factorization | Largest Square Divisor | Contribution |
| --- | --- | --- | --- |
| 25 | $5^2$ | 25 | 1 |
| 26 | $2 \cdot 13$ | 1 | 26 |
| 27 | $3^3$ | 9 | 3 |

Total:

$$1 + 26 + 3 = 30$$

Output:

```
30
```

This example demonstrates all major cases at once: a perfect square, a square-free number, and a number with a nontrivial square divisor.

### Example 2

Input:

```
10 5
```

The years are 10 through 14.

| Year | Largest Square Divisor | Contribution |
| --- | --- | --- |
| 10 | 1 | 10 |
| 11 | 1 | 11 |
| 12 | 4 | 3 |
| 13 | 1 | 13 |
| 14 | 1 | 14 |

Total:

$$10 + 11 + 3 + 13 + 14 = 51$$

Output:

```
51
```

This trace shows how composite numbers with square factors shrink dramatically while primes remain unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M \log \log M)$ | Sieve-style processing over all prime squares |
| Space | $O(M)$ | Arrays storing sieve state and square-free kernels |

Here `M = a + n - 1`.

The upper bound is `10^7`, which is large but still manageable for a linear-size sieve in optimized Python or PyPy. The algorithm avoids expensive per-number factorizations and instead processes square factors globally.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    a, n = map(int, input().split())

    m = a + n - 1

    f = list(range(m + 1))

    is_prime = [True] * (m + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= m:
        if is_prime[p]:
            sq = p * p

            for x in range(sq, m + 1, sq):
                while f[x] % sq == 0:
                    f[x] //= sq

            for multiple in range(p * p, m + 1, p):
                is_prime[multiple] = False

        p += 1

    ans = sum(f[a:m + 1])
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

    return out.strip()

# provided sample
assert run("25 3\n") == "30", "sample 1"

# minimum input
assert run("1 1\n") == "1", "minimum case"

# perfect square
assert run("36 1\n") == "1", "perfect square year"

# prime number
assert run("13 1\n") == "13", "prime year"

# repeated square factors
assert run("144 1\n") == "1", "multiple square removals"

# small interval
assert run("10 5\n") == "51", "mixed interval"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum bounds |
| `36 1` | `1` | Entire number is a square |
| `13 1` | `13` | Prime numbers remain unchanged |
| `144 1` | `1` | Repeated square-factor removal |
| `10 5` | `51` | Mixed interval behavior |

## Edge Cases

Consider the input:

```
13 1
```

The number 13 is prime. The sieve never removes any square factor because none exists. The stored value remains:

$$f[13] = 13$$

The algorithm outputs 13, which is correct because the only square divisor is 1.

Now consider:

```
36 1
```

Initially:

$$f[36] = 36$$

When processing `2² = 4`, the algorithm divides repeatedly:

$$36 \to 9$$

When processing `3² = 9`, it divides again:

$$9 \to 1$$

The final contribution is 1, meaning one month of 36 days.

A more subtle example is:

```
72 1
```

Factorization:

$$72 = 2^3 \cdot 3^2$$

The largest square divisor is:

$$2^2 \cdot 3^2 = 36$$

so the answer should be:

$$72 / 36 = 2$$

The sieve removes `2²` once:

$$72 \to 18$$

then removes `3²` once:

$$18 \to 2$$

The remaining value is exactly the square-free kernel.

Finally, consider a number with higher square powers:

```
144 1
```

Factorization:

$$144 = 2^4 \cdot 3^2$$

The repeated division loop removes `2²` twice:

$$144 \to 36 \to 9$$

then removes `3²`:

$$9 \to 1$$

Without repeated division, the algorithm would incorrectly stop at 9 instead of 1.
