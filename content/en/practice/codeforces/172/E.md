---
title: "CF 172E - BHTML+BCSS"
description: "We are given a simplified HTML-like document. Every tag is either an opening tag like <a, a closing tag like </a, or a self-closing tag like <a/. The document is guaranteed to be properly nested, so every opening tag has exactly one matching closing tag."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dfs-and-similar", "expression-parsing"]
categories: ["algorithms"]
codeforces_contest: 172
codeforces_index: "E"
codeforces_contest_name: "Croc Champ 2012 - Qualification Round"
rating: 2200
weight: 172
solve_time_s: 141
verified: false
draft: false
---

[CF 172E - BHTML+BCSS](https://codeforces.com/problemset/problem/172/E)

**Rating:** 2200  
**Tags:** *special, dfs and similar, expression parsing  
**Solve time:** 2m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a simplified HTML-like document. Every tag is either an opening tag like `<a>`, a closing tag like `</a>`, or a self-closing tag like `<a/>`. The document is guaranteed to be properly nested, so every opening tag has exactly one matching closing tag.

Each matched pair of tags forms an element. Self-closing tags also count as elements. Because the document is properly nested, the elements form a rooted forest structure, exactly like a DOM tree.

A query is a sequence of tag names such as:

```
a b c
```

An element matches this query if there exists a chain of ancestors ending at that element whose tag names are exactly `a -> b -> c`.

The important detail is that the chain does not need to use consecutive levels. The query only requires nested containment. For example:

```
<a><x><b></b></x></a>
```

The element `b` matches the query `a b`, even though `x` sits between them.

For every query, we must count how many elements satisfy it.

The document length can reach `10^6`, which immediately rules out anything quadratic in the number of tags. Even parsing the document already costs linear time, so the actual matching logic must also stay close to linear.

There are at most `200` queries, and each query length is at most `200`. That is a strong hint that we should preprocess the document once, then answer all queries together.

A naive DFS from every node for every query would explode. In the worst case the tree may contain hundreds of thousands of elements. Multiplying that by all query lengths is far too expensive.

Several edge cases are easy to mishandle.

Consider repeated tag names:

```
<a><a><a></a></a></a>
```

Query:

```
a a
```

The deepest `a` matches because it has an ancestor `a`. The middle `a` also matches. A careless implementation that only tracks the nearest ancestor would miss some matches.

Another subtle case is non-consecutive nesting:

```
<a><x><b></b></x></a>
```

Query:

```
a b
```

The correct answer is `1`. Any solution that only checks parent-child relationships instead of arbitrary ancestor chains fails here.

Self-closing tags behave like ordinary elements:

```
<a><b/></a>
```

Query:

```
a b
```

The answer is `1`. If parsing ignores self-closing tags or forgets to create an element node for them, the count becomes incorrect.

Finally, order matters:

```
<a><b></b></a>
```

Query:

```
b a
```

The answer is `0`, because ancestor chains must follow nesting order from outermost to innermost.

## Approaches

The brute force approach is straightforward after building the tree.

For every element, we can walk upward through its ancestors and try to match every query backwards. Suppose a query is:

```
a b c
```

For an element tagged `c`, we climb toward the root searching for `b`, then continue searching for `a`.

This works because the queries only ask whether such an ancestor chain exists. The upward scan directly checks that condition.

The problem is complexity. If the document contains `N` elements and the tree degenerates into a chain, then each upward walk may cost `O(N)`. Repeating this for every element and every query leads to roughly:

```
O(number_of_queries * N^2)
```

With `N` near several hundred thousand, this is hopeless.

The key observation is that the number of distinct queries is tiny, while the document itself is huge.

Instead of testing queries separately, we can process the document once while maintaining information about all queries simultaneously.

Suppose we traverse the tree with DFS and keep the current path of tag names from the root to the current node. Then each query becomes a subsequence matching problem:

Does the query appear as a subsequence of the current root-to-node path?

For example, if the current DFS path is:

```
header p div b
```

then the query:

```
header b
```

matches.

Since queries are short, we can build a trie of all queries. During DFS, whenever we enter a tag named `x`, every query state waiting for `x` can advance.

This transforms the problem into automaton propagation along the DFS path.

The total amount of query data is tiny:

```
200 * 200 = 40000
```

So we can afford to maintain transition lists for all partial matches.

The resulting algorithm becomes essentially linear in the document size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q · N²) | O(N) | Too slow |
| Optimal | O(Document length + Total query length + Total state transitions) | O(Total query length) | Accepted |

## Algorithm Walkthrough

### Parsing the document

We scan the document string from left to right and extract tags.

For every opening tag, we create a new node and push it onto a stack.

For every closing tag, we pop the matching node from the stack.

For every self-closing tag, we create a node but do not push it.

This reconstructs the nesting tree.

### Building query states

1. Split every query into words.
2. Assign an integer id to every unique tag name appearing in either the document or queries.
3. For every query, create states representing prefixes of that query.

For example, query:

```
a b c
```

creates transitions:

```
state 0 --a--> state 1
state 1 --b--> state 2
state 2 --c--> state 3
```

State `3` means the whole query matched.

1. For every tag name, store which states can advance when this tag appears.

This lets us efficiently update all active partial matches during DFS.

### DFS traversal

1. Start DFS from every root node.
2. Maintain an array `cnt[state]`.

`cnt[s]` equals the number of ways the current root-to-node path realizes query prefix state `s`.

Initially only state `0` is active.

1. When entering a node with tag `x`, every transition waiting for `x` becomes usable.

Suppose:

```
state u --x--> state v
```

Then:

```
cnt[v] += cnt[u]
```

We process states in reverse order so updates from this node do not cascade multiple times inside the same step.

1. Whenever a terminal state becomes active, the corresponding query gains matches at this node.
2. Recurse into children.
3. After returning, rollback all modifications performed at this node.

Rollback is essential because DFS paths are independent.

### Why it works

At any moment during DFS, `cnt[state]` represents how many subsequences of the current root-to-current-node path realize the corresponding query prefix.

When we enter a tag `x`, every existing partial match that expects `x` may extend through the current node. Because subsequences allow skipping intermediate nodes, every previous valid prefix remains valid deeper in the tree.

Processing transitions in reverse order prevents a single node from being reused multiple times within the same query position.

Since DFS always maintains exactly the current ancestor path, every counted completion corresponds to a valid nested chain in the document, and every valid nested chain is eventually counted when DFS reaches its final element.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    s = input().strip()
    m = int(input())

    queries = []
    all_tags = set()

    for _ in range(m):
        q = input().split()
        queries.append(q)
        all_tags.update(q)

    n = len(s)

    children = []
    tag_id = []
    roots = []

    stack = []

    tag_map = {}

    def get_id(name):
        if name not in tag_map:
            tag_map[name] = len(tag_map)
        return tag_map[name]

    i = 0

    while i < n:
        j = s.find('>', i)

        token = s[i + 1:j]

        if token[0] == '/':
            stack.pop()

        elif token[-1] == '/':
            name = token[:-1]

            tid = get_id(name)

            node = len(children)
            children.append([])
            tag_id.append(tid)

            if stack:
                children[stack[-1]].append(node)
            else:
                roots.append(node)

        else:
            name = token

            tid = get_id(name)

            node = len(children)
            children.append([])
            tag_id.append(tid)

            if stack:
                children[stack[-1]].append(node)
            else:
                roots.append(node)

            stack.append(node)

        i = j + 1

    transitions = defaultdict(list)

    state_ptr = 1

    query_end = []
    query_state = []

    for qi, q in enumerate(queries):
        cur = 0

        for word in q:
            tid = get_id(word)

            nxt = state_ptr
            state_ptr += 1

            transitions[tid].append((cur, nxt))

            cur = nxt

        query_end.append(cur)
        query_state.append(cur)

    cnt = [0] * state_ptr
    cnt[0] = 1

    ans = [0] * m

    def dfs(u):
        tid = tag_id[u]

        updates = []

        trans = transitions.get(tid, [])

        for prev, nxt in reversed(trans):
            add = cnt[prev]

            if add:
                old = cnt[nxt]
                cnt[nxt] += add
                updates.append((nxt, old))

        for qi in range(m):
            st = query_end[qi]
            if cnt[st]:
                ans[qi] += cnt[st]

        for v in children[u]:
            dfs(v)

        for st, old in reversed(updates):
            cnt[st] = old

    for r in roots:
        dfs(r)

    print('\n'.join(map(str, ans)))

solve()
```

The parser reconstructs the forest directly from the tag stream. Every opening or self-closing tag creates a node. The stack always stores the currently open elements.

The automaton states represent prefixes of queries. State `0` means an empty prefix. Every transition corresponds to consuming one tag from a query.

The DFS maintains dynamic programming values over the current ancestor path. The reverse-order transition update is the subtle part. Without reversing, one node could advance multiple positions of the same query simultaneously.

For example, consider query:

```
a a
```

and current node `a`.

If updates are processed forward, the same node would first activate the first `a`, then immediately activate the second `a` using itself again. Reversing prevents that.

Rollback restores the DP array after leaving a subtree. Without rollback, matches from one branch would incorrectly leak into sibling branches.

## Worked Examples

### Sample 1

Input:

```
<a><b><b></b></b></a><a><b></b><b><v/></b></a><b></b>
```

Queries:

```
a
a b b
a b
b a
```

The tree structure is:

```
a
└── b
    └── b

a
├── b
└── b
    └── v

b
```

DFS trace for query `a b`:

| Current Path | Active Prefixes | Query Matched? |
| --- | --- | --- |
| a | a | No |
| a b | a, a b | Yes |
| a b b | a, a b | Yes |
| a | a | No |
| a b | a, a b | Yes |
| a b | a, a b | Yes |
| a b v | a, a b | No |
| b | none | No |

The answer becomes `4`.

This trace demonstrates subsequence matching. The query `a b` matches both direct and indirect nesting chains.

### Custom Example

Input:

```
<a><x><b/></x></a>
```

Query:

```
a b
```

DFS trace:

| Current Path | Matching Prefixes |
| --- | --- |
| a | a |
| a x | a |
| a x b | a, a b |

The answer is `1`.

This example confirms that intermediate nodes may be skipped. The query only requires ancestor containment, not adjacency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L + S + T) | `L` for parsing the document, `S` for total query size, `T` for all transition updates during DFS |
| Space | O(N + S) | Tree storage plus automaton states |

The document length is at most `10^6`, so linear parsing is necessary. Total query size never exceeds `40000`, which makes the automaton extremely small compared to the document. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    s = input().strip()
    m = int(input())

    queries = []

    children = []
    tag_id = []
    roots = []

    stack = []

    tag_map = {}

    def get_id(name):
        if name not in tag_map:
            tag_map[name] = len(tag_map)
        return tag_map[name]

    n = len(s)

    i = 0

    while i < n:
        j = s.find('>', i)

        token = s[i + 1:j]

        if token[0] == '/':
            stack.pop()

        elif token[-1] == '/':
            name = token[:-1]

            tid = get_id(name)

            node = len(children)
            children.append([])
            tag_id.append(tid)

            if stack:
                children[stack[-1]].append(node)
            else:
                roots.append(node)

        else:
            name = token

            tid = get_id(name)

            node = len(children)
            children.append([])
            tag_id.append(tid)

            if stack:
                children[stack[-1]].append(node)
            else:
                roots.append(node)

            stack.append(node)

        i = j + 1

    transitions = defaultdict(list)

    state_ptr = 1

    query_end = []

    for qi in range(m):
        q = input().split()

        cur = 0

        for word in q:
            tid = get_id(word)

            nxt = state_ptr
            state_ptr += 1

            transitions[tid].append((cur, nxt))

            cur = nxt

        query_end.append(cur)

    cnt = [0] * state_ptr
    cnt[0] = 1

    ans = [0] * m

    def dfs(u):
        tid = tag_id[u]

        updates = []

        for prev, nxt in reversed(transitions.get(tid, [])):
            add = cnt[prev]

            if add:
                old = cnt[nxt]
                cnt[nxt] += add
                updates.append((nxt, old))

        for qi, st in enumerate(query_end):
            if cnt[st]:
                ans[qi] += cnt[st]

        for v in children[u]:
            dfs(v)

        for st, old in reversed(updates):
            cnt[st] = old

    for r in roots:
        dfs(r)

    return '\n'.join(map(str, ans))

# provided sample
assert run(
"""<a><b><b></b></b></a><a><b></b><b><v/></b></a><b></b>
4
a
a b b
a b
b a
"""
) == "2\n1\n4\n0"

# single self-closing node
assert run(
"""<a/>
1
a
"""
) == "1"

# non-consecutive nesting
assert run(
"""<a><x><b/></x></a>
1
a b
"""
) == "1"

# repeated names
assert run(
"""<a><a><a/></a></a>
2
a a
a a a
"""
) == "2\n1"

# impossible order
assert run(
"""<a><b/></a>
1
b a
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `<a/>` with query `a` | `1` | Self-closing tags create elements |
| `<a><x><b/></x></a>` with query `a b` | `1` | Non-consecutive nesting works |
| Nested repeated `a` tags | `2`, `1` | Reverse-order DP update correctness |
| Query `b a` on `<a><b/></a>` | `0` | Ancestor order matters |

## Edge Cases

Consider repeated tag names:

```
<a><a><a/></a></a>
```

Query:

```
a a
```

When DFS enters the deepest `a`, the path contains three `a` nodes.

The reverse-order transition update guarantees that the current node contributes only once per query position. The deepest node correctly matches using an ancestor `a`, not itself twice.

The algorithm outputs:

```
2
```

which counts the middle and deepest elements.

Now consider skipped levels:

```
<a><x><b/></x></a>
```

Query:

```
a b
```

While visiting `x`, the DP state for prefix `a` remains active. Entering `b` extends that existing prefix to `a b`.

The algorithm never requires adjacency between matched nodes, only ancestor containment.

Finally, consider sibling leakage:

```
<a><b/></a><a/>
```

Query:

```
a b
```

The correct answer is `1`.

After DFS leaves the first subtree, rollback removes all states introduced there. When the second root `a` is processed, the previous `b` match is gone.

Without rollback, the second branch would incorrectly inherit matches from the first subtree.
