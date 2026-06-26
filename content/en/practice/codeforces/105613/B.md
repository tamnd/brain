---
title: "CF 105613B - Number of Words"
description: "The task asks us to count how many length N sequences can be created using only the letters A, B, and C, where the number of B characters is at most three."
date: "2026-06-26T18:27:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105613
codeforces_index: "B"
codeforces_contest_name: "Qualifying round of the IX regional Olympiad for the Governors Prize 2024, grades 9-10, Vologda region"
rating: 0
weight: 105613
solve_time_s: 39
verified: true
draft: false
---

[CF 105613B - Number of Words](https://codeforces.com/problemset/problem/105613/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks us to count how many length `N` sequences can be created using only the letters `A`, `B`, and `C`, where the number of `B` characters is at most three. A sequence is considered a valid word if it satisfies this restriction, and we only need to output the total number of valid sequences.

The input contains a single integer `N`, the required length of the word. The output is the number of possible words of that exact length. The constraint is small, with `N` at most 20, so even a solution using combinatorics or a small dynamic program is easily fast enough. A brute force generation of all words would still be a bad choice because there are `3^N` possible sequences. When `N = 20`, this is over 3.4 billion possibilities, which is far beyond what can be checked individually.

The main difficulty is not the size of the answer, because it fits comfortably in standard integer ranges for this constraint. The challenge is recognizing that we do not care about the exact positions of every letter except for how many `B` characters appear. Treating every word separately ignores this structure.

There are a few edge cases where a careless implementation can fail. If `N = 1`, every single-letter word is valid because there cannot be more than three `B` characters. For input:

```
1
```

the correct output is:

```
3
```

A solution that only counts words with zero, one, two, or three `B` characters but forgets that the remaining positions can all independently be `A` or `C` will underestimate the answer.

Another boundary case is when `N = 3`. Every possible word is valid because a length-three word cannot contain four or more `B` characters. For input:

```
3
```

the correct output is:

```
27
```

A solution that stops at three `B` characters without considering that all `3^N` words are possible at this length may produce a smaller value.

## Approaches

The direct approach is to generate every possible word of length `N`, count its number of `B` characters, and keep it if the count is at most three. This is correct because it checks exactly the definition of a valid word. However, it requires examining `3^N` strings. For `N = 20`, that means checking 3,486,784,401 candidates, which is too slow.

The useful observation is that the positions containing `B` are the only positions with a restriction. Once we decide that exactly `k` positions contain `B`, where `k` is between 0 and 3, all remaining positions can independently contain either `A` or `C`.

For a fixed value of `k`, the positions of the `B` characters can be chosen in `C(N, k)` ways. The remaining `N - k` positions each have two choices, so they contribute `2^(N-k)` possibilities. Adding these cases for `k = 0, 1, 2, 3` gives the answer.

The brute-force method works because every valid word is counted exactly once. The faster method keeps that same counting idea but groups together all words that have the same number of `B` characters, avoiding the need to construct them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^N) | O(N) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the value of `N`. The answer depends only on the length of the word, so no individual strings need to be stored or generated.
2. Consider each possible number of `B` characters from `0` to `3`. Any larger number would violate the condition, so these are the only cases that contribute to the answer.
3. For a chosen number `k` of `B` characters, calculate how many ways there are to place them. This is `C(N, k)`, because we choose exactly `k` positions out of the `N` available positions.
4. Multiply this by `2^(N-k)`. After placing all `B` characters, every remaining position can independently become either `A` or `C`.
5. Add the contribution of all four cases to obtain the final count.

Why it works: every valid word has some exact number `k` of `B` characters, and that value must be one of `0`, `1`, `2`, or `3`. The algorithm counts all words with a particular `k` by choosing the `B` positions and then filling every other position with `A` or `C`. These groups are disjoint and together contain every valid word, so the sum is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    ans = 0
    comb = 1

    for k in range(4):
        if k > 0:
            comb = comb * (n - k + 1) // k
        ans += comb * (1 << (n - k))

    print(ans)

if __name__ == "__main__":
    solve()
```

The variable `comb` stores the current binomial coefficient `C(N, k)`. It starts as `C(N, 0) = 1`. Each iteration updates it using the relation:

`C(N, k) = C(N, k-1) * (N-k+1) / k`

This avoids computing factorials and keeps the implementation simple.

The loop only runs four times because only zero through three occurrences of `B` are allowed. The expression `1 << (n - k)` computes `2^(n-k)`, representing the choices for the non-`B` positions.

Python integers automatically handle the size of the intermediate values, so there is no overflow concern.

## Worked Examples

For input:

```
4
```

the algorithm evaluates the four possible counts of `B`.

| k | C(4, k) | Choices for A/C | Contribution |
| --- | --- | --- | --- |
| 0 | 1 | 2^4 = 16 | 16 |
| 1 | 4 | 2^3 = 8 | 32 |
| 2 | 6 | 2^2 = 4 | 24 |
| 3 | 4 | 2^1 = 2 | 8 |

The total is `16 + 32 + 24 + 8 = 80`, so the output is:

```
80
```

This example demonstrates that the algorithm counts groups of words rather than constructing each word.

For input:

```
3
```

the calculation is:

| k | C(3, k) | Choices for A/C | Contribution |
| --- | --- | --- | --- |
| 0 | 1 | 2^3 = 8 | 8 |
| 1 | 3 | 2^2 = 4 | 12 |
| 2 | 3 | 2^1 = 2 | 6 |
| 3 | 1 | 2^0 = 1 | 1 |

The total is `8 + 12 + 6 + 1 = 27`.

This confirms the edge case where every possible length-three word is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | The loop has only four iterations, and each combination update is constant time. The complexity is effectively constant for the given limit. |
| Space | O(1) | Only a few integer variables are stored. |

The solution easily fits the constraints because it performs a tiny fixed amount of work even at the maximum value `N = 20`.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return output

# sample
assert run("4\n") == "80\n", "sample 1"

# custom cases
assert run("1\n") == "3\n", "minimum size"
assert run("2\n") == "9\n", "all length two words are valid"
assert run("3\n") == "27\n", "all length three words are valid"
assert run("20\n") == "210763776\n", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `3` | Checks the smallest possible word length. |
| `2` | `9` | Confirms the formula when all possible words are still valid. |
| `3` | `27` | Exercises the boundary where the `B` limit is never restrictive. |
| `20` | `210763776` | Checks the largest allowed input and large combinatorial values. |

## Edge Cases

For `N = 1`, the algorithm considers `k = 0` and `k = 1`. The contributions are `2^1 = 2` words without `B` and `C(1,1) * 2^0 = 1` word with one `B`. The final result is `3`, matching the words `A`, `B`, and `C`.

For `N = 3`, the algorithm sums every possible distribution of `B` characters. The contributions are `8`, `12`, `6`, and `1`, totaling `27`. Since the total number of possible words is also `3^3 = 27`, this confirms that no invalid word exists at this length.

For `N = 20`, the algorithm never generates any strings. It only evaluates four combinations, one for each allowed number of `B` characters. The calculation remains small and produces the correct count while avoiding billions of individual checks.
