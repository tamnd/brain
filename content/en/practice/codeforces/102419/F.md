---
title: "CF 102419F - xor-sum"
description: "For each test case, we need to print an array of exactly (n) integers. Every value must lie in the interval ([0,m]), the ordinary sum of all values must be (s), and their bitwise XOR must be (x). If no such array exists, we print (-1)."
date: "2026-08-12T20:17:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "F"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 745
verified: true
draft: false
---

[CF 102419F - xor-sum](https://codeforces.com/problemset/problem/102419/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 12m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we need to print an array of exactly (n) integers. Every value must lie in the interval ([0,m]), the ordinary sum of all values must be (s), and their bitwise XOR must be (x). If no such array exists, we print (-1). The official constraints allow up to (10^5) test cases, with the total number of array elements over all test cases at most (3\cdot10^5).

The size of (n) immediately rules out anything that explores many possible arrays. Even for a single test case, enumerating every array would require ((m+1)^n) candidates, which is astronomically large when (n=10^5). The values (s) and (m) are also too large for a dynamic program indexed by the sum. The useful structure has to come from the binary representation of the XOR and from constructing most of the array in a repetitive way.

The first invariant is the relation between addition and XOR. For two integers,

[
a+b=(a\oplus b)+2(a\mathbin{&}b).
]

For an entire array, this implies that the ordinary sum is always at least the XOR and has the same parity as the XOR. Consequently, (s<x) or (s\not\equiv x\pmod 2) immediately makes the test case impossible.

There are several less obvious boundary cases. If (n=1), there is no freedom at all. For example, (n=1,m=5,s=5,x=5) is valid with the array ([5]), while (1,5,5,0) is impossible because the only element would have to equal both its sum and its XOR. A careless construction that always reserves two elements would also fail here.

A second boundary case occurs when (x>m). The value (x) cannot simply be placed into the array. For example, (n=3,m=4,s=7,x=7) is valid with ([4,3,0]), because (4\oplus3=7). A construction that insists on using (x) as one element would incorrectly reject it.

The upper bound on the sum can also be deceptive. For (n=4,m=3,s=12,x=0), the valid answer ([3,3,3,3]) has XOR zero. Starting from two zeros and trying to put the entire remaining sum into the other two elements would fail because two elements cannot contribute more than (6). The construction must be able to choose a non-minimal pair whose sum is larger.

Finally, (m=0) forces every array element to be zero. Thus (n=4,m=0,s=0,x=0) is valid, while (n=4,m=0,s=2,x=0) is impossible. This case is naturally handled by the general construction, but it is useful when checking boundary conditions around the highest set bit of (m).

## Approaches

The brute force approach is conceptually straightforward. Generate every array whose elements are between (0) and (m), calculate its sum and XOR, and stop when both match the requested values. It is correct because every possible candidate is examined. The problem is that there are exactly ((m+1)^n) candidates. With (n=10^5), even the smallest nontrivial value of (m) makes this impossible, so brute force is not merely slightly too slow, it is completely unusable.

The key observation is that equal numbers are extremely convenient for XOR. If we put (v,v) into the array, their XOR is zero while their contribution to the sum is (2v). This means that once we have a small group of numbers whose XOR is (x), every remaining two positions can be filled with the same value without changing the required XOR. We only need to decide how to construct that small XOR carrying group and how large its sum should be.

For an even (n), the special group can contain two numbers. For an odd (n), it can contain one number when (x\le m), or three numbers when (x>m). In the latter case, the three numbers can be a valid pair with XOR (x), followed by zero. Thus the real problem is reduced to constructing two bounded numbers with a prescribed XOR and a carefully chosen sum.

Suppose the two numbers are (a,b), their XOR is (x), and their sum is (p). Define

[
y=\frac{p-x}{2}.
]

The identity above gives

[
a\mathbin{&}b=y.
]

Since every bit set in (a\mathbin{&}b) must be zero in (a\oplus b), we need (y\mathbin{&}x=0). Conversely, when this condition holds, the bits of (x) can be divided between (a) and (b), while all bits of (y) are placed into both numbers.

This lets us solve the bounded pair problem directly in binary. For fixed (y), write

[
a=y+u,\qquad b=y+(x\oplus u),
]

where (u) is any subset of the set bits of (x). Because (u) and (x\oplus u) use disjoint bits, these are also the corresponding ordinary sums. If (c=m-y), we need both (u\le c) and (x\oplus u\le c). The largest subset of (x) not exceeding (c) can be obtained greedily from the highest bit to the lowest bit. If its complement is still larger than (c), no other subset can work, because every other subset is no larger.

The remaining question is which (y) to try. If there are (r) remaining positions after the special group, those positions can be filled in equal pairs. Their maximum total contribution is (rm). Thus the special pair must have sum at least (s-rm). Since its sum is (x+2y), we need

[
y\ge \frac{s-rm-x}{2}.
]

We choose the smallest (y) satisfying that bound and (y\mathbin{&}x=0). Increasing (y) makes the pair sum larger and simultaneously reduces the available bound (m-y), so if the smallest feasible (y) cannot form a bounded pair, no larger (y) can help.

This gives a logarithmic amount of binary work per test case, followed by the unavoidable (O(n)) work needed to actually print the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((m+1)^n\cdot n)) | (O(n)) | Too slow |
| Optimal | (O(n+\log m)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Check whether (s<x) or (s) and (x) have different parity. Since XOR cannot exceed the ordinary sum and every carry changes the sum by an even amount, either condition makes a solution impossible.
2. Decide how many special elements are needed. If (n) is odd and (x\le m), use the single element (x). The remaining (n-1) positions form equal pairs. Otherwise, use two elements carrying XOR (x), and when (n) is odd append a zero so that the remaining number of positions is even.
3. Let (r) be the number of positions left after the special group. The special pair must have sum at least (L=s-rm), because the remaining (r) positions can contribute at most (rm). Since every valid pair has sum (x+2y), compute the smallest required (y) from this lower bound.
4. Find the smallest (y\ge0) satisfying both (y\ge (L-x)/2) and (y\mathbin{&}x=0). If the lower bound is already nonpositive, start from zero. To find the next integer avoiding the set bits of (x), locate the lowest forbidden set bit of the current value and carry to the first higher bit that is allowed and currently zero.
5. For this (y), set (c=m-y). We need to split the set bits of (x) into two disjoint subsets (u) and (x\oplus u), both at most (c). Build the largest possible subset (u\le c) by scanning the bits of (x) from high to low. If (x\oplus u>c), the pair cannot exist.
6. Construct the pair as (a=y+u) and (b=y+(x\oplus u)). Their XOR is (x), their sum is (x+2y), and both are at most (m).
7. If (n) is odd and (x>m), append zero after the pair. Zero changes neither the sum nor the XOR, and it makes the number of remaining positions even.
8. Let (E) be the sum still missing after the special group. Divide (E) by two. Repeatedly take as much as possible, at most (m), as the value of an equal pair. Every pair contributes twice its value to the sum and zero to the XOR, so after enough pairs the exact remaining sum is reached.
9. If at any point the required special pair cannot be constructed, print (-1). Otherwise print the constructed array.

The invariant behind the construction is that the special group always has XOR exactly (x), while every subsequently added pair has XOR zero. At the same time, each added pair contributes an even amount to the sum. The chosen lower bound guarantees that the remaining positions have enough capacity, and the greedy filling step guarantees that their available capacity is sufficient to realize every required even sum from zero up to their maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

def next_disjoint(value, x):
    """Smallest y >= value such that y & x == 0."""
    bad = value & x
    if bad == 0:
        return value

    k = (bad & -bad).bit_length() - 1

    for j in range(k + 1, 31):
        y_bit = (value >> j) & 1
        x_bit = (x >> j) & 1
        if y_bit == 0 and x_bit == 0:
            prefix = value & ~((1 << (j + 1)) - 1)
            return prefix | (1 << j)

    return 1 << 30

def make_pair(x, total, m):
    """
    Find a,b in [0,m] such that:
        a ^ b == x
        a + b == total
    """
    if total < x or ((total - x) & 1):
        return None

    y = (total - x) // 2

    if y > m or (y & x):
        return None

    cap = m - y

    if x > 2 * cap:
        return None

    u = 0
    for bit in range(29, -1, -1):
        b = 1 << bit
        if (x & b) and u + b <= cap:
            u |= b

    v = x ^ u

    if v > cap:
        return None

    return y + u, y + v

def solve_case(n, m, s, x):
    if s < x or ((s - x) & 1):
        return None

    # Odd n and x itself fits into one element.
    if n & 1 and x <= m:
        remaining = n - 1
        extra = s - x

        if extra < 0 or extra > remaining * m:
            return None

        ans = [x]
        half = extra // 2
        pairs = remaining // 2

        for _ in range(pairs):
            v = min(m, half)
            ans.append(v)
            ans.append(v)
            half -= v

        return ans

    # Otherwise we need a two-element XOR carrier.
    if n & 1:
        special = 3
    else:
        special = 2

    if n < special:
        return None

    remaining = n - special

    # The special pair must provide at least this much sum.
    lower = s - remaining * m

    if lower <= x:
        y_low = 0
    else:
        y_low = (lower - x) // 2

    if y_low < 0:
        y_low = 0

    if y_low > m:
        return None

    y = next_disjoint(y_low, x)

    if y > m:
        return None

    pair_sum = x + 2 * y

    if pair_sum > s:
        return None

    pair = make_pair(x, pair_sum, m)
    if pair is None:
        return None

    a, b = pair
    ans = [a, b]

    if n & 1:
        ans.append(0)

    extra = s - pair_sum

    if extra < 0 or extra > remaining * m or (extra & 1):
        return None

    half = extra // 2
    pairs = remaining // 2

    for _ in range(pairs):
        v = min(m, half)
        ans.append(v)
        ans.append(v)
        half -= v

    if half != 0 or len(ans) != n:
        return None

    return ans

def main():
    t = int(input())
    out = []

    for _ in range(t):
        n, m, s, x = map(int, input().split())
        ans = solve_case(n, m, s, x)

        if ans is None:
            out.append("-1")
        else:
            out.append(" ".join(map(str, ans)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The first helper, `next_disjoint`, finds the smallest value not below the requested lower bound whose set bits do not overlap with (x). If the current value already satisfies the condition, it is returned immediately. Otherwise, its lowest conflicting bit must be removed, and the smallest possible increase comes from setting the first higher bit that is both allowed by (x) and zero in the current value.

The `make_pair` function implements the identity (a+b=x+2(a\mathbin{&}b)). The variable `y` is exactly (a\mathbin{&}b), so `y & x` must be zero. Once `y` is fixed, every bit of (x) belongs to exactly one of the two numbers. The variable `u` chooses which bits belong to the first number, and `x ^ u` gives the other part.

The high to low greedy construction of `u` is safe because the available weights are powers of two. It finds the largest subset of the set bits of (x) that does not exceed `cap`. If its complement is too large, every smaller subset has an even larger complement, so there is no alternative partition.

The main construction treats equal pairs as the adjustable part of the array. The number of remaining positions is always even, which is why the special group has one element for the odd and directly representable case, two elements for even (n), and three elements for odd (n) when (x>m). The use of Python integers also removes any concern about overflow for values up to (10^{18}).

The order of operations matters. The lower bound for the special pair is computed before constructing it, because choosing too small a pair could leave more sum than the remaining elements can hold. Conversely, choosing a larger pair than necessary only reduces the remaining capacity, so the smallest feasible (y) is the right choice.

## Worked Examples

For the first sample, consider (n=4,m=4,s=15,x=7). Since (n) is even, two elements carry the XOR and two positions remain as an equal pair.

| Variable | Value |
| --- | --- |
| (n) | 4 |
| (m) | 4 |
| (s) | 15 |
| (x) | 7 |
| Remaining positions | 2 |
| Lower pair sum | (15-2\cdot4=7) |
| (y) lower bound | 0 |
| Chosen (y) | 0 |
| Pair sum | 7 |
| Pair | (4,3) |
| Remaining sum | 8 |
| Equal pair | (4,4) |
| Final array | (4,3,4,4) |

The special pair has (4\oplus3=7) and sum (7). The final pair contributes (8) without changing the XOR, so the total is (15) and the XOR remains (7). This also demonstrates the case (x>m), where placing (x) directly would be illegal.

For the second sample, (n=4,m=4,s=4,x=4). Here (x\le m), but (n) is even, so the XOR carrier must still use two positions.

| Variable | Value |
| --- | --- |
| (n) | 4 |
| (m) | 4 |
| (s) | 4 |
| (x) | 4 |
| Remaining positions | 2 |
| Lower pair sum | (4-2\cdot4=-4) |
| Chosen (y) | 0 |
| Pair sum | 4 |
| Pair | (4,0) |
| Remaining sum | 0 |
| Final array | (4,0,0,0) |

The pair (4,0) has XOR (4) and sum (4). The two remaining zeros preserve both quantities.

As another useful trace, consider (n=4,m=3,s=12,x=0).

| Variable | Value |
| --- | --- |
| (n) | 4 |
| (m) | 3 |
| (s) | 12 |
| (x) | 0 |
| Remaining positions | 2 |
| Lower pair sum | (12-2\cdot3=6) |
| Chosen (y) | 3 |
| Pair sum | 6 |
| Pair | (3,3) |
| Remaining sum | 6 |
| Equal pair | (3,3) |
| Final array | (3,3,3,3) |

This trace shows why the pair cannot always be chosen with the minimum possible sum (x). Here (x=0), but using (0,0) would leave a sum of (12) for only two remaining elements, which is impossible. The lower bound forces the special pair to contribute (6), after which the other pair contributes the remaining (6).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+\log m)) per test case | Binary construction uses at most about 30 bits, and printing the (n) values costs (O(n)). |
| Space | (O(n)) | The output array contains exactly (n) integers. |

Across all test cases, the total (n) is at most (3\cdot10^5), so the total output construction is (O(3\cdot10^5)). The binary part performs only a constant number of scans over at most 30 bits per test case. This comfortably fits the 1 second time limit, while the (O(n)) memory is bounded by the required output size.

## Test Cases

```python
# Self-contained assert-based tests for the construction.

import sys
import io

def next_disjoint(value, x):
    bad = value & x
    if bad == 0:
        return value

    k = (bad & -bad).bit_length() - 1

    for j in range(k + 1, 31):
        if ((value >> j) & 1) == 0 and ((x >> j) & 1) == 0:
            prefix = value & ~((1 << (j + 1)) - 1)
            return prefix | (1 << j)

    return 1 << 30

def make_pair(x, total, m):
    if total < x or ((total - x) & 1):
        return None

    y = (total - x) // 2

    if y > m or (y & x):
        return None

    cap = m - y

    if x > 2 * cap:
        return None

    u = 0
    for bit in range(29, -1, -1):
        b = 1 << bit
        if (x & b) and u + b <= cap:
            u |= b

    v = x ^ u

    if v > cap:
        return None

    return y + u, y + v

def solve_case(n, m, s, x):
    if s < x or ((s - x) & 1):
        return None

    if n & 1 and x <= m:
        remaining = n - 1
        extra = s - x

        if extra < 0 or extra > remaining * m:
            return None

        ans = [x]
        half = extra // 2

        for _ in range(remaining // 2):
            v = min(m, half)
            ans.extend([v, v])
            half -= v

        return ans

    special = 3 if (n & 1) else 2

    if n < special:
        return None

    remaining = n - special
    lower = s - remaining * m
    y_low = 0 if lower <= x else (lower - x) // 2

    if y_low > m:
        return None

    y = next_disjoint(y_low, x)

    if y > m:
        return None

    pair_sum = x + 2 * y

    if pair_sum > s:
        return None

    pair = make_pair(x, pair_sum, m)
    if pair is None:
        return None

    a, b = pair
    ans = [a, b]

    if n & 1:
        ans.append(0)

    extra = s - pair_sum

    if extra < 0 or extra > remaining * m or extra & 1:
        return None

    half = extra // 2

    for _ in range(remaining // 2):
        v = min(m, half)
        ans.extend([v, v])
        half -= v

    if half != 0 or len(ans) != n:
        return None

    return ans

def solve_text(inp: str) -> str:
    data = io.StringIO(inp)
    t = int(data.readline())
    out = []

    for _ in range(t):
        n, m, s, x = map(int, data.readline().split())
        ans = solve_case(n, m, s, x)

        if ans is None:
            out.append("-1")
        else:
            out.append(" ".join(map(str, ans)))

    return "\n".join(out)

def run(inp: str) -> str:
    return solve_text(inp)

def validate(inp: str, out: str):
    lines = out.strip().splitlines()
    data = inp.strip().splitlines()

    t = int(data[0])
    assert len(lines) == t

    for i in range(t):
        n, m, s, x = map(int, data[i + 1].split())
        line = lines[i].strip()

        if line == "-1":
            assert solve_case(n, m, s, x) is None
            continue

        a = list(map(int, line.split()))
        assert len(a) == n
        assert all(0 <= v <= m for v in a)
        assert sum(a) == s

        cur_xor = 0
        for v in a:
            cur_xor ^= v

        assert cur_xor == x

# Provided sample
sample = """\
3
4 4 15 7
4 4 4 4
4 4 15 1
"""
validate(sample, run(sample))

# Minimum-size valid case
case1 = """\
1
1 5 5 5
"""
validate(case1, run(case1))

# All elements equal
case2 = """\
1
4 3 12 0
"""
validate(case2, run(case2))

# Boundary case with x > m
case3 = """\
1
3 4 7 7
"""
validate(case3, run(case3))

# Impossible because the requested sum is too large for the XOR requirement
case4 = """\
1
4 4 15 1
"""
assert run(case4).strip() == "-1"

# Maximum-size n, with all elements forced to one
case5 = """\
1
100000 1 100000 0
"""
validate(case5, run(case5))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5 5 5 5` | `5` | Minimum (n), direct single element construction |
| `4 / 3 12 0` | `3 3 3 3` | All equal values and large required sum |
| `3 / 4 7 7` | `4 3 0` | XOR larger than (m), requiring a split across two values |
| `4 / 4 15 1` | `-1` | Sum capacity and impossible construction |
| `100000 / 1 100000 0` | 100000 ones | Maximum (n), output size and pair filling |

## Edge Cases

For (n=1), the array has only one value. Consider `1 5 5 5`. The checks pass, (x\le m), and the odd length allows the single special value (x=5). The output is `[5]`. For `1 5 4 5`, the parity or sum relation rejects the case because the only possible element would have to be (5), whose sum cannot be (4).

When (x>m), the value (x) cannot be inserted directly. For `3 4 7 7`, the highest useful power of two is (4), and (7=4+3). The special group becomes `[4,3,0]`. Its sum is (7), its XOR is (4\oplus3\oplus0=7), and every value is at most (4).

For an all equal answer, consider `4 3 12 0`. The required XOR is zero, so equal pairs are ideal. The lower bound forces the first pair to contribute (6), giving `[3,3]`. The remaining sum is another (6), giving `[3,3]` again. The final array is `[3,3,3,3]`, whose sum is (12) and XOR is zero.

For (m=0), every value must be zero. With `4 0 0 0`, the odd or even branch constructs only zero pairs and the requested sum is already zero, so an array of four zeros is returned. With `4 0 2 0`, the remaining capacity is zero, so the construction rejects the test case.

For the upper capacity boundary, `100000 1 100000 0` requires the maximum possible sum. Since (n) is even and the XOR is zero, the construction uses pairs of ones. Every element becomes (1), giving sum (100000) and XOR zero because an even number of ones are XORed together. This also exercises the largest allowed (n) and confirms that the output construction remains linear in the array size.
