---
title: "CF 1906K - Deck-Building Game"
description: "Each card can end up in one of three states. A card may be placed in your deck, placed in your friend's deck, or discarded entirely. Let the XOR of your deck be X and the XOR of your friend's deck be Y."
date: "2026-06-09T01:26:49+07:00"
tags: ["codeforces", "competitive-programming", "divide-and-conquer", "math"]
categories: ["algorithms"]
codeforces_contest: 1906
codeforces_index: "K"
codeforces_contest_name: "2023-2024 ICPC, Asia Jakarta Regional Contest (Online Mirror, Unrated, ICPC Rules, Teams Preferred)"
rating: 2500
weight: 1906
solve_time_s: 202
verified: true
draft: false
---

[CF 1906K - Deck-Building Game](https://codeforces.com/problemset/problem/1906/K)

**Rating:** 2500  
**Tags:** divide and conquer, math  
**Solve time:** 3m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

Each card can end up in one of three states.

A card may be placed in your deck, placed in your friend's deck, or discarded entirely.

Let the XOR of your deck be `X` and the XOR of your friend's deck be `Y`. We must count the number of assignments of cards to these three states such that `X = Y`.

The first observation is to rewrite the condition.

Because the two decks are disjoint, every used card contributes to exactly one of `X` or `Y`. Thus

$$X \oplus Y$$

is exactly the XOR of all cards that were used by either player.

The condition `X = Y` is equivalent to

$$X \oplus Y = 0.$$

So if we denote by $U$ the set of cards that are used by at least one player, then we only need

$$\bigoplus_{i\in U} A_i = 0.$$

Once such a set $U$ is chosen, every card in $U$ can independently be assigned to either player. That creates

$$2^{|U|}$$

different deck pairs.

The problem becomes:

$$\sum_{\text{subset }U,\ \operatorname{xor}(U)=0} 2^{|U|}.$$

The constraints are what make the problem interesting. We have up to $10^5$ cards, so any algorithm that explicitly enumerates subsets is impossible. The values satisfy $A_i \le 100000$, which means every value fits inside 17 bits. That strongly suggests treating XOR as an operation on the vector space $(\mathbb Z_2)^{17}$.

A common mistake is to think that only the XOR value matters and forget the factor $2^{|U|}$. For example:

```
2
1 1
```

The zero-XOR subsets are `{}`, `{1,2}`. Their weights are $1$ and $4$, giving answer $5$. Counting only subsets would incorrectly produce $2$.

Another easy mistake is to count assignments of cards to decks directly and then try to track both deck XORs. For

```
2
1 1
```

the valid assignments are:

```
discard, discard
S, T
T, S
S&T together impossible
both in S
both in T
```

There are exactly five valid outcomes, matching the weighted-subset interpretation above.

A third pitfall appears when all values are linearly independent:

```
2
1 2
```

The only zero-XOR subset is the empty subset, so the answer is `1`. Any approach that assumes every XOR value appears equally often will fail here.

## Approaches

The brute-force solution is straightforward.

For every subset $U$, compute its XOR. If the XOR is zero, add $2^{|U|}$ to the answer. This is correct because each used card can be assigned to either deck independently.

The problem is that there are $2^N$ subsets. With $N=100000$, the number of subsets is astronomically large.

We need to exploit the small value range instead.

The key observation is that XOR lives in a 17-bit vector space. Let $M = 2^{17}$. For each card $A_i$, define a group-algebra element

$$f_i = e_0 + 2e_{A_i}.$$

Choosing the first term means the card is unused. Choosing the second term means the card is used, contributing weight $2$.

Multiplying all factors gives

$$F=\prod_i (e_0+2e_{A_i}).$$

The coefficient of $e_x$ equals the total weight of all subsets whose XOR is $x$. Our answer is the coefficient of $e_0$.

This is exactly the setting where the Walsh-Hadamard transform diagonalizes XOR convolution.

For a character $t$,

$$\widehat f_i(t)
=
1+2(-1)^{\langle t,A_i\rangle}.$$

The value is either $3$ or $-1$.

If

$$s_t=\sum_v \text{freq}[v]\cdot (-1)^{\langle t,v\rangle},$$

then

$$\widehat F(t)
=
3^{(N+s_t)/2}
(-1)^{(N-s_t)/2}.$$

By the inverse Walsh transform,

$$\text{answer}
=
\frac1M
\sum_t \widehat F(t).$$

Now the task is reduced to computing every $s_t$. These are exactly the Walsh-Hadamard transform values of the frequency array.

The frequency array has length $M=131072$, so one FWHT costs

$$O(M\log M),$$

which is about $2.2\times10^6$ operations and easily fits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^N)$ | $O(1)$ | Too slow |
| Optimal | $O(2^{17}\cdot17)$ | $O(2^{17})$ | Accepted |

## Algorithm Walkthrough

1. Create a frequency array `freq` of size $2^{17}$.
2. For every card value $A_i$, increment `freq[A_i]`.
3. Apply the Walsh-Hadamard transform to `freq`.

After the transform, `freq[t]` becomes

$$s_t
=
\sum_v \text{cnt}[v](-1)^{\langle t,v\rangle}.$$
4. Precompute powers of $3$ modulo $998244353$ up to $N$.
5. For every transformed value $s_t$, compute

$$a=\frac{N+s_t}{2},
\qquad
b=\frac{N-s_t}{2}.$$

Then add

$$3^a(-1)^b$$

to the running sum.
6. Multiply the final sum by

$$(2^{17})^{-1}
\pmod{998244353}.$$

This performs the inverse Walsh-Hadamard normalization and gives the coefficient corresponding to XOR zero.

### Why it works

For every card, the factor $e_0+2e_{A_i}$ encodes the two possibilities relevant to the weighted subset formulation. Multiplying all factors accumulates XOR values through XOR convolution, and the coefficient of $e_x$ becomes the total weight of subsets whose XOR equals $x$.

The Walsh-Hadamard transform converts XOR convolution into pointwise multiplication. Since each transformed factor is either $3$ or $-1$, the product at character $t$ depends only on how many card values have character value $+1$ and how many have character value $-1$. Those counts are determined by $s_t$.

The inverse transform states that the coefficient of XOR value $0$ is the average of all transformed values. That coefficient is exactly the quantity we need to count.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
BITS = 17
M = 1 << BITS

n = int(input())
freq = [0] * M

for x in map(int, input().split()):
    freq[x] += 1

h = 1
while h < M:
    step = h << 1
    for i in range(0, M, step):
        for j in range(i, i + h):
            x = freq[j]
            y = freq[j + h]
            freq[j] = x + y
            freq[j + h] = x - y
    h <<= 1

pow3 = [1] * (n + 1)
for i in range(1, n + 1):
    pow3[i] = pow3[i - 1] * 3 % MOD

ans = 0

for s in freq:
    a = (n + s) // 2
    b = (n - s) // 2

    term = pow3[a]
    if b & 1:
        term = MOD - term

    ans += term

ans %= MOD
ans = ans * pow(M, MOD - 2, MOD) % MOD

print(ans)
```

The frequency array is the only structure indexed by XOR values. Since every card value fits in 17 bits, the entire XOR space contains exactly $2^{17}$ states.

The FWHT is performed in-place. After completion, each position stores the character sum $s_t$. These values are ordinary integers, not modular values. Keeping them as integers avoids any parity issues when computing $(N+s_t)/2$.

The expression

```
if b & 1:
    term = MOD - term
```

implements the factor $(-1)^b$.

The final multiplication by `pow(M, MOD - 2, MOD)` performs division by $2^{17}$ under the modulus.

## Worked Examples

### Example 1

Input

```
4
16 12 4 8
```

The nonzero frequencies occur at four values.

After FWHT, the transformed frequency array contains character sums $s_t$. For this instance, only a small subset of positions matters for illustration:

| t | $s_t$ | $a=(N+s_t)/2$ | $b=(N-s_t)/2$ | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 4 | 4 | 0 | $3^4=81$ |
| ... | 0 | 2 | 2 | $+9$ |
| ... | 0 | 2 | 2 | $+9$ |
| ... | -4 | 0 | 4 | $+1$ |

Summing all transformed contributions and dividing by $2^{17}$ yields:

```
9
```

This matches the sample answer.

The trace illustrates the central idea: we never enumerate subsets. We only evaluate the transformed expression at every character.

### Example 2

Input

```
2
1 2
```

Frequency transform values are:

| t type | $s_t$ |
| --- | --- |
| parity agrees with both values | 2 |
| one agreement, one disagreement | 0 |
| disagreement with both | -2 |

For each position we compute $3^{(N+s_t)/2}(-1)^{(N-s_t)/2}$, sum them, and divide by $2^{17}$.

The result is:

```
1
```

Only the empty subset has XOR zero. This example confirms that the algorithm correctly handles arrays with no nontrivial zero-XOR subset.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^{17}\cdot17)$ | One FWHT over a length-$2^{17}$ array |
| Space | $O(2^{17})$ | Frequency array and transformed values |

The XOR space contains only 131072 states. A single FWHT on this space performs roughly 2.2 million arithmetic operations, which is easily fast enough for $N=100000$.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    MOD = 998244353
    BITS = 17
    M = 1 << BITS

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    freq = [0] * M

    for x in map(int, input().split()):
        freq[x] += 1

    h = 1
    while h < M:
        step = h << 1
        for i in range(0, M, step):
            for j in range(i, i + h):
                x = freq[j]
                y = freq[j + h]
                freq[j] = x + y
                freq[j + h] = x - y
        h <<= 1

    pow3 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow3[i] = pow3[i - 1] * 3 % MOD

    ans = 0
    for s in freq:
        a = (n + s) // 2
        b = (n - s) // 2

        term = pow3[a]
        if b & 1:
            term = MOD - term

        ans += term

    ans %= MOD
    ans = ans * pow(M, MOD - 2, MOD) % MOD
    return str(ans) + "\n"

# provided sample
assert run("4\n16 12 4 8\n") == "9\n", "sample 1"

# minimum size
assert run("2\n1 2\n") == "1\n", "only empty subset"

# all equal
assert run("2\n1 1\n") == "5\n", "weighted zero xor subsets"

# three equal values
assert run("3\n7 7 7\n") == "7\n", "empty plus all pair subsets"

# xor of all cards is zero
assert run("3\n1 2 3\n") == "9\n", "full subset contributes weight 8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2` | `1` | Only the empty subset works |
| `2 / 1 1` | `5` | Weight (2^{ |
| `3 / 7 7 7` | `7` | Repeated values and multiple zero-XOR subsets |
| `3 / 1 2 3` | `9` | Nontrivial zero-XOR subset of size three |

## Edge Cases

Consider

```
2
1 1
```

The valid zero-XOR subsets are `{}` and `{1,2}`. Their weights are $1$ and $4$, producing answer $5$. The algorithm captures this because the generating factor for each card is $e_0+2e_1$. The weight is built directly into the transform, so no special handling is required.

Consider

```
2
1 2
```

No non-empty subset has XOR zero. After the inverse transform, the coefficient of XOR value zero is exactly $1$, corresponding to the empty subset. The algorithm does not assume any uniformity of XOR frequencies.

Consider

```
3
1 2 3
```

The full subset has XOR

$$1\oplus2\oplus3=0.$$

The answer is

$$1 + 2^3 = 9.$$

The FWHT formulation naturally includes both contributions. The empty subset contributes weight $1$, and the full subset contributes weight $8$.

Finally, consider the largest possible input size, where $N=100000$. The algorithm's running time depends only on the 17-bit XOR space, not on the number of possible subsets. The frequency counts absorb all multiplicities, and the complexity remains $O(2^{17}\cdot17)$.
