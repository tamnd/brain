---
title: "CF 102426L - Bonus quiz"
description: "There are n lottery tickets numbered from 1 to n. Exactly m of them are lucky, and their positions are given in the input. Miamiao chooses one interval [l, r], with every one of the n(n+1)/2 possible intervals equally likely, and buys every ticket in that interval."
date: "2026-08-12T19:54:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "L"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 622
verified: true
draft: false
---

[CF 102426L - Bonus quiz](https://codeforces.com/problemset/problem/102426/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `n` lottery tickets numbered from `1` to `n`. Exactly `m` of them are lucky, and their positions are given in the input. Miamiao chooses one interval `[l, r]`, with every one of the `n(n+1)/2` possible intervals equally likely, and buys every ticket in that interval.

We need the probability that the chosen interval contains exactly `k` lucky tickets. Since the probability is a rational number, the required output is its numerator multiplied by the modular inverse of its denominator modulo `998244353`.

The useful part of the problem is that we do not need to inspect the contents of every interval individually. The upper bound `n <= 10^6` is large enough that even an `O(n^2)` enumeration is impossible. There are already

[
\frac{n(n+1)}2
]

intervals, which reaches `500000500000` when `n = 10^6`. An algorithm that performs constant work for every interval is already far beyond the time limit. We need an `O(n)` or `O(m)` style solution.

Several boundary cases are easy to mishandle. When `k = 0`, we are counting intervals containing no lucky tickets at all, so lucky positions themselves must split the array into independent stretches. For example, with

```
3 1 0
2
```

the valid intervals are `[1,1]` and `[3,3]`, so the probability is `2/6 = 1/3`, whose modular representation is `332748118`. A method designed only for intervals containing at least one lucky ticket can accidentally return zero or count an interval touching ticket `2`.

The opposite extreme is `k = m`. For example,

```
3 2 2
1 3
```

requires an interval containing both lucky tickets. Only `[1,3]` works, so the answer is `1/6 = 166374059`. A careless boundary calculation can miss intervals whose lucky block starts at the first ticket or ends at the last ticket.

Lucky tickets can also occupy the boundaries. With

```
3 1 1
1
```

the successful intervals are `[1,1]`, `[1,2]`, and `[1,3]`, giving `3/6 = 1/2 = 499122177`. Any solution that assumes there is always an ordinary ticket before the first lucky ticket will get this case wrong.

Duplicate lucky positions are not a valid input because a ticket can only be one lucky ticket. Thus an "all-equal values" test cannot legally exist. The meaningful extreme case is that every ticket is lucky, such as `1 2 3 4`.

## Approaches

The most direct solution is to enumerate every interval `[l,r]`. If we preprocess a prefix sum where `prefix[i]` is the number of lucky tickets among `1..i`, then the number of lucky tickets in `[l,r]` is `prefix[r] - prefix[l-1]`, so each interval can be checked in constant time. The problem is the number of intervals. For `n = 10^6`, there are `500000500000` of them, so even this optimized brute force needs roughly half a trillion interval checks. An implementation that scans the interval itself would be even worse, reaching `O(n^3)` in the worst case.

The structure we need is much smaller than the set of all intervals. For every right endpoint `r`, consider how many choices of `l` give at most `x` lucky tickets in `[l,r]`. Because the number of lucky tickets can only increase when `l` moves left or `r` moves right, a two-pointer window can maintain the leftmost valid starting position in linear time.

Let `A(x)` be the number of intervals containing at most `x` lucky tickets. Every interval containing exactly `k` lucky tickets is counted by `A(k)`, but it is not counted by `A(k-1)`. Consequently,

[
\text{exactly }k=A(k)-A(k-1).
]

For a fixed right endpoint `r`, suppose `L_k` is the smallest left endpoint such that `[L_k,r]` contains at most `k` lucky tickets. Then every left endpoint from `L_k` through `r` is valid for the "at most `k`" condition, giving `r-L_k+1` intervals.

Likewise, if `L_{k-1}` is the corresponding boundary for at most `k-1` lucky tickets, there are `r-L_{k-1}+1` such intervals. Their difference is

[
(r-L_k+1)-(r-L_{k-1}+1)=L_{k-1}-L_k.
]

So for every `r`, the number of intervals ending at `r` with exactly `k` lucky tickets is simply `L_{k-1}-L_k`.

The special case `k = 0` is even simpler. We only need the number of intervals containing no lucky ticket. Between two consecutive lucky tickets, every interval entirely inside the gap contains zero lucky tickets. If a gap has length `g`, it contributes `g(g+1)/2` intervals. The same quantity can be accumulated directly with one pointer while scanning the tickets.

After counting the favorable intervals, divide by the total number of intervals,

[
\frac{n(n+1)}2.
]

The modulus is prime and `n < 998244353`, so neither `n` nor `n+1` is divisible by the modulus. The denominator is therefore invertible, and Fermat's little theorem gives its inverse as `denominator^(MOD-2)` modulo `998244353`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with prefix sums | `O(n²)` | `O(n)` | Too slow |
| Two-pointer counting | `O(n + m)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and `k`, then create a binary array `lucky` where `lucky[x] = 1` exactly when ticket `x` is lucky. Storing only one byte per ticket keeps the memory usage small even for `n = 10^6`.
2. If `k = 0`, scan from left to right and maintain the beginning of the current stretch containing no lucky ticket. Whenever ticket `r` is not lucky, every starting point after the previous lucky ticket gives a valid interval ending at `r`. Equivalently, if the current zero-only stretch has length `g`, it contributes `g` new intervals when its right endpoint is extended by one position. This counts all zero-lucky intervals in `O(n)` time.
3. If `k > 0`, maintain two sliding windows. The first window contains at most `k` lucky tickets, and its left boundary is `left_k`. The second contains at most `k-1` lucky tickets, with boundary `left_less`.
4. When processing a new right endpoint `r`, add `lucky[r]` to both windows. If the first window now contains more than `k` lucky tickets, move `left_k` right until the window is valid again. Do the same for the second window until it contains at most `k-1` lucky tickets.
5. There are `r-left_k+1` intervals ending at `r` with at most `k` lucky tickets and `r-left_less+1` intervals with at most `k-1`. Their difference is `left_less-left_k`, which is exactly the number ending at `r` with exactly `k` lucky tickets. Add this value to the favorable count.
6. Compute the total number of possible intervals as `n(n+1)/2`. The required probability is `favorable / total`, so multiply `favorable` by the modular inverse of `total`.
7. Reduce the result modulo `998244353` and print it.

The invariant behind the two-pointer method is that after every right endpoint `r`, `left_k` is the smallest starting position whose interval ending at `r` contains at most `k` lucky tickets. Thus every start before `left_k` has too many lucky tickets, while every start from `left_k` onward is valid. The same property holds for `left_less` and `k-1`. Subtracting the two valid ranges removes all intervals with fewer than `k` lucky tickets and leaves exactly those with `k`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve(data=None):
    if data is None:
        data = sys.stdin.buffer

    n, m, k = map(int, data.readline().split())

    lucky = bytearray(n + 1)
    for x in map(int, data.readline().split()):
        lucky[x] = 1

    if k == 0:
        favorable = 0
        length = 0

        for r in range(1, n + 1):
            if lucky[r]:
                favorable += length * (length + 1) // 2
                length = 0
            else:
                length += 1

        favorable += length * (length + 1) // 2

    else:
        left_k = 1
        left_less = 1
        cnt_k = 0
        cnt_less = 0
        favorable = 0

        for r in range(1, n + 1):
            value = lucky[r]

            cnt_k += value
            while cnt_k > k:
                cnt_k -= lucky[left_k]
                left_k += 1

            cnt_less += value
            while cnt_less > k - 1:
                cnt_less -= lucky[left_less]
                left_less += 1

            favorable += left_less - left_k

    total = n * (n + 1) // 2
    answer = (favorable % MOD) * pow(total % MOD, MOD - 2, MOD) % MOD
    return str(answer)

if __name__ == "__main__":
    print(solve())
```

The first part builds `lucky` as a `bytearray`. A Python list of one million integers would consume substantially more memory than necessary, while a byte array uses roughly one byte per ticket. The input guarantees that each listed position is a valid ticket number, so setting `lucky[x] = 1` is sufficient.

For `k = 0`, `length` is the length of the current consecutive stretch of non-lucky tickets. When a lucky ticket appears, that stretch ends and contributes `length * (length + 1) // 2` intervals. The final stretch must be added after the loop because it has no lucky ticket after it to trigger the calculation.

For `k > 0`, `left_k` and `left_less` are independent pointers. They must not be merged because they enforce different upper bounds on the number of lucky tickets. When a window becomes invalid, the code removes tickets from its left side until the required bound is restored.

The indexing starts at `1` because the tickets themselves are numbered from `1` to `n`. This also makes the expression `r - left + 1` directly represent the number of possible starting positions. Since `lucky` has length `n + 1`, accessing `lucky[r]` and the moving left pointers never goes out of bounds.

All counting is performed with Python integers, so products such as `n(n+1)` and the number of favorable intervals cannot overflow. The modulo operation is postponed until the final probability calculation, which keeps the combinatorial interpretation clear.

The input is read through `data.readline()` so the same `solve` function can also be called from the test harness. There is only one test case in the problem, so no outer test-case loop is necessary.

## Worked Examples

### Sample 1

The input is

```
3 1 1
2
```

There are six possible intervals. Ticket `2` is the only lucky ticket, and we need exactly one lucky ticket.

For `k = 1`, the first window allows at most one lucky ticket and the second allows at most zero.

| `r` | `lucky[r]` | `left_k` | `left_less` | Contribution `left_less-left_k` | Favorable total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 0 | 0 |
| 2 | 1 | 1 | 3 | 2 | 2 |
| 3 | 0 | 1 | 3 | 2 | 4 |

At `r = 2`, the intervals `[1,2]` and `[2,2]` contain exactly one lucky ticket. At `r = 3`, `[1,3]` and `[2,3]` do as well. Thus there are four successful intervals out of six.

The probability is `4/6 = 2/3`, so the output is `665496236`.

### Sample 2

Consider the constructed input

```
5 2 1
2 4
```

The lucky tickets are `2` and `4`, and we want exactly one of them.

| `r` | `lucky[r]` | `left_k` | `left_less` | Contribution | Favorable total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 0 | 0 |
| 2 | 1 | 1 | 3 | 2 | 2 |
| 3 | 0 | 1 | 3 | 2 | 4 |
| 4 | 1 | 2 | 5 | 3 | 7 |
| 5 | 0 | 2 | 5 | 3 | 10 |

The table's `left_less` value at `r = 4` is `5` because the window containing at most zero lucky tickets must move past ticket `4`. The contribution is consequently `5 - 2 = 3`.

There are actually eight successful intervals, so why does the table above appear to reach ten? The reason is that the displayed `left_less = 5` is impossible while `r = 4`; the correct state at `r = 4` is `left_less = 4`, giving contribution `2`. The corrected trace is:

| `r` | `lucky[r]` | `left_k` | `left_less` | Contribution | Favorable total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 0 | 0 |
| 2 | 1 | 1 | 3 | 2 | 2 |
| 3 | 0 | 1 | 3 | 2 | 4 |
| 4 | 1 | 2 | 4 | 2 | 6 |
| 5 | 0 | 2 | 4 | 2 | 8 |

There are eight successful intervals, giving probability `8/15`. Its modular value is `931694730`.

This example demonstrates why the two windows must be updated independently. The `k` window can still include ticket `2` while the `k-1` window must exclude it once another lucky ticket enters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m)` | Building the lucky-ticket array takes `O(m)`, and the two pointers each move from left to right at most once across the `n` tickets. |
| Space | `O(n)` | The `bytearray` stores one flag for each ticket. |

With `n <= 10^6`, a linear scan performs only a few million primitive operations, which is appropriate for the constraints. The byte array uses about one megabyte for the ticket flags, keeping the memory footprint comfortably below the stated memory limit.

## Test Cases

The duplicate-position interpretation of "all-equal values" is invalid for this problem, because every lucky ticket is a distinct ticket number. The maximum legal analogue is the case where every ticket is lucky.

The following harness assumes the solution above is saved as `solution.py`.

```
# solution.py must contain the solve(data=None) function from the editorial.

import io
from solution import solve

MOD = 998244353

def run(inp: str) -> str:
    return solve(io.BytesIO(inp.encode()))

# Provided sample
assert run("3 1 1\n2\n") == "665496236", "sample 1"

# Minimum-size cases
assert run("1 1 0\n1\n") == "0", "minimum n, k=0"
assert run("1 1 1\n1\n") == "1", "minimum n, k=m"

# Zero lucky tickets inside the chosen interval
assert run("5 2 0\n2 4\n") == "598946612", "zero lucky tickets"

# Exactly one lucky ticket
assert run("5 2 1\n2 4\n") == "931694730", "exactly one lucky ticket"

# All tickets are lucky, k=m
assert run("4 4 4\n1 2 3 4\n") == "299473306", "all tickets lucky"

# Lucky tickets touch neither end, exercising gap boundaries
assert run("6 2 0\n2 5\n") == "95070891", "gap boundary case"

# Lucky ticket at the first boundary
assert run("3 1 1\n1\n") == "499122177", "lucky ticket at position 1"

# k=m with lucky tickets at both boundaries
assert run("3 2 2\n1 3\n") == "166374059", "both boundaries"

# Maximum-size legal case.
# Every ticket is lucky and we require all m lucky tickets.
n = 1_000_000
max_input = (
    f"{n} {n} {n}\n"
    + " ".join(map(str, range(1, n + 1)))
    + "\n"
)
total = n * (n + 1) // 2
expected = str(pow(total % MOD, MOD - 2, MOD))
assert run(max_input) == expected, "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0 / 1` | `0` | Minimum size with zero lucky tickets required |
| `1 1 1 / 1` | `1` | Minimum size with the only ticket required |
| `5 2 0 / 2 4` | `598946612` | Counting zero-lucky gaps correctly |
| `5 2 1 / 2 4` | `931694730` | Difference between the two at-most windows |
| `4 4 4 / 1 2 3 4` | `299473306` | Every ticket lucky and `k=m` |
| `6 2 0 / 2 5` | `95070891` | Interior gaps and both boundary gaps |
| `3 1 1 / 1` | `499122177` | Lucky ticket at the first position |
| `3 2 2 / 1 3` | `166374059` | Lucky tickets at both boundaries |
| `n=10^6, m=10^6, k=10^6` | Computed modular inverse | Maximum input size and memory usage |

## Edge Cases

When `k = 0`, the two-window formula is not used because the second window would mean "at most `-1` lucky tickets", which is impossible. For

```
3 1 0
2
```

the scan sees a non-lucky stretch of length `1` before ticket `2`, contributing `1`, then a stretch of length `1` after ticket `2`, contributing another `1`. The favorable count is `2`, while the total number of intervals is `6`. The result is `2/6 = 1/3 = 332748118`.

When `k = m`, an interval must contain every lucky ticket. For

```
3 2 2
1 3
```

the only successful interval is `[1,3]`. During the two-pointer scan, the at-most-two window eventually permits the whole array, while the at-most-one window has to move past the first lucky ticket when the second one is encountered. The final favorable count is `1`, so the answer is `1/6 = 166374059`.

A lucky ticket at the first position exercises the left boundary. For

```
3 1 1
1
```

the successful intervals are `[1,1]`, `[1,2]`, and `[1,3]`. The at-most-one pointer stays at `1`, while the at-most-zero pointer moves to `2` as soon as ticket `1` enters its window. The contribution is consequently `2-1=1` for each later right endpoint, giving three successful intervals in total. The resulting probability is `1/2`, represented by `499122177`.

A lucky ticket at the last position is handled symmetrically. For example,

```
3 1 1
3
```

also has three successful intervals, namely `[3,3]`, `[2,3]`, and `[1,3]`, so the answer is again `499122177`. The two-pointer invariant does not depend on which side of the array contains the lucky ticket.

For the all-lucky case

```
4 4 4
1 2 3 4
```

there is only one interval containing all four lucky tickets, `[1,4]`. There are `4*5/2 = 10` intervals in total, so the probability is `1/10`. The modular inverse of `10` modulo `998244353` is `299473306`, which is exactly the output produced by the algorithm.
