---
title: "CF 1882A - Increasing Sequence"
description: "We need to construct a new sequence $b$ of length $n$. Every element of $b$ must be a positive integer. The sequence must be strictly increasing, and for every position $i$, we are forbidden from choosing $bi = ai$."
date: "2026-06-08T22:34:43+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1882
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 899 (Div. 2)"
rating: 800
weight: 1882
solve_time_s: 42
verified: false
draft: false
---

[CF 1882A - Increasing Sequence](https://codeforces.com/problemset/problem/1882/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 42s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct a new sequence $b$ of length $n$.

Every element of $b$ must be a positive integer. The sequence must be strictly increasing, and for every position $i$, we are forbidden from choosing $b_i = a_i$.

Among all sequences that satisfy these rules, we want the smallest possible value of the final element $b_n$.

The input gives several test cases. For each test case we receive the array $a$, and we must determine the minimum achievable ending value.

The constraints are very small. Each test case has at most 100 elements, and there are at most 100 test cases. Even an $O(n^2)$ solution would be completely fine. This means we should focus on finding the simplest correct strategy rather than worrying about advanced optimization.

The tricky part is that choosing a value too large at some position can force all later values to become larger as well. Since we only care about minimizing the last element, every position should be assigned the smallest value that keeps the sequence valid.

A common mistake is to only avoid the forbidden value $a_i$ and forget that the sequence must stay strictly increasing.

For example:

```
n = 2
a = [1, 2]
```

Choosing $b_1 = 2$ avoids $a_1$, but then $b_2$ must be greater than 2 and different from 2, so the answer becomes 3. A better choice is $b_1 = 2$, $b_2 = 3$, which still gives 3, but this example shows that every choice affects future positions.

Another easy mistake is to start from 0 and repeatedly increase only when encountering a forbidden value.

Example:

```
n = 1
a = [1]
```

The smallest positive integer is 1, but it is forbidden. The correct answer is 2.

A careless implementation that ignores positivity might incorrectly output 0 or 1.

A more subtle case occurs when the next smallest valid value equals $a_i$.

```
n = 3
a = [1, 3, 4]
```

The optimal sequence is:

```
b = [2, 4, 5]
```

At position 2, the smallest value greater than the previous element is 3, but 3 is forbidden, so we must sk
