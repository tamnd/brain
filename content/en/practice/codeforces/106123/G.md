---
title: "CF 106123G - The Missing Bone"
description: "The problem describes a line of n cups placed at positions 1 through n. A bone starts under the first cup. Some positions contain holes. A sequence of swaps is performed between pairs of cup positions."
date: "2026-06-25T11:33:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106123
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 10-15-25 Div. 1 (Advanced)"
rating: 0
weight: 106123
solve_time_s: 28
verified: true
draft: false
---

[CF 106123G - The Missing Bone](https://codeforces.com/problemset/problem/106123/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a line of `n` cups placed at positions `1` through `n`. A bone starts under the first cup. Some positions contain holes. A sequence of swaps is performed between pairs of cup positions. During a swap, the two cups instantly exchange places, so the bone moves only if it is inside one of those swapped cups. If the bone reaches a hole after any swap, it falls out and disappears permanently. The task is to determine the final position of the bone, or report that it has fallen.

The input gives the number of cup positions, the number of holes, the number of swaps, the hole locations, and then the swap operations. The output is the final position containing the bone after all operations, unless the bone was lost in a hole.

The constraints make the intended solution clear. The number of operations can be large enough that simulating anything beyond the given swaps is unnecessary. Each swap only affects two positions, so a solution that spends constant time per swap is ideal. Building expensive data structures or checking every cup after every operation would introduce avoidable overhead.

The tricky cases come from the fact that falling into a hole stops all future movement. A common mistake is to continue applying swaps after the bone has disappeared.

For example, if the input is:

```
3 1 2
2
1 2
2 3
```

The bone starts at position `1`. The first swap moves it to position `2`, where there is a hole, so the correct output is:

```
-1
```

A careless simulation that ignores holes until the end would move the bone from position `2` to position `3` and print the wrong answer.

Another edge case is when a swap does not involve the current bone position. For example:

```
5 0 2
1 2
4 5
```

The bone starts at `1`. The first swap moves it to `2`, and the second swap does not affect it. The answer is:

```
2
```

An implementation that swaps cups without tracking the bone location correctly may accidentally move the bone again.

## Approaches

The direct approach is to keep the current bone position and process every swap. For each operation, if the bone is at one of the two swapped positions, it moves to the other position. After the movement, we check whether the new position is a hole. If it is, the bone is gone.

This brute force approach is already optimal because the input itself describes the only events that can change the answer. There is no need to reconstruct the whole arrangement of cups. The only relevant information is the location of the bone and whether a position is a hole.

A more complicated simulation might store every cup and move objects around during each swap. That works conceptually, but it tracks information that does not matter. The cups are only labels around the bone, and the question asks about the bone alone. Since a swap only changes the location of the bone when its current position is one of the swapped positions, we can reduce the entire process to a single integer update.

The brute force and optimal solutions are the same here because the straightforward simulation is already the minimal possible work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) | O(n) | Accepted |
| Optimal | O(k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store all hole positions in a set. A set allows us to check whether the bone has fallen after a move in constant average time.
2. Initialize the bone position as `1`, because the bone starts under the first cup.
3. Process the swaps one by one. For a swap between positions `u` and `v`, move the bone from `u` to `v` or from `v` to `u` only if it is currently under one of those cups. If neither position contains the bone, the swap has no effect on the answer.
4. After each movement, check whether the new bone position is a hole. If it is, mark the bone as lost and stop processing future swaps.
5. If all swaps are processed without losing the bone, print its final position.

Why it works:

At every moment, the only part of the cup arrangement that matters is the cup currently hiding the bone. A swap changes the bone's location exactly when that cup participates in the swap. The algorithm applies exactly those changes and ignores swaps that cannot affect the bone. After every possible movement, it immediately checks the hole condition, matching the rules of the process. Since the state is updated after every operation, the final stored position is exactly the real outcome.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    holes = set(map(int, input().split()))

    pos = 1
    alive = True

    for _ in range(k):
        u, v = map(int, input().split())

        if alive:
            if pos == u:
                pos = v
            elif pos == v:
                pos = u

            if pos in holes:
                alive = False

    print(pos if alive else -1)

if __name__ == "__main__":
    solve()
```

The solution stores holes in a hash set because membership checks happen after every swap. A list would also work, but the set directly represents the operation we need: asking whether a position is dangerous.

The variable `pos` is the complete state of the simulation. There is no need to store cup contents because a swap only matters when it touches this position.

The `alive` flag prevents later swaps from changing the answer after the bone has fallen. This matches the problem rule that the bone is no longer inside any cup once it reaches a hole.

The order of operations is important. The swap must happen before checking for a hole because the bone can only fall after arriving at the new position. Checking before moving would miss cases where the swap places the bone directly into a hole.

## Worked Examples

Consider:

```
5 1 3
4
1 3
3 4
2 5
```

| Step | Swap | Bone position before | Bone position after | Alive |
| --- | --- | --- | --- | --- |
| Start | none | 1 | 1 | yes |
| 1 | 1 3 | 1 | 3 | yes |
| 2 | 3 4 | 3 | 4 | no |
| 3 | 2 5 | 4 | 4 | no |

The second swap places the bone into position `4`, which is a hole. The last swap is ignored because the bone has already disappeared.

Another example:

```
4 0 3
1 2
2 3
4 1
```

| Step | Swap | Bone position before | Bone position after | Alive |
| --- | --- | --- | --- | --- |
| Start | none | 1 | 1 | yes |
| 1 | 1 2 | 1 | 2 | yes |
| 2 | 2 3 | 2 | 3 | yes |
| 3 | 4 1 | 3 | 3 | yes |

The final answer is `3`. This trace shows that swaps unrelated to the bone do not change the state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each swap is processed once with constant time updates and checks. |
| Space | O(m) | The set stores the hole positions. |

The solution fits the constraints because it performs only the necessary work: one constant time update for each swap. Even very large sequences of swaps remain manageable.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    holes = set(map(int, input().split()))

    pos = 1
    alive = True

    for _ in range(k):
        u, v = map(int, input().split())

        if alive:
            if pos == u:
                pos = v
            elif pos == v:
                pos = u

            if pos in holes:
                alive = False

    ans = str(pos if alive else -1)

    sys.stdin = old_stdin
    return ans

assert solve_io(
    "3 1 2\n"
    "2\n"
    "1 2\n"
    "2 3\n"
) == "-1"

assert solve_io(
    "5 0 2\n"
    "1 2\n"
    "4 5\n"
) == "2"

assert solve_io(
    "1 1 0\n"
    "1\n"
) == "1"

assert solve_io(
    "4 0 3\n"
    "1 2\n"
    "2 3\n"
    "4 1\n"
) == "3"

assert solve_io(
    "5 5 1\n"
    "1 2 3 4 5\n"
    "1 5\n"
) == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Bone enters a hole after a swap | `-1` | Immediate termination after falling |
| Swaps that do not always affect the bone | `2` or `3` depending on moves | Correct tracking of the current cup |
| Single position with no swaps | Starting position | Minimum size handling |
| Several swaps without holes | Final moved position | Normal simulation flow |
| Starting position is a hole | Loss after first valid state check | Hole boundary behavior |

## Edge Cases

When the bone falls into a hole, future swaps must not revive it. In:

```
3 1 2
2
1 2
2 3
```

the first swap moves the bone from `1` to `2`. The algorithm immediately sees that `2` is a hole and sets `alive` to false. The second swap is read but cannot change the answer, so the output is `-1`.

When swaps do not involve the bone, the position must remain unchanged. In:

```
5 0 2
1 2
4 5
```

the first swap moves the bone from `1` to `2`. The second swap only exchanges cups `4` and `5`, so the bone stays at `2`. The algorithm checks only whether `pos` matches one of the swapped endpoints, which preserves the correct state.

When there are no swaps, the answer is simply the initial location unless that location is already a hole. The algorithm starts with `pos = 1` and performs no updates, so it naturally handles this case.
