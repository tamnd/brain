---
title: "CF 61A - Ultra-Fast Mathematician"
description: "We are given two binary strings of equal length. Each character is either '0' or '1'. For every position, we compare the characters from the two strings. If the two characters are different, the resulting string gets '1' at that position."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 61
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 57 (Div. 2)"
rating: 800
weight: 61
solve_time_s: 124
verified: true
draft: false
---

[CF 61A - Ultra-Fast Mathematician](https://codeforces.com/problemset/problem/61/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two binary strings of equal length. Each character is either `'0'` or `'1'`. For every position, we compare the characters from the two strings.

If the two characters are different, the resulting string gets `'1'` at that position. If they are the same, the resulting string gets `'0'`.

This operation is exactly the binary XOR operation applied digit by digit.

For example, if one string has `'1'` and the other has `'0'`, the output becomes `'1'`. If both are `'1'` or both are `'0'`, the output becomes `'0'`.

The strings are at most length 100, which is extremely small. Even a simple linear scan over the strings is easily fast enough. Any algorithm with time complexity proportional to the string length will finish instantly within the limits.

The main danger in this problem is not performance but correctness. Small implementation mistakes can silently produce the wrong binary string.

One easy mistake is forgetting to preserve leading zeros. Consider:

```
Input:
001
001
```

The correct output is:

```
000
```

If someone converts the strings to integers and back, they may accidentally print just `0`, which is wrong because the problem requires keeping all positions.

Another common mistake is misunderstanding the operation as binary addition instead of XOR. For example:

```
Input:
1
1
```

Correct output:

```
0
```

A careless implementation using addition modulo 2 incorrectly or handling carry bits could produce the wrong result.

A third subtle case is alternating patterns where every comparison changes:

```
Input:
1010
0101
```

Correct output:

```
1111
```

This checks whether the implementation compares each position independently instead of trying to interpret the strings as full binary numbers.

## Approaches

The most direct approach is to process the strings character by character. For every index, compare the two characters. If they are different, append `'1'` to the answer. Otherwise append `'0'`.

This already solves the problem efficiently because the maximum length is only 100. Even if we did several passes over the strings, the runtime would still be tiny.

A more naive version would repeatedly build the answer using string concatenation:

```
ans += '1'
```

inside the loop. In Python, repeated string concatenation can become inefficient for very large inputs because strings are immutable. Every concatenation creates a new string. For length 100 this still works perfectly fine, but in larger problems this pattern can become quadratic.

The cleaner approach is to collect characters in a list and join them once at the end. The key observation is that every output digit depends only on the corresponding pair of input digits. No position affects any other position. That means we never need carries, preprocessing, or advanced data structures.

The entire task reduces to a simple linear comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force string concatenation | O(n²) in theory | O(n) | Accepted |
| Optimal character-by-character build | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the two binary strings.

Both strings are guaranteed to have the same length, so we can safely process them index by index.
2. Create an empty list to store the answer characters.

Using a list avoids repeated string reallocations during construction.
3. Iterate through every position from `0` to `n - 1`.

Each position is independent from the others.
4. Compare the characters at the current index.

If the characters differ, append `'1'` to the answer list. Otherwise append `'0'`.

This directly matches the XOR definition from the problem.
5. Join all collected characters into one string.

The final string preserves every position, including leading zeros.
6. Print the result.

### Why it works

For every index `i`, the problem defines the answer digit entirely from the pair `(a[i], b[i])`.

The algorithm applies exactly this rule independently at every position:

- equal digits produce `'0'`
- different digits produce `'1'`

Since every position is processed correctly and independently, the complete resulting string is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = input().strip()
b = input().strip()

ans = []

for x, y in zip(a, b):
    if x != y:
        ans.append('1')
    else:
        ans.append('0')

print(''.join(ans))
```

The first two lines read the binary strings and remove trailing newline characters with `strip()`.

The answer is stored in a list because appending to a list is efficient. After processing all positions, `''.join(ans)` creates the final string in one operation.

The loop uses `zip(a, b)` to iterate through matching positions from both strings simultaneously. Since the problem guarantees equal lengths, every character pair aligns correctly.

The comparison `x != y` exactly matches the XOR condition from the statement. No integer conversion is necessary, which avoids mistakes involving leading zeros or binary arithmetic.

## Worked Examples

### Example 1

Input:

```
1010100
0100101
```

| Position | First String | Second String | Different? | Output Digit |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | Yes | 1 |
| 1 | 0 | 1 | Yes | 1 |
| 2 | 1 | 0 | Yes | 1 |
| 3 | 0 | 0 | No | 0 |
| 4 | 1 | 1 | No | 0 |
| 5 | 0 | 0 | No | 0 |
| 6 | 0 | 1 | Yes | 1 |

Final output:

```
1110001
```

This trace shows that each position is processed independently. Matching digits become `0`, differing digits become `1`.

### Example 2

Input:

```
1111
1111
```

| Position | First String | Second String | Different? | Output Digit |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | No | 0 |
| 1 | 1 | 1 | No | 0 |
| 2 | 1 | 1 | No | 0 |
| 3 | 1 | 1 | No | 0 |

Final output:

```
0000
```

This example confirms that leading zeros in the result must be preserved. The answer is not a single `0`, it is a four-character string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(n) | The answer string stores `n` characters |

The maximum length is only 100, so the algorithm runs comfortably within the limits. Both runtime and memory usage are tiny.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    a = input().strip()
    b = input().strip()

    ans = []

    for x, y in zip(a, b):
        if x != y:
            ans.append('1')
        else:
            ans.append('0')

    print(''.join(ans))

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
assert run("1010100\n0100101\n") == "1110001\n", "sample 1"

# minimum size
assert run("0\n0\n") == "0\n", "single equal digits"

# minimum size different
assert run("1\n0\n") == "1\n", "single different digits"

# all equal values
assert run("11111\n11111\n") == "00000\n", "all positions equal"

# alternating pattern
assert run("1010\n0101\n") == "1111\n", "every position differs"

# leading zeros preserved
assert run("0011\n0011\n") == "0000\n", "leading zeros must remain"

# maximum-style repeated pattern
a = "01" * 50
b = "10" * 50
expected = "11" * 50 + "\n"
assert run(f"{a}\n{b}\n") == expected, "length 100 case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 / 0` | `0` | Smallest possible input |
| `1 / 0` | `1` | Different single digits |
| `11111 / 11111` | `00000` | Equal strings |
| `1010 / 0101` | `1111` | Every position differs |
| `0011 / 0011` | `0000` | Leading zeros preserved |
| Length 100 alternating strings | All `1`s | Maximum constraint behavior |

## Edge Cases

Consider the case where both strings are identical and begin with zeros:

```
Input:
001
001
```

The algorithm compares each pair of digits:

- `0` vs `0` → `0`
- `0` vs `0` → `0`
- `1` vs `1` → `0`

The produced answer is:

```
000
```

Because the solution works directly with strings instead of integers, the leading zeros remain intact.

Now consider the smallest possible differing input:

```
Input:
1
0
```

The algorithm processes the only position:

- `1` vs `0` → `1`

Output:

```
1
```

This confirms the XOR rule is implemented correctly.

Finally, consider a case where every position differs:

```
Input:
1010
0101
```

Step-by-step comparisons:

- `1` vs `0` → `1`
- `0` vs `1` → `1`
- `1` vs `0` → `1`
- `0` vs `1` → `1`

Output:

```
1111
```

This verifies that the algorithm treats positions independently instead of performing binary arithmetic with carries.
