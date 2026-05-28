---
title: "CF 80A - Panoramix's Prediction"
description: "We are given two numbers representing the number of Roman soldiers defeated on two consecutive days. The first number, n, is guaranteed to be prime. The second number, m, is larger than n. The task is to determine whether m is exactly the next prime number after n."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 80
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 69 (Div. 2 Only)"
rating: 800
weight: 80
solve_time_s: 93
verified: false
draft: false
---

[CF 80A - Panoramix's Prediction](https://codeforces.com/problemset/problem/80/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 1m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two numbers representing the number of Roman soldiers defeated on two consecutive days. The first number, `n`, is guaranteed to be prime. The second number, `m`, is larger than `n`.

The task is to determine whether `m` is exactly the next prime number after `n`. Not just any larger prime, but the immediate one. For example, after `3` the next prime is `5`, so `(3, 5)` should produce `YES`. But `(3, 7)` should produce `NO` because `5` exists in between.

The constraints are extremely small. Both values are at most `50`, so even a very slow primality-checking approach is completely safe. A brute-force search through all numbers after `n` would perform only a few dozen operations in the worst case. There is no need for advanced number theory or sieves.

The main danger in this problem is misunderstanding what “next prime” means. A careless implementation might only check whether both `n` and `m` are prime and whether `m > n`. That would incorrectly accept inputs like:

```
3 7
```

The correct answer is:

```
NO
```

because `5` is the next prime after `3`, not `7`.

Another subtle case appears when there is exactly one composite number between the primes:

```
7 11
```

The correct output is:

```
YES
```

because `8`, `9`, and `10` are all composite, making `11` the immediate next prime after `7`.

A buggy implementation might stop at the first odd number greater than `n`, assuming it is prime. That would fail here because `9` is not prime.

## Approaches

The brute-force idea is straightforward. Starting from `n + 1`, test every number until we find a prime. Once we discover the first prime larger than `n`, we compare it with `m`. If they match, print `YES`; otherwise print `NO`.

Primality testing itself can also be done naively. For a number `x`, try dividing it by every integer from `2` to `x - 1`. If any divisor works, the number is composite; otherwise it is prime.

Even this fully naive version is fast enough. The largest possible value is only `50`, so the worst-case operation count is tiny.

The key observation is that we do not need to generate all primes up to `50`. We only care about the first prime after one specific number. That lets us reduce the work to a small linear scan with a simple primality test.

The brute-force solution already fits comfortably within the limits, so the “optimal” solution is really just a cleaner and slightly improved version. Instead of checking divisibility up to `x - 1`, we can stop at `sqrt(x)`. If a number has a divisor larger than its square root, the paired divisor must be smaller than the square root and would already have been found.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n√n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers `n` and `m`.
2. Create a helper function `is_prime(x)` that checks whether `x` is prime.

The function tries all divisors from `2` up to `sqrt(x)`. If any divisor divides evenly, the number is composite.
3. Start checking numbers from `n + 1` upward.

We are searching for the first prime larger than `n`.
4. For each candidate number, call `is_prime(candidate)`.

The first candidate that returns `True` is the next prime after `n`.
5. Compare this next prime with `m`.

If they are equal, print `YES`. Otherwise print `NO`.

### Why it works

The algorithm explicitly searches for the smallest prime greater than `n`. By definition, that value is the next prime after `n`.

The scan checks numbers in increasing order, so the first prime encountered must be the immediate next one. Since we compare that exact value against `m`, the algorithm returns `YES` only when `m` is truly the next prime after `n`.

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

The `is_prime` function implements the standard square-root optimization. If `x` has a divisor larger than `sqrt(x)`, the matching paired divisor must be smaller than `sqrt(x)`, so checking beyond that point is unnecessary.

The main loop starts from `n + 1` because the next prime must be larger than `n`. It keeps moving upward until it encounters the first prime number.

The moment that prime is found, the program compares it with `m` and immediately prints the answer. Returning immediately is important because we only care about the first prime after `n`, not later primes.

A common off-by-one mistake is starting the search from `n` instead of `n + 1`. Since `n` itself is prime, that would incorrectly treat `n` as its own next prime.

## Worked Examples

### Example 1

Input:

```
3 5
```

| Step | Candidate | Prime? | Action |
| --- | --- | --- | --- |
| 1 | 4 | No | Continue |
| 2 | 5 | Yes | Compare with `m` |

The first prime after `3` is `5`, which matches `m`, so the output is `YES`.

### Example 2

Input:

```
3 7
```

| Step | Candidate | Prime? | Action |
| --- | --- | --- | --- |
| 1 | 4 | No | Continue |
| 2 | 5 | Yes | Compare with `m` |

The algorithm stops as soon as it finds `5`, because that is the next prime after `3`. Since `5 != 7`, the output is `NO`.

This trace demonstrates why checking only whether `m` is prime is insufficient. `7` is prime, but it is not the immediate next prime.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n√n) | We scan numbers after `n`, and each primality test checks up to `sqrt(x)` divisors |
| Space | O(1) | Only a few integer variables are used |

Since the maximum value is only `50`, the actual runtime is tiny. The program finishes almost instantly and uses negligible memory.

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

    def solve():
        n, m = map(int, input().split())

        candidate = n + 1

        while True:
            if is_prime(candidate):
                return "YES" if candidate == m else "NO"

            candidate += 1

    return solve()

# provided sample
assert run("3 5\n") == "YES", "sample 1"

# custom cases
assert run("2 3\n") == "YES", "minimum valid primes"
assert run("3 7\n") == "NO", "later prime but not next prime"
assert run("7 11\n") == "YES", "multiple composite numbers in between"
assert run("47 49\n") == "NO", "maximum range with composite target"
assert run("47 53\n") == "YES", "largest valid next-prime pair"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3` | `YES` | Smallest valid input |
| `3 7` | `NO` | Rejects non-immediate primes |
| `7 11` | `YES` | Correctly skips several composites |
| `47 49` | `NO` | Composite `m` near upper bound |
| `47 53` | `YES` | Largest next-prime transition in range |

## Edge Cases

Consider the input:

```
3 7
```

The algorithm checks `4`, then `5`. Since `5` is prime, the search stops immediately. The algorithm never reaches `7` because the next prime after `3` has already been found. Since `5 != 7`, the output is correctly `NO`.

Now consider:

```
7 11
```

The scan proceeds through `8`, `9`, and `10`, all of which fail the primality test. When the algorithm reaches `11`, it identifies it as prime and compares it with `m`. Since they match, the output is `YES`.

Finally, consider the smallest valid case:

```
2 3
```

The search starts from `3`. Since `3` is prime and equals `m`, the algorithm prints `YES`. This confirms that starting from `n + 1` handles boundary values correctly.
