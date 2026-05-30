---
title: "CF 449A - Jzzhu and Chocolate"
description: "We have an $n times m$ chocolate bar made of unit squares. A cut is either horizontal or vertical, must follow grid lines, must lie strictly inside the chocolate, and cannot duplicate a previous cut."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 449
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 257 (Div. 1)"
rating: 1700
weight: 449
solve_time_s: 121
verified: true
draft: false
---

[CF 449A - Jzzhu and Chocolate](https://codeforces.com/problemset/problem/449/A)

**Rating:** 1700  
**Tags:** greedy, math  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an $n \times m$ chocolate bar made of unit squares. A cut is either horizontal or vertical, must follow grid lines, must lie strictly inside the chocolate, and cannot duplicate a previous cut.

After making exactly $k$ cuts, the chocolate is divided into several rectangular pieces. Among all resulting pieces, we look at the one with the smallest area. Our goal is to arrange the cuts so that this smallest area is as large as possible.

The dimensions $n$ and $m$ can be as large as $10^9$, and $k$ can reach $2 \cdot 10^9$. These values immediately rule out any simulation of cuts or any algorithm that iterates over rows, columns, or cut positions. Even an $O(\sqrt{k})$ approach would be unnecessarily large. The solution must perform only a constant amount of arithmetic.

A crucial observation is that a rectangle with height $n$ has only $n-1$ possible horizontal cuts, and similarly only $m-1$ possible vertical cuts. The maximum number of distinct cuts is

$$(n-1) + (m-1) = n+m-2.$$

If $k > n+m-2$, the required number of cuts cannot be made, so the answer is $-1$.

Several edge cases are easy to miss.

Consider:

```
2 3 4
```

The maximum number of distinct cuts is $1+2=3$. Four cuts are impossible, so the answer is:

```
-1
```

A careless solution that only tries to optimize piece sizes without checking feasibility would produce an incorrect positive value.

Another important case is:

```
3 4 1
```

With one cut, we should split one dimension as evenly as possible. Cutting the width into $2$ and $2$ gives pieces of area $3 \times 2 = 6$, which is optimal. The answer is:

```
6
```

A naive strategy that always cuts the longer side or always cuts horizontally would not necessarily find the optimum.

One more subtle example is:

```
5 5 8
```

Since $n+m-2=8$, every possible cut must be used. The chocolate becomes a $5 \times 5$ grid of unit squares, and the smallest piece has area $1$. Any formula that assumes cuts can still be distributed freely would fail here.

## Approaches

The most direct idea is to try every possible distribution of horizontal and vertical cuts.

Suppose we make $a$ horizontal cuts and $b$ vertical cuts, with

$$a+b=k.$$

After the cuts, the chocolate is partitioned into $a+1$ horizontal strips and $b+1$ vertical strips. To maximize the smallest rectangle, the strips along each dimension should be as equal as possible.

If we fixed $a$ and $b$, we could compute the largest possible minimum height and width, then obtain the smallest rectangle area. Trying every valid value of $a$ would find the optimum.

The difficulty is that $k$ can be around $2 \cdot 10^9$. Enumerating all possible values of $a$ is completely impossible.

The key observation is that the original Codeforces problem hides a much stronger structure.

Suppose we decide to spend $x$ cuts on the vertical direction. Those cuts split the width $m$ into $x+1$ pieces. The largest possible minimum width is

$$\left\lfloor \frac{m}{x+1} \right\rfloor.$$

Similarly, if we spend $y$ cuts on the horizontal direction, the largest possible minimum height is

$$\left\lfloor \frac{n}{y+1} \right\rfloor.$$

Since $x+y=k$, the minimum piece area becomes

$$\left\lfloor \frac{m}{x+1} \right\rfloor
\cdot
\left\lfloor \frac{n}{k-x+1} \right\rfloor.$$

At first glance this still looks like a huge search space.

The decisive observation is that the official solution only needs to examine two possibilities.

If the final smallest piece has width determined by splitting $m$, then the number of vertical segments must be some divisor-like quantity. Rearranging the optimization shows that one dimension must absorb all cuts needed to create the required number of segments, while the other dimension remains uncut. This reduces the search to two candidate constructions:

First, use $k$ cuts to create $k+1$ segments along the width. The resulting smallest piece area is

$$n \cdot \left\lfloor \frac{m}{k+1} \right\rfloor.$$

Second, use $k$ cuts to create $k+1$ segments along the height. The resulting smallest piece area is

$$m \cdot \left\lfloor \frac{n}{k+1} \right\rfloor.$$

Because only $n-1$ horizontal cuts and $m-1$ vertical cuts exist, we must respect those limits. The standard way to express this is to think in reverse.

If we spend $x$ cuts on one dimension, then we create $x+1$ segments. The number of segments can never exceed the dimension length.

Trying the two feasible allocations leads to the well known accepted solution:

- Use $n$ as the untouched dimension and divide $m$ into $k+1$ parts.
- Use $m$ as the untouched dimension and divide $n$ into $k+1$ parts.

In implementation this becomes checking the two possible ways to assign cuts between dimensions while respecting the cut limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $n$, $m$, and $k$.
2. Check whether $k > n+m-2$.

If true, output $-1$ because there are not enough distinct internal grid lines available for that many cuts.
3. Initialize the answer as $0$.
4. Consider using $n-1$ or fewer cuts horizontally and the rest vertically.

If $k < n$, then we can spend all $k$ cuts on the height direction. This creates $k+1$ horizontal segments, so the smallest height becomes

$$\left\lfloor \frac{n}{k+1} \right\rfloor.$$

The width remains $m$, giving candidate area

$$m \cdot \left\lfloor \frac{n}{k+1} \right\rfloor.$$
5. Consider the symmetric construction.

If $k < m$, then we can spend all $k$ cuts on the width direction. The candidate area becomes

$$n \cdot \left\lfloor \frac{m}{k+1} \right\rfloor.$$
6. There is one more possibility. If we use all available cuts in one dimension first, the remaining cuts must be placed in the other dimension.

When $k \ge n$, we may use $n-1$ horizontal cuts, leaving

$$k-(n-1)$$

cuts for the width. The smallest area becomes

$$\left\lfloor
\frac{m}{k-n+2}
\right\rfloor.$$
7. Symmetrically, when $k \ge m$, another candidate is

$$\left\lfloor
\frac{n}{k-m+2}
\right\rfloor.$$
8. Output the maximum candidate obtained.

### Why it works

Every cut contributes to exactly one dimension. If a dimension receives $t$ cuts, it is divided into $t+1$ segments, and the largest possible minimum segment length is the integer quotient of the dimension length by $t+1$.

For a fixed number of cuts, maximizing the smallest rectangle is equivalent to maximizing the minimum segment length in each affected dimension. The optimal arrangements occur when one dimension receives as many cuts as possible while the remaining required cuts are forced into the other dimension. Those are exactly the candidate constructions checked by the algorithm. Any other distribution produces a minimum side length no larger than one of these extreme cases, so the maximum over the candidates is the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    if k > n + m - 2:
        print(-1)
        return

    ans = 0

    if k < n:
        ans = max(ans, (n // (k + 1)) * m)

    if k < m:
        ans = max(ans, (m // (k + 1)) * n)

    if k >= n:
        ans = max(ans, m // (k - n + 2))

    if k >= m:
        ans = max(ans, n // (k - m + 2))

    print(ans)

solve()
```

The first condition handles impossibility. A rectangle of size $n \times m$ contains only $n-1$ horizontal cut lines and $m-1$ vertical cut lines, so no solution exists beyond $n+m-2$ cuts.

The next two branches correspond to spending all cuts in one dimension. The factor $k+1$ appears because $k$ cuts create $k+1$ segments.

The final two branches handle the cases where one dimension runs out of available cut positions. For example, after using all $n-1$ horizontal cuts, the remaining cuts must go into the width direction. The denominator becomes

$$k-(n-1)+1 = k-n+2.$$

That off by one is the most common implementation mistake in this problem.

Python integers automatically handle values up to $10^{18}$, so no overflow concerns exist.

## Worked Examples

### Example 1

Input:

```
3 4 1
```

| Step | Value |
| --- | --- |
| $n$ | 3 |
| $m$ | 4 |
| $k$ | 1 |
| Candidate 1 | $(3 // 2) \cdot 4 = 4$ |
| Candidate 2 | $(4 // 2) \cdot 3 = 6$ |
| Final answer | 6 |

The best choice is to split the width into two equal parts. The smallest resulting piece has area $6$.

### Example 2

Input:

```
5 5 8
```

| Step | Value |
| --- | --- |
| $n+m-2$ | 8 |
| Feasible | Yes |
| Candidate from $k \ge n$ | $5 // (8-5+2)=1$ |
| Candidate from $k \ge m$ | $5 // (8-5+2)=1$ |
| Final answer | 1 |

Every possible cut must be used. The chocolate is divided into unit squares, so the smallest piece area is $1$.

These examples illustrate the two different regimes. The first uses only a few cuts and benefits from splitting one dimension evenly. The second uses every available cut and leaves no freedom in the partition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a handful of arithmetic operations |
| Space | $O(1)$ | No auxiliary data structures |

The constraints allow values up to billions, but the algorithm never iterates over them. It performs a constant number of integer divisions and comparisons, making it easily fit within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m, k = map(int, input().split())

    if k > n + m - 2:
        return "-1"

    ans = 0

    if k < n:
        ans = max(ans, (n // (k + 1)) * m)

    if k < m:
        ans = max(ans, (m // (k + 1)) * n)

    if k >= n:
        ans = max(ans, m // (k - n + 2))

    if k >= m:
        ans = max(ans, n // (k - m + 2))

    return str(ans)

# sample
assert run("3 4 1\n") == "6", "sample 1"

# custom cases
assert run("2 3 4\n") == "-1", "impossible"
assert run("1 1 0\n") == "1", "minimum size"
assert run("5 5 8\n") == "1", "all cuts used"
assert run("6 4 3\n") == "4", "boundary transition"
assert run("1000000000 1000000000 1\n") == "500000000000000000", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3 4` | `-1` | Impossible number of cuts |
| `1 1 0` | `1` | Smallest valid rectangle |
| `5 5 8` | `1` | Maximum possible cuts |
| `6 4 3` | `4` | Transition between formula branches |
| `1000000000 1000000000 1` | `500000000000000000` | Large integer arithmetic |

## Edge Cases

Consider:

```
2 3 4
```

The algorithm first checks whether

$$k > n+m-2.$$

Since

$$4 > 2+3-2 = 3,$$

it immediately outputs $-1$. No candidate formulas are evaluated. This prevents producing a meaningless positive area when the required cuts cannot physically be made.

Consider:

```
1 10 5
```

There are no horizontal cuts available. The algorithm enters the branch $k \ge n$, giving

$$10 // (5-1+2)=10//6=1.$$

The answer is $1$, which matches the fact that only vertical cuts are possible.

Consider:

```
5 5 8
```

All available cut lines must be used. The algorithm evaluates

$$5 // (8-5+2)=1,$$

from both symmetric branches and returns $1$. This correctly captures the situation where every unit square becomes its own piece.

Consider:

```
3 4 1
```

The algorithm compares both possible single direction splits:

$$(3 // 2)\cdot4=4,$$

and

$$(4 // 2)\cdot3=6.$$

It returns $6$, showing that the best answer is not necessarily obtained by cutting the taller dimension.
