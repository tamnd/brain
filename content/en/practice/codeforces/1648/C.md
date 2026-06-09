---
title: "CF 1648C - Tyler and Strings"
description: "We are given two sequences of integers, s and t, representing letters of two strings. Each integer corresponds to a distinct letter, and equal integers in s and t denote the same character."
date: "2026-06-10T03:58:28+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1648
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 775 (Div. 1, based on Moscow Open Olympiad in Informatics)"
rating: 1900
weight: 1648
solve_time_s: 57
verified: true
draft: false
---

[CF 1648C - Tyler and Strings](https://codeforces.com/problemset/problem/1648/C)

**Rating:** 1900  
**Tags:** combinatorics, data structures, implementation  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of integers, `s` and `t`, representing letters of two strings. Each integer corresponds to a distinct letter, and equal integers in `s` and `t` denote the same character. Tyler wants to count how many distinct rearrangements of `s` result in a string that is lexicographically smaller than `t`. The output should be taken modulo `998244353`.

Lexicographic comparison is defined as usual: given two sequences, the first differing element determines the order, or if one sequence is a strict prefix of the other, the shorter sequence is smaller. For example, `[1,2]` is smaller than `[1,2,3]`, but `[2,1]` is larger than `[1,2]`.

The constraints allow `n` and `m` up to 200,000. Computing all permutations of `s` is clearly infeasible because the factorial growth is extreme. Even storing all permutations is impossible. Therefore, we need an approach that counts arrangements without generating them explicitly.

A few tricky scenarios arise. If `s` contains repeated elements, naive counting of distinct permutations can overcount. If `n < m`, some permutations of `s` may be smaller simply because they are shorter than `t` but share a prefix. Also, if `n > m`, only permutations that differ in the first `m` elements and are smaller at that point are relevant; otherwise, they are automatically larger.

For example, if `s = [1,1,2]` and `t = [1,2,1,2]`, the permutations `[1,1,2]` and `[1,2,1]` are smaller than `t`, but `[2,1,1]` is larger. A careless approach that assumes all permutations of `s` shorter than `t` are smaller would overcount.

## Approaches

The brute-force method is to generate all distinct permutations of `s` and count those that are lexicographically smaller than `t`. This method works for correctness but fails immediately for `n > 10`, because the number of permutations is `n!` and can easily exceed `10^12`. Therefore, it is impractical for the given constraints.

The key insight for a faster solution is that lexicographic order can be determined incrementally by comparing the first element, then the second, and so on. If we know how many permutations begin with a certain number, we can count all permutations smaller than `t` without generating them. This reduces the problem to counting permutations with multiset constraints. Using factorials and modular inverses, we can compute the number of arrangements for each prefix efficiently. A Fenwick tree (binary indexed tree) helps quickly sum the counts of elements smaller than a current `t_i` in `O(log n)` time.

Thus, instead of generating permutations, we compute how many sequences start with each possible prefix that is smaller than `t`. When a prefix equals the start of `t`, we continue checking the next character. The first mismatch below `t` allows counting all remaining permutations using factorial division to account for repeated elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n!) | Too slow |
| Optimal | O(n log n + max_element) | O(max_element + n) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and modular inverses up to `max(n, max(s))` for use in permutation counting. This allows us to compute multinomial coefficients modulo `998244353`.
2. Count occurrences of each integer in `s` and store them in an array or dictionary `freq`. This represents the multiset of letters.
3. Initialize a Fenwick tree over the range of possible integers. Insert frequencies of all elements from `s`. This allows us to query quickly how many elements are smaller than a given integer.
4. Initialize the total number of permutations remaining as the multinomial coefficient of `s`, `total_perms = n! / (product of freq[i]!)`. This counts all distinct arrangements of `s`.
5. Iterate through `t` by index `i`:

a. For `t_i`, query the Fenwick tree for the sum of counts of elements smaller than `t_i`. Multiply this sum by the number of permutations of the remaining `n-i` elements (updating factorials to remove the used element), and add to the answer.

b. If `freq[t_i] == 0`, stop the iteration, because no permutation can continue to match `t`.

c. Otherwise, reduce `freq[t_i]` by one, update the Fenwick tree, and update `total_perms` accordingly to account for one element used.
6. If the iteration completes without stopping and `n < m`, add 1 to the answer because `s` itself is a prefix of `t` and therefore smaller.
7. Output the answer modulo `998244353`.

**Why it works:** At each step, the algorithm counts all sequences that diverge from `t` at that position in a smaller way, using multinomial coefficients to account for repeated elements. The Fenwick tree allows querying how many choices exist smaller than the current `t_i`. The invariant is that the number of permutations counted at each step is exactly the number of lexicographically smaller sequences starting with the prefix considered so far.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n, m = map(int, input().split())
    s = list(map(int, input().split()))
    t = list(map(int, input().split()))

    max_val = max(max(s, default=0), max(t, default=0)) + 2

    # Precompute factorials and inverses
    fact = [1] * (n + 2)
    invfact = [1] * (n + 2)
    for i in range(1, n + 2):
        fact[i] = fact[i - 1] * i % MOD
    invfact[n + 1] = modinv(fact[n + 1])
    for i in range(n + 1, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Frequency count
    freq = [0] * max_val
    for num in s:
        freq[num] += 1

    class Fenwick:
        def __init__(self, size):
            self.n = size
            self.tree = [0] * (size + 2)
        def add(self, i, v):
            while i <= self.n:
                self.tree[i] += v
                i += i & -i
        def sum(self, i):
            res = 0
            while i > 0:
                res += self.tree[i]
                i -= i & -i
            return res

    ft = Fenwick(max_val)
    for i in range(1, max_val):
        if freq[i]:
            ft.add(i, freq[i])

    total_perms = fact[n]
    for i in range(1, max_val):
        total_perms = total_perms * invfact[freq[i]] % MOD

    ans = 0
    rem = n
    for i in range(min(n, m)):
        x = t[i]
        smaller = ft.sum(x - 1)
        if smaller > 0:
            temp = total_perms * smaller % MOD
            temp = temp * modinv(rem) % MOD
            ans = (ans + temp) % MOD
        if freq[x] == 0:
            break
        total_perms = total_perms * freq[x] % MOD
        total_perms = total_perms * modinv(rem) % MOD
        freq[x] -= 1
        ft.add(x, -1)
        rem -= 1
    else:
        if n < m:
            ans = (ans + 1) % MOD

    print(ans)

solve()
```

The solution first sets up factorials and modular inverses to compute multinomial coefficients. Frequencies are stored and managed through a Fenwick tree to allow quick sum queries of smaller elements. The `total_perms` variable keeps track of the number of permutations remaining as elements are used. Each iteration through `t` counts permutations that start with a prefix smaller than `t` and adjusts the remaining permutations accordingly. Boundary conditions, such as `n < m` or missing elements in `s`, are handled explicitly.

## Worked Examples

**Sample 1:**

Input:

```
3 4
1 2 2
2 1 2 1
```

| i | t[i] | smaller | freq | total_perms | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | [1,2,2] | 3 | 1 |
| 1 | 1 | 1 | [1,1,2] | 1 | 2 |

Iteration stops after 2 elements, as next t[2]=2 but remaining freq allows permutations. Since n<m, no further addition. Answer = 2.

**Sample 2:**

Input:

```
4 4
1 2 3 4
4 3 2 1
```

| i | t[i] | smaller | freq | total_perms | ans |
| --- | --- | --- | --- | --- | --- |
