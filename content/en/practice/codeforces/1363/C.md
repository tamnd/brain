---
title: "CF 1363C - Game On Leaves"
description: "The game is played on a tree, which is an undirected, connected, acyclic graph. Each node is numbered from $1$ to $n$, and one node $x$ is special. Two players take turns removing leaf nodes, where a leaf is a node with only one neighbor, along with its connecting edge."
date: "2026-06-11T12:32:11+07:00"
tags: ["codeforces", "competitive-programming", "games", "trees"]
categories: ["algorithms"]
codeforces_contest: 1363
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 646 (Div. 2)"
rating: 1600
weight: 1363
solve_time_s: 372
verified: true
draft: false
---

[CF 1363C - Game On Leaves](https://codeforces.com/problemset/problem/1363/C)

**Rating:** 1600  
**Tags:** games, trees  
**Solve time:** 6m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played on a tree, which is an undirected, connected, acyclic graph. Each node is numbered from $1$ to $n$, and one node $x$ is special. Two players take turns removing leaf nodes, where a leaf is a node with only one neighbor, along with its connecting edge. The player who removes the special node $x$ wins. Ayush moves first, and the task is to determine which player will win under optimal play.

The input describes the tree as $n$ nodes and $n-1$ edges, followed by a number of test cases $t$. The output is a string identifying the winner for each test case. The number of nodes $n$ is at most $1000$, so any algorithm that is quadratic in $n$ or better will run efficiently.

Non-obvious edge cases include situations where the special node $x$ is already a leaf, because then Ayush can remove it on the first turn and immediately win. Another subtle case arises when $x$ has exactly one neighbor and the total number of nodes is small. If a careless solution assumes all nodes have degree at least 2 or blindly alternates turns without checking the structure around $x$, it will give the wrong result.

For example, consider a tree with $n=3$, $x=1$, and edges $1-2$ and $1-3$. Nodes $2$ and $3$ are leaves. Ayush can only remove one of these, after which $1$ becomes a leaf, and Ashish can remove it, winning the game. This illustrates that even with a small tree, the local structure around $x$ determines the outcome.

## Approaches

A brute-force approach would simulate the game explicitly. At each turn, we would enumerate all current leaves, generate the tree that results from each possible move, and recursively compute the winner for the next turn. This method is correct because it directly applies the rules and explores all game states, but it is exponentially slow in $n$ because the number of subtrees grows rapidly, and $n$ can be up to 1000, making this approach infeasible.

The optimal approach uses the insight that the game is completely determined by the degree of the special node $x$ and the parity of the total number of nodes. If $x$ has degree $1$ or $0$, it is a leaf or isolated, so Ayush can remove it immediately and win. Otherwise, the game becomes equivalent to a simple turn-based removal of $n-1$ nodes, with the last move determining the winner. Specifically, if $n$ is even, Ayush will remove the last leaf and win; if $n$ is odd, Ashish will remove the last leaf and win. This observation reduces the problem to checking the degree of $x$ and the parity of $n$, avoiding any simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read the number of nodes $n$ and the special node $x$.
3. Construct an adjacency list for the tree from the $n-1$ edges.
4. Compute the degree of the special node $x$.
5. If the degree of $x$ is $1$ or $0$, Ayush wins immediately because he can remove it on the first move.
6. Otherwise, check the parity of $n$. If $n$ is even, Ayush wins; if $n$ is odd, Ashish wins. The reasoning is that each move removes exactly one node, and the player who moves when the total number of nodes remaining is $1$ wins.

Why it works: The key invariant is that the winner is determined by who is forced to remove the last node. If $x$ is a leaf initially, Ayush immediately wins. Otherwise, each move reduces the number of nodes by one, so the parity of $n$ relative to the first move determines who will remove the last node. The algorithm leverages the tree structure without explicit simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            adj[u].append(v)
            adj[v].append(u)
        if len(adj[x]) <= 1:
            print("Ayush")
        else:
            if n % 2 == 0:
                print("Ayush")
            else:
                print("Ashish")

if __name__ == "__main__":
    main()
```

The solution first reads the input efficiently and constructs the adjacency list for the tree. Checking `len(adj[x])` gives the degree of the special node, which directly determines an immediate win scenario. The parity check on `n` accounts for the alternation of moves when $x$ is not a leaf. Handling multiple test cases in a loop ensures correctness across varying inputs. A subtle point is using `n+1` for adjacency to match 1-based node indices.

## Worked Examples

**Sample Input 1**

```
1
3 1
2 1
3 1
```

| Step | n | x | deg(x) | n % 2 | Winner |
| --- | --- | --- | --- | --- | --- |
| initial | 3 | 1 | 2 | 1 | Ashish |

Ayush cannot remove node 1 immediately, so we check parity. n=3 is odd, so the second player Ashish wins.

**Custom Input 1**

```
1
4 2
1 2
2 3
3 4
```

| Step | n | x | deg(x) | n % 2 | Winner |
| --- | --- | --- | --- | --- | --- |
| initial | 4 | 2 | 2 | 0 | Ayush |

Degree of x is 2, so first move does not remove x. Total nodes n=4 is even, so Ayush wins.

These traces confirm that both the immediate leaf case and the parity-based scenario are correctly handled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Reading the tree edges and constructing the adjacency list for each test case takes O(n) time. |
| Space | O(n) | The adjacency list uses O(n) space, and a few integers per test case are negligible. |

The algorithm easily handles n ≤ 1000 and t ≤ 10 within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided samples
assert run("1\n3 1\n2 1\n3 1\n") == "Ashish", "sample 1"

# Custom cases
assert run("1\n4 2\n1 2\n2 3\n3 4\n") == "Ayush", "even n, x not leaf"
assert run("1\n1 1\n") == "Ayush", "single node, x is leaf"
assert run("1\n2 2\n1 2\n") == "Ayush", "x is leaf initially"
assert run("1\n5 3\n1 2\n2 3\n3 4\n4 5\n") == "Ashish", "odd n, x internal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 2, edges 1-2,2-3,3-4 | Ayush | Even n, x not leaf scenario |
| 1 node x=1 | Ayush | Single node edge case |
| 2 nodes x=2, edge 1-2 | Ayush | x is initially leaf |
| 5 nodes x=3, path | Ashish | Odd n, x internal node |

## Edge Cases

If the tree consists of a single node, that node is automatically a leaf. The algorithm handles this by checking `len(adj[x]) <= 1`, correctly reporting Ayush as the winner.

In the case where x is initially a leaf but n > 1, Ayush wins immediately, and the adjacency list correctly shows `len(adj[x]) == 1`, triggering the proper branch.

For long chains or trees with x as a central node of degree >1, the parity of n dictates the outcome. Constructing the adjacency list with 1-based indexing ensures that degree calculation is accurate, and the modulo check correctly identifies the player who will remove the last node. These edge cases confirm that both structural and parity-based logic are correctly implemented.
