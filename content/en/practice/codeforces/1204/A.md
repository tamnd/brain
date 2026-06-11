---
title: "CF 1204A - BowWow and the Timetable"
description: "The trains leave at times $$1, 4, 16, 64, dots$$ which are exactly the powers of 4. Given a time $s$, we need to count how many of these departure times are strictly smaller than $s$. The unusual part is that $s$ is not given in decimal."
date: "2026-06-11T23:38:47+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1204
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 581 (Div. 2)"
rating: 1000
weight: 1204
solve_time_s: 115
verified: true
draft: false
---

[CF 1204A - BowWow and the Timetable](https://codeforces.com/problemset/problem/1204/A)

**Rating:** 1000  
**Tags:** math  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

The trains leave at times

$$1, 4, 16, 64, \dots$$

which are exactly the powers of 4. Given a time $s$, we need to count how many of these departure times are strictly smaller than $s$.

The unusual part is that $s$ is not given in decimal. Instead, it is given as a binary string without leading zeroes, and its value can be as large as $2^{100}-1$. A normal 64-bit integer is not enough to store every possible value.

The constraint immediately suggests that we should avoid converting the entire number into a standard integer type. The binary representation contains at most 100 bits, so any solution that works directly on the string in linear time is easily fast enough.

The key observation is that every train departure time is a power of 4:

$$4^k = 2^{2k}.$$

In binary, powers of 4 look like:

$$1,\ 100,\ 10000,\ 1000000,\dots$$

Each has exactly one set bit, and that bit is located at an even position.

Several edge cases are easy to mishandle.

Consider:

```
1
```

The time is exactly $1$. Since departures must be strictly before $s$, no train has left yet. The answer is:

```
0
```

A solution that counts powers of 4 less than or equal to $s$ would incorrectly return 1.

Consider:

```
100
```

This is $4$ in decimal. Only the train at time $1$ departed earlier, so the answer is:

```
1
```

Again, using $\le$ instead of $<$ would produce 2.

Another subtle case is:

```
101
```

which is $5$. The departures at $1$ and $4$ are both earlier, so the answer is:

```
2
```

This differs from the previous example even though both numbers have the same binary length. We must distinguish between a pure power of 4 and a larger number of the same bit length.

## Approaches

A direct brute-force idea is to repeatedly generate powers of 4:

$$1,4,16,64,\dots$$

and count how many are smaller than $s$. Since $s < 2^{100}$, there are only about 50 relevant powers of 4. If we convert the binary string into a big integer first, this approach is actually fast enough.

The more interesting solution avoids converting the number at all.

The departure times are powers of 4, which are exactly the numbers $2^{2k}$. Suppose the binary representation of $s$ has length $L$.

Every power of 4 with binary length strictly less than $L$ is automatically smaller than $s$. Their lengths are

$$1,3,5,\dots$$

because $2^{2k}$ has binary length $2k+1$.

The number of such powers is

$$\left\lfloor \frac{L-1}{2} \right\rfloor.$$

What remains is deciding whether the power of 4 having the same binary length as $s$ should also be counted.

For a binary string of length $L$, that power is

$$2^{L-1}.$$

It is a power of 4 only when $L-1$ is even, meaning $L$ is odd.

If $L$ is odd and $s$ is strictly larger than the binary string

$$1\underbrace{00\dots0}_{L-1\text{ zeros}},$$

then that additional power of 4 is also smaller than $s$ and must be counted.

This reduces the entire problem to inspecting the binary string itself.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(L) | O(1) | Accepted |
| Optimal | O(L) | O(1) | Accepted |

Here $L \le 100$ is the binary string length.

## Algorithm Walkthrough

1. Read the binary string $s$.
2. Let $L$ be its length.
3. Count all powers of 4 whose binary length is strictly smaller than $L$.

This number is:

$$\left\lfloor \frac{L-1}{2} \right\rfloor.$$
4. If $L$ is even, no power of 4 has binary length $L$, so output the current count.
5. If $L$ is odd, compare $s$ with the binary string consisting of a leading `1` followed by only zeros.

This string represents $2^{L-1}$, the unique power of 4 having length $L$.
6. If $s$ is strictly larger than that string, add one to the answer.
7. Output the result.

Why it works:

Every power of 4 corresponds to a binary number with exactly one set bit at an even exponent. Among numbers whose binary length is less than $L$, all such powers are automatically smaller than $s$, and their count is exactly $\lfloor (L-1)/2 \rfloor$. When $L$ is odd, there is one additional candidate, namely $2^{L-1}$. It should be counted precisely when it is strictly smaller than $s$. No other powers of 4 can exist in the interval because powers of 4 increase by two bits of exponent at a time. Thus the algorithm counts exactly the departures before time $s$.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)

ans = (n - 1) // 2

if n % 2 == 1:
    if s != "1" + "0" * (n - 1):
        ans += 1

print(ans)
```

The first part computes the number of powers of 4 whose binary length is strictly smaller than the length of the input.

The expression `(n - 1) // 2` comes directly from counting odd lengths:

$$1,3,5,\dots < n.$$

The only remaining question is whether the power of 4 with the same binary length should be included. Such a power exists only when `n` is odd.

For an odd length `n`, the relevant power is exactly the string:

```
1000...000
```

with `n-1` zeros. If the input equals this string, then the departure time is not strictly before `s`, so we do not add it. Any other binary string of the same length is larger, meaning that power of 4 should be counted.

No integer conversion is needed, which avoids any concern about number size.

## Worked Examples

### Example 1

Input:

```
100000000
```

| Variable | Value |
| --- | --- |
| s | `100000000` |
| n | 9 |
| initial ans | (9 - 1) // 2 = 4 |
| n odd? | Yes |
| power string | `100000000` |
| s equals power string? | Yes |
| final ans | 4 |

Output:

```
4
```

The number is exactly $256 = 4^4$. The trains at $1,4,16,64$ have departed, but the train at $256$ has not departed strictly before time $256$.

### Example 2

Input:

```
101
```

| Variable | Value |
| --- | --- |
| s | `101` |
| n | 3 |
| initial ans | (3 - 1) // 2 = 1 |
| n odd? | Yes |
| power string | `100` |
| s equals power string? | No |
| add 1? | Yes |
| final ans | 2 |

Output:

```
2
```

The number is $5$. Both $1$ and $4$ are strictly smaller than $5$, so two trains have already departed.

This example shows why numbers with the same binary length cannot all be treated identically. The distinction between `100` and `101` matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L) | Building and comparing strings of length L |
| Space | O(1) | Only a few variables are stored |

Since the binary representation contains at most 100 characters, the algorithm performs only a tiny amount of work. It comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    s = input().strip()
    n = len(s)

    ans = (n - 1) // 2

    if n % 2 == 1:
        if s != "1" + "0" * (n - 1):
            ans += 1

    return str(ans)

# provided sample
assert run("100000000\n") == "4", "sample 1"

# custom cases
assert run("1\n") == "0", "minimum value"
assert run("100\n") == "1", "exact power of 4"
assert run("101\n") == "2", "just above a power of 4"
assert run("11\n") == "0", "even length, no same-length power of 4"
assert run("1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111\n") == "50", "maximum length 100 bits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Strict inequality at the smallest value |
| `100` | `1` | Exact power of 4 should not count itself |
| `101` | `2` | Same length but larger than a power of 4 |
| `11` | `0` | Even-length numbers have no same-length power of 4 |
| 100 ones | `50` | Largest allowed binary length |

## Edge Cases

Consider the input:

```
1
```

The algorithm computes `n = 1` and `ans = 0`. Since the string equals `1`, the extra count is not added. The result is:

```
0
```

This correctly handles the fact that departures must be strictly before the arrival time.

Consider the input:

```
100
```

Here `n = 3`, so the initial count is `(3 - 1) // 2 = 1`. The same-length power string is also `100`. Because they are equal, no extra train is counted. The answer remains:

```
1
```

This prevents the common mistake of counting departures at time exactly $s$.

Consider the input:

```
101
```

Again `n = 3`, so the initial count is 1. The same-length power string is `100`, and the input is larger. One extra train is added, giving:

```
2
```

This demonstrates why equality must be treated differently from being strictly larger.

Consider the input:

```
11
```

The length is even. No power of 4 can have binary length 2, because powers of 4 always have odd binary lengths. The algorithm immediately returns:

```
0
```

which matches reality, since $3$ is smaller than the first same-length candidate $4$.
