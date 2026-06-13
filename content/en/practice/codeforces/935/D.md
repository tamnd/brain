---
title: "CF 935D - Fafa and Ancient Alphabet"
description: "We are given two words of equal length over an alphabet consisting of symbols 1...m. Some positions are known, while others were erased and are represented by 0. Every erased position is filled independently and uniformly with one of the m alphabet symbols."
date: "2026-06-13T03:22:46+07:00"
tags: ["codeforces", "competitive-programming", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 935
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 465 (Div. 2)"
rating: 1900
weight: 935
solve_time_s: 264
verified: true
draft: false
---

[CF 935D - Fafa and Ancient Alphabet](https://codeforces.com/problemset/problem/935/D)

**Rating:** 1900  
**Tags:** math, probabilities  
**Solve time:** 4m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two words of equal length over an alphabet consisting of symbols `1...m`. Some positions are known, while others were erased and are represented by `0`.

Every erased position is filled independently and uniformly with one of the `m` alphabet symbols. After all replacements are made, we obtain two complete words. We must compute the probability that the first word is lexicographically larger than the second.

The answer is not required as a fraction. If the probability is

$$\frac{P}{Q},$$

we must print

$$P \cdot Q^{-1} \pmod{10^9+7}.$$

Since $m \le 10^5$, the denominator is always coprime to the modulus $10^9+7$, so modular inverses exist.

The length of the words can also reach $10^5$. Any algorithm that explicitly enumerates assignments of erased symbols is impossible. Even a single unknown position already introduces $m$ possibilities, and with many unknown positions the number of completions becomes exponential.

The time limit strongly suggests a linear or near-linear solution. Processing each position once is completely safe, while anything quadratic in $n$ is ruled out.

Several situations are easy to mishandle.

Consider

```
n = 1, m = 2
S1 = [0]
S2 = [1]
```

The unknown symbol in `S1` becomes either `1` or `2`. Only one of the two possibilities produces a larger word, so the answer is $1/2$. A solution that treats unknown positions greedily instead of probabilistically would fail.

Consider

```
n = 2, m = 3
S1 = [0, 3]
S2 = [0, 1]
```

The first position does not immediately determine the comparison because both symbols are unknown. We must account for the probability that they become equal and continue to the second position. Ignoring the "still equal" state produces an incorrect result.

Consider

```
n = 2, m = 5
S1 = [2, 1]
S2 = [2, 4]
```

The first position is equal and fixed. The second position decides the comparison immediately, and the answer is exactly zero. A probabilistic transition should stop as soon as a fixed unequal pair is encountered.

Another subtle case is

```
n = 1, m = 5
S1 = [0]
S2 = [0]
```

Both symbols are unknown. Among the $25$ assignments, exactly $10$ satisfy `S1 > S2`. The probability is

$$\frac{10}{25}=\frac{2}{5}.$$

The counting formula for two unknown symbols must be derived carefully.

## Approaches

A brute-force solution would generate every possible completion of both words, compare the resulting strings, count successful outcomes, and divide by the total number of outcomes.

Suppose there are $k$ erased positions in total. The number of completions is $m^k$. With $m=10^5$ and $k$ potentially close to $2\cdot10^5$, this is astronomically large. Even for very small values it becomes infeasible.

The key observation comes from how lexicographic comparison works.

When comparing two words, only the first position where they differ matters. Everything after that position becomes irrelevant. This means that while scanning from left to right, we only need to know one piece of information:

What is the probability that all previous positions ended up equal?

Let this probability be `same`.

At a position, some fraction of assignments makes the first word larger immediately. Those outcomes contribute directly to the final answer. Another fraction keeps the two prefixes equal, allowing the comparison to continue.

This transforms the problem into a simple left-to-right probability DP with only one state.

For each position we compute:

1. The probability that this position makes `S1 > S2`, assuming all previous positions were equal.
2. The probability that this position keeps them equal.

The first quantity contributes to the answer. The second quantity updates `same`.

Every position can be processed independently in constant time, producing an $O(n)$ solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m^k)$ | $O(k)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

Let `MOD = 10^9 + 7`.

Let `same` denote the probability that all positions processed so far are equal.

Initially,

$$same = 1.$$

Let `ans` store the probability that the first word is already known to be lexicographically larger.

### 1. Precompute modular inverses

We repeatedly divide by `m` and `m²`, so compute

$$inv_m = m^{-1} \pmod{MOD}.$$

### 2. Scan positions from left to right

For each position, examine the pair `(a[i], b[i])`.

The contribution depends on four cases.

### 3. Both symbols are known

If both values are fixed:

If `a[i] > b[i]`, then every assignment represented by `same` becomes successful.

Add `same` to the answer and stop.

If `a[i] < b[i]`, success becomes impossible and we stop.

If they are equal, continue.

### 4. First symbol unknown, second known

Suppose `a[i]=0` and `b[i]=x`.

Among the `m` possible values of `a[i]`:

`m-x` values are greater than `x`.

So the probability that this position immediately gives `S1>S2` is

$$\frac{m-x}{m}.$$

Add

$$same \cdot \frac{m-x}{m}$$

to the answer.

Exactly one value keeps equality, namely `a[i]=x`.

Update

$$same \leftarrow same \cdot \frac1m.$$

### 5. First known, second unknown

Suppose `a[i]=x` and `b[i]=0`.

Among the `m` choices for `b[i]`:

`x-1` values are smaller than `x`.

Thus the probability that this position makes `S1>S2` equals

$$\frac{x-1}{m}.$$

Add

$$same \cdot \frac{x-1}{m}.$$

Only one value preserves equality, so again

$$same \leftarrow same \cdot \frac1m.$$

### 6. Both symbols unknown

There are $m^2$ equally likely assignments.

The number of pairs with first symbol larger than second symbol is

$$\frac{m(m-1)}2.$$

Thus the probability that this position immediately produces `S1>S2` is

$$\frac{m(m-1)/2}{m^2} = \frac{m-1}{2m}.$$

Add

$$same \cdot \frac{m(m-1)/2}{m^2}.$$

Equality occurs in exactly `m` assignments, so

$$same \leftarrow same \cdot \frac1m.$$

### 7. Finish the scan

If all positions remain equal, the words are equal and do not contribute to the probability.

Output `ans`.

### Why it works

At every step, `same` equals the probability that all previously processed positions are equal after random replacement.

Lexicographic comparison depends only on the first position where the words differ. When processing a position, every outcome falls into exactly one of three categories:

1. The first word becomes larger.
2. The second word becomes larger.
3. The position remains equal.

The first category contributes permanently to the final answer. The second category can never contribute later. The third category is the only one that allows future positions to matter, so its probability becomes the new value of `same`.

Since these categories partition all possible assignments, and every position is processed under the condition that all earlier positions were equal, the accumulated probability is exactly the probability that the first word is lexicographically larger.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def main():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    inv_m = pow(m, MOD - 2, MOD)
    inv_m2 = inv_m * inv_m % MOD
    inv2 = (MOD + 1) // 2

    same = 1
    ans = 0

    for x, y in zip(a, b):
        if x == 0 and y == 0:
            greater_pairs = m * (m - 1) // 2
            ans = (ans + same * (greater_pairs % MOD) % MOD * inv_m2) % MOD
            same = same * inv_m % MOD

        elif x == 0:
            ans = (ans + same * (m - y) % MOD * inv_m) % MOD
            same = same * inv_m % MOD

        elif y == 0:
            ans = (ans + same * (x - 1) % MOD * inv_m) % MOD
            same = same * inv_m % MOD

        else:
            if x > y:
                ans = (ans + same) % MOD
                break
            elif x < y:
                break

    print(ans)

if __name__ == "__main__":
    main()
```

The variable `same` is the central state of the algorithm. It always represents the probability that every processed position ended up equal.

The three probabilistic cases correspond directly to the counting arguments from the walkthrough. Since all arithmetic is performed modulo `MOD`, divisions are replaced by multiplication with modular inverses.

The case with two unknown symbols deserves special attention. The number of ordered pairs `(u,v)` satisfying `u>v` is not `m²/2`. Equal pairs must be excluded first. The correct count is

$$1+2+\cdots+(m-1)=\frac{m(m-1)}2.$$

Another subtle detail is stopping when two fixed symbols differ. Once the first differing position is known, later positions can never influence the lexicographic result.

## Worked Examples

### Sample 1

Input

```
1 2
0
1
```

| Position | a[i] | b[i] | same before | Contribution | same after | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | (2-1)/2 = 1/2 | 1/2 | 1/2 |

The only unknown symbol can be either `1` or `2`. Exactly one choice produces a larger word, so the probability is $1/2$.

### Example 2

Input

```
2 3
0 3
0 1
```

| Position | a[i] | b[i] | same before | Contribution | same after | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 3/9 = 1/3 | 1/3 | 1/3 |
| 2 | 3 | 1 | 1/3 | 1/3 | stop | 2/3 |

At the first position, one third of all assignments already satisfy `S1>S2`. Another third make the first symbols equal, allowing the second position to decide. Since `3>1`, all of that remaining probability is added, giving $2/3$.

This trace demonstrates the key invariant: `same` always represents the probability mass that survives to future positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each position is processed once |
| Space | $O(1)$ | Only a few variables are maintained |

With $n \le 10^5$, a linear scan is easily fast enough. The memory usage remains constant regardless of input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 1000000007

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    inv_m = pow(m, MOD - 2, MOD)
    inv_m2 = inv_m * inv_m % MOD

    same = 1
    ans = 0

    for x, y in zip(a, b):
        if x == 0 and y == 0:
            greater_pairs = m * (m - 1) // 2
            ans = (ans + same * (greater_pairs % MOD) % inv_m2) % MOD
            same = same * inv_m % MOD

        elif x == 0:
            ans = (ans + same * (m - y) % MOD * inv_m) % MOD
            same = same * inv_m % MOD

        elif y == 0:
            ans = (ans + same * (x - 1) % MOD * inv_m) % MOD
            same = same * inv_m % MOD

        else:
            if x > y:
                ans = (ans + same) % MOD
                break
            elif x < y:
                break

    return str(ans)

# provided sample
assert run("1 2\n0\n1\n") == "500000004"

# minimum size, fixed equal symbols
assert run("1 5\n3\n3\n") == "0"

# minimum size, fixed greater
assert run("1 5\n4\n2\n") == "1"

# both unknown, m=2 => probability 1/4
assert run("1 2\n0\n0\n") == "250000002"

# fixed equal prefix, later position decides
assert run("2 5\n2 5\n2 1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 / 3 / 3` | `0` | Equal words never count |
| `1 5 / 4 / 2` | `1` | Immediate fixed victory |
| `1 2 / 0 / 0` | `250000002` | Correct counting for two unknown symbols |
| `2 5 / 2 5 / 2 1` | `1` | Equal prefix followed by fixed deciding position |

## Edge Cases

Consider

```
1 2
0
0
```

There are four equally likely assignments:

```
(1,1)
(1,2)
(2,1)
(2,2)
```

Only `(2,1)` satisfies `S1>S2`, so the probability is `1/4`. The algorithm computes

$$\frac{2(2-1)/2}{2^2} = \frac14,$$

which matches the exact count.

Consider

```
2 5
2 1
2 4
```

The first symbols are equal, so processing continues. At the second position, `1<4`, meaning the first differing position already favors the second word. The algorithm immediately stops and returns zero.

Consider

```
2 3
0 3
0 1
```

The first position contributes probability mass to three groups: larger, smaller, and equal. Only the equal group survives into the second position. The update

$$same \leftarrow same \cdot \frac13$$

captures exactly that surviving probability. When the second position is processed, every surviving assignment wins because `3>1`.

These examples illustrate the fundamental invariant: `same` always equals the probability that all earlier positions remain equal, which is precisely the condition required for later positions to influence the lexicographic comparison.
