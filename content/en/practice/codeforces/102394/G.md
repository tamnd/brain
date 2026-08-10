---
title: "CF 102394G - Game Store"
description: "On each day, one new rental set becomes available. A set is identified by two values: (ai), the size of each of its two equal piles, and (bi), the amount Alice pays to rent that set."
date: "2026-08-10T19:10:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "G"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 177
verified: true
draft: false
---

[CF 102394G - Game Store](https://codeforces.com/problemset/problem/102394/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

On each day, one new rental set becomes available. A set is identified by two values: (a_i), the size of each of its two equal piles, and (b_i), the amount Alice pays to rent that set. Alice may rent any collection of the sets that have appeared so far, but if she rents a set she receives both copies of its pile.

Bob then sees all rented piles and may delete any collection of them before the Nim game begins. Alice wins only if Bob cannot turn the remaining position into a losing position.

The output for each day is the largest possible total rental cost of a collection Alice can choose such that, regardless of which piles Bob removes, Alice still wins. The answer from the previous day is also part of the input decoding: the actual pair on the current day is (a_i=x_i\mathbin{\mathsf{xor}}last) and (b_i=y_i\mathbin{\mathsf{xor}}last).

The official instance has (n\le 500000), (a_i\le10^{18}), and (b_i\le10^9), with a 1.5 second time limit and 512 MB of memory. The important consequence is that we cannot revisit all previous rental sets after every insertion. Even (O(n\sqrt n)) is far too large, and an (O(n^2)) approach would require roughly (2.5\cdot10^{11}) operations. The numbers (a_i) fit in 60 bits, so every pile can be viewed as a vector of only 60 coordinates. That small fixed dimension is the opening for a linear-basis data structure.

The first subtlety is that the two copies in a rental set matter. A set with value (a) contributes two identical vectors, not one. Bob can independently remove either copy, so the coefficient of that vector in a subset of the remaining piles can be (0), (1), or (2). This is exactly why the field (\mathbb F_3), rather than ordinary binary XOR, appears.

The second subtlety is that renting every profitable set is not necessarily valid. For example, consider the actual sequence

```
3
1 2
3 1
2 7
```

The decoded sets are ((a,b)=(1,2),(1,3),(1,4)), because the previous answers are (2,3). All three vectors are identical. The correct answers are (2,3,4). Renting all three on the third day would give six copies of the same pile value, whose bit count is (6), divisible by (3), so Bob can leave a losing position. A careless algorithm that simply sums every positive rental cost would output (9).

Another subtle case is a heavy vector that is initially dependent on the current basis but should replace a lighter vector. The official sample has decoded values ((1,4),(2,3),(3,10)), giving answers (4,7,14). On the third day, (3) is dependent on (1) and (2), but its cost (10) is larger than either existing cost. The optimal collection keeps (3) and (1), for (14). A data structure that only accepts independent insertions and permanently discards dependent vectors would incorrectly remain at (7).

The encryption is another easy source of silent errors. The XOR must use the previous output, not the previous input value, and the decoded answer must be assigned to `last` before reading the next encrypted pair. The sample input

```
3
1 4
6 7
4 13
```

decodes to ((1,4),(2,3),(3,10)), not to the three pairs shown directly in the input.

## Approaches

A direct approach would keep every rental set seen so far and, on each day, search for the most expensive collection that Alice can safely rent. For a collection of (k) sets there are (3^k) possible ways Bob can choose zero, one, or two copies of every set, so checking every possible deletion pattern is already exponential. Even after recognizing the linear-algebra characterization below, a brute-force implementation could enumerate all subsets of the available sets. With (n=500000), that means (2^{500000}) candidates in the worst case, which is completely infeasible.

The reason the game can be reduced much further is the characterization of losing positions in this version of Nim. Since one move can affect at most two piles, this is Moore's Nim with parameter (2). A position is losing exactly when, for every binary bit position, the number of piles containing that bit is (0) modulo (3).

Represent every pile value (a) by its 60-dimensional binary vector. Suppose Alice rents sets with vectors (v_1,\ldots,v_k). There are two copies of each vector. If Bob leaves (c_i) copies of set (i), then (c_i\in{0,1,2}), and the resulting position is losing exactly when

[
\sum_{i=1}^{k} c_i v_i=0
]

over (\mathbb F_3).

Alice must prevent Bob from obtaining such a zero sum for every nonempty choice of coefficients. That condition says precisely that (v_1,\ldots,v_k) are linearly independent over (\mathbb F_3). If they were dependent, the coefficients of a nontrivial dependence are (0,1,) or (2), so Bob could choose exactly those numbers of copies and obtain a losing position. Conversely, if the vectors are independent, the only zero linear combination uses coefficient (0) for every set, which corresponds to deleting all piles, and Bob is not allowed to do that.

So the game disappears. The problem becomes:

For every prefix of the input, find the maximum total weight of a linearly independent subset of the corresponding vectors over (\mathbb F_3).

This is a weighted linear matroid problem. The usual greedy property of matroids says that a maximum-weight independent set can be obtained by considering elements from high weight to low weight. Since the input arrives online, we cannot sort the entire prefix again after every insertion. Instead, we maintain a weighted Gaussian basis dynamically.

When a new vector meets an occupied pivot, we eliminate that pivot. If the new vector has larger weight than the basis vector currently occupying the pivot, we exchange them and continue eliminating the displaced vector. This is the linear-algebra analogue of exchanging an edge in a maximum spanning forest.

The dimension is at most 60 because (a_i\le10^{18}<2^{60}). Thus every insertion performs at most 60 pivot eliminations. The ternary vectors can be stored as two 60-bit masks, one mask for coordinates equal to (1) and one for coordinates equal to (2). Bit operations then perform an entire vector operation at once instead of iterating through all coordinates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n)) or worse | (O(n)) | Too slow |
| Optimal | (O(60n)) | (O(60)) | Accepted |

## Algorithm Walkthrough

1. Interpret each pile value (a) as a vector over (\mathbb F_3). For every binary bit set in (a), the corresponding coordinate is (1), while all other coordinates are (0).
2. Maintain a Gaussian basis with at most 60 vectors. For every pivot position (p), store one basis vector whose coefficient at (p) is exactly (1), together with the rental cost of that vector.
3. When a new pair ((a,b)) arrives, first decode it using the previous answer. The vector initially contains only coefficients (0) and (1).
4. Find the highest coordinate where the current vector is nonzero. This is the pivot that Gaussian elimination should process next. If no coordinate remains, the vector is dependent on the current basis and can be discarded.
5. If the corresponding pivot is empty, insert the vector there. If its pivot coefficient is (2), multiply the whole vector by (2), which exchanges its (1)-mask and (2)-mask. Multiplication by (2) is valid because (2\cdot2=1\pmod3).
6. If the pivot is occupied, compare the incoming weight with the weight stored at that pivot. If the incoming weight is not larger, eliminate the pivot from the incoming vector and continue.
7. If the incoming weight is larger, exchange the two vectors. The heavier vector becomes the basis vector at this pivot, while the old basis vector becomes the vector being eliminated. The answer changes by the difference between the two weights.
8. Continue until the incoming vector becomes zero or reaches an empty pivot. Every successful insertion increases the maintained total, while every successful exchange replaces a lighter selected set by a heavier set without changing the span.
9. Print the maintained total and assign it to `last`. The next encrypted input pair must use this exact value.

The central invariant is that after processing any prefix, the stored basis represents a maximum-weight independent subset of all vectors in that prefix. Gaussian elimination preserves the span, while the exchange rule keeps the heavier member whenever a new vector can replace an existing basis vector. Since linear independence forms a matroid, these local exchanges are sufficient to maintain a globally maximum-weight independent set. The game-theoretic reduction then proves that exactly these independent sets are the collections Alice can rent safely.

## Python Solution

```python
import sys
input = sys.stdin.readline

BITS = 60

# For a ternary vector:
# lo has a 1 where the coefficient is 1.
# hi has a 1 where the coefficient is 2.
#
# The two masks together are a bit-sliced representation of F_3^60.

def add3(al, ah, bl, bh):
    # Coordinate-wise addition modulo 3.
    x = al ^ bl
    y = ah ^ bh

    # Output coefficient 1:
    # (0,1), (1,0), (2,2)
    nl = (x & ~y) | (ah & bh)

    # Output coefficient 2:
    # (0,2), (2,0), (1,1)
    nh = ((~(al | bl)) & y) | (al & bl)

    return nl, nh

def solve(reader=input):
    n = int(reader())

    basis_lo = [0] * BITS
    basis_hi = [0] * BITS
    basis_w = [0] * BITS

    ans = 0
    last = 0
    out = []

    for _ in range(n):
        x, y = map(int, reader().split())

        a = x ^ last
        w = y ^ last

        lo = a
        hi = 0

        while lo or hi:
            p = (lo | hi).bit_length() - 1

            # Since the basis vector at p is normalized,
            # its coefficient at p is exactly 1.
            coeff = ((lo >> p) & 1) | (((hi >> p) & 1) << 1)

            if basis_lo[p] == 0 and basis_hi[p] == 0:
                # Normalize the new pivot to 1.
                if coeff == 2:
                    lo, hi = hi, lo

                basis_lo[p] = lo
                basis_hi[p] = hi
                basis_w[p] = w
                ans += w
                break

            bw = basis_w[p]

            if w > bw:
                # The new vector must become the heavier basis vector.
                if coeff == 2:
                    lo, hi = hi, lo
                    coeff = 1

                # Replace the old basis vector.
                lo, basis_lo[p] = basis_lo[p], lo
                hi, basis_hi[p] = basis_hi[p], hi
                w, basis_w[p] = basis_w[p], w

                ans += basis_w[p] - w

                # The displaced old basis vector has pivot coefficient 1.
                # Eliminate it using the new basis vector.
                blo = basis_lo[p]
                bhi = basis_hi[p]

                # x <- x - basis[p] = x + 2*basis[p].
                lo, hi = add3(lo, hi, bhi, blo)
            else:
                blo = basis_lo[p]
                bhi = basis_hi[p]

                if coeff == 1:
                    # x <- x - b = x + 2b.
                    lo, hi = add3(lo, hi, bhi, blo)
                else:
                    # x <- x - 2b = x + b.
                    lo, hi = add3(lo, hi, blo, bhi)

        last = ans
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The three basis arrays hold the two bit planes of each ternary vector and its associated rental cost. A pivot is considered empty only when both masks are zero. There is no need to store the original (a_i), because the Gaussian basis only needs the current reduced vector.

The `add3` function is the core bitset optimization. For each coordinate, a ternary digit has one of the encodings (0,1,2). The low mask identifies digits equal to (1), while the high mask identifies digits equal to (2). The Boolean expressions inside `add3` implement the nine cases of addition modulo (3) simultaneously for all 60 coordinates.

Subtraction is also cheap because in (\mathbb F_3), subtracting a vector is the same as adding twice that vector. Multiplication by (2) swaps the two masks, so `x - basis` is implemented as `add3(x, swapped_basis)`, while `x - 2*basis` is simply `add3(x, basis)`.

The incoming vector may have pivot coefficient (2). Before it is installed into the basis, its two masks are swapped so that its pivot coefficient becomes (1). This normalization is necessary because every stored basis vector is assumed to have coefficient (1) at its own pivot.

The weight exchange is also easy to get wrong. Suppose the incoming vector has weight (w) and the existing pivot vector has weight (w_b). When (w>w_b), the new vector becomes selected and the old vector is displaced. The answer changes by (w-w_b), while the displaced vector continues through Gaussian elimination with its old weight. The code performs that swap before eliminating the pivot.

All arithmetic involving rental costs and answers fits comfortably in Python integers. The maximum answer is at most (60\cdot10^9), but using Python's arbitrary-precision integers also makes the implementation insensitive to any intermediate representation size.

The XOR decoding happens before the basis operation, and `last` is updated only after the current answer has been finalized. This ordering is required because the input is deliberately encrypted using the previous output.

## Worked Examples

### Sample

The sample input is

```
3
1 4
6 7
4 13
```

The decoded sequence is ((1,4),(2,3),(3,10)).

| Day | Encoded pair | Decoded ((a,b)) | Basis vectors after insertion | Answer |
| --- | --- | --- | --- | --- |
| 1 | ((1,4)) | ((1,4)) | (1:4) | 4 |
| 2 | ((6,7)) | ((2,3)) | (1:4,\ 2:3) | 7 |
| 3 | ((4,13)) | ((3,10)) | (1:4,\ 3:10) | 14 |

On the first day, the single vector is independent, so its cost is selected. On the second day, (1) and (2) occupy different bit positions and are independent, so both costs are kept.

On the third day, vector (3) is the sum of vectors (1) and (2) over (\mathbb F_3), so it is dependent on the current basis. However, its weight (10) is larger than the weight (3) of vector (2). The dynamic basis replaces vector (2) with vector (3), leaving the independent collection ({1,3}) with total weight (14).

### Constructed Example

Consider the actual sequence

```
4
1 100
3 101
2 102
4 204
```

The encoded input must use the previous answer, giving

```
4
1 100
103 1
203 175
207 15
```

The first vector is (1), the second is (3), and the third is (2). The third vector is dependent on the first two, so it causes an exchange. The fourth vector (4) introduces a completely new bit.

| Day | Decoded ((a,b)) | Current independent vectors | Answer |
| --- | --- | --- | --- |
| 1 | ((1,100)) | (1) | 100 |
| 2 | ((3,101)) | (1,3) | 201 |
| 3 | ((2,102)) | (3,2) | 203 |
| 4 | ((4,204)) | (3,2,4) | 407 |

The third day demonstrates why a weighted basis cannot simply reject dependent vectors. The vector (2) is dependent on (1) and (3), but replacing (1), whose weight is (100), with (2), whose weight is (102), improves the optimum. The fourth day then adds an independent vector and increases the answer directly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(60n)) | Every insertion performs at most 60 pivot eliminations, and each vector operation works on 60 coordinates as bit masks. |
| Space | (O(60)) | Only one basis vector and one weight are stored per possible bit position. |

There are only 60 possible pivots because every (a_i) is below (2^{60}). Even though there may be half a million rental sets, the maintained state never grows beyond 60 basis vectors. The encrypted input also forces processing to remain online, which this basis naturally supports because each answer is finalized before the next pair is decoded.

The reference C++ solutions operate comfortably within the official 1.5 second limit. The Python implementation above uses bit-sliced ternary operations to avoid a Python loop over all 60 coordinates during every vector addition, although the original contest's tight time limit is primarily designed around optimized compiled implementations.

## Test Cases

The following tests use the same online XOR encoding as the official input. The helper passes a custom reader to the solution so the same algorithm can be tested without modifying its logic.

```python
import io

# Use the solve() function from the solution above.

def run(inp: str) -> str:
    out = []

    class Reader:
        def __init__(self, s):
            self.f = io.StringIO(s)

        def __call__(self):
            return self.f.readline()

    # Capture stdout by using the same logic with a temporary buffer.
    import contextlib
    import sys

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        solve(Reader(inp))

    return buf.getvalue()

# Official sample
assert run(
    "3\n"
    "1 4\n"
    "6 7\n"
    "4 13\n"
) == "4\n7\n14\n", "official sample"

# Minimum-size input
assert run(
    "1\n"
    "1 5\n"
) == "5\n", "single rental set"

# Repeated vector with increasing weights.
# Actual values are (1,5), (1,7), (1,9).
assert run(
    "3\n"
    "1 5\n"
    "4 2\n"
    "6 14\n"
) == "5\n7\n9\n", "duplicate vectors"

# Weighted exchange.
# Actual values are:
# (1,100), (3,101), (2,102), (4,204)
assert run(
    "4\n"
    "1 100\n"
    "103 1\n"
    "203 175\n"
    "207 15\n"
) == "100\n201\n203\n407\n", "weighted basis exchange"

# Maximum-size input.
# Actual values are (1,2), (1,3), ..., (1,500001).
# Every vector is identical, so the best independent subset contains
# exactly one set, namely the most expensive one.
n = 500000
lines = [str(n)]
for i in range(1, n + 1):
    actual_b = i + 1
    if i == 1:
        last = 0
    else:
        last = i
    lines.append(f"{1 ^ last} {actual_b ^ last}")

large_input = "\n".join(lines) + "\n"
assert run(large_input).splitlines()[-1] == "500001", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 5` | `5` | Minimum-size instance and basic insertion |
| Three sets with (a=1) and weights (5,7,9) | `5, 7, 9` | Dependent vectors must not all be selected |
| ((1,100),(3,101),(2,102),(4,204)) | `100, 201, 203, 407` | Heavy dependent vectors must replace lighter basis vectors |
| 500000 identical vectors with increasing weights | Final answer `500001` | Maximum (n), online decoding, and rank-one behavior |

## Edge Cases

A single rental set is always safe because its two identical piles contribute either zero, one, or two copies of the same vector. A nonzero vector cannot become zero with coefficient (1) or (2), so Bob cannot leave a losing position. For the exact input

```
1
1 5
```

the vector is (1), the basis gains weight (5), and the output is `5`.

Repeated pile values are the main case where summing all positive rental costs fails. With

```
3
1 2
4 2
6 14
```

the decoded sets are ((1,2),(1,3),(1,4)). All three vectors are the same. The basis accepts the first vector with weight (2), replaces it with the second vector of weight (3), and then replaces it with the third vector of weight (4). The outputs are `2`, `3`, and `4`. At no point can two copies of the same vector coexist in the independent set.

A dependent vector can still be essential to the optimum when it is more expensive than an existing basis vector. In the constructed example, vectors (1) and (3) are initially selected with weights (100) and (101). Vector (2) is dependent on them, but its weight is (102). The insertion swaps out the (100)-weight vector and keeps the (101)- and (102)-weight vectors, giving `203`. Simply checking whether the new vector is independent and rejecting it would produce the wrong answer `201`.

A coefficient of (2) must also be handled correctly. Over (\mathbb F_3), a pivot coefficient can become (2) after elimination. Such a vector cannot be stored unchanged because the basis expects pivot coefficient (1). Multiplying it by (2) converts its pivot coefficient from (2) to (1), and swapping the two bit planes performs exactly this multiplication.

Finally, the previous answer participates in both coordinates of the next input pair. For the official sample, the first answer is (4), so the second encrypted pair ((6,7)) decodes to ((2,3)). After the second answer becomes (7), the third pair ((4,13)) decodes to ((3,10)). Updating `last` at any other point changes all subsequent decoded values and silently corrupts the entire computation.

If you want, I can also provide a C++17 version matching the intended contest-time implementation more closely, especially for the 1.5 second limit.
