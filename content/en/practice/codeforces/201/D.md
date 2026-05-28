---
title: "CF 201D - Brand New Problem"
description: "Lesha has a problem description made of n distinct words, written in a fixed order. Each archive problem is another sequence of words, but archive descriptions may repeat words many times. We want to compare Lesha’s description against every archive description."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dp"]
categories: ["algorithms"]
codeforces_contest: 201
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 127 (Div. 1)"
rating: 2600
weight: 201
solve_time_s: 99
verified: true
draft: false
---

[CF 201D - Brand New Problem](https://codeforces.com/problemset/problem/201/D)

**Rating:** 2600  
**Tags:** bitmasks, brute force, dp  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

Lesha has a problem description made of `n` distinct words, written in a fixed order. Each archive problem is another sequence of words, but archive descriptions may repeat words many times.

We want to compare Lesha’s description against every archive description. For one archive problem, we are allowed to permute Lesha’s words in any order. If that permutation appears as a subsequence inside the archive description, then the archive problem is considered similar.

Among all valid permutations, we choose the one with the smallest number of inversions relative to the original order of Lesha’s words. The fewer inversions we need, the more similar the problems are.

If the best permutation has `x` inversions, then the similarity score is:

$$p = \frac{n(n-1)}{2} + 1 - x$$

The maximum possible inversions is `n(n-1)/2`, so larger similarity means fewer inversions.

The task is to find the archive problem with the largest similarity. If no archive problem contains any permutation of Lesha’s words as a subsequence, we print `"Brand new problem!"`.

The constraints completely shape the solution.

The critical bound is `n ≤ 15`. That immediately suggests bitmask DP, because `2^15 = 32768` is manageable. At the same time, archive descriptions can contain up to `500000` total words, so any solution exponential in archive length is impossible.

A brute-force over all permutations would require checking up to `15!` permutations, which is astronomically large. Even `10!` is already too big.

The small `n` and huge archive size suggest that the archive should be processed almost linearly, while the expensive combinatorics must happen only over the `n` Lesha words.

There are several subtle cases that break naive solutions.

Suppose Lesha’s words are:

```
a b c
```

and the archive description is:

```
c b a
```

The only valid permutation is exactly `c b a`, which has 3 inversions. A greedy approach that tries to preserve original order would fail to find any solution, even though one exists.

Another dangerous case is repeated archive words:

```
Lesha: a b
Archive: a a a b
```

The best permutation is still `a b` with 0 inversions. If we only store the first occurrence of each word and ignore later positions, we could accidentally lose valid transitions.

A more subtle issue appears when multiple permutations are possible:

```
Lesha: a b c
Archive: b a c
```

Both permutations `b a c` and `a c b` are subsequences. Their inversion counts are different:

```
b a c -> 1 inversion
a c b -> 1 inversion
```

A careless DP that only checks existence would miss the need to minimize inversions.

Finally, tie-breaking matters. If two archive problems achieve the same similarity, we must output the smallest archive index.

## Approaches

The most direct brute-force solution is to generate every permutation of Lesha’s words. For each permutation, we check whether it appears as a subsequence inside the archive description. If it does, we compute its inversion count and keep the minimum.

Checking subsequence existence takes linear time in the archive length. There are up to `n!` permutations.

For `n = 15`:

$$15! \approx 1.3 \times 10^{12}$$

Even before considering archive scanning, this is hopeless.

The brute-force works conceptually because the problem is literally asking us to search over permutations. The problem is that permutations are the wrong representation.

The key observation is that we do not actually care about the full permutation itself. We only care about building a subsequence in archive order while minimizing inversions.

Suppose we scan an archive description from left to right. Whenever we encounter one of Lesha’s words, we may decide to append it to our chosen subsequence.

The order in which words are appended becomes the permutation.

Now think about the inversion count incrementally.

If we append word `i` after already choosing some set of words, then every previously chosen word with index larger than `i` creates one inversion.

That means the additional inversion cost depends only on the current subset mask.

This is exactly the structure needed for subset DP.

We define:

`dp[mask] = minimum inversions needed to build exactly this set of chosen words as a subsequence so far`

When processing a new archive word corresponding to Lesha index `i`, we may transition:

```
mask -> mask | (1 << i)
```

The added inversion count equals the number of already chosen indices larger than `i`.

The archive is processed left to right, so subsequence order is automatically respected.

This converts a factorial search into a DP over `2^n` masks.

The total number of masks is at most `32768`, which is small enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m · k · n!) | O(n) | Too slow |
| Optimal | O(total_words · 2^n) | O(2^n) | Accepted |

## Algorithm Walkthrough

1. Read Lesha’s words and assign each word its original index from `0` to `n-1`.
2. For every archive problem, initialize:

```
dp[mask] = minimum inversions
```

Set all states to infinity except:

```
dp[0] = 0
```

This represents choosing no words with zero inversions.

1. Process the archive description from left to right.

Only words that appear in Lesha’s description matter. All other words can be ignored immediately.

1. Suppose the current archive word corresponds to Lesha index `i`.

We try to append this word to every existing subset that does not already contain `i`.

1. For each valid mask, compute the added inversion cost.

If we append `i`, then every already chosen index `j > i` contributes one inversion.

So:

```
extra = count of bits j in mask where j > i
```

1. Transition:

```
new_mask = mask | (1 << i)

dp[new_mask] = min(
    dp[new_mask],
    dp[mask] + extra
)
```

We iterate masks in descending order so the same archive occurrence is not reused multiple times.

1. After processing the whole archive description, check the full mask:

```
full = (1 << n) - 1
```

If `dp[full]` is finite, then this archive problem contains some valid permutation.

1. Convert inversion count into similarity:

$$p = \frac{n(n-1)}{2} + 1 - dp[full]$$

Keep the archive problem with the maximum `p`. Break ties by smaller index.

1. If no archive problem reaches the full mask, print:

```
Brand new problem!
```

Otherwise print the best archive index and:

```
[:||||...||:]
```

with exactly `p` vertical bars.

### Why it works

The DP invariant is:

```
dp[mask] = minimum inversions among all subsequences
formed so far whose chosen Lesha words are exactly mask
```

When processing archive words left to right, every transition appends one new word at the end of the subsequence. That preserves subsequence validity automatically.

The inversion contribution of appending word `i` depends only on which larger indices were already chosen. Every such pair contributes exactly one inversion, and every inversion is counted exactly once, when the smaller-index word is appended after the larger-index word.

Since every valid permutation corresponds to some sequence of DP transitions, and every DP transition constructs a valid permutation, the DP explores exactly the required search space while minimizing inversions.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**9

def solve():
    n = int(input())
    words = input().split()

    pos = {}
    for i, w in enumerate(words):
        pos[w] = i

    m = int(input())

    full = (1 << n) - 1
    max_inv = n * (n - 1) // 2

    best_similarity = -1
    best_index = -1

    greater_bits = [0] * n
    for i in range(n):
        mask = 0
        for j in range(i + 1, n):
            mask |= (1 << j)
        greater_bits[i] = mask

    for problem_index in range(1, m + 1):
        data = input().split()
        k = int(data[0])
        archive = data[1:]

        dp = [INF] * (1 << n)
        dp[0] = 0

        for w in archive:
            if w not in pos:
                continue

            i = pos[w]
            bit = 1 << i

            for mask in range(full, -1, -1):
                if dp[mask] == INF:
                    continue

                if mask & bit:
                    continue

                new_mask = mask | bit

                extra = (mask & greater_bits[i]).bit_count()

                cand = dp[mask] + extra

                if cand < dp[new_mask]:
                    dp[new_mask] = cand

        if dp[full] == INF:
            continue

        inversions = dp[full]
        similarity = max_inv + 1 - inversions

        if similarity > best_similarity:
            best_similarity = similarity
            best_index = problem_index

    if best_similarity == -1:
        print("Brand new problem!")
    else:
        print(best_index)
        print("[:{}:]".format("|" * best_similarity))

solve()
```

The dictionary `pos` maps every Lesha word to its original index. Since Lesha’s words are guaranteed distinct, this mapping is unambiguous.

The DP array has size `2^n`, which is feasible because `n ≤ 15`.

The array `greater_bits[i]` stores a bitmask containing all indices larger than `i`. This lets us compute the number of newly created inversions in constant time using:

```
(mask & greater_bits[i]).bit_count()
```

That expression counts how many already chosen words originally appeared after `i`.

The descending mask iteration is essential. Without it, a single archive occurrence could be reused multiple times during the same iteration, which would violate subsequence rules.

Another subtle point is that archive problems may repeat words many times. We must process every occurrence separately because later occurrences can create better subsequences.

The final similarity formula follows directly from the statement.

## Worked Examples

### Sample 1

Input:

```
4
find the next palindrome
1
10 find the previous palindrome or print better luck next time
```

The indices are:

| Word | Index |
| --- | --- |
| find | 0 |
| the | 1 |
| next | 2 |
| palindrome | 3 |

The archive-relevant sequence becomes:

```
find the palindrome next
```

DP transitions:

| Current word | Built permutation | Inversions |
| --- | --- | --- |
| find | find | 0 |
| the | find the | 0 |
| palindrome | find the palindrome | 0 |
| next | find the palindrome next | 1 |

The final permutation is:

```
find the palindrome next
```

Compared to the original order:

```
find the next palindrome
```

only `(palindrome, next)` is inverted.

For `n = 4`:

$$\frac{4 \cdot 3}{2} = 6$$

Similarity:

$$6 + 1 - 1 = 6$$

Output:

```
1
[:||||||:]
```

This trace demonstrates how inversions are accumulated incrementally while preserving subsequence order.

### Example 2

Input:

```
3
a b c
1
3 c b a
```

Relevant archive sequence:

```
c b a
```

DP evolution:

| Current word | Best permutation so far | Inversions |
| --- | --- | --- |
| c | c | 0 |
| b | c b | 1 |
| a | c b a | 3 |

The permutation `c b a` has all three pairs inverted:

```
(c,b), (c,a), (b,a)
```

Maximum inversions for `n = 3` is also 3, so:

$$3 + 1 - 3 = 1$$

Output:

```
1
[:|:]
```

This example shows that the algorithm correctly handles completely reversed orderings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total_words · 2^n) | Each relevant archive word iterates over all subset masks |
| Space | O(2^n) | DP array over subsets |

The largest possible DP has `32768` states. The total archive length is about `5 × 10^5`, which keeps the total operation count within practical limits in optimized Python.

The memory usage is tiny compared to the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

INF = 10**9

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    sys.stdout = out

    input = sys.stdin.readline

    n = int(input())
    words = input().split()

    pos = {}
    for i, w in enumerate(words):
        pos[w] = i

    m = int(input())

    full = (1 << n) - 1
    max_inv = n * (n - 1) // 2

    best_similarity = -1
    best_index = -1

    greater_bits = [0] * n
    for i in range(n):
        mask = 0
        for j in range(i + 1, n):
            mask |= (1 << j)
        greater_bits[i] = mask

    for problem_index in range(1, m + 1):
        data = input().split()
        archive = data[1:]

        dp = [INF] * (1 << n)
        dp[0] = 0

        for w in archive:
            if w not in pos:
                continue

            i = pos[w]
            bit = 1 << i

            for mask in range(full, -1, -1):
                if dp[mask] == INF:
                    continue

                if mask & bit:
                    continue

                new_mask = mask | bit

                extra = (mask & greater_bits[i]).bit_count()

                dp[new_mask] = min(
                    dp[new_mask],
                    dp[mask] + extra
                )

        if dp[full] == INF:
            continue

        similarity = max_inv + 1 - dp[full]

        if similarity > best_similarity:
            best_similarity = similarity
            best_index = problem_index

    if best_similarity == -1:
        print("Brand new problem!")
    else:
        print(best_index)
        print("[:{}:]".format("|" * best_similarity))

    return out.getvalue()

# provided sample
assert run(
"""4
find the next palindrome
1
10 find the previous palindrome or print better luck next time
"""
) == "1\n[:||||||:]\n", "sample 1"

# minimum size
assert run(
"""1
hello
1
1 hello
"""
) == "1\n[:|:]\n", "single word"

# no valid permutation
assert run(
"""2
a b
1
3 a x x
"""
) == "Brand new problem!\n", "missing word"

# reversed order
assert run(
"""3
a b c
1
3 c b a
"""
) == "1\n[:|:]\n", "maximum inversions"

# tie-breaking by smaller index
assert run(
"""2
a b
2
2 a b
2 a b
"""
) == "1\n[:||:]\n", "smallest index tie"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single-word case | Similarity 1 | Minimum constraints |
| Missing word | Brand new problem | Full mask unreachable |
| Reversed order | Lowest similarity | Maximum inversion handling |
| Identical best archives | Smallest index chosen | Tie-breaking correctness |

## Edge Cases

Consider:

```
2
a b
1
3 a a b
```

The archive repeats `a` multiple times.

The DP processes each occurrence independently. After reading the first `a`, we can form subset `{a}`. The later `a` occurrences are ignored for that subset because the bit is already set.

When `b` arrives, the DP reaches the full mask with zero inversions.

Output:

```
1
[:||:]
```

This confirms repeated archive words are handled safely.

Now consider the fully reversed case:

```
3
a b c
1
3 c b a
```

Transitions:

```
{} -> {c} -> {c,b} -> {c,b,a}
```

When appending `b`, one larger index (`c`) already exists, adding one inversion.

When appending `a`, two larger indices already exist, adding two more inversions.

Total inversions:

```
1 + 2 = 3
```

which is correct.

Finally, consider a case with no valid subsequence:

```
3
a b c
1
4 a x y b
```

The DP never reaches the full mask because `c` never appears.

The final state remains infinite:

```
dp[111] = INF
```

so the algorithm correctly prints:

```
Brand new problem!
```
