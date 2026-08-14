---
title: "CF 102396G - Weight Overflow"
description: "We have up to 25 weights, and each weight may be placed on the first plate, the second plate, or left unused. The scale does not compare the ordinary sums. Instead, it reduces both plate sums modulo (m), and reports balance when those two residues are equal."
date: "2026-08-14T14:17:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102396
codeforces_index: "G"
codeforces_contest_name: "2019-2020 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 19)"
rating: 0
weight: 102396
solve_time_s: 196
verified: false
draft: false
---

[CF 102396G - Weight Overflow](https://codeforces.com/problemset/problem/102396/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We have up to 25 weights, and each weight may be placed on the first plate, the second plate, or left unused. The scale does not compare the ordinary sums. Instead, it reduces both plate sums modulo (m), and reports balance when those two residues are equal.

If the first plate contains a set (L) and the second plate contains a disjoint set (R), the required condition is

[
\sum_{i\in L} a_i \equiv \sum_{i\in R} a_i \pmod m.
]

Equivalently,

[
\sum_{i\in L} a_i-\sum_{i\in R}a_i\equiv0\pmod m.
]

So every weight has exactly three possible states. We can encode these states by (0), (+1), and (-1), where (0) means unused, (+1) means the first plate, and (-1) means the second plate. We need a nonzero assignment whose signed sum is divisible by (m).

The bound (n\le25) is the central clue. A direct enumeration has (3^n) states, and (3^{25}=847288609443), which is far beyond what a one-second solution can examine. The modulo (m) can be almost (4\cdot10^7), so a dynamic programming array indexed by every residue would also be too expensive if we processed all weights. The relatively small number of weights suggests splitting them into two halves and enumerating the three choices independently in each half.

The values (a_i) can be as large as (10^9), but only their residues modulo (m) affect the scale. Python integers also avoid overflow, so there is no arithmetic overflow issue in the implementation.

A first edge case is (n=1). For example,

```
1 5
3
```

has no answer, because the only nonempty placement puts weight 3 on one plate and leaves the other empty, giving residues 3 and 0. A careless solution that only checks whether some subset sum is divisible by (m) happens to handle this case, but a solution based on comparing two independently generated subsets must explicitly forbid using the same weight on both sides.

A second edge case occurs when a single weight is already divisible by (m). For example,

```
1 5
10
```

has the valid output

```
1
1
0
```

because the first plate has residue (10\bmod5=0), while the second plate is empty. A careless implementation that requires both plates to contain a weight would reject a valid answer.

A third edge case is (m=1). For example,

```
1 1
7
```

is always solvable because every integer is congruent to zero modulo 1. The algorithm must allow the empty plate and must not accidentally treat the all-unused assignment as a valid answer.

A fourth edge case is that the ordinary sums do not need to be equal. For example,

```
4 14
1 3 7 10
```

can put weights (1,3,10) on one plate. Their ordinary sum is 14, which becomes residue 0, while the other plate is empty. A solution looking only for equal ordinary sums would miss this valid modular equality.

## Approaches

The brute-force approach follows directly from the three possible states of every weight. For every weight, choose unused, first plate, or second plate, compute the resulting signed sum modulo (m), and accept a nonzero assignment whose residue is zero. This is correct because every legal placement corresponds to exactly one of these three-state assignments.

The problem is the number of assignments. With (n=25), there are

[
3^{25}=847288609443
]

possibilities. Even if checking one assignment took only a single constant-time operation, this is much too large for the one-second limit.

The useful observation is that the signed sum is additive. If we divide the weights into two groups, every complete assignment can be written as a signed sum from the first half plus a signed sum from the second half. For a residue (x) produced by the first half, we only need a second-half residue equal to (-x\bmod m).

This is the meet-in-the-middle idea. Instead of exploring all (3^n) assignments, we explore (3^{\lfloor n/2\rfloor}) assignments in one half and (3^{\lceil n/2\rceil}) in the other. For (n=25), these numbers are (3^{12}=531441) and (3^{13}=1594323), which are practical.

There is one detail that makes this formulation especially convenient. We store not only whether a residue exists in the first half, but also one assignment producing that residue. When the second half finds the complementary residue, the two stored assignments together directly describe the two plates.

The all-zero assignment must be treated specially. It always gives residue zero, but putting no weights anywhere is forbidden. If either half contributes a nonzero choice, the combined assignment is valid. Only the case where both stored codes are zero must be rejected.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(3^n)) | (O(n)) | Too slow |
| Optimal | (O(3^{\lceil n/2\rceil})) | (O(3^{\lfloor n/2\rfloor})) | Accepted |

## Algorithm Walkthrough

1. Split the weights into a first half of size (\lfloor n/2\rfloor) and a second half containing the remaining weights. The split is chosen so that the larger enumeration contains only 13 weights at the maximum.
2. Enumerate every assignment of the first half. Each weight has three choices: contribute (0), contribute (+a_i), or contribute (-a_i). Store the resulting residue modulo (m) in a dictionary, together with one encoded assignment that produces it. If several assignments produce the same residue, only one is needed because every one of them is equally useful for completing a solution.
3. Enumerate every assignment of the second half using the same three choices. Suppose its signed sum has residue (s). To make the complete signed sum divisible by (m), the first half must have residue

[
(-s)\bmod m.
]

Look this residue up in the dictionary.

1. When a matching residue is found, decode both assignments. A choice (+1) goes to the first plate, a choice (-1) goes to the second plate, and a choice (0) is ignored.
2. Reject the match only when both assignment codes are zero. In every other case at least one weight is used, and the two half-sums add to zero modulo (m), so the scale is balanced.
3. If the complete enumeration finishes without a match, print (-1). Every possible placement has been represented by a pair of half-assignments, so no solution can have been missed.

Why it works: every legal placement corresponds to a vector of coefficients (c_i\in{-1,0,+1}), where the coefficient indicates the plate or unused state. Splitting the vector into two halves gives residues (x) and (y) satisfying (x+y\equiv0\pmod m) exactly when the placement balances the scale. The first-half dictionary contains one representative for every residue it can produce, and the second-half search checks precisely the complementary residue for every possible second-half assignment. Thus every valid nonempty placement is found, while every reported placement has signed sum divisible by (m).

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = [x % m for x in map(int, input().split())]

    mid = n // 2
    left = a[:mid]
    right = a[mid:]

    # choice encoding:
    # 0 = unused
    # 1 = first plate
    # 2 = second plate
    #
    # Two bits are enough for every choice.
    first = {}

    def build_first(pos, end, residue, code):
        if pos == end:
            first.setdefault(residue, code)
            return

        x = a[pos]

        build_first(pos + 1, end, residue, code)

        nr = residue + x
        if nr >= m:
            nr -= m
        build_first(pos + 1, end, nr, code | (1 << (2 * (pos - 0))))

        nr = residue - x
        if nr < 0:
            nr += m
        build_first(pos + 1, end, nr, code | (2 << (2 * (pos - 0))))

    build_first(0, mid, 0, 0)

    answer = None

    def search_second(pos, end, residue, code):
        nonlocal answer

        if answer is not None:
            return

        if pos == end:
            need = (-residue) % m
            if need in first:
                left_code = first[need]
                if left_code != 0 or code != 0:
                    answer = (left_code, code)
            return

        x = a[pos]

        # Leave the weight unused.
        search_second(pos + 1, end, residue, code)

        if answer is not None:
            return

        # Put it on the first plate.
        nr = residue + x
        if nr >= m:
            nr -= m
        search_second(
            pos + 1,
            end,
            nr,
            code | (1 << (2 * (pos - mid)))
        )

        if answer is not None:
            return

        # Put it on the second plate.
        nr = residue - x
        if nr < 0:
            nr += m
        search_second(
            pos + 1,
            end,
            nr,
            code | (2 << (2 * (pos - mid)))
        )

    search_second(mid, n, 0, 0)

    if answer is None:
        return "-1\n"

    left_code, right_code = answer
    first_plate = []
    second_plate = []

    for i in range(mid):
        choice = (left_code >> (2 * i)) & 3
        if choice == 1:
            first_plate.append(i + 1)
        elif choice == 2:
            second_plate.append(i + 1)

    for i in range(n - mid):
        choice = (right_code >> (2 * i)) & 3
        idx = mid + i + 1
        if choice == 1:
            first_plate.append(idx)
        elif choice == 2:
            second_plate.append(idx)

    out = [
        str(len(first_plate)),
        " ".join(map(str, first_plate)),
        str(len(second_plate)),
        " ".join(map(str, second_plate)),
    ]
    return "\n".join(out) + "\n"

if __name__ == "__main__":
    sys.stdout.write(solve())
```

The first half is stored in a dictionary keyed by residue. `setdefault` keeps the first assignment encountered for a residue and avoids unnecessary replacement. Since only one witness is needed for each residue, this is enough.

The assignment is encoded with two bits per weight. The values 0, 1, and 2 represent unused, first plate, and second plate. Keeping the code as an integer makes the dictionary substantially smaller than storing Python lists or tuples for every state.

The recursion computes residues modulo (m) at every transition. Since the current residue is already in the range (0) through (m-1), adding one residue requires at most one subtraction of (m), and subtracting one requires at most one addition of (m). This avoids the more expensive general `%` operation inside the hottest part of the enumeration.

The two halves use separate local bit positions. When decoding the second half, the indices are shifted by `mid` to recover the original weight numbering. The same local encoding can consequently be used in both halves.

Python does not suffer from the fixed-width integer overflow that would occur in languages using 32-bit integers. The original weights are reduced modulo (m) before enumeration, so every stored residue remains small anyway.

## Worked Examples

For Sample 1,

```
4 14
1 3 7 10
```

the split is ( [1,3] \mid [7,10] ). The first half can produce signed residues such as (0,1,3,4,10,12,\ldots). The second-half search eventually considers putting weight 10 on the first plate, which contributes residue 10. Its complement is (14-10=4), and the first half can produce residue 4 by putting weights 1 and 3 on the first plate.

| Stage | First-half residue | Second-half residue | Required residue | Assignment found |
| --- | --- | --- | --- | --- |
| Initial | 0 | 0 | 0 | all unused, rejected |
| First-half enumeration | 4 | 0 | 0 | weights 1 and 2 produce 4 |
| Second-half search | 4 | 10 | 4 | match found |

The resulting placement is weights 1, 2, and 4 on the first plate and nothing on the second. Their ordinary sum is (1+3+10=14), so the scale sees (0) on both plates modulo 14. This demonstrates that the algorithm is looking for modular equality rather than equality of ordinary sums.

For Sample 2,

```
3 7
1 2 4
```

the split is ( [1]\mid[2,4] ). The first half produces residues (0,1,6). The second half can produce residue 6 by putting both weights 2 and 4 on the first plate. Its required complement is 1, which exists in the first-half dictionary.

| Stage | First-half residue | Second-half residue | Required residue | Assignment found |
| --- | --- | --- | --- | --- |
| Initial | 0 | 0 | 0 | all unused, rejected |
| First-half enumeration | 1 | 0 | 0 | weight 1 produces 1 |
| Second-half enumeration | 1 | 6 | 1 | weights 2 and 3 produce 6 |

The resulting placement puts all three weights on the first plate. Their sum is (1+2+4=7), which is zero modulo 7, while the second plate is empty. This is also a useful example of why the empty second plate is legal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(3^{\lceil n/2\rceil})) | Each half enumerates every ternary assignment, and the larger half has at most 13 weights. |
| Space | (O(3^{\lfloor n/2\rfloor})) | The dictionary stores one assignment for every distinct residue generated by the smaller half. |

At (n=25), the larger half has (3^{13}=1,594,323) assignments and the stored half has at most (3^{12}=531,441) entries. This is exponentially smaller than the (3^{25}) brute-force search and fits comfortably inside the 512 MB memory limit with the compact integer representation used by the implementation.

## Test Cases

The test harness below checks the structural validity of the returned placement rather than requiring a particular valid witness. That is the right way to test this problem because many different outputs can satisfy the same input.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

def check_output(inp: str, out: str) -> bool:
    data = list(map(int, inp.split()))
    n, m = data[0], data[1]
    a = data[2:2 + n]

    tokens = out.split()
    if not tokens:
        return False

    if tokens[0] == "-1":
        return len(tokens) == 1

    p = 0

    k = int(tokens[p])
    p += 1
    left = [int(tokens[p + i]) for i in range(k)]
    p += k

    q = int(tokens[p])
    p += 1
    right = [int(tokens[p + i]) for i in range(q)]
    p += q

    if p != len(tokens):
        return False

    if k + q == 0:
        return False

    if any(x < 1 or x > n for x in left + right):
        return False

    if len(set(left)) != len(left):
        return False
    if len(set(right)) != len(right):
        return False
    if set(left) & set(right):
        return False

    s_left = sum(a[i - 1] for i in left) % m
    s_right = sum(a[i - 1] for i in right) % m

    return s_left == s_right

# Provided sample 1
sample1 = """\
4 14
1 3 7 10
"""
out = run(sample1)
assert check_output(sample1, out), "sample 1"

# Provided sample 2
sample2 = """\
3 7
1 2 4
"""
out = run(sample2)
assert check_output(sample2, out), "sample 2"

# Minimum size, and m = 1.
case1 = """\
1 1
7
"""
out = run(case1)
assert check_output(case1, out), "minimum size"

# Minimum size with no possible answer.
case2 = """\
1 5
3
"""
assert run(case2).strip() == "-1", "single weight with nonzero residue"

# All equal values. One copy can balance another.
case3 = """\
4 10
7 7 7 7
"""
out = run(case3)
assert check_output(case3, out), "all equal values"

# Boundary-style pair: 2 + 3 = 5 modulo 5.
case4 = """\
2 5
2 3
"""
out = run(case4)
assert check_output(case4, out), "modulo boundary"

# Maximum n and a guaranteed no-answer instance.
# The sum of all powers of two is 2^25 - 1 = 33554431,
# which is smaller than m, so every subset has a distinct ordinary sum.
powers = [1 << i for i in range(25)]
case5 = "25 39999999\n" + " ".join(map(str, powers)) + "\n"
assert run(case5).strip() == "-1", "maximum-size no-answer case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7` | Any valid nonempty placement | Minimum (n), modulo 1, and an empty second plate |
| `1 5 / 3` | `-1` | Smallest impossible instance |
| `4 10 / 7 7 7 7` | Any placement with equal nonempty or empty-side residues | All-equal values and duplicate residues |
| `2 5 / 2 3` | One weight on each plate | Exact modulo boundary |
| `25 39999999 / 1 2 4 ... 2^24` | `-1` | Maximum (n), large (m), and a case with no modular collision |

## Edge Cases

For

```
1 5
3
```

the first half is empty and the second half contains weight 3. The first-half dictionary contains only residue 0 with the empty assignment. The second half can produce residues 0, 3, and 2, but only residue 0 has a matching complement. That match would use no weights in either half, so the algorithm rejects it and prints `-1`. This is exactly the required behavior.

For

```
1 5
10
```

the only weight has residue 0. The first-half dictionary again contains residue 0, while the second-half assignment that puts weight 1 on the first plate also has residue 0. The two assignment codes are not both zero, so the match is accepted. The output places weight 1 on the first plate and leaves the second plate empty.

For

```
1 1
7
```

every residue is zero because the modulus is 1. The second-half enumeration immediately finds a nonempty assignment with residue zero, and the first-half empty assignment supplies the required complement. The resulting placement is valid because every plate sum is congruent to zero modulo 1.

For

```
4 14
1 3 7 10
```

the first half can produce signed residue 4 from weights 1 and 2 placed on the first plate. The second-half assignment placing weight 4 on the first plate contributes residue 10. Since (4+10=14), their combined signed residue is zero. The output can consequently place weights 1, 2, and 4 on the first plate, giving a modular sum of zero, with the second plate empty.

For the maximum-size no-answer case

```
25 39999999
1 2 4 8 16 32 64 128 256 512 1024 2048 4096
8192 16384 32768 65536 131072 262144 524288 1048576
2097152 4194304 8388608 16777216
```

the total of all weights is (2^{25}-1=33554431), which is smaller than (m). Every subset consequently has a different ordinary sum, so two disjoint subsets cannot have equal sums unless both are empty. Since the total never reaches (m), there is also no nonempty subset whose sum is divisible by (m). The meet-in-the-middle search exhausts all three-state assignments and correctly returns `-1`.
