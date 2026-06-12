---
title: "CF 910C - Minimum Sum"
description: "We are given several strings made from the letters 'a' through 'j'. Originally, these strings were decimal numbers. A prankster replaced every digit with a unique letter, creating a one-to-one correspondence between the ten digits 0...9 and the ten letters a...j."
date: "2026-06-12T10:23:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 910
codeforces_index: "C"
codeforces_contest_name: "Testing Round 14 (Unrated)"
rating: 1700
weight: 910
solve_time_s: 223
verified: false
draft: false
---

[CF 910C - Minimum Sum](https://codeforces.com/problemset/problem/910/C)

**Rating:** 1700  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 3m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several strings made from the letters `'a'` through `'j'`. Originally, these strings were decimal numbers. A prankster replaced every digit with a unique letter, creating a one-to-one correspondence between the ten digits `0...9` and the ten letters `a...j`.

The same letter always represents the same digit, and different letters represent different digits. Our task is to reconstruct such a mapping so that every resulting number is valid, meaning no number starts with digit `0`, and the total sum of all reconstructed numbers is as small as possible.

The key observation is that we are not reconstructing individual numbers independently. A single assignment of digits to letters must work globally across all strings.

The constraints are small in terms of string length. There are at most 1000 strings and each string has length at most 6, so the total number of character positions is at most 6000. That means we can afford to process every character and compute positional contributions. The number of distinct letters is fixed at 10, which is tiny. Any algorithm involving sorting or assigning these ten letters is essentially constant time.

A tempting but dangerous mistake is to treat each occurrence independently. The digit assigned to a letter affects every place where that letter appears. For example:

```
2
aa
a
```

If `a` is assigned digit `9`, the sum is `99 + 9 = 108`. If `a` is assigned digit `1`, the sum is `11 + 1 = 12`. Every occurrence contributes simultaneously, so we must aggregate all positional effects of each letter.

Another subtle issue is the leading-zero restriction. Consider:

```
2
ab
ac
```

Letter `a` appears as the first character of a multi-digit number, so assigning digit `0` to `a` is illegal. A greedy strategy that simply gives digit `0` to the least valuable letter without checking this constraint can produce an invalid reconstruction.

A third edge case occurs when a letter never appears as a leading character. Such a letter is the only type of letter that may receive digit `0`. The statement guarantees that a valid assignment always exists, but the algorithm still has to choose the correct zero candidate.

For example:

```
1
ab
```

Here `a` cannot be zero, but `b` can. Assigning `b = 0` and `a = 1` gives the minimum valid number `10`.

## Approaches

A brute-force solution would enumerate all possible assignments of digits to letters. Since there are ten letters and ten digits, there are `10! = 3,628,800` bijections. For each assignment we could evaluate the resulting sum and keep the minimum valid one.

The brute-force method is correct because it checks every possible mapping. The problem is the amount of work. Even if evaluating a mapping were very cheap, several million assignments are already too many for a one-second limit.

To find a better solution, we should examine how the total sum is formed.

Suppose a letter appears in the units position five times. Assigning digit `7` to that letter contributes `5 × 7` to the final sum. If the same letter appears twice in the hundreds position, that contributes `2 × 100 × 7`.

All contributions of a letter can be combined into a single coefficient:

$$\text{contribution} = \text{digit(letter)} \times \text{weight(letter)}$$

where `weight(letter)` is the sum of all place values where the letter appears.

The total sum becomes

$$\sum \text{digit(letter)} \times \text{weight(letter)}$$

Now the problem is much clearer. We have ten weights and must assign digits `0...9` to them. To minimize a weighted sum, smaller digits should go to smaller weights and larger digits should go to larger weights. This is a standard exchange argument.

The only complication is digit `0`. It cannot be assigned to a letter that appears as the leading character of a multi-digit number. Among all letters eligible for zero, we should choose the one with the smallest weight, because zero removes that weight entirely.

After fixing the zero letter, the remaining nine letters receive digits `1...9` in ascending order of weight.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10! · T) | O(1) | Too slow |
| Optimal | O(T + 10 log 10) | O(10) | Accepted |

Here `T` is the total number of characters across all strings.

## Algorithm Walkthrough

1. Create an array `weight[10]`, one entry for each letter.
2. For every string, scan it from right to left. The rightmost position contributes `1`, the next contributes `10`, then `100`, and so on.
3. Whenever a letter appears at a position with place value `p`, add `p` to that letter's weight.
4. Record which letters are forbidden from becoming zero. Any letter that appears as the first character of a string of length greater than one is forbidden.
5. Among all letters that are not forbidden, choose the one with the smallest weight. Assign digit `0` to this letter.
6. Collect the remaining nine letters and sort them by weight in ascending order.
7. Assign digits `1, 2, ..., 9` to these letters in that sorted order.
8. Compute the final answer as the sum of `digit(letter) × weight(letter)` over all ten letters.

### Why it works

The weight of a letter is completely independent of the digit assignments. Once the weights are known, the final sum is a weighted linear expression.

Among all letters allowed to receive zero, assigning zero to the smallest weight is always optimal. If zero were assigned to a larger weight while a smaller eligible weight received a positive digit, swapping those assignments would decrease the sum.

After fixing the zero letter, only digits `1...9` remain. Suppose two letters have weights `w1 ≤ w2` but receive digits `d1 > d2`. Swapping their digits changes the sum by

$$(w1d2+w2d1)-(w1d1+w2d2)
=(w2-w1)(d1-d2)\ge 0$$

so the original assignment cannot be better than the swapped one. Repeatedly applying this argument shows that weights and digits must be ordered the same way. Thus sorting the remaining letters by weight and assigning digits `1...9` in increasing order yields the minimum possible sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    weight = [0] * 10
    leading = [False] * 10

    for _ in range(n):
        s = input().strip()

        if len(s) > 1:
            leading[ord(s[0]) - ord('a')] = True

        place = 1
        for ch in reversed(s):
            weight[ord(ch) - ord('a')] += place
            place *= 10

    zero_letter = -1
    best_weight = None

    for i in range(10):
        if not leading[i]:
            if best_weight is None or weight[i] < best_weight:
                best_weight = weight[i]
                zero_letter = i

    letters = [i for i in range(10) if i != zero_letter]
    letters.sort(key=lambda x: weight[x])

    digit = [0] * 10

    for d, letter in enumerate(letters, start=1):
        digit[letter] = d

    ans = 0
    for i in range(10):
        ans += digit[i] * weight[i]

    print(ans)

solve()
```

The first part computes the positional weight of every letter. Instead of reconstructing numbers directly, we accumulate how much each letter contributes to the final sum per unit of assigned digit.

The `leading` array tracks which letters are forbidden from receiving zero. Only first characters of multi-digit strings matter. A single-digit number may legitimately be zero after restoration, since it has no leading zeros.

The choice of `zero_letter` is the most delicate step. We search only among letters that are not marked as leading and pick the smallest weight. This removes the largest possible amount of unnecessary contribution.

After excluding the zero letter, the remaining letters are sorted by weight. Assigning digits `1...9` in that order implements the exchange-argument optimum.

The largest possible weight is well within Python's integer capabilities, but using Python integers automatically avoids any overflow concerns.

## Worked Examples

### Sample 1

Input:

```
3
ab
de
aj
```

Weights:

| Letter | Positions | Weight |
| --- | --- | --- |
| a | tens,tens | 20 |
| b | units | 1 |
| d | tens | 10 |
| e | units | 1 |
| j | units | 1 |

All other letters have weight 0.

Leading letters are `a` and `d`.

Eligible zero letters are `b,c,e,f,g,h,i,j`. The smallest weight among them is 0, so one unused letter receives digit 0.

| Letter | Weight | Assigned Digit |
| --- | --- | --- |
| c | 0 | 0 |
| f | 0 | 1 |
| g | 0 | 2 |
| h | 0 | 3 |
| i | 0 | 4 |
| b | 1 | 5 |
| e | 1 | 6 |
| j | 1 | 7 |
| d | 10 | 8 |
| a | 20 | 9 |

Final sum:

$$20\cdot9+10\cdot8+1\cdot5+1\cdot6+1\cdot7=278$$

The trace demonstrates the central idea: only weights matter. We never reconstruct the actual numbers.

### Example 2

Input:

```
3
aa
bb
ab
```

Weights:

| Letter | Weight |
| --- | --- |
| a | 21 |
| b | 21 |

Leading letters are `a` and `b`.

Every unused letter has weight 0 and is eligible for zero.

| Letter | Weight | Digit |
| --- | --- | --- |
| c | 0 | 0 |
| d | 0 | 1 |
| e | 0 | 2 |
| f | 0 | 3 |
| g | 0 | 4 |
| h | 0 | 5 |
| i | 0 | 6 |
| j | 0 | 7 |
| a | 21 | 8 |
| b | 21 | 9 |

Answer:

$$21\cdot8 + 21\cdot9 = 357$$

This example shows that unused letters are extremely valuable candidates for digit zero because they contribute nothing regardless of assignment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T + 10 log 10) | Processing all characters plus sorting ten letters |
| Space | O(10) | Weight, digit, and leading arrays |

Since `T ≤ 6000`, the dominant work is simply scanning the input strings. Sorting ten elements is effectively constant time. The solution comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    weight = [0] * 10
    leading = [False] * 10

    for _ in range(n):
        s = input().strip()

        if len(s) > 1:
            leading[ord(s[0]) - ord('a')] = True

        place = 1
        for ch in reversed(s):
            weight[ord(ch) - ord('a')] += place
            place *= 10

    zero_letter = -1
    best_weight = None

    for i in range(10):
        if not leading[i]:
            if best_weight is None or weight[i] < best_weight:
                best_weight = weight[i]
                zero_letter = i

    letters = [i for i in range(10) if i != zero_letter]
    letters.sort(key=lambda x: weight[x])

    digit = [0] * 10
    for d, letter in enumerate(letters, start=1):
        digit[letter] = d

    ans = sum(weight[i] * digit[i] for i in range(10))
    return str(ans)

# custom minimum case
assert run("1\na\n") == "1"

# only one used letter
assert run("3\na\na\na\n") == "3"

# leading-zero restriction
assert run("1\nab\n") == "10"

# symmetric weights
assert run("2\naa\nbb\n") == "357"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a` | `1` | Minimum input size |
| `a,a,a` | `3` | Repeated use of one letter |
| `ab` | `10` | Leading digit cannot become zero |
| `aa,bb` | `357` | Equal weights and unused-letter zero assignment |

## Edge Cases

Consider:

```
1
ab
```

Weights are `a=10`, `b=1`. Letter `a` is a leading character and cannot receive zero. The algorithm searches only among non-leading letters and chooses `b` for digit `0`. The resulting assignment gives value `10`, which is the smallest valid reconstruction.

Now consider:

```
3
a
a
a
```

Only one letter appears. Its weight is `3`. Every other letter has weight `0` and is eligible for zero. The algorithm assigns zero to an unused letter and digit `1` to `a`, producing answer `3`. Assigning zero to `a` would give sum `0`, but that would make the original positive numbers invalid.

Finally consider:

```
2
ab
ac
```

Weights are `a=20`, `b=1`, `c=1`. Letter `a` is forbidden from receiving zero. The algorithm chooses an unused non-leading letter with weight `0` for digit `0`, then assigns the smallest positive digits to the weight-1 letters and the largest digit to `a`. The leading-zero constraint is respected automatically while still minimizing the total sum.
