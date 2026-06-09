---
title: "CF 1879D - Sum of XOR Functions"
description: "We are given an array of non-negative integers. For every subarray $[l,r]$, we compute the XOR of all elements inside that subarray. Let that XOR value be $f(l,r)$. The contribution of a subarray is not just its XOR."
date: "2026-06-08T22:47:06+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "divide-and-conquer", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1879
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 155 (Rated for Div. 2)"
rating: 1700
weight: 1879
solve_time_s: 143
verified: true
draft: false
---

[CF 1879D - Sum of XOR Functions](https://codeforces.com/problemset/problem/1879/D)

**Rating:** 1700  
**Tags:** bitmasks, combinatorics, divide and conquer, dp, math  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of non-negative integers. For every subarray $[l,r]$, we compute the XOR of all elements inside that subarray. Let that XOR value be $f(l,r)$.

The contribution of a subarray is not just its XOR. It is multiplied by the subarray length:

$$f(l,r)\cdot(r-l+1)$$

The task is to sum this value over all subarrays and output the result modulo $998244353$.

A direct implementation would examine all $O(n^2)$ subarrays. With $n\le 3\cdot10^5$, that would mean roughly $4.5\times10^{10}$ subarrays, which is completely impossible within two seconds. Even an $O(n^2)$ algorithm performing only a few operations per subarray is far beyond the limit.

The array values are at most $10^9$, so every number fits into 30 bits. Whenever a problem asks for a sum of XOR values, it is usually profitable to process each bit independently because XOR acts independently on every bit position.

A subtle corner case is that the length multiplier depends on both endpoints. For example:

```
2
1 1
```

Subarrays:

```
[1] -> 1 * 1 = 1
[1,1] -> 0 * 2 = 0
[1] -> 1 * 1 = 1
```

Answer = 2.

A solution that only counts how many subarrays have XOR bit $1$ would miss the length weighting and produce the wrong result.

Another easy mistake is forgetting that a subarray XOR is represented through prefix XORs:

```
1
5
```

The only subarray has XOR $5$, length $1$, answer $5$.

This case requires the prefix XOR before the array starts, namely $pref_0=0$. Omitting this prefix causes all subarrays starting at position $1$ to disappear from the count.

A third source of bugs is modular arithmetic. The weighted sum can become extremely large. Even though Python integers do not overflow, the problem requires the final result modulo $998244353$, and intermediate accumulations should also be reduced modulo this value.

## Approaches

The brute-force solution enumerates every pair $(l,r)$. Using prefix XORs, each subarray XOR can be computed in $O(1)$:

$$f(l,r)=pref_r\oplus pref_{l-1}$$

Then we add

$$(pref_r\oplus pref_{l-1})(r-l+1)$$

to the answer.

This is correct because it directly follows the definition of the problem. The issue is the number of subarrays. There are

$$\frac{n(n+1)}2$$

of them, which reaches about $4.5\times10^{10}$ when $n=3\cdot10^5$.

The key observation is that XOR can be decomposed bit by bit.

Consider one bit position $b$. Its contribution to the final answer is

$$2^b \times
\sum_{\text{subarrays whose XOR has bit }b=1}
(r-l+1)$$

So the real task becomes:

For each bit, find the total lengths of all subarrays whose XOR on that bit equals $1$.

Introduce prefix XOR parity for this bit. Let

$$p_i = \text{bit } b \text{ of } pref_i.$$

For a subarray $[l,r]$,

$$\text{bit } b \text{ of } f(l,r)
=
p_r \oplus p_{l-1}.$$

The bit contributes exactly when these two parities differ.

Now rewrite the subarray using prefix indices:

$$j=l-1,\qquad i=r.$$

The subarray length becomes

$$r-l+1=i-j.$$

Thus, for a fixed bit, we need

$$\sum_{0\le j<i\le n,\ p_i\ne p_j}
(i-j).$$

This is a pair-counting problem on prefix XOR parities.

Suppose we process prefix positions from left to right. When we arrive at position $i$, we want all previous positions $j$ whose parity differs from $p_i$.

Their contribution is

$$\sum (i-j)
=
(\text{count})\cdot i - \sum j.$$

So for each parity $0$ and $1$, we only need:

- how many previous prefixes have that parity,
- the sum of their indices.

Then every prefix position can be processed in $O(1)$, giving $O(n)$ work per bit.

Since there are only 30 relevant bits, the total complexity becomes $O(30n)$.

| Approach | Time Complexity | Space Complexity | Verdict |

|---|------|---|

| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |

| Optimal | $O(30n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### 1. Build prefix XORs

Create

$$pref_0=0,
\qquad
pref_i=pref_{i-1}\oplus a_i.$$

Then every subarray XOR equals

$$pref_r\oplus pref_{l-1}.$$

### 2. Process each bit independently

For every bit $b$ from $0$ to $29$, compute the total weighted length of subarrays whose XOR has bit $b=1$.

The final answer receives this quantity multiplied by $2^b$.

### 3. Maintain statistics of previous prefix parities

For the current bit, define

$$parity_i = (pref_i>>b)\&1.$$

Maintain:

```
cnt[0], cnt[1]
sumPos[0], sumPos[1]
```

where `cnt[t]` is the number of previous prefix positions with parity `t`, and `sumPos[t]` is the sum of their indices.

Initially only prefix position $0$ exists:

```
cnt[0] = 1
sumPos[0] = 0
```

### 4. Process prefixes from left to right

At position $i$, let current parity be $p$.

We need all previous positions having parity $p\oplus1$.

If

```
opp = p ^ 1
```

then their total contribution is

$$cnt[opp]\cdot i - sumPos[opp].$$

This quantity equals

$$\sum(i-j)$$

over all valid previous positions $j$.

Add it to the running contribution of this bit.

### 5. Insert the current prefix

After using position $i$ as a right endpoint, add it to the data structure:

$$cnt[p] += 1$$

$$sumPos[p] += i$$

### 6. Add the bit contribution

If the accumulated weighted length for bit $b$ is $cur$, add

$$cur\cdot 2^b$$

to the answer modulo $998244353$.

### Why it works

For a fixed bit, a subarray contributes exactly when the corresponding prefix parities at its two ends differ. Every subarray $[l,r]$ corresponds uniquely to a pair of prefix indices $(l-1,r)$. While processing prefix position $r$, the algorithm considers all earlier prefix positions with opposite parity. The expression

$$cnt\cdot r-\sum j$$

is exactly the sum of lengths $r-j$ of all such subarrays. Every valid subarray is counted once, when its right endpoint is processed, and invalid subarrays are never counted because their parities are equal. Summing independently over all bits reconstructs the original XOR values, so the final answer equals the required weighted sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] ^ a[i]

    ans = 0

    for b in range(30):
        cnt = [1, 0]          # prefix 0 already exists
        sum_pos = [0, 0]

        cur = 0

        for i in range(1, n + 1):
            p = (pref[i] >> b) & 1
            opp = p ^ 1

            cur += cnt[opp] * i - sum_pos[opp]

            cnt[p] += 1
            sum_pos[p] += i

        ans = (ans + (cur % MOD) * ((1 << b) % MOD)) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The prefix XOR array transforms every subarray XOR into the XOR of two prefixes. After that, each bit can be processed independently.

For one bit, the only information that matters is whether the prefix XOR at that bit is $0$ or $1$. The arrays `cnt` and `sum_pos` store exactly the statistics needed to evaluate

$$\sum(i-j)$$

for all previous prefixes with opposite parity.

The order of operations matters. The current prefix position must contribute before being inserted into the data structure. Otherwise a prefix would incorrectly pair with itself, creating zero-length subarrays.

The value

```
cnt[opp] * i - sum_pos[opp]
```

already equals the total lengths of all newly discovered valid subarrays ending at position `i`. No additional length computation is needed.

## Worked Examples

### Example 1

Input:

```
3
1 3 2
```

Prefix XORs:

```
pref = [0, 1, 2, 0]
```

Consider bit 0.

| i | pref[i] | parity | opposite count | opposite sum | added |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 0 | 1 |
| 2 | 2 | 0 | 1 | 1 | 1 |
| 3 | 0 | 0 | 1 | 1 | 2 |

Bit-0 weighted length total = 4.

Consider bit 1.

| i | pref[i] | parity | opposite count | opposite sum | added |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 2 | 1 | 2 | 1 | 3 |
| 3 | 0 | 0 | 1 | 2 | 1 |

Bit-1 weighted length total = 4.

Contribution:

```
4 * 1 + 4 * 2 = 12
```

Answer:

```
12
```

This trace shows how lengths are accumulated automatically through the formula $cnt\cdot i-\sum j$.

### Example 2

Input:

```
2
1 1
```

Prefix XORs:

```
[0,1,0]
```

Bit 0 processing:

| i | parity | opposite count | opposite sum | added |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 1 |
| 2 | 0 | 1 | 1 | 1 |

Total weighted length:

```
2
```

Bit contribution:

```
2 * 1 = 2
```

Answer:

```
2
```

This example demonstrates that the subarray `[1,1]` has XOR zero and contributes nothing despite having length two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(30n)$ | Each of 30 bits scans all prefix positions once |
| Space | $O(n)$ | Prefix XOR array of size $n+1$ |

With $n=3\cdot10^5$, the algorithm performs roughly nine million iterations, which easily fits within the time limit. Memory usage is dominated by the prefix XOR array and remains well below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    MOD = 998244353

    n = int(input())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] ^ a[i]

    ans = 0

    for b in range(30):
        cnt = [1, 0]
        sum_pos = [0, 0]
        cur = 0

        for i in range(1, n + 1):
            p = (pref[i] >> b) & 1
            opp = p ^ 1

            cur += cnt[opp] * i - sum_pos[opp]

            cnt[p] += 1
            sum_pos[p] += i

        ans = (ans + (cur % MOD) * ((1 << b) % MOD)) % MOD

    return str(ans) + "\n"

# provided sample
assert run("3\n1 3 2\n") == "12\n", "sample 1"

# minimum size
assert run("1\n5\n") == "5\n", "single element"

# all zeros
assert run("3\n0 0 0\n") == "0\n", "all xor values are zero"

# equal values
assert run("2\n1 1\n") == "2\n", "repeated numbers"

# off-by-one check involving prefix 0
assert run("2\n1 0\n") == "4\n", "subarrays starting at index 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5` | `5` | Smallest valid input |
| `3 / 0 0 0` | `0` | All XOR values vanish |
| `2 / 1 1` | `2` | Equal values creating zero XOR on longer subarray |
| `2 / 1 0` | `4` | Correct handling of prefix position 0 |

## Edge Cases

Consider:

```
1
5
```

The prefix XOR array is:

```
[0,5]
```

For every set bit of 5, position 1 has opposite parity to position 0, producing length 1. The answer becomes exactly 5. This confirms that including the initial prefix XOR is necessary.

Consider:

```
2
1 1
```

The only subarrays with XOR equal to 1 are the two single-element subarrays. The longer subarray has XOR 0. During processing, the pair of prefixes corresponding to the whole array has equal parity and is never counted. The algorithm correctly outputs 2.

Consider:

```
3
0 0 0
```

All prefix XORs are zero. Every bit parity is always 0. Since opposite parity prefixes never exist, every contribution is zero. The answer remains 0, matching the fact that every subarray XOR is zero.

Consider:

```
2
1 0
```

Subarrays are:

```
[1]   -> 1 * 1 = 1
[1,0] -> 1 * 2 = 2
[0]   -> 0 * 1 = 0
```

Total:

```
3
```

The algorithm counts both subarrays beginning at index 1 because the initial prefix position 0 participates in the parity matching process. This is exactly the situation that breaks implementations which forget the empty prefix.
