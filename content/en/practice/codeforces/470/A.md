---
title: "CF 470A - Crystal Ball Sequence"
description: "The sequence in this problem comes from counting lattice points inside a growing hexagon on a hexagonal grid. Instead of having to construct the hexagon or count points manually, the problem already gives the formula for the sequence: $$Hn = 3 cdot n cdot (n+1) + 1$$ The input…"
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 470
codeforces_index: "A"
codeforces_contest_name: "Surprise Language Round 7"
rating: 1400
weight: 470
solve_time_s: 96
verified: true
draft: false
---

[CF 470A - Crystal Ball Sequence](https://codeforces.com/problemset/problem/470/A)

**Rating:** 1400  
**Tags:** *special, implementation  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The sequence in this problem comes from counting lattice points inside a growing hexagon on a hexagonal grid. Instead of having to construct the hexagon or count points manually, the problem already gives the formula for the sequence:

$$H_n = 3 \cdot n \cdot (n+1) + 1$$

The input consists of a single integer `n`, representing the index of the sequence element we need to compute. The output is the value of $H_n$.

The constraints are extremely small. The value of `n` is between 0 and 9 inclusive. Even the largest possible answer is tiny:

$$H_9 = 3 \cdot 9 \cdot 10 + 1 = 271$$

Because of these bounds, performance is not a concern. Any reasonable solution runs instantly. The real task is simply applying the given formula correctly.

One edge case is `n = 0`. Many sequence problems start from index 1, and a careless implementation might accidentally assume that. For example:

Input:

```
0
```

Correct output:

```
1
```

Substituting into the formula gives:

$$3 \cdot 0 \cdot 1 + 1 = 1$$

Another common mistake is misreading the formula as `3*n*n + 1` instead of `3*n*(n+1) + 1`.

For example:

Input:

```
1
```

Correct output:

```
7
```

The correct computation is:

$$3 \cdot 1 \cdot 2 + 1 = 7$$

Using `3*n*n+1` would incorrectly produce 4.

## Approaches

A brute-force interpretation would be to actually model the hexagonal lattice and count all points contained in a hexagon with `n+1` points on each side. Such a solution would generate coordinates, determine which points belong to the shape, and count them. It would be correct because it directly simulates the geometric definition of the sequence.

Even though the constraints are tiny, this approach is unnecessary. The problem already provides the exact formula for the answer. Once the sequence definition is given algebraically, there is no reason to reconstruct the geometry.

The key observation is that the desired value is explicitly defined as:

$$H_n = 3n(n+1)+1$$

So the entire problem reduces to reading `n`, evaluating the expression, and printing the result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Hn) | O(Hn) | Unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` from input.
2. Compute the sequence value using the given formula:

$$H_n = 3 \cdot n \cdot (n+1) + 1$$

This is exactly how the sequence is defined, so no additional derivation is required.
3. Output the computed value.

### Why it works

The problem directly defines the sequence element as:

$$H_n = 3n(n+1)+1$$

The algorithm evaluates this formula for the given input `n`. Since the formula itself is the definition of the sequence, the computed value is precisely the required answer. There is no approximation, simulation, or intermediate reasoning that could alter the result.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
print(3 * n * (n + 1) + 1)
```

The program begins by reading the single input value `n`.

It then evaluates `3 * n * (n + 1) + 1`, matching the mathematical definition given in the statement. Multiplication is performed before addition according to Python's operator precedence, but the parentheses around `(n + 1)` make the intended computation completely explicit.

Finally, the result is printed.

There are no boundary issues because the formula works for every valid input, including `n = 0`. Integer overflow is also impossible in Python, and the largest answer in this problem is only 271.

## Worked Examples

### Example 1

Input:

```
1
```

| Step | n | Computation | Result |
| --- | --- | --- | --- |
| Read input | 1 | - | - |
| Apply formula | 1 | 3 × 1 × (1 + 1) + 1 | 7 |
| Output | 1 | - | 7 |

The trace shows the simplest non-zero case. The formula produces 7, which matches the sample output.

### Example 2

Input:

```
9
```

| Step | n | Computation | Result |
| --- | --- | --- | --- |
| Read input | 9 | - | - |
| Apply formula | 9 | 3 × 9 × 10 + 1 | 271 |
| Output | 9 | - | 271 |

This example uses the largest allowed input. The computation remains a single arithmetic expression and produces 271.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | A constant number of arithmetic operations |
| Space | O(1) | Only a few integer variables are stored |

The algorithm performs one formula evaluation regardless of the input value. Its running time and memory usage are constant, which is far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline
    n = int(input())
    print(3 * n * (n + 1) + 1)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("1\n") == "7", "sample 1"

# custom cases
assert run("0\n") == "1", "minimum input"
assert run("2\n") == "19", "small positive value"
assert run("5\n") == "91", "middle of range"
assert run("9\n") == "271", "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1` | Sequence starts correctly at index 0 |
| `2` | `19` | Correct use of `n + 1` in the formula |
| `5` | `91` | Typical non-boundary case |
| `9` | `271` | Maximum allowed input |

## Edge Cases

The first important edge case is the smallest possible index.

Input:

```
0
```

The algorithm computes:

$$3 \cdot 0 \cdot (0+1) + 1 = 1$$

Output:

```
1
```

This confirms that the formula remains valid at the lower boundary and that the sequence is zero-indexed.

Another subtle case is checking whether the implementation correctly uses `(n + 1)`.

Input:

```
1
```

The algorithm computes:

$$3 \cdot 1 \cdot 2 + 1 = 7$$

Output:

```
7
```

An incorrect implementation using `3*n*n + 1` would return 4. This test verifies that the formula has been transcribed accurately.

The upper boundary is also worth checking.

Input:

```
9
```

The algorithm computes:

$$3 \cdot 9 \cdot 10 + 1 = 271$$

Output:

```
271
```

The computation stays well within integer limits and demonstrates that the solution handles the largest allowed input correctly.
