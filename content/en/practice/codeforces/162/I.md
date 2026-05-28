---
title: "CF 162I - Truncatable primes"
description: "We are given a single integer and must decide whether it satisfies a very specific prime property. A number is considered truncatable if every suffix formed by repeatedly removing the leftmost digit is still prime."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 162
codeforces_index: "I"
codeforces_contest_name: "VK Cup 2012 Wild-card Round 1"
rating: 2000
weight: 162
solve_time_s: 82
verified: true
draft: false
---

[CF 162I - Truncatable primes](https://codeforces.com/problemset/problem/162/I)

**Rating:** 2000  
**Tags:** *special  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer and must decide whether it satisfies a very specific prime property.

A number is considered truncatable if every suffix formed by repeatedly removing the leftmost digit is still prime. For example, starting from `9137`, we check:

`9137`, `137`, `37`, `7`

All four numbers are prime, so the answer is `"YES"`.

The number must also contain no digit `0`. A value like `103` immediately fails even if some suffixes happen to be prime, because the definition explicitly forbids zeros.

The input limit is at most `10^7`, which is small enough that direct primality testing is completely practical. A square root primality check for one number takes about `O(sqrt(n))` operations. Since a number up to `10^7` has at most 8 digits, we only need to test at most 8 suffixes. Even in the worst case, this is only a few tens of thousands of arithmetic operations, far below the time limit.

The tricky part is not performance, it is correctly generating and validating every suffix.

One easy mistake is forgetting that single digit suffixes must also be prime.

Consider:

```
19
```

The suffixes are:

`19`, `9`

Even though `19` itself is prime, `9` is not, so the correct answer is `"NO"`.

Another common bug is ignoring the restriction on zeros.

Consider:

```
1013
```

The suffixes are:

`1013`, `13`, `3`

All of them are prime, but the number still fails because it contains a zero. The correct answer is `"NO"`.

A third subtle issue is treating `1` as prime.

Consider:

```
11
```

The suffixes are:

`11`, `1`

Since `1` is not prime, the answer must be `"NO"`.

A careless implementation that uses an incorrect primality test might accidentally accept it.

## Approaches

The most direct solution is to generate every suffix and independently test whether it is prime.

Suppose the number is represented as a string. We can repeatedly remove the first character:

```
9137
137
37
7
```

For each value, we run a primality test. If any suffix is composite, or if the original number contains a zero, we immediately answer `"NO"`.

This brute-force idea is already fast enough because the input is tiny. A number up to `10^7` has at most 8 suffixes. Each primality test costs at most `O(sqrt(n))`, which is about `3162` iterations in the worst case. Even multiplying these together gives a very small runtime.

There is no need for sieves, preprocessing, or probabilistic primality tests. The constraints are designed so that straightforward trial division passes comfortably.

The key observation is that the number of suffixes is extremely small. Instead of searching through many candidate numbers, we only validate one chain of at most 8 values. That reduces the problem to repeated primality checking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force using naive divisor check up to n | O(n) per suffix | O(1) | Too slow conceptually |
| Optimal using square root primality test | O(d × sqrt(n)) | O(1) | Accepted |

Here, `d` is the number of digits, at most 8.

## Algorithm Walkthrough

1. Read the integer as a string.

Using a string makes suffix generation simple and avoids repeated digit extraction logic.
2. Check whether the string contains the digit `'0'`.

If it does, immediately print `"NO"` because truncatable primes are not allowed to contain zeros.
3. Generate every suffix of the number.

For index `i`, the suffix is `s[i:]`.
4. Convert each suffix to an integer and test whether it is prime.

A number is prime if:

- it is at least 2
- no integer from `2` to `sqrt(x)` divides it
5. If any suffix is not prime, print `"NO"` and stop.
6. If all suffixes are prime, print `"YES"`.

### Why it works

The algorithm directly matches the definition of a truncatable prime.

Every valid suffix is checked exactly once. The zero restriction is enforced before any primality testing. The primality test correctly rejects `1` and all composite numbers.

Since the answer is `"YES"` only when all suffixes satisfy the prime condition, and `"NO"` otherwise, the algorithm is correct.

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
    s = input().strip()

    if '0' in s:
        print("NO")
        return

    for i in range(len(s)):
        value = int(s[i:])

        if not is_prime(value):
            print("NO")
            return

    print("YES")

solve()
```

The solution starts by reading the number as a string because suffixes are naturally represented this way. Using string slicing avoids manual arithmetic for removing leading digits.

The zero check happens first because it is an immediate disqualifier. There is no reason to spend time on primality testing if the number already violates the definition.

The `is_prime` function uses standard trial division up to the square root. If a composite number exists, at least one factor must be at most `sqrt(x)`, so checking beyond that point is unnecessary.

The condition `x < 2` is critical. Without it, the suffix `1` would incorrectly be treated as prime.

The loop iterates through every suffix `s[i:]`. The moment one suffix fails, the algorithm exits early with `"NO"`. This keeps the implementation simple and efficient.

## Worked Examples

### Example 1

Input:

```
19
```

| Step | Suffix | Prime? |
| --- | --- | --- |
| 1 | 19 | Yes |
| 2 | 9 | No |

The second suffix is `9`, which is composite. The algorithm immediately prints `"NO"`.

This example demonstrates that being prime itself is not enough. Every suffix must also remain prime.

### Example 2

Input:

```
9137
```

| Step | Suffix | Prime? |
| --- | --- | --- |
| 1 | 9137 | Yes |
| 2 | 137 | Yes |
| 3 | 37 | Yes |
| 4 | 7 | Yes |

All suffixes are prime, so the algorithm prints `"YES"`.

This trace confirms the invariant that every remaining suffix must independently satisfy primality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d × sqrt(n)) | At most `d` suffixes, each checked with square root trial division |
| Space | O(1) | Only a few variables are stored |

Since `d ≤ 8` and `sqrt(10^7) ≈ 3162`, the runtime is tiny compared to the 3 second limit. The solution easily fits within both time and memory constraints.

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
        s = input().strip()

        if '0' in s:
            return "NO"

        for i in range(len(s)):
            if not is_prime(int(s[i:])):
                return "NO"

        return "YES"

    return solve()

# provided sample
assert run("19\n") == "NO", "sample 1"

# custom cases
assert run("9137\n") == "YES", "valid truncatable prime"
assert run("2\n") == "YES", "single digit prime"
assert run("11\n") == "NO", "suffix becomes 1"
assert run("1013\n") == "NO", "contains zero"
assert run("9999991\n") == "NO", "large composite suffix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `9137` | `YES` | Typical successful chain of prime suffixes |
| `2` | `YES` | Smallest valid prime |
| `11` | `NO` | Correct handling of suffix `1` |
| `1013` | `NO` | Zero digit rejection |
| `9999991` | `NO` | Larger values and composite detection |

## Edge Cases

Consider the input:

```
11
```

The suffixes are:

```
11
1
```

The algorithm first checks `11`, which is prime. It then checks `1`. Since the primality function explicitly rejects all numbers below `2`, the algorithm correctly prints `"NO"`.

Now consider:

```
1013
```

Before generating suffixes, the algorithm detects the digit `'0'` in the string. It immediately returns `"NO"` without any further work. This exactly matches the definition.

Finally, consider the smallest valid case:

```
2
```

There is only one suffix, `2` itself. The primality test succeeds, so the algorithm prints `"YES"`.

This confirms that single digit primes are accepted correctly.
