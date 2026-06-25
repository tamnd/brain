---
title: "CF 106113E - Una extra\u00f1a sucesi\u00f3n"
description: "The teacher builds an \"infinite alphabet\" by repeating the letters a through z forever. Each block of 26 letters is prefixed by how many complete alphabet cycles came before it. The first few values are: 0a, 0b, ..., 0z, 1a, 1b, ..., 1z, 2a, ..."
date: "2026-06-25T11:38:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106113
codeforces_index: "E"
codeforces_contest_name: "Coding Cup TecNM 2025"
rating: 0
weight: 106113
solve_time_s: 43
verified: true
draft: false
---

[CF 106113E - Una extra\u00f1a sucesi\u00f3n](https://codeforces.com/problemset/problem/106113/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The teacher builds an "infinite alphabet" by repeating the letters `a` through `z` forever. Each block of 26 letters is prefixed by how many complete alphabet cycles came before it.

The first few values are:

`0a, 0b, ..., 0z, 1a, 1b, ..., 1z, 2a, ...`

If we number these positions starting from 1, then:

`0a` is at position 1, `0b` at position 2, ..., `0z` at position 26, `1a` at position 27, and so on.

The sequence `s` is obtained by taking the numeric sequence

$$5,\ 8,\ 13,\ 20,\ 29,\dots$$

and replacing each number by the value stored at that position in the infinite alphabet. The statement gives the beginning of `s`:

`0e, 0h, 0m, 0t, 1c, ...`

The task is the reverse operation. Given one value of the infinite alphabet, determine at which position of `s` it appears. If it never appears, print `-1`.

The key observation comes from converting the shown values of `s` back into their alphabet positions:

| Value | Alphabet position |
| --- | --- |
| 0e | 5 |
| 0h | 8 |
| 0m | 13 |
| 0t | 20 |
| 1c | 29 |

The differences are:

$$3,\ 5,\ 7,\ 9,\dots$$

which are consecutive odd numbers. That means the underlying numeric sequence is

$$n^2 + 4$$

for $n = 1, 2, 3, \dots$.

The input size is tiny. The numeric prefix can be as large as $10^8$, so the resulting alphabet position is at most about $2.6 \times 10^9$. A constant-time arithmetic solution is more than enough.

A common mistake is forgetting that alphabet positions are 1-indexed.

For example:

```
Input:
0a
```

The alphabet position is 1, not 0. Since

$$1 - 4 = -3$$

is not a perfect square, the correct answer is:

```
-1
```

Another easy mistake is accepting any square root after floating-point rounding.

For example:

```
Input:
0d
```

The alphabet position is 4. Then:

$$4 - 4 = 0$$

which gives square root 0. The sequence starts at $n=1$, so position 0 does not exist. The correct answer is:

```
-1
```

This is one of the sample cases.

## Approaches

A brute-force solution would generate values of the sequence

$$n^2 + 4$$

convert each value into its infinite-alphabet representation, and compare it against the input. This works because the sequence is explicit.

The problem is deciding how far to generate. The alphabet position represented by the input can be larger than two billion, so the corresponding sequence index can be around fifty thousand. That is still not huge, but generating and converting values is unnecessary work.

The real structure becomes visible once we translate the input back into its numeric alphabet position.

If the input is `pX`, where `X` is a letter, then its alphabet position is

$$N = 26p + \text{letterIndex}(X)$$

with `a = 1`, `b = 2`, ..., `z = 26`.

The sequence contains exactly the numbers

$$n^2 + 4.$$

So the question becomes:

$$n^2 + 4 = N$$

or

$$n^2 = N - 4.$$

Now we only need to check whether $N-4$ is a positive perfect square. If it is, that square root is precisely the position inside the sequence. Otherwise the value never appears.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O($\sqrt N$) | O(1) | Unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Separate the numeric prefix and the final letter.
3. Convert the letter into its position inside the alphabet, where `a = 1` and `z = 26`.
4. Compute the infinite-alphabet position:

$$N = 26 \cdot prefix + letterPosition$$

This follows directly from the construction of the infinite alphabet.

1. Compute:

$$x = N - 4$$

because every element of the hidden numeric sequence has the form $n^2 + 4$.

1. If $x \le 0$, print `-1`.

The sequence starts at $n=1$, so $n=0$ is not valid.

1. Compute the integer square root $r = \lfloor \sqrt{x} \rfloor$.
2. If $r^2 = x$, print $r$. Otherwise print `-1`.

### Why it works

Every value of `s` comes from the numeric sequence $n^2 + 4$. A string from the infinite alphabet corresponds to exactly one alphabet position $N$. The string appears in `s` if and only if its position satisfies

$$N = n^2 + 4$$

for some positive integer $n$.

Rearranging gives

$$n^2 = N - 4.$$

A positive integer $n$ exists exactly when $N-4$ is a positive perfect square. In that case the unique square root is the sequence position. No other answer is possible.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

s = input().strip()

letter = s[-1]
prefix = int(s[:-1])

pos = 26 * prefix + (ord(letter) - ord('a') + 1)

x = pos - 4

if x <= 0:
    print(-1)
else:
    r = isqrt(x)
    print(r if r * r == x else -1)
```

The first part extracts the numeric prefix and the final letter.

The conversion to an alphabet position uses the fact that each completed block contributes 26 positions. The letter contributes a value between 1 and 26.

After obtaining `pos`, the problem reduces to checking whether `pos - 4` is a positive perfect square.

Using `math.isqrt` avoids floating-point precision issues. A floating-point square root could incorrectly classify very large values near a perfect square. The integer square root gives an exact result, and the final check `r * r == x` confirms perfect-square status.

The condition `x <= 0` is important. For example, `0d` produces `x = 0`, but the sequence starts from $n=1$, so the answer must be `-1`.

## Worked Examples

### Example 1

Input:

```
3z
```

| Variable | Value |
| --- | --- |
| prefix | 3 |
| letter | z |
| letterPosition | 26 |
| N | 104 |
| x = N - 4 | 100 |
| r | 10 |

Since $10^2 = 100$, the answer is:

```
10
```

This matches the sample.

### Example 2

Input:

```
104d
```

| Variable | Value |
| --- | --- |
| prefix | 104 |
| letter | d |
| letterPosition | 4 |
| N | 2708 |
| x = N - 4 | 2704 |
| r | 52 |

Since $52^2 = 2704$, the answer is:

```
52
```

This demonstrates that even large prefixes reduce to a simple perfect-square test.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | A few arithmetic operations and one integer square root |
| Space | O(1) | Only a handful of variables are stored |

The largest possible alphabet position is only a few billion, so all calculations fit comfortably in standard integer types. The constant-time solution easily satisfies the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys
from math import isqrt

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    s = sys.stdin.readline().strip()

    letter = s[-1]
    prefix = int(s[:-1])

    pos = 26 * prefix + (ord(letter) - ord('a') + 1)

    x = pos - 4

    if x <= 0:
        return "-1\n"

    r = isqrt(x)
    return f"{r if r * r == x else -1}\n"

# provided samples
assert run("0e\n") == "1\n", "sample 1"
assert run("3z\n") == "10\n", "sample 2"
assert run("104d\n") == "52\n", "sample 3"
assert run("0d\n") == "-1\n", "sample 4"

# custom cases
assert run("0a\n") == "-1\n", "smallest alphabet value"
assert run("0h\n") == "2\n", "second sequence element"
assert run("1c\n") == "5\n", "crossing alphabet block boundary"
assert run("99999999z\n") == "-1\n", "large non-member"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0a` | `-1` | Smallest possible alphabet position |
| `0h` | `2` | Basic perfect-square detection |
| `1c` | `5` | Correct handling across 26-letter blocks |
| `99999999z` | `-1` | Large-value arithmetic and square checking |

## Edge Cases

Consider:

```
0a
```

The alphabet position is:

$$1$$

Then:

$$1 - 4 = -3$$

Since the value is negative, there is no positive integer $n$ satisfying $n^2=-3$. The algorithm immediately prints `-1`.

Now consider:

```
0d
```

The alphabet position is:

$$4$$

Then:

$$4 - 4 = 0$$

The square root is 0, but the sequence starts with $n=1$. The algorithm rejects `x <= 0` and correctly prints:

```
-1
```

Finally, consider:

```
1c
```

The alphabet position is:

$$26 + 3 = 29$$

Then:

$$29 - 4 = 25 = 5^2$$

The algorithm finds the exact square root 5 and outputs:

```
5
```

This confirms that the block number and the letter contribution are combined correctly when converting back to the numeric alphabet position.
