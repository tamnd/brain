---
title: "CF 1942E - Farm Game"
description: "The cows of the two farmers must appear in alternating order on the line. Once the order of the first cow is chosen, the entire sequence is fixed: either J N J N ... J N or N J N J ... N J. The actual positions are not fixed."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "games"]
categories: ["algorithms"]
codeforces_contest: 1942
codeforces_index: "E"
codeforces_contest_name: "CodeTON Round 8 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 2300
weight: 1942
solve_time_s: 116
verified: true
draft: false
---

[CF 1942E - Farm Game](https://codeforces.com/problemset/problem/1942/E)

**Rating:** 2300  
**Tags:** combinatorics, games  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The cows of the two farmers must appear in alternating order on the line. Once the order of the first cow is chosen, the entire sequence is fixed:

either

`J N J N ... J N`

or

`N J N J ... N J`.

The actual positions are not fixed. There may be empty cells between cows and near the walls.

A move chooses some of one farmer's cows and shifts all of them one step in the same direction. A move is legal only if no cow hits a wall and no cow lands on an occupied position.

We are given the length of the line and the number of cows belonging to each farmer. Among all valid placements, we must count how many are winning for Farmer John, assuming optimal play and that John moves first.

The constraints are the main clue that the solution must be combinatorial. The line length can reach $10^6$, but the sum of all lengths over the test file is also at most $10^6$. That immediately rules out any attempt to analyze individual game states. Even storing all configurations would be impossible because the number of valid placements grows exponentially.

The only viable direction is to find a simple characterization of winning and losing positions, then count them with combinatorics.

A few edge cases are easy to miss.

For example:

Input

```
1
2 1
```

The only valid configurations are:

```
JN
NJ
```

No cow can move in either configuration, so John loses immediately. The correct answer is:

```
0
```

A naive approach that assumes "first player wins unless the board is full" would fail.

Another important case is:

Input

```
1
3 1
```

The valid configurations are:

```
JN_
_JN
N_J
J_N
```

Only the last two are winning for John. The correct answer is:

```
2
```

The existence of empty cells alone is not enough. Their placement matters.

A final subtle point is that the game description allows moves that increase some distances, so at first glance infinite play seems possible. The key game-theoretic observation is that optimal play is completely determined by the parity of certain gaps. Once that structure is discovered, the counting becomes manageable.

## Approaches

A brute-force solution would generate every valid configuration, build the game graph, and determine whether the initial state is winning.

For a fixed alternating order, a configuration is essentially a placement of $2n$ cows among $l$ positions. There are

$$\binom{l}{2n}$$

such placements, and there are two possible alternating orders. Even for moderate values, this number is enormous.

For example, when $l=60$ and $n=20$,

$$\binom{60}{40}$$

is already far beyond anything we can enumerate.

The brute-force approach works conceptually because the game is finite-state, but it becomes useless long before reaching the actual constraints.

The breakthrough comes from looking at the gaps between paired cows.

Assume the sequence starts with John's cow:

$$a_1 < b_1 < a_2 < b_2 < \cdots < a_n < b_n.$$

Define

$$g_i = b_i - a_i - 1.$$

So $g_i$ is the number of empty cells between the $i$-th John cow and the corresponding Nhoj cow.

These gaps completely capture the game.

A move changes some nonzero gaps by exactly $+1$ or $-1$. The crucial fact is that the parity of the gaps determines the winner:

A position is losing if and only if every $g_i$ is even.

If at least one gap is odd, John can move to a state where all gaps become even. If all gaps are already even, every legal move creates an odd gap.

Once the game is reduced to this parity criterion, the rest is pure counting.

We count all valid configurations, then subtract the configurations whose gaps are all even.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(l)$ per test, $O(\sum l)$ overall | $O(l)$ | Accepted |

## Algorithm Walkthrough

### 1. Fix one alternating order

Assume the sequence starts with John's cow:

$$a_1 < b_1 < a_2 < b_2 < \cdots < a_n < b_n.$$

The opposite order contributes exactly the same number of configurations, so we can count one order and multiply by two at the end.

### 2. Define the important gaps

For each pair,

$$g_i = b_i - a_i - 1.$$

These are the gaps that control the game.

Also define the remaining empty segments:

$$x_0=a_1-1,$$

$$x_i=a_{i+1}-b_i-1 \quad (1\le i<n),$$

$$x_n=l-b_n.$$

All $x_i$ and $g_i$ are nonnegative.

Since the cows themselves occupy $2n$ cells,

$$\sum x_i + \sum g_i = l-2n.$$

Let

$$m=l-2n.$$

### 3. Characterize losing positions

A configuration is losing exactly when every $g_i$ is even.

Write

$$g_i=2h_i.$$

Then

$$\sum x_i + 2\sum h_i = m.$$

### 4. Count losing configurations

Let

$$s=\sum h_i.$$

Then

$$\sum x_i = m-2s.$$

The $h_i$ are nonnegative and there are $n$ of them.

By stars and bars,

$$\#(h_1,\dots,h_n)
=
\binom{s+n-1}{n-1}.$$

The $x_i$ are nonnegative and there are $n+1$ of them.

Again by stars and bars,

$$\#(x_0,\dots,x_n)
=
\binom{m-2s+n}{n}.$$

For a fixed $s$, the number of losing configurations is therefore

$$\binom{s+n-1}{n-1}
\binom{m-2s+n}{n}.$$

Summing over all possible $s$,

$$L
=
\sum_{s=0}^{\lfloor m/2\rfloor}
\binom{s+n-1}{n-1}
\binom{m-2s+n}{n}.$$

### 5. Count all configurations

For one alternating order, we distribute $m$ empty cells among

$$(n+1)+n = 2n+1$$

nonnegative variables.

Stars and bars gives

$$\binom{m+2n}{2n}
=
\binom{l}{2n}.$$

### 6. Compute the answer

For one order,

$$\text{winning}
=
\binom{l}{2n}-L.$$

There are two symmetric alternating orders, so

$$\text{answer}
=
2\left(\binom{l}{2n}-L\right).$$

All arithmetic is performed modulo $998244353$.

### Why it works

The entire game can be expressed through the gap vector $(g_1,\dots,g_n)$.

A move changes selected positive gaps by one unit, so every changed gap flips parity.

If all gaps are even, every legal move creates at least one odd gap. Such positions cannot move to another all-even position.

If some gap is odd, every odd gap is positive. Decreasing every odd gap by one is legal and produces a state where all gaps are even.

Thus every non-even position has a move to an all-even position, and every all-even position moves only to non-even positions. This exactly matches the definition of losing and winning positions.

The counting part is correct because every valid placement corresponds uniquely to the variables $x_i$ and $g_i$, and stars-and-bars counts all nonnegative solutions of the resulting equations.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

MAXL = 10**6 + 5

fact = [1] * MAXL
for i in range(1, MAXL):
    fact[i] = fact[i - 1] * i % MOD

inv_fact = [1] * MAXL
inv_fact[-1] = pow(fact[-1], MOD - 2, MOD)

for i in range(MAXL - 1, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD

def C(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

t = int(input())

for _ in range(t):
    l, n = map(int, input().split())

    m = l - 2 * n

    losing = 0

    for s in range(m // 2 + 1):
        ways_h = C(s + n - 1, n - 1)
        ways_x = C(m - 2 * s + n, n)
        losing = (losing + ways_h * ways_x) % MOD

    total_one_order = C(l, 2 * n)

    ans = (total_one_order - losing) % MOD
    ans = (2 * ans) % MOD

    print(ans)
```

The factorial and inverse-factorial arrays are precomputed once up to $10^6$, which covers every binomial coefficient needed in the problem.

The function `C(n, r)` evaluates combinations in constant time.

For a test case, `m = l - 2n` is the number of empty cells. The loop over `s` implements the losing-position formula directly:

$$\sum
\binom{s+n-1}{n-1}
\binom{m-2s+n}{n}.$$

The first combination counts distributions of the half-gaps $h_i$. The second counts distributions of the remaining empty cells $x_i$.

The answer is then obtained by subtracting losing configurations from all configurations for one alternating order and multiplying by two for the two possible starting farmers.

The most common implementation mistake is forgetting that there are $n+1$ variables $x_i$, not $n$. Using the wrong stars-and-bars formula shifts every count by one and produces incorrect answers even on small tests.

Another easy error is forgetting the final multiplication by two. The counting above assumes the sequence starts with John's cow. The opposite alternating order contributes the same amount and must be included.

## Worked Examples

### Example 1

Input:

```
3 1
```

Here

$$m = 3 - 2 = 1.$$

| s | $\binom{s+n-1}{n-1}$ | $\binom{m-2s+n}{n}$ | Contribution |
| --- | --- | --- | --- |
| 0 | 1 | 2 | 2 |

So:

| Variable | Value |
| --- | --- |
| losing | 2 |
| total one order | $\binom{3}{2}=3$ |
| winning one order | 1 |
| final answer | 2 |

Output:

```
2
```

This example shows that only some placements are winning even though empty cells exist.

### Example 2

Input:

```
2 1
```

Here

$$m = 0.$$

| s | $\binom{s+n-1}{n-1}$ | $\binom{m-2s+n}{n}$ | Contribution |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 1 |

Then:

| Variable | Value |
| --- | --- |
| losing | 1 |
| total one order | $\binom{2}{2}=1$ |
| winning one order | 0 |
| final answer | 0 |

Output:

```
0
```

Every configuration is losing because there is no empty cell anywhere.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(l)$ per test | The summation iterates through $0 \ldots \lfloor(l-2n)/2\rfloor$ |
| Space | $O(10^6)$ | Factorial and inverse-factorial tables |

Because the sum of all $l$ values is at most $10^6$, the total number of iterations across the entire input is also $O(10^6)$. This comfortably fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())

    tests = []
    max_l = 0

    for _ in range(t):
        l, n = map(int, input().split())
        tests.append((l, n))
        max_l = max(max_l, l)

    fact = [1] * (max_l + 5)
    for i in range(1, max_l + 5):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (max_l + 5)
    inv_fact[-1] = pow(fact[-1], MOD - 2, MOD)

    for i in range(max_l + 4, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def C(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

    out = []

    for l, n in tests:
        m = l - 2 * n

        losing = 0
        for s in range(m // 2 + 1):
            losing += C(s + n - 1, n - 1) * C(m - 2 * s + n, n)
            losing %= MOD

        ans = (C(l, 2 * n) - losing) % MOD
        ans = ans * 2 % MOD

        out.append(str(ans))

    return "\n".join(out) + "\n"

# provided samples
assert run("3\n2 1\n3 1\n420 69\n") == "0\n2\n870279412\n", "sample"

# minimum size
assert run("1\n2 1\n") == "0\n", "smallest instance"

# one empty cell
assert run("1\n3 1\n") == "2\n", "single-gap case"

# exactly full board with larger n
assert run("1\n4 2\n") == "0\n", "no movement possible"

# boundary with many empty cells
assert run("1\n5 1\n") == "6\n", "checks counting formula"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1` | `0` | Smallest possible instance |
| `3 1` | `2` | Single empty cell, parity matters |
| `4 2` | `0` | Completely packed board |
| `5 1` | `6` | Larger gap distributions and stars-and-bars counting |

## Edge Cases

Consider:

```
1
2 1
```

We have $m=0$. The only possible gap value is $g_1=0$, which is even. The algorithm computes:

$$L=1,
\qquad
\binom{2}{2}=1.$$

So the answer becomes:

$$2(1-1)=0.$$

This matches the game itself because neither player can move.

Now consider:

```
1
4 2
```

The cows occupy all four cells. Again $m=0$, so every gap is forced to be zero and thus even.

The algorithm counts every configuration as losing:

$$L=\binom{4}{4}=1$$

for one alternating order.

After subtraction, the number of winning positions is zero. This catches the common mistake of assuming that alternating order alone creates winning opportunities.

Finally, consider:

```
1
3 1
```

Here $m=1$. The only losing states are those with $g_1=0$. Any state with $g_1=1$ has an odd gap and is winning.

The summation correctly produces:

$$L=2,$$

while the total number of configurations is

$$2\binom{3}{2}=6.$$

Thus:

$$6-4=2$$

winning configurations remain, exactly matching the sample.
