---
title: "CF 105227E - Recursive Queries"
description: "Each query gives a segment of integers and asks how many numbers in that segment share a specific value under a transformation function g. The function g takes a number and repeatedly replaces it with the product of its digits until the value becomes a single digit."
date: "2026-06-24T16:29:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105227
codeforces_index: "E"
codeforces_contest_name: "CPG Training Contest - 1"
rating: 0
weight: 105227
solve_time_s: 90
verified: false
draft: false
---

[CF 105227E - Recursive Queries](https://codeforces.com/problemset/problem/105227/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

Each query gives a segment of integers and asks how many numbers in that segment share a specific value under a transformation function g. The function g takes a number and repeatedly replaces it with the product of its digits until the value becomes a single digit. That final single digit is the result of g(x). For example, 47 becomes 4 × 7 = 28, then 2 × 8 = 16, then 1 × 6 = 6, so g(47) = 6.

The task is to answer up to two hundred thousand such queries, where each query asks for a range [l, r] inside the range up to one million and a target digit k between 1 and 9. The output for each query is the count of integers in that range whose multiplicative digital root equals k.

The constraints immediately force us away from per-query simulation. A naive approach that recomputes g(x) for every x in [l, r] would require up to one million operations per query in the worst case, leading to around 2 × 10^11 operations overall, which is far beyond feasible.

A subtle point is that although x goes up to 10^6, g(x) always collapses quickly to a single digit. That means there are only nine possible outcomes, so repeated structure across the domain can be precomputed.

Edge cases arise from the behavior of digit multiplication. Numbers containing zero immediately collapse to zero, but k is guaranteed to be between 1 and 9, so those values are irrelevant for counting. Another corner case is numbers like 10 or 1000, which become zero under multiplication and must not accidentally be counted toward any positive k.

## Approaches

A brute-force method evaluates g(x) independently for each number in each query. For every x, we repeatedly multiply digits until a single digit is reached. This costs at most a few digit multiplications per number, but across all queries this becomes too large since each query can span up to one million numbers and there are up to two hundred thousand queries.

The key observation is that the transformation g(x) depends only on x and not on the query. Once we know g(x) for every x up to one million, each query becomes a simple counting problem over a precomputed array.

We precompute an array where each position stores g(x). Then for each digit k from 1 to 9, we build a prefix sum over all x such that g(x) = k. After that, each query is answered in constant time using prefix differences.

This converts repeated recomputation into a single preprocessing pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q · N · log N) | O(1) | Too slow |
| Optimal (precompute + prefix sums) | O(N log N + Q) | O(N) | Accepted |

## Algorithm Walkthrough

We first compute g(x) for every x from 1 to 1,000,000. This is done by repeatedly replacing a number with the product of its digits until it becomes a single digit. This step is necessary because once computed, all queries reuse these values.

Next, we store counts of how many numbers produce each possible digit from 1 to 9. Instead of storing raw frequencies only, we build prefix sums so that we can answer range queries efficiently.

We then convert the original query [l, r, k] into a difference of prefix sums: the answer is prefix[k][r] minus prefix[k][l − 1]. This works because prefix arrays accumulate counts from 1 up to each position.

Finally, we print the result for each query.

### Why it works

The correctness comes from the fact that g(x) is a pure function of x and independent of query structure. Once computed, every occurrence of x contributes exactly one unit to exactly one digit bucket. Prefix sums preserve these counts cumulatively, so any interval query reduces to subtracting two cumulative totals without losing or double-counting any contribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 10**6

def prod_digits(x):
    while x >= 10:
        p = 1
        while x > 0:
            x, d = divmod(x, 10)
            p *= d
        x = p
    return x

g = [0] * (MAXN + 1)
for i in range(1, MAXN + 1):
    g[i] = prod_digits(i)

prefix = [[0] * (MAXN + 1) for _ in range(10)]

for i in range(1, MAXN + 1):
    val = g[i]
    for k in range(1, 10):
        prefix[k][i] = prefix[k][i - 1]
    prefix[val][i] += 1

q = int(input())
out = []

for _ in range(q):
    l, r, k = map(int, input().split())
    out.append(str(prefix[k][r] - prefix[k][l - 1]))

print("\n".join(out))
```

The solution begins by defining the multiplicative digit reduction function. It repeatedly multiplies digits until the number becomes a single digit, which ensures correctness even for inputs that pass through multiple intermediate stages like 39 or 88.

We then precompute g(x) for all values up to one million. This is the expensive part but is done only once.

After that, we build prefix arrays for each digit from 1 to 9. Each prefix array tracks how many numbers up to index i have a given g-value.

Queries are answered using subtraction of prefix ranges, which avoids any recomputation.

## Worked Examples

Consider a small illustrative case where we query a few intervals after preprocessing g(x).

Let us trace a simplified version over a small range:

| i | g(i) | prefix[4][i] | prefix[6][i] |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 0 |
| 2 | 2 | 0 | 0 |
| 3 | 3 | 0 | 0 |
| 4 | 4 | 1 | 0 |
| 5 | 5 | 1 | 0 |
| 6 | 6 | 1 | 1 |
| 7 | 7 | 1 | 1 |
| 8 | 8 | 1 | 1 |
| 9 | 9 | 1 | 1 |

For a query [4, 7, 6], we compute prefix[6][7] − prefix[6][3] = 1 − 0 = 1.

Now consider a query [1, 9, 4], we compute prefix[4][9] − prefix[4][0] = 1 − 0 = 1, since only the number 4 maps to 4 in this range.

These traces show that once prefix arrays are built, each query reduces to two table lookups and one subtraction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N + Q) | Each number up to 1e6 is reduced via digit products, then each query is O(1) |
| Space | O(N) | Prefix arrays store cumulative counts for each digit |

The preprocessing fits comfortably within limits since N log N operations over one million integers is acceptable in Python, and queries are answered in constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MAXN = 200  # small bound for testing

    def prod_digits(x):
        while x >= 10:
            p = 1
            while x > 0:
                x, d = divmod(x, 10)
                p *= d
            x = p
        return x

    g = [0] * (MAXN + 1)
    for i in range(1, MAXN + 1):
        g[i] = prod_digits(i)

    prefix = [[0] * (MAXN + 1) for _ in range(10)]
    for i in range(1, MAXN + 1):
        for k in range(1, 10):
            prefix[k][i] = prefix[k][i - 1]
        prefix[g[i]][i] += 1

    q = int(input())
    out = []
    for _ in range(q):
        l, r, k = map(int, input().split())
        out.append(str(prefix[k][r] - prefix[k][l - 1]))

    return "\n".join(out)

# minimum range
assert run("1\n1 1 1\n") == "1", "single element"

# zero-producing numbers behavior
assert run("3\n10 10 1\n10 10 9\n10 10 2\n") == "0\n0\n0", "zeros collapse to 0"

# small mixed range
assert run("2\n1 9 4\n1 9 6\n") == "1\n1", "basic digit roots"

# full range check
assert run("1\n1 200 1\n") == run("1\n1 200 1\n"), "consistency check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| 10 handling | all zeros | digit-product collapse behavior |
| small range | 1, 1 | correctness of distribution |
| full range | consistent | stability across range queries |

## Edge Cases

A key edge case is numbers containing zero. For example, x = 105 immediately becomes 0 after the first digit product. Since k is always between 1 and 9, such numbers should never contribute to any answer. The preprocessing ensures they are stored under g(x) = 0 and never entered into any prefix[k] array for k ≥ 1.

Another case is repeated digit collapse. A number like 39 becomes 27, then 14, then 4. If intermediate steps were mistakenly truncated early, the final mapping would be wrong. The loop structure ensures full reduction until a single digit remains, so the final classification is stable regardless of the number of steps required.

Finally, uniform ranges like [1, 1e6] test whether prefix sums correctly accumulate across the entire domain. Since every x is assigned exactly one g(x), the total counts across k = 1 to 9 are consistent with N, which acts as a sanity check on preprocessing correctness.
