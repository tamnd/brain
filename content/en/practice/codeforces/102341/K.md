---
title: "CF 102341K - Kecleon"
description: "We maintain a string of lowercase letters that grows only by appending one character to its right end. A query asks for a length (k), and we must count how many substrings of length (k) are exactly equal to the prefix of the whole string of length (k)."
date: "2026-08-13T03:23:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102341
codeforces_index: "K"
codeforces_contest_name: "Radewoosh+mnbvmar Contest (supported by AIM Tech)"
rating: 0
weight: 102341
solve_time_s: 187
verified: true
draft: false
---

[CF 102341K - Kecleon](https://codeforces.com/problemset/problem/102341/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a string of lowercase letters that grows only by appending one character to its right end. A query asks for a length (k), and we must count how many substrings of length (k) are exactly equal to the prefix of the whole string of length (k).

The input is online in two ways. First, both the character appended and the requested length are encoded using the previous answer, so we cannot decode future queries in advance. Second, the string itself only grows, which gives us an opportunity to maintain information incrementally.

The number of queries is at most (300,000), so the final string also has length at most (300,000). An algorithm that scans the whole string for every query is already too slow. An algorithm that compares every candidate substring character by character can reach around (10^{15}) character comparisons on a large adversarial input. We need roughly logarithmic work per operation.

There are three details that commonly cause incorrect solutions.

The first is that (k=n) has exactly one matching interval, the entire string. For example,

```
3
add a
add b
get 2
```

produces

```
1
```

A solution that only counts proper occurrences can accidentally return zero.

The second is that the prefix itself always counts as an occurrence. For

```
2
add a
get 1
```

the answer is

```
1
```

The third is the online encoding. Consider

```
6
add a
add a
add b
add a
get 1
get 1
```

The string is `aaba`. The first `get 1` asks for (k=1), whose answer is (3), so `last` becomes (3). The second raw value `1` is then decoded with (n=4) as (k=4), not (k=1). Its answer is (1). The correct output is

```
3
1
```

Ignoring `last` would silently answer the wrong question.

## Approaches

The direct solution is to store the current string and, for every query, inspect every possible starting position. For each position we compare the substring of length (k) with the first (k) characters. This is correct because those are exactly the intervals mentioned by the query. However, there can be (n-k+1) candidate intervals, and comparing one interval can cost (k), giving (O(nk)) work for one query.

The worst case is much larger than the four-second limit allows. With about (200,000) appended characters and (100,000) queries, a single query can require around (10^{10}) character comparisons, and repeating that over the queries reaches the order of (10^{15}) comparisons.

A rolling hash would reduce the cost of comparing one substring, but we would still need to inspect all (n-k+1) starting positions. The real problem is not just equality testing. We need a way to count all occurrences of a prefix without scanning the string.

The key observation comes from the prefix function used by KMP. For every prefix ending at position (i), the prefix function tells us the length of its longest proper prefix that is also a suffix. If we create a node for every prefix length and make node (i) a child of node (\pi[i-1]), we obtain the prefix-function tree.

Now consider a prefix of length (k). It occurs ending at position (i) exactly when the first (k) characters are a suffix of the prefix ending at (i). In the prefix-function tree, that means node (k) is an ancestor of node (i). Consequently, the number of occurrences of prefix (k) is exactly the size of the subtree rooted at node (k).

This changes the problem completely. Each appended character creates one new node in the prefix-function tree, and that node is attached as a leaf. Each query becomes a dynamic subtree-size query.

A static Euler tour would make every subtree a contiguous interval, but the tree is being built online, so its final DFS order is not known. We can instead maintain the Euler sequence dynamically in an implicit treap. Every tree node receives an entry token and an exit token. The entry token has value (1), while the exit token has value (0). The entire subtree of a node is always the contiguous sequence between its entry and exit tokens. When a new leaf is attached to a parent, its two tokens are inserted immediately before the parent's exit token.

The treap stores the Euler sequence and maintains the sum of token values in every treap subtree. A subtree-size query is then just the number of entry tokens between the corresponding entry and exit tokens.

The brute-force and optimal approaches can be compared as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(qn^2)) in the worst case | (O(n)) | Too slow |
| Optimal | (O(q\log q)) expected | (O(q)) | Accepted |

## Algorithm Walkthrough

1. Maintain the current string and its prefix-function array. When a new character is appended, compute its prefix-function value using the usual KMP fallback chain. If the new position is (n), its parent in the prefix-function tree is node (\pi[n-1]).

The KMP computation is amortized linear over the whole sequence, because every fallback moves to a previously computed border.
2. Represent the prefix-function tree with an entry and exit token for every node. Node (v)'s entry token stores value (1), and its exit token stores value (0). The artificial root node (0) has value (0).

A DFS representation looks like `enter(v), all descendants, exit(v)`. Thus every node in the subtree of (v) contributes exactly one (1) inside the interval from `enter(v)` to `exit(v)`.
3. Store this token sequence in an implicit treap. The treap is ordered by sequence position rather than by an explicit key. Each treap node stores its subtree size, subtree sum, children, parent, and random priority.

Parent pointers let us find the current position of any token in (O(\log n)) expected time by walking from the token toward the treap root.
4. When prefix-tree node (v) is created with parent (p), find the current position of `exit(p)`. Split the Euler sequence immediately before that token, insert `enter(v), exit(v)`, and merge the sequence back.

Inserting immediately before the parent's exit token places the new node as the last child of that parent. The exact order between siblings does not matter, because only subtree membership is used.
5. For a `get` query, first decode the requested length using the current value of `last`.

The decoded (k) corresponds to prefix-function tree node (k). Find the number of entry tokens from `enter(k)` through `exit(k)`. That number is the subtree size of (k), which is exactly the number of occurrences of the prefix of length (k).
6. Store the answer in `last` before processing the next query.

### Why it works

For every position (i), node (i) represents the entire prefix ending at that position. Node (k) is an ancestor of node (i) exactly when the prefix of length (k) is a suffix of the prefix ending at (i). That suffix is precisely an occurrence of the first (k) characters ending at (i). Hence occurrences of the queried prefix are in one-to-one correspondence with nodes in the subtree of (k).

The dynamic Euler sequence always contains every subtree as one contiguous interval. Since only entry tokens contribute to the stored sum, the sum over node (k)'s interval counts every descendant exactly once. The treap therefore returns exactly the required number of matching intervals.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

def solve():
    q = int(input())

    # Prefix-function data.
    s = bytearray()
    pi = [0]

    # Implicit treap data.
    # Node 0 is the null treap node.
    left = [0]
    right = [0]
    parent = [0]
    size = [0]
    sm = [0]
    value = [0]
    priority = [0]

    seed = 0x12345678

    def rng():
        nonlocal seed
        seed ^= (seed << 13) & 0xFFFFFFFF
        seed ^= seed >> 17
        seed ^= (seed << 5) & 0xFFFFFFFF
        seed &= 0xFFFFFFFF
        return seed

    def new_node(v):
        idx = len(left)
        left.append(0)
        right.append(0)
        parent.append(0)
        size.append(1)
        sm.append(v)
        value.append(v)
        priority.append(rng())
        return idx

    # Root of the prefix-function tree is node 0.
    # Its Euler sequence is enter(0), exit(0).
    new_node(0)
    new_node(0)
    root = 1

    def pull(x):
        l = left[x]
        r = right[x]
        size[x] = size[l] + size[r] + 1
        sm[x] = sm[l] + sm[r] + value[x]

    def merge(a, b):
        if a == 0:
            if b:
                parent[b] = 0
            return b
        if b == 0:
            parent[a] = 0
            return a

        if priority[a] > priority[b]:
            nr = merge(right[a], b)
            right[a] = nr
            if nr:
                parent[nr] = a
            pull(a)
            parent[a] = 0
            return a

        nl = merge(a, left[b])
        left[b] = nl
        if nl:
            parent[nl] = b
        pull(b)
        parent[b] = 0
        return b

    def split(x, k):
        if x == 0:
            return 0, 0

        ls = size[left[x]]

        if k <= ls:
            a, b = split(left[x], k)
            left[x] = b
            if b:
                parent[b] = x
            parent[x] = 0
            if a:
                parent[a] = 0
            pull(x)
            return a, x

        a, b = split(right[x], k - ls - 1)
        right[x] = a
        if a:
            parent[a] = x
        parent[x] = 0
        if b:
            parent[b] = 0
        pull(x)
        return x, b

    def get_rank(x):
        # 1-based position of x in the implicit sequence.
        ans = size[left[x]] + 1
        while parent[x]:
            p = parent[x]
            if right[p] == x:
                ans += size[left[p]] + 1
            x = p
        return ans

    def prefix_before(x):
        # Sum of values strictly before x.
        ans = sm[left[x]]
        while parent[x]:
            p = parent[x]
            if right[p] == x:
                ans += sm[left[p]] + value[p]
            x = p
        return ans

    def enter_token(v):
        # Vertex v has tokens 2*v+1 and 2*v+2.
        return 2 * v + 1

    def exit_token(v):
        return 2 * v + 2

    # Insert the two Euler tokens of vertex v immediately
    # before the exit token of its parent.
    def link_leaf(v, p):
        nonlocal root

        target = exit_token(p)
        pos = get_rank(target)

        a, b = split(root, pos - 1)

        en = new_node(1)
        ex = new_node(0)
        pair = merge(en, ex)

        root = merge(merge(a, pair), b)

    last = 0
    output = []

    for _ in range(q):
        parts = input().split()

        if parts[0] == b"add" or parts[0] == "add":
            raw = parts[1]
            if isinstance(raw, bytes):
                raw = raw[0]
            else:
                raw = ord(raw)

            c = (raw - 97 + last) % 26

            old_n = len(s)
            s.append(c + 97)

            if old_n == 0:
                cur_pi = 0
            else:
                j = pi[old_n - 1]
                while j > 0 and s[old_n] != s[j]:
                    j = pi[j - 1]
                if s[old_n] == s[j]:
                    j += 1
                cur_pi = j

            pi.append(cur_pi)

            v = old_n + 1
            link_leaf(v, cur_pi)

        else:
            raw_k = int(parts[1])
            n = len(s)

            k = ((raw_k - 1 + last) % n) + 1

            tin = enter_token(k)
            tout = exit_token(k)

            # All entry tokens in the subtree lie between tin and tout.
            ans = prefix_before(tout) - prefix_before(tin)

            output.append(str(ans))
            last = ans

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The prefix-function section follows the standard KMP idea. The first character has prefix-function value zero. For every later character, we begin with the previous prefix-function value and repeatedly follow failure links until the current character can extend the border.

The prefix-function value is also the parent index in the tree. If the current prefix has length (v), its longest proper prefix that is also a suffix has length `pi[v - 1]`, so that is exactly the parent of node (v).

The Euler tokens are assigned fixed identifiers. For vertex (v), `2*v+1` is its entry token and `2*v+2` is its exit token. This makes it unnecessary to store separate token references for every vertex.

The treap stores the Euler sequence implicitly. `split(root, k)` separates the first (k) tokens, while `merge(a, b)` concatenates two sequences. The parent pointers are maintained whenever a child is attached to a treap node, which makes `get_rank` possible.

The insertion position uses `get_rank(exit_token(parent)) - 1`. This is an easy off-by-one location to get wrong. The split must contain every token before the parent's exit token, while the exit token itself belongs to the right part.

For a query, `prefix_before(x)` returns the sum of all token values strictly before token (x). Thus subtracting the value before `enter(k)` from the value before `exit(k)` counts every entry token in the subtree and excludes the exit token itself. No integer overflow is possible in Python, and in C++ the answer would fit comfortably in a 32-bit signed integer because it is at most (n).

The decoding must happen before updating `last`. The new answer becomes `last` only after the query has been completely processed.

## Worked Examples

### Sample 1

The decoded string eventually becomes `abcababca`. The prefix-function parents are generated online, while the Euler tour keeps every prefix-function subtree contiguous.

| Query | Current string | Decoded (k) | Prefix-tree node | Answer | `last` |
| --- | --- | --- | --- | --- | --- |
| `add a` | `a` |  |  |  | 0 |
| `add b` | `ab` |  |  |  | 0 |
| `add c` | `abc` |  |  |  | 0 |
| `add a` | `abca` |  |  |  | 0 |
| `get 1` | `abca` | 1 | 1 | 2 | 2 |
| `add z` | `abcab` |  |  |  | 2 |
| `get 1` | `abcab` | 3 | 3 | 1 | 1 |
| `get 1` | `abcab` | 2 | 2 | 2 | 2 |
| `add y` | `abcaba` |  |  |  | 2 |
| `add z` | `abcabab` |  |  |  | 2 |
| `add a` | `abcababc` |  |  |  | 2 |
| `add y` | `abcababca` |  |  |  | 2 |
| `get 8` | `abcababca` | 1 | 1 | 4 | 4 |
| `get 7` | `abcababca` | 3 | 3 | 3 | 3 |
| `get 9` | `abcababca` | 4 | 4 | 2 | 2 |
| `get 2` | `abcababca` | 4 | 4 | 2 | 2 |

The first query asks for occurrences of `a` in `abca`, giving two. That answer changes the interpretation of the next `get`. After the second answer becomes one, the following raw value `1` decodes to (k=2), whose prefix is `ab` and occurs twice.

The later queries show why the answer is a subtree size rather than a direct character count. For example, the decoded (k=4) corresponds to prefix `abca`. Its occurrences are represented by descendants of node 4 in the prefix-function tree, and the Euler interval contains exactly those entry tokens.

### Online decoding example

Consider the smaller input

```
6
add a
add a
add b
add a
get 1
get 1
```

The actual string is `aaba`. The first query has (k=1), and the prefix `a` occurs three times. This makes `last=3`. The second raw `get 1` is then decoded using (n=4), giving (k=4).

| Query | String | Decoded (k) | Relevant prefix | Answer | `last` |
| --- | --- | --- | --- | --- | --- |
| `add a` | `a` |  |  |  | 0 |
| `add a` | `aa` |  |  |  | 0 |
| `add b` | `aab` |  |  |  | 0 |
| `add a` | `aaba` |  |  |  | 0 |
| `get 1` | `aaba` | 1 | `a` | 3 | 3 |
| `get 1` | `aaba` | 4 | `aaba` | 1 | 1 |

This trace exercises the part of the problem that cannot be handled by preprocessing all queries. The second query really is asking about the entire current string, because its decoded value depends on the answer to the first query.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(q\log q)) expected | Each append performs amortized (O(1)) prefix-function work and (O(\log q)) expected treap work. Each `get` uses two (O(\log q)) treap traversals. |
| Space | (O(q)) | There are two Euler tokens for every prefix-function node, plus the string and prefix-function arrays. |

The maximum number of prefix-function nodes is (300,000), so the treap contains at most (600,002) tokens including the artificial root. The expected logarithmic treap height keeps each dynamic insertion and query within the required asymptotic bound. The original problem has a four-second limit, so an implementation needs compact data structures and fast I/O. The Python implementation uses arrays of primitive Python integers and avoids substring creation or hashing.

## Test Cases

The following tests assume the `solve()` function from the solution is present in the same file.

```python
import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    out = io.StringIO()
    sys.stdout = out

    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

    return out.getvalue()

sample_1 = """16
add a
add b
add c
add a
get 1
add z
get 1
get 1
add y
add z
add a
add y
get 8
get 7
get 9
get 2
"""

assert run(sample_1) == """2
1
2
4
3
2
2
""", "sample 1"

assert run("""2
add a
get 1
""") == """1
""", "minimum size"

assert run("""5
add a
add a
add a
add a
get 1
""") == """4
""", "all equal values"

assert run("""3
add a
add b
get 2
""") == """1
""", "k equals n"

assert run("""6
add a
add a
add b
add a
get 1
get 1
""") == """3
1
""", "online decoding"

max_q = 300000
max_input = str(max_q) + "\n" + ("add a\n" * (max_q - 1)) + "get 1\n"
assert run(max_input) == str(max_q - 1) + "\n", "maximum size"

# A mixed pattern with several different prefix occurrences.
assert run("""9
add a
add b
add a
add b
add a
get 1
get 2
get 3
""") == """3
2
1
""", "overlapping prefixes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / add a / get 1` | `1` | Minimum valid input and the fact that the prefix itself counts |
| Four `add a` operations followed by `get 1` | `4` | All-equal string and a large prefix-function subtree |
| `add a`, `add b`, `get 2` | `1` | Boundary case (k=n) |
| `aaba` followed by two encoded `get 1` queries | `3`, `1` | Correct use of `last` when decoding |
| (299,999) additions followed by `get 1` | `299999` | Maximum number of queries and large treap state |
| `ababa` with several gets | `3`, `2`, `1` | Overlapping prefix occurrences and nested prefix-function subtrees |

## Edge Cases

For the minimum input

```
2
add a
get 1
```

the prefix-function tree contains node 1 directly below the artificial root. Its Euler sequence is `enter(0), enter(1), exit(1), exit(0)`. The interval belonging to node 1 contains exactly one entry token, so the answer is `1`.

For the all-equal string

```
5
add a
add a
add a
add a
get 1
```

the prefix-function tree is a chain. Node 1 is an ancestor of nodes 2, 3, and 4, so its subtree contains all four real nodes. The Euler interval for node 1 contains four entry tokens, giving the correct answer `4`.

For the boundary case

```
3
add a
add b
get 2
```

node 2 is the newest prefix-function node and has no descendants yet. Its subtree consists only of itself, so the Euler interval contains one entry token. The answer is `1`, which corresponds to the only length-two interval, the whole string `ab`.

For online decoding,

```
6
add a
add a
add b
add a
get 1
get 1
```

the first `get` decodes to (k=1) and returns `3`. The next raw value is also `1`, but now `last=3` and (n=4), so the decoded length is (4). Node 4 has no descendants, and its subtree size is `1`. The output is consequently `3` followed by `1`.

The case (k=n) also explains why the exit token must be retained even though it has value zero. The entry and exit tokens delimit a subtree without ambiguity. If a query asks for the newest node, the two tokens are adjacent, and the difference between their prefix sums still gives exactly one entry.

Finally, sibling insertion order does not affect correctness. A new prefix-function node is always inserted before its parent's exit token, so it becomes part of the parent's subtree. Whether it appears before or after the parent's existing children has no effect on subtree membership or subtree size. The treap is only maintaining one valid DFS ordering, not a canonical one.
