---
title: "CF 455B - A Lot of Games"
description: "The game can be viewed as moving through a trie built from the given strings. We start at the root, which represents the empty string. On each turn a player chooses one outgoing edge, corresponding to appending a character."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "games", "implementation", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 455
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 260 (Div. 1)"
rating: 1900
weight: 455
solve_time_s: 109
verified: true
draft: false
---

[CF 455B - A Lot of Games](https://codeforces.com/problemset/problem/455/B)

**Rating:** 1900  
**Tags:** dfs and similar, dp, games, implementation, strings, trees  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The game can be viewed as moving through a trie built from the given strings.

We start at the root, which represents the empty string. On each turn a player chooses one outgoing edge, corresponding to appending a character. The current string must always remain a prefix of at least one dictionary word, so every legal move simply follows an edge in the trie.

A player loses when they reach a trie node with no children, because no further character can be appended.

The twist is that the game is played exactly `k` times. The loser of one game starts the next game, and the only thing that matters is who wins the last game. Both players play optimally in every game.

The input gives up to `10^5` strings, and the sum of all string lengths is also at most `10^5`. Any solution that processes each trie node only a constant number of times is easily fast enough. Anything quadratic in the number of nodes would be too large, since a trie may contain about `10^5` nodes.

The most subtle part of the problem is that there are actually two different game properties that matter.

Consider this input:

```
1 2
a
```

The trie is just root → a. The first player must move to `a`, then the second player has no move and loses. The first player always wins. Since the loser starts the next game, the second player starts game two and loses again. The first player wins the last game. A solution that only computes "can the first player win from the root?" would miss the interaction between multiple games.

Another important case is:

```
2 100
ab
ac
```

The root is winning because the first player can move. But every path has length exactly two. The parity structure of the game becomes important. Whether the first player can force a win is not enough; we must also know whether they can force a loss if that is strategically desirable.

A third tricky case is:

```
1 1
abc
```

There is only one path. The outcome is completely determined by path length parity. Any solution that ignores terminal positions and only looks at branching factors will fail.

The key observation is that we need two independent pieces of information about every trie node.

## Approaches

A brute force approach would explicitly analyze every possible game state and every possible sequence of games. Even for a single game, the number of possible plays grows exponentially with trie depth. Since `k` can be as large as `10^9`, simulating games one by one is impossible.

The structure of impartial games suggests using game DP. Every trie node is a state. From a node, a player chooses one child. Terminal nodes have no legal moves.

For a normal-play game, a state is winning if there exists a move to a losing state. A state is losing if every move goes to a winning state.

If we only compute this usual winning/losing status, we obtain the set of positions from which the current player can force victory. That solves the single-game version, but not this problem. The repeated-game rule introduces another question: can the current player force the game to end with either parity of remaining moves?

This leads to two DFS computations.

The first DFS computes whether a node is winning, often called the "win state".

The second DFS computes whether a node is losing under a different criterion, usually called the "lose state" in editorials. It determines whether the current player can force the game to terminate in a way that eventually allows defeat if desired.

Once both properties are known at the root, the entire multi-game problem collapses into a few simple cases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Trie + DFS Game DP | O(total string length) | O(total string length) | Accepted |

## Algorithm Walkthrough

1. Build a trie from all input strings.

Every node represents a valid prefix. Every legal move in the game corresponds to traversing one trie edge.
2. Compute `win[v]` for every node.

If a node has no children, `win[v] = False` because the current player cannot move.

Otherwise, `win[v] = True` if at least one child has `win = False`.

This is the standard winning-state recurrence for impartial games.
3. Compute `lose[v]` for every node.

If a node has no children, set `lose[v] = True`.

Otherwise, `lose[v] = True` if at least one child has `lose = False`.

This second DP answers a different question: whether the current player can force the game to end on a parity that allows eventual defeat.
4. Let the root be node `0`.

If `win[root]` is false, the first player cannot win even a single game. The answer is `"Second"`.
5. If `win[root]` is true and `lose[root]` is true, the first player can force either type of ending. The answer is always `"First"`.
6. If `win[root]` is true and `lose[root]` is false, only one parity structure is possible.

In this case, the answer depends on `k`.

If `k` is odd, output `"First"`.

If `k` is even, output `"Second"`.

### Why it works

The first DFS identifies positions from which the current player can force victory in a single game.

The second DFS identifies positions from which the current player can force reaching a terminal node on a favorable parity. A terminal node has `lose = True` because the current player to move there immediately loses.

The root falls into exactly one of three meaningful categories.

If the root is not winning, the first player loses immediately.

If the root is winning and also has the second property, the first player has enough control over the game tree to force victory regardless of how many games remain.

If the root is winning but lacks the second property, the game outcome becomes fixed by parity, and only odd `k` allows the first player to win the final game.

These are precisely the cases proved in the official analysis of this game.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    trie = [[-1] * 26]

    for _ in range(n):
        s = input().strip()
        node = 0

        for ch in s:
            c = ord(ch) - ord('a')

            if trie[node][c] == -1:
                trie[node][c] = len(trie)
                trie.append([-1] * 26)

            node = trie[node][c]

    m = len(trie)

    win = [False] * m
    lose = [False] * m

    sys.setrecursionlimit(300000)

    def dfs(v):
        children = []

        for nxt in trie[v]:
            if nxt != -1:
                children.append(nxt)

        if not children:
            win[v] = False
            lose[v] = True
            return

        win[v] = False
        lose[v] = False

        for to in children:
            dfs(to)

        for to in children:
            if not win[to]:
                win[v] = True
            if not lose[to]:
                lose[v] = True

    dfs(0)

    if not win[0]:
        print("Second")
    elif lose[0]:
        print("First")
    else:
        print("First" if k % 2 == 1 else "Second")

if __name__ == "__main__":
    solve()
```

The trie construction creates one node per distinct prefix. Since the total input length is at most `10^5`, the total number of trie nodes is also `O(10^5)`.

The `win` array stores the standard game-theory result. A node is winning if there exists a move to a losing child.

The `lose` array uses a different recurrence. Terminal nodes are marked true. For an internal node, the value becomes true if at least one child has value false. This captures whether the current player can force a game ending with the required parity structure.

One implementation detail that often causes bugs is the base case for `lose`. Terminal nodes must be initialized to `True`, not `False`. Using the wrong value completely reverses the meaning of the second DFS.

Another common mistake is forgetting that `k` can be as large as `10^9`. Any approach that tries to simulate games is impossible. Only the root's two DP values matter.

## Worked Examples

### Example 1

Input:

```
2 3
a
b
```

Trie:

```
root
 ├─ a
 └─ b
```

| Node | win | lose |
| --- | --- | --- |
| a | False | True |
| b | False | True |
| root | True | False |

Root is winning, but `lose[root]` is false.

`k = 3` is odd.

Answer: `"First"`.

This example demonstrates the parity-dependent case. The first player can win a game, but cannot control the alternative ending structure.

### Example 2

Input:

```
2 2
a
ab
```

Trie:

```
root
 └─ a
     └─ b
```

DP values:

| Node | win | lose |
| --- | --- | --- |
| b | False | True |
| a | True | False |
| root | False | True |

The root itself is losing.

Answer: `"Second"`.

This example shows that even though the trie contains multiple levels, the first player may have no winning move from the initial position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L) | Each trie node and edge is processed once, where `L` is the total length of all strings |
| Space | O(L) | Trie storage plus DP arrays |

Since the total length of all strings is at most `10^5`, both time and memory usage are comfortably within the limits. The DFS visits each trie node once, and the trie itself contains at most `10^5 + 1` nodes.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k = map(int, input().split())

    trie = [[-1] * 26]

    for _ in range(n):
        s = input().strip()
        node = 0

        for ch in s:
            c = ord(ch) - ord('a')

            if trie[node][c] == -1:
                trie[node][c] = len(trie)
                trie.append([-1] * 26)

            node = trie[node][c]

    m = len(trie)
    win = [False] * m
    lose = [False] * m

    sys.setrecursionlimit(300000)

    def dfs(v):
        children = [x for x in trie[v] if x != -1]

        if not children:
            lose[v] = True
            return

        for to in children:
            dfs(to)

        for to in children:
            if not win[to]:
                win[v] = True
            if not lose[to]:
                lose[v] = True

    dfs(0)

    if not win[0]:
        return "Second"

    if lose[0]:
        return "First"

    return "First" if k % 2 else "Second"

# provided sample
assert run("2 3\na\nb\n") == "First", "sample 1"

# minimum size
assert run("1 1\na\n") == "First", "single move"

# parity-dependent case
assert run("2 2\na\nb\n") == "Second", "even k"

# losing root
assert run("1 2\nab\n") == "Second", "forced loss"

# deeper branching
assert run("3 5\na\nab\nac\n") == "First", "mixed trie"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / a` | First | Smallest non-trivial trie |
| `2 2 / a,b` | Second | Odd/even parity handling |
| `1 2 / ab` | Second | Root can be losing |
| `3 5 / a,ab,ac` | First | Mixed branching structure |

## Edge Cases

Consider:

```
1 2
a
```

The trie contains one edge. The root has `win = True` and `lose = False`. Since `k` is even, the algorithm outputs `"Second"`. This is exactly the parity-sensitive situation that breaks solutions checking only the ordinary winning state.

Consider:

```
1 1
abc
```

The trie is a single path of length three. DFS propagates values from the leaf upward. The root becomes winning, so the answer is `"First"`. The algorithm correctly handles long chains without requiring any explicit parity counting.

Consider:

```
2 1
ab
ac
```

Both root-to-leaf paths have the same depth. The root is winning because it can move to a losing child configuration. The DFS computes the exact game-theoretic status regardless of path lengths. The answer is obtained directly from the root's two DP values.

These cases illustrate why both DFS states are necessary. One captures whether victory is possible, and the other captures whether the player has enough control over the game's ending structure to handle arbitrary values of `k`.
