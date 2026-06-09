---
title: "CF 1613A - Long Comparison"
description: "Each number in this problem is not given in its expanded form, but as a compact description. Instead of writing the full integer, we are given a base value x and a number of trailing zeros p, meaning the actual number is x × 10^p."
date: "2026-06-10T06:53:37+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1613
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 118 (Rated for Div. 2)"
rating: 900
weight: 1613
solve_time_s: 79
verified: true
draft: false
---

[CF 1613A - Long Comparison](https://codeforces.com/problemset/problem/1613/A)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

Each number in this problem is not given in its expanded form, but as a compact description. Instead of writing the full integer, we are given a base value `x` and a number of trailing zeros `p`, meaning the actual number is `x × 10^p`.

So every test case gives two such “decimal-shifted” numbers. The task is simply to determine which of the two resulting integers is larger, or whether they are equal.

The key difficulty is that `p` can be as large as 10^6. That makes constructing the actual number impossible, since writing down 10^6 digits is already far beyond memory and time constraints. The comparison must be done purely from the structure of the numbers.

The constraints allow up to 10^4 test cases. Any solution that tries to explicitly build or simulate full numbers would immediately fail due to both time and memory blowups. Even string-based construction would be infeasible because a single test case can demand up to a million digits.

A subtle edge case appears when the base numbers are small but exponents differ. For example, comparing `1 × 10^5` and `10 × 10^4` looks like comparing `100000` and `100000`, which are equal, even though the base values differ. A naive approach that compares `(x, p)` lexicographically would incorrectly conclude that `10 × 10^4` is larger because `10 > 1`.

Another failure case arises when one number’s exponent dominates the other’s magnitude entirely, for example `999 × 10^0` versus `1 × 10^3`. The correct answer depends entirely on digit length after expansion, not on base magnitude.

The comparison must therefore simulate arithmetic magnitude without constructing numbers.

## Approaches

A direct brute-force method would construct the full integer representation of each number by appending `p` zeros to the decimal string of `x`, then compare the resulting strings numerically. This is conceptually straightforward and correct because it mirrors the actual numbers.

However, in the worst case, each number can have up to 10^6 digits. With up to 10^4 test cases, this leads to a theoretical output size on the order of 10^10 characters. Even ignoring memory limits, simply writing or comparing these strings would be far beyond time constraints.

The key observation is that trailing zeros only affect the scale of the number, not its internal digit structure. The only meaningful comparison comes from total digit length after expansion. If two numbers have different effective lengths, the longer one is larger immediately. If they have the same length, the comparison reduces to comparing their significant prefixes digit by digit, because the trailing zeros align perfectly.

This reduces the problem to balancing digit lengths and then comparing normalized representations of equal length numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (build full numbers) | O(sum of 10^p digits) | O(sum of 10^p) | Too slow |
| Optimal (length + normalization) | O(t · log x) | O(1) | Accepted |

## Algorithm Walkthrough

We treat each number as having two components: a significant part `x` and a magnitude shift `p`.

1. Compute the effective length of each number as `len(str(x)) + p`.

This represents how many digits the full expanded number would have without constructing it.
2. If the two lengths differ, the number with the larger length is automatically greater.

This follows directly from the fact that adding more trailing zeros always increases magnitude by orders of ten.
3. If the lengths are equal, we cannot decide from length alone. In this case, we compare digit by digit as if both numbers were fully expanded.
4. To compare without expansion, we conceptually align both numbers:

the larger exponent contributes extra trailing zeros to the smaller base, so we effectively compare `x1 × 10^(p1 - p2)` and `x2 × 10^(p2 - p1)` depending on which exponent is larger.
5. We simulate this by padding the smaller representation logically with zeros and comparing only the overlapping significant portions.
6. The comparison is performed as string comparison of the constructed aligned representations, but without actually materializing full strings.

### Why it works

Every number is of the form `x × 10^p`, which is equivalent to shifting the decimal representation of `x` to the left by `p` positions. The magnitude of a number in base 10 is determined first by digit count, and only then by lexicographic comparison of digits when lengths match.

By separating each number into “length class” and “aligned digit sequence”, we preserve the exact ordering of real integers. No transformation changes the relative order because multiplication by powers of 10 only affects digit positioning, not digit values.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
out = []

for _ in range(t):
    x1, p1 = map(int, input().split())
    x2, p2 = map(int, input().split())

    s1 = str(x1)
    s2 = str(x2)

    len1 = len(s1) + p1
    len2 = len(s2) + p2

    if len1 > len2:
        out.append(">")
        continue
    if len1 < len2:
        out.append("<")
        continue

    # same length case: compare digit by digit
    i = 0
    j = 0
    zero1 = p1
    zero2 = p2

    while i < len(s1) or j < len(s2):
        d1 = int(s1[i]) if i < len(s1) else 0
        d2 = int(s2[j]) if j < len(s2) else 0

        if d1 != d2:
            out.append(">" if d1 > d2 else "<")
            break

        i += 1
        j += 1
    else:
        out.append("=")

sys.stdout.write("\n".join(out))
```

The implementation begins by converting each base number into a string so digit access is efficient. It first compares total effective lengths, which resolves most cases immediately.

When lengths match, the code performs a synchronized digit comparison. Once one string runs out of digits, it implicitly treats missing positions as zero, which corresponds exactly to the effect of trailing zeros in the original number.

A subtle point is that we never explicitly construct padded strings. Instead, we simulate padding by treating out-of-range positions as zeros during comparison. This avoids any risk of memory overflow while preserving correctness.

## Worked Examples

Consider the sample pair `(2, 1)` and `(19, 0)`.

We compare effective lengths: `2 × 10^1` has length 2, while `19 × 10^0` also has length 2. Since lengths are equal, we compare digit by digit.

| Step | s1 digit | s2 digit | Decision |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 2 > 1 → first is larger |

So output is `>`.

Now consider `(10, 2)` and `(100, 1)`.

Effective lengths: both are 3 digits.

| Step | s1 digit | s2 digit | Decision |
| --- | --- | --- | --- |
| 1 | 1 | 1 | equal |
| 2 | 0 | 0 | equal |
| 3 | 0 | 0 | equal |

All digits match, so result is `=`.

These examples show that the algorithm first uses structural dominance (length) and only falls back to digit alignment when necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · log x) | Each test processes digit strings of size up to 6 |
| Space | O(1) | Only constant extra space beyond output storage |

The algorithm is efficient because it avoids any dependence on `p`, which can be extremely large. All operations are bounded by the number of digits in `x`, which is small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        x1, p1 = map(int, input().split())
        x2, p2 = map(int, input().split())

        s1 = str(x1)
        s2 = str(x2)

        len1 = len(s1) + p1
        len2 = len(s2) + p2

        if len1 > len2:
            out.append(">")
        elif len1 < len2:
            out.append("<")
        else:
            i = j = 0
            while i < len(s1) or j < len(s2):
                d1 = int(s1[i]) if i < len(s1) else 0
                d2 = int(s2[j]) if j < len(s2) else 0
                if d1 != d2:
                    out.append(">" if d1 > d2 else "<")
                    break
                i += 1
                j += 1
            else:
                out.append("=")

    return "\n".join(out)

# provided sample
assert run("""5
2 1
19 0
10 2
100 1
1999 0
2 3
1 0
1 0
99 0
1 2
""") == """>\n=\n<\n=\n<"""

# edge: equal expansion
assert run("""1
1 3
1000 0
""") == "="

# edge: exponent dominates
assert run("""1
1 5
999 0
""") == ">"""

# edge: same x different p
assert run("""1
10 1
10 2
""") == "<"""

# edge: large equal structure
assert run("""1
123 2
12300 0
""") == "="
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 vs 1000 0` | `=` | Equalized magnitude via trailing zeros |
| `1 5 vs 999 0` | `>` | Length dominance from exponent |
| `10 1 vs 10 2` | `<` | Effect of extra trailing zero |
| `123 2 vs 12300 0` | `=` | Exact structural equivalence |

## Edge Cases

One edge case is when one number becomes significantly longer due to trailing zeros, even though its base is small. For input `1 5` and `999 0`, the first number becomes 100000 while the second remains 999. The algorithm immediately compares lengths, finds the first is longer, and outputs `>` without inspecting digits.

Another edge case occurs when both numbers end up with identical effective lengths but require digit alignment. For `10 2` and `100 1`, both expand to three digits. The algorithm compares digit by digit and finds equality at every position, correctly outputting `=`.

A third case involves identical base values with different exponents, such as `10 1` and `10 2`. The effective lengths differ, so the comparison is resolved immediately without digit inspection, correctly reflecting that adding a trailing zero increases magnitude.
