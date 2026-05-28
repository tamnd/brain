---
title: "CF 134C - Swaps"
description: "Each player initially owns cards of exactly one color, their own color. Player i starts with a[i] cards, all of color i. During a swap, two players exchange one card each. A player may only give away cards of their own color, and may never receive a color they already possess."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 134
codeforces_index: "C"
codeforces_contest_name: "Codeforces Testing Round 3"
rating: 2200
weight: 134
solve_time_s: 135
verified: false
draft: false
---

[CF 134C - Swaps](https://codeforces.com/problemset/problem/134/C)

**Rating:** 2200  
**Tags:** constructive algorithms, graphs, greedy  
**Solve time:** 2m 15s  
**Verified:** no  

## Solution
## Problem Understanding

Each player initially owns cards of exactly one color, their own color. Player `i` starts with `a[i]` cards, all of color `i`. During a swap, two players exchange one card each. A player may only give away cards of their own color, and may never receive a color they already possess.

The goal is stronger than simply redistributing cards. Every player must eventually get rid of all cards of their own color. Since a player can only give their own color, every card of color `i` must be transferred away through swaps until none remain with player `i`.

The restriction about duplicate colors is the central difficulty. Once a player has received color `x`, they can never receive another color `x` again. A careless sequence of swaps can easily deadlock the process even when a solution exists.

The constraints are large. Both `n` and `s` are up to `2 * 10^5`, and the total number of swaps can also become large. Any algorithm that repeatedly scans all players or simulates card ownership explicitly would be too slow. Quadratic behavior is immediately ruled out. The solution must work close to linear time in the number of swaps produced.

There is also a hidden counting condition. Every swap removes exactly one card from each of two players. If player `i` starts with `a[i]` cards, then player `i` must participate in exactly `a[i]` swaps, because each swap lets them give away one of their cards. Summing over all players:

$$\sum a[i]$$

must be even, because every swap contributes `2` to the total participation count.

That condition alone is not sufficient. One player also cannot participate more times than all others combined. If some player has more cards than the rest together, eventually everyone else runs out of swaps while this player still has cards remaining.

For example:

```
3 5
5 0 0
```

Player 1 needs five swaps, but players 2 and 3 together can only participate in zero swaps. The correct answer is `No`.

Another subtle case is:

```
3 3
1 1 1
```

The total sum is odd. Since every swap consumes two cards, no sequence can finish all three cards. The correct answer is `No`.

A more interesting valid case is:

```
4 4
2 1 1 0
```

A naive greedy strategy might repeatedly pair the largest counts without tracking received colors carefully. That can create duplicate-color conflicts later. The correct construction must guarantee that no pair of players swaps more than once, because repeating a pair would force each player to receive the same color twice.

This observation becomes the key structural insight.

## Approaches

The brute-force way to think about the problem is to simulate card ownership directly. At every step, we search for two players who can legally swap, perform the exchange, update ownership sets, and continue until either all cards disappear or no legal move remains.

This approach is correct if it eventually succeeds, because it obeys the game rules literally. The problem is efficiency and state complexity. Each player may accumulate many colors, so checking legality requires maintaining large sets. Worse, deciding which pair to swap is non-trivial. A bad local choice can deadlock later even when a valid global solution exists.

In the worst case, there can be up to

$$\frac{\sum a[i]}{2}$$

swaps, and a naive search for a valid pair at every step becomes quadratic or worse.

The key observation is that a player can never receive the same color twice. Since player `i` always gives color `i`, another player can swap with player `i` at most once.

That transforms the problem completely.

Instead of thinking about cards, think about a graph. Every swap between players `u` and `v` creates one edge. Because two players cannot swap twice, the graph must be simple. The degree of player `i` equals exactly `a[i]`, since they must participate in that many swaps to give away all their cards.

Now the task becomes:

Construct a simple undirected graph on `n` vertices whose degree sequence is `a`.

This is a classic graphical-sequence problem.

The standard greedy construction for graphical sequences is the Havel-Hakimi process. Repeatedly take the vertex with largest remaining degree and connect it to several other highest-degree vertices. Every connection reduces both degrees by one.

This matches the swap interpretation perfectly. Connecting `u` and `v` means we schedule exactly one swap between them.

The brute-force simulation fails because it reasons about transient card ownership states. The graph interpretation removes that complexity entirely. Once we ensure no edge repeats, the color constraints are automatically satisfied.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(s²) or worse | O(s) | Too slow |
| Optimal | O(s log n) | O(s) | Accepted |

## Algorithm Walkthrough

1. Read the degree sequence `a[i]`.
2. Check whether the total sum of degrees is even.

Every swap contributes degree `2`, one to each endpoint. An odd sum makes a solution impossible immediately.
3. Insert all players with positive degree into a max-heap ordered by remaining degree.
4. Repeatedly extract the player `u` with largest remaining degree `d`.

Player `u` still needs `d` distinct swap partners.
5. If there are fewer than `d` other players remaining in the heap, the construction is impossible.

A simple graph cannot connect one vertex to more distinct vertices than currently exist.
6. Temporarily remove the next `d` highest-degree players from the heap.
7. For each extracted player `v`:

1. Add swap `(u, v)` to the answer.
2. Decrease `v`'s remaining degree by one.
3. Store `v` for reinsertion if its degree stays positive.
8. After processing all `d` neighbors, reinsert every updated player back into the heap.
9. Continue until the heap becomes empty.
10. Output all constructed edges as swaps.

### Why it works

The invariant is that the remaining degrees always describe the unfinished swap requirements of a partially constructed simple graph.

When we remove the largest degree vertex `u` and connect it to `d` distinct vertices, we satisfy all remaining swaps required for `u` in one step. Because every chosen neighbor is distinct, no repeated edge appears. Since each edge corresponds to one swap, no player receives the same color twice.

The Havel-Hakimi theorem guarantees that if a graphical realization exists, this greedy reduction preserves feasibility. If at some step there are not enough distinct vertices to connect to, then no simple graph with the required degrees can exist.

Thus the algorithm constructs a valid swap schedule exactly when one exists.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, s = map(int, input().split())
    a = list(map(int, input().split()))

    if sum(a) % 2:
        print("No")
        return

    pq = []

    for i, deg in enumerate(a, 1):
        if deg > 0:
            heapq.heappush(pq, (-deg, i))

    ans = []

    while pq:
        deg_u, u = heapq.heappop(pq)
        deg_u = -deg_u

        if deg_u > len(pq):
            print("No")
            return

        taken = []

        for _ in range(deg_u):
            deg_v, v = heapq.heappop(pq)
            deg_v = -deg_v

            ans.append((u, v))

            deg_v -= 1

            if deg_v < 0:
                print("No")
                return

            if deg_v > 0:
                taken.append((-deg_v, v))

        for item in taken:
            heapq.heappush(pq, item)

    print("Yes")
    print(len(ans))

    for u, v in ans:
        print(u, v)

solve()
```

The heap stores pairs `(-degree, vertex)` so that Python's min-heap behaves like a max-heap.

The most delicate part is the feasibility check:

```
if deg_u > len(pq):
```

Player `u` needs `deg_u` distinct neighbors. If fewer than that many vertices remain, a simple graph construction is impossible.

Another subtle detail is that we do not immediately reinsert neighbors after decrementing them. We first remove all `deg_u` neighbors, process them once each, then push updated values back. This guarantees all neighbors are distinct, preventing duplicate edges.

The algorithm never explicitly tracks card colors. The graph structure already enforces the color rules. Since each pair of players swaps at most once, no player can ever receive the same color twice.

## Worked Examples

### Example 1

Input:

```
4 8
2 2 2 2
```

Initial heap:

| Step | Extracted | Remaining Heap Degrees | New Edges |
| --- | --- | --- | --- |
| 1 | 1(2) | 2,2,2 | (1,2), (1,3) |
| 2 | 4(2) | 1,1 | (4,2), (4,3) |
| 3 | none | empty | done |

Produced swaps:

```
1 2
1 3
4 2
4 3
```

Every player appears exactly twice, matching their initial card count.

This trace demonstrates the degree interpretation directly. Once a player's degree becomes zero, they never appear again because all their cards have been given away.

### Example 2

Input:

```
3 3
1 1 1
```

The total degree sum is:

$$1 + 1 + 1 = 3$$

which is odd.

| Step | Check | Result |
| --- | --- | --- |
| 1 | sum % 2 == 1 | impossible |

Output:

```
No
```

This example shows the parity condition. Every swap removes exactly two remaining cards, so an odd total can never reach zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(s log n) | Every edge causes heap operations |
| Space | O(s) | Stores heap and answer edges |

The number of swaps equals

$$\frac{\sum a[i]}{2}$$

which is at most `2 * 10^5`. Each heap operation costs `O(log n)`, so the total runtime easily fits within the limit.

The memory usage is also safe because the answer itself can contain at most `2 * 10^5` swaps.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    input = sys.stdin.readline

    def solve():
        n, s = map(int, input().split())
        a = list(map(int, input().split()))

        if sum(a) % 2:
            print("No")
            return

        pq = []

        for i, deg in enumerate(a, 1):
            if deg > 0:
                heapq.heappush(pq, (-deg, i))

        ans = []

        while pq:
            deg_u, u = heapq.heappop(pq)
            deg_u = -deg_u

            if deg_u > len(pq):
                print("No")
                return

            taken = []

            for _ in range(deg_u):
                deg_v, v = heapq.heappop(pq)
                deg_v = -deg_v

                ans.append((u, v))

                deg_v -= 1

                if deg_v > 0:
                    taken.append((-deg_v, v))

            for item in taken:
                heapq.heappush(pq, item)

        print("Yes")
        print(len(ans))

        for u, v in ans:
            print(u, v)

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("4 8\n2 2 2 2\n").startswith("Yes")

# minimum case
assert run("1 0\n0\n") == "Yes\n0\n"

# odd total degree
assert run("3 3\n1 1 1\n") == "No\n"

# impossible because one degree too large
assert run("3 4\n4 0 0\n") == "No\n"

# complete graph on 4 vertices
res = run("4 6\n3 3 3 3\n")
assert res.startswith("Yes")

# sparse valid graph
res = run("5 4\n1 1 1 1 0\n")
assert res.startswith("Yes")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 0` | `Yes` with zero swaps | Minimum boundary |
| `3 3 / 1 1 1` | `No` | Odd total degree |
| `3 4 / 4 0 0` | `No` | Degree larger than available neighbors |
| `4 6 / 3 3 3 3` | `Yes` | Dense valid construction |
| `5 4 / 1 1 1 1 0` | `Yes` | Handles isolated vertices |

## Edge Cases

Consider the input:

```
3 3
1 1 1
```

The algorithm immediately checks the parity of the total degree sum. Since the sum is odd, it prints `No` before any heap processing begins. This avoids constructing partial swap sequences that can never terminate.

Now consider:

```
3 4
4 0 0
```

The heap initially contains only one vertex with degree `4`. When we pop it, the heap has zero remaining vertices. The condition

```
deg_u > len(pq)
```

becomes true because `4 > 0`. The algorithm correctly concludes that player 1 cannot swap with four distinct partners.

A more subtle valid case is:

```
4 4
2 1 1 0
```

Initial heap:

```
(2,1), (1,2), (1,3)
```

Player 1 connects to players 2 and 3. Their degrees become zero, and the heap empties cleanly.

Constructed swaps:

```
1 2
1 3
```

Player 1 gives away both of their cards, while players 2 and 3 each give away one. No pair repeats, so no duplicate color is ever received.

Finally, consider:

```
5 8
2 2 2 2 0
```

The isolated player causes no issue. The heap simply ignores zero-degree vertices. The algorithm builds a cycle among the four active players, satisfying all requirements without ever touching player 5.
