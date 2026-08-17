---
title: "CF 102253J - Journey with Knapsack"
description: "There are (n) food types. Type (i) occupies (i) units of volume, and we may choose between (0) and (ai) pieces of it. We must also choose exactly one equipment type."
date: "2026-08-17T21:43:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102253
codeforces_index: "J"
codeforces_contest_name: "2017 Chinese Multi-University Training, BeihangU Contest"
rating: 0
weight: 102253
solve_time_s: 163
verified: true
draft: false
---

[CF 102253J - Journey with Knapsack](https://codeforces.com/problemset/problem/102253/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) food types. Type (i) occupies (i) units of volume, and we may choose between (0) and (a_i) pieces of it. We must also choose exactly one equipment type. Equipment (j) occupies (b_j) units of volume, and two equal-volume equipment pieces are still different choices if they have different indices.

The knapsack has capacity (2n). If the chosen equipment has volume (b), the food must occupy exactly (2n-b). Let (f(s)) be the number of valid food selections with total volume (s). The final answer is simply

[
\sum_{j=1}^{m} f(2n-b_j).
]

The input can contain about 100 test cases, with (n) reaching (5\cdot 10^4). A quadratic algorithm over the (2n) possible volumes is already too large, and a conventional bounded-knapsack transition over all (n) food types would be (O(n^2)). The restriction that at most five tests have (n\ge 1000) tells us that a roughly (O(n\sqrt n)) solution is intended. The memory bound also favors a few one-dimensional arrays rather than a full two-dimensional dynamic program.

The distinctive condition is that (a_1<a_2<\cdots<a_n). Since the (a_i) are distinct nonnegative integers, (a_i\ge i-1). This apparently small observation is the key to making the generating function manageable.

There are several boundary cases that can silently break a careless implementation. Consider

```
1 1
0
1
```

There is no food available at all, and the only equipment fills the knapsack, so the answer is `Case #1: 1`. An implementation that assumes every food type can contribute at least one piece would count an impossible selection.

Repeated equipment volumes must also remain repeated choices. For

```
2 3
0 1
4 4 4
```

the food must have volume zero, so there is exactly one food selection. There are three different equipment types, hence the answer is `Case #1: 3`. Deduplicating the (b_i) values would incorrectly return one.

The upper bounds on food must be respected even when an unrestricted partition gives another representation. For

```
2 1
0 1
2
```

the only possible food volume is (2), obtained by taking one piece of type 2. Taking two pieces of type 1 is forbidden because (a_1=0). The answer is `Case #1: 1`. Treating the denominator as an ordinary unrestricted partition function without restoring the numerator factors would count two representations.

The same boundary issue appears at the largest equipment volume. If (b_j=2n), the required food volume is zero, and exactly one food selection exists, namely taking nothing. The coefficient (f(0)) must remain equal to one throughout every polynomial operation.

## Approaches

A direct solution can enumerate every possible number of pieces of every food type, calculate its total volume, and then check whether the remaining capacity matches one of the equipment pieces. For a fixed equipment type this examines

[
\prod_{i=1}^{n}(a_i+1)
]

food combinations. Because the (a_i) are distinct and lie in ([0,2n]), the largest possible product is obtained by choosing (a_i=n+i), giving

\frac{(2n+1)!}{(n+1)!}.
]

Multiplying by up to (2n) equipment types makes this completely infeasible. Even the weaker lower bound (\prod_i(a_i+1)\ge n!), which follows from (a_i\ge i-1), is already astronomically large for (n=5\cdot10^4).

The usual dynamic programming approach is much better conceptually. We could maintain the number of ways to obtain every volume and process each food type with a bounded-knapsack transition. Unfortunately, there are (n) types and (2n) possible volumes, so the straightforward implementation still costs (O(n^2)).

The useful way to compress the problem is to write its ordinary generating function. For food type (i), the possible contributions are

\frac{1-x^{(a_i+1)i}}{1-x^i}.
]

Thus

\prod_{i=1}^{n}
\frac{1-x^{(a_i+1)i}}{1-x^i}.
]

Only coefficients through (x^{2n}) matter, so all polynomial calculations can be performed modulo (x^{2n+1}). This is the main reduction used in the official editorial.

Now consider the numerator. Because (a_i\ge i-1),

[
(a_i+1)i\ge i^2.
]

If (i^2>2n), then the factor

[
1-x^{(a_i+1)i}
]

is just (1) modulo (x^{2n+1}). Consequently, only (O(\sqrt n)) numerator factors can affect the answer. We can multiply those factors into a polynomial explicitly in (O(n\sqrt n)) time.

The denominator resembles the generating function for integer partitions:

[
P(x)=\prod_{i\ge1}\frac1{1-x^i}
=\sum_{k\ge0}p(k)x^k.
]

Euler's pentagonal-number recurrence computes (p(k)) through (k=2n) in (O(n\sqrt n)) time. The standard recurrence is

[
p(k)=
\sum_{r\ge1}(-1)^{r+1}
\left(
p\left(k-\frac{r(3r-1)}2\right)
+
p\left(k-\frac{r(3r+1)}2\right)
\right).
]

We need the denominator with only factors (1,\ldots,n), not all positive integers. Up to degree (2n), we can write

P(x)\prod_{i=n+1}^{2n}(1-x^i).
]

Any product of two powers (x^i x^j) with (i,j>n) has degree greater than (2n), so modulo (x^{2n+1}),

1-\sum_{i=n+1}^{2n}x^i.
]

Thus the denominator coefficients are obtained from the partition numbers using a simple prefix sum. This is the second key observation behind the (O(n\sqrt n)) solution.

The brute-force and optimal approaches can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O\left(m\prod_i(a_i+1)\right)) | (O(n)) | Too slow |
| Bounded Knapsack DP | (O(n^2)) | (O(n)) | Too slow |
| Generating Function + Pentagonal Recurrence | (O(n\sqrt n+m)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Let (N=2n). We only need the coefficients of (F(x)) from degree (0) through (N), because an equipment item has positive volume and the knapsack capacity is exactly (N).
2. Compute the unrestricted partition numbers (p(0),p(1),\ldots,p(N)) using Euler's pentagonal recurrence. Here (p(k)) counts partitions of (k) using arbitrary positive integer part sizes.
3. Convert the unrestricted partition sequence into the denominator for food types (1,\ldots,n). Let (q(k)) denote the coefficient of

[
\prod_{i=1}^{n}\frac1{1-x^i}.
]

For (k\le n), (q(k)=p(k)). For (k>n), the extra unrestricted partitions are exactly those containing one part greater than (n). Since (k\le2n), there can be at most one such part. Equivalently, using the polynomial identity above,

[
q(k)=p(k)-\sum_{r=0}^{k-n-1}p(r).
]

A running prefix sum computes every such coefficient in linear time.

1. Copy these denominator coefficients into the working array (f). Initially, (f(k)=q(k)), which corresponds to allowing every food type to appear without its upper bound.
2. Process the numerator factors

[
1-x^{(a_i+1)i}.
]

For type (i), define

[
t_i=(a_i+1)i.
]

If (t_i>N), the factor has no effect on the coefficients we care about. Since (a_i) is increasing, the values (t_i) are also increasing, so we can stop at the first such (i).

For every useful (t_i), multiply the current polynomial by (1-x^{t_i}). In coefficient form,

[
f[k]\leftarrow f[k]-f[k-t_i].
]

The update must run from large (k) down to (t_i). Descending order makes every (f[k-t_i]) come from the polynomial before this factor was applied, exactly like a zero-one knapsack transition.

1. After all useful numerator factors have been applied, (f(s)) is exactly the number of legal food selections whose total volume is (s). For every equipment item of volume (b_j), the food must have volume (N-b_j). Add

[
f[N-b_j]
]

for every equipment index (j), preserving duplicates because different equipment types represent different ways.

### Why it works

The generating function for one food type records every allowed number of pieces of that type exactly once. Multiplying these factors combines independent choices, so the coefficient of (x^s) counts precisely the food selections of total volume (s).

Replacing each finite geometric series by

[
\frac{1-x^{(a_i+1)i}}{1-x^i}
]

separates the problem into an unrestricted denominator and correction factors that remove selections exceeding each upper bound. The denominator is computed exactly through the partition generating function, and every relevant numerator factor is then applied exactly once. Since all omitted numerator factors have degree greater than (2n), they cannot affect any coefficient used by the answer.

Finally, choosing equipment (j) leaves exactly (2n-b_j) volume for food, so summing the corresponding coefficient once for every equipment index counts every valid packing exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

# Partition numbers p(k), initially p(0) = 1.
part = [1]

def ensure_partitions(N):
    """Extend part[] so that it contains p(0)..p(N)."""
    old = len(part)
    if old > N:
        return

    part.extend([0] * (N + 1 - old))

    pent = []
    r = 1
    while True:
        g1 = r * (3 * r - 1) // 2
        if g1 > N:
            break

        sign = 1 if (r & 1) else -1
        pent.append((g1, sign))

        g2 = r * (3 * r + 1) // 2
        if g2 <= N:
            pent.append((g2, sign))

        r += 1

    # The generalized pentagonal numbers are generated in increasing order.
    for k in range(old, N + 1):
        s = 0
        for g, sign in pent:
            if g > k:
                break
            if sign == 1:
                s += part[k - g]
            else:
                s -= part[k - g]
        part[k] = s % MOD

def solve_case(n, m, a, b):
    N = 2 * n
    ensure_partitions(N)

    # Start with P(x) = sum p(k)x^k.
    f = part[:N + 1]

    # Replace unrestricted partitions by partitions whose parts are <= n.
    # For k > n, subtract sum_{r=0}^{k-n-1} p(r).
    prefix = 0
    for k in range(n + 1, N + 1):
        prefix += part[k - n - 1]
        if prefix >= MOD:
            prefix -= MOD

        value = f[k] - prefix
        if value < 0:
            value += MOD
        f[k] = value

    # Apply the useful numerator factors:
    # product (1 - x^((a_i + 1)i)).
    #
    # Since a_i is increasing, t_i is increasing too.
    for i, ai in enumerate(a, 1):
        t = (ai + 1) * i
        if t > N:
            break

        for k in range(N, t - 1, -1):
            value = f[k] - f[k - t]
            if value < 0:
                value += MOD
            f[k] = value

    # Choose one equipment type. Equal b values are intentionally counted
    # repeatedly because the equipment types themselves are different.
    ans = 0
    for bj in b:
        ans += f[N - bj]
        if ans >= MOD:
            ans -= MOD

    return ans

def solve():
    case_no = 1
    out = []

    while True:
        line = input()
        if not line:
            break

        if not line.strip():
            continue

        n, m = map(int, line.split())

        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        ans = solve_case(n, m, a, b)
        out.append(f"Case #{case_no}: {ans}")
        case_no += 1

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The global `part` array is extended only when a larger value of (2n) is needed. This matters because the input contains many test cases, and recomputing the partition sequence independently for every test would repeat the most expensive part of the computation. The recurrence for a newly appended (p(k)) depends only on earlier values, so extending the existing array is valid.

The partition recurrence uses generalized pentagonal numbers (r(3r-1)/2) and (r(3r+1)/2). The sign is positive for odd (r) and negative for even (r). The inner loop stops as soon as the pentagonal number exceeds the current degree.

The denominator correction deserves special attention. For (k=n+1), the prefix contains only (p(0)), so exactly the partitions with one part (n+1) are removed. For (k=2n), the prefix contains (p(0),\ldots,p(n-1)), covering every possible partition whose unique part above (n) is (n+1,\ldots,2n).

The numerator multiplication uses descending indices. If the loop ran upward, a coefficient modified earlier in the same factor could be used again, effectively applying (1-x^t) multiple times. Descending order prevents that contamination.

The condition `if t > N: break` is safe because (t_i=(a_i+1)i) increases with (i). It is also the reason the numerator work is only (O(n\sqrt n)).

There is no integer-overflow issue in Python. The values are reduced modulo (10^9+7), and even the temporary sum in the partition recurrence remains within a manageable integer size because it contains only (O(\sqrt N)) terms.

## Worked Examples

### Sample 1

The first sample case is

```
1 1
1
1
```

Here (n=1), so the knapsack capacity is (N=2). There is one food type of volume (1), with at most one piece, and one equipment item of volume (1).

| Step | State | Value |
| --- | --- | --- |
| Capacity | (N=2n) | 2 |
| Partition coefficients | (p(0),p(1),p(2)) | (1,1,2) |
| Denominator | parts allowed up to 1 | (1,1,1) |
| Numerator exponent | ((a_1+1)\cdot1) | 2 |
| After numerator | (f(0),f(1),f(2)) | (1,1,0) |
| Equipment target | (N-b_1) | 1 |
| Added contribution | (f(1)) | 1 |

The numerator factor (1-x^2) removes the invalid choice of two pieces of the type-1 food. The coefficient at volume one remains one, corresponding to taking one food piece.

### Sample 2

The second sample case is

```
2 2
1 2
3 4
```

The capacity is (N=4). Type 1 allows one piece, and type 2 allows two pieces.

| Step | State | Value |
| --- | --- | --- |
| Capacity | (N=2n) | 4 |
| Partition coefficients | (p(0)\ldots p(4)) | (1,1,2,3,5) |
| Denominator | parts allowed up to 2 | (1,1,2,2,3) |
| Type 1 exponent | ((1+1)\cdot1) | 2 |
| Type 1 update | multiply by (1-x^2) | (1,1,1,1,1) |
| Type 2 exponent | ((2+1)\cdot2) | 6 |
| Type 2 update | exponent exceeds 4 | unchanged |
| Equipment 1 target | (4-3) | 1 |
| Equipment 2 target | (4-4) | 0 |
| Total | (f(1)+f(0)) | 2 |

The first numerator factor removes the unrestricted representation containing two pieces of type 1. The second factor cannot affect degrees through four because its exponent is six. Both equipment choices have exactly one compatible food selection, giving two total ways.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\sqrt n+m)) per large test | Partition recurrence costs (O(n\sqrt n)), useful numerator factors cost (O(n\sqrt n)), equipment processing costs (O(m)) |
| Space | (O(n)) | Two coefficient arrays of length (2n+1), plus the (a) and (b) arrays |

The largest relevant polynomial degree is (2n\le10^5). Only (O(\sqrt n)) numerator factors can matter because their exponents are at least (i^2). The restriction that at most five test cases have (n\ge10^3) keeps the total amount of expensive work under control, while smaller cases require substantially fewer operations. The implementation also reuses the partition sequence across test cases.

## Test Cases

```python
import sys
import io

MOD = 1_000_000_007

part = [1]

def ensure_partitions(N):
    old = len(part)
    if old > N:
        return

    part.extend([0] * (N + 1 - old))

    pent = []
    r = 1
    while True:
        g1 = r * (3 * r - 1) // 2
        if g1 > N:
            break

        sign = 1 if r & 1 else -1
        pent.append((g1, sign))

        g2 = r * (3 * r + 1) // 2
        if g2 <= N:
            pent.append((g2, sign))

        r += 1

    for k in range(old, N + 1):
        s = 0
        for g, sign in pent:
            if g > k:
                break
            s += sign * part[k - g]
        part[k] = s % MOD

def solve_case(n, m, a, b):
    N = 2 * n
    ensure_partitions(N)

    f = part[:N + 1]

    prefix = 0
    for k in range(n + 1, N + 1):
        prefix += part[k - n - 1]
        if prefix >= MOD:
            prefix -= MOD

        f[k] -= prefix
        if f[k] < 0:
            f[k] += MOD

    for i, ai in enumerate(a, 1):
        t = (ai + 1) * i
        if t > N:
            break

        for k in range(N, t - 1, -1):
            f[k] -= f[k - t]
            if f[k] < 0:
                f[k] += MOD

    ans = 0
    for bj in b:
        ans += f[N - bj]
        if ans >= MOD:
            ans -= MOD

    return ans

def solution():
    input = sys.stdin.readline
    case_no = 1
    out = []

    while True:
        line = input()
        if not line:
            break

        if not line.strip():
            continue

        n, m = map(int, line.split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        out.append(f"Case #{case_no}: {solve_case(n, m, a, b)}")
        case_no += 1

    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        # Reuse the same global partition cache as the actual solution.
        exec_result = solution()
        sys.stdout.write(exec_result)
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples.
sample = """\
1 1
1
1
2 2
1 2
3 4
3 3
1 2 3
2 3 3
"""

assert run(sample) == (
    "Case #1: 1\n"
    "Case #2: 2\n"
    "Case #3: 6"
), "provided samples"

# Minimum-size input, with no food available.
assert run("""\
1 1
0
1
""") == "Case #1: 1", "minimum-size case"

# All equipment volumes are equal, so every equipment type must be counted.
assert run("""\
2 3
0 1
4 4 4
""") == "Case #1: 3", "duplicate equipment types"

# Boundary case for a food upper bound.
# With a = [0, 1], volume 2 can only be formed by one type-2 food.
assert run("""\
2 1
0 1
2
""") == "Case #1: 1", "food upper-bound boundary"

# Maximum n. Choosing equipment of volume 2n leaves zero volume for food,
# so the answer is exactly one regardless of the many food types.
n = 50000
a = " ".join(str(i) for i in range(n))
large_input = f"{n} 1\n{a}\n{2 * n}\n"
assert run(large_input) == "Case #1: 1", "maximum-size boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0 / 1` | `Case #1: 1` | Minimum size and zero food availability |
| `2 3 / 0 1 / 4 4 4` | `Case #1: 3` | Equal equipment volumes must remain separate choices |
| `2 1 / 0 1 / 2` | `Case #1: 1` | Food upper bound and numerator correction |
| (n=50000,\ a_i=i-1,\ b_1=100000) | `Case #1: 1` | Maximum size and the (b=2n) boundary |

## Edge Cases

When a food upper bound is zero, its entire generating-function factor is just (1). For

```
1 1
0
1
```

the exponent of its numerator correction is ((0+1)\cdot1=1), so the food generating function is

[
\frac{1-x}{1-x}=1.
]

The only food volume is zero, and equipment volume one consumes the remaining unit. The algorithm produces `Case #1: 1`.

When several equipment types have the same volume, they must not be merged. For

```
2 3
0 1
4 4 4
```

every equipment item leaves food volume zero. The coefficient (f(0)=1), and the final loop adds that coefficient three times. The result is `Case #1: 3`.

For the upper-bound correction example

```
2 1
0 1
2
```

the unrestricted denominator allows partitions of two using parts one and two, giving two possibilities: (1+1) and (2). The numerator factor for type 1 is (1-x), because (a_1=0), while the factor for type 2 is (1-x^4). Multiplying by (1-x) removes the (1+1) representation, leaving (f(2)=1). The required food volume is two, so the answer is `Case #1: 1`.

When equipment fills the entire knapsack, the required food volume is zero. For the maximum-size test with (n=50000), (a_i=i-1), and (b_1=100000=2n), every numerator and denominator operation preserves (f(0)=1). The final lookup is (f(0)), so the answer is exactly one. This also verifies that the coefficient arrays include degree zero and that the expression `N - bj` never needs a negative index because every equipment volume is at most (N).

The most subtle boundary in the polynomial construction occurs at degree (2n). The product of any two factors (x^i) and (x^j) with (i,j>n) has degree greater than (2n), so those cross terms can safely be discarded. This is precisely why the denominator correction reduces to one prefix-sum subtraction instead of requiring another polynomial multiplication.

The numerator has the opposite kind of boundary. A factor with exponent exactly (2n) still changes the coefficient at degree (2n), so the condition must be `t > N`, not `t >= N`. The descending update includes `k=N` when `t=N`, which is necessary to remove that contribution correctly.
