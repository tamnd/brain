---
title: "CF 106367A - The World Is Full of Colors"
description: "We are given a sequence of RGB colors written in the standard hexadecimal web format, where each color starts with followed by six lowercase hexadecimal characters."
date: "2026-06-19T08:25:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106367
codeforces_index: "A"
codeforces_contest_name: "Whalica Cup (Round 2)"
rating: 0
weight: 106367
solve_time_s: 44
verified: true
draft: false
---

[CF 106367A - The World Is Full of Colors](https://codeforces.com/problemset/problem/106367/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of RGB colors written in the standard hexadecimal web format, where each color starts with `#` followed by six lowercase hexadecimal characters. These six characters encode three integers: red, green, and blue, each in the range from 0 to 255, stored as two hex digits per channel.

For every input color, we must construct its complementary color. Two colors are complementary when each corresponding RGB component sums to 255. In other words, if the original color has components `(R, G, B)`, the output color must be `(255 − R, 255 − G, 255 − B)`, then converted back into a properly formatted hexadecimal string with lowercase letters and leading zeros if needed.

The input size is large in terms of test cases, up to 10^4. Each test case is processed independently, and each operation is constant time per color. This rules out anything quadratic or involving repeated string scanning beyond O(1) per test case. A direct per-character transformation is sufficient.

A subtle failure case comes from formatting. Each RGB component must always be represented using exactly two hexadecimal digits. If this is ignored, values like 0 become `0` instead of `00`, which breaks the required fixed-length format.

For example, if input is `#000000`, the correct output is `#ffffff`. A naive implementation that forgets padding might produce `#fff`, which is invalid under the specification.

Another edge detail is case sensitivity. Output must be lowercase hexadecimal. Using uppercase like `#E0E1CC` would be rejected even though numerically correct.

## Approaches

A brute-force interpretation would be to convert each hex digit string into an integer color value by manually parsing each character, then compute 255 minus each channel, and finally rebuild the string by repeatedly converting integers back to hex. This is already O(1) per test case, but if implemented inefficiently, for example by repeatedly concatenating strings or using slow manual base conversion, it could degrade in practice due to repeated character operations across up to 10^4 inputs.

The key observation is that each channel is independent and always bounded in [0, 255], so Python’s built-in integer parsing and formatting functions are sufficient and optimal. We only need to extract fixed substrings, convert them once, subtract from 255, and format back using two-digit hexadecimal formatting. This avoids manual digit-by-digit processing entirely.

The structure of the input guarantees constant-size strings, so the optimal solution is simply a direct transformation per test case with no auxiliary data structures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Manual brute parsing + reconstruction | O(t) | O(1) | Accepted |
| Direct slicing + int conversion + formatting | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the color string `s`. It always has the form `#RRGGBB`. This fixed structure allows direct slicing without scanning.
2. Extract the red component using `s[1:3]`, green using `s[3:5]`, and blue using `s[5:7]`. Each substring is exactly two hex characters, which guarantees valid parsing.
3. Convert each substring from hexadecimal to integer using base-16 conversion. This gives `(R, G, B)` in numeric form.
4. Compute the complement for each channel by subtracting from 255, producing `(255 − R, 255 − G, 255 − B)`. This step is independent per channel, reflecting the problem’s definition of complementarity.
5. Convert each resulting integer back into a two-character lowercase hexadecimal string. If the value is less than 16, a leading zero must be included. This fixed-width formatting preserves the required RGB encoding.
6. Concatenate the results in order and prepend `#` to form the final output string.

### Why it works

Each RGB component is encoded independently in a fixed 8-bit range. The transformation `x → 255 − x` is an involution on this domain, meaning applying it twice returns the original value. Since hexadecimal representation is a bijection between `[0, 255]` and `00` to `ff`, converting to integers, transforming, and formatting back preserves correctness exactly. No cross-component interaction exists, so processing channels independently cannot introduce inconsistencies.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        s = input().strip()

        r = int(s[1:3], 16)
        g = int(s[3:5], 16)
        b = int(s[5:7], 16)

        cr = 255 - r
        cg = 255 - g
        cb = 255 - b

        out.append("#" + format(cr, "02x") + format(cg, "02x") + format(cb, "02x"))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution relies on fixed slicing positions, which avoids any per-character loop overhead. Each `int(..., 16)` call handles conversion safely even for leading zeros. The `format(x, "02x")` ensures both lowercase output and mandatory zero-padding.

A common implementation mistake is using `hex(x)` directly, which produces strings like `0xa` instead of `0a`. That would break formatting unless manually post-processed. Another subtle issue is forgetting `.strip()` on input lines, which could leave newline characters interfering with slicing.

## Worked Examples

We trace two inputs.

### Example 1: `#1f1e33`

| Step | R | G | B | Result R | Result G | Result B | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Parse hex | 31 | 30 | 51 | - | - | - | - |
| Complement | - | - | - | 224 | 225 | 204 | - |
| Format | - | - | - | e0 | e1 | cc | `#e0e1cc` |

This shows correct independent channel inversion and proper hex formatting.

### Example 2: `#0000ff`

| Step | R | G | B | Result R | Result G | Result B | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Parse hex | 0 | 0 | 255 | - | - | - | - |
| Complement | - | - | - | 255 | 255 | 0 | - |
| Format | - | - | - | ff | ff | 00 | `#ffff00` |

This example stresses boundary values, ensuring zero-padding is handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case processes constant-size string operations and arithmetic |
| Space | O(1) | Only a fixed number of variables per test case, output stored linearly |

The constraints allow up to 10^4 test cases, and each is handled with constant-time slicing and conversion, keeping total runtime comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()

    def solve():
        t = int(sys.stdin.readline())
        res = []
        for _ in range(t):
            s = sys.stdin.readline().strip()
            r = int(s[1:3], 16)
            g = int(s[3:5], 16)
            b = int(s[5:7], 16)
            res.append("#" + format(255-r, "02x") + format(255-g, "02x") + format(255-b, "02x"))
        print("\n".join(res))

    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("2\n#1f1e33\n#114514") == "#e0e1cc\n#eebaeb"

# minimum value edge
assert run("1\n#000000") == "#ffffff"

# maximum value edge
assert run("1\n#ffffff") == "#000000"

# mixed boundary
assert run("1\n#0f10f0") == "#f0ef0f"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| #000000 | #ffffff | all-zero boundary inversion |
| #ffffff | #000000 | max-value inversion |
| #0f10f0 | #f0ef0f | mixed small/large channel correctness |

## Edge Cases

The all-zero color `#000000` demonstrates correct handling of leading-zero hex parsing and formatting. Each channel becomes 255, which must be printed as `ff`, confirming that no padding logic is missing.

The all-white color `#ffffff` checks the opposite extreme. Each channel becomes 0, which must appear as `00`. A naive formatter that drops leading zeros would incorrectly output `#0`, but fixed-width formatting ensures correctness.

A mixed-value case like `#0f10f0` ensures that independent channel processing does not interfere across components. Each byte is inverted separately, preserving alignment between RGB positions and preventing accidental reordering or shared computation errors.
