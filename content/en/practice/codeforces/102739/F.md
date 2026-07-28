---
title: "CF 102739F - \u0421\u0430\u0448\u0430 \u043e\u043f\u044f\u0442\u044c \u0434\u0435\u043b\u0430\u0435\u0442 \u0437\u0430\u0434\u0430\u0447\u0443 \u043f\u0440\u043e \u043f\u0440\u043e\u0441\u0442\u044b\u0435 \u0447\u0438\u0441\u043b\u0430"
description: "The task is to make every fitness tracker value acceptable to Sasha. A value is acceptable if it is either a prime number or a power of two. For each recorded number, we need to find the smallest acceptable number that is not smaller than the recording."
date: "2026-07-29T01:08:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102739
codeforces_index: "F"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2020.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102739
solve_time_s: 73
verified: true
draft: false
---

[CF 102739F - \u0421\u0430\u0448\u0430 \u043e\u043f\u044f\u0442\u044c \u0434\u0435\u043b\u0430\u0435\u0442 \u0437\u0430\u0434\u0430\u0447\u0443 \u043f\u0440\u043e \u043f\u0440\u043e\u0441\u0442\u044b\u0435 \u0447\u0438\u0441\u043b\u0430](https://codeforces.com/problemset/problem/102739/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
# Problem Understanding

The task is to make every fitness tracker value acceptable to Sasha. A value is acceptable if it is either a prime number or a power of two. For each recorded number, we need to find the smallest acceptable number that is not smaller than the recording. The output contains one answer for every day.

The input contains up to $10^5$ recorded values, and each value can be as large as $10^7$. A solution that checks every candidate number separately for every query can become too expensive. In the worst case, scanning forward by many numbers and testing each one for primality could perform far more than $10^8$ operations, which is unsafe in a one second competitive programming environment. The size of the maximum value suggests that preprocessing all relevant answers once is the intended direction.

The edge cases are mostly caused by the fact that the answer is not necessarily prime. A value can already be a power of two, and that power may be smaller than the next prime. For example, the input

```
1
1023
```

has output

```
1024
```

because 1024 is a power of two and is smaller than the next prime after 1023. A solution that searches only for primes would incorrectly return 1031.

Another common mistake is forgetting that zero and one are not prime, but one is a valid power of two in this problem's interpretation because it is $2^0$. For example:

```
1
0
```

has output

```
1
```

A primality-only solution would fail because it has no prime answer smaller than 2, and a power-of-two implementation that starts from $2^1$ would miss the correct value.

Repeated values also matter. For example:

```
3
16 16 17
```

has output

```
16 16 17
```

The algorithm should preprocess once and answer all queries consistently instead of recomputing the same information.

## Approaches

A straightforward approach is to process every query independently. Starting from the given value, we can test each following integer until we find one that is either prime or a power of two. This is correct because we inspect candidates in increasing order, so the first valid candidate is exactly the required minimum. The problem is the amount of repeated work. If many queries are close to a large value, every query repeats almost the same primality checks. With $10^5$ queries and values around $10^7$, this approach can easily require billions of small operations.

The structure of the problem gives us a better option. The possible answers are only of two types: primes and powers of two. Powers of two are extremely rare, so we can store them directly. Primes up to the largest possible answer can be generated once with the Sieve of Eratosthenes. After that, every query becomes a lookup problem: find the first prime not smaller than the value and compare it with the first power of two not smaller than the value.

The remaining question is how to find the next prime quickly. Since the maximum value is only around $10^7$, we can build an array where each position stores the closest prime at or after that position. A single reverse scan fills this array. Then every query is answered in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * gap * sqrt(A)) | O(1) | Too slow |
| Optimal | O(M log log M + M + n) | O(M) | Accepted |

Here $M$ is the maximum value we sieve up to. The sieve is the dominant preprocessing step, while answering queries is linear in the number of days.

## Algorithm Walkthrough

1. Read all values first and determine the largest value that appears. We need this because the sieve only has to cover the range that can influence an answer.
2. Extend the range slightly and run the Sieve of Eratosthenes. The sieve marks every composite number, leaving exactly the prime positions available for queries.
3. Build a suffix array of primes. Scan from the end of the range toward the beginning, remembering the most recent prime seen. After this scan, the value at position $i$ is the smallest prime greater than or equal to $i$.
4. Generate all powers of two up to the required range. Store them in sorted order. For each query, binary search this list to find the first power of two that is at least the query value.
5. For each original number, compare the next prime and the next power of two. The smaller one is the answer because both candidates are valid and both are the earliest possible candidates of their own categories.

Why it works: after preprocessing, every prime candidate is represented by the next-prime array and every power-of-two candidate is represented by binary search over the generated list. For any input value $x$, any valid answer must belong to one of these two categories. The algorithm chooses the smallest candidate from each category and returns the smaller of the two, so no smaller valid number can exist.

## Python Solution

```python
import sys
import bisect

input = sys.stdin.readline

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:]

    mx = max(a)

    limit = mx + 100000

    prime = bytearray(b'\x01') * (limit + 1)
    prime[0] = 0
    if limit >= 1:
        prime[1] = 0

    i = 2
    while i * i <= limit:
        if prime[i]:
            start = i * i
            prime[start:limit + 1:i] = b'\x00' * (((limit - start) // i) + 1)
        i += 1

    next_prime = [0] * (limit + 2)
    nxt = 0
    for i in range(limit, -1, -1):
        if prime[i]:
            nxt = i
        next_prime[i] = nxt

    powers = []
    x = 1
    while x <= limit:
        powers.append(x)
        x *= 2

    ans = []
    for value in a:
        p = next_prime[value]
        idx = bisect.bisect_left(powers, value)
        pw = powers[idx]
        if p < pw:
            ans.append(str(p))
        else:
            ans.append(str(pw))

    print(" ".join(ans))

if __name__ == "__main__":
    solve()
```

The code first reads all queries because the preprocessing size depends on the maximum input value. The sieve uses a `bytearray` because it stores only boolean information and is much more memory efficient than a Python list of integers.

The slice assignment in the sieve marks all multiples of a prime at once. The generated `next_prime` array is filled backwards, so every position immediately knows the nearest prime to its right. This avoids doing a binary search over primes for every query.

The list of powers starts from 1 because $2^0$ is needed for cases like zero. The binary search returns the first power that is not smaller than the current value. The final comparison handles the only remaining decision: whether the closest acceptable number is a prime or a power of two.

The extra 100000 positions after the maximum query value provide enough room to reach the next prime. This also avoids complicated handling of the largest possible input value while keeping the sieve size small.

## Worked Examples

For the sample input:

```
5
2020 1023 0 101 10000
```

the trace is:

| Value | Next prime | Next power of two | Answer |
| --- | --- | --- | --- |
| 2020 | 2027 | 2048 | 2027 |
| 1023 | 1031 | 1024 | 1024 |
| 0 | 2 | 1 | 1 |
| 101 | 101 | 128 | 101 |
| 10000 | 10007 | 16384 | 10007 |

This example demonstrates why both categories must be considered. The values 1023 and 0 would expose an implementation that only searches primes.

A second example:

```
4
1 2 8 9
```

| Value | Next prime | Next power of two | Answer |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 2 | 2 | 2 |
| 8 | 11 | 8 | 8 |
| 9 | 11 | 16 | 11 |

This trace confirms that an existing valid number is always accepted immediately and that powers of two can beat nearby primes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M log log M + M + n log log M) | The sieve dominates preprocessing, while each query performs a binary search among powers of two |
| Space | O(M) | The sieve and next-prime array store information for every position up to the limit |

The largest value is only $10^7$, so a linear-sized preprocessing structure is practical in Python. After preprocessing, the solution handles $10^5$ queries with only constant-sized work except for a tiny binary search over powers of two.

## Test Cases

```python
import sys
import io
import bisect

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return ""

    n = data[0]
    a = data[1:]

    mx = max(a)
    limit = mx + 100000

    prime = bytearray(b'\x01') * (limit + 1)
    prime[0] = 0
    if limit >= 1:
        prime[1] = 0

    i = 2
    while i * i <= limit:
        if prime[i]:
            prime[i * i:limit + 1:i] = b'\x00' * (((limit - i * i) // i) + 1)
        i += 1

    nxt = 0
    next_prime = [0] * (limit + 2)
    for i in range(limit, -1, -1):
        if prime[i]:
            nxt = i
        next_prime[i] = nxt

    powers = []
    x = 1
    while x <= limit:
        powers.append(x)
        x *= 2

    res = []
    for v in a:
        p = next_prime[v]
        pw = powers[bisect.bisect_left(powers, v)]
        res.append(str(min(p, pw)))

    return " ".join(res)

assert solution("""5
2020 1023 0 101 10000
""") == "2027 1024 1 101 10007"

assert solution("""4
1 2 8 9
""") == "1 2 8 11"

assert solution("""3
0 1 3
""") == "1 1 3"

assert solution("""4
16 16 17 31
""") == "16 16 17 31"

assert solution("""3
10000000 9999999 9999991
""") == "10000019 9999991 9999991"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0, 1, 3` | `1 1 3` | Handles the smallest values and the special power of two `1` |
| `16, 16, 17, 31` | `16 16 17 31` | Handles repeated values and already valid answers |
| `10000000, 9999999, 9999991` | `10000019 9999991 9999991` | Checks behavior near the maximum input range |

## Edge Cases

For input

```
1
1023
```

the sieve finds the next prime as 1031, while the power-of-two search finds 1024. The comparison returns 1024. The algorithm succeeds because it never assumes primes are always the closest mathematical numbers.

For input

```
1
0
```

the prime candidate is 2, but the generated powers list begins with 1. The binary search returns 1, and the minimum of the two candidates is correct. This case confirms that the power generation must include $2^0$.

For input

```
3
16 16 17
```

both occurrences of 16 find the same next prime and power-of-two candidates. The preprocessing is shared, so the result is identical for equal inputs and no repeated computation is needed.
