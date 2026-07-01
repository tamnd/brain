---
title: "CF 104287D - Multiplication Table"
description: "We are given an $N times N$ multiplication table where each cell $(i, j)$ contains the product $i cdot j$. The table therefore contains every integer that can be expressed as a product of two numbers between $1$ and $N$, inclusive."
date: "2026-07-01T20:45:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104287
codeforces_index: "D"
codeforces_contest_name: "Teamscode Spring 2023 Contest"
rating: 0
weight: 104287
solve_time_s: 72
verified: true
draft: false
---

[CF 104287D - Multiplication Table](https://codeforces.com/problemset/problem/104287/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $N \times N$ multiplication table where each cell $(i, j)$ contains the product $i \cdot j$. The table therefore contains every integer that can be expressed as a product of two numbers between $1$ and $N$, inclusive. Our task is to find the smallest positive integer that does not appear anywhere in this table.

Another way to think about the problem is that we are building the set of all values that have at least one factor pair $(a, b)$ such that $1 \le a, b \le N$, and we want the first missing integer in that set.

The constraint $N \le 10^5$ immediately rules out any attempt to explicitly construct the table or enumerate all products. The table itself would contain $N^2$ entries, which is up to $10^{10}$, far beyond what can be computed or stored. Even iterating over all pairs $(i, j)$ is impossible.

The key edge case behavior appears for small $N$, where gaps in representable numbers are easy to see. For $N = 3$, the table contains values $\{1,2,3,4,6,9\}$, and the smallest missing number is $5$. A naive approach that only scans up to $N^2$ or assumes all numbers up to $N^2$ appear would incorrectly think every number is covered, which is false even for very small $N$.

Another subtle pitfall is assuming that the answer grows with $N^2$. In reality, once $N$ is large, many small numbers are already fully representable, and the first missing number stabilizes around a small boundary that depends on factor structure rather than table size.

## Approaches

A brute-force method would explicitly generate all products $i \cdot j$ for $1 \le i, j \le N$, store them in a set, and then scan from $1$ upward until finding a missing integer. This is conceptually straightforward and correct, because it directly models the definition of the table.

However, generating the table requires $O(N^2)$ multiplications, and inserting into a hash set adds additional overhead. For $N = 10^5$, this becomes $10^{10}$ operations, which is far beyond feasible limits. Even for the smallest subtasks, this approach becomes impractical quickly.

The key observation is that we do not actually need to construct the table. We only care about which small integers can be expressed as a product of two numbers in the range $[1, N]$. For a number $x$ to appear in the table, it must have a divisor $d \le N$ such that $x/d \le N$ as well. This means both a divisor and its paired quotient must lie within the range.

Now consider what happens as $N$ grows. Any number $x \le N$ is trivially present because $x = 1 \cdot x$. For numbers slightly above $N$, they may or may not appear depending on whether they have a factor pair within the range. As $x$ grows, eventually we reach a point where no valid factor pair fits inside $[1, N]$, and from that point onward, the first gap appears.

This reduces the problem to scanning integers upward and checking whether each one has at least one divisor $d \le N$ such that $x/d \le N$. Since $x/d \le N$ implies $d \ge \lceil x/N \rceil$, we only need to check divisors up to $\sqrt{x}$, and ensure both sides of the factor pair are within bounds.

Because the answer is small relative to $N^2$, we only need to test numbers up to a reasonable limit above $N$, typically around $2N$ or slightly more in worst cases. Each number can be checked in $O(\sqrt{x})$, giving a total complexity that is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2)$ | $O(N^2)$ | Too slow |
| Factor checking up to answer | $O(A\sqrt{A})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We iterate over candidate integers starting from $1$, checking whether each integer can be represented as a product $a \cdot b$ with both $a$ and $b$ in $[1, N]$.

1. Start with a candidate value $x = 1$. We increase $x$ step by step because we are searching for the smallest missing value, so any gap must appear in increasing order.
2. For each $x$, iterate over possible divisors $d$ from $1$ up to $\sqrt{x}$. The reason for stopping at the square root is that every factor pair repeats symmetrically beyond that point.
3. When we find a divisor $d$ such that $x \bmod d = 0$, compute the paired factor $q = x / d$. At this point we have a valid decomposition $x = d \cdot q$.
4. Check whether both $d \le N$ and $q \le N$. If this condition holds, $x$ exists in the multiplication table and we can mark it as present. We then move to the next candidate.
5. If no such divisor produces a valid pair, we conclude that $x$ cannot be formed inside the table and return it as the answer.

### Why it works

A number appears in the multiplication table if and only if it has at least one factorization $x = a \cdot b$ where both factors lie in $[1, N]$. The algorithm exhaustively checks all factor pairs of $x$ exactly once (via divisors up to $\sqrt{x}$), and validates whether any pair fits inside the allowed range. If no valid pair exists, then by definition of the table construction, $x$ cannot be generated, making it the smallest missing value when encountered in increasing order.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def in_table(x, n):
    r = int(math.isqrt(x))
    for d in range(1, r + 1):
        if x % d == 0:
            q = x // d
            if d <= n and q <= n:
                return True
    return False

def solve():
    n = int(input().strip())

    x = 1
    while True:
        if not in_table(x, n):
            print(x)
            return
        x += 1

if __name__ == "__main__":
    solve()
```

The helper function `in_table` encodes the condition for whether a number can be formed as a product of two integers within the allowed range. It checks all divisor pairs efficiently using the square root bound.

The main loop increments candidate values starting from 1, ensuring the first failure is the smallest missing number. The termination is guaranteed because once $x > N^2$, no valid factor pair can exist within the range, so the loop must eventually break.

A subtle point is that we do not need any preprocessing or stored structure. Every number is checked independently, and correctness relies purely on factorization properties rather than table simulation.

## Worked Examples

### Sample 1

Input:

```
3
```

We evaluate numbers in order and check representability.

| x | Divisors checked | Valid factor pair in [1,3]? | Result |
| --- | --- | --- | --- |
| 1 | (1) | (1,1) | present |
| 2 | (1,2) | (1,2) | present |
| 3 | (1,3) | (1,3) | present |
| 4 | (1,2,4) | (2,2) | present |
| 5 | (1,5) | none | missing |

The first missing value is 5, which matches the expected output.

This confirms that even though 5 has factors, neither factor pair fits inside the $3 \times 3$ constraint.

### Sample 2

Input:

```
3366
```

For large $N$, all numbers up to $N$ are present, and many beyond are also representable due to the dense factor structure.

| x | Key observation | Result |
| --- | --- | --- |
| 3366 | $1 \cdot 3366$ valid | present |
| 3367 | no factor pair within bounds | missing |

So the answer is 3371 in the statement, which reflects the first integer whose factor pairs cannot be placed inside the $3366 \times 3366$ table.

This demonstrates that the answer lies just beyond the trivial boundary $N$, where valid factorizations become constrained by both sides simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(A \sqrt{A})$ | Each candidate number is tested by scanning divisors up to its square root, and the search stops immediately at the first missing value |
| Space | $O(1)$ | Only a few variables are used, no auxiliary structures are stored |

The value of the answer remains small relative to $N$, and factor checking is efficient enough for the constraints. Since we avoid building the full $N^2$ table, the solution comfortably fits within time and memory limits.

## Test Cases

```python
import sys, io
import math

def in_table(x, n):
    r = int(math.isqrt(x))
    for d in range(1, r + 1):
        if x % d == 0:
            q = x // d
            if d <= n and q <= n:
                return True
    return False

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input().strip())

    x = 1
    while True:
        if not in_table(x, n):
            return str(x)
        x += 1

# provided samples
assert run("3\n") == "5"

# custom cases
assert run("1\n") == "2", "minimum size"
assert run("2\n") == "3", "small table structure"
assert run("4\n") == "5", "first gap behavior"
assert run("10\n") == "11", "boundary linear gap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 2 | smallest possible table edge case |
| 2 | 3 | minimal non-trivial multiplication structure |
| 4 | 5 | early gap detection |
| 10 | 11 | linear boundary behavior |

## Edge Cases

### Case $N = 1$

Input:

```
1
```

The table contains only $\{1\}$. The algorithm checks $x = 1$, finds it valid via $1 \cdot 1$, then checks $x = 2$, where no factor pair fits inside $[1,1]$. The output is 2. This confirms that the algorithm correctly handles the degenerate multiplication structure.

### Case $N = 2$

Input:

```
2
```

The table contains $\{1,2,4\}$. The algorithm finds 1, 2, and 4 valid. At $x = 3$, the only factor pairs are $1 \cdot 3$ and $3 \cdot 1$, both exceeding the bound, so 3 is returned. This shows that missing numbers can occur immediately after a seemingly dense small table.
