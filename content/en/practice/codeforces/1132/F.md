---
title: "CF 1132F - Clear the String"
description: "We have a string of lowercase letters. In one operation, we may choose any contiguous block whose characters are all the same and remove it. After removal, the remaining parts of the string join together."
date: "2026-06-12T04:10:22+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1132
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 61 (Rated for Div. 2)"
rating: 2000
weight: 1132
solve_time_s: 102
verified: true
draft: false
---

[CF 1132F - Clear the String](https://codeforces.com/problemset/problem/1132/F)

**Rating:** 2000  
**Tags:** dp  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string of lowercase letters. In one operation, we may choose any contiguous block whose characters are all the same and remove it. After removal, the remaining parts of the string join together.

The goal is to delete the entire string using as few operations as possible.

The key difficulty is that deletions change the structure of the string. Characters that were originally separated can become adjacent after intermediate characters are removed. This means a decision that looks suboptimal locally may create a better opportunity later.

For example, consider:

```
abaca
```

If we delete each character independently, we need five operations. A better strategy is:

```
abaca
delete b  -> aaca
delete both a blocks together after merging -> c
delete c
```

This takes only three operations.

The length of the string is at most 500. That immediately rules out any approach that explicitly explores all deletion sequences. The number of possible deletion orders grows exponentially. With $n=500$, even $O(n^4)$ is already around 62.5 billion operations and far too slow. We need a dynamic programming solution around $O(n^3)$.

Several edge cases are easy to mishandle.

Consider:

```
3
aaa
```

The answer is:

```
1
```

All characters can be deleted at once. A naive DP that always splits intervals may incorrectly produce 3.

Consider:

```
3
aba
```

The answer is:

```
2
```

Delete the middle `b`, then the two `a` characters become adjacent and can be removed together. Any approach that only looks at currently adjacent equal characters misses this possibility.

Consider:

```
4
abab
```

The answer is:

```
3
```

The equal letters cannot all be merged into a single deletion. We must carefully account for which characters can be combined after intermediate deletions.

These examples show that the problem is fundamentally about intervals and future merges.

## Approaches

A brute-force approach would recursively try every valid deletion. For each state, we choose one of the currently removable uniform substrings, delete it, and continue.

This is correct because it explores every possible sequence of operations. Unfortunately, the number of resulting strings grows explosively. Even for moderate lengths, the state space becomes enormous. In the worst case, the running time is exponential.

The structure of the problem suggests something different. The effect of deletions is confined to intervals. Whenever we focus on a substring $s[l..r]$, the optimal way to clear it depends only on that interval.

This naturally leads to interval DP.

Let $dp[l][r]$ denote the minimum number of operations needed to delete the substring $s[l..r]$.

Suppose we want to remove character $s[l]$. One option is to delete it separately and then clear the rest:

$$dp[l][r] = 1 + dp[l+1][r]$$

The interesting observation appears when another occurrence of the same character exists inside the interval.

If $s[l] = s[k]$, then after deleting everything between them, these two equal characters can participate in the same deletion operation. We do not need to pay an extra operation for the character at position $l$.

This gives the transition:

$$dp[l][r] = \min(dp[l][r], dp[l+1][k-1] + dp[k][r])$$

The first term removes everything between the matching characters. After that, position $l$ can merge with the deletion involving position $k$.

This observation converts an exponential search into a cubic interval DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Interval DP | O(n³) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Define `dp[l][r]` as the minimum number of operations required to delete the substring from index `l` to index `r`.
2. Initialize all single-character intervals.

A single character can always be deleted in one operation, so:

```
dp[i][i] = 1
```
3. Process intervals in increasing order of length.

Smaller intervals must be solved before larger ones because larger states depend on them.
4. For each interval `[l, r]`, start with the strategy of deleting `s[l]` separately.

```
dp[l][r] = 1 + dp[l+1][r]
```

This is always valid.
5. Search every position `k` with `l < k ≤ r` such that `s[l] == s[k]`.

Equal characters may be removed together after the middle section disappears.
6. For each such `k`, try merging the deletion of `s[l]` with the deletion containing `s[k]`.

```
cost = dp[l+1][k-1] + dp[k][r]
```

The first term removes everything between the two equal characters. The second term clears the suffix while allowing the character at `l` to join the operation that removes the character at `k`.
7. Keep the minimum value among all possibilities.
8. The final answer is `dp[0][n-1]`.

### Why it works

The DP examines every possible fate of the leftmost character in an interval.

Either that character is deleted alone, which is represented by `1 + dp[l+1][r]`, or it is eventually deleted together with a matching character somewhere to its right. For every matching position `k`, the interval between them must be completely removed first, which costs `dp[l+1][k-1]`. After that, the character at `l` can be absorbed into the same deletion operation as the character at `k`, so no extra operation is needed.

Every valid optimal strategy falls into exactly one of these cases. Since the recurrence takes the minimum over all of them, `dp[l][r]` equals the true optimum for every interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1

            dp[l][r] = 1 + dp[l + 1][r]

            for k in range(l + 1, r + 1):
                if s[l] == s[k]:
                    middle = dp[l + 1][k - 1] if l + 1 <= k - 1 else 0
                    dp[l][r] = min(
                        dp[l][r],
                        middle + dp[k][r]
                    )

    print(dp[0][n - 1])

if __name__ == "__main__":
    solve()
```

The DP table stores answers for every interval. Single-character intervals are initialized to 1 because one operation removes one character.

Intervals are processed by increasing length. This guarantees that whenever we compute `dp[l][r]`, all smaller intervals appearing in the recurrence are already available.

The subtle part is the merge transition. When `s[l] == s[k]`, we do not add an extra operation for position `l`. The character at `l` joins the deletion that eventually removes position `k`. That is exactly why the recurrence uses:

```
middle + dp[k][r]
```

instead of:

```
middle + 1 + dp[k][r]
```

Another easy mistake is handling the empty interval between `l+1` and `k-1`. When `k = l + 1`, that interval has cost zero. The implementation explicitly checks for this case.

The answer is stored in `dp[0][n-1]`, representing the entire string.

## Worked Examples

### Example 1

Input:

```
5
abaca
```

Relevant DP states:

| Interval | Substring | DP Value |
| --- | --- | --- |
| [0,0] | a | 1 |
| [1,1] | b | 1 |
| [2,2] | a | 1 |
| [3,3] | c | 1 |
| [4,4] | a | 1 |
| [0,2] | aba | 2 |
| [2,4] | aca | 2 |
| [0,4] | abaca | 3 |

For the full interval `[0,4]`, the first and last characters are both `a`. After removing the middle parts appropriately, these `a` characters can participate in the same deletion. This reduces the answer from the naive value of 5 down to 3.

### Example 2

Input:

```
3
aaa
```

| Interval | Substring | DP Value |
| --- | --- | --- |
| [0,0] | a | 1 |
| [1,1] | a | 1 |
| [2,2] | a | 1 |
| [0,1] | aa | 1 |
| [1,2] | aa | 1 |
| [0,2] | aaa | 1 |

Every character can merge into the same deletion operation. The recurrence repeatedly finds matching characters and never needs additional operations beyond the first.

This example confirms that the DP correctly handles long runs of equal letters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³) | O(n²) intervals, each scans O(n) matching positions |
| Space | O(n²) | DP table for all intervals |

With $n \le 500$, the DP table contains 250,000 states. The cubic transition count is about 125 million simple operations in the worst case, which is acceptable in optimized Codeforces solutions for this problem and fits comfortably within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1

            dp[l][r] = 1 + dp[l + 1][r]

            for k in range(l + 1, r + 1):
                if s[l] == s[k]:
                    middle = dp[l + 1][k - 1] if l + 1 <= k - 1 else 0
                    dp[l][r] = min(dp[l][r], middle + dp[k][r])

    return str(dp[0][n - 1])

def run(inp: str) -> str:
    return solve_io(inp)

# provided sample
assert run("5\nabaca\n") == "3", "sample 1"

# custom cases
assert run("1\na\n") == "1", "single character"
assert run("3\naaa\n") == "1", "all equal"
assert run("3\naba\n") == "2", "merge after middle deletion"
assert run("4\nabab\n") == "3", "alternating pattern"
assert run("5\nabcde\n") == "5", "all distinct"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a` | `1` | Minimum size input |
| `3 / aaa` | `1` | Complete merging of equal letters |
| `3 / aba` | `2` | Characters become adjacent after deletion |
| `4 / abab` | `3` | Multiple competing merge choices |
| `5 / abcde` | `5` | No merges available |

## Edge Cases

### All characters identical

Input:

```
3
aaa
```

The DP first sets all single-character intervals to 1. When computing `[0,1]`, it notices both ends are `a`, allowing a merge and reducing the answer to 1. The same happens for `[0,2]`.

Final answer:

```
1
```

This case verifies that repeated equal letters are merged into one operation instead of being counted separately.

### Equal characters separated by another character

Input:

```
3
aba
```

The interval `[0,2]` begins and ends with `a`.

The recurrence evaluates:

```
dp[1][1] + dp[2][2]
= 1 + 1
= 2
```

The middle `b` is deleted first. Afterwards the two `a` characters become adjacent and disappear together.

Final answer:

```
2
```

This is exactly the situation that defeats greedy approaches based only on current adjacency.

### No equal characters

Input:

```
5
abcde
```

No merge transition is ever applicable because every character is different.

The DP repeatedly uses:

```
dp[l][r] = 1 + dp[l+1][r]
```

which yields:

```
5
```

Every character must be deleted individually.

### Alternating pattern

Input:

```
4
abab
```

There are matching pairs, but they cannot all be merged into a single operation. The DP explores every matching position and discovers that the best achievable value is:

```
3
```

This case confirms that the recurrence does not overestimate the benefit of matching characters and only performs merges that are actually achievable after intermediate deletions.
