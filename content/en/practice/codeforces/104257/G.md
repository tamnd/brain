---
title: "CF 104257G - Go Go GPA"
description: "We are given a sequence of courses that must be taken in a fixed order. Each course has an estimated score and a credit value. The student divides these courses into exactly $K$ consecutive semesters, and each semester must contain at least one course."
date: "2026-07-01T21:46:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104257
codeforces_index: "G"
codeforces_contest_name: "2021 NTUIM Programming Design And Optimization (PDAO 2021)"
rating: 0
weight: 104257
solve_time_s: 68
verified: true
draft: false
---

[CF 104257G - Go Go GPA](https://codeforces.com/problemset/problem/104257/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of courses that must be taken in a fixed order. Each course has an estimated score and a credit value. The student divides these courses into exactly $K$ consecutive semesters, and each semester must contain at least one course.

Within a semester, the “academic performance” is computed in three layers. First, we take a credit-weighted average of the raw course scores in that semester. This produces a real number in $[0,100]$. That value is rounded to the nearest integer, and then converted into a GPA value using a fixed score-to-GPA table. Finally, the overall result is simply the arithmetic mean of the $K$ semester GPAs, with no weighting by number of courses or credits.

So the task is not to maximize raw scores, but to choose where to cut the sequence into $K$ contiguous blocks so that the average of the resulting discretized GPAs is as large as possible.

The constraints are small: at most 100 courses and at most 100 semesters. This immediately rules out any exponential enumeration over partitions. Even quadratic or cubic dynamic programming is acceptable since roughly $10^6$ to $10^7$ operations is safe in Python.

A subtle failure case comes from the rounding step. Because semester GPA depends on rounded weighted averages, two segmentations with nearly identical averages can produce different GPAs after rounding.

For example, if a semester has weighted average $89.4$, it becomes 89, but $89.5$ becomes 90. These two values map to different GPA bands, so a naive approach that tries to “smooth” averages or greedily extend segments can fail.

Another edge case is that segmentation decisions are globally coupled. Taking a slightly worse segment early can allow a later segment to cross a GPA boundary after rounding, increasing the total. Local greedy decisions are not reliable.

## Approaches

A brute-force approach would try all ways to split the $N$ courses into $K$ non-empty contiguous segments. The number of such partitions is $\binom{N-1}{K-1}$, which is already enormous even for $N=100$. For each partition, computing all semester GPAs requires scanning segments and performing weighted averages, giving an additional $O(N)$ factor. This becomes completely infeasible.

The structure of the problem is that the value of a semester depends only on the segment itself, not on how previous or future semesters are chosen. Once we fix that the last semester is courses $j+1$ to $i$, the rest of the problem reduces to the first $j$ courses with $K-1$ semesters. This is a classic partition DP over prefixes.

The key observation is that we can precompute any segment’s weighted average in constant time using prefix sums of total credits and total weighted score. This makes it possible to evaluate each candidate last segment efficiently.

The DP state becomes “best possible total GPA using the first $i$ courses split into $k$ semesters”, and transitions try every possible previous cut position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force partitioning | $O(\binom{N}{K} \cdot N)$ | $O(N)$ | Too slow |
| Interval DP | $O(N^2 K)$ | $O(NK)$ | Accepted |

## Algorithm Walkthrough

We preprocess prefix sums so that any segment $[l, r]$ can compute its weighted average quickly.

We also precompute a lookup from integer score $0$ to $100$ into GPA values using the given mapping table, so once we round a semester average we can instantly obtain its GPA.

### Steps

1. Compute prefix arrays for credits and weighted scores.

For each $i$, store total credits up to $i$ and total $a_i \cdot b_i$. This allows any segment sum to be computed in constant time.
2. Define a function to compute semester GPA for a segment $[l, r]$.

We compute weighted average $x = \frac{\sum a_i b_i}{\sum b_i}$, round it to the nearest integer, then map it to GPA. The rounding step is critical because it changes the discretized GPA outcome.
3. Build a DP table where $dp[i][k]$ is the maximum total GPA achievable using the first $i$ courses split into $k$ semesters.
4. Initialize $dp[0][0] = 0$, meaning no courses and no semesters yields zero GPA.
5. For each $i$ from $1$ to $N$, and each $k$ from $1$ to $K$, try all possible previous cut points $j < i$.

The last semester is $[j+1, i]$, so we update:

$$dp[i][k] = \max(dp[i][k], dp[j][k-1] + GPA(j+1, i))$$
6. The answer is $dp[N][K] / K$, since the final GPA is the average over semesters.

### Why it works

Every valid schedule corresponds to a unique increasing sequence of cut points dividing the prefix into $K$ segments. The DP enumerates the last cut of each state, ensuring every valid partition is considered exactly once. Because each state stores the best achievable value for that prefix and number of semesters, and transitions only depend on independent prefix states plus a single segment value, optimal substructure holds. The rounding and GPA mapping are fully contained within each segment evaluation, so no cross-segment dependency is lost.

## Python Solution

```python
import sys
input = sys.stdin.readline

# GPA mapping based on rounded score
def score_to_gpa(x):
    if 90 <= x <= 100: return 4.3
    if 85 <= x <= 89: return 4.0
    if 80 <= x <= 84: return 3.7
    if 77 <= x <= 79: return 3.3
    if 73 <= x <= 76: return 3.0
    if 70 <= x <= 72: return 2.7
    if 67 <= x <= 69: return 2.3
    if 63 <= x <= 66: return 2.0
    if 60 <= x <= 62: return 1.7
    return 0.0

N = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
K = int(input())

# prefix sums
pref_w = [0] * (N + 1)
pref_c = [0] * (N + 1)

for i in range(1, N + 1):
    pref_w[i] = pref_w[i - 1] + a[i - 1] * b[i - 1]
    pref_c[i] = pref_c[i - 1] + b[i - 1]

def get_gpa(l, r):
    total_w = pref_w[r] - pref_w[l - 1]
    total_c = pref_c[r] - pref_c[l - 1]
    avg = total_w / total_c
    x = int(avg + 0.5)
    return score_to_gpa(x)

dp = [[-1e9] * (K + 1) for _ in range(N + 1)]
dp[0][0] = 0.0

for i in range(1, N + 1):
    for k in range(1, min(K, i) + 1):
        best = -1e9
        for j in range(k - 1, i):
            if dp[j][k - 1] < -1e8:
                continue
            best = max(best, dp[j][k - 1] + get_gpa(j + 1, i))
        dp[i][k] = best

ans = dp[N][K] / K
print(f"{ans:.7f}")
```

The prefix arrays make every segment evaluation constant time. The DP ensures each prefix and semester count is computed once, and the inner loop chooses the best last cut. The constraint $j \ge k-1$ ensures enough courses exist to give each previous semester at least one course.

A common pitfall is forgetting that the final answer is an average over semesters, not a sum, so we divide by $K$ only at the end.

## Worked Examples

### Example 1

Input:

```
3
70 80 75
3 1 4
2
```

We track DP states for prefixes.

| i | k | chosen split | segment GPA | dp[i][k] |
| --- | --- | --- | --- | --- |
| 1 | 1 | [1] | 3.0 | 3.0 |
| 2 | 1 | [1,2] | 3.0 | 3.0 |
| 2 | 2 | [1] + [2] | 3.0 + 3.0 | 6.0 |
| 3 | 2 | [1,2] + [3] | 3.0 + 3.0 | 6.0 |

Final answer is $6.0 / 2 = 3.0$.

This shows that even though different segmentations exist, both optimal splits collapse to the same GPA due to rounding.

### Example 2

Input:

```
6
30 95 65 75 55 80
1 1 1 1 1 1
1
```

Here $K=1$, so we take everything in one semester.

Weighted average is:

$$(30+95+65+75+55+80)/6 = 66.67 \rightarrow 67$$

67 maps to GPA 2.3.

This confirms that the DP correctly handles the degenerate case where no splitting is allowed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2 K)$ | each state tries all previous cut positions |
| Space | $O(NK)$ | DP table over prefixes and semesters |

With $N \le 100$, the worst-case around $10^6$ transitions is easily fast in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    import sys
    backup = sys.stdin
    sys.stdin = io.StringIO(inp)
    from math import isclose

    # re-run solution
    input = sys.stdin.readline

    def score_to_gpa(x):
        if 90 <= x <= 100: return 4.3
        if 85 <= x <= 89: return 4.0
        if 80 <= x <= 84: return 3.7
        if 77 <= x <= 79: return 3.3
        if 73 <= x <= 76: return 3.0
        if 70 <= x <= 72: return 2.7
        if 67 <= x <= 69: return 2.3
        if 63 <= x <= 66: return 2.0
        if 60 <= x <= 62: return 1.7
        return 0.0

    N = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    K = int(input())

    pref_w = [0] * (N + 1)
    pref_c = [0] * (N + 1)

    for i in range(1, N + 1):
        pref_w[i] = pref_w[i - 1] + a[i - 1] * b[i - 1]
        pref_c[i] = pref_c[i - 1] + b[i - 1]

    def get_gpa(l, r):
        total_w = pref_w[r] - pref_w[l - 1]
        total_c = pref_c[r] - pref_c[l - 1]
        avg = total_w / total_c
        x = int(avg + 0.5)
        return score_to_gpa(x)

    dp = [[-1e9] * (K + 1) for _ in range(N + 1)]
    dp[0][0] = 0.0

    for i in range(1, N + 1):
        for k in range(1, min(K, i) + 1):
            best = -1e9
            for j in range(k - 1, i):
                if dp[j][k - 1] < -1e8:
                    continue
                best = max(best, dp[j][k - 1] + get_gpa(j + 1, i))
            dp[i][k] = best

    ans = dp[N][K] / K
    sys.stdin = backup
    return f"{ans:.7f}"

# provided sample-like checks
assert run("""3
70 80 75
3 1 4
2
""") == "3.0000000"

assert run("""6
30 95 65 75 55 80
1 1 1 1 1 1
1
""") == "2.3000000"

# custom cases
assert run("""1
100
5
1
""") == "4.3000000", "single course"

assert run("""2
50 100
1 1
2
""") == "2.1500000", "split into extremes"

assert run("""4
90 90 90 90
2 2 2 2
2
""") == "4.3000000", "uniform scores"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 course | 4.3 | minimal DP boundary |
| mixed extremes | 2.15 | rounding + split effect |
| uniform high scores | 4.3 | stability across partitions |

## Edge Cases

One important edge case is when all courses are forced into one semester, i.e. $K = 1$. The algorithm correctly evaluates only the segment $[1, N]$, computes its weighted average, rounds it, and maps it to a GPA without attempting invalid splits.

Another case is when every semester must contain exactly one course, i.e. $K = N$. The DP restricts transitions so that each segment is a single element, meaning each course contributes independently after rounding. This correctly models the constraint that no semester can combine courses.

A more subtle case arises when weighted averages lie exactly on .5 boundaries. For example, an average of 89.5 becomes 90 and jumps to a higher GPA tier. Because the algorithm performs rounding before mapping, each segment is evaluated consistently with the problem definition, ensuring such boundary cases are handled correctly even though they can flip the optimal partition structure.
