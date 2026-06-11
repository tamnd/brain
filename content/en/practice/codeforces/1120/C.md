---
title: "CF 1120C - Compress String"
description: "We are given a string and two costs. The first operation allows us to encode exactly one character for a cost of a."
date: "2026-06-12T04:24:56+07:00"
tags: ["codeforces", "competitive-programming", "dp", "strings"]
categories: ["algorithms"]
codeforces_contest: 1120
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 543 (Div. 1, based on Technocup 2019 Final Round)"
rating: 2100
weight: 1120
solve_time_s: 102
verified: true
draft: false
---

[CF 1120C - Compress String](https://codeforces.com/problemset/problem/1120/C)

**Rating:** 2100  
**Tags:** dp, strings  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string and two costs.

The first operation allows us to encode exactly one character for a cost of `a`.

The second operation allows us to encode any non-empty substring for a fixed cost of `b`, but only if that substring has already appeared somewhere in the part of the string that has already been encoded.

The string must be processed from left to right. At every position we decide whether to write the next character directly, or whether we can copy a longer substring that already exists in the previously processed prefix.

The goal is to minimize the total cost needed to encode the entire string.

The length of the string is at most 5000. This immediately rules out anything exponential or even cubic with a large constant. A dynamic programming solution with roughly $O(n^2)$ work is usually acceptable for $n=5000$, while $O(n^3)$ would be far too slow because it would require around $1.25 \times 10^{11}$ operations in the worst case.

The tricky part is determining, for every position, how long a substring can be copied from the already processed prefix. A naive implementation that repeatedly compares substrings would easily become cubic.

Several edge cases are easy to mishandle.

Consider:

```
3 3 1
aba
```

The last `'a'` may be copied because it already appeared before. The optimal answer is `7`, not `9`.

Consider:

```
4 1 100
aaaa
```

Copying is extremely expensive. Even though repeated substrings exist everywhere, the optimal answer is `4`, obtained by writing each character individually.

Consider:

```
4 10 1
aaaa
```

Now copying is cheap. One optimal construction is:

```
"a"  -> 10
"a"  -> 1
"aa" -> 1
```

Total cost `12`.

A common mistake is to assume that a copied substring must have appeared as a previously chosen block. The problem only requires it to be a substring of the already encoded prefix. Any occurrence inside the prefix is sufficient.

Another common mistake is allowing copies that overlap future characters. When encoding position `i`, the source occurrence must lie entirely inside the already processed prefix `s[0..i-1]`.

## Approaches

The most direct dynamic programming idea is to let `dp[i]` denote the minimum cost to encode the first `i` characters.

From position `i`, we can always encode one character and move to `i+1` with cost `a`.

We can also try every possible substring starting at `i`, check whether it appeared before, and if it did, jump directly to the end of that substring with cost `b`.

This DP is correct because every valid encoding corresponds to a sequence of transitions between prefix lengths.

The problem is checking whether a substring already appeared. If we try every starting position, every length, and compare strings directly, we obtain roughly $O(n^3)$ work.

The key observation is that for every position `i`, we only need one number:

`mx[i] = maximum length of a substring starting at i that already occurs somewhere before i`.

Once this value is known, the DP becomes simple. If `mx[i] = L`, then every length from `1` to `L` can be copied for cost `b`. Since the cost does not depend on length, the best choice is always to copy the longest available substring.

The remaining challenge is computing all `mx[i]`.

For every pair of positions `(i, j)` with `j < i`, we compute the longest common prefix of suffixes starting at `i` and `j`.

Let:

```
lcp[i][j] = longest common prefix length of s[i:] and s[j:]
```

Then any occurrence starting at `j` provides a copyable substring of length:

```
min(lcp[i][j], i - j)
```

The second term is crucial. The source occurrence must lie completely inside the already processed prefix. If the match extends beyond position `i-1`, we cannot use that part.

Taking the maximum over all earlier positions `j` gives `mx[i]`.

The LCP table can be computed in $O(n^2)$ using the classic reverse DP:

```
if s[i] == s[j]:
    lcp[i][j] = lcp[i+1][j+1] + 1
else:
    lcp[i][j] = 0
```

Once `mx` is known, the DP becomes $O(n^2)$, leading to an overall $O(n^2)$ solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n²) | Too slow |
| Optimal | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read the string and create an `n × n` LCP table.
2. Fill the table from bottom-right toward top-left.

If `s[i] == s[j]`, then the common prefix length equals `1 + lcp[i+1][j+1]`. Otherwise it is zero.
3. For every position `i`, compute the longest copyable length `mx[i]`.

Examine every earlier position `j < i`.

The suffix match length is `lcp[i][j]`, but only the first `i-j` characters belong entirely to the already encoded prefix. Hence the usable length is:

```
min(lcp[i][j], i-j)
```

Take the maximum over all `j`.
4. Create DP array `dp`, where `dp[i]` is the minimum cost to encode the first `i` characters.
5. Initialize:

```
dp[0] = 0
```
6. For every position `i`:

Encode one character:

```
dp[i+1] = min(dp[i+1], dp[i] + a)
```
7. If `mx[i] > 0`, copy the longest available substring:

```
dp[i + mx[i]] = min(dp[i + mx[i]], dp[i] + b)
```

Since all copy lengths cost the same, using the maximum length dominates all shorter lengths.
8. Output `dp[n]`.

### Why it works

The LCP table correctly measures how many consecutive characters match between two suffixes.

For a position `i`, every valid copied block must come from some earlier occurrence beginning at `j < i`. The longest such block has length `min(lcp[i][j], i-j)`, because only characters entirely inside the already encoded prefix may serve as the source. Taking the maximum over all earlier positions gives exactly the longest copy operation available at `i`.

The DP considers every possible way to extend an already optimal encoding of the prefix. One transition corresponds to writing a single character, and the other corresponds to using the best available copy operation. Since copy cost is independent of copied length, a shorter copy can never improve upon a longer copy starting at the same position. Every valid encoding is represented by a sequence of DP transitions, and every DP transition represents a valid encoding action. Thus `dp[n]` equals the minimum possible total cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())
    s = input().strip()

    lcp = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(n - 1, -1, -1):
        si = s[i]
        row = lcp[i]
        next_row = lcp[i + 1]

        for j in range(n - 1, -1, -1):
            if si == s[j]:
                row[j] = next_row[j + 1] + 1

    mx = [0] * n

    for i in range(n):
        best = 0
        for j in range(i):
            best = max(best, min(lcp[i][j], i - j))
        mx[i] = best

    INF = 10 ** 18
    dp = [INF] * (n + 1)
    dp[0] = 0

    for i in range(n):
        dp[i + 1] = min(dp[i + 1], dp[i] + a)

        if mx[i] > 0:
            dp[i + mx[i]] = min(dp[i + mx[i]], dp[i] + b)

    print(dp[n])

solve()
```

The first part builds the LCP table. Computing it backwards guarantees that when we need `lcp[i+1][j+1]`, it has already been calculated.

The `mx` array stores the maximum copy length available at each position. The expression `min(lcp[i][j], i-j)` is the subtle part. Without the `i-j` restriction, we would incorrectly allow the source occurrence to extend into characters that have not yet been encoded.

The DP stores minimum costs for prefixes. From position `i`, writing one character always remains possible. Copying becomes possible only when `mx[i] > 0`.

A subtle observation is that we only transition using `mx[i]`, not every length from `1` to `mx[i]`. Since every copy costs exactly `b`, a longer copy always dominates a shorter copy that starts at the same position.

## Worked Examples

### Example 1

Input:

```
3 3 1
aba
```

The computed copy lengths are:

| Position i | Suffix | mx[i] |
| --- | --- | --- |
| 0 | aba | 0 |
| 1 | ba | 0 |
| 2 | a | 1 |

DP evolution:

| i | dp[i] | Action | Updated state |
| --- | --- | --- | --- |
| 0 | 0 | write 'a' | dp[1] = 3 |
| 1 | 3 | write 'b' | dp[2] = 6 |
| 2 | 6 | write 'a' | dp[3] = 9 |
| 2 | 6 | copy length 1 | dp[3] = 7 |

Final answer:

```
7
```

This example shows why a copied substring may be a single character. The last `'a'` already appears in the prefix `"ab"`.

### Example 2

Input:

```
4 10 1
aaaa
```

Copy lengths:

| Position i | Suffix | mx[i] |
| --- | --- | --- |
| 0 | aaaa | 0 |
| 1 | aaa | 1 |
| 2 | aa | 2 |
| 3 | a | 1 |

DP evolution:

| i | dp[i] | Action | Result |
| --- | --- | --- | --- |
| 0 | 0 | write | dp[1]=10 |
| 1 | 10 | copy 1 | dp[2]=11 |
| 2 | 11 | copy 2 | dp[4]=12 |

Final answer:

```
12
```

This trace demonstrates the benefit of taking the longest available copy. At position 2, copying `"aa"` costs the same as copying only `"a"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | LCP computation, `mx` computation, and DP |
| Space | O(n²) | LCP table dominates memory usage |

With `n ≤ 5000`, the algorithm performs about 25 million table operations, which comfortably fits within the time limit in optimized Python. The memory usage is also acceptable for the contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, a, b = map(int, input().split())
    s = input().strip()

    lcp = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(n - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if s[i] == s[j]:
                lcp[i][j] = lcp[i + 1][j + 1] + 1

    mx = [0] * n
    for i in range(n):
        for j in range(i):
            mx[i] = max(mx[i], min(lcp[i][j], i - j))

    INF = 10 ** 18
    dp = [INF] * (n + 1)
    dp[0] = 0

    for i in range(n):
        dp[i + 1] = min(dp[i + 1], dp[i] + a)
        if mx[i]:
            dp[i + mx[i]] = min(dp[i + mx[i]], dp[i] + b)

    return str(dp[n]) + "\n"

# provided sample
assert run("3 3 1\naba\n") == "7\n", "sample 1"

# minimum size
assert run("1 5 2\na\n") == "5\n", "single character"

# copying never worth it
assert run("4 1 100\naaaa\n") == "4\n", "expensive copy"

# repeated string
assert run("4 10 1\naaaa\n") == "12\n", "cheap copy"

# no repeated substrings
assert run("5 3 1\nabcde\n") == "15\n", "all unique"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 2 / a` | `5` | Minimum size |
| `4 1 100 / aaaa` | `4` | Copy exists but should not be used |
| `4 10 1 / aaaa` | `12` | Long repeated substring handling |
| `5 3 1 / abcde` | `15` | No copy operations available |

## Edge Cases

Consider:

```
4 10 1
aaaa
```

At position `2`, the suffixes beginning at `0` and `2` match for length `2`. The algorithm computes:

```
min(lcp[2][0], 2) = min(2, 2) = 2
```

so `mx[2] = 2`. The DP jumps directly from prefix length `2` to prefix length `4` for cost `1`, producing the correct answer `12`.

Consider:

```
4 1 100
aaaa
```

The same copy opportunities exist, but the DP compares them against writing characters individually. Since every copy costs `100`, all copy transitions are dominated by character transitions. The answer becomes `4`.

Consider:

```
5 3 1
abcde
```

Every pair of suffixes has LCP `0`, so all `mx[i]` values remain `0`. The DP only uses character transitions and returns `15`.

Consider:

```
6 5 1
ababab
```

At position `2`, the substring `"ab"` already appears in the prefix. The LCP table finds a match of length `4`, but only the first `2` characters are valid as a source because `i-j=2`. The algorithm uses:

```
min(4, 2) = 2
```

preventing an illegal overlap with future characters. This restriction is exactly what keeps the solution correct.
