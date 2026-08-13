---
title: "CF 102367A - Cake Distribution"
description: "We need to cut one cake into a small number of integer-weight pieces. The number of guests is not known in advance: it will be exactly (A), (B), or (C)."
date: "2026-08-14T02:59:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102367
codeforces_index: "A"
codeforces_contest_name: "Fall 2019 ICPC-style Waterloo Local Contest"
rating: 0
weight: 102367
solve_time_s: 82
verified: true
draft: false
---

[CF 102367A - Cake Distribution](https://codeforces.com/problemset/problem/102367/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to cut one cake into a small number of integer-weight pieces. The number of guests is not known in advance: it will be exactly (A), (B), or (C). For each of those three possibilities, every piece must have a predetermined recipient, and after distributing all pieces, every guest must receive exactly the same total weight.

The output describes each physical piece by four numbers. The first is its weight. The other three numbers say who receives that piece when there are (A), (B), or (C) guests. The same physical piece can be assigned to different people in the three scenarios.

The cake itself may have any total weight from (1) through (10^{18}), so we are free to choose a convenient total. The three guest counts are at most (1000). That makes a construction with (O(A+B+C)) pieces entirely practical, while a construction with up to (10^9) pieces is not. The limit of 5000 pieces is the key constraint that tells us to search for a compressed representation rather than constructing one piece per gram.

A useful edge case is (A=B=C=1). The correct output can simply contain one piece of weight 1 assigned to person 1 in all three scenarios. A careless construction based on internal boundaries might accidentally create zero-weight pieces if it does not remove duplicate boundaries.

For example, with input `1 1 1`, the only boundary is 0 and the final boundary is 1. There is exactly one interval, so the output is `1` followed by `1 1 1 1`. Treating the three sets of boundaries as separate arrays without deduplication could incorrectly count the same interval several times.

Another boundary case is `1 2 3`. The least common multiple is 6. The three equal-share boundaries are at 0 and 6 for one guest, 0, 3, 6 for two guests, and 0, 2, 4, 6 for three guests. Their union is `0, 2, 3, 4, 6`, producing four pieces. The sample output is one valid realization of exactly those four intervals. A careless implementation that uses floating-point division can also misidentify boundaries for large values, so every boundary must be computed with integer arithmetic.

Finally, the maximum input values are still harmless for the chosen construction. Since (\operatorname{lcm}(A,B,C)) divides (ABC), the cake can always be chosen with weight at most (1000^3=10^9), far below (10^{18}). The number of distinct internal boundaries is at most ((A-1)+(B-1)+(C-1)), so the number of pieces is at most (A+B+C-2), which is at most 2998. Thus the 5000-piece limit has substantial room to spare.

## Approaches

A straightforward construction is to choose the cake weight as (L=\operatorname{lcm}(A,B,C)) and make every gram a separate piece. There are (L) unit pieces. For the (A)-guest scenario, assign (L/A) consecutive unit pieces to each guest. Do the analogous thing for (B) and (C). This is correct because (L) is divisible by all three guest counts, so every guest receives exactly (L/A), (L/B), or (L/C) grams respectively.

The problem is the number of pieces. In the worst case (L) can be close to (10^9). For example, (A=997), (B=998), and (C=999) have least common multiple (994010994). A unit-piece construction would consequently need 994010994 output lines, far beyond the limit of 5000 and far beyond what can be processed in one second.

The key observation is that we do not actually need a separate piece for every gram. For a fixed guest count, imagine the cake as a continuous interval from 0 to (L). If there are (A) guests, guest 1 needs the interval from 0 to (L/A), guest 2 needs the next interval, and so on. The only places where the recipient can change are the boundaries

[
0,\frac{L}{A},\frac{2L}{A},\ldots,L.
]

Do the same for (B) and (C). Now take the union of all these boundaries and cut the cake only there.

Every resulting piece lies entirely inside one (A)-guest interval, one (B)-guest interval, and one (C)-guest interval. We can consequently assign the whole piece to the corresponding recipient in each scenario. The pieces are exactly the common refinement of the three equal partitions.

There are at most (A-1), (B-1), and (C-1) internal boundaries, so after taking their union there are at most (A+B+C-2) internal cuts and at most (A+B+C-1) pieces. With all three values at most 1000, this is at most 2999 pieces.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(\operatorname{lcm}(A,B,C))) | (O(\operatorname{lcm}(A,B,C))) | Too slow |
| Optimal | (O((A+B+C)\log(A+B+C))) | (O(A+B+C)) | Accepted |

## Algorithm Walkthrough

1. Compute (L=\operatorname{lcm}(A,B,C)). This gives a cake whose total weight can be divided equally among any of the three possible guest counts.
2. Create a set containing 0 and (L). These are the two ends of the cake.
3. For every integer (i) from 1 through (A-1), insert (i(L/A)) into the set. These are exactly the places where the recipient changes when there are (A) guests.
4. Repeat the same process for (B) and (C), inserting (i(L/B)) and (i(L/C)). Since (L) is divisible by all three values, every boundary is an integer.
5. Sort the resulting set of boundaries. Consecutive values (x<y) define one physical cake piece with weight (y-x). Duplicate boundaries have already been removed by the set, so every weight is positive.
6. For each interval starting at (x), compute its recipient under each scenario. With (A) guests, the interval containing (x) belongs to guest

[
\left\lfloor\frac{x}{L/A}\right\rfloor+1.
]

The corresponding formulas for (B) and (C) give the other two recipients. Because (x) is itself a boundary from the union, the interval cannot cross another boundary belonging to any scenario.
7. Output every piece as its weight followed by the three recipient indices. The total weight is exactly (L), and the number of pieces is below 5000.

### Why it works

The invariant is that every generated piece lies completely inside one equal-share interval for each of the three possible guest counts. Consider the (A)-guest partition. Its boundaries are all included in our global boundary set, so no generated piece can cross an (A)-guest boundary. Every piece therefore belongs to exactly one (A)-guest interval, and we assign it to that interval's guest. Since those intervals each have weight (L/A), every one of the (A) guests receives exactly (L/A) grams. The same argument applies independently to (B) and (C). The pieces are positive because they are formed from distinct sorted boundaries, and their total weight telescopes to (L).

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def lcm(a, b):
    return a // gcd(a, b) * b

def solve():
    A, B, C = map(int, input().split())

    L = lcm(lcm(A, B), C)

    cuts = {0, L}

    part_a = L // A
    part_b = L // B
    part_c = L // C

    for i in range(1, A):
        cuts.add(i * part_a)

    for i in range(1, B):
        cuts.add(i * part_b)

    for i in range(1, C):
        cuts.add(i * part_c)

    cuts = sorted(cuts)

    ans = []

    for i in range(len(cuts) - 1):
        left = cuts[i]
        right = cuts[i + 1]
        weight = right - left

        a = left // part_a + 1
        b = left // part_b + 1
        c = left // part_c + 1

        ans.append((weight, a, b, c))

    out = [str(len(ans))]
    out.extend(f"{w} {a} {b} {c}" for w, a, b, c in ans)
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first section computes the common cake weight. The nested `lcm` calls are safe because Python integers have arbitrary precision, although in this problem the resulting value is already below (10^9).

The three `part_*` variables are the exact weight each guest must receive. They also serve as the widths of the equal intervals in the three possible scenarios.

The `cuts` set is the central part of the construction. Every possible place where a recipient changes is inserted exactly once. Using a set matters because the same boundary can occur in several partitions. For example, when (A=2) and (B=4), the midpoint (L/2) is also the boundary after two of the four (B)-guest intervals.

After sorting, consecutive cuts describe actual pieces. The expression `right - left` is always positive because duplicate cuts have been removed.

The recipient calculation uses integer division rather than floating point. If `left` lies in the (j)-th interval of the (A)-partition, then `left // part_a` is (j-1), so adding one converts the zero-based interval number into the required one-based person index.

There is no overflow concern in Python. In languages with fixed-width integers, a 64-bit integer is sufficient because the problem explicitly permits totals up to (10^{18}), and the construction here is much smaller than that.

## Worked Examples

### Sample 1

For input `1 2 3`, the common cake weight is

[
L=\operatorname{lcm}(1,2,3)=6.
]

The three partition widths are 6, 3, and 2.

| left | right | weight | A recipient | B recipient | C recipient |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 2 | 1 | 1 | 1 |
| 2 | 3 | 1 | 1 | 1 | 2 |
| 3 | 4 | 1 | 1 | 2 | 2 |
| 4 | 6 | 2 | 1 | 2 | 3 |

For one guest, that person receives all six grams. For two guests, person 1 receives the first two pieces for a total of three grams, while person 2 receives the last two pieces for three grams. For three guests, the three groups have weights two, two, and two.

The trace also demonstrates why the global boundaries are sufficient. No interval crosses any boundary from any of the three partitions.

### Custom trace: `2 3 4`

Here

[
L=\operatorname{lcm}(2,3,4)=12.
]

The partition widths are 6, 4, and 3. Their union of boundaries is `0, 3, 4, 6, 8, 9, 12`.

| left | right | weight | A recipient | B recipient | C recipient |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 3 | 1 | 1 | 1 |
| 3 | 4 | 1 | 1 | 1 | 2 |
| 4 | 6 | 2 | 1 | 2 | 2 |
| 6 | 8 | 2 | 2 | 2 | 3 |
| 8 | 9 | 1 | 2 | 3 | 3 |
| 9 | 12 | 3 | 2 | 3 | 4 |

For two guests, the first three pieces total (3+1+2=6), and the last three total (2+1+3=6). For three guests, the totals are (4), (4), and (4). For four guests, the totals are (3), (3), (3), and (3).

The example demonstrates that the physical pieces do not need to form equal-size pieces. Their sizes only need to align with the boundaries of every possible equal partition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((A+B+C)\log(A+B+C))) | At most (A+B+C-1) boundaries are inserted and sorted |
| Space | (O(A+B+C)) | The boundary set and output contain (O(A+B+C)) elements |

Since (A,B,C\le1000), fewer than 3000 pieces are produced. The construction performs only a few thousand arithmetic operations and one small sort, so it is easily within the stated 1 second time limit and 256 MB memory limit.

## Test Cases

The exact textual output of a constructive problem is not uniquely determined by the problem. The following tests use the deterministic implementation above, then validate the structural conditions that every accepted output must satisfy.

```python
import sys
import io
from math import gcd

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        A, B, C = map(int, sys.stdin.readline().split())

        def lcm(a, b):
            return a // gcd(a, b) * b

        L = lcm(lcm(A, B), C)

        cuts = {0, L}
        pa = L // A
        pb = L // B
        pc = L // C

        for i in range(1, A):
            cuts.add(i * pa)
        for i in range(1, B):
            cuts.add(i * pb)
        for i in range(1, C):
            cuts.add(i * pc)

        cuts = sorted(cuts)

        ans = []
        for i in range(len(cuts) - 1):
            x = cuts[i]
            y = cuts[i + 1]
            ans.append((
                y - x,
                x // pa + 1,
                x // pb + 1,
                x // pc + 1
            ))

        out = [str(len(ans))]
        out.extend(f"{w} {a} {b} {c}" for w, a, b, c in ans)
        return "\n".join(out)
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, output: str):
    A, B, C = map(int, inp.split())
    lines = output.strip().splitlines()

    K = int(lines[0])
    assert K == len(lines) - 1
    assert 1 <= K <= 5000

    pieces = []
    total = 0

    for line in lines[1:]:
        w, a, b, c = map(int, line.split())
        assert w > 0
        assert 1 <= a <= A
        assert 1 <= b <= B
        assert 1 <= c <= C
        pieces.append((w, a, b, c))
        total += w

    assert 1 <= total <= 10**18

    for count, column in ((A, 1), (B, 2), (C, 3)):
        sums = [0] * (count + 1)

        for w, a, b, c in pieces:
            person = (a, b, c)[column - 1]
            sums[person] += w

        assert len(set(sums[1:])) == 1

def run(inp: str) -> str:
    out = solve_data(inp)
    validate(inp, out)
    return out

# Provided sample
sample = run("1 2 3")
assert sample == (
    "4\n"
    "2 1 1 1\n"
    "1 1 1 2\n"
    "1 1 2 2\n"
    "2 1 2 3"
), "sample 1"

# Minimum-size input
out = run("1 1 1")
assert out == "1\n1 1 1 1", "minimum case"

# All values equal
out = run("7 7 7")
assert out == "7\n" + "\n".join(
    f"1 {i} {i} {i}" for i in range(1, 8)
), "all equal"

# Boundary-heavy case
out = run("2 3 4")
assert out == (
    "6\n"
    "3 1 1 1\n"
    "1 1 1 2\n"
    "2 1 2 2\n"
    "2 2 2 3\n"
    "1 2 3 3\n"
    "3 2 3 4"
), "boundary case"

# Maximum values
out = run("1000 999 997")
validate("1000 999 997", out)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3` | Four pieces matching the sample | Provided sample and overlapping partition boundaries |
| `1 1 1` | One piece of weight 1 | Duplicate boundaries and minimum values |
| `7 7 7` | Seven unit pieces, each assigned to the same index in all scenarios | All three partitions coincide |
| `2 3 4` | Six pieces with boundaries at 0, 3, 4, 6, 8, 9, 12 | Several different boundary alignments |
| `1000 999 997` | Any output satisfying the validator | Large input values and the piece-count bound |

## Edge Cases

For `1 1 1`, the least common multiple is 1 and all three loops that generate internal boundaries are empty. The boundary set is simply `{0, 1}`. The only interval has weight 1, and all three recipient indices are 1. The algorithm cannot create a zero-weight piece because it sorts a set rather than a list containing repeated copies of the same boundary.

For `1 2 3`, the cake has weight 6. The (A)-partition has no internal cuts, the (B)-partition has a cut at 3, and the (C)-partition has cuts at 2 and 4. The union gives `0, 2, 3, 4, 6`, so the four output weights are 2, 1, 1, and 2. The single (A)-guest receives all four pieces, while the other two scenarios split those same pieces at their own boundaries.

For `2 3 4`, the cake has weight 12. The (A)-boundaries are 0, 6, 12, the (B)-boundaries are 0, 4, 8, 12, and the (C)-boundaries are 0, 3, 6, 9, 12. The combined boundaries produce six pieces. Their recipient assignments are determined by integer division against widths 6, 4, and 3, so every guest receives exactly 6, 4, or 3 grams in the corresponding scenario.

For the large case `1000 999 997`, the least common multiple is below (10^9), but the algorithm never constructs (10^9) pieces. It creates at most (999+998+996+1=2994) boundary positions before duplicate removal, and consequently at most 2993 pieces. Every boundary is an exact integer multiple of one of the three partition widths, so no floating-point arithmetic is needed even at the largest allowed input values.
