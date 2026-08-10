---
title: "CF 102409B - Xor Sums"
description: "For each test case, we are given an integer (N), and we need to compute the bitwise XOR of every integer from (1) through (N): [ 1 oplus 2 oplus 3 oplus cdots oplus N. ] The order does not matter because XOR is associative and commutative."
date: "2026-08-11T06:34:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102409
codeforces_index: "B"
codeforces_contest_name: "Semana i 2019"
rating: 0
weight: 102409
solve_time_s: 636
verified: true
draft: false
---

[CF 102409B - Xor Sums](https://codeforces.com/problemset/problem/102409/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we are given an integer (N), and we need to compute the bitwise XOR of every integer from (1) through (N):

[
1 \oplus 2 \oplus 3 \oplus \cdots \oplus N.
]

The order does not matter because XOR is associative and commutative. The task is simply to determine the value of this prefix XOR for as many as (10^5) different values of (N).

The upper bound (N \le 10^{18}) immediately rules out anything that visits every integer up to (N). Even for a single maximum-size test case, a direct loop would perform (10^{18}) XOR operations. With (10^5) test cases, the theoretical worst case reaches (10^{23}) operations, far beyond what a one-second limit can support. We need a constant-time calculation for each test case.

The large value of (N) also means that fixed-width integer overflow would be a concern in languages such as C++, Java, or JavaScript if an unsuitable type were chosen. Python integers grow automatically, so the arithmetic itself is safe. The answer is at most slightly larger than (N), so it remains comfortably within the range represented by Python's integer type.

The smallest values expose several common mistakes. For (N=1), the answer is (1), because there is only one number:

```
Input:
1
```

```
Output:
1
```

A formula that accidentally starts from (0) or uses the wrong residue class can fail here.

For (N=2), the answer is (1 \oplus 2=3):

```
Input:
2
```

```
Output:
3
```

This catches formulas that treat the (N \equiv 2 \pmod 4) case as zero.

For (N=3), we get (1\oplus2\oplus3=0):

```
Input:
3
```

```
Output:
0
```

This is a useful boundary case because the prefix XOR first becomes zero here.

The transition at a multiple of four is also easy to mishandle. For (N=4),

[
1\oplus2\oplus3\oplus4=4,
]

so the answer is (4), not (0). The reason behind this pattern is the key observation used by the optimal solution.

## Approaches

The direct approach is straightforward. Start with an accumulator equal to zero and XOR every integer from (1) through (N) into it. After processing (N), the accumulator is exactly the required value because it contains every number in the requested range once.

This approach is correct, but its running time is (O(N)) for one test case. When (N=10^{18}), that means exactly (10^{18}) loop iterations for one input. With (10^5) test cases all having (N=10^{18}), the total would be (10^{23}) iterations. The one-second time limit makes such an approach impossible.

The structure that saves us is the behavior of XOR over consecutive integers. Consider the XOR of the integers from (1) to (N). The first few values are

[
1,\ 3,\ 0,\ 4,\ 1,\ 7,\ 0,\ 8,\ldots
]

A pattern appears immediately when we group (N) by its remainder modulo (4):

[
\operatorname{xor}(1\ldots N)=
\begin{cases}
N & N\bmod4=0,\
1 & N\bmod4=1,\
N+1 & N\bmod4=2,\
0 & N\bmod4=3.
\end{cases}
]

The reason this repeats every four positions comes from the identity

[
x\oplus(x+1)\oplus(x+2)\oplus(x+3)=0
]

whenever (x) is divisible by (4). For example,

[
4\oplus5\oplus6\oplus7=0.
]

Thus, complete blocks of four consecutive integers cancel in XOR. Once those complete blocks are removed, only zero, one, two, or three numbers remain, and their contribution depends only on (N\bmod4).

The brute-force method works because it explicitly builds the prefix XOR one number at a time, but fails because (N) can be astronomically large. The observation that every complete block of four numbers has XOR zero lets us discard almost the entire range and calculate the remaining contribution from (N\bmod4).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N)) per test case | (O(1)) | Too slow |
| Optimal | (O(1)) per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (N) for the current test case and calculate (N\bmod4). Only this remainder is needed to determine which part of the repeating XOR pattern we are in.
2. If (N\bmod4=0), return (N). The prefix can be divided into complete groups of four, and each complete group cancels to zero except for the final pattern contribution, which leaves (N).
3. If (N\bmod4=1), return (1). After all complete groups of four cancel, the only remaining contribution has XOR equal to (1).
4. If (N\bmod4=2), return (N+1). The remaining prefix ends with two numbers whose XOR produces this value.
5. If (N\bmod4=3), return (0). The remaining three-number prefix cancels completely.
6. Output the selected value immediately and continue with the next test case. Every test case is independent, so there is no state to preserve between them.

The underlying invariant is that after removing every complete block of four consecutive integers, the XOR contribution of those removed blocks is zero. The only information left is the number of elements in the incomplete final block, which is exactly (N\bmod4). The four cases above give the XOR of that remaining prefix, so the algorithm always produces the same value as explicitly XORing every integer from (1) through (N).

## Python Solution

```python
import sys
input = sys.stdin.readline

def xor_upto(n):
    r = n % 4

    if r == 0:
        return n
    if r == 1:
        return 1
    if r == 2:
        return n + 1
    return 0

def solve():
    t = int(input())

    answers = []
    for _ in range(t):
        n = int(input())
        answers.append(str(xor_upto(n)))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The `xor_upto` function implements the four cases from the algorithm directly. Computing `n % 4` is enough to select the answer, so there is no loop depending on the magnitude of (N).

The `r == 0` case returns (N) itself. This boundary is easy to confuse with the `r == 3` case, where the answer is zero. For example, (N=3) gives zero, while increasing (N) to (4) gives four.

The `r == 2` case returns `n + 1`, so it is important not to accidentally return (N). For (N=2), the required XOR is (1\oplus2=3=N+1).

Python's arbitrary-precision integers make `n + 1` safe even at (N=10^{18}). There is no multiplication or other unnecessary arithmetic, so the implementation stays both simple and fast.

The solution collects the answers and writes them once with `sys.stdout.write`. With (10^5) test cases, this avoids unnecessary repeated output operations while keeping the implementation compatible with the required fast input style.

## Worked Examples

For the first sample, the test case (N=1) has remainder (1) modulo (4).

| (N) | (N\bmod4) | Selected case | Answer |
| --- | --- | --- | --- |
| 1 | 1 | (N\bmod4=1) | 1 |

The actual XOR is simply (1), so the formula matches the direct calculation.

For (N=2), the calculation moves into the second residue class.

| (N) | (N\bmod4) | Selected case | Answer |
| --- | --- | --- | --- |
| 2 | 2 | (N\bmod4=2) | 3 |

Here the direct calculation is (1\oplus2=3), which is exactly (N+1).

For the third sample, (N=5).

| (N) | (N\bmod4) | Selected case | Answer |
| --- | --- | --- | --- |
| 5 | 1 | (N\bmod4=1) | 1 |

We can also see this directly:

[
1\oplus2\oplus3\oplus4\oplus5.
]

The first four numbers contribute zero as a complete block, leaving only (5) together with the pattern contribution of the prefix. Equivalently, the established formula for residue (1) gives (1). Directly evaluating,

[
1\oplus2=3,\qquad
3\oplus3=0,\qquad
0\oplus4=4,\qquad
4\oplus5=1.
]

So the output is (1).

A second useful trace is (N=8), where two complete groups of four are present.

| (N) | (N\bmod4) | Selected case | Answer |
| --- | --- | --- | --- |
| 8 | 0 | (N\bmod4=0) | 8 |

The sequence can be grouped as ((1,2,3,4)) and ((5,6,7,8)). Each four-number group follows the same XOR structure, and the complete prefix through a multiple of four has XOR equal to that endpoint. The formula consequently returns (8).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T)) | Each test case requires one modulo operation and a constant number of comparisons |
| Space | (O(T)) | The implementation stores the output strings before writing them |

The calculation itself uses (O(1)) extra space per test case. The (O(T)) space shown above comes only from storing all formatted answers. With (T\le10^5), this is comfortably below the 256 MB memory limit. The total running time is linear in the number of test cases rather than in the values of (N), so even (10^5) inputs with (N=10^{18}) are easily manageable.

## Test Cases

```python
import sys
import io

def xor_upto(n):
    r = n % 4

    if r == 0:
        return n
    if r == 1:
        return 1
    if r == 2:
        return n + 1
    return 0

def solve():
    t = int(input())
    answers = []

    for _ in range(t):
        n = int(input())
        answers.append(str(xor_upto(n)))

    sys.stdout.write("\n".join(answers))

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
            return sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided sample
assert run("3\n1\n2\n5\n") == "1\n3\n1", "sample 1"

# Minimum value
assert run("1\n1\n") == "1", "minimum input"

# Every residue class modulo 4
assert run("4\n2\n3\n4\n5\n") == "3\n0\n4\n1", "modulo-4 boundaries"

# Repeated equal values
assert run("5\n8\n8\n8\n8\n8\n") == "8\n8\n8\n8\n8\n", "repeated values"

# Maximum allowed value
assert run("1\n1000000000000000000\n") == "1000000000000000000", "maximum N"

# Larger boundary crossing
assert run("4\n7\n8\n9\n10\n") == "0\n8\n1\n11", "off-by-one boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n` | `1` | Minimum-size input and the (N\bmod4=1) case |
| `4\n2\n3\n4\n5\n` | `3\n0\n4\n1` | All four residue classes and adjacent boundaries |
| `5\n8\n8\n8\n8\n8\n` | `8\n8\n8\n8\n8` | Multiple test cases with identical values |
| `1\n1000000000000000000\n` | `1000000000000000000` | Maximum (N) and large-integer handling |
| `4\n7\n8\n9\n10\n` | `0\n8\n1\n11` | Transitions across multiples of four and off-by-one errors |

## Edge Cases

The minimum input is (N=1). The algorithm computes (1\bmod4=1), selects the second formula, and returns (1). The exact input and output are:

```
Input:
1
1
```

```
Output:
1
```

This catches implementations that accidentally include zero in the XOR range or use an incorrect starting pattern.

The first zero result occurs at (N=3). Here (3\bmod4=3), so the algorithm returns zero immediately. Direct calculation confirms it:

[
1\oplus2\oplus3=3\oplus3=0.
]

Thus:

```
Input:
1
3
```

```
Output:
0
```

A careless implementation that assumes the answer must be positive, or that only checks whether (N) is even or odd, will fail this case.

The boundary at (N=4) is another common source of errors. Since (4\bmod4=0), the algorithm returns (4). Direct evaluation gives

[
1\oplus2\oplus3\oplus4=0\oplus4=4.
]

So:

```
Input:
1
4
```

```
Output:
4
```

The distinction between (N=3) and (N=4) demonstrates why grouping only by parity is insufficient. Consecutive values can have completely different answers even though their parity alternates predictably.

The (N=2) case checks the (N\bmod4=2) branch. The algorithm returns (N+1=3), matching

[
1\oplus2=3.
]

The exact input is:

```
Input:
1
2
```

```
Output:
3
```

This catches the frequent mistake of returning (N) for every even value.

Finally, the maximum value (N=10^{18}) is divisible by four, because (10^{18}\bmod4=0). The algorithm therefore returns (10^{18}) without iterating through any of the numbers in the range:

```
Input:
1
1000000000000000000
```

```
Output:
1000000000000000000
```

The execution still performs only one modulo operation and one branch. This is exactly the behavior required by the constraints, because the algorithm's work depends on the number of test cases, not on the magnitude of the numbers themselves.
