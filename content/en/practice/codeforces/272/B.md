---
title: "CF 272B - Dima and Sequence"
description: "We are given an array of positive integers. For every number x, a recursive function f(x) is defined as: $f(0)=0,quad f(2x)=f(x),quad f(2x+1)=f(x)+1$ The task is to count how many index pairs (i, j) with i < j satisfy f(ai) = f(aj)."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 272
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 167 (Div. 2)"
rating: 1400
weight: 272
solve_time_s: 90
verified: true
draft: false
---

[CF 272B - Dima and Sequence](https://codeforces.com/problemset/problem/272/B)

**Rating:** 1400  
**Tags:** implementation, math  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. For every number `x`, a recursive function `f(x)` is defined as:

$f(0)=0,\quad f(2x)=f(x),\quad f(2x+1)=f(x)+1$

The task is to count how many index pairs `(i, j)` with `i < j` satisfy `f(ai) = f(aj)`.

The recursive definition looks unusual at first, but the transitions reveal what the function actually measures. Dividing an even number by two does not change the value of `f`, while removing the last binary digit `1` increases it by one. Repeatedly applying the recurrence means that `f(x)` counts the number of `1` bits in the binary representation of `x`.

For example:

- `f(4)` becomes `f(2)` then `f(1)` then `f(0)+1 = 1`
- `4` in binary is `100`, which contains one set bit
- `f(7)` becomes `3`, because `111` has three set bits

So the real problem is:

Count how many pairs of numbers have the same number of set bits.

The array size can reach `10^5`, so comparing every pair directly is too expensive. A quadratic algorithm would require roughly:

$\frac{10^5\cdot(10^5-1)}{2}\approx 5\times10^9$

comparisons in the worst case, which is far beyond what fits in two seconds.

The values themselves can be as large as `10^9`, but that is not a problem because the number of set bits in such integers is at most about 30. The small range of possible bit counts becomes the key observation for the optimal solution.

There are a few easy-to-miss edge cases.

Consider:

```
1
8
```

The answer is `0` because there is only one element, so no pair exists. A careless implementation that assumes at least one pair could accidentally produce garbage output.

Another tricky case is:

```
4
1 2 4 8
```

All four numbers contain exactly one set bit. Every pair is valid, so the answer is:

$\binom{4}{2}=6$

A buggy solution that only compares adjacent elements would incorrectly return `3`.

One more subtle scenario is:

```
5
3 5 6 9 10
```

All these numbers contain exactly two set bits. The correct answer is:

$\binom{5}{2}=10$

This catches implementations that misunderstand the recurrence and compare numeric values instead of set-bit counts.

## Approaches

The most direct solution is brute force. For every pair `(i, j)`, compute `f(ai)` and `f(aj)` and compare them. Since there are `O(n^2)` pairs, this quickly becomes too slow when `n = 10^5`.

The brute-force idea is still useful because it exposes the actual structure of the problem. We do not care about the numbers themselves. We only care about how many set bits each number contains.

The recurrence defines exactly the population count of a number. Dividing by two removes the last binary digit. If that digit is `0`, the count does not change. If the digit is `1`, the count increases by one. Eventually every number reaches zero, and the total number of odd steps equals the number of `1` bits.

Once we realize that `f(x)` is simply the set-bit count, the problem becomes a frequency-counting problem.

Suppose several numbers share the same bit count. If a particular count appears `k` times, then every pair among those `k` elements is valid. The number of valid pairs contributed by this group is:

$\binom{k}{2}=\frac{k(k-1)}{2}$

So the optimal algorithm is:

1. Compute the set-bit count of every number.
2. Count how many times each count appears.
3. Sum `k * (k - 1) / 2` over all frequencies.

This reduces the complexity from quadratic to linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) to O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array size and the array values.
2. For each number, compute how many set bits it contains.

In Python, this can be done efficiently with `bin(x).count('1')`.
3. Store how many numbers produce each bit count.

A dictionary works well because the possible counts are small and sparse.
4. After processing the entire array, iterate through the frequencies.
5. If a particular bit count appears `k` times, add:

$\frac{k(k-1)}{2}$

to the answer.

Every unordered pair inside that group satisfies the condition.
6. Print the final answer.

### Why it works

Two numbers contribute to the answer if and only if their values of `f(x)` are equal. The recurrence defines `f(x)` as the number of set bits in `x`. The algorithm groups numbers by this exact quantity.

Inside one group of size `k`, every pair is valid, and no pair across different groups is valid. Counting combinations inside each group counts every valid pair exactly once and never counts an invalid pair.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    freq = defaultdict(int)

    for x in arr:
        bits = bin(x).count('1')
        freq[bits] += 1

    ans = 0

    for k in freq.values():
        ans += k * (k - 1) // 2

    print(ans)

solve()
```

The first part reads the input array. Since the constraints are large, the solution uses fast input with `sys.stdin.readline`.

The dictionary `freq` stores how many numbers share the same set-bit count. For every value `x`, the expression `bin(x).count('1')` computes its population count directly from the binary representation.

After all frequencies are known, the solution computes the number of unordered pairs inside each group. Integer division `// 2` is necessary because the formula produces an integer result.

The answer can become large. For example, if all `10^5` numbers belong to the same group, the result is about `5 × 10^9`. Python integers handle this safely without overflow.

## Worked Examples

### Sample 1

Input:

```
3
1 2 4
```

| Number | Binary | Set bits | Frequency after insertion |
| --- | --- | --- | --- |
| 1 | 1 | 1 | {1: 1} |
| 2 | 10 | 1 | {1: 2} |
| 4 | 100 | 1 | {1: 3} |

Now the only group has size `3`.

| Bit count | Frequency | Pair contribution |
| --- | --- | --- |
| 1 | 3 | 3 |

Final answer: `3`.

This example shows that completely different numeric values can still belong to the same group because only the number of set bits matters.

### Example 2

Input:

```
5
3 5 6 8 9
```

| Number | Binary | Set bits | Frequency after insertion |
| --- | --- | --- | --- |
| 3 | 11 | 2 | {2: 1} |
| 5 | 101 | 2 | {2: 2} |
| 6 | 110 | 2 | {2: 3} |
| 8 | 1000 | 1 | {2: 3, 1: 1} |
| 9 | 1001 | 2 | {2: 4, 1: 1} |

Now compute contributions:

| Bit count | Frequency | Pair contribution |
| --- | --- | --- |
| 2 | 4 | 6 |
| 1 | 1 | 0 |

Final answer: `6`.

This trace demonstrates that groups are independent. Numbers with different set-bit counts never contribute to the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number is processed once |
| Space | O(1) to O(n) | Frequency map stores bit-count groups |

The maximum number of distinct bit counts is tiny because numbers are at most `10^9`, so the practical memory usage is extremely small. The linear running time easily fits within the limits for `n = 10^5`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def solve():
    input = sys.stdin.readline

    n = int(input())
    arr = list(map(int, input().split()))

    freq = defaultdict(int)

    for x in arr:
        bits = bin(x).count('1')
        freq[bits] += 1

    ans = 0

    for k in freq.values():
        ans += k * (k - 1) // 2

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("3\n1 2 4\n") == "3", "sample 1"

# minimum size
assert run("1\n7\n") == "0", "single element"

# all values with same bit count
assert run("5\n3 5 6 9 10\n") == "10", "all pairs valid"

# mixed groups
assert run("6\n1 2 3 4 7 8\n") == "6", "multiple frequency groups"

# powers of two
assert run("4\n1 2 4 8\n") == "6", "all have one set bit"

# no valid pairs
assert run("4\n1 3 7 15\n") == "0", "all bit counts distinct"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` | Minimum-size input |
| `5 / 3 5 6 9 10` | `10` | All elements in one group |
| `6 / 1 2 3 4 7 8` | `6` | Multiple independent groups |
| `4 / 1 2 4 8` | `6` | Powers of two all match |
| `4 / 1 3 7 15` | `0` | No valid pairs |

## Edge Cases

Consider the smallest possible input:

```
1
8
```

The algorithm computes one set-bit count:

| Number | Set bits |
| --- | --- |
| 8 | 1 |

The frequency map becomes `{1: 1}`. The contribution is:

$\frac{1\cdot0}{2}=0$

so the output is correctly `0`.

Now consider a case where every number belongs to the same group:

```
4
1 2 4 8
```

All four numbers contain one set bit.

| Bit count | Frequency |
| --- | --- |
| 1 | 4 |

The algorithm computes:

$\frac{4\cdot3}{2}=6$

which counts all unordered pairs correctly.

Finally, consider distinct groups:

```
4
1 3 7 15
```

The set-bit counts are `1, 2, 3, 4`.

| Bit count | Frequency |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

Every group has size one, so every contribution is zero. The algorithm correctly prints `0`, confirming that it never mixes elements from different groups.
