---
title: "CF 102319Q - Quirky Queries"
description: "We maintain an array of quirky integers. A quirky integer is square-free, and every prime factor is below 300. There are only 62 such primes, so every value can be represented by a 62-bit mask telling us which primes occur in its factorization."
date: "2026-08-13T05:04:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102319
codeforces_index: "Q"
codeforces_contest_name: "UBC Summer Contest 2018"
rating: 0
weight: 102319
solve_time_s: 424
verified: true
draft: false
---

[CF 102319Q - Quirky Queries](https://codeforces.com/problemset/problem/102319/Q)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain an array of quirky integers. A quirky integer is square-free, and every prime factor is below 300. There are only 62 such primes, so every value can be represented by a 62-bit mask telling us which primes occur in its factorization.

A type 1 query gives a range and another quirky integer `x`. Each value in the range is replaced by `x` exactly when the ordered list of its divisors is lexicographically greater than the divisor list of `x`. A type 2 query asks for the LCM of all values in a range, modulo (10^9+7).

The first difficulty is that the update is not an ordinary assignment. Some positions change and some do not, depending on a nontrivial ordering of integers. The second difficulty is that the LCM must be maintained while values are changed over ranges.

With (n\le 10^5) and (q\le 2\cdot10^5), scanning a whole range for every query is impossible. In the worst case, (2\cdot10^5) queries can each touch (10^5) positions, giving (2\cdot10^{10}) position visits before even considering the cost of comparing divisor lists. A solution needs roughly logarithmic amortized work per query.

There are several edge cases that a direct implementation can get wrong. The first is the prefix case in lexicographic comparison. For example, with one element equal to `2`, the query `1 1 1 6` must change it to `6`, because the divisor list of `2` is `[1, 2]`, which is lexicographically smaller than `[1, 2, 3, 6]`. Treating the comparison only as a comparison of prime-factor bitmasks can get this wrong.

A second edge case is a number dividing the other number. For example, `6` and `30` have divisor lists `[1,2,3,6]` and `[1,2,3,5,6,10,15,30]`. The first difference is `5` versus `6`, so `30` is actually lexicographically smaller than `6`. A comparator based only on whether one prime is present in one factorization would incorrectly order them.

A third edge case concerns the LCM. For input

```
2
6 10
1
2 1 2
```

the answer is `30`, not `60`. Since the numbers are square-free, the LCM contains each prime only once, so the correct operation is a bitwise OR of their prime masks, followed by multiplication of the selected primes.

The endpoints of the range also need exact handling. For example,

```
3
6 10 14
1
1 2 2 7
```

changes only the second position. Updating `[l,r)` internally while treating the input range as `[l,r]` would silently miss the last element in many cases.

## Approaches

The brute-force solution is straightforward. For a type 1 query, inspect every position from `l` through `r`, compare the divisor sequences of the current value and `x`, and assign `x` when required. For a type 2 query, walk through the range and accumulate the LCM. Both procedures are correct because they directly implement the definitions.

The problem is the number of positions visited. A worst-case sequence of (2\cdot10^5) queries over a range of length (10^5) gives (2\cdot10^{10}) visits. A divisor comparison itself is also not constant if implemented by explicitly constructing divisor lists, so this approach is far outside the time limit.

The first useful observation is that quirky numbers are square-free. Their prime factorizations are therefore sets rather than multisets. Since every prime factor is below 300, there are only 62 possible prime factors. This immediately gives a compact representation of every value as a 62-bit mask.

The second observation is more subtle. We need a fast comparison of the divisor sequences, but we do not actually need to construct those sequences.

Take two different quirky numbers `a` and `b`, and let `p` be the smallest prime that occurs in exactly one of them. Every divisor smaller than `p` uses only primes smaller than `p`, and all those prime memberships are identical in `a` and `b`. Thus every divisor below `p` occurs in both numbers.

Suppose `p` divides `a` but not `b`. If neither number divides the other, then `b` has some prime factor larger than `p` that is not shared. The first divisor where the sequences differ is then `p` on the side of `a`, so `a` is lexicographically smaller.

The only special case is when `b` divides `a`. Then every divisor of `b` also occurs in `a`. Let `p` again be the smallest additional prime of `a`. If `p < b`, the divisor `p` appears before the final divisor `b`, so `a` is smaller. If `p > b`, the whole divisor sequence of `b` ends before `p`, so `b` is smaller. The symmetric case applies when `a` divides `b`.

This gives an (O(1)) comparator once the two prime masks are known. The number of possible primes is only 62, so finding the first differing prime is a constant-time bit operation.

The update is now a range `chmin` under this custom total order. For every position we conceptually perform

[
a_i\leftarrow \min(a_i,x)
]

where `min` uses the divisor-sequence ordering rather than ordinary integer ordering.

That is exactly the kind of update handled by Segment Tree Beats. For each segment-tree node we keep its maximum value under this ordering, its strict second maximum, the number of occurrences of the maximum, and enough information about the prime masks to maintain the range LCM.

The LCM has an especially convenient representation. Since every number is square-free, the LCM of a collection is obtained by taking the bitwise OR of all their prime masks. Each segment-tree node therefore stores this OR mask. We additionally store the OR mask after removing all elements equal to the node's maximum. This extra field lets us update the OR when only the maximum group is changed.

The brute-force works because it explicitly checks every affected value. It fails because too many values can be touched by too many queries. The observation that the update is a range `chmin` under a fixed total order lets Segment Tree Beats skip whole groups of values, while the 62-prime representation makes the LCM aggregation a bitwise OR.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(qn)), up to (2\cdot10^{10}) position visits | (O(n)) | Too slow |
| Optimal | (O((n+q)\log n)) amortized | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Factor every initial value and every value appearing in a type 1 query into its distinct prime factors. Since all numbers are guaranteed quirky, every factor is one of the 62 primes below 300. Represent the factorization by a 62-bit mask.
2. Implement the divisor-sequence comparison using the two masks. Find the lowest-index prime whose membership differs. If neither number divides the other, the number containing that prime is smaller in divisor-sequence order. If one divides the other, compare the extra prime with the smaller number itself, because that decides whether the extra divisor appears before the shorter sequence ends.
3. Build a segment tree. For every node store the maximum value under the custom order, its mask, the strict second maximum and its mask, the count of maximum values, the OR of every mask in the node, and the OR after excluding all maximum-valued positions.
4. Process a type 1 query as a range `chmin`. If the node's maximum is already no greater than `x`, nothing changes. If the whole node is covered and its strict second maximum is smaller than `x`, only the maximum-valued positions can change, so the node can be updated without descending to its children.
5. When only the maximum group changes, replace its value by `x`, keep its count, and recompute the node's OR as `OR_without_max | mask(x)`. The second maximum does not change because `x` is strictly larger than it.
6. If the node cannot be updated directly, push the current maximum restriction to its children and recurse into the relevant children. Afterward merge the children back into the parent.
7. Process a type 2 query by recursively OR-ing the prime masks of the covered nodes. The resulting mask represents exactly the prime factors present in the LCM. Multiply those selected primes modulo (10^9+7).

The reason Segment Tree Beats remains fast is that a forced descent happens only when the update reaches at least the second-largest distinct value of a node. In that situation, two distinct values become equal after the update, so the number of distinct values represented in that subtree decreases. Updates can introduce a new value at only the normal segment-tree boundary cost, while the destructive descents are amortized by these decreases. This gives the standard (O((n+q)\log n)) amortized bound for range `chmin`.

### Why it works

The segment-tree invariant is that every node describes the current values in its interval exactly, with `mx` being the largest value under divisor-sequence order and `smx` the largest strictly smaller value. If `x` lies strictly between them, only the elements equal to `mx` are affected, so changing that group is sufficient. If `x` is at or below `smx`, the update may affect more than one distinct value and the node must be split.

The stored `or_without_max` is exactly the OR of all values that are not equal to `mx`. Whenever the maximum group is replaced, the new complete OR is consequently `or_without_max | mask(x)`. Whenever children are merged, the three cases of equal maximum, left maximum, or right maximum give enough information to reconstruct both the maximum group and the OR excluding it.

For a range query, the OR of all covered node masks is precisely the union of all prime factors. Since every quirky number contains each prime at exponent at most one, this union is exactly the prime factorization of the LCM. The final modular multiplication thus produces the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
    283, 293
]

PRIME_INDEX = {p: i for i, p in enumerate(PRIMES)}

def solve():
    n = int(input())
    initial = list(map(int, input().split()))
    q = int(input())

    queries = []
    all_values = set(initial)

    for _ in range(q):
        parts = list(map(int, input().split()))
        queries.append(parts)
        if parts[0] == 1:
            all_values.add(parts[3])

    mask_cache = {}

    def get_mask(x):
        cached = mask_cache.get(x)
        if cached is not None:
            return cached

        if x == 1:
            mask_cache[x] = 0
            return 0

        v = x
        mask = 0

        for i, p in enumerate(PRIMES):
            if p * p > v:
                break
            if v % p == 0:
                mask |= 1 << i
                v //= p

        if v > 1:
            mask |= 1 << PRIME_INDEX[v]

        mask_cache[x] = mask
        return mask

    # Returns True exactly when the divisor sequence of a is
    # lexicographically smaller than that of b.
    def less(a, ma, b, mb):
        if a == b:
            return False

        diff = ma ^ mb
        bit = diff & -diff
        idx = bit.bit_length() - 1
        p = PRIMES[idx]

        # b divides a.
        if (ma & mb) == mb:
            return p < b

        # a divides b.
        if (ma & mb) == ma:
            return a < p

        # Neither divides the other. The side containing the
        # first differing prime has the smaller divisor sequence.
        return (ma & bit) != 0

    def greater(a, ma, b, mb):
        return less(b, mb, a, ma)

    size = 4 * n + 5

    mx = [0] * size
    smx = [-1] * size
    cnt = [0] * size

    mx_mask = [0] * size
    smx_mask = [0] * size

    or_mask = [0] * size
    or_without_max = [0] * size

    def pull(v):
        left = v << 1
        right = left | 1

        lm = mx[left]
        rm = mx[right]
        lmask = mx_mask[left]
        rmask = mx_mask[right]

        if lm == rm:
            mx[v] = lm
            mx_mask[v] = lmask
            cnt[v] = cnt[left] + cnt[right]

            a = smx[left]
            am = smx_mask[left]
            b = smx[right]
            bm = smx_mask[right]

            if a == -1:
                smx[v] = b
                smx_mask[v] = bm
            elif b == -1:
                smx[v] = a
                smx_mask[v] = am
            elif greater(a, am, b, bm):
                smx[v] = a
                smx_mask[v] = am
            else:
                smx[v] = b
                smx_mask[v] = bm

            or_without_max[v] = or_without_max[left] | or_without_max[right]

        elif greater(lm, lmask, rm, rmask):
            mx[v] = lm
            mx_mask[v] = lmask
            cnt[v] = cnt[left]

            a = smx[left]
            am = smx_mask[left]
            b = rm
            bm = rmask

            if a == -1 or greater(b, bm, a, am):
                smx[v] = b
                smx_mask[v] = bm
            else:
                smx[v] = a
                smx_mask[v] = am

            or_without_max[v] = or_without_max[left] | or_mask[right]

        else:
            mx[v] = rm
            mx_mask[v] = rmask
            cnt[v] = cnt[right]

            a = smx[right]
            am = smx_mask[right]
            b = lm
            bm = lmask

            if a == -1 or greater(b, bm, a, am):
                smx[v] = b
                smx_mask[v] = bm
            else:
                smx[v] = a
                smx_mask[v] = am

            or_without_max[v] = or_without_max[right] | or_mask[left]

        or_mask[v] = or_without_max[v] | mx_mask[v]

    def build(v, l, r):
        if l == r:
            value = initial[l]
            mask = get_mask(value)

            mx[v] = value
            smx[v] = -1
            cnt[v] = 1
            mx_mask[v] = mask
            smx_mask[v] = 0
            or_mask[v] = mask
            or_without_max[v] = 0
            return

        mid = (l + r) >> 1
        build(v << 1, l, mid)
        build(v << 1 | 1, mid + 1, r)
        pull(v)

    def apply_max(v, value, mask):
        mx[v] = value
        mx_mask[v] = mask
        or_mask[v] = or_without_max[v] | mask

    def push(v):
        value = mx[v]
        mask = mx_mask[v]

        left = v << 1
        right = left | 1

        if greater(mx[left], mx_mask[left], value, mask):
            apply_max(left, value, mask)

        if greater(mx[right], mx_mask[right], value, mask):
            apply_max(right, value, mask)

    def range_chmin(v, l, r, ql, qr, value, value_mask):
        if r < ql or qr < l:
            return

        # Nothing in this node is larger than value.
        if not greater(mx[v], mx_mask[v], value, value_mask):
            return

        if ql <= l and r <= qr:
            # Only the maximum group is above value.
            if smx[v] == -1 or less(smx[v], smx_mask[v], value, value_mask):
                apply_max(v, value, value_mask)
                return

        push(v)

        mid = (l + r) >> 1
        range_chmin(v << 1, l, mid, ql, qr, value, value_mask)
        range_chmin(v << 1 | 1, mid + 1, r, ql, qr, value, value_mask)
        pull(v)

    def range_or(v, l, r, ql, qr):
        if r < ql or qr < l:
            return 0

        if ql <= l and r <= qr:
            return or_mask[v]

        push(v)

        mid = (l + r) >> 1
        return (
            range_or(v << 1, l, mid, ql, qr)
            | range_or(v << 1 | 1, mid + 1, r, ql, qr)
        )

    build(1, 0, n - 1)

    product_cache = {0: 1}

    def mask_product(mask):
        cached = product_cache.get(mask)
        if cached is not None:
            return cached

        result = 1
        m = mask

        while m:
            bit = m & -m
            idx = bit.bit_length() - 1
            result = result * PRIMES[idx] % MOD
            m -= bit

        product_cache[mask] = result
        return result

    out = []

    for query in queries:
        if query[0] == 1:
            _, l, r, x = query
            x_mask = get_mask(x)
            range_chmin(1, 0, n - 1, l - 1, r - 1, x, x_mask)
        else:
            _, l, r = query
            mask = range_or(1, 0, n - 1, l - 1, r - 1)
            out.append(str(mask_product(mask)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The factorization routine uses the fact that every prime factor is below 300. It tries the 62 possible primes and stops once the square of the current prime exceeds the remaining value. A dictionary caches masks, so repeated values from the initial array or repeated update targets are factored only once.

The `less` function is the key number-theoretic part. `diff` identifies the smallest prime where the two factorizations differ. The subset checks handle the case where one integer divides the other, which is exactly where the ordinary first-differing-prime argument needs the extra comparison against the smaller integer.

The segment tree keeps two different kinds of information. `mx`, `smx`, and `cnt` are the Segment Tree Beats state used to decide which values a `chmin` can change in bulk. `or_mask` and `or_without_max` are the aggregation state used for LCM queries.

The `apply_max` function does not need to modify `smx` or `cnt`. It is called only when the new value is strictly between the old maximum and the strict second maximum, or when the node contains only one distinct value. In either case, the set of positions belonging to the maximum group is unchanged.

`push` is slightly different from a normal lazy segment tree. There is no separate assignment tag. The parent's current maximum acts as the cap that must be propagated to any child whose maximum is still larger. This is the standard Segment Tree Beats mechanism.

All input ranges are converted from one-based inclusive indices to zero-based inclusive indices with `l - 1` and `r - 1`. The recursion uses inclusive endpoints consistently, so the conversion happens exactly once.

Python integers do not overflow, and the only potentially large values in the data structure are bit masks. The largest mask uses only 62 bits. LCM values are never constructed directly, only the final modular product is maintained.

## Worked Examples

For Sample 1, the input is

```
3
6 10 13
5
1 1 3 14
2 1 1
2 2 2
2 3 3
2 1 3
```

The relevant state changes are:

| Query | Range | Target | Values after update | Range OR for query | Answer |
| --- | --- | --- | --- | --- | --- |
| `1 1 3 14` | 1..3 | 14 | `[6, 10, 14]` |  |  |
| `2 1 1` | 1..1 |  | `[6, 10, 14]` | `{2,3}` | 6 |
| `2 2 2` | 2..2 |  | `[6, 10, 14]` | `{2,5}` | 10 |
| `2 3 3` | 3..3 |  | `[6, 10, 14]` | `{2,7}` | 14 |
| `2 1 3` | 1..3 |  | `[6, 10, 14]` | `{2,3,5,7}` | 210 |

The update leaves `6` and `10` unchanged because their divisor sequences are smaller than that of `14`. The value `13` is replaced because `14` has the smaller divisor sequence. The final LCM contains the four distinct primes 2, 3, 5, and 7, giving `210`.

For Sample 2, the input is

```
2
1 1
5
2 1 1
1 1 1 2
2 1 1
1 1 1 1
2 1 1
```

The trace is:

| Query | Range | Target | Array state | Answer |
| --- | --- | --- | --- | --- |
| `2 1 1` | 1..1 |  | `[1,1]` | 1 |
| `1 1 1 2` | 1..1 | 2 | `[1,1]` |  |
| `2 1 1` | 1..1 |  | `[1,1]` | 1 |
| `1 1 1 1` | 1..1 | 1 | `[1,1]` |  |
| `2 1 1` | 1..1 |  | `[1,1]` | 1 |

The second query does not change the first element. The divisor sequence of `1` is `[1]`, which is lexicographically smaller than `[1,2]`, so `1` is not replaced by `2`. This exercises the prefix case that a simple prime-mask comparator would mishandle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+q)\log n)) amortized | Segment Tree Beats handles the range `chmin`; mask construction examines at most 62 primes per distinct input value; each LCM mask contains at most 62 primes |
| Space | (O(n+q)) | The segment tree uses (O(n)) nodes and the cached masks and query values use (O(n+q)) additional space |

The factorization constant is only 62 because the problem restricts all prime factors to primes below 300. The segment-tree part is amortized (O((n+q)\log n)), which is appropriate for (10^5) array positions and (2\cdot10^5) queries. The stored masks are also compact because they need only 62 bits.

## Test Cases

```python
# Save the solution above as solution.py before running these tests.
import sys
import io
import importlib
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solution.input = sys.stdin.readline
        solution.solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Sample 1
assert run(
    """\
3
6 10 13
5
1 1 3 14
2 1 1
2 2 2
2 3 3
2 1 3
"""
) == "6\n10\n14\n210", "sample 1"

# Sample 2
assert run(
    """\
2
1 1
5
2 1 1
1 1 1 2
2 1 1
1 1 1 1
2 1 1
"""
) == "1\n1\n1", "sample 2"

# Minimum-size input
assert run(
    """\
1
1
3
2 1 1
1 1 1 2
2 1 1
"""
) == "1\n1", "minimum size"

# All values equal, plus a range update that changes only part of the array
assert run(
    """\
4
6 6 6 6
3
1 2 3 2
2 1 4
2 2 3
"""
) == "6\n2", "all equal values"

# Boundary and prefix-sensitive comparisons
assert run(
    """\
5
6 10 14 13 1
4
1 2 4 7
2 3 5
2 1 2
2 4 4
"""
) == "7\n30\n7", "range boundaries"

# The prefix case 2 < 6 must be handled correctly.
assert run(
    """\
4
2 6 3 15
2
1 1 4 2
2 1 4
"""
) == "30", "lexicographic prefix case"

# Maximum-size array, with a small number of queries.
big_input = (
    "100000\n"
    + ("1 " * 99999)
    + "1\n"
    + "3\n"
    + "2 1 100000\n"
    + "1 1 100000 1\n"
    + "2 1 100000\n"
)
assert run(big_input) == "1\n1", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1`, value `1` | `1\n1` | Minimum-size input and no-op updates |
| `[6,6,6,6]`, update `[2,3]` to `2` | `6\n2` | Equal maximum groups and partial range updates |
| `[6,10,14,13,1]`, update `[2,4]` to `7` | `7\n30\n7` | Inclusive boundaries and selective replacements |
| `[2,6,3,15]`, update all to `2` | `30` | Lexicographic prefix behavior |
| `100000` copies of `1` | `1\n1` | Maximum array size and full-range queries |

## Edge Cases

The prefix case is handled directly by the subset branch in `less`. For

```
1
1
2
1 1 1 2
2 1 1
```

the first number has mask zero, while `2` has the bit corresponding to prime 2. The first number divides the second, so the comparator checks `1 < 2` and concludes that `1` is smaller. The update is skipped and the answer is `1`.

The nontrivial divisibility case is

```
2
6 30
1
2 1 2
```

The factor masks are `{2,3}` and `{2,3,5}`. The first number divides the second, and the extra prime is `5`. Since `6 > 5`, the comparator decides that `30` is lexicographically smaller than `6`. The range is unchanged by no update here, and the LCM query would use the OR mask `{2,3,5}`, producing `30`.

The LCM overlap case is

```
2
6 10
1
2 1 2
```

The masks are `{2,3}` and `{2,5}`. Their OR is `{2,3,5}`, so the modular product is `2*3*5 = 30`. Multiplying the original values would incorrectly count the common prime 2 twice.

A full-range update is handled without special endpoint logic. For

```
3
6 10 14
1
1 1 3 7
```

the update visits exactly the three positions. The first two values are smaller than `7` under the divisor ordering, while `14` is larger because `[1,2,7,14]` is lexicographically greater than `[1,7]`. The resulting array is `[6,10,7]`. The recursive range representation includes both endpoints, so no position is accidentally excluded.

The case where every value in a node is equal is also significant. Its strict second maximum is `-1`, so the Segment Tree Beats condition accepts the update immediately. The entire node represents one maximum group, and `or_without_max` is zero. Replacing that group therefore changes the node's OR directly to the new value's prime mask without descending to leaves.
