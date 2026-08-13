---
title: "CF 102284M - \u0422\u0440\u0438\u0441\u043a\u0430\u0439\u0434\u0435\u043a\u0430\u0444\u043e\u0431\u0438\u044f"
description: "We need to work with the increasing sequence of all positive integers whose prime factors belong to the fixed set {2, 3, 5, 7, 11}. Such numbers can be written exactly as [ 2^a3^b5^c7^d11^e, ] where all five exponents are nonnegative integers."
date: "2026-08-13T09:04:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102284
codeforces_index: "M"
codeforces_contest_name: "\u041b\u041a\u0428 2019, \u0418\u044e\u043b\u044c, \u041c\u0438\u043a\u0441 \u0441\u0442\u0430\u0440\u0448\u0435\u0439 \u0438 \u043c\u043b\u0430\u0434\u0448\u0435\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434"
rating: 0
weight: 102284
solve_time_s: 155
verified: false
draft: false
---

[CF 102284M - \u0422\u0440\u0438\u0441\u043a\u0430\u0439\u0434\u0435\u043a\u0430\u0444\u043e\u0431\u0438\u044f](https://codeforces.com/problemset/problem/102284/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We need to work with the increasing sequence of all positive integers whose prime factors belong to the fixed set `{2, 3, 5, 7, 11}`. Such numbers can be written exactly as

[
2^a3^b5^c7^d11^e,
]

where all five exponents are nonnegative integers. The number `1` is included because it has no prime factors.

The input contains `n` and `k`. The first `n` elements of the sequence are considered already skipped, and we must print the following `k` elements, namely `a_{n+1}` through `a_{n+k}`. Since `n + k <= 200000`, we never need more than the first 200000 sequence elements.

The main difficulty is that the sequence is sparse. Even though we need only 200000 elements, the 200000th element is much larger than 200000, so scanning every ordinary integer up to that value is wasteful. The bounds are designed for an algorithm whose work depends on the number of generated sequence elements, rather than on the numerical value of those elements. An `O((n+k) log(n+k))` solution is easily reasonable, while an algorithm proportional to the largest value we have to inspect can require hundreds of millions or billions of iterations.

There are several indexing and duplication traps. First, `n = 0` means that the answer starts with `1`. For example, input `0 1` must produce `1`. An implementation that initializes the generated array with `1` but then starts reading from index `n + 1` incorrectly can skip it.

A second trap is that different products can represent the same number. For example, `6` is both `2 * 3` and `3 * 2`. For input `5 1`, the correct output is `6`. An implementation that advances only one generator when several candidate products equal the minimum will insert `6` twice and shift every later answer.

A third trap is the distinction between the zero-based array used by the implementation and the one-based mathematical sequence. For input `12 1`, the correct answer is `14`, because the first twelve elements end at `12`. Using `dp[n]` as the first requested value would instead return `14` only if the array indexing is handled consistently, while mixing one-based and zero-based positions can silently return `12` or `15`.

Finally, `k` may be as small as one even when `n` is close to its maximum. For example, `199999 1` is valid because `n + k = 200000`. The algorithm must generate exactly 200000 elements internally and print only the final one.

## Approaches

The direct approach is to examine positive integers in increasing order and test whether each one has any prime factor larger than `11`. A simple test repeatedly divides the candidate by `2`, `3`, `5`, `7`, and `11`, then checks whether the remaining value is `1`. Every accepted number is appended until we have generated `n+k` elements.

This is correct because after removing every possible factor from the allowed set, a number is smooth exactly when nothing remains. The problem is the size of the search interval. If the last required sequence element is `a_{n+k}`, the brute-force method examines every integer from `1` through `a_{n+k}`. With five divisibility tests per integer, it performs roughly `5 * a_{n+k}` divisibility checks in a straightforward implementation. The quantity `a_{n+k}` is vastly larger than `n+k`, so the algorithm spends almost all of its time rejecting numbers that were never candidates for the answer.

The useful structural observation is that every valid number can be obtained from another valid number by multiplying by one of the five allowed primes. Starting from `1`, multiplying by `2`, `3`, `5`, `7`, or `11` always keeps us inside the sequence. More importantly, if the sequence is already known up to `a_i`, then every possible next element must be one of

[
2a_j,\quad 3a_j,\quad 5a_j,\quad 7a_j,\quad 11a_j
]

for some earlier index `j`.

For each prime we can keep a pointer to the first sequence element whose product with that prime has not yet been considered. The smallest of the five current products is the next sequence value. When several products equal that value, all corresponding pointers must advance. This is the same monotone-generation idea used for classic ugly-number sequences, extended from three primes to five.

The pointers never move backwards. Each pointer advances at most `n+k` times, and each generated element requires only five candidate comparisons. That changes the cost from depending on the numerical size of the answer to depending directly on the number of sequence elements we need.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(a_{n+k})` divisibility checks | `O(n+k)` | Too slow |
| Optimal | `O(n+k)` | `O(n+k)` | Accepted |

## Algorithm Walkthrough

1. Store `1` as the first sequence element. It is valid because its prime factorization is empty.
2. Create five pointers, one for each prime `2`, `3`, `5`, `7`, and `11`. Initially all pointers are `0`, meaning that every generator starts from `1`.
3. For the next sequence position, compute the five candidates `dp[p2] * 2`, `dp[p3] * 3`, `dp[p5] * 5`, `dp[p7] * 7`, and `dp[p11] * 11`. The smallest candidate is the smallest valid number that has not yet been generated.
4. Append that minimum to `dp`. Since every candidate is a valid number and every valid number larger than the current last element can be represented as an earlier valid number multiplied by one of the five primes, the minimum candidate must be the next sequence element.
5. For every prime whose candidate equals the newly generated value, advance its pointer by one. All matching pointers must move, because otherwise the same value would appear again on a later iteration.
6. Continue until `n+k` elements have been generated. The requested answer occupies zero-based positions `n` through `n+k-1`, so output `dp[n:n+k]`.

The key invariant is that after generating `dp[i]`, the array contains exactly the first `i+1` elements of the required sequence in strictly increasing order. For every allowed prime `p`, its pointer identifies the first index whose product with `p` is still greater than the last generated value. Consequently, the five current products represent the smallest not-yet-covered candidates from all five multiplication families. Taking their minimum cannot skip a valid number. Advancing every pointer that produced the minimum prevents duplicates. By induction, every generated element is exactly the next element of the mathematical sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_terms(n, k):
    total = n + k
    primes = (2, 3, 5, 7, 11)

    dp = [1]
    ptr = [0] * 5

    while len(dp) < total:
        candidates = [
            dp[ptr[i]] * primes[i]
            for i in range(5)
        ]

        nxt = min(candidates)
        dp.append(nxt)

        for i in range(5):
            if candidates[i] == nxt:
                ptr[i] += 1

    return dp[n:n + k]

def solve():
    n, k = map(int, input().split())
    print(*get_terms(n, k))

if __name__ == "__main__":
    solve()
```

The `dp` array stores the sequence in increasing order, starting with `1`. The five entries of `ptr` are the moving generators. At every iteration, the code constructs exactly five candidates, chooses their minimum, and then advances every pointer responsible for that minimum.

The equality check in the final loop is essential. Suppose the current candidates include `6` from both `2 * 3` and `3 * 2`. If only one pointer moved, `6` would remain as a candidate of the other generator and would be appended again. Advancing all equal candidates removes every representation of the value that has just been consumed.

The stopping condition uses `len(dp) < total`, so exactly `n+k` sequence values are constructed. This avoids an off-by-one error around the requested interval. Since the mathematical sequence is one-based but Python lists are zero-based, `a_{n+1}` corresponds to `dp[n]`, which is exactly why the slice starts at `n`.

Python integers have arbitrary precision, so multiplication by `11` cannot overflow. In a language with fixed-width integers, the corresponding implementation should use a type large enough for the largest generated value.

The five pointers move only forward. Across the entire run, each pointer advances at most `n+k` times, so the pointer maintenance contributes linear work. The five candidate computations per generated element are constant work.

## Worked Examples

For Sample 1, the input is `0 13`. We need the first thirteen sequence elements, so generation starts from `1` and continues until thirteen values have been stored.

| Step | Generated value | Sequence prefix |
| --- | --- | --- |
| 1 | 1 | `1` |
| 2 | 2 | `1 2` |
| 3 | 3 | `1 2 3` |
| 4 | 4 | `1 2 3 4` |
| 5 | 5 | `1 2 3 4 5` |
| 6 | 6 | `1 2 3 4 5 6` |
| 7 | 7 | `1 2 3 4 5 6 7` |
| 8 | 8 | `1 2 3 4 5 6 7 8` |
| 9 | 9 | `1 2 3 4 5 6 7 8 9` |
| 10 | 10 | `1 2 3 4 5 6 7 8 9 10` |
| 11 | 11 | `1 2 3 4 5 6 7 8 9 10 11` |
| 12 | 12 | `1 2 3 4 5 6 7 8 9 10 11 12` |
| 13 | 14 | `1 2 3 4 5 6 7 8 9 10 11 12 14` |

The interesting transition is from `12` to `14`. The number `13` cannot be generated by multiplying an earlier sequence element by one of `2`, `3`, `5`, `7`, or `11`, because `13` itself is a forbidden prime factor. The next available candidate is `14 = 2 * 7`.

For Sample 2, the first sixteen elements are skipped, so the first requested value is `a_17 = 20`. The relevant part of the generated sequence is:

| Sequence index | Generated value | Requested position |
| --- | --- | --- |
| 17 | 20 | 1 |
| 18 | 21 | 2 |
| 19 | 22 | 3 |
| 20 | 24 | 4 |
| 21 | 25 | 5 |
| 22 | 27 | 6 |
| 23 | 28 | 7 |
| 24 | 30 | 8 |
| 25 | 32 | 9 |
| 26 | 33 | 10 |
| 27 | 35 | 11 |
| 28 | 36 | 12 |
| 29 | 40 | 13 |
| 30 | 42 | 14 |
| 31 | 44 | 15 |
| 32 | 45 | 16 |

For example, after `36`, the next candidates include `40 = 2 * 20`, `42 = 2 * 21` or `3 * 14`, and larger values from the other generators. The minimum is `40`, so it becomes the next sequence element. The duplicate representation of `42` also illustrates why all pointers whose candidate equals the selected minimum must advance together.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n+k)` | Five constant-time candidates are evaluated for each generated element, and all five pointers only move forward. |
| Space | `O(n+k)` | The generated sequence contains exactly `n+k` values, plus five pointers. |

The maximum required sequence length is only 200000, so the optimal algorithm performs a small constant amount of work per required element. It does not depend on how large the 200000th value itself is, which is the property that makes it suitable for the constraints.

## Test Cases

```python
import sys
import io
import heapq

input = sys.stdin.readline

def get_terms(n, k):
    total = n + k
    primes = (2, 3, 5, 7, 11)

    dp = [1]
    ptr = [0] * 5

    while len(dp) < total:
        candidates = [
            dp[ptr[i]] * primes[i]
            for i in range(5)
        ]

        nxt = min(candidates)
        dp.append(nxt)

        for i in range(5):
            if candidates[i] == nxt:
                ptr[i] += 1

    return dp[n:n + k]

def solve():
    n, k = map(int, input().split())
    print(*get_terms(n, k))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def reference_heap(count):
    primes = (2, 3, 5, 7, 11)
    heap = [1]
    seen = {1}
    result = []

    while len(result) < count:
        x = heapq.heappop(heap)
        result.append(x)

        for p in primes:
            y = x * p
            if y not in seen:
                seen.add(y)
                heapq.heappush(heap, y)

    return result

# Provided samples
assert run("0 13") == (
    "1 2 3 4 5 6 7 8 9 10 11 12 14"
), "sample 1"

assert run("16 16") == (
    "20 21 22 24 25 27 28 30 32 33 35 36 40 42 44 45"
), "sample 2"

# Minimum input
assert run("0 1") == "1", "must include 1"

# Consecutive early values
assert run("1 5") == "2 3 4 5 6", "basic indexing"

# Equal candidate products: 6 can be produced as 2*3 and 3*2
assert run("5 1") == "6", "duplicate candidate handling"

# Boundary around 12, 14 and 15
assert run("12 5") == "14 15 16 18 20", "off-by-one boundary"

# Maximum-size input
expected = reference_heap(200000)[199999]
assert run("199999 1") == str(expected), "maximum n+k boundary"

# Large output length
answer = run("190000 10000").split()
assert len(answer) == 10000, "maximum k"
assert all(int(answer[i]) < int(answer[i + 1])
           for i in range(len(answer) - 1)), "strictly increasing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 1` | `1` | The sequence starts with `1`. |
| `1 5` | `2 3 4 5 6` | Basic one-based to zero-based indexing. |
| `5 1` | `6` | Multiple generators producing the same value. |
| `12 5` | `14 15 16 18 20` | The missing prime `13` and an indexing boundary. |
| `199999 1` | The independently generated 200000th value | Maximum allowed `n+k`. |
| `190000 10000` | 10000 increasing values | Maximum `k` and output length. |

The maximum-size assertion uses a heap-based reference implementation rather than the pointer algorithm itself. That gives the test a structurally different way to generate the expected value and makes the boundary check more useful.

## Edge Cases

For input `0 1`, the algorithm initializes `dp` with `[1]`. Since the requested total is already one, the generation loop does not run, and `dp[0:1]` gives `1`. This catches implementations that accidentally start generation from `2`.

For input `5 1`, the first five values are `1, 2, 3, 4, 5`. The current candidates for the next value include `2 * 3 = 6` and `3 * 2 = 6`. The minimum is `6`, and both the `2` pointer and the `3` pointer are advanced. On the next iteration neither generator proposes `6` again, so the output is exactly `6`. This is the central duplicate-handling case.

For input `12 1`, the generated prefix is `1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12`. The next candidates contain `14 = 2 * 7`, while `13` has no valid construction because `13` is not one of the allowed prime factors. The algorithm appends `14` and outputs it. This catches both the missing-prime boundary and an off-by-one error in selecting `a_{n+1}`.

For input `199999 1`, the algorithm generates exactly 200000 elements and then returns the element at zero-based index `199999`. It does not generate an unnecessary 200001st value. This exercises the upper boundary of `n+k` and confirms that the implementation scales with the number of required sequence elements rather than with the numerical magnitude of the final answer.
