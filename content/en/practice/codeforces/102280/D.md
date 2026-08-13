---
title: "CF 102280D - \u0422\u0430\u0440\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f"
description: "A route has a value k. If a passenger wants to travel through n stops, the fare is the n-th k-gonal number. For k = 4, these are square numbers, for k = 3 they are triangular numbers, and larger values of k describe regular polygonal figures with more sides."
date: "2026-08-13T09:45:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102280
codeforces_index: "D"
codeforces_contest_name: "2010, \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430 \u0421\u0413\u0410\u0423 aka \u041a\u043e\u043d\u0442\u0435\u0441\u0442 \u043f\u0440\u043e \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0438"
rating: 0
weight: 102280
solve_time_s: 367
verified: true
draft: false
---

[CF 102280D - \u0422\u0430\u0440\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f](https://codeforces.com/problemset/problem/102280/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

A route has a value `k`. If a passenger wants to travel through `n` stops, the fare is the `n`-th `k`-gonal number. For `k = 4`, these are square numbers, for `k = 3` they are triangular numbers, and larger values of `k` describe regular polygonal figures with more sides.

The input contains two integers, `n` and `k`. Here `n` is the number of stops the passenger wants to travel, and `k` determines which polygonal-number sequence the route uses. We need to output the `n`-th `k`-gonal number.

The key formula for the `n`-th polygonal number is

[
P_k(n)=\frac{(k-2)n^2-(k-4)n}{2}.
]

The constraints allow `n` to reach (10^8) and `k` to reach `100`. The input contains only one pair of values, so the intended solution should not depend on `n`. A loop running once for every stop would already require up to (10^8) iterations, which is unnecessarily expensive under a 0.5 second limit. The formula gives a constant-time solution with only a few arithmetic operations.

There are two boundary cases that are easy to mishandle. First, `n = 0` must produce zero. For example, the input `0 4` has output `0`. A formula or implementation that assumes polygonal numbering starts from `n = 1` and performs some special initialization can accidentally return `1`.

Second, the division must be performed after the numerator has been formed. For example, `4 5` gives

# \frac{48-4}{2}

1. 

]

A careless implementation that uses an incorrect triangular-number formula, or drops the linear term, would produce the wrong value. The square case gives another useful check: `4 4` produces (4^2=16).

## Approaches

A direct approach is to construct the polygonal figure layer by layer. The first polygonal number is `1`, and each following layer adds a number of points determined by `k` and the current layer. This is correct because polygonal numbers are defined exactly by adding successive geometric layers.

The problem is that such a simulation needs one iteration for each value up to `n`. With `n = 10^8`, the worst case is on the order of (10^8) iterations. In Python this is far beyond what a 0.5 second contest limit can reasonably allow, and even in a faster language it is solving a problem that has a closed-form expression.

The useful observation is that the layer sizes form an arithmetic progression. For a `k`-gonal sequence, the increase from one term to the next is

[
(k-2)n-(k-3).
]

Starting with (P_k(1)=1), summing these arithmetic increments gives a quadratic expression in `n`. After simplifying the sum, we obtain

[
P_k(n)=\frac{(k-2)n^2-(k-4)n}{2}.
]

The brute-force method works because it explicitly performs this summation, but it fails when `n` is large. The closed form performs the same summation algebraically, reducing the whole computation to constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `k`. They completely determine the requested polygonal number, so no additional data structure is needed.
2. Compute the numerator

[
(k-2)n^2-(k-4)n.
]

This is the standard closed form obtained by summing the arithmetic progression of layer sizes.
3. Divide the numerator by `2` and print the result. Polygonal numbers are integers, so the division is exact.

### Why it works

The `k`-gonal sequence starts with (P_k(1)=1), and its consecutive differences form the arithmetic progression

[
k-2,\ 2(k-2)-(k-4),\ 3(k-2)-(k-4),\ldots
]

which simplifies to

[
(k-2)n-(k-3).
]

Summing these differences from the first term through the `n`-th term gives

# \frac{n((k-2)n-(k-4))}{2}

\frac{(k-2)n^2-(k-4)n}{2}.
]

The algorithm evaluates exactly this mathematical definition, so the printed value is the required fare for every valid `n` and `k`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())

answer = ((k - 2) * n * n - (k - 4) * n) // 2
print(answer)
```

The first line reads the only input pair. There are no test cases to iterate over because the statement provides exactly one `n` and one `k`.

The expression follows the closed form directly. Computing `n * n` before multiplying by `k - 2` keeps the correspondence with the formula clear. Python integers have arbitrary precision, so there is no overflow problem even at the maximum input size.

The `// 2` operation is safe because the numerator is always even for integer `n` and `k`. Using integer division also guarantees that the output is printed as an integer rather than as a floating-point value.

The case `n = 0` requires no special branch. Both terms in the numerator contain `n`, so the expression naturally evaluates to zero.

## Worked Examples

For the first sample, `n = 4` and `k = 4`. A value of `4` means square numbers, so the expected result is (4^2=16).

| Step | `n` | `k` | `(k - 2) * n * n` | `(k - 4) * n` | Numerator | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 32 | 0 | 32 | 16 |

The formula reduces to (2n^2/2=n^2) when `k = 4`, confirming that the general formula agrees with ordinary squares.

For the second sample, `n = 4` and `k = 5`. These are pentagonal numbers.

| Step | `n` | `k` | `(k - 2) * n * n` | `(k - 4) * n` | Numerator | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 5 | 48 | 4 | 44 | 22 |

The result is `22`, the fourth pentagonal number. The same calculation also shows why the linear correction term involving `k - 4` cannot be omitted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed. |
| Space | O(1) | The algorithm stores only `n`, `k`, and the resulting integer. |

The maximum `n` is (10^8), but the algorithm never iterates up to `n`. It performs a constant number of operations, so it easily fits the 0.5 second time limit. Python's arbitrary-precision integers also safely handle the largest possible result, which is about (4.9\cdot10^{17}) for `n = 10^8` and `k = 100`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    n, k = map(int, input().split())
    answer = ((k - 2) * n * n - (k - 4) * n) // 2
    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("4 4\n") == "16\n", "sample 1"
assert run("4 5\n") == "22\n", "sample 2"

# Minimum n
assert run("0 3\n") == "0\n", "zero stops"

# Minimum polygon size, triangular numbers
assert run("1 3\n") == "1\n", "first triangular number"

# Square numbers, catches the linear-term handling
assert run("5 4\n") == "25\n", "fifth square number"

# Maximum values
assert run("100000000 100\n") == "489999995200000000\n", "maximum constraints"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 3` | `0` | Minimum `n` and zero handling |
| `1 3` | `1` | First polygonal number and indexing boundary |
| `5 4` | `25` | Square-number special case |
| `100000000 100` | `489999995200000000` | Maximum constraints and large integer arithmetic |

## Edge Cases

The first edge case is `n = 0`. For input `0 4`, the algorithm computes

# \frac{0}{2}

1. 

]

No special condition is required, and the output is `0`. An implementation that starts from the first geometric layer and assumes at least one layer exists could incorrectly return `1`.

The second edge case is the first valid value, `n = 1`. For input `1 3`, the calculation is

# \frac{1+1}{2}

1. 

]

This confirms that the sequence is indexed in the standard way, with the first polygonal number equal to `1`. An off-by-one implementation based on the number of added layers could accidentally produce the second triangular number instead.

The square case is another useful boundary check. For input `5 4`, the formula becomes

# \frac{50}{2}

1. 

]

The linear term disappears exactly when `k = 4`, leaving the familiar square formula.

Finally, consider the largest possible input, `100000000 100`. The algorithm performs no loop at all. It evaluates

489999995200000000.
]

The result fits comfortably in Python's integer representation, and the running time remains constant despite `n` being as large as (10^8).
