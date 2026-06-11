---
title: "CF 1326A - Bad Ugly Numbers"
description: "We need to construct a positive decimal number with exactly n digits. Every digit must be nonzero, and the whole number must fail divisibility by each digit that appears in it. For each test case, the input gives only the required length n."
date: "2026-06-11T16:34:05+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1326
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 7"
rating: 1000
weight: 1326
solve_time_s: 175
verified: false
draft: false
---

[CF 1326A - Bad Ugly Numbers](https://codeforces.com/problemset/problem/1326/A)

**Rating:** 1000  
**Tags:** constructive algorithms, number theory  
**Solve time:** 2m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct a positive decimal number with exactly `n` digits. Every digit must be nonzero, and the whole number must fail divisibility by each digit that appears in it.

For each test case, the input gives only the required length `n`. We may output any valid number of that length. If no such number exists, we print `-1`.

The constraints immediately suggest that we are not expected to search through candidate numbers. A single test case may require producing a number with up to `10^5` digits, and the sum of all lengths is also up to `10^5`. Any algorithm that examines many candidates or performs expensive arithmetic on huge integers would be unnecessary. The intended solution must construct the answer directly in time proportional to the output size.

The first non-obvious edge case is `n = 1`.

Input:

```
1
1
```

Output:

```
-1
```

A one-digit positive number is always divisible by itself. Since the only digit in the number equals the number, no valid answer exists.

Another easy mistake is constructing a number consisting entirely of `9`s.

Input:

```
1
3
```

Candidate:

```
999
```

This fails because `999` is divisible by `9`. Having no zero digits is not enough.

A third mistake is forgetting that divisibility must fail for every digit present. For example:

```
444
```

is divisible by `4`, so it is invalid even though all digits are nonzero.

The challenge is not checking divisibility efficiently. The challenge is finding a pattern that is guaranteed to work for every length greater than one.

## Approaches

A brute-force strategy would generate `n`-digit numbers and test whether each candidate satisfies the condition. Testing one candidate is easy: inspect its digits and check divisibility by each digit. The problem is the search space. There are `9^n` numbers with `n` nonzero digits. Even for `n = 20`, this is already astronomically large. For `n = 100000`, exhaustive search is completely impossible.

The key observation is that we only need one valid answer, not all of them.

Suppose we construct a number containing only the digits `2` and `3`. If the number is odd, then it cannot be divisible by `2`. If the sum of its digits is not a multiple of `3`, then it cannot be divisible by `3`. Since those are the only digits appearing in the number, both requirements would be satisfied.

A very simple pattern achieves exactly this:

```
2333...333
```

The first digit is `2`, and the remaining `n - 1` digits are `3`.

Let us verify it.

The last digit is `3`, so the number is odd and cannot be divisible by `2`.

The digit sum equals

$$2 + 3(n-1)=3n-1.$$

Since `3n - 1` leaves remainder `2` when divided by `3`, the number is not divisible by `3`.

The only digits present are `2` and `3`, so the number is not divisible by any of its digits.

This construction works for every `n > 1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(9^n · n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`.
2. If `n = 1`, print `-1`.

A one-digit positive number is always divisible by its only digit, so no solution exists.
3. Otherwise, output the string consisting of one `'2'` followed by `n - 1` copies of `'3'`.

This gives an `n`-digit number containing only the digits `2` and `3`.

### Why it works

For every `n > 1`, the constructed number ends with digit `3`, so it is odd. Any number divisible by `2` must be even, hence the number is not divisible by `2`.

The digit sum is

$$2 + 3(n-1)=3n-1.$$

This value is not divisible by `3`, so the number itself is not divisible by `3`.

The only digits appearing in the number are `2` and `3`. We have shown that the number is divisible by neither of them. Consequently, it is not divisible by any digit appearing in its decimal representation.

For `n = 1`, no valid number exists, so printing `-1` is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())

        if n == 1:
            ans.append("-1")
        else:
            ans.append("2" + "3" * (n - 1))

    sys.stdout.write("\n".join(ans))

solve()
```

The program processes each test case independently.

The special case `n == 1` must be handled first. Forgetting this case would produce `"2"`, which is invalid because `2` is divisible by `2`.

For all larger lengths, the expression `"2" + "3" * (n - 1)` directly builds the required string. Working with strings is preferable to constructing a huge integer because `n` can reach `100000`. The problem only asks us to print the number, not perform arithmetic on it.

The output is accumulated in a list and printed once at the end. This avoids repeated output operations and matches standard competitive-programming practice.

## Worked Examples

### Example 1

Input:

```
n = 1
```

| Step | n | Action | Output |
| --- | --- | --- | --- |
| 1 | 1 | Check special case | `-1` |

The example demonstrates the only impossible situation. Any one-digit positive number equals its only digit and is divisible by it.

### Example 2

Input:

```
n = 4
```

| Step | n | Action | Current Result |
| --- | --- | --- | --- |
| 1 | 4 | `n != 1` | Continue |
| 2 | 4 | Build `"2" + "3" * 3` | `2333` |
| 3 | 4 | Print answer | `2333` |

Verification:

| Property | Value |
| --- | --- |
| Digits present | 2, 3 |
| Last digit | 3 |
| Divisible by 2? | No |
| Digit sum | 11 |
| Divisible by 3? | No |

This trace confirms the invariant behind the construction. The number is neither divisible by `2` nor by `3`, which covers every digit appearing in it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Constructing the output string requires writing `n` characters |
| Space | O(n) | The generated answer itself contains `n` characters |

The total length of all printed numbers is at most `10^5`, so linear work in the output size is easily within the limits. Memory usage is also proportional to the generated output and comfortably fits within 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)

    def input():
        return input_data.readline()

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())

        if n == 1:
            ans.append("-1")
        else:
            ans.append("2" + "3" * (n - 1))

    return "\n".join(ans)

# provided sample
assert run("4\n1\n2\n3\n4\n") == "-1\n23\n233\n2333"

# custom cases
assert run("1\n1\n") == "-1", "minimum length"

assert run("1\n2\n") == "23", "smallest valid length"

assert run("1\n5\n") == "23333", "general construction"

assert run("1\n10\n") == "2" + "3" * 9, "larger construction"

assert len(run("1\n100000\n")) == 100000, "maximum length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n` | `-1` | Impossible single-digit case |
| `1\n2\n` | `23` | Smallest valid construction |
| `1\n5\n` | `23333` | General correctness |
| `1\n10\n` | `2333333333` | Longer output generation |
| `1\n100000\n` | Length `100000` string | Maximum constraint |

## Edge Cases

Consider the input:

```
1
1
```

The algorithm immediately enters the special branch and prints `-1`. This is correct because every one-digit positive integer is divisible by itself. No construction can satisfy the requirement.

Consider the input:

```
1
2
```

The algorithm outputs `23`. The number is odd, so it is not divisible by `2`. Its digit sum is `5`, so it is not divisible by `3`. Since the only digits present are `2` and `3`, the answer is valid.

Consider the input:

```
1
100000
```

The algorithm constructs one `'2'` followed by `99999` copies of `'3'`. No arithmetic on huge integers is performed. The output has exactly `100000` digits, remains odd, and has digit sum

$$2 + 3 \cdot 99999 = 299999,$$

which is not divisible by `3`. The same proof used for small values applies unchanged to the maximum input size.
