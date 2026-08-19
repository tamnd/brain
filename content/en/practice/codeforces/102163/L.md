---
title: "CF 102163L - Chemistry Exam"
description: "Each student's exam paper is encoded as an integer. The binary representation of that integer records the student's answers, with a 1 meaning the answer to that question was correct and a 0 meaning it was incorrect."
date: "2026-08-19T15:07:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "L"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 613
verified: false
draft: false
---

[CF 102163L - Chemistry Exam](https://codeforces.com/problemset/problem/102163/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 13s  
**Verified:** no  

## Solution
## Problem Understanding

Each student's exam paper is encoded as an integer. The binary representation of that integer records the student's answers, with a `1` meaning the answer to that question was correct and a `0` meaning it was incorrect. The task is to determine the number of correct answers for every student, so for each value `A_i` we need the number of `1` bits in its binary representation.

For example, `5` is `101` in binary, so it contains two `1` bits and the corresponding student receives `2` marks. Similarly, `8` is `1000`, so its answer is `1`.

The number of students in one test case can reach `10^5`, and each encoded paper can be as large as `10^9`. Since `10^9 < 2^30`, every number has at most 30 relevant binary bits. An approach that performs a constant amount of work per bit is already effectively linear in `N`, because it performs at most about three million bit operations for `10^5` students. An approach that compares every pair of students would require about `10^10` comparisons and is immediately unsuitable. Since the input contains multiple test cases, using Python's integer bit operations directly is preferable to explicitly simulating the bits.

There are a few small cases where an implementation can go wrong. The smallest valid paper is `1`, whose binary form is `1`, so the answer is `1`. An implementation that accidentally starts checking bits from position `1` instead of position `0` would incorrectly produce zero.

Another boundary case is a power of two. For example, the input

```
1
4
1 2 4 8
```

must produce

```
1 1 1 1
```

Every power of two has exactly one set bit. Code that tries to infer the number of marks from the magnitude of the number rather than its binary representation can easily get this wrong.

The opposite case is a number with several set bits. For

```
1
1
7
```

the output is

```
3
```

because `7 = 111₂`. A common mistake is to count the number of binary digits rather than the number of `1` digits, which would also happen to work for `7` but fails for a value such as `8`, where the correct answer is `1` while the binary length is `4`.

Finally, the upper boundary matters because `10^9` is not a special binary value. Its answer is the number of set bits in its ordinary binary representation, and Python integers handle this value directly without overflow.

## Approaches

The direct approach is to examine the binary representation of every student's number and count its `1` bits. One way to do this without constructing a string is to repeatedly inspect the least significant bit with `x & 1`, add it to the answer, and shift `x` right by one position. The method is correct because every iteration removes exactly one binary digit, and every original `1` contributes exactly once to the count.

Since every `A_i` is at most `10^9`, at most 30 iterations are needed for one number. For `N = 10^5`, that means at most about `3 × 10^6` bit inspections for one test case. That is not asymptotically bad, but Python can do the same operation more efficiently using its built-in integer operation `int.bit_count()`, which performs the popcount in optimized native code.

The key observation is that the required mark is exactly the population count of the integer. There is no interaction between students and no need to reconstruct the questions themselves. Each `A_i` can be processed independently, and `A_i.bit_count()` directly returns the number of set bits in its binary representation.

The brute-force method works because the number of bits is bounded, but it still performs the loop in Python for every bit of every number. The observation that the answer is precisely an integer popcount lets us reduce the per-student work to one optimized operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N log A) | O(1) auxiliary | Accepted, but unnecessary Python-level looping |
| Optimal | O(N log A) in bit complexity, with native popcount per integer | O(N) for stored input/output | Accepted |

Here `A` denotes the maximum encoded paper value. With `A ≤ 10^9`, `log A` is at most about 30. The practical advantage of the optimal version is that the bit counting itself is implemented by Python's integer machinery rather than an explicit Python loop.

## Algorithm Walkthrough

1. Read the number of test cases and process each test case independently. Each student's result depends only on that student's encoded paper, so there is no state that needs to be shared between test cases.
2. Read the `N` encoded exam papers into an array. The values themselves are already the complete information needed to calculate the marks.
3. For every value `x`, compute `x.bit_count()`. This returns exactly the number of positions containing `1` in the binary representation of `x`.
4. Store the resulting counts in the same order as the students appear in the input. Preserving this order is necessary because the output corresponds position by position to the input array.
5. Print all counts for the current test case on one line.

### Why it works

For any positive integer `x`, its binary representation contains one binary digit for each question represented by the integer. A correct answer corresponds to a `1`, so the student's mark is exactly the number of `1` digits. Python's `x.bit_count()` returns precisely that quantity. Since the operation is applied independently to every `A_i`, every output value is the correct mark for the corresponding student, and preserving input order preserves the required student order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ans = [x.bit_count() for x in a]
        print(*ans)

if __name__ == "__main__":
    solve()
```

The first line of `solve` reads the number of test cases. The outer loop then isolates the processing of each exam.

For each test case, `map(int, input().split())` converts the encoded papers into Python integers. The list comprehension applies `bit_count()` independently to every value and produces the marks in exactly the same order.

There is no need for special handling of powers of two, numbers with many set bits, or the upper bound `10^9`. Python's arbitrary-precision integers also mean there is no integer overflow issue.

The code assumes the input follows the stated format, where all `N` values for a test case occur on the next line. This is sufficient for the given problem. The output is generated with `print(*ans)`, which places spaces between the answers and ends the line correctly.

## Worked Examples

For the first test case of the sample, the input values are `1, 2, 3, 4, 5`. The important state is the current integer and its binary representation.

| Student | Value | Binary | `bit_count()` | Marks |
| --- | --- | --- | --- | --- |
| 1 | 1 | `1` | 1 | 1 |
| 2 | 2 | `10` | 1 | 1 |
| 3 | 3 | `11` | 2 | 2 |
| 4 | 4 | `100` | 1 | 1 |
| 5 | 5 | `101` | 2 | 2 |

The resulting line is `1 1 2 1 2`. This demonstrates that the value itself is simply an encoding of the answers, and only its set bits matter.

For the second test case, the values are powers of two.

| Student | Value | Binary | `bit_count()` | Marks |
| --- | --- | --- | --- | --- |
| 1 | 2 | `10` | 1 | 1 |
| 2 | 4 | `100` | 1 | 1 |
| 3 | 8 | `1000` | 1 | 1 |
| 4 | 16 | `10000` | 1 | 1 |

The output is `1 1 1 1`. This is a useful boundary trace because every value has exactly one set bit despite the binary representations having different lengths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log A) bit complexity | Every value has at most `log₂(A) + 1` binary digits, and each is counted once |
| Space | O(N) | The input array and the output array contain `N` integers |

With `A ≤ 10^9`, each number has at most 30 binary digits. Thus the amount of work grows linearly with the number of students, with a very small constant factor. The implementation uses the native `bit_count()` operation, so it avoids a Python-level loop over those 30 bits. The memory usage is also comfortably below 256 MB for `N = 10^5`.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())

    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(" ".join(str(x.bit_count()) for x in a))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided sample
assert run(
    """2
5
1 2 3 4 5
4
2 4 8 16
"""
) == """1 1 2 1 2
1 1 1 1
""", "sample 1"

# Minimum-size case
assert run(
    """1
1
1
"""
) == """1
""", "minimum-size input"

# All values equal
assert run(
    """1
5
15 15 15 15 15
"""
) == """4 4 4 4 4
""", "all-equal values"

# Boundary values, including the largest allowed value
assert run(
    """1
6
1 2 3 4 5 1000000000
"""
) == """1 1 2 1 2 13
""", "boundary values"

# Maximum-size case
max_n = 100000
inp = "1\n" + str(max_n) + "\n" + ("1 " * (max_n - 1)) + "1\n"
expected = " ".join(["1"] * max_n) + "\n"

assert run(inp) == expected, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `1` | Minimum valid input and the lowest possible encoded paper |
| `5 / 15 15 15 15 15` | `4 4 4 4 4` | Repeated values and a number with many set bits |
| `1 2 3 4 5 1000000000` | `1 1 2 1 2 13` | Powers of two, adjacent values, and the maximum numeric boundary |
| `100000` copies of `1` | `100000` copies of `1` | Maximum `N` and preservation of output order |

## Edge Cases

The minimum value `1` is represented as `1₂`, so the input

```
1
1
1
```

produces

```
1
```

The algorithm calls `1.bit_count()`, which returns `1`. There is no zero value in the input constraints, so there is no need to handle an empty binary representation.

A power of two contains exactly one set bit. For example,

```
1
4
1 2 4 8
```

gives

```
1 1 1 1
```

The values have different binary lengths, but each representation contains exactly one `1`. This catches implementations that accidentally count binary digits rather than set bits.

A value with consecutive set bits exercises the other side of the representation. For

```
1
1
15
```

we have `15 = 1111₂`, so the answer is

```
4
```

The call `15.bit_count()` counts all four set positions directly.

The maximum allowed value also needs no special arithmetic. For

```
1
1
1000000000
```

the binary representation contains 13 set bits, so the output is

```
13
```

Python handles this value exactly, and `bit_count()` works without any overflow or signed-integer concerns.

Finally, a test case containing `100000` students checks the scale of the algorithm. If every paper is `1`, every answer is `1`, so the output contains `100000` ones. Each student is processed independently, and the algorithm does not accidentally merge adjacent values or lose their order.
