---
title: "CF 75A - Life Without Zeros"
description: "We are given two positive integers, a and b. First we compute their normal sum c = a + b. Then we apply the same transformation to all three numbers: remove every digit 0 from their decimal representation. The question is whether the transformed equation still holds."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 75
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 67 (Div. 2)"
rating: 1000
weight: 75
solve_time_s: 94
verified: true
draft: false
---

[CF 75A - Life Without Zeros](https://codeforces.com/problemset/problem/75/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two positive integers, `a` and `b`. First we compute their normal sum `c = a + b`. Then we apply the same transformation to all three numbers: remove every digit `0` from their decimal representation.

The question is whether the transformed equation still holds. In other words, after deleting all zeros from `a`, `b`, and `c`, do we still have:

`remove_zero(a) + remove_zero(b) = remove_zero(c)` ?

The input consists of the two integers `a` and `b`. The output is `"YES"` if the equality remains true after removing zeros, otherwise `"NO"`.

The constraints are very small. Both numbers are at most `10^9`, which means each number has at most 10 digits. Any operation that processes digits one by one is effectively constant time. Even converting numbers to strings multiple times is trivial here. This immediately tells us the problem is not about optimization, but about implementing the transformation correctly.

The main source of mistakes is handling the zero-removal step carelessly.

One easy bug appears when the transformed number becomes empty. Consider:

```
a = 1000
b = 9000
```

After removing zeros:

```
a -> 1
b -> 9
c = 10000 -> 1
```

A careless implementation that tries to parse an empty string could crash if a number were all zeros. In this problem the original inputs are positive and nonzero, but intermediate handling still needs to be robust.

Another common mistake is removing only leading zeros instead of all zeros. For example:

```
a = 105
b = 106
```

Correct transformation:

```
105 -> 15
106 -> 16
211 -> 211
```

Since `15 + 16 != 211`, the answer is `"NO"`.

If someone only strips leading zeros, they would incorrectly keep `105` and `106` unchanged.

A subtler issue comes from comparing strings instead of integers. Consider:

```
a = 500
b = 500
```

After removing zeros:

```
500 -> 5
500 -> 5
1000 -> 1
```

We get:

```
5 + 5 = 10
1 != 10
```

The answer is `"NO"`.

The comparison must happen numerically after transformation.

## Approaches

The most direct brute-force idea is to simulate exactly what the statement describes. Compute `c = a + b`, convert all three numbers to strings, remove every `'0'` character, convert the results back to integers, and finally compare the transformed equation.

Because every number has at most 10 digits, this already runs in constant time. Even if we count operations precisely, we only scan a few dozen characters total.

There is no meaningful slower approach here, but a more awkward implementation could rebuild numbers digit by digit using arithmetic. For example, repeatedly taking `% 10`, skipping zeros, and reconstructing the answer. That also works correctly, but the implementation becomes more error-prone because digits arrive in reverse order.

The key observation is that the transformation is naturally a string operation. Removing all zeros from a decimal representation is exactly what string replacement is designed for. Once we realize the constraints are tiny and the operation is textual, the cleanest solution becomes obvious.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Digit-by-digit arithmetic reconstruction | O(d) | O(1) | Accepted |
| String transformation | O(d) | O(d) | Accepted |

Here, `d` is the number of digits, at most 10.

## Algorithm Walkthrough

1. Read integers `a` and `b`.

We need both original values because the transformed equality depends on the original sum.
2. Compute `c = a + b`.

The problem defines `c` this way, so we must transform the actual sum, not recompute after removing zeros.
3. Create a helper function that removes all `'0'` characters from a number’s decimal representation.

Convert the number to a string, replace all `'0'` characters with an empty string, then convert the result back to an integer.
4. Apply the transformation to `a`, `b`, and `c`.

Let these values be `na`, `nb`, and `nc`.
5. Check whether `na + nb == nc`.

If true, print `"YES"`, otherwise print `"NO"`.

### Why it works

The algorithm directly follows the definition of the problem. The helper function produces exactly the number obtained after deleting every zero digit from the decimal representation. Since we apply the same transformation independently to `a`, `b`, and `a + b`, the final comparison matches the required condition exactly. No approximation or shortcut is involved, so the algorithm cannot produce an incorrect result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def remove_zeros(x):
    return int(str(x).replace('0', ''))

def solve():
    a = int(input())
    b = int(input())

    c = a + b

    na = remove_zeros(a)
    nb = remove_zeros(b)
    nc = remove_zeros(c)

    if na + nb == nc:
        print("YES")
    else:
        print("NO")

solve()
```

The helper function handles the entire transformation in one line. Converting to a string allows us to remove every zero directly with `replace('0', '')`. Converting back to an integer gives the numeric value required for comparison.

The order of operations matters. We must first compute `c = a + b` using the original numbers. Only after that do we remove zeros. Computing the sum after transformation would solve a different problem.

The implementation stays safe because the original inputs are positive integers, and after removing zeros there is always at least one nonzero digit remaining. For example, `1000` becomes `"1"`, not an empty string.

## Worked Examples

### Example 1

Input:

```
101
102
```

| Variable | Value |
| --- | --- |
| a | 101 |
| b | 102 |
| c | 203 |
| remove(a) | 11 |
| remove(b) | 12 |
| remove(c) | 23 |
| 11 + 12 | 23 |

Since both sides are equal, the output is:

```
YES
```

This example demonstrates the core behavior of the problem. Even though zeros disappear from every number, the equality still survives.

### Example 2

Input:

```
105
106
```

| Variable | Value |
| --- | --- |
| a | 105 |
| b | 106 |
| c | 211 |
| remove(a) | 15 |
| remove(b) | 16 |
| remove(c) | 211 |
| 15 + 16 | 31 |

Since `31 != 211`, the output is:

```
NO
```

This case shows why we must remove zeros from every number independently. The transformed equation can completely change structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d) | Each digit is scanned a constant number of times |
| Space | O(d) | Temporary strings store transformed numbers |

Here `d` is the number of digits in the largest number, at most 10. The runtime and memory usage are tiny compared to the limits, so the solution easily fits within the constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def remove_zeros(x):
        return int(str(x).replace('0', ''))

    a = int(input())
    b = int(input())

    c = a + b

    na = remove_zeros(a)
    nb = remove_zeros(b)
    nc = remove_zeros(c)

    return "YES" if na + nb == nc else "NO"

# provided sample
assert run("101\n102\n") == "YES", "sample 1"

# custom cases
assert run("105\n106\n") == "NO", "zeros break equality"
assert run("1\n1\n") == "YES", "minimum nonzero inputs"
assert run("500\n500\n") == "NO", "transformed sum differs"
assert run("1000\n9000\n") == "NO", "many zeros in all numbers"
assert run("999999999\n1\n") == "YES", "boundary near maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `105 106` | `NO` | Internal zeros must be removed |
| `1 1` | `YES` | Smallest valid inputs |
| `500 500` | `NO` | Numeric comparison after transformation |
| `1000 9000` | `NO` | Heavy zero removal |
| `999999999 1` | `YES` | Large values near constraint limit |

## Edge Cases

Consider the input:

```
105
106
```

The algorithm computes:

```
c = 211
```

Then transforms:

```
105 -> 15
106 -> 16
211 -> 211
```

Finally:

```
15 + 16 = 31
```

Since `31 != 211`, the algorithm prints `"NO"`.

This confirms the implementation removes zeros everywhere, not just leading zeros.

Now consider:

```
500
500
```

The computation becomes:

```
c = 1000
```

After transformation:

```
500 -> 5
500 -> 5
1000 -> 1
```

The algorithm compares:

```
5 + 5 = 10
```

against:

```
1
```

and prints `"NO"`.

This case verifies that transformed values must be interpreted numerically after zero removal.

Finally, consider:

```
1000
9000
```

The transformed numbers are:

```
1000 -> 1
9000 -> 9
10000 -> 1
```

The algorithm checks:

```
1 + 9 = 10
```

which does not equal `1`, so the output is `"NO"`.

This confirms the solution correctly handles numbers containing many zeros without any special-case logic.
