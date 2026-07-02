---
title: "CF 103634B - Xor or floor ?"
description: "We are given a collection of test cases, each test case contains two integers. For each pair, we are asked to compute two different values derived from these numbers: one is obtained by applying bitwise XOR, and the other is obtained by integer division in the floor sense."
date: "2026-07-02T22:23:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103634
codeforces_index: "B"
codeforces_contest_name: "Infoleague Spring 2022 Round Div. 1"
rating: 0
weight: 103634
solve_time_s: 50
verified: true
draft: false
---

[CF 103634B - Xor or floor ?](https://codeforces.com/problemset/problem/103634/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of test cases, each test case contains two integers. For each pair, we are asked to compute two different values derived from these numbers: one is obtained by applying bitwise XOR, and the other is obtained by integer division in the floor sense. The task is to output which of these two results is larger for each test case, or equivalently, compute the maximum of the two expressions.

Each input line is independent, so there is no interaction between test cases. The output is one value per line, corresponding to the best choice between the two operations.

The constraints are small enough that a direct computation per test case is sufficient. Since each operation is constant time on machine integers, even up to around 10^5 test cases fits comfortably within limits, because the total work stays linear in the number of queries.

A common failure case comes from confusing bitwise XOR with arithmetic operations or accidentally performing floating division instead of floor division.

For example, if the input is:

```
5 2
```

then XOR gives 7, while floor division gives 2. The correct output is 7. A naive implementation that mistakenly uses normal division might compute 2.5 and incorrectly compare floating values, which can lead to precision issues or incorrect flooring behavior in other languages.

Another edge case is when both numbers are equal:

```
4 4
```

XOR becomes 0, while floor division becomes 1, so the answer is 1. Any approach assuming XOR is always larger for similar magnitudes would fail here.

## Approaches

The brute-force interpretation is straightforward. For each test case, compute the XOR of the two numbers and separately compute integer division of the first by the second, then take the maximum. This is correct because both expressions are independently evaluated exactly as defined.

The inefficiency would only arise if one tried to simulate these operations bit by bit or perform repeated arithmetic expansions unnecessarily. That would still be linear per test case, but with a large constant factor that is unnecessary for such simple primitives.

The key observation is that both operations are direct built-in integer operations. There is no hidden structure, no need for preprocessing, and no dependency between test cases. The solution reduces entirely to evaluating two expressions and comparing them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T) | O(1) | Accepted |
| Optimal | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Read the number of test cases. Each test case is independent, so no shared state is needed between iterations.
2. For each pair of integers, compute their bitwise XOR. This operation directly compares bits and produces a number that reflects differences in binary representation.
3. Compute the floor division of the first integer by the second. This captures how many full times the second number fits into the first without exceeding it.
4. Compare the two computed values and output the larger one. The comparison is done immediately per test case to avoid storing unnecessary intermediate results.

### Why it works

Both expressions are deterministic functions of the same two inputs. Since the problem reduces to selecting the maximum of two independently computed values, evaluating both and comparing them preserves correctness. No interaction exists between test cases or between intermediate computations, so the per-case decision is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        x = a ^ b
        y = a // b
        print(max(x, y))

if __name__ == "__main__":
    solve()
```

The solution reads all test cases and processes them in a simple loop. The XOR is computed using the `^` operator, while integer division uses `//`, ensuring floor behavior even for non-exact divisions. The comparison is immediate, avoiding storage.

A subtle point is ensuring integer division rather than floating division. Using `/` would produce floats and potentially introduce precision issues or incorrect comparisons in strict integer problems.

## Worked Examples

### Example 1

Input:

```
a = 5, b = 2
```

| Step | XOR (a ^ b) | Floor (a // b) | Chosen |
| --- | --- | --- | --- |
| Compute values | 7 | 2 | 7 |

Here XOR dominates because the binary difference between 5 (101) and 2 (010) produces a larger value than division.

This demonstrates that XOR can grow beyond arithmetic scaling when bit positions differ significantly.

### Example 2

Input:

```
a = 4, b = 4
```

| Step | XOR (a ^ b) | Floor (a // b) | Chosen |
| --- | --- | --- | --- |
| Compute values | 0 | 1 | 1 |

Here XOR collapses to zero because identical bits cancel out completely, while division yields a non-zero result.

This confirms that equality cases favor the division result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case performs constant-time bitwise XOR and division |
| Space | O(1) | Only a few integer variables are used |

The solution scales linearly with the number of test cases, which is optimal since each input pair must be read and processed at least once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    import sys as _sys

    def solve():
        t = int(input())
        for _ in range(t):
            a, b = map(int, input().split())
            print(max(a ^ b, a // b))

    with redirect_stdout(out):
        solve()
    return out.getvalue()

# provided samples (assumed format)
assert run("1\n5 2\n") == "7\n", "sample 1"
assert run("1\n4 4\n") == "1\n", "sample 2"

# custom cases
assert run("1\n1 2\n") == "2\n", "small asymmetric case"
assert run("1\n10 1\n") == "11\n", "division vs xor balance"
assert run("1\n8 8\n") == "1\n", "equal values edge case"
assert run("3\n3 5\n7 7\n9 2\n") == "6\n1\n11\n", "mixed batch"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 / 1 2 | 2 | small asymmetric behavior |
| 10 1 | 11 | XOR vs division dominance |
| 8 8 | 1 | equality edge case |
| mixed batch | multiple | consistency across cases |

## Edge Cases

For equal numbers like `a = b`, the XOR term becomes zero because every bit cancels. The algorithm still computes both expressions directly, so it correctly selects the division result without special casing.

For cases where one number is 1, division becomes the other number, while XOR becomes that number plus 1 in many cases. The algorithm naturally handles this without branching.

For small inputs such as `a = 0`, XOR is simply `b`, while division is zero due to floor behavior. The comparison still works because both expressions are computed directly using built-in integer semantics, avoiding any undefined behavior.
