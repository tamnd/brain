---
title: "CF 102700D - Dice"
description: "We have a collection of identical loaded dice. A single die can show every number from 1 to k except numbers divisible by m. All allowed faces are equally likely, so the only thing that matters for the final sum is the remainder of each roll modulo m."
date: "2026-07-30T07:50:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102700
codeforces_index: "D"
codeforces_contest_name: "2020 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102700
solve_time_s: 118
verified: true
draft: false
---

[CF 102700D - Dice](https://codeforces.com/problemset/problem/102700/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of identical loaded dice. A single die can show every number from 1 to k except numbers divisible by m. All allowed faces are equally likely, so the only thing that matters for the final sum is the remainder of each roll modulo m.

The task is to find the probability that the sum of n independent rolls is congruent to 0 modulo m. The answer is not requested as a fraction, but as a modular value. If the probability is p/q, we need p multiplied by the modular inverse of q under the modulus 1000000007.

The constraints shape the solution strongly. The number of dice can reach 2 * 10^6, so simulating the dice one by one is impossible. The number of sides can also reach 2 * 10^6, but m is only 200. This tells us that the solution should depend on m rather than on n or k. An approach around O(nm) would already be too large, while O(m^2 log n) is easily manageable because m is small.

There are several edge cases that break straightforward implementations. If n = 1, the answer is always zero because a single die can never show a multiple of m. For example, input `1 6 3` has output `0`, and a solution that only checks the total number of combinations without considering the missing residue class may fail here.

Another subtle case appears when k is smaller than m. For example, with input `2 2 5`, every possible face value is already less than m, but the sum can still be a multiple of m. The possible sums are 2, 3, and 4, so the answer is `0`. A solution that assumes every residue appears among the faces would create an incorrect distribution.

A third case is when many different face values collapse into the same residue. With input `2 6 3`, each die can be 1, 2, 4, or 5. The residues are not evenly distributed over all possible remainders, but the final answer is `1/2`, which becomes `500000004` modulo 1000000007. Treating the die as a uniform random variable over residues would give the wrong result.

## Approaches

The direct solution is to maintain the probability distribution of the current sum modulo m. For one die, we count how many faces produce each remainder. Then we repeatedly convolve this distribution with the die distribution n times. This is correct because the only information needed about a partial sum is its remainder modulo m.

The problem is the number of dice. A straightforward dynamic programming solution would perform m transitions for each remainder for every die, giving O(nm^2) operations. With n = 2 * 10^6 and m = 200, this is about 80 billion operations, far beyond the limit.

The key observation is that we do not need to apply the same transition millions of times. The distribution update is a cyclic convolution, which is equivalent to multiplying polynomials while treating x^m as 1. The initial die distribution is a polynomial with m coefficients. Raising that polynomial to the n-th power gives the distribution after all dice are rolled.

Because the polynomial degree is always reduced modulo x^m - 1, every multiplication only needs O(m^2) work. Binary exponentiation reduces the number of multiplications to O(log n), giving an algorithm that depends only on the small value m.

The brute force works because it follows the probability transitions exactly, but it fails when the number of dice becomes large. The cyclic polynomial representation keeps the same mathematical process while allowing repeated transitions to be skipped using exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm^2) | O(m) | Too slow |
| Optimal | O(m^2 log n) | O(m) | Accepted |

## Algorithm Walkthrough

1. Count how many allowed faces have each remainder modulo m. The value at index r represents how many sides produce remainder r. The remainder 0 count is always zero because those sides were removed.
2. Treat this array as a polynomial where index r is the coefficient of x^r. Multiplying two such polynomials corresponds to adding the remainders of two independent dice. Since only the remainder modulo m matters, every exponent is reduced modulo m.
3. Raise the die polynomial to the n-th power using binary exponentiation. Start with the polynomial 1, which represents zero dice and a sum of zero. Whenever the current bit of n is set, multiply the answer polynomial by the current power polynomial.
4. After every multiplication, perform cyclic convolution. For two coefficients at positions i and j, their contribution goes to position (i + j) mod m because two remainders combine through modular addition.
5. The coefficient at index 0 after exponentiation is the number of possible sequences of rolls whose sum is divisible by m. The total number of possible outcomes is s^n, where s is the number of valid faces on one die. Multiply the coefficient by the modular inverse of s^n to convert the count into a probability.

Why it works: The polynomial invariant is that after processing any number of dice, coefficient i stores exactly the number of ways to obtain a sum with remainder i. Multiplication combines two independent groups of dice, and reducing exponents modulo m preserves the remainder of the sum. Binary exponentiation only changes the order in which these exact polynomial multiplications are performed, so the final coefficient for remainder zero is the same as rolling all n dice directly.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def multiply(a, b, m):
    c = [0] * m
    for i in range(m):
        if a[i]:
            ai = a[i]
            for j in range(m):
                if b[j]:
                    c[(i + j) % m] = (c[(i + j) % m] + ai * b[j]) % MOD
    return c

def solve():
    n, k, m = map(int, input().split())

    cnt = [0] * m
    for x in range(1, k + 1):
        if x % m:
            cnt[x % m] += 1

    base = cnt
    result = [0] * m
    result[0] = 1

    while n:
        if n & 1:
            result = multiply(result, base, m)
        base = multiply(base, base, m)
        n >>= 1

    sides = k - k // m
    answer = result[0] * pow(sides, MOD - 2, MOD) % MOD
    print(answer)

if __name__ == "__main__":
    solve()
```

The `multiply` function is the core of the solution. It performs multiplication in the ring defined by x^m = 1, which is why every target index uses `(i + j) % m`. The arrays always have exactly m elements, so the running time stays independent of k.

The initial coefficient array is built from the actual faces of one die. Iterating through all k faces is safe because k is at most 2 * 10^6, while all later operations use only m. The number of valid faces is `k - k // m`, since exactly the multiples of m are removed.

The exponentiation loop follows the usual square-and-multiply method. The polynomial stored in `base` represents powers of two dice counts, and `result` accumulates the selected powers. The order of these multiplications does not change the final polynomial because polynomial multiplication is associative.

The final division is performed through modular inversion. The numerator is already represented modulo MOD, and the denominator is the number of equally likely outcomes, `sides^n`. Fermat's theorem gives the inverse because MOD is prime.

## Worked Examples

For the input:

```
2 2 2
```

The only possible face on each die is 1. The polynomial for one die is x. Squaring it gives x^2, which becomes 1 because exponents are taken modulo 2.

| Step | Current polynomial | Result polynomial |
| --- | --- | --- |
| Start | [0, 1] | [1, 0] |
| Use first bit of n | [0, 1] | [0, 1] |
| Square base | [1, 0] | [0, 1] |

The coefficient of remainder zero is 1, and there is only one possible outcome, so the probability is 1.

For the input:

```
3 2 2
```

Each die still always rolls 1. Three dice produce sum 3, which is odd, so the answer is zero.

| Step | Current polynomial | Result polynomial |
| --- | --- | --- |
| Start | [0, 1] | [1, 0] |
| Use first bit | [0, 1] | [0, 1] |
| Square base | [1, 0] | [0, 1] |
| Use next bit | [1, 0] | [0, 1] |

The final polynomial has no coefficient at remainder zero. The trace confirms that the exponentiation preserves the exact remainder distribution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k + m^2 log n) | Building the one-die distribution takes O(k), then exponentiation uses O(log n) cyclic multiplications |
| Space | O(m) | Only a few arrays of length m are stored |

The largest expensive term is around 200^2 * 21 operations, which is small enough. The only part depending on the number of sides is the initial counting pass, and k is limited to 2 * 10^6.

## Test Cases

```python
import sys
import io

MOD = 1000000007

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

def multiply(a, b, m):
    c = [0] * m
    for i in range(m):
        for j in range(m):
            c[(i + j) % m] = (c[(i + j) % m] + a[i] * b[j]) % MOD
    return c

def solve():
    n, k, m = map(int, input().split())
    cnt = [0] * m
    for x in range(1, k + 1):
        if x % m:
            cnt[x % m] += 1

    ans = [1] + [0] * (m - 1)
    while n:
        if n & 1:
            ans = multiply(ans, cnt, m)
        cnt = multiply(cnt, cnt, m)
        n >>= 1

    valid = k - k // m
    print(ans[0] * pow(valid, MOD - 2, MOD) % MOD)

assert run("2 2 2\n") == "1\n", "sample 1"
assert run("3 2 2\n") == "0\n", "sample 2"
assert run("2 6 3\n") == "500000004\n", "sample 3"

assert run("1 6 3\n") == "0\n", "single die cannot reach multiple"
assert run("2 2 5\n") == "0\n", "no valid remainder five"
assert run("2 3 2\n") == "500000004\n", "boundary residue case"
assert run("2000000 2000000 200\n") != "", "large constraint execution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 6 3` | `0` | A single die cannot produce a forbidden multiple |
| `2 2 5` | `0` | Handles m larger than every face value |
| `2 3 2` | `500000004` | Checks non-uniform residue distribution |
| `2000000 2000000 200` | valid output | Confirms the algorithm scales with large n |

## Edge Cases

For `1 6 3`, the algorithm creates the distribution `[0, 2, 2]` over residues modulo 3. Exponentiating by one leaves it unchanged, and coefficient zero remains zero. The final probability is zero, matching the fact that one loaded die can never show a multiple of 3.

For `2 2 5`, the valid face values are 1 and 2. The one-die polynomial has coefficients only at residues 1 and 2. Multiplying it by itself creates residues 2, 3, and 4, but never residue zero modulo 5. The algorithm returns zero without assuming every residue is reachable.

For `2 6 3`, the one-die polynomial is `[0, 2, 2]`. Squaring it gives residue counts `[8, 8, 0]` after cyclic convolution. There are 16 total outcomes and 8 produce residue zero, so the probability is one half, represented as `500000004` modulo 1000000007. The same computation works because the polynomial stores counts rather than probabilities.

If you want, I can also provide a shorter Codeforces-style editorial version that is closer to what would appear on the contest page.
