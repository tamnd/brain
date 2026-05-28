---
title: "CF 5C - Longest Regular Bracket Sequence"
description: "We are given a string containing only '(' and ')'. Among all substrings, we need to find the longest one that forms a va"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dp", "greedy", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 5
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 5"
rating: 1900
weight: 5
solve_time_s: 160
verified: true
draft: false
---
## Solution
## Problem Understanding

We are given a string containing only `'('` and `')'`. Among all substrings, we need to find the longest one that forms a valid bracket sequence. After that, we also need to count how many substrings achieve that maximum length.

A valid bracket sequence behaves like properly matched parentheses in an expression. Every opening bracket must eventually be closed, and at no point can closing brackets outnumber opening brackets while scanning from left to right.

The input length can reach $10^6$. That changes the problem completely. A quadratic solution would need around $10^{12}$ operations in the worst case, which is impossible in 2 seconds. Even $O(n \sqrt n)$ would be risky in Python at this scale. The target is linear time, or very close to it.

The tricky part is that we are not checking the whole string. We are checking every possible substring implicitly. A naive implementation often recomputes validity from scratch for many overlapping ranges.

One edge case is a string with no valid substring at all.

Input:

```
))))
```

There is no valid bracket sequence anywhere. The required output is:

```
0 1
```

The count must be `1`, not `0`. The problem defines this special case explicitly.

Another dangerous case is when multiple longest substrings exist.

Input:

```
()())()()
```

The longest valid substring length is `4`, and there are two such substrings: `"()()"` at two different positions. A careless solution might only remember one occurrence.

Nested structures also matter.

Input:

```
((()))
```

The entire string is valid, even though no prefix becomes balanced until the end. Solutions based only on counting adjacent pairs fail here.

Broken prefixes are another common trap.

Input:

```
)()())
```

The first character is invalid immediately, but later parts contain correct sequences. A correct algorithm must reset appropriately after unmatched closing brackets.

## Approaches

The brute-force solution is straightforward. Generate every substring, check whether it is a regular bracket sequence, and keep track of the maximum length and its frequency.

Checking one substring can be done with a balance counter. Increment for `'('`, decrement for `')'`. If balance ever becomes negative, the substring is invalid. At the end, balance must return to zero.

This works logically, but the complexity is terrible. There are $O(n^2)$ substrings. Validating each substring takes $O(n)$ time in the worst case. Total complexity becomes $O(n^3)$.

Even if we optimize validity checking with prefix sums, we still examine $O(n^2)$ substrings. With $n = 10^6$, that is completely infeasible.

The key insight is that valid bracket substrings have a strong structural property. Whenever we encounter a closing bracket `')'`, it can only complete a sequence if there is an unmatched `'('` before it.

This naturally suggests using a stack.

We store indices of unmatched opening brackets. When we see `'('`, we push its index. When we see `')'`, we try to match it with the latest unmatched `'('`.

The subtle trick is handling invalid boundaries. Suppose we encounter a closing bracket with nothing to match. Then any future valid substring must start after this position. To represent that boundary cleanly, we keep a special index on the stack.

At every successful match, the current valid substring length becomes:

$$i - \text{stack top}$$

because the stack top marks the position before the valid segment starts.

This gives a linear scan with constant work per character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal Stack Solution | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a stack with `-1`.

This acts as a virtual boundary before the string starts. It helps compute substring lengths correctly when a valid sequence begins at index `0`.
2. Maintain two variables, `best_len` and `count`.

`best_len` stores the maximum valid substring length found so far. `count` stores how many substrings achieve that length.
3. Scan the string from left to right.

Each position is processed once, which keeps the algorithm linear.
4. If the current character is `'('`, push its index onto the stack.

This bracket may later match some closing bracket.
5. If the current character is `')'`, pop once from the stack.

We try to match this closing bracket with the most recent unmatched opening bracket.
6. After popping, check whether the stack became empty.

If it is empty, this `')'` has no valid matching `'('`. Push the current index as the new invalid boundary.
7. Otherwise, compute the current valid substring length as:

$$\text{current\_len} = i - \text{stack[-1]}$$

The stack top now represents the position before the valid substring starts.
8. Compare `current_len` with `best_len`.

If it is larger, update `best_len` and reset `count = 1`.
9. If `current_len == best_len`, increment `count`.

Another substring with the same maximum length has been found.
10. After processing the entire string, handle the special case.

If `best_len == 0`, print:

```
0 1
```

Otherwise print `best_len` and `count`.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

stack = [-1]

best_len = 0
count = 0

for i, ch in enumerate(s):
    if ch == '(':
        stack.append(i)
    else:
        stack.pop()

        if not stack:
            stack.append(i)
        else:
            current_len = i - stack[-1]

            if current_len > best_len:
                best_len = current_len
                count = 1
            elif current_len == best_len:
                count += 1

if best_len == 0:
    print(0, 1)
else:
    print(best_len, count)
```

The stack stores indices, not characters. That detail matters because we need substring lengths later.

The initial `-1` is the core trick. Without it, substrings starting at index `0` would require special handling. For example, `"()"` would produce incorrect lengths.

When processing a closing bracket, we pop first. If the stack becomes empty afterward, that means there was no matching opening bracket. We push the current index as a reset boundary.

The expression:

```
i - stack[-1]
```

works because `stack[-1]` points to the last unmatched position before the current valid substring.

The special case `0 1` is easy to forget. If no valid substring exists, the count is defined as `1`.

## Worked Examples

### Example 1

Input:

```
)((())))(()())
```

| i | char | stack after operation | current_len | best_len | count |
| --- | --- | --- | --- | --- | --- |
| 0 | ) | [0] | - | 0 | 0 |
| 1 | ( | [0,1] | - | 0 | 0 |
| 2 | ( | [0,1,2] | - | 0 | 0 |
| 3 | ( | [0,1,2,3] | - | 0 | 0 |
| 4 | ) | [0,1,2] | 2 | 2 | 1 |
| 5 | ) | [0,1] | 4 | 4 | 1 |
| 6 | ) | [0] | 6 | 6 | 1 |
| 7 | ) | [7] | - | 6 | 1 |
| 8 | ( | [7,8] | - | 6 | 1 |
| 9 | ( | [7,8,9] | - | 6 | 1 |
| 10 | ) | [7,8] | 2 | 6 | 1 |
| 11 | ( | [7,8,11] | - | 6 | 1 |
| 12 | ) | [7,8] | 4 | 6 | 1 |
| 13 | ) | [7] | 6 | 6 | 2 |

Final output:

```
6 2
```

This trace shows two different valid substrings of length `6`. The invalid bracket at index `7` resets the boundary correctly.

### Example 2

Input:

```
)()())
```

| i | char | stack after operation | current_len | best_len | count |
| --- | --- | --- | --- | --- | --- |
| 0 | ) | [0] | - | 0 | 0 |
| 1 | ( | [0,1] | - | 0 | 0 |
| 2 | ) | [0] | 2 | 2 | 1 |
| 3 | ( | [0,3] | - | 2 | 1 |
| 4 | ) | [0] | 4 | 4 | 1 |
| 5 | ) | [5] | - | 4 | 1 |

Final output:

```
4 1
```

This example demonstrates why unmatched closing brackets must reset the boundary. Without that reset, later lengths would be computed incorrectly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is pushed and popped at most once |
| Space | O(n) | The stack may store all indices in the worst case |

With $n \le 10^6$, a linear solution is exactly what we need. The algorithm performs a single pass over the string and uses only simple stack operations, which easily fits within the time limit in Python.

## Test Cases

### Test Case 1

Input:

```
(
```

Expected output:

```
0 1
```

This verifies the minimum-size invalid input.

### Test Case 2

Input:

```
()()()
```

Expected output:

```
6 1
```

The whole string is valid, even though it consists of multiple smaller valid blocks.

### Test Case 3

Input:

```
))))((((
```

Expected output:

```
0 1
```

This checks that the algorithm handles completely invalid strings correctly.

### Test Case 4

Input:

```
()(())
```

Expected output:

```
6 1
```

This combines concatenation and nesting in the same valid substring.

## Edge Cases

Consider the input:

```
))))
```

The algorithm starts with `stack = [-1]`.

At index `0`, we encounter `')'`. After popping, the stack becomes empty, so we push `0`.

The same thing happens for every remaining character. No valid substring is ever formed, so `best_len` remains `0`.

Final output:

```
0 1
```

Now consider:

```
()())()()
```

The algorithm finds `"()()"` twice. The first occurs before the unmatched `')'`, the second occurs after it.

When the unmatched closing bracket appears, its index becomes the new boundary. This prevents invalid substrings from incorrectly extending across the broken point.

Final output:

```
4 2
```

For nested brackets:

```
((()))
```

The stack grows during the opening brackets and shrinks during the closing brackets.

At the final character, the computed length becomes:

```
5 - (-1) = 6
```

The whole string is recognized as valid.

Final output:

```
6 1
```

Finally, consider:

```
)()(()
```

The first character immediately creates an invalid boundary. Later, the algorithm still correctly detects the substring `"()"`.

The unfinished `"(()"` at the end never reaches balance zero, so it does not count.

Final output:

```
2 1
```
