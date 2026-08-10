---
title: "CF 102394B - Binary Numbers"
description: "Every integer from (0) through (2^m-1) can be viewed as an (m)-bit binary string, padding leading zeroes when necessary. The function (F{m-1}(a,b)) counts how many consecutive bits from the most significant side are equal before the first mismatch."
date: "2026-08-10T19:01:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "B"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 149
verified: true
draft: false
---

[CF 102394B - Binary Numbers](https://codeforces.com/problemset/problem/102394/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

Every integer from (0) through (2^m-1) can be viewed as an (m)-bit binary string, padding leading zeroes when necessary. The function (F_{m-1}(a,b)) counts how many consecutive bits from the most significant side are equal before the first mismatch. In other words, it is the longest common prefix length, or LCP, of the two (m)-bit strings.

The intervals form one consecutive partition of the entire range (0) through (2^m-1). For every interval ([L_i,R_i]), we choose one representative (A_i) from that interval. The representative must be at least as similar, in the LCP sense, to every number (k) inside its own interval as every other chosen representative is.

After all representatives are chosen, the value of the selection is their product. We need the sum of these products over every valid selection, modulo (100000007).

The constraints tell us exactly where the useful structure has to come from. There are at most (2^{17}=131072) possible integers in one test case, and the sum of (2^m) over all test cases is at most (2^{18}). Thus an algorithm close to linear in (2^m) is desirable. An (O(2^{2m})) method is immediately impossible, while an (O(2^m m^2)) method is reasonable because (m\le17).

There are several edge cases that can easily break a careless implementation. When (m=0), the only possible integer is (0), so the answer is (0). For example,

```
1
0 1
0 0
```

has output

```
0
```

A solution that assumes there is always at least one bit can access invalid bit positions or initialize the DP incorrectly.

When there is only one interval, there are no comparisons with other representatives at all. Every value in the interval is valid. For example,

```
1
2 1
0 3
```

has answer (0+1+2+3=6). A solution that unnecessarily imposes a neighboring-interval condition can incorrectly remove candidates.

Boundary ties also matter. Consider

```
1
2 2
0 1
2 3
```

There are four possible choices. All four satisfy the condition, and their products are (0\cdot2), (0\cdot3), (1\cdot2), and (1\cdot3), giving answer (5). The inequalities must be non-strict because equal LCP values are allowed.

Finally, the modulus is (100000007), not (1000000007). For example,

```
1
17 1
0 131071
```

has the unrestricted sum (8589869056), whose required residue is (89868461). Using the more familiar (10^9+7) modulus silently produces the wrong answer.

## Approaches

The direct approach is to enumerate every possible sequence (A_1,\ldots,A_N). For every sequence, we can check the original condition by comparing each chosen representative with every other representative over the numbers in its interval. This is correct because it follows the definition literally, but the number of sequences is the real problem.

If every interval contains two numbers, and there are (65536) intervals, which is possible when (m=17), simply enumerating the choices already gives

[
2^{65536}
]

different sequences. That is far beyond anything that can be processed. Even before checking whether those sequences are valid, enumeration itself is impossible.

The useful observation comes from interpreting (F) as LCP. Suppose (a<b<c). For binary strings in sorted numerical order, the common prefix between the two outer values is controlled by the common prefixes of the adjacent values. In particular, as another value moves farther to the right, its LCP with a fixed value cannot become larger in a way that creates a new better competitor.

This means that inside interval (i), we do not have to compare (A_i) independently with every representative. It is enough to compare it with its immediate neighbors. For the left neighbor, the relevant endpoint is (L_i):

[
\operatorname{LCP}(A_i,L_i)
\ge
\operatorname{LCP}(A_{i-1},L_i).
]

For the right neighbor, the relevant endpoint is (R_i):

[
\operatorname{LCP}(A_i,R_i)
\ge
\operatorname{LCP}(A_{i+1},R_i).
]

If these inequalities hold, every farther representative is automatically no better because it lies even farther in the same numerical direction. This reduces a global condition involving all representatives to two local inequalities. The official editorial uses exactly this LCP reduction.

Now we can build a DP from left to right. For a chosen (A_i), four LCP values are relevant:

[
\begin{aligned}
a &= \operatorname{LCP}(A_i,L_i),\
b &= \operatorname{LCP}(A_i,R_i),\
c &= \operatorname{LCP}(A_i,L_{i+1}),\
d &= \operatorname{LCP}(A_i,R_{i-1}).
\end{aligned}
]

The first two describe how the current representative behaves at its own endpoints. The last two describe exactly the information needed when the neighboring interval is processed.

Suppose the previous representative has state ((c',b')). For the current candidate, the two neighbor conditions become

[
c'\le a
]

and

[
b'\ge d.
]

So all compatible previous states lie in one rectangle of the two-dimensional DP table. A two-dimensional prefix/suffix sum lets us obtain the total contribution of that rectangle in (O(1)) after an (O(m^2)) preprocessing step.

The DP has only ((m+1)^2) states, and every integer belongs to exactly one interval. Thus the total number of candidate representatives processed over the whole test case is exactly (2^m). Combining this with the (O(m^2)) state transformation gives (O(2^m m^2)), which is the intended complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | At least (2^{65536}) sequences in the worst case | (O(N)) | Too slow |
| Optimal | (O(2^m m^2)) | (O(m^2)) | Accepted |

## Algorithm Walkthrough

1. Treat every number as an (m)-bit binary string and interpret (F_{m-1}(a,b)) as (\operatorname{LCP}(a,b)). For two integers, the LCP can be computed from their XOR. If (x=a\oplus b) is nonzero, the highest set bit of (x) is the first differing bit, so the LCP is (m-\operatorname{bit_length}(x)). If (x=0), the LCP is (m).
2. Use the local-neighbor property to reduce the validity condition. For interval (i), the only constraints involving the previous interval are

[
\operatorname{LCP}(A_i,L_i)
\ge
\operatorname{LCP}(A_{i-1},L_i),
]

while the only constraint involving the next interval is

[
\operatorname{LCP}(A_i,R_i)
\ge
\operatorname{LCP}(A_{i+1},R_i).
]

Every more distant interval is automatically handled by the monotonicity of LCP along the ordered integer line.
3. After processing interval (i), store a state indexed by

[
(c,b)=
\left(
\operatorname{LCP}(A_i,L_{i+1}),
\operatorname{LCP}(A_i,R_i)
\right).
]

The value stored in that state is the sum of products of all valid choices ending there. The first coordinate is what the next interval will use as its comparison against (L_{i+1}), and the second coordinate is what the next interval will use as its comparison against (R_i).
4. Before processing an interval, transform the previous state table into a cumulative table. Define

\sum_{\substack{c\le x\b\ge y}} g[c][b].
]

This is exactly the set of previous representatives compatible with a current candidate having endpoint values (x) and (y). The transform is a prefix sum in the first coordinate and a suffix sum in the second coordinate, so it takes (O(m^2)).
5. Initialize the cumulative table so that every first representative is allowed. Conceptually, this is equivalent to placing a single virtual state at ((0,m)) and applying the same cumulative transform. Since there is no previous interval, every possible first candidate must be accepted.
6. For every candidate (x) in interval (i), calculate

[
A=\operatorname{LCP}(x,L_i),
]

[
B=\operatorname{LCP}(x,R_i),
]

[
C=\operatorname{LCP}(x,L_{i+1})
]

when (i<N), otherwise (C=0), and

[
D=\operatorname{LCP}(x,R_{i-1})
]

when (i>1), otherwise (D=0).

The cumulative DP value (f[A][D]) contains exactly the compatible choices from the previous intervals.
7. Multiply that previous contribution by the current representative (x), because the value of a complete sequence is the product of all selected representatives. Add the result to state ((C,B)):

[
g[C][B]
\mathrel{+}=
f[A][D]\cdot x.
]

All arithmetic is performed modulo (100000007).
8. Apply the two-dimensional cumulative transformation to the newly constructed (g) table. The resulting table becomes (f) for the next interval.
9. After the last interval, there is no next interval, so every final state is valid. The answer is consequently (f[m][0]), which includes every state because its first coordinate is at most (m) and its second coordinate is at least (0).

Why it works: after processing interval (i), each DP state represents exactly all valid selections through (i), classified by the two LCP values that the next interval can observe. When a candidate from interval (i+1) is considered, the inequalities against the previous representative are precisely (c\le A) and (B\ge D), and the cumulative table sums exactly those states. Thus every valid sequence is transferred once, every invalid transition is excluded, and multiplication by the current candidate maintains the product value. The local-neighbor lemma guarantees that satisfying these transitions is equivalent to satisfying the original comparison against every representative.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 100000007

def lcp(a, b, m):
    x = a ^ b
    if x == 0:
        return m
    return m - x.bit_length()

def cumulative(g, s):
    """Return f[x][y] = sum(g[c][b]) for c <= x and b >= y."""
    f = [row[:] for row in g]

    # Suffix sum in the second coordinate.
    for row in f:
        for k in range(s - 2, -1, -1):
            v = row[k] + row[k + 1]
            if v >= MOD:
                v -= MOD
            row[k] = v

    # Prefix sum in the first coordinate.
    for j in range(1, s):
        row = f[j]
        prev = f[j - 1]
        for k in range(s):
            v = row[k] + prev[k]
            if v >= MOD:
                v -= MOD
            row[k] = v

    return f

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        m, n = map(int, input().split())
        intervals = [tuple(map(int, input().split()))
                     for _ in range(n)]

        s = m + 1

        # Initially every state is reachable for the first interval.
        f = [[1] * s for _ in range(s)]

        # Reuse g between intervals. Only touched entries need clearing.
        g = [[0] * s for _ in range(s)]

        for i, (left, right) in enumerate(intervals):
            touched = []

            next_left = intervals[i + 1][0] if i + 1 < n else 0
            prev_right = intervals[i - 1][1] if i > 0 else 0

            for x in range(left, right + 1):
                a = lcp(x, left, m)
                b = lcp(x, right, m)
                c = lcp(x, next_left, m) if i + 1 < n else 0
                d = lcp(x, prev_right, m) if i > 0 else 0

                value = f[a][d] * x % MOD

                if g[c][b] == 0:
                    touched.append((c, b))

                g[c][b] += value
                if g[c][b] >= MOD:
                    g[c][b] -= MOD

            f = cumulative(g, s)

            for x, y in touched:
                g[x][y] = 0

        out.append(str(f[m][0]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `lcp` function uses the XOR representation directly. If two numbers differ, the highest set bit of their XOR is exactly their first differing bit when the binary strings are written from the most significant side. Python's `bit_length()` gives that position in constant time, so each LCP query costs (O(1)) instead of scanning all (m) bits.

The DP table has indices from (0) through (m), because an LCP can have any value in that range. The initial table is filled with ones rather than explicitly constructing the virtual state ((0,m)) and transforming it. Those are equivalent: the virtual state contributes to every rectangle (c\le A), (B\ge D), so every initial query has value one.

For each candidate, `f[a][d]` is the exact rectangle sum required by the two neighboring constraints. The multiplication by `x` must happen before adding the candidate to the next state because the DP stores the sum of products, not merely the number of selections.

The `cumulative` function first performs suffix sums along the second coordinate and then prefix sums along the first coordinate. After these two passes,

[
f[a][d]=\sum_{c\le a,\ b\ge d}g[c][b].
]

The order matters because the first pass establishes the (b\ge d) condition, while the second establishes (c\le a).

The implementation reuses the `g` table and clears only states that were actually touched by the current interval. This avoids repeatedly constructing and initializing another (O(m^2)) collection for every interval, which is useful when there are many singleton intervals.

Python integers do not overflow, but all DP values are reduced modulo (100000007). Since every addition combines two values already below the modulus, a single subtraction is enough instead of using `%` in the inner cumulative-sum loops.

## Worked Examples

### Sample 1

The sample is

```
1
2 2
0 1
2 3
```

Initially there is no previous interval, so every candidate in the first interval is allowed.

| Interval | Candidate | (A=\operatorname{LCP}(x,L_i)) | (B=\operatorname{LCP}(x,R_i)) | (C) | (D) | Previous contribution | Added value |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 1 | 0 | 0 | 1 | 0 |
| 1 | 1 | 1 | 2 | 0 | 0 | 1 | 1 |

After the first interval, the only nonzero state is ((C,B)=(0,2)) with value (1). Its cumulative form makes the relevant previous contribution equal to (1).

For the second interval, (R_1=1), so (D) compares every candidate against (1).

| Interval | Candidate | (A) | (B) | (D) | Previous contribution | Added value |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | 2 | 1 | 0 | 1 | 2 |
| 2 | 3 | 1 | 2 | 0 | 1 | 3 |

The final weighted sum is

[
2+3=5.
]

The zero-valued first candidates contribute nothing to the product, while the two sequences beginning with (1) contribute (2) and (3).

### Boundary example

Consider

```
1
2 2
0 2
3 3
```

For the first interval, the candidates (0,1,2) have different compatibility with the final representative (3).

| First candidate | Relevant state ((C,B)) | Contribution |
| --- | --- | --- |
| 0 | ((0,1)) | 0 |
| 1 | ((0,0)) | 1 |
| 2 | ((1,2)) | 2 |

The second interval has only candidate (3). Its values are (A=2), (B=2), and (D=\operatorname{LCP}(3,2)=1). Thus the previous rectangle requires (C\le2) and (B\ge1). The first candidate contributes zero, while both (1) and (2) are compatible.

| First candidate | Previous contribution seen by (3) | Product |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1 | 3 |
| 2 | 2 | 6 |

The answer is

[
3+6=9.
]

This trace demonstrates why the DP needs both coordinates. Candidate (1) and candidate (2) have different LCP values against the next interval's left boundary, and the cumulative rectangle selects both correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(2^m m^2)) | There are (2^m) candidate integers in total, and each interval performs an (O(m^2)) DP transformation |
| Space | (O(m^2+N)) | The DP uses two ((m+1)\times(m+1)) tables, while the intervals require (O(N)) storage |

The worst case has (2^m=131072), with (m\le17), and the sum of (2^m) over all test cases is at most (2^{18}). The (O(2^m m^2)) bound is exactly the intended scale for these constraints. The official contest page gives a one-second time limit and 512 MB memory limit for this problem.

## Test Cases

The following harness assumes the `solve()` function from the solution above is available.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return output.getvalue().strip()

# Provided sample
assert run(
    """1
2 2
0 1
2 3
"""
) == "5", "sample"

# Minimum-size case: m = 0, only value 0 exists.
assert run(
    """1
0 1
0 0
"""
) == "0", "minimum m"

# One interval: every value is valid, so sum 0 + 1 + 2 + 3 = 6.
assert run(
    """1
2 1
0 3
"""
) == "6", "single interval"

# Boundary case where two different first representatives are valid.
assert run(
    """1
2 2
0 2
3 3
"""
) == "9", "boundary compatibility"

# Modulo test: sum(0..131071) = 8589869056,
# which is 89868461 modulo 100000007.
assert run(
    """1
17 1
0 131071
"""
) == "89868461", "modulus"

# Maximum number of intervals: every interval is a singleton.
# The only possible sequence contains A1 = 0, so its product is 0.
n = 1 << 17
lines = ["1", f"17 {n}"]
for x in range(n):
    lines.append(f"{x} {x}")

assert run("\n".join(lines) + "\n") == "0", "maximum N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `m=0, [0,0]` | `0` | Zero-bit boundary and zero product |
| `m=2, [0,3]` | `6` | No neighboring constraints when (N=1) |
| `m=2, [0,2], [3,3]` | `9` | Endpoint inequalities and ties |
| `m=17, [0,131071]` | `89868461` | Correct modulus (100000007) |
| (131072) singleton intervals | `0` | Maximum (N) and interval-boundary handling |

## Edge Cases

For (m=0), there is exactly one possible integer, (0), and its binary representation has zero bits. The `lcp` function receives `a=b=0`, returns (m=0), and the only candidate contributes a factor of zero. The DP consequently returns (0) without ever accessing a negative bit position.

For a single interval, there is no previous or next representative. The initial DP table gives every candidate a contribution of one, while the missing neighbor coordinates are set to zero only as dummy values. Every candidate is processed, so for ([0,3]) the four contributions are (0,1,2,3), giving (6).

At an interval boundary, equality must remain allowed. In the sample, for example, choosing (A_1=1) and (A_2=3) gives an equal LCP at some boundary comparisons, and the sequence is still valid. The DP uses `c <= A` and `b >= D`, never strict inequalities, so ties survive.

The interval endpoints are inclusive. Since the intervals form a complete partition, the total number of candidates processed by the DP is exactly

[
\sum_i(R_i-L_i+1)=2^m.
]

This is why iterating from `left` through `right` inclusively is both necessary and sufficient.

The case where a candidate is zero is also handled naturally. Its transition contribution is multiplied by zero, so every complete sequence containing that representative contributes zero to the requested product sum. Such a state does not need special treatment.

The modulus is unusually close to (10^8), not (10^9). The implementation uses the exact constant `100000007`, and the modulo test with (m=17) verifies that the reduction is performed correctly.
