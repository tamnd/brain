---
title: "CF 433A - Kitahara Haruki's Gift"
description: "We have a collection of apples where every apple weighs either 100 grams or 200 grams. The task is to split all apples into two groups so that both groups have exactly the same total weight. The input gives the number of apples and then the weight of each apple."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 433
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 248 (Div. 2)"
rating: 1100
weight: 433
solve_time_s: 102
verified: false
draft: false
---

[CF 433A - Kitahara Haruki's Gift](https://codeforces.com/problemset/problem/433/A)

**Rating:** 1100  
**Tags:** brute force, implementation  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We have a collection of apples where every apple weighs either 100 grams or 200 grams. The task is to split all apples into two groups so that both groups have exactly the same total weight.

The input gives the number of apples and then the weight of each apple. The output is simply whether such a fair division exists.

The constraints are tiny. There are at most 100 apples, so even a brute-force subset search is theoretically possible for small inputs, but a full subset enumeration would still require checking up to $2^{100}$ possibilities, which is astronomically large. The problem is not really about optimization tricks or advanced algorithms. The key is recognizing the structure created by having only two possible weights.

The first observation is that the total weight must be even. If the total weight is odd, splitting it equally is impossible immediately.

The second observation is more subtle. Since every apple weighs a multiple of 100, we can think in units of 100 grams. Then each apple is either weight 1 or weight 2. We are trying to form half of the total sum.

A common mistake is to only check whether the total sum is even. Consider this input:

```
1
200
```

The total weight is 200, which is even, but we cannot split one apple into two 100-gram halves. The correct answer is `NO`.

Another tricky case happens when the target half-sum is odd in 100-gram units and we have no 100-gram apples to adjust parity.

Example:

```
3
200 200 200
```

The total weight is 600, so each person would need 300 grams. But every apple weighs 200 grams, so no combination can produce 300. The correct answer is `NO`.

A careless implementation that only checks divisibility by 2 would incorrectly return `YES`.

Now consider:

```
4
100 100 200 200
```

The total is 600, so each side needs 300. One side can take `100 + 200`, and the other side gets the remaining `100 + 200`. The answer is `YES`.

The parity of the number of 100-gram apples is what fixes the situations where half the sum is odd in 100-gram units.

## Approaches

The brute-force approach is straightforward. We can try every subset of apples, compute its total weight, and check whether it equals half of the total sum. This works because every valid partition corresponds to some subset whose weight is exactly half the total.

The problem is the number of subsets. With $n = 100$, the total number of subsets is $2^{100}$, which is completely infeasible. Even checking a billion subsets per second would still take far longer than the age of the universe.

The structure of the weights gives us a much simpler route. Since every apple is either 100 or 200 grams, only two counts actually matter:

```
count100 = number of 100-gram apples
count200 = number of 200-gram apples
```

Let the total weight be:

$$100 \cdot count100 + 200 \cdot count200$$

If the total weight is odd, equal division is impossible.

Otherwise, each person needs half the total. In units of 100 grams, each person needs:

$$count100 + 2 \cdot count200
\over 2$$

Now parity becomes the entire problem.

If the number of 200-gram apples is odd and there are no 100-gram apples, then the target becomes odd while every available apple contributes an even amount. We cannot build an odd target using only even numbers.

Outside of that case, a valid split always exists.

The brute-force works because it directly searches all partitions, but it fails because the search space grows exponentially. The observation that weights only have two possible values reduces the problem to a few parity checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of apples and the list of weights.
2. Count how many apples weigh 100 grams and how many weigh 200 grams.
3. Compute the total weight.
4. If the total weight is odd, print `NO`.

An odd total can never be split into two equal integers.
5. If the number of 100-gram apples is zero and the number of 200-gram apples is odd, print `NO`.

In this situation, each side would need an odd multiple of 100 grams, but every available apple contributes 200 grams. Reaching an odd target is impossible.
6. Otherwise, print `YES`.

### Why it works

Every achievable weight is a multiple of 100, so we can reason entirely in 100-gram units.

If the total sum is odd, no equal partition exists.

After dividing by 100, every apple contributes either 1 or 2 units. If we have at least one 100-gram apple, we can adjust parity freely and construct the needed half-sum whenever the total is even.

The only impossible even-total situation occurs when all apples are 200 grams and their count is odd. Then the target half-sum is odd, but every selected apple contributes an even value, so no subset can reach it.

These checks cover all possible configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    apples = list(map(int, input().split()))

    count100 = apples.cou
```
