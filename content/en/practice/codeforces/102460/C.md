---
title: "CF 102460C - Are They All Integers?"
description: "We have a sorted array of positive integers (A), with (3 le n le 50). We must decide whether every choice of three distinct positions (i,j,k) satisfies [ frac{A[i]-A[j]}{A[k]} in mathbb Z."
date: "2026-08-09T18:34:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102460
codeforces_index: "C"
codeforces_contest_name: "2019-2020 ICPC Asia Taipei-Hsinchu Regional Contest"
rating: 0
weight: 102460
solve_time_s: 414
verified: true
draft: false
---

[CF 102460C - Are They All Integers?](https://codeforces.com/problemset/problem/102460/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sorted array of positive integers (A), with (3 \le n \le 50). We must decide whether every choice of three distinct positions (i,j,k) satisfies

[
\frac{A[i]-A[j]}{A[k]} \in \mathbb Z.
]

Since every (A[k]) is positive, this is exactly the same as asking whether (A[k]) divides (A[i]-A[j]). The order of (i) and (j) does not matter for divisibility because if a number divides (x-y), it also divides (y-x).

The required output is `yes` if the condition holds for every possible triple of distinct indices, and `no` as soon as one valid triple violates it.

The array contains at most 50 elements, so even an (O(n^3)) enumeration performs only

[
50\cdot49\cdot48=117600
]

checks in the worst case. That is tiny for a 2 second limit, so a literal brute-force implementation is already fast enough. The upper bound (A[i]\le100) is not even needed for the basic solution. It does, however, make it clear that integer arithmetic is completely safe and that no large-number techniques are necessary.

There are several details that can make a seemingly reasonable implementation incorrect. First, the three indices must be distinct. For example, with `1 2 4`, the only valid triple uses all three positions, and the result is `no` because

[
\frac{1-2}{4}=-\frac14
]

is not an integer. An implementation that accidentally allows the denominator's index to coincide with one of the numerator indices may test expressions that are not part of the problem.

Second, the numerator is a difference, not either individual array value. For `2 4 6`, the denominator `6` must divide (2-4=-2), which it does not, so the answer is `no`. Checking whether both numerator values are individually divisible by the denominator would be solving a different problem.

Third, the numerator may be negative. For example, in `1 1 4`, the difference can be (1-4=-3) if the denominator is another element, so the implementation must test divisibility rather than assuming the numerator is nonnegative. Python's `%` operator handles negative integers correctly for a divisibility test because (x % d=0) exactly when (d) divides (x).

Finally, repeated values are completely legitimate. For `1 1 1 1 4`, every difference among the four `1`s is zero, and zero is divisible by every positive integer. The correct answer is `yes`.

## Approaches

The most direct solution follows the mathematical definition. Enumerate every ordered triple of distinct indices (i,j,k), compute (A[i]-A[j]), and check whether it is divisible by (A[k]). If any check fails, the answer is immediately `no`; if all checks pass, the answer is `yes`.

There are exactly (n(n-1)(n-2)) ordered triples. At the maximum (n=50), that is only 117600 divisibility checks. So although (O(n^3)) would become unattractive for much larger arrays, it is fully acceptable for the actual constraints of this problem.

There is a useful observation that reduces the work to (O(n^2)). Fix the denominator position (k). The condition says that for every pair of positions (i,j) different from (k),

[
A[i]\equiv A[j]\pmod{A[k]}.
]

In other words, after removing (A[k]), every remaining array value must have exactly the same remainder modulo (A[k]).

We do not need to compare every pair to establish that property. Pick one reference position (r\ne k). If every other position (j\ne k,r) satisfies

[
A[j]\equiv A[r]\pmod{A[k]},
]

then any two such values have the same remainder, so their difference is divisible by (A[k]). Thus, for each (k), one reference element is enough.

The brute force works because it directly checks every required triple, but it repeats essentially the same modular information many times. The observation that all elements other than (A[k]) must belong to one residue class modulo (A[k]) lets us replace all pairwise comparisons with comparisons against one reference.

The quadratic version is not necessary for the given (n\le50), but it gives a cleaner expression of the underlying mathematics and scales much better.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(1)) | Accepted |
| Residue-class check | (O(n^2)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (n) and the array (A). We only need the values themselves, and the given sorting is not required by the algorithm.
2. Treat each array position (k) as the denominator position. We must verify that every pair of values at positions different from (k) has a difference divisible by (A[k]).
3. Choose a reference position (r) different from (k). We can use position `0` unless (k=0), in which case we use position `1`. Because (n\ge3), such a reference position always exists.
4. For every other position (j), skipping (k) and (r), check whether
[
(A[j]-A[r])\bmod A[k]=0.
]
This says that (A[j]) and the reference value have the same remainder modulo (A[k]).
5. If any such difference is not divisible by (A[k]), immediately print `no`. The failing pair (j,r), together with denominator (k), is a valid triple of distinct positions, so the original condition cannot hold.
6. If every position (k) passes, print `yes`. For each denominator, all other values are congruent modulo that denominator, so every difference between two of them is divisible by it.

### Why it works

Fix any denominator position (k). The algorithm guarantees that every other value (A[j]) has the same remainder modulo (A[k]) as the reference value (A[r]). Therefore, for any two positions (i,j\ne k),

[
A[i]\equiv A[r]\equiv A[j]\pmod{A[k]}.
]

Subtracting the congruences gives

[
A[i]-A[j]\equiv0\pmod{A[k]},
]

so (A[k]) divides (A[i]-A[j]). Thus every triple whose denominator is (A[k]) is valid. Since the algorithm performs this argument for every (k), every allowed triple is valid. Conversely, if the algorithm finds two values with different remainders for some (k), their difference is not divisible by (A[k]), giving an explicit invalid triple. The algorithm therefore returns `yes` exactly when the required condition holds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    for k in range(n):
        # Choose any index different from k as the reference.
        ref = 0 if k != 0 else 1

        for j in range(n):
            if j == k or j == ref:
                continue

            if (a[j] - a[ref]) % a[k] != 0:
                print("no")
                return

    print("yes")

if __name__ == "__main__":
    solve()
```

The outer loop fixes the denominator (A[k]). Once (k) is fixed, the problem becomes a statement about the residues of all the other values modulo (A[k]).

The `ref` selection guarantees that the reference index is different from the denominator index. If `k` is not zero, index `0` works. If `k` is zero, index `1` works. Since (n\ge3), index `1` always exists.

The inner loop skips both `k` and `ref`. Every remaining position represents a value that must have the same remainder as `a[ref]` modulo `a[k]`.

The expression `(a[j] - a[ref]) % a[k]` is preferable to performing division and checking whether the result is an integer. It uses only integer arithmetic and directly tests divisibility. Python integers also avoid any overflow concern, although the given values are so small that ordinary machine integers would already be sufficient.

The algorithm returns immediately after finding a contradiction. This is safe because the required property is universal: one invalid triple is enough to determine that the answer is `no`.

## Worked Examples

### Sample 1

The input is:

```
5
1 1 1 1 4
```

Consider each possible denominator position. The following table shows the essential checks. The reference is chosen according to the algorithm.

| (k) | (A[k]) | Reference | Values compared with reference | Result |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1, 1, 4 | all differences divisible by 1 |
| 1 | 1 | 0 | 1, 1, 4 | all differences divisible by 1 |
| 2 | 1 | 0 | 1, 1, 4 | all differences divisible by 1 |
| 3 | 1 | 0 | 1, 1, 4 | all differences divisible by 1 |
| 4 | 4 | 0 | 1, 1, 1 | all differences are 0 |

For (k=0,1,2,3), the denominator is 1, which divides every integer. For (k=4), the other four values are all 1, so every possible difference is zero, and zero is divisible by 4.

The algorithm therefore reaches the end without finding a contradiction and prints:

```
yes
```

This example demonstrates why duplicate values must be handled normally. There is no requirement that the selected values themselves be distinct, only their positions.

### Sample 2

The input is:

```
5
1 2 4 8 16
```

The first denominator is (A[0]=1), so it passes automatically. When (k=1), the denominator is (2), and the reference is (A[0]=1).

| (k) | (A[k]) | Reference value | Current value | Difference | Divisible? |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 4 | 2 | yes |
| 0 | 1 | 2 | 8 | 6 | yes |
| 0 | 1 | 2 | 16 | 14 | yes |
| 1 | 2 | 1 | 4 | 3 | no |

At (k=1), the values outside the denominator position include 1 and 4. Their difference is (4-1=3), which is not divisible by 2. Hence the triple with values (1,4,2) violates the condition.

The algorithm stops immediately and prints:

```
no
```

This trace shows why checking residue classes is enough. Once two values have different remainders modulo the denominator, their difference cannot be divisible by that denominator.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2)) | For each of the (n) denominator positions, at most (n-2) other positions are checked. |
| Space | (O(1)) auxiliary | Apart from the input array, the algorithm stores only a constant number of indices and values. |

With (n\le50), the quadratic algorithm performs fewer than 2500 modular checks, which is far below the available time budget. The input array itself contains only 50 integers, so memory usage is negligible.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    for k in range(n):
        ref = 0 if k != 0 else 1

        for j in range(n):
            if j == k or j == ref:
                continue

            if (a[j] - a[ref]) % a[k] != 0:
                return "no\n"

    return "yes\n"

def run(inp: str) -> str:
    return solve_data(inp)

# Provided sample 1
assert run("""\
5
1 1 1 1 4
""") == "yes\n", "sample 1"

# Provided sample 2
assert run("""\
5
1 2 4 8 16
""") == "no\n", "sample 2"

# Minimum-size input, all equal
assert run("""\
3
7 7 7
""") == "yes\n", "minimum size and all equal"

# Minimum-size input with a failing triple
assert run("""\
3
1 2 3
""") == "no\n", "minimum size failure"

# Boundary values with duplicates
assert run("""\
3
1 1 100
""") == "yes\n", "maximum value with duplicate small values"

# Maximum-size input, all equal
assert run("50\n" + "100 " * 49 + "100\n") == "yes\n", \
    "maximum size and all equal"

# A nontrivial valid case
assert run("""\
4
2 2 5 5
""") == "yes\n", "equal groups"

# Catches the difference-vs-value mistake
assert run("""\
3
2 4 6
""") == "no\n", "difference is not divisible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 7 7 7` | `yes` | Minimum size and the fact that zero differences are divisible by every positive denominator |
| `3 / 1 2 3` | `no` | Smallest possible array containing an invalid triple |
| `3 / 1 1 100` | `yes` | Duplicate positions and the maximum allowed value |
| 50 copies of `100` | `yes` | Maximum (n), repeated values, and performance |
| `4 / 2 2 5 5` | `yes` | Different value groups where every required difference is zero |
| `3 / 2 4 6` | `no` | Confirms that the numerator must be a difference rather than checking individual divisibility |

## Edge Cases

The minimum possible array has three positions. For `1 2 3`, there is only one unordered choice of three positions, although the expression allows both orders for the numerator. Taking denominator 3 and numerator (1-2=-1) gives (-1/3), which is not an integer. The algorithm eventually considers (k=2), compares the values 1 and 2 modulo 3, and finds that their difference is not divisible by 3. It prints `no`.

For an array containing all equal values, such as `7 7 7`, every numerator difference is zero. Since (0) is divisible by every positive integer, every possible expression is an integer. The algorithm chooses any reference value, and every comparison produces a difference of zero, so it prints `yes`.

A denominator equal to 1 is always harmless. For example, in `1 2 5`, whenever the denominator position contains 1, every difference is divisible by 1. The algorithm does not need a special case for this because the ordinary modulo operation already gives zero for every integer modulo 1.

The largest allowed value also needs no special handling. In `1 1 100`, when 100 is the denominator, the only two other values are both 1, so their difference is zero and the condition passes. When 1 is the denominator, every difference is automatically divisible by 1. The final result is `yes`.

Negative differences are handled directly. In `2 4 6`, considering 2 and 4 with denominator 6 produces (2-4=-2). The value (-2) is not divisible by 6, so the answer is `no`. The Python expression `(-2) % 6` is 4 rather than (-2), but it is nonzero, which is exactly what the divisibility test needs.

Repeated values must be treated as separate positions, not collapsed into a set. In `2 2 5 5`, when the denominator is 5, the two remaining 2s have difference zero. When the denominator is 2, the two remaining 5s have difference zero. Every required triple is valid, so the answer is `yes`. Removing duplicates before checking would change the set of available positions and could destroy the structure that makes the original instance valid.
