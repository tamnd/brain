---
title: "CF 5B - Center Alignment"
description: "The task is to print a block of text inside a rectangular frame made of characters. Every line of text must be centered"
date: "2026-05-27T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 5
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 5"
rating: 1200
weight: 5
solve_time_s: 187
verified: true
draft: false
---

[CF 5B - Center Alignment](https://codeforces.com/problemset/problem/5/B)

**Rating:** 1200  
**Tags:** implementation, strings  
**Solve time:** 3m 7s  
**Verified:** yes  
**Share:** https://chatgpt.com/share/6a17224c-69e4-83ec-a904-d4ed640fb74c  

## Solution
## Problem Understanding

The task is to print a block of text inside a rectangular frame made of `*` characters. Every line of text must be centered horizontally.

The width of the block is determined by the longest input line. Every shorter line needs spaces added on both sides until it reaches that width. After padding, we surround the line with `*` on the left and right.

The tricky part is handling odd differences. Suppose the longest line has length `10`, and another line has length `7`. We need `3` extra spaces. Perfect centering is impossible because the spaces cannot be split evenly. The problem asks us to alternate the extra space between the left and right sides. The first such ambiguous line gets the larger padding on the left side, the next one gets it on the right side, and so on.

The input size is tiny. The total number of characters across all lines is at most `1000`. Even an `O(n^2)` implementation would pass comfortably because the worst case is only about one million simple operations. That means the challenge is not efficiency, it is careful implementation of the formatting rules.

The first easy-to-miss edge case is empty lines. Blank lines are valid input because lines may contain spaces or even be empty after stripping the newline. A careless solution might skip them while reading input. For example:

```
abc

x
```

The middle line still has to appear inside the frame as a centered empty row.

Another subtle case happens when the padding difference is odd multiple times in a row. Consider:

```
abcd
a
b
c
```

The maximum width is `4`. Each single-letter line needs `3` spaces of padding. The first ambiguous line should place the extra space on the left, the second on the right, the third on the left again. If we always bias to one side, the output becomes incorrect.

A third source of bugs is forgetting that the frame width includes two border stars. If the longest line has length `m`, the top and bottom borders must contain `m + 2` stars. Missing those extra two characters shifts the whole output.

## Approaches

A brute-force idea is to repeatedly insert spaces into each line until it reaches the maximum width. For every short line, we could alternately add spaces to the left and right sides one by one. This works because eventually every line reaches the target length while maintaining the centering rule.

The problem with that approach is not performance, since the constraints are small enough anyway. The real issue is complexity of implementation. Repeatedly modifying strings character by character is awkward and easy to get wrong, especially with the alternating tie-breaking rule.

The cleaner observation is that we already know exactly how many spaces are needed. If a line has length `L` and the maximum width is `W`, then:

- Total padding is `W - L`
- Left padding is `(W - L) // 2`
- Right padding is the remaining spaces

When the difference is even, both sides are equal. When it is odd, one side gets one extra space. The only remaining job is deciding which side receives it. We keep a boolean toggle that alternates every time we encounter an odd difference.

This turns the whole problem into direct arithmetic instead of simulation. Every line is processed once, and the output is built immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total_chars²) | O(total_chars) | Accepted but clumsy |
| Optimal | O(total_chars) | O(total_chars) | Accepted |

## Algorithm Walkthrough

1. Read all input lines until EOF.

The problem does not provide the number of lines, so we simply read everything from standard input.
2. Remove only the trailing newline character from each line.

We must preserve all internal spaces and empty lines. Using `strip()` would be wrong because it removes meaningful spaces.
3. Compute the maximum line length `W`.

Every line must eventually become exactly this width before adding the frame borders.
4. Print the top border using `W + 2` stars.

The extra two characters account for the left and right frame borders.
5. Maintain a toggle variable for odd padding cases.

Start with the rule "extra space goes to the left". After handling one odd-length difference, flip the toggle.
6. For each line, compute the required padding.

Let `diff = W - len(line)`.

If `diff` is even:

- Left padding = `diff // 2`
- Right padding = `diff // 2`

If `diff` is odd:

- One side gets `diff // 2`
- The other gets `diff // 2 + 1`
- Alternate which side receives the larger share.
7. Print the formatted line.

The final structure is:

```
* + left spaces + line + right spaces + *
```
8. Print the bottom border.

It is identical to the top border.

## Python Solution

```python
import sys
input = sys.stdin.readline

lines = [line.rstrip('\n') for line in sys.stdin]

width = max(len(line) for line in lines)

border = '*' * (width + 2)
print(border)

left_extra = True

for line in lines:
    diff = width - len(line)

    left = diff // 2
    right = diff // 2

    if diff % 2 == 1:
        if left_extra:
            left += 1
        else:
            right += 1

        left_extra = not left_extra

    print('*' + ' ' * left + line + ' ' * right + '*')

print(border)
```

The first part reads every line from standard input and removes only the newline character. Using `rstrip('\n')` is important because `strip()` would remove spaces that belong to the actual text.

The variable `width` stores the longest line length. Every other line is padded until it matches this width.

The toggle variable `left_extra` controls the alternating behavior for odd padding differences. If the current ambiguous line gives the extra space to the left, the next ambiguous line gives it to the right.

The padding calculation is straightforward integer arithmetic. Even differences split perfectly. Odd differences split almost evenly, with one extra space assigned according to the toggle.

Finally, every line is wrapped with `*` characters, and the border is printed above and below the text block.

## Worked Examples

### Example 1

Input:

```
This  is

Codeforces
Beta
Round
5
```

Maximum width is `10` because `"Codeforces"` has length `10`.

| Line | Length | diff | Left Spaces | Right Spaces | Toggle After |
| --- | --- | --- | --- | --- | --- |
| `This  is` | 8 | 2 | 1 | 1 | unchanged |
| `` | 0 | 10 | 5 | 5 | unchanged |
| `Codeforces` | 10 | 0 | 0 | 0 | unchanged |
| `Beta` | 4 | 6 | 3 | 3 | unchanged |
| `Round` | 5 | 5 | 3 | 2 | flipped |
| `5` | 1 | 9 | 4 | 5 | flipped |

Output:

```
************
* This  is *
*          *
*Codeforces*
*   Beta   *
*   Round  *
*    5     *
************
```

This trace shows the alternating rule in action. `"Round"` receives the larger padding on the left side, while `"5"` receives it on the right side.

### Example 2

Input:

```
abcd
a
bb
ccc
```

Maximum width is `4`.

| Line | Length | diff | Left Spaces | Right Spaces | Toggle After |
| --- | --- | --- | --- | --- | --- |
| `abcd` | 4 | 0 | 0 | 0 | unchanged |
| `a` | 1 | 3 | 2 | 1 | flipped |
| `bb` | 2 | 2 | 1 | 1 | unchanged |
| `ccc` | 3 | 1 | 0 | 1 | flipped |

Output:

```
******
*abcd*
*  a *
* bb *
*ccc *
******
```

This example highlights both odd and even padding differences. The line `"a"` gets the extra space on the left because it is the first odd case. The line `"ccc"` gets the extra space on the right because the toggle has flipped.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total_chars) | Each character is processed a constant number of times |
| Space | O(total_chars) | All input lines are stored |

The constraints are extremely small, with at most `1000` total characters. A linear solution runs instantly and easily fits within the memory limit.

## Test Cases

### Test Case 1

Input:

```
a
```

Expected output:

```
***
*a*
***
```

This verifies the minimum valid input.

### Test Case 2

Input:

```
abcd
x
y
```

Expected output:

```
******
*abcd*
*  x *
* y  *
******
```

This checks alternating behavior across multiple odd differences.

### Test Case 3

Input:

```
abc

de
```

Expected output:

```
*****
*abc*
*   *
*de *
*****
```

This confirms that empty lines are preserved correctly.

### Test Case 4

Input:

```
same
size
test
case
```

Expected output:

```
******
*same*
*size*
*test*
*case*
******
```

This verifies that lines with equal length receive no extra padding.

## Edge Cases

The first tricky case is empty lines.

Input:

```
abc

x
```

The maximum width is `3`. The empty line has length `0`, so it needs `3` spaces of padding. Since the difference is odd and this is the first ambiguous case, the extra space goes to the left side. The algorithm produces:

```
*****
*abc*
*   *
* x *
*****
```

The blank line remains visible inside the frame instead of disappearing.

Another subtle case is repeated odd differences.

Input:

```
abcd
a
b
c
```

All three short lines need `3` spaces of padding. The algorithm alternates the larger side correctly:

```
******
*abcd*
*  a *
* b  *
*  c *
******
```

Without the toggle variable, all lines would lean in the same direction.

The final edge case is handling already centered lines.

Input:

```
long
wide
text
```

Every line already has length `4`, so `diff = 0` for all rows. The algorithm adds no padding and simply wraps the text with borders:

```
******
*long*
*wide*
*text*
******
```

This confirms that the padding logic does not introduce unnecessary spaces.
