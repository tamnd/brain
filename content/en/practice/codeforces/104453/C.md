---
title: "CF 104453C - \u0411\u0438\u0442\u043e\u0432\u044b\u0435 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438"
description: "We are given two binary strings, each of length exactly N. They may contain leading zeros, so their “written form” is not necessarily their canonical binary representation."
date: "2026-06-30T14:32:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104453
codeforces_index: "C"
codeforces_contest_name: "ICPC Central Russia Regional Qualyfing Round, 2021"
rating: 0
weight: 104453
solve_time_s: 80
verified: true
draft: false
---

[CF 104453C - \u0411\u0438\u0442\u043e\u0432\u044b\u0435 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438](https://codeforces.com/problemset/problem/104453/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two binary strings, each of length exactly N. They may contain leading zeros, so their “written form” is not necessarily their canonical binary representation. Our task is to compute their bitwise XOR, position by position, and then output the resulting binary string after removing any leading zeros.

Conceptually, we are aligning two equal-length bit arrays and producing a third array where each position is 1 if the input bits differ and 0 if they are the same. The final step is purely formatting: we must not print unnecessary leading zeros, which means the answer should represent the same binary value in its shortest form, except that the special case where the result is zero must output a single `0`.

The input size N can be as large as 100,000. This immediately rules out any approach that repeatedly converts strings into integers and performs arithmetic using naive big integer operations in higher-level constructs, since repeated conversion or bit-by-bit string concatenation inside expensive loops risks quadratic behavior. A linear scan over the strings is the only safe target complexity.

A subtle edge case appears when the XOR result is all zeros. For example, if both inputs are identical, such as `0001` XOR `0001`, the raw result is `0000`, but the output must be `0`, not an empty string. A careless implementation that strips leading zeros without checking emptiness would incorrectly print nothing.

Another edge case comes from leading zeros in the input itself. For instance, `0001` and `0001` should still produce `0`, not `0000` or an empty line. This reinforces that normalization must happen only after computing XOR, not before.

## Approaches

A brute-force interpretation would treat both binary strings as numbers: convert them into integers, apply XOR, and convert back to binary. This is logically correct and extremely compact in code. However, the conversion step for large N involves parsing up to 100,000 characters per string, and repeated conversions or inefficient big-integer operations could degrade performance depending on implementation language and runtime constraints. In Python it is still linear, but in a strict competitive programming setting the intended solution avoids unnecessary parsing overhead and extra allocations.

A more direct and reliable approach is to process the strings character by character. Since XOR on bits is independent across positions, each output bit depends only on the corresponding input bits. We can scan from left to right, compute XOR on the fly, and then remove leading zeros from the result. The key observation is that we do not need to store intermediate numeric representations at all; the strings already encode everything we need.

This reduces the problem to a single linear pass, followed by a simple trimming step. We also avoid building large temporary integers or repeated string concatenations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (int conversion) | O(N) | O(N) | Accepted |
| Direct string XOR scan | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read the integer N and the two binary strings A and B.

The value of N is not strictly required beyond input validation because both strings already carry explicit length information.
2. Initialize an empty list to store result characters.

Using a list instead of repeated string concatenation is important because Python strings are immutable and repeated concatenation would degrade performance to O(N²).
3. Iterate over indices from 0 to N − 1.

At each index, compare A[i] and B[i]. If they differ, append `'1'` to the result list, otherwise append `'0'`.
4. Convert the list into a string.

At this point we have the full XOR result but it may contain leading zeros.
5. Strip leading zeros from the string.

This is done by finding the first occurrence of `'1'`. If no such character exists, the result is entirely zero.
6. If stripping results in an empty string, output `'0'`.

This handles the special case where all bits cancel out.
7. Otherwise print the trimmed string.

### Why it works

XOR is defined independently on each bit position: the output bit depends only on the two input bits at the same index. This means the problem has no cross-position dependencies, so a single pass is sufficient. The only global transformation is formatting: removing leading zeros, which does not change the numeric value represented by the bit sequence. The algorithm preserves per-bit correctness by construction and only adjusts representation at the end.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input().strip())
    a = input().strip()
    b = input().strip()

    res = []

    for i in range(n):
        if a[i] == b[i]:
            res.append('0')
        else:
            res.append('1')

    s = ''.join(res)

    # remove leading zeros
    i = 0
    while i < len(s) and s[i] == '0':
        i += 1

    ans = s[i:]
    if ans == "":
        ans = "0"

    print(ans)

if __name__ == "__main__":
    main()
```

The implementation keeps the logic strictly linear. The loop constructs the XOR result without any intermediate numeric conversion. The use of a list for accumulation avoids repeated string reallocation. After the main pass, a second linear scan removes leading zeros. The final conditional ensures correctness when the XOR result is zero everywhere.

A common mistake is to forget that stripping leading zeros can produce an empty string. Another subtle issue is attempting to use `int(a, 2) ^ int(b, 2)` without considering that extremely large strings still need to be parsed fully; while Python supports big integers, this introduces unnecessary overhead compared to direct bitwise processing.

## Worked Examples

### Sample 1

Input:

```
N = 2
A = 11
B = 10
```

Step-by-step XOR construction:

| i | A[i] | B[i] | XOR result |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | 1 | 0 | 1 |

Result before trimming: `01`

After removing leading zeros: `1`

This confirms that leading zero removal changes representation but not value.

### Sample 2

Input:

```
N = 4
A = 0011
B = 1100
```

| i | A[i] | B[i] | XOR result |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 0 | 1 |
| 3 | 1 | 0 | 1 |

Result before trimming: `1111`

After trimming: `1111`

No leading zeros exist, so output remains unchanged.

These traces show that the algorithm is purely position-wise and does not depend on interpretation of the strings as numbers until final formatting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each position is processed exactly once for XOR construction and once for trimming |
| Space | O(N) | We store the output string of length N in the worst case |

The solution comfortably fits within limits for N up to 100,000, since both passes are linear and involve only simple character comparisons and appends.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    a = input().strip()
    b = input().strip()

    res = []
    for i in range(n):
        res.append('0' if a[i] == b[i] else '1')

    s = ''.join(res)
    i = 0
    while i < len(s) and s[i] == '0':
        i += 1

    ans = s[i:]
    if ans == "":
        ans = "0"
    return ans

# provided samples
assert run("2\n11\n10\n") == "1", "sample 1"
assert run("4\n0011\n1100\n") == "1111", "sample 2"

# custom cases
assert run("1\n0\n0\n") == "0", "minimum size all zero"
assert run("1\n1\n0\n") == "1", "minimum size single bit"
assert run("5\n00000\n00000\n") == "0", "all equal zeros"
assert run("5\n10101\n10101\n") == "0", "all equal non-zero"
assert run("6\n000111\n111000\n") == "111111", "full complement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-bit equal zeros | 0 | minimal boundary case |
| 1-bit differing | 1 | single-position XOR correctness |
| all zeros equal | 0 | full-zero trimming |
| identical non-zero | 0 | leading zero removal after full cancellation |
| complement pattern | 111111 | full XOR propagation |

## Edge Cases

A critical edge case is when all bits cancel out. For input `A = 0000`, `B = 0000`, the computed XOR string becomes `0000`. The trimming step removes every character, producing an empty string. The algorithm explicitly checks for this and returns `0`, ensuring a valid binary representation.

Another case is when the result has leading zeros but not complete cancellation, such as `A = 0010`, `B = 0001`. The XOR result is `0011`. The trimming loop removes only the leading zeros and preserves the meaningful suffix, producing `11`. This confirms that the trimming logic only affects representation, not value.

Finally, when N = 1, the algorithm degenerates to a single comparison. The logic still works without special casing, demonstrating that the approach is uniform across all input sizes.
