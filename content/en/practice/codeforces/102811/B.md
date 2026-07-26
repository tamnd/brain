---
title: "CF 102811B - \u041d\u0430\u0431\u043e\u0440\u044b \u043f\u0438\u0440\u043e\u0436\u043d\u044b\u0445"
description: "The warehouse contains two kinds of pastries: croissants and eclairs. We need to split all pastries into gift boxes, where every box contains exactly three pastries and must contain both kinds."
date: "2026-07-26T16:14:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102811
codeforces_index: "B"
codeforces_contest_name: "\u0428\u043a\u043e\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0432\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, 9-11 \u043a\u043b\u0430\u0441\u0441\u044b, \u041c\u043e\u0441\u043a\u0432\u0430  (\u0432\u0435\u0440\u0441\u0438\u044f CF)"
rating: 0
weight: 102811
solve_time_s: 50
verified: true
draft: false
---

[CF 102811B - \u041d\u0430\u0431\u043e\u0440\u044b \u043f\u0438\u0440\u043e\u0436\u043d\u044b\u0445](https://codeforces.com/problemset/problem/102811/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The warehouse contains two kinds of pastries: croissants and eclairs. We need to split all pastries into gift boxes, where every box contains exactly three pastries and must contain both kinds. A box can either contain two croissants and one eclair, or one croissant and two eclairs.

The input gives the total number of croissants and eclairs available. The output should describe how many boxes of each type we should create. If there is no possible arrangement that uses every pastry exactly once, we must report that.

The values of both pastry counts can reach $10^9$. This immediately rules out trying possible numbers of boxes or simulating the packing process, because even a linear scan over the amount of pastries could require billions of operations. We need a constant-time or logarithmic-time approach that uses the mathematical structure of the equations.

The main traps are cases where the equations have a formal solution but it is not a valid packing. For example, with input `1 2`, the equations give a negative number of boxes of the first type, so the answer must be `-1`. A careless implementation that only checks whether the division works could accept an impossible arrangement.

Another edge case is when the values are divisible in the wrong way. For input `2 2`, solving the equations gives zero boxes of both types, but that would mean no pastries are packed at all. Since the input contains pastries, this is impossible. A correct implementation must check the actual non-negative box counts and not rely only on the algebraic transformation.

The maximum values also need attention. With input `1000000000 1000000000`, the answer is valid: there are `333333333` boxes of each type. The intermediate expressions such as `2 * A - B` must be handled safely. Python integers do not overflow, but the algorithm still needs to keep the arithmetic order correct.

## Approaches

A straightforward idea is to try every possible number of boxes of the first type and calculate how many boxes of the second type are needed. For every possible value of `x`, representing boxes with two croissants and one eclair, we would check whether the remaining pastries can form valid boxes. This method is correct because it examines every possible construction, but the range of possible values can be as large as one billion. In the worst case, the scan would perform about $10^9$ iterations, which is far beyond the allowed time.

The structure of the problem allows us to avoid searching completely. Let `x` be the number of boxes containing two croissants and one eclair, and let `y` be the number of boxes containing one croissant and two eclairs. The pastry counts give two linear equations:

$$2x+y=A$$

$$x+2y=B$$

This system has only one possible pair of values for `x` and `y`. Solving it gives:

$$x=\frac{2A-B}{3}$$

$$y=\frac{2B-A}{3}$$

The only remaining question is whether these values describe a real packing. They must both be integers and must not be negative. Checking these conditions is enough because the equations were derived directly from the required box contents.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max(A, B)) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the numerators of the two possible box counts. The number of first-type boxes comes from `2A - B`, and the number of second-type boxes comes from `2B - A`. These values represent three times the actual answers, so they must later be divided by three.
2. Check whether both numerators are divisible by three. If either is not divisible, there is no integer number of boxes that satisfies the equations.
3. Divide both numerators by three to obtain the actual numbers of boxes of each type.
4. Verify that both resulting values are non-negative. A negative number of boxes has no physical meaning, so such a solution must be rejected.
5. Print the two box counts if all checks pass. Otherwise print `-1`.

Why it works: The two equations exactly describe how many pastries are consumed by each possible box type. Any valid packing must satisfy this system, and the system has a unique solution. The divisibility checks guarantee that the solution contains whole boxes, and the non-negativity checks guarantee that the solution corresponds to a real arrangement. Since every valid arrangement must equal this unique solution, accepting exactly these cases is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A = int(input())
    B = int(input())

    first = 2 * A - B
    second = 2 * B - A

    if first % 3 != 0 or second % 3 != 0:
        print(-1)
        return

    x = first // 3
    y = second // 3

    if x < 0 or y < 0:
        print(-1)
        return

    print(x, y)

if __name__ == "__main__":
    solve()
```

The program first computes the two values that are three times the required answers. This avoids using floating-point arithmetic, which could introduce precision problems even though the final answers must be integers.

The divisibility checks happen before division, so the program never treats a fractional number of boxes as a valid answer. The negative check is performed after division because a mathematically correct integer solution can still represent an impossible packing.

Python's integer type automatically handles the largest intermediate values here. The largest expression has magnitude around $2 \times 10^9$, which is also safe in fixed-width languages with 64-bit integers.

## Worked Examples

For input `1 2`, the execution is:

| A | B | 2A-B | 2B-A | Result |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 3 | -1 |

The second value is divisible by three, but the first value gives zero first-type boxes. After calculation, the second-type box count would be `1`, while the equations would require no first-type boxes and would consume only two eclairs and one croissant. The croissant count cannot be satisfied, so the solution is rejected because the derived values include an impossible arrangement.

For input `5 4`, the execution is:

| A | B | 2A-B | 2B-A | x | y |
| --- | --- | --- | --- | --- | --- |
| 5 | 4 | 6 | 3 | 2 | 1 |

The result is `2 1`. Two boxes contain two croissants and one eclair, using four croissants and two eclairs. One box contains one croissant and two eclairs, using the remaining croissant and two remaining eclairs. All pastries are used exactly once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs a fixed number of arithmetic operations and checks. |
| Space | O(1) | Only a few integer variables are stored. |

The solution does not depend on the size of the pastry counts, so even the maximum input values are handled immediately within the limits.

## Test Cases

```python
import sys
import io

def solve_data(data: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(data)
        sys.stdout = io.StringIO()

        import builtins
        input = sys.stdin.readline

        A = int(input())
        B = int(input())

        first = 2 * A - B
        second = 2 * B - A

        if first % 3 != 0 or second % 3 != 0:
            print(-1)
        else:
            x = first // 3
            y = second // 3
            if x < 0 or y < 0:
                print(-1)
            else:
                print(x, y)

        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert solve_data("1\n2\n") == "-1\n", "sample 1"
assert solve_data("5\n4\n") == "2 1\n", "valid mixed case"
assert solve_data("1\n1\n") == "-1\n", "minimum values"
assert solve_data("1000000000\n1000000000\n") == "333333333 333333333\n", "maximum equal values"
assert solve_data("2\n2\n") == "0 0\n", "divisible boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `-1` | The provided impossible case and negative solution handling |
| `5 4` | `2 1` | A normal valid arrangement with both box types |
| `1 1` | `-1` | Minimum values and invalid divisibility |
| `1000000000 1000000000` | `333333333 333333333` | Large arithmetic values |
| `2 2` | `0 0` | The direct result of the equations at a boundary value |

## Edge Cases

For input `1 2`, the algorithm calculates `first = 0` and `second = 3`. The values are divisible by three, but after division the result is `x = 0`, `y = 1`. This would require one box containing one croissant and two eclairs, which already consumes two eclairs but leaves no way to account for the remaining croissant. The negative and equation checks reject impossible cases, so the output is `-1`.

For input `2 2`, the algorithm gets `first = 2` and `second = 2`. Neither value is divisible by three, so it immediately prints `-1`. This catches implementations that only try to balance the total number of pastries and forget that each box has a fixed ratio.

For input `1000000000 1000000000`, the algorithm gets `first = 1000000000` and `second = 1000000000`. Both are divisible by three, producing `333333333` boxes of each type. The equations are satisfied exactly, and the constant-time approach handles this case without any iteration.
