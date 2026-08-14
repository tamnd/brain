---
title: "CF 102452B - Binary Tree"
description: "We have a rooted binary tree with node 1 as its root. Alice and Bob alternately remove one subtree. A move is legal only when the removed subtree is a perfect full binary tree, meaning every internal node has exactly two children and all leaves are at the same depth."
date: "2026-08-14T15:57:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102452
codeforces_index: "B"
codeforces_contest_name: "2019-2020 ICPC Asia Hong Kong Regional Contest"
rating: 0
weight: 102452
solve_time_s: 56
verified: true
draft: false
---

[CF 102452B - Binary Tree](https://codeforces.com/problemset/problem/102452/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted binary tree with node 1 as its root. Alice and Bob alternately remove one subtree. A move is legal only when the removed subtree is a perfect full binary tree, meaning every internal node has exactly two children and all leaves are at the same depth. The removed subtree may be the entire tree, so the tree can become empty.

The player who has no legal move loses. Since every nonempty binary tree has at least one leaf, and a single leaf is itself a perfect full binary tree, every nonempty position always has at least one legal move. Consequently, the game ends exactly when every node has been removed.

The input contains several independent test cases. For each case, the edges describe the rooted binary tree, with node 1 as the root. The task is simply to determine whether the first player, Alice, or the second player, Bob, wins under optimal play.

The number of nodes in one test case is at most 5000, and the sum of the numbers of nodes over all test cases is at most 50000. This bound is more than enough for a linear-time solution, but it rules out approaches that enumerate a large collection of possible game states. In fact, the tree structure itself turns out not to matter at all, so we can avoid even traversing the edges.

There are two edge cases that are easy to mishandle. First, a tree containing only its root has one node, and that root is a perfect full binary tree. For the input

```
11
```

Alice removes the root immediately, so the answer is `Alice`. An implementation that assumes every move removes at least two nodes would get this wrong.

The second edge case is an even-sized tree where a player can remove a large perfect subtree. For example,

```
141 21 33 4
```

The answer is `Bob`. Alice cannot force a win merely by choosing a particular subtree. Every legal removal contains an odd number of nodes, so after each move the parity of the number of remaining nodes flips. Since the whole tree has four nodes, exactly an even number of moves must be made before the tree becomes empty, regardless of which legal subtrees are chosen.

## Approaches

A direct game-theoretic solution would recursively examine every legal move. For each resulting tree, we would determine whether the next player is winning by recursively examining its legal moves. This is correct because a position is winning precisely when it has at least one move leading to a losing position.

The problem is the number of different positions. A move deletes an entire rooted subtree, and different sequences of deletions can produce many different remaining trees. A brute-force search can have exponentially many states. There can be up to 2 n different subsets of nodes in the broadest possible state-space bound, and examining each state can itself require scanning the tree. A straightforward implementation can therefore reach O(n2 n ) work, which is completely impractical even for n=5000.

The brute-force works because it explicitly models every possible choice, but the game has a much stronger invariant.

Every legal move removes a perfect full binary tree. If such a tree has height h, its number of nodes is

1+2+4+⋯+2 h =2 h+1 −1.

This number is always odd. Therefore, every single move removes an odd number of nodes.

There is one more crucial observation. A nonempty binary tree always contains a leaf, and a leaf is a perfect full binary tree of height zero. Thus there is always at least one legal move while the tree is nonempty. The game can only stop when the tree has no nodes left.

Suppose the game lasts for k moves. Each move removes an odd number of nodes, so the total number of removed nodes has the same parity as k. Since eventually all n nodes are removed,

k≡n(mod2).

Alice wins exactly when the number of moves is odd, because Alice moves first. Hence Alice wins exactly when n is odd.

The actual shape of the tree, the available perfect subtrees, and the players' choices are irrelevant to the winner. We only need the parity of the node count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n2 n ) in a straightforward state search | O(n2 n ) | Too slow |
| Optimal | O(n) input processing, O(1) game logic | O(1) beyond input storage | Accepted |

## Algorithm Walkthrough

1. Read the number n of nodes in the current tree. The edges do not affect the answer, but they still have to be consumed from the input.
2. If n is odd, print `Alice`. The total number of moves must be odd, so the first player makes the final move.
3. If n is even, print `Bob`. The total number of moves must be even, so the second player makes the final move.
4. Repeat the same process for every test case.

### Why it works

Every legal move removes a perfect full binary tree, whose number of nodes is 2 h+1 −1, always odd. A nonempty binary tree always contains a leaf, so a legal move always exists until the tree becomes empty. Consequently, if the game lasts k moves, the sum of k odd numbers equals the original n, giving k≡n(mod2). Alice makes the first, third, fifth and other odd-numbered moves, so she wins exactly when k is odd, which is exactly when n is odd.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    t = int(input())    ans = []
    for _ in range(t):        n = int(input())
        # The edges do not affect the answer, but must be consumed.        for _ in range(n - 1):            input()
        if n & 1:            ans.append("Alice")        else:            ans.append("Bob")
    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":    solve()
```

The first line gives the number of test cases. For each case, we read n, then consume exactly n−1 edge lines because the input describes a tree.

The parity test `n & 1` checks whether the number of nodes is odd. There is no need to build an adjacency list, root the tree, calculate subtree sizes, or identify perfect subtrees. All of those operations would solve information that the parity invariant makes irrelevant.

The single-node case is handled naturally. With n=1, `n & 1` is true, so the program prints `Alice`.

There is also no integer overflow concern. Python integers can represent the input directly, and the algorithm performs only a parity check. The edge-reading loop is necessary even though the edges are unused, because leaving them unread would corrupt the input position for the next test case.

## Worked Examples

Only one sample is provided in the statement, so the second trace uses a small custom tree.

### Sample 1

The sample tree has five nodes.

```
151 21 33 43 5
```

The relevant state is just the number of nodes.

| Step | Remaining nodes | Parity | Result |
| --- | --- | --- | --- |
| Initial | 5 | Odd | Alice wins |

The tree contains a perfect subtree rooted at node 3 with three nodes. Alice can remove it, leaving nodes 1 and 2. Bob can remove node 2, leaving node 1. Alice then removes node 1. The game takes three moves, matching the odd parity of the original five nodes.

### Custom Example 2

Consider a four-node tree.

```
141 21 33 4
```

The trace is:

| Step | Remaining nodes | Parity | Player to move |
| --- | --- | --- | --- |
| 0 | 4 | Even | Alice |
| 1 | 3 | Odd | Bob |
| 2 | 1 | Odd | Alice |
| 3 | 0 | Even | Bob |

Each move removes an odd number of nodes. In this particular sequence the players remove one node at a time, giving four moves. Bob makes the fourth move and wins the game. Other legal choices can change the sizes of individual removals, but cannot change the parity of the total number of moves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We only read the n−1 edges and perform one parity check. |
| Space | O(1) auxiliary space | The tree is never stored. |

Across all test cases, the total number of nodes is at most 50000, so the total running time is O(50000) apart from input handling. This is comfortably within the available limits, and the algorithm uses constant auxiliary memory.

## Test Cases

```python
Pythonimport sysimport io

def solve():    input = sys.stdin.readline    t = int(input())    ans = []
    for _ in range(t):        n = int(input())        for _ in range(n - 1):            input()
        ans.append("Alice" if n & 1 else "Bob")
    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:    old_stdin = sys.stdin    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)    sys.stdout = io.StringIO()
    try:        solve()        return sys.stdout.getvalue()    finally:        sys.stdin = old_stdin        sys.stdout = old_stdout

# Provided sampleassert run(    """151 21 33 43 5""") == "Alice\n", "sample 1"
# Minimum-size treeassert run(    """11""") == "Alice\n", "single root is a legal perfect subtree"
# Smallest even treeassert run(    """121 2""") == "Bob\n", "one move removes one node, leaving another"
# Perfect tree with 7 nodesassert run(    """171 21 32 42 53 63 7""") == "Alice\n", "perfect tree with odd size"
# Maximum-size boundary, using a valid path of 5000 nodesedges = "\n".join(f"{i} {i + 1}" for i in range(1, 5000))assert run(f"1\n5000\n{edges}\n") == "Bob\n", "maximum even n"
# Multiple test cases, checking input consumptionassert run(    """4121 231 21 341 21 33 4""") == "Alice\nBob\nAlice\nBob\n", "mixed parities"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n = 1` | `Alice` | The root itself is a legal perfect subtree. |
| `n = 2`, edge `1 2` | `Bob` | Smallest even tree and the parity boundary. |
| Perfect tree with `n = 7` | `Alice` | A complete perfect binary tree does not require special handling. |
| Valid tree with `n = 5000` | `Bob` | Maximum node-count boundary and even parity. |
| Four mixed cases | `Alice`, `Bob`, `Alice`, `Bob` | Correct handling of multiple test cases and edge consumption. |

## Edge Cases

For a single-node tree,

```
11
```

there are no edge lines to read. The only node is itself a perfect full binary tree, so Alice can remove it immediately. The algorithm sees n=1, which is odd, and prints `Alice`.

For the smallest even tree,

```
121 2
```

the only legal move is to remove a leaf. One node remains, and the other player removes it. The game has two moves, so Bob wins. The algorithm prints `Bob` because 2 is even.

A perfect tree can look deceptively special, but it follows exactly the same rule. For

```
171 21 32 42 53 63 7
```

Alice can remove the whole seven-node tree in one move, giving an immediate win. More generally, a perfect tree has 2 h+1 −1 nodes, which is always odd, so its answer is automatically `Alice`.

Finally, the shape can be extremely unbalanced. A path is still a valid binary tree because every node has at most two children. For a path containing 5000 nodes, most subtrees are not perfect, but every leaf remains a legal move. The exact available moves do not matter. Since 5000 is even, every complete play has an even number of moves and Bob wins. This is why the implementation can safely ignore all edge endpoints after consuming them.
