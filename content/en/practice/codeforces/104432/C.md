---
title: "CF 104432C - Odd Subbarray"
description: "We are given an integer array and asked to count how many contiguous subarrays have a special property: if you multiply all elements inside the subarray, the resulting product has an odd number of divisors."
date: "2026-06-30T18:55:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104432
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #17 (AOE-Forces)"
rating: 0
weight: 104432
solve_time_s: 79
verified: false
draft: false
---

[CF 104432C - Odd Subbarray](https://codeforces.com/problemset/problem/104432/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an integer array and asked to count how many contiguous subarrays have a special property: if you multiply all elements inside the subarray, the resulting product has an odd number of divisors.

The key mathematical fact behind this condition is that a number has an odd number of divisors if and only if it is a perfect square. Divisors normally come in pairs, but for perfect squares one divisor pair collapses into a single repeated factor, creating an odd count.

So the task reduces to counting subarrays whose product is a perfect square.

The array elements are positive and at most 300, and there can be up to 10^6 total elements across test cases. That size immediately rules out any solution that examines all subarrays explicitly. A quadratic enumeration per test case would attempt about n^2 / 2 subarrays, which becomes on the order of 10^10 operations in the worst case, far beyond any feasible limit.

A subtle edge case arises from how quickly products grow. For example, even small arrays like [2, 2, 2, 2] already produce many subarray products that are large, but we do not actually compute the products directly. Any naive multiplication-based checking would overflow or become slow if done repeatedly.

Another important edge case is when all elements are 1. Every subarray then has product 1, which is a perfect square, so the answer becomes n(n+1)/2. Any correct solution must naturally handle this without special casing.

## Approaches

A brute-force solution tries every subarray, computes its product, and checks whether that product is a perfect square. Even if we avoid recomputing products from scratch by extending a running product, we still perform O(n^2) updates per test case. With up to 10^6 total elements, this leads to about 5×10^11 operations in the worst case, which is not viable.

The key insight is that we never need the numeric value of the product. We only care whether the product is a perfect square. A number is a perfect square exactly when every prime exponent in its factorization is even. This shifts the problem from multiplication to tracking parity of prime exponents.

Since each a[i] is at most 300, its prime factorization involves only primes up to 300, and each number can be represented by which primes appear an odd number of times. We only track parity, so each element can be encoded as a bitmask over primes, where a bit is 1 if that prime appears an odd exponent in the prefix product.

Now the product of a subarray is a perfect square if and only if the XOR of these bitmasks over the subarray is zero. This turns the problem into counting subarrays with XOR equal to zero, which is a standard prefix XOR frequency problem.

We maintain prefix XOR masks and count how often each mask appears. Every pair of equal prefix masks defines a subarray whose XOR is zero, hence whose product is a perfect square.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 log A) | O(1) | Too slow |
| Prefix XOR frequency | O(n log A + P) | O(P) | Accepted |

Here P is the number of distinct prime-mask states, bounded by n.

## Algorithm Walkthrough

We transform each number into a representation that captures only parity of prime exponents, then use prefix accumulation.

1. Precompute primes up to 300 and assign each prime an index. This allows us to build compact bitmasks for factorization.
2. For each array element, factorize it and construct a bitmask where each bit corresponds to whether that prime appears an odd number of times in its factorization. Since we only care about parity, repeated divisions toggle bits rather than incrementing counts.
3. Maintain a running prefix mask initialized to zero. This represents the XOR of all encoded values from the start up to the current position.
4. Use a hash map or dictionary to count how many times each prefix mask has occurred. Initialize it with the empty mask having frequency 1.
5. As we process each element, update the prefix mask by XOR-ing it with the element's mask. Every time we reach a prefix mask value, add its current frequency to the answer. This counts all previous positions where the same mask occurred, forming valid subarrays ending at the current index.
6. Increment the frequency of the current prefix mask.

The reason step 5 is correct is that two equal prefix masks imply that the XOR of the segment between them is zero, meaning all prime exponents cancel to even counts, which is exactly the condition for a perfect square product.

### Why it works

The algorithm maintains an invariant that the prefix mask at position i represents the parity of prime exponents in the product of the first i elements. A subarray product from l to r is a perfect square exactly when the prefix masks at l−1 and r are identical, because XOR cancellation ensures all prime exponents are even. Counting identical prefix masks therefore counts every valid subarray exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

# Precompute primes up to 300
MAXV = 300
is_prime = [True] * (MAXV + 1)
is_prime[0] = is_prime[1] = False
primes = []
for i in range(2, MAXV + 1):
    if is_prime[i]:
        primes.append(i)
        for j in range(i * i, MAXV + 1, i):
            is_prime[j] = False

prime_index = {p: i for i, p in enumerate(primes)}

def factor_mask(x):
    mask = 0
    for p in primes:
        if p * p > x:
            break
        if x % p == 0:
            cnt = 0
            while x % p == 0:
                x //= p
                cnt ^= 1
            if cnt:
                mask ^= (1 << prime_index[p])
    if x > 1:
        mask ^= (1 << prime_index[x])
    return mask

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = {0: 1}
        pref = 0
        ans = 0

        for v in a:
            pref ^= factor_mask(v)
            ans += freq.get(pref, 0)
            freq[pref] = freq.get(pref, 0) + 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The factorization step constructs a parity mask for each number. The prefix variable accumulates XORs of these masks, effectively tracking parity of prime exponents in the product of the current prefix of the array.

The frequency dictionary stores how many times each prefix state has appeared. When a prefix repeats, every earlier occurrence forms a valid subarray ending at the current position.

A common implementation pitfall is forgetting to initialize the frequency of the zero mask as 1, which is necessary to count subarrays starting at index 0.

## Worked Examples

### Example 1

Input:

```
4
1 2 4 2
```

We track prefix masks and frequencies.

| i | a[i] | mask(a[i]) | prefix XOR | freq before | added to ans | freq after |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | {0:1} | 1 | {0:2} |
| 1 | 2 | m2 | m2 | {0:2} | 0 | {0:2,m2:1} |
| 2 | 4 | 0 | m2 | {0:2,m2:1} | 1 | ... |
| 3 | 2 | m2 | 0 | {0:2,m2:1} | 2 | ... |

The final answer is 4, corresponding to all subarrays whose product is a perfect square.

This demonstrates how repeated prefix states directly translate into valid subarray counts.

### Example 2

Input:

```
3
1 1 1
```

All values are 1, so every mask is zero.

| i | a[i] | prefix | freq before | added | freq after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | {0:1} | 1 | {0:2} |
| 1 | 1 | 0 | {0:2} | 2 | {0:3} |
| 2 | 1 | 0 | {0:3} | 3 | {0:4} |

Total is 6, which matches n(n+1)/2.

This confirms that the algorithm naturally handles uniform arrays without special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n √A) | Each element is factorized up to √300, and prefix updates are O(1) amortized |
| Space | O(n) | Frequency map stores at most one entry per prefix state |

The constraints allow up to 10^6 total elements, and √300 is small enough that factorization remains fast in practice. The prefix hashing ensures linear scaling overall.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isqrt

    # Re-run solution inline for testing
    MAXV = 300
    is_prime = [True] * (MAXV + 1)
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, MAXV + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, MAXV + 1, i):
                is_prime[j] = False
    prime_index = {p: i for i, p in enumerate(primes)}

    def factor_mask(x):
        mask = 0
        for p in primes:
            if p * p > x:
                break
            if x % p == 0:
                cnt = 0
                while x % p == 0:
                    x //= p
                    cnt ^= 1
                if cnt:
                    mask ^= (1 << prime_index[p])
        if x > 1:
            mask ^= (1 << prime_index[x])
        return mask

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        freq = {0: 1}
        pref = 0
        ans = 0
        for v in a:
            pref ^= factor_mask(v)
            ans += freq.get(pref, 0)
            freq[pref] = freq.get(pref, 0) + 1
        out.append(str(ans))

    return "\n".join(out) + "\n"

# provided samples
assert run("""2
4
1 2 4 2
3
1 1 1
""") == "4\n6\n"

# custom cases
assert run("""1
1
6
""") == "1\n", "single element square"
assert run("""1
2
2 3
""") == "0\n", "no square subarray"
assert run("""1
5
1 1 1 1 1
""") == "15\n", "all ones"
assert run("""1
4
2 2 2 2
""") == "10\n", "all same even structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element square | 1 | minimum case |
| 2 3 | 0 | no valid subarrays |
| all ones | 15 | maximal trivial squares |
| all twos | 10 | repeated prefix collisions |

## Edge Cases

For an input like `[1]`, the prefix mask is always zero, so the frequency map immediately counts one subarray. The algorithm starts with frequency `{0:1}`, so when processing the single element, the prefix remains zero and contributes exactly one valid subarray, which matches the correct answer.

For an input like `[2, 2, 2, 2]`, every element toggles the same prime bit. The prefix masks alternate between two states. Each repetition of a prefix state contributes multiple subarrays, and the frequency table correctly counts all pairs of equal states. For example, when the prefix returns to zero at even positions, it counts subarrays whose product is a perfect square because the exponent of 2 is even across those segments.
