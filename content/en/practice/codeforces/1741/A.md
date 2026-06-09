---
title: "CF 1741A - Compare T-Shirt Sizes"
description: "We are asked to compare two T-shirt sizes represented as strings. Each string ends with one of three letters: S for small, M for medium, or L for large. In addition, there may be a sequence of Xs before an S or L, indicating extra-small or extra-large."
date: "2026-06-09T16:25:33+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1741
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 826 (Div. 3)"
rating: 800
weight: 1741
solve_time_s: 159
verified: true
draft: false
---

[CF 1741A - Compare T-Shirt Sizes](https://codeforces.com/problemset/problem/1741/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 2m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compare two T-shirt sizes represented as strings. Each string ends with one of three letters: S for small, M for medium, or L for large. In addition, there may be a sequence of Xs before an S or L, indicating extra-small or extra-large. Medium never has an X, so M is fixed. The input gives multiple pairs of sizes, and for each pair we must print whether the first is smaller, larger, or equal to the second.

The key is understanding the ordering. Any small is smaller than medium or large, and any large is larger than medium or small. Among smalls, more Xs make the shirt smaller, e.g., XXXS < XS. Among larges, more Xs make it larger, e.g., XXXL > XL. Medium is always between all smalls and all larges.

Constraints tell us that there can be up to 10,000 test cases, and each size string is at most 50 characters. A naive approach that involves any nested loops over string characters could still work because 50 × 10,000 = 500,000 operations, which is acceptable for a 1-second limit. However, careful string parsing is needed to handle the varying number of Xs and the final letter.

Edge cases arise when comparing extreme sizes or unusual combinations. For example, XXXXXS versus M should return `<`, because any small, regardless of length, is smaller than medium. Similarly, L versus XXXL should return `<`, because XXXL is a large and L is a single large, so XXXL > L. A naive lexicographical string comparison would fail here, because "XXXXXS" > "M" as strings, even though the size is smaller.

## Approaches

The brute-force approach is to encode each T-shirt size as an integer representing its absolute rank and then compare these integers. For smalls, we could assign a negative number decreasing with the number of Xs; for medium, zero; for larges, a positive number increasing with the number of Xs. This works because all sizes fall into a linear order, and encoding them allows a simple numeric comparison. This approach is correct but introduces unnecessary bookkeeping if we only need to compare two strings at a time.

The optimal approach leverages the fact that the ordering rules are simple and localized: the last character determines the category (S, M, L), and the number of preceding Xs determines the relative ordering within S and L. We can first check the last character. If they differ, comparison is immediate: S < M < L. If the last characters are equal, we compare the counts of Xs: for S, more Xs means smaller; for L, more Xs means larger. This requires at most counting characters per string, which is linear in string length, or O(1) since length ≤ 50. No additional data structures are needed, and we can handle all test cases efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (rank encoding) | O(t * n) | O(1) | Accepted but slightly more complicated |
| Optimal (character-based comparison) | O(t * n) | O(1) | Accepted and simpler |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the two T-shirt size strings `a` and `b`.
3. Extract the last character of each string to determine its type: small, medium, or large.
4. If the types differ, compare directly using the order S < M < L. Print `<` if `a` is smaller, `>` if larger, or continue if equal.
5. If the types are the same, count the number of Xs in each string. For smalls, more Xs means the size is smaller; for larges, more Xs means the size is larger. Medium has no Xs and is always equal to another medium.
6. Compare the counts according to the type and print `<`, `>`, or `=` as appropriate.

Why it works: The algorithm relies on two properties. First, the last character encodes the main category, which already partially orders all sizes. Second, the number of Xs fine-tunes the order within S or L categories. By handling these two cases explicitly, the algorithm guarantees correct comparison for all valid size strings.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b = input().split()
    type_a, type_b = a[-1], b[-1]
    
    if type_a != type_b:
        if type_a == 'S':
            print('<')
        elif type_a == 'M':
            if type_b == 'S':
                print('>')
            else:
                print('<')
        else:  # type_a == 'L'
            print('>' if type_b != 'L' else '=')
    else:
        count_a, count_b = a.count('X'), b.count('X')
        if type_a == 'S':
            print('<' if count_a > count_b else '>' if count_a < count_b else '=')
        elif type_a == 'L':
            print('>' if count_a > count_b else '<' if count_a < count_b else '=')
        else:
            print('=')
```

The code first reads the number of test cases and loops through them. The last character determines the main type, allowing us to short-circuit the comparison when the types differ. If the types match, we count Xs and adjust the comparison according to whether it is S or L. The ordering is inverted for S because more Xs makes it smaller. Medium is handled as a simple equality.

## Worked Examples

For input `XXXS XS`:

| a | b | type_a | type_b | count_a | count_b | Comparison |
| --- | --- | --- | --- | --- | --- | --- |
| XXXS | XS | S | S | 3 | 1 | count_a > count_b → `<` |

We see that XXXS is smaller than XS because three Xs make it smaller.

For input `XL M`:

| a | b | type_a | type_b | count_a | count_b | Comparison |
| --- | --- | --- | --- | --- | --- | --- |
| XL | M | L | M | 1 | 0 | type_a > type_b → `>` |

XL is large and M is medium, so XL > M.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each test case scans at most 50 characters to count Xs, repeated t times |
| Space | O(1) | Only a few variables for counting and type comparison |

With t ≤ 10,000 and n ≤ 50, the algorithm performs at most 500,000 operations, well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        t = int(input())
        for _ in range(t):
            a, b = input().split()
            type_a, type_b = a[-1], b[-1]
            
            if type_a != type_b:
                if type_a == 'S':
                    print('<')
                elif type_a == 'M':
                    print('>' if type_b == 'S' else '<')
                else:  # type_a == 'L'
                    print('>' if type_b != 'L' else '=')
            else:
                count_a, count_b = a.count('X'), b.count('X')
                if type_a == 'S':
                    print('<' if count_a > count_b else '>' if count_a < count_b else '=')
                elif type_a == 'L':
                    print('>' if count_a > count_b else '<' if count_a < count_b else '=')
                else:
                    print('=')
    return out.getvalue().strip()

# provided samples
assert run("6\nXXXS XS\nXXXL XL\nXL M\nXXL XXL\nXXXXXS M\nL M\n") == "<\n>\n>\n=\n<\n>", "sample 1"

# custom cases
assert run("3\nM M\nS M\nXXXL L\n") == "=\n<\n>", "medium equality and extremes"
assert run("2\nXS XXS\nXL XXL\n") == ">\n<", "small and large X counts"
assert run("1\nXXXXXXS XXXXXS\n") == "<", "multiple Xs for small"
assert run("1\nXXXL XXXL\n") == "=", "identical large sizes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| M M | = | Medium equality |
| S M | < | Small vs medium |
| XXXL L | > | Large with extra Xs |
| XS XXS | > | Small X count ordering |
| XL XXL | < | Large X count ordering |
| XXXXXXS XXXXXS | < | Extreme small sizes |
| XXXL XXXL | = | Identical large sizes |

## Edge Cases

For input `XXXXXS M`, the last character comparison immediately identifies M as larger than any small. The algorithm prints `<` without needing to count the Xs. For `XXXL L`, both are large, so the counts of Xs are compared: 3 Xs > 1 X, resulting in `>`. For `
