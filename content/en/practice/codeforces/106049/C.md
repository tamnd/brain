---
title: "CF 106049C - Alyona Loves Ranges"
description: "We are given a number n and a range of allowed values [l, r]. We need to find the smallest integer x inside this range such that the greatest common divisor of n and x is also inside the same range. If no such x exists, we print -1."
date: "2026-06-25T12:33:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106049
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #44 (DIV3.5-Forces)"
rating: 0
weight: 106049
solve_time_s: 41
verified: true
draft: false
---

[CF 106049C - Alyona Loves Ranges](https://codeforces.com/problemset/problem/106049/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number `n` and a range of allowed values `[l, r]`. We need to find the smallest integer `x` inside this range such that the greatest common divisor of `n` and `x` is also inside the same range. If no such `x` exists, we print `-1`.

The important observation comes from the definition of gcd. Whatever value `gcd(n, x)` is, it must divide `n`. Also, it can never be larger than `x`. This means every valid answer is connected to a divisor of `n`.

The input contains up to `1000` test cases. The values of `n`, `l`, and `r` can be as large as `10^9`, so iterating over every value in `[l, r]` is impossible. The range itself may contain a billion numbers. We need an approach that depends on the size of `n`'s factorization instead. Checking up to `sqrt(n)` is acceptable because `sqrt(10^9)` is only about `31623`, giving around `3.2 * 10^7` operations over all test cases.

The tricky cases come from confusing a valid gcd with a valid `x`. A number can have a valid gcd without itself being the smallest possible answer. For example, if the input is:

```
6 5 6
```

The values in the range are `5` and `6`. The first value gives `gcd(6,5)=1`, which is invalid. The second gives `gcd(6,6)=6`, so the answer is `6`. A solution that only checks whether the range contains some value with a non-trivial gcd may incorrectly accept `5`.

Another edge case is when a divisor exists but lies below `l`. For:

```
12 7 11
```

The divisors of `12` are `1, 2, 3, 4, 6, 12`. The only divisor inside or above the range is `12`, but it is outside the range because `12 > 11`. No valid `x` exists, so the answer is `-1`. A careless implementation that finds the next divisor after `l` without checking `r` would fail.

A final boundary case is a single-element range:

```
10 1 1
```

The only possible answer is `1`. Since `gcd(10,1)=1`, the output is `1`. This tests whether the algorithm handles `l = r` correctly.

## Approaches

A straightforward method would try every possible `x` from `l` to `r`, compute `gcd(n, x)`, and return the first value that works. This is correct because we examine candidates in increasing order, so the first valid one is automatically minimal.

The problem is the size of the range. If `l = 1` and `r = 10^9`, this requires up to a billion gcd calculations for a single test case. With up to `1000` tests, the worst case is far beyond what the time limit allows.

The key observation is that a valid gcd must be a divisor of `n`. Suppose `x` is a valid answer and `d = gcd(n, x)`. Since `d` divides `n` and `d` is inside `[l, r]`, the number `d` itself is also a valid choice because `gcd(n, d) = d`. Also, `d <= x`, so replacing `x` with `d` never makes the answer worse.

This transforms the problem completely. We only need to find the smallest divisor of `n` that belongs to `[l, r]`. Since `n` is at most `10^9`, we can enumerate divisors by checking pairs around `sqrt(n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(r - l + 1) per test case | O(1) | Too slow |
| Optimal | O(sqrt(n)) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate through all possible divisor candidates `i` from `1` to `sqrt(n)`. If `i` divides `n`, then both `i` and `n / i` are divisors.
2. For every found divisor, check whether it belongs to `[l, r]`. Keep the smallest valid divisor seen so far.
3. After all divisors are processed, output the smallest stored value. If no divisor was inside the range, output `-1`.

The reason checking up to `sqrt(n)` is enough is that every divisor greater than `sqrt(n)` has a matching divisor smaller than `sqrt(n)`. The pair `(i, n / i)` lets us discover both sides of the factorization.

Why it works: Every possible valid answer can be reduced to a divisor of `n`. The algorithm examines every divisor of `n`, so it cannot miss a valid candidate. Since it always keeps the smallest divisor in the required interval, the final value is exactly the minimum possible `x`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, l, r):
    ans = 10**18
    i = 1
    while i * i <= n:
        if n % i == 0:
            if l <= i <= r and i < ans:
                ans = i
            other = n // i
            if l <= other <= r and other < ans:
                ans = other
        i += 1

    return -1 if ans == 10**18 else ans

def main():
    t = int(input())
    out = []
    for _ in range(t):
        n, l, r = map(int, input().split())
        out.append(str(solve_case(n, l, r)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The function `solve_case` performs the divisor search. The loop condition `i * i <= n` is enough because every factor pair has one member at most the square root.

When a divisor `i` is found, the code also checks `n // i`, which is the paired divisor. This avoids missing large divisors that may be inside the interval. The answer starts with a very large value instead of `None`, which makes the minimum comparison simple.

The main function reads all test cases and collects the answers before printing. The implementation uses integer arithmetic only, so there are no overflow concerns in Python.

## Worked Examples

### Sample 1

Input:

```
6 5 7
```

The divisors of `6` are checked.

| divisor candidate | valid range check | current answer |
| --- | --- | --- |
| 1 | no | none |
| 2 | no | none |
| 3 | no | none |
| 6 | yes | 6 |

The smallest divisor inside `[5,7]` is `6`, so the answer is `6`.

### Sample 2

Input:

```
10 1 10
```

| divisor candidate | valid range check | current answer |
| --- | --- | --- |
| 1 | yes | 1 |
| 2 | yes | 1 |
| 5 | yes | 1 |
| 10 | yes | 1 |

The first valid divisor is `1`, and no later divisor can improve it. The answer is `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(n)) | We test divisor candidates only up to the square root of `n` |
| Space | O(1) | Only a few integer variables are stored |

The maximum of `sqrt(10^9)` is about `31623`, so even across all test cases the number of operations stays small enough for the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    main()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided samples
assert solve("""3
6 5 7
10 1 10
2 3 4
""") == """6
1
-1
""", "samples"

# minimum size
assert solve("""1
1 1 1
""") == """1
""", "single value"

# all divisors outside the range
assert solve("""1
12 7 11
""") == """-1
""", "no divisor"

# catches missing large divisor checks
assert solve("""1
999983 999982 999983
""") == """999983
""", "prime number"

# several divisor choices, smallest must be chosen
assert solve("""1
100 20 100
""") == """20
""", "smallest divisor"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Handles the smallest possible range |
| `12 7 11` | `-1` | Detects cases with no divisor in the interval |
| `999983 999982 999983` | `999983` | Checks large prime behavior |
| `100 20 100` | `20` | Ensures the minimum divisor is chosen |

## Edge Cases

For the input:

```
6 5 6
```

The algorithm checks divisors of `6`. It finds `1`, `2`, `3`, and `6`. Only `6` lies in the required interval, so the answer becomes `6`. This handles the case where values in the range are not automatically valid.

For:

```
12 7 11
```

The divisor search finds `1`, `2`, `3`, `4`, `6`, and `12`. None are between `7` and `11`, so the stored answer remains unchanged and the algorithm prints `-1`. The range check prevents accepting a divisor that is outside the allowed interval.

For:

```
10 1 1
```

The first divisor found is `1`, which immediately becomes the answer. The algorithm still finishes the divisor scan, but no other value can be smaller. This covers a range containing exactly one possible value.
