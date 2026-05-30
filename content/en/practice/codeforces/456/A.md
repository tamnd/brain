---
title: "CF 456A - Laptops"
description: "We are given a collection of laptops. Each laptop has a price and a quality value. Prices are all distinct, and qualities are all distinct. Dima believes that a more expensive laptop must always have better quality. Alex claims that this is not necessarily true."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 456
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 260 (Div. 2)"
rating: 1100
weight: 456
solve_time_s: 88
verified: true
draft: false
---

[CF 456A - Laptops](https://codeforces.com/problemset/problem/456/A)

**Rating:** 1100  
**Tags:** sortings  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of laptops. Each laptop has a price and a quality value. Prices are all distinct, and qualities are all distinct.

Dima believes that a more expensive laptop must always have better quality. Alex claims that this is not necessarily true. He says there may exist two laptops such that the cheaper one actually has higher quality than the more expensive one.

Our task is to determine whether Alex's claim is true for the given set of laptops.

The input consists of up to $10^5$ laptops. For each laptop we receive two integers: its price and its quality. The output is `"Happy Alex"` if there exists at least one pair where a cheaper laptop has higher quality than a more expensive laptop. Otherwise we print `"Poor Alex"`.

The constraint $n \le 10^5$ immediately rules out checking every pair of laptops. A quadratic algorithm would perform roughly

$$\frac{10^5 \cdot (10^5 - 1)}{2} \approx 5 \times 10^9$$

comparisons in the worst case, which is far beyond what can run within one second. We need something around $O(n \log n)$ or better.

A subtle point is that laptop indices do not matter. Only the relationship between prices and qualities matters. A laptop appearing earlier in the input does not imply it is cheaper or more expensive.

Consider this example:

```
3
10 100
20 200
30 300
```

The correct output is:

```
Poor Alex
```

Every increase in price is accompanied by an increase in quality.

Now consider:

```
3
10 300
20 200
30 100
```

The correct output is:

```
Happy Alex
```

The laptop priced at 10 has better quality than the laptops priced at 20 and 30.

Another easy mistake is comparing only neighboring input lines:

```
3
30 300
10 200
20 100
```

The correct output is:

```
Happy Alex
```

The contradiction becomes obvious only after ordering laptops by price. The original input order contains no useful structure.

## Approaches

The most direct solution is brute force. For every laptop, compare it with every other laptop. Whenever we find two laptops where one has a smaller price but larger quality, Alex's claim is proven and we can stop.

This works because it explicitly checks the exact condition from the problem statement. Unfortunately, with $10^5$ laptops, the number of pairs is about $5 \times 10^9$. Even a very fast implementation cannot process that many comparisons within the time limit.

The key observation is that the condition depends only on the ordering of prices. If we sort all laptops by price, then every laptop to the right is more expensive than every laptop to the left.

Suppose we sort by price and obtain the sequence of qualities:

```
100 200 150
```

The quality decreases from 200 to 150 while price increases. That immediately gives a valid pair. The laptop with quality 200 is cheaper than the laptop with quality 150.

More generally, after sorting by price, Dima's belief is true if and only if qualities are also strictly increasing. Since all quality values are distinct, any decrease in quality means we have found a cheaper laptop with better quality.

So we only need to sort by price and scan the resulting qualities. If at any position the current quality is smaller than the previous quality, Alex is correct.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all laptops as `(price, quality)` pairs.
2. Sort the laptops by price in ascending order.

After sorting, every laptop appears before all more expensive laptops.
3. Scan the sorted list from left to right.
4. For each adjacent pair, compare their qualities.
5. If the current laptop has lower quality than the previous laptop, print `"Happy Alex"` and terminate.

The previous laptop is cheaper because of the sorting order, yet has higher quality. This is exactly the situation Alex described.
6. If the scan finishes without finding any decrease in quality, print `"Poor Alex"`.

### Why it works

After sorting by price, the laptops are arranged from cheapest to most expensive. If quality ever decreases while moving right, then a cheaper laptop has higher quality than a more expensive one, which proves Alex's claim.

Conversely, if quality never decreases, then qualities increase together with prices. Since all qualities are distinct, this means every more expensive laptop also has higher quality. No contradictory pair can exist.

The algorithm checks exactly this property, so it produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
laptops = []

for _ in range(n):
    price, quality = map(int, input().split())
    laptops.append((price, quality))

laptops.sort()

for i in range(1, n):
    if laptops[i][1] < laptops[i - 1][1]:
        print("Happy Alex")
        break
else:
    print("Poor Alex")
```

The first part reads all laptop descriptions into a list of pairs. The call to `sort()` orders them by price because price is the first element of each tuple.

The scan starts from the second laptop. For every position, we compare its quality with the quality of the immediately previous laptop in price order.

A decrease in quality is enough to prove Alex's claim. Once such a decrease is found, the answer is known and we terminate immediately.

The `for-else` construct is convenient here. The `else` block executes only if the loop completes without encountering a `break`, meaning no quality decrease was found.

There are no overflow concerns because all values are at most $10^5$, and the algorithm performs only comparisons and sorting.

## Worked Examples

### Example 1

Input:

```
2
1 2
2 1
```

After sorting by price:

| Index | Price | Quality |
| --- | --- | --- |
| 0 | 1 | 2 |
| 1 | 2 | 1 |

Scan:

| i | Previous Quality | Current Quality | Decrease? |
| --- | --- | --- | --- |
| 1 | 2 | 1 | Yes |

The quality drops from 2 to 1 while price increases from 1 to 2. A cheaper laptop is better than a more expensive one, so the answer is `"Happy Alex"`.

### Example 2

Input:

```
4
1 10
2 20
3 30
4 40
```

After sorting by price:

| Index | Price | Quality |
| --- | --- | --- |
| 0 | 1 | 10 |
| 1 | 2 | 20 |
| 2 | 3 | 30 |
| 3 | 4 | 40 |

Scan:

| i | Previous Quality | Current Quality | Decrease? |
| --- | --- | --- | --- |
| 1 | 10 | 20 | No |
| 2 | 20 | 30 | No |
| 3 | 30 | 40 | No |

No decrease is found. Every increase in price comes with an increase in quality, so the answer is `"Poor Alex"`.

This example confirms the invariant that qualities remain increasing throughout the sorted order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(n) | Storage of all laptop pairs |

With $n = 10^5$, an $O(n \log n)$ solution is easily fast enough. The memory usage is also small, requiring storage for only $10^5$ pairs.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    laptops = [tuple(map(int, input().split())) for _ in range(n)]

    laptops.sort()

    for i in range(1, n):
        if laptops[i][1] < laptops[i - 1][1]:
            print("Happy Alex")
            return

    print("Poor Alex")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("2\n1 2\n2 1\n") == "Happy Alex", "sample 1"

# minimum size
assert run("1\n5 10\n") == "Poor Alex", "single laptop"

# already increasing
assert run("4\n1 10\n2 20\n3 30\n4 40\n") == "Poor Alex", "perfect agreement"

# contradiction appears after sorting
assert run("3\n30 300\n10 200\n20 100\n") == "Happy Alex", "must sort first"

# contradiction far apart
assert run("5\n1 10\n2 20\n3 30\n4 40\n5 15\n") == "Happy Alex", "late decrease"

# two laptops only, opposite ordering
assert run("2\n100 200\n200 100\n") == "Happy Alex", "smallest non-trivial case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single laptop | Poor Alex | No pair exists |
| Strictly increasing qualities | Poor Alex | Dima's belief holds |
| Unsorted input | Happy Alex | Sorting by price is necessary |
| Late quality drop | Happy Alex | Scan must continue through entire array |
| Two opposite laptops | Happy Alex | Smallest valid contradiction |

## Edge Cases

Consider the smallest possible input:

```
1
5 10
```

After sorting, there is still only one laptop. The scan never executes because there is no pair to compare. The algorithm correctly prints:

```
Poor Alex
```

because Alex's claim requires two laptops.

Consider an input where the contradiction is hidden by the original ordering:

```
3
30 300
10 200
20 100
```

Sorting by price produces:

```
(10, 200)
(20, 100)
(30, 300)
```

During the scan, the quality drops from 200 to 100 at the second element. The algorithm immediately outputs:

```
Happy Alex
```

This shows why examining input order directly would be incorrect.

Consider a case where the contradiction appears near the end:

```
5
1 10
2 20
3 30
4 40
5 15
```

Sorted order is unchanged. The scan sees increasing qualities until the last comparison:

```
40 -> 15
```

Since quality decreases while price increases, the algorithm prints:

```
Happy Alex
```

This demonstrates that every adjacent comparison in price order must be checked until a violation is found.
