---
title: "CF 1842H - Tenzing and Random Real Numbers"
description: "We have $n$ independent random variables, each chosen uniformly from the interval $[0,1]$. Between pairs of variables we are given constraints of the form $$xi+xjle 1$$ or $$xi+xjge 1.$$ The task is to compute the probability that all constraints hold simultaneously."
date: "2026-06-09T06:16:39+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "graphs", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1842
codeforces_index: "H"
codeforces_contest_name: "CodeTON Round 5 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 3000
weight: 1842
solve_time_s: 115
verified: false
draft: false
---

[CF 1842H - Tenzing and Random Real Numbers](https://codeforces.com/problemset/problem/1842/H)

**Rating:** 3000  
**Tags:** bitmasks, dp, graphs, math, probabilities  
**Solve time:** 1m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We have $n$ independent random variables, each chosen uniformly from the interval $[0,1]$. Between pairs of variables we are given constraints of the form

$$x_i+x_j\le 1$$

or

$$x_i+x_j\ge 1.$$

The task is to compute the probability that all constraints hold simultaneously.

The most important observation is that the variables are continuous. Equalities such as $x_i+x_j=1$ happen with probability $0$, so we are free to reason using strict inequalities whenever it simplifies the argument.

The constraint $n\le 20$ immediately suggests that exponential algorithms in $n$ are possible. A state space of size $2^n$ is about one million, which is feasible. Anything involving all permutations of the variables would require $20!$ possibilities and is hopeless.

A subtle point is that the constraints do not compare individual variables. They compare sums relative to $1$. Trying to discretize the values of the variables or integrate directly over $[0,1]^n$ quickly becomes intractable.

Another easy mistake is mishandling self-loops.

For example:

```
1 1
1 1 1
```

The constraint is $2x_1\ge 1$, which means $x_1\ge \tfrac12$. The answer is $\tfrac12$, not $1$.

Similarly:

```
1 1
0 1 1
```

requires $x_1\le \tfrac12$, again probability $\tfrac12$.

A different trap is contradictory structure created indirectly.

```
4 4
0 1 2
0 3 4
1 1 3
1 2 4
```

This is the fourth sample. The constraints force a cycle of sign requirements that cannot be satisfied, so the answer is $0$. A local check on each edge is not enough.

## Approaches

A brute-force viewpoint is to think of the probability as the volume of a region inside the unit cube $[0,1]^n$. Every constraint cuts the cube by a hyperplane. Computing the resulting volume exactly would require integrating over a complicated polytope. Even for $n=20$, this is completely unrealistic.

The key observation comes from rewriting the variables around the midpoint $1/2$.

Define

$$y_i=x_i-\frac12.$$

Each $y_i$ is uniformly distributed on $\left[-\frac12,\frac12\right]$.

Now every constraint becomes

$$y_i+y_j\le 0$$

or

$$y_i+y_j\ge 0.$$

Suppose $|y_i|<|y_j|$.

If $y_i+y_j\le 0$, the sign of the sum is determined by the larger magnitude term $y_j$. Since $|y_j|$ dominates, the inequality is equivalent to requiring $y_j<0$.

Likewise, if $y_i+y_j\ge 0$, it is equivalent to requiring $y_j>0$.

This is the breakthrough. For every edge, only the endpoint with larger absolute value matters.

So instead of working with actual values, we only need:

1. The ordering of the absolute values $|y_i|$.
2. The sign of each $y_i$.

Once those are fixed, every constraint is either satisfied or violated.

The absolute values are independent uniform variables. Every ordering of their magnitudes occurs with probability $1/n!$. The sign of every variable is independently positive or negative with probability $1/2$.

Thus the problem becomes:

Count the number of valid pairs

$$(\text{ordering of }|y|,\ \text{sign assignment})$$

and divide by

$$2^n n!.$$

The counting itself can be done with a subset DP over the ordering of magnitudes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force geometric integration | Exponential in continuous dimension | Huge | Too slow |
| Bitmask DP on magnitude order | $O(n2^n)$ | $O(2^n)$ | Accepted |

## Algorithm Walkthrough

### Step 1

Transform every variable:

$$y_i=x_i-\frac12.$$

The constraints become $y_i+y_j\le 0$ and $y_i+y_j\ge 0$.

### Step 2

For every variable, store two bitmasks.

`LE[i]` contains all vertices connected to $i$ by a constraint $y_i+y_j\le 0$.

`GE[i]` contains all vertices connected to $i$ by a constraint $y_i+y_j\ge 0$.

Self-loops are included naturally.

### Step 3

Process variables in increasing order of $|y|$.

Let $S$ be the set of vertices already placed. Every vertex in $S$ has smaller absolute value than every vertex outside $S$.

Suppose we want to place vertex $i$ next.

Then $i$ becomes the largest magnitude among $S\cup\{i\}$.

### Step 4

Count how many sign choices are possible for $i$.

If $i$ is positive, then every constraint of type $\ge 0$ incident to $i$ must point toward a still-unplaced vertex. Otherwise $i$ would be the larger magnitude endpoint and would be forced to be positive by that edge.

So positive is allowed iff

$$GE[i]\cap(S\cup\{i\})=\varnothing.$$

If this holds, add one transition.

Similarly, negative is allowed iff

$$LE[i]\cap(S\cup\{i\})=\varnothing.$$

If this holds, add another transition.

Each allowed sign contributes exactly one way.

### Step 5

Run a standard subset DP.

Let

$$dp[S]$$

be the number of valid constructions of the ordering and signs for the vertices in $S$.

Initialize

$$dp[\varnothing]=1.$$

For every state and every vertex not yet chosen, apply the two checks above and update $dp[S\cup\{i\}]$.

### Step 6

After finishing, $dp[(1<<n)-1]$ equals the number of valid pairs

$$(\text{ordering},\text{sign assignment}).$$

Every sign assignment has probability $1/2^n$.

Every ordering of the absolute values has probability $1/n!$.

Hence the answer is

$$\frac{dp[(1<<n)-1]}{2^n n!}.$$

All arithmetic is done modulo $998244353$.

### Why it works

For any constraint, only the endpoint with larger absolute value determines whether the sum is positive or negative. Once the order of absolute values is fixed, every edge imposes a sign requirement on exactly one endpoint, namely the later endpoint in that order.

The DP constructs the order from smallest magnitude to largest. When vertex $i$ is inserted, all vertices in $S$ have smaller magnitude. Any edge between $i$ and a vertex of $S$ already determines which sign $i$ must have. The two bitmask tests check precisely whether positive or negative remains possible.

Every valid ordering and sign assignment is counted exactly once, and every counted configuration satisfies all constraints. Since signs and magnitude orderings are uniformly distributed, dividing by $2^n n!$ converts the count into the desired probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def main():
    n, m = map(int, input().split())

    LE = [0] * n
    GE = [0] * n

    for _ in range(m):
        t, i, j = map(int, input().split())
        i -= 1
        j -= 1

        if t == 0:
            LE[i] |= 1 << j
            LE[j] |= 1 << i
        else:
            GE[i] |= 1 << j
            GE[j] |= 1 << i

    N = 1 << n
    dp = [0] * N
    dp[0] = 1

    for S in range(N):
        cur = dp[S]
        if cur == 0:
            continue

        for i in range(n):
            if (S >> i) & 1:
                continue

            T = S | (1 << i)

            if (GE[i] & T) == 0:
                dp[T] = (dp[T] + cur) % MOD

            if (LE[i] & T) == 0:
                dp[T] = (dp[T] + cur) % MOD

    ans = dp[N - 1]

    inv2 = pow(2, MOD - 2, MOD)
    for k in range(1, n + 1):
        ans = ans * pow(k, MOD - 2, MOD) % MOD
        ans = ans * inv2 % MOD

    print(ans)

if __name__ == "__main__":
    main()
```

The two masks `LE` and `GE` encode the entire constraint graph. A self-loop automatically places the vertex inside its own mask, which is exactly what we want. For example, a constraint $x_i+x_i\ge 1$ becomes a self-bit in `GE[i]`, making the negative transition impossible.

The DP state only stores the subset of already processed vertices. No additional information is needed because the ordering is reconstructed from the order in which vertices are inserted.

The expression `GE[i] & T` checks whether any forbidden `>=` edge already points to a smaller magnitude vertex. If it does, choosing the positive sign would violate a constraint.

Finally, we multiply by the modular inverses of $2$ and $1,2,\dots,n$ to divide by $2^n n!$.

## Worked Examples

### Sample 1

Input:

```
3 2
0 1 2
1 3 3
```

The masks are:

| Vertex | LE | GE |
| --- | --- | --- |
| 1 | {2} | {} |
| 2 | {1} | {} |
| 3 | {} | {3} |

DP transitions:

| State | Added vertex | Allowed signs |
| --- | --- | --- |
| {} | 1 | + and - |
| {} | 2 | + and - |
| {} | 3 | only + |
| ... | ... | ... |

The final count is $6$.

There are $3!\cdot 2^3 = 48$ equally likely order/sign pairs. Thus

$$\frac{6}{48}=\frac14.$$

Modulo $998244353$, this is `748683265`.

This example shows how self-loops restrict the sign of a single variable without affecting the ordering logic.

### Sample 2

Input:

```
3 3
0 1 2
0 1 3
0 2 3
```

Every edge is of type $\le 0$.

For whichever pair we inspect, the larger magnitude endpoint must be negative.

Therefore the largest magnitude variable overall must be negative. The remaining two variables may have either sign.

| Largest magnitude vertex | Required sign |
| --- | --- |
| 1 | negative |
| 2 | negative |
| 3 | negative |

The DP counts all valid order/sign pairs and again produces probability $1/4$.

This example illustrates the central principle that only the larger magnitude endpoint matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n2^n)$ | Every subset tries all vertices not yet chosen |
| Space | $O(2^n)$ | One DP value per subset |

With $n\le 20$, we have at most $2^{20}=1,048,576$ states. The resulting complexity is well within the limits, especially in a low-constant bitmask DP.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    MOD = 998244353

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())

    LE = [0] * n
    GE = [0] * n

    for _ in range(m):
        t, i, j = map(int, input().split())
        i -= 1
        j -= 1

        if t == 0:
            LE[i] |= 1 << j
            LE[j] |= 1 << i
        else:
            GE[i] |= 1 << j
            GE[j] |= 1 << i

    N = 1 << n
    dp = [0] * N
    dp[0] = 1

    for S in range(N):
        for i in range(n):
            if (S >> i) & 1:
                continue

            T = S | (1 << i)

            if (GE[i] & T) == 0:
                dp[T] = (dp[T] + dp[S]) % MOD

            if (LE[i] & T) == 0:
                dp[T] = (dp[T] + dp[S]) % MOD

    ans = dp[N - 1]
    inv2 = pow(2, MOD - 2, MOD)

    for k in range(1, n + 1):
        ans = ans * pow(k, MOD - 2, MOD) % MOD
        ans = ans * inv2 % MOD

    return str(ans)

# provided sample
assert run(
"""3 2
0 1 2
1 3 3
"""
) == "748683265"

# x1 >= 1/2
assert run(
"""1 1
1 1 1
"""
) == str((pow(2, 998244351, 998244353)))

# x1 <= 1/2
assert run(
"""1 1
0 1 1
"""
) == str((pow(2, 998244351, 998244353)))

# no constraints, probability = 1
assert run(
"""1 0
"""
) == "1"

# impossible configuration from sample 4
assert run(
"""4 4
0 1 2
0 3 4
1 1 3
1 2 4
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex, no constraints | 1 | Empty graph |
| $x_1+x_1\ge1$ | $1/2$ | Self-loop handling |
| $x_1+x_1\le1$ | $1/2$ | Opposite self-loop type |
| Sample 1 | $1/4$ | Mixed edge types |
| Sample 4 | 0 | Global contradiction |

## Edge Cases

Consider:

```
1 1
1 1 1
```

The self-loop is stored inside `GE[1]`. When the DP tries to place the vertex with a negative sign, the condition

$$GE[1]\cap\{1\}\neq\varnothing$$

blocks that transition. Only the positive sign remains. The DP count becomes $1$, and dividing by $2$ yields probability $1/2$.

Now consider:

```
1 1
0 1 1
```

The same reasoning applies with `LE`. Only the negative sign is allowed, again producing probability $1/2$.

Finally, consider:

```
4 4
0 1 2
0 3 4
1 1 3
1 2 4
```

Whichever vertex among $\{1,3\}$ has larger magnitude must be positive. Whichever vertex among $\{1,2\}$ has larger magnitude must be negative. Chasing these requirements around the graph produces a contradiction. During the DP every partial construction eventually gets stuck, so the final count is zero and the algorithm outputs $0$. This demonstrates that the DP detects global inconsistency automatically rather than relying on local checks.
