---
title: "CF 130A - Hexagonal numbers"
description: "We need to compute the $n$-th hexagonal number. The sequence is defined by the formula $$hn = 2n^2 - n$$ The input contains a single integer $n$, and the output is the value produced by this formula."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 130
codeforces_index: "A"
codeforces_contest_name: "Unknown Language Round 4"
rating: 900
weight: 130
solve_time_s: 84
verified: true
draft: false
---

[CF 130A - Hexagonal numbers](https://codeforces.com/problemset/problem/130/A)

**Rating:** 900  
**Tags:** *special, implementation  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to compute the $n$-th hexagonal number. The sequence is defined by the formula

$$h_n = 2n^2 - n$$

The input contains a single integer $n$, and the output is the value produced by this formula.

For example, when $n = 2$,

$$h_2 = 2 \cdot 2^2 - 2 = 8 - 2 = 6$$

so the answer is `6`.

The constraints are extremely small. The largest possible value of $n$ is only $100$, so even a very slow algorithm would run instantly. The biggest hexagonal number we may compute is

$$2 \cdot 100^2 - 100 = 19900$$

which easily fits inside standard integer types.

The main risk in this problem is not performance, but implementing the formula incorrectly. A few common mistakes are easy to make.

One possible error is forgetting operator precedence. Consider the input

```
2
```

The correct calculation is

$$2 \cdot 2^2 - 2 = 6$$

A careless implementation like `2*n*n-n` is fine, but writing something such as `2*n^(2-n)` or confusing `^` with exponentiation in Python would produce a wrong result because Python uses `**` for powers.

Another common mistake is using the wrong formula. Some figurate number formulas look similar. For input

```
1
```

the correct output is

```
1
```

because

$$2 \cdot 1^2 - 1 = 1$$

If someone mistakenly uses $n^2$ or $3n^2-n$, the sequence becomes incorrect immediately.

## Approaches

A brute-force approach would be to build the hexagonal pattern layer by layer. The first figure contains $1$ cell, the next adds more cells around it, and so on until reaching the $n$-th layer. Since $n \le 100$, even simulating the construction directly would be fast enough.

For example, we could repeatedly add the number of cells contributed by each new layer and maintain a running total. This works because each step mirrors the geometric definition of hexagonal numbers.

The weakness of that method is that it performs unnecessary work. We already know the exact mathematical formula for the answer:

$$h_n = 2n^2 - n$$

Once we recognize that the sequence is given explicitly, there is no reason to simulate anything. We can compute the answer directly in constant time.

The optimal solution simply reads $n$, evaluates the formula, and prints the result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ | $O(1)$ | Accepted |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$ from input.
2. Compute the value

$$2n^2 - n$$

This directly matches the definition of the $n$-th hexagonal number given in the problem.

1. Print the computed value.

### Why it works

The problem defines the sequence explicitly by the formula

$$h_n = 2n^2 - n$$

The algorithm evaluates exactly this expression for the provided $n$. Since there are no approximations, iterations, or transformations involved, the produced value is precisely the required hexagonal number.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

answer = 2 * n * n - n

print(answer)
```

The program starts by reading the integer $n$. Since there is only one value, no loops or additional parsing are needed.

The expression

```
2 * n * n - n
```

computes $2n^2 - n$. Writing it this way avoids any confusion about exponent operators and keeps the arithmetic simple.

Python integers automatically handle values much larger than this problem requires, so overflow is impossible here.

Finally, the result is printed directly.

## Worked Examples

### Example 1

Input:

```
2
```

| Step | n | Computation | Result |
| --- | --- | --- | --- |
| Read input | 2 | - | - |
| Compute answer | 2 | $2 \cdot 2^2 - 2$ | 6 |
| Print | 2 | - | 6 |

This example confirms that the formula produces the sample answer exactly.

### Example 2

Input:

```
5
```

| Step | n | Computation | Result |
| --- | --- | --- | --- |
| Read input | 5 | - | - |
| Compute answer | 5 | $2 \cdot 5^2 - 5$ | 45 |
| Print | 5 | - | 45 |

This trace shows that the algorithm scales directly with the formula. No iteration or simulation is needed, regardless of the value of $n$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | The program performs a fixed number of arithmetic operations |
| Space | $O(1)$ | Only a few integer variables are stored |

The constraints are tiny, so constant-time arithmetic easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    print(2 * n * n - n)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    sys.stdout = out

    solve()

    return out.getvalue().strip()

# provided samples
assert run("2\n") == "6", "sample 1"

# custom cases
assert run("1\n") == "1", "minimum input"
assert run("3\n") == "15", "small odd value"
assert run("10\n") == "190", "two-digit input"
assert run("100\n") == "19900", "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum valid input |
| `3` | `15` | Correct arithmetic for small values |
| `10` | `190` | Formula works for larger numbers |
| `100` | `19900` | Maximum constraint value |

## Edge Cases

The smallest possible input is

```
1
```

The algorithm computes

$$2 \cdot 1^2 - 1 = 1$$

and prints

```
1
```

This confirms that the formula handles the lower boundary correctly without any special cases.

Another useful edge case is the maximum allowed input:

```
100
```

The computation becomes

$$2 \cdot 100^2 - 100
= 2 \cdot 10000 - 100
= 19900$$

The algorithm prints

```
19900
```

This verifies that the implementation correctly handles the upper constraint and that integer overflow is not an issue.

A final edge case checks operator correctness. For input

```
2
```

the program computes

$$2 \cdot 2^2 - 2 = 6$$

and prints

```
6
```

This catches implementations that accidentally misuse exponentiation syntax or apply the wrong formula.
