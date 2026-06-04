---
title: "CF 260A - Adding Digits"
description: "We start with a number a. We want to extend it exactly n times. A single extension means appending one decimal digit to the right of the current number. The digit can be anything from 0 to 9, but after appending it, the resulting number must be divisible by b."
date: "2026-06-04T17:49:33+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 260
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 158 (Div. 2)"
rating: 1400
weight: 260
solve_time_s: 146
verified: false
draft: false
---

[CF 260A - Adding Digits](https://codeforces.com/problemset/problem/260/A)

**Rating:** 1400  
**Tags:** implementation, math  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a number `a`. We want to extend it exactly `n` times.

A single extension means appending one decimal digit to the right of the current number. The digit can be anything from `0` to `9`, but after appending it, the resulting number must be divisible by `b`.

After performing this operation exactly `n` times, we must output the final number. If at any step there is no digit that can be appended while keeping divisibility by `b`, then the process stops and the answer is `-1`.

The constraints are small for `a` and `b`, but `n` can be as large as `100000`. That immediately tells us that any algorithm that performs expensive arithmetic on the whole growing number is dangerous, because the number itself may end up containing more than 100000 digits. We need a method whose work per appended digit is constant or nearly constant.

A subtle point is that the divisibility condition must hold after every extension, not only at the end. For example:

```
a = 1, b = 11, n = 2
```

If we append digits arbitrarily and only check the final number, we might create an invalid intermediate state. The operation itself requires divisibility at each step.

Another easy mistake is assuming that if one extension is possible, all future extensions are possible. Consider:

```
a = 1, b = 2, n = 1
```

Appending `0` gives `10`, which works.

But for

```
a = 1, b = 11, n = 1
```

there is no digit `d` such that `1d` is divisible by `11`, so the correct answer is:

```
-1
```

A careless implementation that tries to continue anyway would be wrong.

There is also an important observation about later steps. Once we have found a number divisible by `b`, appending a `0` keeps divisibility only when `10` is compatible with `b`. In general, appending `0` does not preserve divisibility. For example:

```
12 % 3 = 0
120 % 3 = 0
```

but

```
14 % 7 = 0
140 % 7 = 0
```

works only because of the specific divisor. We must reason carefully about what happens after the first successful extension.

## Approaches

The most direct approach is to simulate the process exactly as described. At each step, try all ten possible digits. For each digit, construct the new number and check whether it is divisible by `b`. If some digit works, append it and continue.

The logic is correct because it literally follows the definition of the operation. The problem is that the number quickly becomes huge. After `100000` extensions, it may contain over `100000` digits. Repeatedly constructing and dividing such numbers is far too expensive.

The key observation is that divisibility depends only on the remainder modulo `b`.

Suppose the current number is `x`. Appending digit `d` creates

```
x' = 10x + d
```

We need

```
(10x + d) % b = 0
```

The current value of `x` itself is not important. Only `x % b` matters.

At the beginning, we know the remainder of `a` modulo `b`. We try digits `0` through `9` and look for one that makes

```
(10 * remainder + d) % b == 0
```

If such a digit exists, then the newly formed number is divisible by `b`.

Now comes the crucial simplification. After the first successful extension, the current number is divisible by `b`, so its remainder becomes `0`.

From that point onward, every future step starts from remainder `0`. We only need a digit `d` satisfying

```
d % b = 0
```

Since `0` is always such a digit, appending `0` works forever once we already have a divisible number.

So the whole problem reduces to finding a single digit that makes the first extension divisible by `b`. If no such digit exists, the answer is `-1`. Otherwise, append that digit once and then append `n - 1` zeros.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10n) arithmetic on increasingly large integers | O(n) | Too slow |
| Optimal | O(10 + n) | O(n) for the output string | Accepted |

## Algorithm Walkthrough

1. Compute `r = a % b`.
2. Try every digit `d` from `0` to `9`.
3. Check whether `(r * 10 + d) % b == 0`.
4. If no digit satisfies the condition, output `-1`.
5. Otherwise, let the first valid digit be `d`.
6. Form the answer as the decimal representation of `a`, followed by digit `d`.
7. Append exactly `n - 1` zeros.
8. Output the resulting string.

The reason step 7 works is that after appending the first valid digit, the current number is divisible by `b`. Its remainder modulo `b` is now zero. Appending a zero produces

```
10 * current
```

whose remainder is still zero because

```
(10 * 0) % b = 0
```

when working with the current remainder representation.

### Why it works

Let `r = a % b`.

The first appended digit must satisfy

```
(10r + d) % b = 0
```

because appending `d` transforms the number into `10a + d`, and remainders modulo `b` are preserved by this expression.

If no digit from `0` to `9` satisfies the equation, the very first operation is impossible, so the answer must be `-1`.

If a digit `d` satisfies it, then the new number is divisible by `b`. Its remainder becomes zero. Every later extension appends digit `0`. Starting from remainder zero, the next remainder is

```
(10 * 0 + 0) % b = 0.
```

The remainder never changes again. Every intermediate number is divisible by `b`, so all required operations are valid. The constructed number is exactly the result after `n` extensions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, n = map(int, input().split())

    r = a % b

    for d in range(10):
        if (r * 10 + d) % b == 0:
            ans = str(a) + str(d) + "0" * (n - 1)
            print(ans)
            return

    print(-1)

if __name__ == "__main__":
    solve()
```

The first part computes the remainder of `a` modulo `b`. This is the only information needed to determine whether a digit can be appended successfully.

The loop over digits `0` through `9` searches for a valid first extension. There are only ten possibilities, so this search is constant time.

Once a valid digit is found, the answer is built as a string. Using strings is important because the final number may contain over 100000 digits. Storing it as an integer would be unnecessary and inefficient.

The expression `"0" * (n - 1)` appends exactly the remaining extensions. When `n = 1`, this becomes an empty string, which correctly produces only one appended digit.

If the loop finishes without finding a valid digit, the first operation cannot be performed and the correct answer is `-1`.

## Worked Examples

### Example 1

Input:

```
5 4 5
```

| Step | Value |
| --- | --- |
| a | 5 |
| b | 4 |
| n | 5 |
| r = a % b | 1 |
| First valid digit | 2 |
| Prefix after first extension | 52 |
| Added zeros | 4 |
| Final answer | 520000 |

The check succeeds because:

```
(1 * 10 + 2) % 4 = 0
```

After obtaining `52`, which is divisible by `4`, every remaining extension can use digit `0`.

### Example 2

Input:

```
1 11 1
```

| Step | Value |
| --- | --- |
| r = 1 % 11 | 1 |
| Digits tested | 0..9 |
| Successful digit | none |
| Output | -1 |

The values checked are:

```
10, 11, 12, ..., 19
```

None of them is divisible by `11`, so the very first extension is impossible.

This example demonstrates the failure case where no valid digit exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Ten digit checks plus construction of an output string of length about n |
| Space | O(n) | The output string itself contains O(n) characters |

The dominant cost is producing the answer, which may contain up to roughly 100001 digits. This fits comfortably within the limits. The algorithm performs only ten modular checks regardless of `n`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        a, b, n = map(int, input().split())

        r = a % b

        for d in range(10):
            if (r * 10 + d) % b == 0:
                return str(a) + str(d) + "0" * (n - 1)

        return "-1"

    return solve()

# sample from statement
assert run("5 4 5\n") == "520000", "sample"

# minimum values
assert run("1 1 1\n") == "10", "minimum case"

# impossible first extension
assert run("1 11 1\n") == "-1", "no valid digit"

# n = 1, exactly one append
assert run("12 3 1\n") == "120", "single extension"

# divisor requiring nonzero first digit
assert run("5 7 2\n") == "560", "first digit 6 gives divisibility"

# large n shape check
out = run("1 1 100000\n")
assert len(out) == 100001, "large output length"
assert out[0] == "1", "starts correctly"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `10` | Smallest legal input |
| `1 11 1` | `-1` | No valid first extension |
| `12 3 1` | `120` | Exactly one extension |
| `5 7 2` | `560` | Nonzero first digit needed |
| `1 1 100000` | Length 100001 | Maximum-size output |

## Edge Cases

### No valid first digit

Input:

```
1 11 1
```

The remainder is:

```
1 % 11 = 1
```

The algorithm checks all digits:

```
(10 + d) % 11
```

for `d = 0..9`.

None produces zero. Since the first operation cannot be performed, the algorithm immediately outputs:

```
-1
```

which matches the definition of the process.

### Only one extension required

Input:

```
12 3 1
```

The remainder is zero.

Digit `0` immediately satisfies:

```
(0 * 10 + 0) % 3 = 0
```

The answer becomes:

```
120
```

No extra zeros are appended because `n - 1 = 0`.

### Very large n

Input:

```
1 1 100000
```

The first valid digit is `0`.

The algorithm constructs:

```
10 + 99999 zeros
```

without performing any expensive arithmetic on the huge number. The running time grows linearly with the output size, which is optimal because the output itself contains 100001 digits.

### Valid first digit is not zero

Input:

```
5 7 2
```

The remainder is:

```
5
```

The algorithm tests digits until:

```
(5 * 10 + 6) % 7 = 56 % 7 = 0
```

It chooses digit `6`, producing `56`. One additional zero is appended, giving:

```
560
```

Every intermediate number satisfies the divisibility requirement, so the construction is valid.
