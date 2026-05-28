---
title: "CF 202B - Brand New Easy Problem"
description: "We are given the title words of Lesha's new problem and several archive problems from Torcoder. The words in Lesha's title are all distinct. An archive title may repeat words."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 202
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 127 (Div. 2)"
rating: 1700
weight: 202
solve_time_s: 209
verified: true
draft: false
---

[CF 202B - Brand New Easy Problem](https://codeforces.com/problemset/problem/202/B)

**Rating:** 1700  
**Tags:** brute force  
**Solve time:** 3m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the title words of Lesha's new problem and several archive problems from Torcoder. The words in Lesha's title are all distinct. An archive title may repeat words.

For every archive problem, we want to know whether we can find all words from Lesha's title inside it as a subsequence, possibly in a different order. Among all valid orders, we choose the one with the minimum number of inversions compared to the original order of Lesha's title.

An inversion means two words swapped relative to the original order. If Lesha's title is:

```
find the next palindrome
```

then the permutation:

```
find the palindrome next
```

has one inversion because `palindrome` moved before `next`.

If the best permutation for some archive problem has `x` inversions and Lesha's title has `n` words, the similarity score is:

```
p = n * (n - 1) / 2 - x
```

The maximum possible value appears when there are zero inversions, meaning the archive already contains the words in the original order.

We must find the archive problem with the largest similarity. If no archive problem contains any permutation of all words, we print `"Brand new problem!"`.

The constraints completely shape the solution. Lesha's title contains at most 4 words. That is tiny. The number of permutations is at most:

```
4! = 24
```

Each archive description contains at most 20 words, and there are at most 10 archive problems. Even a brute-force check over all permutations is trivial here.

The dangerous part is not performance, it is correctness.

One easy mistake is forgetting that the archive may contain repeated words. Suppose Lesha's title is:

```
a b
```

and an archive title is:

```
a a a
```

The word `b` never appears, so no permutation works. A careless subsequence matcher that only checks lengths or partial matches would incorrectly accept it.

Another subtle case is choosing the wrong permutation when multiple permutations appear as subsequences. We must minimize inversions, not maximize subsequence flexibility.

Example:

```
Lesha: a b c
Archive: b a c
```

Both permutations `b a c` and `a c b` are subsequences. Their inversion counts are different:

| Permutation | Inversions |
| --- | --- |
| b a c | 1 |
| a c b | 1 |

Here they tie, but in larger cases the minimum matters because similarity depends directly on inversions.

Another common bug is mishandling ties between archive problems. If two problems achieve the same similarity, we must output the smallest index.

Example:

```
Lesha: a b
Archive 1: b a
Archive 2: b a
```

Both have the same score, so the answer must be archive `1`.

## Approaches

The most direct approach is to generate every permutation of Lesha's words. Since `n ≤ 4`, there are at most 24 permutations. For every archive problem, we check which permutations appear as subsequences. Among those, we compute the inversion count and keep the minimum.

Checking whether a sequence is a subsequence is linear in the archive length. The archive contains at most 20 words, so one check costs at most 20 comparisons.

The total work is tiny:

```
10 archive problems × 24 permutations × 20 checks
```

That is only a few thousand operations.

A more naive brute-force would try every subset of archive positions and compare the resulting sequences. For an archive of length 20 and `n = 4`, that means checking:

```
C(20,4) = 4845
```

position combinations per archive problem. Even that still fits easily, but it complicates the implementation because we would need to reconstruct permutations from chosen positions.

The key observation is that `n` is extremely small. Since the number of possible orderings is bounded by 24, we can directly enumerate all candidate permutations and test them independently. The problem becomes a clean combination of permutation generation, subsequence matching, and inversion counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over archive position subsets | O(m × C(k,n) × n) | O(n) | Accepted |
| Enumerate all permutations | O(m × n! × k) | O(n!) | Accepted |

Here `k ≤ 20` and `n ≤ 4`.

## Algorithm Walkthrough

1. Read Lesha's words into an array `base`.
2. Generate all permutations of `base`.

Since `n ≤ 4`, this produces at most 24 sequences.
3. For every permutation, compute its inversion count relative to the original order.

We map every original word to its index. Then for every pair `(i,j)` with `i < j`, we count an inversion if the original position of `perm[i]` is larger than the original position of `perm[j]`.
4. Process every archive problem independently.
5. For each permutation, check whether it appears as a subsequence inside the archive title.

Use two pointers:

- one pointer scans the permutation
- one pointer scans the archive words

Whenever words match, advance the permutation pointer.

If the permutation pointer reaches the end, the permutation is a subsequence.
6. Among all subsequences found in the current archive problem, keep the minimum inversion count.

Minimum inversions means maximum similarity.
7. Convert the minimum inversion count into similarity:

```
p = n * (n - 1) / 2 - inversions
```

1. Track the archive problem with the highest similarity.

If similarities tie, keep the smaller archive index.
2. If no archive problem matched any permutation, print:

```
Brand new problem!
```

1. Otherwise print the best archive index and construct the similarity bar:

```
[:||||...||:]
```

with exactly `p` vertical bars.

### Why it works

Every valid solution corresponds to some permutation of Lesha's words. Since we enumerate all permutations, we never miss a candidate.

The subsequence check is exact. A permutation is accepted if and only if its words can be matched in order inside the archive title.

Among all accepted permutations, the problem definition explicitly asks for the one with minimum inversions. We compute inversion counts for every valid permutation and keep the minimum, so the chosen permutation is correct.

Finally, similarity is a monotonic transformation of inversions. Minimizing inversions is equivalent to maximizing similarity.

## Python Solution

```python
import sys
from itertools import permutations

input = sys.stdin.readline

def is_subsequence(perm, archive):
    j = 0

    for word in archive:
        if j < len(perm) and word == perm[j]:
            j += 1

    return j == len(perm)

def solve():
    n = int(input())
    base = input().split()

    pos = {word: i for i, word in enumerate(base)}

    perms = []

    for perm in permutations(base):
        inv = 0

        for i in range(n):
            for j in range(i + 1, n):
                if pos[perm[i]] > pos[perm[j]]:
                    inv += 1

        perms.append((perm, inv))

    m = int(input())

    best_similarity = -1
    best_index = -1

    max_pairs = n * (n - 1) // 2

    for idx in range(1, m + 1):
        parts = input().split()

        k = int(parts[0])
        archive = parts[1:]

        best_inv = None

        for perm, inv in perms:
            if is_subsequence(perm, archive):
                if best_inv is None or inv < best_inv:
                    best_inv = inv

        if best_inv is not None:
            similarity = max_pairs - best_inv

            if similarity > best_similarity:
                best_similarity = similarity
                best_index = idx

    if best_index == -1:
        print("Brand new problem!")
    else:
        print(best_index)
        print("[:{}:]".format('|' * best_similarity))

if __name__ == "__main__":
    solve()
```

The solution starts by generating every permutation once. Since the number of words is tiny, precomputing all permutations and their inversion counts simplifies the later logic.

The inversion calculation uses the original order mapping stored in `pos`. This avoids repeatedly searching for indices inside arrays.

The subsequence matcher uses the standard greedy scan. Greedy works because matching earlier occurrences can never make a subsequence impossible later.

One implementation detail that often causes mistakes is computing similarity correctly. The formula uses:

```
n * (n - 1) / 2
```

which is the maximum possible number of ordered pairs. Since Python uses integer division with `//`, we compute:

```
max_pairs = n * (n - 1) // 2
```

Another subtle detail is tie handling. We only update the best archive when the new similarity is strictly larger. Since we iterate archive problems in increasing order, ties automatically keep the smaller index.

## Worked Examples

### Sample 1

Input:

```
4
find the next palindrome
1
10 find the previous palindrome or print better luck next time
```

Key permutations checked:

| Permutation | Inversions | Subsequence? |
| --- | --- | --- |
| find the next palindrome | 0 | No |
| find the palindrome next | 1 | Yes |
| the find palindrome next | 2 | No |

The best valid permutation is:

```
find the palindrome next
```

with one inversion.

Maximum possible pair count:

```
4 × 3 / 2 = 6
```

Similarity:

```
6 - 1 = 5
```

Output:

```
1
[:|||||:]
```

This trace shows why minimum inversions matter. Several permutations may appear, but only the one closest to the original order determines the score.

### Custom Example

Input:

```
3
a b c
2
3 c b a
3 a b c
```

Trace:

| Archive | Best Permutation | Inversions | Similarity |
| --- | --- | --- | --- |
| c b a | c b a | 3 | 0 |
| a b c | a b c | 0 | 3 |

The second archive wins.

Output:

```
2
[:|||:]
```

This example demonstrates that similarity directly rewards preserving the original order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m × n! × k) | For every archive, check every permutation as a subsequence |
| Space | O(n!) | Store all permutations and inversion counts |

With `n ≤ 4`, we have at most 24 permutations. Even in the worst case:

```
10 × 24 × 20 = 4800
```

subsequence comparisons are performed. The solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import permutations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def is_subsequence(perm, archive):
        j = 0

        for word in archive:
            if j < len(perm) and word == perm[j]:
                j += 1

        return j == len(perm)

    out = io.StringIO()

    n = int(input())
    base = input().split()

    pos = {word: i for i, word in enumerate(base)}

    perms = []

    for perm in permutations(base):
        inv = 0

        for i in range(n):
            for j in range(i + 1, n):
                if pos[perm[i]] > pos[perm[j]]:
                    inv += 1

        perms.append((perm, inv))

    m = int(input())

    best_similarity = -1
    best_index = -1

    max_pairs = n * (n - 1) // 2

    for idx in range(1, m + 1):
        parts = input().split()
        archive = parts[1:]

        best_inv = None

        for perm, inv in perms:
            if is_subsequence(perm, archive):
                if best_inv is None or inv < best_inv:
                    best_inv = inv

        if best_inv is not None:
            similarity = max_pairs - best_inv

            if similarity > best_similarity:
                best_similarity = similarity
                best_index = idx

    if best_index == -1:
        print("Brand new problem!", file=out)
    else:
        print(best_index, file=out)
        print("[:{}:]".format('|' * best_similarity), file=out)

    return out.getvalue()

# provided sample
assert run(
"""4
find the next palindrome
1
10 find the previous palindrome or print better luck next time
"""
) == "1\n[:|||||:]\n", "sample 1"

# minimum size
assert run(
"""1
hello
1
1 hello
"""
) == "1\n[::]\n", "single word"

# no valid permutation
assert run(
"""2
a b
1
3 a a a
"""
) == "Brand new problem!\n", "missing word"

# tie between archives, smaller index wins
assert run(
"""2
a b
2
2 b a
2 b a
"""
) == "1\n[::]\n", "tie breaking"

# perfect ordering
assert run(
"""3
a b c
1
3 a b c
"""
) == "1\n[:|||:]\n", "maximum similarity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single-word case | `[::]` | Zero inversions and zero maximum pairs |
| Missing word in archive | `Brand new problem!` | Subsequence validation correctness |
| Two identical archive scores | Smaller index selected | Tie handling |
| Perfect ordering | Maximum similarity | Correct inversion calculation |

## Edge Cases

Consider the case where the archive contains repeated words but misses one required word:

```
2
a b
1
4 a a a a
```

The algorithm checks every permutation:

```
a b
b a
```

The subsequence matcher never reaches the end of either permutation because `b` never appears. `best_inv` remains `None`, so the archive is rejected correctly.

Now consider tie handling:

```
2
a b
2
2 b a
2 b a
```

Both archives contain permutation `b a` with one inversion. Since:

```
max_pairs = 1
similarity = 1 - 1 = 0
```

both archives have equal similarity.

The algorithm updates the answer only when similarity is strictly larger. Archive `1` stays selected, which matches the required behavior.

Finally, consider the smallest possible input:

```
1
hello
1
1 hello
```

There is only one permutation and zero possible inversions:

```
1 × 0 / 2 = 0
```

The similarity bar becomes:

```
[::]
```

The implementation handles this naturally because multiplying `'|' * 0` produces an empty string.
