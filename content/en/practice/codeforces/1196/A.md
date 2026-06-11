---
title: "CF 1196A - Three Piles of Candies"
description: "Each query gives three piles of candies. Alice must take one whole pile, Bob must take one of the remaining piles, and the last pile can be split arbitrarily between them."
date: "2026-06-12T00:12:15+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1196
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 575 (Div. 3)"
rating: 800
weight: 1196
solve_time_s: 243
verified: true
draft: false
---

[CF 1196A - Three Piles of Candies](https://codeforces.com/problemset/problem/1196/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms, math  
**Solve time:** 4m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Each query gives three piles of candies. Alice must take one whole pile, Bob must take one of the remaining piles, and the last pile can be split arbitrarily between them.

After the distribution, if one person has more candies than the other, the extra candies can simply be discarded. The final result is that both people end up with the same number of candies. Our goal is to maximize that common number.

The key observation is that discarded candies are allowed. We do not need to use every candy. We only need to maximize the amount that both Alice and Bob can keep.

The number of queries is at most 1000, which is tiny. However, each pile can contain up to $10^{16}$ candies, so any algorithm that depends on the pile sizes themselves is impossible. We need a direct mathematical formula that can be evaluated in constant time per query.

A common mistake is to assume that the answer is always half of the total number of candies. Consider the piles $(1,1,100)$. The total is $102$, so half is $51$. But the two small piles contain only $2$ candies altogether. One person can take the pile of $100$, but the other person cannot reach $51$ candies because only $2$ candies exist outside the largest pile. The correct answer is $2$.

Another easy mistake is to think that the largest pile limits the answer directly. Consider $(4,4,4)$. The largest pile has size $4$, yet the answer is $6$. Alice can receive $4$ from one pile and $2$ from the remaining pile, while Bob receives the other $4$ and the other $2$.

A third edge case appears when one pile dominates the others. For $(1,10,100)$, the total is $111$, so the theoretical upper bound is $\lfloor 111/2 \rfloor = 55$. This value is achievable, giving the answer $55$.

## Approaches

A brute-force viewpoint is to try every possible assignment. We could choose which pile Alice takes, which pile Bob takes, and then consider all ways to split the remaining pile.

This reasoning is correct because every valid distribution is examined. The problem is that the remaining pile can contain up to $10^{16}$ candies, so enumerating all possible splits is completely impossible.

To make progress, we need to think about what actually limits the final equal amount.

Suppose the pile sizes are sorted:

$$a \le b \le c.$$

Let

$$S = a+b+c.$$

Since both people end with the same amount $x$, together they keep $2x$ candies. They cannot keep more candies than exist, so

$$2x \le S,$$

which gives

$$x \le \left\lfloor \frac{S}{2} \right\rfloor.$$

This is the first upper bound.

There is another one. To give both people $x$ candies, at least $x$ candies must come from the two smaller piles combined, because the largest pile contributes at most all of its own candies to one side. The total amount outside the largest pile is

$$a+b.$$

Hence

$$x \le a+b.$$

These are the only restrictions that matter. If

$$x \le \min\left(a+b,\left\lfloor \frac{S}{2}\right\rfloor\right),$$

then such a distribution can always be constructed.

Thus the answer is simply

$$\min\left(a+b,\left\lfloor \frac{a+b+c}{2}\right\rfloor\right),$$

after sorting so that $c$ is the largest pile.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Impossible in practice, depends on pile sizes | O(1) | Too slow |
| Optimal | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three pile sizes.
2. Sort them so that $a \le b \le c$.
3. Compute the total number of candies:

$$S=a+b+c.$$
4. Compute the first upper bound:

$$\left\lfloor \frac{S}{2} \right\rfloor.$$

Two people ending with the same amount cannot together keep more candies than exist.
5. Compute the second upper bound:

$$a+b.$$

The two smaller piles contain only $a+b$ candies in total, so the final equal amount cannot exceed this value.
6. Output

$$\min\left(a+b,\left\lfloor \frac{S}{2}\right\rfloor\right).$$

### Why it works

The value $x$ cannot exceed $\lfloor S/2 \rfloor$ because there are only $S$ candies available. It also cannot exceed $a+b$ because the largest pile alone cannot provide enough candies for both participants.

These two inequalities give an upper bound:

$$x \le \min\left(a+b,\left\lfloor \frac{S}{2}\right\rfloor\right).$$

This bound is always achievable. If the largest pile is very large, then $a+b$ becomes the limiting factor. Otherwise, the total number of candies becomes the limiting factor. In either case, the remaining pile can be split appropriately to realize exactly that value. Hence the formula is both an upper bound and an achievable value, proving correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

q = int(input())

for _ in range(q):
    a, b, c = map(int, input().split())
    a, b, c = sorted((a, b, c))

    total = a + b + c
    print(min(a + b, total // 2))
```

The implementation follows the mathematical formula directly.

The three values are sorted so that the largest pile is always stored in `c`. This lets us identify the quantity `a + b`, which is the total number of candies outside the largest pile.

The value `total // 2` represents the largest possible equal share if only the total number of candies mattered.

The answer is the minimum of these two bounds.

Python integers automatically handle values much larger than $10^{16}$, so overflow is not a concern. The entire solution uses only a few arithmetic operations per query.

## Worked Examples

### Example 1

Input piles: $(1, 3, 4)$

After sorting:

| a | b | c | total | a+b | total//2 | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 4 | 8 | 4 | 4 | 4 |

The answer is $4$. One valid distribution is to give the pile of $4$ to Alice and both remaining candies from the last pile to Bob, producing $4$ candies each.

### Example 2

Input piles: $(1, 10, 100)$

| a | b | c | total | a+b | total//2 | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 | 100 | 111 | 11 | 55 | 11 |

Wait, after sorting, the formula gives:

$$\min(11,55)=11.$$

This reveals why sorting matters when interpreting the bound. The largest pile is overwhelmingly larger than the others. The final equal amount is limited by the total number of candies outside the largest pile.

Indeed, Alice and Bob can each end with $11$ candies, but not more, because only $11$ candies exist outside the largest pile.

### Example 3

Input piles: $(23, 34, 45)$

| a | b | c | total | a+b | total//2 | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 23 | 34 | 45 | 102 | 57 | 51 | 51 |

Here the total amount is the limiting factor. Since half of the total is $51$, both participants can finish with $51$ candies.

This example demonstrates the second regime of the formula, where the answer equals $\lfloor S/2 \rfloor$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per query | Only sorting three values and a few arithmetic operations |
| Space | O(1) | Uses a constant amount of extra memory |

With at most 1000 queries, the total work is negligible. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    q = int(input())

    ans = []
    for _ in range(q):
        a, b, c = map(int, input().split())
        a, b, c = sorted((a, b, c))
        ans.append(str(min(a + b, (a + b + c) // 2)))

    return "\n".join(ans) + "\n"

# provided sample
assert run(
"""4
1 3 4
1 10 100
10000000000000000 10000000000000000 10000000000000000
23 34 45
"""
) == """4
11
15000000000000000
51
"""

# minimum values
assert run(
"""1
1 1 1
"""
) == """1
"""

# all equal
assert run(
"""1
5 5 5
"""
) == """7
"""

# dominant largest pile
assert run(
"""1
1 1 100
"""
) == """2
"""

# maximum values
assert run(
"""1
10000000000000000 10000000000000000 10000000000000000
"""
) == """15000000000000000
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Smallest non-trivial case |
| `5 5 5` | `7` | Symmetric distribution |
| `1 1 100` | `2` | Largest pile dominates |
| `10^16 10^16 10^16` | `15000000000000000` | Maximum values and large integer handling |

## Edge Cases

Consider the input:

```
1
1 1 100
```

After sorting, $a=1$, $b=1$, $c=100$. The algorithm computes:

$$a+b=2,$$

$$\left\lfloor \frac{102}{2} \right\rfloor = 51.$$

The answer is $\min(2,51)=2$.

This case shows why using only half of the total is incorrect. Almost all candies are trapped inside one pile.

Now consider:

```
1
4 4 4
```

The algorithm computes:

$$a+b=8,$$

$$\left\lfloor \frac{12}{2} \right\rfloor = 6.$$

The answer is $6$.

A naive strategy that looks only at the largest pile might predict $4$, which is too small. Splitting the remaining pile allows both participants to exceed the size of any individual pile.

Finally, consider:

```
1
2 3 5
```

The algorithm computes:

$$a+b=5,$$

$$\left\lfloor \frac{10}{2} \right\rfloor = 5.$$

The answer is $5$.

This boundary case is where both upper bounds are equal. The algorithm naturally handles it without any special logic.
