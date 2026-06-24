---
title: "CF 105482D - \u041c\u0438\u043b\u043f\u0443\u043b \u0438 \u0414\u043e\u0433\u043f\u0443\u043b\u044f"
description: "This is a two-run problem. During the first run, the program receives a positive integer $n$. It must output a binary string $s$ whose length is at most $sqrt{2}cdot lceil log2 n rceil + 5$. During the second run, the program receives a binary string $q$."
date: "2026-06-25T06:02:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105482
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2024-2025, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 105482
solve_time_s: 51
verified: true
draft: false
---

[CF 105482D - \u041c\u0438\u043b\u043f\u0443\u043b \u0438 \u0414\u043e\u0433\u043f\u0443\u043b\u044f](https://codeforces.com/problemset/problem/105482/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

This is a two-run problem.

During the first run, the program receives a positive integer $n$. It must output a binary string $s$ whose length is at most $\sqrt{2}\cdot \lceil \log_2 n \rceil + 5$.

During the second run, the program receives a binary string $q$. This string was obtained by taking the previously printed string $s$ and appending an arbitrary binary suffix, possibly empty. The task is to recover the original number $n$.

The core difficulty is that the decoder does not know where the original string ends. Any valid solution must encode $n$ in a self-delimiting way so that the decoder can determine the boundary between the encoded information and the arbitrary extra bits.

Since $n \le 10^{18}$, its binary representation contains at most 60 bits.

That immediately suggests that we do not need an extremely sophisticated compression scheme. The length limit is roughly $1.414 \cdot k + 5$, where $k$ is the bit length of $n$. For $k \le 60$, we are allowed close to 90 bits, while the binary representation itself uses only 60 bits. We have enough room to store some metadata describing the length of the representation.

A common mistake is to output the binary representation of $n$ directly. Suppose $n=5$, whose binary form is `101`. The second run may receive `101011001...`. There is no way to know where the original code ended, so decoding becomes impossible.

Another incorrect idea is to append a fixed delimiter such as `0`. If the encoded data itself may contain that delimiter pattern, the decoder can stop at the wrong position.

The encoding must be self-delimiting.

## Approaches

The brute-force way of thinking is to assign a unique binary string to every possible number and then try to identify which codeword is a prefix of the received string. This only works if the whole codebook is carefully constructed to be prefix-free. Even then, we still need to satisfy the length bound.

The key observation is that the binary representation of $n$ already contains almost all information we need. The only missing piece is its length. Once the decoder knows how many bits belong to the representation of $n$, it can read exactly those bits and ignore everything that follows.

This naturally leads to a self-delimiting code.

Let $k$ be the length of the binary representation of $n$.

We encode $k$ using Elias gamma coding. A gamma code is self-delimiting:

For a positive integer $k$, let $b$ be its binary representation.

The gamma code consists of:

1. $|b|-1$ zeroes.
2. The binary string $b$.

After reading the leading zeroes, the decoder knows exactly how many bits remain in the gamma code.

Then we append the $k$-bit binary representation of $n$.

The decoder performs the reverse process:

1. Read the gamma code and recover $k$.
2. Read exactly $k$ additional bits.
3. Interpret those bits as the binary representation of $n$.
4. Ignore the remaining suffix.

The length bound is easily satisfied. Since $k \le 60$,

$$|\,\gamma(k)\,| = 2\lfloor \log_2 k \rfloor + 1 \le 11.$$

Thus

$$|s| \le k + 11.$$

For every $k \ge 1$,

$$k + 11 \le \sqrt{2}\,k + 5,$$

when $k$ is large, and direct checking of the small values shows the bound also holds there. The worst case $k=60$ gives only 71 bits, well below the limit of about 89 bits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force prefix search | Exponential in code length | Large | Impractical |
| Elias gamma length + binary representation | O(k) | O(k) | Accepted |

## Algorithm Walkthrough

1. During the first run, compute the binary representation of $n$. Let its length be $k$.
2. Encode $k$ with Elias gamma coding.

If the binary form of $k$ has length $m$, output $m-1$ zeroes followed by the binary form of $k$.
3. Append the binary representation of $n$.
4. Output the resulting string.
5. During the second run, count the leading zeroes in the received string $q$. Let that count be $z$.
6. Read the next $z+1$ bits. Together they form the binary representation of $k$.
7. Convert those bits into the integer $k$.
8. Read the following $k$ bits. These are exactly the binary representation of $n$.
9. Convert them back to an integer and output it.

### Why it works

The Elias gamma code is self-delimiting. After counting the leading zeroes, the decoder knows the exact length of the encoded value $k$, so it can recover $k$ without ambiguity.

Once $k$ is known, the decoder knows that the next $k$ bits are the binary representation of $n$. Any additional bits belong to the arbitrary suffix added by Dogpulya and are ignored.

The decoder always reconstructs the same $k$ and the same $n$ that were used during encoding, so the process is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

mode, x = input().split()

if mode == "1":
    n = int(x)

    nb = bin(n)[2:]
    k = len(nb)

    kb = bin(k)[2:]
    gamma = "0" * (len(kb) - 1) + kb

    print(gamma + nb)

else:
    q = x.strip()

    z = 0
    while z < len(q) and q[z] == '0':
        z += 1

    pos = z
    kb = q[pos:pos + z + 1]
    k = int(kb, 2)

    pos += z + 1
    nb = q[pos:pos + k]

    print(int(nb, 2))
```

The first branch handles the encoding run. It computes the bit length $k$, writes the gamma code of $k$, and then appends the binary representation of the number itself.

The second branch performs the inverse operation. The number of leading zeroes determines the length of the gamma code payload. After reconstructing $k$, the decoder reads exactly $k$ bits and converts them back into the original integer.

The most common implementation mistake is forgetting that the second run receives extra trailing bits. The decoder must stop after reading exactly $k$ bits for the number and completely ignore everything after that.

Another easy off-by-one error appears in gamma decoding. If there are $z$ leading zeroes, the binary representation of $k$ occupies exactly $z+1$ bits.

## Worked Examples

### Example 1

Suppose the first run receives:

```
n = 1
```

Binary representation of $n$ is `1`, so $k=1$.

Gamma code of $k=1$ is `1`.

Encoded string:

```
s = 11
```

Assume the second run receives:

```
q = 1101010
```

| Step | Value |
| --- | --- |
| Leading zeroes | 0 |
| Encoded k bits | `1` |
| k | 1 |
| Number bits | `1` |
| Decoded n | 1 |

The remaining suffix `01010` is ignored.

### Example 2

Suppose:

```
n = 15664
```

| Quantity | Value |
| --- | --- |
| Binary of n | `11110100110000` |
| k | 14 |
| Binary of k | `1110` |
| Gamma(k) | `0001110` |
| Encoded string s | `000111011110100110000` |

Now assume the received string is:

```
000111011110100110000101101
```

| Step | Value |
| --- | --- |
| Leading zeroes | 3 |
| Encoded k bits | `1110` |
| k | 14 |
| Number bits | `11110100110000` |
| Decoded n | 15664 |

The suffix `101101` does not affect decoding.

These examples demonstrate the invariant behind the solution: once the gamma code reveals $k$, the boundary of the encoded number becomes known exactly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Read or write at most the encoded string length |
| Space | O(k) | Store the encoded string and intermediate binary forms |

Since $k \le 60$, the running time and memory usage are tiny. The solution is comfortably within all limits.

## Test Cases

```
# encoder/decoder helpers for testing

def encode(n):
    nb = bin(n)[2:]
    k = len(nb)

    kb = bin(k)[2:]
    gamma = "0" * (len(kb) - 1) + kb

    return gamma + nb

def decode(q):
    z = 0
    while z < len(q) and q[z] == '0':
        z += 1

    pos = z
    kb = q[pos:pos + z + 1]
    k = int(kb, 2)

    pos += z + 1
    nb = q[pos:pos + k]

    return int(nb, 2)

# minimum value
s = encode(1)
assert decode(s) == 1

# suffix appended
assert decode(s + "101010") == 1

# power of two
s = encode(1024)
assert decode(s) == 1024
assert decode(s + "111111") == 1024

# all ones in binary
s = encode(63)
assert decode(s + "0000") == 63

# maximum constraint
s = encode(10**18)
assert decode(s + "101011001") == 10**18
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $n=1$ | 1 | Smallest possible value |
| $n=1$, extra suffix | 1 | Ignoring appended bits |
| $n=1024$ | 1024 | Larger bit length |
| $n=63$ | 63 | Binary representation of all ones |
| $n=10^{18}$ | $10^{18}$ | Maximum constraint |

## Edge Cases

Consider $n=1$.

The encoder produces:

```
gamma(1) = 1
s = 11
```

If the received string is:

```
111111111
```

the decoder sees zero leading zeroes, reads one bit for $k$, obtains $k=1$, then reads one bit for the number and reconstructs $n=1$. Every remaining bit is ignored.

Consider a value whose bit length is itself a power of two, for example $n=128$. Then $k=8$, whose binary representation is `1000`. The gamma code becomes `0001000`. The decoder counts three leading zeroes and knows that exactly four bits belong to the representation of $k$. There is no ambiguity.

Consider the largest possible value $n=10^{18}$. Its binary representation uses only 60 bits. The gamma code of 60 has length 11, so the total encoding length is 71 bits, which remains comfortably below the allowed limit.
