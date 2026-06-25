---
title: "CF 106157J - Joust Sort"
description: "We are given a set of ordering rules between lowercase letters. A rule such as a < b means every occurrence of a must appear before every occurrence of b in the final rearranged word. A rule a b means the same thing as b < a. The input also contains a word."
date: "2026-06-25T11:19:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106157
codeforces_index: "J"
codeforces_contest_name: "2025 United Kingdom and Ireland Programming Contest (UKIEPC 2025)"
rating: 0
weight: 106157
solve_time_s: 37
verified: true
draft: false
---

[CF 106157J - Joust Sort](https://codeforces.com/problemset/problem/106157/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of ordering rules between lowercase letters. A rule such as `a < b` means every occurrence of `a` must appear before every occurrence of `b` in the final rearranged word. A rule `a > b` means the same thing as `b < a`.

The input also contains a word. We may rearrange its letters however we like, but the final arrangement must satisfy every ordering rule simultaneously.

The task is to output any valid rearrangement of the word. If the rules contradict each other, making it impossible to satisfy all of them at once, we must print `IMPOSSIBLE`.

A useful observation is that there are only 26 possible letters. Even though the number of rules can be as large as 700 and the word length can reach 100,000, the actual dependency graph is built on only 26 vertices.

The large word length tells us that repeatedly comparing or moving individual characters would be wasteful. The constraints instead suggest separating the problem into two parts. First, determine a valid global order of letters. Second, use the frequency of each letter to construct the answer efficiently.

A common source of mistakes is handling indirect contradictions.

Consider:

```
3
a < b
b < c
c < a
abc
```

The rules form a cycle. No arrangement can place `a` before `b`, `b` before `c`, and `c` before `a` at the same time. The correct output is:

```
IMPOSSIBLE
```

Another subtle case is when two letters have no relation.

```
1
b < n
banana
```

The rule only constrains `b` and `n`. The letter `a` is unrelated to both. Any arrangement where all `b` characters come before all `n` characters is valid. Multiple answers exist.

A third edge case occurs when the word does not contain some constrained letters.

```
2
x < y
y < z
banana
```

The constraints still participate in cycle detection, but missing letters contribute zero copies to the output. A valid topological order is still required.

## Approaches

A brute-force approach would try different permutations of the letters appearing in the word and check whether every rule is satisfied. This is immediately infeasible. Even if only 10 distinct letters appear, there are `10! = 3,628,800` possible orders.

The structure of the problem is much more restrictive than a general rearrangement problem. Every rule only describes a relative ordering between letter types. The exact positions of individual copies do not matter.

This suggests representing each letter as a vertex in a directed graph. For a rule `a < b`, we add an edge `a → b`. Any valid final arrangement must place letter `a` before letter `b`, so every valid solution corresponds to a topological ordering of this graph.

If the graph contains a cycle, no topological order exists and the answer is impossible.

If the graph is acyclic, a topological order gives a valid global ordering of all 26 letters. Once that order is known, constructing the word is easy. Count how many times each letter appears in the original word, then output all copies of each letter following the topological order.

The graph is tiny, only 26 vertices, so topological sorting is essentially constant time. The dominant work becomes counting characters and writing the output string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k!) | O(k) | Too slow |
| Optimal | O(n + \|s\|) | O(n + 26) | Accepted |

Here `n` is the number of ordering rules and `|s|` is the word length.

## Algorithm Walkthrough

1. Create a directed graph with 26 vertices, one for each lowercase letter.
2. For every rule:

- If the rule is `a < b`, add edge `a → b`.
- If the rule is `a > b`, add edge `b → a`.

This encodes the required precedence relationship.
3. Compute the indegree of every vertex.
4. Run Kahn's topological sort.

- Start with every vertex whose indegree is zero.
- Repeatedly remove such a vertex and append it to the topological order.
- Decrease the indegree of its outgoing neighbours.
- Whenever a neighbour reaches indegree zero, add it to the queue.
5. If fewer than 26 vertices are processed, the graph contains a cycle. Output `IMPOSSIBLE`.
6. Count the frequency of every letter in the given word.
7. Traverse the computed topological order. For each letter, append that letter exactly as many times as it appears in the word.
8. Output the resulting string.

### Why it works

Every edge in the graph represents a mandatory ordering constraint. Kahn's algorithm produces an ordering in which every directed edge goes from an earlier letter to a later letter.

When we output all copies of a letter together according to this topological order, every occurrence of the source letter appears before every occurrence of the destination letter for every edge. Since topological order satisfies all edges, it also satisfies every ordering rule.

If a cycle exists, some set of letters must each come before another letter in the same cycle. No linear arrangement can satisfy that requirement, so `IMPOSSIBLE` is the correct answer.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

n = int(input())

adj = [[] for _ in range(26)]
indeg = [0] * 26
seen = set()

for _ in range(n):
    a, op, b = input().split()

    if op == "<":
        u = ord(a) - ord('a')
        v = ord(b) - ord('a')
    else:
        u = ord(b) - ord('a')
        v = ord(a) - ord('a')

    if (u, v) not in seen:
        seen.add((u, v))
        adj[u].append(v)
        indeg[v] += 1

s = input().strip()

q = deque(i for i in range(26) if indeg[i] == 0)

topo = []

while q:
    u = q.popleft()
    topo.append(u)

    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

if len(topo) != 26:
    print("IMPOSSIBLE")
    sys.exit()

cnt = [0] * 26
for ch in s:
    cnt[ord(ch) - ord('a')] += 1

ans = []

for x in topo:
    ans.append(chr(x + ord('a')) * cnt[x])

print("".join(ans))
```

The graph construction converts every comparison into a directed edge whose direction matches the required order.

The `seen` set prevents duplicate edges from artificially increasing indegrees. Even if the input guarantees distinct rules, this makes the implementation robust.

Kahn's algorithm produces a valid topological ordering whenever one exists. The cycle check is performed by verifying that all 26 letters were processed.

The final construction step uses frequencies rather than sorting the entire string. This is important because the word may contain up to 100,000 characters. Appending `count(letter)` copies of each character directly is linear in the word length.

## Worked Examples

### Example 1

Input:

```
3
m > i
n < i
i > o
minion
```

The rules become:

- `i < m`
- `n < i`
- `o < i`

Relevant frequencies:

| Letter | Count |
| --- | --- |
| i | 2 |
| m | 1 |
| n | 2 |
| o | 1 |

One valid topological order begins with:

| Step | Chosen Letter | Partial Order |
| --- | --- | --- |
| 1 | n | n |
| 2 | o | n o |
| 3 | i | n o i |
| 4 | m | n o i m |

Constructing the word from frequencies gives:

```
noniim
```

This satisfies `n < i`, `o < i`, and `i < m`.

### Example 2

Input:

```
1
b < n
banana
```

Frequencies:

| Letter | Count |
| --- | --- |
| a | 3 |
| b | 1 |
| n | 2 |

One valid topological order could place:

| Step | Letter |
| --- | --- |
| 1 | a |
| 2 | b |
| 3 | n |

Result:

```
aaabnn
```

The only required condition is that all `b` characters come before all `n` characters, which is satisfied.

This example demonstrates that unrelated letters may appear anywhere relative to each other.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + \|s\|) | Building the graph from rules plus counting and outputting the word |
| Space | O(n + 26) | Graph edges and frequency arrays |

Since the graph contains only 26 vertices, topological sorting is effectively constant time. The running time is dominated by processing the input rules and the characters of the word, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())

    adj = [[] for _ in range(26)]
    indeg = [0] * 26
    seen = set()

    for _ in range(n):
        a, op, b = input().split()

        if op == "<":
            u = ord(a) - 97
            v = ord(b) - 97
        else:
            u = ord(b) - 97
            v = ord(a) - 97

        if (u, v) not in seen:
            seen.add((u, v))
            adj[u].append(v)
            indeg[v] += 1

    s = input().strip()

    q = deque(i for i in range(26) if indeg[i] == 0)
    topo = []

    while q:
        u = q.popleft()
        topo.append(u)

        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(topo) != 26:
        return "IMPOSSIBLE\n"

    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - 97] += 1

    ans = []
    for x in topo:
        ans.append(chr(x + 97) * cnt[x])

    return "".join(ans) + "\n"

# custom cases

out = run("""0
a
""")
assert sorted(out.strip()) == ['a']

assert run("""3
a < b
b < c
c < a
abc
""") == "IMPOSSIBLE\n"

out = run("""1
b < n
banana
""")
assert out.strip().count('a') == 3
assert out.strip().index('b') < out.strip().rindex('n')

out = run("""2
x < y
y < z
banana
""")
assert sorted(out.strip()) == sorted("banana")

out = run("""1
a > b
abba
""")
s = out.strip()
assert s.rfind('b') < s.find('a')
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single-letter word | Any valid one-letter answer | Minimum size |
| Cycle `a<b<b<c<c<a` | `IMPOSSIBLE` | Cycle detection |
| `b<n` with `banana` | Any valid arrangement | Partial-order handling |
| Constraints on absent letters | Valid rearrangement | Missing letters in word |
| `a>b` with `abba` | All `b` before all `a` | Correct edge direction |

## Edge Cases

Consider the cyclic input:

```
3
a < b
b < c
c < a
abc
```

The graph contains edges `a → b`, `b → c`, and `c → a`. Every vertex has positive indegree. Kahn's algorithm cannot process all 26 letters, so the topological order is incomplete. The algorithm outputs:

```
IMPOSSIBLE
```

which is correct because no valid ordering exists.

Consider an input with unrelated letters:

```
1
b < n
banana
```

The graph contains only one edge. The topological sort may place `a` anywhere relative to `b` and `n`. The produced string could be `aaabnn`, `baaann`, or many others. Every valid answer keeps all `b` characters before all `n` characters.

Consider constraints involving absent letters:

```
2
x < y
y < z
banana
```

The topological order still includes `x`, `y`, and `z`, but their frequencies are zero. During construction, zero copies are appended for those letters. The algorithm outputs a rearrangement of `banana` and correctly respects all constraints even though those letters never appear in the word.
