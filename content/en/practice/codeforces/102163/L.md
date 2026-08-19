---
title: "CF 102163L - Chemistry Exam"
description: "Each student has encoded their complete True/False answer sheet as one positive integer. The binary representation of that integer stores the answers, with a set bit representing a correct answer and an unset bit representing an incorrect answer."
date: "2026-08-19T07:54:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "L"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 102
verified: false
draft: false
---

[CF 102163L - Chemistry Exam](https://codeforces.com/problemset/problem/102163/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

Each student has encoded their complete True/False answer sheet as one positive integer. The binary representation of that integer stores the answers, with a set bit representing a correct answer and an unset bit representing an incorrect answer. The task is simply to determine how many correct answers each student's number contains.

For example, the number `13` is `1101` in binary. It contains three set bits, so that student's score is `3`.

The number of students in one test case can reach `10^5`, while every answer sheet value is at most `10^9`. Since `10^9 < 2^30`, every number uses at most 30 relevant binary positions. A straightforward scan of all 30 positions would perform at most about `3 * 10^6` bit checks for one test case, which is computationally manageable in many languages. However, the structure of the task gives us a direct bit-count operation, reducing the work for each student to a constant-time operation. We should use that operation rather than explicitly constructing the binary representation.

There is no zero-valued input because every `A_i` is at least `1`, but the algorithm should still conceptually handle zero correctly because its binary representation contains no set bits. More relevant edge cases occur at powers of two. For example, with input `8`, the binary representation is `1000`, so the answer is `1`, not `4`. A careless implementation that counts the number of digits in the binary representation would fail here.

Another useful boundary case is a number whose low and high relevant bits are both set. For example, `536870913 = 2^29 + 1`, whose binary representation has a `1` at both ends and zeros between them, so the answer is `2`. Any method that accidentally stops before checking bit 29 would produce `1`.

Repeated values also need no special treatment. If three students all have the value `7`, each has binary representation `111`, so the output is `3 3 3`. The score belongs independently to each array element, and there is no interaction between students.

## Approaches

The direct brute-force approach is to inspect every possible binary position for every student. Because `A_i <= 10^9 < 2^30`, positions `0` through `29` are enough. For each position, we test whether `(A_i >> bit) & 1` is one and increment the student's score when it is. This is correct because every correct answer corresponds exactly to one set bit.

For `N = 10^5`, this performs at most `30 * 10^5 = 3,000,000` bit checks in a test case. Thus, strictly under the stated constraints, this approach is not asymptotically disastrous and can be accepted with an efficient implementation. The real observation is that scanning all 30 positions is unnecessary.

The key operation we need is the population count, also called the popcount: the number of set bits in an integer. Python provides this directly through `int.bit_count()`. The binary encoding already contains exactly the information we need, so there is no reason to convert the number to a string or manually inspect every bit.

The brute-force method works because it examines the same bits that define the score, but it fails to exploit the fact that the required quantity is a standard property of an integer. The observation that the answer is precisely the integer's population count lets us reduce the work for each student to one operation, giving linear time in the number of students.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Scan all 30 bit positions | O(30N) = O(N) | O(1) besides output | Accepted, but unnecessary work |
| Built-in population count | O(N) | O(1) besides output | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases and process each test case independently. Each test case has its own collection of students, so no state needs to be shared between test cases.
2. Read the `N` answer-sheet integers. For each integer `x`, compute `x.bit_count()`. This returns exactly the number of `1` bits in the binary representation of `x`, which is exactly the student's number of correct answers.
3. Store the resulting scores in an output array and print them separated by spaces. Keeping the results in order preserves the correspondence between each input student and their score.

### Why it works

For every student, each binary position represents one True/False answer, and a correct answer corresponds to a set bit. Consequently, the student's score is exactly the number of set bits in their integer. `bit_count()` returns precisely that quantity, so every produced score is correct independently of all other students. Processing every input integer once gives the required result for the entire test case.

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

The first line determines how many independent test cases must be processed. For each case, the program reads the number of students and then the corresponding integer array.

The list comprehension is the central part of the algorithm. For each `x`, `x.bit_count()` counts its set bits without requiring us to construct a binary string or manually shift through every position.

There is no off-by-one boundary to manage because `bit_count()` operates on the entire integer representation. In particular, a set bit at position 29 is counted just like a set bit at position 0. Python integers also do not overflow, although the input bound already guarantees that the values are small enough for ordinary 32-bit reasoning.

The output is generated with `print(*ans)`, which produces the required space-separated scores. Since the input contains at most 30 significant bits per value, there is no need for any special handling based on the magnitude of an individual integer.

## Worked Examples

For the first sample, the first test case contains the values `1 2 3 4 5`.

| Student | Value | Binary | `bit_count()` | Score |
| --- | --- | --- | --- | --- |
| 1 | 1 | `1` | 1 | 1 |
| 2 | 2 | `10` | 1 | 1 |
| 3 | 3 | `11` | 2 | 2 |
| 4 | 4 | `100` | 1 | 1 |
| 5 | 5 | `101` | 2 | 2 |

The resulting array is `1 1 2 1 2`. The trace directly demonstrates the invariant that the score of each student is the number of set bits in their answer-sheet integer.

For the second test case, the values are powers of two.

| Student | Value | Binary | `bit_count()` | Score |
| --- | --- | --- | --- | --- |
| 1 | 2 | `10` | 1 | 1 |
| 2 | 4 | `100` | 1 | 1 |
| 3 | 8 | `1000` | 1 | 1 |
| 4 | 16 | `10000` | 1 | 1 |

Every power of two contains exactly one set bit, so the output is `1 1 1 1`. This is also a useful boundary-style example because it confirms that the number of binary digits has nothing to do with the score.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each student's integer is processed once with a population-count operation |
| Space | O(N) | The input array and resulting score array are stored for the test case |

The stated limit of `10^5` students is easily compatible with a linear pass. Since every `A_i` is at most `10^9`, each integer has at most 30 significant bits, and Python's integer population count is implemented efficiently. The memory usage is also comfortably below 256 MB for the given input size.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(" ".join(str(x.bit_count()) for x in a))

    return "\n".join(out)

# Provided sample 1
assert solution(
    """2
5
1 2 3 4 5
4
2 4 8 16
"""
) == """1 1 2 1 2
1 1 1 1""", "sample 1"

# Minimum-size case
assert solution(
    """1
1
1
"""
) == """1""", "minimum input"

# All values equal
assert solution(
    """1
5
7 7 7 7 7
"""
) == """3 3 3 3 3""", "all equal values"

# Boundary around powers of two
assert solution(
    """1
6
1 2 3 4 7 8
"""
) == """1 1 2 1 3 1""", "power-of-two boundaries"

# Maximum allowed value and a number with two extreme set bits
assert solution(
    """1
4
1000000000 536870913 1073741823 999999999
"""
) == """13 2 30 18""", "large values"

# Maximum-size input
large_input = "1\n100000\n" + " ".join(["1"] * 100000) + "\n"
large_output = solution(large_input)
assert large_output == " ".join(["1"] * 100000), "maximum N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Minimum number of students and smallest possible value |
| `7 7 7 7 7` | `3 3 3 3 3` | Repeated values are processed independently |
| `1 2 3 4 7 8` | `1 1 2 1 3 1` | Powers of two and adjacent bit patterns |
| `1000000000 536870913 1073741823 999999999` | `13 2 30 18` | Large values and high set-bit positions |
| 100000 copies of `1` | 100000 copies of `1` | Maximum input size and linear processing |

## Edge Cases

A single student with the smallest allowed value gives the input

```
1
1
1
```

The integer `1` is binary `1`, so `bit_count()` returns `1`. The output is `1`. There is no special case required for `N = 1`, because the same per-student operation applies.

A power of two is a common source of mistakes. For

```
1
1
8
```

the binary representation is `1000`. There is only one set bit, so the correct output is `1`. An implementation that uses the binary length instead of counting set bits would incorrectly return `4`.

A high set bit must also be included. Consider

```
1
1
536870913
```

Since `536870913 = 2^29 + 1`, its binary representation has a set bit at position 29 and another at position 0. Its score is `2`. A manual loop that accidentally checks only positions `0` through `28` would miss the high bit and return `1`.

Finally, a value can have every one of its first 30 bits set. The input

```
1
1
1073741823
```

uses `2^30 - 1`, whose binary representation is thirty `1` bits. The correct output is `30`. The population count handles this naturally and has no boundary condition at the highest allowed bit.
