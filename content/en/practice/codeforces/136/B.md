---
title: "CF 136B - Ternary Logic"
description: "We are given two decimal integers, a and c. The computer in this problem does not use binary xor. Instead, it uses a ternary operation called tor. To apply tor, both numbers are written in base 3."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 136
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 97 (Div. 2)"
rating: 1100
weight: 136
solve_time_s: 101
verified: true
draft: false
---

[CF 136B - Ternary Logic](https://codeforces.com/problemset/problem/136/B)

**Rating:** 1100  
**Tags:** implementation, math  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two decimal integers, `a` and `c`. The computer in this problem does not use binary xor. Instead, it uses a ternary operation called `tor`.

To apply `tor`, both numbers are written in base 3. If one number has fewer digits, we pad it with leading zeroes so both lengths match. Then we add corresponding digits modulo 3, independently for every position. There is no carry between digits.

For example, in base 3:

- `14 = 112`
- `50 = 1212`

After padding:

- `0112`
- `1212`

Digit-wise modulo-3 addition gives:

- `(0+1)%3 = 1`
- `(1+2)%3 = 0`
- `(1+1)%3 = 2`
- `(2+2)%3 = 1`

So the result is `1021₃ = 34`.

The task is reversed. We know `a` and `c`, and we must construct the smallest decimal integer `b` such that:

```
a tor b = c
```

The constraints are very small numerically, both values are at most `10^9`. A base-3 representation of `10^9` has only about 20 digits, because:

```
3^20 ≈ 3.4 × 10^9
```

That means we can safely process the numbers digit by digit in ternary form. Any algorithm that works in linear time with respect to the number of ternary digits is effectively constant time for these constraints.

The dangerous part of this problem is handling subtraction modulo 3 correctly. A careless implementation may compute:

```
b_digit = c_digit - a_digit
```

and forget that the result must stay in the range `[0, 2]`.

Consider:

```
a = 2
c = 0
```

In ternary:

```
2 tor 1 = 0
```

because:

```
(2 + 1) % 3 = 0
```

The correct answer is `1`, not `-2`. The proper formula is:

```
b_digit = (c_digit - a_digit + 3) % 3
```

Another easy mistake is forgetting to process remaining digits after one number becomes zero.

Example:

```
a = 0
c = 5
```

Since `5` in ternary is `12`, we need:

```
0 tor b = b
```

so the answer must be `5`.

If we stop as soon as `a == 0`, we would incorrectly ignore higher ternary digits of `c`.

Leading zeroes also matter conceptually. Suppose:

```
a = 14
c = 34
```

The ternary forms have different lengths:

```
14 = 112
34 = 1021
```

We must interpret them as:

```
0112
1021
```

Otherwise digit alignment breaks and produces the wrong answer.

## Approaches

The most direct brute-force solution is to try every possible value of `b`, compute `a tor b`, and check whether it equals `c`.

To compute `tor`, we convert both numbers to base 3 and simulate digit-wise modulo-3 addition. This operation itself is cheap, about 20 digit operations. The problem is the search space. Since `b` could be as large as roughly `10^9`, the brute-force approach may require billions of checks. Even at a few million operations per second, this is completely infeasible.

The reason brute-force works logically is that the operation is deterministic. For every candidate `b`, either:

```
a tor b = c
```

or it does not.

The key observation is that `tor` behaves independently on each ternary digit. There is no carry propagation between positions. That changes the problem from a global search into a local reconstruction problem.

Suppose we are looking at one ternary digit position:

```
(a_digit + b_digit) % 3 = c_digit
```

We know `a_digit` and `c_digit`, so we can solve directly for `b_digit`:

```
b_digit = (c_digit - a_digit + 3) % 3
```

Every ternary position can be reconstructed independently. Once all digits are recovered, we convert the ternary result back to decimal.

This works because modulo arithmetic gives a unique answer in `{0,1,2}` for every pair `(a_digit, c_digit)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^9 × log₃10^9) | O(log₃10^9) | Too slow |
| Optimal | O(log₃10^9) | O(log₃10^9) | Accepted |

## Algorithm Walkthrough

1. Read integers `a` and `c`.
2. Initialize:

- `power = 1`
- `b = 0`

The variable `power` represents the current ternary place value: `1, 3, 9, 27, ...`.
3. While either `a` or `c` still has remaining ternary digits:

- Extract the current ternary digits:

```
da = a % 3
dc = c % 3
```
- Compute the required digit of `b`:

```
db = (dc - da + 3) % 3
```
- Add this digit into the answer:

```
b += db * power
```

This reconstructs the unique ternary digit that satisfies:

```
(da + db) % 3 = dc
```
4. Remove the processed ternary digits:

```
a //= 3
c //= 3
```
5. Move to the next ternary position:

```
power *= 3
```
6. After all digits are processed, print `b`.

### Why it works

The operation `tor` treats every ternary digit independently because there is no carry between positions. For each position we solve:

```
(a_digit + b_digit) % 3 = c_digit
```

Modulo arithmetic guarantees exactly one valid digit `b_digit` in `{0,1,2}`:

```
b_digit = (c_digit - a_digit) mod 3
```

Since every position is reconstructed correctly and positions do not interact, the full number `b` is correct.

The solution is also minimal automatically. Each ternary digit is uniquely determined, so there is only one possible `b`.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, c = map(int, input().split())

b = 0
power = 1

while a > 0 or c > 0:
    da = a % 3
    dc = c % 3

    db = (dc - da + 3) % 3

    b += db * power

    a //= 3
    c //= 3
    power *= 3

print(b)
```

The solution processes the numbers directly in ternary without explicitly building strings or arrays of digits.

The expression:

```
da = a % 3
```

extracts the least significant ternary digit. Integer division by 3 removes that digit afterward.

The subtle part is:

```
db = (dc - da + 3) % 3
```

The extra `+3` prevents negative intermediate values. Without it, cases like:

```
dc = 0
da = 2
```

would incorrectly produce `-2` instead of `1`.

The variable `power` tracks the current ternary place value. When we compute a digit `db`, we place it into the correct position in the final decimal answer using:

```
b += db * power
```

The loop continues while either number still has remaining ternary digits. This correctly handles cases where `a` and `c` have different ternary lengths.

## Worked Examples

### Example 1

Input:

```
14 34
```

Ternary forms:

```
14 = 112
34 = 1021
```

| Step | da | dc | db = (dc-da+3)%3 | power | b |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 2 | 1 | 2 |
| 2 | 1 | 2 | 1 | 3 | 5 |
| 3 | 1 | 0 | 2 | 9 | 23 |
| 4 | 0 | 1 | 1 | 27 | 50 |

Final answer:

```
50
```

This trace shows how differing ternary lengths are handled naturally. Once `a` runs out of digits, its remaining digits behave like leading zeroes.

### Example 2

Input:

```
2 0
```

| Step | da | dc | db | power | b |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 1 | 1 | 1 |

Final answer:

```
1
```

This example demonstrates why modulo subtraction matters. A naive subtraction would give `-2`, but modulo 3 arithmetic correctly wraps it to `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log₃ n) | One iteration per ternary digit |
| Space | O(1) | Only a few integer variables are used |

Even for the maximum input size of `10^9`, the loop runs only about 20 times. The solution is comfortably within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a, c = map(int, input().split())

    b = 0
    power = 1

    while a > 0 or c > 0:
        da = a % 3
        dc = c % 3

        db = (dc - da + 3) % 3

        b += db * power

        a //= 3
        c //= 3
        power *= 3

    print(b)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("14 34\n") == "50\n", "sample 1"

# minimum values
assert run("0 0\n") == "0\n", "both zero"

# modulo wraparound
assert run("2 0\n") == "1\n", "requires modulo subtraction"

# different ternary lengths
assert run("0 5\n") == "5\n", "remaining digits must be processed"

# large values
assert run("1000000000 1000000000\n") == "0\n", "a tor 0 = a"

# carry-like situation should not exist
assert run("8 0\n") == "4\n", "independent ternary digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0` | Minimum boundary |
| `2 0` | `1` | Correct modulo subtraction |
| `0 5` | `5` | Handling different ternary lengths |
| `1000000000 1000000000` | `0` | Large input values |
| `8 0` | `4` | No carry propagation between digits |

## Edge Cases

Consider:

```
0 0
```

The loop never executes because both numbers are already zero. The initialized answer `b = 0` is printed directly. This is correct because:

```
0 tor 0 = 0
```

Now consider:

```
2 0
```

In ternary:

```
2 tor 1 = 0
```

The algorithm computes:

```
db = (0 - 2 + 3) % 3 = 1
```

and returns `1`. This confirms the modulo correction handles negative differences correctly.

Consider different digit lengths:

```
0 5
```

Ternary representation:

```
0 = 0
5 = 12
```

The algorithm keeps running while `c > 0`, producing ternary digits `2` and `1`. The reconstructed number is exactly `12₃ = 5`.

Finally, consider:

```
8 0
```

In ternary:

```
8 = 22
```

We solve digit by digit:

```
(2 + 1) % 3 = 0
(2 + 1) % 3 = 0
```

So:

```
b = 11₃ = 4
```

This example confirms there is no carry interaction between positions. Each digit is solved independently.
