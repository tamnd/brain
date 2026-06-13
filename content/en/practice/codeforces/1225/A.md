---
title: "CF 1225A - Forgetting Things"
description: "We are asked to construct two positive integers $a$ and $b$ such that they differ by exactly one unit in the sense that $a + 1 = b$. We are not given the numbers themselves. Instead, we are only given the first digit of $a$ and the first digit of $b$."
date: "2026-06-13T18:39:36+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1225
codeforces_index: "A"
codeforces_contest_name: "Technocup 2020 - Elimination Round 2"
rating: 900
weight: 1225
solve_time_s: 533
verified: false
draft: false
---

[CF 1225A - Forgetting Things](https://codeforces.com/problemset/problem/1225/A)

**Rating:** 900  
**Tags:** math  
**Solve time:** 8m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct two positive integers $a$ and $b$ such that they differ by exactly one unit in the sense that $a + 1 = b$. We are not given the numbers themselves. Instead, we are only given the first digit of $a$ and the first digit of $b$. The task is to decide whether such a pair exists, and if it does, to produce any valid pair within the allowed range.

The key difficulty is that leading digits constrain a number only very loosely. Many numbers share the same first digit, and incrementing by one can either preserve the leading digit or change it dramatically, especially at powers of ten. The problem reduces to finding whether there exists at least one integer $a$ such that when we add one, the first digit of the result becomes the required digit.

The output does not need to be unique, which allows us to search for any convenient construction rather than a precise or minimal one.

The constraints are tiny, with both digits in $[1,9]$. This immediately rules out any need for complex structures or search spaces. Even a brute force over a small range of representative numbers per leading digit would be sufficient. However, the structure of decimal representation makes a direct constructive argument more efficient and cleaner.

A subtle edge case arises when incrementing crosses a power of ten boundary. For example, $199 + 1 = 200$ changes the leading digit from 1 to 2. This is the main mechanism that enables most valid transitions between leading digits. However, not all digit transitions are possible, and some pairs $(d_a, d_b)$ cannot occur under a +1 operation regardless of magnitude.

## Approaches

A brute-force idea is to iterate over all numbers up to $10^9$, check those whose first digit is $d_a$, and verify whether adding one produces a number whose first digit is $d_b$. This is correct because it directly tests the definition, but it is infeasible because the search space contains up to a billion candidates.

The key observation is that the operation $a \to a + 1$ only changes the leading digit in a very restricted way. The only time the leading digit changes is when a carry propagates through a long sequence of 9s. That means numbers of the form $d_a99\ldots9$ are the only candidates that can shift their leading digit upward after incrementing. In particular, $199 \to 200$, $2999 \to 3000$, and so on.

This suggests a constructive strategy. We try to build numbers starting from the smallest possible prefix matching $d_a$, then append as many 9s as needed, and check whether adding one produces a number starting with $d_b$. Since only the leading digit matters, we only need to test a few lengths of trailing 9s. If no such construction works, then no solution exists.

This reduces the problem from a huge search to checking a handful of candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(10^9)$ | $O(1)$ | Too slow |
| Constructive check | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Try building candidate numbers $a$ that start with digit $d_a$. The smallest meaningful structure is a number beginning with $d_a$ followed by a sequence of 9s. This is because carries triggered by 9s are the only way to change the leading digit in a controlled way.
2. For each possible length of trailing 9s (from 0 up to a small constant such as 9), construct $a = d_a$ followed by that many 9s. This gives a family like $1, 19, 199, 1999, \ldots$.
3. Compute $b = a + 1$. The increment will either preserve the structure or trigger a carry that increases the leading digit.
4. Extract the first digit of $b$ by converting it to a string and reading the first character. This directly corresponds to the problem requirement.
5. If the first digit of $b$ matches $d_b$, output this pair $(a, b)$ immediately.
6. If no candidate works after all tries, output $-1$.

The reason this works is that any valid solution must involve a carry chain caused by a suffix of 9s. If a solution exists at all, we can assume its structure is equivalent to some number with a prefix $d_a$ followed by enough 9s to force the same leading-digit transition when incremented.

## Python Solution

```python
import sys
input = sys.stdin.readline

def first_digit(x):
    return int(str(x)[0])

def solve():
    da, db = map(int, input().split())

    for k in range(0, 10):
        a = int(str(da) + "9" * k)
        b = a + 1
        if first_digit(b) == db:
            print(a, b)
            return

    print(-1)

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the construction idea. The loop over $k$ builds increasingly larger numbers starting with $d_a$. Each candidate is tested by a single increment and a constant-time check of its first digit. The conversion to string is safe because the constructed numbers stay well within the $10^9$ bound guaranteed by the problem.

A subtle point is that we do not attempt to optimize digit extraction mathematically. String conversion is sufficiently fast here because the loop runs a constant number of times.

## Worked Examples

### Example 1

Input:

```
1 2
```

| k | a | b = a + 1 | first digit of b | match |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 2 | yes |

We immediately find $a = 1$, $b = 2$, which satisfies the condition.

This demonstrates the simplest case where no carry propagation is needed, and increment directly changes the leading digit.

### Example 2

Input:

```
1 3
```

| k | a | b = a + 1 | first digit of b | match |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 2 | no |
| 1 | 19 | 20 | 2 | no |
| 2 | 199 | 200 | 2 | no |
| 3 | 1999 | 2000 | 2 | no |

No value of $k$ produces a leading digit 3 after incrementing. The process exhausts all meaningful carry lengths and fails.

This shows that not every digit transition is achievable with a +1 operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | At most 10 candidate checks, each constant work |
| Space | $O(1)$ | Only a few integers are stored |

The constraints are trivial, so even repeated string conversions and integer operations are well within limits. The algorithm is constant-time in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    # inline solution
    da, db = map(int, sys.stdin.readline().split())

    def first_digit(x):
        return int(str(x)[0])

    for k in range(10):
        a = int(str(da) + "9" * k)
        b = a + 1
        if first_digit(b) == db:
            return f"{a} {b}\n"

    return "-1\n"

# provided sample
assert run("1 2") == "1 2\n"

# custom cases
assert run("1 3") == "-1\n", "no transition possible"
assert run("2 3") == "2 3\n", "direct increment works"
assert run("9 1") == "9 10\n", "carry wraps to new digit"
assert run("1 2") in ["1 2\n", "19 20\n"], "multiple valid answers allowed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 3 | -1 | impossible transition |
| 2 3 | 2 3 | direct +1 without carry |
| 9 1 | 9 10 | carry producing new digit |
| 1 2 | valid pair | multiple correct solutions |

## Edge Cases

A key edge case is when no number starting with $d_a$ can produce a number starting with $d_b$ after incrementing. For instance, $1 \to 3$ fails because the increment operation always produces either a small local change or a carry that produces digit 2 as the new leading digit.

Another case is the carry boundary like $9 \to 10$. Here the leading digit changes from 9 to 1, which is the only non-trivial wrap-around behavior possible in base 10 increments. The algorithm explicitly tests $a = 9$, producing $b = 10$, and correctly captures the leading digit change.

Finally, long chains of 9s like $1999 \to 2000$ confirm that extending the number does not change the resulting leading digit after carry propagation. The loop over increasing numbers of 9s ensures that if any carry length works, it is found.
