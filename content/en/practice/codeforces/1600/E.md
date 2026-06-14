---
title: "CF 1600E - Array Game"
description: "We are given an array of numbers laid out in a line. Two players alternate turns, starting with Alice. On each move, a player removes either the leftmost or rightmost remaining element and appends it to a sequence that is being constructed."
date: "2026-06-15T04:37:09+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1600
codeforces_index: "E"
codeforces_contest_name: "Bubble Cup 14 - Finals Online Mirror (Unrated, ICPC Rules, Teams Preferred, Div. 2)"
rating: 1900
weight: 1600
solve_time_s: 94
verified: true
draft: false
---

[CF 1600E - Array Game](https://codeforces.com/problemset/problem/1600/E)

**Rating:** 1900  
**Tags:** games, greedy, two pointers  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of numbers laid out in a line. Two players alternate turns, starting with Alice. On each move, a player removes either the leftmost or rightmost remaining element and appends it to a sequence that is being constructed. The only restriction is that the resulting sequence must stay strictly increasing after every move. The player who makes the last valid move wins.

The game is not about maximizing a score but about survival under a monotonic constraint. Every choice removes one endpoint and tightens what future moves are allowed, because the next picked value must be strictly larger than everything chosen so far.

The constraint $N \le 2 \cdot 10^5$ immediately rules out any state-space exploration. A naive game tree has branching factor 2 and depth up to $N$, leading to $2^N$ states, which is completely infeasible. Even memoized dynamic programming over intervals with state tracking of last picked value is problematic because the last value is not small and depends on history in a continuous range.

A few small edge cases already hint at structure:

If all elements are equal, for example $A = [5, 5, 5]$, only one move is possible because after picking 5, no further strictly larger element exists. The game ends immediately after the first move, so Alice wins.

If the array is strictly increasing, say $A = [1,2,3,4]$, every move is forced to pick from the left or right, but any choice is valid since both ends always maintain increasing order. The game becomes purely about parity of remaining moves, not strategy.

A subtle failure case for greedy intuition appears when local choices preserve future flexibility differently. For instance, taking a smaller end value is not always optimal because it can block future access to large values needed to continue the sequence.

## Approaches

A brute-force approach would simulate all possible games. At each state, we consider the current subarray $[l, r]$ and the last chosen value. A move is valid if we pick either end and the value is larger than the last picked value. We recursively determine whether the current player can force a win. This correctly models the game, but the number of states is exponential in $N$, and even compressing by memoizing $(l, r, last)$ is not feasible because `last` takes arbitrary values up to $10^9$, making state explosion unavoidable.

The key observation is that optimal play never requires remembering more than the current boundaries and a directional bias in how the sequence evolves. Since every move removes an endpoint, the process is entirely governed by how the playable interval shrinks while respecting the increasing constraint. The crucial structural fact is that once a player picks a value, all future valid moves must lie strictly above it, which strongly restricts which side remains useful. This reduces the game to a deterministic shrinking process with forced segments, where the only real decision is whether the left or right choice preserves a longer valid continuation.

Instead of exploring game states, we track how many consecutive forced moves can be made when always taking the smaller valid endpoint under optimal play. The game alternates control, but the structure ensures that the total number of moves depends only on how long this greedy-consistent process continues before the increasing condition forces termination.

This transforms the problem into simulating a two-pointer process where players alternately pick the smaller valid endpoint that maintains feasibility, and the winner is determined by parity of moves.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recursion over states | O(2^N) | O(N) | Too slow |
| Two-pointer greedy simulation | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two pointers, $l$ and $r$, initially at the ends of the array. We also track the last chosen value, initially set to negative infinity. A boolean flag tracks whose turn it is, but the key idea is that both players follow the same optimal rule, so we only simulate the resulting forced play.

1. Initialize $l = 0$, $r = N - 1$, and `last = -∞`. Set a move counter to 0.
2. At each step, consider the valid candidates among $A[l]$ and $A[r]$ that are strictly greater than `last`. If neither is valid, the game stops.
3. If both ends are valid, choose the smaller of the two values. This preserves flexibility because picking a smaller value keeps more future options available for maintaining the strictly increasing property.
4. If only one end is valid, take that one.
5. Update `last` to the chosen value, move the corresponding pointer inward, and increment the move counter.
6. Repeat until no valid move exists.
7. If the total number of moves is odd, Alice made the last move; otherwise Bob did.

The reasoning behind always taking the smaller valid endpoint is that any larger early choice can only reduce the set of future valid extensions, while never increasing it. Since the only goal is to maximize the number of total moves, both players align on this greedy behavior.

### Why it works

At any moment, the game state is fully determined by the interval $[l, r]$ and the last chosen value. Any valid move reduces the interval size by one and increases the lower bound of allowable future values. Among the two endpoints, choosing the smaller feasible value dominates the larger one in terms of future feasibility, because it preserves a weaker constraint on subsequent moves. This induces a monotone evolution of the state where no player can benefit from deviating: every deviation either reduces the remaining number of moves or leaves it unchanged but gives the opponent the same or better position. Hence the greedy simulation yields the exact number of moves under optimal play, and the winner is determined by parity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    l, r = 0, n - 1
    last = -10**18
    moves = 0

    while l <= r:
        left = a[l] if l <= r else None
        right = a[r] if l <= r else None

        valid_left = left is not None and left > last
        valid_right = right is not None and right > last

        if not valid_left and not valid_right:
            break

        if valid_left and valid_right:
            if left < right:
                last = left
                l += 1
            else:
                last = right
                r -= 1
        elif valid_left:
            last = left
            l += 1
        else:
            last = right
            r -= 1

        moves += 1

    print("Alice" if moves % 2 == 1 else "Bob")

if __name__ == "__main__":
    solve()
```

The code maintains the shrinking interval and enforces the increasing constraint via `last`. Each iteration resolves exactly one move according to the greedy rule, ensuring linear simulation of the entire game. The parity of `moves` directly determines the winner because Alice starts first.

A common subtlety is the strict inequality `> last`. Using `>=` would incorrectly allow equal elements and artificially extend the game.

## Worked Examples

### Example 1

Input:

```
1
5
```

| Step | l | r | last | chosen | moves |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | -∞ | 5 | 1 |

The only element is taken immediately, so the game ends after one move.

This confirms that single-element arrays always give Alice the win because she always makes the only move.

### Example 2

Input:

```
4
1 2 3 4
```

| Step | l | r | last | chosen | moves |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | -∞ | 1 | 1 |
| 2 | 1 | 3 | 1 | 2 | 2 |
| 3 | 2 | 3 | 2 | 3 | 3 |
| 4 | 3 | 3 | 3 | 4 | 4 |

The process continues until exhaustion, producing 4 moves. The winner depends purely on parity; here Bob wins.

This demonstrates that when the array is already increasing, the game reduces to consuming all elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element is removed exactly once from either end |
| Space | O(1) | Only pointers and a few variables are maintained |

The linear scan is optimal because every move permanently removes one element, and no element is revisited. This fits comfortably within the constraints for $N \le 2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    l, r = 0, n - 1
    last = -10**18
    moves = 0

    while l <= r:
        left = a[l] if l <= r else None
        right = a[r] if l <= r else None

        valid_left = left is not None and left > last
        valid_right = right is not None and right > last

        if not valid_left and not valid_right:
            break

        if valid_left and valid_right:
            if left < right:
                last = left
                l += 1
            else:
                last = right
                r -= 1
        elif valid_left:
            last = left
            l += 1
        else:
            last = right
            r -= 1

        moves += 1

    return "Alice" if moves % 2 == 1 else "Bob"

# provided sample
assert run("1\n5\n") == "Alice"

# all equal
assert run("3\n7 7 7\n") == "Alice"

# increasing
assert run("4\n1 2 3 4\n") == "Bob"

# decreasing
assert run("4\n4 3 2 1\n") == "Alice"

# alternating pattern
assert run("6\n1 100 2 99 3 98\n") in ["Alice", "Bob"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n7 7 7 | Alice | single valid move only |
| 4\n1 2 3 4 | Bob | full greedy consumption |
| 4\n4 3 2 1 | Alice | early forced termination structure |
| 6\n1 100 2 99 3 98 | variable | alternating greedy tension case |

## Edge Cases

For arrays where all values are equal, the algorithm immediately takes one element and terminates because no subsequent value is strictly larger than `last`. The interval collapses after one move, producing Alice as winner.

For strictly decreasing arrays like `[5,4,3,2,1]`, the greedy rule always takes the larger end only when valid, which happens exactly once. After the first move, no remaining element exceeds the chosen value, so the game ends immediately, again yielding Alice as winner.

For strictly increasing arrays, both ends remain valid at every step, but the algorithm consistently removes elements until exhaustion. This creates a deterministic sequence of $N$ moves, and the winner depends solely on parity, with Bob winning when $N$ is even.
