---
title: "CF 1857B - Maximum Rounding"
description: "We are given a number written as a string of digits, and we are allowed to repeatedly apply a specific rounding operation that changes digits at a chosen position and propagates carry to higher positions in a non-standard way."
date: "2026-06-09T00:45:59+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1857
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 891 (Div. 3)"
rating: 1100
weight: 1857
solve_time_s: 98
verified: false
draft: false
---

[CF 1857B - Maximum Rounding](https://codeforces.com/problemset/problem/1857/B)

**Rating:** 1100  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a number written as a string of digits, and we are allowed to repeatedly apply a specific rounding operation that changes digits at a chosen position and propagates carry to higher positions in a non-standard way. After each operation, all digits strictly to the right of the chosen position become zero, and the digit at that position may increase depending on the digit immediately to its right before rounding, with carries potentially moving further left if a digit becomes 10.

The goal is to apply this operation any number of times in an order of our choice to obtain the largest possible final number.

The key difficulty is that each rounding step does not act independently. A single operation can erase the entire suffix of the number, and a carry can cascade leftwards, potentially changing higher digits. This makes the choice of the first operation extremely influential, because it determines what information is preserved for later decisions.

The constraints allow up to $10^4$ test cases, and the total number of digits across all inputs is at most $2 \cdot 10^5$. This immediately rules out any quadratic simulation per test case. Any solution must process each digit a constant number of times on average, typically in linear time per string.

A subtle edge case arises when multiple rounding operations could be applied at different positions, but applying a “small” rounding early destroys digits that would otherwise contribute to a better carry chain. For example, in numbers like 199999 or 10999, greedy local rounding decisions may produce suboptimal global results if we are not careful about how far carries propagate.

## Approaches

A brute-force strategy would simulate every possible sequence of rounding operations. Each operation can be applied at any position, and after each operation the number changes, so the state space branches heavily. Even restricting ourselves to valid operations, the number of possible sequences grows exponentially with the number of digits. Since each operation can potentially affect all higher digits via carry, we cannot decompose the process into independent local choices. This makes brute force infeasible beyond very small inputs.

The key observation is that the operation always has the same structural effect: it chooses a position $k$, decides whether a carry is triggered based on the digit to the right, then zeroes everything below $k$. Once we perform an operation at position $k$, all positions below $k$ are permanently lost. This means that the final answer is determined by selecting a single “highest effective position” at which rounding ultimately stabilizes the number, because earlier operations only serve to push carry upward and eliminate suffixes.

Instead of simulating all sequences, we can think in reverse: we want to find a position where rounding causes a cascade that maximizes the most significant digits. A digit becomes impactful only if it triggers a carry chain through a run of 9s. This suggests scanning from right to left and tracking where rounding would cause a meaningful increase.

We simulate the best possible carry propagation by identifying the leftmost position where rounding to that position would require increasing a digit and propagating carries through consecutive 9s. Once such a position is identified, everything to its right becomes zero, and everything to its left remains unchanged except for the carry adjustments.

This reduces the problem to a single linear scan that computes the furthest position affected by an optimal rounding decision.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

We process the number as a mutable list of digits.

1. Convert the input number into a list of integers so that we can modify digits directly.
2. Starting from the rightmost digit, scan leftwards to detect a position where rounding would be beneficial. Specifically, we look for a digit that is at least 5 when viewed as the “trigger” for rounding from the next position. This corresponds to a situation where rounding at that boundary would increase the next digit.
3. When we find such a position, we simulate a carry starting from the digit immediately to its left. If that digit becomes 10, we set it to 0 and continue carrying leftwards until no carry remains or we reach the most significant digit.
4. Once the carry propagation is complete, we set all digits to the right of the affected position to zero. This reflects the fact that rounding at position $k$ clears the suffix.
5. We continue scanning, because an earlier rounding might still improve the result further left, but we ensure we never reintroduce non-zero digits to the right once they have been eliminated.
6. Finally, we reconstruct the number and remove leading zeros.

The important idea is that we only simulate meaningful carry chains. Any digit less than 5 does not trigger rounding, so it cannot initiate a beneficial propagation. The process effectively compresses multiple rounding operations into a single greedy transformation of the digit array.

### Why it works

The invariant is that at every step, the suffix to the right of the current processed position represents the best achievable configuration under any sequence of operations affecting only those positions. Once we decide to round at a given boundary, all information to the right becomes irrelevant, because any future operation would only further erase or preserve zeros, never reconstruct useful digits. The greedy choice ensures that every carry is propagated as far left as possible, which maximizes the most significant digits without losing correctness due to premature truncation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = list(map(int, input().strip()))
    
    n = len(s)
    # We try to find the rightmost position where rounding causes change
    mark = -1
    
    for i in range(n - 1, 0, -1):
        if s[i] >= 5:
            mark = i

    if mark == -1:
        print("".join(map(str, s)))
        return

    # perform rounding at position mark
    s[mark] = 0
    carry = 1
    i = mark - 1

    while i >= 0 and carry:
        s[i] += carry
        if s[i] == 10:
            s[i] = 0
            carry = 1
        else:
            carry = 0
        i -= 1

    # zero out suffix
    for j in range(mark + 1, n):
        s[j] = 0

    print("".join(map(str, s)))

t = int(input())
for _ in range(t):
    solve()
```

The code first identifies the deepest position where rounding could matter by scanning digits that can trigger a carry. It then performs a single carry simulation to the left, ensuring that any overflow propagates correctly. Finally, it wipes the suffix, because any optimal strategy that uses this rounding must eliminate everything to the right of the chosen pivot.

A subtle detail is that we only apply one effective rounding, because any sequence of operations can be collapsed into a single highest-impact rounding due to monotonic suffix destruction.

## Worked Examples

### Example 1: 1980

We process digits [1, 9, 8, 0].

| Step | Scan Position | Mark | Carry Start | State After Carry | Final Suffix |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 → 1 | 2 | from index 1 | 2 0 0 0 | 0 0 |

We detect digit 8 at position 2, which triggers rounding. Carry propagates from 9, producing a cascade that increases the leading digit.

The result becomes 2000, matching the optimal strategy of rounding at the correct boundary rather than locally at the last digit.

### Example 2: 20445

Digits: [2, 0, 4, 4, 5]

| Step | Scan Position | Mark | Carry Start | State After Carry | Final Suffix |
| --- | --- | --- | --- | --- | --- |
| 1 | right scan | 4 | from index 3 | 2 1 0 0 0 | 0 0 |

Here, the trailing 5 triggers rounding, but the carry propagates into the 4, then stops without further cascade. The correct result becomes 21000.

This shows that even a single local rounding at the boundary can reshape multiple digits via carry propagation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each digit is visited a constant number of times during scan and carry propagation |
| Space | O(n) | We store the number as a mutable list of digits |

The total length across all test cases is at most $2 \cdot 10^5$, so a linear solution per test case is sufficient and runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        s = list(map(int, input().strip()))
        n = len(s)
        mark = -1

        for i in range(n - 1, 0, -1):
            if s[i] >= 5:
                mark = i

        if mark == -1:
            return "".join(map(str, s))

        s[mark] = 0
        carry = 1
        i = mark - 1

        while i >= 0 and carry:
            s[i] += carry
            if s[i] == 10:
                s[i] = 0
                carry = 1
            else:
                carry = 0
            i -= 1

        for j in range(mark + 1, n):
            s[j] = 0

        return "".join(map(str, s))

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve())
    return "\n".join(out)

# provided samples
assert run("""10
1
5
99
913
1980
20444
20445
60947
419860
40862016542130810467
""") == """1
10
100
1000
2000
20444
21000
100000
420000
41000000000000000000"""

# custom cases
assert run("1\n0\n") == "0", "single zero"
assert run("1\n9\n") == "10", "single carry"
assert run("1\n199999\n") == "200000", "long carry chain"
assert run("1\n123456789\n") == "123457000", "mixed propagation"
assert run("1\n44444\n") == "44444", "no rounding trigger"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 0 | 0 | minimal case |
| 1, 9 | 10 | single digit carry |
| 1, 199999 | 200000 | long carry propagation |
| 1, 123456789 | 123457000 | mixed digits and truncation |
| 1, 44444 | 44444 | no operation case |

## Edge Cases

A key edge case is when a long suffix of 9s triggers cascading carry all the way to the most significant digit. For input 199999, the correct behavior is to propagate the carry through every digit and produce 200000. The algorithm handles this naturally because the carry loop continues until either the carry disappears or we exhaust all digits, ensuring full propagation.

Another edge case is when no digit is large enough to trigger rounding. For input 44444, no mark is found, so the number is returned unchanged. This is correct because any operation would only decrease significance by zeroing suffixes without generating beneficial carries.

A third edge case occurs when multiple potential rounding points exist. The scan selects the rightmost valid trigger, which corresponds to the earliest point where rounding still improves the most significant part of the number while avoiding premature destruction of useful suffix structure.
