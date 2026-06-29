---
title: "CF 104637F - Subtractions"
description: "We are given several independent pairs of positive integers. For each pair, we repeatedly apply a deterministic transformation: identify the larger of the two numbers and subtract the smaller from it."
date: "2026-06-29T17:01:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104637
codeforces_index: "F"
codeforces_contest_name: "\u041c\u0438\u0441\u0438\u0441 2023 \u043e\u0441\u0435\u043d\u044c - \u0431\u0430\u0437\u043e\u0432\u0430\u044f \u043c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u043a\u0430, \u0443\u0441\u043b\u043e\u0432\u0438\u044f, \u0446\u0438\u043a\u043b\u044b"
rating: 0
weight: 104637
solve_time_s: 76
verified: false
draft: false
---

[CF 104637F - Subtractions](https://codeforces.com/problemset/problem/104637/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent pairs of positive integers. For each pair, we repeatedly apply a deterministic transformation: identify the larger of the two numbers and subtract the smaller from it. If both numbers are equal, we subtract one from the other, which immediately produces a zero.

Each operation strictly decreases at least one of the numbers, and we continue until at least one component becomes zero. The task is to compute, for every input pair, how many such subtraction operations occur before termination.

The constraints allow up to 1000 pairs, with each value as large as 10^9. A solution that simulates each subtraction one-by-one can degrade to linear work per step. In the worst case, such as pairs of consecutive Fibonacci numbers, the number of operations is proportional to the magnitude of the numbers themselves, making direct simulation completely infeasible.

A subtle edge case appears when numbers are equal. For example, starting with (5, 5), the process performs one operation and immediately reaches (0, 5). Any reasoning that assumes strictly decreasing ratios or only considers unequal reductions must explicitly account for this termination behavior, otherwise it risks off-by-one errors in the final step count.

## Approaches

A direct simulation mimics the process exactly. At each step, we subtract the smaller value from the larger one and increment a counter. This is correct because it faithfully follows the rules, but its cost depends on how many subtraction steps are needed.

The key issue is that the process can take extremely many steps. In the worst case, when one number is only slightly larger than the other, each operation reduces the larger value by a tiny amount. This leads to a chain of updates proportional to the larger number, which is far beyond what is acceptable for values up to 10^9.

The crucial observation is that we are not changing the smaller number during repeated subtractions while the larger one stays significantly bigger. Instead, we are repeatedly subtracting the same value until the larger number drops below it. This is exactly integer division behavior. If a is much larger than b, then we perform floor(a / b) subtractions in one conceptual block, reducing a to a % b. This is the same transformation used in the Euclidean algorithm, except we also accumulate how many subtractions we compressed.

We repeatedly replace the larger value by its remainder against the smaller value, and we add the quotient to the answer. The process continues until one value becomes zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(max(a, b)) per pair | O(1) | Too slow |
| Euclidean Jump (Division Optimization) | O(log max(a, b)) per pair | O(1) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Treat the pair so that the first value is always the larger one. Swapping ensures we always perform reductions in a consistent direction, which simplifies reasoning about how many times we subtract.
2. If the smaller value is zero, stop immediately. No further operations are possible, so the accumulated count is already final.
3. Compute how many times the smaller value fits into the larger value using integer division. This quotient represents exactly how many subtraction operations the naive process would perform before the larger value drops below the smaller one.
4. Add this quotient to the running total of operations. This compresses many repeated single subtractions into one arithmetic step without changing the final state.
5. Replace the larger value by its remainder modulo the smaller value. This reflects the state after performing all those subtractions at once.
6. Swap roles again if necessary so that the larger value is always first, then repeat the process.

This iterative reduction mirrors the Euclidean algorithm, except that instead of only tracking gcd progress, we are also accumulating the total number of quotient steps taken at each reduction stage.

### Why it works

At any moment where a is greater than b, the subtraction process would repeatedly transform (a, b) into (a - b, b), then (a - 2b, b), and so on until a becomes less than b. The number of such steps is exactly floor(a / b), and the resulting value is a mod b. Because every subtraction preserves the invariant that the smaller number remains unchanged during this phase, compressing the entire sequence into a division does not skip or merge distinct structural states incorrectly. The process is therefore equivalent to summing all quotients encountered during the Euclidean reduction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_pair(a, b):
    ops = 0
    while b:
        if a < b:
            a, b = b, a
        ops += a // b
        a %= b
    return ops

def main():
    n = int(input())
    out = []
    for _ in range(n):
        a, b = map(int, input().split())
        out.append(str(solve_pair(a, b)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution is structured around repeatedly enforcing that we always subtract the smaller value from the larger one. The loop invariant is that `b` is the smaller element before each division step. The expression `a // b` counts exactly how many naive subtraction operations would occur before `a` drops below `b`, and `a %= b` updates the state to the remainder after all those subtractions.

The termination condition `while b:` ensures the process stops when one number becomes zero, matching the original stopping rule. The swap step is essential, since after taking a modulo, the roles of the numbers may reverse.

## Worked Examples

### Example 1: (24, 17)

We trace the compressed Euclidean steps.

| a | b | a // b | ops added | a % b |
| --- | --- | --- | --- | --- |
| 24 | 17 | 1 | 1 | 7 |
| 17 | 7 | 2 | 2 | 3 |
| 7 | 3 | 2 | 2 | 1 |
| 3 | 1 | 3 | 3 | 0 |

Final answer is 1 + 2 + 2 + 3 = 8.

This trace shows how each row corresponds to a full block of repeated subtractions in the original process. Each remainder step reflects the state after exhausting all possible subtractions with the current pair.

### Example 2: (10, 4)

| a | b | a // b | ops added | a % b |
| --- | --- | --- | --- | --- |
| 10 | 4 | 2 | 2 | 2 |
| 4 | 2 | 2 | 2 | 0 |

Total operations = 4.

This demonstrates that even small inputs can already contain multiple layers of repeated subtraction, and the algorithm compresses them cleanly into division steps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log max(a, b)) per pair | Each modulo step reduces at least one number to a strictly smaller remainder, mirroring Euclid’s algorithm depth |
| Space | O(1) | Only a constant number of variables are maintained per pair |

The logarithmic behavior follows from the fact that the Euclidean algorithm reduces the magnitude of numbers quickly, and the number of remainder steps is bounded by the number of digits in the inputs. With at most 1000 pairs, this comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve_pair(a, b):
        ops = 0
        while b:
            if a < b:
                a, b = b, a
            ops += a // b
            a %= b
        return ops

    n, *rest = map(int, inp.split())
    n = n
    lines = inp.strip().splitlines()[1:]
    out = []
    for line in lines:
        a, b = map(int, line.split())
        out.append(str(solve_pair(a, b)))
    return "\n".join(out)

# provided sample
assert run("1\n24 17\n") == "8"

# equal numbers
assert run("1\n5 5\n") == "1"

# one divides another
assert run("1\n10 2\n") == "5"

# chain-like case
assert run("1\n7 3\n") == "3"

# large numbers
assert run("1\n1000000000 999999999\n") == str((1000000000 // 999999999) + (999999999 // 1))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 5 | 1 | Equal values terminate immediately |
| 10 2 | 5 | Exact divisibility case |
| 7 3 | 3 | Multi-step Euclidean reduction |
| 1e9 999999999 | computed | Large boundary stress case |

## Edge Cases

When both numbers are equal, the algorithm performs exactly one operation before termination. For input (5, 5), the swap is irrelevant and the first division gives 5 // 5 = 1, after which the remainder becomes 0. The loop stops immediately, matching the rule that equality leads to a single subtraction step.

When one number is much larger than the other, such as (100, 1), the algorithm performs a single division step with quotient 100 and remainder 0. This matches the fact that the naive process would subtract 1 repeatedly until the larger number vanishes.

When the numbers are consecutive Fibonacci numbers, such as (21, 13), each modulo step reduces the pair to the previous Fibonacci pair, ensuring the process takes multiple Euclidean layers. The algorithm correctly accumulates each quotient, reflecting the long subtraction chain that would otherwise be explicit in the brute force simulation.
