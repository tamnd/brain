---
title: "CF 106106E - \u0420\u0438\u043a \u0438 \u041c\u043e\u0440\u0442\u0438, \u0430 \u0442\u0430\u043a\u0436\u0435 \u0437\u043b\u043e\u0439 \u0442\u0430\u043c\u043e\u0436\u0435\u043d\u043d\u0438\u043a"
description: "We must decide whether it is possible to fill an n × m table with all integers from 1 to n·m exactly once so that two conditions hold."
date: "2026-06-25T11:41:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106106
codeforces_index: "E"
codeforces_contest_name: "\u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u042e\u043d\u0438\u043e\u0440\u044b 2024"
rating: 0
weight: 106106
solve_time_s: 47
verified: true
draft: false
---

[CF 106106E - \u0420\u0438\u043a \u0438 \u041c\u043e\u0440\u0442\u0438, \u0430 \u0442\u0430\u043a\u0436\u0435 \u0437\u043b\u043e\u0439 \u0442\u0430\u043c\u043e\u0436\u0435\u043d\u043d\u0438\u043a](https://codeforces.com/problemset/problem/106106/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We must decide whether it is possible to fill an `n × m` table with all integers from `1` to `n·m` exactly once so that two conditions hold.

For every pair of different rows, if we multiply all numbers inside the first row and all numbers inside the second row, those two products must have a common divisor greater than `1`.

The same requirement applies to every pair of different columns.

The input contains only the dimensions of the table. We do not need to construct the table, only determine whether such a table exists.

The values of `n` and `m` can be as large as `10^9`, which immediately tells us that any solution depending on the actual cells of the table is impossible. We cannot build the table, iterate over its elements, or perform any computation proportional to `n·m`. The answer must come from a purely mathematical characterization.

The most dangerous edge cases are the one-dimensional tables.

Consider:

```
n = 1
m = 2
```

The table must contain the numbers `1` and `2`. Each column contains exactly one number, so one column product is `1` and the other is `2`. Their gcd is `1`, which violates the requirement. The correct answer is `NO`.

A symmetric example is:

```
n = 2
m = 1
```

The row products are `1` and `2`, again coprime. The correct answer is `NO`.

The smallest valid case is:

```
n = 1
m = 1
```

There are no pairs of distinct rows and no pairs of distinct columns. Every condition is vacuously true, so the correct answer is `YES`.

A careless solution that prints `YES` whenever at least one dimension equals `1` would fail on both `1 × 2` and `2 × 1`.

## Approaches

A brute-force way of thinking is to try constructing a table and then checking all row and column products. Even for moderate dimensions this becomes enormous, because the number of possible fillings is `(n·m)!`. With dimensions reaching `10^9`, this direction is completely hopeless.

The key observation is that the actual values inside the table matter much less than the number `1`.

If one dimension equals `1` and the other is larger than `1`, then one row or one column consists of a single cell. Since every number from `1` to `n·m` must appear exactly once, one of those row or column products is exactly `1`. The gcd of `1` with any other positive integer is always `1`, so the condition immediately fails.

The interesting part is showing that every table with at least two rows and at least two columns is feasible.

Suppose `n > 1` and `m > 1`. If every row product is even, then any two row products share the divisor `2`. Similarly, if every column product is even, then any two column products also share the divisor `2`.

So the entire problem reduces to placing the even numbers so that every row and every column receives at least one even number.

There are `⌊nm/2⌋` even numbers among `1, 2, ..., nm`. For all `n, m > 1`,

```
⌊nm/2⌋ ≥ max(n, m)
```

which gives enough even numbers to cover every row and every column. After placing those even numbers appropriately, all remaining cells can be filled arbitrarily with the remaining numbers.

Thus every table with both dimensions greater than `1` is possible.

The final characterization is extremely simple:

```
YES  if n = 1 and m = 1
YES  if n > 1 and m > 1
NO   otherwise
```

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Construction | Exponential | Exponential | Too slow |
| Mathematical Characterization | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. If `n = 1` and `m = 1`, print `"YES"`.

There are no pairs of distinct rows or columns, so all requirements are automatically satisfied.
3. If exactly one of `n` or `m` equals `1`, print `"NO"`.

The number `1` must occupy some row or column by itself, creating a product equal to `1`, which is coprime with every other product.
4. Otherwise, print `"YES"`.

When both dimensions are at least `2`, we can distribute even numbers so that every row and every column contains one. Then every row product and every column product is divisible by `2`.

### Why it works

When one dimension is `1` and the other is larger than `1`, some row or column product equals exactly `1`. Any pair involving that product has gcd `1`, so the requirements cannot be satisfied.

When both dimensions exceed `1`, enough even numbers exist to place at least one even number in every row and every column. Every row product becomes divisible by `2`, and every column product becomes divisible by `2`. Any two such products share the divisor `2`, so all required gcds are greater than `1`.

These two cases cover all possible inputs, making the characterization complete.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
m = int(input())

if (n == 1 and m == 1) or (n > 1 and m > 1):
    print("YES")
else:
    print("NO")
```

The implementation mirrors the mathematical result directly.

The first condition handles the special `1 × 1` table. This case is valid because there are no pairs of rows or columns to check.

The second condition handles all tables where both dimensions are at least two. The existence proof described above guarantees that a suitable arrangement can always be created.

Every remaining case has exactly one dimension equal to `1`, which is impossible because the number `1` creates a row or column product equal to `1`.

No arithmetic larger than simple comparisons is needed, so the huge limits on `n` and `m` are irrelevant.

## Worked Examples

### Example 1

Input:

```
2
2
```

| n | m | Condition matched | Answer |
| --- | --- | --- | --- |
| 2 | 2 | n > 1 and m > 1 | YES |

A valid arrangement exists. For example:

```
1 2
4 3
```

Row products are `2` and `12`, whose gcd is `2`. Column products are `4` and `6`, whose gcd is `2`.

### Example 2

Input:

```
2
1
```

| n | m | Condition matched | Answer |
| --- | --- | --- | --- |
| 2 | 1 | Exactly one dimension equals 1 | NO |

The table must contain:

```
1
2
```

The row products are `1` and `2`. Their gcd is `1`, so the requirement fails.

This example demonstrates why every nontrivial one-dimensional table is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few comparisons are performed |
| Space | O(1) | No auxiliary data structures are used |

The solution runs in constant time regardless of how large `n` and `m` are, which easily fits the limits up to `10^9`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    m = int(sys.stdin.readline())

    if (n == 1 and m == 1) or (n > 1 and m > 1):
        return "YES\n"
    return "NO\n"

# provided samples
assert run("2\n2\n") == "YES\n", "sample 1"
assert run("2\n1\n") == "NO\n", "sample 2"

# custom cases
assert run("1\n1\n") == "YES\n", "single cell"
assert run("1\n5\n") == "NO\n", "single row"
assert run("5\n1\n") == "NO\n", "single column"
assert run("1000000000\n1000000000\n") == "YES\n", "maximum dimensions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `YES` | Vacuous conditions |
| `1 5` | `NO` | One-dimensional row |
| `5 1` | `NO` | One-dimensional column |
| `10^9 10^9` | `YES` | Largest possible dimensions |

## Edge Cases

Consider the input:

```
1
2
```

The numbers used are `1` and `2`. Each column contains exactly one value, so the column products are `1` and `2`. Their gcd equals `1`, violating the condition. The algorithm falls into the "exactly one dimension equals 1" branch and correctly prints `NO`.

Now consider:

```
2
1
```

The row products are `1` and `2`, again giving gcd `1`. The algorithm again prints `NO`.

Finally:

```
1
1
```

There are no pairs of rows and no pairs of columns. Every requirement is automatically true. The algorithm recognizes this special case and prints `YES`.
