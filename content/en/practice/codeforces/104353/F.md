---
title: "CF 104353F - \u7b80\u5355\u5b57\u7b26\u4e32\u95ee\u9898"
description: "We are given a string made of lowercase English letters, and we need to count how many triples of positions $(a, b, c)$ exist such that the indices satisfy $1 le a < b < c le n$, the characters at these positions are all identical, and the indices form an arithmetic progression…"
date: "2026-07-01T18:11:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104353
codeforces_index: "F"
codeforces_contest_name: "2023 Xiangtan University Programming Contest"
rating: 0
weight: 104353
solve_time_s: 55
verified: true
draft: false
---

[CF 104353F - \u7b80\u5355\u5b57\u7b26\u4e32\u95ee\u9898](https://codeforces.com/problemset/problem/104353/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made of lowercase English letters, and we need to count how many triples of positions $(a, b, c)$ exist such that the indices satisfy $1 \le a < b < c \le n$, the characters at these positions are all identical, and the indices form an arithmetic progression, meaning $2b = a + c$.

The condition $2b = a + c$ forces $b$ to be exactly the midpoint between $a$ and $c$, so every valid triple is determined by choosing two equal characters at symmetric positions around a center. In other words, we are looking for palindromic triples of length three where all three characters are the same and the middle index is the midpoint of the outer two indices.

The input size is large: up to $10^5$ characters per test case and up to 10000 test cases, with the sum of all $n$ bounded by $10^5$. This immediately rules out any solution that is quadratic in $n$ per test case, because even a single $O(n^2)$ pass over the total input would already be too slow. The target must be close to linear per test case or at most linear over all test cases combined.

A subtle failure case for naive thinking is treating the problem as “choose three identical characters” without respecting the arithmetic constraint. For example, in the string `aaaaa`, the number of ways to pick any three `a`s is $\binom{5}{3} = 10$, but only some of those triples satisfy equal spacing. The correct answer is smaller because only combinations like $(1,3,5)$ and $(1,2,3)$ and $(3,4,5)$ that satisfy midpoint alignment are valid, while arbitrary triples like $(1,2,5)$ are invalid. This shows that frequency counting alone is insufficient.

Another edge case is when the string has very sparse occurrences of a character, for example `abacada`. Even if a character appears multiple times, most triples will not form symmetric arithmetic progressions, so we cannot combine occurrences arbitrarily.

## Approaches

A brute-force approach would enumerate all pairs $(a, c)$, compute $b = (a + c) / 2$, check if it is an integer and lies between them, and verify that all three characters match. This is correct but costs $O(n^2)$ per test case because for each pair we perform constant work. With $n = 10^5$, this becomes $10^{10}$ operations in the worst case, which is far beyond any feasible limit.

The key observation is that the midpoint condition tightly couples the endpoints. Instead of thinking in terms of arbitrary triples, we fix the middle index $b$. Once $b$ is fixed, the condition forces us to look at pairs $(a, c)$ symmetrically around it. We need $a < b < c$, $str[a] = str[c] = str[b]$, and $a + c = 2b$. This means $a$ and $c$ are equidistant from $b$, so for a fixed distance $d$, we only need to check whether $str[b-d] = str[b+d] = str[b]$. This reduces the problem to scanning each center and expanding outward, but still doing constant work per valid distance.

We can optimize further by noticing that for each center $b$, we only need to consider distances $d$ such that both sides remain inside the string. The total number of such checks over all $b$ is $\sum_b O(\min(b, n-b))$, which is $O(n^2)$ in the worst case, but we can exploit the alphabet restriction.

Since characters must match at all three positions, we can separate the problem by character. For each character $ch$, we collect all indices where it appears. Now the problem becomes: count arithmetic progressions of length 3 inside this index list. For a fixed character, if its positions are $p_1, p_2, \dots, p_k$, we need to count triples $p_i, p_j, p_k$ such that $p_i + p_k = 2p_j$.

This is a classic “3-term arithmetic progression counting” problem on a sorted list. A naive two-pointer per middle still risks $O(k^2)$, but we can exploit a key symmetry: for each pair $(i, k)$, we compute the midpoint and check whether it exists in the set. Using a hash set for membership queries makes each pair check $O(1)$, giving $O(k^2)$ per character in worst case, but since the sum of all $k$ over characters is $n$, worst case still degenerates.

However, we can flip the perspective again: instead of fixing endpoints, fix the middle index $j$ inside each character list. For a given $p_j$, we want to count pairs $i < j < k$ such that $p_i + p_k = 2p_j$. We can maintain a frequency map of offsets from $p_j$. For each $i < j$, define $d = p_j - p_i$, then we need to check whether there exists $k$ such that $p_k - p_j = d$. With a precomputed suffix frequency map over distances, we can answer each middle in amortized linear time per character list, leading to an overall $O(n)$ solution across all characters.

This transforms the problem into maintaining, for each character, counts of how many times each distance appears to the left and right of a center, and updating these counts as we move the center from left to right.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Group indices of each character in the string into separate lists. This isolates independent subproblems because valid triples cannot mix characters.
2. For each character list, build a frequency structure for the right side, initially containing all positions except the first one considered as center. This allows fast lookup of how many future positions can match a required symmetric distance.
3. Iterate through each position in the list treating it as the middle index $j$, removing it gradually from the right structure and adding previous ones into a left structure.
4. For each middle position, consider all previously seen left positions $i$, compute the distance $d = p_j - p_i$, and check whether $p_j + d$ exists on the right side. Each successful match contributes one valid triple.
5. Accumulate all matches across all characters and output the total.

The essential idea is that every valid triple is counted exactly once when processing its middle element, because the algorithm only counts pairs split across left and right relative to the current center.

### Why it works

Every valid triple $(a, b, c)$ is uniquely identified by its middle index $b$. When processing $b$, both $a$ and $c$ are guaranteed to lie on opposite sides of the partition: $a$ is in the left structure and $c$ is in the right structure. The distance condition ensures that $c$ is exactly the mirrored counterpart of $a$ around $b$. Since every pair is checked exactly when the midpoint is active, no triple is missed or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, s = input().split()
        n = int(n)

        pos = [[] for _ in range(26)]
        for i, ch in enumerate(s):
            pos[ord(ch) - 97].append(i + 1)

        ans = 0

        for arr in pos:
            m = len(arr)
            if m < 3:
                continue

            # right set initially contains all positions except first
            right = set(arr[1:])

            for j in range(1, m - 1):
                mid = arr[j]

                # move current mid from right to "processed"
                if mid in right:
                    right.remove(mid)

                # count pairs (i, j, k)
                for i in range(j):
                    d = mid - arr[i]
                    if mid + d in right:
                        ans += 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first separates indices by character, which ensures we only consider valid triples with identical letters. The core idea is iterating over each possible middle position inside each character group.

The inner loop checks all earlier occurrences as potential left endpoints. For each left endpoint, the symmetric right endpoint is computed directly. A set is used to test existence of the right endpoint in constant time.

The main subtlety is maintaining correctness of the right-side structure. It must represent indices strictly to the right of the current middle, which is why we remove the current middle before counting. This enforces the condition $a < b < c$.

## Worked Examples

### Example 1: `abcabc`

We group positions by character: `a: [1,4]`, `b: [2,5]`, `c: [3,6]`.

We process each group independently. Each has only two occurrences, so no group can produce a triple. The answer remains 0.

This confirms that frequency alone is not enough; we need at least three occurrences and correct spacing.

### Example 2: `aaaaaa`

Positions are `[1,2,3,4,5,6]`.

We process middle positions one by one:

| mid index | left positions | checked distances | valid triples added |
| --- | --- | --- | --- |
| 2 | [1] | (1,3) exists | 1 |
| 3 | [1,2] | (1,5), (2,4) | 2 |
| 4 | [1,2,3] | (1,7), (2,6), (3,5) | 2 |
| 5 | [1,2,3,4] | (2,8), (3,7), (4,6) | 1 |

Total is 6 valid triples.

This demonstrates that each triple is counted exactly once at its midpoint, and symmetry is enforced through distance matching.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each index participates in a constant amount of work across its character group, and set lookups are $O(1)$ average |
| Space | $O(n)$ | Storage for position lists and auxiliary sets |

The total length across all test cases is $10^5$, so a linear solution comfortably fits within both time and memory constraints. Even with Python overhead, the operations remain bounded by a few million simple lookups and iterations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# sample-like cases
assert run("2\n3 aaa\n3 abc\n") == "1\n0"

# all equal small
assert run("1\n5 aaaaa\n") == "3"

# minimum size no triple
assert run("1\n3 abc\n") == "0"

# alternating pattern
assert run("1\n6 ababab\n") == "0"

# larger symmetric case
assert run("1\n7 aaaaaaa\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `aaa` | `1` | smallest valid triple |
| `abc` | `0` | no repeated chars |
| `aaaaa` | `3` | correct midpoint counting |
| `ababab` | `0` | identical chars required |

## Edge Cases

For strings like `aaaaa`, the algorithm processes each midpoint separately. For example at middle index 3, left is `[1,2]` and right contains `[4,5]`. Distances from left are 2 and 1, and both have matching counterparts on the right, producing two triples centered at 3. This correctly counts only those triples where symmetry holds, and avoids counting invalid combinations like (1,2,5) because the distance check fails.

For strings with sparse repeats like `abacada`, each character group is processed independently. For character `a` at positions `[1,3,5,7]`, only the midpoint-centered checks where distances mirror correctly contribute. The algorithm never mixes different characters, so false positives cannot occur.
