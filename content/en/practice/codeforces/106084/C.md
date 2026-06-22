---
title: "CF 106084C - One-Way Abyss"
description: "Each test case describes a vertical cave system with several shafts. You start at the top of one chosen shaft and move strictly downward. While descending, you may encounter horizontal tunnels placed at distinct depths."
date: "2026-06-22T18:57:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106084
codeforces_index: "C"
codeforces_contest_name: "2025 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 106084
solve_time_s: 74
verified: true
draft: false
---

[CF 106084C - One-Way Abyss](https://codeforces.com/problemset/problem/106084/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes a vertical cave system with several shafts. You start at the top of one chosen shaft and move strictly downward. While descending, you may encounter horizontal tunnels placed at distinct depths. Each tunnel connects two shafts, and it lies at a specific depth, with tunnels ordered from top to bottom.

The movement rule is the key constraint. When you reach the depth of a tunnel, if you are currently in one of its two endpoint shafts, you are forced to traverse it immediately to the other shaft. If you are not in either endpoint shaft, the tunnel has no effect on your path. Because movement is always downward and tunnels are processed in increasing depth order, your trajectory is completely determined once you choose the starting shaft.

Each tunnel has a value, and you collect it if and only if you traverse that tunnel during your descent. The task is to choose the starting shaft that maximizes the total collected value.

The input size is large, with up to two hundred thousand shafts and tunnels in total across test cases. This immediately rules out simulating the process separately for every starting shaft, since that would lead to roughly O(nm) behavior in the worst case, which is far beyond the time limit.

A few corner cases are worth isolating.

If there are no tunnels, the answer is always zero regardless of starting shaft, since nothing is collected.

If all tunnels are disjoint in terms of depth but connect arbitrary shafts, the process still forces deterministic toggling, but naive per-start simulation may incorrectly assume independence between tunnels, even though earlier tunnels change whether later ones are activated.

A subtle failure case for naive reasoning is when a tunnel changes the current shaft, which then determines whether future tunnels are triggered. For example, starting at shaft 1 might allow you to enter a valuable tunnel later, while starting at shaft 2 might avoid it entirely, even if both choices initially look symmetric.

The core difficulty is that each tunnel does not just add a value locally, it also changes the state that determines future activations.

## Approaches

A direct simulation for each starting shaft would track the current shaft as we scan tunnels from top to bottom. For each start, this costs O(m), giving O(nm) total work. With n and m up to 2×10^5, this approach is infeasible.

The main obstacle is that different starting shafts only differ in how the same sequence of forced swaps affects them. The tunnel sequence applies the same transformation rule to every starting position: at each tunnel, only two specific current states matter, and those states get swapped if reached.

Instead of simulating each start independently, we reverse the viewpoint. At any fixed time before processing a tunnel, every starting shaft maps to a current shaft. This mapping is a permutation over shafts, because every start is in exactly one current shaft. Each tunnel updates this permutation by swapping the images of the two endpoints.

This observation turns the problem into maintaining a dynamic permutation while accumulating values. A tunnel contributes its value to exactly those starting shafts whose current image is one of its endpoints. Those starting shafts are precisely the preimages of the two endpoints under the current permutation.

So for each tunnel, we only need to identify which two starting positions currently map into its endpoints, add the value to them, and then update the permutation by swapping those endpoints.

This reduces the problem to O(m) updates, each in O(1), by maintaining the inverse mapping of the permutation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation per start | O(nm) | O(1) | Too slow |
| Maintain permutation + inverse updates | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We process tunnels in the given top-to-bottom order, maintaining a permutation that describes where each starting shaft currently is after processing all previous tunnels.

1. Initialize an array `inv`, where `inv[i] = i`. This means that initially, the start at shaft i is still at shaft i before any tunnel is processed.
2. Also initialize an array `score[i] = 0`, which will store the total collected value for starting shaft i.
3. For each tunnel `(x, y, v)` in order, we first identify which starting shafts are currently located at shafts x and y. These are exactly `inv[x]` and `inv[y]`.
4. We add `v` to both `score[inv[x]]` and `score[inv[y]]`, because any start that is currently at x or y will traverse this tunnel and collect its value.
5. After applying the tunnel, we update the permutation to reflect the forced movement. Every start currently at x moves to y, and every start currently at y moves to x. This is done by swapping `inv[x]` and `inv[y]`.
6. After processing all tunnels, the answer is the maximum value in `score`.

The important structural point is that `inv` always represents the current location of each starting shaft under the evolution induced by previous tunnels. Each tunnel only affects two positions in this structure, so updates stay constant time.

### Why it works

At any moment, the function mapping a starting shaft to its current position is a bijection over shafts. Each tunnel acts as a transposition on the current position space, swapping the two endpoints if they are active. A starting shaft contributes to a tunnel if and only if its current mapped position equals one of the endpoints, which corresponds exactly to being in the inverse image of those endpoints under the permutation. Since we maintain this permutation exactly, every contribution is counted once and only when it should be, and the swap update preserves correctness for all future tunnels.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())

        inv = list(range(n + 1))
        score = [0] * (n + 1)

        for _ in range(m):
            x, y, v = map(int, input().split())

            sx, sy = inv[x], inv[y]

            score[sx] += v
            score[sy] += v

            inv[x], inv[y] = inv[y], inv[x]

        out.append(str(max(score[1:])))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The key implementation detail is the direction of the permutation. The array `inv` is used as an inverse mapping from current shaft to starting shaft. This is what allows us to directly identify which starts are affected by each tunnel in O(1) time per endpoint.

The swap step must happen after the score update. Swapping earlier would incorrectly attribute the tunnel to the wrong starting shafts because the contribution depends on the pre-tunnel state.

## Worked Examples

Consider a small scenario with three shafts and two tunnels. Start with identity mapping.

| Step | Tunnel | inv before | affected starts | score updates | inv after |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,2,3) | [1,2,3] | 1,2 | +3 to 1 and 2 | [2,1,3] |
| 2 | (2,3,9) | [2,1,3] | 1,3 | +9 to 1 and 3 | [2,3,1] |

After processing, scores become:

start 1: 3 + 9 = 12

start 2: 3

start 3: 9

The maximum is 12, achieved by starting at shaft 1.

This trace shows how the identity of “which start is currently at a shaft” evolves over time, and how each tunnel only touches two entries of that mapping.

Now consider a case where tunnels swap back and forth, emphasizing permutation behavior.

| Step | Tunnel | inv before | affected starts | score updates | inv after |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,2,5) | [1,2,3] | 1,2 | +5 to 1 and 2 | [2,1,3] |
| 2 | (1,2,7) | [2,1,3] | 2,1 | +7 to 2 and 1 | [1,2,3] |

Here the second tunnel effectively restores the original mapping, showing that the system behaves like repeated transpositions on a permutation rather than independent per-tunnel effects.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | Each tunnel performs O(1) work: two array reads, two additions, one swap |
| Space | O(n) | Arrays `inv` and `score` store per-shaft state |

The total constraints sum n and m across test cases to 2×10^5, so a linear-time approach is sufficient and comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n, m = map(int, input().split())
        inv = list(range(n + 1))
        score = [0] * (n + 1)

        for _ in range(m):
            x, y, v = map(int, input().split())
            sx, sy = inv[x], inv[y]
            score[sx] += v
            score[sy] += v
            inv[x], inv[y] = inv[y], inv[x]

        res.append(str(max(score[1:])))
    return "\n".join(res) + ("\n" if res else "")

# sample-style sanity checks
assert run("1\n3 2\n1 2 3\n2 3 9\n") == "12\n"

# no tunnels
assert run("1\n5 0\n") == "0\n"

# single tunnel
assert run("1\n4 1\n2 4 10\n") == "10\n"

# chain swaps
assert run("1\n3 3\n1 2 5\n2 3 7\n1 3 2\n") == "14\n"

# symmetric case
assert run("1\n2 2\n1 2 4\n1 2 6\n") == "10\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no tunnels | 0 | base case correctness |
| single tunnel | value | single activation logic |
| chain swaps | 14 | permutation evolution across multiple swaps |
| symmetric repeated | 10 | accumulation and repeated updates |

## Edge Cases

A minimal case with no tunnels confirms that the algorithm correctly leaves all scores at zero and does not access invalid mappings.

A case with a single tunnel verifies that both endpoints correctly contribute once and only once to their respective starting shafts.

A sequence where tunnels repeatedly swap the same pair of shafts demonstrates that the permutation state is truly dynamic and must be updated after every tunnel, not treated as static adjacency.

A final subtle case is when a high-value tunnel is preceded by swaps that move different starting shafts into its endpoints. The algorithm handles this correctly because it always queries `inv[x]` and `inv[y]` at the moment of processing, rather than relying on initial shaft identity.
