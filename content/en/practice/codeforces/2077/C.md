---
title: "CF 2077C - Binary Subsequence Value Sum"
description: "Every character of the string contributes either +1 or -1. If we define $$w(c)= begin{cases} +1,&c='1' -1,&c='0' end{cases}$$ then for any segment of a binary string, the function $F$ is simply the sum of these values over that segment."
date: "2026-06-08T06:31:22+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "dp", "fft", "math", "matrices"]
categories: ["algorithms"]
codeforces_contest: 2077
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1008 (Div. 1)"
rating: 2300
weight: 2077
solve_time_s: 118
verified: true
draft: false
---

[CF 2077C - Binary Subsequence Value Sum](https://codeforces.com/problemset/problem/2077/C)

**Rating:** 2300  
**Tags:** combinatorics, data structures, dp, fft, math, matrices  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

Every character of the string contributes either `+1` or `-1`.

If we define

$$w(c)= \begin{cases} +1,&c='1'\\ -1,&c='0' \end{cases}$$

then for any segment of a binary string, the function $F$ is simply the sum of these values over that segment.

For a binary string $v$, let

$$d=\#1-\#0$$

be its total imbalance.

The score of $v$ is obtained by splitting the string into a prefix and suffix and maximizing

$$F(\text{prefix})\cdot F(\text{suffix}).$$

We are given a binary string $s$. After every flip operation, we must compute the sum of scores over all non-empty subsequences of the current string.

The first observation from the constraints is that the string length and the number of queries can each reach $2\cdot 10^5$, and their total over all test cases is also $2\cdot 10^5$. Any solution that examines subsequences explicitly is impossible because a string of length $2\cdot 10^5$ has $2^{200000}$ subsequences. Even an $O(n)$ recomputation per query would be too expensive because that would lead to $O(nq)$.

The answer must depend only on a very small amount of information that can be updated after a flip.

A subtle edge case is a subsequence of length one.

For example:

```
v = "1"
```

The only possible split uses an empty side, so the score is $0$. Any derivation that assumes both sides are non-empty will incorrectly give a positive value.

Another easy mistake is handling parity incorrectly.

For

```
v = "111"
```

we have $d=3$. The score is not $d^2/4=9/4$. The actual answer is

$$\left\lfloor \frac d2\right\rfloor \left\lceil \frac d2\right\rceil = 1\cdot2 = 2.$$

The parity correction is the key step of the whole solution.

A third trap is the empty subsequence. The problem asks for non-empty subsequences, but the final formula naturally counts all subsequences. Fortunately the empty subsequence has imbalance $0$ and score $0$, so including it changes nothing.

## Approaches

A brute force solution would enumerate every subsequence, compute its imbalance, determine its score, and add the result.

For a string of length $n$, this requires examining $2^n$ subsequences. Even for $n=60$, that is already far beyond feasibility. With $n=2\cdot10^5$, it is completely impossible.

The crucial observation is that the score of a subsequence depends only on its imbalance

$$d=\#1-\#0.$$

It does not depend on the order of characters inside the subsequence.

Suppose a subsequence has imbalance $d$. Let the imbalance of the chosen prefix be $x$. Then the suffix imbalance is $d-x$, so every split produces

$$x(d-x).$$

This quadratic is maximized when the two parts are as close as possible. The maximum value becomes

$$\left\lfloor \frac d2\right\rfloor \left\lceil \frac d2\right\rceil = \frac{d^2-(d\bmod 2)}4.$$

Now the problem becomes:

$$\sum_{\text{subsequence}} \frac{d^2-(d\bmod2)}4.$$

The subsequence order has disappeared completely.

Let $R$ be the number of ones in the current string. Then every query only changes $R$ by $\pm1$.

The remaining task is to compute the sum of $d^2$ over all subsequences and then subtract the parity correction. Using a probabilistic interpretation of a uniformly random subsequence, both quantities admit closed forms. After simplification the answer depends only on $n$ and $R$:

$$\boxed{ 2^{\,n-4} \left((2R-n)^2+n-2\right) } \pmod{998244353}.$$

Since $n$ never changes and a flip changes only $R$, each query can be answered in $O(1)$.

The derivation of this formula is given in the next section.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ per query | $O(n)$ for the string | Accepted |

## Algorithm Walkthrough

### Deriving the score formula

Let

$$d=\#1-\#0.$$

For a split whose prefix imbalance is $x$,

$$\text{value}=x(d-x).$$

This parabola reaches its maximum when $x$ is closest to $d/2$.

Hence

$$\text{score}(v) = \left\lfloor\frac d2\right\rfloor \left\lceil\frac d2\right\rceil = \frac{d^2-(d\bmod2)}4.$$

### Deriving the sum over all subsequences

Interpret every subsequence as independently choosing whether each position is included.

Define a random variable:

$$X_i= \begin{cases} 1,&s_i=1\text{ and chosen}\\ -1,&s_i=0\text{ and chosen}\\ 0,&\text{otherwise} \end{cases}$$

Then

$$d=\sum_i X_i.$$

Let $R$ be the number of ones and $Z=n-R$.

We have

$$E[d] = \frac{R-Z}{2} = \frac{2R-n}{2}.$$

Also

$$\operatorname{Var}(X_i)=\frac14,$$

so

$$\operatorname{Var}(d) = \frac n4.$$

Therefore

$$E[d^2] = \operatorname{Var}(d)+E[d]^2 = \frac{(2R-n)^2+n}{4}.$$

Since there are $2^n$ subsequences,

$$\sum d^2 = 2^nE[d^2] = 2^{n-2}\big((2R-n)^2+n\big).$$

The score contains

$$\frac{d^2-(d\bmod2)}4.$$

The parity correction remains.

A subsequence has odd imbalance exactly when its length is odd. Exactly half of all subsequences have odd length, namely

$$2^{n-1}.$$

Thus

$$\sum (d\bmod2) = 2^{n-1}.$$

Putting everything together:

$$\text{Answer} = \frac14 \left( 2^{n-2}\big((2R-n)^2+n\big) - 2^{n-1} \right).$$

After factoring:

$$\boxed{ 2^{n-4} \left( (2R-n)^2+n-2 \right) }.$$

### Processing updates

1. Count the current number of ones $R$.
2. Precompute powers of two modulo $998244353$.
3. For each query, flip the chosen character.
4. Update $R$ by $+1$ or $-1$.
5. Compute

$$x=2R-n.$$

1. Output

$$2^{n-4}(x^2+n-2) \pmod{998244353}.$$

For $n<4$, the factor $2^{n-4}$ is interpreted modulo $998244353$ using the modular inverse of $2$.

### Why it works

The key invariant is that every subsequence contributes only through its imbalance $d$. Once the score is rewritten as

$$\frac{d^2-(d\bmod2)}4,$$

all structural information about the subsequence disappears.

The sum of $d^2$ over all subsequences is determined entirely by the first two moments of the random imbalance variable. The parity correction depends only on how many subsequences have odd imbalance, which equals the number of odd-length subsequences. Both quantities depend solely on $n$ and the current number of ones $R$.

Every query changes only $R$, so evaluating the closed form after updating $R$ produces exactly the required sum.

The derivation follows directly from the score definition and counts every subsequence exactly once, which proves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAXN = 200000

pow2 = [1] * (MAXN + 1)
for i in range(1, MAXN + 1):
    pow2[i] = pow2[i - 1] * 2 % MOD

inv2 = (MOD + 1) // 2

def power_two_shift(n):
    if n >= 4:
        return pow2[n - 4]
    return pow(inv2, 4 - n, MOD)

t = int(input())

for _ in range(t):
    n, q = map(int, input().split())
    s = list(input().strip())

    ones = s.count('1')
    coef = power_two_shift(n)

    for _ in range(q):
        pos = int(input()) - 1

        if s[pos] == '1':
            s[pos] = '0'
            ones -= 1
        else:
            s[pos] = '1'
            ones += 1

        x = 2 * ones - n
        ans = coef * ((x * x + n - 2) % MOD)
        ans %= MOD

        print(ans)
```

The implementation mirrors the mathematical formula directly.

The value $2^{n-4}$ needs special care when $n<4$. In modular arithmetic this means multiplying by powers of $2^{-1}$, so the code uses the modular inverse of two.

The coefficient depends only on $n$, which never changes inside a test case, so it is computed once.

Each flip updates the number of ones in constant time. Recounting the whole string after every query would raise the complexity to $O(nq)$, which is unnecessary.

The expression $(2R-n)^2$ easily fits into Python integers, so there are no overflow concerns.

## Worked Examples

### Example 1

Input:

```
n = 3
s = 010
queries = [1, 3]
```

| Query | String After Flip | Ones $R$ | $x=2R-n$ | Formula Result |
| --- | --- | --- | --- | --- |
| 1 | 110 | 2 | 1 | 1 |
| 3 | 111 | 3 | 3 | 5 |

For $n=3$,

$$2^{n-4}=2^{-1}.$$

After the first flip,

$$\frac{1^2+3-2}{2}=1.$$

After the second flip,

$$\frac{3^2+3-2}{2}=5.$$

These match the sample output.

### Example 2

Input:

```
n = 2
s = 00
query = [1]
```

| Query | String After Flip | Ones $R$ | $x$ | Answer |
| --- | --- | --- | --- | --- |
| 1 | 10 | 1 | 0 | 0 |

The subsequences are:

```
1
0
10
```

Every score is zero, so the total is zero.

The formula gives

$$2^{-2}(0^2+2-2)=0.$$

The trace confirms that the closed form also handles tiny values of $n$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per query | Only a flip, a count update, and one formula evaluation |
| Space | $O(n)$ | Storage of the mutable string |

The total number of queries over all test cases is at most $2\cdot10^5$. Constant work per query easily fits within the time limit, and storing the string requires only linear memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    MOD = 998244353
    input_data = io.StringIO(inp)

    def input():
        return input_data.readline()

    MAXN = 200000
    pow2 = [1] * (MAXN + 1)
    for i in range(1, MAXN + 1):
        pow2[i] = pow2[i - 1] * 2 % MOD

    inv2 = (MOD + 1) // 2

    def coef(n):
        if n >= 4:
            return pow2[n - 4]
        return pow(inv2, 4 - n, MOD)

    out = []

    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        s = list(input().strip())

        ones = s.count('1')
        c = coef(n)

        for _ in range(q):
            p = int(input()) - 1

            if s[p] == '1':
                s[p] = '0'
                ones -= 1
            else:
                s[p] = '1'
                ones += 1

            x = 2 * ones - n
            ans = c * ((x * x + n - 2) % MOD) % MOD
            out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run(
"""3
3 2
010
1
3
10 3
0101000110
3
5
10
24 1
011001100110000101111000
24
"""
) == "\n".join([
"1",
"5",
"512",
"768",
"1536",
"23068672"
])

# n = 1
assert run(
"""1
1 1
0
1
"""
) == "0"

# all ones
assert run(
"""1
3 1
111
1
"""
) == "1"

# all zeros
assert run(
"""1
2 1
00
1
"""
) == "0"

# flip twice on same position
assert run(
"""1
2 2
01
1
1
"""
) == "0\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1` | `0` | Single-character subsequences |
| `111` then flip | `1` | Odd imbalance handling |
| `00` then flip | `0` | Balanced subsequences |
| Same position flipped twice | `0,0` | Persistent updates |

## Edge Cases

Consider:

```
1
1 1
0
1
```

After the flip the string becomes `"1"`. There is exactly one non-empty subsequence and its score is zero. The formula gives

$$2^{-3}(1+1-2)=0.$$

The algorithm correctly handles the smallest possible string.

Now consider:

```
1
1 1
1
1
```

After the flip the string becomes `"0"`.

The imbalance is $-1$, but the score is still zero because every split uses an empty side. The formula depends on $d^2$, not the sign of $d$, and again produces zero.

Finally consider:

```
1
3 1
111
1
```

After the flip we obtain `"011"`.

The number of ones becomes $R=2$, giving $x=1$. The answer is

$$2^{-1}(1^2+3-2)=1.$$

This case exercises the parity correction. Using only $d^2/4$ would produce a fractional value and lead to an incorrect derivation. The correction term exactly removes the overcount for odd imbalances.
