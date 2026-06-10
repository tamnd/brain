---
title: "CF 1566B - MIN-MEX Cut"
description: "We are given a binary string and may split it into any number of contiguous pieces. Every character must belong to exactly one piece. For each piece, we compute its MEX."
date: "2026-06-10T11:56:24+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1566
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 16"
rating: 800
weight: 1566
solve_time_s: 308
verified: false
draft: false
---

[CF 1566B - MIN-MEX Cut](https://codeforces.com/problemset/problem/1566/B)

**Rating:** 800  
**Tags:** bitmasks, constructive algorithms, dp, greedy  
**Solve time:** 5m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string and may split it into any number of contiguous pieces. Every character must belong to exactly one piece.

For each piece, we compute its MEX. Since the string contains only `0` and `1`, there are only three possible values:

| Piece contents | MEX |
| --- | --- |
| Contains no `0` | 0 |
| Contains `0` but no `1` | 1 |
| Contains both `0` and `1` | 2 |

Our goal is to choose the cuts so that the sum of the MEX values of all pieces is as small as possible.

The total length over all test cases is at most $10^5$. That means we should expect a solution close to linear time. Quadratic approaches would require around $10^{10}$ operations in the worst case, which is far beyond the limit.

The tricky part is understanding when cutting helps and when it hurts.

Consider the string `1111`. The whole string contains only `1`s, so its MEX is `0`. The answer is `0`. A solution that always tries to create more pieces would miss this.

Consider the string `0000`. The whole string contains only `0`s, so its MEX is `1`. The answer is `1`. Splitting it into several all-zero pieces gives MEX `1` for each piece and only increases the sum.

Consider the string `01010`. The whole string contains both digits, so its MEX is `2`. A careless observation might suggest that every string containing both digits has answer `2`. That is false. We can cut it as `0 | 1010`, giving `1 + 1 = 2`, but we cannot do better.

Now consider `100001`. The whole string has MEX `2`, but cutting as `1 | 0000 | 1` gives `0 + 1 + 0 = 1`. The answer becomes `1`. Understanding why this happens is the key insight of the problem.

## Approaches

A brute-force solution would try every possible set of cut positions. A string of length $n$ has $n-1$ potential cut locations, and each location may or may not contain a cut. That gives $2^{n-1}$ partitions.

For each partition we could compute the MEX of every piece and keep the minimum sum. This is correct because it examines every valid answer, but it becomes impossible even for $n=50$, let alone $10^5$.

To find a pattern, let us look at what contributes positive cost.

Any piece containing only `1`s has MEX `0`, so such pieces are free.

Any piece containing at least one `0` costs at least `1`.

This immediately suggests that the only characters we really care about are the zeros.

Suppose all zeros belong to a single contiguous block, for example `111000111`. We can isolate the zero block and surround it with all-one pieces:

`111 | 000 | 111`

The cost is `0 + 1 + 0 = 1`.

Now suppose the string has two separate zero blocks, for example `0011100`.

The two zero groups cannot be merged into one all-zero piece because there are ones between them. We have two choices.

We can keep everything together, producing one piece containing both digits and paying `2`.

Or we can isolate both zero groups:

`00 | 111 | 00`

which costs `1 + 0 + 1 = 2`.

Either way the answer is `2`.

This observation completely characterizes the problem.

If there are no zeros at all, the answer is `0`.

If there is exactly one contiguous block of zeros, the answer is `1`.

If there are two or more zero blocks, the answer is `2`.

Nothing larger than `2` is ever optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the binary string.
2. Count how many contiguous blocks of `0` appear in the string.
3. If the number of zero blocks is `0`, output `0`.

The string consists entirely of `1`s, so the whole string has MEX `0`.
4. If the number of zero blocks is `1`, output `1`.

We can isolate that zero block into one piece containing only zeros. All remaining pieces contain only ones and contribute zero cost.
5. If the number of zero blocks is at least `2`, output `2`.

At least two separate zero groups exist. They cannot be merged into a single all-zero piece because ones separate them. The best possible cost is exactly `2`.

### Why it works

The crucial property is that every piece containing a zero contributes at least `1` to the answer.

If the string contains one zero block, all zeros can be placed inside a single all-zero piece, giving total cost `1`.

If the string contains multiple zero blocks, we have two possibilities. We may keep some ones together with the zeros, creating a piece whose MEX is `2`, or isolate the zero blocks and pay `1` for each relevant piece. Either strategy achieves cost `2`, and no strategy can achieve cost `1` because a single all-zero piece cannot cover multiple separated zero blocks.

Thus the answer depends only on the number of zero blocks:

$$\min(2,\text{number of zero blocks})$$

with the special case that zero blocks equal to zero produces answer `0`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        s = input().strip()

        blocks = 0
        n = len(s)

        for i in range(n):
            if s[i] == '0' and (i == 0 or s[i - 1] == '1'):
                blocks += 1

        ans.append(str(min(blocks, 2)))

    sys.stdout.write("\n".join(ans))

solve()
```

The implementation only counts contiguous zero segments.

A new zero block starts whenever we see a `0` whose previous character is either absent or equal to `1`. That condition identifies the first character of every zero run.

Once the number of zero blocks is known, the answer is simply `min(blocks, 2)`. This compact formula covers all cases naturally:

If `blocks = 0`, the result is `0`.

If `blocks = 1`, the result is `1`.

If `blocks >= 2`, the result is `2`.

No additional handling is required.

## Worked Examples

### Example 1

Input string: `01100`

| Index | Character | New zero block? | Blocks |
| --- | --- | --- | --- |
| 0 | 0 | Yes | 1 |
| 1 | 1 | No | 1 |
| 2 | 1 | No | 1 |
| 3 | 0 | Yes | 2 |
| 4 | 0 | No | 2 |

Final value: `blocks = 2`

Answer: `min(2, 2) = 2`

This example shows two separated zero groups. No matter how we cut the string, the minimum achievable cost is `2`.

### Example 2

Input string: `100001`

| Index | Character | New zero block? | Blocks |
| --- | --- | --- | --- |
| 0 | 1 | No | 0 |
| 1 | 0 | Yes | 1 |
| 2 | 0 | No | 1 |
| 3 | 0 | No | 1 |
| 4 | 0 | No | 1 |
| 5 | 1 | No | 1 |

Final value: `blocks = 1`

Answer: `min(1, 2) = 1`

The zeros form one contiguous segment. Cutting as `1 | 0000 | 1` achieves cost `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each character is examined once |
| Space | $O(1)$ | Only a few counters are stored |

Since the total input length across all test cases is at most $10^5$, a single linear scan per string easily fits within the time limit. Memory usage remains constant regardless of string length.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        s = input().strip()

        blocks = 0
        for i, ch in enumerate(s):
            if ch == '0' and (i == 0 or s[i - 1] == '1'):
                blocks += 1
```
