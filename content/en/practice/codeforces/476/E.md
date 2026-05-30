---
title: "CF 476E - Dreamoon and Strings"
description: "We start with a string s. We may delete exactly x characters, keeping the remaining characters in their original order. The resulting string is a subsequence of s. Inside that resulting string, we look for as many non-overlapping occurrences of a pattern p as possible."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "strings"]
categories: ["algorithms"]
codeforces_contest: 476
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 272 (Div. 2)"
rating: 2200
weight: 476
solve_time_s: 345
verified: true
draft: false
---

[CF 476E - Dreamoon and Strings](https://codeforces.com/problemset/problem/476/E)

**Rating:** 2200  
**Tags:** dp, strings  
**Solve time:** 5m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a string `s`. We may delete exactly `x` characters, keeping the remaining characters in their original order. The resulting string is a subsequence of `s`.

Inside that resulting string, we look for as many **non-overlapping** occurrences of a pattern `p` as possible. For every deletion count `x` from `0` to `|s|`, we must output the maximum number of occurrences that can be achieved.

The key difficulty is that the occurrences are counted after deletions. A copy of `p` does not need to appear as a substring of the original string. We may delete characters in between and make distant characters become adjacent.

The length of `s` is at most 2000, while `p` has length at most 500. A cubic solution is already risky, and anything close to enumerating all subsequences is completely impossible. A solution around `O(n²)` or `O(n² + nm)` is the right target.

A few situations are easy to get wrong.

Consider:

```
s = "aa"
p = "aa"
```

With zero deletions we have one occurrence. With one deletion we have only `"a"`, so the answer becomes zero. A common mistake is to compute only the minimum deletions needed for one occurrence and conclude that every larger deletion count is also possible. That is false here.

Another subtle case is:

```
s = "abca"
p = "aa"
```

The pattern is not a substring of `s`, but it can be formed by deleting `"bc"`. Any solution that only searches for substrings of the original string misses valid answers.

A third pitfall appears when occurrences share characters in the original string:

```
s = "aaaaa"
p = "aa"
```

The occurrences in the final string must be non-overlapping. Choosing positions `(1,2)` and `(2,3)` is illegal because the same character participates in both copies. The dynamic programming must enforce disjoint intervals.

## Approaches

A brute-force approach would try every subsequence of `s`, count how many non-overlapping copies of `p` appear, and update answers for the corresponding deletion count. Since a string of length 2000 has `2^2000` subsequences, this is hopeless.

The next observation is that a single occurrence of `p` in the final string corresponds to selecting positions in `s` that spell `p` as a subsequence. Suppose the first selected position is `l` and the last selected position is `r`. Inside the interval `[l, r]`, every character not used by the occurrence must be deleted. The number of mandatory deletions is

$$(r-l+1)-|p|.$$

If we know the cheapest interval representing one occurrence, then the problem starts looking like interval scheduling.

For every starting position `i`, we compute the earliest possible ending position `end[i]` such that `p` can be matched as a subsequence beginning at `i`. If such an interval exists, choosing it contributes one occurrence and forces

$$(end[i]-i+1)-|p|$$

deletions.

Now the problem becomes:

Choose several non-overlapping occurrence intervals. Minimize the number of mandatory deletions needed to obtain exactly `k` occurrences.

Once that minimum is known, the final answers become easy. Characters outside all chosen intervals are irrelevant. They may be kept or deleted freely. This converts a minimum-deletion DP into answers for every exact deletion count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n)` | `O(n)` | Too slow |
| Optimal DP with interval transitions | `O(n² + nm)` | `O(n²)` | Accepted |

## Algorithm Walkthrough

1. Precompute a next-occurrence table for `s`.

For every position and every letter, store the first occurrence of that letter at or after the position. This allows subsequence matching in constant time per character of `p`.
2. For every position `i` in `s`, compute the earliest interval representing one occurrence of `p`.

If `s[i]` is not equal to `p[0]`, no occurrence can start there.

Otherwise, greedily match the remaining characters of `p` using the next-occurrence table. If matching succeeds and finishes at position `r`, store:

```
end[i] = r
cost[i] = (r - i + 1) - m
```

where `m = |p|`.
3. Let `dp[pos][k]` be the minimum number of mandatory deletions needed after processing the prefix ending before `pos`, while creating exactly `k` occurrences.

Initialize:

```
dp[0][0] = 0
```
4. Process positions from left to right.

At position `i`, there are two choices.

Skip the position:

```
dp[i+1][k] = min(dp[i+1][k], dp[i][k])
```

Take the occurrence interval starting at `i`:

```
dp[end[i]+1][k+1]
    = min(dp[end[i]+1][k+1],
          dp[i][k] + cost[i])
```

Jumping directly to `end[i]+1` guarantees that chosen occurrences are disjoint.
5. After all transitions, `dp[n][k]` equals the minimum mandatory deletions needed for exactly `k` occurrences.
6. Convert these minima into answers for every deletion count.

If `dp[n][k] = d`, then:

```
mandatory deletions = d
maximum deletions preserving k copies = n - k*m
```

Every deletion count in the interval

```
[d, n - k*m]
```

is achievable.

For each such deletion count, update the answer with `k`.

### Why it works

Each chosen occurrence corresponds to an interval whose interior must be cleaned of all characters not used by the match. The DP explicitly accumulates those mandatory deletions and forbids overlap by jumping past the interval's end.

Any character outside the chosen occurrence intervals does not affect whether the occurrences exist. Such characters can be kept or deleted independently. Because of that, the DP only needs to minimize mandatory deletions. Once those are fixed, every larger deletion count up to `n - km` is achievable by deleting additional outside characters.

The DP explores every valid set of non-overlapping occurrence intervals and records the smallest mandatory deletion cost for each number of occurrences. That is exactly the quantity needed to derive all answers.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    s = input().strip()
    p = input().strip()

    n = len(s)
    m = len(p)

    # next occurrence table
    nxt = [[n] * 26 for _ in range(n + 2)]

    for c in range(26):
        nxt[n][c] = n

    for i in range(n - 1, -1, -1):
        nxt[i] = nxt[i + 1][:]
        nxt[i][ord(s[i]) - 97] = i

    end = [-1] * n
    cost = [0] * n

    for i in range(n):
        if s[i] != p[0]:
            continue

        pos = i
        ok = True

        for j in range(1, m):
            pos = nxt[pos + 1][ord(p[j]) - 97]
            if pos == n:
                ok = False
                break

        if ok:
            end[i] = pos
            cost[i] = (pos - i + 1) - m

    INF = 30000

    dp = [array('H', [INF]) * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(n):
        cur = dp[i]
        nxt_row = dp[i + 1]

        for k in range(n + 1):
            val = cur[k]
            if val == INF:
                continue

            if val < nxt_row[k]:
                nxt_row[k] = val

            if end[i] != -1:
                r = end[i] + 1
                nv = val + cost[i]
                if nv < dp[r][k + 1]:
                    dp[r][k + 1] = nv

    min_del = dp[n]

    ans = [0] * (n + 1)

    for k in range(n + 1):
        d = min_del[k]
        if d == INF:
            continue

        max_del = n - k * m
        if max_del < d:
            continue

        for x in range(d, max_del + 1):
            if k > ans[x]:
                ans[x] = k

    print(*ans)

solve()
```

The next-occurrence table allows us to find the earliest ending position of a subsequence match in `O(m)` time for each starting position. Since there are at most 2000 starts and `m ≤ 500`, this preprocessing costs `O(nm)`.

The DP stores minimum mandatory deletions. The transition that jumps from `i` directly to `end[i] + 1` is the mechanism that prevents overlap. Two occurrences can never share characters because the second one is forced to start after the first interval ends.

The final conversion step is where many incorrect solutions fail. Knowing the minimum deletions for `k` occurrences is not enough. We must also respect the upper bound `n - km`, because each occurrence needs `m` surviving characters.

## Worked Examples

### Sample 1

Input:

```
s = "aaaaa"
p = "aa"
```

The occurrence intervals are:

| Start | End | Cost |
| --- | --- | --- |
| 0 | 1 | 0 |
| 1 | 2 | 0 |
| 2 | 3 | 0 |
| 3 | 4 | 0 |

Key DP states:

| Position | Occurrences | Min mandatory deletions |
| --- | --- | --- |
| 0 | 0 | 0 |
| 2 | 1 | 0 |
| 4 | 2 | 0 |
| 5 | 2 | 0 |

The DP finds:

| k | minDel[k] |
| --- | --- |
| 0 | 0 |
| 1 | 0 |
| 2 | 0 |

For `k = 2`, the achievable deletion range is:

```
[0, 5 - 2*2] = [0, 1]
```

So deletion counts `0` and `1` can still keep two occurrences.

Final output:

```
2 2 1 1 0 0
```

This example shows that extra deletions outside occurrence intervals are allowed.

### Example 2

Input:

```
s = "abca"
p = "aa"
```

Occurrence intervals:

| Start | End | Cost |
| --- | --- | --- |
| 0 | 3 | 2 |

The interval length is 4, while the pattern length is 2, so two deletions are mandatory.

DP result:

| k | minDel[k] |
| --- | --- |
| 0 | 0 |
| 1 | 2 |

For one occurrence:

```
deletion range = [2, 4 - 2] = [2, 2]
```

Only exactly two deletions can keep one copy of `"aa"`.

The answers become:

```
0 0 1 0 0
```

This demonstrates why merely checking whether `minDel[k] ≤ x` is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n² + nm)` | DP is `O(n²)`, interval construction is `O(nm)` |
| Space | `O(n²)` | DP table of size `(n+1) × (n+1)` |

With `n ≤ 2000`, the DP performs about four million state updates, which comfortably fits within the limits. The memory usage also stays within the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from array import array

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    s = input().strip()
    p = input().strip()

    n = len(s)
    m = len(p)

    nxt = [[n] * 26 for _ in range(n + 2)]
    for i in range(n - 1, -1, -1):
        nxt[i] = nxt[i + 1][:]
        nxt[i][ord(s[i]) - 97] = i

    end = [-1] * n
    cost = [0] * n

    for i in range(n):
        if s[i] != p[0]:
            continue

        pos = i
        ok = True

        for j in range(1, m):
            pos = nxt[pos + 1][ord(p[j]) - 97]
            if pos == n:
                ok = False
                break

        if ok:
            end[i] = pos
            cost[i] = (pos - i + 1) - m

    INF = 30000
    dp = [array('H', [INF]) * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(n):
        for k in range(n + 1):
            v = dp[i][k]
            if v == INF:
                continue

            if v < dp[i + 1][k]:
                dp[i + 1][k] = v

            if end[i] != -1:
                r = end[i] + 1
                nv = v + cost[i]
                if nv < dp[r][k + 1]:
                    dp[r][k + 1] = nv

    ans = [0] * (n + 1)

    for k in range(n + 1):
        d = dp[n][k]
        if d == INF:
            continue

        mx = n - k * m
        if mx < d:
            continue

        for x in range(d, mx + 1):
            ans[x] = max(ans[x], k)

    return " ".join(map(str, ans))

# provided sample
assert run("aaaaa\naa\n") == "2 2 1 1 0 0"

# minimum size
assert run("a\na\n") == "1 0"

# pattern impossible
assert run("abc\nd\n") == "0 0 0 0"

# exact deletion bound
assert run("aa\naa\n") == "1 0 0"

# subsequence but not substring
assert run("abca\naa\n") == "0 0 1 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / a` | `1 0` | Smallest valid input |
| `abc / d` | `0 0 0 0` | Pattern cannot be formed |
| `aa / aa` | `1 0 0` | Upper deletion bound `n - km` |
| `abca / aa` | `0 0 1 0 0` | Subsequence matching with mandatory deletions |

## Edge Cases

Consider:

```
aa
aa
```

The DP finds one occurrence with mandatory deletion cost `0`. The maximum deletion count preserving that occurrence is also `0`, because both characters are required. The achievable range is `[0, 0]`. For deletion count `1`, the answer correctly becomes `0`.

Now consider:

```
abca
aa
```

The earliest occurrence interval is `[0, 3]`. Its length is `4`, while the pattern length is `2`, so two deletions are unavoidable. The DP records `minDel[1] = 2`. Since `n - km = 2`, the only achievable deletion count for one occurrence is exactly `2`.

Finally:

```
aaaaa
aa
```

There are many overlapping ways to choose occurrences. The DP never allows overlap because selecting an interval jumps directly to the position after its end. Two chosen occurrences are always disjoint, matching the problem's requirement of non-overlapping copies in the final string.
