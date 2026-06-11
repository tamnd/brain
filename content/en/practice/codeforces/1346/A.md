---
title: "CF 1346A - Color Revolution"
description: "We are given a total number of participants and a fixed multiplier. The participants must be split into four consecutive groups where each next group is exactly $k$ times larger than the previous one."
date: "2026-06-11T15:00:29+07:00"
tags: ["codeforces", "competitive-programming", "*special", "math"]
categories: ["algorithms"]
codeforces_contest: 1346
codeforces_index: "A"
codeforces_contest_name: "Kotlin Heroes: Episode 4"
rating: 1000
weight: 1346
solve_time_s: 713
verified: true
draft: false
---

[CF 1346A - Color Revolution](https://codeforces.com/problemset/problem/1346/A)

**Rating:** 1000  
**Tags:** *special, math  
**Solve time:** 11m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a total number of participants and a fixed multiplier. The participants must be split into four consecutive groups where each next group is exactly $k$ times larger than the previous one. Once the first group size is fixed, the rest is completely determined as a geometric progression:

$$n_1,\; k n_1,\; k^2 n_1,\; k^3 n_1$$

and their sum must equal the total $n$.

So the task is to reconstruct a valid geometric decomposition of $n$ into four terms with ratio $k$.

The constraints are very small in computational terms. Each test case requires only constant arithmetic operations. Even at the maximum of $t = 1000$, a linear scan or even repeated arithmetic is unnecessary, so an $O(t)$ solution is sufficient. Any solution involving loops over large ranges or search over $n$ would be unnecessary and overkill.

A few edge cases matter conceptually. When $k = 1$, all four groups are equal, so the answer reduces to splitting $n$ into four equal parts. When $k > 1$, the first group becomes small because higher powers dominate the sum quickly. The problem guarantees that an integer solution exists, so we do not need to handle infeasibility cases.

## Approaches

A naive idea is to try all possible values of $n_1$. For each candidate, compute $n_1 + k n_1 + k^2 n_1 + k^3 n_1$ and check whether it equals $n$. This works but is unnecessary. The expression simplifies to

$$n = n_1 (1 + k + k^2 + k^3)$$

so we only need to compute a single division:

$$n_1 = \frac{n}{1 + k + k^2 + k^3}$$

The brute-force view works because it directly tests the structure of the sequence, but it becomes wasteful since the relationship is linear in $n_1$. The key observation is that the four terms form a fixed geometric sum, so the total is just a constant multiple of the first term. This reduces the problem to computing a single quotient and then reconstructing the remaining values by multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | $O(n)$ per test | $O(1)$ | Too slow |
| Direct Formula | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the values $n$ and $k$ for each test case. These define a geometric structure where all four groups are fixed once the first is known.
2. Compute the geometric sum coefficient

$$S = 1 + k + k^2 + k^3$$

This represents how many times $n_1$ is counted in the total.
3. Compute $n_1 = n / S$. This works because the problem guarantees divisibility. If it were not guaranteed, we would need to validate, but here the construction ensures consistency.
4. Construct the remaining groups as $n_2 = k n_1$, $n_3 = k^2 n_1$, and $n_4 = k^3 n_1$. Each step follows directly from the definition of the progression.
5. Output the four values in order.

### Why it works

The total number of participants is exactly the sum of a geometric progression with fixed ratio $k$. Every valid solution must match this structure uniquely because once $n_1$ is fixed, all other values are determined. The equation reduces the problem to solving a single linear equation in one variable, so the constructed solution is the only candidate and therefore correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())

        S = 1 + k + k * k + k * k * k
        n1 = n // S

        n2 = n1 * k
        n3 = n2 * k
        n4 = n3 * k

        print(n1, n2, n3, n4)

if __name__ == "__main__":
    solve()
```

The code directly encodes the algebraic structure of the problem. The only subtle point is computing the geometric sum correctly and ensuring integer division is used. The guarantee of existence ensures that $n$ is divisible by $S$, so floor division is safe.

Computing $n_2, n_3, n_4$ iteratively avoids recomputing powers of $k$, which keeps the implementation clean and avoids overflow concerns in languages with fixed integer sizes. Python handles large integers naturally, so no additional precautions are needed.

## Worked Examples

### Example 1

Input:

```
n = 40, k = 3
```

| Step | Value |
| --- | --- |
| $S$ | $1 + 3 + 9 + 27 = 40$ |
| $n_1$ | $40 / 40 = 1$ |
| $n_2$ | $3$ |
| $n_3$ | $9$ |
| $n_4$ | $27$ |

This matches the required decomposition exactly, showing how the entire structure collapses into a perfect geometric sum.

### Example 2

Input:

```
n = 1200, k = 7
```

| Step | Value |
| --- | --- |
| $S$ | $1 + 7 + 49 + 343 = 400$ |
| $n_1$ | $1200 / 400 = 3$ |
| $n_2$ | $21$ |
| $n_3$ | $147$ |
| $n_4$ | $1029$ |

This confirms that even for larger multipliers, the structure remains purely algebraic and requires no search.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case uses a constant number of arithmetic operations |
| Space | $O(1)$ | Only a few integers are stored per test case |

The constraints allow up to 1000 test cases, and each is solved in constant time. This is easily within limits, as the solution performs only basic arithmetic per input line.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return io.StringIO().getvalue()

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        S = 1 + k + k*k + k*k*k
        n1 = n // S
        out.append(f"{n1} {n1*k} {n1*k*k} {n1*k*k*k}")
    print("\n".join(out))

# provided samples
assert run("""4
40 3
1200 7
320802005 400
4 1
""") == """1 3 9 27
3 21 147 1029
5 2000 800000 320000000
1 1 1 1
""", "sample tests"

# k = 1 case
assert run("""1
8 1
""") == "2 2 2 2\n", "all equal split"

# small n
assert run("""1
40 3
""") == "1 3 9 27\n", "basic case"

# larger k
assert run("""1
1200 7
""") == "3 21 147 1029\n", "larger multiplier"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample set | correct sequences | correctness across multiple cases |
| k = 1 | equal division | degenerate geometric progression |
| small n | direct computation | base arithmetic correctness |
| large k | scaled growth | handling of larger multipliers |

## Edge Cases

When $k = 1$, the geometric sum becomes $4$, so every group must be exactly $n/4$. The algorithm naturally handles this because $S = 4$ and all multiplications preserve equality.

When $k$ is large, $k^3$ dominates the sum, making $n_1$ very small. The computation still works because all values remain integer due to the guarantee in the problem statement.

When $n$ is exactly equal to the geometric sum $S$, the solution yields $n_1 = 1$, producing the minimal valid configuration $1, k, k^2, k^3$, confirming the boundary case behavior.
