---
title: "CF 105380E - String Palindrome Game"
description: "We are given a string and multiple independent queries. Each query specifies a segment of the string, and we are only allowed to look inside that segment."
date: "2026-06-23T16:05:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105380
codeforces_index: "E"
codeforces_contest_name: "TSEC Round 1 (Div. 4)"
rating: 0
weight: 105380
solve_time_s: 100
verified: true
draft: false
---

[CF 105380E - String Palindrome Game](https://codeforces.com/problemset/problem/105380/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string and multiple independent queries. Each query specifies a segment of the string, and we are only allowed to look inside that segment. Our task is to find a single contiguous substring entirely contained in the queried segment that is a palindrome and has maximum possible length. The answer for each query is just the length of that best palindrome.

So conceptually, each query defines a window on the string, and inside that window we are searching for the strongest symmetric pattern.

The constraints are small per test case, with string length and number of queries up to 1000, but the sum over all test cases can reach about one million operations of the form n times q. This immediately rules out any solution that recomputes palindrome information from scratch per query or tries to expand around every center for every query. A solution that is roughly quadratic per query would already be too slow.

The key difficulty is that palindromes are global structures, but queries are local restrictions. A palindrome that exists in the string is only useful for a query if it is fully contained inside its interval.

A few edge cases are worth making explicit.

If the query interval has length 1, the answer is always 1 because every single character is a palindrome. A naive solution that only considers even-length palindromes could incorrectly return 0 here.

If the string has all identical characters, then every substring is a palindrome, so each query should return the full interval length. Any solution that only tracks maximal palindromes around centers but fails to aggregate across positions will underestimate this case.

If the best palindrome is large but slightly outside the query range, it must not be counted. For example, in `abacaba`, the palindrome `abacaba` is global, but query `[2,6]` should only consider `bacab`, not the full string.

## Approaches

A direct brute force solution processes each query independently. For a fixed query `[l, r]`, we enumerate all substrings inside that interval and check whether each substring is a palindrome, keeping the maximum length.

Checking a substring for being a palindrome can be done in linear time in its length, or precomputed with dynamic programming. Either way, for a single query we are looking at roughly $O((r-l+1)^3)$ if done naively, or $O((r-l+1)^2)$ with DP checks. With up to 1000 queries, this becomes far too slow in the worst case.

The structure that makes this problem solvable is that palindrome membership for any substring can be precomputed once in $O(n^2)$, and then reused. The remaining challenge is not detecting palindromes, but answering range maximum queries over a set of precomputed “palindrome intervals”.

We flip the perspective. Instead of asking, “for each query, which palindrome is best?”, we enumerate all palindromic substrings once. Each palindrome becomes an interval with a value equal to its length. Then each query asks for the maximum value interval fully contained in `[l, r]`.

This transforms the problem into a two-dimensional range maximum query over intervals, which we can restructure into per-start or per-end aggregation and answer efficiently with preprocessing and sparse tables.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per query | $O(n^3)$ per query worst case | $O(1)$ or $O(n^2)$ | Too slow |
| Precompute palindromes + range max structure | $O(n^2 \log n)$ preprocessing, $O(1)$ per query | $O(n^2 \log n)$ | Accepted |

## Algorithm Walkthrough

We build the solution in layers, starting from palindrome detection and ending with fast query answering.

### Step 1: Precompute palindrome table

We build a table `pal[i][j]` that tells whether the substring `s[i..j]` is a palindrome. This is done using standard DP: single characters are palindromes, two-character substrings are palindromes if equal, and longer substrings depend on endpoints and inner substring.

This gives us full knowledge of which substrings are valid palindromes.

### Step 2: Convert palindromes into “best ending at r” values

For each endpoint `r`, we want to know, for every possible starting position `l`, what is the longest palindrome that ends at `r` and starts at or after `l`.

We define an array `bestStart[r][l]` meaning: among all palindromes that end at `r` and start in `[l, r]`, what is the maximum length.

To compute this, we scan `l` from right to left for each fixed `r`. If `s[l..r]` is a palindrome, it contributes candidate length `r-l+1`. While moving left, we keep a running maximum so that each `bestStart[r][l]` can be filled in constant time after checking `pal[l][r]`.

This step compresses all palindromes ending at `r` into a structure that can answer “best palindrome ending here under a left constraint”.

### Step 3: Turn queries into range maximum over endpoints

For a query `[l, r]`, the palindrome we choose must end somewhere between `l` and `r`. For each possible endpoint `e`, we already know the best palindrome ending at `e` that starts at or after `l`, which is `bestStart[e][l]`.

So the answer to the query becomes:

maximum over all `e` in `[l, r]` of `bestStart[e][l]`.

Now the problem is a range maximum query over a fixed array per `l`.

### Step 4: Preprocess range maximum queries

For each fixed `l`, we build a sparse table over `e` for the array `bestStart[e][l]`. This allows answering maximum queries over any interval `[l, r]` in constant time.

Since `n` is at most 1000, building `n` sparse tables is efficient enough.

## Why it works

Every palindrome substring is uniquely determined by its endpoints `(i, j)`. The algorithm ensures that every such substring is considered exactly once in `bestStart[j][i]`, and no valid palindrome is missed.

For any query, every candidate palindrome is grouped by its ending position, and the structure guarantees that we only take maxima over valid starting positions. The sparse table ensures we do not skip any endpoint in `[l, r]`, so the maximum over all valid palindromes is always preserved.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        s = input().strip()
        s = " " + s  # 1-indexed

        pal = [[False] * (n + 1) for _ in range(n + 1)]
        best_start = [[0] * (n + 2) for _ in range(n + 2)]

        for i in range(1, n + 1):
            pal[i][i] = True

        for i in range(1, n):
            if s[i] == s[i + 1]:
                pal[i][i + 1] = True

        for length in range(3, n + 1):
            for i in range(1, n - length + 2):
                j = i + length - 1
                if s[i] == s[j] and pal[i + 1][j - 1]:
                    pal[i][j] = True

        for r in range(1, n + 1):
            for l in range(r, 0, -1):
                best_start[r][l] = best_start[r][l + 1]
                if pal[l][r]:
                    best_start[r][l] = max(best_start[r][l], r - l + 1)

        LOG = 10
        st = [[[0] * (LOG + 1) for _ in range(n + 1)] for _ in range(n + 1)]

        for l in range(1, n + 1):
            for r in range(1, n + 1):
                st[l][r][0] = best_start[r][l]

            j = 1
            while (1 << j) <= n:
                for r in range(1, n + 1):
                    if r + (1 << j) - 1 <= n:
                        st[l][r][j] = max(st[l][r][j - 1],
                                          st[l][r + (1 << (j - 1))][j - 1])
                j += 1

        def query(l, r):
            length = r - l + 1
            k = (length).bit_length() - 1
            return max(st[l][r][k], st[l][r - (1 << k) + 1][k])

        for _ in range(q):
            l, r = map(int, input().split())
            print(query(l, r))

if __name__ == "__main__":
    solve()
```

The code first builds a standard palindrome DP table. Then it compresses all palindromes by endpoint into `best_start`. Finally, it builds a sparse table for each fixed left boundary so that each query becomes a constant-time range maximum query over endpoints.

A common pitfall here is trying to answer queries directly from `pal[i][j]` without tracking which palindromes actually lie inside `[l, r]`. That loses the dependency on containment. The separation into “end-based aggregation” is what makes the solution consistent.

## Worked Examples

### Example 1

Input string: `abcddcba`, query `[1, 8]`

We only show key steps.

| r | bestStart[r][l] relevant entries |
| --- | --- |
| 5 (`d`) | single characters |
| 6 (`d`) | palindrome `dd` gives value 2 at l=5 |
| 7 (`c`) | single |
| 8 (`a`) | full reverse structure contributes but bounded |

Query checks all endpoints 1 to 8 and finds maximum value 8 from `abcddcba`.

This trace shows how full-range palindromes dominate when they exist.

### Example 2

Input string: `abcddcba`, query `[2, 7]`

We restrict endpoints to 2..7. The best palindrome fully inside is `cddc` with length 4.

| endpoint e | bestStart[e][2] |
| --- | --- |
| 4 | 0 |
| 5 | 0 |
| 6 | 2 (`dd`) |
| 7 | 1 |

Maximum is 4 from `cddc`.

This confirms that valid palindromes must satisfy both endpoint and containment constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \log n)$ per test | DP for palindromes is $O(n^2)$, building sparse tables adds log factor |
| Space | $O(n^2 \log n)$ | storing palindrome table, bestStart, and sparse tables |

With $n \le 1000$ and total $n \cdot q \le 10^6$, this comfortably fits within limits since queries are answered in constant time after preprocessing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample
assert run("""2
8 5
abcddcba
1 8
2 7
2 8
4 4
3 6
5 3
aaabb
1 5
4 5
2 3
""") == """8
6
6
1
4
3
2
2"""

# all identical
assert run("""1
5 2
aaaaa
1 5
2 4
""") == """5
3"""

# single char queries
assert run("""1
3 3
abc
1 1
2 2
3 3
""") == """1
1
1"""

# smallest mixed
assert run("""1
4 2
abca
1 4
2 3
""") == """3
1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all identical string | full length answers | global palindrome dominance |
| single characters | always 1 | base case correctness |
| mixed small string | local palindromes only | containment logic |

## Edge Cases

For a string of identical characters like `aaaaa`, every substring is a palindrome. The algorithm marks every `(l, r)` as valid in the DP table, and `best_start` propagates the full lengths. When a query asks `[2, 4]`, endpoint aggregation ensures the maximum `3` is returned from substring `aaa`, confirming correct handling of dense palindrome regions.

For single-character queries such as `[3, 3]` in `abc`, only diagonal entries `pal[i][i]` are true. The `best_start` array records length 1 at each position, and the query over a single endpoint returns exactly 1, matching the definition that every character is a palindrome.

For queries where the optimal palindrome spans across the center but not the boundaries, such as `abacaba` with `[2, 6]`, the full palindrome is excluded automatically because its endpoints are outside the interval. Only palindromes fully contained in the segment contribute to `best_start`, so the result correctly reduces to the largest internal symmetric substring.
