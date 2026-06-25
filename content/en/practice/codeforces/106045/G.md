---
title: "CF 106045G - GCD vs. LCM"
description: "We need to construct an array of n positive integers with a very specific property. Let G be the gcd of the whole array. For every position i, if we remove the i-th element and compute the gcd of the remaining n - 1 numbers, that gcd must become strictly larger than G."
date: "2026-06-25T12:42:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106045
codeforces_index: "G"
codeforces_contest_name: "IUT Intra University Programming Contest 2025"
rating: 0
weight: 106045
solve_time_s: 47
verified: true
draft: false
---

[CF 106045G - GCD vs. LCM](https://codeforces.com/problemset/problem/106045/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct an array of `n` positive integers with a very specific property.

Let `G` be the gcd of the whole array. For every position `i`, if we remove the `i`-th element and compute the gcd of the remaining `n - 1` numbers, that gcd must become strictly larger than `G`.

At the same time, the lcm of the entire array must not exceed a given limit `l`.

For each test case we either output any valid array or report that no such array exists.

The input contains up to `10^5` test cases, and the sum of all `n` values is at most `2 · 10^5`. That immediately suggests that we can afford work proportional to `n` per test case, but anything quadratic in `n` would be far too expensive.

The bound `l ≤ 10^18` is the most interesting constraint. Since the answer only depends on divisibility structure, we should expect a number-theoretic construction whose lcm stays within this limit.

The dangerous part of the problem is that the condition must hold for _every_ removed element. A construction that only works for some positions is invalid.

Consider `n = 3` and the array:

```
6 10 15
```

The gcd of all numbers is `1`.

Removing `6` leaves `{10,15}`, whose gcd is `5`.

Removing `10` leaves `{6,15}`, whose gcd is `3`.

Removing `15` leaves `{6,10}`, whose gcd is `2`.

All are strictly larger than `1`, so this array is interesting.

Now consider:

```
2 4 8
```

The gcd of all numbers is `2`.

Removing `8` leaves `{2,4}`, whose gcd is still `2`.

The condition requires a _strict_ increase, so this array is invalid.

Another easy mistake is assuming that repeating numbers helps. For example:

```
6 6 6
```

The gcd of the whole array is `6`, and removing any element still leaves gcd `6`. The condition fails everywhere.

These examples show that every element must be responsible for destroying some common divisor that all other elements share.

## Approaches

A brute-force mindset starts by trying to directly satisfy the definition.

We could generate candidate arrays, compute the gcd of the whole array, then for every position compute the gcd of the remaining elements and verify the condition. This is correct as a checker, but completely impractical as a construction strategy. The search space is enormous, and even checking many candidates would be hopeless.

The key is to understand what the condition implies structurally.

Let the gcd of the whole array be `G`. Divide every element by `G`. After this normalization, the gcd of the entire array becomes `1`.

Now focus on a fixed position `i`.

Since removing `a[i]` must increase the gcd, the remaining numbers have some common divisor greater than `1`. Let `p_i` be any prime factor of that gcd.

Then `p_i` divides every element except `a[i]`.

Because the gcd of the entire normalized array is `1`, that same prime cannot divide `a[i]`. Otherwise it would divide every element.

So each position `i` has a prime `p_i` that divides all elements except the `i`-th one.

An even stronger fact follows. These primes must be distinct.

Suppose `p_i = p_j = p`.

Since `p` divides all elements except `a[i]`, it divides `a[j]`.

Since `p` divides all elements except `a[j]`, it divides `a[i]`.

Hence `p` divides every element, contradicting the fact that the normalized gcd is `1`.

So any interesting array of length `n` requires at least `n` distinct primes.

Since every such prime must divide the lcm, we obtain a necessary condition:

$$\text{LCM} \ge p_1 p_2 \cdots p_n$$

The smallest possible product of `n` distinct primes is obtained by taking the first `n` primes:

$$2 \cdot 3 \cdot 5 \cdot 7 \cdots$$

If that product already exceeds `l`, no solution can exist.

This observation also gives the construction.

Let

$$P = p_1 p_2 \cdots p_n$$

where `p_1, ..., p_n` are the first `n` primes.

Define

$$a_i = \frac{P}{p_i}.$$

Then:

- Every prime except `p_i` appears in `a_i`.
- The gcd of all numbers is `1`.
- Removing `a_i` leaves numbers all divisible by `p_i`, so the gcd becomes at least `p_i > 1`.
- The lcm is exactly `P`.

Thus the construction is valid whenever `P ≤ l`.

Since `l ≤ 10^18`, the product of the first primes exceeds the limit very quickly. In fact only the first fifteen primes fit:

$$2 \cdot 3 \cdot 5 \cdots 47
= 614889782588491410.$$

Multiplying by the next prime `53` already exceeds `10^{18}`. So for `n > 15`, a solution is automatically impossible.

The entire problem reduces to checking whether the product of the first `n` primes is at most `l`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | Exponential | Exponential | Too slow |
| Prime Product Construction | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the first fifteen primes.
2. Precompute their prefix products.

The product of the first fifteen primes is still within `10^18`, so 64-bit arithmetic is sufficient.
3. For a test case with value `n`:

If `n > 15`, output `-1`.

No interesting array can exist because any valid array would require at least `n` distinct primes in its lcm.
4. Let `P` be the product of the first `n` primes.
5. If `P > l`, output `-1`.

Even the minimum possible lcm of an interesting array would exceed the allowed limit.
6. Construct the array

$$a_i = P / p_i.$$
7. Output the constructed array.

### Why it works

After normalization, every position must correspond to a distinct prime that divides all other elements and does not divide that position's element. This forces the lcm to contain at least `n` distinct primes. The smallest possible lcm is obtained by using the first `n` primes.

The construction achieves exactly that lower bound. The gcd of all elements is `1` because every prime is missing from one element. When element `i` is removed, the prime `p_i` appears in every remaining element, so the gcd of the remaining set is at least `p_i > 1`. Hence every removal strictly increases the gcd.

Since the lcm of the construction is exactly `P`, it satisfies the limit precisely when `P ≤ l`.

## Python Solution

```python
import sys
input = sys.stdin.readline

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

pref = [1]
for p in primes:
    pref.append(pref[-1] * p)

t = int(input())
ans = []

for _ in range(t):
    n, l = map(int, input().split())

    if n > 15:
        ans.append("-1")
        continue

    P = pref[n]

    if P > l:
        ans.append("-1")
        continue

    arr = [str(P // p) for p in primes[:n]]
    ans.append(" ".join(arr))

sys.stdout.write("\n".join(ans))
```

The first section precomputes the first fifteen primes and the product of their prefixes. This allows every test case to answer the existence question in constant time.

The check `n > 15` is essential. Since `l` never exceeds `10^18`, the lcm cannot contain more than fifteen distinct primes. Any interesting array would require at least `n` distinct primes, making larger values impossible.

The construction itself is straightforward. If `P` is the product of the first `n` primes, each element is obtained by removing exactly one prime factor from `P`.

No gcd or lcm computation is required during execution. The mathematical proof guarantees correctness.

## Worked Examples

### Example 1

Input:

```
1
3 500
```

The first three primes are `2, 3, 5`.

`P = 30`.

| i | Prime Removed | Value |
| --- | --- | --- |
| 1 | 2 | 15 |
| 2 | 3 | 10 |
| 3 | 5 | 6 |

Output:

```
15 10 6
```

Verification:

| Removed Element | Remaining Numbers | GCD |
| --- | --- | --- |
| 15 | 10, 6 | 2 |
| 10 | 15, 6 | 3 |
| 6 | 15, 10 | 5 |

The gcd of all numbers is `1`, and every removal increases it.

### Example 2

Input:

```
1
4 200
```

The first four primes give:

$$P = 2 \cdot 3 \cdot 5 \cdot 7 = 210.$$

Since `210 > 200`, no valid array can exist.

| n | Minimum Possible LCM |
| --- | --- |
| 4 | 210 |

Output:

```
-1
```

This demonstrates the lower-bound argument. Even the best possible construction exceeds the allowed limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Outputting `n` numbers dominates the work |
| Space | O(n) | Storage of the constructed array |

The sum of all `n` values is at most `2 · 10^5`, so the total output size is the true bottleneck. The algorithm performs only simple arithmetic and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    pref = [1]
    for p in primes:
        pref.append(pref[-1] * p)

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, l = map(int, input().split())

        if n > 15:
            out.append("-1")
            continue

        P = pref[n]

        if P > l:
            out.append("-1")
            continue

        out.append(" ".join(str(P // p) for p in primes[:n]))

    return "\n".join(out)

# sample-like cases
assert run("1\n3 500\n") == "15 10 6"

assert run("1\n4 200\n") == "-1"

# minimum n
assert run("1\n2 6\n") == "3 2"

# exact boundary
assert run("1\n4 210\n") == "105 70 42 30"

# impossible because n > 15
assert run("1\n16 1000000000000000000\n") == "-1"

# l too small
assert run("1\n3 29\n") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 6` | `3 2` | Smallest valid size |
| `4 210` | Constructed array | Exact lcm boundary |
| `16 10^18` | `-1` | More than fifteen distinct primes required |
| `3 29` | `-1` | Minimum possible lcm already exceeds limit |

## Edge Cases

Consider:

```
1
2 5
```

For `n = 2`, the smallest possible lcm is `2 × 3 = 6`.

Since `6 > 5`, the algorithm outputs:

```
-1
```

This is correct because any interesting array of length two requires two distinct primes in its lcm.

Now consider:

```
1
15 1000000000000000000
```

The product of the first fifteen primes is

$$614889782588491410.$$

This fits inside the limit, so the algorithm constructs a valid array. Every element omits exactly one prime factor, preserving the invariant that removing that element restores the missing prime to the gcd.

Finally consider:

```
1
16 1000000000000000000
```

Even before checking `l`, the algorithm outputs `-1`.

Any interesting array would require sixteen distinct primes in its lcm, but the product of the first sixteen primes already exceeds `10^{18}`. No valid construction can exist. This is exactly the impossibility condition proved in the solution.
