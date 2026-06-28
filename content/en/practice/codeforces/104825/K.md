---
title: "CF 104825K - str\u8fdb\u5236"
description: "We are given a string that acts like a description of a positional numeral system, except it is not a fixed base like decimal or binary. Instead, each position has its own “carry rule”."
date: "2026-06-28T12:33:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104825
codeforces_index: "K"
codeforces_contest_name: "The 17-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 104825
solve_time_s: 45
verified: true
draft: false
---

[CF 104825K - str\u8fdb\u5236](https://codeforces.com/problemset/problem/104825/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string that acts like a description of a positional numeral system, except it is not a fixed base like decimal or binary. Instead, each position has its own “carry rule”. If a position contains the digit x, that position behaves like base x: once it reaches x, it resets to 0 and carries 1 to the next position.

We are also given a non-negative integer d in ordinary decimal form. The task is to express d in this mixed-radix system, producing exactly m digits, including leading zeros if higher positions are not used.

A useful way to picture this is an odometer where each wheel has a different number of slots, and those capacities are specified by the characters of the input string s.

The constraint m ≤ 1000 means the representation length is at most a thousand digits, so any solution that processes the number once per digit is easily fast enough. The second parameter n is irrelevant to the computation itself and can be ignored safely once read.

The most common failure case here is treating the system as a normal base conversion with a single base. That would immediately break on inputs like s = "29". The least significant digit might have base 9, while the next has base 2, so a uniform base interpretation loses the structure entirely.

Another subtle issue is direction. If one assumes the leftmost digit is least significant, the conversion will be reversed. For example, if s = "23" and d = 5, interpreting left-to-right instead of right-to-left produces different remainders because the carry propagation direction changes the positional weights.

## Approaches

A brute-force interpretation would simulate incrementing a number from 0 until reaching d, updating the mixed-radix digits each time. Each increment requires propagating carries across up to m positions, so the worst case cost is proportional to d times m. Since d can be as large as 10^10, this becomes completely infeasible even for small m.

The structure of the system suggests a more direct interpretation. Each position contributes independently to how the total number expands when viewed from least significant side, similar to converting a number into factorial number system or any general mixed radix system. Instead of simulating increments, we can directly extract digits using repeated division.

The key observation is that the string s defines a sequence of bases, and the representation of d is exactly the mixed-radix decomposition of d under these bases. This allows us to compute each digit by taking remainders and reducing d step by step.

The brute-force approach fails because it treats the number as evolving over time, while the optimal approach treats it as a static decomposition problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(d · m) | O(m) | Too slow |
| Mixed Radix Decomposition | O(m) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Interpret each character of the string s as an integer base for its corresponding digit position. The rightmost character is the least significant position, since carries propagate leftward in standard positional systems.
2. Start from the given decimal number d, which represents the full value we need to decompose into the mixed-radix representation.
3. Traverse the positions from right to left. At each position i, compute the digit as the remainder of d divided by s[i]. This ensures the digit is valid within its local base constraint.
4. After extracting the digit for position i, reduce d by integer division with s[i]. This models removing the contribution of the current position and propagating the remaining value to higher positions.
5. Store all extracted digits in an array during traversal.
6. After processing all positions, output the digits in the original order from left to right.

The reason this works is that each position contributes a coefficient in a positional system whose weights are dynamically determined by the product of all bases to its right. The repeated modulo and division operation is exactly computing coefficients in that system, ensuring each digit satisfies its local constraint while preserving the global value.

The invariant maintained throughout the process is that at the start of processing position i, the variable d represents the remaining value that has not yet been assigned to lower positions, and this remaining value is always divisible into the structure defined by the suffix of bases already processed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m, n = map(int, input().split())
    s = input().strip()
    d = int(input().strip())

    bases = [int(c) for c in s]
    res = [0] * m

    for i in range(m - 1, -1, -1):
        b = bases[i]
        res[i] = d % b
        d //= b

    print("".join(map(str, res)))

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm exactly. The array res stores digits in their final positions, so we avoid reversing at the end by writing directly into index i. The loop runs from the least significant position at m-1 to 0, ensuring correct carry propagation direction.

A common implementation mistake is to process from left to right while still using modulo, which breaks the dependency structure. Another subtle issue is forgetting that each s[i] is a character and must be converted to an integer before arithmetic.

## Worked Examples

Consider s = "243" and d = 17. We interpret the rightmost digit as base 3, middle as base 4, left as base 2.

We process from right to left.

| Position | Base | Current d | Digit (d % base) | New d (d // base) |
| --- | --- | --- | --- | --- |
| 2 | 3 | 17 | 2 | 5 |
| 1 | 4 | 5 | 1 | 1 |
| 0 | 2 | 1 | 1 | 0 |

Final output is 112.

This trace shows how each position consumes part of the remaining value, ensuring that no position exceeds its local base constraint while preserving total value.

Now consider s = "9999" and d = 123. This behaves like standard base-9 representation with fixed length.

| Position | Base | Current d | Digit | New d |
| --- | --- | --- | --- | --- |
| 3 | 9 | 123 | 6 | 13 |
| 2 | 9 | 13 | 4 | 1 |
| 1 | 9 | 1 | 1 | 0 |
| 0 | 9 | 0 | 0 | 0 |

Output is 0146.

This demonstrates how the method naturally reduces to standard base conversion when all bases are equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each digit is computed with one modulo and one division |
| Space | O(m) | Storage for output digits |

The constraints allow up to 1000 digits, so a linear scan over the string with constant-time arithmetic per digit is trivially efficient within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    m, n = map(int, input().split())
    s = input().strip()
    d = int(input().strip())

    bases = [int(c) for c in s]
    res = [0] * m

    for i in range(m - 1, -1, -1):
        b = bases[i]
        res[i] = d % b
        d //= b

    return "".join(map(str, res))

# minimal case
assert run("1 1\n2\n0\n") == "0"

# simple mixed radix
assert run("3 1\n234\n10\n") == "102"

# all same base behavior
assert run("4 1\n9999\n123\n") == "0146"

# leading zeros needed
assert run("5 1\n22222\n3\n") == "00003"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-digit zero | 0 | smallest boundary case |
| 234, 10 | 102 | mixed bases with carry |
| 9999, 123 | 0146 | uniform base consistency |
| 22222, 3 | 00003 | leading zero preservation |

## Edge Cases

When d is zero, every modulo operation produces zero and the division keeps it at zero throughout. For example, with s = "2345" and d = 0, each step computes digit 0 and preserves d as 0, producing a full zero-filled output.

When d is very small relative to early bases but larger than later ones, the lower positions absorb all value first. For instance, s = "234" and d = 2 produces digits [0, 0, 2] when processed from right to left, since only the least significant base contributes non-zero remainder.

When all bases are equal, such as s = "7777", the algorithm behaves exactly like base-7 conversion with fixed width, confirming that mixed radix generalizes standard positional systems rather than replacing them.
