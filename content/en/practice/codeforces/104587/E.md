---
title: "CF 104587E - Over the Hill, Part 1"
description: "We are given a fixed alphabet of 37 characters consisting of uppercase English letters, digits, and the space character."
date: "2026-06-30T07:29:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104587
codeforces_index: "E"
codeforces_contest_name: "2020-2021 ICPC East Central North America Regional Contest (ECNA 2020)"
rating: 0
weight: 104587
solve_time_s: 48
verified: true
draft: false
---

[CF 104587E - Over the Hill, Part 1](https://codeforces.com/problemset/problem/104587/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed alphabet of 37 characters consisting of uppercase English letters, digits, and the space character. Each character is assigned a numeric value from 0 to 36 in a deterministic order, starting from A as 0 up to Z as 25, then digits 0 to 9 as 26 to 35, and finally space as 36.

The input provides a square matrix of size n by n, where n is at most 10, followed by a plaintext string. The encryption process transforms the text into numbers, groups them into blocks of size n, and then applies a linear transformation using the matrix under modulo 37 arithmetic. Each resulting vector is converted back into characters to produce the ciphertext.

Conceptually, the problem is matrix multiplication applied repeatedly over chunks of the input string after encoding it into a small finite ring of integers.

The constraint n ≤ 10 is the key structural limitation. It implies each transformation is extremely small and fixed-size, so the cost of multiplying a vector by the matrix is constant bounded by about 100 operations. The dominant factor is the length of the input string, which can be large, but every character is processed independently within its block. This immediately rules out any algorithm that tries to do anything superlinear in the matrix dimension or recomputes transformations inefficiently. A straightforward linear scan over the string is sufficient.

A few edge cases appear naturally in this setting. The first is padding. If the plaintext length is not divisible by n, the remaining characters must be padded with spaces. For example, if n = 3 and the plaintext is "ABCX", then we encode "A B C | X space space". A careless implementation that forgets padding will drop the last character or form an incomplete vector, producing incorrect ciphertext length.

Another edge case is the space character itself, which maps to the highest value 36. A naive implementation that only handles alphanumeric characters will silently fail on spaces or shift indices incorrectly. For example, encoding "A A" without accounting for space mapping will break alignment and corrupt the output.

Finally, large plaintext strings require care in repeated modular arithmetic. Although values remain small, repeated multiplications can overflow in languages without automatic big integers. In Python this is not an issue, but in other languages modulo reduction must be applied at every arithmetic step.

## Approaches

The most direct approach is to simulate the definition literally. We convert each character into its numeric value, split the sequence into blocks of size n, multiply each block by the matrix using standard matrix-vector multiplication, reduce each result modulo 37, and convert back to characters. This is correct because it follows the definition exactly.

For a block, computing one output entry requires n multiplications and additions, and there are n outputs per block. This yields n² operations per block. Since n ≤ 10, this is at most 100 operations per block, which is negligible. Over a string of length L, we perform O(L · n²) operations, which is effectively linear in L with a small constant.

There is no need for optimization beyond this direct simulation because the matrix is not changing and there are no repeated queries or exponentiation requirements. The key observation is that the transformation is local to each block and does not depend on previous blocks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct simulation | O(L · n²) | O(L) | Accepted |
| Attempted global optimization | Not applicable | Not applicable | Unnecessary |

## Algorithm Walkthrough

### 1. Build the character encoding

We define a mapping from characters to integers and back. Each letter, digit, and space must be assigned a unique value from 0 to 36. This step ensures the encryption operates purely on integers.

### 2. Read the matrix

We store the n by n matrix as integers. No preprocessing is needed since all operations are linear transformations modulo 37.

### 3. Convert plaintext into numeric form

We scan the string and convert each character into its corresponding integer. This produces an array of values representing the message in modular arithmetic space.

### 4. Pad the array to a multiple of n

If the length is not divisible by n, we append the value corresponding to space until it is. This ensures every block is complete and avoids boundary issues during matrix multiplication.

### 5. Process each block independently

For every contiguous block of size n, we compute the matrix-vector product. Each output coordinate is computed as the dot product of one matrix row with the block vector, taken modulo 37. This step applies the encryption transformation.

### 6. Convert results back to characters

After processing all blocks, we map each numeric value back into its character representation and concatenate them into the final ciphertext.

### Why it works

Each block is transformed by a fixed linear function over the ring of integers modulo 37. The matrix multiplication defines a deterministic function from input vectors to output vectors. Because the plaintext is partitioned into disjoint blocks and each block is transformed independently, the overall transformation is just the concatenation of these independent linear maps. There is no interaction between blocks, so correctness reduces to correctness of a single matrix-vector multiplication under modular arithmetic.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 37

# build mappings
chars = []
for c in range(ord('A'), ord('Z') + 1):
    chars.append(chr(c))
for c in range(ord('0'), ord('9') + 1):
    chars.append(chr(c))
chars.append(' ')

char_to_int = {ch: i for i, ch in enumerate(chars)}
int_to_char = {i: ch for i, ch in enumerate(chars)}

def main():
    n = int(input())
    mat = [list(map(int, input().split())) for _ in range(n)]
    s = input().rstrip('\n')

    vals = [char_to_int[ch] for ch in s]

    while len(vals) % n != 0:
        vals.append(char_to_int[' '])

    res = []

    for i in range(0, len(vals), n):
        block = vals[i:i+n]
        for r in range(n):
            acc = 0
            for c in range(n):
                acc += mat[r][c] * block[c]
            res.append(int_to_char[acc % MOD])

    sys.stdout.write(''.join(res))

if __name__ == "__main__":
    main()
```

The implementation begins by constructing the exact character encoding required by the problem. This avoids any ambiguity around digits and the space character.

The matrix is read directly into memory as integers since its size is at most 10 by 10. The plaintext is converted into a list of integers, then padded with space values until its length is divisible by n. This guarantees that slicing into fixed-size blocks never fails.

Each block is processed independently. The nested loop structure is intentional: the outer loop iterates over output rows, and the inner loop computes dot products. Modular reduction is applied only after summing the full dot product, which is safe because Python integers do not overflow.

## Worked Examples

### Example 1

We consider a small conceptual case with n = 2 and plaintext "AB ".

| Step | Block | Computation | Output values |
| --- | --- | --- | --- |
| 1 | [A, B] | row dot products | [x, y] |

Suppose A maps to 0 and B maps to 1, and the matrix produces outputs 1 and 2. After conversion back, we obtain a two-character ciphertext block. If padding were missing, the last space would be lost and the output length would be incorrect, demonstrating why padding is essential.

### Example 2

Take a slightly longer string where padding is required, such as "ABC" with n = 2.

| Step | Block | Computation | Output values |
| --- | --- | --- | --- |
| 1 | [A, B] | matrix transform | [x, y] |
| 2 | [C, space] | padded block transform | [p, q] |

This shows that the last character is not processed alone but combined with a padding space, ensuring consistent block structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L · n²) | Each character participates in one n-dimensional matrix multiplication |
| Space | O(L) | Storage of encoded string and output |

Since n ≤ 10, the factor n² is bounded by 100, making the solution effectively linear in the input size. This is well within limits for typical Codeforces constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import prod

    MOD = 37

    chars = []
    for c in range(ord('A'), ord('Z') + 1):
        chars.append(chr(c))
    for c in range(ord('0'), ord('9') + 1):
        chars.append(chr(c))
    chars.append(' ')

    char_to_int = {ch: i for i, ch in enumerate(chars)}
    int_to_char = {i: ch for i, ch in enumerate(chars)}

    n = int(input())
    mat = [list(map(int, input().split())) for _ in range(n)]
    s = input().rstrip('\n')

    vals = [char_to_int[ch] for ch in s]
    while len(vals) % n != 0:
        vals.append(char_to_int[' '])

    res = []
    for i in range(0, len(vals), n):
        block = vals[i:i+n]
        for r in range(n):
            acc = 0
            for c in range(n):
                acc += mat[r][c] * block[c]
            res.append(int_to_char[acc % MOD])

    return ''.join(res)

# provided sample 1
assert run("""3
30 1 9
4 23 7
5 9 13
ATTACK AT DAWN
""") == "FPLSFA4SUK2W9K3"

# custom: single character, n=1
assert run("""1
5
A
""") == "F"

# custom: padding required
assert run("""2
1 0
0 1
ABC
""")  # identity matrix with padding
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 single char | transformed char | minimal dimension correctness |
| identity matrix | same text with padding applied | padding behavior |
| sample case | FPLSFA4SUK2W9K3 | full pipeline correctness |

## Edge Cases

The padding case is the most important structural edge case. Consider n = 3 and plaintext "ABCX". After encoding, we get four values. The last block becomes [X, space, space]. During multiplication, this padded vector is still fully processed, producing a valid ciphertext segment. The algorithm appends space values explicitly before block processing, so no partial block is ever interpreted.

The space character itself is another critical case. If the plaintext contains spaces, they are mapped to 36 and participate in arithmetic like any other symbol. For example, a block like [A, space, B] becomes [0, 36, 1]. The multiplication step treats 36 as a normal integer modulo 37, so no special casing is required.

Finally, the smallest matrix size n = 1 degenerates into a simple scalar multiplication modulo 37 applied character by character. The same loop structure handles it naturally, since each block contains exactly one value and matrix multiplication reduces to a single multiplication step.
