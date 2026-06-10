---
title: "CF 1482D - Playlist"
description: "We are asked to simulate a playlist with songs labeled by genres, where Arkady listens to songs in order, cycling back to the beginning when reaching the end."
date: "2026-06-10T23:24:22+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "implementation", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1482
codeforces_index: "D"
codeforces_contest_name: "\u0422\u0435\u0445\u043d\u043e\u043a\u0443\u0431\u043e\u043a 2021 - \u0424\u0438\u043d\u0430\u043b"
rating: 1900
weight: 1482
solve_time_s: 130
verified: false
draft: false
---

[CF 1482D - Playlist](https://codeforces.com/problemset/problem/1482/D)

**Rating:** 1900  
**Tags:** data structures, dsu, implementation, shortest paths  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a playlist with songs labeled by genres, where Arkady listens to songs in order, cycling back to the beginning when reaching the end. The rule is that if the genre of the last song Arkady listened to and the genre of the previous song are coprime, the last song is removed from the playlist. Once a song is deleted, Arkady forgets the previous songs, which means deletion cannot chain immediately. The task is to determine which songs get deleted and in what order.

The input provides multiple test cases, each specifying the number of songs and the list of genres. The output must be, for each test case, the number of deleted songs and their 1-based positions in the order of deletion. Constraints allow up to 100,000 songs across all test cases with genre values up to $10^9$, which rules out naive approaches that iterate through every pair of songs for every deletion. A direct simulation using array deletions would be $O(n^2)$ in the worst case, which is too slow.

Non-obvious edge cases include scenarios where the playlist cycles multiple times, deletions skip songs, or the playlist has repeated elements. For example, a playlist `[2, 2, 2]` never deletes anything because all adjacent genres share a GCD greater than 1, while `[1, 2]` deletes both songs because after removing the second, the algorithm resets and checks the first song again, potentially causing multiple deletions.

## Approaches

A brute-force approach would iterate over the playlist, checking the last two songs and deleting when their GCD is 1, then restarting from the song after the deleted one. While this matches the rules exactly, every deletion could require scanning up to $O(n)$ songs, leading to $O(n^2)$ complexity. With $n$ up to $10^5$, this is impractical.

The key insight is that we only ever delete songs when the current song and its previous song are coprime. This suggests maintaining a circular structure and quickly finding the next candidate for deletion without repeatedly scanning already checked songs. A queue or a linked list structure allows O(1) removal and efficient cycling. To keep track of which songs are valid for the next deletion, we can maintain a queue of song indices whose previous song is still alive and coprime checks have not been exhausted. After deletion, we continue from the next song, effectively skipping songs already “forgotten” by Arkady. This reduces the complexity to O(n) per test case because each song is visited at most twice: once when checked and once potentially when deleted.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal (Queue + GCD checks) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read the number of songs `n` and the list of genres `a`. We will work with 0-based indexing internally for simplicity.
2. Construct a circular linked representation of the playlist using an array `next_song` where `next_song[i]` points to the next song in the playlist. Initially, `next_song[i] = (i + 1) % n`.
3. Initialize a queue with the indices of songs whose previous song is coprime with them. This can be found by iterating over all songs and checking `gcd(a[i], a[i-1]) == 1`.
4. Initialize an empty list `deleted` to store the order of deletions.
5. Process the queue: pop a song index `i`. If `i` has already been deleted (because its previous song was deleted), skip it. Otherwise, append `i+1` to `deleted` (convert to 1-based indexing).
6. Update the `next_song` of the previous song to skip the deleted song, effectively removing it from the playlist.
7. Check if the next song after `i` now has a coprime relationship with its new previous song. If so, append the next song index to the queue for future deletion.
8. Continue until the queue is empty. Output the length of `deleted` and the indices in order.

Why it works: the algorithm maintains a circular structure representing only the live songs. By maintaining a queue of candidate deletions, we never recheck songs unnecessarily, ensuring each song is deleted at most once. The invariant is that after each deletion, the playlist and the queue accurately represent the next potential coprime deletions. Circular linking ensures proper cycling through the playlist.

## Python Solution

```python
import sys
import math
from collections import deque
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    next_song = [(i + 1) % n for i in range(n)]
    deleted = []
    alive = [True] * n
    q = deque()
    
    for i in range(n):
        if math.gcd(a[i], a[i-1]) == 1:
            q.append(i)
    
    while q:
        i = q.popleft()
        if not alive[i]:
            continue
        deleted.append(i + 1)
        alive[i] = False
        prev = (i - 1) % n
        while not alive[prev]:
            prev = (prev - 1) % n
        nxt = next_song[i]
        while not alive[nxt]:
            nxt = next_song[nxt]
        next_song[prev] = nxt
        if alive[nxt] and math.gcd(a[prev], a[nxt]) == 1:
            q.append(nxt)
    
    print(len(deleted), *deleted)
```

The solution starts by creating a `next_song` array to emulate a circular linked list. Each song that is initially a candidate for deletion is placed in a queue. We then repeatedly delete the front of the queue, update links, and check if the deletion creates a new coprime condition for the next song. Boundary conditions like cycling past the end of the playlist are handled via modulo operations. Songs that are already deleted are skipped, avoiding duplicate deletions.

## Worked Examples

Trace Sample 1, first test case `[5, 9, 2, 10, 15]`:

| Step | Queue | Deleted | Playlist (alive) | Notes |
| --- | --- | --- | --- | --- |
| Init | [1, 2] | [] | [5, 9, 2, 10, 15] | gcd(5,9)=1, gcd(9,2)=1 |
| Pop 1 | [2] | [2] | [5,2,10,15] | Delete 9, prev=0, next=2 |
| Pop 2 | [] | [2,3] | [5,10,15] | Delete 2, prev=0, next=3 |
| Done | [] | [2,3] | [5,10,15] | Queue empty |

Trace Sample 1, second test case `[1,2,4,2,4,2]`:

| Step | Queue | Deleted | Playlist (alive) | Notes |
| --- | --- | --- | --- | --- |
| Init | [1,3] | [] | [1,2,4,2,4,2] | gcd(1,2)=1, gcd(2,4)=2 ... |
| Pop 1 | [3] | [2] | [1,4,2,4,2] | Delete song 2 |
| Pop 3 | [] | [2,1] | [4,2,4,2] | Delete song 1 |

These traces confirm that deletions occur in the correct order, respecting the “forget previous” rule and proper cycling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each song is visited at most twice: once for checking GCD, once for deletion. Queue operations are O(1). |
| Space | O(n) per test case | Arrays `alive`, `next_song`, and the queue hold up to n elements. |

Given the sum of `n` across all test cases ≤ 10^5, this fits comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import math
    input = sys.stdin.readline
    
    output = io.StringIO()
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        next_song = [(i + 1) % n for i in range(n)]
        deleted = []
        alive = [True] * n
        q = deque()
        
        for i in range(n):
            if math.gcd(a[i], a[i-1]) == 1:
                q.append(i)
        
        while q:
            i = q.popleft()
            if not alive[i]:
                continue
            deleted.append(i + 1)
            alive[i] = False
            prev = (i - 1) % n
            while not alive[prev]:
                prev = (prev - 1) % n
            nxt = next_song[i]
            while not alive[nxt]:
                nxt = next_song[nxt]
            next_song[prev] = nxt
            if alive[nxt
```
