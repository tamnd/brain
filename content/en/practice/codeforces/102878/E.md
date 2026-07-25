---
title: "CF 102878E - Eigen Substring"
description: "We are given a lowercase string s. A substring of a string is called an eigen substring when that exact sequence of characters appears only once inside the string. The task is to look at every prefix of s and find the length of the shortest eigen substring inside that prefix."
date: "2026-07-25T12:43:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102878
codeforces_index: "E"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 102878
solve_time_s: 41
verified: true
draft: false
---

[CF 102878E - Eigen Substring](https://codeforces.com/problemset/problem/102878/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase string `s`. A substring of a string is called an eigen substring when that exact sequence of characters appears only once inside the string. The task is to look at every prefix of `s` and find the length of the shortest eigen substring inside that prefix.

For example, when the prefix is `ababb`, the substring `b` is not valid because it appears several times, but `ba` is valid because it occurs only once. The answer for this prefix is `2`.

The input contains the length of the string and the string itself. The output contains one number for every prefix, where the number describes the shortest substring that appears exactly once in that prefix.

The length of the string can reach `10^6`. A solution that enumerates substrings cannot work because a string of this size has about `n²/2` substrings. Even storing and checking every possible substring would already require around `10^12` operations. The solution must process each character a constant or logarithmic number of times.

The difficult cases are not only long strings. Repeated patterns are where incorrect solutions usually fail. A substring that was unique can stop being unique after appending more characters, and a substring that was not unique can become irrelevant because a longer substring becomes unique.

For example:

```
1
a
```

The answer is:

```
1
```

The only substring is `a`, and it appears once.

Another example:

```
4
aaaa
```

The answers are:

```
1
2
3
4
```

After the first character, `a` is unique. After the second character, `a` appears twice, so `aa` is the shortest unique substring. The same reasoning continues as the string grows. A solution that only checks the newest suffix would miss that previous substrings can lose uniqueness.

A final important case is a string with many different characters:

```
5
abcde
```

The answer is:

```
1
1
1
1
1
```

Every single character is already unique, so longer substrings should never replace them.

## Approaches

A direct approach would generate every substring of the current prefix, count how many times each one appears, and keep the shortest one with count one. This is correct because it follows the definition exactly. The problem is the cost. For a prefix of length `n`, there are `O(n²)` substrings, and checking their occurrences can add another factor. The worst case becomes far beyond what is possible for `n = 10^6`.

The key observation is that substrings do not need to be stored individually. A suffix automaton groups substrings that have identical occurrence behaviour. Each state represents an interval of substring lengths. If a state corresponds to substrings that appear once, every length in that interval is also unique. The shortest candidate represented by a state is `link_length + 1`.

The automaton can be built while scanning the string from left to right. During construction, we maintain the states whose represented substrings are currently unique. When adding a character, some states become non unique and must be removed, while the new state created by the extension becomes a candidate. The minimum value among the remaining candidates is the answer for the current prefix.

The reason this works online is that a suffix automaton state changes from unique to non unique exactly when another occurrence reaches the same equivalence class. The construction process already exposes those changes while following suffix links and handling clones.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n²) | Too slow |
| Suffix Automaton Maintenance | O(n log n) with ordered set | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a suffix automaton while reading the string one character at a time. Each insertion represents adding the current character to the current prefix.
2. Whenever a new automaton state is created, insert its shortest represented substring length into the candidate structure. The state represents a substring family, and the shortest member of that family is the only length that can improve the answer.
3. When the insertion modifies an existing state because its occurrence count is no longer one, remove that state from the candidate structure. A state that has multiple occurrences cannot contribute an eigen substring.
4. If a clone state is created during suffix automaton construction, update the candidate structure for the affected original state because the clone splits the represented substring interval.
5. After processing each character, the smallest stored length is the answer for the current prefix.

The invariant is that the candidate structure contains exactly the shortest lengths of all suffix automaton states whose represented substrings occur once in the current prefix. Every possible eigen substring belongs to one of these states, and every stored candidate is itself an eigen substring. Taking the minimum therefore gives the correct shortest length.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n = int(input())
    s = input().strip()

    nxt = [dict()]
    link = [-1]
    length = [0]

    unique = [False]
    heap = []

    def add_candidate(v):
        if unique[v]:
            heapq.heappush(heap, (length[link[v]] + 1, v))

    def extend(c, last):
        cur = len(nxt)
        nxt.append({})
        length.append(length[last] + 1)
        link.append(0)
        unique.append(True)

        p = last
        while p != -1 and c not in nxt[p]:
            nxt[p][c] = cur
            p = link[p]

        if p == -1:
            link[cur] = 0
        else:
            q = nxt[p][c]
            if length[p] + 1 == length[q]:
                link[cur] = q
                if unique[q]:
                    unique[q] = False
            else:
                clone = len(nxt)
                nxt.append(nxt[q].copy())
                length.append(length[p] + 1)
                link.append(link[q])
                unique.append(unique[q])

                while p != -1 and nxt[p].get(c) == q:
                    nxt[p][c] = clone
                    p = link[p]

                link[q] = clone
                link[cur] = clone

                unique[q] = False
                unique[clone] = False

        add_candidate(cur)
        return cur

    last = 0
    for i, ch in enumerate(s):
        last = extend(ch, last)

        while heap:
            val, state = heap[0]
            if unique[state]:
                break
            heapq.heappop(heap)

        print(heap[0][0])

if __name__ == "__main__":
    solve()
```

The automaton arrays store the transition map, suffix link, and maximum length for every state. The `unique` array represents whether a state can currently produce an eigen substring.

The heap stores possible answers. Lazy deletion is used because many states can become invalid after insertion. Instead of searching and deleting every stale value immediately, invalid entries are removed only when they reach the minimum position.

The expression `length[link[v]] + 1` is the smallest substring length represented by state `v`. The state itself may represent many different lengths, but this is the only value that can improve the current answer.

The clone handling is the most delicate part of the implementation. A clone splits a substring equivalence class, so the previous uniqueness information cannot simply be copied without adjustment.

(Part 2 continues with worked examples, complexity details, and the complete test suite.)
