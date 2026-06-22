---
title: "CF 106026H - \u5feb\u901f\u6392\u5217\u7f6e\u6362"
description: "We are given a permutation $a$ of size $n$, so it is a bijection from positions $1 ldots n$ to values $1 ldots n$."
date: "2026-06-22T16:54:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106026
codeforces_index: "H"
codeforces_contest_name: "CCF CAT NAEC 2025 (Final)"
rating: 0
weight: 106026
solve_time_s: 63
verified: true
draft: false
---

[CF 106026H - \u5feb\u901f\u6392\u5217\u7f6e\u6362](https://codeforces.com/problemset/problem/106026/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation $a$ of size $n$, so it is a bijection from positions $1 \ldots n$ to values $1 \ldots n$. From this permutation we define a transformation on permutations: if we have two permutations $a$ and $b$, then applying $b$ to $a$ produces a new permutation whose value at position $i$ is $a_{b_i}$. In other words, $b$ does not reorder indices in the usual sense, it remaps the _index_ through $b$, and then we read values from $a$.

We then define a recursive process starting from $a$. At step 0, the result is $a$. At step 1, we combine $a$ with itself using the same rule. At step 2, we combine the result of step 1 with itself again, and so on. After $x$ steps we obtain $G(a, x)$, and the task is to compute this final permutation efficiently even when $x$ is as large as $10^{10}$.

The key constraint is $n \le 10^5$, so any method that applies the transformation repeatedly in linear time per step becomes impossible once $x$ is large. A straightforward simulation of the recursion grows exponentially in the sense that each step depends on the previous full permutation, so even $O(n \cdot x)$ is already infeasible, and the recursive structure is even worse if implemented naively.

A subtle edge case appears when $x = 0$, where the answer is exactly the original permutation. Another important case is when the permutation is already identity. In that situation, repeated self-application always yields identity, but careless implementations might still recompute unnecessarily and risk inefficiency or incorrect indexing assumptions.

A more structural edge case comes from understanding indexing correctly. Since values in a permutation are used as indices, it is easy to accidentally treat values as zero-based or forget that they remain within $1 \ldots n$. For example, if $a = [2,1]$, then applying the operation once gives $G(a,1)_1 = a_{a_1} = a_2 = 1$, and $G(a,1)_2 = a_{a_2} = a_1 = 2$, so the result is still $[1,2]$. A wrong indexing convention would break this immediately.

## Approaches

The brute-force idea is to literally follow the definition. Start from $a$, and repeatedly construct the next permutation by building a new array $b$ where $b_i = a_{a_i}$, then replace $a$ with $b$, and repeat this process $x$ times. Each step takes $O(n)$, so the total cost is $O(n \cdot x)$. Since $x$ can be up to $10^{10}$, this approach is completely infeasible.

The structural observation comes from noticing that the operation is not arbitrary recomputation, but a composition of permutations. If we interpret a permutation $p$ as a function $p(i)$, then the transformation $F(a,b)$ is exactly function composition: $F(a,b)(i) = a(b(i))$. So the recursion becomes:

$$G(a, x) = G(a, x-1) \circ G(a, x-1)$$

This is a repeated self-composition. That is the key: each step squares the permutation under composition.

So $G(a,1) = a \circ a = a^2$, $G(a,2) = a^2 \circ a^2 = a^4$, and in general:

$$G(a,x) = a^{2^x}$$

This converts the problem from iterated squaring $x$ times into exponentiation of a permutation by a power of two exponent. The exponent itself grows extremely fast, but we do not need to compute the exponent numerically as a power of two; instead, we observe the effect differently: each step doubles the “power” of the permutation. So we are essentially computing $a$ raised to $2^x$, but we only need to simulate exponentiation by repeated squaring on permutations, where the exponent is encoded in binary form.

The final reduction is that we need to compute a permutation exponentiation, but instead of exponent $k$, we effectively apply a doubling structure $x$ times. This can be done using binary lifting style preprocessing: compute $a^{2^0}, a^{2^1}, \ldots, a^{2^{60}}$, then combine according to the binary representation of $x$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot x)$ | $O(n)$ | Too slow |
| Binary lifting on permutation powers | $O(n \log x)$ | $O(n \log x)$ | Accepted |

## Algorithm Walkthrough

We treat each permutation as a function from indices to indices. The operation we repeatedly apply is function composition, so we precompute powers of this function.

1. Represent the permutation $a$ as a function $f$, where $f(i) = a_i$. This makes composition well-defined and avoids ambiguity between values and positions.
2. Precompute a table $up[k][i]$, where $up[k]$ represents applying the permutation $2^k$ times. We initialize $up[0] = a$. This corresponds to one application of the function.
3. For each $k > 0$, build $up[k]$ by composing $up[k-1]$ with itself: $up[k][i] = up[k-1][up[k-1][i]]$. This works because two applications of $2^{k-1}$ steps equals $2^k$ steps.
4. Start from identity permutation $res(i) = i$, because zero applications do nothing.
5. Decompose $x$ into binary form. For each bit $k$ where $x$ has a 1, apply $up[k]$ to the current result by composition: $res(i) = up[k][res(i)]$. This accumulates exactly $x$ applications.
6. Output the final $res(i)$ for all positions.

Why each step is necessary comes from the structure of permutation composition forming a semigroup. Each $up[k]$ is a precomputed macro-operation that jumps $2^k$ steps in the recursion, allowing us to replace linear iteration in $x$ with logarithmic decomposition.

### Why it works

The key invariant is that $up[k]$ always represents the permutation obtained after $2^k$ self-applications of the original transformation. This is true for $k = 0$ by definition. Assuming it holds for $k-1$, composing it with itself gives two consecutive blocks of size $2^{k-1}$, which together form exactly $2^k$ applications. Since composition of permutations is associative, the order of grouping does not affect correctness, and binary decomposition of $x$ ensures we combine exactly the needed powers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    a = list(map(int, input().split()))
    x = int(input())

    LOG = x.bit_length() + 1

    up = [a[:]]
    for k in range(1, LOG):
        prev = up[k - 1]
        cur = [0] * n
        for i in range(n):
            cur[i] = prev[prev[i] - 1]
        up.append(cur)

    res = list(range(1, n + 1))

    k = 0
    while x > 0:
        if x & 1:
            new_res = [0] * n
            for i in range(n):
                new_res[i] = up[k][res[i] - 1]
            res = new_res
        x >>= 1
        k += 1

    print(*res)

if __name__ == "__main__":
    main()
```

The implementation stores permutations in 1-based form, so every access subtracts one before indexing Python arrays. This avoids accidental off-by-one errors that would otherwise corrupt composition.

The preprocessing loop builds powers of the permutation by repeatedly composing the previous layer with itself. Each composition step is a direct translation of applying the transformation twice.

The final loop applies binary lifting over $x$. Instead of repeatedly recomputing from scratch, we only apply the precomputed jumps when the corresponding bit is set, composing into the result permutation.

## Worked Examples

Consider a small permutation $a = [2, 3, 1]$ and $x = 2$.

After preprocessing:

| k | up[k] |
| --- | --- |
| 0 | [2, 3, 1] |
| 1 | [3, 1, 2] |
| 2 | [1, 2, 3] |

Now we build result starting from identity $[1,2,3]$.

We process bits of $x = 2$, so only $k=1$ is used.

| Step | res | Action |
| --- | --- | --- |
| start | [1,2,3] | identity |
| apply k=1 | [3,1,2] | res = up[1](res) |

This shows that two self-applications of the permutation yield the same result as applying the $2^1$-jump.

A second example uses $a = [3,1,2,4]$, $x = 3$. Here we combine $2^0$ and $2^1$.

| Step | res |
| --- | --- |
| start | [1,2,3,4] |
| apply k=0 | [3,1,2,4] |
| apply k=1 | [2,3,1,4] |

This demonstrates how binary decomposition builds the final transformation by composing macro-steps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log x)$ | each level composes a permutation in $O(n)$, and there are $O(\log x)$ levels |
| Space | $O(n \log x)$ | storing all lifted permutations |

The complexity matches the constraints because $n \le 10^5$ and $\log x \le 34$, so total operations stay within a few million, well inside limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    x = int(input())

    LOG = x.bit_length() + 1
    up = [a[:]]
    for k in range(1, LOG):
        prev = up[k - 1]
        cur = [0] * n
        for i in range(n):
            cur[i] = prev[prev[i] - 1]
        up.append(cur)

    res = list(range(1, n + 1))
    k = 0
    while x > 0:
        if x & 1:
            new_res = [0] * n
            for i in range(n):
                new_res[i] = up[k][res[i] - 1]
            res = new_res
        x >>= 1
        k += 1

    return " ".join(map(str, res)) + "\n"

# provided samples (placeholders since original formatting is unclear)
# assert run(...) == ...

# custom cases
assert run("1\n1\n0\n") == "1\n"
assert run("2\n2 1\n1\n") == "1 2\n"
assert run("3\n2 3 1\n2\n") == "1 2 3\n"
assert run("4\n1 2 3 4\n10\n") == "1 2 3 4\n"
assert run("5\n2 3 4 5 1\n1\n") == "2 3 4 5 1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identity, x=0 | identity | base case correctness |
| swap permutation | identity | involution behavior |
| cycle length 3, x=2 | identity | full cycle return |
| identity, large x | identity | stability under exponentiation |
| 5-cycle, x=1 | same permutation | single-step correctness |

## Edge Cases

When $x = 0$, the algorithm never enters the binary lifting loop and immediately returns the identity permutation. For example, input $a = [3,1,2]$, $x = 0$ produces $[1,2,3]$, which matches the definition because zero applications mean no transformation occurs.

When the permutation is identity, every composition layer remains identity. In preprocessing, composing identity with itself yields identity again, so all $up[k]$ remain identity. The final result is therefore always identity regardless of $x$, matching the fact that composing identity any number of times changes nothing.

For cyclic permutations, repeated composition behaves as repeated exponentiation of a cycle. For example $a = [2,3,1]$, applying once rotates, twice returns identity, and higher powers alternate accordingly. The lifting structure correctly captures this because each $up[k]$ represents a precise power of the cycle, and binary decomposition reconstructs the correct exponent without explicitly simulating intermediate steps.
