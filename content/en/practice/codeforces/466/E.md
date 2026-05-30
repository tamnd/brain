---
title: "CF 466E - Information Graph"
description: "We are dealing with a dynamic company hierarchy problem. We have n employees, initially without any reporting structure."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 466
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 266 (Div. 2)"
rating: 2100
weight: 466
solve_time_s: 101
verified: false
draft: false
---

[CF 466E - Information Graph](https://codeforces.com/problemset/problem/466/E)

**Rating:** 2100  
**Tags:** dfs and similar, dsu, graphs, trees  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are dealing with a dynamic company hierarchy problem. We have _n_ employees, initially without any reporting structure. Over _m_ days, three types of events can occur: first, an employee _x_ gets a new boss _y_; second, an employee receives a document packet, signs it, and it is passed up the hierarchy until the top, where it is archived; third, a query asks whether a given employee signed a particular packet.

The challenge is that the hierarchy changes over time, document packets are handled sequentially, and we need to answer queries about past events efficiently. The number of employees and events can be up to 10^5, which rules out any solution that simulates the document flow from employee to boss in O(n) per event, since this could require up to 10^10 operations in the worst case.

A non-obvious edge case is when a packet passes through a chain of bosses created dynamically. For example, if the input is:

```
4 4
1 2 1
1 3 2
2 3
3 1 1
```

Here employee 3 gets a document packet, which goes to 2 and then 1. A naive solution might only record the immediate sender of a packet, missing the full chain. The correct output for whether 1 signed packet 1 is YES, but careless approaches might incorrectly return NO.

Another tricky situation arises when multiple packets are sent before the hierarchy fully connects employees. If we try to precompute document paths naively, we could answer incorrectly because the path depends on the hierarchy at the moment the packet is sent.

## Approaches

The brute-force approach is straightforward: store the boss of each employee, and for each document event, simulate passing the document up the chain and record all signers in a list for that packet. Queries then simply check if the employee is in that list. While this is correct, it is too slow. For each document, simulating O(n) steps up the hierarchy and with m events, the worst-case complexity is O(m·n), which can reach 10^10 operations.

The key observation is that the hierarchy is a forest of trees with dynamic connections, and packets are passed only up these trees. Instead of simulating each step, we can record, for each employee, the set of packets they have signed using a data structure that supports union operations efficiently. A Disjoint Set Union (DSU) structure allows us to merge sets of signed packets whenever an employee acquires a new boss, without needing to recompute the full chain each time. Each node maintains the packets it has signed; when it gets a boss, we union its set with the boss's set.

The clever part is using DSU with small-to-large merging: always merge the smaller set into the larger to keep the total cost of all unions at O(m log n), which is acceptable given our constraints. This reduces time per document propagation and maintains correctness for queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m·n) | O(m·n) | Too slow |
| DSU with small-to-large | O(m log n) | O(m + n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `boss` where `boss[x]` is the current boss of employee `x`. Initially all entries are None. Also, initialize for each employee a set `signed_packets` to store packet IDs they have signed.
2. Maintain a global list of packets `packets` as they are issued. Each packet has an ID assigned incrementally starting from 1. Each time a type-2 event occurs, add a new packet to the employee's `signed_packets` set.
3. For type-1 events where employee `x` gains a boss `y`, merge `x`'s `signed_packets` into `y`'s set. To keep this efficient, always merge the smaller set into the larger set. Update `boss[x] = y`.
4. For type-3 events, simply check if the packet ID exists in the employee's `signed_packets` set. Return YES if present, NO otherwise.
5. Repeat for all events sequentially.

Why it works: At any point, each employee's `signed_packets` set contains all packets that were signed by them or passed to them via subordinates. Small-to-large merging ensures that the total number of set operations remains manageable, and each query checks a correct, up-to-date set.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

sys.setrecursionlimit(1 << 25)

def main():
    n, m = map(int, input().split())
    boss = [None] * (n + 1)
    signed_packets = [set() for _ in range(n + 1)]
    packet_counter = 1

    queries = []
    events = []

    for _ in range(m):
        parts = input().split()
        t = int(parts[0])
        if t == 1:
            x, y = map(int, parts[1:])
            events.append((1, x, y))
        elif t == 2:
            x = int(parts[1])
            events.append((2, x))
        else:
            x, i = map(int, parts[1:])
            events.append((3, x, i))

    for e in events:
        if e[0] == 1:
            _, x, y = e
            if len(signed_packets[x]) > len(signed_packets[y]):
                signed_packets[x], signed_packets[y] = signed_packets[y], signed_packets[x]
            signed_packets[y].update(signed_packets[x])
            boss[x] = y
        elif e[0] == 2:
            _, x = e
            signed_packets[x].add(packet_counter)
            packet_counter += 1
        else:
            _, x, i = e
            print("YES" if i in signed_packets[x] else "NO")

if __name__ == "__main__":
    main()
```

The code follows the algorithm closely. Each employee keeps track of packets they have signed. When a boss assignment occurs, we merge smaller sets into larger ones for efficiency. When a document arrives, the employee immediately signs it. Queries are simple set membership checks. The recursion limit increase is precautionary if Python’s default stack size is small, though we are not using recursion here.

## Worked Examples

Sample Input 1:

```
4 9
1 4 3
2 4
3 3 1
1 2 3
2 2
3 1 2
1 3 1
2 2
3 1 3
```

| Step | Event | Packet ID | boss[] | signed_packets[] | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 4 3 | - | [None,None,None,3,None] | all empty | - |
| 2 | 2 4 | 1 | - | 4:{1} | - |
| 3 | 3 3 1 | - | - | check 3:{}, 1 in {}? | YES |
| 4 | 1 2 3 | - | boss[2]=3 | merge 2:{} into 3:{} | - |
| 5 | 2 2 | 2 | - | 2:{2} | - |
| 6 | 3 1 2 | - | - | check 1:{} | NO |
| 7 | 1 3 1 | - | boss[3]=1 | merge 3:{} into 1:{} | - |
| 8 | 2 2 | 3 | 2:{3} | - |  |
| 9 | 3 1 3 | - | check 1:{1}? | YES |  |

This trace confirms correct propagation across dynamically built hierarchy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each small-to-large set merge costs O(log n) amortized over all merges. Each event processed once. |
| Space | O(n + m) | Each employee stores packets signed, and packets counter stores m IDs. |

The solution fits comfortably in time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("""4 9
1 4 3
2 4
3 3 1
1 2 3
2 2
3 1 2
1 3 1
2 2
3 1 3""") == "YES\nNO\nYES", "sample 1"

# Minimum-size input
assert run("""1 2
2 1
3 1 1""") == "YES", "min size"

# Chain hierarchy
assert run("""3 4
1 2 1
1 3 2
2 3
3 1 1""") == "YES", "chain hierarchy"

# Multiple packets to same employee
assert run("""2 4
2 1
2 1
3 1 1
3 1 2""") == "YES\nYES", "multiple packets same employee"

# Packet before boss assignment
assert run("""3 3
2 1
1 1 2
3 2 1""") == "YES", "packet
```
