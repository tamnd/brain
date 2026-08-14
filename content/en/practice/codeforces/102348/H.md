---
title: "CF 102348H - Berland Prospect"
description: "The lanterns are given as strictly increasing coordinates, so their input order is already their order along the street. We need to select the largest subsequence of these coordinates that forms an arithmetic progression."
date: "2026-08-14T12:11:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "H"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 1176
verified: false
draft: false
---

[CF 102348H - Berland Prospect](https://codeforces.com/problemset/problem/102348/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 19m 36s  
**Verified:** no  

## Solution
## Problem Understanding

The lanterns are given as strictly increasing coordinates, so their input order is already their order along the street. We need to select the largest subsequence of these coordinates that forms an arithmetic progression. If we select coordinates (a_1,a_2,\ldots,a_k), every consecutive gap must be identical. Any selection of one or two lanterns is automatically valid, so the interesting part begins at length three.

The coordinates can be as large as (10^{18}), which rules out approaches that depend on the coordinate range. We have at most (n=3000) lanterns, however, so an (O(n^2)) algorithm is realistic. There are about (n^2/2=4.5) million pairs when (n=3000), which is a suitable amount of work for a quadratic dynamic program. An (O(n^3)) algorithm would perform on the order of (3000^3/6=4.5) billion inner iterations in a natural implementation, far beyond the two-second limit.

The strict increase of the coordinates also gives us a useful ordering property. If (i<j), the common difference of an arithmetic progression ending at (x_i,x_j) is (x_j-x_i>0). Its previous coordinate, if one exists, must be

[
x_i-(x_j-x_i)=2x_i-x_j.
]

Because (2x_i-x_j<x_i), that previous coordinate must have a smaller index. This lets every state depend only on states that have already been computed.

There are several edge cases that can expose an incorrect implementation. With three consecutive coordinates such as

```
3
1 2 3
```

the answer is 3, because the whole array has equal gaps. An implementation that initializes every progression to length 2 but forgets to extend it when the middle point exists would incorrectly return 2.

A second case is

```
5
1 2 4 6 7
```

whose answer is 3. The coordinates (1,4,7) form an arithmetic progression, even though they are not consecutive in the input. A solution that only examines consecutive lanterns would miss this and return 2.

A third issue is a progression whose predecessor is absent. For example,

```
3
1 2 4
```

has answer 2. For the pair (2,4), the required previous coordinate would be (0), which is not present. The pair is still a valid progression of length 2, so the implementation must not treat a missing predecessor as an error.

Finally, the coordinates can be extremely large. An expression such as (2x_i-x_j) can temporarily leave the interval ([0,10^{18}]), so it must be handled as an integer rather than relying on array indexing by coordinate. Python integers have arbitrary precision, which makes this straightforward.

## Approaches

A direct approach is to choose the first two lanterns of a progression, determine their difference, and then repeatedly search for the next coordinate having the same difference. There are (O(n^2)) possible starting pairs. If each pair scans the remaining coordinates, the worst-case number of iterations is

[
\sum_{i=0}^{n-1}\sum_{j=i+1}^{n-1}(n-j-1)=O(n^3),
]

with roughly (n^3/6), or 4.5 billion, iterations at (n=3000). A hash set can make each individual search constant time, but it does not remove the third factor because every starting pair can still generate a long scan.

The brute-force approach works because once the first two coordinates are fixed, the entire arithmetic progression is determined. The problem is that it repeatedly discovers the same suffixes. For example, if several different starting pairs eventually reach the same pair of coordinates (x_k,x_i), all of them would independently redo the work needed to extend that pair.

The key observation is that a pair of consecutive selected coordinates completely describes the state we need for future extensions. Define (dp[i][j]), for (i<j), as the maximum length of an arithmetic progression whose last two selected coordinates are (x_i,x_j). If we want to extend this progression backwards, its previous coordinate must be (2x_i-x_j). There is at most one such lantern because all coordinates are distinct.

Suppose that coordinate exists at index (k<i). Then the progression ending at (x_i,x_j) is obtained by taking the progression ending at (x_k,x_i) and appending (x_j). Thus

[
dp[i][j]=dp[k][i]+1.
]

If (2x_i-x_j) is absent, the pair (x_i,x_j) can still start a valid progression, so (dp[i][j]=2).

The recurrence gives (O(n^2)) states and constant work per state once coordinates are mapped to indices. The usual two-dimensional Python list would waste a large amount of memory because millions of Python integer objects and list references are expensive. Since the answer is at most 3000, every DP value fits into an unsigned 16-bit integer. We can store all triangular DP states in an `array('H')`, reducing the DP storage to roughly 9 MB.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(n)) | Too slow |
| Optimal | (O(n^2)) | (O(n^2)) packed into 16-bit values | Accepted |

## Algorithm Walkthrough

1. Store the coordinates in the given sorted order and build a dictionary mapping every coordinate to its index. The dictionary lets us determine whether the required predecessor (2x_i-x_j) exists in constant expected time.
2. Allocate one packed DP entry for every pair (i<j). We only need triangular storage because states with (i\ge j) are meaningless, and each value is at most (n\le3000), so an unsigned 16-bit integer is sufficient.
3. Process the first index (i) from left to right, and for every (j>i), consider the pair (x_i,x_j). Every predecessor of this pair must have an index smaller than (i), so the state needed by the recurrence has already been computed.
4. Compute the required predecessor coordinate as (p=2x_i-x_j). If (p) is present at index (k), read the already computed state (dp[k][i]) and set

[
dp[i][j]=dp[k][i]+1.
]

The arithmetic identity behind this step is exactly the equal-gap condition. If the gap from (x_k) to (x_i) equals the gap from (x_i) to (x_j), then (x_k=2x_i-x_j).

1. If (p) is not present, set (dp[i][j]=2). Any pair of lanterns is valid regardless of their distance, so every pair provides a progression of length at least two.
2. Update the global answer with the largest DP value seen. Since (n\ge3), the answer is always at least 2, and if a valid three-or-more progression exists, the recurrence records its full length.

Why it works: the invariant is that after processing a pair (i,j), `dp[i,j]` is exactly the longest arithmetic progression whose final two coordinates are (x_i,x_j). If the required predecessor (2x_i-x_j) exists, every progression ending at (i,j) must use that unique predecessor, so extending the best progression ending at (k,i) gives the optimal value. If the predecessor does not exist, no progression of length at least three can end at (i,j), leaving the pair itself as the optimal length 2. Since every possible arithmetic progression has some final pair, taking the maximum over all pairs gives the global optimum.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())
    x = list(map(int, input().split()))

    pos = {value: i for i, value in enumerate(x)}

    # For row i, store dp[i][i+1], dp[i][i+2], ..., dp[i][n-1].
    # Number of stored pairs is n * (n - 1) // 2.
    total = n * (n - 1) // 2
    dp = array('H', [0]) * total

    # base[i] is the first position belonging to row i.
    base = [0] * n
    for i in range(1, n):
        base[i] = base[i - 1] + (n - i)

    def index(i, j):
        return base[i] + (j - i - 1)

    ans = 2

    for i in range(n - 1):
        xi = x[i]

        for j in range(i + 1, n):
            previous = 2 * xi - x[j]
            k = pos.get(previous)

            if k is not None:
                length = dp[index(k, i)] + 1
            else:
                length = 2

            dp[index(i, j)] = length

            if length > ans:
                ans = length

    print(ans)

if __name__ == "__main__":
    solve()
```

The coordinate dictionary is built first, so a predecessor lookup does not require binary search for every pair. Since the coordinates are distinct, `pos.get(previous)` either returns the unique predecessor index or `None`.

The triangular DP layout deserves some attention. Row `i` contains only pairs `(i, i+1)` through `(i, n-1)`. Its starting position is

[
\text{base}[i]=\sum_{r=0}^{i-1}(n-r-1).
]

The recurrence then maps `(i,j)` to `base[i] + (j-i-1)`. The subtraction by one is needed because the first stored pair in row `i` is `(i,i+1)`.

The recurrence reads `dp[index(k, i)]`, not `dp[index(i, k)]`, because the progression is ordered by coordinate and (k<i). The predecessor calculation guarantees this ordering automatically whenever the predecessor exists.

The DP value is stored in an unsigned 16-bit array. The maximum possible progression length is 3000, comfortably below 65535. This avoids the memory overhead of millions of Python integers. Python's integer arithmetic also handles coordinates near (10^{18}) without overflow.

There is no special case for three lanterns. The pair recurrence naturally changes a length-2 state into length 3 when the required predecessor exists, so the sample `1 2 3` produces 3 without separate logic.

## Worked Examples

For Sample 1, the coordinates are `1 2 3`. The only three-lantern progression has common difference 1.

| i | j | pair | previous coordinate | predecessor index | dp[i][j] | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1, 2 | 0 | absent | 2 | 2 |
| 0 | 2 | 1, 3 | -1 | absent | 2 | 2 |
| 1 | 2 | 2, 3 | 1 | 0 | 3 | 3 |

For the final pair `(2,3)`, the required predecessor is `1`, which is present at index 0. The already computed state for `(1,2)` has length 2, so appending 3 gives length 3. The answer is consequently 3.

For Sample 2, the coordinates are `1 2 4 6 7`. The best progression is `1,4,7`, with common difference 3.

| i | j | pair | previous coordinate | predecessor index | dp[i][j] | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1, 2 | 0 | absent | 2 | 2 |
| 0 | 2 | 1, 4 | -2 | absent | 2 | 2 |
| 0 | 3 | 1, 6 | -4 | absent | 2 | 2 |
| 0 | 4 | 1, 7 | -5 | absent | 2 | 2 |
| 1 | 2 | 2, 4 | 0 | absent | 2 | 2 |
| 1 | 3 | 2, 6 | -2 | absent | 2 | 2 |
| 1 | 4 | 2, 7 | -3 | absent | 2 | 2 |
| 2 | 3 | 4, 6 | 2 | index 1 | 3 | 3 |
| 2 | 4 | 4, 7 | 1 | index 0 | 3 | 3 |
| 3 | 4 | 6, 7 | 5 | absent | 2 | 3 |

The state `(2,4)` corresponds to coordinates `4,7`. Its predecessor is coordinate `1`, so it extends the state `(0,2)`, representing `1,4`, to length 3. This demonstrates why the DP must consider non-consecutive input indices rather than only neighboring lanterns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2)) | Every pair (i<j) is processed once, with constant expected-time dictionary work. |
| Space | (O(n^2)) | There are (n(n-1)/2) DP states, stored as 16-bit integers, plus the coordinate dictionary and index array. |

For (n=3000), there are only about 4.5 million DP states. The packed representation uses roughly 9 MB for the DP itself, while the remaining Python data structures stay comfortably within the 512 MB memory limit. The quadratic loop performs about 4.5 million iterations, which is appropriate for the given limit.

## Test Cases

```python
import sys
import io
from array import array

def solve():
    input = sys.stdin.readline

    n = int(input())
    x = list(map(int, input().split()))

    pos = {value: i for i, value in enumerate(x)}

    total = n * (n - 1) // 2
    dp = array('H', [0]) * total

    base = [0] * n
    for i in range(1, n):
        base[i] = base[i - 1] + (n - i)

    def index(i, j):
        return base[i] + (j - i - 1)

    ans = 2

    for i in range(n - 1):
        xi = x[i]
        for j in range(i + 1, n):
            previous = 2 * xi - x[j]
            k = pos.get(previous)

            if k is None:
                length = 2
            else:
                length = dp[index(k, i)] + 1

            dp[index(i, j)] = length
            ans = max(ans, length)

    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("3\n1 2 3\n") == "3\n", "sample 1"
assert run("5\n1 2 4 6 7\n") == "3\n", "sample 2"
assert run("10\n5 10 15 20 35 60 80 85 110 120\n") == "5\n", "sample 3"

# Minimum-size input
assert run("3\n1 2 4\n") == "2\n", "no three-term progression"

# Boundary coordinates near 10^18
assert run("5\n0 250000000000000000 500000000000000000 750000000000000000 1000000000000000000\n") == "5\n", "large coordinates"

# Off-by-one case: progression uses non-consecutive input positions
assert run("7\n1 2 4 7 10 13 20\n") == "4\n", "non-consecutive progression"

# Maximum-size case: all 3000 coordinates form one progression
n = 3000
maximum_case = str(n) + "\n" + " ".join(map(str, range(n))) + "\n"
assert run(maximum_case) == "3000\n", "maximum-size arithmetic progression"

# The following would be an all-equal input:
# 3
# 5 5 5
# It is intentionally not asserted because the problem requires
# x_1 < x_2 < ... < x_n. Such an input is outside the specification.
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 1 2 4` | 2 | Minimum valid input where no three-term progression exists |
| `5 / 0 250000000000000000 ... 1000000000000000000` | 5 | Coordinates near the (10^{18}) boundary and large integer arithmetic |
| `7 / 1 2 4 7 10 13 20` | 4 | Progressions whose members are not adjacent in the input |
| 3000 consecutive coordinates | 3000 | Maximum (n), quadratic state count, and the maximum possible answer |
| `3 / 5 5 5` | Not applicable | All-equal coordinates are outside the strict-increasing input constraint |

## Edge Cases

The first edge case is the smallest possible input. With

```
3
1 2 3
```

the pair `(1,2)` is initialized to length 2. When the algorithm reaches `(2,3)`, it computes (2\cdot2-3=1), finds coordinate 1, and reads the length-2 state for `(1,2)`. It produces (2+1=3), so the final answer is 3. No special handling for `n=3` is required.

The second edge case is a pair without a predecessor. For

```
3
1 2 4
```

the pair `(2,4)` requires coordinate (2\cdot2-4=0). Since 0 is absent, the algorithm assigns length 2 to that pair. The pair `(1,2)` also has length 2, and no state reaches length 3. The output is 2.

The third edge case is a progression hidden among unrelated coordinates. For

```
7
1 2 4 7 10 13 20
```

the coordinates `1, 4, 7, 10` form a progression with difference 3. When processing `(7,10)`, the predecessor is 4, so the state extends `1,4,7` to `1,4,7,10`. The answer becomes 4. This catches implementations that only inspect adjacent input elements.

The fourth edge case uses the largest legal coordinate values:

```
5
0 250000000000000000 500000000000000000 750000000000000000 1000000000000000000
```

Every gap is (250000000000000000), so the answer is 5. The predecessor calculation repeatedly produces values as large as (10^{18}), and Python handles them exactly.

The requested all-equal case, such as

```
3
5 5 5
```

cannot occur in a valid test because the problem guarantees strictly increasing coordinates. The dictionary and DP are designed around that guarantee, so this malformed input is deliberately excluded from the executable assertions rather than pretending it is a legal test.
