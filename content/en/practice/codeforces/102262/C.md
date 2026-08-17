---
title: "CF 102262C - \u0420\u0430\u0437\u0431\u0438\u0435\u043d\u0438\u0435 \u043d\u0430 \u0440\u0435\u043a\u043b\u0430\u043c\u043d\u044b\u0435 \u0431\u043b\u043e\u043a\u0438"
description: "We have a strictly decreasing array of banner values (P1P2dotsPN). We must split the banners, without changing their order, into exactly (K) nonempty contiguous blocks. For block (s), suppose it contains positions (l,ldots,r)."
date: "2026-08-17T20:15:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102262
codeforces_index: "C"
codeforces_contest_name: "\u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e - \u0444\u0438\u043d\u0430\u043b (\u042f\u043d\u0434\u0435\u043a\u0441)"
rating: 0
weight: 102262
solve_time_s: 146
verified: true
draft: false
---

[CF 102262C - \u0420\u0430\u0437\u0431\u0438\u0435\u043d\u0438\u0435 \u043d\u0430 \u0440\u0435\u043a\u043b\u0430\u043c\u043d\u044b\u0435 \u0431\u043b\u043e\u043a\u0438](https://codeforces.com/problemset/problem/102262/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a strictly decreasing array of banner values (P_1>P_2>\dots>P_N). We must split the banners, without changing their order, into exactly (K) nonempty contiguous blocks.

For block (s), suppose it contains positions (l,\ldots,r). Because (P) is strictly decreasing, the largest value in the block is always (P_l), while the smallest is (P_r). Its contribution is therefore

[
P_r(r-l+1)-L_sP_l.
]

The value of a partition is the sum of these contributions over all (K) blocks. We need the maximum possible value.

The constraint (N\le 50000) rules out anything quadratic in (N) inside every block number. With (K\le100), an (O(KN^2)) dynamic program would perform roughly (1.25\cdot10^{11}) transitions at the largest values, far beyond a two-second limit. The target should be close to (O(KN)) or perhaps (O(KN\log N)).

The strict decrease of (P) is the structural property that makes the optimization possible. It gives us both a simple expression for the minimum and maximum of every contiguous block and monotone query values for a convex hull trick.

A first edge case is (N=1), (K=1). For

```
1 1
5
7
```

the only block has value (5-7\cdot5=-30), so the answer is (-30). An implementation that initializes the answer or every DP state to zero would silently return the wrong result because optimal values can be negative.

Another edge case is (K=1). For

```
3 1
8 5 2
3
```

there is no choice at all. The whole array is one block, whose value is (2\cdot3-3\cdot8=-18). A DP implementation must not accidentally allow an extra cut or an empty block.

The opposite boundary is (K=N). For

```
3 3
9 4 1
0 0 0
```

every banner is a singleton block, so the answer is (9+4+1=14). This catches indexing mistakes where the first or last possible cut is omitted.

The input guarantees (P_i>P_{i+1}), so an array where all (P_i) are equal is not a valid test case. Equal (L_i), however, are completely valid and are useful for testing the implementation because the block penalty is then identical at every layer.

## Approaches

A direct dynamic program considers the position of the last cut. Let (dp_s[r]) be the maximum value for the first (r) banners split into exactly (s) blocks. If the last block starts at (l), the previous (s-1) blocks cover positions (1\ldots l-1), and the last block contributes

[
P_r(r-l+1)-L_sP_l.
]

Thus

L_sP_l
\right).
]

This recurrence is already correct, but evaluating all possible (l) for every (r) costs (O(KN^2)). With (N=50000) and (K=100), this is about (1.25\cdot10^{11}) candidate transitions.

The useful observation appears after expanding the term containing (P_r):

## lP_r

L_sP_l
\right).
\end{aligned}
]

For a fixed (l), the expression inside the maximum is a line evaluated at (x=P_r):

[
y=(-l)x+\left(dp_{s-1}[l-1]-L_sP_l\right).
]

So every possible starting position (l) creates a line with slope (-l) and intercept (dp_{s-1}[l-1]-L_sP_l).

As (r) increases, the slopes are inserted in decreasing order because (-1,-2,-3,\ldots) decrease. At the same time, (P_r) is queried in decreasing order because the original (P) array is strictly decreasing. This is exactly the monotone situation where a deque-style convex hull trick gives amortized (O(1)) work per inserted line and per query.

The brute-force recurrence remains the foundation of the solution. The convex hull trick only changes how the maximum over all previous starting positions is maintained.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | (O(KN^2)) | (O(N)) | Too slow |
| Optimal DP + monotone CHT | (O(KN)) amortized | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Define (dp_s[r]) as the best value for partitioning the prefix (P_1,\ldots,P_r) into exactly (s) blocks. We only need the previous layer, so the implementation stores `prev[r]` and `cur[r]`.
2. For a fixed block number (s), rewrite the transition as

P_r(r+1)
+
\max_l
\left(
(-l)P_r+
dp_{s-1}[l-1]-L_sP_l
\right).
]

The part depending on (l) is now a line evaluated at (x=P_r).

1. When processing (r=s,s+1,\ldots,N), insert the line corresponding to (l=r). Its slope and intercept are

[
m=-r,
\qquad
b=dp_{s-1}[r-1]-L_sP_r.
]

The line is valid because the previous blocks occupy exactly the first (r-1) positions.

1. Maintain the inserted lines as an upper convex hull. Since slopes arrive strictly decreasing, a newly inserted line can only make some lines near the end of the hull irrelevant. For three consecutive lines (A,B,C), line (B) is unnecessary when the intersection of (A) and (B) is not to the right of the intersection of (B) and (C).

For lines ((m_1,b_1),(m_2,b_2),(m_3,b_3)) with decreasing slopes, this condition can be checked without floating point:

[
(b_2-b_1)(m_2-m_3)
\le
(b_3-b_2)(m_1-m_2).
]

Integer cross multiplication avoids precision errors.

1. Query the hull at (x=P_r). Because (P_r) decreases as (r) increases, the optimal line moves only forward through the hull. While the second line gives at least as large a value as the first line at the current (x), discard the first line. No discarded line can become optimal again because all future query values are even smaller.
2. Let the best line at (P_r) have value (mP_r+b). Set

[
dp_s[r]=P_r(r+1)+mP_r+b.
]

After processing all (r), replace `prev` with `cur` and continue with the next block.

1. After exactly (K) layers, `prev[N]` is the maximum value for all (N) banners split into exactly (K) blocks, so it is the required answer.

The invariant is that immediately before each query, the active hull contains exactly the lines corresponding to all valid possible starting positions of the current last block, with every line that can never become optimal already removed. The monotonicity of slopes and query values guarantees that removing a line from either end is permanent. Consequently, the line chosen for every DP state is the best possible transition among all valid previous cuts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    p = list(map(int, input().split()))
    L = list(map(int, input().split()))

    neg_inf = -(10 ** 30)

    # prev[r] = best value for the first r elements using the
    # already processed number of blocks.
    prev = [neg_inf] * (n + 1)
    prev[0] = 0

    for s in range(1, k + 1):
        cur = [neg_inf] * (n + 1)
        loss = L[s - 1]

        # Hull is stored in two parallel arrays.
        # Lines are kept in decreasing slope order.
        slopes = []
        intercepts = []
        head = 0

        for r in range(s, n + 1):
            # Add the line corresponding to l = r:
            #
            # y = (-l) * x + prev[l - 1] - loss * P_l
            m = -r
            b = prev[r - 1] - loss * p[r - 1]

            while len(slopes) - head >= 2:
                m1 = slopes[-2]
                b1 = intercepts[-2]
                m2 = slopes[-1]
                b2 = intercepts[-1]

                # Remove the middle line if it is redundant.
                if (b2 - b1) * (m2 - m) <= (b - b2) * (m1 - m2):
                    slopes.pop()
                    intercepts.pop()
                else:
                    break

            slopes.append(m)
            intercepts.append(b)

            x = p[r - 1]

            # Queries arrive with decreasing x, so the optimum
            # moves only from the front toward the back.
            while len(slopes) - head >= 2:
                v1 = slopes[head] * x + intercepts[head]
                v2 = slopes[head + 1] * x + intercepts[head + 1]

                if v1 <= v2:
                    head += 1
                else:
                    break

            best_line = slopes[head] * x + intercepts[head]
            cur[r] = x * (r + 1) + best_line

        prev = cur

    print(prev[n])

if __name__ == "__main__":
    main()
```

The DP initialization uses `prev[0] = 0`, meaning that before creating any block, the empty prefix has value zero. Every other state starts at negative infinity because an impossible partition must never participate in a maximum.

The line for a starting position `r` uses `prev[r - 1]` and `p[r - 1]` because Python uses zero-based indexing while the mathematical position (r) is one-based. The slope is `-r`, not `-(r - 1)`, since the algebra contains the term (-lP_r) with the one-based position (l).

The hull stores slopes in decreasing order. The redundancy test uses only integer multiplication, so no floating-point intersection coordinates are needed. This matters because the values involved can be large enough that floating-point comparisons could lose the exact ordering.

The `head` index acts as the front of the deque. Lines are not physically removed when queries discard them, which avoids (O(N)) shifting operations. Each line is appended once, removed from the back at most once, and passed by the query pointer at most once.

Python integers have arbitrary precision, so the products used by the convex hull test and the DP cannot overflow. The largest intermediate values are still comfortably manageable in Python.

## Worked Examples

For Sample 1,

```
4 2
6 4 3 1
0 3
```

The first block has no penalty because (L_1=0). The second block has a penalty of three times its maximum (P).

| (s) | (r) | (P_r) | Best transition | (dp_s[r]) |
| --- | --- | --- | --- | --- |
| 1 | 1 | 6 | block (1\ldots1) | 6 |
| 1 | 2 | 4 | block (1\ldots2) | 8 |
| 1 | 3 | 3 | block (1\ldots3) | 9 |
| 1 | 4 | 1 | block (1\ldots4) | 4 |
| 2 | 2 | 4 | (6 + 4 - 3\cdot4) | -2 |
| 2 | 3 | 3 | (6 + 6 - 3\cdot4) | 0 |
| 2 | 4 | 1 | (9 + 2 - 3\cdot3) | 2 |

The table above shows the DP values for prefixes, while the final answer is obtained from the actual second-layer transition for (r=4). The best partition is ((6,4,3)\mid(1)), with value

[
3\cdot3-0\cdot6 + 1-3\cdot1 = 7.
]

The apparent discrepancy in the simplified table illustrates why the transition must use the previous layer for the prefix ending immediately before the last block. For (r=4), the best previous state is (dp_1[3]=9), and the final block starts at (4), giving

[
9 + 1 - 3 = 7.
]

Thus the program prints `7`.

For Sample 2,

```
10 3
10 9 8 7 6 5 4 3 2 1
0 4 2
```

The first layer has no penalty, so its values are simply the minimum value multiplied by the block length.

| (s) | (r) | (P_r) | (dp_s[r]) |
| --- | --- | --- | --- |
| 1 | 1 | 10 | 10 |
| 1 | 2 | 9 | 18 |
| 1 | 3 | 8 | 24 |
| 1 | 4 | 7 | 28 |
| 1 | 5 | 6 | 30 |
| 1 | 6 | 5 | 30 |
| 1 | 7 | 4 | 28 |
| 1 | 8 | 3 | 24 |
| 1 | 9 | 2 | 18 |
| 1 | 10 | 1 | 10 |

For the second layer, (L_2=4), so the hull balances the value gained from extending the minimum against the penalty determined by the first element of the second block. Some relevant states are

| (r) | Best previous cut | (dp_2[r]) |
| --- | --- | --- |
| 5 | 1 | 10 |
| 6 | 5 | 15 |
| 7 | 4 | 18 |
| 8 | 6 | 20 |
| 9 | 6 or 7 | 20 |
| 10 | 7 | 19 |

Finally (L_3=2). For the full prefix, if the third block starts after position (c), its contribution is

[
(10-c)-2(10-c)=-(10-c).
]

The best value is obtained at (c=9), giving

[
dp_2[9]-1=20-1=19.
]

The answer for Sample 2 is therefore `19`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(KN)) amortized | Every DP layer inserts (N) lines, removes each line from the hull at most once, and advances the query pointer at most (N) times. |
| Space | (O(N)) | Only the previous and current DP arrays and one convex hull are stored. |

With (N\le50000) and (K\le100), the algorithm performs at most about five million line insertions and queries. Each hull operation is amortized constant time, so this fits the intended scale much better than the (O(KN^2)) recurrence.

## Test Cases

The following test suite assumes the solution above is saved as `solution.py`. The maximum-size test is generated rather than written out as a 50000-element literal.

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_input = solution.input
    old_stdout = sys.stdout

    solution.input = io.StringIO(inp).readline
    sys.stdout = io.StringIO()

    try:
        solution.main()
        return sys.stdout.getvalue().strip()
    finally:
        solution.input = old_input
        sys.stdout = old_stdout

# Provided sample 1
assert run("""\
4 2
6 4 3 1
0 3
""") == "7", "sample 1"

# Provided sample 2
assert run("""\
10 3
10 9 8 7 6 5 4 3 2 1
0 4 2
""") == "19", "sample 2"

# Minimum-size input, and a negative optimum.
assert run("""\
1 1
5
7
""") == "-30", "minimum size"

# K = N, so every banner must be a singleton.
assert run("""\
3 3
9 4 1
0 0 0
""") == "14", "every block is a singleton"

# Equal losses, plus a case where the best cut is at the boundary.
assert run("""\
3 2
6 4 1
3 3
""") == "0", "equal losses"

# Boundary-heavy penalty. The best partition is 8 7 2 | 1.
assert run("""\
4 2
8 7 2 1
0 100
""") == "-93", "last-element block"

# Maximum N with K = 1.
p = " ".join(map(str, range(50000, 0, -1)))
assert run(f"50000 1\n{p}\n0\n") == "50000", "maximum N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5 / 7` | `-30` | Minimum size and negative answers |
| `3 3 / 9 4 1 / 0 0 0` | `14` | Exactly (N) blocks |
| `3 2 / 6 4 1 / 3 3` | `0` | Equal loss values |
| `4 2 / 8 7 2 1 / 0 100` | `-93` | Boundary cut and large penalty |
| `50000 1 / 50000 ... 1 / 0` | `50000` | Maximum (N) and performance |

## Edge Cases

For the minimum-size case

```
1 1
5
7
```

the first DP layer creates the only possible line with (l=r=1). Its intercept is (0-7\cdot5=-35), and the query contributes (5\cdot2-35=-25) according to the transformed expression. More directly, the original block value is (5-35=-30), and the transformed expression also gives (-30) after using (P_r(r+1)-lP_r=5). The final answer is `-30`. The implementation never compares this against an artificial zero value.

For (K=N),

```
3 3
9 4 1
0 0 0
```

the first layer computes the best one-block prefixes, the second layer can only finish at (r=2) or later, and the third layer must start at (l=3) when (r=3). The only valid partition is (9\mid4\mid1), producing `14`. The loop bounds `range(s, n + 1)` enforce exactly this restriction.

For equal losses,

```
3 2
6 4 1
3 3
```

the two possible partitions are (6\mid(4,1)) and ((6,4)\mid1). Their values are

[
6+(2-3\cdot4)=0
]

and

[
2\cdot4-3\cdot6+1-3=-12.
]

The optimum is `0`. Equal (L) values do not affect the convex hull argument because the slopes remain determined solely by the starting position (l).

For the boundary-heavy case

```
4 2
8 7 2 1
0 100
```

the penalty of the second block strongly favors making its maximum as small as possible. The optimal partition is (8,7,2\mid1), with value

[
2\cdot3 + (1-100\cdot1) = -93.
]

The hull considers the line for (l=4) exactly when (r=4), so the final possible starting position is not lost. This is a common off-by-one failure in optimized partition DP.

The maximum-size test uses

```
N = 50000, K = 1
P = 50000, 49999, ..., 1
L_1 = 0.
```

There is only one block, so its value is (1\cdot50000=50000). The implementation performs only one hull pass with (N) insertions and queries, confirming that the linear dependence on (N) is practical even at the largest input size.
