---
title: "CF 4A - Watermelon"
description: "The problem gives a single integer w, the weight of a watermelon. We need to decide whether it can be split into two pos"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 4
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 4 (Div. 2 Only)"
rating: 800
weight: 4
solve_time_s: 46
verified: true
draft: false
---
## Solution
## Problem Understanding

The problem gives a single integer `w`, the weight of a watermelon. We need to decide whether it can be split into two positive parts such that both parts are even numbers.

The word "positive" matters here. Splitting `2` into `0 + 2` is not allowed because one part would have zero weight. Both children must receive a strictly positive piece.

The constraints are tiny, `w` is at most `100`. Even a slow brute-force solution would easily run within the time limit. That means the challenge is not performance, it is recognizing the exact mathematical condition that makes the split possible.

The first important observation is that the sum of two even numbers is always even. So if `w` is odd, the answer is immediately `NO`.

The second observation is less obvious. Even if `w` itself is even, some values still fail. The smallest even number is `2`, and it cannot be split into two positive even numbers. The only possible split is `1 + 1`, which uses odd numbers, or `0 + 2`, which is invalid because zero is not positive.

A careless implementation often checks only whether `w` is even. That fails for input:

```
2
```

A naive condition like `w % 2 == 0` would print `YES`, but the correct answer is `NO`.

Another edge case is the smallest odd value:

```
1
```

There is no way to split an odd number into two even numbers because even plus even is always even. The correct output is `NO`.

The first valid case is:

```
4
```

We can split it into `2 + 2`, both positive and even. The correct output is `YES`.

## Approaches

The most direct brute-force approach is to try every possible first piece from `1` to `w - 1`. For each value `a`, compute the second piece as `b = w - a`. If both `a` and `b` are even and positive, we found a valid split.

This works because it checks every possible partition of the watermelon. With `w ≤ 100`, the brute-force solution performs at most `99` checks, which is completely fine.

Still, the brute-force approach is doing more work than necessary. The real structure of the problem comes from parity.

If two positive even numbers add up to `w`, then `w` must itself be even. That removes every odd number immediately.

Now consider even numbers. Any even number greater than `2` can always be written as:

```
2 + (w - 2)
```

If `w > 2` and even, then `w - 2` is also even and positive. That guarantees a valid split.

So the entire problem reduces to one condition:

```
w is even and w > 2
```

That gives an O(1) mathematical solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(w) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `w`.

This is the total weight of the watermelon.
2. Check whether `w` is even.

If `w` is odd, it cannot be expressed as the sum of two even numbers, so the answer must be `NO`.
3. Check whether `w` is greater than `2`.

The value `2` is even, but it cannot be divided into two positive even parts. Every even number larger than `2` works.
4. If both conditions are true, print `YES`. Otherwise, print `NO`.

## Python Solution

```python
import sys
input = sys.stdin.readline

w = int(input())

if w % 2 == 0 and w > 2:
    print("YES")
else:
    print("NO")
```

The program reads the watermelon weight and applies the mathematical condition directly.

The expression `w % 2 == 0` checks whether the number is even. The second condition, `w > 2`, removes the only invalid even case.

The order of the checks does not matter here because both are constant-time operations. There are no overflow concerns since the input size is extremely small.

One easy mistake is forgetting the positivity requirement for both parts. Without the `w > 2` condition, input `2` would incorrectly return `YES`.

## Worked Examples

### Example 1

Input:

```
8
```

| Step | Value |
| --- | --- |
| Read `w` | 8 |
| `w % 2 == 0` | True |
| `w > 2` | True |
| Output | YES |

The number `8` is even and greater than `2`. One valid split is `2 + 6`.

### Example 2

Input:

```
2
```

| Step | Value |
| --- | --- |
| Read `w` | 2 |
| `w % 2 == 0` | True |
| `w > 2` | False |
| Output | NO |

This example demonstrates the tricky edge case. Although `2` is even, there is no way to split it into two positive even integers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic checks are performed |
| Space | O(1) | No extra memory is used |

The solution easily fits within the limits. It performs constant work regardless of the input value and uses only a couple of variables.

## Test Cases

### Test Case 1

Input:

```
1
```

Expected output:

```
NO
```

This verifies that odd numbers are rejected immediately.

### Test Case 2

Input:

```
4
```

Expected output:

```
YES
```

This is the smallest valid watermelon weight.

### Test Case 3

Input:

```
2
```

Expected output:

```
NO
```

This catches implementations that only check whether the number is even.

### Test Case 4

Input:

```
100
```

Expected output:

```
YES
```

This checks the upper boundary of the constraints.

## Edge Cases

The first non-obvious edge case is:

```
2
```

The algorithm checks `w % 2 == 0`, which is true. Then it checks `w > 2`, which is false. Since both conditions are not satisfied, the program prints `NO`.

This correctly handles the positivity requirement. The only even decomposition would involve zero, which is not allowed.

Another important edge case is:

```
1
```

The algorithm checks `w % 2 == 0`. Since `1` is odd, the condition fails immediately and the output becomes `NO`.

This matches the mathematical fact that two even numbers can never sum to an odd number.

Now consider:

```
4
```

The algorithm sees that `4` is even and greater than `2`, so it prints `YES`.

A valid split is `2 + 2`, where both parts are positive and even.
