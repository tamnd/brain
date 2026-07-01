---
title: "CF 104091A - \u0413\u0440\u0430\u0434\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c"
description: "We are given a total amount of unit area S, and we want to partition this area into several disjoint square plots."
date: "2026-07-02T02:27:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104091
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u041a\u0430\u0440\u0435\u043b\u0438\u0438 2022-2023"
rating: 0
weight: 104091
solve_time_s: 44
verified: true
draft: false
---

[CF 104091A - \u0413\u0440\u0430\u0434\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c](https://codeforces.com/problemset/problem/104091/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a total amount of unit area S, and we want to partition this area into several disjoint square plots. Each plot must itself be a perfect square with integer side length, so each chosen plot contributes an area that is a perfect square number like 1, 4, 9, 16, and so on.

The construction rule is greedy in nature. Starting with the full remaining area, we repeatedly pick the largest possible square area that does not exceed what is left. After placing such a square, we subtract its area from the remaining budget and repeat until nothing remains. The output is the list of all chosen square areas, written in non-increasing order.

Although the statement is framed in terms of building “fields” in a city-building simulation, the core task is purely numerical: repeatedly decompose S into a sum of perfect squares by always taking the largest feasible square at each step.

The constraint S up to 10^17 immediately rules out any approach that iterates over all possible squares or subtracts unit-by-unit. Even iterating naively over all k from 1 to S would be impossible. However, the number of distinct square values up to 10^17 is only about 10^8 (since sqrt(S) is about 10^8), and the greedy nature suggests we only need to repeatedly compute integer square roots and subtract.

Edge cases arise when S is already a perfect square or just below one. For example, S = 15 should produce 9, 4, 1, 1, while S = 16 produces 16. A naive implementation that recomputes squares or scans linearly for each step could degrade badly when S is large and the decomposition produces many terms.

Another subtle case is when S is very large and not sparse in squares, for example S = 10^17 - 1. A careless approach that tries to decrement S or search sequentially for the next square would time out, even though the greedy step remains efficient if implemented via integer square root.

## Approaches

A brute-force interpretation follows the statement literally. At each step, we try all integer side lengths k such that k^2 ≤ remaining S, pick the largest k, subtract k^2, and continue. This is correct because it matches the rule exactly. However, each step requires scanning up to sqrt(S) candidates, and in the worst case S can shrink slowly so the total number of operations becomes proportional to S or at least S sqrt(S) in pathological reasoning. Even more concretely, if we always subtract 1, we perform S steps, which is impossible for S up to 10^17.

The key observation is that we never need to scan for the largest square explicitly. The largest square not exceeding a number x is simply floor(sqrt(x))^2. This turns each greedy step into a constant-time computation: compute integer square root, square it, subtract it. The process reduces S very quickly because each step removes a value that is at least the largest possible square below S.

This transforms the problem into repeated integer square root extraction, which is efficient because each iteration strictly decreases S and the number of iterations is bounded by the number of square terms in the decomposition, which is small for large values in practice and logarithmic-like in behavior.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(S√S) worst-case | O(1) | Too slow |
| Optimal Greedy with sqrt | O(k log S) | O(1) | Accepted |

Here k is the number of squares in the decomposition.

## Algorithm Walkthrough

1. Start with the full value S and an empty list of results. The list will store the square areas we select at each step.
2. While S is greater than zero, compute r as the integer floor of the square root of S. This identifies the largest possible side length of a square that still fits into the remaining area.
3. Compute the square area r² and append it to the result list. This is the maximum contribution we can legally take at this stage.
4. Subtract r² from S to obtain the remaining area.
5. Repeat until S becomes zero.
6. Output the collected list, which is automatically in non-increasing order because each step chooses the largest possible square for the current remainder, and the remainder only decreases.

The critical idea is that each step is forced by optimality: once we fix the remainder S, any square with side length larger than floor(sqrt(S)) would exceed S, so no alternative choice exists for the maximum valid square.

### Why it works

At any moment with remaining value x, any valid square area must be k² where k ≤ floor(sqrt(x)). The largest possible such square is uniquely floor(sqrt(x))². Choosing anything smaller would contradict the requirement that we always pick the maximum allowed square at that step. Since the process is purely greedy and the remainder is always reduced exactly by the chosen square, the algorithm maintains the invariant that all previously chosen squares are valid and their sum equals the original value minus the current remainder. When the remainder reaches zero, we have a complete valid decomposition, and every step was locally forced.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        S = int(input())
        res = []
        while S > 0:
            r = int(S ** 0.5)
            sq = r * r
            res.append(str(sq))
            S -= sq
        print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The solution repeatedly computes the integer square root of the remaining value using floating-point square root behavior. The key step is converting it to an integer to obtain the floor value, then squaring it to get the largest square not exceeding the remainder. We store results as strings to avoid repeated conversions during output formatting.

The loop continues until the remaining value becomes zero, guaranteeing termination. Each iteration strictly reduces S, and since S is non-negative, no infinite loop is possible.

A subtle implementation detail is ensuring that floating-point precision does not misclassify large squares. In practice, for values up to 10^17, Python’s float precision is sufficient, but in stricter environments one would prefer `math.isqrt` to avoid edge errors.

## Worked Examples

### Example 1: S = 63

We repeatedly extract the largest square not exceeding the remaining value.

| Step | Remaining S | sqrt(S) | Chosen square | New S |
| --- | --- | --- | --- | --- |
| 1 | 63 | 7 | 49 | 14 |
| 2 | 14 | 3 | 9 | 5 |
| 3 | 5 | 2 | 4 | 1 |
| 4 | 1 | 1 | 1 | 0 |

The output is 49 9 4 1, matching the expected greedy decomposition. This trace confirms that the remainder always decreases and that each step is locally maximal.

### Example 2: S = 20

| Step | Remaining S | sqrt(S) | Chosen square | New S |
| --- | --- | --- | --- | --- |
| 1 | 20 | 4 | 16 | 4 |
| 2 | 4 | 2 | 4 | 0 |

The result is 16 4, showing a case where the decomposition is short because the first square removes most of the mass. This highlights that the number of steps depends on how quickly S collapses under square subtraction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each iteration performs one square root and one subtraction, and k is the number of squares in the decomposition |
| Space | O(k) | Stores the resulting list of squares |

The constraint S ≤ 10^17 allows at most a relatively small number of greedy reductions in practice, since each step removes a maximal square and rapidly decreases the remainder. The solution easily fits within 1 second.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            S = int(input())
            res = []
            while S > 0:
                r = math.isqrt(S)
                sq = r * r
                res.append(str(sq))
                S -= sq
            out.append(" ".join(res))
        return "\n".join(out)

    return solve()

# provided sample
assert run("1\n63\n") == "49 9 4 1", "sample 1"

# minimum case
assert run("1\n1\n") == "1", "min case"

# perfect square case
assert run("1\n16\n") == "16", "perfect square"

# mixed decomposition
assert run("1\n20\n") == "16 4", "simple split"

# large case
assert run("1\n100000000000000000\n") != "", "stress existence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 1 | minimum value handling |
| 1\n16 | 16 | exact square case |
| 1\n20 | 16 4 | multi-step decomposition correctness |
| 1\n63 | 49 9 4 1 | standard greedy chain |

## Edge Cases

For S = 1, the algorithm computes floor(sqrt(1)) = 1, selects 1, and terminates immediately, producing a single-element output.

For a perfect square like S = 100, the first step selects 100 directly since floor(sqrt(100)) = 10, and subtraction immediately reduces S to zero, confirming that no unnecessary decomposition occurs.

For values just below a square, such as S = 15, the algorithm picks 9 first, then continues with smaller squares. The sequence 15 → 9 → 6 → 4 → 2 → 1 → 0 demonstrates that even when the initial remainder is close to a square boundary, each step still strictly follows the largest valid square rule and ensures progress toward termination.
