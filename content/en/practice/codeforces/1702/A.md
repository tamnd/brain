---
title: "CF 1702A - Round Down the Price"
description: "Each test case gives the current price of an item. A \"round\" price is any power of ten: 1, 10, 100, 1000, and so on. We want to reduce the item's price until it becomes the largest round number that does not exceed the original price."
date: "2026-06-09T21:41:10+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1702
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 805 (Div. 3)"
rating: 800
weight: 1702
solve_time_s: 114
verified: true
draft: false
---

[CF 1702A - Round Down the Price](https://codeforces.com/problemset/problem/1702/A)

**Rating:** 800  
**Tags:** constructive algorithms  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives the current price of an item. A "round" price is any power of ten: 1, 10, 100, 1000, and so on.

We want to reduce the item's price until it becomes the largest round number that does not exceed the original price. The answer is the amount removed from the price.

For example, if the price is 178, the largest power of ten not greater than 178 is 100. The reduction is 178 - 100 = 78.

The price is at most $10^9$, and there can be up to $10^4$ test cases. These limits are very small for arithmetic operations. Even an $O(\log m)$ solution per test case is easily fast enough because $m$ has at most 10 digits. There is no need for heavy data structures or preprocessing.

The tricky part is correctly identifying the largest power of ten not exceeding the given value.

One edge case occurs when the price is already a power of ten.

Input:

```
1
1000
```

Output:

```
0
```

The largest valid round number is 1000 itself, so nothing needs to be removed. A careless solution that always chooses a strictly smaller power of ten would incorrectly output 900.

Another edge case is the smallest possible value.

Input:

```
1
1
```

Output:

```
0
```

Since 1 is $10^0$, the answer is again zero.

A third useful example is a number just below the next power of ten.

Input:

```
1
999999999
```

Output:

```
899999999
```

The largest power of ten not exceeding the price is $10^8 = 100000000$, not $10^9$, because $10^9$ is larger than the given value.

## Approaches

A brute-force idea is to generate powers of ten and search for the largest one not exceeding the given price. Since powers of ten grow quickly, there are only a handful of candidates up to $10^9$: 1, 10, 100, ..., $10^9$. Checking all of them for every test case is already fast enough.

The real observation is that the largest power of ten not exceeding a number is determined entirely by the number of digits. For a positive integer with $d$ digits, the largest power of ten not exceeding it is $10^{d-1}$.

For example, 178 has three digits, so the desired round number is $10^2 = 100$. Likewise, 987654321 has nine digits, so the desired round number is $10^8 = 100000000$.

Once we know this power of ten, the answer is simply:

$$m - 10^{d-1}$$

The brute-force and optimal approaches are very similar here because the constraints are tiny. The digit-count observation gives the cleanest implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(log m) | O(1) | Accepted |
| Optimal | O(log m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the price $m$.
2. Convert $m$ to a string and compute its length $d$.

The length directly tells us how many digits the number contains.
3. Compute the largest power of ten not exceeding $m$ as $10^{d-1}$.

Any positive integer with $d$ digits is at least $10^{d-1}$ and less than $10^d$.
4. Compute the required reduction:

$$\text{answer} = m - 10^{d-1}$$
5. Output the answer.

### Why it works

For every positive integer $m$ with $d$ digits,

$$10^{d-1} \le m < 10^d$$

This means $10^{d-1}$ is a valid round number not exceeding $m$. Any larger power of ten would be $10^d$, which is strictly greater than $m$. Thus $10^{d-1}$ is exactly the largest round number allowed by the problem. Subtracting it from $m$ gives the required decrease.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    m = int(input())
    d = len(str(m))
    round_price = 10 ** (d - 1)
    print(m - round_price)
```

The program processes each test case independently.

The number of digits is obtained using `len(str(m))`. If a number has `d` digits, the largest power of ten not exceeding it is `10 ** (d - 1)`.

The subtraction `m - round_price` directly produces the required reduction.

There are no overflow concerns because the largest value involved is $10^9$, which is trivial for Python integers.

A common mistake is using the nearest power of ten rather than the largest power of ten not exceeding the price. For example, 9000 should use 1000, not 10000, because 10000 is larger than the original price.

## Worked Examples

### Example 1

Input price:

```
178
```

| m | Digits d | Largest valid power of ten | Answer |
| --- | --- | --- | --- |
| 178 | 3 | 100 | 78 |

The number has three digits, so the target round price is $10^2 = 100$. The reduction is $178 - 100 = 78$.

### Example 2

Input price:

```
987654321
```

| m | Digits d | Largest valid power of ten | Answer |
| --- | --- | --- | --- |
| 987654321 | 9 | 100000000 | 887654321 |

The number has nine digits. The largest power of ten not exceeding it is $10^8$. Subtracting gives the required reduction.

These examples illustrate the key invariant: once the digit count is known, the target round number is fixed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log m) | Converting the number to a string takes time proportional to its digit count |
| Space | O(1) | Only a few variables are stored |

Since $m \le 10^9$, each number has at most 10 digits. Even with $10^4$ test cases, the total work is tiny and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        m = int(input())
        ans.append(str(m - 10 ** (len(str(m)) - 1)))

    return "\n".join(ans)

# provided sample
assert run(
"""7
1
2
178
20
999999999
9000
987654321
"""
) == "\n".join([
"0",
"1",
"78",
"10",
"899999999",
"8000",
"887654321"
]), "sample"

# minimum value
assert run(
"""1
1
"""
) == "0", "minimum input"

# already a power of ten
assert run(
"""1
1000
"""
) == "0", "already round"

# just below next power of ten
assert run(
"""1
999
"""
) == "899", "boundary below power"

# maximum constraint
assert run(
"""1
1000000000
"""
) == "0", "maximum value"

# mixed values
assert run(
"""4
10
11
99
100
"""
) == "\n".join([
"0",
"1",
"89",
"0"
]), "mixed boundary cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | Smallest possible value |
| 1000 | 0 | Already a power of ten |
| 999 | 899 | Number immediately below a power of ten |
| 1000000000 | 0 | Maximum allowed value |
| 10, 11, 99, 100 | 0, 1, 89, 0 | Boundary transitions between digit lengths |

## Edge Cases

Consider the input:

```
1
1
```

The number has one digit, so the algorithm computes $10^{1-1} = 1$. The answer is $1 - 1 = 0$. This correctly handles the smallest possible value.

Consider the input:

```
1
1000
```

The number has four digits. The algorithm computes $10^3 = 1000$. The answer is $1000 - 1000 = 0$. Since the price is already a round number, no reduction is needed.

Consider the input:

```
1
999999999
```

The number has nine digits. The algorithm computes $10^8 = 100000000$. The answer becomes:

$$999999999 - 100000000 = 899999999$$

The next power of ten, $10^9$, is too large and cannot be used. The digit-count rule automatically selects the correct round number.

Consider the input:

```
1
20
```

The number has two digits. The algorithm chooses $10^1 = 10$. The answer is $20 - 10 = 10$. This confirms that the target is the largest power of ten not exceeding the value, not the nearest power of ten.
