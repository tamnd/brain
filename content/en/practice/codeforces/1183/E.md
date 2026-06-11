---
title: "CF 1183E - Subsequences (easy version)"
description: "We start with a string and want to build a set containing exactly k distinct subsequences. Adding a subsequence of length L costs the number of removed characters, which is n - L. The same subsequence cannot be added twice."
date: "2026-06-12T01:22:43+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "implementation", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1183
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 570 (Div. 3)"
rating: 2000
weight: 1183
solve_time_s: 100
verified: true
draft: false
---

[CF 1183E - Subsequences (easy version)](https://codeforces.com/problemset/problem/1183/E)

**Rating:** 2000  
**Tags:** dp, graphs, implementation, shortest paths  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a string and want to build a set containing exactly `k` distinct subsequences. Adding a subsequence of length `L` costs the number of removed characters, which is `n - L`. The same subsequence cannot be added twice. The task is to minimize the total cost, or report that there are not enough distinct subsequences.

The cost structure immediately suggests that longer subsequences are preferable. A subsequence of length `n` costs `0`, length `n-1` costs `1`, and so on. If we know how many distinct subsequences exist for every length, the optimal strategy is obvious: take as many subsequences as possible from length `n`, then from length `n-1`, and continue downward until we have collected `k` of them.

The easy version has `n ≤ 100`, which allows dynamic programming with roughly `O(n²)` or `O(n³)` operations. Enumerating all subsequences is impossible because a string of length `100` has `2^100` subsequences, far beyond any feasible limit.

Several situations are easy to mishandle.

Consider

```
1 2
a
```

The distinct subsequences are `"a"` and `""`. Their costs are `0` and `1`, so the answer is

```
1
```

A solution that forgets the empty subsequence would incorrectly print `-1`.

Another example is

```
3 8
aaa
```

The distinct subsequences are

```
"aaa"
"aa"
"a"
""
```

Only four different subsequences exist because many deletion patterns produce identical strings. The correct output is

```
-1
```

Counting deletion masks instead of distinct strings would mistakenly conclude that eight choices are available.

A third example is

```
4 5
abcd
```

All characters are different. There are many distinct subsequences, and the cheapest five are

```
abcd  cost 0
abc   cost 1
abd   cost 1
acd   cost 1
bcd   cost 1
```

The answer is

```
4
```

Choosing shorter subsequences too early would increase the total cost unnecessarily.

## Approaches

The brute force approach generates every subsequence, stores the resulting strings in a set to remove duplicates, sorts them by length, and takes the longest `k`. This method is correct because it directly follows the definition. The problem is the number of masks. For `n = 100`, there are `2^100 ≈ 10^30` subsequences, which makes this approach completely impossible.

The key observation is that we do not need the subsequences themselves. We only need to know how many distinct subsequences have each possible length.

Suppose we process the string from left to right. Let `dp[i][j]` denote the number of distinct subsequences of length `j` that can be formed using the prefix ending at position `i`. If we append `s[i]`, we must avoid creating duplicates that were already created by a previous occurrence of the same character. The last occurrence of each character allows us to subtract exactly those duplicates.

This turns an exponential enumeration problem into a polynomial dynamic programming problem. Once the counts are known, we greedily take subsequences from larger lengths to smaller lengths because every additional deleted character increases the cost by one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(2^n) | Too slow |
| Optimal | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Define `dp[i][j]` as the number of distinct subsequences of length `j` that can be formed using the first `i` characters.
2. Initialize `dp[0][0] = 1`, because the empty string has one subsequence, namely itself.
3. Process characters one by one. For position `i`, first copy all values from `dp[i-1][j]`, representing subsequences that do not use the new character.
4. For every length `j ≥ 1`, append the current character to all distinct subsequences of length `j-1` from the previous prefix. This contributes `dp[i-1][j-1]`.
5. If the current character appeared before, let its previous position be `p`. Appending the current character to subsequences that already existed before position `p` creates duplicates. Subtract `dp[p-1][j-1]` from the contribution.

The subtraction removes exactly the subsequences that were already generated when the earlier occurrence of this character was used.

1. Store the current position as the latest occurrence of this character.
2. After filling the table, `dp[n][j]` gives the number of distinct subsequences of length `j`.
3. Starting from length `n` and moving downward, take as many subsequences as possible while `k > 0`.
4. If we take `x` subsequences of length `j`, their contribution to the answer is

```
x × (n - j)
```

1. If after considering length `0` we still have `k > 0`, fewer than `k` distinct subsequences exist, so print `-1`.

### Why it works

For every prefix and every length, `dp[i][j]` counts distinct subsequences exactly once. Whenever a character appears again, the only duplicate subsequences produced are those whose last occurrence of that character comes from the previous copy. Subtracting the contribution from before that previous occurrence removes precisely those duplicates and nothing else.

Since the cost decreases as the subsequence length increases, any optimal solution must use as many longer subsequences as possible before considering shorter ones. Thus the greedy collection phase produces the minimum total cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
s = input().strip()

dp = [[0] * (n + 1) for _ in range(n + 1)]
dp[0][0] = 1

last = [-1] * 26

for i in range(1, n + 1):
    c = ord(s[i - 1]) - ord('a')

    for j in range(n + 1):
        dp[i][j] = dp[i - 1][j]

    prev = last[c]

    for j in range(1, i + 1):
        add = dp[i - 1][j - 1]
        if prev != -1:
            add -= dp[prev][j - 1]
        dp[i][j] += add

    last[c] = i - 1

ans = 0

for length in range(n, -1, -1):
    take = min(k, dp[n][length])
    ans += take * (n - length)
    k -= take

if k > 0:
    print(-1)
else:
    print(ans)
```

The table has dimensions `(n+1) × (n+1)`. Row `i` represents the first `i` characters. Every row begins by copying the previous one because every subsequence that existed earlier still exists after adding a new character.

The subtle part is the subtraction. Suppose the current character previously appeared at index `prev`. Any subsequence formed by extending something that already existed before position `prev` was already created when that earlier occurrence was used. Subtracting `dp[prev][j-1]` removes exactly those repetitions.

The greedy phase starts from length `n`, because these subsequences cost the least. Moving downward guarantees minimum total cost.

No integer overflow issues exist in Python. In the easy version the total number of distinct subsequences never exceeds `2^100`, which Python handles naturally.

## Worked Examples

### Example 1

Input

```
4 5
asdf
```

All characters are different.

| Length | Count of distinct subsequences | Cost | Taken |
| --- | --- | --- | --- |
| 4 | 1 | 0 | 1 |
| 3 | 4 | 1 | 4 |
| 2 | 6 | 2 | 0 |
| 1 | 4 | 3 | 0 |
| 0 | 1 | 4 | 0 |

Total cost:

```
1×0 + 4×1 = 4
```

This example shows why taking longer subsequences first is optimal.

### Example 2

Input

```
3 8
aaa
```

| Length | Count of distinct subsequences | Cost | Taken |
| --- | --- | --- | --- |
| 3 | 1 | 0 | 1 |
| 2 | 1 | 1 | 1 |
| 1 | 1 | 2 | 1 |
| 0 | 1 | 3 | 1 |

Only four distinct subsequences exist.

After taking all four, we still need four more, so the answer is `-1`.

This example demonstrates that repeated characters drastically reduce the number of distinct subsequences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Filling an `(n+1) × (n+1)` DP table |
| Space | O(n²) | Storing all DP states |

With `n ≤ 100`, at most about ten thousand states are needed. The algorithm runs comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    s = input().strip()

    dp = [[0] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    last = [-1] * 26

    for i in range(1, n + 1):
        c = ord(s[i - 1]) - ord('a')

        for j in range(n + 1):
            dp[i][j] = dp[i - 1][j]

        prev = last[c]

        for j in range(1, i + 1):
            add = dp[i - 1][j - 1]
            if prev != -1:
                add -= dp[prev][j - 1]
            dp[i][j] += add

        last[c] = i - 1

    ans = 0
    k = int(k)

    for length in range(n, -1, -1):
        take = min(k, dp[n][length])
        ans += take * (n - length)
        k -= take

    if k > 0:
        print(-1)
    else:
        print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("4 5\nasdf\n") == "4"

# custom cases
assert run("1 1\na\n") == "0", "minimum size"
assert run("1 2\na\n") == "1", "empty subsequence needed"
assert run("3 8\naaa\n") == "-1", "not enough distinct subsequences"
assert run("2 4\nab\n") == "4", "all subsequences are used"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / a` | 0 | Minimum size |
| `1 2 / a` | 1 | Empty subsequence handling |
| `3 8 / aaa` | -1 | Duplicate subsequences caused by repeated letters |
| `2 4 / ab` | 4 | Using every possible subsequence |

## Edge Cases

Consider

```
1 2
a
```

The DP counts one subsequence of length `1` and one of length `0`. The greedy phase takes both. Their costs are `0` and `1`, giving answer `1`. The empty subsequence is handled naturally by `dp[0][0]=1`.

Now consider

```
3 8
aaa
```

The table ends with

```
length 3 : 1
length 2 : 1
length 1 : 1
length 0 : 1
```

Even though there are eight deletion masks, many produce the same strings. After using all four distinct subsequences, `k` remains positive, so the algorithm correctly prints `-1`.

Finally, consider

```
4 5
abcd
```

All characters are different, so no subtraction occurs. The counts become

```
1, 4, 6, 4, 1
```

for lengths `0` through `4`. The greedy phase selects one subsequence of length `4` and four of length `3`, producing total cost `4`, which is the minimum possible.
