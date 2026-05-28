---
title: "CF 58B - Coins"
description: "We are given the value of the largest coin denomination, n. We must build a sequence of distinct coin values such that every larger coin is divisible by every smaller coin. Among all valid sequences, we want the one containing the maximum possible number of coins."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 58
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 54 (Div. 2)"
rating: 1300
weight: 58
solve_time_s: 111
verified: false
draft: false
---

[CF 58B - Coins](https://codeforces.com/problemset/problem/58/B)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are given the value of the largest coin denomination, `n`. We must build a sequence of distinct coin values such that every larger coin is divisible by every smaller coin. Among all valid sequences, we want the one containing the maximum possible number of coins.

The output must list the denominations from largest to smallest.

The divisibility condition creates a chain structure. If the coins are:

```
a1 > a2 > a3 > ...
```

then every earlier value must be divisible by every later value. In particular:

```
a1 % a2 == 0
a2 % a3 == 0
a1 % a3 == 0
```

and so on.

The limit is only `10^6`, which is small enough for trial division and repeated factor operations. Even an `O(sqrt(n))` algorithm is easily fast enough within 2 seconds. On the other hand, generating and checking all subsets or all divisor chains would explode combinatorially and is unnecessary.

The tricky part is understanding what "maximum number of coins" really means. A careless solution might try to jump directly from `n` to `1`, but that wastes opportunities to insert intermediate divisors.

For example:

Input:

```
12
```

A valid sequence is:

```
12 1
```

but it is not maximal. We can insert more values:

```
12 6 3 1
```

Another common mistake is dividing by arbitrary divisors instead of the smallest possible prime factor. Suppose we start from `60`.

If we divide aggressively:

```
60 -> 10 -> 1
```

we only get three coins.

If we remove factors one at a time:

```
60 -> 30 -> 15 -> 5 -> 1
```

the chain becomes longer.

The edge case `n = 1` is also easy to mishandle. There are no smaller positive divisors to add, so the answer is simply:

```
1
```

## Approaches

A brute-force approach would try to generate all divisors of `n`, then search for the longest divisibility chain among them. Since every pair in the chain must divide correctly, we could sort divisors and run dynamic programming similar to longest increasing subsequence.

This works because the divisibility relation forms a partial order. If `a` divides `b`, then `a` can appear after `b` in the sequence.

The problem is that this approach solves a much harder problem than necessary. Even though `n ≤ 10^6` keeps the divisor count manageable, building all chains and transitions is still unnecessary work.

The key observation is that maximizing the number of coins means we should reduce the number as slowly as possible.

Suppose the current coin is `x`. The next coin must be a proper divisor of `x`. To maximize how many steps remain, we want the next value to stay as large as possible while still being smaller than `x`.

The best move is dividing by the smallest prime factor of `x`.

For example:

```
60 -> 30
```

is better than:

```
60 -> 20
```

because removing only one prime factor preserves more divisibility steps later.

Each operation removes exactly one prime factor from the factorization of the number. Since a number with factorization

```
n = p1^a1 * p2^a2 * ...
```

contains exactly `a1 + a2 + ...` prime factors counting multiplicity, the longest possible chain removes them one at a time until reaching `1`.

So the algorithm becomes simple:

Start from `n`. Repeatedly divide by its smallest prime factor and print each intermediate value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d²) where d is the number of divisors | O(d) | Unnecessarily complicated |
| Optimal | O(sqrt(n)) | O(1) excluding output | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Print the current value of `n` because the sequence must start from the largest denomination.
3. While `n` is greater than `1`, find the smallest divisor of `n` larger than `1`.

We search from `2` upward until we find a divisor. The first divisor found is always the smallest prime factor.
4. Divide `n` by this smallest prime factor.

This removes exactly one prime factor from the number, which gives the slowest possible decrease and maximizes the remaining chain length.
5. Print the new value of `n`.
6. Repeat until `n` becomes `1`.

At every step, the new value divides the previous value because it is obtained by dividing by an integer factor. Since divisibility is transitive, every larger coin remains divisible by every smaller coin later in the sequence.

### Why it works

The longest chain is obtained by removing prime factors one at a time.

Suppose we have a current number `x`. Any next value must be:

```
x / d
```

where `d` is a divisor greater than `1`.

If `d` is composite, then removing it discards multiple prime factors at once. That shortens the possible chain because fewer intermediate divisors remain.

Dividing by the smallest prime factor removes exactly one prime factor and keeps the next number as large as possible. Repeating this process guarantees that every prime factor contributes one extra coin to the sequence, which is the maximum achievable length.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

ans = []

while True:
    ans.append(str(n))

    if n == 1:
        break

    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            n //= d
            break
    else:
        n = 1

print(" ".join(ans))
```

The solution maintains the current denomination in `n` and repeatedly appends it to the answer sequence.

The loop stops only after printing `1`, since `1` must also appear as the final coin.

The inner loop searches for the smallest divisor starting from `2`. The first divisor found is automatically the smallest prime factor. Dividing by it removes exactly one prime factor from the factorization.

The `else` attached to the `for` loop is important. It runs only if no divisor was found. That means the current `n` is prime. A prime number has only one proper divisor, namely `1`, so the next step must become `1`.

A common mistake is forgetting to print the initial value before starting divisions. Another easy bug is stopping immediately when `n` becomes prime, which would skip the final `1`.

The square root bound keeps divisor search efficient. Since `n` shrinks after every step, the total running time stays very small.

## Worked Examples

### Example 1

Input:

```
10
```

| Current n | Smallest Prime Factor | Next n | Output So Far |
| --- | --- | --- | --- |
| 10 | 2 | 5 | 10 |
| 5 | prime | 1 | 10 5 |
| 1 | - | - | 10 5 1 |

The sequence becomes:

```
10 5 1
```

This trace shows how prime numbers immediately transition to `1`, since they have no intermediate divisors.

### Example 2

Input:

```
72
```

| Current n | Smallest Prime Factor | Next n | Output So Far |
| --- | --- | --- | --- |
| 72 | 2 | 36 | 72 |
| 36 | 2 | 18 | 72 36 |
| 18 | 2 | 9 | 72 36 18 |
| 9 | 3 | 3 | 72 36 18 9 |
| 3 | prime | 1 | 72 36 18 9 3 |
| 1 | - | - | 72 36 18 9 3 1 |

Final output:

```
72 36 18 9 3 1
```

This example demonstrates the core greedy idea. The algorithm removes one prime factor at a time, producing the maximum possible number of denominations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(n)) | Each step searches divisors up to sqrt(current n), and n rapidly decreases |
| Space | O(1) excluding output | Only a few variables are used |

With `n ≤ 10^6`, this easily fits within the limits. Even in the worst case, divisor checks remain small because the number shrinks after every division.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    ans = []

    while True:
        ans.append(str(n))

        if n == 1:
            break

        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                n //= d
                break
        else:
            n = 1

    return " ".join(ans)

# provided sample
assert run("10\n") == "10 5 1", "sample 1"

# minimum value
assert run("1\n") == "1", "n = 1"

# prime number
assert run("13\n") == "13 1", "prime input"

# power of two
assert run("16\n") == "16 8 4 2 1", "repeated smallest factor"

# mixed prime factors
assert run("60\n") == "60 30 15 5 1", "multiple distinct factors"

# maximum bound style case
out = run("1000000\n")
assert out.startswith("1000000 "), "large input handled"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Smallest possible input |
| `13` | `13 1` | Prime numbers jump directly to 1 |
| `16` | `16 8 4 2 1` | Repeated prime factors |
| `60` | `60 30 15 5 1` | Greedy removal of one factor at a time |
| `1000000` | Valid long chain | Performance near upper bound |

## Edge Cases

Consider the smallest input:

```
1
```

The algorithm immediately appends `1` to the answer and stops. No divisor search occurs because there is no smaller positive divisor. The output is correctly:

```
1
```

Now consider a prime number:

```
13
```

The divisor search checks all integers from `2` to `sqrt(13)` and finds none. The `for-else` branch triggers, setting the next value to `1`.

The sequence becomes:

```
13 1
```

This is optimal because a prime number has no divisors other than `1`.

Finally, consider a number with many repeated factors:

```
16
```

The execution goes:

```
16 -> 8 -> 4 -> 2 -> 1
```

Each step divides by `2`, removing only one prime factor at a time. A careless solution dividing by larger factors might produce:

```
16 -> 4 -> 1
```

which is valid but not maximal. The greedy strategy correctly preserves the longest possible chain.
