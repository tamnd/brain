---
title: "CF 105826F - \u041b\u044f\u0433\u0443\u0448\u043a\u0430 \u0438 \u0441\u0442\u0440\u043e\u043a\u0430"
description: "The problem describes a frog moving along a string. Every position contains one character, and characters belong to one of three categories: lowercase letters, uppercase letters, or digits. The frog starts at the first position and wants to reach the last one."
date: "2026-06-25T14:58:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105826
codeforces_index: "F"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u043d\u0430 \u0412\u041a\u041e\u0428\u041f.Junior 2025"
rating: 0
weight: 105826
solve_time_s: 29
verified: true
draft: false
---

[CF 105826F - \u041b\u044f\u0433\u0443\u0448\u043a\u0430 \u0438 \u0441\u0442\u0440\u043e\u043a\u0430](https://codeforces.com/problemset/problem/105826/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a frog moving along a string. Every position contains one character, and characters belong to one of three categories: lowercase letters, uppercase letters, or digits. The frog starts at the first position and wants to reach the last one. A jump can move the frog forward by at most `k` positions, but the frog is only allowed to land on positions containing the same category of character as its current position.

The task is to find the minimum number of jumps needed to reach the end, or report that it is impossible.

The input gives the length of the string, the maximum jump length, and the string itself. The output is the smallest number of valid jumps needed to move from the first character to the last character.

The length of the string can reach 200,000. That immediately rules out solutions that repeatedly try every possible path, because the number of possible routes can grow exponentially. Even an approach that checks every pair of positions can become around `n²`, which is about 40 billion operations at the upper bound and far beyond what a normal time limit allows.

The key is that the frog only moves to the right. There are no cycles, so we can process positions in order and keep only the information that matters for future jumps.

A few cases are easy to miss.

If the first and last characters have different categories, the answer is impossible. For example:

```
5 3
aB123
```

The first character is a lowercase letter, while the last character is a digit. The frog can never change category, so the correct answer is:

```
-1
```

A careless implementation might only check whether some positions of the correct type exist near the end, but that is not enough because the frog must preserve its category throughout the whole path.

Another tricky case is when the correct category exists, but there is a gap larger than `k`.

Example:

```
6 2
aaabca
```

The first and last characters are lowercase letters, but the lowercase positions are:

`1, 2, 3, 6`

The jump from position 3 to position 6 is length 3, which is too large. The answer is:

```
-1
```

An implementation that counts only how many valid positions exist would incorrectly think a path exists.

A final edge case is when every useful jump is exactly the maximum allowed length.

Example:

```
7 3
aaaaaaa
```

The frog can jump:

`1 -> 4 -> 7`

so the answer is:

```
2
```

Using a strict `< k` comparison instead of `<= k` would fail here.

## Approaches

The straightforward way to solve the problem is to simulate all possible movements. From every reachable position, we try every next position within distance `k`, check whether its character has the same category, and continue. This is correct because every possible path is explored.

The problem is the amount of work. In the worst case, every position can try almost `k` next positions. Since both `n` and `k` can be close to 200,000, this becomes roughly `O(nk)`, which is far too large.

The useful observation comes from the fact that all jumps go only forward. We do not need to know every possible path. We only need the best answer for the latest reachable position of each character category.

Suppose we are currently at a position of some category. Any future position of that same category can be reached from the farthest reachable position behind it, because that gives the largest remaining jump distance. If the farthest reachable position is at least `i - k`, then the current position is reachable.

This transforms the problem into a single scan. While moving from left to right, we keep the last reachable position for each of the three categories. Whenever we encounter a character, we check whether the previous reachable position of its category is close enough. If it is, we update the number of jumps needed and mark this position as reachable.

The three categories can be compressed into three states. There is no need for maps or complex data structures because the alphabet groups are fixed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert every character into one of three category identifiers. Lowercase letters, uppercase letters, and digits each get their own state. This lets the algorithm compare categories without caring about the actual characters.
2. Start at the first position. It is always reachable with zero jumps, so store it as the latest reachable position for its category.
3. Scan the string from left to right. For every position, look at the most recent reachable position with the same category.

If that position is within `k` characters behind the current one, the frog can jump there. The current position becomes reachable.
4. When a position becomes reachable, update the number of jumps needed to get there. The minimum jump count is found by taking the previous position's answer and adding one.

The stored reachable positions are always the furthest possible ones for their categories. A farther reachable position is always at least as useful as a closer one because it leaves the frog with more distance available for the next jump.
5. After processing the whole string, check whether the last position was reachable. If not, print `-1`.

Why it works:

The invariant is that after processing any prefix of the string, for each category we store the furthest position in that prefix that the frog can reach, together with the minimum number of jumps needed to get there. When we process a new position, any valid previous jump must come from the same category. The furthest reachable position is the only one that matters because if it cannot reach the current position, no earlier position can. If it can reach the current position, using it gives the smallest possible number of jumps. This keeps the invariant true for every position and guarantees the final answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    def get_type(c):
        if 'a' <= c <= 'z':
            return 0
        if 'A' <= c <= 'Z':
            return 1
        return 2

    last = [-1, -1, -1]
    dist = [-1] * n

    dist[0] = 0
    last[get_type(s[0])] = 0

    for i in range(1, n):
        t = get_type(s[i])

        if last[t] != -1 and i - last[t] <= k:
            dist[i] = dist[last[t]] + 1
            last[t] = i

    print(dist[-1])

if __name__ == "__main__":
    solve()
```

The `get_type` function reduces every character to one of three states. This avoids repeatedly checking ranges throughout the algorithm and keeps the main loop simple.

The `last` array stores the furthest reachable position for each category. Updating it only when a position is reachable is necessary, because an unreachable position cannot help future jumps.

The distance array stores the minimum number of jumps required to reach every position. When we find a valid jump, the current answer is exactly one more than the answer of the previous reachable position.

The boundary check uses `<= k` because a jump of exactly length `k` is allowed. Positions are processed from left to right, so there is no need for backward movement or revisiting states.
