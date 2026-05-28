---
title: "CF 80A - Panoramix's Prediction"
description: "Yesterday the Gauls defeated n Roman soldiers, and n is guaranteed to be a prime number. Today they defeated m soldiers, where m n. We need to decide whether m is exactly the next prime number that comes immediately after n. The key detail is the phrase \"next prime\"."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 80
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 69 (Div. 2 Only)"
rating: 800
weight: 80
solve_time_s: 78
verified: true
draft: false
---

[CF 80A - Panoramix's Prediction](https://codeforces.com/problemset/problem/80/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

Yesterday the Gauls defeated `n` Roman soldiers, and `n` is guaranteed to be a prime number. Today they defeated `m` soldiers, where `m > n`. We need to decide whether `m` is exactly the next prime number that comes immediately after `n`.

The key detail is the phrase "next prime". It is not enough for both numbers to be prime. There must be no other prime between them.

The constraints are tiny. Both numbers are at most 50, so even very slow brute-force checking works comfortably within the time limit. A primality test by trial division up to the square root of a number takes only a few operations here. Even checking every number from `n + 1` upward is effectively instant.

The main danger is misunderstanding what qualifies as the next prime.

Consider this input:

```
3 7
```

The correct answer is:

```
NO
```

Both 3 and 7 are prime, but 5 lies between them and is also prime. A careless implementation that only checks whether `m` is prime would incorrectly print `YES`.

Another easy mistake is stopping too late while searching for the next prime.

For example:

```
7 11
```

The next prime after 7 is actually 11, because 8, 9, and 10 are composite. The algorithm must skip non-prime numbers correctly instead of assuming primes are consecutive odd numbers.

A final edge case is the smallest valid input:

```
2 3
```

The answer is:

```
YES
```

Since 2 is the first prime, the next prime after it is 3.

## Approaches

The most direct approach is to generate all prime numbers greater than `n` until reaching `m`. We could repeatedly test each integer for primality and collect primes. Once we find the first prime larger than `n`, we compare it with `m`.

This works because the constraints are extremely small. In the worst case we check numbers up to 50, and each primality test examines only a handful of divisors. Even an inefficient implementation runs instantly.

A slightly different brute-force idea is to precompute every prime up to 50 using nested loops, then scan the list to see whether `m` immediately follows `n`. That also works comfortably within the limits.

The cleaner solution uses a simple observation: we do not need all primes. We only need the very first prime greater than `n`.

So instead of generating everything, we start from `n + 1` and search upward until we encounter a prime number. That first prime is, by definition, the next prime after `n`. If it equals `m`, the answer is `YES`; otherwise it is `NO`.

This reduces the task to two small components:

1. A function that checks whether a number is prime.
2. A loop that finds the first prime larger than `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force precompute all primes up to 50 | O(50²) | O(50) | Accepted |
| Optimal direct search for next prime | O(50√50) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers `n` and `m`.
2. Write a helper function `is_prime(x)` that checks whether `x` is prime.

A number is prime if it has no divisor between 2 and `√x`. If any divisor exists, the number is composite.
3. Start checking integers from `n + 1` upward.

We are looking for the first prime larger than `n`.
4. For each candidate number, call `is_prime(candidate)`.

If the number is not prime, continue searching.
5. As soon as the first prime is found, compare it with `m`.

If they are equal, print `YES`. Otherwise print `NO`.
6. Stop immediately after finding the first prime.

We only care about the immediate next prime after `n`.

### Why it works

The algorithm searches integers in increasing order starting from `n + 1`. The first number encountered that passes the primality test is exactly the smallest prime greater than `n`, which matches the mathematical definition of the next prime.

If this number equals `m`, then `m` is the next prime after `n`. If it differs from `m`, then either `m` is not prime or another prime exists between `n` and `m`. In both cases the correct answer is `NO`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_prime(x):
    if x < 2:
        return False

    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1

    return True

def solve():
    n, m = map(int, input().split())

    candidate = n + 1

    while True:
        if is_prime(candidate):
            if candidate == m:
                print("YES")
            else:
                print("NO")
            return

        candidate += 1

solve()
```

The `is_prime` function performs trial division. It checks every divisor from 2 up to the square root of the number. If any divisor divides evenly, the number is composite.

The main loop begins at `n + 1` because we only care about numbers strictly larger than `n`. Each candidate is tested for primality. The first prime encountered is automatically the next prime after `n`.

One subtle implementation detail is stopping immediately after finding the first prime. Continuing further would be incorrect because later primes are irrelevant. Another small detail is the loop condition `d * d <= x`. This avoids missing perfect-square divisors such as 7 for 49.

## Worked Examples

### Example 1

Input:

```
3 5
```

| Step | candidate | is_prime(candidate) | Action |
| --- | --- | --- | --- |
| 1 | 4 | False | Continue |
| 2 | 5 | True | Compare with m |
| 3 | 5 | True | Print YES |

The first prime after 3 is 5, which matches `m`. The algorithm correctly prints `YES`.

### Example 2

Input:

```
7 13
```

| Step | candidate | is_prime(candidate) | Action |
| --- | --- | --- | --- |
| 1 | 8 | False | Continue |
| 2 | 9 | False | Continue |
| 3 | 10 | False | Continue |
| 4 | 11 | True | Compare with m |
| 5 | 11 | True | Print NO |

The first prime after 7 is 11, not 13. Even though 13 is prime, it is not the immediate next prime, so the correct output is `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(50√50) | At most a few dozen numbers are checked, each with trial division up to its square root |
| Space | O(1) | Only a few variables are stored |

The constraints are extremely small, so this solution easily fits within the time and memory limits. Even a much slower implementation would still pass comfortably.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def is_prime(x):
        if x < 2:
            return False

        d = 2
        while d * d <= x:
            if x % d == 0:
                return False
            d += 1

        return True

    n, m = map(int, input().split())

    candidate = n + 1

    while True:
        if is_prime(candidate):
            return "YES\n" if candidate == m else "NO\n"

        candidate += 1

# provided sample
assert run("3 5\n") == "YES\n", "sample 1"

# custom cases
assert run("2 3\n") == "YES\n", "smallest primes"

assert run("3 7\n") == "NO\n", "prime exists in between"

assert run("7 11\n") == "YES\n", "skip composite numbers correctly"

assert run("47 49\n") == "NO\n", "m is not prime"

assert run("47 53\n") == "YES\n", "largest-range valid case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3` | `YES` | Smallest valid primes |
| `3 7` | `NO` | Another prime exists between them |
| `7 11` | `YES` | Consecutive primes with composites in between |
| `47 49` | `NO` | Second number is not prime |
| `47 53` | `YES` | Correct handling near upper constraint |

## Edge Cases

Consider the input:

```
3 7
```

The algorithm starts from 4. It checks 4, which is composite, then checks 5, which is prime. Since 5 is the first prime greater than 3, it is the next prime after 3. Because 5 does not equal 7, the algorithm prints `NO`. This handles the common mistake of checking only whether `m` itself is prime.

Now consider:

```
7 11
```

The search examines 8, 9, and 10, rejecting all of them because they are composite. The first prime found is 11, so the algorithm prints `YES`. This confirms that the algorithm correctly skips arbitrary stretches of composite numbers.

Finally, consider the smallest boundary case:

```
2 3
```

The algorithm starts with candidate 3. Since 3 is prime and equals `m`, the output is `YES`. This confirms correct behavior at the lower bound of the constraints.
