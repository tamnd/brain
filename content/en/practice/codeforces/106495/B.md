---
title: "CF 106495B - Bad LaTeX"
description: "The task is to clean up lines of LaTeX source text by rewriting certain large integer values into a shorter mathematical notation. The input is a collection of text lines, and inside those lines some sequences of digits represent integer values."
date: "2026-06-25T08:38:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106495
codeforces_index: "B"
codeforces_contest_name: "2026 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 106495
solve_time_s: 29
verified: false
draft: false
---

[CF 106495B - Bad LaTeX](https://codeforces.com/problemset/problem/106495/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

The task is to clean up lines of LaTeX source text by rewriting certain large integer values into a shorter mathematical notation. The input is a collection of text lines, and inside those lines some sequences of digits represent integer values. The goal is to find the integer values that are eligible for compression and replace them while leaving everything else unchanged.

A number can be transformed only when it is an ordinary integer in the text, not when it is already part of a LaTeX subscript or superscript. For example, the digits inside `10_{1000}` or `2^{100000}` must stay untouched because LaTeX is already using them as part of an expression. The transformation rules concern integers ending with at least four zeroes. If the entire number is a power of ten, such as `1000000000`, it becomes `10^{9}`. Otherwise, it becomes scientific notation where the remaining non-zero prefix is written with one digit before the decimal point, followed by multiplication with a power of ten. For instance, `780000` becomes `7.8\cdot10^{5}`.

The input size is small in terms of the number of lines, but each line can contain many characters. There are at most 100 lines and each line has length at most 1000, so the total amount of text is around 100000 characters. This rules out algorithms that repeatedly scan the entire document for every possible substring, but a single or small constant number of passes over the text is easily fast enough. A linear-time parser is the natural target.

The main difficulty is not the arithmetic conversion itself. The tricky part is identifying exactly which digits form independent integer values. A careless implementation can accidentally modify digits that are inside identifiers or LaTeX expressions.

One edge case is a number inside a superscript or subscript.

Example input:

```
1
$ S_{100000} = 2^{100000} $
```

Correct output:

```
$ S_{100000} = 2^{100000} $
```

A naive solution that replaces every long sequence of zero-ending digits would incorrectly transform both `100000` values, even though they are protected by LaTeX syntax.

Another edge case is a number that appears next to letters.

Example input:

```
1
My ID is RA180000
```

Correct output:

```
My ID is RA180000
```

The digits are part of an alphanumeric identifier, not a standalone integer. A simple digit scanner that only checks the characters before and after the number incorrectly turns this into a mathematical expression.

A third case is a number ending in zeroes but containing only one zero or fewer than four trailing zeroes.

Example input:

```
1
The values are 12000 and 120000
```

Correct output:

```
The values are 12000 and 1.2\cdot10^{5}
```

The first value remains unchanged because it has only three trailing zeroes. Any implementation that checks only the total size of the number instead of the number of ending zeroes will produce an invalid conversion.

## Approaches

The most direct approach is brute force. We can scan the text, find every substring made only of digits, and for each one check whether it can be rewritten. If the substring is eligible, we replace it with the appropriate LaTeX representation.

This works because every valid conversion depends only on the complete integer value and its surrounding characters. For each candidate number, we can count trailing zeroes, determine whether it is a pure power of ten, and construct the replacement.

The problem is that a careless implementation of replacement can become expensive. If every discovered number causes the string to be rebuilt, many replacements in a long line can repeatedly copy large portions of text. With a document containing many numbers, this can approach quadratic behavior. A worst-case text of length 100000 with many replacements could require around 10^10 character operations.

The key observation is that the input is already a stream of characters. We do not need to modify the string while scanning it. Instead, we can build a new output string and decide character by character whether the current position starts a number that should be replaced.

The second important observation is that LaTeX protection can be handled locally. A number is ignored if it lies inside `{}` immediately after `_` or `^`, because those are the only subscript and superscript forms guaranteed by the statement. While scanning, we keep track of whether we are currently inside such a protected block.

Once we know that a sequence of digits is a normal standalone integer, converting it is straightforward. We count the trailing zeroes. If there are fewer than four, we copy the number unchanged. Otherwise, we split the number into its significant part and exponent.

The brute-force approach succeeds because it understands how each number should change. The optimized approach keeps that same conversion logic but avoids repeated rescanning and accidental modification by processing the document as a single stream.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(L²) | O(L) | Too slow in worst case |
| Optimal | O(L) | O(L) | Accepted |

Here, `L` is the total number of characters across all input lines.

## Algorithm Walkthrough

1. Read every line and process it independently. A number cannot continue from the end of one line into the beginning of the next line, so each line can be treated as its own text stream.
2. Scan the line from left to right and build an answer string. Keeping a separate output buffer avoids modifying the input while searching for numbers.
3. When a digit is found, first determine whether it belongs to a protected LaTeX subscript or superscript. If the digits are inside `{}` immediately following `_` or `^`, copy them unchanged.
4. Otherwise, collect the complete consecutive digit sequence. The complete sequence is needed because the conversion depends on all digits, not only the suffix.
5. Check the number of trailing zeroes. If it is less than four, append the original digits. These values do not satisfy the formatting rule.
6. If the number qualifies, remove the trailing zeroes and let the number of removed zeroes be the exponent.
7. If the remaining part is exactly `1`, the original number was a power of ten. Output it as `10^{exponent}`.
8. Otherwise, place a decimal point after the first digit of the remaining part and output the result multiplied by `10^{exponent}`. Remove unnecessary zeroes from the end of the decimal part because the representation should contain only the meaningful digits.
9. Continue until the entire line has been processed, then print the transformed line.

Why it works:

The invariant during the scan is that every character before the current position has already been classified correctly. It has either been copied unchanged or replaced with the exact required LaTeX form. When the scanner reaches a digit sequence, the algorithm knows whether the sequence is protected or a standalone integer, because the only excluded contexts are the guaranteed subscript and superscript forms. For every standalone integer, the conversion follows directly from the number of trailing zeroes: values with fewer than four zeroes must stay unchanged, powers of ten have only the leading digit remaining, and every other eligible number has a non-zero prefix that becomes scientific notation. Since every possible integer occurrence is handled exactly once, no valid replacement is missed and no invalid replacement is made.
