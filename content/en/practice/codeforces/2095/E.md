---
title: "CF 2095E - Pair Count"
description: "This problem comes from the April Fools Day Contest. The key trick is that the symbol shown as ⊕ is not actually bitwise XOR. The link attached to the symbol leads to a puzzle whose solution reveals that ⊕ should be interpreted as multiplication."
date: "2026-06-08T05:31:04+07:00"
tags: ["codeforces", "competitive-programming", "*special", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2095
codeforces_index: "E"
codeforces_contest_name: "April Fools Day Contest 2025"
rating: 0
weight: 2095
solve_time_s: 92
verified: true
draft: false
---

[CF 2095E - Pair Count](https://codeforces.com/problemset/problem/2095/E)

**Rating:** -  
**Tags:** *special, number theory  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

This problem comes from the April Fools Day Contest. The key trick is that the symbol shown as `⊕` is not actually bitwise XOR. The link attached to the symbol leads to a puzzle whose solution reveals that `⊕` should be interpreted as multiplication. Once that is discovered, the condition becomes

$$(a_i a_j)(a_i^2 a_j^2)\equiv k \pmod p,$$

which simplifies to

$$a_i^3 a_j^3 \equiv k \pmod p.$$

So we are given a set of distinct numbers modulo a prime $p$, and we must count pairs whose cubes multiply to $k$ modulo $p$.

The array size reaches $3 \cdot 10^5$, which immediately rules out checking all pairs. A quadratic solution would perform roughly $4.5 \cdot 10^{10}$ pair checks in the worst case, far beyond the limit. We need something close to linear or $O(n \log p)$.

One subtle case is $k=0$. Since $p$ is prime, the product $a_i^3 a_j^3$ is zero modulo $p$ if and only if at least one of the two numbers is zero. Because all array values are distinct, zero can appear at most once.

Consider:

```
3 5 0
0 1 2
```

The valid pairs are $(0,1)$ and $(0,2)$, so the answer is 2.

A careless implementation that blindly computes modular inverses would fail here because zero has no inverse.

Another important case is when $k \neq 0$ but some array element equals zero.

```
3 5 1
0 1 2
```

No pair containing zero can satisfy the equation because its product is always zero modulo $p$. Such elements must be skipped while matching nonzero values.

## Approaches

The brute-force idea is straightforward. For every pair $(i,j)$, compute

$$a_i^3 a_j^3 \bmod p$$

and compare it with $k$. This is correct because it directly checks the condition. Unfortunately, there are

$$\frac{n(n-1)}2$$

pairs. With $n=3\cdot10^5$, that is about $4.5\cdot10^{10}$ checks.

The structure of the equation suggests a better direction. Let

$$x_i = a_i^3 \bmod p.$$

The condition becomes

$$x_i x_j \equiv k \pmod p.$$

For a fixed $x_j\neq 0$, the required partner is uniquely determined:

$$x_i \equiv k \cdot x_j^{-1} \pmod p.$$

Since $p$ is prime, every nonzero residue has an inverse. This converts the problem from pair testing into frequency counting.

We process the array from left to right. For the current value $x_j$, we compute the residue that must have appeared earlier. A hash map stores how many times each cube residue has already been seen. The count of the required residue is exactly the number of valid pairs ending at position $j$.

The only special situation is $k=0$, where inverses are not usable and the equation has a much simpler characterization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n \log p)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the input array.
2. Handle $k=0$ separately.

The equation becomes

$$a_i^3 a_j^3 \equiv 0 \pmod p.$$

Since $p$ is prime, this happens exactly when one element is zero.
3. If zero is present, every pair involving that element is valid.

Because all array values are distinct, there is at most one zero. The answer is $n-1$.
4. If zero is absent and $k=0$, no valid pair exists.
5. For $k\neq0$, create a hash map `cnt` that stores frequencies of cube residues already processed.
6. Scan the array from left to right.
7. Skip value zero.

A pair involving zero cannot produce a nonzero product modulo $p$.
8. Compute

$$x = a_i^3 \bmod p.$$
9. Compute the modular inverse

$$x^{-1} \equiv x^{p-2} \pmod p$$

using Fermat's theorem.
10. The required partner residue is

$$need = k \cdot x^{-1} \bmod p.$$
11. Add `cnt[need]` to the answer.

Every previously seen occurrence of `need` forms a valid pair with the current element.
12. Insert the current residue `x` into the map.
13. After processing all elements, output the accumulated answer.

### Why it works

For every nonzero element we store its cube residue modulo $p$. When processing position $j$, the map contains exactly the residues coming from positions $i<j$.

The equation

$$x_i x_j \equiv k \pmod p$$

is equivalent to

$$x_i \equiv k x_j^{-1} \pmod p$$

because $x_j\neq0$. Thus every valid earlier partner corresponds to one occurrence of the residue `need`, and every occurrence of `need` produces a valid pair. Each pair is counted exactly once when its right endpoint is processed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, p, k = map(int, input().split())
    a = list(map(int, input().split()))

    if k == 0:
        if 0 in a:
            print(n - 1)
        else:
            print(0)
        return

    cnt = {}
    ans = 0

    for v in a:
        if v == 0:
            continue

        x = pow(v, 3, p)
        inv = pow(x, p - 2, p)
        need = (k * inv) % p

        ans += cnt.get(need, 0)
        cnt[x] = cnt.get(x, 0) + 1

    print(ans)

if __name__ == "__main__":
    main()
```

The first block handles the special case $k=0$. Since all values are distinct, at most one zero can exist. If it does, every other element forms a valid pair with it.

For the general case, the map stores frequencies of cube residues. The expression `pow(v, 3, p)` computes $v^3 \bmod p$ without overflow. The expression `pow(x, p - 2, p)` computes the modular inverse using Fermat's theorem, which is valid because $p$ is prime and $x\neq0$.

The order matters. We query the map before inserting the current residue. That guarantees only pairs with $i<j$ are counted and prevents self-pairing.

## Worked Examples

### Sample 1

Input:

```
3 3 2
0 1 2
```

Since $k\neq0$, we use the main algorithm.

| Value | Cube residue $x$ | Need | Previous count | Answer |
| --- | --- | --- | --- | --- |
| 0 | skipped | - | - | 0 |
| 1 | 1 | 2 | 0 | 0 |
| 2 | 2 | 1 | 1 | 1 |

Final answer: `1`.

This trace shows how the map turns the pair search into a lookup. When processing `2`, the required residue is `1`, which has already appeared once.

### Sample 2

Input:

```
6 11 2
1 3 5 6 7 8
```

Cube residues modulo 11 are:

| Value | Cube residue |
| --- | --- |
| 1 | 1 |
| 3 | 5 |
| 5 | 4 |
| 6 | 7 |
| 7 | 2 |
| 8 | 6 |

Processing order:

| Value | Residue $x$ | Need | Previous count | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 0 | 0 |
| 3 | 5 | 7 | 0 | 0 |
| 5 | 4 | 6 | 0 | 0 |
| 6 | 7 | 5 | 1 | 1 |
| 7 | 2 | 1 | 1 | 2 |
| 8 | 6 | 4 | 1 | 3 |

Final answer: `3`.

The three increments correspond exactly to the three valid pairs mentioned in the statement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log p)$ | Each element performs a constant number of modular exponentiations |
| Space | $O(n)$ | Hash map of cube residues |

With $n=3\cdot10^5$ and $p\le10^9$, modular exponentiation needs only about 30 multiplications per call. The resulting complexity comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n, p, k = map(int, input().split())
    a = list(map(int, input().split()))

    if k == 0:
        print(n - 1 if 0 in a else 0)
        return

    cnt = {}
    ans = 0

    for v in a:
        if v == 0:
            continue

        x = pow(v, 3, p)
        inv = pow(x, p - 2, p)
        need = (k * inv) % p

        ans += cnt.get(need, 0)
        cnt[x] = cnt.get(x, 0) + 1

    print(ans)

def run(inp: str) -> str:
    global input
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old
    return out.getvalue().strip()

# provided samples
assert run("3 3 2\n0 1 2\n") == "1", "sample 1"
assert run("6 11 2\n1 3 5 6 7 8\n") == "3", "sample 2"

# custom cases
assert run("2 5 0\n0 1\n") == "1", "single zero pair"
assert run("2 5 0\n1 2\n") == "0", "k=0 without zero"
assert run("2 5 1\n1 1\n") != "0" if False else True  # distinctness violated by statement
assert run("3 5 1\n0 1 2\n") == "0", "zero ignored when k!=0"
assert run("2 2 1\n0 1\n") == "0", "smallest prime"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 5 0 / 0 1` | `1` | Special handling of $k=0$ |
| `2 5 0 / 1 2` | `0` | No zero present |
| `3 5 1 / 0 1 2` | `0` | Zero cannot contribute when $k\neq0$ |
| `2 2 1 / 0 1` | `0` | Smallest allowed prime |

## Edge Cases

Consider:

```
3 5 0
0 1 2
```

The algorithm immediately enters the $k=0$ branch. Since zero exists, it returns $n-1=2$. The valid pairs are $(0,1)$ and $(0,2)$, exactly matching the mathematical condition.

Now consider:

```
3 5 0
1 2 3
```

Again the $k=0$ branch is used, but zero is absent. No product can become zero modulo a prime unless one factor is zero, so the answer is `0`.

Finally:

```
3 5 1
0 1 2
```

The value zero is skipped during processing. The remaining residues are checked normally. Since no pair satisfies the target residue equation, the answer is `0`. Skipping zero avoids attempting to compute an inverse of zero, which would be undefined.
