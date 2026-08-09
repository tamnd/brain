---
title: "CF 102440C - A + B = C"
description: "We are given exactly three integers, and we may reorder them. The goal is to print an ordering x y z such that x + y = z. If no permutation has this property, we print -1 -1 -1. Any valid ordering is accepted. The input values satisfy -2^63 < ai < 2^63."
date: "2026-08-09T13:19:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "C"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 530
verified: true
draft: false
---

[CF 102440C - A + B = C](https://codeforces.com/problemset/problem/102440/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given exactly three integers, and we may reorder them. The goal is to print an ordering `x y z` such that `x + y = z`. If no permutation has this property, we print `-1 -1 -1`. Any valid ordering is accepted.

The input values satisfy `-2^63 < a_i < 2^63`. The numbers can therefore be close to the limits of signed 64-bit integers, so an implementation should avoid assumptions that values fit into a smaller integer type. Python integers have arbitrary precision, so arithmetic such as `a + b` is safe even when the mathematical sum is outside the input range.

There are only three numbers. That makes the search space constant: there are at most six permutations, and checking each one takes constant time. Even a direct enumeration of all permutations is easily fast enough. The interesting part of the problem is not performance, but recognizing that there are only three possible choices for which number acts as `C`.

Several edge cases can make a careless implementation fail. First, the numbers can contain zero. For input `0 0 0`, the correct output is `0 0 0`, because `0 + 0 = 0`. An implementation that treats zero as a special failure value would be wrong.

Duplicate values are also valid. For input `1 1 2`, the output `1 1 2` works because `1 + 1 = 2`. A solution that assumes all three numbers must be distinct would reject a valid case.

Negative values require no special treatment. For input `-5 2 -3`, the correct output is `-5 2 -3`, since `-5 + 2 = -3`. Looking only for positive sums would incorrectly reject it.

Finally, the input values can be near the 64-bit boundary. For example, `9223372036854775807 -1 9223372036854775806` has a valid ordering. A fixed-width implementation that performs an overflowing addition before comparing it could produce an incorrect result, while Python handles the calculation exactly.

## Approaches

The most direct approach is to try every possible ordering of the three numbers. There are `3! = 6` permutations. For each permutation, we check whether the first two values add up to the third. If one permutation satisfies the equation, we print it immediately. If all six fail, no valid ordering exists.

This brute-force method is already optimal for the actual problem. Its worst case performs exactly six checks, so its running time is `O(6)`, which is simply `O(1)`. There is no input size that can make six checks too slow.

We can make the constant amount of work even smaller by observing that the only meaningful choice is which of the three numbers becomes `C`. If `a` is `C`, the other two must be `b` and `c`, so we check `b + c = a`. Likewise, we check `a + c = b` and `a + b = c`. These are exactly the three possible equations, and each successful equation immediately gives the required ordering.

The brute-force approach works because the permutation space is tiny. The structural observation lets us avoid generating permutations altogether, reducing the solution to three arithmetic comparisons. Both approaches are accepted, but the direct three-check version is simpler and makes the reasoning especially transparent.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1), at most 6 permutations | O(1) | Accepted |
| Optimal | O(1), 3 equations | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three integers as `a`, `b`, and `c`. We keep their original order because each of the three possible choices for the right-hand side can then be checked directly.
2. Check whether `a + b = c`. If it is true, print `a b c`. Here `c` is the chosen right-hand side, while `a` and `b` are the two addends.
3. Otherwise, check whether `a + c = b`. If it is true, print `a c b`. This uses `b` as the right-hand side and places the other two values first.
4. Otherwise, check whether `b + c = a`. If it is true, print `b c a`. This is the final possible choice for the right-hand side.
5. If none of the three equations holds, print `-1 -1 -1`. Every possible ordering must choose exactly one of the three input values as the third value, so all possible cases have now been exhausted.

### Why it works

The key invariant is that every valid ordering must designate exactly one input number as the right-hand side `C`. If `C` is `c`, the required equation is `a + b = c`. If `C` is `b`, it is `a + c = b`. If `C` is `a`, it is `b + c = a`. The algorithm checks precisely these three possibilities, so whenever it prints a valid ordering, that ordering satisfies the required equation. If all three checks fail, no choice of `C` can work, which means no permutation can be a solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, c = map(int, input().split())

    if a + b == c:
        print(a, b, c)
    elif a + c == b:
        print(a, c, b)
    elif b + c == a:
        print(b, c, a)
    else:
        print(-1, -1, -1)

if __name__ == "__main__":
    solve()
```

The first line of `solve` reads exactly the three input integers. There are no test cases to loop over because the problem provides one triple.

The first condition corresponds to the first algorithm step and uses `c` as the result. The second condition swaps `b` and `c` in the output because `b` is now the result. The third condition similarly places `a` last.

The checks use `elif`, so once a valid ordering is found, no later case can replace it. This also handles duplicate values correctly. For example, with `0 0 0`, the first condition succeeds and the program prints the original ordering.

Python's arbitrary-precision integers are useful at the numerical boundaries. The input values can be close to `2^63`, and an intermediate sum can exceed the signed 64-bit range, but Python evaluates the sum without overflow.

## Worked Examples

### Sample 1

For the input `2 1 3`, the algorithm evaluates the possible right-hand sides in the original order.

| `a` | `b` | `c` | Check | Result |
| --- | --- | --- | --- | --- |
| 2 | 1 | 3 | `2 + 1 = 3` | True |

The first equation succeeds immediately, so the program prints `2 1 3`. The sample output uses `1 2 3`, which is also valid because `1 + 2 = 3`. The problem allows any valid ordering.

### Sample 2

For `2 4 42`, none of the three values can be the sum of the other two.

| `a` | `b` | `c` | Check | Result |
| --- | --- | --- | --- | --- |
| 2 | 4 | 42 | `2 + 4 = 42` | False |
| 2 | 4 | 42 | `2 + 42 = 4` | False |
| 2 | 4 | 42 | `4 + 42 = 2` | False |

All possible choices for the right-hand side have failed, so the program prints `-1 -1 -1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Exactly three additions and comparisons are performed in the worst case. |
| Space | O(1) | Only the three input integers are stored. |

The input contains only three numbers, so the solution performs a fixed amount of work regardless of their magnitude. The memory usage is also constant. The absence of a large `n` means there is no meaningful performance pressure here, and the solution comfortably fits any standard Codeforces limits for this problem.

## Test Cases

```python
import sys
import io

def solve():
    a, b, c = map(int, input().split())

    if a + b == c:
        print(a, b, c)
    elif a + c == b:
        print(a, c, b)
    elif b + c == a:
        print(b, c, a)
    else:
        print(-1, -1, -1)

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            solve()
            return sys.stdout.getvalue().strip()
        finally:
            sys.stdout = old_stdout
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run("2 1 3\n") == "2 1 3", "sample 1"
assert run("2 4 42\n") == "-1 -1 -1", "sample 2"

# All equal values
assert run("0 0 0\n") == "0 0 0", "all equal values"

# Maximum positive boundary
assert run("9223372036854775807 -1 9223372036854775806") == \
       "9223372036854775807 -1 9223372036854775806", \
       "maximum positive boundary"

# Minimum negative boundary
assert run("-9223372036854775807 1 -9223372036854775806") == \
       "-9223372036854775807 1 -9223372036854775806", \
       "minimum negative boundary"

# Valid equation appears only when the second value is the result
assert run("5 7 12\n") == "5 7 12", "direct sum"

# Valid equation appears when the first value is the result
assert run("12 5 7\n") == "5 7 12", "first value is the sum"

# No valid permutation
assert run("-10 3 8\n") == "-1 -1 -1", "no solution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 3` | `2 1 3` | Provided sample with a valid sum |
| `2 4 42` | `-1 -1 -1` | Provided sample with no valid ordering |
| `0 0 0` | `0 0 0` | All-equal values and zero |
| `9223372036854775807 -1 9223372036854775806` | Same ordering | Upper 64-bit input boundary and large intermediate values |
| `-9223372036854775807 1 -9223372036854775806` | Same ordering | Lower 64-bit input boundary |
| `12 5 7` | `5 7 12` | The first input value must be placed last |
| `-10 3 8` | `-1 -1 -1` | Negative values with no solution |

## Edge Cases

The all-zero case `0 0 0` reaches the first condition because `0 + 0 = 0`. The algorithm prints `0 0 0`, so duplicate values and zero require no special branch.

For duplicate nonzero values, consider `1 1 2`. The first check gives `1 + 1 = 2`, so the program prints `1 1 2`. The fact that two input positions contain the same value does not change the arithmetic or invalidate the ordering.

For negative values, consider `-5 2 -3`. The first check succeeds because `-5 + 2 = -3`, and the program prints `-5 2 -3`. The algorithm never assumes that the operands or result are positive.

For a case where the first input value is the sum, consider `12 5 7`. The first check tests `12 + 5 = 7` and fails. The second tests `12 + 7 = 5` and fails. The third tests `5 + 7 = 12` and succeeds, so the output is `5 7 12`. This confirms that the algorithm checks all three possible choices for the right-hand side.

At the numerical boundary, `9223372036854775807 -1 9223372036854775806` satisfies `9223372036854775807 + (-1) = 9223372036854775806`. Python computes this exactly, so the boundary value does not introduce overflow or truncation.

Finally, `2 4 42` exercises the failure path. The three possible equations are `2 + 4 = 42`, `2 + 42 = 4`, and `4 + 42 = 2`, all false. Since every possible choice of the third value has been rejected, `-1 -1 -1` is the only correct response.
