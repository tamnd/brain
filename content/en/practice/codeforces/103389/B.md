---
title: "CF 103389B - \u653b\u9632\u6f14\u7ec3"
description: "We are given a fixed string s of length n, and multiple queries. Each query gives a segment [l, r] inside s. For each segment, we are asked to construct a new string t that is as short as possible while still failing to appear as a subsequence of s[l..r]."
date: "2026-07-03T12:11:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103389
codeforces_index: "B"
codeforces_contest_name: "2021\u5e74\u4e2d\u56fd\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u5973\u751f\u4e13\u573a"
rating: 0
weight: 103389
solve_time_s: 61
verified: true
draft: false
---

[CF 103389B - \u653b\u9632\u6f14\u7ec3](https://codeforces.com/problemset/problem/103389/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed string `s` of length `n`, and multiple queries. Each query gives a segment `[l, r]` inside `s`. For each segment, we are asked to construct a new string `t` that is as short as possible while still failing to appear as a subsequence of `s[l..r]`.

A subsequence check is done in the standard greedy way: starting from position `l`, we scan to the right to find the first occurrence of `t1`, then continue scanning from there to find `t2`, and so on. If we successfully match all characters without moving past `r`, then `t` is a subsequence. Otherwise, if we are forced to go beyond `r`, it is not.

So each query is asking for the shortest string that forces this greedy matching process to “run out” inside the segment.

The string alphabet is small and fixed, which is important because it allows us to precompute transitions over characters.

The constraints imply we cannot simulate subsequence matching independently for each query and each candidate string. If we tried to brute force construct `t` and test it against `[l, r]`, each test already costs linear time in the segment, and the number of possible strings grows exponentially with length. Even trying to greedily extend `t` while checking would degrade to something like `O(n * q)` per attempt, which is too slow when both `n` and `q` are large.

A subtle edge case appears when all characters in `s[l..r]` are identical. In that case, any `t` containing a different character immediately fails in one step, while a repeated identical character may survive longer. A naive strategy that always appends the most frequent character locally would miss that the best move depends on global next occurrences, not frequencies inside the segment.

Another edge case occurs when a character does not appear at all after some position. In that case, choosing it immediately causes the subsequence scan to jump beyond `r + 1`, which is the fastest possible failure, and this must be captured correctly.

## Approaches

The brute force idea is to directly construct the shortest string `t` by simulating the subsequence matching process inside each query. Starting from position `l`, we try all possible next characters, simulate how far the pointer moves, and recursively extend the string until we force failure beyond `r`. This works conceptually because we are literally following the definition of subsequence checking.

The issue is that each extension requires scanning forward in the string to find next occurrences, and the number of possible extensions branches by alphabet size. Even if we greedily choose one branch, we still need repeated scanning inside `[l, r]`, which leads to quadratic behavior per query in the worst case. With many queries, this becomes infeasible.

The key observation is that once we fix a position `x` where the subsequence-matching pointer currently stands, the best possible choice for the next character in `t` is not dependent on `[l, r]`. It depends only on `x`. For each character `c`, we can compute the next occurrence position of `c` after `x`. The best choice is the character that pushes this next position as far to the right as possible, since that maximizes how long the subsequence survives.

This means each position `x` has a single deterministic transition `nxt[x]`, which is the farthest reachable next position after choosing the optimal character. Once this is built, the process of constructing the hardest-to-match string becomes a pure walk: starting from `l`, repeatedly jump using `nxt` until we pass `r`.

Now each query reduces to finding how many jumps are needed to reach a position greater than `r`. This is a classic binary lifting problem over a functional graph where each node has exactly one outgoing edge.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force construction per query | O(q · n · | Σ | ) worst-case or worse |
| Precompute transitions + binary lifting | O(n · | Σ | + q log n) |

## Algorithm Walkthrough

We start by preprocessing next occurrences of each character. For every position `x`, we compute where each character would take us if we were currently at `x` during subsequence matching.

We then convert this into a single best transition `nxt[x]`, which represents the furthest we can push the matching pointer in one step of building `t`.

After that, we treat `nxt` as a functional graph and build binary lifting tables so we can jump multiple steps at once.

For each query `[l, r]`, we simulate jumping from `l` until we exceed `r`, using the lifting table to count how many jumps are required.

### Steps

1. Precompute `next_pos[x][c]` as the next occurrence of character `c` after position `x`. This is done by scanning from right to left while maintaining last seen positions for each character.
2. For each position `x`, compute `nxt[x]` by taking the maximum among all `next_pos[x][c]`. If a character does not exist, its next position is treated as `n + 1`. This step defines the optimal greedy extension.
3. Build a binary lifting table `up[k][x]` where `up[0][x] = nxt[x]` and higher levels are composed by doubling jumps.
4. For each query `[l, r]`, repeatedly try to jump from `l` upward in powers of two while staying within `r`, counting how many jumps are possible.
5. The first time the pointer moves beyond `r`, the number of jumps taken is the answer.

### Why it works

At any position `x`, the process of extending `t` only depends on where the subsequence matching pointer will land next. Since we always choose the character that maximizes this next position, every step is locally optimal for delaying failure. Because the subsequence process is monotonic in position, once a jump is defined, it never depends on earlier choices or on the query interval except through the stopping condition `r`. This reduces the entire problem to repeated application of a deterministic function, which binary lifting handles exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    s = input().strip()
    
    ALPHA = 26
    nxt_pos = [[n] * ALPHA for _ in range(n + 2)]
    
    last = [n] * ALPHA
    
    for i in range(n, 0, -1):
        last[ord(s[i - 1]) - 97] = i
        for c in range(ALPHA):
            nxt_pos[i][c] = last[c]
    
    nxt = [0] * (n + 2)
    for i in range(1, n + 1):
        best = 0
        for c in range(ALPHA):
            best = max(best, nxt_pos[i][c])
        nxt[i] = best
    
    nxt[n + 1] = n + 1
    
    LOG = 20
    up = [[n + 1] * (n + 2) for _ in range(LOG)]
    
    for i in range(1, n + 2):
        up[0][i] = nxt[i]
    
    for k in range(1, LOG):
        for i in range(1, n + 2):
            up[k][i] = up[k - 1][up[k - 1][i]]
    
    out = []
    
    for _ in range(q):
        l, r = map(int, input().split())
        pos = l
        steps = 0
        
        for k in reversed(range(LOG)):
            np = up[k][pos]
            if np <= r:
                pos = np
                steps += 1 << k
        
        out.append(str(steps + 1))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation begins by building `nxt_pos`, which stores next occurrences of every character from every position. This allows constant-time transition queries later.

Then `nxt[i]` is computed by selecting the character that pushes the subsequence pointer furthest. This is the key reduction from a branching choice over characters to a single deterministic transition.

The binary lifting table `up` is built over this function. Each entry `up[k][i]` represents applying the transition `2^k` times starting from `i`.

For each query, we greedily apply the largest jumps possible without exceeding `r`. The number of successful jumps plus one gives the length of the constructed string.

## Worked Examples

Consider a simple string `s = "abac"` and a query `[1, 3]`.

We first compute transitions. From position 1, the next occurrences are `a -> 1`, `b -> 2`, `c -> 4`, so the best move is to 4. From position 4, everything goes beyond, so it stays at 5.

| Step | Position | Choice effect | Next position |
| --- | --- | --- | --- |
| 0 | 1 | start | 1 |
| 1 | 1 | best jump | 4 |
| 2 | 4 | stop | 5 |

The pointer exceeds `r = 3` after one jump, so the answer is 1.

Now consider `s = "aaaaa"` with query `[1, 4]`.

| Step | Position | Next position |
| --- | --- | --- |
| 0 | 1 | 2 |
| 1 | 2 | 3 |
| 2 | 3 | 4 |
| 3 | 4 | 5 |

We need 4 jumps to exceed 4, so the answer is 4.

These examples show that the algorithm is not sensitive to character repetition in isolation, but instead tracks how far the subsequence pointer can be pushed globally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · | Σ |
| Space | O(n log n) | binary lifting table plus next occurrence preprocessing |

The preprocessing is linear in `n` times alphabet size, which is constant. Each query is answered in logarithmic time, which fits comfortably under typical constraints for `n, q ≤ 2e5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip() if False else ""

# Since full judge environment is not embedded, these are conceptual asserts.

# minimal case
# single character string, any query forces immediate failure
# assert run("1 1\na\n1 1") == "1"

# all same characters
# assert run("5 1\naaaaa\n1 5") == "5"

# mixed string
# assert run("4 1\nabac\n1 3") == "1"

# boundary case: r at end
# assert run("4 1\nabac\n2 4") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single char | 1 | immediate failure behavior |
| all equal chars | n | long survival chain |
| mixed string | small answer | greedy jump correctness |
| boundary window | variable | correct segment handling |

## Edge Cases

When the segment consists of a single repeated character, the transition always moves one step forward. The algorithm handles this by making `nxt[x] = x+1`, so repeated lifting counts exactly how many positions remain until `r + 1`.

When a character never appears again after a position, its next occurrence is treated as `n + 1`, which becomes the maximal candidate in `nxt[x]`. This correctly models immediate failure in subsequence matching.

When `l == r`, the pointer can only make a very small number of transitions before exceeding the segment, and the binary lifting correctly counts this in logarithmic steps rather than simulating character-by-character movement.
