---
title: "CF 1793A - Yet Another Promotion"
description: "You need at least n kilograms of potatoes. The store is open on two different days. On the first day, each kilogram costs a, and there is a promotion: every time you pay for m kilograms, you receive one extra kilogram for free."
date: "2026-06-09T10:17:56+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1793
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 852 (Div. 2)"
rating: 800
weight: 1793
solve_time_s: 217
verified: true
draft: false
---

[CF 1793A - Yet Another Promotion](https://codeforces.com/problemset/problem/1793/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 3m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

You need at least `n` kilograms of potatoes. The store is open on two different days.

On the first day, each kilogram costs `a`, and there is a promotion: every time you pay for `m` kilograms, you receive one extra kilogram for free. A purchase of `m` paid kilograms gives you `m + 1` kilograms in total.

On the second day, each kilogram costs `b` and there is no promotion.

You may buy any nonnegative integer number of kilograms on either day. The goal is to obtain at least `n` kilograms while spending the smallest possible number of coins.

The constraints immediately suggest that each test case must be solved in constant time. The values can reach `10^9`, so iterating over possible purchase amounts is impossible. With up to `10^4` test cases, even an `O(n)` solution per test case would be far too slow.

The main difficulty is deciding when the promotion is actually useful. A common mistake is to assume that the first-day promotion should always be used as much as possible. That is false when buying `m` kilograms on day one costs more than simply buying `m + 1` kilograms on day two.

Consider:

```
a = 10, b = 1, m = 2, n = 3
```

One promotion block gives 3 kilograms for cost 20. Buying all 3 kilograms on day two costs only 3. Using the promotion is disastrous here.

Another easy mistake is mishandling the final incomplete block.

Consider:

```
a = 5, b = 4, m = 2, n = 4
```

One full promotion block gives 3 kilograms for cost 10. One kilogram is still needed. Buying that kilogram on day two costs 4, for a total of 14. Buying all 4 kilograms on day two costs 16. The remainder must be treated separately.

A third edge case appears when `n < m + 1`.

Consider:

```
a = 5, b = 4, m = 100, n = 2
```

You cannot form even a single promotion block. The answer is simply `2 * min(a, b)`.

## Approaches

A brute-force solution would try every possible number of kilograms purchased on the first day, compute how many kilograms are obtained after gifts, then buy the remaining kilograms on the second day. This is correct because it examines every feasible strategy.

The problem is that the number of possibilities is proportional to `n`, and `n` may be `10^9`. Even one test case would be impossible to process this way.

The key observation is that the promotion behaves in fixed-size blocks. Paying for `m` kilograms on day one yields `m + 1` kilograms.

A promotion block therefore costs

$$m \cdot a$$

and produces

$$m+1$$

kilograms.

If obtaining `m+1` kilograms entirely on day two costs

$$(m+1)\cdot b,$$

then we should compare these two values.

If

$$m a \ge (m+1)b,$$

a promotion block is never better than buying the same amount on day two. In that situation we should completely ignore the promotion and buy every kilogram at the cheaper daily price.

If

$$m a < (m+1)b,$$

every full promotion block is beneficial. Then we use as many complete blocks as possible and handle the remaining kilograms separately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the cost of one promotion block:

$$\text{promo} = m \cdot a.$$

A promotion block gives exactly `m + 1` kilograms.

1. Compute the cost of obtaining the same number of kilograms entirely on day two:

$$\text{normal} = (m+1)\cdot b.$$

1. If

$$m a \ge (m+1)b,$$

ignore the promotion. Every kilogram should simply be bought at the cheaper daily price, giving

$$n \cdot \min(a,b).$$

1. Otherwise, the promotion is worthwhile. Let

$$q = \left\lfloor \frac{n}{m+1} \right\rfloor$$

be the number of complete promotion blocks.

1. These blocks contribute

$$q \cdot m \cdot a$$

coins.

1. Let

$$r = n \bmod (m+1).$$

These kilograms are not enough to form another full promotion block.

1. For the remaining `r` kilograms, buy each kilogram using the cheaper of the two daily prices:

$$r \cdot \min(a,b).$$

1. Add both contributions and print the result.

### Why it works

Whenever

$$m a < (m+1)b,$$

a complete promotion block is strictly cheaper than obtaining the same number of kilograms on day two. Replacing a full block with any other method cannot improve the answer.

Whenever

$$m a \ge (m+1)b,$$

a promotion block is never advantageous. Any solution containing such a block can be replaced by buying the same number of kilograms on day two for no greater cost.

After taking all profitable complete blocks, the remaining quantity is less than `m+1`. Forming another promotion block would necessarily purchase extra unnecessary kilograms. For these remaining kilograms, each unit can be bought independently at cost `min(a,b)`, which is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        a, b = map(int, input().split())
        n, m = map(int, input().split())

        if m * a >= (m + 1) * b:
            print(n * min(a, b))
        else:
            blocks = n // (m + 1)
            rem = n % (m + 1)

            ans = blocks * m * a
            ans += rem * min(a, b)

            print(ans)

solve()
```

The first branch handles the case where the promotion is not competitive with ordinary purchases. In that situation every kilogram should simply be bought at the cheaper available unit price.

The second branch uses as many profitable promotion blocks as possible. The integer division computes how many complete groups of `m + 1` kilograms fit into the target quantity. The remainder is handled independently.

The multiplication order matters only for readability because Python integers have arbitrary precision. In languages with fixed-width integers, 64-bit arithmetic would be required because values can reach roughly `10^18`.

A common off-by-one error is dividing by `m` instead of `m + 1`. The promotion produces `m + 1` kilograms, so complete blocks must be counted using that size.

## Worked Examples

### Example 1

Input:

```
a = 5, b = 4
n = 3, m = 1
```

| Quantity | Value |
| --- | --- |
| Promotion block cost | 5 |
| Same amount on day two | 8 |
| Blocks | 1 |
| Remainder | 1 |
| Block contribution | 5 |
| Remainder contribution | 4 |
| Answer | 9 |

One promotion block gives 2 kilograms for cost 5. One more kilogram is bought on day two for 4. Total cost is 9.

### Example 2

Input:

```
a = 20, b = 15
n = 10, m = 2
```

| Quantity | Value |
| --- | --- |
| Promotion block cost | 40 |
| Same amount on day two | 45 |
| Blocks | 3 |
| Remainder | 1 |
| Block contribution | 120 |
| Remainder contribution | 15 |
| Answer | 135 |

Three promotion blocks provide 9 kilograms. One kilogram remains and is bought on day two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations |
| Space | O(1) | No auxiliary data structures |

Even with `10^4` test cases, the total work is tiny. The solution easily fits within the time and memory limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        a, b = map(int, input().split())
        n, m = map(int, input().split())

        if m * a >= (m + 1) * b:
            out.append(str(n * min(a, b)))
        else:
            blocks = n // (m + 1)
            rem = n % (m + 1)
            ans = blocks * m * a + rem * min(a, b)
            out.append(str(ans))

    return "\n".join(out)

# sample
assert run(
"""5
5 4
3 1
5 4
3 2
3 4
3 5
20 15
10 2
1000000000 900000000
1000000000 8
"""
) == "\n".join([
    "9",
    "10",
    "9",
    "135",
    "888888888900000000"
])

# minimum case
assert run(
"""1
1 1
1 1
"""
) == "1"

# promotion useless
assert run(
"""1
10 1
100 2
"""
) == "100"

# n smaller than one block
assert run(
"""1
5 4
2 100
"""
) == "8"

# exact multiple of block size
assert run(
"""1
3 10
9 2
"""
) == "18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a=1,b=1,n=1,m=1` | `1` | Smallest valid input |
| `a=10,b=1,n=100,m=2` | `100` | Promotion should be ignored |
| `a=5,b=4,n=2,m=100` | `8` | No complete promotion block fits |
| `a=3,b=10,n=9,m=2` | `18` | Exact multiple of block size |

## Edge Cases

Consider:

```
a = 10
b = 1
n = 3
m = 2
```

A full promotion block costs 20 and yields 3 kilograms. Buying 3 kilograms on day two costs only 3. Since

$$20 \ge 3,$$

the algorithm enters the first branch and returns

$$3 \cdot 1 = 3.$$

This correctly avoids the promotion.

Consider:

```
a = 5
b = 4
n = 2
m = 100
```

No promotion block can be completed because one block would produce 101 kilograms. The algorithm computes zero complete blocks and buys the remaining two kilograms at cost `min(5,4)=4`, giving 8.

Consider:

```
a = 3
b = 10
n = 9
m = 2
```

Each promotion block costs 6 and yields 3 kilograms. Three complete blocks exactly provide the required amount. The remainder is zero, so the answer is simply

$$3 \cdot 6 = 18.$$

This verifies that exact divisibility is handled without purchasing unnecessary kilograms.
