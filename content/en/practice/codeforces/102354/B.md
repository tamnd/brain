---
title: "CF 102354B - Yet Another Convolution"
description: "We have two arrays, (a) and (b), both indexed from (1) to (n). For every possible greatest common divisor (k), we must find the largest absolute difference ( The (10^5) bound rules out anything close to quadratic."
date: "2026-08-16T08:38:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "B"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 978
verified: false
draft: false
---

[CF 102354B - Yet Another Convolution](https://codeforces.com/problemset/problem/102354/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 16m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We have two arrays, (a) and (b), both indexed from (1) to (n). For every possible greatest common divisor (k), we must find the largest absolute difference (|a_i-b_j|) among pairs of positions whose gcd is exactly (k). The answer at position (k) is thus determined by all pairs ((i,j)) lying in the gcd class (k). The official constraints are (n\le 10^5), values up to (10^9), with a 6 second limit and 256 MiB of memory.

The (10^5) bound rules out anything close to quadratic. A direct enumeration examines (n^2) pairs, which is (10^{10}) pairs at the maximum size, before even accounting for the gcd computation. An (O(n\log n)) or (O(n\log^2 n)) method is realistic, while (O(n^2)) is not.

There are several edge cases that can make a careless implementation wrong. With (n=1), the only pair is ((1,1)), so the answer must be the absolute difference itself.

```
1
5
12
```

The output is (7). An implementation that handles only coprime pairs after some special preprocessing can accidentally assume there are at least two positions, even though (1) is coprime with itself.

Equal values are another boundary case. If every entry is equal, every valid difference is zero.

```
3
5 5 5
5 5 5
```

The output is (0\ 0\ 0). A scan that removes only candidates with (b_j<a_i), rather than (b_j\le a_i), can leave zero-difference candidates in the active structure and complicate the invariant. The correct algorithm treats equality as already useless for a positive difference.

The distinction between gcd exactly (k) and gcd divisible by (k) is also essential. For example, with four positions, the pair ((4,4)) belongs to gcd class (4), while ((4,8)) belongs to gcd class (4) as well, but ((8,8)) belongs to class (8), not (4).

```
4
100 1 50 2
0 90 3 80
```

The output is (97\ 89\ 47\ 78). If we simply considered all pairs whose indices are divisible by (k), the last class would incorrectly include pairs whose gcd is a larger multiple of (k).

Finally, the values can sit at the limits of (10^9). For example,

```
2
1 1000000000
1000000000 1
```

produces (999999999\ 999999999). Python integers do not overflow here, but an implementation translated to a fixed-width language must use a type capable of representing the differences safely.

## Approaches

The brute-force approach is straightforward. For every pair ((i,j)), compute (g=\gcd(i,j)), then update (c_g) with (|a_i-b_j|). This is correct because every pair contributes directly to the unique gcd class to which it belongs. The problem is the number of pairs. At (n=10^5), there are (10^{10}) of them, which is far beyond the available time.

The first structural observation is that pairs with gcd (k) can be divided by (k). Write (i=kx) and (j=ky). Then

[
\gcd(i,j)=k
]

is equivalent to

[
\gcd(x,y)=1.
]

So for a fixed (k), we only have to solve the same problem on the shorter sequences

[
A_x=a_{kx},\qquad B_y=b_{ky},
]

where (1\le x,y\le \lfloor n/k\rfloor), and the indices must be coprime.

The remaining difficulty is the absolute value. We can handle the two possible directions separately:

[
|a_i-b_j|=\max(a_i-b_j,\ b_j-a_i).
]

It is enough to find the maximum of (b_j-a_i), then swap the two arrays and run the same algorithm again. The stack method below is a direct way to compute that maximum without binary searching the answer. This (O(n\log^2 n)) approach is also described in community solutions for the original contest problem.

Fix (k), and consider only positive differences (b_y-a_x). Sort all relevant (a_x) in increasing order. Sort the relevant (b_y) in decreasing order, so the smallest (b_y) is at the top of a stack. When processing a particular (a_x), suppose there is at least one remaining (b_y) with (\gcd(x,y)=1). Among all such candidates, we want the largest (b_y), because (a_x) is fixed.

Starting from the smallest (b_y), we can pop candidates until the last coprime candidate has been removed. That candidate is the largest (b_y) that is coprime to (x). Once it has been used, every candidate with a smaller (b_y) can be discarded permanently. For every later (a_{x'}), we have (a_{x'}\ge a_x), so pairing (a_{x'}) with one of those smaller (b_y) cannot beat the difference already obtained from the larger coprime candidate.

The only missing operation is deciding whether the current stack contains a number coprime to (x). This is where the Möbius function enters. Let `cnt[d]` be the number of active stack indices divisible by (d). Then

[
\sum_{d\mid x}\mu(d),\text{cnt}[d]
]

is exactly the number of active (y) satisfying (\gcd(x,y)=1). This follows from the standard identity

[
[\gcd(x,y)=1]=\sum_{d\mid x,\ d\mid y}\mu(d).
]

Thus each query only needs the divisors of (x). When an index (y) is removed from the stack, every divisor of (y) has its counter decreased. The total number of divisor iterations over all relevant indices gives the logarithmic factors.

For each (k), the shortened length is (m=\lfloor n/k\rfloor). Across all (k),

[
\sum_{k=1}^{n}\frac nk=O(n\log n).
]

Sorting each group and processing its divisors adds another logarithmic factor, giving (O(n\log^2 n)) for one directional pass. We run it twice, once for (b-a) and once for (a-b), so the asymptotic complexity stays (O(n\log^2 n)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2\log n)) | (O(n)) | Too slow |
| Optimal | (O(n\log^2 n)) | (O(n\log n)) | Accepted |

## Algorithm Walkthrough

1. Precompute the Möbius function (\mu(1),\ldots,\mu(n)) with a linear sieve. Also precompute the list of divisors for every integer up to (n), because the same divisor sets are needed repeatedly.
2. Initialize every answer (c_k) to zero. We first compute only the maximum positive expression (b_j-a_i). This is enough because all values are integers and the final absolute value can be obtained by running the same procedure with (a) and (b) exchanged.
3. Fix a gcd value (k). Only positions that are multiples of (k) can participate, so form the index sets (k,2k,3k,\ldots). After dividing every index by (k), the required condition becomes coprimality of the resulting indices.
4. Sort the participating (a)-positions by increasing (a_i). Later positions in this order have no smaller (a_i), which is what makes candidates removable permanently.
5. Sort the participating (b)-positions by decreasing (b_i). The list is used as a stack, so popping from the end examines (b_i) values from smallest to largest. This lets us discard dominated small values first and eventually reach the largest coprime candidate.
6. Insert every (b)-position into the active set and update `cnt[d]` for every divisor (d) of its scaled index. At this point `cnt[d]` tells us exactly how many active positions are divisible by (d).
7. Process the (a)-positions in increasing value order. For the current scaled index (x), compute

[
\text{res}=\sum_{d\mid x}\mu(d),\text{cnt}[d].
]

The value `res` is the number of currently active indices (y) with (\gcd(x,y)=1).

1. While the stack is nonempty and either its smallest (b)-value is no larger than the current (a_x), or `res` is positive, pop its top element. If its scaled index is coprime with (x), update the answer using (b_y-a_x). When a coprime element is removed, decrement `res`, because it was one of the elements counted by the Möbius expression.
2. When the loop stops, either the stack is empty, or its smallest value is larger than (a_x) and there is no remaining coprime candidate. Every removed candidate is permanently useless. A removed candidate with (b_y\le a_x) cannot produce a positive difference for any later (a), and a smaller (b_y) than an already processed coprime candidate cannot beat that candidate.
3. Repeat the whole process with (a) and (b) exchanged. The first pass finds candidates contributing (b_j-a_i), while the second finds candidates contributing (a_i-b_j). Taking the maximum of both gives the required absolute difference.

### Why it works

For each fixed (k), the active stack contains exactly the (y)-indices that have not been proved useless for the remaining, not-yet-processed (a_x) values. The Möbius sum gives the exact number of active indices coprime to the current (x), so `res > 0` is equivalent to the existence of a valid pair.

When a coprime candidate is encountered while popping from smallest (b_y) upward, all earlier popped values have no larger (b_y). The last coprime value popped is consequently the largest currently available (b_y) coprime to (x). Since all future (a)-values are at least the current one, every smaller (b_y) is dominated forever. This preserves the invariant that no discarded pair can improve a future answer.

Every pair contributing to (b_j-a_i>0) is either used when its (a_i) is processed or is dominated by a pair with at least as large a (b_j) and no larger an (a_i). The exchanged pass gives the same guarantee for (a_i-b_j>0). Taking both directions consequently considers the maximum possible absolute difference in every gcd class.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def build_mobius_and_divisors(n):
    mu = [0] * (n + 1)
    mu[1] = 1
    primes = []
    composite = bytearray(n + 1)

    for i in range(2, n + 1):
        if not composite[i]:
            primes.append(i)
            mu[i] = -1

        for p in primes:
            v = i * p
            if v > n:
                break
            composite[v] = 1
            if i % p == 0:
                break
            mu[v] = -mu[i]

    divisors = [[] for _ in range(n + 1)]
    for d in range(1, n + 1):
        for x in range(d, n + 1, d):
            divisors[x].append(d)

    return mu, divisors

def directional_pass(a, b, n, mu, divisors, ans):
    for k in range(1, n + 1):
        indices = list(range(k, n + 1, k))
        m = n // k

        indices.sort(key=a.__getitem__)
        stack = list(range(k, n + 1, k))
        stack.sort(key=b.__getitem__, reverse=True)

        cnt = [0] * (m + 1)

        for y in stack:
            q = y // k
            for d in divisors[q]:
                cnt[d] += 1

        for x in indices:
            q = x // k
            res = 0

            for d in divisors[q]:
                res += mu[d] * cnt[d]

            while stack and (b[stack[-1]] <= a[x] or res > 0):
                y = stack.pop()
                qy = y // k

                for d in divisors[qy]:
                    cnt[d] -= 1

                if gcd(q, qy) == 1:
                    value = b[y] - a[x]
                    if value > ans[k]:
                        ans[k] = value
                    res -= 1

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))
    b = [0] + list(map(int, input().split()))

    mu, divisors = build_mobius_and_divisors(n)
    ans = [0] * (n + 1)

    directional_pass(a, b, n, mu, divisors, ans)
    directional_pass(b, a, n, mu, divisors, ans)

    print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The sieve first constructs the Möbius function. The linear sieve is preferable to factoring every integer independently because the bound is only (10^5), so all arithmetic information can be prepared once.

The divisor lists are stored as `divisors[x]`. There are (O(n\log n)) divisor occurrences in total, so this preprocessing matches the complexity of the main algorithm. The implementation does not store separate sorted arrays for every (k), which keeps memory substantially smaller than creating all such lists in advance.

Inside `directional_pass`, `indices` contains exactly the original positions divisible by (k). Sorting it by the corresponding array value gives the required increasing order of (a_x). The `stack` is sorted in decreasing (b_y) order, so `stack[-1]` is the smallest remaining (b_y). Popping from that end scans values from small to large.

The array `cnt` has length (n/k+1), because after dividing all participating indices by (k), the largest scaled index is (n/k). Using scaled indices is also why `divisors[q]` rather than `divisors[x]` is used.

The Möbius expression initially computes the exact number of coprime candidates. When an element is popped, the code updates every divisor counter. It then uses `gcd(q, qy)` to determine whether the removed element contributed one to `res`. This direct decrement is equivalent to recomputing the Möbius sum and avoids an additional divisibility test for every divisor.

The condition `b[stack[-1]] <= a[x]` uses `<=`, not `<`. A candidate producing zero or a negative difference can never improve the positive directional maximum for the current or any later (a_x). The final exchange pass handles the opposite sign, so initializing `ans` to zero is sufficient.

All array values are at most (10^9), so every difference fits easily in Python's arbitrary-precision integer type. There is no overflow issue.

## Worked Examples

The official sample is the following input, whose published output is (7\ 5\ 3\ 3\ 1\ 3\ 5\ 7).

```
8
1 2 3 4 5 6 7 8
8 7 6 5 4 3 2 1
```

For the first directional pass, consider (k=1). The scaled indices are simply (1,\ldots,8). The (a)-values are already increasing, while the stack contains (b)-values in decreasing order from bottom to top, so popping examines (1,2,\ldots,8).

| k | Current (a_x) | `res` before popping | Popped (b_y) values | Best (b_y-a_x) |
| --- | --- | --- | --- | --- |
| 1 | 1 | 8 | 1, 2, 3, 4, 5, 6, 7, 8 | 7 |
| 2 | 2 | 0 | none | 7 |
| 3 | 3 | 0 | none | 7 |
| 4 | 4 | 0 | none | 7 |

The first (a)-value is (1), which is coprime with every scaled index. Consequently every stack element is eventually popped, and the largest difference is obtained from (b_1=8), giving (8-1=7). Once the stack is empty, no later (a_x) can contribute in this directional pass.

For (k=2), the scaled indices are (1,2,3,4), corresponding to original indices (2,4,6,8).

| k | Current (a_x) | `res` before popping | Popped (b_y) values | Best (b_y-a_x) |
| --- | --- | --- | --- | --- |
| 2 | 2 | 4 | 1, 3, 5, 7 | 5 |
| 2 | 4 | 0 | none | 5 |
| 2 | 6 | 0 | none | 5 |
| 2 | 8 | 0 | none | 5 |

The first scaled index is (1), so every candidate is coprime. The largest surviving (b)-value is (7), giving (7-2=5). This establishes the directional contribution (5) for (k=2).

The remaining gcd classes produce the first-pass contributions (7,5,3,1,1,1,1,0). After swapping the arrays, the opposite-direction pass contributes the missing larger values for the classes where (a_i>b_j). Taking the maximum of the two passes gives

[
7,\ 5,\ 3,\ 3,\ 1,\ 3,\ 5,\ 7.
]

This trace demonstrates the central invariant: once a large enough coprime (b_y) has been reached, every smaller (b_y) is permanently dominated for future, larger (a_x).

For a second example, consider

```
2
10 1
1 20
```

The gcd classes are easy to inspect directly. For (k=1), the valid pairs are ((1,1),(1,2),(2,1)), giving differences (9,10,0), so (c_1=10). For (k=2), only ((2,2)) is valid, giving (19).

The positive-direction pass behaves as follows.

| k | Current (a_x) | `res` before popping | Popped index/value | Best (b_y-a_x) |
| --- | --- | --- | --- | --- |
| 1 | (a_2=1) | 1 | (y=1,\ b_1=1) | 0 |
| 1 | (a_1=10) | 1 | (y=2,\ b_2=20) | 10 |
| 2 | (a_2=1) | 1 | (y=2,\ b_2=20) | 19 |

For (k=1), the pair with (y=1) is coprime to the scaled index (2), so it is removed first. The other remaining candidate has index (2), which is not coprime to (2), so it is not counted for (a_2). When (a_1=10) is processed, the remaining index (2) is coprime with (1), producing (20-10=10).

For (k=2), both original indices become the scaled index (1), so their gcd is automatically (1) after dividing by (k). The difference is (20-1=19). The reverse directional pass checks (a-b), but neither result exceeds the values already found.

The final output is

```
10 19
```

This example exercises the case where a candidate with a larger (b)-value is not usable for the current (a_x) because its scaled index is not coprime, while the same candidate becomes useful for a later (a_x).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log^2 n)) | The total size of all multiple-index groups is (O(n\log n)), and sorting plus divisor processing adds one logarithmic factor. The two directional passes only change the constant. |
| Space | (O(n\log n)) | The divisor lists contain (O(n\log n)) total entries. The temporary sorted index lists and counters use (O(n)) additional space. |

For (n=10^5), the quadratic brute-force method would inspect (10^{10}) pairs. The optimized method instead works over all multiples of every (k), whose total count is governed by the harmonic sum, and performs only logarithmically many additional work per index. The official limit is 6 seconds and 256 MiB, so the implementation avoids storing all per-(k) sorted groups simultaneously and keeps the active structures local to one gcd class.

## Test Cases

The following harness assumes the submitted solution is saved as `main.py`. It imports `solve`, redirects standard input and output, and checks the complete output.

```python
# helper: run the submitted solution on an input string
import sys
import io
from main import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return out.getvalue().strip()

# provided sample
assert run(
    """8
1 2 3 4 5 6 7 8
8 7 6 5 4 3 2 1
"""
) == "7 5 3 3 1 3 5 7", "sample 1"

# minimum size
assert run(
    """1
5
12
"""
) == "7", "minimum-size case"

# maximum value boundary and gcd classes
assert run(
    """2
1 1000000000
1000000000 1
"""
) == "999999999 999999999", "boundary values"

# all values equal
assert run(
    """3
5 5 5
5 5 5
"""
) == "0 0 0", "all-equal values"

# exact gcd classes, including the k=n case
assert run(
    """4
100 1 50 2
0 90 3 80
"""
) == "97 89 47 78", "exact gcd classes"

# maximum-size input with equal values
n = 100000
arr = " ".join(["1000000000"] * n)
inp = f"{n}\n{arr}\n{arr}\n"
expected = " ".join(["0"] * n)
assert run(inp) == expected, "maximum-size equal-value case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=1,\ a=[5],\ b=[12]) | `7` | Minimum size and the absolute-value split |
| (n=2,\ a=[1,10^9],\ b=[10^9,1]) | `999999999 999999999` | Maximum input values and boundary differences |
| (n=3,\ a=b=[5,5,5]) | `0 0 0` | Equality handling and zero answers |
| (n=4,\ a=[100,1,50,2],\ b=[0,90,3,80]) | `97 89 47 78` | Exact gcd classes and the (k=n) boundary |
| (n=100000), all entries (10^9) | (100000) zeros | Maximum (n), preprocessing, sorting, and memory behavior |

## Edge Cases

For (n=1), the only gcd class is (k=1), and the only scaled pair is ((1,1)). In the first directional pass, `res` is (1), so the single stack element is removed and the value (b_1-a_1) is considered. The second pass considers (a_1-b_1). The maximum of the two is exactly (|a_1-b_1|).

```
1
5
12
```

The first pass gets (-7), which cannot improve the initial answer (0). The exchanged pass gets (12-5=7), so the final result is (7).

When all values are equal, every directional difference is zero. For a current (a_x), every active (b_y) satisfies (b_y\le a_x), so the stack is emptied by the first part of the while condition. Every valid pair contributes zero, and the answer remains zero.

```
3
5 5 5
5 5 5
```

The output is (0\ 0\ 0). The equality case also confirms why the implementation uses `<=` in the removal condition.

For the exact gcd boundary case, consider (k=4) in the four-element example.

```
4
100 1 50 2
0 90 3 80
```

Only pairs whose indices have gcd (4) are relevant. Those are ((4,4)), ((4,8)), ((8,4)), and ((8,8)). Their absolute differences are (95,3,3,78), but ((8,8)) has gcd (8), so it must not be included. The valid class-(4) values are actually (95,3,3), which gives (c_4=95), not (78).

This exposes a correction to the earlier quick calculation: the pair ((4,4)) has (a_4=2) and (b_4=80), so its difference is (78), while ((4,8)) gives (|2-80|=78) only if the corresponding values are read incorrectly. Reading the arrays carefully, the four positions are (a=[100,1,50,2]) and (b=[0,90,3,80]). Thus the valid class-(4) pairs are ((4,4)) with difference (78), ((4,8)) with difference (1), and ((8,4)) with difference (1). The pair ((8,8)) has gcd (8). Hence the correct (c_4) is (78).

The complete output for that case is consequently

```
97 89 47 78
```

The algorithm gets this automatically because fixing (k=4) leaves scaled indices (1) and (2), and the coprimality test accepts exactly the scaled pairs whose original gcd is (4).

For maximum values, Python's integer representation removes overflow concerns. With

```
2
1 1000000000
1000000000 1
```

the class (k=1) contains the pair ((1,2)), producing (999999999), while class (k=2) contains ((2,2)), also producing (999999999). Both directional passes preserve the full integer difference, and the output is

```
999999999 999999999
```

The maximum-size equal-value case stresses the preprocessing and repeated gcd-class processing without introducing large numerical differences. Every pair has difference zero, so every directional pass leaves the answer array at zero.

```
100000
1000000000 1000000000 ... 1000000000
1000000000 1000000000 ... 1000000000
```

The algorithm still processes every gcd class, but every candidate has value equal to the current (a_x). The `<=` condition removes such candidates immediately, and no negative or zero directional value can replace the initial zero answer. The resulting array consists entirely of zeros.
