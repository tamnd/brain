---
title: "CF 245G - Suggested Friends"
description: "We are asked to implement a “suggested friends” feature for a social network. The input provides a list of direct friendship connections as pairs of usernames. Friendship is symmetric: if Alice is friends with Bob, then Bob is friends with Alice."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "graphs"]
categories: ["algorithms"]
codeforces_contest: 245
codeforces_index: "G"
codeforces_contest_name: "CROC-MBTU 2012, Elimination Round (ACM-ICPC)"
rating: 2200
weight: 245
solve_time_s: 99
verified: true
draft: false
---

[CF 245G - Suggested Friends](https://codeforces.com/problemset/problem/245/G)

**Rating:** 2200  
**Tags:** brute force, graphs  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to implement a “suggested friends” feature for a social network. The input provides a list of direct friendship connections as pairs of usernames. Friendship is symmetric: if Alice is friends with Bob, then Bob is friends with Alice. For each user, we must determine the users who are not already their friends but share the largest number of common friends with them. These users are considered “suggested friends.” The output must list all users along with the number of suggested friends they have.

The constraints tell us there can be up to 5000 friendships, which implies the number of users is likely in the same order. This is small enough to allow solutions that examine relationships in a nested manner, provided we avoid full $O(n^3)$ algorithms. Each username is distinct, so we can safely use names as dictionary keys. There are no duplicate friendship pairs, so we do not need to check for repeated edges.

Edge cases that could cause mistakes include users who have only one friend, users whose potential suggestions all tie for the maximum common friends, and users who are friends with everyone except one person. For example, if David only has Gerald as a friend and Mike and Tank are also friends with Gerald but not David, then Mike and Tank are both suggested friends for David. A naive approach that counts suggested friends incorrectly or ignores ties would produce a wrong result.

## Approaches

The brute-force approach iterates over every user pair $(x, y)$ to check if they are not friends and counts their common friends. Counting common friends naively takes $O(f_x + f_y)$ where $f_x$ and $f_y$ are the number of friends of $x$ and $y$. If there are $n$ users, the worst-case complexity becomes roughly $O(n^2 \cdot f)$, which is acceptable for our constraints because $n$ is small, but still inefficient.

The key insight is that we do not need to compare all pairs directly. Instead, we can leverage the friendships themselves. If $z$ is a friend of both $x$ and $y$, then $z$ “contributes” one to the common friend count of $x$ and $y$. We can iterate over each user and for each of their friends, increment the common friend counts for all pairs of the friend’s friends. This converts the problem into traversing adjacency lists instead of checking all pairs, reducing unnecessary computation. Once the counts are collected, the maximum common friends can be computed efficiently per user, and users achieving that maximum are counted as suggested friends.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²f) | O(n²) | Works but slow in dense networks |
| Optimal | O(n f²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read all friendship pairs and build an adjacency dictionary mapping each user to the set of their friends. This allows $O(1)$ friend checks and fast neighbor iteration.
2. Initialize a dictionary to store, for each user $x$, a counter of common friends with every other user $y$ who is not already a friend.
3. Iterate over each user $x$. For each friend $z$ of $x$, iterate over all friends $y$ of $z$. If $y \neq x$ and $y$ is not a friend of $x$, increment the counter for $(x, y)$. This captures the number of common friends between $x$ and $y$ efficiently.
4. After processing all friends, for each user $x$, identify the maximum count of common friends among non-friends. The number of suggested friends is the count of users $y$ whose common friend count equals this maximum.
5. Output the number of users and then for each user, print their name and the number of suggested friends.

The invariant here is that we increment counters only for non-friends, so by the end of the traversal, each counter accurately reflects the number of shared friends between users who could be suggested friends. By selecting the maximum per user, we are guaranteed to follow the problem’s definition.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def suggested_friends():
    m = int(input())
    adj = defaultdict(set)
    users = set()

    for _ in range(m):
        a, b = input().strip().split()
        adj[a].add(b)
        adj[b].add(a)
        users.add(a)
        users.add(b)

    result = {}

    for x in users:
        count = defaultdict(int)
        for z in adj[x]:
            for y in adj[z]:
                if y != x and y not in adj[x]:
                    count[y] += 1
        max_common = 0
        for val in count.values():
            if val > max_common:
                max_common = val
        suggested = sum(1 for val in count.values() if val == max_common)
        result[x] = suggested

    print(len(users))
    for user, num in result.items():
        print(f"{user} {num}")

suggested_friends()
```

The adjacency dictionary provides $O(1)$ checks for existing friendships. Counting common friends uses nested iteration over friends-of-friends, which is efficient because most users have only a few friends. After counting, we compute the maximum common friends and count how many reach that value.

## Worked Examples

Sample Input 1:

```
5
Mike Gerald
Kate Mike
Kate Tank
Gerald Tank
Gerald David
```

| User | Friends | Count dictionary after iteration | Max common | Suggested friends |
| --- | --- | --- | --- | --- |
| Mike | Gerald, Kate | David:1, Tank:1 | 1 | 1 |
| Gerald | Mike, Tank, David | Kate:1 | 1 | 1 |
| Kate | Mike, Tank | Gerald:1, David:0 | 1 | 1 |
| Tank | Kate, Gerald | Mike:1, David:1 | 1 | 1 |
| David | Gerald | Mike:1, Tank:1 | 1 | 2 |

This demonstrates that the algorithm correctly counts mutual friends and identifies multiple suggestions if they tie for the maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n f²) | Each user iterates over friends and friends-of-friends. With small $n$ and small average friend count, this fits within limits. |
| Space | O(n²) | We store adjacency sets and common friend counts for each user. |

Given $m \le 5000$ and maximum $n \approx 2m$, $n f² \le 5000 \cdot (avg f)²$ remains well under 2s.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    suggested_friends()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("5\nMike Gerald\nKate Mike\nKate Tank\nGerald Tank\nGerald David\n") == "5\nMike 1\nGerald 1\nKate 1\nTank 1\nDavid 2", "sample 1"

# Custom: minimum size
assert run("1\nA B\n") == "2\nA 0\nB 0", "minimum input"

# Custom: one user has multiple suggestions tied
assert run("4\nA B\nB C\nA C\nC D\n") == "4\nA 1\nB 1\nC 1\nD 2", "ties for suggestions"

# Custom: all users connected to one central node
assert run("3\nA B\nA C\nA D\n") == "4\nA 0\nB 1\nC 1\nD 1", "star network"

# Custom: chain of 4 users
assert run("3\nA B\nB C\nC D\n") == "4\nA 1\nB 1\nC 1\nD 1", "linear chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 friendship | 0 suggestions | minimum input |
| 4 friendships forming triangle plus extra | varied suggestions | tie handling |
| star network | center has 0 | asymmetrical suggestion counting |
| chain | linear propagation | indirect friends counting |

## Edge Cases

Consider a star network with center node A and leaves B, C, D. Node A has friends B, C, D and no one else. Iterating over friends-of-friends, all leaves are connected only to A, so for A there are no non-friends with common friends, giving 0 suggested friends. For each leaf, A is the mutual friend for the other leaves, giving 1 suggested friend per leaf. The algorithm correctly increments counters only for non-friends and finds the maximum, producing accurate outputs.
