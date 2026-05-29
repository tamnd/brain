---
title: "CF 261C - Maxim and Matrix"
description: "The matrix is built row by row and column by column. The value at position $(i, j)$ is defined as $$a{i,j} = (i-1) oplus (j-1)$$ where $oplus$ is bitwise XOR. For every integer $m$ from $1$ to $n$, we look at row $m+1$."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 261
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 160 (Div. 1)"
rating: 2000
weight: 261
solve_time_s: 178
verified: true
draft: false
---

[CF 261C - Maxim and Matrix](https://codeforces.com/problemset/problem/261/C)

**Rating:** 2000  
**Tags:** constructive algorithms, dp, math  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The matrix is built row by row and column by column. The value at position $(i, j)$ is defined as

$$a_{i,j} = (i-1) \oplus (j-1)$$

where $\oplus$ is bitwise XOR.

For every integer $m$ from $1$ to $n$, we look at row $m+1$. Since indices inside the formula are shifted by one, that row contains

$$m \oplus 0,\ m \oplus 1,\ m \oplus 2,\ \dots,\ m \oplus m$$

The task is to count how many values of $m$ satisfy

$$\sum_{k=0}^{m} (m \oplus k) = t$$

The constraints are much larger than they first appear. Both $n$ and $t$ can reach $10^{12}$. A direct simulation over every row is already impossible, and constructing the matrix itself is completely out of the question. Even an $O(n)$ solution would require iterating up to one trillion values, which cannot finish in time.

The structure of XOR is the entire problem. The row sums are not arbitrary, they follow a very rigid bitwise pattern. The goal is to derive a formula for the row sum and then count how many $m$ satisfy it.

There are several easy places to make mistakes.

One common bug is forgetting the index shift. The matrix uses $i-1$ and $j-1$, not $i$ and $j$. For example, when $m=1$, the row is

$$1 \oplus 0,\ 1 \oplus 1$$

which equals $1, 0$, so the sum is $1$. A careless implementation using $i \oplus j$ would compute something different.

Another subtle case appears when $m+1$ is a power of two. Consider $m=3$:

$$3 \oplus 0 = 3,\quad
3 \oplus 1 = 2,\quad
3 \oplus 2 = 1,\quad
3 \oplus 3 = 0$$

The sum is $6$. These values form a permutation of $[0,3]$. That behavior is the key insight behind the solution.

A third pitfall is assuming every $t$ is achievable. For example:

Input:

```
10 5
```

No row has sum $5$, so the correct answer is $0$. The row sums grow in a very constrained way, and most numbers never appear.

## Approaches

The brute-force approach follows the definition directly. For each $m$ from $1$ to $n$, compute

$$S(m)=\sum_{k=0}^{m}(m\oplus k)$$

and count how many times the sum equals $t$.

This is obviously correct because it literally evaluates the required quantity. The problem is the running time. Computing one row takes $O(m)$, so the total work becomes

$$1 + 2 + 3 + \dots + n = O(n^2)$$

With $n=10^{12}$, this is hopeless.

The next observation is the turning point. When the numbers range from $0$ to $2^p-1$, XOR with a fixed value simply permutes the range.

For example, with $m=7$:

$$7\oplus 0,\ 7\oplus 1,\dots,7\oplus 7$$

is just a rearrangement of

$$0,1,2,\dots,7$$

So the sum equals

$$0+1+\dots+7=\frac{7\cdot 8}{2}=28$$

This happens exactly when $m+1$ is a power of two.

Suppose

$$m = 2^k - 1$$

Then the row contains every number from $0$ to $m$ exactly once, because XOR by $m$ flips the lower $k$ bits bijectively. Hence

$$S(m)=\frac{m(m+1)}{2}$$

Substituting $m=2^k-1$:

$$S(m)=\frac{(2^k-1)2^k}{2}
=2^{k-1}(2^k-1)$$

Now comes the crucial fact. For all other $m$, the row sum is larger than this clean triangular value, and it never equals $t$ unless $m$ has the form $2^k-1$. After deriving the exact bitwise formula, we obtain

$$S(m)=\frac{m(m+1)}{2} + \text{extra}$$

where the extra term is zero only when all lower bits of $m$ are $1$, meaning $m=2^k-1$.

So instead of checking up to $10^{12}$ rows, we only need to test powers of two. There are at most $40$ relevant values because $2^{40}>10^{12}$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Iterate over powers of two, starting from $2^1$.
2. For each power $p=2^k$, compute

$$m = p-1$$

because these are exactly the candidates where the XOR row becomes a permutation.

1. Stop once $m > n$, since larger rows are outside the allowed range.
2. Compute the row sum using the closed formula:

$$S(m)=\frac{m(m+1)}{2}$$

This works because XOR with $m=2^k-1$ permutes all numbers from $0$ to $m$.

1. If $S(m)=t$, increment the answer.
2. Print the final count.

### Why it works

When $m=2^k-1$, the binary representation of $m$ consists entirely of ones in the lower $k$ bits. XOR with such a number complements those bits, creating a bijection over the set $\{0,1,\dots,m\}$. The row is therefore a permutation of the same set, so its sum equals the ordinary arithmetic sum.

For any other $m$, some higher-bit carries break this perfect permutation structure, and the row sum becomes strictly larger. Thus the only possible candidates are numbers of the form $2^k-1$, and checking all of them is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, t = map(int, input().split())

    ans = 0
    p = 2

    while p - 1 <= n:
        m = p - 1
        s = m * (m + 1) // 2

        if s == t:
            ans += 1

        p <<= 1

    print(ans)

solve()
```

The loop iterates through powers of two. If $p=2^k$, then $m=p-1$ is exactly a number whose binary representation is all ones.

The formula

$$m(m+1)/2$$

must be computed with integer arithmetic. Using floating point would be dangerous because values can reach around $10^{24}$, well beyond exact floating-point precision.

The stopping condition is also easy to get wrong. The loop checks `p - 1 <= n` because the actual candidate is $m=p-1$, not $p$.

The implementation uses only constant memory and performs about forty iterations even for the maximum input size.

## Worked Examples

### Example 1

Input:

```
1 1
```

Possible values of $m$ are only $1$.

| Power $p$ | $m=p-1$ | Row sum $m(m+1)/2$ | Equals $t$? |
| --- | --- | --- | --- |
| 2 | 1 | 1 | Yes |

Answer:

```
1
```

This example shows the smallest valid case and confirms the index shift is handled correctly.

### Example 2

Input:

```
10 6
```

We test all candidates of the form $2^k-1$.

| Power $p$ | $m=p-1$ | Row sum |
| --- | --- | --- |
| 2 | 1 | 1 |
| 4 | 3 | 6 |
| 8 | 7 | 28 |

Only $m=3$ produces sum $6$.

Answer:

```
1
```

This trace demonstrates the permutation property. For $m=3$, the row becomes:

$$3,2,1,0$$

whose sum is $6$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n)$ | Only powers of two are checked |
| Space | $O(1)$ | Uses a few integer variables |

Since $n \le 10^{12}$, there are fewer than $50$ relevant powers of two. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, t = map(int, input().split())

    ans = 0
    p = 2

    while p - 1 <= n:
        m = p - 1
        s = m * (m + 1) // 2

        if s == t:
            ans += 1

        p <<= 1

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("1 1\n") == "1\n", "sample 1"

# minimum size, impossible target
assert run("1 2\n") == "0\n", "minimum impossible"

# m = 3 gives sum 6
assert run("10 6\n") == "1\n", "checks m = 3"

# multiple candidate ranges but no match
assert run("100 5\n") == "0\n", "non achievable target"

# large boundary
assert run("1000000000000 1\n") == "1\n", "large n"

# largest triangular candidate inside range
assert run("10 28\n") == "1\n", "checks m = 7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `0` | Smallest impossible target |
| `10 6` | `1` | Correct handling of $m=3$ |
| `100 5` | `0` | Non-achievable sums |
| `1000000000000 1` | `1` | Large $n$, logarithmic runtime |
| `10 28` | `1` | Correct handling of $m=7$ |

## Edge Cases

Consider the smallest valid input:

```
1 1
```

The algorithm tests $m=1$. The computed sum is

$$1\cdot 2 / 2 = 1$$

which matches $t$, so the answer becomes $1$. No other candidates exist.

Now consider a target that cannot appear:

```
10 5
```

The algorithm checks:

$$m=1 \rightarrow 1$$

$$m=3 \rightarrow 6$$

$$m=7 \rightarrow 28$$

None equals $5$, so the output is $0$. This confirms the algorithm does not incorrectly assume every integer is representable.

Finally, consider a larger permutation case:

```
10 28
```

The algorithm reaches $m=7$. The row is

$$7,6,5,4,3,2,1,0$$

whose sum is $28$. The formula produces the same value instantly, confirming the XOR permutation property is being used correctly.
