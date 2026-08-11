---
title: "CF 102409J - Best division"
description: "There are (N-1) legal cutting positions inside a chocolate bar of length (L). Adding the two endpoints (0) and (L), we have (N+1) positions that describe (N) elementary pieces. We must choose exactly three of the interior positions, producing four contiguous pieces."
date: "2026-08-12T00:04:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102409
codeforces_index: "J"
codeforces_contest_name: "Semana i 2019"
rating: 0
weight: 102409
solve_time_s: 132
verified: true
draft: false
---

[CF 102409J - Best division](https://codeforces.com/problemset/problem/102409/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (N-1) legal cutting positions inside a chocolate bar of length (L). Adding the two endpoints (0) and (L), we have (N+1) positions that describe (N) elementary pieces. We must choose exactly three of the interior positions, producing four contiguous pieces.

If the chosen cuts are at positions (a<b<c), the four piece lengths are

[
a,\qquad b-a,\qquad c-b,\qquad L-c.
]

The quality of this division is the difference between its largest and smallest piece. We need the minimum possible value of that difference over every legal choice of three cuts.

The input size is the first warning sign. With (N) as large as (10^5), trying every triple of cuts requires

\frac{(N-1)(N-2)(N-3)}{6}
]

possibilities, which is about (1.67\times10^{14}) when (N=10^5). A one-second limit rules that out completely. The coordinates can reach (10^{15}), so the implementation must also use 64-bit integer arithmetic. Python integers already handle this range safely.

There are several boundary cases that can make an otherwise plausible implementation wrong. First, when (N=4), there are exactly three legal cuts, so there is only one possible division. For example,

```
4 10
2 5 7
```

produces pieces (2,3,2,3), so the answer is (1). An implementation that assumes there are several middle-cut choices can accidentally skip this case.

The endpoints (0) and (L) are not cutting spots. For

```
4 10
1 5 9
```

the only valid pieces are (1,4,4,1), giving answer (3). Treating an endpoint as if it were an available cut changes the problem and can produce an invalid division.

Another subtle case occurs when the ideal midpoint lies exactly between two available cuts. Consider

```
5 10
2 4 6 8
```

For a suitable middle cut, the left half has target coordinate (3), and both (2) and (4) are equally close. Either choice produces the same two left-piece lengths in reversed order, so the answer is (2). A search only checking one side of the insertion point can miss the optimum.

Finally, coordinates can be much larger than the usual machine-integer range. For

```
4 1000000000000000
1 2 3
```

the only division has lengths (1,1,1,999999999999997), so the answer is

```
999999999999996
```

Using floating point to locate a midpoint is unnecessary and potentially unsafe at this scale. The solution below performs all midpoint calculations with integer arithmetic.

## Approaches

The direct solution is to choose the first, second, and third cuts. If their positions are (a<b<c), we calculate the four lengths and update the answer with

[
\max(a,b-a,c-b,L-c)-\min(a,b-a,c-b,L-c).
]

This is correct because every legal division corresponds to exactly one increasing triple of interior cuts, so checking all triples checks every possible division. The problem is the number of triples. For (N=10^5), there are about (1.67\times10^{14}) of them, far beyond what the time limit permits.

The useful structure appears when we temporarily fix the second, or middle, cut at position (b). Once (b) is fixed, the problem separates into two independent pairs.

The two pieces on the left are

[
a,\qquad b-a,
]

and their sum is fixed at (b). The two pieces on the right are

[
c-b,\qquad L-c,
]

and their sum is fixed at (L-b).

For two numbers with a fixed sum, making them closer to each other can never make the global maximum-minus-minimum worse. Suppose the current pair is (x,S-x). Moving (x) toward (S/2) simultaneously moves the larger member downward and the smaller member upward. Any other pieces outside this pair are unaffected, so the global range cannot increase.

This gives the central observation: for a fixed middle cut (b), the best first cut is the available cut position closest to (b/2). The best third cut is the available cut position closest to

[
\frac{b+L}{2}.
]

The first target is the point where (a=b-a), and the second target is the point where (c-b=L-c). Since the cut positions are sorted, each nearest position can be found with binary search.

The brute force works because it explicitly examines every triple, but fails because there are too many triples. The observation that a fixed middle cut lets each side be optimized independently reduces the problem to (O(N)) middle cuts, with two (O(\log N)) binary searches for each one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3)) | (O(N)) | Too slow |
| Optimal | (O(N\log N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Store the cut positions together with the two endpoints. Define

[
p_0=0,\quad p_1=x_1,\ldots,p_{N-1}=x_{N-1},\quad p_N=L.
]

The array has (N+1) positions, while only indices (1) through (N-1) are legal cuts.
2. Iterate over every possible middle cut (j), so (2\le j\le N-2). A middle cut needs at least one legal cut before it and one legal cut after it.

Let its coordinate be (p_j). The two left pieces have total length (p_j), so their ideal split occurs at

[
\frac{p_j}{2}.
]
3. Find the legal cut (i<j) whose coordinate is closest to (p_j/2). Because the positions are sorted, binary search gives the insertion point immediately around this target. We only need to inspect the position at the insertion point and its predecessor.

The resulting left pieces are (p_i) and (p_j-p_i). Choosing the closest position to the midpoint makes these two pieces as balanced as the available cuts permit.
4. For the right side, the two pieces have total length (L-p_j). If the third cut is (p_k), they are

[
p_k-p_j,\qquad L-p_k.
]

They are equal when

[
p_k=\frac{p_j+L}{2}.
]

Binary search for the legal position (k>j) closest to this coordinate, again checking the insertion point and its predecessor.
5. Compute the four lengths produced by these two locally balanced choices and update the global minimum range.
6. After all possible middle cuts have been processed, output the smallest range found.

The midpoint search uses integer targets rather than floating point. For a midpoint (S/2), using ((S+1)//2) gives the upper integer midpoint. Checking that position and its predecessor covers both sides when (S) is odd, while for even (S) the exact midpoint is found directly.

### Why it works

Fix any middle cut (b). Consider any valid first cut (a). The left pair has fixed sum (b), so replacing (a) by an available position closer to (b/2) makes the two left lengths less spread out. Its smaller member can only increase and its larger member can only decrease. The same argument applies independently to the right pair, whose sum is (L-b). Consequently, for this fixed middle cut, the pair of midpoint-nearest cuts produces a division whose global range is no larger than any other division using the same middle cut. Since the algorithm examines every possible middle cut, at least one iteration considers the middle cut of an optimal division, and that iteration reconstructs a division no worse than the optimum. It must consequently produce the global optimum.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n, L = map(int, input().split())
    cuts = list(map(int, input().split()))

    # p[0] = 0, p[1..n-1] are legal cuts, p[n] = L.
    p = [0] + cuts + [L]

    ans = L

    # j is the middle cut. There must be one legal cut
    # on each side of it.
    for j in range(2, n - 1):
        pj = p[j]

        # Left pair: p[i], pj - p[i].
        # Its balance is best when p[i] is closest to pj / 2.
        left_target = (pj + 1) // 2
        i = bisect_left(p, left_target, 1, j)

        left_candidates = []
        if i < j:
            left_candidates.append(i)
        if i - 1 >= 1:
            left_candidates.append(i - 1)

        best_i = min(
            left_candidates,
            key=lambda idx: abs(2 * p[idx] - pj)
        )

        # Right pair: p[k] - pj, L - p[k].
        # Balance is best when p[k] is closest to (pj + L) / 2.
        right_target = (pj + L + 1) // 2
        k = bisect_left(p, right_target, j + 1, n)

        right_candidates = []
        if k < n:
            right_candidates.append(k)
        if k - 1 > j:
            right_candidates.append(k - 1)

        best_k = min(
            right_candidates,
            key=lambda idx: abs(2 * p[idx] - (pj + L))
        )

        a = p[best_i]
        b = pj
        c = p[best_k]

        pieces = (
            a,
            b - a,
            c - b,
            L - c
        )

        current = max(pieces) - min(pieces)
        ans = min(ans, current)

    print(ans)

if __name__ == "__main__":
    solve()
```

The position array starts with (0) and ends with (L). This is convenient because every piece length can then be written as a difference of two entries. The three chosen cuts still come only from indices (1) through (N-1).

The loop uses `range(2, n - 1)`, which corresponds exactly to middle cuts that have at least one legal cut on both sides. For (N=4), this loop contains exactly one index, (j=2), which is the only possible middle cut.

For the left search, `bisect_left` is restricted to indices `[1, j)`. That prevents the binary search from selecting the middle cut itself or the left endpoint. The right search is similarly restricted to `[j+1, n)`, preventing the middle cut and the endpoint (L) from being selected.

The expression `abs(2 * p[idx] - pj)` compares a candidate's distance from (p_j/2) without using floating point. The right side uses `abs(2 * p[idx] - (pj + L))` for the same reason. All calculations remain exact even when coordinates are around (10^{15}).

Only two candidate indices around each binary-search insertion point can be optimal. Since the positions are sorted, every earlier position is farther from the target than the predecessor, and every later position is farther than the insertion point.

## Worked Examples

Only one official sample is supplied, so the second trace uses a small constructed input.

For Sample 1, the complete position array is

[
[0,3,4,5,8,10,12,15,18].
]

For every possible middle cut, the algorithm balances the left and right pairs independently.

| Middle index (j) | (p_j) | First cut (p_i) | Third cut (p_k) | Four pieces | Range |
| --- | --- | --- | --- | --- | --- |
| 2 | 4 | 3 | 10 | (3,1,6,8) | 7 |
| 3 | 5 | 3 | 12 | (3,2,7,6) | 5 |
| 4 | 8 | 4 | 12 | (4,4,4,6) | 2 |
| 5 | 10 | 5 | 15 | (5,5,5,3) | 2 |
| 6 | 12 | 8 | 15 | (8,4,3,3) | 5 |

The best range is (2), matching the sample output. The two rows with range (2) correspond exactly to the two optimal divisions described by the sample: (4,4,4,6) and (5,5,5,3).

For the second example,

```
5 10
2 4 7 9
```

the position array is

[
[0,2,4,7,9,10].
]

There are three possible middle cuts.

| Middle index (j) | (p_j) | First cut (p_i) | Third cut (p_k) | Four pieces | Range |
| --- | --- | --- | --- | --- | --- |
| 2 | 4 | 2 | 7 | (2,2,3,3) | 1 |
| 3 | 7 | 4 | 9 | (4,3,2,1) | 3 |

The algorithm actually needs only two middle-cut iterations because (j=2,3) are the valid indices for (N=5). The first gives (2,2,3,3), so the answer is (1).

This example demonstrates why balancing each side is enough. With middle cut (4), the best left split is (2,2), and the best right split is (3,3). No unbalanced alternative can improve the global range.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) | There are (O(N)) middle cuts, and each uses two binary searches. |
| Space | (O(N)) | The sorted position array contains (N+1) integers. |

For (N=10^5), the algorithm performs only (O(N)) iterations and two logarithmic searches per iteration. This is comfortably within the intended scale of the problem, while the brute-force approach would require roughly (1.67\times10^{14}) triples at the maximum (N). The position values are at most around (10^{15}), which Python handles exactly without overflow.

## Test Cases

```python
import sys
import io
from bisect import bisect_left

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        n, L = map(int, sys.stdin.readline().split())
        cuts = list(map(int, sys.stdin.readline().split()))

        p = [0] + cuts + [L]
        ans = L

        for j in range(2, n - 1):
            pj = p[j]

            left_target = (pj + 1) // 2
            i = bisect_left(p, left_target, 1, j)

            left_candidates = []
            if i < j:
                left_candidates.append(i)
            if i - 1 >= 1:
                left_candidates.append(i - 1)

            best_i = min(
                left_candidates,
                key=lambda idx: abs(2 * p[idx] - pj)
            )

            right_target = (pj + L + 1) // 2
            k = bisect_left(p, right_target, j + 1, n)

            right_candidates = []
            if k < n:
                right_candidates.append(k)
            if k - 1 > j:
                right_candidates.append(k - 1)

            best_k = min(
                right_candidates,
                key=lambda idx: abs(2 * p[idx] - (pj + L))
            )

            pieces = (
                p[best_i],
                p[j] - p[best_i],
                p[best_k] - p[j],
                L - p[best_k],
            )

            ans = min(ans, max(pieces) - min(pieces))

        print(ans)
        return sys.stdout.getvalue()

    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    "8 18\n"
    "3 4 5 8 10 12 15\n"
) == "2\n", "sample 1"

# Minimum N, only one possible division
assert run(
    "4 10\n"
    "2 5 7\n"
) == "1\n", "minimum-size case"

# Very large coordinates, checks integer arithmetic and boundary handling
assert run(
    "4 1000000000000000\n"
    "1 2 3\n"
) == "999999999999996\n", "large-coordinate boundary case"

# Designed to catch midpoint and insertion-point errors
assert run(
    "5 10\n"
    "2 4 7 9\n"
) == "1\n", "midpoint search case"

# Maximum N, every elementary piece has length 1.
# Cuts are 1, 2, ..., 99999 and L = 100000.
max_n = 100000
max_input = (
    f"{max_n} {max_n}\n"
    + " ".join(map(str, range(1, max_n)))
    + "\n"
)
assert run(max_input) == "0\n", "maximum-N equal-piece case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 10 / 2 5 7` | `1` | Minimum (N), exactly one possible division |
| `4 1000000000000000 / 1 2 3` | `999999999999996` | Large coordinates and integer arithmetic |
| `5 10 / 2 4 7 9` | `1` | Binary-search midpoint selection and index boundaries |
| `100000 100000 / 1 2 ... 99999` | `0` | Maximum (N), balanced division, performance |

## Edge Cases

When (N=4), the three supplied cutting spots are the only possible cuts. For

```
4 10
2 5 7
```

the position array is (0,2,5,7,10). The only possible four pieces are (2,3,2,3), giving range (3-2=1). The loop processes (j=2), finds (i=1) and (k=3), and returns (1).

When the ideal midpoint lies between two legal positions, both neighboring candidates must be considered. In

```
5 10
2 4 6 8
```

consider the middle cut at (6). The left target is (3), and the legal positions (2) and (4) are equally distant. Choosing either produces the same pair (2,4), only in reversed order. On the right, the target is (8), which is an available cut, giving pieces (2,4,2,2) and range (2). The algorithm's insertion-point and predecessor checks cover the tie correctly.

Endpoints must never become selected cuts. In

```
4 10
1 5 9
```

the position array is (0,1,5,9,10). The only valid division is (1,4,4,1), with answer (3). The left binary search is restricted to legal cut indices before the middle cut, and the right search is restricted to legal cut indices after it, so neither (0) nor (L) can enter the chosen triple.

Large coordinates require exact midpoint handling. For

```
4 1000000000000000
1 2 3
```

the four lengths are (1,1,1,999999999999997), so the answer is (999999999999996). The implementation never converts these values to floating point. The midpoint comparisons are performed through expressions such as (2p_i-p_j), preserving exactness for every allowed input value.

The maximum-size equal-piece case also exercises the indexing boundaries. With (N=100000), (L=100000), and cuts at every integer from (1) through (99999), the bar can be divided at (25000,50000,75000). Every resulting piece has length (25000), so the answer is (0). The algorithm handles all (99998) possible middle-cut positions without enumerating triples, demonstrating why the (O(N\log N)) structure is necessary for the largest input.
