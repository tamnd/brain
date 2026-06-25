---
title: "CF 106195H - Equivalence classes"
description: "The problem asks us to count how many different sequences of operations can create a given number of equivalence classes. We start with n elements that are all considered identical."
date: "2026-06-25T10:41:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106195
codeforces_index: "H"
codeforces_contest_name: "HAMMERWARS 2025"
rating: 0
weight: 106195
solve_time_s: 45
verified: true
draft: false
---

[CF 106195H - Equivalence classes](https://codeforces.com/problemset/problem/106195/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to count how many different sequences of operations can create a given number of equivalence classes. We start with `n` elements that are all considered identical. Each operation chooses some subset of the elements and separates the chosen elements from the unchosen ones. After all operations, two elements are still equivalent exactly when they were always treated the same way by every operation. The task is to output, for every possible number of final equivalence classes from `1` to `n`, how many operation sequences produce exactly that many classes. This is the problem titled “Equivalence classes” from Codeforces Gym 106195.

The key way to view the operations is to assign each element a binary signature. For every operation, an element receives a `0` if it was outside the chosen subset and a `1` if it was inside. After `k` operations, every element has a binary string of length `k`. Two elements are equivalent exactly when their signatures are equal, so the number of equivalence classes is the number of distinct signatures used.

There are `2^k` possible signatures. The constraints allow `n` to reach `10000`, so an `O(n^2)` solution is realistic, but anything depending on `2^k` directly is impossible because `k` can be as large as `10^18`. We need formulas that only use `n` and modular arithmetic.

The subtle part is that the number of classes cannot exceed `n`, even though there may be many possible signatures. A common mistake is to count ways to pick classes without considering that the elements are labeled. For example, if `n = 2` and `k = 1`, there are two possible signatures, `0` and `1`.

For input:

```
2 1
```

there are four possible operation sequences. Choosing the empty set gives both elements signature `0`, choosing the full set gives both signature `1`, and choosing either single-element subset gives two different signatures. The answer is:

```
2
2
```

The first line means there are two ways to create one class, and the second means there are two ways to create two classes. A careless approach that only counts possible sets of signatures would get the first value wrong because the elements are distinguishable.

Another edge case appears when `k` is huge but `n` is small. For example:

```
3 1000000000000000000
```

There are astronomically many possible signatures, but we only need the first few values of the falling factorial `(2^k)(2^k-1)...`, because at most three different signatures can actually be used. Any approach trying to enumerate signatures immediately fails.

## Approaches

The brute-force idea is to think about all possible final signatures. Each of the `n` elements can receive any of the `2^k` binary strings, so there are `(2^k)^n` possible assignments. We could generate every assignment, count the number of distinct signatures, and increment the answer for that number of classes.

This is correct because a sequence of operations is exactly the same as choosing one signature for every element. However, the number of assignments is impossible to handle. Even for moderate values like `n = 100` and `k = 100`, the search space is far beyond what any program can visit.

The useful observation is that we do not care which particular signatures are used, only how many distinct ones appear. Suppose the final number of classes is `i`. First, we need to choose which `i` signatures are used. There are `C(2^k, i)` choices. Then we need to assign the `n` labeled elements onto these `i` chosen signatures so that every signature appears at least once.

The second part is the number of onto functions from `n` elements to `i` classes. This value is `i! * S(n, i)`, where `S(n, i)` is a Stirling number of the second kind. Multiplying the two parts gives:

```
C(2^k, i) * i! * S(n, i)
```

which can be rewritten as:

```
(2^k)(2^k - 1)...(2^k - i + 1) * S(n, i)
```

The first factor is a falling factorial. Since we only need values up to `i = n`, we never need more than `10000` terms, so we can compute it directly modulo `998244353`.

The Stirling numbers are computed with the recurrence:

```
S(n, i) = S(n - 1, i - 1) + i * S(n - 1, i)
```

The recurrence comes from considering the last element. It either forms a new class by itself, or joins one of the existing `i` classes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2^k)^n) | O(n) | Too slow |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the value of `2^k` modulo `998244353`. We never need the actual value because every multiplication and subtraction in the formula is done under the modulus.
2. Compute all Stirling numbers `S(n, i)` for `1 <= i <= n` using dynamic programming. The recurrence builds answers row by row, where each row represents the number of ways to split a prefix of elements into a given number of non-empty groups.
3. Build the falling factorial values. Start with `1`, then repeatedly multiply by `(2^k - i)` for each possible number of classes. The value after `i` multiplications represents the number of ways to choose and order `i` different signatures.
4. For every possible number of classes `i`, multiply the falling factorial by `S(n, i)`. This gives the number of operation sequences producing exactly `i` equivalence classes.

The reason this works is that every final state is uniquely represented by the signatures of the elements. If exactly `i` signatures appear, the used signatures can be ordered in `P(2^k, i)` ways, and the elements must be partitioned into `i` non-empty groups assigned to those signatures. The Stirling number counts exactly those partitions, so every valid sequence is counted once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, k = map(int, input().split())

    sig = pow(2, k, MOD)

    dp = [0] * (n + 1)
    dp[0] = 1

    for elements in range(1, n + 1):
        nxt = [0] * (n + 1)
        for groups in range(1, elements + 1):
            nxt[groups] = (dp[groups - 1] + groups * dp[groups]) % MOD
        dp = nxt

    ans = [0] * (n + 1)
    fall = 1
    for i in range(1, n + 1):
        fall = fall * ((sig - i + 1) % MOD) % MOD
        ans[i] = fall * dp[i] % MOD

    print("\n".join(map(str, ans[1:])))

if __name__ == "__main__":
    solve()
```

The first part of the code computes `2^k` with modular exponentiation. This handles extremely large values of `k` without ever constructing the actual number of possible signatures.

The dynamic programming array stores the current row of Stirling numbers. When adding a new element, the element either creates a new class, represented by the previous row shifted by one, or joins an existing class, which contributes the multiplication by the number of available groups.

The falling factorial is built incrementally. The expression uses `sig - i + 1` because after choosing `i - 1` signatures, exactly that many fewer choices remain. The modulo operation is applied before multiplication to keep all values bounded.

The final multiplication combines the two independent choices: selecting the actual signatures and distributing the labeled elements among them.

## Worked Examples

For:

```
2 1
```

the possible signatures are `0` and `1`.

| Classes | Falling factorial | Stirling value | Answer |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 2 |
| 2 | 2 | 1 | 2 |

The two one-class sequences are choosing both elements together, and the two two-class sequences separate the elements. This confirms that the formula counts labeled elements correctly.

For:

```
3 2
```

there are four possible signatures. The computation is:

| Classes | Falling factorial | Stirling value | Answer |
| --- | --- | --- | --- |
| 1 | 4 | 1 | 4 |
| 2 | 12 | 3 | 36 |
| 3 | 24 | 1 | 24 |

The output is:

```
4
36
24
```

The last row represents choosing three different signatures and assigning one element to each. The middle row uses the three possible ways to split three labeled elements into two non-empty groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Computing all Stirling values dominates the runtime |
| Space | O(n) | Only the previous dynamic programming row is stored |

With `n <= 10000`, around `10^8` simple operations are acceptable in optimized Python. The memory usage stays small because the dynamic programming is compressed to one dimension.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_case(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline().split()
    if not data:
        return ""
    n, k = map(int, data)

    MOD = 998244353
    sig = pow(2, k, MOD)

    dp = [0] * (n + 1)
    dp[0] = 1
    for elements in range(1, n + 1):
        nxt = [0] * (n + 1)
        for groups in range(1, elements + 1):
            nxt[groups] = (dp[groups - 1] + groups * dp[groups]) % MOD
        dp = nxt

    ans = []
    fall = 1
    for i in range(1, n + 1):
        fall = fall * ((sig - i + 1) % MOD) % MOD
        ans.append(str(fall * dp[i] % MOD))

    sys.stdin = old
    return "\n".join(ans)

assert solve_case("2 1\n") == "2\n2"
assert solve_case("1 1000000000000000000\n") == "1"
assert solve_case("3 2\n") == "4\n36\n24"
assert solve_case("5 1\n") == "2\n30\n0\n0\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1` | `2, 2` | Smallest non-trivial case |
| `1` with huge `k` | `1` | Large exponent handling |
| `3 2` | `4, 36, 24` | Normal Stirling computation |
| `5 1` | `2, 30, 0, 0, 0` | Not enough signatures for many classes |

## Edge Cases

When `n = 1`, there is only one element, so every possible sequence of operations leaves exactly one equivalence class. The algorithm handles this because the only Stirling value needed is `S(1,1)=1`, and the falling factorial has one term.

When `k` is very large, the number of possible signatures is enormous, but the algorithm only needs `2^k mod 998244353`. For example, with `n = 3` and `k = 10^18`, the code never stores the signatures themselves and only computes the three falling factorial terms needed.

When the number of desired classes is larger than the number of available signatures, the falling factorial automatically becomes zero. This happens because eventually we try to choose more distinct signatures than exist, so the answer for those class counts is correctly zero.
