---
title: "CF 102309E - Expectation of Orz Pandas"
description: "There are (n) boxes arranged from left to right. A type 1 operation chooses an interval ([l,r]), a digit (x), and an offset (c). For every position (p) in that interval, where (p=l+k-1), exactly one new paper strip is placed into box (p)."
date: "2026-08-13T23:45:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102309
codeforces_index: "E"
codeforces_contest_name: "The 2019 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102309
solve_time_s: 161
verified: true
draft: false
---

[CF 102309E - Expectation of Orz Pandas](https://codeforces.com/problemset/problem/102309/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) boxes arranged from left to right. A type 1 operation chooses an interval ([l,r]), a digit (x), and an offset (c). For every position (p) in that interval, where (p=l+k-1), exactly one new paper strip is placed into box (p). Its value is the number consisting of (c+k) copies of digit (x).

A type 2 operation asks us to look at every paper strip currently stored in boxes ([l,r]), choose one uniformly at random, and return the expected value of the chosen strip. Thus the answer is the sum of all strip values in the interval divided by the total number of strips there. The division is performed modulo (10^9+7).

The constraints make a direct simulation impossible. There can be (10^5) operations and (10^4) boxes, so processing every affected box for every update can require (10^9) box updates. The value parameter (c) can also reach (10^9), so constructing the actual decimal strings is completely out of the question. We need to represent every strip value algebraically and update whole intervals at once.

There are several edge cases that a straightforward implementation can mishandle. First, a query can cover boxes containing no strips at all. For example,

```
1 1
2 1 1
```

has no available strip, so the answer is `0`. A solution that blindly computes an inverse of the count would divide by zero.

Second, (c) can be zero while (l>1). For example,

```
3 2
1 3 3 1 0
2 3 3
```

places the one-digit strip `1` into box 3, so the answer is `1`. The algebraic representation naturally contains (10^{c-l+1}=10^{-2}), so treating this exponent as an ordinary nonnegative exponent would give a wrong result. We handle this by precomputing inverse powers of 10.

Third, the query interval need not match an update interval. For example,

```
4 2
1 2 4 3 1
2 3 4
```

creates `33`, `333`, and `3333` in boxes 2, 3, and 4. The query sees only `333` and `3333`, so the answer is (3666/2=1833). A solution that stores only the total contribution of each update without respecting its position boundaries would include `33` incorrectly.

Finally, many updates can overlap. The strips are not replaced by later operations, they accumulate. For example,

```
1 3
1 1 1 9 0
1 1 1 9 0
2 1 1
```

leaves two strips, both equal to `9`, so the expectation is still `9`. The data structure must maintain sums and counts under additive updates.

## Approaches

The brute-force approach is straightforward. Maintain, for every box, the list of strips currently inside it. For a type 1 operation, iterate through (p=l,\ldots,r), compute the corresponding repeated-digit number, and append it to box (p). For a type 2 operation, iterate through the requested boxes and sum both the number of strips and the values of those strips. This is correct because the expectation of a uniformly selected item is exactly the total value divided by the number of items.

The problem is the amount of work. One type 1 operation can touch (10^4) boxes, and there can be (10^5) operations, giving as many as (10^9) individual box updates. Queries can also require scanning (10^4) boxes each. The data itself can contain up to (10^9) strips over the lifetime of the operations, so explicitly storing every strip is not viable either.

The useful observation is that the value of the strip added at position (p) has a very simple form. A repeated digit number of length (L) is

[
x\frac{10^L-1}{9}.
]

For an update starting at (l), position (p) corresponds to (k=p-l+1), so its strip has length (c+p-l+1). Its value is

[
x\frac{10^{c+p-l+1}-1}{9}.
]

Rearranging gives

[
\frac{x10^{c-l+1}}9 10^p-\frac{x}{9}.
]

For a fixed update, this is simply

[
A\cdot 10^p+B,
]

where (A) and (B) are constants over the whole update interval.

That is exactly the structure a lazy segment tree can exploit. For every segment, we store the sum of (10^p), the sum of all current strip values, and the number of strips. Applying an update with coefficients (A,B) changes the value sum of a segment ([L,R]) by

[
A\sum_{p=L}^{R}10^p+B(R-L+1).
]

At the same time, one new strip is added to every position, so the strip count increases by (R-L+1).

The segment tree therefore performs an entire type 1 operation lazily in (O(\log n)), and a type 2 operation obtains both the total value and total count in (O(\log n)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(mn)) | (O(mn)) in the worst case | Too slow |
| Optimal | (O(m\log n+\sum \log c_i)) | (O(n)) | Accepted |

The (\log c_i) term comes from modular exponentiation when computing (10^{c_i}). Since (c_i\le 10^9), this is only about 30 modular multiplications per update.

## Algorithm Walkthrough

1. Precompute (10^p\bmod M) and (10^{-p}\bmod M) for every (0\le p\le n). The inverse powers are needed because the coefficient (10^{c-l+1}) can have a negative exponent when (c<l-1). We can write it safely as (10^c10^{1-l}).
2. Build a segment tree over positions (1,\ldots,n). Each node stores `pow_sum`, the sum of (10^p) over its segment, and two dynamic quantities: `value_sum`, the sum of all paper-strip values currently in the segment, and `count_sum`, the number of strips currently in the segment.
3. For a type 1 operation ((l,r,x,c)), rewrite the value added at position (p) as

[
\frac{x10^{c-l+1}}9 10^p-\frac{x}{9}.
]

Define

[
A=x10^c10^{1-l}9^{-1}\pmod M
]

and

[
B=-x9^{-1}\pmod M.
]

The update on every position (p\in[l,r]) is then exactly (A10^p+B).
4. Apply this update lazily to the segment tree. For a fully covered node representing ([L,R]), add

[
A\cdot\text{pow_sum}+B(R-L+1)
]

to its value sum, and add (R-L+1) to its count. Store (A,B), and the count increment in the node's lazy fields so that descendants receive the same update later.
5. For a type 2 query ([l,r]), query the segment tree for the pair ((S,C)), where (S) is the total value of all strips in those boxes and (C) is their total count. If (C=0), output `0`. Otherwise output

[
S C^{-1}\pmod M.
]
6. Process test cases until EOF. The tree is rebuilt for each new pair ((n,m)), so strips from different test cases never interact.

### Why it works

The invariant is that for every segment tree node, `value_sum` equals the sum of the values of every strip currently belonging to positions in that node's interval, while `count_sum` equals the number of those strips. The static `pow_sum` equals the sum of (10^p) over the same positions.

A type 1 operation adds (A10^p+B) to exactly one new strip at each affected position. For a complete segment, summing this expression gives (A\cdot\text{pow_sum}+B\cdot\text{length}), exactly the update applied by the tree, and the number of new strips is exactly the segment length. Lazy propagation preserves these same quantities for every descendant.

A type 2 query consequently obtains the exact total value and exact total number of selectable strips in its interval. Dividing the former by the latter is precisely the definition of the requested expectation, so the returned modular value is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007
INV9 = pow(9, MOD - 2, MOD)
INV10 = pow(10, MOD - 2, MOD)

def solve():
    out = []

    while True:
        first = input()
        if not first:
            break

        n, m = map(int, first.split())

        pow10 = [1] * (n + 1)
        invpow10 = [1] * (n + 1)

        for i in range(1, n + 1):
            pow10[i] = pow10[i - 1] * 10 % MOD
            invpow10[i] = invpow10[i - 1] * INV10 % MOD

        size = 4 * n + 5

        pow_sum = [0] * size
        value_sum = [0] * size
        count_sum = [0] * size

        lazy_a = [0] * size
        lazy_b = [0] * size
        lazy_c = [0] * size

        def build(node, left, right):
            if left == right:
                pow_sum[node] = pow10[left]
                return

            mid = (left + right) >> 1
            lc = node << 1
            rc = lc | 1

            build(lc, left, mid)
            build(rc, mid + 1, right)

            pow_sum[node] = (pow_sum[lc] + pow_sum[rc]) % MOD

        def apply(node, left, right, a, b, c):
            length = right - left + 1

            value_sum[node] = (
                value_sum[node]
                + a * pow_sum[node]
                + b * length
            ) % MOD

            count_sum[node] += c * length

            lazy_a[node] = (lazy_a[node] + a) % MOD
            lazy_b[node] = (lazy_b[node] + b) % MOD
            lazy_c[node] += c

        def push(node, left, right):
            a = lazy_a[node]
            b = lazy_b[node]
            c = lazy_c[node]

            if a == 0 and b == 0 and c == 0:
                return

            if left != right:
                mid = (left + right) >> 1
                lc = node << 1
                rc = lc | 1

                apply(lc, left, mid, a, b, c)
                apply(rc, mid + 1, right, a, b, c)

            lazy_a[node] = 0
            lazy_b[node] = 0
            lazy_c[node] = 0

        def update(node, left, right, ql, qr, a, b):
            if ql <= left and right <= qr:
                apply(node, left, right, a, b, 1)
                return

            push(node, left, right)

            mid = (left + right) >> 1
            lc = node << 1
            rc = lc | 1

            if ql <= mid:
                update(lc, left, mid, ql, qr, a, b)

            if qr > mid:
                update(rc, mid + 1, right, ql, qr, a, b)

            value_sum[node] = (value_sum[lc] + value_sum[rc]) % MOD
            count_sum[node] = count_sum[lc] + count_sum[rc]

        def query(node, left, right, ql, qr):
            if ql <= left and right <= qr:
                return value_sum[node], count_sum[node]

            push(node, left, right)

            mid = (left + right) >> 1
            lc = node << 1
            rc = lc | 1

            total_value = 0
            total_count = 0

            if ql <= mid:
                v, c = query(lc, left, mid, ql, qr)
                total_value += v
                total_count += c

            if qr > mid:
                v, c = query(rc, mid + 1, right, ql, qr)
                total_value += v
                total_count += c

            return total_value % MOD, total_count

        build(1, 1, n)

        for _ in range(m):
            operation = list(map(int, input().split()))

            if operation[0] == 1:
                _, l, r, x, c = operation

                # x * 10^(c-l+1) / 9
                # = x * 10^c * 10^(1-l) / 9
                a = x * pow(10, c, MOD) % MOD
                a = a * invpow10[l - 1] % MOD
                a = a * 10 % MOD
                a = a * INV9 % MOD

                b = (-x * INV9) % MOD

                update(1, 1, n, l, r, a, b)

            else:
                _, l, r = operation

                total_value, total_count = query(
                    1, 1, n, l, r
                )

                if total_count == 0:
                    out.append("0")
                else:
                    answer = total_value * pow(
                        total_count, MOD - 2, MOD
                    ) % MOD
                    out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `pow10` array contains the static weight (10^p) for every box. The `invpow10` array handles the case where (c-l+1) is negative. Using

[
10^{c-l+1}=10^c10^{-(l-1)}10
]

keeps every exponent passed to `pow` nonnegative.

The segment tree's `pow_sum` never changes because box positions never change. The other three node quantities are dynamic. `value_sum` stores the modular sum of strip values, `count_sum` stores an ordinary integer count, and the three lazy arrays describe an update that still needs to be propagated to the children.

The order inside `apply` matters conceptually. First, the current node receives the complete update. Only afterward does lazy propagation defer that same update to its children. When a query partially intersects a node, `push` is called before descending, so the children see every update that was previously stored only at their ancestor.

The count is deliberately not reduced modulo (M). At most (10^5) operations can each contribute at most (10^4) strips to a query, so the total count is at most (10^9), which is smaller than (M=10^9+7). Thus a nonzero count is always invertible modulo (M), and keeping it as an ordinary integer also makes the zero test direct.

Python integers do not overflow, so the intermediate product `a * pow_sum[node]` is safe. The value sums and lazy coefficients are reduced modulo (M) after arithmetic so that their sizes remain controlled.

## Worked Examples

### Sample 1

The input is

```
3 3
1 2 3 5 1
1 1 2 1 3
2 2 3
```

The first update puts `55` into box 2 and `555` into box 3. The second update puts `1111` into box 1 and `11111` into box 2. The query covers boxes 2 and 3.

| Operation | Affected positions | New strips | Query result |
| --- | --- | --- | --- |
| `1 2 3 5 1` | 2, 3 | 55, 555 |  |
| `1 1 2 1 3` | 1, 2 | 1111, 11111 |  |
| `2 2 3` | 2, 3 | 55, 11111, 555 | ((55+11111+555)/3=3907) |

The segment tree has total value (11721) and total count (3) over boxes 2 through 3, giving `3907`.

This demonstrates that different updates can overlap at the same box, with every strip remaining independently selectable.

### Example 2

Consider

```
4 4
1 1 4 2 0
2 1 4
1 2 3 3 1
2 2 3
```

The first update creates `2`, `22`, `222`, and `2222`. Its first query therefore sees four strips whose sum is (2468).

| Operation | Positions | Values added | Queried sum | Queried count |
| --- | --- | --- | --- | --- |
| `1 1 4 2 0` | 1, 2, 3, 4 | 2, 22, 222, 2222 |  |  |
| `2 1 4` | 1, 2, 3, 4 |  | 2468 | 4 |
| `1 2 3 3 1` | 2, 3 | 33, 333 |  |  |
| `2 2 3` | 2, 3 | 22, 222, 33, 333 | 610 | 4 |

The first expectation is (2468/4=617). The second is (610/4=305/2), which is `500000156` modulo (10^9+7).

The second query confirms that the tree combines old and new strips while restricting the result exactly to the requested interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(m\log n+\sum \log c_i)) | Each update and query visits (O(\log n)) segment-tree nodes, while each type 1 operation computes (10^c\bmod M) in (O(\log c)). |
| Space | (O(n)) | The segment tree and the power arrays each contain (O(n)) entries. |

With (n\le10^4) and (m\le10^5), the segment tree performs only logarithmic work per operation. The largest exponent is (10^9), so modular exponentiation requires only a small constant number of multiplication steps per update. The memory consumption is also comfortably within 256 MB.

## Test Cases

The following test harness assumes the submitted solution is saved as `solution.py`. The helper replaces both standard input and the module's `input` function so that the same `solve()` implementation can be exercised repeatedly.

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solution.input = sys.stdin.readline
        solution.solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    """3 3
1 2 3 5 1
1 1 2 1 3
2 2 3
"""
) == "3907", "sample 1"

# Minimum-size input, with no available strips
assert run(
    """1 1
2 1 1
"""
) == "0", "empty query"

# Repeated identical strips in one box
assert run(
    """1 4
1 1 1 9 0
1 1 1 9 0
1 1 1 9 0
2 1 1
"""
) == "9", "all-equal values"

# Boundary case with c = 0 and l > 1, which needs inverse powers of 10
assert run(
    """3 2
1 3 3 1 0
2 3 3
"""
) == "1", "negative exponent case"

# Large c, checking modular exponentiation
MOD = 1000000007
INV9 = pow(9, MOD - 2, MOD)
huge_value = 7 * (pow(10, 1000000001, MOD) - 1) % MOD
huge_value = huge_value * INV9 % MOD

assert run(
    """2 2
1 2 2 7 1000000000
2 2 2
"""
) == str(huge_value), "large c"

# Maximum-size n and m.
# Every update covers the whole array, so the expected value in the last
# box is just the same repunit value, regardless of the number of updates.
n = 10000
m = 100000
lines = [f"{n} {m}"]
lines.extend(["1 1 10000 1 0"] * (m - 1))
lines.append("2 10000 10000")
max_input = "\n".join(lines) + "\n"

repunit = (pow(10, 10000, MOD) - 1) * INV9 % MOD
expected_max = repunit * (m - 1) % MOD

assert run(max_input) == str(expected_max), "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 2 1 1` | `0` | Empty query and division-by-zero protection |
| Three identical updates on one box | `9` | Accumulation of multiple equal strips |
| `1 3 3 1 0` followed by a query | `1` | Negative exponent in (10^{c-l+1}) |
| Update with (c=10^9) | Computed modular value | Large exponent handling |
| (n=10^4,\ m=10^5) | Computed modular value | Maximum input size and lazy full-range updates |

## Edge Cases

An empty query is handled before modular inversion. For

```
1 1
2 1 1
```

the root represents the only box and has `count_sum = 0`. The query returns `(0, 0)`, so the code immediately appends `0`. No inverse is attempted.

The negative exponent case is handled through the inverse-power array. For

```
3 2
1 3 3 1 0
2 3 3
```

the strip has length (c+1=1), so its value is exactly `1`. Algebraically,

[
1\frac{10^{0+1}-1}{9}=1.
]

The coefficient representation uses

[
10^{c-l+1}=10^{-2},
]

which is represented as `10^0 * 10^-2`. The segment tree multiplies this coefficient by (10^3) and subtracts the constant (1/9), recovering `1` modulo (M).

Boundary alignment is handled by the segment tree's half-open logic implemented through inclusive intervals. For

```
4 2
1 2 4 3 1
2 3 4
```

the update affects exactly positions 2, 3, and 4. The query visits only positions 3 and 4, returning values `333` and `3333`, with sum `3666` and count `2`. The result is `1833`.

Overlapping updates are additive because every type 1 operation represents a new strip rather than a replacement. If two identical updates affect the same box, the node's `value_sum` and `count_sum` each receive two independent contributions. For three updates adding `9` to the only box, the stored pair becomes `(27,3)`, and the query returns (27/3=9).

Large (c) is never used to construct a decimal string. For (c=10^9), the code computes (10^{c}\bmod M) with modular exponentiation and combines it with the precomputed inverse power for the starting position. The resulting value is mathematically identical to the enormous repeated-digit integer, but all arithmetic stays modulo (10^9+7).

The maximum total number of strips in one query can reach (10^9), but this is still below (M). Consequently the denominator cannot become congruent to zero modulo (M) under the given constraints. Storing the count as an ordinary Python integer also avoids accidentally losing information through modular reduction.
