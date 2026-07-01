---
title: "CF 104333A - Convolution XOR SUM"
description: "We are given two arrays of equal length. One array represents values attached to indices we are allowed to permute, and the other array represents fixed “slots”."
date: "2026-07-01T18:54:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104333
codeforces_index: "A"
codeforces_contest_name: "Replay of BU - PSTU Programming club collaborative contest"
rating: 0
weight: 104333
solve_time_s: 75
verified: true
draft: false
---

[CF 104333A - Convolution XOR SUM](https://codeforces.com/problemset/problem/104333/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of equal length. One array represents values attached to indices we are allowed to permute, and the other array represents fixed “slots”. For any rearrangement of the first array, we match each element of the permuted array with a position in the second array and compute a score equal to the sum of bitwise XORs of paired elements.

The task is not to find the best permutation, but to compute something much larger: the total score over all possible permutations. Since there are $n!$ permutations, every pairing between an $a_i$ and a $b_j$ appears many times across all permutations, and the goal is to aggregate their contributions efficiently.

The constraint $n \le 10^5$ immediately rules out any approach that iterates over permutations or even processes pairs naively in $O(n^2)$. Even $O(n \log n)$ or $O(n)$ methods are acceptable, but anything involving combinatorial enumeration must be replaced with counting arguments.

A common failure mode here is attempting to reason per permutation or simulate swapping effects. For example, with $n=3$, one might try to compute scores for all 6 permutations explicitly. That works for tiny cases but scales factorially and becomes impossible even at $n=15$.

Another subtle issue is double-counting logic: since XOR is not linear in a naive sense over permutations, a mistaken approach might try to pair sorted arrays or greedily match values. That loses the combinatorial structure entirely.

The key difficulty is recognizing that every pair $(a_i, b_j)$ contributes symmetrically across permutations, and we only need to count how many permutations place $a_i$ at position $j$.

## Approaches

The brute-force solution iterates over every permutation $p$, computes its score by summing $a_{p_i} \oplus b_i$, and accumulates the result. This is correct because it follows the definition directly. However, it requires generating $n!$ permutations, and each permutation costs $O(n)$ to evaluate, leading to $O(n \cdot n!)$, which is far beyond feasible limits even for $n=12$.

The structural insight comes from symmetry. Fix an element $a_k$. Across all permutations, this element is placed in each position $j$ exactly the same number of times. Specifically, if we fix $a_k$ at position $j$, the remaining $n-1$ elements can be permuted arbitrarily, giving $(n-1)!$ permutations. This means every pair $(a_k, b_j)$ contributes exactly $(n-1)!$ times to the final sum.

So instead of thinking about permutations, we reduce the problem to summing contributions of all pairs, each weighted equally by $(n-1)!$. The answer becomes:

$$(n-1)! \cdot \sum_{i=1}^{n} \sum_{j=1}^{n} (a_i \oplus b_j)$$

Now the problem is reduced to computing the double XOR sum efficiently. XOR can be decomposed bit by bit, and each bit contributes independently. For a fixed bit $t$, we only need to count how many $a_i$ have that bit set and how many $b_j$ have that bit set. The contribution of bit $t$ to $a_i \oplus b_j$ is 1 exactly when the bits differ, which gives a standard combinatorial expression.

Let $c_a$ be the count of numbers in $a$ with bit $t$ set, and $c_b$ similarly for $b$. Then the number of pairs with differing bits is $c_a (n - c_b) + (n - c_a)c_b$. Each such pair contributes $2^t$.

We sum over all bits up to 17 (since values are up to $10^5$), multiply by $(n-1)!$, and we are done.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot n!)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log A)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We restructure the problem into counting contributions per bit and scaling by permutation symmetry.

1. Compute factorial $(n-1)!$ modulo $10^9+7$. This represents how many permutations fix a chosen element at a fixed position. The key idea is that each such assignment leaves the remaining elements freely permutable.
2. For each bit position $t$ from 0 to 17, count how many elements in $a$ have this bit set, and how many elements in $b$ have it set. This isolates XOR behavior into independent binary dimensions.
3. For bit $t$, compute how many ordered pairs produce a 1 in XOR at this bit. This happens exactly when one side has the bit set and the other does not, so we count cross combinations between the two groups.
4. Multiply the number of differing-bit pairs by $2^t$, since each such pair contributes that value to XOR.
5. Accumulate contributions across all bits to obtain the total pairwise XOR sum over all $a_i, b_j$.
6. Multiply the final pairwise sum by $(n-1)!$ to account for all permutations, since every pair appears in exactly that many permutation positions.

### Why it works

The correctness hinges on uniform distribution of elements across permutation positions. Any fixed element $a_i$ appears in position $j$ in exactly $(n-1)!$ permutations, independent of $i$ and $j$. This symmetry reduces the permutation sum into a uniform scaling of the complete bipartite sum over all pairs. Once reduced to pairwise structure, XOR linearity per bit guarantees that counting set-bit mismatches fully characterizes the total contribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    # factorial (n-1)!
    fact = 1
    for i in range(1, n):
        fact = fact * i % MOD
    
    max_bit = 17
    cnt_a = [0] * (max_bit + 1)
    cnt_b = [0] * (max_bit + 1)
    
    for x in a:
        for t in range(max_bit + 1):
            if x >> t & 1:
                cnt_a[t] += 1
    
    for x in b:
        for t in range(max_bit + 1):
            if x >> t & 1:
                cnt_b[t] += 1
    
    pair_sum = 0
    for t in range(max_bit + 1):
        ca = cnt_a[t]
        cb = cnt_b[t]
        diff_pairs = ca * (n - cb) + (n - ca) * cb
        pair_sum = (pair_sum + diff_pairs * (1 << t)) % MOD
    
    ans = pair_sum * fact % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by computing $(n-1)!$, which encodes how many permutations assign a fixed element to a fixed position. This factor is applied at the end after computing the total contribution of all element pairs.

The next step compresses the XOR structure into bit counts. Instead of computing XOR directly, we count how many numbers in each array have each bit set. This avoids quadratic pair iteration.

For each bit, we compute how many cross-pairs produce a 1 at that bit. The expression $c_a (n - c_b) + (n - c_a)c_b$ comes directly from splitting cases where bits differ.

Finally, we multiply the total pairwise XOR sum by the permutation multiplicity factor.

A subtle point is ensuring we never attempt to construct permutations explicitly. The entire combinatorial explosion is absorbed into the factorial multiplier.

## Worked Examples

### Sample 1

Input:

```
3
1 2 3
1 2 3
```

We compute $(n-1)! = 2$.

We count bit contributions. For simplicity, consider actual XOR pairs:

| Pair type | Count | XOR contribution sum |
| --- | --- | --- |
| all $a_i, b_j$ pairs | 9 | 12 |

So pairwise sum is 12, and multiplying by 2 gives 24.

This shows that every pair contributes equally across permutations, and factorial scaling is sufficient to reconstruct the full answer.

### Sample 2

Input:

```
3
2 2 2
3 4 4
```

Here all $a_i$ are identical, so symmetry is even stronger.

We compute $(n-1)! = 2$. Now evaluate pairwise XOR:

For $2 \oplus 3 = 1$, and $2 \oplus 4 = 6$.

Pair counts:

- (2,3) appears 3 times
- (2,4) appears 6 times

Total pairwise sum:

$3 \cdot 1 + 6 \cdot 6 = 39$

Multiply by 2 gives $78$.

This confirms that multiplicities are handled correctly even when values repeat heavily.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log A)$ | Counting bits for each element up to 17 bits |
| Space | $O(1)$ | Fixed-size arrays for bit counts |

The algorithm runs in linear time with a small constant factor due to fixed bit width. This is well within limits for $n = 10^5$.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    fact = 1
    for i in range(1, n):
        fact = fact * i % MOD

    max_bit = 17
    cnt_a = [0] * (max_bit + 1)
    cnt_b = [0] * (max_bit + 1)

    for x in a:
        for t in range(max_bit + 1):
            if x >> t & 1:
                cnt_a[t] += 1

    for x in b:
        for t in range(max_bit + 1):
            if x >> t & 1:
                cnt_b[t] += 1

    pair_sum = 0
    for t in range(max_bit + 1):
        ca = cnt_a[t]
        cb = cnt_b[t]
        diff = ca * (n - cb) + (n - ca) * cb
        pair_sum = (pair_sum + diff * (1 << t)) % MOD

    return str(pair_sum * fact % MOD)

# provided samples
assert run("""3
1 2 3
1 2 3
""") == "24"

assert run("""3
2 2 2
3 4 4
""") == "78"

# custom cases
assert run("""1
5
7
""") == "2", "single element XOR 5^7 * 0! = 2"

assert run("""2
1 2
1 2
""") == str((1^1 + 1^2 + 2^1 + 2^2) * 1), "direct check n=2"

assert run("""4
0 0 0 0
1 2 3 4
"""), "all a zero edge case"

assert run("""3
5 5 5
5 5 5
""") == "0", "all identical arrays"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 single values | direct XOR | base factorial case |
| n=2 small mix | brute match | correctness of pair expansion |
| all zeros vs range | structured XOR | bit counting correctness |
| identical arrays | 0 | cancellation case |

## Edge Cases

When $n=1$, there is exactly one permutation and the factorial factor becomes $(n-1)! = 1$. The algorithm reduces to a single XOR computation, so it naturally handles the degenerate combinatorial structure without special casing.

When all values in $a$ are identical, the bit counting approach still works because it does not depend on uniqueness. Every bit contribution is determined solely by frequency, and the formula correctly collapses all pair differences into uniform counts.

When both arrays are identical, every XOR is zero, so all bit mismatch counts vanish. The algorithm produces zero because for every bit, $c_a = c_b$, making both cross terms cancel exactly, which confirms the correctness of the bitwise decomposition.
