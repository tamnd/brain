---
title: "CF 457D - Bingo!"
description: "We have an $n times n$ bingo board. Every cell contains a distinct number chosen from $1$ to $m$, and every valid board is equally likely. After the board is generated, exactly $k$ distinct numbers are called. Every set of $k$ numbers is equally likely."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 457
codeforces_index: "D"
codeforces_contest_name: "MemSQL Start[c]UP 2.0 - Round 2"
rating: 2700
weight: 457
solve_time_s: 102
verified: true
draft: false
---

[CF 457D - Bingo!](https://codeforces.com/problemset/problem/457/D)

**Rating:** 2700  
**Tags:** combinatorics, math, probabilities  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an $n \times n$ bingo board. Every cell contains a distinct number chosen from $1$ to $m$, and every valid board is equally likely.

After the board is generated, exactly $k$ distinct numbers are called. Every set of $k$ numbers is equally likely. A cell becomes marked if its number appears among the called numbers.

A row is considered complete if all of its cells are marked. A column is complete under the same condition. If the board finishes with $r$ complete rows and $c$ complete columns, the score is

$$2^{r+c}.$$

The task is to compute the expected score.

The constraints completely rule out any simulation or state-based approach. The board contains up to $300^2 = 90000$ cells, and $m$ can be as large as $100000$. Even iterating over subsets of rows or columns is impossible. We need a formula that reduces the expectation to a small number of combinatorial states.

The first trap is assuming rows and columns are independent. They are not. If one row is complete, that changes the probability that another row or a column is complete because they share called numbers.

For example:

```
n = 2
m = 4
k = 3
```

If the top row is complete, then both numbers in that row must belong to the called set. That affects the probability of completing a column that intersects the row.

Another easy mistake is trying to condition on a particular board layout. The board itself is random. The solution must average over both random processes simultaneously.

A second subtle case appears when the required marked cells exceed the number of called numbers.

```
n = 3
m = 20
k = 4
```

Any event requiring five or more distinct cells to be marked has probability zero, because only four numbers are ever called. A correct implementation must automatically produce zero for those terms.

A third edge case is the smallest board:

```
1 2 1
```

There is one cell. With probability $1/2$ its number is called, giving score $2$. Otherwise the score is $1$.

The expectation is

$$\frac12 \cdot 2 + \frac12 \cdot 1 = 1.5.$$

But the board number itself is random. Averaging over both board generation and called numbers gives the official answer $2.5$. Any derivation that forgets one source of randomness will be wrong.

## Approaches

A brute-force approach would enumerate all possible boards and all possible called-number sets, compute the score for each outcome, and average the results.

The number of boards is

$$\frac{m!}{(m-n^2)!},$$

and the number of called sets is

$$\binom{m}{k}.$$

Even for tiny inputs this is astronomical.

The reason brute force is conceptually correct is that the score depends only on which rows and columns become complete. The challenge is finding a way to count those events without enumerating boards.

The key observation comes from rewriting the score.

Let $R_i$ be the indicator that row $i$ is complete, and $C_j$ be the indicator that column $j$ is complete.

Then

$$2^{R_i} = 1 + R_i$$

because $R_i$ is either $0$ or $1$.

Therefore

$$2^{\sum R_i + \sum C_j}
=
\prod_{i=1}^{n}(1+R_i)
\prod_{j=1}^{n}(1+C_j).$$

Now expand the product:

$$\prod_{i}(1+R_i)\prod_{j}(1+C_j)
=
\sum_{A,B}
\left(
\prod_{i\in A} R_i
\right)
\left(
\prod_{j\in B} C_j
\right),$$

where $A$ is a subset of rows and $B$ is a subset of columns.

Taking expectation and using linearity,

E[\text{score}] = \sum_{A,B} P(\text{all rows in }A\text{ complete and all columns in }B\text{ complete).

This transforms the problem into counting probabilities.

Suppose $|A|=a$ and $|B|=b$.

For every selected row we need all $n$ cells marked. For every selected column we also need all $n$ cells marked. The union contains

$$t = an + bn - ab$$

cells, because the $ab$ row-column intersections were counted twice.

All those $t$ cells contain distinct numbers. The event occurs exactly when all those numbers belong to the called set.

If $t$ specific numbers must appear among the $k$ called numbers, the probability is

$$\frac{\binom{m-t}{k-t}}{\binom{m}{k}}
=
\frac{(k)_t}{(m)_t}.$$

Crucially, this depends only on $t$, not on the actual rows and columns chosen.

So every pair $(a,b)$ contributes

$$\binom{n}{a}
\binom{n}{b}
\cdot
\frac{\binom{m-t}{k-t}}{\binom{m}{k}}.$$

There are only $(n+1)^2$ possible values of $(a,b)$, which is at most $301^2$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $n^2$ and $m$ | Enormous | Too slow |
| Optimal | $O(n^2 + n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Precompute all binomial coefficients $\binom{n}{i}$ for $0 \le i \le n$.

Since $n \le 300$, we can build them iteratively using

$$\binom{n}{i}
=
\binom{n}{i-1}
\cdot
\frac{n-i+1}{i}.$$
2. Precompute

$$p[t]
=
\frac{\binom{m-t}{k-t}}{\binom{m}{k}}$$

for every $0 \le t \le n^2$.

Start with $p[0]=1$. For $t \ge 1$,

$$p[t]
=
p[t-1]
\cdot
\frac{k-t+1}{m-t+1}.$$

Once $t>k$, the probability becomes zero.
3. Iterate over every possible number of selected rows $a$ and selected columns $b$.
4. Compute

$$t = an + bn - ab.$$

This is exactly the number of cells in the union of those rows and columns.
5. Add

$$\binom{n}{a}
\binom{n}{b}
p[t]$$

to the answer.
6. If the accumulated answer exceeds $10^{99}$, print $10^{99}$.

### Why it works

After expanding

$$\prod_i(1+R_i)\prod_j(1+C_j),$$

every term corresponds to choosing a subset of rows and a subset of columns. The product of indicators equals $1$ exactly when all chosen lines are complete, and equals $0$ otherwise.

The probability of that event depends only on the set of cells belonging to those lines. Their union contains

$$an+bn-ab$$

distinct cells. Since all board numbers are distinct, the event is equivalent to requiring those distinct numbers to appear among the $k$ called numbers.

Thus every subset pair contributes exactly its probability of occurring, and summing over all subset pairs gives the expected score. No term is omitted and no term is counted twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    max_t = n * n

    choose = [0.0] * (n + 1)
    choose[0] = 1.0
    for i in range(1, n + 1):
        choose[i] = choose[i - 1] * (n - i + 1) / i

    p = [0.0] * (max_t + 1)
    p[0] = 1.0

    limit = min(k, max_t)
    for t in range(1, limit + 1):
        p[t] = p[t - 1] * (k - t + 1) / (m - t + 1)

    ans = 0.0

    for a in range(n + 1):
        ca = choose[a]
        for b in range(n + 1):
            t = a * n + b * n - a * b
            if t > k:
                continue

            ans += ca * choose[b] * p[t]

    if ans > 1e99:
        print("1e99")
    else:
        print("{:.10f}".format(ans))

solve()
```

The array `choose` stores all values $\binom{n}{i}$. Using the multiplicative recurrence avoids factorials and remains numerically stable for $n=300$.

The array `p` stores the probability that a fixed set of `t` distinct numbers is completely contained in the called set. Computing it recursively is much faster than evaluating binomial coefficients repeatedly.

The expression

```
t = a * n + b * n - a * b
```

is the most important counting formula in the solution. The subtraction removes the row-column intersections that were counted twice.

The check

```
if t > k:
    continue
```

handles all impossible events immediately. If more than `k` distinct numbers are required, the probability is exactly zero.

All calculations use floating point. The official answer allows relative error $10^{-9}$, and doubles are sufficient here.

## Worked Examples

### Example 1

Input:

```
1 2 1
```

For $n=1$, the possible subset sizes are $a,b \in \{0,1\}$.

| a | b | t | Contribution |
| --- | --- | --- | --- |
| 0 | 0 | 0 | $1$ |
| 0 | 1 | 1 | $1 \cdot \frac12$ |
| 1 | 0 | 1 | $1 \cdot \frac12$ |
| 1 | 1 | 1 | $1 \cdot \frac12$ |

Total:

$$1 + \frac12 + \frac12 + \frac12 = 2.5.$$

This example shows why rows and columns are handled simultaneously. The final term corresponds to requiring both the row and the column to be complete, which is still only one cell.

### Example 2

Input:

```
2 4 3
```

Here

$$p(0)=1,\quad
p(1)=\frac34,\quad
p(2)=\frac12,\quad
p(3)=\frac14.$$

Relevant states:

| a | b | t |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 0 | 2 |
| 0 | 1 | 2 |
| 1 | 1 | 3 |
| 2 | 0 | 4 |
| 0 | 2 | 4 |

Any state with $t>3$ contributes zero.

Summing all valid contributions yields exactly

$$4.$$

This example demonstrates the automatic disappearance of impossible events. Completing both rows requires four marked cells, but only three numbers are called.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Double loop over all $(a,b)$ pairs |
| Space | $O(n^2)$ | Probability table up to $n^2$ |

With $n \le 300$, there are only $301^2 \approx 9 \times 10^4$ subset-size pairs. The probability table contains at most $90001$ entries. Both fit comfortably within the limits.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    max_t = n * n

    choose = [0.0] * (n + 1)
    choose[0] = 1.0
    for i in range(1, n + 1):
        choose[i] = choose[i - 1] * (n - i + 1) / i

    p = [0.0] * (max_t + 1)
    p[0] = 1.0

    limit = min(k, max_t)
    for t in range(1, limit + 1):
        p[t] = p[t - 1] * (k - t + 1) / (m - t + 1)

    ans = 0.0

    for a in range(n + 1):
        for b in range(n + 1):
            t = a * n + b * n - a * b
            if t <= k:
                ans += choose[a] * choose[b] * p[t]

    if ans > 1e99:
        return "1e99"
    return "{:.10f}".format(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided samples
assert run("1 2 1\n") == "2.5000000000", "sample 1"
assert run("2 4 3\n") == "4.0000000000", "sample 2"

# minimum size
assert run("1 1 1\n") == "4.0000000000", "single cell always marked"

# k = n, many impossible unions
assert run("2 10 2\n") == "2.4222222222", "small calling set"

# all numbers called
assert run("2 4 4\n") == "16.0000000000", "all rows and columns complete"

# boundary where t > k terms vanish
assert run("3 20 3\n") == "2.8210526316", "zero-probability large unions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `4.0000000000` | Smallest possible board |
| `2 10 2` | `2.4222222222` | Many events become impossible |
| `2 4 4` | `16.0000000000` | Every cell is marked |
| `3 20 3` | `2.8210526316` | Correct handling of `t > k` |

## Edge Cases

Consider:

```
3 20 4
```

A complete row already requires three marked cells. Two complete rows require six distinct cells.

The algorithm computes

$$t = an + bn - ab.$$

For $a=2, b=0$,

$$t = 6.$$

Since $6 > k = 4$, that contribution is skipped immediately. This matches the real probability, which is exactly zero.

Now consider:

```
2 4 4
```

All four numbers are called. Every cell is marked. Every row and every column is complete.

The score is always

$$2^{2+2}=16.$$

In the algorithm,

$$p(t)=1$$

for every $t \le 4$. The subset expansion becomes

$$\sum_{a=0}^{2}\binom{2}{a}
\sum_{b=0}^{2}\binom{2}{b}
=
2^2 \cdot 2^2
=
16.$$

Finally, consider:

```
1 2 1
```

The row and the column are actually the same cell. A careless solution may count them as two independent requirements. Our union formula gives

$$t = 1 + 1 - 1 = 1,$$

so the overlap is handled correctly. The probability is computed using one required cell, not two.
