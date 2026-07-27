---
title: "CF 102780J - Something that resembles Waring's problem"
description: "We need write a given positive integer as a sum of at most five integer cubes. The input number can be extremely large, up to $10^{100000}$, so it cannot fit into normal integer types."
date: "2026-07-28T03:36:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102780
codeforces_index: "J"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19)"
rating: 0
weight: 102780
solve_time_s: 121
verified: true
draft: false
---

[CF 102780J - Something that resembles Waring's problem](https://codeforces.com/problemset/problem/102780/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We need write a given positive integer as a sum of at most five integer cubes. The input number can be extremely large, up to $10^{100000}$, so it cannot fit into normal integer types. The output is either a list of at most five integers whose cubes add up to the input, or `-1` if such a representation cannot be found.

The size of the number changes the entire approach. A linear scan over possible cube roots is impossible because even storing the input already requires 100000 decimal digits. The algorithm must work with big integers and use only a small number of arithmetic operations. Python's built in arbitrary precision integers are suitable here because the number of operations is tiny compared with the cost of the arithmetic itself.

A common mistake is trying to search for small cube roots. For example, for input `1000000000000`, checking cubes up to the cube root of the number only works for ordinary sized integers, but here the input length makes such enumeration meaningless. Another mistake is assuming only positive cubes are useful. Negative cubes are essential because they allow cancellation of large terms.

The key edge cases are small values and values whose remainder is unusual. For input `1`, the correct answer is one cube, `1^3`. A method that always subtracts a large construction before handling the remainder can accidentally create unnecessary negative values or fail on small numbers. For input `5`, the answer can be five copies of `1`, while a construction based only on dividing by six must also handle the remaining residue correctly.

## Approaches

The brute force approach would try to find five integers around the cube root of the number and test every possible combination. This is correct because checking every possible tuple would eventually find a representation if one exists. The problem is the number of possibilities. If the number has magnitude about $M$, there are about $M^{1/3}$ possible cube roots, and five nested choices create roughly $M^{5/3}$ combinations. With $M=10^{100000}$, this is not even remotely possible.

The useful observation comes from the identity

$$(y+1)^3+(y-1)^3+(-y)^3+(-y)^3=6y$$

This means any number divisible by six can be written using four cubes. Every integer has a remainder from 0 to 5 modulo six, and every such remainder is itself an integer cube modulo six. We can remove that remainder first, then apply the identity to the remaining divisible part.

The whole problem becomes a constant number of big integer operations. We find a small cube $r^3$ with the same remainder as the input modulo six, compute $y=(x-r^3)/6$, and use the identity for $6y$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M^(5/3)) | O(1) | Too slow |
| Optimal | O(d^2) where d is the number of digits | O(d) | Accepted |

## Algorithm Walkthrough

1. Compute the remainder of the input number modulo six. Cubes modulo six cover every possible remainder, so choose a small integer `r` from `0` to `5` whose cube has the same remainder.
2. Subtract `r^3` from the number. The remaining value is guaranteed to be divisible by six because both values have the same remainder modulo six.
3. Divide the remaining value by six to get `y`.
4. Use the identity

$$(y+1)^3+(y-1)^3+(-y)^3+(-y)^3=6y$$

and append `r` as the fifth cube. If `r` is zero, it does not need to be printed because fewer cubes are allowed.

The invariant is that after step two, the remaining value is exactly a multiple of six. The identity in step four represents that multiple using four cubes, and the removed remainder is represented by one cube, so the final sum always equals the original number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x = int(input().strip())

    r = None
    for i in range(6):
        if (i * i * i - x) % 6 == 0:
            r = i
            break

    ans = []

    if r != 0:
        ans.append(r)

    y = (x - r * r * r) // 6

    if y != 0:
        ans.extend([y + 1, y - 1, -y, -y])

    if not ans:
        ans.append(0)

    print(len(ans))
    print(*ans)

if __name__ == "__main__":
    solve()
```

The program first searches only six candidates because the residue modulo six has only six possibilities. This is independent of the input size.

The variable `y` can contain up to 100000 digits, but Python integers handle this directly. The expression `(x - r * r * r) // 6` is safe because the previous loop guarantees divisibility.

When `y` is zero, the four cube identity would create redundant zero terms. The code omits them and only prints the necessary remainder cube. The answer still satisfies the limit of five numbers.

## Worked Examples

For input `5`, the chosen remainder cube is:

| x | r | y | Output cubes |
| --- | --- | --- | --- |
| 5 | 5 | 0 | 5 |

The algorithm recognizes that `5^3` has the same remainder as `5` modulo six because `125 mod 6 = 5`. Since the remaining part is zero, only the cube `5^3` is needed.

For input `17`, we get:

| x | r | y | Output cubes |
| --- | --- | --- | --- |
| 17 | 5 | -19 | 5, -18, -20, 19, 19 |

This is a valid construction because the four large cubes sum to $6y$, and the final cube restores the removed residue. The output is not required to match the sample, only to satisfy the equation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d²) | Big integer addition, subtraction, multiplication and division operate on d digit numbers |
| Space | O(d) | The stored numbers have at most the input digit length plus a small constant |

The algorithm performs only a few big integer operations on a 100000 digit value, so it fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    x = int(sys.stdin.readline().strip())

    r = None
    for i in range(6):
        if (i * i * i - x) % 6 == 0:
            r = i
            break

    ans = []
    if r != 0:
        ans.append(r)

    y = (x - r * r * r) // 6

    if y != 0:
        ans.extend([y + 1, y - 1, -y, -y])

    if not ans:
        ans.append(0)

    out = str(len(ans)) + "\n" + " ".join(map(str, ans)) + "\n"

    sys.stdin = old
    return out

def check(inp):
    out = run(inp).split()
    k = int(out[0])
    vals = list(map(int, out[1:]))
    assert k == len(vals)
    assert k <= 5
    x = int(inp)
    assert sum(v ** 3 for v in vals) == x

check("5")
check("17")
check("1")
check("6")
check("1000000000000000000000000")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 | Any valid representation with at most 5 cubes | Small residue handling |
| 17 | Any valid representation with at most 5 cubes | Nonzero remainder plus negative cubes |
| 1 | `1` cubed | Minimum value |
| 6 | Four cube identity | Divisible by six boundary |
| 1000000000000000000000000 | Any valid representation with at most 5 cubes | Very large integer arithmetic |

## Edge Cases

For input `1`, the algorithm finds `r = 1`, so `y = 0`. It prints only `1`, and the sum of cubes is exactly one. This avoids producing unnecessary terms from the general identity.

For input `6`, the remainder is zero, so `r = 0` and `y = 1`. The generated cubes are `2, 0, -1, -1`, whose cubes sum to

$$8+0-1-1=6$$

The zero term can be omitted, but keeping or removing it does not affect correctness.

For very large values, the algorithm never converts the number into digits or iterates through its magnitude. It only performs a constant number of arithmetic operations, so inputs with 100000 digits are handled in the same way as small inputs.
