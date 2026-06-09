---
title: "CF 1811A - Insert Digit"
description: "We are given a decimal number written as a string and a single extra digit. We are allowed to insert this digit at any position in the number, including before the first digit or after the last digit."
date: "2026-06-09T08:37:49+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "strings"]
categories: ["algorithms"]
codeforces_contest: 1811
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 863 (Div. 3)"
rating: 800
weight: 1811
solve_time_s: 91
verified: true
draft: false
---

[CF 1811A - Insert Digit](https://codeforces.com/problemset/problem/1811/A)

**Rating:** 800  
**Tags:** greedy, math, strings  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a decimal number written as a string and a single extra digit. We are allowed to insert this digit at any position in the number, including before the first digit or after the last digit. The goal is to choose the insertion position so that the resulting number, interpreted normally in base 10 without leading zeros being special-cased, is as large as possible.

The key mental model is that we are inserting one character into a string and want the lexicographically largest possible resulting string, since comparing two equal-length decimal strings digit by digit matches numeric comparison for non-negative integers.

The input size is large across test cases, with the total length of all numbers summing up to at most 200,000. That immediately suggests that any solution that tries every insertion position independently and rebuilds full strings repeatedly will still be fine in aggregate only if it is linear per test case. Anything quadratic per test case would collapse under worst-case inputs.

A naive approach might try inserting the digit at each of the n+1 positions, constructing the resulting string each time, and comparing all results. This would already cost O(n^2) per test case in the worst case due to repeated string construction and comparison. With total n up to 2e5 across tests, this is too slow.

There are a few edge cases that break careless greedy intuition. One is when the extra digit is small, such as inserting 1 into a descending number like 98765. Always appending would be wrong because inserting early yields a larger number. Another is when digits are equal to the inserted digit, for example inserting 5 into 5555, where placement does not matter but off-by-one insertion rules can easily shift correctness if the condition is strict in the wrong direction. A final edge case is inserting 0, where placement still matters because leading zeros are not allowed in the original but are allowed as part of intermediate construction; correctness depends purely on maximizing lexicographic order.

## Approaches

The brute-force method tries every possible insertion point. For each position i from 0 to n, we construct a new string by inserting the digit and compare it with the best seen so far. This is correct because it explicitly evaluates all valid configurations. The failure point is performance. Each insertion costs O(n) to build and O(n) to compare, giving O(n^2) per test case. Over 2e5 total characters, this becomes far too slow.

The structure of the problem allows a simpler observation. We are inserting one digit into a fixed string, and we want the resulting string to be as large as possible in lexicographic order. This means we want the inserted digit to be as far left as possible while still maintaining maximal ordering. If we move left to right through the number, we should keep existing digits as long as they are greater than or equal to the inserted digit, because placing the digit after them preserves a larger prefix. The first position where the current digit is strictly smaller than the inserted digit is where we should insert it.

If we never find such a position, it means all digits are greater than or equal to the inserted digit, so the best position is at the end.

This reduces the problem to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the string number and the digit d, converted to a character. Working with characters avoids repeated integer conversions and aligns directly with lexicographic comparison.
2. Initialize an empty result list and a flag indicating whether we have inserted the digit.
3. Scan the original number from left to right. At each position, compare the current digit with d.
4. While the current digit is greater than or equal to d, we append it to the result. We do this because placing d earlier would make the prefix smaller in lexicographic order.
5. As soon as we find a digit that is strictly smaller than d, we insert d at this position, append it to the result, and then append the rest of the original number.
6. If we reach the end without inserting d, we append it at the end.

The crucial decision point is the strict inequality. If the current digit equals d, we still postpone insertion, because placing d later preserves the prefix and does not reduce the resulting number.

Why it works: at any point in the scan, all digits already appended to the result are guaranteed to be optimal for their positions. The first position where placing d improves the prefix is exactly where the existing digit is smaller than d. Any later insertion would reduce the prefix earlier than necessary, and any earlier insertion would replace a larger or equal digit, which cannot increase the final lexicographic value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, d = input().split()
        s = input().strip()

        inserted = False
        res = []

        for ch in s:
            if not inserted and ch < d:
                res.append(d)
                inserted = True
            res.append(ch)

        if not inserted:
            res.append(d)

        out.append("".join(res))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the greedy scan described earlier. The result is built using a list for efficiency since repeated string concatenation would otherwise degrade performance to quadratic behavior. The insertion check happens once per character, ensuring linear complexity.

A subtle point is that insertion happens before appending the current character when we detect ch < d. This preserves correctness because the digit must appear strictly before the first smaller digit. If we instead appended first and then inserted, we would incorrectly shift the position by one.

## Worked Examples

### Example 1

Input:

```
5 4
76543
```

We scan digit by digit and track whether insertion has happened.

| Step | Current digit | d | Action | Result so far |
| --- | --- | --- | --- | --- |
| 1 | 7 | 4 | 7 ≥ 4, keep | 7 |
| 2 | 6 | 4 | 6 ≥ 4, keep | 76 |
| 3 | 5 | 4 | 5 ≥ 4, keep | 765 |
| 4 | 4 | 4 | 4 ≥ 4, keep | 7654 |
| 5 | 3 | 4 | 3 < 4, insert then append | 76543 + 4 inserted before 3 |

Final result: 765443

This shows the digit is inserted right before the first strictly smaller digit.

### Example 2

Input:

```
5 8
97531
```

| Step | Current digit | d | Action | Result so far |
| --- | --- | --- | --- | --- |
| 1 | 9 | 8 | 9 ≥ 8 | 9 |
| 2 | 7 | 8 | 7 < 8 insert | 98 |
| remaining | 5 3 1 | 8 | append rest | 98531 |

Final result: 98531

Here, the inserted digit moves forward as early as possible to maximize lexicographic value.

These two traces demonstrate the invariant that we always maintain the best possible prefix, and only decide insertion at the first point where the new digit improves ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | single linear scan with constant work per character |
| Space | O(n) | output buffer stores constructed string |

The total input size across test cases is bounded by 2e5, so the overall runtime is linear in the size of input and easily fits within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, d = input().split()
        s = input().strip()

        inserted = False
        res = []

        for ch in s:
            if not inserted and ch < d:
                res.append(d)
                inserted = True
            res.append(ch)

        if not inserted:
            res.append(d)

        out.append("".join(res))

    return "\n".join(out)

# provided samples
assert run("11\n5 4\n76543\n1 0\n1\n2 5\n44\n3 6\n666\n5 6\n13579\n5 8\n97531\n19 4\n9876543210123456789\n5 7\n73737\n8 1\n20000000\n7 0\n7058959\n12 1\n828127127732\n") == \
"765443\n10\n544\n6666\n613579\n987531\n98765443210123456789\n773737\n210000000\n70589590\n8281271277321"

# custom cases
assert run("1\n3 5\n123\n") == "5123", "insert at front"
assert run("1\n3 5\n999\n") == "9995", "append at end"
assert run("1\n5 4\n44444\n") == "444444", "all equal digits"
assert run("1\n5 9\n12345\n") == "912345", "always insert at beginning"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 5 / 123 | 5123 | insertion at beginning |
| 3 5 / 999 | 9995 | insertion at end |
| 5 4 / 44444 | 444444 | equality handling |
| 5 9 / 12345 | 912345 | strict dominance of large digit |

## Edge Cases

A key edge case is when all digits are equal to the inserted digit. For input `44444` with `d = 4`, the scan never finds a digit strictly smaller than 4, so insertion happens at the end. The algorithm appends all digits first, then appends 4, producing `444444`, which is correct because any earlier insertion would produce the same multiset of digits but identical ordering, and the rule still places the digit at the last valid position consistently.

Another edge case is when the inserted digit is 0. For example, inserting into `7058959`, the algorithm places 0 at the first digit smaller than 0, which never happens, so it is appended at the end. This is correct because leading position insertion would only reduce lexicographic value since 0 is the smallest digit.

A final edge case is when the inserted digit is the largest possible, 9. In `12345`, the first digit 1 is smaller than 9, so we insert immediately at the front, producing `912345`. This confirms the greedy rule correctly prioritizes maximizing the most significant digit position.
