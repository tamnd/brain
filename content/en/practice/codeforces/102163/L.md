---
title: "CF 102163L - Chemistry Exam"
description: "Each student's exam paper is encoded as one positive integer. The binary representation of that integer describes the student's True and False answers: a set bit represents a correct True answer, while an unset bit represents a False answer."
date: "2026-08-23T08:37:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "L"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 1546
verified: true
draft: false
---

[CF 102163L - Chemistry Exam](https://codeforces.com/problemset/problem/102163/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 25m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

Each student's exam paper is encoded as one positive integer. The binary representation of that integer describes the student's True and False answers: a set bit represents a correct True answer, while an unset bit represents a False answer. Since every answer on the exam was correct, the student's score is exactly the number of set bits in the binary representation of their number.

For example, the number `13` is `1101` in binary. It contains three set bits, so the corresponding student scored `3`.

For every test case, we receive an array of `N` such encoded exam papers and must output the popcount, or number of set bits, of every element in the same order.

The value of `N` can reach `10^5`, so an approach that compares every pair of students, or performs work proportional to `N^2`, is immediately unsuitable. The values themselves are at most `10^9`, which means each number has at most 30 binary digits. That small fixed bit width is the key reason a linear scan is enough. With a 1 second limit, we should aim for roughly `O(N)` work per test case, with only a small constant amount of processing per number.

There are a few cases where an implementation can go wrong if it assumes the binary representation has a particular shape. Consider the smallest possible input:

```
1
1
1
```

The correct output is:

```
1
```

The number `1` has exactly one set bit. An implementation that accidentally starts checking bits from position 1 instead of position 0 would incorrectly produce zero.

Another boundary case is a power of two:

```
1
3
2 4 8
```

The correct output is:

```
1 1 1
```

Every power of two has exactly one set bit. A careless implementation that counts the number of binary digits instead of the number of set bits would return `2 3 4`, which is the wrong quantity.

A value can also contain adjacent set bits and zeros between them:

```
1
3
3 5 10
```

The binary forms are `11`, `101`, and `1010`, so the correct output is:

```
2 2 2
```

Checking only the highest or lowest set bit would miss some correct answers. The entire bit pattern has to be counted.

## Approaches

The direct approach is to convert every integer to binary and inspect all of its bits, incrementing the answer whenever a bit is `1`. This is completely correct because every `1` in the binary representation corresponds to one correct question.

Since every `A_i` is at most `10^9`, it has at most 30 bits. Thus this approach takes `O(30N)`, which simplifies to `O(N)` because 30 is a constant. In Python, the cleanest implementation is to use the built-in integer operation `bit_count()`, which performs exactly this popcount operation without requiring us to manually manipulate the bits.

A manual bit-counting loop can also be derived from first principles. The expression `x & 1` tells us whether the lowest bit is set, and `x >> 1` removes that bit. Repeating this until `x` becomes zero counts every set bit. There is an even better bit-manipulation observation: `x & (x - 1)` removes the lowest set bit from `x`. Consequently, repeatedly applying that operation performs exactly one iteration per set bit rather than one iteration per binary digit.

The brute-force interpretation is useful for understanding why the answer is a popcount, but there is no need for an `O(N^2)` algorithm at all. The structure of each student record is independent of every other record. We can process each integer separately, and the bounded 30-bit representation means even a manual scan is fast enough. Python's `int.bit_count()` gives the same result directly and is the simplest optimal implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Manual bit scan | O(30N) = O(N) | O(1) auxiliary | Accepted |
| Built-in popcount | O(N) | O(1) auxiliary | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Each test case is independent, so the same procedure can be applied separately.
2. Read `N` and the `N` encoded exam papers. We only need the value of each integer, because the score depends entirely on its own binary representation.
3. For every integer `x`, compute `x.bit_count()`. This returns the number of set bits in the binary representation of `x`, which is exactly the number of correct answers encoded by that integer.
4. Store the resulting counts in the same order as the input and print them as one space-separated line. Preserving order matters because each output score corresponds to the student at the same position in the input array.

Why it works: for every student, each binary position represents one question and a set bit represents a correct answer. The `bit_count()` operation counts exactly those set bits, so the produced value is exactly that student's score. Since students are processed independently and in input order, every output position receives the correct score.

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

The program first reads `T`, then processes each test case independently. The array is read as integers, and the list comprehension applies `bit_count()` to every student record.

The use of `bit_count()` is deliberate. The problem asks for the number of `1` bits, not the binary length or the position of the highest set bit. Python integers do not have the fixed-width overflow behavior of languages such as C++, so values up to `10^9` are handled directly without any special type.

There is also no off-by-one issue because `bit_count()` treats bit position zero correctly. For example, `1` is represented by the single set bit at position zero, so its count is `1`.

The output is produced with `print(*ans)`, which inserts spaces between all scores and avoids constructing a large formatted string manually. The input uses `sys.stdin.readline`, satisfying the required fast-I/O pattern.

## Worked Examples

For the first test case of the sample, the input array is `1 2 3 4 5`. The algorithm processes each number independently.

| Student value | Binary representation | Set-bit count | Output |
| --- | --- | --- | --- |
| 1 | `1` | 1 | 1 |
| 2 | `10` | 1 | 1 |
| 3 | `11` | 2 | 2 |
| 4 | `100` | 1 | 1 |
| 5 | `101` | 2 | 2 |

The resulting line is `1 1 2 1 2`. This trace demonstrates the central invariant: the score is exactly the number of `1` bits, regardless of where those bits occur.

For the second test case, the input is `2 4 8 16`.

| Student value | Binary representation | Set-bit count | Output |
| --- | --- | --- | --- |
| 2 | `10` | 1 | 1 |
| 4 | `100` | 1 | 1 |
| 8 | `1000` | 1 | 1 |
| 16 | `10000` | 1 | 1 |

The output is `1 1 1 1`. This is a useful boundary pattern because every value is a power of two. Exactly one binary position is set in each case, even though the number of binary digits keeps increasing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each of the `N` values is processed once, and every value has at most 30 bits. |
| Space | O(N) | The input array and output list contain `N` integers. |

Across all test cases, the work is linear in the total number of students. With at most 30 relevant bits per integer and `N <= 10^5` per test case, this comfortably fits the 1 second time limit. The memory usage is also far below 256 MB for the given input size.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        print(*(x.bit_count() for x in a))

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

# Provided sample
sample = """\
2
5
1 2 3 4 5
4
2 4 8 16
"""
assert run(sample) == "1 1 2 1 2\n1 1 1 1\n", "sample"

# Minimum-size input
assert run("""\
1
1
1
""") == "1\n", "minimum size"

# All values equal
assert run("""\
1
5
7 7 7 7 7
""") == "3 3 3 3 3\n", "all equal values"

# Boundary powers of two
assert run("""\
1
6
1 2 4 8 16 536870912
""") == "1 1 1 1 1 1\n", "powers of two"

# Mixed bit patterns, including the largest allowed value
assert run("""\
1
5
3 5 10 15 1000000000
""") == "2 2 2 4 13\n", "mixed patterns and upper boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `1` | Minimum input and bit position zero |
| `5 / 7 7 7 7 7` | `3 3 3 3 3` | Repeated identical values |
| `1 2 4 8 16 536870912` | Six ones | Powers of two and increasing bit positions |
| `3 5 10 15 1000000000` | `2 2 2 4 13` | Mixed binary patterns and the `10^9` upper boundary |

## Edge Cases

The smallest possible value is `1`, represented as binary `1`. For the input

```
1
1
1
```

`bit_count()` returns `1`, so the output is

```
1
```

There is no missing leading bit to account for. Leading zeroes are irrelevant because they cannot represent correct answers.

A power of two is another common source of mistakes. For

```
1
3
2 4 8
```

the binary forms are `10`, `100`, and `1000`. Each contains one set bit, so the algorithm returns

```
1 1 1
```

The number of binary digits changes, but the score does not. This distinguishes counting set bits from counting the binary length.

Values with several separated set bits are handled without special cases. For

```
1
3
3 5 10
```

the binary representations are `11`, `101`, and `1010`. Each contains two set bits, giving

```
2 2 2
```

The algorithm does not depend on adjacency or position of the set bits, so zeros between correct answers have no effect.

Finally, the largest allowed value is `10^9`. Its binary representation contains 13 set bits, so

```
1
1
1000000000
```

produces

```
13
```

The value is comfortably within Python's integer range, and `bit_count()` handles it directly. No special treatment is needed at the numeric boundary.
