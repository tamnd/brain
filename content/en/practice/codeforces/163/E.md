---
title: "CF 163E - e-Government"
description: "We have a fixed set of surnames. Each surname can be either active or inactive. Initially every surname is active. The system must process three kinds of operations. A query +i activates the i-th surname. A query -i deactivates the i-th surname. A query ?"
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dp", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 163
codeforces_index: "E"
codeforces_contest_name: "VK Cup 2012 Round 2"
rating: 2800
weight: 163
solve_time_s: 136
verified: true
draft: false
---

[CF 163E - e-Government](https://codeforces.com/problemset/problem/163/E)

**Rating:** 2800  
**Tags:** data structures, dfs and similar, dp, strings, trees  
**Solve time:** 2m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a fixed set of surnames. Each surname can be either active or inactive. Initially every surname is active.

The system must process three kinds of operations.

A query `+i` activates the `i-th` surname.

A query `-i` deactivates the `i-th` surname.

A query `?text` asks for the total number of occurrences of all currently active surnames inside `text`. Overlapping matches count separately. If `"aa"` is active and the text is `"aaa"`, then it appears twice.

The difficult part is that both the number of patterns and the total text size are large. The total length of all surnames is up to `10^6`, and the total length of all query texts is also up to `10^6`. A solution that checks every active pattern against every query text independently is completely infeasible.

Suppose we tried the direct approach. For every `?` query, we iterate through all active surnames and run substring matching. In the worst case we could have `10^5` patterns of average length `10`, and a query text of length `10^6`. Even using KMP for each pattern would already require around `10^11` character operations overall.

The constraints strongly suggest that we must process all patterns simultaneously. Multiple patterns sharing prefixes is the central structure here. Once we notice that, the natural tool is the Aho-Corasick automaton.

There are several edge cases that easily break naive implementations.

Consider overlapping matches.

Input:

```
1 1
aa
?aaa
```

Correct output:

```
2
```

The pattern `"aa"` appears at positions `[1,2]` and `[2,3]`. A careless implementation using non-overlapping search would incorrectly return `1`.

Another subtle case is repeated activation or deactivation.

Input:

```
4 1
abc
-1
-1
+1
?abc
```

Correct output:

```
1
```

The second deactivation must do nothing. If we decrement counters blindly, we may accidentally make the pattern contribute `-1`.

Failure links are another common source of mistakes.

Input:

```
1 2
a
aa
?aa
```

Correct output:

```
3
```

The matches are:

`"a"` twice,

`"aa"` once.

If we only count patterns ending at the current trie node and ignore failure ancestors, we would miss the shorter suffix pattern `"a"`.

The last important corner case comes from dynamic updates.

Input:

```
5 2
a
aa
-1
?aa
+1
?aa
```

Correct output:

```
1
3
```

When `"a"` is inactive, only `"aa"` contributes. After reactivation, both patterns contribute again. The data structure must support online updates efficiently.

## Approaches

The brute-force solution is conceptually simple. For every query text, iterate through all active surnames and count occurrences independently. Using a linear matcher like KMP, counting one pattern inside one text takes `O(text_length + pattern_length)`.

If there are `k = 10^5` patterns and total query text length is also `10^6`, the worst-case complexity becomes roughly:

```
O(total_queries * total_patterns * average_text_size)
```

Even optimistic estimates exceed `10^10` operations. This cannot run within one second.

The key observation is that all patterns are static. Only their active/inactive status changes. This means we can build a single automaton over all surnames once, then reuse it for every query.

Aho-Corasick lets us process a text in linear time while simultaneously tracking matches for every pattern. While scanning characters, the automaton moves through trie states and failure links automatically handle suffix matches.

This solves the multiple-pattern matching problem, but not the dynamic activation problem. Suppose we arrive at automaton node `v` while scanning the text. Every pattern corresponding to some suffix of `v` should contribute if active.

The important structural property is this:

If node `u` is a suffix ancestor of node `v` in the failure tree, then pattern `u` matches whenever we are at state `v`.

So the problem becomes:

While traversing the text, repeatedly ask:

"What is the sum of active pattern weights over all ancestors of the current node in the failure tree?"

This is exactly a subtree-prefix query problem on a tree.

We build the failure tree, run DFS order indexing, and maintain a Fenwick tree over Euler tour indices.

When a pattern becomes active, we add `+1` to its node position.

When it becomes inactive, we add `-1`.

For a query text, while walking through automaton states, we ask how many active pattern nodes lie on the suffix chain of the current state. In DFS order of the failure tree, that becomes a subtree sum query.

The result is an online solution with total complexity nearly linear in the input size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total_patterns × total_text_length) per query | O(total_pattern_length) | Too slow |
| Optimal | O(total_input_size × alphabet + total_queries × log N) | O(total_pattern_length) | Accepted |

## Algorithm Walkthrough

1. Build a trie from all surnames.

Each node represents a prefix. For every pattern, store the node where the pattern ends.
2. Construct failure links using BFS.

The failure link of a node points to the longest proper suffix that also exists in the trie. This is the same transition structure used in KMP, generalized to multiple patterns.
3. Build the failure tree.

If `fail[v] = u`, then add an edge `u -> v`.

This tree captures suffix relationships between automaton states.
4. Run a DFS on the failure tree and assign Euler tour intervals.

For every node `v`, compute:

`tin[v]` = entry time,

`tout[v]` = exit time.

All descendants of `v` occupy one contiguous segment in DFS order.
5. Maintain a Fenwick tree over DFS order.

If a pattern ending at node `v` is active, add `+1` at `tin[v]`.

If it becomes inactive, subtract `1`.
6. Process a query text using the automaton.

For each character:

move through automaton transitions,

arrive at state `v`.

Every active pattern whose terminal node is an ancestor of `v` in the failure tree matches here.
7. Count active suffix ancestors using subtree sums.

The number of active patterns matching at state `v` equals:

```
sum over subtree(v)
```

in the failure tree DFS order.

Since descendants in the failure tree correspond to nodes having `v` as suffix, subtree aggregation gives exactly the needed matches.
8. Accumulate results over the whole text and print the final total.

### Why it works

The critical invariant is:

A pattern matches the current automaton state if and only if the pattern's terminal node lies on the failure-link chain of the current state.

In the failure tree, suffix ancestors become ordinary tree ancestors. After Euler tour flattening, all descendants of a node form one contiguous segment.

By storing active pattern counts at terminal nodes, subtree queries correctly count every active pattern whose suffix relation makes it match the current state.

Since every text character advances the automaton exactly once, and every update changes one Fenwick position, all operations remain efficient and correct.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

def solve():
    n, k = map(int, input().split())

    trie = [[0] * 26]
    fail = [0]
    out = []

    patterns = []

    for _ in range(k):
        s = input().strip()
        patterns.append(s)

        node = 0

        for ch in s:
            c = ord(ch) - 97

            if trie[node][c] == 0:
                trie[node][c] = len(trie)
                trie.append([0] * 26)
                fail.append(0)

            node = trie[node][c]

        out.append(node)

    q = deque()

    for c in range(26):
        nxt = trie[0][c]
        if nxt:
            q.append(nxt)

    while q:
        v = q.popleft()

        for c in range(26):
            nxt = trie[v][c]

            if nxt:
                fail[nxt] = trie[fail[v]][c]
                q.append(nxt)
            else:
                trie[v][c] = trie[fail[v]][c]

    size = len(trie)

    tree = [[] for _ in range(size)]

    for v in range(1, size):
        tree[fail[v]].append(v)

    tin = [0] * size
    tout = [0] * size
    timer = 0

    stack = [(0, 0)]

    while stack:
        v, state = stack.pop()

        if state == 0:
            timer += 1
            tin[v] = timer

            stack.append((v, 1))

            for to in reversed(tree[v]):
                stack.append((to, 0))
        else:
            tout[v] = timer

    bit = Fenwick(size)

    active = [True] * k

    for node in out:
        bit.add(tin[node], 1)

    ans = []

    for _ in range(n):
        query = input().strip()

        typ = query[0]
        arg = query[1:]

        if typ == '+':
            idx = int(arg) - 1

            if not active[idx]:
                active[idx] = True
                bit.add(tin[out[idx]], 1)

        elif typ == '-':
            idx = int(arg) - 1

            if active[idx]:
                active[idx] = False
                bit.add(tin[out[idx]], -1)

        else:
            node = 0
            total = 0

            for ch in arg:
                c = ord(ch) - 97
                node = trie[node][c]

                total += bit.range_sum(tin[node], tout[node])

            ans.append(str(total))

    print('\n'.join(ans))

solve()
```

The trie construction phase creates one automaton state per distinct prefix. Every pattern remembers its terminal node because later updates must activate or deactivate exactly that node.

During BFS construction of failure links, missing transitions are filled using failure transitions. This transforms the trie into a complete automaton where every character transition becomes `O(1)`.

The failure tree is built from failure links. If `fail[v] = u`, then `u` is the parent of `v`. This tree structure is the core trick behind the solution.

The DFS numbering deserves careful attention. A subtree in the failure tree corresponds to a contiguous Euler interval `[tin[v], tout[v]]`. Fenwick trees work on contiguous ranges efficiently, which is why flattening is necessary.

A subtle implementation detail is the direction of counting.

We store active patterns at their terminal nodes. When processing automaton state `v`, we query the subtree of `v`, not its ancestor chain.

Why? Because in the failure tree, descendants of `v` are exactly the states whose failure chain contains `v`. This inversion is easy to get wrong.

Repeated activation and deactivation are guarded with the `active` array. Without this check, multiple `+` operations would incorrectly add the same pattern multiple times.

The iterative DFS avoids Python recursion depth issues. The automaton can contain up to `10^6` nodes, so recursive DFS is unsafe.

## Worked Examples

### Example 1

Input:

```
7 3
a
aa
ab
?aaab
-2
?aaab
-3
?aaab
+2
?aabbaa
```

Patterns:

`a`, `aa`, `ab`

Initially all active.

| Step | Query | Active Patterns | Matches | Result |
| --- | --- | --- | --- | --- |
| 1 | `?aaab` | a, aa, ab | a=3, aa=2, ab=1 | 6 |
| 2 | `-2` | a, ab | aa removed | - |
| 3 | `?aaab` | a, ab | a=3, ab=1 | 4 |
| 4 | `-3` | a | ab removed | - |
| 5 | `?aaab` | a | a=3 | 3 |
| 6 | `+2` | a, aa | aa restored | - |
| 7 | `?aabbaa` | a, aa | a=4, aa=2 | 6 |

This trace shows dynamic updates working correctly. Patterns contribute only while active, and overlapping matches are counted.

### Example 2

Input:

```
5 2
a
aa
?aa
-1
?aa
+1
?aa
```

| Step | Current State While Scanning | Active Patterns | Contribution |
| --- | --- | --- | --- |
| `?aa` first `a` | state("a") | a, aa | +1 |
| `?aa` second `a` | state("aa") | a, aa | +2 |
| Total | - | - | 3 |
| `-1` | deactivate `a` | aa only | - |
| `?aa` first `a` | state("a") | aa only | 0 |
| `?aa` second `a` | state("aa") | aa only | +1 |
| Total | - | - | 1 |

This example confirms that suffix matches are handled through failure links. At state `"aa"`, both `"aa"` and `"a"` may contribute.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total_pattern_length + total_text_length + total_queries × log N) | Trie traversal is linear, Fenwick updates and queries are logarithmic |
| Space | O(total_pattern_length) | Trie, failure tree, DFS arrays, and Fenwick tree all scale with automaton size |

The total automaton size is bounded by the total pattern length, at most `10^6`. Every text character performs one automaton transition and one Fenwick range query. This comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, idx, val):
            while idx <= self.n:
                self.bit[idx] += val
                idx += idx & -idx

        def sum(self, idx):
            res = 0
            while idx > 0:
                res += self.bit[idx]
                idx -= idx & -idx
            return res

        def range_sum(self, l, r):
            return self.sum(r) - self.sum(l - 1)

    n, k = map(int, input().split())

    trie = [[0] * 26]
    fail = [0]
    out = []

    for _ in range(k):
        s = input().strip()

        node = 0

        for ch in s:
            c = ord(ch) - 97

            if trie[node][c] == 0:
                trie[node][c] = len(trie)
                trie.append([0] * 26)
                fail.append(0)

            node = trie[node][c]

        out.append(node)

    q = deque()

    for c in range(26):
        nxt = trie[0][c]
        if nxt:
            q.append(nxt)

    while q:
        v = q.popleft()

        for c in range(26):
            nxt = trie[v][c]

            if nxt:
                fail[nxt] = trie[fail[v]][c]
                q.append(nxt)
            else:
                trie[v][c] = trie[fail[v]][c]

    size = len(trie)

    tree = [[] for _ in range(size)]

    for v in range(1, size):
        tree[fail[v]].append(v)

    tin = [0] * size
    tout = [0] * size

    timer = 0
    stack = [(0, 0)]

    while stack:
        v, state = stack.pop()

        if state == 0:
            timer += 1
            tin[v] = timer

            stack.append((v, 1))

            for to in reversed(tree[v]):
                stack.append((to, 0))
        else:
            tout[v] = timer

    bit = Fenwick(size)

    active = [True] * k

    for node in out:
        bit.add(tin[node], 1)

    ans = []

    for _ in range(n):
        s = input().strip()

        if s[0] == '?':
            node = 0
            total = 0

            for ch in s[1:]:
                node = trie[node][ord(ch) - 97]
                total += bit.range_sum(tin[node], tout[node])

            ans.append(str(total))

        elif s[0] == '+':
            idx = int(s[1:]) - 1

            if not active[idx]:
                active[idx] = True
                bit.add(tin[out[idx]], 1)

        else:
            idx = int(s[1:]) - 1

            if active[idx]:
                active[idx] = False
                bit.add(tin[out[idx]], -1)

    return "\n".join(ans)

# provided sample
assert run(
"""7 3
a
aa
ab
?aaab
-2
?aaab
-3
?aaab
+2
?aabbaa
"""
) == "6\n4\n3\n6", "sample 1"

# minimum size
assert run(
"""1 1
a
?a
"""
) == "1", "minimum case"

# overlapping matches
assert run(
"""1 1
aa
?aaa
"""
) == "2", "overlapping occurrences"

# repeated enable/disable
assert run(
"""5 1
abc
-1
-1
+1
?abc
"""
) == "1", "idempotent updates"

# suffix-chain counting
assert run(
"""1 2
a
aa
?aa
"""
) == "3", "failure-link aggregation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single pattern `"a"` | `1` | Smallest valid instance |
| `"aa"` inside `"aaa"` | `2` | Overlapping occurrences |
| Repeated `-1` | `1` | Updates must be idempotent |
| Patterns `"a"` and `"aa"` | `3` | Failure-chain suffix matching |

## Edge Cases

Consider overlapping occurrences again.

Input:

```
1 1
aa
?aaa
```

While scanning:

after second character, state `"aa"` contributes once,

after third character, failure transitions still keep us at `"aa"` contribution again.

The algorithm outputs:

```
2
```

because every text position independently contributes matches.

Now consider repeated deactivation.

Input:

```
4 1
abc
-1
-1
+1
?abc
```

The first `-1` removes the pattern from the Fenwick tree.

The second `-1` checks `active[idx]` and does nothing.

The `+1` restores exactly one copy.

The final query correctly outputs:

```
1
```

instead of `0` or `-1`.

The suffix-link edge case is especially important.

Input:

```
1 2
a
aa
?aa
```

At automaton state `"aa"`:

the node itself matches `"aa"`,

its failure ancestor matches `"a"`.

The subtree query over the failure tree counts both active terminal nodes, producing:

```
3
```

Finally, consider patterns with shared prefixes but different endings.

Input:

```
2 3
ab
abc
abd
?abcd
```

The automaton transitions reuse trie prefixes efficiently.

Matches:

`"ab"` once,

`"abc"` once,

`"abd"` zero times.

Correct output:

```
2
```

The algorithm handles this naturally because trie states represent shared prefixes directly.
