---
title: "CF 104669E - Turnaround"
description: "We are given a non-negative integer and asked to reinterpret it through a transformation on its binary representation. The process is straightforward in description but slightly indirect in execution."
date: "2026-06-29T09:41:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104669
codeforces_index: "E"
codeforces_contest_name: "Turtle Codes"
rating: 0
weight: 104669
solve_time_s: 55
verified: true
draft: false
---

[CF 104669E - Turnaround](https://codeforces.com/problemset/problem/104669/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a non-negative integer and asked to reinterpret it through a transformation on its binary representation. The process is straightforward in description but slightly indirect in execution. First, we write the number in binary without any leading zeros, which means we only keep the significant bits from the most significant 1 down to the least significant bit. Then we reverse the order of these bits as a string. Finally, we interpret this reversed bit string as a new binary number and convert it back into a base-10 integer.

The key subtlety is that the transformation is purely positional on bits. No arithmetic is performed on the value itself beyond binary decomposition and reconstruction. This means the problem is fundamentally about bit manipulation rather than number theory or combinatorics.

The constraint on the input size, up to 10^18, implies that the binary representation has at most 60 bits. Any solution that processes the number in O(log N) time is sufficient. This immediately rules out any approach that tries to simulate bit operations in a linear range up to N or performs repeated heavy string operations over large structures beyond the bit-length of the number.

A naive misunderstanding appears when people think the reversal applies to a fixed-width binary representation. For example, padding to 64 bits and reversing would produce a different result. The problem explicitly forbids leading zeros in the original representation, so padding must not be introduced.

Another common edge case is zero itself. If the input is 0, its binary representation is "0". Reversing still yields "0", and the output remains 0. Any implementation that assumes at least one leading 1-bit will fail here if it does not handle this explicitly.

## Approaches

The brute-force way to think about this problem is to explicitly construct the binary string of the number, reverse it, and then interpret it again as a binary number. Converting a number to binary takes O(log N) time since each step divides by 2. Reversing a string of length log N is also O(log N), and reconstructing the number from the reversed string is again O(log N). This already fits comfortably within constraints.

However, we can avoid building full strings entirely by observing what the reversal does structurally. When we extract bits from the least significant side of N, those bits become the most significant bits in the output. This means that instead of storing a string and reversing it, we can build the result incrementally by shifting and adding bits in the order we extract them.

The core insight is that reversing binary representation is equivalent to reading bits of N from least significant to most significant and constructing a new number by shifting left and inserting each extracted bit. This removes any need for string manipulation and keeps the entire process purely arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(log N) | O(log N) | Accepted |
| Optimal | O(log N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the given number and an empty result initialized to zero. The result will accumulate the reversed binary interpretation as we process bits.
2. While the number is greater than zero, repeatedly extract its least significant bit using modulo 2 or bitwise AND with 1. This bit is exactly the next symbol in the reversed binary string.
3. Shift the result left by one position to make space for the new bit. This ensures the earlier extracted bits occupy higher significance positions in the final number.
4. Add the extracted bit into the result. This appends the reversed binary digit in its correct position.
5. Shift the original number right by one bit to discard the processed bit and move to the next.
6. Continue until all bits are consumed. The constructed result is the final answer.

For the special case where the input is zero, the loop does not execute and the correct output is directly zero.

### Why it works

At every iteration, we are effectively simulating the construction of a reversed bit string. The invariant is that after processing k bits, the result contains exactly the reversed prefix of the original binary representation’s last k bits, in correct order. Since each new bit from the original number is appended to the least significant side of the result after a left shift, positional correctness is preserved throughout the process. No bit is ever overwritten or misplaced, and the process terminates exactly when all significant bits have been consumed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    res = 0

    while n > 0:
        res = (res << 1) | (n & 1)
        n >>= 1

    print(res)

if __name__ == "__main__":
    solve()
```

The implementation reads the number, then repeatedly consumes its binary representation from least significant bit to most significant bit. Each step shifts the result left and inserts the extracted bit. This directly constructs the reversed binary interpretation without ever explicitly building a string.

A subtle point is the order of operations in the update step. The expression `(res << 1) | (n & 1)` ensures that the current result is shifted before inserting the new bit, preserving positional structure. Using addition instead of bitwise OR would also work here since the inserted bit is always 0 or 1, but OR is more explicit in intent.

## Worked Examples

### Example 1

Input:

```
5
```

Binary of 5 is `101`.

We process bits from least significant side.

| Step | n (binary) | extracted bit | res (binary) |
| --- | --- | --- | --- |
| 1 | 101 | 1 | 1 |
| 2 | 10 | 0 | 10 |
| 3 | 1 | 1 | 101 |

After processing all bits, the result is `101`, which is 5 in decimal.

This shows that symmetric binary patterns remain unchanged under reversal, and the algorithm naturally preserves that structure.

### Example 2

Input:

```
731053868524
```

We do not need to fully expand the binary representation; instead we follow the same extraction logic conceptually.

| Step summary | Behavior |
| --- | --- |
| Start | res = 0 |
| Process bit 0 | res stays 0 or shifts without change depending on bit |
| Process full 60-bit sequence | res accumulates reversed bit order |

The final computed result is:

```
238960798805
```

This demonstrates that even for large inputs, the algorithm remains strictly linear in the number of bits, not the magnitude of the number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log N) | Each iteration removes one binary bit from the number |
| Space | O(1) | Only a constant number of integer variables are used |

The runtime is bounded by the number of bits in the input, which is at most around 60 for the given constraints. This ensures the solution executes comfortably within the time limit.

## Test Cases

```python
import sys, io

def solve():
    n = int(sys.stdin.readline().strip())
    res = 0
    while n > 0:
        res = (res << 1) | (n & 1)
        n >>= 1
    print(res)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# provided samples
assert run("5\n") == "5", "sample 1"
assert run("731053868524\n") == "238960798805", "sample 2"

# custom cases
assert run("0\n") == "0", "zero case"
assert run("1\n") == "1", "single bit"
assert run("2\n") == "1", "10 -> 01"
assert run("6\n") == "3", "110 -> 011"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | handles zero without looping |
| 1 | 1 | single-bit stability |
| 2 | 1 | leading zero in reversed form |
| 6 | 3 | multi-bit reversal correctness |

## Edge Cases

The zero input is the only structurally degenerate case because it produces no iterations in the main loop. For input `0`, the binary representation is `0`, and the algorithm immediately outputs `0` since the accumulator is never modified.

For input `1`, the binary representation is a single bit. The loop runs once, extracts `1`, and places it into the result, yielding `1`. This confirms that the algorithm correctly handles minimal non-zero structure without requiring special casing.

For inputs that are powers of two, such as `2` or `8`, the binary representation has a single high bit followed by zeros. Reversal moves that high bit to the least significant position. The loop naturally achieves this because zeros contribute shifts without setting bits, and the final 1-bit ends up in the correct reversed position.
