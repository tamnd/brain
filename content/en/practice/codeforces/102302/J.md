---
title: "CF 102302J - Weird Sanchola"
description: "We need to transform an array into a constant array whose common value is prime. Changing one element by one costs one operation, so if the final prime is (p), the cost for an element (ai) is exactly ( [ F(p)=sum{i=1}^{N} ] The task is to find the prime (p) that minimizes this…"
date: "2026-08-13T08:01:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "J"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 1030
verified: false
draft: false
---

[CF 102302J - Weird Sanchola](https://codeforces.com/problemset/problem/102302/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 17m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We need to transform an array into a constant array whose common value is prime. Changing one element by one costs one operation, so if the final prime is (p), the cost for an element (a_i) is exactly (|a_i-p|). The total cost for choosing (p) is therefore

[
F(p)=\sum_{i=1}^{N}|a_i-p|.
]

The task is to find the prime (p) that minimizes this sum and output the minimum value.

The official constraints allow (N) to reach (10^5), while each array value can reach (10^9), with only one second available. This immediately rules out trying many possible targets and evaluating the entire array for each one. Even checking (10^6) candidates would already require around (10^{11}) distance calculations in the worst case. We need to reduce the number of candidate targets to a constant-sized set.

There are several boundary cases that can make an otherwise reasonable implementation incorrect. First, (1) is not prime. For the input

```
1
1
```

the answer is (1), because the only sensible target is (2), not (1). A primality check that treats (1) as prime would incorrectly return (0).

Second, when (N) is even, there is an entire interval of integer medians rather than one median. For

```
2
8 10
```

the median interval is ([8,10]), but neither endpoint is prime. The optimal target is (11), giving (3+1=4), while choosing only the lower median and searching downward could incorrectly miss it.

Third, the best prime can be larger than every input value. For

```
1
1000000000
```

the closest prime below is (999999937), at distance (63), while (1000000007) is also prime and is only (7) away. The correct answer is (7). An implementation that searches only up to the maximum array value would miss the optimal target.

Finally, if every element is already the same prime, no operation is needed. For

```
4
7 7 7 7
```

the answer is (0). This is a useful check that the algorithm allows the current value itself to be the target.

## Approaches

A direct brute-force solution can try every possible integer target, discard non-primes, and compute (\sum |a_i-p|) for every prime candidate. This is correct because every legal final array is represented by exactly one prime target. For these constraints, however, it is far too expensive. There are about (10^9) relevant integer targets in the input range, and evaluating one target costs (O(N)), giving roughly (10^{14}) distance calculations in the worst case. Even restricting the enumeration to primes still leaves tens of millions of possible targets.

The key observation is that the function

[
F(p)=\sum |a_i-p|
]

is minimized at a median when (p) is allowed to be any real number. More precisely, if the sorted array is

[
a_1\le a_2\le\cdots\le a_N,
]

then for odd (N), the minimum is at (a_{(N+1)/2}). For even (N), every value in the interval ([a_{N/2},a_{N/2+1}]) has the same minimum.

We are not allowed to choose an arbitrary integer, since the target must be prime. Outside the median interval, moving toward the interval can only decrease the cost. Consequently, the best prime must be either the largest prime not greater than the upper median, or the smallest prime not smaller than the lower median. If a prime lies inside the median interval, these two searches will find it.

The brute-force method works because it evaluates every possible target, but fails because almost all of those targets are irrelevant. The median property reduces the optimization to finding just two nearby primes. Since all input values are at most (10^9), primality can be tested efficiently using a precomputed list of primes up to (\sqrt{10^9+7}), which is only about (31623).

We sort the array to obtain the two middle values. Then we search downward from the upper middle value for the previous prime and upward from the lower middle value for the next prime. Only those two primes need to be evaluated.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N\cdot 10^9)) | (O(N)) | Too slow |
| Optimal | (O(N\log N + S\log\log S + G\pi(S))) | (O(N+S)) | Accepted |

Here (S=\sqrt{10^9+7}), and (G) is the number of nearby integers inspected while looking for the surrounding primes. Because the target is restricted to this fixed numeric range, the search is tiny in practice.

## Algorithm Walkthrough

1. Sort the array.

Sorting lets us identify the median interval directly. The two middle values are `a[n // 2 - 1]` and `a[n // 2]` for an even-sized array, while they are equal for an odd-sized array.
2. Let `left` be the lower middle value and `right` be the upper middle value.

The real-valued minimum of (\sum |a_i-p|) occurs somewhere between these two values. Any target below `left` becomes worse as it moves farther away, and any target above `right` behaves symmetrically.
3. Find the largest prime `p1` such that `p1 <= right`.

This is the best possible prime on the left side of the median interval. If `right` itself is prime, the search immediately returns `right`.
4. Find the smallest prime `p2` such that `p2 >= left`.

This is the best possible prime on the right side of the median interval. If there is a prime inside the median interval, `p2` will be one such prime.
5. Compute the total distance for every valid candidate among `p1` and `p2`.

We calculate

[
\sum_i |a_i-p|
]

for each candidate and keep the smaller result.
6. Print the minimum cost.

No other prime can be better because every prime below the median interval is no better than `p1`, and every prime above the interval is no better than `p2`.

The correctness invariant is that after identifying the median interval, every possible target prime can be replaced by one of the two boundary primes without increasing the cost. For a target below the interval, increasing it toward the interval decreases or preserves every relevant side of the absolute-value objective. The same argument holds for a target above the interval when moving downward. Thus only the nearest prime on each side can be optimal, and evaluating both gives the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_primes(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    p = 2
    while p * p <= limit:
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * (
                (limit - p * p) // p + 1
            )
        p += 1

    return [p for p in range(2, limit + 1) if sieve[p]]

PRIMES = build_primes(31623)

def is_prime(x):
    if x < 2:
        return False

    for p in PRIMES:
        if p * p > x:
            break
        if x % p == 0:
            return x == p

    return True

def previous_prime(x):
    while x >= 2:
        if is_prime(x):
            return x
        x -= 1
    return None

def next_prime(x):
    x = max(x, 2)
    while True:
        if is_prime(x):
            return x
        x += 1

def cost(a, p):
    return sum(abs(x - p) for x in a)

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    left = a[(n - 1) // 2]
    right = a[n // 2]

    candidates = []

    p = previous_prime(right)
    if p is not None:
        candidates.append(p)

    p = next_prime(left)
    candidates.append(p)

    answer = min(cost(a, p) for p in candidates)
    print(answer)

if __name__ == "__main__":
    solve()
```

The sieve is built once for all possible inputs. The largest value that we may need to test as a target is just above (10^9), and checking divisibility only requires primes up to its square root. A limit of `31623` safely covers (\sqrt{1000000007}).

`is_prime` first rejects values below (2), which handles the special case that (1) is not prime. It then tries only precomputed prime divisors. Once `p * p > x`, no larger divisor can be the first factor of `x`, so the number is prime.

The two search functions deliberately include their starting value. This avoids an off-by-one error when a median itself is prime. `previous_prime(right)` gives the largest prime at or below the upper median, while `next_prime(left)` gives the smallest prime at or above the lower median.

Python integers do not overflow, but the answer can be around (10^{14}), so using Python's normal integer arithmetic is necessary and sufficient. The code does not impose the input's (10^9) limit on the target, which is also necessary because the optimal prime can be (1000000007).

The array is sorted before the median positions are read. For an odd-sized array, both expressions select the same middle element. For an even-sized array, they select the two endpoints of the median interval.

## Worked Examples

For Sample 1,

```
3
2 3 10
```

the array is already sorted. The middle value is `3`, so both median boundaries are `3`.

| Step | Array | `left` | `right` | Candidate | Cost |
| --- | --- | --- | --- | --- | --- |
| Sort | `[2, 3, 10]` | 3 | 3 |  |  |
| Previous prime | `[2, 3, 10]` | 3 | 3 | 3 | 10 |
| Next prime | `[2, 3, 10]` | 3 | 3 | 3 | 10 |
| Final | `[2, 3, 10]` | 3 | 3 | 3 | 10 |

The table seems to give a cost of (10), but the optimal target is actually (5), with cost (3+2+5=10), while the sample output is (8). This exposes an important correction to the median-boundary argument: for an odd-sized array, the median is `3`, but the nearest prime on the upper side is not necessarily enough when the median itself is prime. In fact, targeting `3` costs (1+0+7=8), so the correct calculation for the candidate `3` is (8). The final answer is (8).

For Sample 2,

```
2
1 1000000000
```

the sorted array is unchanged and the median interval is `[1, 1000000000]`.

| Step | `left` | `right` | Previous prime | Next prime | Best cost |
| --- | --- | --- | --- | --- | --- |
| Median selection | 1 | 1000000000 |  |  |  |
| Prime search | 1 | 1000000000 | 999999937 | 2 |  |
| Evaluate `999999937` | 1 | 1000000000 | 999999937 | 2 | 63 |
| Evaluate `2` | 1 | 1000000000 | 999999937 | 2 | 999999998 |

The first candidate gives a cost of (999999936+63), which is (999999999). The second candidate gives (1+999999998=999999999) as well. Both are optimal, matching the sample output.

The second example also demonstrates why the even-sized median interval matters. Every integer between `1` and `1000000000` is a real-valued minimizer, so the nearest primes to either side of that interval can both achieve the same optimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N + S\log\log S + G\pi(S))) | Sorting dominates the array processing; the sieve handles primality divisors up to (S=31623), and only nearby candidates are tested |
| Space | (O(N+S)) | The sorted array and the sieve's prime list are stored |

With (N\le10^5), sorting takes roughly (N\log N) comparisons, which is easily manageable. The sieve contains only about (31623) entries, and primality testing is performed only while searching near the two median values. The memory usage is far below 256 MB.

## Test Cases

```python
import sys
import io

def build_primes(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    p = 2
    while p * p <= limit:
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * (
                (limit - p * p) // p + 1
            )
        p += 1

    return [p for p in range(2, limit + 1) if sieve[p]]

PRIMES = build_primes(31623)

def is_prime(x):
    if x < 2:
        return False

    for p in PRIMES:
        if p * p > x:
            break
        if x % p == 0:
            return x == p

    return True

def previous_prime(x):
    while x >= 2:
        if is_prime(x):
            return x
        x -= 1
    return None

def next_prime(x):
    x = max(x, 2)
    while True:
        if is_prime(x):
            return x
        x += 1

def compute(a):
    a = sorted(a)
    n = len(a)

    left = a[(n - 1) // 2]
    right = a[n // 2]

    candidates = []

    p = previous_prime(right)
    if p is not None:
        candidates.append(p)

    candidates.append(next_prime(left))

    return min(sum(abs(x - p) for x in a) for p in candidates)

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    n = data[0]
    a = data[1:1 + n]
    return str(compute(a))

# Provided samples
assert run("3\n2 3 10\n") == "8", "sample 1"
assert run("2\n1 1000000000\n") == "999999999", "sample 2"
assert run("4\n3 5 7 11\n") == "10", "sample 3"

# Minimum-size input
assert run("1\n1\n") == "1", "1 must become the prime 2"

# All elements are already the same prime
assert run("4\n7 7 7 7\n") == "0", "already fixed"

# Even-sized array with a prime inside the median interval
assert run("2\n4 6\n") == "2", "target 5 is inside the median interval"

# Maximum input value, requiring a target above the input
assert run("1\n1000000000\n") == "7", "1000000007 is only 7 away"

# Boundary around small primes
assert run("2\n2 4\n") == "2", "target 3 is optimal"

# Large array
assert run("100000\n" + " ".join(["1000000000"] * 100000)) == "0", \
    "maximum-size all-equal input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Minimum size and the fact that `1` is not prime |
| `4 / 7 7 7 7` | `0` | Already-valid array |
| `2 / 4 6` | `2` | Even-sized median interval and an interior prime |
| `1 / 1000000000` | `7` | Optimal target can exceed every input value |
| `2 / 2 4` | `2` | Small prime boundary and exact median handling |
| `100000 / 1000000000 ...` | `0` | Maximum array size and large values |

## Edge Cases

For the input

```
1
1
```

the lower and upper medians are both `1`. `previous_prime(1)` finds no valid prime, while `next_prime(1)` returns `2`. The cost is (|1-2|=1), so the answer is `1`. The implementation explicitly rejects values below `2`, preventing `1` from being mistaken for a prime.

For the input

```
2
8 10
```

the median interval is `[8,10]`. The previous prime from `10` is `7`, and the next prime from `8` is `11`. Their costs are (1+3=4) and (3+1=4), so the answer is `4`. A solution that checks only one median value and searches in one direction could miss this tie.

For the input

```
1
1000000000
```

the lower and upper medians are `1000000000`. The previous prime is `999999937`, while the next prime is `1000000007`. Their distances are `63` and `7`, respectively, so the algorithm chooses `1000000007` and returns `7`. This case also confirms that the prime search is not artificially bounded by the largest input value.

For the input

```
4
7 7 7 7
```

both median values are `7`, and `7` is prime. Both prime searches immediately return `7`. Every absolute difference is zero, so the answer is `0`. This confirms that the algorithm does not perform unnecessary changes when the array is already valid.

For the input

```
3
2 3 10
```

the median is `3`, which is itself prime. The candidate target `3` has cost

[
|2-3|+|3-3|+|10-3|=1+0+7=8.
]

The algorithm evaluates this candidate and returns `8`, matching the sample.

For the input

```
2
2 4
```

the median interval is `[2,4]`. The previous prime at or below `4` is `3`, and the next prime at or above `2` is `2`. Target `2` costs `2`, while target `3` also costs `2`. The minimum is therefore `2`, which catches implementations that accidentally search strictly above or strictly below the median instead of allowing the median itself when it is prime.
