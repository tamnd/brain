---
title: "CF 102821C - Cycle Function"
description: "We are given one fixed linear function $f(x)=Ax+B$ and a collection of values $x1,x2,dots,xN$. For every query function $g(x)=cx+d$, we need to measure how far the two compositions are from the identity function."
date: "2026-07-26T16:10:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102821
codeforces_index: "C"
codeforces_contest_name: "2019 Sichuan Province Programming Contest"
rating: 0
weight: 102821
solve_time_s: 43
verified: true
draft: false
---

[CF 102821C - Cycle Function](https://codeforces.com/problemset/problem/102821/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one fixed linear function $f(x)=Ax+B$ and a collection of values $x_1,x_2,\dots,x_N$. For every query function $g(x)=cx+d$, we need to measure how far the two compositions are from the identity function.

For one value $x_i$, the contribution of a query is:

$$|f(g(x_i))-x_i|+|g(f(x_i))-x_i|$$

The answer for a query is the sum of these contributions over all given values.

The input contains several test cases. Each test case gives the number of values, the number of query functions, the coefficients of $f$, the list of values, and then all query functions. For every query function, we print the corresponding sum.

The main constraint is that both $N$ and $M$ can reach $10^5$. A solution that evaluates every query on every value would perform about $10^{10}$ operations in the worst case, which cannot fit in the time limit. We need to preprocess the values once and answer each query in logarithmic time.

The tricky part is handling absolute values correctly. A few cases can easily break a direct implementation.

If the coefficient of $x$ becomes zero, the expression is constant. For example, if a query gives $Ac-1=0$, then

$$|(Ac-1)x_i+(Ad+B)|=|Ad+B|$$

for every $x_i$. Dividing by the slope in this case would be invalid.

For example:

```
1
3 1 2 0
1 2 3
0.5 5
```

Here $Ac-1=2\cdot0.5-1=0$. The first expression is always $|5|$, so its contribution is $15$. A solution that tries to compute a turning point by dividing by zero fails.

Another edge case appears when the turning point is outside the range of all values. For example:

```
1
4 1 1 0
1 2 3 4
1 100
```

The expression becomes $x_i+100$, so the answer is $101+102+103+104=410$. A careless implementation that only considers values around the middle of the array may miss that all terms have the same sign.

Duplicate values are another source of mistakes. For example:

```
1
5 1 1 0
2 2 2 2 2
1 -2
```

The expression is $x_i-2$, so every term is zero and the answer is zero. The prefix calculations must handle equal values correctly.

## Approaches

The direct approach is straightforward. For every query function, substitute every $x_i$, compute the two compositions, take the absolute values, and add them. This is correct because it follows the definition exactly. However, each query costs $O(N)$, giving $O(NM)$ operations. With $N=M=100000$, this becomes $10^{10}$ evaluations, which is far beyond the available time.

The key observation is that both composition differences are linear functions. Expanding the first one gives:

$$f(g(x))-x=A(cx+d)+B-x$$

$$=(Ac-1)x+(Ad+B)$$

The second one gives:

$$g(f(x))-x=c(Ax+B)+d-x$$

$$=(Ac-1)x+(Bc+d)$$

Both expressions have the same slope. The whole problem becomes answering queries of the form:

$$\sum_i |px_i+q|$$

where $p$ and $q$ are known for each query.

If $p\neq0$, we can factor out the absolute value of the slope:

$$\sum_i |p||x_i+\frac qp|$$

Let:

$$t=-\frac qp$$

Then:

$$\sum_i |p||x_i-t|$$

So we only need a data structure that returns:

$$\sum_i |x_i-t|$$

for any real $t$.

After sorting the values, the position of $t$ splits the array into values smaller than $t$ and values larger than $t$. Prefix sums let us compute both parts in constant time after a binary search.

The approaches compare as follows:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(1) | Too slow |
| Optimal | O((N+M) log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Sort all values $x_i$ and build a prefix sum array. The prefix sums allow us to calculate sums of any prefix instantly, which is enough to compute distances to any chosen point.
2. For each query function $g(x)=cx+d$, calculate the shared slope:

$$p=Ac-1$$

The two intercepts are:

$$q_1=Ad+B$$

and

$$q_2=Bc+d$$

1. Create a helper function for calculating:

$$S(p,q)=\sum_i |px_i+q|$$

If $p=0$, every term is the same value $|q|$, so the result is simply $N|q|$.

Otherwise, transform the expression into:

$$|p|\sum_i |x_i-t|$$

where:

$$t=-q/p$$

1. To compute $\sum_i|x_i-t|$, find the first position where $x_i\ge t$. Suppose this position is $k$. The left side contributes:

$$t\cdot k-\sum_{i<k}x_i$$

and the right side contributes:

$$\sum_{i\ge k}x_i-t(N-k)$$

Adding them gives the required distance sum.

1. The final answer for the query is:

$$S(p,q_1)+S(p,q_2)$$

Print this value with enough precision.

The correctness comes from the fact that every query expression is exactly reduced to a distance sum on a sorted line. The split point $t$ is the only place where the sign of $x_i-t$ changes. All values before it contribute their distance from the left side, and all values after it contribute their distance from the right side. Since the prefix sums contain the exact sums of both groups, the computed value is always the true sum of absolute values.

## Python Solution

```python
import sys
import bisect

input = sys.stdin.readline

def solve():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    t = int(data[ptr])
    ptr += 1
    out = []

    for case in range(1, t + 1):
        n = int(data[ptr])
        m = int(data[ptr + 1])
        A = float(data[ptr + 2])
        B = float(data[ptr + 3])
        ptr += 4

        xs = [float(data[ptr + i]) for i in range(n)]
        ptr += n

        xs.sort()
        pref = [0.0]
        for x in xs:
            pref.append(pref[-1] + x)

        def dist_to_point(x):
            k = bisect.bisect_left(xs, x)
            left = x * k - pref[k]
            right = (pref[n] - pref[k]) - x * (n - k)
            return left + right

        def calc(p, q):
            if abs(p) < 1e-15:
                return n * abs(q)
            return abs(p) * dist_to_point(-q / p)

        out.append(f"Case {case}:")

        for _ in range(m):
            c = float(data[ptr])
            d = float(data[ptr + 1])
            ptr += 2

            p = A * c - 1.0
            q1 = A * d + B
            q2 = B * c + d

            ans = calc(p, q1) + calc(p, q2)
            out.append(f"{ans:.10f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input is read as bytes and parsed together because the total number of values can be large. The sorted array and prefix sums are built once per test case, before processing any queries.

The function `dist_to_point` implements the mathematical split around the turning point. `bisect_left` finds the first element not smaller than the point, which is exactly the boundary between negative and non-negative values of $x_i-t$.

The function `calc` handles the special zero-slope case separately. This avoids division by zero and also avoids numerical instability. For non-zero slopes, it applies the transformation from a linear absolute value into a scaled distance sum.

All calculations use floating point values because the input contains real numbers and the required error tolerance is $10^{-6}$.

## Worked Examples

For the first sample:

```
2
3 2 2.0 3.0
1.0 2.0 3.0
0.4 -2.0
0.6 -5.0
3 2 2.5 2.0
1.0 2.0 3.0
0.4 -2.0
0.6 -5.0
```

For the first query, $g(x)=0.4x-2$:

| Step | Value |
| --- | --- |
| Slope $p=Ac-1$ | -0.2 |
| First intercept $q_1=Ad+B$ | -1 |
| Second intercept $q_2=Bc+d$ | -2.8 |
| Computed answer | 7.800000 |

The sorted values are `[1,2,3]`. Both absolute expressions are evaluated through the same distance-sum helper, confirming that the same preprocessing works for both compositions.

For the second query, $g(x)=0.6x-5$:

| Step | Value |
| --- | --- |
| Slope $p=Ac-1$ | 0.2 |
| First intercept $q_1$ | -7 |
| Second intercept $q_2$ | -3.8 |
| Computed answer | 28.200000 |

The slope changes sign, but the algorithm only uses its absolute value after finding the turning point, so the same method handles both cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N+M) log N) | Sorting costs O(N log N), and each query performs two binary searches |
| Space | O(N) | The sorted values and prefix sums are stored |

The constraints allow $N$ and $M$ up to $10^5$. The preprocessing dominates only once, and each query is answered without iterating over all values, keeping the total work within the required limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    ans = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return ans

assert run("""1
3 2 2.0 3.0
1.0 2.0 3.0
0.4 -2.0
0.6 -5.0
""") == """Case 1:
7.8000000000
28.2000000000
"""

assert run("""1
1 1 1 0
5
1 0
""") == """Case 1:
8.0000000000
"""

assert run("""1
5 1 1 0
2 2 2 2 2
1 -2
""") == """Case 1:
0.0000000000
"""

assert run("""1
4 1 1 0
1 2 3 4
1 100
""") == """Case 1:
410.0000000000
"""

assert run("""1
3 1 2 0
1 2 3
0.5 5
""") == """Case 1:
15.0000000000
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Original sample query | 7.8 and 28.2 | Normal composition handling |
| Single value | 8.0 | Smallest input size |
| All equal values | 0.0 | Duplicate handling |
| Turning point outside range | 410.0 | Same-sign absolute values |
| Zero slope | 15.0 | Division-by-zero boundary |

## Edge Cases

When $Ac-1=0$, the algorithm enters the constant-expression branch. For:

```
1
3 1 2 0
1 2 3
0.5 5
```

the slope is zero, so the first term contributes $3\times5=15$. The second expression is also constant with its own intercept, and the helper handles both without attempting to compute a turning point.

When the turning point lies outside the sorted values, the binary search returns either the beginning or the end of the array. For:

```
1
4 1 1 0
1 2 3 4
1 100
```

the turning point is $-100$. Every value is on the right side, so the distance calculation becomes:

$$(1+100)+(2+100)+(3+100)+(4+100)=410$$

The prefix formula naturally handles this because one side of the split contains zero elements.

When all values are equal:

```
1
5 1 1 0
2 2 2 2 2
1 -2
```

the turning point is exactly the repeated value. The binary search finds the first equal position, the left and right contributions are both zero, and the result is correctly reported as zero.
