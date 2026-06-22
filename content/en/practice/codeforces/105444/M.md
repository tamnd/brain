---
title: "CF 105444M - Methodic Multiplication"
description: "We are given two natural numbers, but they are not written in decimal form. Instead, each number is encoded using Peano arithmetic, where a number is represented as repeated applications of a successor function applied to zero."
date: "2026-06-23T03:33:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105444
codeforces_index: "M"
codeforces_contest_name: "2020-2021 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2020)"
rating: 0
weight: 105444
solve_time_s: 53
verified: true
draft: false
---

[CF 105444M - Methodic Multiplication](https://codeforces.com/problemset/problem/105444/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two natural numbers, but they are not written in decimal form. Instead, each number is encoded using Peano arithmetic, where a number is represented as repeated applications of a successor function applied to zero. Concretely, 0 is written as `0`, one is `S(0)`, two is `S(S(0))`, and so on.

The task is to read two such representations and compute their product, then output the result in the same symbolic format.

Although the input looks like nested function notation, there is no need to simulate Peano multiplication directly. The real value of each number is simply the count of how many `S(` wrappers appear around the final `0`. So each input string encodes an integer equal to its nesting depth.

The output must again be the Peano representation of the product, meaning we must print `S` applied that many times to `0`, where the count equals the product of the two decoded integers.

The input size constraint of up to 1000 characters per number means the decoded integers are at most 1000. Their product is at most 1,000,000, which is small enough to construct directly in output form without overflow concerns or performance issues.

A naive mistake is to attempt literal symbolic evaluation of the Peano axioms. For example, expanding multiplication recursively using the definition `x · S(y) = x · y + x` would lead to exponential blowup in repeated additions. Even a linear recursion per operation becomes unnecessary overhead because the structure already encodes the numeric value directly.

A second common pitfall is misparsing the string. The structure is guaranteed well-formed, but one must correctly count only the `S` occurrences, ignoring parentheses and zeros. Any mismatch in counting leads to incorrect numeric reconstruction.

Edge cases include:

A single `0` multiplied by anything should yield `0`. For example, input `0` and `S(S(0))` must produce `0`. A careless parser that assumes at least one `S` might incorrectly output `S(0)`.

Another case is maximum nesting such as 1000 `S` applications. If both inputs are maximal, the output must contain one million `S(` wrappers. Any recursive construction of strings without careful repetition handling risks stack overflow or excessive concatenation overhead.

## Approaches

The brute-force approach is to directly implement Peano multiplication using its recursive definitions. One would first implement addition by repeatedly applying `x + S(y) = S(x + y)`, and then multiplication by repeated addition using `x · S(y) = x · y + x`. This is mathematically faithful and correct, but operationally expensive.

If x and y are both of size n in Peano form, multiplication expands into y additions of x, and each addition itself may traverse the entire structure of x. This leads to a worst-case complexity on the order of O(n²) symbolic operations, and worse in practice due to string or tree reconstruction overhead. With input sizes up to 1000, this is unnecessary overkill.

The key observation is that Peano notation is unary. Each number is literally encoded as its value, so decoding reduces to counting symbols. Once both values are recovered as integers, multiplication becomes a single arithmetic operation. The result is then re-encoded by repeating `S(` exactly the product number of times.

This reduces the entire problem to linear parsing plus linear output construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Peano recursion | O(n²) | O(n²) | Too slow |
| Count + construct | O(n + xy) | O(xy) | Accepted |

## Algorithm Walkthrough

1. Read each input string and interpret it as a sequence of tokens. The structure is always of the form repeated `S(` followed by a single `0` and then closing parentheses. The only meaningful information is how many times `S(` appears before the `0`. This count is the numeric value.
2. Scan the first string and count occurrences of the substring pattern corresponding to a successor application. Each valid number contributes exactly one `S`, so the count directly gives x. This works because Peano representation is unary encoding of integers.
3. Repeat the same process for the second string to obtain y.
4. Compute the product z = x × y using standard integer multiplication. Since x and y are at most 1000, z is at most 1,000,000, which is safe.
5. Construct the output string by repeating the pattern `S(` exactly z times, followed by `0`, followed by z closing parentheses `)`.
6. Output the constructed string.

### Why it works

The Peano representation is structurally isomorphic to unary integers, where each application of the successor function increases the value by exactly one. The parsing step extracts this unary length. Since multiplication is defined over natural numbers independent of representation, once values are recovered correctly, arithmetic can be performed in standard integer form. The reconstruction step preserves correctness because each successor corresponds exactly to one structural wrapper in the original encoding.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse_peano(s: str) -> int:
    # count occurrences of 'S'
    return s.count('S')

a = input().strip()
b = input().strip()

x = parse_peano(a)
y = parse_peano(b)

z = x * y

# build Peano representation
# S(S(...S(0)...))
print("S(" * z + "0" + ")" * z)
```

The parsing function relies on the fact that every number is constructed only from repeated `S(` wrappers, so counting `S` is equivalent to decoding the integer value. No structural validation is needed beyond trusting the input format.

The multiplication is done using native integers, which is efficient given the small bounds.

The output construction is the only potentially heavy step. It creates a string of size O(z), which is unavoidable since the output itself is that large.

## Worked Examples

### Sample 1

Input:

```
S(S(0))
S(S(S(0)))
```

Here the first number has two `S` applications, so x = 2. The second has three, so y = 3. Thus z = 6.

| Step | First value x | Second value y | Product z |
| --- | --- | --- | --- |
| Parse | 2 | 3 | - |
| Multiply | - | - | 6 |
| Build output | - | - | S repeated 6 times |

Output:

```
S(S(S(S(S(S(0)))))))
```

This confirms that unary multiplication corresponds to concatenation of successor layers.

### Sample 2

Input:

```
S(S(S(S(S(0)))))
S(0)
```

Here x = 5 and y = 1, so z = 5.

| Step | x | y | z |
| --- | --- | --- | --- |
| Parse | 5 | 1 | - |
| Multiply | - | - | 5 |
| Build output | - | - | 5 S wrappers |

Output:

```
S(S(S(S(S(0)))))
```

This demonstrates the identity property of multiplication by one, preserved directly in unary structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + xy) | linear scan to count S plus output construction proportional to result size |
| Space | O(xy) | output string dominates memory usage |

The constraints allow up to 1000 symbols per input, so x and y are at most 1000. The output size is therefore at most 1,000,000 characters, which is acceptable in typical Codeforces environments for a single output string.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def parse_peano(s: str) -> int:
        return s.count('S')

    a = input().strip()
    b = input().strip()

    x = parse_peano(a)
    y = parse_peano(b)
    z = x * y

    return "S(" * z + "0" + ")" * z

# provided samples (interpreted)
assert run("S(S(0))\nS(S(S(0)))\n") == "S(" * 6 + "0" + ")" * 6

# minimum case
assert run("0\n0\n") == "0"

# identity case
assert run("S(0)\nS(S(S(0)))\n") == "S(" * 3 + "0" + ")" * 3

# zero times anything
assert run("0\nS(S(S(S(0))))\n") == "0"

# large-ish balanced case
assert run("S(" * 100 + "0\n" + "S(" * 100 + "0\n") == "S(" * 10000 + "0" + ")" * 10000
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0, 0 | 0 | zero absorption |
| S(0), S(S(S(0))) | SSSS...0 | basic multiplication |
| 0, nonzero | 0 | edge case correctness |
| 100 S and 100 S | large balanced output | performance and scaling |

## Edge Cases

One critical edge case is when either input is exactly `0`. In that case, the parsed value is zero, so the product is zero. The algorithm produces `"S(" * 0 + "0" + ")" * 0`, which collapses cleanly to `"0"`. This avoids generating invalid structure.

Another case is maximum nesting. If both inputs contain 1000 successive `S(` applications, parsing yields x = 1000 and y = 1000, so z = 1,000,000. The construction step produces one million repetitions of `"S("` and `")"`, surrounding a single `"0"`. Execution remains linear in output size, and correctness follows from direct repetition semantics of unary encoding.

A subtle case is malformed intuition about counting parentheses instead of `S`. Only `S` matters, since parentheses are structural noise. The algorithm remains correct even if parentheses vary, as long as the `S` count matches the encoding definition.
