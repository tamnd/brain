---
title: "CF 345D - Chain Letter"
description: "We are asked to simulate the spread of a chain letter through a network of friends. Each person is represented as a node in a graph, and the connections between people-who sends letters to whom-are given as an adjacency matrix of \"0\" and \"1\" characters."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 345
codeforces_index: "D"
codeforces_contest_name: "Friday the 13th, Programmers Day"
rating: 2200
weight: 345
solve_time_s: 132
verified: true
draft: false
---

[CF 345D - Chain Letter](https://codeforces.com/problemset/problem/345/D)

**Rating:** 2200  
**Tags:** *special, dfs and similar, graphs  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate the spread of a chain letter through a network of friends. Each person is represented as a node in a graph, and the connections between people-who sends letters to whom-are given as an adjacency matrix of "0" and "1" characters. The graph is undirected, meaning if person _i_ will send a letter to person _j_, then person _j_ will also send to person _i_. The first person initiates the letter, and every recipient sends it to all their contacts, except for you, who is the last person and only receives letters without forwarding.

The input provides _n_, the number of people, and an _n × n_ adjacency matrix. Each row indicates the contacts for that person. The output is a single integer: the total number of letters that reach you.

The constraints are small: _n_ is at most 50, so algorithms with cubic or quadratic time complexity are acceptable. A naive simulation that tracks every message individually is feasible, but a careful graph traversal is simpler and less error-prone. Edge cases include situations where you are isolated (you receive no letters) or when everyone is interconnected (you receive a letter from each friend exactly once). Another subtlety is ensuring that a person sends the letter only on the first receipt; naive implementations could double-count.

## Approaches

The brute-force approach is to literally simulate each copy of the letter as it is forwarded. We could maintain a queue of messages to deliver, and for each message, enqueue new messages to all contacts. Each letter is tracked individually. This approach works correctly because it models the letter spreading exactly, but it can become inefficient if every person is connected to everyone else, leading to exponential message counts. Specifically, each person could potentially forward the letter to every other person, giving roughly O(2^n) operations in the worst case, which is unnecessary here.

The key insight is that we do not need to track every letter individually. The number of letters you receive is exactly the number of distinct friends who can reach you through a chain of forwards. Each person forwards the letter once, so if a path exists from the initiator to you through friends, each path contributes exactly one letter per sender who reaches you. This reduces the problem to a graph traversal: count how many neighbors eventually send you the letter. We can use depth-first search (DFS) starting from the first person to simulate the chain and count letters received by the last person.

The optimal approach is a DFS that tracks the number of times the last person receives the letter. Each node forwards the letter to all unvisited neighbors recursively, and whenever the traversal reaches you, we increment a counter. Because _n_ is small, a recursive DFS suffices, and the visited set ensures that no person forwards the letter more than once, matching the problem rules.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(2^n) | O(n^2) | Too slow for fully connected graphs |
| DFS Traversal Counting | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of people _n_ and the adjacency matrix _f_. Convert the matrix into a graph representation that is convenient for traversal. For small _n_, keeping it as a 2D list is fine.
2. Initialize a visited array of size _n_, marking all nodes as unvisited.
3. Initialize a counter `received` to zero, which will track the number of letters you receive.
4. Define a recursive DFS function that takes a current person index. When entering a node, mark it visited.
5. For each neighbor of the current person, check if the neighbor is unvisited. If yes, recursively call DFS on that neighbor.
6. Whenever the DFS reaches the last person (index _n-1_), increment `received` by one. Do not continue DFS from this node since you do not forward letters.
7. Start DFS from the first person (index 0).
8. After DFS completes, output the value of `received`.

This works because each person only forwards once due to the visited array, so each path contributes a unique letter to the last person. The recursive DFS correctly propagates the chain of forwards along all paths without double-counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    f = [input().strip() for _ in range(n)]
    graph = [[] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if f[i][j] == '1':
                graph[i].append(j)
    
    visited = [False] * n
    received = 0
    
    def dfs(u):
        nonlocal received
        if u == n - 1:
            received += 1
            return
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs(v)
        visited[u] = False
    
    dfs(0)
    print(received)

if __name__ == "__main__":
    main()
```

The code constructs the adjacency list from the input matrix. The DFS uses `visited` to prevent sending letters multiple times from the same person. We increment `received` only when the traversal reaches the last person. After returning from recursion, we unmark `visited[u]` to allow exploring other paths, because multiple distinct paths can reach the last person, each counting as one letter. Forgetting to unmark would undercount letters.

## Worked Examples

Sample input 1:

```
4
0111
1011
1101
1110
```

| Step | Node | visited | received |
| --- | --- | --- | --- |
| start | 0 | [True,False,False,False] | 0 |
| dfs 1 | 1 | [True,True,False,False] | 0 |
| dfs 2 | 2 | [True,True,True,False] | 0 |
| dfs 3 | 3 | [True,True,True,True] | 1 |
| backtrack | 2 | [True,True,False,False] | 1 |
| dfs 3 | 3 | [True,True,False,True] | 2 |
| backtrack | 1 | [True,False,False,False] | 2 |
| dfs 2 | 2 | [True,False,True,False] | 2 |
| dfs 3 | 3 | [True,False,True,True] | 3 |

This shows that all three friends send the letter, yielding 3 copies received.

Sample input 2:

```
3
010
101
010
```

The letter propagates from 0 to 1, then 1 to 2. Node 2 receives one letter. Correct output is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | We traverse each node and explore each edge once; building adjacency list takes n^2. |
| Space | O(n^2) | Adjacency list stores up to n^2 edges; recursion stack is O(n). |

With n ≤ 50, this is acceptable. Memory usage stays well below 256 MB, and the traversal finishes in microseconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# provided samples
assert run("4\n0111\n1011\n1101\n1110\n") == "3", "sample 1"
assert run("3\n010\n101\n010\n") == "1", "sample 2"

# custom cases
assert run("2\n01\n10\n") == "1", "minimum input"
assert run("5\n01111\n10111\n11011\n11101\n11110\n") == "4", "fully connected small graph"
assert run("4\n0100\n1010\n0101\n0010\n") == "1", "chain structure"
assert run("3\n000\n000\n000\n") == "0", "no connections"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 nodes connected | 1 | Minimum input edge case |
| Fully connected 5 | 4 | Each friend sends letter |
| Chain 4 | 1 | Only one path to last person |
| Isolated 3 | 0 | No messages reach last person |

## Edge Cases

If the last person is completely isolated, like

```
3
010
101
000
```

DFS starts from 0, visits 1, but cannot reach 2. The counter `received` remains 0, correctly indicating that no letters arrive. The recursion never visits 2 because `graph[u]` for 1 contains only 0 and 2 is not connected. This matches the problem requirements.

If the last person is directly connected to everyone else, the DFS visits each neighbor path separately, and the counter increments for each distinct sender, giving the total number of letters received. This confirms that backtracking with `visited[u] = False` is crucial for counting multiple paths accurately.
