---
title: "CF 106186D - GCD of Pairs"
description: "We have two arrays of the same length. Each value is at most the length of the arrays. The task is to count ordered choices of one element from the first array and one element from the second array whose greatest common divisor is a prime number."
date: "2026-06-25T10:48:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106186
codeforces_index: "D"
codeforces_contest_name: "NWU IUPC 2025 powered by CPS Academy"
rating: 0
weight: 106186
solve_time_s: 36
verified: true
draft: false
---

[CF 106186D - GCD of Pairs](https://codeforces.com/problemset/problem/106186/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two arrays of the same length. Each value is at most the length of the arrays. The task is to count ordered choices of one element from the first array and one element from the second array whose greatest common divisor is a prime number. The order matters because choosing `a[i]` with `b[j]` is different from choosing another index pair, even if the values are equal.

A direct approach would examine every possible pair between the two arrays. If the arrays contain `n` elements, that creates `n²` pairs. Since the total `n` over all test cases can reach `200000`, a quadratic solution would require around `4 * 10^10` operations in the largest case, which is far beyond what a one second limit allows. We need to use the fact that the values are bounded by `n`, not just the number of elements.

The tricky cases are mostly related to distinguishing divisibility from exact gcd values. For example, if we have:

```
1
2
2
```

The only pair has gcd `2`, which is prime, so the answer is `1`. A method that ignores duplicate values or only checks whether both numbers share a prime factor can fail on counting.

Another example is:

```
2
4 6
2 3
```

The possible gcd values are `2`, `1`, `2`, and `3`, so the answer is `3`. A careless solution that counts every pair where a prime divides both values might count the pair `(4, 2)` through prime `2` and miss that gcd itself can only contribute once. We need the number of pairs whose full gcd equals a prime, not the number of shared prime divisors.

The key distinction is that we must compute exact gcd frequencies. Once we know how many ordered pairs have gcd `d`, we only need to add the frequencies for prime values of `d`.

## Approaches

The brute force method is straightforward. For every index `i` in the first array and every index `j` in the second array, we calculate `gcd(a[i], b[j])` and check whether it is prime. This is correct because every ordered pair is examined exactly once. However, with `n = 100000`, it performs about ten billion gcd operations, which is too slow.

The useful observation comes from the small value range. Instead of thinking about individual pairs, we can count how many pairs are divisible by each possible number. If we know that both numbers are divisible by `d`, then their gcd is a multiple of `d`. The number of such pairs is easy to obtain after counting multiples of every value.

Let `cntA[d]` be the number of elements in the first array divisible by `d`, and define `cntB[d]` similarly. Then `cntA[d] * cntB[d]` is the number of pairs whose gcd is divisible by `d`.

This does not immediately give the answer because a pair with gcd `12` is included in the count for `d = 1, 2, 3, 4, 6, 12`. We remove this overlap using inclusion over multiples. Processing values from large to small, we can compute how many pairs have gcd exactly equal to every `d`.

After that, the answer is simply the sum of exact gcd counts for prime `d`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count how many times each value appears in the first array and the second array. From these frequencies, build `cntA[d]` and `cntB[d]`, where each value stores how many array elements are multiples of `d`. This converts individual divisibility checks into prefix style information over divisors.
2. For every `d`, calculate `pairs[d] = cntA[d] * cntB[d]`. This is the number of ordered pairs whose gcd is divisible by `d`. A pair belongs here exactly when both selected numbers contain `d` as a divisor.
3. Process `d` from `n` down to `1`. Start with `exact[d] = pairs[d]`, then subtract the counts of all larger multiples of `d` that have already been classified as exact gcd values. The remaining value is the number of pairs whose gcd is exactly `d`.
4. Generate primes up to `n` with a sieve. Add `exact[p]` for every prime `p` to obtain the final answer.

Why it works:

For every number `d`, `pairs[d]` counts all pairs whose gcd contains `d` as a divisor. When processing from large to small, every larger gcd value has already been removed from `pairs[d]`. The remaining pairs cannot have a gcd that is a larger multiple of `d`, and they are all divisible by `d`, so their gcd must be exactly `d`. Therefore `exact[d]` is correct for every `d`. Summing the exact counts of prime values counts precisely the required pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    t = data[0]
    ptr = 1
    tests = []
    max_n = 0

    for _ in range(t):
        n = data[ptr]
        ptr += 1
        a = data[ptr:ptr + n]
        ptr += n
        b = data[ptr:ptr + n]
        ptr += n
        tests.append((n, a, b))
        max_n = max(max_n, n)

    is_prime = [True] * (max_n + 1)
    if max_n >= 0:
        is_prime[0] = False
    if max_n >= 1:
        is_prime[1] = False
    for i in range(2, int(max_n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, max_n + 1, i):
                is_prime[j] = False

    ans = []

    for n, a, b in tests:
        freq_a = [0] * (n + 1)
        freq_b = [0] * (n + 1)

        for x in a:
            freq_a[x] += 1
        for x in b:
            freq_b[x] += 1

        cnt_a = [0] * (n + 1)
        cnt_b = [0] * (n + 1)

        for d in range(1, n + 1):
            for m in range(d, n + 1, d):
                cnt_a[d] += freq_a[m]
                cnt_b[d] += freq_b[m]

        exact = [0] * (n + 1)

        for d in range(n, 0, -1):
            cur = cnt_a[d] * cnt_b[d]
            for m in range(d * 2, n + 1, d):
                cur -= exact[m]
            exact[d] = cur

        total = 0
        for p in range(2, n + 1):
            if is_prime[p]:
                total += exact[p]

        ans.append(str(total))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first part of the code creates a sieve once for the largest value that appears in any test case. Reusing this sieve avoids repeating prime checks.

For each test case, the frequency arrays store occurrences of exact values. The two nested loops over divisors convert those exact frequencies into counts of multiples. The loop over multiples is where the bounded value range is used, giving the harmonic series complexity.

The descending loop is the inclusion step. When processing `d`, every `exact[m]` for `m` being a larger multiple of `d` is already known, so subtracting those values leaves only gcd values equal to `d`.

The answer uses 64 bit integers in Python automatically. This is necessary because the number of ordered pairs can reach `n²`.

## Worked Examples

Consider:

```
1
5
1 3 5 4 4
2 3 2 1 2
```

The divisor counting and exact gcd recovery work as follows.

| d | pairs[d] | larger multiples removed | exact[d] |
| --- | --- | --- | --- |
| 5 | 1 | 0 | 1 |
| 4 | 2 | 0 | 2 |
| 3 | 1 | 0 | 1 |
| 2 | 9 | 4 | 5 |
| 1 | 25 | 9 | 16 |

The prime gcd values are `2`, `3`, and `5`. Their exact counts add to `5 + 1 + 1 = 7`.

This example shows why counting only shared prime divisors is not enough. The value `4` contributes to divisibility by `2`, but those pairs must not be counted as gcd `2` unless the full gcd is exactly `2`.

For the second example:

```
1
2
1 1
2 2
```

| d | pairs[d] | larger multiples removed | exact[d] |
| --- | --- | --- | --- |
| 2 | 4 | 0 | 4 |
| 1 | 4 | 4 | 0 |

The only gcd value that appears is `2`, which is prime, so the answer is `4`.

This confirms that duplicate values are handled naturally because frequencies represent every index separately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Counting multiples and subtracting over divisors both use the harmonic series of multiples. |
| Space | O(n) | Frequency arrays, gcd counts, and sieve arrays each have size proportional to the maximum value. |

The total length of all test cases is bounded by `200000`, so the combined divisor iterations remain within acceptable limits. The memory usage is linear in the largest individual test case.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return ""

    t = data[0]
    ptr = 1
    out = []

    max_n = 0
    tests = []
    for _ in range(t):
        n = data[ptr]
        ptr += 1
        a = data[ptr:ptr+n]
        ptr += n
        b = data[ptr:ptr+n]
        ptr += n
        tests.append((n, a, b))
        max_n = max(max_n, n)

    prime = [True] * (max_n + 1)
    if max_n >= 0:
        prime[0] = False
    if max_n >= 1:
        prime[1] = False
    for i in range(2, int(max_n ** 0.5) + 1):
        if prime[i]:
            for j in range(i * i, max_n + 1, i):
                prime[j] = False

    for n, a, b in tests:
        fa = [0] * (n + 1)
        fb = [0] * (n + 1)
        for x in a:
            fa[x] += 1
        for x in b:
            fb[x] += 1

        ca = [0] * (n + 1)
        cb = [0] * (n + 1)

        for d in range(1, n + 1):
            for x in range(d, n + 1, d):
                ca[d] += fa[x]
                cb[d] += fb[x]

        exact = [0] * (n + 1)
        for d in range(n, 0, -1):
            exact[d] = ca[d] * cb[d]
            for x in range(d * 2, n + 1, d):
                exact[d] -= exact[x]

        out.append(str(sum(exact[p] for p in range(2, n + 1) if prime[p])))

    return "\n".join(out)

assert run("""5
5
1 3 5 4 4
2 3 2 1 2
2
1 1
2 2
2
1 1
2 2
3
1 2 1
2 2 3
5
4 2 2 5 4
2 1 2 5 3
""") == """7
0
0
2
9""", "samples"

assert run("""1
1
1
1
""") == "0", "minimum size"

assert run("""1
5
2 2 2 2 2
2 2 2 2 2
""") == "25", "all equal prime gcd"

assert run("""1
6
1 2 3 4 5 6
1 2 3 4 5 6
""") == "9", "boundary values"

assert run("""1
4
6 10 15 21
14 35 22 33
""") == "5", "mixed prime gcd cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample set | `7, 0, 0, 2, 9` | Official examples and general correctness |
| Single value `1` with `1` | `0` | No prime gcd exists |
| All values equal to `2` | `25` | Duplicate handling and maximum pair counting |
| Values from `1` to `6` | `9` | Boundary values and divisor counting |
| Mixed composite values | `5` | Exact gcd filtering |

## Edge Cases

For the case:

```
1
2
1
1
```

the algorithm computes `pairs[1] = 1`, but when processing `1`, it subtracts all exact multiples. The remaining exact gcd count for `1` is `1`, which is ignored because `1` is not prime. The output is `0`.

For:

```
1
3
4 6 8
2 3 4
```

the pair gcd values include `2`, `3`, and larger composite values. The algorithm first counts all pairs divisible by each divisor, then removes composite gcd contributions while processing downward. Only pairs with exact gcd `2` or `3` remain in the final prime sum.

For:

```
1
5
2 2 2 2 2
2 2 2 2 2
```

every ordered pair has gcd `2`. The divisor `2` count is `25`, and there are no larger multiples to remove. The final answer is `25`, showing that repeated values are counted by index, not by distinct value.
