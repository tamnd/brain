---
title: "CF 105690D - Lion Dancers"
description: "The corridor is a sequence of columns. Column i contains ki platforms stacked vertically, and all n dancers must stand on distinct platforms in that column."
date: "2026-06-26T09:03:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105690
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 1-29-25 Div. 1 (Advanced)"
rating: 0
weight: 105690
solve_time_s: 40
verified: true
draft: false
---

[CF 105690D - Lion Dancers](https://codeforces.com/problemset/problem/105690/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

The corridor is a sequence of columns. Column `i` contains `k_i` platforms stacked vertically, and all `n` dancers must stand on distinct platforms in that column. The dancers are ordered by height, so dancer `1` must always be the lowest occupied platform and dancer `n` must always be the highest occupied platform. The task is to count how many complete performances are possible, where a performance is the choice of dancer positions in every column.

For a single column with `k_i` platforms, the only real decision is which `n` platform positions are occupied. Once those positions are chosen, the ordering rule automatically assigns the lowest chosen position to dancer `1`, the next one to dancer `2`, and so on. The number of possibilities for that column is the number of ways to choose `n` positions from `k_i`, which is the binomial coefficient `C(k_i, n)`.

The columns do not affect each other. The dancers only need to preserve their order inside each column, and there is no restriction connecting the chosen platforms in one column to the chosen platforms in the next column. The total number of performances is the product of the number of choices for every column.

The constraints are designed around this observation. The number of columns can reach `100000`, while `n` is at most `100`. A solution that tries to enumerate dancer positions or simulate all possible arrangements is impossible because even a single column can have an enormous number of valid states. We need an approach where each column is processed in constant or very small time. Since `n` is small, computing combinations with a short loop is sufficient.

Several edge cases can break a careless implementation. When `n = 1`, each column contributes exactly `k_i` possibilities because the single dancer can stand anywhere. For example:

```
Input:
1 3
2 5 4

Output:
40
```

A solution that treats the ordering rule as requiring a special arrangement might incorrectly output something smaller, but the answer is simply `2 * 5 * 4`.

When a column has exactly `n` platforms, every platform must be used and that column contributes only one choice. For example:

```
Input:
3 2
3 5

Output:
10
```

The first column contributes `C(3,3) = 1`, while the second contributes `C(5,3) = 10`. Forgetting this case can lead to an unnecessary subtraction or incorrect assumption that there are always multiple choices.

Large values also require care. A column can have `100000` platforms, so factorials up to `100000` can be used, but only if the modular inverse calculation is handled correctly. Since `n` is only `100`, computing each combination with a product of at most `100` terms avoids unnecessary complexity.

## Approaches

The direct brute force approach is to generate every possible set of `n` occupied platforms for each column, then combine those choices across columns. This is correct because every valid performance is exactly one selection of platforms per column. However, the number of choices in one column is already `C(k_i, n)`. With `k_i = 100000` and `n = 50`, this number is far beyond anything that can be enumerated. The brute force approach would need to process an astronomical number of states.

The key observation is that the identity of the dancers does not add extra choices. Once a set of platforms is selected, the ordering rule forces the assignment. A column with `k_i` platforms contributes only a combination value, not a permutation value.

This turns the whole problem into multiplying independent contributions. Because `n` is small, we can compute `C(k_i, n)` directly as:

`k_i * (k_i - 1) * ... * (k_i - n + 1) / n!`

The division must be performed modulo `1e9 + 7`, so we precompute the modular inverse of `n!` and multiply every column contribution by it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(product of C(k_i, n)) | O(product of C(k_i, n)) | Too slow |
| Optimal | O(m * n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and the heights of all columns. The answer is built by considering one column at a time because each column choice is independent.
2. Compute `n!` modulo `1e9 + 7` and find its modular inverse using fast exponentiation. Every combination calculation needs division by `n!`, and modular inverses provide the equivalent operation under modulo arithmetic.
3. For every column height `k_i`, compute the number of ways to choose the occupied platforms. Start with `1` and multiply by the `n` consecutive values from `k_i - n + 1` through `k_i`. Then multiply by the inverse of `n!`.
4. Multiply this column contribution into the global answer modulo `1e9 + 7`. Multiplication is valid because choosing platforms in one column never restricts choices in another column.
5. Print the final product.

Why it works: For every column, the algorithm counts exactly the possible sets of occupied platforms. The ordering condition does not create additional possibilities because each chosen set has exactly one assignment of dancers from lowest platform to highest platform. Since a full performance consists of independently choosing one valid state for every column, the multiplication rule gives the exact number of performances.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def mod_pow(a, b):
    res = 1
    while b:
        if b & 1:
            res = res * a % MOD
        a = a * a % MOD
        b >>= 1
    return res

def solve():
    n, m = map(int, input().split())
    k = list(map(int, input().split()))

    fact = 1
    for i in range(1, n + 1):
        fact = fact * i % MOD

    inv_fact = mod_pow(fact, MOD - 2)

    ans = 1
    for height in k:
        cur = 1
        for x in range(n):
            cur = cur * (height - x) % MOD
        cur = cur * inv_fact % MOD
        ans = ans * cur % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The factorial computation only goes up to `n`, not the maximum column height. This is intentional because `n` is the number of selected platforms, and the formula only needs the denominator `n!`.

The modular inverse is computed with Fermat's little theorem because `1e9 + 7` is prime. The exponent `MOD - 2` gives the inverse of `n!` under modulo arithmetic.

For each column, the loop multiplies exactly `n` values. The first value is `height`, the next is `height - 1`, and so on. This directly constructs the numerator of the combination formula. The range stops after `n` values, so there are no off by one errors.

Python integers do not overflow, but every multiplication is reduced modulo `MOD` immediately to keep the values small and match the required arithmetic.

## Worked Examples

### Sample 1

Input:

```
2 3
2 3 2
```

| Column | Height | Product for numerator | Combination | Answer so far |
| --- | --- | --- | --- | --- |
| Start |  |  |  | 1 |
| 1 | 2 | 2 × 1 | 1 | 1 |
| 2 | 3 | 3 × 2 | 3 | 3 |
| 3 | 2 | 2 × 1 | 1 | 3 |

The middle column has three possible pairs of platforms. The other columns force both dancers to use all available platforms, so they contribute one possibility each.

### Sample 2

Input:

```
1 5
3 2 1 4 2
```

| Column | Height | Numerator | Combination | Answer so far |
| --- | --- | --- | --- | --- |
| Start |  |  |  | 1 |
| 1 | 3 | 3 | 3 | 3 |
| 2 | 2 | 2 | 2 | 6 |
| 3 | 1 | 1 | 1 | 6 |
| 4 | 4 | 4 | 4 | 24 |
| 5 | 2 | 2 | 2 | 48 |

With one dancer, choosing a platform is the only decision, so every column contributes its full height.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * n) | Each of the `m` columns requires `n` multiplications to compute its combination. |
| Space | O(n) | Only a few variables and the inverse factorial are stored. |

The maximum values are `m = 100000` and `n = 100`, giving about ten million simple operations. This fits comfortably within the time limit, while storing only constant extra data keeps memory usage minimal.

## Test Cases

```python
import sys
import io

MOD = 10 ** 9 + 7

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

def mod_pow(a, b):
    res = 1
    while b:
        if b & 1:
            res = res * a % MOD
        a = a * a % MOD
        b >>= 1
    return res

def solve():
    n, m = map(int, sys.stdin.readline().split())
    k = list(map(int, sys.stdin.readline().split()))

    fact = 1
    for i in range(1, n + 1):
        fact = fact * i % MOD

    inv_fact = mod_pow(fact, MOD - 2)

    ans = 1
    for height in k:
        cur = 1
        for x in range(n):
            cur = cur * (height - x) % MOD
        cur = cur * inv_fact % MOD
        ans = ans * cur % MOD

    print(ans)

assert run("""2 3
2 3 2
""") == "3\n", "sample 1"

assert run("""1 5
3 2 1 4 2
""") == "48\n", "sample 2"

assert run("""3 2
3 5
""") == "10\n", "exactly n platforms in first column"

assert run("""1 3
2 5 4
""") == "40\n", "single dancer"

assert run("""2 4
2 2 2 2
""") == "1\n", "all columns forced"

assert run("""100 1
100
""") == "1\n", "maximum n with minimum column height"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3 / 2 3 2` | `3` | Provided sample and normal combination multiplication |
| `1 5 / 3 2 1 4 2` | `48` | Single dancer behavior |
| `3 2 / 3 5` | `10` | A column with exactly `n` platforms |
| `2 4 / 2 2 2 2` | `1` | All columns having only one possible arrangement |
| `100 1 / 100` | `1` | Large `n` boundary |

## Edge Cases

When there is only one dancer, the combination formula becomes `C(k_i, 1) = k_i`. For the input:

```
1 3
2 5 4
```

the algorithm computes column contributions `2`, `5`, and `4`. The product is `40`, matching the fact that the dancer independently chooses one platform in each column.

When a column has exactly as many platforms as dancers, every platform must be occupied. For:

```
3 2
3 5
```

the first column gives `C(3, 3) = 1`. The second gives `C(5, 3) = 10`. The algorithm multiplies these values and returns `10`.

When every column has height equal to `n`, every movement is forced. For:

```
2 4
2 2 2 2
```

each column contributes `C(2, 2) = 1`, so the final answer remains `1`. This confirms that the algorithm does not accidentally count different dancer assignments as separate performances.
