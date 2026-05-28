---
title: "CF 66A - Petya and Java"
description: "We are given a decimal integer as a string. The number can be extremely large, up to 100 digits long, so it may not fit into normal integer types in many programming languages. The task is to determine the smallest Java integer type that can store this value."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 66
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 61 (Div. 2)"
rating: 1300
weight: 66
solve_time_s: 93
verified: true
draft: false
---

[CF 66A - Petya and Java](https://codeforces.com/problemset/problem/66/A)

**Rating:** 1300  
**Tags:** implementation, strings  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a decimal integer as a string. The number can be extremely large, up to 100 digits long, so it may not fit into normal integer types in many programming languages.

The task is to determine the smallest Java integer type that can store this value. The available types are checked in this order: `byte`, `short`, `int`, `long`, and finally `BigInteger`. Each primitive type has a fixed inclusive range. We must print the first type whose range contains the given number.

The main difficulty comes from the input size. A 100-digit integer is far larger than a 64-bit signed integer, so directly converting the input into a normal numeric type is dangerous in languages with fixed-width integers. A careless implementation could overflow before the comparison even happens.

The constraints are tiny in terms of input size. We only process one string of length at most 100, so even linear-time work is trivial. The problem is not about optimization, it is about safe comparison and handling boundary values correctly.

Several edge cases can silently break incorrect solutions.

Consider the input:

```
128
```

The correct answer is:

```
short
```

`byte` ends at `127`, and the boundaries are inclusive. A strict `<` comparison instead of `<=` would reject `127` incorrectly or accept `128` incorrectly.

Another dangerous case is:

```
9223372036854775808
```

The correct answer is:

```
BigInteger
```

This value is exactly one greater than the maximum signed 64-bit integer. In C++ or Java, attempting to parse this directly into a `long long` or `long` would overflow. The safer approach is either arbitrary-precision arithmetic or direct string comparison.

A smaller but subtle example is:

```
2147483647
```

The correct answer is:

```
int
```

This is the exact upper bound of `int`, so the algorithm must treat the limits as inclusive.

## Approaches

A brute-force approach would try to parse the number into increasingly larger numeric types and catch failures. In Python this works because Python integers are arbitrary precision, but in languages with fixed-width integers this becomes risky. Parsing a 100-digit value into a normal integer type may overflow before we even compare it.

Another brute-force style solution is to compare the input string against every possible integer in each range, but that is obviously infeasible. Even the `long` range contains more than $10^{18}$ values.

The useful observation is that we only need to compare the input against four fixed boundary values:

- 127
- 32767
- 2147483647
- 9223372036854775807

If the number is less than or equal to one of these limits, then that type can store it.

Because Python supports arbitrary-precision integers naturally, the simplest accepted solution is to convert the string into an integer once, then compare against the known limits in order. The input length is only 100 digits, so parsing is cheap.

The algorithm becomes a sequence of comparisons from the smallest type upward. The first matching range gives the answer immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated parsing / unsafe fixed-width conversion | O(L) | O(1) | Risky in many languages |
| Sequential comparison against limits | O(L) | O(1) | Accepted |

Here, $L$ is the number of digits in the input.

## Algorithm Walkthrough

1. Read the input number as a string.
2. Convert the string into a Python integer.

Python integers have arbitrary precision, so even a 100-digit value is handled safely.
3. Compare the value against the `byte` upper bound `127`.

If the value is at most `127`, print `"byte"` and stop.
4. Otherwise compare against the `short` upper bound `32767`.

If the value fits here, print `"short"`.
5. Otherwise compare against the `int` upper bound `2147483647`.

If the value fits here, print `"int"`.
6. Otherwise compare against the `long` upper bound `9223372036854775807`.

If the value fits here, print `"long"`.
7. If none of the previous ranges worked, print `"BigInteger"`.

### Why it works

The integer types are ordered by increasing capacity. If a number fits inside `byte`, that is automatically the smallest valid type because every earlier type is smaller. The same logic applies to `short`, `int`, and `long`.

The algorithm checks the limits in exactly this order. The first successful comparison identifies the smallest valid type, so the answer is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

if n <= 127:
    print("byte")
elif n <= 32767:
    print("short")
elif n <= 2147483647:
    print("int")
elif n <= 9223372036854775807:
    print("long")
else:
    print("BigInteger")
```

The program first reads the input and converts it into a Python integer. This is safe because Python integers do not overflow for large values.

The comparisons are ordered from the smallest type to the largest primitive type. That ordering matters. If we checked `long` first, then every smaller value would also match `long`, and we would lose the requirement to return the smallest fitting type.

The comparisons use `<=` because the ranges are inclusive. Values like `127` and `2147483647` must still belong to `byte` and `int` respectively.

The final `else` handles every number larger than the maximum signed 64-bit integer. Those values require `BigInteger`.

## Worked Examples

### Example 1

Input:

```
127
```

| Step | Condition Checked | Result |
| --- | --- | --- |
| 1 | `127 <= 127` | True |
| 2 | Print `"byte"` | Done |

The first condition already succeeds, so the algorithm immediately returns the smallest valid type.

### Example 2

Input:

```
2147483648
```

| Step | Condition Checked | Result |
| --- | --- | --- |
| 1 | `2147483648 <= 127` | False |
| 2 | `2147483648 <= 32767` | False |
| 3 | `2147483648 <= 2147483647` | False |
| 4 | `2147483648 <= 9223372036854775807` | True |
| 5 | Print `"long"` | Done |

This trace shows why boundary handling matters. The value is exactly one greater than the maximum `int`, so it must move to the next type.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L) | Parsing the input integer takes linear time in the number of digits |
| Space | O(1) | Only a few variables are stored |

The input length is at most 100 digits, so even linear processing is tiny. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input().strip())

    if n <= 127:
        print("byte")
    elif n <= 32767:
        print("short")
    elif n <= 2147483647:
        print("int")
    elif n <= 9223372036854775807:
        print("long")
    else:
        print("BigInteger")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("127\n") == "byte\n", "sample 1"

# boundary cases
assert run("128\n") == "short\n", "byte to short boundary"
assert run("32767\n") == "short\n", "maximum short"
assert run("32768\n") == "int\n", "short to int boundary"

# large boundaries
assert run("2147483647\n") == "int\n", "maximum int"
assert run("2147483648\n") == "long\n", "int to long boundary"

# beyond long
assert run("9223372036854775808\n") == "BigInteger\n", "requires BigInteger"

# minimum positive input
assert run("1\n") == "byte\n", "smallest valid input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `128` | `short` | Correct transition after byte limit |
| `32767` | `short` | Inclusive upper boundary |
| `32768` | `int` | Next type selection |
| `2147483648` | `long` | Crossing int boundary |
| `9223372036854775808` | `BigInteger` | Larger than signed 64-bit range |
| `1` | `byte` | Smallest positive input |

## Edge Cases

Consider the input:

```
127
```

The algorithm checks:

```
127 <= 127
```

This is true, so it prints:

```
byte
```

This confirms that the boundaries are inclusive. Using a strict `<` comparison would incorrectly reject this value.

Now consider:

```
128
```

The first comparison fails:

```
128 <= 127
```

The next comparison succeeds:

```
128 <= 32767
```

So the output becomes:

```
short
```

This verifies the transition between adjacent integer types.

A more dangerous case is:

```
9223372036854775808
```

The comparisons proceed until the `long` check:

```
9223372036854775808 <= 9223372036854775807
```

This is false, so the algorithm falls into the final branch and prints:

```
BigInteger
```

This case catches implementations that rely on fixed-width integer parsing and accidentally overflow before comparing.
