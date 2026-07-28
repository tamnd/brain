---
title: "CF 102766D - Regular Bracket Sequence Again?"
description: "We have exactly N opening brackets and N closing brackets, so every valid answer is a regular bracket sequence of length 2N. Among all such sequences, we need to count only the ones that cannot be obtained by taking some string of length N and writing it twice consecutively."
date: "2026-07-28T23:38:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102766
codeforces_index: "D"
codeforces_contest_name: "Codedigger Training Contest -String"
rating: 0
weight: 102766
solve_time_s: 56
verified: true
draft: false
---

[CF 102766D - Regular Bracket Sequence Again?](https://codeforces.com/problemset/problem/102766/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We have exactly `N` opening brackets and `N` closing brackets, so every valid answer is a regular bracket sequence of length `2N`. Among all such sequences, we need to count only the ones that cannot be obtained by taking some string of length `N` and writing it twice consecutively.

A string is called `N`-periodic when its first half and second half are identical. For example, with `N = 2`, the string `)()(` is periodic because the first two characters `)(` are repeated, while `)(()` is not.

The task is not to construct the sequences. We only need the count modulo `10^9 + 7`.

The constraint `N <= 1000` and the number of test cases being at most `1000` tell us that an `O(N)` or `O(N log N)` preprocessing approach is enough. A solution that generates bracket sequences is impossible because the number of regular bracket sequences is the Catalan number, which grows exponentially. Even for moderately small `N`, enumeration becomes far too large.

The main edge cases come from confusing the length of the repeated part with the number of pairs of brackets. For `N = 1`, the only regular bracket sequence is `()`. It cannot be split into two equal non-empty halves, so the answer is `1`. A careless solution that always subtracts one periodic sequence would incorrectly output `0`.

Another important case is when `N` is odd. For example, with input `N = 3`, the total number of regular bracket sequences is `5`. A periodic sequence would need a first half of length `3` that contains equal numbers of opening and closing brackets. That is impossible because a string of odd length cannot have equal counts of both brackets. The correct answer is `5`, and a careless approach that assumes every `N` creates a smaller Catalan subtraction would be wrong.

The last boundary case is when `N` is even. For `N = 4`, the regular sequences are counted by `Catalan(4) = 14`. The periodic ones are exactly the sequences formed by repeating a regular sequence of length `4`, giving `Catalan(2) = 2` invalid sequences. The answer is `12`. Forgetting that the repeated half must itself be balanced would subtract too many strings.

## Approaches

The direct approach is to generate every regular bracket sequence with `N` pairs, check whether it is periodic, and count the ones that are not. This is correct because it examines exactly the required set. However, the number of regular bracket sequences is `Catalan(N)`, which is approximately exponential. For `N = 1000`, even representing the answer space is impossible, so brute force cannot work.

The useful observation comes from looking at what a periodic regular bracket sequence must look like. Suppose a valid sequence `S` has length `2N` and is `N`-periodic. Then it has the form `T + T`, where `T` has length `N`.

Because the whole sequence is balanced, the total bracket balance of `T + T` must be zero. The balance of the first copy is therefore some value `x`, and the second copy contributes another `x`, giving `2x = 0`. Hence `x = 0`, meaning the first half already contains the same number of opening and closing brackets.

Now consider validity. Every prefix of the whole sequence must have at least as many opening brackets as closing brackets. The first copy of `T` is a prefix of the full string, so every prefix inside `T` must be valid. Since `T` also has balance zero, `T` itself is a regular bracket sequence.

This gives a one-to-one relationship. Every `N`-periodic regular bracket sequence corresponds to a regular bracket sequence of length `N`, and such a sequence exists only when `N` is even. If `N = 2k`, the number of periodic sequences is `Catalan(k)`.

The total number of regular bracket sequences with `N` pairs is `Catalan(N)`, so the final answer is:

`Catalan(N) - Catalan(N / 2)` when `N` is even.

`Catalan(N)` when `N` is odd.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential, approximately O(Catalan(N)) | Exponential | Too slow |
| Optimal | O(N) preprocessing and O(1) per query | O(N) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials up to `1000`. The Catalan numbers can be calculated using the combination formula:

`Catalan(n) = C(2n, n) - C(2n, n + 1)`

which is equivalent to:

`Catalan(n) = (2n choose n) / (n + 1)`.

Precomputing these values allows every query to be answered immediately.
2. For each query with value `N`, start with the total number of regular bracket sequences, which is `Catalan(N)`.

This counts every possible valid sequence before removing the periodic ones.
3. If `N` is even, subtract `Catalan(N / 2)`.

The only sequences that are removed are exactly those where the first half is itself a regular bracket sequence.
4. If `N` is odd, do not subtract anything.

A half of odd length cannot contain equal numbers of opening and closing brackets, so no periodic regular sequence exists.
5. Print the resulting value modulo `10^9 + 7`.

Why it works:

The invariant behind the solution is that every invalid sequence has a unique first half. A sequence counted as periodic must be two identical copies of that half. For the complete string to be regular, the half must have zero balance and every prefix of it must be valid. These are precisely the conditions for the half to be a regular bracket sequence. Therefore the periodic sequences are counted exactly by the smaller Catalan number, and subtracting them removes every and only unwanted sequence.

## Python Solution

```python
import sys

input = sys.stdin.readline

MOD = 10**9 + 7

MAX_N = 1000

fact = [1] * (2 * MAX_N + 5)
for i in range(1, len(fact)):
    fact[i] = fact[i - 1] * i % MOD

inv_fact = [1] * (2 * MAX_N + 5)
inv_fact[-1] = pow(fact[-1], MOD - 2, MOD)
for i in range(len(inv_fact) - 1, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD

def comb(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

catalan = [0] * (MAX_N + 1)
for i in range(MAX_N + 1):
    catalan[i] = (comb(2 * i, i) - comb(2 * i, i + 1)) % MOD

def solve():
    t = int(input())
    ans = []
    for _ in range(t):
        n = int(input())
        cur = catalan[n]
        if n % 2 == 0:
            cur -= catalan[n // 2]
        ans.append(str(cur % MOD))
    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The preprocessing part builds factorials and inverse factorials so combinations can be computed in constant time under the modulo. The largest needed Catalan index is `1000`, but calculating `Catalan(1000)` requires `C(2000, 1000)`, so factorials are stored up to `2000`.

The query processing follows the mathematical result directly. It first takes the total number of regular bracket sequences. When `N` is even, the repeated halves are counted by the Catalan number of `N / 2` pairs and are removed.

The modulo subtraction is handled at the end with `% MOD` because the intermediate value can become negative after removing the periodic sequences.

## Worked Examples

For `N = 2`, the computation is:

| Step | N | Total Catalan | Periodic Count | Answer |
| --- | --- | --- | --- | --- |
| Start | 2 | 2 | 0 | 2 |
| Remove periodic | 2 | 2 | Catalan(1)=1 | 1 |

The two regular sequences are `(())` and `()()`. The second one is the repeated form of `()`, so only one sequence remains.

For `N = 4`, the computation is:

| Step | N | Total Catalan | Periodic Count | Answer |
| --- | --- | --- | --- | --- |
| Start | 4 | 14 | 0 | 14 |
| Remove periodic | 4 | 14 | Catalan(2)=2 | 12 |

The two removed sequences are created by taking the two regular sequences with two pairs of brackets and repeating them twice. Every other valid sequence is non-periodic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MAX_N + T) | Catalan values are precomputed once and each query is answered in constant time |
| Space | O(MAX_N) | Only factorial arrays and Catalan values are stored |

The maximum `N` is small enough that precomputing all values is easily within the memory limit. The final query processing is effectively constant time, which comfortably handles the maximum number of test cases.

## Test Cases

```python
import sys
import io

MOD = 10**9 + 7

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    # insert the solution function here when running locally

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# Expected outputs from the actual solution:
assert run("4\n1\n2\n3\n4\n") == "1\n1\n5\n12\n", "samples"

# The following expected values validate the logic:
# N = 1: Catalan(1) = 1, no periodic sequence
# N = 2: Catalan(2) - Catalan(1) = 1
# N = 3: Catalan(3) = 5 because odd N has no periodic sequences
# N = 6: Catalan(6) - Catalan(3) = 132 - 5 = 127
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum size where no periodic subtraction is possible |
| `2` | `1` | Smallest even case with one periodic sequence |
| `3` | `5` | Odd length half cannot be balanced |
| `6` | `127` | Larger even case with Catalan subtraction |

## Edge Cases

For `N = 1`, the algorithm computes `Catalan(1) = 1`. Since `N` is odd, it does not subtract anything. The result is `1`, matching the only sequence `()`.

For `N = 3`, the total number of valid sequences is `Catalan(3) = 5`. The algorithm checks parity and sees that `3` is odd, so it leaves the count unchanged. This handles the case where no valid first half of length three can exist.

For `N = 4`, the algorithm starts with `Catalan(4) = 14`. Since the length is even, it subtracts `Catalan(2) = 2`. Those two sequences represent all possible repeated halves, leaving `12` non-periodic regular bracket sequences.

For very large allowed values such as `N = 1000`, the algorithm never builds the sequences themselves. It only uses precomputed combinatorial values, so it avoids the exponential growth of the actual number of bracket strings.

I can also provide a shorter contest-editorial version or a more formal proof-focused version if needed.
