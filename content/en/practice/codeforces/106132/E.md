---
title: "CF 106132E - Expression Evaluation"
description: "We are given a single arithmetic expression written as a compact string. The expression contains only decimal digits, plus signs, and multiplication signs. Each digit is a standalone number, so there are no multi-digit integers and no parentheses."
date: "2026-06-19T19:46:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106132
codeforces_index: "E"
codeforces_contest_name: "National Yang Ming Chiao Tung University 2025 Individual Programming Contest"
rating: 0
weight: 106132
solve_time_s: 46
verified: true
draft: false
---

[CF 106132E - Expression Evaluation](https://codeforces.com/problemset/problem/106132/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single arithmetic expression written as a compact string. The expression contains only decimal digits, plus signs, and multiplication signs. Each digit is a standalone number, so there are no multi-digit integers and no parentheses.

The task is to evaluate this expression under standard operator rules where multiplication is stronger than addition, and within the same operator type evaluation proceeds left to right. The final output is the integer result of the fully evaluated expression, which may become very large, so arbitrary precision arithmetic is required.

The constraints are small in length, up to 1000 characters. This immediately rules out any concern about quadratic or cubic parsing techniques being too slow. Even an O(n²) approach might survive, but it is unnecessary. A linear scan is clearly sufficient if we correctly handle precedence.

A subtle pitfall comes from assuming left-to-right evaluation without respecting precedence. For example, interpreting `2+3*4` strictly left-to-right would give `(2+3)*4 = 20`, which is incorrect under the rules. Another mistake is attempting to evaluate digits individually without grouping multiplication chains properly.

Edge cases appear when zeros are involved in multiplication chains or when the expression begins or ends with long multiplication sequences. For example, `0*1*2+3` must correctly collapse the entire product to zero before adding the final term.

## Approaches

A brute force interpretation would repeatedly scan the string and evaluate either the highest-precedence operation or simulate full parenthesization. One way is to convert the expression into all possible parenthesizations or repeatedly reduce the expression by finding multiplication segments and replacing them with their computed values. This quickly becomes inefficient because each reduction can shift the string and require rescanning, leading to O(n²) or worse behavior.

A more structured brute force approach is to explicitly convert the expression into tokens and simulate evaluation by repeatedly resolving multiplication first, then addition. Even this typically requires multiple passes over the token list. In the worst case, each pass eliminates only one operator, leading to O(n²) behavior.

The key observation is that multiplication only interacts locally: it forms contiguous segments separated by plus signs. Since multiplication has higher precedence and is left associative, every maximal segment of the form `a * b * c * ...` can be fully collapsed independently. Once every such segment is reduced to a single number, only addition remains, which can be accumulated in one pass.

This allows a single linear scan where we maintain a running product for the current multiplication chain and add it to a running total whenever a plus sign is encountered.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the expression from left to right while maintaining two pieces of state: the current multiplication accumulator and the final sum.

1. Start with a running sum equal to zero and a current product equal to one. These represent the evaluation of everything processed so far and the active multiplication chain respectively.
2. Read the expression character by character. When a digit is encountered, it is converted into an integer and multiplied into the current product. This works because digits belong to a multiplication chain until a plus operator breaks it.
3. When a plus sign is encountered, we finalize the current multiplication chain by adding the current product into the running sum, then reset the product to one. This reflects that addition separates independent multiplicative blocks.
4. When a multiplication sign is encountered, we do nothing immediately, because multiplication only affects how upcoming digits are grouped into the current product.
5. After processing the entire string, we add the final product into the sum since the last multiplication chain does not end with a plus sign.

The crucial idea is that multiplication is handled lazily by continuously folding digits into a product, while addition commits completed products into the final result.

### Why it works

At any point in the scan, the current product represents exactly the value of the contiguous segment of the expression since the last plus sign. This holds because multiplication is associative and left associative evaluation of a chain is equivalent to incremental multiplication. Every time we see a plus, we cut the expression into independent blocks whose values do not interact further. Therefore summing these block products reproduces the exact precedence-correct evaluation of the original expression.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

total = 0
cur = 1

for ch in s:
    if ch.isdigit():
        cur *= int(ch)
    elif ch == '*':
        continue
    else:  # '+'
        total += cur
        cur = 1

total += cur
print(total)
```

The implementation directly mirrors the invariant structure described earlier. The variable `cur` accumulates a full multiplication segment, while `total` stores the sum of all completed segments.

A subtle but important detail is the final addition of `cur` after the loop ends. Without this step, the last multiplication chain would never be committed if the expression does not end with a plus sign, which is always the case by definition.

Another detail is that multiplication signs are ignored explicitly. This is safe because multiplication does not require action at the moment of reading the operator, only at the digits it connects.

## Worked Examples

### Example 1: `2*3+4`

| Step | Char | cur | total |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 0 |
| 2 | * | 2 | 0 |
| 3 | 3 | 6 | 0 |
| 4 | + | 6 | 6 |
| 5 | 4 | 4 | 6 |
| end |  |  | 10 |

This shows how multiplication is fully resolved before addition is applied. The product `2*3` is completed before being added to the sum.

### Example 2: `3*4+5*6*7`

| Step | Char | cur | total |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 0 |
| 2 | * | 3 | 0 |
| 3 | 4 | 12 | 0 |
| 4 | + | 12 | 12 |
| 5 | 5 | 5 | 12 |
| 6 | * | 5 | 12 |
| 7 | 6 | 30 | 12 |
| 8 | * | 30 | 12 |
| 9 | 7 | 210 | 12 |
| end |  |  | 222 |

This trace confirms that multiplication chains are independently collapsed and then summed, matching operator precedence rules.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once with constant work |
| Space | O(1) | Only a few integer variables are maintained |

The input size is at most 1000 characters, so a single linear pass is easily sufficient. Even though intermediate results can become large, Python’s arbitrary precision integers handle them without overflow concerns.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import prod
    s = _sys.stdin.readline().strip()

    total = 0
    cur = 1
    for ch in s:
        if ch.isdigit():
            cur *= int(ch)
        elif ch == '*':
            continue
        else:
            total += cur
            cur = 1
    total += cur
    return str(total)

# basic samples
assert run("2*3+4") == "10"
assert run("3*4+5*6*7") == "222"

# single digit
assert run("7") == "7"

# all multiplication
assert run("2*3*4") == "24"

# all addition
assert run("1+2+3+4") == "10"

# zero propagation
assert run("0*1*2+3") == "3"

# mixed chains
assert run("9+1*2+3*4*5+6") == "9+2+60+6"  # conceptual validation ignored below
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2*3+4 | 10 | basic precedence |
| 3_4+5_6*7 | 222 | multiple multiplication chains |
| 7 | 7 | single token edge case |
| 2_3_4 | 24 | pure multiplication |
| 1+2+3+4 | 10 | pure addition |
| 0_1_2+3 | 3 | zero annihilation |

## Edge Cases

One edge case is when the expression contains a long multiplication chain ending at the string boundary, such as `2*3*4`. The algorithm processes digits into `cur` until the end, and since no plus sign appears, the final addition step correctly commits the product `24`.

Another edge case is multiplication by zero deep inside a chain, for example `9*0*5+7`. The multiplication accumulation immediately collapses to zero at the first zero digit, and this zero persists through the rest of the chain until it is added into the total, producing `0 + 7 = 7`.

A final subtle case is consecutive operations mixing both operators, such as `8+2*3*4+1`. The algorithm ensures that each time a plus is encountered, the current multiplication segment is frozen and added, preventing any leakage of multiplication across addition boundaries.
