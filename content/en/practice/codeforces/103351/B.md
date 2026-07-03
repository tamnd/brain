---
title: "CF 103351B - A+B"
description: "The task is the classic arithmetic building block: we are given integer pairs, and for each pair we must output their sum. Each input line represents two numbers that should be combined directly, with no additional structure such as graphs or arrays."
date: "2026-07-03T13:30:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103351
codeforces_index: "B"
codeforces_contest_name: "SDU Open 2021 Fall"
rating: 0
weight: 103351
solve_time_s: 52
verified: true
draft: false
---

[CF 103351B - A+B](https://codeforces.com/problemset/problem/103351/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is the classic arithmetic building block: we are given integer pairs, and for each pair we must output their sum. Each input line represents two numbers that should be combined directly, with no additional structure such as graphs or arrays. The output is simply the resulting integer for each pair, written in order.

Even though the problem looks trivial, the constraints still matter in practice. Problems of this type typically allow very large integers, often up to 10^18 in absolute value. That immediately rules out any approach that relies on fixed-width integer assumptions in languages where overflow is a risk. In Python this is naturally handled, but in other languages it forces careful use of 64-bit types.

The input size is also important. Since each line is independent, the total number of pairs can be large, potentially up to 10^5 or more. This means any per-test overhead beyond constant time per line, such as repeated parsing logic or unnecessary data structures, would still pass but should be avoided conceptually.

There are a few subtle edge cases that can break naive implementations. One is assuming only a single test case exists. For example, if the input is:

```
1 2
3 4
```

the correct output is:

```
3
7
```

A mistaken implementation that reads only one line would incorrectly output only `3`.

Another edge case is negative numbers, such as:

```
-5 2
```

The correct output is `-3`. A fragile string-splitting or parsing method that does not handle the minus sign correctly would fail here.

Finally, very large values like:

```
1000000000000000000 1000000000000000000
```

must be handled without overflow in fixed-size integer languages.

## Approaches

The brute-force approach is already the intended solution: read each pair of integers, compute their sum, and print it. There is no combinatorial structure or optimization problem hidden behind it. The correctness comes directly from the definition of addition.

If we describe a “less optimal” version, it would only differ in how input is processed. For example, reading the entire file into a list of tokens and repeatedly converting substrings to integers is still correct, but it introduces unnecessary overhead. Another inefficient variant might rebuild strings or perform redundant parsing per character, increasing constant factors without changing asymptotic complexity.

The key observation is that each pair is independent. No result depends on previous computations, so we never need storage beyond the current line. That reduces the problem to a single linear scan over the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Line-by-line parsing and summation | O(n) | O(1) | Accepted |
| Token buffering with repeated parsing overhead | O(n) | O(n) | Accepted but unnecessary |

Here, n is the number of input lines.

## Algorithm Walkthrough

1. Read input until end of file, treating each line as a separate pair of integers. This ensures we handle an arbitrary number of test cases without needing a predefined count.
2. For each line, split it into two integer tokens. The structure is fixed, so we always expect exactly two values per line.
3. Convert both tokens into integers. This step is necessary to ensure arithmetic addition rather than string concatenation.
4. Compute the sum of the two integers immediately after parsing. Since each line is independent, no intermediate storage is needed.
5. Output the result before moving to the next line. This keeps memory usage constant regardless of input size.

### Why it works

The correctness rests on the fact that each input line defines an independent arithmetic expression. There are no hidden dependencies between lines, so computing each sum in isolation produces the global solution. The algorithm maintains the invariant that after processing k lines, exactly k correct sums have been output, each corresponding to the k-th input pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        a, b = map(int, line.split())
        print(a + b)

if __name__ == "__main__":
    main()
```

The solution processes input in a streaming fashion using `sys.stdin`, which avoids storing the entire dataset in memory. Each line is stripped and split exactly once, ensuring constant work per test case.

One subtle implementation detail is handling empty lines. Competitive programming input can sometimes include trailing newlines, so skipping empty strings prevents accidental parsing errors. Another important detail is using `map(int, ...)` directly, which avoids intermediate list construction and keeps the code concise.

## Worked Examples

### Example 1

Input:

```
1 2
10 20
-5 7
```

| Step | a | b | a + b |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 3 |
| 2 | 10 | 20 | 30 |
| 3 | -5 | 7 | 2 |

This trace shows that each line is processed independently, and the computation is purely local. No state is carried across iterations, confirming the independence assumption.

### Example 2

Input:

```
1000000000000000000 1
-100 100
0 0
```

| Step | a | b | a + b |
| --- | --- | --- | --- |
| 1 | 10^18 | 1 | 1000000000000000001 |
| 2 | -100 | 100 | 0 |
| 3 | 0 | 0 | 0 |

This demonstrates correct handling of large integers and cancellation cases. The first line also verifies that arbitrary-precision arithmetic behaves correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the n lines is parsed and processed exactly once |
| Space | O(1) | Only two integers are stored at any time |

The algorithm is linear in the number of input lines, which is optimal because every line must be read at least once. Memory usage remains constant since no accumulation of results is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO as _StringIO

    out = _StringIO()
    backup = sys.stdout
    sys.stdout = out

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            a, b = map(int, line.split())
            print(a + b)
    finally:
        sys.stdout = backup

    return out.getvalue().strip()

# provided samples
assert run("1 2\n3 4\n") == "3\n7"

# custom cases
assert run("-1 1\n") == "0", "zero cancellation"
assert run("0 0\n5 5\n") == "0\n10", "zeros and small positives"
assert run("1000000000000000000 1000000000000000000\n") == "2000000000000000000", "large values"
assert run("   2    3   \n") == "5", "extra whitespace handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `-1 1` | `0` | sign handling and cancellation |
| `0 0 / 5 5` | `0 / 10` | multiple lines and zero values |
| large integers | big sum | overflow-safe arithmetic |
| spaced input | correct sum | robustness of parsing |

## Edge Cases

For multiple lines input, the algorithm correctly processes each pair independently. For example:

Input:

```
1 2
3 4
```

Execution processes the first line, outputs `3`, then proceeds to the next line and outputs `7`. The loop invariant is preserved because after each iteration exactly one line is consumed and one result is produced.

For negative numbers:

Input:

```
-5 2
```

The parsing step correctly converts tokens into signed integers, and the sum is computed as `-3`. There is no ambiguity in representation because `int()` correctly interprets the minus sign.

For very large values:

Input:

```
1000000000000000000 1000000000000000000
```

Python’s integer type automatically expands precision, so the sum is computed exactly without overflow. The algorithm does not introduce any intermediate narrowing conversions, so correctness is preserved.
