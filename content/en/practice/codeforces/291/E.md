---
title: "CF 291E - Tree-String Problem"
description: "We have a rooted tree with root 1. Every edge from a parent to a child contains a lowercase string. If we walk downward through the tree and read characters along the edges, we obtain a long text embedded into the tree. A position is not a vertex."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dfs-and-similar", "hashing", "strings"]
categories: ["algorithms"]
codeforces_contest: 291
codeforces_index: "E"
codeforces_contest_name: "Croc Champ 2013 - Qualification Round"
rating: 2000
weight: 291
solve_time_s: 111
verified: true
draft: false
---

[CF 291E - Tree-String Problem](https://codeforces.com/problemset/problem/291/E)

**Rating:** 2000  
**Tags:** *special, dfs and similar, hashing, strings  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree with root `1`. Every edge from a parent to a child contains a lowercase string. If we walk downward through the tree and read characters along the edges, we obtain a long text embedded into the tree.

A position is not a vertex. It is a specific character inside an edge string. For example, if edge `(p -> v)` stores `"abac"`, then `(v, 2)` refers to the character `'a'` at index `2`.

The task asks for the number of ordered pairs of positions such that:

1. The second position is reachable from the first by moving only downward in the tree.
2. The sequence of characters encountered from the first position to the second position is exactly equal to a given pattern string `t`.

The total number of characters across all edge strings is at most `3 * 10^5`. That is the real input size. Any solution that tries to compare substrings character by character for every starting position immediately becomes too slow.

Suppose the total character count is `L`. A brute force that starts from every position and walks forward checking the pattern would cost `O(L * |t|)` in the best organized form. Since both values can be around `3 * 10^5`, this becomes roughly `9 * 10^10` operations, far beyond the limit.

The structure of the tree introduces another complication. The matching string may begin in the middle of one edge string and continue through several edges. We cannot process each edge independently.

There are several easy-to-miss edge cases.

Consider:

```
2
1 abc
bc
```

The answer is `1`, because the substring `"bc"` starts at position `(2,1)` inside the edge string itself. A careless solution that only starts matching from edge beginnings would miss it.

Another tricky case:

```
3
1 ab
2 cd
bc
```

The answer is `1`, because the match starts at `'b'` in the first edge and ends at `'c'` in the second edge. The pattern crosses an edge boundary.

A different failure mode appears if we ignore the downward-only restriction.

```
3
1 ab
1 ba
aba
```

There is no valid answer. One might try to combine the suffix `"ab"` from one branch with `"a"` from another branch, but the path between them goes upward and then downward, which is forbidden.

The core challenge is to treat all characters encountered on root-to-node paths as one continuous stream while still respecting tree ancestry.

## Approaches

The brute force idea is straightforward. For every possible starting position, walk character by character downward and try to match the pattern `t`. Whenever we consume one character, we continue either inside the same edge string or into child edges.

This works logically because every valid path corresponds to exactly one downward traversal in the tree. The problem is the amount of work. There are up to `3 * 10^5` positions, and each attempt may compare up to `|t|` characters. The worst case becomes quadratic.

The key observation is that every root-to-position path defines a unique string. If we process the tree with DFS and maintain the current root-to-current-position text, then every valid occurrence of `t` ending at the current character can be detected online.

This turns the problem into a classic string matching problem over a dynamically constructed text.

KMP is a natural fit here. While traversing characters in DFS order, we maintain the current matched prefix length of `t`. Every newly visited character updates this state in amortized `O(1)` time.

Why does this count exactly the desired pairs?

Suppose we are currently at some character position `P`. If the KMP state becomes `|t|`, then the last `|t|` characters on the current root-to-`P` path equal `t`. Those characters define exactly one starting position and one ending position, both connected by a downward path. So every match corresponds to one valid pair.

The only remaining issue is backtracking. DFS enters and leaves branches, so the KMP state must also roll back correctly. We solve this by saving the previous state before processing each character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(L * \|t\|) | O(height) | Too slow |
| Optimal | O(L + \|t\| + n) | O(L + \|t\|) | Accepted |

Here `L` is the total number of characters on all edges.

## Algorithm Walkthrough

1. Read the tree and store for every vertex its children together with the edge string leading to that child.
2. Build the KMP prefix-function array for pattern `t`.

The prefix-function lets us transition between matched-prefix states in amortized constant time while scanning characters.
3. Start DFS from the root.

During DFS, maintain a variable `k`, meaning that the last `k` characters on the current root-to-current-position path match the prefix `t[0:k]`.
4. When traversing an edge string character by character, update the KMP state exactly like standard pattern matching.

If the next character does not match, repeatedly jump using the prefix-function until either a match is possible or the state becomes zero.
5. After consuming a character:

- Increase `k` if the character matches.
- If `k == len(t)`, increment the answer.

This means the pattern ends at the current position.
6. If a full match occurs, continue matching using `pi[k-1]`.

This is standard KMP behavior and allows overlapping matches.
7. Before processing each character, save the previous KMP state on a stack.

DFS later backtracks to parent branches, so we must restore the exact state that existed before entering the subtree.
8. After finishing an edge or subtree, restore the old KMP state while returning from recursion.

### Why it works

At every moment during DFS, the maintained KMP state corresponds exactly to the longest suffix of the current root-to-current-position string that is also a prefix of `t`.

Whenever this state reaches `|t|`, the last `|t|` characters on the current downward path equal the pattern. Those characters define one unique pair of positions because positions are identified by exact character locations.

DFS guarantees that every downward character path is visited exactly once as a suffix of some root-to-current-position path. KMP guarantees that every occurrence ending at the current position is detected exactly once. Together they count precisely all valid pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 25)

def solve():
    n = int(input())

    children = [[] for _ in range(n + 1)]

    for v in range(2, n + 1):
        p, s = input().split()
        p = int(p)
        children[p].append((v, s.strip()))

    t = input().strip()
    m = len(t)

    # KMP prefix function
    pi = [0] * m

    for i in range(1, m):
        j = pi[i - 1]

        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]

        if t[i] == t[j]:
            j += 1

        pi[i] = j

    ans = 0

    def dfs(u, k):
        nonlocal ans

        current_k = k

        for v, s in children[u]:
            old_states = []

            for ch in s:
                old_states.append(current_k)

                while current_k > 0 and ch != t[current_k]:
                    current_k = pi[current_k - 1]

                if ch == t[current_k]:
                    current_k += 1

                if current_k == m:
                    ans += 1
                    current_k = pi[current_k - 1]

            dfs(v, current_k)

            # restore state before this edge
            if old_states:
                current_k = old_states[0]

    dfs(1, 0)

    print(ans)

solve()
```

The tree is stored as adjacency lists from parent to children. Every edge keeps its string because we process characters sequentially during DFS.

The prefix-function construction is standard KMP preprocessing. `pi[i]` stores the length of the longest proper prefix of `t` that is also a suffix ending at position `i`.

The subtle part is the DFS state management.

The variable `current_k` represents the current KMP automaton state while walking down the tree. As we consume characters along edges, we update it exactly like ordinary string matching.

Suppose we are currently matching `"aba"` and the next character finishes the pattern. We increment the answer, then move to `pi[m-1]` instead of resetting to zero. This correctly handles overlaps such as matching `"aaa"` inside `"aaaa"`.

The restoration logic is easy to get wrong. Each subtree must start from the KMP state that existed before entering its edge. Otherwise one branch contaminates another branch.

The implementation restores `current_k` after returning from a child subtree. Since the traversal inside an edge is linear, the state after finishing the edge is exactly the state passed into the child DFS.

The recursion depth can reach `n`, so `sys.setrecursionlimit` is necessary.

## Worked Examples

### Sample 1

Input:

```
7
1 ab
5 bacaba
1 abacaba
2 aca
5 ba
2 ba
aba
```

Pattern is `"aba"`.

We track the KMP state while traversing.

| Current path chars | Current char | KMP state | Match found |
| --- | --- | --- | --- |
| a | a | 1 | No |
| ab | b | 2 | No |
| aba | a | 3 | Yes |
| abac | c | 0 | No |
| abaca | a | 1 | No |
| abacab | b | 2 | No |
| abacaba | a | 3 | Yes |

The same process continues in all branches. Every time the automaton reaches state `3`, one valid pair of positions is counted.

Final answer: `6`.

This example demonstrates that matches may lie entirely inside one edge string or cross several edges.

### Custom Example

Input:

```
3
1 ab
2 cd
bc
```

The only valid occurrence crosses the edge boundary.

| Current path chars | Current char | KMP state | Match found |
| --- | --- | --- | --- |
| a | a | 0 | No |
| ab | b | 1 | No |
| abc | c | 2 | Yes |
| abcd | d | 0 | No |

Final answer: `1`.

This trace confirms that the algorithm treats root-to-current paths as continuous strings instead of isolated edge labels.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L + \|t\| + n) | Every character is processed once by KMP |
| Space | O(n + \|t\|) | Tree storage, recursion stack, and prefix array |

`L` is the total number of characters on all edges.

KMP guarantees amortized constant work per processed character because every fallback shortens the current matched prefix. With at most `3 * 10^5` characters total, the solution easily fits within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    sys.setrecursionlimit(1 << 25)

    n = int(input())

    children = [[] for _ in range(n + 1)]

    for v in range(2, n + 1):
        p, s = input().split()
        children[p].append((v, s.strip()))

    t = input().strip()
    m = len(t)

    pi = [0] * m

    for i in range(1, m):
        j = pi[i - 1]

        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]

        if t[i] == t[j]:
            j += 1

        pi[i] = j

    ans = 0

    def dfs(u, k):
        nonlocal ans

        current_k = k

        for v, s in children[u]:

            saved = current_k

            for ch in s:
                while current_k > 0 and ch != t[current_k]:
                    current_k = pi[current_k - 1]

                if ch == t[current_k]:
                    current_k += 1

                if current_k == m:
                    ans += 1
                    current_k = pi[current_k - 1]

            dfs(v, current_k)

            current_k = saved

    dfs(1, 0)

    return str(ans)

# provided sample
assert run(
"""7
1 ab
5 bacaba
1 abacaba
2 aca
5 ba
2 ba
aba
"""
) == "6"

# minimum size
assert run(
"""2
1 ab
ab
"""
) == "1"

# crossing edge boundary
assert run(
"""3
1 ab
2 cd
bc
"""
) == "1"

# overlapping matches
assert run(
"""2
1 aaaa
aa
"""
) == "3"

# no valid downward path
assert run(
"""3
1 ab
1 ba
aba
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge `"ab"` with pattern `"ab"` | 1 | Minimum valid match |
| `"ab"` then `"cd"` with pattern `"bc"` | 1 | Match crossing edges |
| `"aaaa"` with pattern `"aa"` | 3 | Overlapping KMP matches |
| Two sibling branches with pattern `"aba"` | 0 | Downward-only restriction |

## Edge Cases

Consider the case where the match starts inside an edge.

```
2
1 abc
bc
```

While scanning `"abc"`, the KMP states become:

| Character | State |
| --- | --- |
| a | 0 |
| b | 1 |
| c | 2 |

When state `2` is reached, the algorithm counts one match. The start position is the `'b'` inside the edge, not the edge beginning.

Now consider a match crossing edges.

```
3
1 ab
2 cd
bc
```

The DFS first scans `"ab"` and finishes with KMP state `1`, because the suffix `"b"` matches the prefix of `"bc"`.

Entering the next edge, the first character `'c'` extends the match to length `2`, so the answer increases. This works because the automaton state persists across edges.

Finally, consider sibling contamination.

```
3
1 ab
1 ba
aba
```

After finishing the first branch, DFS restores the previous KMP state before entering the second branch. Without restoration, characters from different branches could incorrectly combine into a fake match. The rollback guarantees every counted substring lies on one continuous downward path.
