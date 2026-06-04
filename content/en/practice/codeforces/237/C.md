---
title: "CF 237C - Primes on Interval"
description: "We are given an interval of integers from a to b. We want to choose a length l such that every contiguous segment of length l inside this interval contains at least k prime numbers. Among all lengths that satisfy this condition, we need the smallest one."
date: "2026-06-04T17:02:55+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "number-theory", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 237
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 147 (Div. 2)"
rating: 1600
weight: 237
solve_time_s: 162
verified: true
draft: false
---

[CF 237C - Primes on Interval](https://codeforces.com/problemset/problem/237/C)

**Rating:** 1600  
**Tags:** binary search, number theory, two pointers  
**Solve time:** 2m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an interval of integers from `a` to `b`. We want to choose a length `l` such that **every** contiguous segment of length `l` inside this interval contains at least `k` prime numbers.

Among all lengths that satisfy this condition, we need the smallest one. If no length works, we print `-1`.

Another way to view the problem is that for a candidate length `l`, we examine every window

`[x, x+l-1]`

that fits completely inside `[a, b]`. The candidate is valid only if each of those windows contains at least `k` primes.

The interval endpoints are at most `10^6`. This is the crucial constraint. Since primality information is needed repeatedly, precomputing all primes up to `10^6` with a sieve is very cheap. The interval itself can also contain up to `10^6` numbers, so any solution that checks every window separately for every possible length would perform roughly `10^12` operations and is completely infeasible.

The structure of the condition suggests a monotonic property. If a certain length `l` works, then any larger length also works. A larger window can only contain at least as many primes as the smaller window it contains. This monotonicity points directly toward binary search.

There are several easy-to-miss edge cases.

Consider:

```
14 16 1
```

There are no primes in the interval. Even the largest possible window contains zero primes, so the answer is `-1`. A careless binary search implementation might never explicitly verify that a solution exists.

Consider:

```
2 5 2
```

The window `[2,3]` contains two primes, but `[3,4]` contains only one. Looking at only a few windows is not enough. Every window must satisfy the condition.

Consider:

```
2 2 1
```

The interval contains a single prime. The only possible length is `1`, which is valid. Boundary cases where `a = b` often reveal off-by-one errors in window handling.

Consider:

```
8 12 1
```

The only prime is `11`. Length `4` works because every length-4 window contains `11`, while length `3` fails because `[8,10]` contains no prime. The minimum valid length is not necessarily related to the distance between consecutive primes alone.

## Approaches

The most direct solution is to try every possible length `l`. For each length, inspect every window of that size and count how many primes it contains. If all windows contain at least `k` primes, record the answer.

Prime counts inside a window can be computed efficiently using a prefix sum of primality values. With such a prefix sum, checking one window becomes `O(1)`. Unfortunately, there are up to `10^6` possible lengths and up to `10^6` windows per length. Even after optimizing window queries, the total work remains around `10^12`, which is far beyond the limit.

The key observation is monotonicity.

Suppose length `l` is valid. Every window of length `l` contains at least `k` primes. Now consider any larger length `L > l`. Every length-`L` window contains some length-`l` subwindow. Since that subwindow already contains at least `k` primes, the larger window also contains at least `k` primes.

This means:

- invalid lengths come first,
- valid lengths come afterward.

The answer is the first valid length, which can be found with binary search.

To test a candidate length `l`, we slide a window through `[a,b]`. Using a prefix sum of primes, we can compute the number of primes in every window in constant time. If any window contains fewer than `k` primes, the candidate fails.

The remaining ingredient is fast primality preprocessing. Since all numbers are at most `10^6`, a standard sieve of Eratosthenes computes primality for every relevant number in roughly `O(10^6 log log 10^6)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((b-a+1)²) | O(b) | Too slow |
| Optimal | O(b log log b + (b-a+1) log(b-a+1)) | O(b) | Accepted |

## Algorithm Walkthrough

1. Build a sieve of Eratosthenes up to `b` and determine which numbers are prime.
2. Construct a prefix sum array `pref` where `pref[i]` equals the number of primes from `1` through `i`.
3. Define a function `check(l)`.
4. For every starting position `x` from `a` to `b-l+1`, compute the number of primes in window `[x, x+l-1]` using:

`pref[x+l-1] - pref[x-1]`
5. If any window contains fewer than `k` primes, return `False`.
6. If all windows satisfy the requirement, return `True`.
7. Before binary searching, verify that the largest possible length works. This corresponds to the entire interval `[a,b]`.
8. If even the largest length fails, print `-1`.
9. Otherwise binary search on lengths from `1` to `b-a+1`.
10. When `check(mid)` succeeds, record it as a candidate answer and continue searching the left half.
11. When `check(mid)` fails, search the right half.
12. Print the smallest valid length found.

### Why it works

The prefix sum array guarantees that every window's prime count is computed exactly. The `check(l)` function returns true precisely when every length-`l` window contains at least `k` primes.

The crucial property is monotonicity. If length `l` is valid, any larger length is also valid because every larger window contains a valid length-`l` subwindow and thus already contains at least `k` primes. Consequently, the set of valid lengths forms a suffix of all possible lengths. Binary search on this monotone predicate finds the smallest valid length, which is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, k = map(int, input().split())

    is_prime = [True] * (b + 1)
    if b >= 0:
        is_prime[0] = False
    if b >= 1:
        is_prime[1] = False

    p = 2
    while p * p <= b:
        if is_prime[p]:
            start = p * p
            for x in range(start, b + 1, p):
                is_prime[x] = False
        p += 1

    pref = [0] * (b + 1)
    for i in range(1, b + 1):
        pref[i] = pref[i - 1] + (1 if is_prime[i] else 0)

    def count_primes(l, r):
        return pref[r] - pref[l - 1]

    def check(length):
        end_start = b - length + 1
        for start in range(a, end_start + 1):
            if count_primes(start, start + length - 1) < k:
                return False
        return True

    n = b - a + 1

    if not check(n):
        print(-1)
        return

    lo, hi = 1, n
    ans = n

    while lo <= hi:
        mid = (lo + hi) // 2

        if check(mid):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The sieve computes primality for all numbers that can appear in any window. Since every query asks for prime counts on intervals, a prefix sum is built immediately afterward.

The `check()` function is the core predicate used by binary search. It scans all windows of the candidate length and rejects the length as soon as one bad window is found. This early exit matters because many candidates fail quickly.

The existence check before binary search is essential. If the entire interval contains fewer than `k` primes, no smaller window can possibly satisfy the requirement. Without this step, binary search would incorrectly return some length even when no solution exists.

The window count uses:

```
pref[r] - pref[l - 1]
```

which is why the prefix array is indexed from `0`. This avoids special cases when `l = 1`.

## Worked Examples

### Example 1

Input:

```
2 4 2
```

Primes in the interval are `{2, 3}`.

| Length | Windows | Prime counts | Valid |
| --- | --- | --- | --- |
| 1 | [2], [3], [4] | 1, 1, 0 | No |
| 2 | [2,3], [3,4] | 2, 1 | No |
| 3 | [2,4] | 2 | Yes |

Binary search eventually reaches length `3`, which is the first valid length.

Output:

```
3
```

This example demonstrates that every window must satisfy the requirement. One failing window is enough to reject a candidate.

### Example 2

Input:

```
8 12 1
```

Primes in the interval are `{11}`.

| Length | Windows checked | Result |
| --- | --- | --- |
| 3 | [8,10] has 0 primes | Fail |
| 4 | [8,11] has 1 prime, [9,12] has 1 prime | Pass |

The minimum valid length is `4`.

Output:

```
4
```

This example shows that a single prime can still make a solution possible if every window of sufficient size is forced to include it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(b log log b + (b-a+1) log(b-a+1)) | Sieve plus binary search, each check scans all windows |
| Space | O(b) | Primality and prefix arrays up to `b` |

Since `b ≤ 10^6`, the sieve is easily affordable. The binary search performs about `20` checks at most, and each check scans at most `10^6` windows. This comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    a, b, k = map(int, input().split())

    is_prime = [True] * (b + 1)
    if b >= 0:
        is_prime[0] = False
    if b >= 1:
        is_prime[1] = False

    p = 2
    while p * p <= b:
        if is_prime[p]:
            for x in range(p * p, b + 1, p):
                is_prime[x] = False
        p += 1

    pref = [0] * (b + 1)
    for i in range(1, b + 1):
        pref[i] = pref[i - 1] + is_prime[i]

    def check(length):
        for s in range(a, b - length + 2):
            cnt = pref[s + length - 1] - pref[s - 1]
            if cnt < k:
                return False
        return True

    n = b - a + 1

    if not check(n):
        return "-1"

    lo, hi = 1, n
    ans = n

    while lo <= hi:
        mid = (lo + hi) // 2
        if check(mid):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1

    return str(ans)

# provided sample
assert run("2 4 2\n") == "3", "sample 1"

# custom cases
assert run("2 2 1\n") == "1", "single prime"
assert run("14 16 1\n") == "-1", "no primes in interval"
assert run("8 12 1\n") == "4", "single prime coverage"
assert run("2 5 1\n") == "2", "boundary windows"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 1` | `1` | Single-element interval |
| `14 16 1` | `-1` | No solution exists |
| `8 12 1` | `4` | Minimum length covering every window |
| `2 5 1` | `2` | Off-by-one handling in window ranges |

## Edge Cases

Consider:

```
14 16 1
```

The interval contains no primes. The largest possible window is `[14,16]`, whose prime count is zero. The preliminary `check(n)` fails immediately, so the algorithm prints `-1`. Binary search never starts, avoiding a false answer.

Consider:

```
2 2 1
```

There is only one window, `[2]`, containing one prime. The existence check succeeds. Binary search operates on the range `[1,1]` and returns `1`. This verifies that the implementation handles intervals of length one correctly.

Consider:

```
2 5 2
```

Length `2` fails because window `[4,5]` contains only one prime. Length `3` fails because `[3,5]` contains only one prime. Length `4` succeeds because the only window is `[2,5]`, containing three primes. The algorithm checks every window and does not incorrectly accept a length just because some windows work.

Consider:

```
8 12 1
```

The only prime is `11`. For length `3`, the first window `[8,10]` has zero primes, so the candidate is rejected immediately. For length `4`, every window includes `11`, so the candidate succeeds. This confirms the monotonic behavior that binary search relies upon.
