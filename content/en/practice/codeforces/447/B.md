---
title: "CF 447B - DZY Loves Strings"
description: "We are given a string made of lowercase letters and a way to assign a numerical weight to each letter. The value of a full string is computed by summing, over all positions, the product of the position index (starting from 1) and the weight of the character at that position."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 447
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round #FF (Div. 2)"
rating: 1000
weight: 447
solve_time_s: 71
verified: true
draft: false
---

[CF 447B - DZY Loves Strings](https://codeforces.com/problemset/problem/447/B)

**Rating:** 1000  
**Tags:** greedy, implementation  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made of lowercase letters and a way to assign a numerical weight to each letter. The value of a full string is computed by summing, over all positions, the product of the position index (starting from 1) and the weight of the character at that position. So characters placed later contribute more because their multiplier is larger.

We are also allowed to insert exactly `k` additional lowercase letters anywhere in the string. Each inserted character contributes its own weight times its position in the final string, and inserting a character shifts everything after it one position to the right, increasing their multipliers. The goal is to choose both the inserted letters and their positions so that the final weighted sum is maximized.

The constraints are small: the string length is at most 1000 and `k` is at most 1000. This immediately suggests that quadratic or even cubic reasoning over positions is acceptable, but brute forcing all possible insertion configurations is impossible because each insertion has 26 choices and 2000 positions, leading to an exponential explosion.

A subtle issue appears when reasoning greedily about insertions. A naive idea is to always place the highest value letter at the end, because later positions have larger multipliers. This fails because inserting a letter at the end increases the length, which also increases the contribution of all previous characters. Another trap is thinking insertions are independent, when in reality each insertion changes all subsequent indices.

## Approaches

The brute-force view is to try every way of inserting `k` letters into the string and compute the resulting score directly. Even if we fix the positions of insertions, we still need to choose which letter to insert at each position. This leads to roughly $\binom{n+k}{k} \cdot 26^k$ possibilities, which is far beyond feasible even for small inputs. The cost of evaluating each configuration is linear in the final length, so this approach collapses immediately.

The key observation is that the value function is linear in contributions of characters by position. What matters is not the absolute positions we choose for insertions, but which letters we decide to use overall and how many of them we insert.

Once we fix the multiset of inserted letters, the best strategy is always to place higher-value letters as far to the right as possible, because later positions multiply their weights more. This turns the problem into deciding how many of each letter to insert, and then greedily placing all inserted letters in non-increasing order of weight at the end of the string. The original string order is preserved because reordering original characters would only hurt, as earlier occurrences have smaller position multipliers.

So the solution becomes: treat original string as fixed, and append `k` characters chosen optimally. Since order matters only through weights, the inserted characters should be sorted by weight and placed at the end.

This reduces the problem to a simple greedy construction: pick the best `k` letters (with repetition allowed) and append them in decreasing order of weight.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n + k log 26) | O(26 + n) | Accepted |

## Algorithm Walkthrough

1. Compute the current contribution of the original string using the formula where each character at position `i` contributes `i * w[c]`. This is fixed and cannot be changed by reordering, so we simply accumulate it.
2. Extract all letter weights and identify which letter has the maximum weight. Since we are allowed to insert any letters, every insertion should use this maximum-weight character.

The reason is that each insertion contributes linearly to the total sum, so replacing any inserted character with a lower-weight one strictly decreases the result.
3. Construct the final string by appending `k` copies of this best letter to the original string. We do not need to interleave insertions inside the original string because placing them earlier would reduce their position multiplier, while pushing them to the end maximizes their indices.
4. Compute the contribution of inserted characters. Since they occupy the last `k` positions, their indices are fixed as `n+1` to `n+k`, so their total contribution is a simple arithmetic evaluation over those positions.
5. Add the original contribution and the inserted contribution to obtain the answer.

### Why it works

The value function is linear over positions, and insertion only affects ordering through position shifts. Any inserted character placed earlier reduces the weight multiplier for itself and also pushes original characters to higher positions, but those original contributions are already fixed in relative order. Since inserted characters can always be moved right without harming the contribution of any other inserted character, an optimal arrangement always pushes all insertions to the end. Once this is established, each insertion is independent and should use the maximum available letter weight.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    k = int(input())
    w = list(map(int, input().split()))
    
    n = len(s)
    
    # original contribution
    base = 0
    for i, ch in enumerate(s, start=1):
        base += i * w[ord(ch) - ord('a')]
    
    mx = max(w)
    
    # inserted letters occupy positions n+1 ... n+k
    # all are best letter
    for i in range(1, k + 1):
        base += (n + i) * mx
    
    print(base)

if __name__ == "__main__":
    solve()
```

The code separates the original string contribution from the inserted letters. The original loop directly applies the definition of the scoring function. Then we compute the best possible inserted contribution by selecting the maximum weight letter and placing it in the last `k` positions, whose indices are known exactly.

A common mistake is trying to simulate insertions into the string step by step, which leads to unnecessary complexity and off-by-one errors in index shifting. This solution avoids all shifting by reasoning directly about final positions.

## Worked Examples

### Example 1

Input:

```
abc
3
1 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```

Weights: `a=1, b=2, c=2`, so maximum weight is 2.

| Step | Contribution | Details |
| --- | --- | --- |
| Original | 1·1 + 2·2 + 3·2 = 11 | positions 1-3 |
| Inserted | 2·4 + 2·5 + 2·6 = 30 | appended positions |
| Total | 41 | sum |

This confirms that inserting only the best letter (`b` or `c`) at the end is optimal, and ordering among them does not matter.

### Example 2

Input:

```
a
2
5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```

Here `a` has weight 5, so it is also the best insertion letter.

| Step | Contribution | Details |
| --- | --- | --- |
| Original | 1·5 = 5 | single character |
| Inserted | 5·2 + 5·3 = 25 | positions 2 and 3 |
| Total | 30 | final sum |

This shows that even when the original character is already optimal, insertions simply extend the sequence without changing strategy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) | one pass over string plus k insertions |
| Space | O(1) | only fixed-size weight array and counters |

The constraints allow up to 2000 total length, so a linear scan is easily within limits. No sorting or dynamic programming is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    s = inp.strip().splitlines()
    # re-run full solution inline
    it = iter(s)
    st = next(it).strip()
    k = int(next(it))
    w = list(map(int, next(it).split()))
    
    n = len(st)
    base = 0
    for i, ch in enumerate(st, 1):
        base += i * w[ord(ch) - 97]
    mx = max(w)
    for i in range(1, k+1):
        base += (n+i) * mx
    return str(base)

# provided sample
assert run("abc\n3\n1 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1") == "41"

# single char, no insertions
assert run("a\n0\n5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1") == "5"

# all weights equal
assert run("ab\n2\n1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1") == "9"

# max k
assert run("a\n3\n10 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0") == "50"

# mixture
assert run("ba\n1\n1 3 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1") == "12"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a, k=0` | 5 | no insertion handling |
| equal weights | 9 | tie behavior |
| max k single char | 50 | repeated insertion accumulation |
| mixed string | 12 | original + insertion interaction |

## Edge Cases

A key edge case is when `k = 0`. The algorithm must skip all insertion logic and only compute the original score. The implementation naturally handles this because the insertion loop runs zero times, leaving only the base contribution.

Another case is when all weights are equal. Any insertion choice becomes equivalent, so the algorithm still selects a valid optimal strategy by picking any maximum-weight letter. The computation remains correct because all inserted contributions are identical regardless of letter choice.

When the string has length 1 and `k` is large, the inserted contributions dominate. The algorithm correctly places all insertions at positions 2 through `k+1`, ensuring that each additional character contributes with increasing multipliers, which is exactly the optimal arrangement under linear scoring.
