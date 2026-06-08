---
title: "CF 2014B - Robin Hood and the Major Oak"
description: "The tree produces new leaves every year. In year $i$, it grows $i^i$ leaves. Leaves do not stay forever. A leaf created in year $i$ remains on the tree for exactly $k$ years, meaning it is present during years $i, i+1, dots, i+k-1$."
date: "2026-06-08T12:59:15+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2014
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 974 (Div. 3)"
rating: 800
weight: 2014
solve_time_s: 54
verified: true
draft: false
---

[CF 2014B - Robin Hood and the Major Oak](https://codeforces.com/problemset/problem/2014/B)

**Rating:** 800  
**Tags:** math  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The tree produces new leaves every year. In year $i$, it grows $i^i$ leaves. Leaves do not stay forever. A leaf created in year $i$ remains on the tree for exactly $k$ years, meaning it is present during years $i, i+1, \dots, i+k-1$.

For a given year $n$, we need to determine whether the total number of leaves currently on the tree is even or odd.

A leaf grown in year $i$ is still present in year $n$ if and only if

$$i \le n \le i+k-1.$$

Rearranging gives

$$n-k+1 \le i \le n.$$

Since years start at $1$, the leaves visible in year $n$ come from the interval

$$\max(1, n-k+1), \dots, n.$$

The constraints are the first clue that a direct simulation is impossible. Both $n$ and $k$ can be as large as $10^9$, and there can be up to $10^4$ test cases. Any solution that iterates through years would require billions of operations in the worst case.

The answer only asks whether the total number of leaves is even. That means we only care about parity, not the actual leaf count. This observation turns a huge-number arithmetic problem into a simple counting problem.

A common mistake is trying to compute values such as 10^9^{10^9}. These numbers are unimaginably large and completely unnecessary because parity depends only on whether a value is odd or even.

Another easy mistake is forgetting that only the last $k$ years contribute. For example:

```
n = 5, k = 2
```

Only years $4$ and $5$ matter. Using all years from $1$ through $5$ would produce the wrong answer.

A third subtle case occurs when $k=1$. Then only year $n$ contributes. For example:

```
n = 1, k = 1
```

The tree has exactly $1^1=1$ leaf, which is odd, so the answer is `NO`.

## Approaches

A brute-force solution would identify every year whose leaves are still alive, compute $i^i$, sum them, and check the parity of the final total.

The active years are

$$n-k+1,\dots,n.$$

Even if we ignore the enormous size of $i^i$, this approach requires iterating through up to $10^9$ years. With $10^4$ test cases, the operation count becomes completely infeasible.

The key observation is that parity is much simpler than the actual value.

Consider $i^i$.

If $i$ is even, then $i^i$ is even.

If $i$ is odd, then $i^i$ is odd.

So the parity of $i^i$ is exactly the parity of $i$.

The total parity of the leaf count depends only on how many odd years contribute. Every even year contributes an even number and does not affect parity.

The active interval contains

$$[n-k+1,\, n].$$

The total number of leaves is odd if the number of odd integers in this interval is odd. It is even if the number of odd integers in this interval is even.

Now we only need the parity of the count of odd numbers in a consecutive interval.

Among any two consecutive integers, exactly one is odd. That means the parity of the odd-count depends only on the interval length $k$.

If $k$ is even, the interval contains exactly $k/2$ odd numbers and $k/2$ even numbers. The answer is determined by whether $k/2$ is even or odd.

There is an even simpler observation. Let

$$S = \sum_{i=n-k+1}^{n} i^i.$$

Modulo $2$,

$$S \equiv \sum_{i=n-k+1}^{n} i.$$

The parity of a sum equals the parity of the number of odd terms. In any interval of length $k$, the count of odd numbers is odd exactly when $k \bmod 4$ is $1$ or $2$, and even exactly when $k \bmod 4$ is $0$ or $3$.

An even cleaner derivation comes from examining the ending year $n$. Since only parity matters, the accepted solution reduces to counting odd numbers in the interval. The resulting parity depends only on $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, determine the interval of years whose leaves are still present:

$$[n-k+1,\; n].$$
2. Observe that $i^i$ has the same parity as $i$. Replace every term $i^i$ by its parity contribution.
3. Count how many odd integers lie in the interval.
4. If the count of odd integers is even, output `YES` because the total leaf count is even.
5. Otherwise output `NO`.

A convenient formula for the number of odd integers from $1$ through $x$ is

$$\left\lfloor \frac{x+1}{2} \right\rfloor.$$

So the number of odd integers in $[L,R]$ is

$$\left\lfloor \frac{R+1}{2} \right\rfloor
-
\left\lfloor \frac{L}{2} \right\rfloor.$$

Only the parity of this count matters.

### Why it works

Every even base produces an even power, and every odd base produces an odd power. Modulo $2$, each term $i^i$ behaves exactly like $i$.

The parity of the total leaf count is thus the parity of the number of odd years contributing leaves. The algorithm computes exactly that quantity for the active interval. If the number of odd contributors is even, the total leaf count is even. If the number is odd, the total leaf count is odd. Since parity is preserved at every step, the algorithm always produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
ans = []

for _ in range(t):
    n, k = map(int, input().split())

    l = n - k + 1

    odd_count = (n + 1) // 2 - (l // 2)

    if odd_count % 2 == 0:
        ans.append("YES")
    else:
        ans.append("NO")

print("\n".join(ans))
```

The first step computes the active interval $[n-k+1,n]$. These are exactly the years whose leaves remain alive in year
