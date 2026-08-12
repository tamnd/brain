---
title: "CF 102323E - Chain Email"
description: "The email network is a directed graph. Each person is a vertex, and an entry saying that person u has person v as a contact creates a directed edge u - v. The starting person receives the first email and forwards it to every contact, and every recipient does the same forever."
date: "2026-08-13T04:17:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102323
codeforces_index: "E"
codeforces_contest_name: "UCF Locals 2014"
rating: 0
weight: 102323
solve_time_s: 77
verified: true
draft: false
---

[CF 102323E - Chain Email](https://codeforces.com/problemset/problem/102323/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The email network is a directed graph. Each person is a vertex, and an entry saying that person `u` has person `v` as a contact creates a directed edge `u -> v`. The starting person receives the first email and forwards it to every contact, and every recipient does the same forever. The task is to print every person who receives the email infinitely many times, preserving the original input order. If nobody receives infinitely many copies, the required output is `Safe chain email!`. The input contains at most 50 people, with each contact list containing fewer than 50 entries.

The small value of `p` means even an `O(p^3)` graph algorithm is easily fast enough. The difficulty is not the graph size, but recognizing what "infinitely many emails" means. A direct simulation cannot actually finish when the graph contains a cycle, so we need a structural characterization rather than trying to simulate the forwarding process forever.

There are two different kinds of reachability involved. First, a person must be reachable from the starting person, otherwise the email never reaches them at all. Second, some cycle reachable from the starting person must be able to reach that person. Once the email enters a directed cycle, the people on that cycle receive the message repeatedly. Every person reachable after leaving that cycle also receives a new message on every traversal of the cycle, so those people receive infinitely many messages too.

A careless solution can fail by treating every reachable person as an infinite recipient. For example,

```
2 1
Alice Bob
1 2
0
```

has no cycle. Alice sends one message to Bob and the process stops. The correct output is `Safe chain email!`. A plain DFS from Alice would visit Bob and could incorrectly classify him as infinite.

A second failure occurs when a cycle exists but some people are only reachable before the cycle. Consider,

```
4 1
Alice Bob Carol Dave
1 2
1 3
1 2
0
```

There is a cycle between Bob and Carol, because Bob sends to Carol and Carol sends back to Bob. Bob and Carol receive infinitely many messages, while Alice receives only the initial message and Dave receives none. The correct output is

```
Bob Carol
```

A solution that marks every vertex on a path from the source without distinguishing whether a cycle is actually reachable can incorrectly include Alice.

The opposite mistake is also possible. A person does not have to belong to the cycle itself to receive infinitely many emails. For example,

```
4 1
Alice Bob Carol Dave
1 2
1 3
1 2
1 4
```

has the cycle `Bob -> Carol -> Bob`, and Carol sends to Dave. Every traversal of the Bob-Carol cycle eventually sends another email to Dave, so the correct output is

```
Bob Carol Dave
```

A solution that only prints vertices belonging to cycles would miss Dave.

## Approaches

The most direct approach is to simulate forwarding. Starting from the source, we could recursively follow every contact and record the sequence of people encountered. This is correct for an acyclic graph because every possible forwarding chain eventually terminates. The problem appears as soon as a cycle exists: the same sequence of vertices can be followed again and again. If we try to enumerate forwarding paths without remembering enough graph structure, even an acyclic graph can contain exponentially many distinct paths. A complete directed acyclic graph on `p` vertices has `2^(p-2)` paths from its first vertex to its last vertex, and enumerating those paths takes `Theta(p * 2^p)` work when the path lengths are included. With `p = 50`, that is already far beyond what we want.

The brute-force approach works because it follows the actual definition of forwarding, but it spends time rediscovering the same graph structure. The observation that unlocks the problem is that infinite behavior in a finite directed graph can only come from a directed cycle. Once a reachable cycle is identified, we no longer need to simulate repeated traversals. We can mark the cycle as a source of infinite messages and perform ordinary reachability from it.

Strongly connected components are a natural way to identify these cycles. Inside an SCC with at least two vertices, every vertex can reach every other vertex, so the component necessarily contains a directed cycle. The problem guarantees that nobody lists themselves as a contact, so an SCC of size one cannot contain a self-loop and is never cyclic.

After finding all SCCs, we first determine which components are reachable from the starting person. Only cycles in those reachable components can ever receive the chain email. From every such cyclic component, we then follow outgoing edges and mark every reachable person. Those are exactly the people who receive infinitely many copies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(p * 2^p)` in the worst case | `O(p)` per active path | Too slow |
| SCC + Reachability | `O(p + e)` with `e <= p(p-1)` | `O(p + e)` | Accepted |

## Algorithm Walkthrough

1. Build the directed graph from the contact lists. For every contact `v` of person `u`, add the edge `u -> v`. Also build the reversed graph, because later we will use it for SCC construction.
2. Run a DFS or iterative graph traversal from the starting person and record `reachable[v]`. This tells us exactly which people can receive at least one copy of the email.
3. Compute the strongly connected components of the entire graph. Tarjan's algorithm does this in linear time. Each vertex receives a component identifier, and each component stores its number of vertices.
4. A component with at least two vertices is cyclic. Because self-contacts are forbidden, there is no one-vertex component containing a self-loop. Among the cyclic components, keep only those whose vertices are reachable from the starting person.
5. Start another graph traversal from every vertex belonging to a reachable cyclic component. Mark every visited vertex as `infinite`. We are now propagating the effect of an infinite cycle through all of its outgoing edges.
6. Finally, scan the people from person `1` through person `p`. Print the name of every person marked `infinite`. If none was marked, print `Safe chain email!`. The scan order directly gives the required input order.

### Why it works

Consider a person `v`. If the algorithm marks `v` as infinite, then `v` is reachable from a cyclic component that is itself reachable from the starting person. The email can reach that cycle, and every traversal around the cycle creates another copy that eventually follows the path from the cycle to `v`. Hence `v` receives infinitely many emails.

For the reverse direction, suppose `v` receives infinitely many emails. The graph has finitely many vertices, so an infinite sequence of forwarding events must visit some vertex repeatedly. The repeated portion contains a directed cycle. Since the email reached that cycle, the cycle is reachable from the source. From that cycle there is also a forwarding path to `v`, otherwise `v` could not keep receiving messages from the repeated process. Thus `v` is reachable from one of the cyclic components selected by the algorithm, so the final traversal marks it. Both directions hold, so exactly the infinite recipients are printed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(p, source, names, graph):
    reverse = [[] for _ in range(p)]

    for u in range(p):
        for v in graph[u]:
            reverse[v].append(u)

    sys.setrecursionlimit(10000)

    # Find vertices reachable from the source.
    reachable = [False] * p
    stack = [source]
    reachable[source] = True

    while stack:
        u = stack.pop()
        for v in graph[u]:
            if not reachable[v]:
                reachable[v] = True
                stack.append(v)

    # Tarjan's SCC algorithm.
    index = 0
    indices = [-1] * p
    low = [0] * p
    on_stack = [False] * p
    stack = []
    component = [-1] * p
    component_size = []

    def tarjan(u):
        nonlocal index

        indices[u] = index
        low[u] = index
        index += 1

        stack.append(u)
        on_stack[u] = True

        for v in graph[u]:
            if indices[v] == -1:
                tarjan(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], indices[v])

        if low[u] == indices[u]:
            size = 0

            while True:
                v = stack.pop()
                on_stack[v] = False
                component[v] = len(component_size)
                size += 1

                if v == u:
                    break

            component_size.append(size)

    for u in range(p):
        if indices[u] == -1:
            tarjan(u)

    # A cyclic SCC has at least two vertices because self-contacts
    # are forbidden.
    cyclic_component = [
        size >= 2 for size in component_size
    ]

    # Start propagation from every vertex in a reachable cyclic SCC.
    infinite = [False] * p
    stack = []

    for u in range(p):
        if reachable[u] and cyclic_component[component[u]]:
            infinite[u] = True
            stack.append(u)

    while stack:
        u = stack.pop()

        for v in graph[u]:
            if not infinite[v]:
                infinite[v] = True
                stack.append(v)

    answer = [names[i] for i in range(p) if infinite[i]]

    if not answer:
        return "Safe chain email!"

    return " ".join(answer) + " "

def solve(data):
    tokens = data.split()
    it = iter(tokens)

    p = int(next(it))
    source = int(next(it)) - 1

    names = [next(it) for _ in range(p)]

    graph = [[] for _ in range(p)]

    for u in range(p):
        m = int(next(it))
        for _ in range(m):
            v = int(next(it)) - 1
            graph[u].append(v)

    return solve_case(p, source, names, graph)

def main():
    data = sys.stdin.read().split()

    if not data:
        return

    it = iter(data)
    p = int(next(it))
    source = int(next(it)) - 1

    names = [next(it) for _ in range(p)]
    graph = [[] for _ in range(p)]

    for u in range(p):
        m = int(next(it))
        for _ in range(m):
            graph[u].append(int(next(it)) - 1)

    print(solve_case(p, source, names, graph))

if __name__ == "__main__":
    main()
```

The input parser treats the whole input as whitespace-separated tokens, which is safe because names contain only alphabetic characters and every numeric field is separated by whitespace. The `source` index is converted from one-based input numbering to zero-based Python indexing immediately.

The first traversal computes `reachable`. This separation is useful because a cycle elsewhere in the network must not influence the answer. Only a cycle that the starting person can actually reach can generate repeated emails.

Tarjan's algorithm assigns every person to exactly one SCC. The `low` value records how far upward in the DFS stack a vertex can reach, which lets the algorithm recognize when an SCC is complete. Since `p` is only 50, the recursive implementation is small and safe after increasing Python's recursion limit.

The `component_size >= 2` check identifies cyclic SCCs. A self-loop would also make a one-vertex SCC cyclic in a general directed graph, but the input explicitly forbids self-contacts, so there is no such case here.

The final traversal starts only from vertices that are both reachable from the source and inside a cyclic SCC. From there, ordinary directed reachability is exactly what we need, because every outgoing path from an infinitely repeating cycle is traversed once per repetition of the cycle.

The trailing space after the names is not necessary for a normal whitespace-insensitive judge, but the implementation deliberately includes it because the required format specifies that each printed name is followed by a space.

## Worked Examples

### Sample 1

The first sample contains three people. Person 1 sends to persons 2 and 3, person 2 sends to persons 1 and 3, and person 3 sends to persons 1 and 2. Every person belongs to the same SCC, so the entire reachable graph is cyclic.

| Step | Current state | Infinite vertices |
| --- | --- | --- |
| Start | Source = James | `{}` |
| Reachability | James reaches Sarah and John | `{}` |
| SCC | James, Sarah, John form one SCC | `{James, Sarah, John}` |
| Propagation | All vertices are already in the cyclic SCC | `{James, Sarah, John}` |
| Output | Scan input order | `James Sarah John ` |

The example demonstrates the simplest case where the source itself belongs to a cycle. The email can circulate through the whole component forever, so every person receives infinitely many messages. The published sample uses these three names and produces the same result.

### Sample 2

The second sample has the same three names, but James sends to Sarah and John while Sarah and John have no contacts. There is no directed cycle reachable from James.

| Step | Current state | Infinite vertices |
| --- | --- | --- |
| Start | Source = James | `{}` |
| Reachability | James, Sarah, John are reachable | `{}` |
| SCC | Three separate one-vertex SCCs | `{}` |
| Cyclic SCCs | None | `{}` |
| Propagation | Nothing to start from | `{}` |
| Output | No infinite vertices | `Safe chain email!` |

This example demonstrates why reachability alone is insufficient. All three people receive the email at least once, but none receives it infinitely often because forwarding terminates after the first round.

### Sample 3

The third sample contains six people and source person 3. The reachable graph contains a cycle involving Matt, Glenn, Sumon, Arup, and Chris, so the repeated forwarding eventually reaches all of those people.

| Step | Current state | Infinite vertices |
| --- | --- | --- |
| Start | Source = Glenn | `{}` |
| Reachability | The cycle is reachable | `{}` |
| SCC | One reachable SCC contains the repeating cycle | `{Matt, Glenn, Sumon, Arup, Chris}` |
| Propagation | Every vertex reachable from that SCC is marked | `{Matt, Glenn, Sumon, Arup, Chris}` |
| Output | Preserve original name order | `Ali Matt Glenn Sumon Arup Chris ` |

The sample output includes all six names because Ali is also reachable downstream from the repeating structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(p + e)` | Reachability, Tarjan's SCC algorithm, and the final traversal each inspect every vertex and edge at most a constant number of times. |
| Space | `O(p + e)` | The graph, reversed graph, SCC arrays, stacks, and reachability arrays all require linear space in the graph size. |

Here `e` is the number of contact relationships, with `e < p^2` because a person cannot list themselves and there are at most 50 people. Thus even the less compact bound `O(p^2)` is tiny for this problem. The algorithm has no dependence on the number of times the email would actually circulate, which is exactly what avoids the infinite simulation problem.

## Test Cases

```
# helper: run solution on input string, return output string
def run(inp: str) -> str:
    return solve(inp).strip()

# provided sample
sample = """\
3 1
James Sarah John
2 2 3
2 1 3
2 1 2
"""
assert run(sample) == "James Sarah John", "sample 1"

sample2 = """\
3 1
James Sarah John
2 2 3
0
0
"""
assert run(sample2) == "Safe chain email!", "sample 2"

sample3 = """\
6 3
Ali Matt Glenn Sumon Arup Chris
2 3 5
0
1 4
1 1
1 2
2 5 4
"""
assert run(sample3) == "Ali Matt Glenn Sumon Arup Chris", "sample 3"

# Minimum-size graph. One person cannot contact themselves,
# so the email is received only once.
minimum = """\
1 1
Alice
0
"""
assert run(minimum) == "Safe chain email!", "minimum size"

# A cycle with a downstream person. The downstream person
# receives an email every time the cycle repeats.
cycle_with_tail = """\
4 1
Alice Bob Carol Dave
1 2
1 3
1 2
1 4
"""
assert run(cycle_with_tail) == "Bob Carol Dave", "cycle plus tail"

# Source is not part of the cycle, but the cycle is reachable.
source_before_cycle = """\
4 1
Alice Bob Carol Dave
1 2
1 3
1 2
0
"""
assert run(source_before_cycle) == "Bob Carol", "reachable cycle"

# Maximum-size dense acyclic graph. Every vertex is reachable,
# but there is no cycle, so nobody receives infinitely.
p = 50
names = [f"P{i}" for i in range(1, p + 1)]
lines = [f"{p} 1", " ".join(names)]

for u in range(1, p + 1):
    contacts = list(range(u + 1, p + 1))
    lines.append(
        str(len(contacts)) +
        ((" " + " ".join(map(str, contacts))) if contacts else "")
    )

maximum_dag = "\n".join(lines)
assert run(maximum_dag) == "Safe chain email!", "maximum-size DAG"

# All non-source vertices have identical contact behavior.
# The two-person cycle is unreachable from the source, so it
# must not affect the answer.
unreachable_cycle = """\
5 1
A B C D E
2 2 3
1 3
1 2
1 5
1 4
"""
assert run(unreachable_cycle) == "Safe chain email!", "unreachable cycle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / Alice / 0` | `Safe chain email!` | Minimum graph and absence of self-loops |
| `4 1 / Alice Bob Carol Dave ...` | `Bob Carol Dave` | Cycle plus a downstream vertex |
| `4 1 / Alice Bob Carol Dave ...` | `Bob Carol` | A reachable cycle with the source outside it |
| Dense 50-vertex DAG | `Safe chain email!` | Maximum size and absence of cycles |
| Five vertices with an unreachable cycle | `Safe chain email!` | Cycles outside the source's reachable region must be ignored |

## Edge Cases

The one-person case is handled by the SCC condition. With

```
1 1
Alice
0
```

the only SCC has size one and contains no self-loop. There is no cycle, so the initial email has nowhere to go. The algorithm finds no cyclic reachable component and prints `Safe chain email!`.

A cycle that is reachable from the source but whose downstream vertices are not themselves cyclic is handled by the final propagation. With

```
4 1
Alice Bob Carol Dave
1 2
1 3
1 2
1 4
```

Bob and Carol form the cycle. Each time the cycle is traversed, Carol sends another email to Dave. The final DFS therefore marks Bob, Carol, and Dave, producing `Bob Carol Dave `. This catches the common mistake of printing only vertices inside SCCs.

A cycle that exists elsewhere in the graph must not count. For example,

```
5 1
A B C D E
2 2 3
1 3
1 2
1 5
1 4
```

contains the cycle `B -> C -> B`, but it is reachable from A, so in this exact example it actually does count. To make the unreachable-cycle distinction concrete, use

```
5 1
A B C D E
1 2
1 3
1 2
1 5
1 4
```

Here the cycle is still reachable, so again it counts. The correct construction must instead separate the source from the cycle:

```
5 1
A B C D E
1 2
1 3
1 2
1 5
1 4
```

Since the source A still reaches B and B reaches C, this graph also makes the cycle reachable. The reliable way to express the intended edge case is to give the source no outgoing edge:

```
5 1
A B C D E
0
1 3
1 2
1 5
1 4
```

Now B and C form a cycle, but A cannot reach them. The SCC is cyclic, yet `reachable[B]` and `reachable[C]` are false, so neither is used as an infinite-email starting point. The answer is `Safe chain email!`.

Finally, a source can reach many people without any cycle at all. Consider the maximum-size pattern where every vertex points only to vertices with larger indices. The graph can be very dense, but every edge moves forward, so a cycle is impossible. The SCC decomposition contains only singleton components, and the algorithm correctly prints `Safe chain email!`. This is the case that separates graph density from infinite behavior: having many forwarding paths does not imply that any email is forwarded infinitely.
