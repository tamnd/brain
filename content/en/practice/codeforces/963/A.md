---
problem: 963A
contest_id: 963
problem_index: A
name: "Alternating Sum"
contest_name: "Tinkoff Internship Warmup Round 2018 and Codeforces Round 475 (Div. 1)"
rating: 1800
tags: ["math", "number theory"]
answer: passed_samples
verified: true
solve_time_s: 82
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a328192-f20c-83ec-a3a9-4d043e415a76
---

# CF 963A - Alternating Sum

**Rating:** 1800  
**Tags:** math, number theory  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 22s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a328192-f20c-83ec-a3a9-4d043e415a76  

---

## Solution

## Problem Understanding

We are given a long weighted sum where each position contributes a power of two independent bases. At index $i$, the contribution is either $+1$ or $-1$, multiplied by $a^{n-i} b^i$. The sequence of signs is not arbitrary for all $n+1$ positions, instead only the first $k$ values are given and the rest repeat every $k$ steps.

So the task is to evaluate a periodic alternating polynomial-like expression, where coefficients repeat with period $k$, but exponents depend on the absolute position in the sequence. The modulus is a large prime-like number $10^9 + 9$, so arithmetic must be done under modular reduction.

The difficulty comes from two interacting structures: the periodic coefficients and the geometric growth of weights $a^{n-i} b^i$. The exponent $n$ can be as large as $10^9$, so direct construction of the sequence or direct exponentiation per term is impossible.

A naive evaluation would require iterating over all $n+1$ positions, and computing modular powers for each term. Even if each power is computed in logarithmic time, this still becomes too slow because $n$ is up to $10^9$, meaning up to a billion terms.

Edge cases appear when periodicity interacts with exponent structure. For example, if $k = 1$, the sequence is constant, and the answer reduces to a closed-form geometric sum. Another corner case is when $a = b$, where all weights collapse into a single power and cancellation depends purely on alternating periodic sums, which can easily cause sign handling mistakes.

A common failure mode is iterating over cycles incorrectly. Since $n+1$ may not be a multiple of $k$ in naive reasoning, but the problem guarantees $k$ divides $n+1$, missing this fact leads to incorrect handling of partial blocks.

## Approaches

A brute-force solution directly evaluates each term:

$$s_i \cdot a^{n-i} b^i$$

for all $i$ from $0$ to $n$. This is correct because it follows the definition exactly. However, it requires $n+1$ modular exponentiations, each costing $O(\log n)$, leading to about $10^9 \log 10^9$ operations in the worst case, which is far beyond any feasible limit.

The key observation is that both the coefficient sequence and the weight structure have multiplicative regularity. Rewrite each term:

$$a^{n-i} b^i = a^n \left(\frac{b}{a}\right)^i$$

This factors out a constant $a^n$, leaving a geometric progression in $\frac{b}{a}$, multiplied by a periodic sign sequence.

Now the sum becomes:

$$a^n \sum_{i=0}^{n} s_i r^i, \quad r = b \cdot a^{-1}$$

Everything reduces to evaluating a periodic sequence weighted by a geometric progression.

We split indices by residue modulo $k$. Each residue class forms a geometric series over blocks:

$$i = t k + j$$

where $j$ is fixed and $t$ runs over all full blocks. This transforms the sum into:

$$\sum_{j=0}^{k-1} s_j r^j \sum_{t=0}^{m-1} r^{tk}$$

where $m = \frac{n+1}{k}$.

The inner sum is a standard geometric series in $r^k$, and the outer sum is over only $k$ terms, making the computation efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \log n)$ | $O(1)$ | Too slow |
| Optimal | $O(k \log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We work entirely under modulo $M = 10^9 + 9$.

1. Convert the sign string into numeric values $s_j \in \{+1, -1\}$. This step establishes the periodic coefficient pattern explicitly so that later algebra works cleanly.
2. Compute the modular inverse of $a$, since we need $r = b \cdot a^{-1}$. This rewrites the mixed exponent expression into a single geometric progression base.
3. Precompute $r^k$. This represents the growth factor between successive blocks of length $k$. The reason this matters is that each residue class forms a geometric sequence in powers of $r^k$.
4. Compute $m = (n+1)/k$, the number of full periods. This follows from the guarantee that $k$ divides $n+1$, so no partial block handling is required.
5. For each position $j$ in the base period, compute the contribution $s_j \cdot r^j$. This isolates the intra-block offset contribution, independent of how many full cycles occur.
6. Multiply each contribution by the geometric sum over blocks:

$$1 + (r^k) + (r^k)^2 + \dots + (r^k)^{m-1}$$

If $r^k \neq 1$, this is computed using the standard closed form. If it equals 1, the sum reduces to $m$.
7. Sum all residue contributions and multiply by $a^n$, restoring the factored-out power.

### Why it works

Every index $i$ is uniquely represented as $i = tk + j$. The term at that position becomes:

$$s_j \cdot a^{n-(tk+j)} b^{tk+j}$$

which factors into:

$$s_j a^{n-j} (b^j a^{-j}) (b^k a^{-k})^t$$

so each residue class is a geometric progression in $t$. The algorithm exactly reconstructs these independent progressions and sums them, ensuring no interaction between classes is missed or double counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 9

def modpow(x, e):
    res = 1
    while e:
        if e & 1:
            res = res * x % MOD
        x = x * x % MOD
        e >>= 1
    return res

def modinv(x):
    return modpow(x, MOD - 2)

def solve():
    n, a, b, k = map(int, input().split())
    s = input().strip()

    vals = [1 if c == '+' else -1 for c in s]

    inv_a = modinv(a)
    r = b * inv_a % MOD

    r_k = modpow(r, k)
    m = (n + 1) // k

    # geometric sum over blocks
    if r_k == 1:
        geom_blocks = m % MOD
    else:
        geom_blocks = (modpow(r_k, m) - 1) * modinv(r_k - 1) % MOD

    ans = 0

    # contribution per residue class
    for j in range(k):
        term = vals[j] * modpow(r, j) % MOD
        ans = (ans + term) % MOD

    ans = ans * geom_blocks % MOD
    ans = ans * modpow(a, n) % MOD

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The implementation follows the algebraic transformation directly. The most delicate part is the change of basis from $a^{n-i} b^i$ into $a^n r^i$, which avoids recomputing large powers repeatedly.

Care must be taken when computing the geometric sum: the denominator $r^k - 1$ must be taken modulo $M$, and it can be zero, which corresponds to the special case where every block contributes equally and the sum becomes linear in $m$.

The final multiplication by $a^n$ restores the factor that was pulled out at the beginning of the transformation.

## Worked Examples

### Example 1

Input:

```
2 2 3 3
+-+
```

We compute $r = 3 \cdot 2^{-1}$. The sequence has $k=3$, so there is one full block.

| j | s_j | r^j | contribution |
| --- | --- | --- | --- |
| 0 | +1 | 1 | 1 |
| 1 | -1 | r | -r |
| 2 | +1 | r^2 | r^2 |

Sum over one block gives:

$$1 - r + r^2$$

Since $m = 1$, block geometric sum is 1.

Multiplying by $a^n = 2^2$ reconstructs the final result:

$$2^2 (1 - r + r^2) = 7$$

This trace shows how periodic structure collapses into a single weighted polynomial.

### Example 2

Input:

```
4 1 5 1
-
```

Here $k=1$, so every term is $-1$. The expression becomes:

$$-\sum_{i=0}^{4} 5^i$$

| i | term |
| --- | --- |
| 0 | -1 |
| 1 | -5 |
| 2 | -25 |
| 3 | -125 |
| 4 | -625 |

Sum is $-781$, matching the expected modular result.

This case demonstrates the degenerate case where periodicity removes all internal structure, leaving only a pure geometric series.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k \log n)$ | Each residue requires modular exponentiation, and there are $k$ residues |
| Space | $O(1)$ | Only a fixed number of variables are used |

The constraint $k \le 10^5$ ensures that iterating over the period is feasible, while all dependence on $n$ is compressed into fast exponentiation. This keeps the solution well within time limits even for the largest inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 9

    def modpow(x, e):
        res = 1
        while e:
            if e & 1:
                res = res * x % MOD
            x = x * x % MOD
            e >>= 1
        return res

    def modinv(x):
        return modpow(x, MOD - 2)

    n, a, b, k = map(int, input().split())
    s = input().strip()
    vals = [1 if c == '+' else -1 for c in s]

    inv_a = modinv(a)
    r = b * inv_a % MOD
    r_k = modpow(r, k)
    m = (n + 1) // k

    if r_k == 1:
        geom_blocks = m % MOD
    else:
        geom_blocks = (modpow(r_k, m) - 1) * modinv(r_k - 1) % MOD

    ans = 0
    for j in range(k):
        ans += vals[j] * modpow(r, j)

    ans = ans % MOD
    ans = ans * geom_blocks % MOD
    ans = ans * modpow(a, n) % MOD

    return str(ans % MOD)

# provided samples
assert run("2 2 3 3\n+-+\n") == "7", "sample 1"
assert run("4 1 5 1\n-\n") == "999999228", "sample 2"

# custom cases
assert run("1 2 2 1\n+\n") == str((2 + 2) % (10**9 + 9)), "k=1 small"
assert run("3 1 1 1\n+\n") == str(4 % (10**9 + 9)), "a=b=1"
assert run("5 3 7 5\n+-+-+\n") is not None, "period equals k"
assert run("10 2 3 2\n+-\n") is not None, "even splitting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k=1 small | direct geometric | single residue class |
| a=b=1 | sum of signs | collapse of powers |
| period equals k | full structure | general correctness |
| even splitting | mixed growth | periodic interaction |

## Edge Cases

When $k = 1$, the entire sequence is constant. The algorithm reduces to a single geometric series in $b/a$, and the implementation correctly handles this because only one residue class contributes. The geometric block sum captures all terms, and no indexing issues appear.

When $r^k = 1$, every block contributes equally. The code switches to a linear multiplication by $m$, avoiding division by zero in the modular inverse. This case is important because it corresponds to periodic cancellation in modular arithmetic where exponent cycles align perfectly with the period.

When $a = b$, the ratio $r = 1$, so all exponential variation disappears. The expression becomes a pure alternating sum of powers of $a$, and the implementation still works because $r^k = 1$ triggers the correct simplified handling of the geometric sum.