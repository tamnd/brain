---
title: "CF 102218B - Buying Piles of Stones"
description: "Alice buys (M) piles. Every pile independently receives one of the (K) allowed positive sizes, each with probability (1/K). Once the sizes are known, the game is an ordinary Nim position. For Nim, the first player wins exactly when the bitwise XOR of all pile sizes is nonzero."
date: "2026-08-17T23:09:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "B"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 153
verified: false
draft: false
---

[CF 102218B - Buying Piles of Stones](https://codeforces.com/problemset/problem/102218/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

Alice buys (M) piles. Every pile independently receives one of the (K) allowed positive sizes, each with probability (1/K). Once the sizes are known, the game is an ordinary Nim position.

For Nim, the first player wins exactly when the bitwise XOR of all pile sizes is nonzero. Thus the problem is equivalent to finding the probability that the XOR of (M) independently chosen values from the set

[
C={c_1,c_2,\ldots,c_K}
]

is not zero. The required answer is this probability modulo (998244353), so division is performed with modular inverses.

The difficult part is the size of (M). It can be as large as (10^9), so we cannot process the piles one by one. The number of possible values is bounded by (2^{17}), which is the key structural constraint. It means the entire problem lives in a finite XOR group of only (131072) elements. That size is small enough for an (O(2^{17}\cdot17)) transform, while the huge (M) can be handled with binary exponentiation.

A brute force enumeration of all possible ordered sequences would have (K^M) cases. Even with (K=2) and (M=10^9), that is already hopeless. Enumerating all XOR states after every pile would also require (O(M2^{17})), which is too large because (M) is enormous.

There are several edge cases that can make an otherwise reasonable implementation wrong. With one pile, the XOR is simply its positive size, so Alice always wins. For example,

```
1 1
5
```

has answer (1). An implementation that treats zero XOR as a winning position would incorrectly return zero.

With only one possible pile size, every pile is identical. If (K=1), the XOR is zero when (M) is even and nonzero when (M) is odd. For example,

```
2 1
5
```

has answer (0), while

```
11 1
5
```

has answer (1). A solution that assumes several different values exist can mishandle this case.

Another boundary case is when the available sizes contain values near (2^{17}). The XOR of two values below (2^{17}) is still below (2^{17}), so an array of exactly (2^{17}) states is sufficient. For example, with

```
2 2
65536 131071
```

the only zero-XOR outcomes are the two equal choices, so Alice wins with probability (1/2). Using an array of size (2^{17}-1) would access an invalid state.

## Approaches

The direct solution follows immediately from the rules of Nim. Generate every possible sequence of (M) pile sizes, XOR all values in the sequence, and count the sequences whose XOR is nonzero. Since every ordered sequence has probability (1/K^M), the winning probability is the number of winning sequences divided by (K^M).

This is correct because the complete sequence determines the exact Nim position, and Nim has a winning first move exactly when its XOR is nonzero. The problem is the number of sequences. In the worst case there are (K^M) of them, which is exponential in (M). With (K=131071) and even a tiny (M), this becomes infeasible.

A more structured brute force can maintain the number of ways to obtain each XOR value. If (dp[x]) is the number of sequences whose XOR is (x), adding another pile means

[
newdp[x]=\sum_{c\in C}dp[x\oplus c].
]

There are (2^{17}) possible XOR values, so one transition costs (O(K2^{17})). Repeating it (M) times gives (O(MK2^{17})), which still fails because (M) can be (10^9).

The key observation is that XOR is not ordinary addition, but it forms a group in which the Walsh-Hadamard transform diagonalizes convolution. The transition above is an XOR convolution with the frequency function of the available pile sizes. After applying the Walsh-Hadamard transform, every XOR-convolution becomes pointwise multiplication.

Let (f[x]) be (1) when (x) is an available size and (0) otherwise. The transform of (f), written (F), describes the contribution of every XOR frequency. Choosing (M) independent piles corresponds to taking the (M)-th XOR convolution power of (f), so after transformation each component simply becomes (F[i]^M).

The inverse Walsh-Hadamard transform then recovers the number of sequences for every resulting XOR value. We only need the value at XOR (0). For the standard unnormalized transform, the inverse contributes a factor (1/2^{17}). Since the original choices are equiprobable, we also divide by (K^M).

The whole calculation is thus reduced to one Walsh-Hadamard transform, (2^{17}) modular exponentiations, and one final normalization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(K^M M)) | (O(M)) | Too slow |
| DP over XOR states | (O(MK2^{17})) | (O(2^{17})) | Too slow |
| Walsh-Hadamard Transform | (O(2^{17}\cdot17 + 2^{17}\log M)) | (O(2^{17})) | Accepted |

## Algorithm Walkthrough

1. Create an array `a` of length (N=2^{17}). Put (1) at every allowed pile size (c_i), and (0) elsewhere. This represents the number of available choices producing each XOR value.
2. Apply the Walsh-Hadamard transform to `a`. For XOR convolution, the transform replaces convolution by pointwise multiplication. After this operation, `a[x]` is the transform value associated with frequency (x).
3. Raise every transformed value to the (M)-th power modulo (998244353). This represents choosing (M) piles, because (M)-fold XOR convolution becomes ordinary multiplication after the transform.
4. Sum all (N) powered transform values. The inverse Walsh-Hadamard transform at position zero is exactly this sum divided by (N), because every sign in the zero-frequency inverse coefficient is (+1).
5. Divide the resulting number of winning sequences by (K^M). We can perform both divisions modulo (998244353), using modular inverses. Equivalently, multiply by (N^{-1}) and ((K^M)^{-1}).
6. The resulting value is the probability that the XOR is zero. Since Alice wins when the XOR is nonzero, subtract it from (1).

Why it works: let (g_M[x]) denote the number of ordered sequences of (M) allowed pile sizes whose XOR is (x). The base function is (g_1=f), and adding a pile gives the XOR convolution (g_{m+1}=g_m*f). The Walsh-Hadamard transform converts this recurrence into (\widehat g_{m+1}[x]=\widehat g_m[x]\widehat f[x]), so induction gives (\widehat g_M[x]=\widehat f[x]^M). The inverse transform therefore recovers the exact count (g_M[0]). Dividing by the total number (K^M) gives the probability of a losing position, and taking its complement gives Alice's winning probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
N = 1 << 17

def fwht(a):
    n = len(a)
    length = 1

    while length < n:
        step = length << 1
        for start in range(0, n, step):
            end = start + length
            for i in range(start, end):
                x = a[i]
                y = a[i + length]
                a[i] = (x + y) % MOD
                a[i + length] = (x - y) % MOD
        length <<= 1

def solve():
    M, K = map(int, input().split())
    c = list(map(int, input().split()))

    a = [0] * N
    for x in c:
        a[x] = 1

    fwht(a)

    total_zero_xor = 0
    for x in a:
        total_zero_xor = (total_zero_xor + pow(x, M, MOD)) % MOD

    inv_n = pow(N, MOD - 2, MOD)
    inv_k_power = pow(pow(K, M, MOD), MOD - 2, MOD)

    zero_probability = total_zero_xor * inv_n % MOD
    zero_probability = zero_probability * inv_k_power % MOD

    answer = (1 - zero_probability) % MOD
    print(answer)

if __name__ == "__main__":
    solve()
```

The array has size (N=2^{17}), because every pile size is below (2^{17}), and XOR never sets a bit above the highest bit appearing in its operands. The array is initialized with frequency one for every allowed size.

`fwht` performs the XOR Walsh-Hadamard transform in place. At each layer, pairs of values are replaced by their sum and difference. There are (17) layers, and every layer processes all (N) entries, giving (O(N\log N)) time.

The transformed value is raised to `M` with Python's modular `pow`, which uses binary exponentiation. This is crucial because (M) can be (10^9); explicitly multiplying (M) times would be impossible.

The sum of all powered transform values is the unnormalized inverse transform at XOR zero. Dividing by (N) gives the number of zero-XOR sequences. The original array contains counts rather than probabilities, so this number must additionally be divided by (K^M), the total number of ordered pile configurations.

The modular inverse is computed with Fermat's theorem because (998244353) is prime. There is no integer overflow issue in Python, and every intermediate modular multiplication is reduced by `% MOD`.

The transform does not need to be inverted explicitly. We only need coefficient zero, and for that coefficient every inverse-transform sign is positive. Computing a full inverse transform would add unnecessary work.

## Worked Examples

### Sample 1

The input is

```
2 2
1 3
```

There are (N=8) possible XOR states, and the initial frequency array has ones at positions (1) and (3).

For these two values, the Walsh-Hadamard transform contains only the values (2) or (0), depending on whether the corresponding mask gives the same sign to both values.

| Quantity | Value |
| --- | --- |
| (M) | 2 |
| (K) | 2 |
| Number of XOR states | 8 |
| Nonzero initial positions | 1, 3 |
| Total configurations | (2^2=4) |
| Zero-XOR configurations | 2 |
| Zero-XOR probability | (2/4=1/2) |
| Alice's probability | (1/2) |

Modulo (998244353), (1/2) is (499122177), matching the sample.

The two losing configurations are `(1,1)` and `(3,3)`. The other two configurations have XOR (1\oplus3=2), so Alice wins.

### Sample 2

The input is

```
11 1
5
```

There is only one possible pile size. Consequently, every one of the eleven piles contains (5).

| Quantity | Value |
| --- | --- |
| (M) | 11 |
| (K) | 1 |
| Only pile value | 5 |
| Resulting XOR | (5) |
| Zero-XOR probability | 0 |
| Alice's probability | 1 |

Because eleven is odd,

[
5\oplus5\oplus\cdots\oplus5=5.
]

The position is winning, so the answer is (1).

This example also confirms that the algorithm handles (K=1) without any special case. In the transform, every transformed value is either (1) or (-1), and raising them to an odd power preserves the required zero-XOR count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(2^{17}\cdot17 + 2^{17}\log M)) | One FWHT plus one modular exponentiation for every transform coefficient |
| Space | (O(2^{17})) | The transform array contains (131072) modular values |

The largest transform has only (131072) entries and 17 layers, so the transform itself requires about (2.2) million pair operations. The exponentiation stage performs roughly (17) modular multiplication steps per entry for (M\le10^9). This is easily compatible with the (256) MB memory limit and is the appropriate complexity for a problem where (M) can be (10^9).

## Test Cases

```python
import sys
import io

MOD = 998244353
N = 1 << 17

def fwht(a):
    n = len(a)
    length = 1
    while length < n:
        step = length << 1
        for start in range(0, n, step):
            end = start + length
            for i in range(start, end):
                x = a[i]
                y = a[i + length]
                a[i] = (x + y) % MOD
                a[i + length] = (x - y) % MOD
        length <<= 1

def solve(data: str) -> str:
    it = iter(map(int, data.split()))
    M = next(it)
    K = next(it)

    a = [0] * N
    for _ in range(K):
        a[next(it)] = 1

    fwht(a)

    s = sum(pow(x, M, MOD) for x in a) % MOD
    zero_probability = s * pow(N, MOD - 2, MOD) % MOD
    zero_probability = zero_probability * pow(pow(K, M, MOD), MOD - 2, MOD) % MOD

    return str((1 - zero_probability) % MOD)

assert solve("""2 2
1 3
""") == "499122177", "sample 1"

assert solve("""11 1
5
""") == "1", "sample 2"

assert solve("""7 3
1 2 3
""") == "50665352", "sample 3"

assert solve("""1 1
1
""") == "1", "single pile always wins"

assert solve("""2 1
5
""") == "0", "two identical piles have zero XOR"

assert solve("""2 2
1 2
""") == "499122177", "two distinct values, equal choices lose"

assert solve("""1 2
65536 131071
""") == "1", "boundary values with one pile"

assert solve("""2 3
1 2 3
""") == str((2 * pow(3, MOD - 2, MOD)) % MOD), \
    "for two piles, exactly equal pairs have zero XOR"

expected = (1 - pow(131071, MOD - 2, MOD)) % MOD
assert solve("""2 131071
""" + " ".join(map(str, range(1, 131072))) + "\n") == str(expected), \
    "maximum K and maximum value boundary"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | Minimum (M), single available value |
| `2 1 / 5` | `0` | All piles equal and even (M) |
| `2 2 / 1 2` | `499122177` | Basic zero-XOR counting |
| `1 2 / 65536 131071` | `1` | Values at the upper boundary |
| `2 3 / 1 2 3` | (2/3) modulo MOD | Two-pile equality property |
| (M=2,K=131071) with values (1\ldots131071) | (1-1/131071) | Maximum (K) and large transform |

For two piles, the XOR is zero precisely when the two chosen sizes are equal. With (K) distinct choices, there are (K) losing ordered pairs among (K^2) total pairs, so the winning probability is (1-1/K). This gives a convenient independent check for the large test.

## Edge Cases

When (M=1), the only possible pile size is positive, so its XOR cannot be zero. For example,

```
1 1
5
```

has answer (1). In the algorithm, the transformed values are used to reconstruct the original frequency array, and the zero-XOR coefficient is zero because the input array has no value at position zero. The final complement is consequently (1).

When (K=1), all piles have the same size. For

```
2 1
5
```

the XOR is (5\oplus5=0), so the answer is (0). For odd (M), the XOR is (5), so Alice wins. The sample

```
11 1
5
```

has eleven copies of (5), giving XOR (5) and answer (1). The transform handles both parities naturally because each transformed component is raised to the corresponding power.

When pile sizes are close to the maximum allowed value, the transform still needs only (2^{17}) states. Consider

```
1 2
65536 131071
```

The single pile is either (65536) or (131071), both nonzero, so the answer is (1). The array indices are valid because the largest possible value is exactly (2^{17}-1=131071). The array therefore must have indices from (0) through (131071), requiring exactly (2^{17}) entries.

For two piles with distinct available values, the only zero-XOR outcomes are equal values. With

```
2 2
1 2
```

the four ordered outcomes are `(1,1)`, `(1,2)`, `(2,1)`, and `(2,2)`. Two have zero XOR and two have nonzero XOR, giving Alice probability (1/2). This catches an easy mistake where unordered pairs are counted instead of ordered independent choices.

Finally, the implementation must not use an array of size equal to the largest pile value. The transform represents the entire XOR group, including state zero, so its size is (2^{17}), not (131071). This distinction is essential for values such as (131071), whose index is the final valid position of the transform array.
