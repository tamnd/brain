---
title: "CF 237C - Primes on Interval"
description: "We are looking at every contiguous segment inside the interval $[a, b]$. For a chosen length $l$, every segment of exactly $l$ consecutive integers must contain at least $k$ prime numbers. The task is to find the smallest such $l$. If no segment length works, we print $-1$."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "number-theory", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 237
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 147 (Div. 2)"
rating: 1600
weight: 237
solve_time_s: 244
verified: true
draft: false
---

[CF 237C - Primes on Interval](https://codeforces.com/problemset/problem/237/C)

**Rating:** 1600  
**Tags:** binary search, number theory, two pointers  
**Solve time:** 4m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking at every contiguous segment inside the interval $[a, b]$. For a chosen length $l$, every segment of exactly $l$ consecutive integers must contain at least $k$ prime numbers.

The task is to find the smallest such $l$. If no segment length works, we print $-1$.

A useful way to think about the condition is this: we slide a window of length $l$ across the interval. Every possible window must contain enough primes. The answer is the minimum window size that satisfies this guarantee.

The bounds go up to $10^6$. That changes the problem completely. A direct primality test for every number inside every window would be far too slow. Even checking primality in $O(\sqrt n)$ per number would already be expensive when repeated many times.

The interval itself can also be as large as $10^6$, which means an $O(n^2)$ sliding-window simulation is impossible. Around $10^{12}$ operations would be required in the worst case.

The size limit strongly suggests two standard tools:

First, we should precompute primes with a sieve in roughly linear or $n \log \log n$ time.

Second, we should avoid testing every possible length directly with brute force. The condition has monotonic behavior: if some length $l$ works, then every larger length also works. That makes binary search natural.

There are several edge cases that can silently break incorrect implementations.

Consider:

```
1 2 2
```

The interval contains only one prime, namely 2. No segment can contain two primes, so the correct answer is:

```
-1
```

A careless solution may binary search forever or incorrectly return the interval length.

Another tricky case is:

```
2 2 1
```

There is exactly one number and it is prime. The answer is:

```
1
```

Off-by-one mistakes in the window boundaries often fail here because there is only one valid segment.

This case is also important:

```
14 16 1
```

There are no primes at all. Every segment fails. The correct output is:

```
-1
```

An implementation that only checks the largest window may incorrectly accept length 3 because it forgets that the segment itself still contains zero primes.

Finally, consider:

```
2 10 2
```

Length 3 fails because the segment $[8,10]$ contains only one prime, namely 9 is composite and 10 is composite. Length 4 succeeds. The answer is:

```
4
```

This catches implementations that only test some windows instead of all of them.

## Approaches

The brute-force approach is straightforward. For every possible length $l$, we examine every window of size $l$ inside $[a,b]$. For each window, we count how many primes it contains. The first valid $l$ is the answer.

The brute-force idea is correct because it directly implements the definition from the problem. The problem is the amount of repeated work. If the interval length is $n$, then there are $O(n)$ candidate lengths and $O(n)$ windows for each length. Counting primes inside each window naively costs another $O(n)$. The total complexity becomes $O(n^3)$, which is completely unusable for $n = 10^6$.

Even after improving prime counting with prefix sums, we still get $O(n^2)$, because we would test every possible length and every window.

The key observation is monotonicity.

Suppose length $l$ works. Every window of size $l$ has at least $k$ primes. Now consider a larger length $l+1$. Every window of size $l+1$ contains some window of size $l$, so it must also contain at least $k$ primes. Larger windows can only gain numbers, never lose them.

That means the predicate:

```
"length l works"
```

changes from false to true exactly once.

Whenever a property behaves like this, binary search becomes possible.

To check a fixed length efficiently, we precompute prime counts with a prefix sum array. Then the number of primes inside any interval can be queried in $O(1)$.

The final structure becomes:

First, generate all primes up to $10^6$ with the Sieve of Eratosthenes.

Second, build a prefix sum array where:

$$pref[i] = \text{number of primes from } 1 \text{ to } i$$

Third, binary search the minimum valid length.

Each validity check scans all windows once, so it costs $O(n)$. Binary search performs $O(\log n)$ checks.

The total complexity becomes $O(n \log n)$, which easily fits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ to $O(n^3)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Build a sieve up to $b$ to determine which numbers are prime.

The sieve lets us answer primality queries in constant time after preprocessing.
2. Construct a prefix sum array over the interval of primality values.

If `is_prime[x]` is 1 for primes and 0 otherwise, then:

$$pref[i] = pref[i-1] + is\_prime[i]$$

Using this array, the number of primes inside $[L,R]$ becomes:

$$pref[R] - pref[L-1]$$
3. Before binary search, check whether the entire interval contains at least $k$ primes.

If even the whole range fails, no solution exists.
4. Binary search on the answer $l$.

The search range is from 1 to $b-a+1$.
5. For a candidate length $mid$, slide a window of size $mid$ across the interval.

For every starting position $x$, compute the number of primes inside:

$$[x, x+mid-1]$$

using the prefix sums.
6. If every window contains at least $k$ primes, then this length works.

Try smaller lengths by moving the binary search left boundary.
7. Otherwise, some window failed.

We need a larger window, so move the binary search right boundary.
8. Print the smallest valid length found.

### Why it works

The correctness depends on one monotonic property.

If a window length $l$ satisfies the condition, every larger length also satisfies it. Any larger window fully contains at least one valid smaller window, so it cannot have fewer than $k$ primes.

Because of this monotonic transition from invalid to valid, binary search always converges to the minimum acceptable length.

The prefix sums are correct because each range count is computed as the difference between cumulative counts. Every validity check examines all possible windows, so no failing segment can be missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, k = map(int, input().split())

    limit = b

    is_prime = [True] * (limit + 1)

    if limit >= 0:
        is_prime[0] = False
    if limit >= 1:
        is_prime[1] = False

    p = 2
    while p * p <= limit:
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
        p += 1

    pref = [0] * (limit + 1)

    for i in range(1, limit + 1):
        pref[i] = pref[i - 1] + (1 if is_prime[i] else 0)

    total_primes = pref[b] - pref[a - 1]

    if total_primes < k:
        print(-1)
        return

    def works(length):
        end_start = b - length + 1

        for left in range(a, end_start + 1):
            right = left + length - 1

            prime_count = pref[right] - pref[left - 1]

            if prime_count < k:
                return False

        return True

    left = 1
    right = b - a + 1
    answer = right

    while left <= right:
        mid = (left + right) // 2

        if works(mid):
            answer = mid
            right = mid - 1
        else:
            left = mid + 1

    print(answer)

solve()
```

The sieve section computes primality for every number up to $b$. Starting from $p^2$ is important because smaller multiples were already removed by earlier primes. Forgetting this does not break correctness, but it wastes time.

The prefix sum array converts range prime counting into constant time queries. This is the main optimization that keeps the sliding-window checks efficient.

The early impossibility check is subtle but important. If the whole interval contains fewer than $k$ primes, no window can possibly satisfy the requirement. Skipping this check still works logically, but binary search would never find a valid answer.

The `works(length)` function is where most off-by-one errors happen.

The last valid starting position is:

```
b - length + 1
```

because the window is:

```
[left, left + length - 1]
```

If the loop goes too far, the right endpoint exceeds $b$.

The binary search keeps the invariant that all valid answers are on the right side of the current search space. Whenever a length works, we continue searching smaller values to find the minimum one.

## Worked Examples

### Example 1

Input:

```
2 4 2
```

The interval is:

```
2 3 4
```

Primes are:

```
2, 3
```

| Length | Window | Prime Count | Valid |
| --- | --- | --- | --- |
| 2 | [2,3] | 2 | Yes |
| 2 | [3,4] | 1 | No |
| 3 | [2,4] | 2 | Yes |

Binary search eventually concludes that length 2 fails while length 3 succeeds.

The answer is:

```
3
```

This example demonstrates why every window must be checked. One successful window is not enough.

### Example 2

Input:

```
2 10 2
```

Primes are:

```
2, 3, 5, 7
```

Testing length 3:

| Window | Prime Count | Valid |
| --- | --- | --- |
| [2,4] | 2 | Yes |
| [3,5] | 2 | Yes |
| [4,6] | 1 | No |
| [5,7] | 2 | Yes |
| [6,8] | 1 | No |
| [7,9] | 1 | No |
| [8,10] | 1 | No |

Testing length 4:

| Window | Prime Count | Valid |
| --- | --- | --- |
| [2,5] | 3 | Yes |
| [3,6] | 2 | Yes |
| [4,7] | 2 | Yes |
| [5,8] | 2 | Yes |
| [6,9] | 1 | No |

Testing length 5:

| Window | Prime Count | Valid |
| --- | --- | --- |
| [2,6] | 3 | Yes |
| [3,7] | 3 | Yes |
| [4,8] | 2 | Yes |
| [5,9] | 2 | Yes |
| [6,10] | 1 | No |

Testing length 6:

| Window | Prime Count | Valid |
| --- | --- | --- |
| [2,7] | 4 | Yes |
| [3,8] | 3 | Yes |
| [4,9] | 2 | Yes |
| [5,10] | 2 | Yes |

The minimum valid length is 6.

This trace shows the monotonic behavior clearly. Once a length becomes valid, all larger lengths remain valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((b-a+1)\log(b-a+1) + b \log \log b)$ | Sieve preprocessing plus binary search with linear checks |
| Space | $O(b)$ | Sieve and prefix arrays |

The sieve easily fits within the limits for $10^6$. Binary search performs roughly 20 checks at most, and each check scans the interval once. The total runtime stays comfortably within one second in Python.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        a, b, k = map(int, input().split())

        limit = b

        is_prime = [True] * (limit + 1)

        if limit >= 0:
            is_prime[0] = False
        if limit >= 1:
            is_prime[1] = False

        p = 2
        while p * p <= limit:
            if is_prime[p]:
                for multiple in range(p * p, limit + 1, p):
                    is_prime[multiple] = False
            p += 1

        pref = [0] * (limit + 1)

        for i in range(1, limit + 1):
            pref[i] = pref[i - 1] + (1 if is_prime[i] else 0)

        total_primes = pref[b] - pref[a - 1]

        if total_primes < k:
            return "-1"

        def works(length):
            for left in range(a, b - length + 2):
                right = left + length - 1

                prime_count = pref[right] - pref[left - 1]

                if prime_count < k:
                    return False

            return True

        left = 1
        right = b - a + 1
        answer = right

        while left <= right:
            mid = (left + right) // 2

            if works(mid):
                answer = mid
                right = mid - 1
            else:
                left = mid + 1

        return str(answer)

    return solve()

# provided sample
assert run("2 4 2\n") == "3", "sample 1"

# custom cases
assert run("2 2 1\n") == "1", "single prime"
assert run("1 2 2\n") == "-1", "not enough primes"
assert run("14 16 1\n") == "-1", "interval without primes"
assert run("2 10 2\n") == "6", "off-by-one sliding window"
assert run("1 10 1\n") == "4", "minimum guaranteed prime coverage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 1` | `1` | Single-element interval |
| `1 2 2` | `-1` | Impossible case |
| `14 16 1` | `-1` | No primes at all |
| `2 10 2` | `6` | Correct window boundaries |
| `1 10 1` | `4` | Binary search correctness |

## Edge Cases

Consider:

```
1 2 2
```

The interval contains only one prime, namely 2.

The prefix sum check computes:

```
total_primes = 1
```

Since $1 < 2$, the algorithm immediately prints:

```
-1
```

No binary search is attempted.

Now examine:

```
2 2 1
```

The interval length is exactly 1.

Binary search operates on:

```
left = 1
right = 1
```

The single window is:

```
[2,2]
```

It contains one prime, so the algorithm returns:

```
1
```

This confirms the implementation handles minimum boundaries correctly.

Finally, consider:

```
14 16 1
```

All numbers are composite.

The sieve marks:

```
14 -> composite
15 -> composite
16 -> composite
```

The total prime count becomes zero, so the algorithm prints:

```
-1
```

This case verifies that the solution does not accidentally accept large windows when the interval itself contains insufficient primes.
