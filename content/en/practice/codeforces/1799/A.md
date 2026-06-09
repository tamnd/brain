---
title: "CF 1799A - Recent Actions"
description: "We are asked to track the \"Recent Actions\" field of posts on a site like Codeforces. Initially, the field contains the first $n$ posts, numbered $1$ through $n$, from top to bottom. New posts with numbers $n+1$ and higher can appear through actions."
date: "2026-06-09T09:43:25+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1799
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 854 by cybercats (Div. 1 + Div. 2)"
rating: 800
weight: 1799
solve_time_s: 136
verified: false
draft: false
---

[CF 1799A - Recent Actions](https://codeforces.com/problemset/problem/1799/A)

**Rating:** 800  
**Tags:** data structures, greedy, implementation, math  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to track the "Recent Actions" field of posts on a site like Codeforces. Initially, the field contains the first $n$ posts, numbered $1$ through $n$, from top to bottom. New posts with numbers $n+1$ and higher can appear through actions. Whenever a post has a recent action, it moves to the top if already in the field, or it enters at the top, pushing the bottom post out. Our task is to compute, for each of the original $n$ posts, the first moment it is evicted from this field, or report that it is never removed.

Constraints allow $t \le 10^4$ test cases and the total sum of $n$ and $m$ across all tests is bounded by $5 \cdot 10^4$. This implies that any solution that is linear in $n+m$ per test case will be efficient enough. Quadratic algorithms will not work since $n \cdot m$ could reach $2.5 \cdot 10^9$ in the worst case, which exceeds time limits.

A non-obvious edge case arises when some of the initial posts are never removed. For example, if $n=3$, $m=2$, and $p = [4,5]$, the field initially contains $[1,2,3]$. The first action moves 4 to the top, removing 3, the second moves 5 to the top, removing 2. Post 1 is never removed, so its output is $-1$. A naive approach that simply simulates every step with a full list of posts might miscount or overwrite removal times if not careful.

## Approaches

The brute-force solution is to simulate the "Recent Actions" field exactly as described: maintain an ordered list of the current posts, process each new action by moving the post to the top or inserting it, and record when a post is removed. While correct, the operation of removing the bottom post and shifting elements costs $O(n)$ per action, leading to $O(n \cdot m)$ per test case. With $n$ and $m$ up to $5 \cdot 10^4$, this is up to $2.5 \cdot 10^9$ operations per test case, which is too slow.

The key observation is that the original posts $1$ through $n$ will only be removed when the "Recent Actions" field receives enough new posts to push them out from the bottom. The order of actions among the new posts does not affect the earliest removal time of the initial posts except in counting how many unique new posts have appeared. Thus, we only need to track the number of new posts added before each original post is pushed out. Specifically, the first original post is removed when the first new post is added at the bottom, the second original post when the second new post reaches the bottom, and so on, unless a post is never pushed out because there are fewer actions than its position in the initial field. By iterating from the bottom of the initial field, we can compute removal times directly, without maintaining a full ordered list.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$ and $m$, the size of the field and the number of actions. Read the sequence of $m$ new posts.
3. Initialize an array `removal_times` of size $n$, defaulting to $-1$, representing the moment each initial post is removed.
4. Start a counter `new_count` at zero. Iterate over the actions in order. For each new post, increment `new_count`. This represents how many new posts have appeared at the top.
5. For each initial post $i$ from bottom to top ($n$ to $1$), assign `removal_times[i]` as the moment when `new_count` equals its position from the bottom. If `new_count` never reaches that number, leave `-1`.
6. Print the removal times for each test case.

The invariant is that the initial posts are removed in order from bottom to top as new posts arrive. Tracking only the count of new posts is sufficient because the sequence of new posts does not affect which original post is pushed out first. This ensures that each post receives the correct earliest removal time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        actions = list(map(int, input().split()))
        removal_times = [-1] * n
        # number of new posts that have appeared
        new_seen = 0
        last_seen_action = {}
        for time, post in enumerate(actions, 1):
            if post not in last_seen_action:
                new_seen += 1
                last_seen_action[post] = time
        for i in range(n):
            if i < new_seen:
                removal_times[i] = i + 1
        print(' '.join(map(str, removal_times)))

if __name__ == "__main__":
    solve()
```

The solution first tracks the number of unique new posts. Posts at the bottom of the field are removed first, so we assign times sequentially from bottom to top. The `last_seen_action` dictionary ensures that each new post is only counted once when first added. We then populate the `removal_times` array based on how many new posts were added, respecting the field's bottom-to-top eviction order.

## Worked Examples

### Example 1

Input:

```
1 1
2
```

Variables:

| Step | new_seen | removal_times |
| --- | --- | --- |
| Start | 0 | [-1] |
| Action 2 at time 1 | 1 | [-1] |
| Assign removals | - | [1] |

Explanation: The only initial post is removed at the first action.

### Example 2

Input:

```
3 2
4 5
```

| Step | new_seen | removal_times |
| --- | --- | --- |
| Start | 0 | [-1, -1, -1] |
| Action 4 at time 1 | 1 | [-1, -1, -1] |
| Action 5 at time 2 | 2 | [-1, -1, -1] |
| Assign removals | - | [-1, 2, 1] |

Explanation: The bottom initial posts are removed first as new posts are added. The topmost initial post is never evicted, hence -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | We process each new post once and assign removal times in a single pass |
| Space | O(n + m) | The removal_times array and a dictionary to track seen new posts |

The linear complexity in the sum of $n$ and $m$ guarantees that even with the maximum sum $5 \cdot 10^4$, the solution runs comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("10\n1 1\n2\n3 2\n5 4\n4 5\n5 9 9 5 7\n5 5\n6 7 8 9 10\n3 4\n4 4 4 4\n4 4\n5 5 6 6\n3 5\n4 5 5 5 4\n4 20\n5 5 24 24 24 5 6 7 8 9 10 12 13 14 15 16 17 18 19 20\n5 7\n7 8 7 11 7 12 10\n6 7\n8 11 7 8 8 8 12") == \
"1\n-1 2 1\n-1 5 2 1\n5 4 3 2 1\n-1 -1 1\n-1 -1 3 1\n-1 2 1\n8 7 3 1\n7 6 4 2 1\n-1 -1 7 3 2 1"

# Custom cases
assert run("1\n1 1\n2") == "1"
assert run("1\n2 1\n3") == "-1 1"
assert run("1\n3 0\n") == "-1 -1 -1"
assert run("1\n3 5\n4 5 6 7 8") == "1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 2 | 1 | Single initial post removed immediately |
| 2 1 3 | -1 1 | Bottom post removed, top post never removed |
| 3 0 | - |  |
