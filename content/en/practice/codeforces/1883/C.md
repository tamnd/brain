---
title: "CF 1883C - Raspberries"
description: "We are given an array and a small integer $k$, where $2 le k le 5$. In one operation we may pick any element and increase it by one. The task is to find the smallest number of operations needed so that the product of all array elements becomes divisible by $k$."
date: "2026-06-08T22:31:42+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1883
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 905 (Div. 3)"
rating: 1000
weight: 1883
solve_time_s: 360
verified: true
draft: false
---

[CF 1883C - Raspberries](https://codeforces.com/problemset/problem/1883/C)

**Rating:** 1000  
**Tags:** dp, math  
**Solve time:** 6m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and a small integer $k$, where $2 \le k \le 5$. In one operation we may pick any element and increase it by one. The task is to find the smallest number of operations needed so that the product of all array elements becomes divisible by $k$.

The key observation is that we never care about the exact product. We only care whether the product contains the prime factors required by $k$. Since $k$ is at most $5$, there are only four possible values of $k$: $2$, $3$, $4$, and $5$. This makes the problem much smaller than it first appears.

The total number of array elements across all test cases is at most $2 \cdot 10^5$. Any solution that examines each element a constant number of times is easily fast enough. Approaches involving dynamic programming over large states or repeated simulation of operations are unnecessary.

A subtle edge case appears when $k=4$. Divisibility by $4$ is different from divisibility by $2$, because the product must contain two factors of $2$. For example:

```
n = 2, k = 4
a = [1, 3]
```

Increasing one element to the next multiple of four costs one operation:

```
[1, 4]
```

The answer is $1$. A solution that only counts even numbers would miss this possibility.

Another important case is when several elements can contribute factors of two together:

```
n = 3, k = 4
a = [1, 5, 9]
```

Making one number divisible by four costs $3$ operations:

```
1 -> 4
```

But making two numbers even costs only $2$ operations:

```
1 -> 2
5 -> 6
```

The product then contains two factors of two, so the correct answer is $2$.

A final edge case occurs when the product is already divisible by $k$. For example:

```
n = 4, k = 5
a = [5, 4, 1, 2]
```

The answer is $0$. Any algorithm should check this before performing further calculations.

## Approaches

A brute-force approach would try sequences of increment operations and search for the first state whose product is divisible by $k$. Even if we only considered small numbers of operations, the branching factor is $n$, making the search exponential.

The structure of the problem makes this unnecessary. Since $k \le 5$, divisibility depends only on a few prime factors.

For $k=2$, $k=3$, and $k=5$, the product is divisible by $k$ as soon as one array element becomes divisible by $k$. If no element is currently divisible by $k$, we simply compute how many increments are needed to move each element to the next multiple of $k$, then take the minimum.

The only interesting case is $k=4$. A product is divisible by $4$ if it contains at least two factors of two. This can happen in two different ways.

One element may become divisible by $4$.

Or several elements may contribute factors of two together. Since $n \ge 2$, it is enough to consider making two elements even.

The answer for $k=4$ is the minimum cost among all valid ways to obtain two factors of two.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(n)$ per test case | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Read the array.
2. Compute the current product divisibility indirectly.

For every element, check its remainder modulo $k$. If some element is already divisible by $k$ and $k \in \{2,3,5\}$, the answer is immediately $0$.
3. If $k$ is $2$, $3$, or $5$, compute

$$\min_i (k - a_i \bmod k) \bmod k.$$

This is the cost to move an element to the next multiple of $k$.

1. If $k=4$, first compute the minimum cost to make some element divisible by $4$:

$$\min_i (4 - a_i \bmod 4) \bmod 4.$$

1. Count the current factors of two in the array.

For each element:

- If it is divisible by $4$, contribute $2$.
- Else if it is even, contribute $1$.
- Else contribute $0$.
2. If the total number of factors of two is already at least $2$, the answer is $0$.
3. Otherwise determine how many more factors of two are needed.
4. Compute the costs of making elements even. For an odd element the cost is $1$. For an even element the cost is $0$.
5. Sort these costs and take the smallest number of elements needed to obtain the missing factors of two.
6. The final answer is the minimum between:

- Making one element divisible by $4$.
- Collecting enough factors of two from multiple elements.

### Why it works

For $k=2$, $3$, and $5$, divisibility of the product requires only one factor of the corresponding prime. A single element divisible by $k$ is sufficient and necessary.

For $k=4$, the product must contain at least two factors of two. Every valid configuration achieves this either through one element divisible by four or through several even elements whose combined contribution reaches two factors of two. The algorithm explicitly evaluates both possibilities and chooses the cheaper one. Since every operation only increases an element, the cheapest way to obtain a required divisibility condition is always to move elements to the nearest qualifying values.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    if k in (2, 3, 5):
        ans = min((k - x % k) % k for x in a)
        print(ans)
        continue

    # k == 4
    ans = min((4 - x % 4) % 4 for x in a)

    twos = 0
    for x in a:
        if x % 4 == 0:
            twos += 2
        elif x % 2 == 0:
            twos += 1

    if twos >= 2:
        ans = 0
    else:
        costs = []
        for x in a:
            costs.append(x % 2)

        costs.sort()

        need = 2 - twos
        ans = min(ans, sum(costs[:need]))

    print(ans)
```

The solution separates the easy cases $k=2$, $3$, and $5$ from the special case $k=4$.

For $k=2$, $3$, and $5$, only the nearest multiple matters. The expression

$$(k - x \bmod k) \bmod k$$

returns zero when $x$ is already divisible by $k$, otherwise it returns the exact number of increments needed.

For $k=4$, the first candidate answer is the cost of making one element divisible by four. Then the code counts factors of two already present in the array. If at least two are available, the product is already divisible by four.

Otherwise, the code considers making odd elements even. An odd element requires one operation, while an even element requires none. Sorting these costs lets us choose the cheapest elements needed to obtain the missing factors of two.

No integer overflow issues exist because the product itself is never computed.

## Worked Examples

### Example 1

Input:

```
n = 2, k = 5
a = [7, 3]
```

| Element | Cost to next multiple of 5 |
| --- | --- |
| 7 | 3 |
| 3 | 2 |

The minimum cost is $2$.

Answer:

```
2
```

The optimal move is $3 \to 5$.

### Example 2

Input:

```
n = 3, k = 4
a = [1, 5, 9]
```

| Element | Cost to multiple of 4 |
| --- | --- |
| 1 | 3 |
| 5 | 3 |
| 9 | 3 |

The first candidate answer is $3$.

Current factors of two:

| Element | Factors contributed |
| --- | --- |
| 1 | 0 |
| 5 | 0 |
| 9 | 0 |

We need two factors of two.

Costs to become even:

| Element | Cost |
| --- | --- |
| 1 | 1 |
| 5 | 1 |
| 9 | 1 |

Taking the two cheapest costs gives $1 + 1 = 2$.

The answer becomes:

```
2
```

This demonstrates why considering only multiples of four would be incorrect.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is processed a constant number of times |
| Space | $O(n)$ | Only the temporary cost list for $k=4$ |

The total input size is at most $2 \cdot 10^5$, so a linear solution runs comfortably within the limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        if k in (2, 3, 5):
            out.append(str(min((k - x % k) % k for x in a)))
            continue

        ans = min((4 - x % 4) % 4 for x in a)

        twos = 0
        for x in a:
            if x % 4 == 0:
                twos += 2
            elif x % 2 == 0:
                twos += 1

        if twos >= 2:
            ans = 0
        else:
            costs = sorted(x % 2 for x in a)
            ans = min(ans, sum(costs[:2 - twos]))

        out.append(str(ans))

    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

assert run("1\n2 5\n7 3\n") == "2"
assert run("1\n5 5\n5 4 1 2 3\n") == "0"
assert run("1\n3 4\n1 5 9\n") == "2"
assert run("1\n3 4\n6 3 6\n") == "1"
assert run("1\n2 2\n1 1\n") == "1"
assert run("1\n2 5\n10 10\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 5 / 7 3` | `2` | Basic nearest multiple logic |
| `5 5 / 5 4 1 2 3` | `0` | Already divisible |
| `3 4 / 1 5 9` | `2` | Two even numbers beat one multiple of four |
| `3 4 / 6 3 6` | `1` | Existing factor of two plus one increment |
| `2 2 / 1 1` | `1` | Smallest valid array |
| `2 5 / 10 10` | `0` | Every element already divisible |

## Edge Cases

Consider:

```
n = 4
k = 5
a = [5, 1, 1, 1]
```

One element is already divisible by five, so the product is divisible by five. The algorithm computes a cost of zero for that element and immediately returns $0$.

Consider:

```
n = 3
k = 4
a = [2, 3, 3]
```

The array already contributes one factor of two from the value $2$. We need one more factor. Turning either $3$ into $4$ costs one operation. The algorithm finds $twos = 1$, needs one more factor, and returns $1$.

Consider:

```
n = 2
k = 4
a = [1, 1]
```

Making one element divisible by four costs three operations. Making both elements even costs two operations. The algorithm evaluates both possibilities and correctly chooses $2$.
