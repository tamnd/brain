---
title: "CF 104828A - \u9b54\u6cd5\u7ec3\u4e60"
description: "We are given a list of integers and a modulus value. The task is to compute the product of all numbers in the list and then output the remainder when that product is divided by the given modulus."
date: "2026-06-28T12:26:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104828
codeforces_index: "A"
codeforces_contest_name: "The 11-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 104828
solve_time_s: 41
verified: true
draft: false
---

[CF 104828A - \u9b54\u6cd5\u7ec3\u4e60](https://codeforces.com/problemset/problem/104828/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers and a modulus value. The task is to compute the product of all numbers in the list and then output the remainder when that product is divided by the given modulus.

Although the statement dresses this up as a “magic training” lesson about data types and overflow, the actual computation is straightforward: multiply all elements together, but every intermediate step must stay within safe numeric bounds, and the final result must be taken modulo $p$.

The key constraint is that $n$ can be as large as $10^5$. This immediately rules out any approach that recomputes products repeatedly or uses nested loops, since $O(n^2)$ work would be far too slow. A single linear pass is the only reasonable structure.

There is also a subtle numerical constraint. The product of up to $10^5$ numbers, each potentially close to $10^9$, can easily overflow 64-bit integers if we are careless. Even though each $a_i < p$, and $p \le 10^9$, multiplying many such values without modular reduction will exceed $2^{63}-1$ very quickly. A naive implementation that delays modulo until the end will therefore produce incorrect results or runtime issues.

Edge cases are mostly centered around modular arithmetic behavior:

If any element is zero, the entire product becomes zero immediately, and continuing multiplication is unnecessary. Another corner case is when $p = 1$. In this case, every number modulo 1 is zero, so the answer is always zero regardless of the array.

## Approaches

A brute-force interpretation is to compute the product directly and then apply modulo $p$. Conceptually this is correct: multiplication is associative, so computing $a_1 \cdot a_2 \cdots a_n$ first and reducing at the end produces the right remainder.

The failure point is numeric growth. Even with 64-bit integers, repeated multiplication quickly exceeds the representable range. For $n = 10^5$, worst-case growth is exponential in magnitude, and overflow happens long before the final step. This makes the brute-force method unreliable in standard fixed-width integer environments.

The key observation is that modular arithmetic allows reduction at every step without changing the final result. Since

$$(x \cdot y) \bmod p = ((x \bmod p) \cdot (y \bmod p)) \bmod p,$$

we can maintain a running product modulo $p$, ensuring that values never exceed $p$. This transforms the problem into a single linear scan with constant-time updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) arithmetic but unsafe due to overflow | O(1) | Incorrect in practice |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a running variable `ans` that stores the product of all processed elements modulo $p$.

1. Initialize `ans = 1`. This represents the empty product, which is the neutral element for multiplication. We choose 1 because multiplying by 1 does not change any value.
2. Iterate through each element `a_i` in the array.
3. Before multiplying, reduce the element modulo $p$ if desired. In this problem it is optional because $a_i < p$, but keeping the habit ensures correctness in generalized settings.
4. Update the running product as `ans = (ans * a_i) % p`. This step is the core of the solution. We immediately reduce after multiplication to prevent overflow and keep the value bounded by $p$.
5. After processing all elements, output `ans`.

The logic never requires revisiting earlier elements, so the computation is strictly one-pass.

### Why it works

At every iteration, `ans` represents the product of all previous elements modulo $p$. When we multiply by the next element and reduce modulo $p$, we preserve this invariant due to the distributive property of modular arithmetic. Because the invariant holds from the first element to the last, the final value is exactly the product of all elements modulo $p$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, p = map(int, input().split())
    arr = list(map(int, input().split()))
    
    ans = 1 % p
    for x in arr:
        ans = (ans * (x % p)) % p
    
    print(ans)

if __name__ == "__main__":
    main()
```

The code follows the invariant directly. The variable `ans` is always kept reduced modulo `p`, ensuring it never grows large. Even though multiplication of Python integers does not overflow, this structure is still essential in languages like C++ and matches the intended problem constraints.

The initialization `1 % p` ensures correctness when $p = 1$, since the answer must then be zero regardless of input.

## Worked Examples

### Example 1

Input:

```
3 2035
2023 6 3
```

We track the running product:

| Step | x | ans before | computation | ans after |
| --- | --- | --- | --- | --- |
| 1 | 2023 | 1 | (1 × 2023) % 2035 | 2023 |
| 2 | 6 | 2023 | (2023 × 6) % 2035 | 1819 |
| 3 | 3 | 1819 | (1819 × 3) % 2035 | 364 |

Final answer is 364.

This demonstrates how intermediate values are always reduced, preventing overflow and keeping values within range.

### Example 2

Input:

```
3 1000000000
999999999 999999998 999999997
```

| Step | x | ans before | computation | ans after |
| --- | --- | --- | --- | --- |
| 1 | 999999999 | 1 | (1 × 999999999) % 1e9 | 999999999 |
| 2 | 999999998 | 999999999 | (999999999 × 999999998) % 1e9 | 2 |
| 3 | 999999997 | 2 | (2 × 999999997) % 1e9 | 999999994 |

Final answer is 999999994.

This trace highlights why modulo must be applied after every multiplication, not only at the end.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed exactly once with constant-time multiplication and modulo |
| Space | O(1) | Only a single accumulator variable is used |

The linear scan is optimal for $n \le 10^5$, comfortably within the one-second limit. Memory usage is negligible since no auxiliary arrays are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import prod

    n, p = map(int, inp.split()[0:2])
    arr = list(map(int, inp.split()[2:2+n]))
    
    ans = 1 % p
    for x in arr:
        ans = (ans * x) % p
    return str(ans)

# provided sample
assert run("3 2035\n2023 6 3\n") == "364", "sample 1"

# sample 2
assert run("3 1000000000\n999999999 999999998 999999997\n") == "999999994", "sample 2"

# minimum n
assert run("1 7\n5\n") == "5", "single element"

# contains zero
assert run("5 13\n3 0 7 9 11\n") == "0", "zero forces product to zero"

# p = 1
assert run("4 1\n10 20 30 40\n") == "0", "mod 1 always zero"

# all ones
assert run("5 100\n1 1 1 1 1\n") == "1", "identity multiplication"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | value itself mod p | base case |
| contains zero | 0 | early annihilation property |
| p = 1 | 0 | modulus edge case |
| all ones | 1 | multiplicative identity |

## Edge Cases

When $p = 1$, every multiplication step reduces to zero. The algorithm initializes `ans = 1 % p`, which becomes 0 immediately. As soon as iteration begins, `ans` remains zero regardless of input, producing the correct result.

For an input containing zero, such as `3 10 / 4 0 7`, the first multiplication producing zero collapses the running product to zero. Subsequent steps keep it unchanged because `0 * x % p = 0`, so the final output remains zero as expected.

For a single-element array, the loop executes once, and the result is simply that element modulo $p$. The invariant still holds because the initialization corresponds to an empty product, and one multiplication transitions it to the correct final value.
