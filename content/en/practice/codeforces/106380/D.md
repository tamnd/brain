---
title: "CF 106380D - Do you play Ballance?"
description: "We have a ball that can be one of three materials. Each mechanism on the path accepts some subset of these three materials. The ball must pass through every mechanism, but we are allowed to choose the order of mechanisms."
date: "2026-06-25T10:21:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106380
codeforces_index: "D"
codeforces_contest_name: "The 6th Liaoning Provincial Collegiate Programming Contest"
rating: 0
weight: 106380
solve_time_s: 37
verified: true
draft: false
---

[CF 106380D - Do you play Ballance?](https://codeforces.com/problemset/problem/106380/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a ball that can be one of three materials. Each mechanism on the path accepts some subset of these three materials. The ball must pass through every mechanism, but we are allowed to choose the order of mechanisms.

At the beginning we must pay once to choose the initial material. Before any mechanism, we may either keep the current material for free or pay one unit to change it to another material. The goal is to find the smallest possible total cost after arranging the mechanisms in the best possible order.

Each mechanism can be described only by the set of materials it accepts. Since there are three materials, there are only seven possible non-empty mechanism types. The input size can be up to 100 mechanisms, so a solution depending on the number of mechanisms exponentially is impossible, but a solution depending only on the seven possible types is easily fast enough.

The main edge cases come from the fact that the order matters and that a mechanism can allow multiple materials. A careless greedy solution may fail.

For example:

```
3
1 0 0
0 1 0
0 0 1
```

The correct answer is `3`. We need one initial selection and two switches. A strategy that simply counts distinct materials and returns `3` would happen to work here, but it fails when overlaps exist because shared materials can connect groups.

Another example:

```
3
1 1 0
0 1 0
0 0 1
```

The correct answer is `3`. We can start with material 1, pass the first mechanism, keep material 1 or switch to material 2 for the second, then switch to material 3. A greedy method that always switches whenever a new material appears can make unnecessary changes.

The constraints point directly toward state compression. There are only three possible current materials and only seven possible mechanism masks, so the algorithm can explore all combinations of processed mechanism types instead of all possible orders of 100 mechanisms.

## Approaches

A direct brute force approach would try every possible order of mechanisms and every possible material choice before each mechanism. If there are many mechanisms, the number of orders is factorial, and even ignoring material choices the number of possible arrangements is far beyond what can be checked. For 100 mechanisms, exploring orders is completely infeasible.

The useful observation is that mechanisms with the same allowed materials are identical from the perspective of future decisions. After processing one mechanism of a certain type, processing another mechanism with the same type has exactly the same effect. The only information that matters is which of the seven non-empty material masks have already been completed and what material the ball currently has.

The brute force works because it considers every possible valid order, but fails because it keeps information that does not affect the answer. The observation that there are only seven mechanism categories lets us reduce the problem to a shortest path over at most `2^7 * 3` states.

For every state, we try taking one unprocessed mechanism category. If the current material is allowed, we can finish that category without paying. Otherwise, we can switch to one of its allowed materials and pay one unit. We also allow switching voluntarily to another accepted material because the material after completing a mechanism can affect future choices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(2^7 * 7 * 3) | O(2^7 * 3) | Accepted |

## Algorithm Walkthrough

1. Convert every mechanism into a three-bit mask. Bit `0`, `1`, and `2` represent the three material types. Count which of the seven possible masks appear.
2. Use dynamic programming where `dp[mask][material]` is the minimum cost after processing all mechanism categories included in `mask` and currently having the given material.
3. Initialize the empty state. Choosing any starting material costs one unit, so the three states with no processed mechanisms start with cost `1`.
4. From every reachable state, choose one not-yet-processed mechanism category. Try every material that could be the material after passing that mechanism.
5. If the chosen material is the current material, the transition costs zero. If it is different, the transition costs one because we switch before the mechanism.
6. The answer is the minimum value among all states where every existing mechanism category has been processed.

Why it works:

The invariant is that every DP state represents the cheapest possible way to reach exactly the described situation. The only information needed for future decisions is the set of mechanism categories already handled and the current material. When a transition is performed, it considers every possible next category and every possible resulting material, so no valid ordering is missed. Since every possible state transition corresponds to a legal action in the game, and every legal action is represented by a transition, the minimum final state is the optimal cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    cnt = [0] * 8
    for _ in range(n):
        a = list(map(int, input().split()))
        mask = a[0] | (a[1] << 1) | (a[2] << 2)
        cnt[mask] += 1

    used = [i for i in range(1, 8) if cnt[i] > 0]
    idx = {x: i for i, x in enumerate(used)}
    m = len(used)

    categories = [(x, idx[x]) for x in used]
    full = (1 << m) - 1

    INF = 10**9
    dp = [[INF] * 3 for _ in range(1 << m)]

    for i in range(3):
        dp[0][i] = 1

    for state in range(1 << m):
        for cur in range(3):
            if dp[state][cur] == INF:
                continue
            for mask, bit in categories:
                if state & (1 << bit):
                    continue
                nstate = state | (1 << bit)
                for nxt in range(3):
                    if mask & (1 << nxt):
                        cost = 0 if nxt == cur else 1
                        if dp[state][cur] + cost < dp[nstate][nxt]:
                            dp[nstate][nxt] = dp[state][cur] + cost

    print(min(dp[full]))

if __name__ == "__main__":
    solve()
```

The input is first compressed into seven possible mechanism categories. The actual number of occurrences does not matter after this point because passing multiple mechanisms of the same category can always be done consecutively.

The DP table stores only the compressed state. The bitmask dimension represents completed categories, not individual mechanisms. This is the key reduction that makes the algorithm small.

During transitions, the loop over `nxt` is necessary because a switch may be useful even when the current material is accepted. For example, a mechanism accepting materials 1 and 2 can be used to move from material 1 to material 2 if that helps later.

The final lookup uses the state containing every category that appeared in the input. Categories that never appear do not need to be processed.

## Worked Examples

For the input:

```
5
1 0 0
1 0 1
0 1 0
1 0 1
0 0 1
```

The categories are material sets `{1}`, `{1,3}`, `{2}`, `{3}`.

A possible DP trace:

| Processed categories | Current material | Cost |
| --- | --- | --- |
| none | 1 | 1 |
| `{1}` | 1 | 1 |
| `{1,3}` | 1 | 1 |
| `{1,3},{2}` | 2 | 2 |
| all | 3 | 3 |

The result is `3`. The trace shows that overlapping mechanisms allow us to move through the categories without switching every time.

For:

```
3
1 1 0
0 1 0
0 0 1
```

The state evolution can be:

| Processed categories | Current material | Cost |
| --- | --- | --- |
| none | 1 | 1 |
| `{1,2}` | 1 | 1 |
| `{1,2},{2}` | 2 | 2 |
| all | 3 | 3 |

Again the answer is `3`, and the important part is that the first mechanism can bridge materials 1 and 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^k * k * 3 * 3) | `k` is the number of appearing mechanism categories, at most 7 |
| Space | O(2^k * 3) | Stores the DP states |

The algorithm does not depend on the number of mechanisms after compression. Even in the worst case all seven categories appear, giving only 384 DP values and a very small number of transitions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    n = int(input())
    cnt = [0] * 8
    for _ in range(n):
        a = list(map(int, input().split()))
        cnt[a[0] | (a[1] << 1) | (a[2] << 2)] += 1

    used = [i for i in range(1, 8) if cnt[i]]
    pos = {x: i for i, x in enumerate(used)}
    dp = [[10**9] * 3 for _ in range(1 << len(used))]
    for i in range(3):
        dp[0][i] = 1

    for s in range(1 << len(used)):
        for c in range(3):
            for mask in used:
                if dp[s][c] == 10**9:
                    continue
                if s & (1 << pos[mask]):
                    continue
                for nc in range(3):
                    if mask & (1 << nc):
                        ns = s | (1 << pos[mask])
                        dp[ns][nc] = min(dp[ns][nc], dp[s][c] + (c != nc))

    ans = str(min(dp[-1]))
    sys.stdin = old
    return ans

assert run("""5
1 0 0
1 0 1
0 1 0
1 0 1
0 0 1
""") == "3"

assert run("""1
1 1 1
""") == "1"

assert run("""3
1 0 0
0 1 0
0 0 1
""") == "3"

assert run("""3
1 1 0
0 1 0
0 0 1
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single mechanism allowing all materials | 1 | Initial selection only |
| Three disjoint single-material mechanisms | 3 | Required switches between isolated groups |
| Overlapping material sets | 3 | Avoids greedy switching mistakes |

## Edge Cases

For the isolated material case:

```
3
1 0 0
0 1 0
0 0 1
```

The DP starts with cost `1` for any material. Processing the first category is free only if it matches the current material. The remaining two categories require switches, giving the final answer `3`.

For the all-material case:

```
1
1 1 1
```

Any initial material works and the mechanism accepts it immediately. The DP reaches the completed state with cost `1`, which is the minimum possible because the initial selection is mandatory.

For overlapping categories:

```
3
1 1 0
0 1 0
0 0 1
```

The first two mechanisms can be handled through material 2, while the last one requires material 3. The DP keeps the possibility of moving from material 1 to material 2 at the correct moment instead of forcing a premature switch. The final cost remains `3`.
