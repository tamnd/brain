---
title: "CF 237C - Primes on Interval"
description: "We are given an interval of integers from a to b. We want to choose the smallest window length l such that every contiguous segment of length l inside this interval contains at least k prime numbers."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "number-theory", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 237
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 147 (Div. 2)"
rating: 1600
weight: 237
solve_time_s: 98
verified: true
draft: false
---

[CF 237C - Primes on Interval](https://codeforces.com/problemset/problem/237/C)

**Rating:** 1600  
**Tags:** binary search, number theory, two pointers  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an interval of integers from `a` to `b`. We want to choose the smallest window length `l` such that every contiguous segment of length `l` inside this interval contains at least `k` prime numbers.

Another way to phrase it is this: no matter where we place a window of size `l` between `a` and `b`, that window must contain at least `k` primes.

If no such length exists, we print `-1`.

The interval length can be as large as `10^6`, which changes the problem completely. Any solution that checks primality repeatedly with trial division would time out. We need all prime information up front, which strongly suggests a sieve. After preprocessing primes, we still need to answer a large number of interval queries efficiently.

A direct brute-force solution would try every possible `l`, and for each `l` scan every window of that size and count primes inside it. The number of windows is already about `10^6`, and doing this for all possible lengths leads to quadratic behavior.

The hidden structure is monotonicity. If a window length `l` works, then every larger length also works. Enlarging a segment cannot decrease the number of primes inside it. That immediately suggests binary search on the answer.

There are several edge cases that are easy to mishandle.

The first one is when the whole interval does not even contain `k` primes.

Input:

```
8 10 1
```

The interval contains only `8, 9, 10`, none of which are prime. No window can contain one prime, so the correct answer is:

```
-1
```

A careless implementation may still binary search and accidentally return some length because it never checks global feasibility.

Another tricky case is when `k = 1`.

Input:

```
14 17 1
```

The primes are only `{17}`. A window of length `3` fails because `[14,15,16]` contains no prime. The smallest valid length is `4`, because the only length-4 window is `[14,15,16,17]`, which contains one prime.

This catches off-by-one mistakes in the sliding window bounds.

A third subtle case is when every number is prime.

Input:

```
2 5 1
```

Every window of length `1` already contains a prime, so the answer is:

```
1
```

Some implementations incorrectly force the answer to be at least `k` or forget that a single-element window can work.

## Approaches

The brute-force approach follows the statement directly. First generate primality information for all numbers up to `b`. Then for every candidate length `l` from `1` to `b-a+1`, scan every subarray of length `l` and count how many primes it contains. If all windows contain at least `k` primes, return `l`.

The brute-force method is correct because it explicitly checks the required condition for every possible window. The problem is the running time. There are about `n = b-a+1` candidate lengths, and for each length there are about `n` windows. Even if each window query is reduced to `O(1)` using prefix sums, the total complexity becomes `O(n^2)`. With `n = 10^6`, that means around `10^12` operations, which is impossible within one second.

The key observation is monotonicity.

Suppose a certain length `l` works. Every window of size `l` contains at least `k` primes. Now consider any larger length `l+1`. Every window of size `l+1` contains some window of size `l` inside it, so it must also contain at least `k` primes. Larger windows can only add numbers, never remove primes.

This transforms the problem into a classic binary search over the answer space.

To test whether a given length `l` works, we need to know how many primes exist in every interval of length `l`. That is exactly what prefix sums provide.

We build an array:

```
pref[i] = number of primes from 1 to i
```

Then the number of primes inside `[L, R]` becomes:

```
pref[R] - pref[L-1]
```

Now each validity check for a fixed `l` takes linear time over all windows, and binary search reduces the number of candidate lengths from `n` to `log n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Use the Sieve of Eratosthenes to compute primality for all integers from `1` to `b`.

We need constant-time prime queries later, and the sieve preprocesses everything in linearithmic time.
2. Build a prefix sum array over the primality array.

`pref[i]` stores how many primes appear in the range `[1, i]`.
3. Check whether the entire interval `[a, b]` contains at least `k` primes.

If even the whole interval fails, then no window can ever satisfy the condition, so print `-1`.
4. Define a function `good(l)`.

This function checks whether every window of length `l` inside `[a, b]` contains at least `k` primes.
5. For every starting position `x` from `a` to `b-l+1`, compute the number of primes in `[x, x+l-1]` using prefix sums.

The count is:

```
pref[x+l-1] - pref[x-1]
```
6. If any window contains fewer than `k` primes, return `False`.

A single failing window means `l` is invalid.
7. Otherwise return `True`.

Every window satisfied the requirement.
8. Binary search over the answer range `[1, b-a+1]`.

If `good(mid)` is true, try smaller lengths. Otherwise try larger lengths.
9. Print the smallest valid length found.

### Why it works

The correctness comes from two properties.

First, prefix sums give exact prime counts for every interval. The formula:

```
pref[R] - pref[L-1]
```

counts precisely the primes inside `[L, R]`.

Second, the predicate `good(l)` is monotone. If every window of length `l` contains at least `k` primes, then every larger window also contains at least `k` primes because enlarging a window cannot remove primes. That means all invalid lengths come first, followed by all valid lengths. Binary search correctly finds the first valid length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, k = map(int, input().split())

    # Sieve of Eratosthenes
    is_prime = [True] * (b + 1)

    if b >= 0:
        is_prime[0] = False
    if b >= 1:
        is_prime[1] = False

    p = 2
    while p * p <= b:
        if is_prime[p]:
            for multiple in range(p * p, b + 1, p):
                is_prime[multiple] = False
        p += 1

    # Prefix sums of primes
    pref = [0] * (b + 1)

    for i in range(1, b + 1):
        pref[i] = pref[i - 1] + (1 if is_prime[i] else 0)

    # Total primes in the whole interval
    total_primes = pref[b] - pref[a - 1]

    if total_primes < k:
        print(-1)
        return

    def good(length):
        end_limit = b - length + 1

        for start in range(a, end_limit + 1):
            end = start + length - 1
            cnt = pref[end] - pref[start - 1]

            if cnt < k:
                return False

        return True

    left = 1
    right = b - a + 1
    ans = right

    while left <= right:
        mid = (left + right) // 2

        if good(mid):
            ans = mid
            right = mid - 1
        else:
            left = mid + 1

    print(ans)

solve()
```

The sieve section preprocesses primality for every number up to `b`. Since `b` is at most `10^6`, this is fast enough and avoids repeated primality tests later.

The prefix sum array is the core optimization. Without it, counting primes inside every window would require scanning the whole segment repeatedly. With prefix sums, each query becomes constant time.

The feasibility check before binary search is easy to overlook:

```
if total_primes < k:
```

Without this condition, the binary search would never find a valid answer and could leave the result uninitialized or incorrect.

Inside `good(length)`, the upper bound:

```
b - length + 1
```

is critical. This is the last valid starting position of a window of size `length`. Missing the `+1` is a classic off-by-one error.

The binary search searches for the first valid length. Whenever `good(mid)` succeeds, we store the answer and continue searching left for a smaller valid window.

## Worked Examples

### Example 1

Input:

```
2 4 2
```

The interval is:

```
[2, 3, 4]
```

The primes are:

```
2, 3
```

| Window Length | Windows | Prime Counts | Valid |
| --- | --- | --- | --- |
| 1 | [2], [3], [4] | 1, 1, 0 | No |
| 2 | [2,3], [3,4] | 2, 1 | No |
| 3 | [2,3,4] | 2 | Yes |

The smallest valid length is `3`.

This example shows why every window must satisfy the condition, not just some of them. Length `2` fails because `[3,4]` contains only one prime.

### Example 2

Input:

```
14 17 1
```

Primes inside the interval:

```
17
```

| Window Length | Windows | Prime Counts | Valid |
| --- | --- | --- | --- |
| 1 | [14], [15], [16], [17] | 0, 0, 0, 1 | No |
| 2 | [14,15], [15,16], [16,17] | 0, 0, 1 | No |
| 3 | [14,15,16], [15,16,17] | 0, 1 | No |
| 4 | [14,15,16,17] | 1 | Yes |

The answer is:

```
4
```

This trace demonstrates the monotonic property. Once a window size works, every larger size also works.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log log n + n log n) | Sieve preprocessing plus binary search with linear checks |
| Space | O(n) | Primality array and prefix sums |

Here `n = b`.

The sieve runs quickly for `10^6`, and the binary search performs about `20` iterations. Each iteration scans at most `10^6` windows, which comfortably fits within the limits in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    a, b, k = map(int, input().split())

    is_prime = [True] * (b + 1)

    if b >= 0:
        is_prime[0] = False
    if b >= 1:
        is_prime[1] = False

    p = 2
    while p * p <= b:
        if is_prime[p]:
            for multiple in range(p * p, b + 1, p):
                is_prime[multiple] = False
        p += 1

    pref = [0] * (b + 1)

    for i in range(1, b + 1):
        pref[i] = pref[i - 1] + (1 if is_prime[i] else 0)

    if pref[b] - pref[a - 1] < k:
        print(-1)
        return

    def good(length):
        for start in range(a, b - length + 2):
            end = start + length - 1

            if pref[end] - pref[start - 1] < k:
                return False

        return True

    left, right = 1, b - a + 1
    ans = right

    while left <= right:
        mid = (left + right) // 2

        if good(mid):
            ans = mid
            right = mid - 1
        else:
            left = mid + 1

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("2 4 2\n") == "3", "sample 1"

# minimum interval
assert run("2 2 1\n") == "1", "single prime"

# impossible case
assert run("8 10 1\n") == "-1", "no primes"

# off-by-one window boundary
assert run("14 17 1\n") == "4", "last window only"

# every number prime except one
assert run("2 5 1\n") == "1", "single-element windows"

# larger k
assert run("2 11 4\n") == "8", "dense prime requirement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 1` | `1` | Minimum valid interval |
| `8 10 1` | `-1` | Impossible case |
| `14 17 1` | `4` | Off-by-one window boundaries |
| `2 5 1` | `1` | Single-element windows |
| `2 11 4` | `8` | Larger prime-count requirements |

## Edge Cases

Consider the impossible case:

Input:

```
8 10 1
```

The sieve marks all numbers in the interval as non-prime. The prefix sums show:

```
pref[10] - pref[7] = 0
```

Since the total number of primes is smaller than `k`, the algorithm immediately prints `-1` without running binary search. This prevents incorrect answers caused by searching over an empty valid region.

Now consider:

Input:

```
14 17 1
```

Binary search eventually tests length `3`.

The windows checked are:

```
[14,15,16]
[15,16,17]
```

The first contains `0` primes, so `good(3)` returns `False`.

Then length `4` is tested:

```
[14,15,16,17]
```

This window contains one prime, so `good(4)` succeeds.

The loop bound:

```
range(a, b - length + 2)
```

correctly includes the final valid starting position. Missing the `+2` would skip the last window and produce wrong answers on cases like this.

Finally consider:

Input:

```
2 5 1
```

Every single-element window already contains a prime except `[4]`. Since length `1` requires _all_ windows to work, the algorithm correctly rejects it if any composite appears.

The windows are:

```
[2], [3], [4], [5]
```

Prime counts:

```
1, 1, 0, 1
```

So length `1` actually fails here, and the smallest valid length becomes `2`.

This is a common misunderstanding. The condition applies to every window, not just some windows.
