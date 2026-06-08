---
title: "CF 1886A - Sum of Three"
description: "We are given an integer $n$ and must split it into three numbers whose sum is exactly $n$. The three numbers must satisfy three conditions simultaneously. They must all be positive, they must all be distinct, and none of them may be divisible by $3$."
date: "2026-06-08T22:16:53+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1886
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 156 (Rated for Div. 2)"
rating: 800
weight: 1886
solve_time_s: 225
verified: false
draft: false
---

[CF 1886A - Sum of Three](https://codeforces.com/problemset/problem/1886/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms, math  
**Solve time:** 3m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an integer $n$ and must split it into three numbers whose sum is exactly $n$.

The three numbers must satisfy three conditions simultaneously. They must all be positive, they must all be distinct, and none of them may be divisible by $3$.

For each test case we only need to find one valid construction. If no such construction exists, we print `NO`.

The constraints are very small from an algorithmic perspective. Although $n$ can be as large as $10^9$, there are only up to $10^4$ test cases. Any solution that performs a constant amount of work per test case is effectively instantaneous. A brute force search over possible triples would be impossible because the search space grows roughly as $O(n^2)$ or worse, which is completely infeasible for values near $10^9$.

The tricky part is not efficiency but construction.

One edge case is when $n$ is very small. For example:

```
n = 4
```

The only positive distinct triples summing to $4$ would need to use numbers like $(1,1,2)$ or permutations of it, which are not distinct. The correct answer is `NO`.

Another important case is when the remaining third number becomes divisible by $3$.

Suppose we always choose $1$ and $2$ as the first two numbers. Then:

```
n = 9
```

would produce

```
1 + 2 + 6 = 9
```

but $6$ is divisible by $3$, so this construction is invalid. A solution that only uses $(1,2)$ would fail on all multiples of $3$.

A final subtle case is when the third number collides with one of the chosen numbers.

For example:

```
n = 6
```

Using $(1,2)$ gives

```
z = 3
```

which is divisible by $3$.

Using $(1,4)$ gives

```
z = 1
```

which is not distinct.

The correct answer is `NO`.

## Approaches

A brute force solution would try all triples $(x,y,z)$ with

$$x+y+z=n,$$

check that all numbers are positive, distinct, and not divisible by $3$, then stop when a valid triple is found.

This approach is correct because it explicitly examines every possibility. The problem is the size of the search space. Even fixing $z=n-x-y$, there are roughly $O(n^2)$ candidate pairs $(x,y)$. For $n=10^9$, this is completely impossible.

The key observation is that we do not need to search. We only need one valid construction.

The restriction involving divisibility by $3$ suggests working with small numbers whose remainders modulo $3$ are known.

Consider two cases.

If $n$ is not divisible by $3$, choose

$$x=1,\qquad y=2.$$

Neither number is divisible by $3$, and they are distinct. The third number is

$$z=n-3.$$

Since $n \not\equiv 0 \pmod 3$,

$$z \equiv n \pmod 3,$$

so $z$ is also not divisible by $3$.

If $n$ is divisible by $3$, the previous construction fails because $z=n-3$ would also be divisible by $3$. We need a different pair. Choose

$$x=1,\qquad y=4.$$

Then

$$z=n-5.$$

Because $n \equiv 0 \pmod 3$,

$$z \equiv -5 \equiv 1 \pmod 3,$$

so $z$ is not divisible by $3$.

The only remaining task is checking that $z$ stays positive and distinct from the chosen numbers. This fails only for small values such as $n=6$ and $n=9$, which have no valid answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $n$.
2. If $n \le 6$, print `NO`.

Any three distinct positive integers have minimum possible sum

$$1+2+3=6.$$

For $n<6$ a solution is impossible, and for $n=6$ the only distinct triple is $(1,2,3)$ which contains a multiple of $3$.
3. If $n \bmod 3 \ne 0$, choose

$$x=1,\quad y=2,\quad z=n-3.$$
4. Check whether

$$z>2.$$

This guarantees positivity and distinctness.
5. Print `YES` and the triple.
6. If $n \bmod 3 = 0$, choose

$$x=1,\quad y=4,\quad z=n-5.$$
7. If

$$z\le4,$$

print `NO`.

The only problematic multiple of $3$ larger than $6$ is $n=9$, which gives $z=4$ and violates distinctness.
8. Otherwise print `YES` and the triple.

### Why it works

For $n \not\equiv 0 \pmod 3$, the construction $(1,2,n-3)$ uses numbers that are all nonzero modulo $3$. Since $n-3 \equiv n \pmod 3$, the third number is also not divisible by $3$.

For $n \equiv 0 \pmod 3$, the construction $(1,4,n-5)$ works because $n-5 \equiv 1 \pmod 3$. Again none of the numbers are divisible by $3$.

The only failures occur when the third number becomes nonpositive or equal to one of the chosen values. Those cases are exactly the small values already rejected. Every larger valid case receives a correct construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())

    if n <= 6:
        print("NO")
        continue

    if n % 3 != 0:
        print("YES")
        print(1, 2, n - 3)
    else:
        z = n - 5

        if z == 1 or z == 4:
            print("NO")
        else:
            print("YES")
            print(1, 4, z)
```

The first branch handles numbers not divisible by three. The pair $(1,2)$ is fixed, and the remaining value automatically avoids divisibility by three.

The second branch handles multiples of three. The pair $(1,4)$ avoids the modulo-$3$ issue that breaks the first construction.

The only special failure is $n=9$, where the third value becomes $4$, making the numbers non-distinct. The condition `z == 1 or z == 4` catches all problematic cases. In practice, after the earlier `n <= 6` check, only `z == 4` can occur.

## Worked Examples

### Example 1

Input:

```
n = 10
```

| Step | Value |
| --- | --- |
| n | 10 |
| n % 3 | 1 |
| x | 1 |
| y | 2 |
| z | 7 |

Output:

```
YES
1 2 7
```

The third number is positive, distinct from the first two, and not divisible by $3$.

### Example 2

Input:

```
n = 15
```

| Step | Value |
| --- | --- |
| n | 15 |
| n % 3 | 0 |
| x | 1 |
| y | 4 |
| z | 10 |

Output:

```
YES
1 4 10
```

All three numbers are distinct, positive, and have remainders $1$, $1$, and $1$ modulo $3$.

### Example 3

Input:

```
n = 9
```

| Step | Value |
| --- | --- |
| n | 9 |
| n % 3 | 0 |
| x | 1 |
| y | 4 |
| z | 4 |

Since $z=4$, the numbers would not be distinct.

Output:

```
NO
```

This demonstrates the only nontrivial impossible case larger than $6$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per test case | Only a few arithmetic operations and comparisons |
| Space | $O(1)$ | No auxiliary data structures |

Even with $10^4$ test cases, the program performs only constant work for each one. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        if n <= 6:
            out.append("NO")
            continue

        if n % 3 != 0:
            out.append("YES")
            out.append(f"1 2 {n - 3}")
        else:
            z = n - 5
            if z == 1 or z == 4:
                out.append("NO")
            else:
                out.append("YES")
                out.append(f"1 4 {z}")

    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("4\n10\n4\n15\n9\n") == (
    "YES\n1 2 7\n"
    "NO\n"
    "YES\n1 4 10\n"
    "NO"
)

# minimum value
assert run("1\n1\n") == "NO"

# smallest valid non-multiple of 3
assert run("1\n7\n") == "YES\n1 2 4"

# smallest valid multiple of 3 after failure at 9
assert run("1\n12\n") == "YES\n1 4 7"

# maximum input
assert run("1\n1000000000\n") == "YES\n1 2 999999997"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `NO` | Minimum possible input |
| `7` | `YES 1 2 4` | Smallest valid construction |
| `12` | `YES 1 4 7` | Multiple of 3 using second pattern |
| `1000000000` | Valid triple | Largest allowed value |

## Edge Cases

Consider:

```
n = 6
```

The algorithm immediately rejects it because `n <= 6`. The only distinct positive triple summing to $6$ is $(1,2,3)$, and $3$ is divisible by $3$. The correct answer is `NO`.

Consider:

```
n = 9
```

The algorithm enters the multiple-of-three branch.

$$z = 9 - 5 = 4.$$

The triple would be $(1,4,4)$, which is not distinct. The algorithm prints `NO`, which is correct.

Consider:

```
n = 8
```

The algorithm uses the first construction.

$$(1,2,5).$$

All numbers are positive, distinct, and not divisible by $3$. The algorithm prints a valid answer.

Consider:

```
n = 999999999.
```

Since $n$ is divisible by $3$, the algorithm constructs

$$(1,4,999999994).$$

The third value is positive, distinct, and congruent to $1 \pmod 3$. All requirements are satisfied, demonstrating that the construction works even at the largest scales.
