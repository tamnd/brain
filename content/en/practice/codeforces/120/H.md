---
title: "CF 120H - Brevity is Soul of Wit"
description: "We are given up to 200 distinct lowercase words. For every word, we must choose a short abbreviation whose length is between 1 and 4 characters, and whose characters appear in the original word in the same order."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graph-matchings"]
categories: ["algorithms"]
codeforces_contest: 120
codeforces_index: "H"
codeforces_contest_name: "School Regional Team Contest, Saratov, 2011"
rating: 1800
weight: 120
solve_time_s: 153
verified: false
draft: false
---

[CF 120H - Brevity is Soul of Wit](https://codeforces.com/problemset/problem/120/H)

**Rating:** 1800  
**Tags:** graph matchings  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given up to 200 distinct lowercase words. For every word, we must choose a short abbreviation whose length is between 1 and 4 characters, and whose characters appear in the original word in the same order. The characters do not need to be adjacent, so every abbreviation is simply a subsequence of the word.

The key restriction is uniqueness. Two different words cannot receive the same abbreviation. If such an assignment exists, we must print one valid abbreviation for each word. Otherwise we print `-1`.

The small word length changes the nature of the problem completely. Each word has length at most 10, and abbreviations are limited to length at most 4. That means the total number of possible subsequences per word is small enough to enumerate directly.

For a word of length 10, the number of subsequences of lengths 1 through 4 is:

$$\binom{10}{1} + \binom{10}{2} + \binom{10}{3} + \binom{10}{4}$$

$\binom{10}{1}+\binom{10}{2}+\binom{10}{3}+\binom{10}{4}$

This equals 385. Even after removing duplicates, each word contributes only a few hundred candidate abbreviations. With at most 200 words, we are comfortably within graph-based matching territory.

The dangerous part is not generating subsequences. The real difficulty is handling collisions correctly.

Consider this example:

```
2
abcd
abdc
```

Both words can generate `ab`, `ac`, `ad`, and many others. A greedy algorithm that assigns the first unused abbreviation to each word may fail depending on ordering. If we give `abcd` the abbreviation `abd`, the second word might lose its only remaining option even though a different global assignment exists.

Another subtle case appears when a word generates duplicate subsequences through different index selections.

Example:

```
1
aaaa
```

The subsequence `aa` can be formed many ways, but it must only appear once in the candidate list. Forgetting deduplication bloats the graph and can create unnecessary repeated edges.

There is also the impossible case:

```
3
a
aa
aaa
```

Every word can only generate the abbreviation `a`. Since abbreviations must be distinct, the correct output is:

```
-1
```

A careless implementation that only checks local feasibility would incorrectly print repeated abbreviations.

## Approaches

The most direct idea is brute force backtracking. For every word, generate all valid abbreviations, then recursively try assigning unused abbreviations. If we reach the end successfully, we print the assignment.

This works because the search space is finite. The problem is the branching factor. A single word may have around 300 distinct abbreviations. In the worst case, trying all combinations becomes astronomically large:

$$300^{200}$$

$300^{200}$

Even with pruning, unrestricted backtracking is hopeless.

The important observation is that this is not really a sequencing problem. It is an assignment problem.

Each word has a set of acceptable abbreviations. We need to choose one distinct abbreviation per word. This is exactly bipartite matching.

We build a graph with two sides:

- Left side: words.
- Right side: all distinct abbreviations that appear as subsequences of some word.

We connect a word to every abbreviation it can use.

Now the task becomes finding a matching that covers every word. If such a matching exists, each matched edge gives the chosen abbreviation.

This transformation is powerful because maximum bipartite matching solves global conflicts automatically. If one word takes an abbreviation that blocks another word, the augmenting path process can rearrange previous choices.

The graph is small enough for a standard DFS-based Kuhn algorithm. At most 200 words exist, and each contributes at most a few hundred edges. The total graph size stays manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) recursion | Too slow |
| Optimal | O(VE) | O(E) | Accepted |

## Algorithm Walkthrough

1. Read all words.
2. For every word, generate every distinct subsequence of lengths 1 through 4.

We enumerate subsets of positions using recursion or combinations. Since the original order must be preserved, selecting indices automatically produces valid subsequences.
3. Compress all distinct abbreviations into integer IDs.

Matching algorithms work more efficiently with compact indices than raw strings.
4. Build a bipartite graph.

The left side contains one node per word. The right side contains one node per unique abbreviation. Add an edge from word `i` to abbreviation `j` if that abbreviation can be formed from the word.
5. Run Kuhn's algorithm for maximum bipartite matching.

For every word, try to find an augmenting path that assigns it a unique abbreviation. If an abbreviation is already occupied, recursively try to reroute the currently matched word elsewhere.
6. Count how many words were successfully matched.

If the matching size is smaller than `n`, no valid assignment exists and we print `-1`.
7. Otherwise reconstruct the answer.

Every matched abbreviation corresponds to exactly one word. Output those abbreviations in input order.

### Why it works

The graph contains exactly the valid choices for every word. A matching selects edges so that no two words share the same abbreviation.

If a perfect matching exists, then every word receives one unique valid abbreviation. Conversely, any valid solution directly corresponds to a matching covering all words.

Kuhn's algorithm repeatedly finds augmenting paths. Each augmenting path increases the number of matched words by one while preserving uniqueness. Since augmenting paths are the fundamental characterization of maximum bipartite matching, the final matching is maximum possible. If its size equals `n`, a complete assignment exists.

## Python Solution

```python
import sys
from itertools import combinations

input = sys.stdin.readline

def generate(word):
    s = set()
    m = len(word)

    for length in range(1, min(4, m) + 1):
        for idxs in combinations(range(m), length):
            cur = ''.join(word[i] for i in idxs)
            s.add(cur)

    return list(s)

def solve():
    n = int(input())
    words = [input().strip() for _ in range(n)]

    abbr_id = {}
    abbr_list = []

    graph = []

    for word in words:
        subs = generate(word)

        edges = []

        for sub in subs:
            if sub not in abbr_id:
                abbr_id[sub] = len(abbr_list)
                abbr_list.append(sub)

            edges.append(abbr_id[sub])

        graph.append(edges)

    m = len(abbr_list)

    match_right = [-1] * m

    def dfs(v, vis):
        for to in graph[v]:
            if vis[to]:
                continue

            vis[to] = True

            if match_right[to] == -1 or dfs(match_right[to], vis):
                match_right[to] = v
                return True

        return False

    matched = 0

    for v in range(n):
        vis = [False] * m

        if dfs(v, vis):
            matched += 1

    if matched != n:
        print(-1)
        return

    ans = [""] * n

    for abbr_idx, word_idx in enumerate(match_right):
        if word_idx != -1:
            ans[word_idx] = abbr_list[abbr_idx]

    print('\n'.join(ans))

solve()
```

The `generate` function enumerates all subsequences of lengths 1 through 4. Using `combinations` is convenient because choosing increasing indices automatically preserves character order. The `set` removes duplicates such as multiple ways to form `"aa"` from `"aaaa"`.

The graph construction phase assigns every unique abbreviation an integer ID. This compression matters because many words may share the same abbreviation candidate.

The matching itself uses the standard DFS augmenting-path implementation of Kuhn's algorithm. The recursive call is the critical step. When an abbreviation is already occupied, we try to move the currently assigned word somewhere else. That ability to reshuffle assignments is what makes matching fundamentally stronger than greedy selection.

The `vis` array must be recreated for every DFS attempt. Reusing it across iterations would incorrectly block valid augmenting paths.

Finally, the matching is stored from abbreviation to word. After the algorithm finishes, we invert that mapping into the required output order.

## Worked Examples

### Example 1

Input:

```
6
privet
spasibo
codeforces
java
marmelad
normalno
```

Generated abbreviations are huge, so we only track the successful matching decisions.

| Word | Some candidate abbreviations | Chosen |
| --- | --- | --- |
| privet | `pr`, `pret`, `pvt`, `riv` | `pret` |
| spasibo | `sps`, `spo`, `sbo` | `sps` |
| codeforces | `cdfs`, `code`, `cofs` | `cdfs` |
| java | `j`, `ja`, `java` | `java` |
| marmelad | `mama`, `mard`, `mela` | `mama` |
| normalno | `norm`, `nrml`, `nalo` | `norm` |

Output:

```
pret
sps
cdfs
java
mama
norm
```

This trace shows the central property of matching. Multiple words may share candidates, but the final assignment guarantees uniqueness globally.

### Example 2

Input:

```
3
a
aa
aaa
```

| Word | Candidate abbreviations |
| --- | --- |
| a | `a` |
| aa | `a`, `aa` |
| aaa | `a`, `aa`, `aaa` |

Possible matching process:

| Step | Assigned abbreviation |
| --- | --- |
| Match word 1 | `a` |
| Match word 2 | `aa` |
| Match word 3 | `aaa` |

Output:

```
a
aa
aaa
```

This demonstrates why subsequences longer than 1 matter. Even though all words share `a`, the larger words can move to alternative abbreviations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(VE) | Kuhn's algorithm over the bipartite graph |
| Space | O(E) | Adjacency lists plus matching arrays |

Here, `V` is the number of words plus abbreviations, and `E` is the number of valid word-abbreviation pairs.

Each word generates at most 385 subsequences, so:

$$E \le 200 \times 385$$

$200\times385$

This is comfortably small for a DFS-based matching implementation inside the 2-second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import combinations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def generate(word):
        s = set()
        m = len(word)

        for length in range(1, min(4, m) + 1):
            for idxs in combinations(range(m), length):
                s.add(''.join(word[i] for i in idxs))

        return list(s)

    n = int(input())
    words = [input().strip() for _ in range(n)]

    abbr_id = {}
    abbr_list = []
    graph = []

    for word in words:
        edges = []

        for sub in generate(word):
            if sub not in abbr_id:
                abbr_id[sub] = len(abbr_list)
                abbr_list.append(sub)

            edges.append(abbr_id[sub])

        graph.append(edges)

    m = len(abbr_list)

    match_right = [-1] * m

    def dfs(v, vis):
        for to in graph[v]:
            if vis[to]:
                continue

            vis[to] = True

            if match_right[to] == -1 or dfs(match_right[to], vis):
                match_right[to] = v
                return True

        return False

    matched = 0

    for v in range(n):
        vis = [False] * m

        if dfs(v, vis):
            matched += 1

    if matched != n:
        return "-1"

    ans = [""] * n

    for i, v in enumerate(match_right):
        if v != -1:
            ans[v] = abbr_list[i]

    return "\n".join(ans)

# provided-style sample
out = run(
"""6
privet
spasibo
codeforces
java
marmelad
normalno
"""
)

assert len(out.splitlines()) == 6

# minimum case
assert run(
"""1
a
"""
) == "a"

# impossible case
assert run(
"""2
a
a
"""
) == "-1"

# repeated-character subsequences
out = run(
"""3
a
aa
aaa
"""
)

lines = out.splitlines()
assert len(set(lines)) == 3

# boundary length 10
out = run(
"""2
abcdefghij
jihgfedcba
"""
)

assert len(out.splitlines()) == 2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single word `a` | `a` | Minimum-size input |
| Two identical `a` words | `-1` | Impossible assignment detection |
| `a`, `aa`, `aaa` | Three distinct abbreviations | Matching reassignment logic |
| Two length-10 words | Any valid pair | Maximum subsequence generation |

## Edge Cases

Consider the repeated-character case:

```
1
aaaa
```

The subsequence `aa` can be generated using many index pairs:

- positions `(0,1)`
- positions `(0,2)`
- positions `(1,3)`

The algorithm stores subsequences in a set before adding graph edges. As a result, the graph contains only one edge for `aa`. This prevents unnecessary duplicate edges and keeps matching behavior clean.

Now consider the impossible collision case:

```
2
a
a
```

Both words generate only one abbreviation:

| Word | Candidates |
| --- | --- |
| 1 | `a` |
| 2 | `a` |

The matching can cover at most one word. After running Kuhn's algorithm, the matching size is `1 < 2`, so the algorithm prints `-1`.

Finally, consider a case where greedy fails but matching succeeds:

```
2
abcd
abdc
```

Suppose the first word initially grabs `abd`. The second word may later need that abbreviation. During DFS, the algorithm explores augmenting paths and can reassign the first word to another valid abbreviation like `abc`. This flexibility is exactly why bipartite matching solves the global uniqueness constraint correctly.
