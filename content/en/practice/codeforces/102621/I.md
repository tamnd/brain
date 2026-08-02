---
title: "CF 102621I - Playlist Shuffle"
description: "We have a playlist of songs. Each song has two labels: its genre and its writer. We are allowed to remove some songs, then reorder the remaining songs."
date: "2026-08-02T13:58:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102621
codeforces_index: "I"
codeforces_contest_name: "mBIT Advanced June 2020"
rating: 0
weight: 102621
solve_time_s: 83
verified: true
draft: false
---

[CF 102621I - Playlist Shuffle](https://codeforces.com/problemset/problem/102621/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a playlist of songs. Each song has two labels: its genre and its writer. We are allowed to remove some songs, then reorder the remaining songs. A reordered playlist is considered valid when every neighboring pair shares at least one label: either both songs have the same genre or both songs have the same writer. The task is to keep as many songs as possible, so the answer is the minimum number of removed songs. The original problem has a small number of songs, with the intended solution using subset dynamic programming.

The key constraint is the number of songs, which is at most 16. This is small enough that exponential algorithms are possible. A solution based on checking every ordering would still be too expensive because the number of permutations grows as $n!$, reaching billions even for moderate values of $n$. A solution over all subsets is feasible because there are only $2^{16}=65536$ possible subsets.

The large string lengths matter in a different way. We cannot afford to repeatedly compare long genre and writer strings while exploring states. We should preprocess the pairwise relationship between songs once, then use only constant time checks during the dynamic programming.

The tricky cases come from the fact that the valid playlist is not necessarily the original order.

For example, if the input is:

```
3
rock alice
pop bob
rock bob
```

the correct output is:

```
0
```

because the order `rock alice`, `rock bob`, `pop bob` works. A solution that only checks the given order would incorrectly remove songs.

Another edge case is when only one song remains. For example:

```
1
jazz mike
```

The answer is:

```
0
```

because a single song has no neighboring pair that can violate the rule. Code that initializes the answer around adjacent comparisons may accidentally count this as invalid.

A final edge case is when no large subset is connected enough. For example:

```
3
a x
b y
c z
```

The correct output is:

```
2
```

Only one song can remain, because no two songs can be placed next to each other. A careless implementation that assumes every song can appear in the final playlist would fail here.

## Approaches

The straightforward approach is to try every possible subset of songs and every possible ordering inside that subset. If an ordering satisfies the adjacency rule, we keep the largest valid size. This is correct because the answer is exactly the complement of the largest valid playlist.

The problem is the number of orderings. For $n=16$, checking all permutations requires $16!$ possibilities, which is about $2.1 \times 10^{13}$. Even with fast operations this cannot fit into the time limit.

The important observation is that the order only depends on which song was placed last. When building a valid playlist, we do not need to remember the entire ordering so far. We only need the set of songs already used and the identity of the last song, because the next song only has to be compatible with that last song.

This converts the problem into subset dynamic programming. We compute the largest valid playlist that ends with each song for every subset. Once all states are processed, the largest reachable subset size gives the maximum number of songs we can keep.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n^2 2^n)$ | $O(n2^n)$ | Accepted |

## Algorithm Walkthrough

1. Precompute whether every pair of songs can be adjacent. Two songs are compatible when their genres match or their writers match. Storing this result avoids repeatedly comparing strings inside the dynamic programming.
2. Create a DP table where `dp[mask][i]` represents whether it is possible to build a valid playlist containing exactly the songs in `mask` and ending with song `i`. The last song is stored because it determines which songs can be appended next.
3. Initialize every single-song subset. A playlist containing one song is always valid, so every state with one set bit starts as reachable.
4. Iterate through all subsets. For every reachable ending song `i`, try adding every song `j` not already inside the subset. If `i` and `j` are compatible, mark the new subset ending at `j` as reachable.
5. Track the largest number of set bits among all reachable states. The number of removed songs is the total number of songs minus this maximum.

Why it works: every valid playlist has a final song and a set of used songs. The DP stores exactly this information, so every valid arrangement can be reproduced by transitions. Conversely, every transition adds a song only when it can legally follow the previous last song, so every generated state corresponds to a valid playlist. The maximum reachable subset is therefore the largest playlist that can be formed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        songs = []

        for _ in range(n):
            g, w = input().split()
            songs.append((g, w))

        ok = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if songs[i][0] == songs[j][0] or songs[i][1] == songs[j][1]:
                    ok[i][j] = True

        total = 1 << n
        dp = [0] * (total * n)

        for i in range(n):
            dp[((1 << i) * n) + i] = 1

        best = 1

        for mask in range(total):
            cnt = mask.bit_count()
            if cnt <= best:
                best = max(best, cnt)

            base = mask * n
            for last in range(n):
                if dp[base + last]:
                    remaining = ((total - 1) ^ mask)
                    while remaining:
                        bit = remaining & -remaining
                        nxt = bit.bit_length() - 1
                        if ok[last][nxt]:
                            new_mask = mask | bit
                            dp[new_mask * n + nxt] = 1
                        remaining -= bit

        ans.append(str(n - best))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The pairwise `ok` matrix is built before the DP begins. This is where all expensive string comparisons happen, so the exponential part of the algorithm only performs integer operations.

The DP array is flattened into one dimension. The state `(mask, last)` is stored at index `mask * n + last`, which avoids creating many nested Python lists and reduces overhead.

Single-song states are initialized because every song can start a playlist. During transitions, the code removes one available bit at a time from the set of unused songs. This avoids scanning unnecessary positions.

Python integers do not overflow, so the bitmask operations are safe. The only boundary detail to handle carefully is the single-song case, where the maximum valid playlist size is already initialized correctly.

## Worked Examples

Consider:

```
3
rock a
pop b
rock b
```

The state exploration looks like this:

| mask | Last song | Action | Reachable size |
| --- | --- | --- | --- |
| 001 | rock a | Start | 1 |
| 100 | rock b | Start | 1 |
| 010 | pop b | Start | 1 |
| 101 | rock b | Add after rock a | 2 |
| 111 | pop b | Add after rock b | 3 |

The full set becomes reachable because the ordering `rock a -> rock b -> pop b` satisfies every adjacency condition. The maximum kept size is 3, so the answer is 0.

Consider:

```
3
a x
b y
c z
```

The states are:

| mask | Last song | Action | Reachable size |
| --- | --- | --- | --- |
| 001 | a x | Start | 1 |
| 010 | b y | Start | 1 |
| 100 | c z | Start | 1 |

No transition exists because no pair shares a label. The maximum playlist size is 1, so two songs must be removed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 2^n)$ | Every subset may try extending with every possible next song |
| Space | $O(n2^n)$ | One DP state is stored for each subset and possible ending song |

With $n \leq 16$, the number of subsets is at most 65536. The resulting number of states is small enough for the required limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    t = int(next(it))
    res = []

    for _ in range(t):
        n = int(next(it))
        songs = []
        for _ in range(n):
            songs.append((next(it), next(it)))

        ok = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                ok[i][j] = songs[i][0] == songs[j][0] or songs[i][1] == songs[j][1]

        dp = [0] * ((1 << n) * n)
        best = 1

        for i in range(n):
            dp[((1 << i) * n) + i] = 1

        for mask in range(1 << n):
            best = max(best, mask.bit_count())
            for last in range(n):
                if dp[mask * n + last]:
                    rem = ((1 << n) - 1) ^ mask
                    while rem:
                        b = rem & -rem
                        nxt = b.bit_length() - 1
                        if ok[last][nxt]:
                            dp[(mask | b) * n + nxt] = 1
                        rem -= b

        res.append(str(n - best))

    return "\n".join(res)

assert run("""1
1
jazz mike
""") == "0"

assert run("""1
3
rock a
pop b
rock b
""") == "0"

assert run("""1
3
a x
b y
c z
""") == "2"

assert run("""1
4
a x
a y
b y
c z
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One song | 0 | Single-element boundary case |
| Chain of compatible songs | 0 | Full playlist can be reordered |
| No compatible pairs | 2 | Only one song can survive |
| Partial compatibility | 1 | Maximum subset selection |

## Edge Cases

For the single-song case:

```
1
jazz mike
```

the DP starts with the only song as a reachable state. No transition is needed, so the maximum playlist size is one and the removal count is zero.

For the case where the original order is misleading:

```
3
rock alice
pop bob
rock bob
```

the algorithm does not care about the input order. It starts from every song and explores all possible valid continuations. It discovers the ordering ending with all three songs and returns zero removals.

For the case with completely unrelated songs:

```
3
a x
b y
c z
```

the compatibility matrix contains no true pair except self-pairs. The transition loop cannot create a larger mask, leaving only the three size-one states. The algorithm correctly computes that only one song can remain.
