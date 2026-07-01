---
title: "CF 104453H - \u0421\u043a\u0430\u0437\u043e\u0447\u043d\u044b\u0435 \u0441\u043d\u044b"
description: "We are given a set of lines in the plane, each described by an equation of the form $y = A x + B$. No two lines are identical, so every pair is either parallel or intersects exactly once."
date: "2026-06-30T14:34:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104453
codeforces_index: "H"
codeforces_contest_name: "ICPC Central Russia Regional Qualyfing Round, 2021"
rating: 0
weight: 104453
solve_time_s: 62
verified: false
draft: false
---

[CF 104453H - \u0421\u043a\u0430\u0437\u043e\u0447\u043d\u044b\u0435 \u0441\u043d\u044b](https://codeforces.com/problemset/problem/104453/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of lines in the plane, each described by an equation of the form $y = A x + B$. No two lines are identical, so every pair is either parallel or intersects exactly once.

The task is to choose the line that intersects the fewest other lines, and output that minimum number of intersections.

Reframed more concretely, think of each line as a segmentless infinite straight track. Whenever two tracks are not parallel, they cross at exactly one point. For each track, we count how many other tracks it crosses, and we want the smallest such count across all tracks.

The input size goes up to $N = 10^5$. A direct pairwise comparison over all pairs would require about $10^{10}$ checks, which is far beyond what is feasible in a time limit of a few seconds. This immediately rules out quadratic approaches.

A key structural observation is that intersection depends only on slopes. Two lines $A_1 x + B_1$ and $A_2 x + B_2$ intersect if and only if $A_1 \ne A_2$. If slopes are equal, the lines are parallel and never intersect.

So for any line with slope $A$, its number of intersections is exactly $N - \text{count of lines with slope } A$.

Edge cases appear when many lines share the same slope. For example, if all lines have the same $A$, then no intersections occur and the answer is zero. If slopes are all distinct, every line intersects all others and the answer is $N - 1$. A naive approach that ignores multiplicities would incorrectly assume every pair intersects.

## Approaches

A brute-force solution checks every pair of lines and increments counters whenever slopes differ. This is correct because it directly simulates the definition of intersection. However, it performs $N(N-1)/2$ comparisons, which becomes about five billion operations when $N = 10^5$, which is not viable.

The key simplification comes from separating geometry from counting. Intersection does not depend on intercepts at all, only on whether slopes match. Instead of examining pairs, we only need to know how many times each slope appears.

Once we group lines by slope, we can compute the intersection count for each group in constant time: all lines outside the group intersect every line inside it. So for slope value $A$, the intersection count is $N - f(A)$, where $f(A)$ is its frequency.

This turns the problem into a frequency counting task over integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2)$ | $O(1)$ | Too slow |
| Optimal (frequency counting) | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

### Optimal Strategy

1. Read all lines and extract their slopes $A$. The intercept $B$ is irrelevant because it does not affect whether two lines intersect.
2. Count how many times each slope appears using a hash map or dictionary. This step compresses the geometry into frequency information.
3. For each slope group, compute the number of intersections for lines in that group as $N - f(A)$. This comes from the fact that only lines with the same slope fail to intersect.
4. Track the minimum of these values across all slope groups.
5. Output this minimum value.

### Why it works

Each line only fails to intersect lines with the same slope. Since all other slopes guarantee exactly one intersection, every line in a slope class has identical intersection count. Therefore, minimizing over lines is equivalent to minimizing over slope groups, and the expression $N - f(A)$ correctly captures all non-parallel interactions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    freq = {}

    for _ in range(n):
        a, b = map(int, input().split())
        freq[a] = freq.get(a, 0) + 1

    ans = n
    for cnt in freq.values():
        ans = min(ans, n - cnt)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution reads each line and immediately discards the intercept since it plays no role in intersections. The dictionary `freq` stores how many lines share each slope.

After processing input, we iterate over slope groups. For each group of size `cnt`, we compute `n - cnt`, representing how many lines have different slopes and therefore intersect the group. The minimum over all groups gives the desired answer.

A subtle point is initialization of `ans` as `n`. This is safe because the maximum possible intersections for any line is $n - 1$, and initializing higher or equal does not affect correctness.

## Worked Examples

### Sample 1

Input:

```
3
1 2
1 3
2 3
```

We compute slope frequencies:

| Step | Slope read | Frequency map |
| --- | --- | --- |
| 1 | 1 | {1: 1} |
| 2 | 1 | {1: 2} |
| 3 | 2 | {1: 2, 2: 1} |

Now compute intersection counts:

| Slope | Frequency | Intersections |
| --- | --- | --- |
| 1 | 2 | 3 - 2 = 1 |
| 2 | 1 | 3 - 1 = 2 |

Minimum is 1.

This shows that grouping identical slopes reduces their intersection count because parallel lines do not intersect.

### Sample 2

Input:

```
5
1 1
1 2
1 3
2 2
2 3
```

Slope frequencies:

| Step | Slope | Frequency map |
| --- | --- | --- |
| 1 | 1 | {1: 1} |
| 2 | 1 | {1: 2} |
| 3 | 1 | {1: 3} |
| 4 | 2 | {1: 3, 2: 1} |
| 5 | 2 | {1: 3, 2: 2} |

Intersection counts:

| Slope | Frequency | Intersections |
| --- | --- | --- |
| 1 | 3 | 5 - 3 = 2 |
| 2 | 2 | 5 - 2 = 3 |

Answer is 2.

This confirms that the optimal line is the one in the most frequent slope group.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | One pass to count slopes and one pass over unique slopes |
| Space | $O(N)$ | In worst case all slopes are distinct |

The algorithm easily fits within constraints for $N \le 10^5$. Both memory and runtime are linear, which is optimal since every input line must be read at least once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else capture(inp)

def capture(inp):
    old_in = sys.stdin
    old_out = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_in
    sys.stdout = old_out
    return out.strip()

# provided samples
assert capture("3\n1 2\n1 3\n2 3\n") == "1"
assert capture("5\n1 1\n1 2\n1 3\n2 2\n2 3\n") == "2"

# all equal slopes
assert capture("4\n1 0\n1 1\n1 2\n1 3\n") == "0"

# all distinct slopes
assert capture("4\n1 0\n2 0\n3 0\n4 0\n") == "3"

# mixed distribution
assert capture("6\n1 0\n1 1\n2 0\n2 1\n2 2\n3 0\n") == "3"

# minimum case
assert capture("1\n5 7\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal slopes | 0 | no intersections exist |
| all distinct slopes | n-1 | maximal intersection case |
| mixed distribution | computed minimum | correctness under imbalance |
| single line | 0 | boundary condition |

## Edge Cases

When all slopes are identical, the frequency map contains a single key with value $N$. For input like:

```
3
1 5
1 2
1 9
```

the algorithm computes `n - cnt = 3 - 3 = 0`, correctly reflecting that no intersections occur.

When all slopes are distinct, each frequency is 1. For:

```
3
1 0
2 0
3 0
```

each group yields `3 - 1 = 2`, so the answer is 2. This matches the fact that every line intersects all others.

When there is a dominant slope group, for example:

```
6
1 0
1 1
1 2
2 0
3 0
4 0
```

the largest group has size 3, giving `6 - 3 = 3`. The algorithm correctly identifies that lines in the densest slope group minimize intersections because they avoid the most parallel conflicts.
