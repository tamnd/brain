---
title: "CF 1526B - I Hate 1111"
description: "Every allowed number has a very special form: $$11, 111, 1111, 11111,dots$$ For each query, we are given a target value $x$, and we must determine whether it can be represented as a sum of these numbers, with unlimited reuse of each value."
date: "2026-06-10T17:19:12+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1526
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 723 (Div. 2)"
rating: 1400
weight: 1526
solve_time_s: 123
verified: true
draft: false
---

[CF 1526B - I Hate 1111](https://codeforces.com/problemset/problem/1526/B)

**Rating:** 1400  
**Tags:** dp, math, number theory  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Every allowed number has a very special form:

$$11,\ 111,\ 1111,\ 11111,\dots$$

For each query, we are given a target value $x$, and we must determine whether it can be represented as a sum of these numbers, with unlimited reuse of each value.

The first reaction is to view this as an unbounded knapsack problem. We have infinitely many uses of each denomination and want to know whether a given sum is reachable.

The constraints completely change how we should think about the problem. There can be up to $10^4$ test cases, and each value can be as large as $10^9$. Any dynamic programming approach that depends directly on $x$ is impossible. Even an $O(x)$ algorithm for a single test case would already be far too slow.

The interesting part is that all allowed numbers are built from repeated digit 1s. Looking more closely,

$$111 = 10 \cdot 11 + 1$$

and similarly,

$$1111 = 100 \cdot 11 + 11$$

Every allowed number larger than 11 can be expressed using some number of 111s and 11s. This structure lets us reduce the problem to a much smaller search.

A common mistake is assuming that every sufficiently large number works without proving why. For example:

Input:

```
1
69
```

Output:

```
NO
```

Although 69 is fairly large, no combination of allowed numbers produces it.

Another easy mistake is trying only one copy of 111. Consider:

Input:

```
1
144
```

Output:

```
YES
```

because

$$144 = 111 + 11 + 11 + 11.$$

Any approach that checks only a few hand-picked combinations would miss cases like this.

The smallest values also require care. For example:

Input:

```
1
1
```

Output:

```
NO
```

The number 1 itself is not an allowed summand, so small values are not automatically reachable.

## Approaches

A brute-force solution would treat every allowed number as a coin denomination and perform an unbounded knapsack computation. Since $x$ may be as large as $10^9$, such a DP would require billions of states and is completely infeasible.

The key observation comes from the relationship between 11 and 111.

Since

$$111 \equiv 1 \pmod{11},$$

every time we use one copy of 111, the remainder modulo 11 increases by exactly 1.

Suppose we use $k$ copies of 111. The remaining value becomes

$$x - 111k.$$

If the remainder can be filled using only 11s, then

$$x - 111k$$

must be non-negative and divisible by 11.

This transforms the problem into checking whether there exists some $k$ such that

$$x - 111k \ge 0$$

and

$$(x - 111k) \bmod 11 = 0.$$

At first glance $k$ could be large, but modulo 11 changes everything. Since

$$111 \equiv 1 \pmod{11},$$

the divisibility condition becomes

$$x - k \equiv 0 \pmod{11}.$$

Thus $k$ must be congruent to $x \pmod{11}$.

Let

$$r = x \bmod 11.$$

The smallest non-negative candidate is $k=r$. If even this smallest valid choice makes $111k > x$, then every larger valid choice is worse and no solution exists.

So the entire problem reduces to checking

$$111 \cdot (x \bmod 11) \le x.$$

This yields an $O(1)$ solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | O(x) | O(x) | Too slow |
| Optimal Number Theory | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the target value $x$.
2. Compute the remainder

$$r = x \bmod 11.$$

Any valid number of 111s must satisfy $k \equiv r \pmod{11}$.
3. Choose the smallest non-negative candidate, $k=r$.

Every other valid candidate is $r+11, r+22,\dots$, which uses even more copies of 111.
4. Check whether

$$111r \le x.$$

If true, then using $r$ copies of 111 leaves

$$x-111r,$$

which is non-negative and divisible by 11.
5. Output `"YES"` if the condition holds, otherwise output `"NO"`.

### Why it works

Any representation can be rewritten using only 111s and 11s. Suppose a solution uses $k$ copies of 111. Then $x-111k$ must be a non-negative multiple of 11. Since $111 \equiv 1 \pmod{11}$, this requires $k \equiv x \pmod{11}$.

Among all values satisfying that congruence, the smallest non-negative one is $r=x\bmod 11$. If $111r>x$, then every other valid candidate $r+11m$ uses even more 111s and also exceeds $x$. No solution exists.

If $111r\le x$, then $x-111r$ is non-negative and divisible by 11, giving a valid construction. The algorithm is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

ans = []
for _ in range(t):
    x = int(input())
    r = x % 11

    if 111 * r <= x:
        ans.append("YES")
    else:
        ans.append("NO")

print("\n".join(ans))
```

The implementation follows the mathematical characterization directly.

For each test case we compute the remainder modulo 11. That remainder is the smallest possible number of 111s that can satisfy the divisibility requirement.

The condition `111 * r <= x` checks whether those copies of 111 fit inside the target sum. If they do, the remaining value is automatically a non-negative multiple of 11, so it can be completed using only 11s.

No loops depend on the size of $x$, which is crucial because values can be as large as $10^9$.

## Worked Examples

### Example 1

Input:

```
33
```

| x | r = x % 11 | 111 * r | Condition |
| --- | --- | --- | --- |
| 33 | 0 | 0 | 0 ≤ 33 |

Output:

```
YES
```

Since the remainder is zero, we need no copies of 111. The entire value is simply three copies of 11.

### Example 2

Input:

```
144
```

| x | r = x % 11 | 111 * r | Condition |
| --- | --- | --- | --- |
| 144 | 1 | 111 | 111 ≤ 144 |

Output:

```
YES
```

Using one copy of 111 leaves

$$144 - 111 = 33,$$

which is divisible by 11. The construction is $111+11+11+11$.

### Example 3

Input:

```
69
```

| x | r = x % 11 | 111 * r | Condition |
| --- | --- | --- | --- |
| 69 | 3 | 333 | 333 > 69 |

Output:

```
NO
```

The smallest valid number of 111s would be three, but that already exceeds the target. Every other valid choice uses even more copies of 111, so no representation exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Constant amount of arithmetic per test case |
| Space | O(1) | Only a few variables are used |

Even with $10^4$ test cases, the program performs only a handful of arithmetic operations per query. It easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())

    ans = []
    for _ in range(t):
        x = int(input())
        ans.append("YES" if 111 * (x % 11) <= x else "NO")

    return "\n".join(ans)

# provided sample
assert run("3\n33\n144\n69\n") == "YES\nYES\nNO", "sample"

# minimum value
assert run("1\n1\n") == "NO", "smallest impossible value"

# exactly one 111
assert run("1\n111\n") == "YES", "single denomination"

# boundary around first reachable large values
assert run("2\n110\n112\n") == "YES\nNO", "near 111"

# maximum constraint
assert run("1\n1000000000\n") == "YES", "largest input"

# multiple small impossible values
assert run("5\n1\n2\n3\n4\n5\n") == "NO\nNO\nNO\nNO\nNO", "small values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `NO` | Smallest value cannot be formed |
| `111` | `YES` | Single 111 works directly |
| `110, 112` | `YES, NO` | Boundary around the first 111 |
| `1000000000` | `YES` | Maximum constraint handled correctly |
| `1,2,3,4,5` | All `NO` | Small unreachable values |

## Edge Cases

Consider the smallest input:

```
1
1
```

We compute $r=1$. Then

$$111 \cdot 1 = 111 > 1.$$

The algorithm prints `"NO"`. There is no way to form 1 because every allowed summand is at least 11.

Consider a value just below 111:

```
1
110
```

Here $r=0$, so $111r=0\le110$. The algorithm prints `"YES"`. Indeed,

$$110 = 10 \cdot 11.$$

This case shows why numbers smaller than 111 are not automatically impossible.

Consider a value slightly above 111:

```
1
112
```

We get $r=2$. Then

$$111 \cdot 2 = 222 > 112.$$

The algorithm prints `"NO"`. A careless approach might think that being larger than 111 is enough, but 112 cannot be represented.

Consider the sample counterexample:

```
1
69
```

We obtain $r=3$. Since $333>69$, the answer is `"NO"`. Every feasible solution would require a number of 111s congruent to 3 modulo 11, and the smallest such choice already exceeds the target. This demonstrates the necessity of the modular argument.
