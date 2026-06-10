---
title: "CF 1542B - Plus and Multiply"
description: "We start from the number $1$. From any number already in the set, we may perform either of two operations: multiply by $a$, or add $b$. After applying these operations any number of times in any order, we obtain an infinite set of reachable values."
date: "2026-06-10T14:17:49+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1542
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 729 (Div. 2)"
rating: 1500
weight: 1542
solve_time_s: 980
verified: true
draft: false
---

[CF 1542B - Plus and Multiply](https://codeforces.com/problemset/problem/1542/B)

**Rating:** 1500  
**Tags:** constructive algorithms, math, number theory  
**Solve time:** 16m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We start from the number $1$. From any number already in the set, we may perform either of two operations: multiply by $a$, or add $b$. After applying these operations any number of times in any order, we obtain an infinite set of reachable values.

For each test case, we are given $n$, $a$, and $b$. The task is to determine whether $n$ can be generated starting from $1$.

The constraints are the first clue that brute force cannot work. There are up to $10^5$ test cases, and each parameter can be as large as $10^9$. Any approach that explores reachable states directly would immediately explode, because the set is infinite and even restricting ourselves to values up to $n$ could require examining billions of numbers.

The solution must process each test case in roughly logarithmic time. Since $a \le 10^9$, repeated multiplication by $a$ exceeds $10^9$ after at most about 30 steps when $a \ge 2$. That suggests we should focus on powers of $a$, not on the entire generated set.

Several edge cases are easy to miss.

Consider $a=1$. Multiplication does nothing, so the only useful operation is repeatedly adding $b$. For example:

```
n=13, a=1, b=4
```

The reachable numbers are $1,5,9,13,\dots$, so the answer is Yes. A solution that blindly generates powers of $a$ would loop forever because $1,1,1,\dots$ never changes.

Another tricky case is when $n$ itself is a power of $a$.

```
n=81, a=3, b=5
```

We can simply multiply four times. No additions are needed. The answer is Yes because

$$81 = 3^4 + 0\cdot 5.$$

A solution that insists on using at least one addition would fail.

A third case is when additions must happen before some multiplications.

```
n=24, a=3, b=5
```

One valid construction is

$$1 \to 6 \to 8 \to 24.$$

The sequence is not just "all multiplications, then all additions". A direct simulation of operation order looks complicated, but the mathematical structure turns out to make the order irrelevant for the final test.

## Approaches

A brute-force approach would perform a graph search starting from $1$. Each state $x$ has edges to $x\cdot a$ and $x+b$. This correctly explores all reachable numbers.

The problem is the size of the state space. Even if we stop at values larger than $n$, there may still be up to $n$ states. Since $n$ can be $10^9$, this is completely infeasible.

To find something better, we need to understand what reachable numbers look like.

Suppose we decide how many multiplications by $a$ we will perform. Let that count be $k$. The multiplications contribute a factor of $a^k$. Every addition contributes some multiple of $b$.

A key observation is that modulo $b$, adding $b$ changes nothing. The only thing that affects the residue modulo $b$ is multiplication by $a$.

If a number is reachable, then after fixing the final number of multiplications $k$, it must have the form

$$a^k + m b$$

for some nonnegative integer $m$.

Rearranging gives

$$n-a^k = mb.$$

Thus $n$ is reachable if and only if there exists some power $a^k$ such that

$$n \ge a^k$$

and

$$(n-a^k)\bmod b = 0.$$

Now the search space becomes tiny. We only need to test powers

$$1,a,a^2,a^3,\dots$$

up to $n$. There are at most about 30 of them when $a>1$.

The special case $a=1$ must be handled separately. Then every power is still $1$, so the condition becomes

$$(n-1)\bmod b = 0.$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ or worse | $O(n)$ | Too slow |
| Optimal | $O(\log_a n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $n$, $a$, and $b$.
2. If $a=1$, multiplication never changes the current value.

The only reachable numbers are

$$1,\ 1+b,\ 1+2b,\dots$$

Check whether

$$(n-1)\bmod b = 0.$$

If yes, print `"Yes"`, otherwise print `"No"`.
3. If $a>1$, start with the current power equal to $1$.
4. While the current power is at most $n$, test whether

$$(n-\text{power})\bmod b = 0.$$

If this holds, then

$$n=\text{power}+mb$$

for some nonnegative integer $m$, so $n$ is reachable. Print `"Yes"` and stop processing this test case.
5. Otherwise multiply the current power by $a$ and continue.
6. If every power of $a$ up to $n$ has been checked and none works, print `"No"`.

### Why it works

Every reachable number can be viewed as a power of $a$ plus some number of additions of size $b$. Fix the final count of multiplications to be $k$. The multiplicative part contributes $a^k$, while additions contribute an amount divisible by $b$. Hence every reachable number satisfies

$$n=a^k+mb.$$

Conversely, if for some $k$ we have

$$n=a^k+mb$$

with $m\ge 0$, then starting from $1$, performing $k$ multiplications gives $a^k$, and performing $m$ additions gives $n$. Thus the algorithm checks exactly the necessary and sufficient condition for reachability.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, a, b = map(int, input().split())

    if a == 1:
        print("Yes" if (n - 1) % b == 0 else "No")
        continue

    cur = 1
    ok = False

    while cur <= n:
        if (n - cur) % b == 0:
            ok = True
            break
        cur *= a

    print("Yes" if ok else "No")
```

The first branch handles $a=1$. Without it, the loop over powers would never terminate because multiplying by $1$ leaves the current value unchanged.

The variable `cur` stores successive powers of $a$:

$$1,\ a,\ a^2,\dots$$

For each power we test whether the remaining difference to $n$ is divisible by $b$. A successful divisibility check means that the remaining amount can be supplied entirely through addition operations.

Python integers automatically expand to arbitrary size, so there is no overflow concern. The loop stops once `cur > n`, because larger powers cannot participate in a representation

$$n=a^k+mb$$

with $m\ge 0$.

## Worked Examples

### Example 1

Input:

```
24 3 5
```

| Current Power | $n-\text{power}$ | Divisible by 5? |
| --- | --- | --- |
| 1 | 23 | No |
| 3 | 21 | No |
| 9 | 15 | Yes |

The power $9$ works because

$$24-9=15=3\cdot 5.$$

Thus

$$24=3^2+3\cdot 5,$$

so the answer is Yes.

This example shows that we do not need to reconstruct the actual sequence of operations. The divisibility condition already captures reachability.

### Example 2

Input:

```
10 3 6
```

| Current Power | $n-\text{power}$ | Divisible by 6? |
| --- | --- | --- |
| 1 | 9 | No |
| 3 | 7 | No |
| 9 | 1 | No |

The next power is $27$, which exceeds $10$, so the search ends.

No power of $3$ leaves a difference divisible by $6$. The answer is No.

This example demonstrates that checking only powers of $a$ is enough. If none of them works, no sequence of operations can reach $n$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log_a n)$ | We test each power of $a$ up to $n$ |
| Space | $O(1)$ | Only a few variables are stored |

For $a \ge 2$, the number of powers does not exceed about 30 when $n \le 10^9$. Even with $10^5$ test cases, the total work is only a few million simple arithmetic operations, well within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    data = io.StringIO(inp)
    out = []

    t = int(data.readline())

    for _ in range(t):
        n, a, b = map(int, data.readline().split())

        if a == 1:
            out.append("Yes" if (n - 1) % b == 0 else "No")
            continue

        cur = 1
        ok = False

        while cur <= n:
            if (n - cur) % b == 0:
                ok = True
                break
            cur *= a

        out.append("Yes" if ok else "No")

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""5
24 3 5
10 3 6
2345 1 4
19260817 394 485
19260817 233 264
"""
) == """Yes
No
Yes
No
Yes
"""

# minimum values
assert run(
"""1
1 1 1
"""
) == """Yes
"""

# a = 1 reachable
assert run(
"""1
13 1 4
"""
) == """Yes
"""

# a = 1 not reachable
assert run(
"""1
14 1 4
"""
) == """No
"""

# exact power of a
assert run(
"""1
81 3 5
"""
) == """Yes
"""

# large boundary-style case
assert run(
"""1
1000000000 1000000000 1
"""
) == """Yes
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | Yes | Smallest possible values |
| `13 1 4` | Yes | Special case $a=1$, reachable |
| `14 1 4` | No | Special case $a=1$, unreachable |
| `81 3 5` | Yes | Number is a pure power of $a$ |
| `1000000000 1000000000 1` | Yes | Large values and $b=1$ |

## Edge Cases

Consider the input:

```
1
13 1 4
```

Since $a=1$, the algorithm immediately uses the special branch. It computes

$$(13-1)\bmod 4 = 12\bmod 4 = 0.$$

The answer is Yes. Without the special case, the power-generation loop would never advance.

Consider the input:

```
1
81 3 5
```

The tested powers are $1,3,9,27,81$. When the current power reaches $81$,

$$81-81=0,$$

which is divisible by $5$. The algorithm returns Yes. This confirms that zero additions are allowed.

Consider the input:

```
1
10 3 6
```

The tested powers are $1,3,9$. None leaves a difference divisible by $6$. The next power exceeds $n$, so the answer is No. This verifies the stopping condition when no valid representation exists.
