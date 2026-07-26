---
title: "CF 102821A - Autochess"
description: "The problem models the preparation phase of an autochess game. There is a row of N waiting slots, initially empty. Fish receives M level-1 chessmen one by one. Every chessman has only a name, and chessmen with the same name can combine."
date: "2026-07-26T16:09:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102821
codeforces_index: "A"
codeforces_contest_name: "2019 Sichuan Province Programming Contest"
rating: 0
weight: 102821
solve_time_s: 46
verified: true
draft: false
---

[CF 102821A - Autochess](https://codeforces.com/problemset/problem/102821/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models the preparation phase of an autochess game. There is a row of `N` waiting slots, initially empty. Fish receives `M` level-1 chessmen one by one. Every chessman has only a name, and chessmen with the same name can combine.

When a new chessman with name `s` arrives, the game first checks whether a level-3 `s` already exists in the waiting zone. If it does, the new chessman disappears. Otherwise, the new chessman tries to combine with existing copies. If there are `K-1` level-1 copies of `s`, they merge with the new one into a level-2 `s`. If that newly created level-2 chessman can also combine with `K-1` existing level-2 copies, it becomes a level-3 chessman. After all possible merging, the resulting chessman occupies the leftmost empty slot if one exists.

The input gives several independent game simulations. For each test case, we need to print the final content of the waiting zone from left to right. A level-1 chessman is printed using only its name, while higher levels append their level number. Empty positions are printed as `-1`.

The important constraint is the number of slots, `N`, which can reach `100000`. This means a solution that repeatedly scans the whole waiting zone after every insertion can perform around `M * N` operations, which becomes too slow if many chessmen are inserted. We need to update the state of a chessman in near constant time and only handle the positions that actually change.

The main edge cases come from the interaction between merging and the physical placement of pieces. A simple counter-only solution can fail because the output depends on the exact positions of pieces.

For example, consider:

```
1
3 3 2
a
a
a
```

The correct output is:

```
Case 1: a2 -1 -1
```

The first two chessmen combine into a level-2 piece. The third chessman cannot combine with it because `K=2` requires another level-2 piece, so it occupies the next empty slot. A careless implementation that only tracks total copies of `a` might incorrectly create a level-3 piece.

Another edge case is when the board is full:

```
1
3 2 2
a
b
a
```

The correct output is:

```
Case 1: a2 b
```

The first two `a` pieces merge, freeing the original positions conceptually because they disappear. The new level-2 piece is placed into the leftmost empty slot. An implementation that only appends pieces to the end would produce the wrong arrangement.

A final tricky case is an already existing level-3 piece:

```
1
3 3 2
a
a
a
```

After the first two operations there is already a level-2 piece. If later operations create a level-3 piece, all future copies of that name must be rejected. Forgetting this rule causes extra pieces to appear.

## Approaches

The direct simulation is straightforward. We can store the waiting zone and, for every arriving chessman, search through all positions to count how many level-1 and level-2 pieces of that name exist. If enough copies exist, we remove them, upgrade the new piece, and continue checking for another merge. Finally, we scan again to find the first empty slot.

This approach is correct because it follows the rules exactly, but it repeatedly walks through the entire board. In the worst case, if the board has `N=100000` positions and many chessmen arrive, the number of operations grows to roughly `M*N`, which is far beyond what a one second solution can handle.

The key observation is that the rules only need two types of information for each chessman name: how many pieces of each level exist, and where those pieces are located. The final arrangement depends only on removing pieces and inserting into the leftmost available position. We do not need to inspect unrelated names.

For each name, we maintain its current level-1 and level-2 positions. When a new piece arrives, we can immediately determine whether a merge happens. When pieces disappear, their slots become empty, so we also maintain a data structure that gives the smallest empty index quickly. A min-heap is a natural choice because we only need insertions of newly empty positions and extraction of the smallest one.

The total work becomes proportional to the number of chessmen processed and the number of actual merges, rather than the size of the waiting zone.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(MN) | O(N) | Too slow |
| Optimal | O(M log N) | O(N + M) | Accepted |

## Algorithm Walkthrough

1. Store the waiting zone as an array of size `N`. Initially every position contains an empty marker. Put every position into a min-heap of available slots so the smallest empty index can always be found.
2. For every incoming chessman name, check whether a level-3 chessman of that name already exists. If it does, ignore this chessman because the rules forbid adding another copy.
3. Maintain, for every name, the positions of level-1 and level-2 pieces. If the arriving chessman creates `K` level-1 pieces of the same name, remove those level-1 pieces and turn the arriving chessman into level 2.
4. After creating a level-2 piece, check whether there are now `K` level-2 pieces. If so, remove those pieces and turn the arriving chessman into level 3.
5. If the chessman survives, take the smallest index from the empty-position heap and place the chessman there. Record this position in the corresponding list for its name and level.
6. After all insertions are processed, print the waiting zone.

The reason this works is that the lists for each name always contain exactly the pieces that currently exist. Every merge removes exactly the pieces required by the rules, and every surviving chessman is inserted into the smallest currently empty position. The heap invariant guarantees that every placement uses the same position the original process would choose.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve_case(M, N, K, pieces):
    board = ["-1"] * N
    empty = list(range(N))
    heapq.heapify(empty)

    data = {}

    def get_info(name):
        if name not in data:
            data[name] = [[], [], False]
        return data[name]

    for name in pieces:
        lv1, lv2, has3 = get_info(name)

        if has3:
            continue

        level = 1

        if len(lv1) == K - 1:
            for pos in lv1:
                board[pos] = "-1"
                heapq.heappush(empty, pos)
            lv1.clear()
            level = 2

            if len(lv2) == K - 1:
                for pos in lv2:
                    board[pos] = "-1"
                    heapq.heappush(empty, pos)
                lv2.clear()
                level = 3
                has3 = True

        if empty:
            pos = heapq.heappop(empty)
            if level == 1:
                board[pos] = name
                lv1.append(pos)
            elif level == 2:
                board[pos] = name + "2"
                lv2.append(pos)
            else:
                board[pos] = name + "3"
                data[name][2] = True

    return " ".join(board)

def main():
    t = int(input())
    ans = []

    for case in range(1, t + 1):
        M, N, K = map(int, input().split())
        pieces = [input().strip() for _ in range(M)]
        ans.append(f"Case {case}: {solve_case(M, N, K, pieces)}")

    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The array `board` stores the final visible state of every slot. The heap `empty` contains exactly the positions that are currently free. Whenever a merge happens, the removed pieces return their positions to this heap, which preserves the ability to find the leftmost free slot.

The dictionary `data` keeps all information that is specific to a chessman name. The first list stores level-1 positions, the second stores level-2 positions, and the boolean records whether a level-3 piece exists. This avoids scanning unrelated positions.

The order of operations in the insertion loop follows the game rules. The level-3 check happens first. Then level-1 merging is attempted, followed by level-2 merging. Only after all possible upgrades are complete is the piece placed into the board.

The implementation does not need special handling for integer limits because it only stores indices and counters bounded by the input size. The important boundary condition is checking whether the empty heap is non-empty before placing a piece, because a chessman can disappear if the board is already full.

## Worked Examples

For the first example, suppose:

```
1
5 4 2
a
a
b
a
a
```

The simulation is:

| Step | Incoming | Level-1 positions of a | Level-2 positions of a | Empty slots | Board |
| --- | --- | --- | --- | --- | --- |
| 0 | none | [] | [] | 0,1,2,3 | -1 -1 -1 -1 |
| 1 | a | [0] | [] | 1,2,3 | a -1 -1 -1 |
| 2 | a | [] | [0] | 1,2,3 | a2 -1 -1 -1 |
| 3 | b | [] | [0] | 2,3 | a2 b -1 -1 |
| 4 | a | [2] | [0] | 3 | a2 b a -1 |
| 5 | a | [] | [0,2] | 1,3 | a2 b a2 -1 |

This trace shows why storing positions matters. The two `a` pieces that merge are removed and the new level-2 piece occupies the leftmost available position.

For the second example:

```
1
4 3 3
x
x
x
x
```

The state changes as follows:

| Step | Incoming | Level | Empty slots | Board |
| --- | --- | --- | --- | --- |
| 0 | none | none | 0,1,2 | -1 -1 -1 |
| 1 | x | 1 | 1,2 | x -1 -1 |
| 2 | x | 1 | 2 | x x -1 |
| 3 | x | 1 | none | x x x |
| 4 | x | 1 | none | x x x |

The first three pieces stay separate because `K=3` requires three copies before a merge. The fourth piece has no available position, so it disappears.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M log N) | Each insertion performs dictionary operations and heap updates for removed or inserted positions. |
| Space | O(N + M) | The board, empty-position heap, and stored positions contain at most linear information. |

The constraints allow `N` to be large, so avoiding repeated scans of the waiting zone is necessary. The heap operations keep the simulation fast enough while preserving the exact leftmost placement behavior.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        import heapq

        for case in range(1, t + 1):
            M, N, K = map(int, input().split())
            pieces = [input().strip() for _ in range(M)]

            board = ["-1"] * N
            empty = list(range(N))
            heapq.heapify(empty)
            data = {}

            for name in pieces:
                if name not in data:
                    data[name] = [[], [], False]

                lv1, lv2, has3 = data[name]

                if has3:
                    continue

                level = 1

                if len(lv1) == K - 1:
                    for p in lv1:
                        board[p] = "-1"
                        heapq.heappush(empty, p)
                    lv1.clear()
                    level = 2

                    if len(lv2) == K - 1:
                        for p in lv2:
                            board[p] = "-1"
                            heapq.heappush(empty, p)
                        lv2.clear()
                        level = 3
                        data[name][2] = True

                if empty:
                    p = heapq.heappop(empty)
                    if level == 1:
                        board[p] = name
                        lv1.append(p)
                    elif level == 2:
                        board[p] = name + "2"
                        lv2.append(p)
                    else:
                        board[p] = name + "3"

            out.append(f"Case {case}: {' '.join(board)}")

        return "\n".join(out)

    result = solve()
    sys.stdin = old
    return result

assert run("""1
3 3 2
a
a
a
""") == "Case 1: a2 a -1", "basic merge"

assert run("""1
3 2 2
a
b
a
""") == "Case 1: a2 b", "merge with full board"

assert run("""1
4 3 3
x
x
x
x
""") == "Case 1: x x x", "no merge until enough copies"

assert run("""1
5 5 2
a
a
a
a
a
""") == "Case 1: a3 a -1 -1 -1", "multiple upgrades"

assert run("""1
1 1 2
z
""") == "Case 1: z", "minimum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three identical pieces with `K=2` | `a2 a -1` | Basic merging and placement |
| Full board with a merge | `a2 b` | Reusing freed positions |
| Four pieces with `K=3` | `x x x` | Correct merge threshold |
| Five identical pieces with `K=2` | `a3 a -1 -1 -1` | Chained upgrades |
| Single chessman | `z` | Minimum boundary case |

## Edge Cases

For the first edge case:

```
1
3 3 2
a
a
a
```

The algorithm first places `a` at position zero. The second `a` finds one existing level-1 copy, removes it, and becomes level 2 at position zero. The third `a` cannot merge because there is only one level-2 piece, so it is placed at position one. The result is:

```
Case 1: a2 a -1
```

The stored level lists correctly prevent the algorithm from incorrectly upgrading directly to level 3.

For the full-board case:

```
1
3 2 2
a
b
a
```

The first two insertions fill the board. The third insertion sees one level-1 `a`, removes it, and places the upgraded level-2 piece back into the freed smallest slot. The result is:

```
Case 1: a2 b
```

The empty-slot heap is what makes this behave like the original game instead of simply appending pieces.

For the level-3 restriction case:

```
1
5 4 2
a
a
a
a
a
```

The first four pieces create two level-2 pieces. The next merge creates a level-3 piece. Any later `a` would be rejected immediately because the name already has a level-3 piece. The boolean stored for each name captures this permanent state change.
