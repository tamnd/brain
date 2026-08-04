---
title: "CF 102606F - Find / -type f -or -type d"
description: "The input describes a filesystem snapshot. Each line is an absolute path that represents either a file or a directory, but the lines are mixed in a random order."
date: "2026-08-04T17:03:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102606
codeforces_index: "F"
codeforces_contest_name: "2020 ECNU Campus Online Invitational Contest"
rating: 0
weight: 102606
solve_time_s: 66
verified: true
draft: false
---

[CF 102606F - Find / -type f -or -type d](https://codeforces.com/problemset/problem/102606/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a filesystem snapshot. Each line is an absolute path that represents either a file or a directory, but the lines are mixed in a random order. A directory appears only because some file exists inside it, so every directory in the list is an ancestor of at least one listed file. The task is to recover how many listed entries are files whose names end with `.eoj`.

The difficulty is that the input does not tell us which paths are files and which are directories. A path ending in `.eoj` is not automatically a valid answer because a directory can also have that suffix. For example, `/a.eoj/b` proves that `/a.eoj` is a directory, not a file.

The input size is large enough that every path must be processed efficiently. There can be 100000 paths and the total amount of characters across all paths is at most 1000000. This rules out approaches that compare every pair of paths, because that could require around 10^10 operations. An approach close to linear in the total input size is needed.

The tricky cases come from confusing names with file types. Consider:

```
1
/a.eoj
```

The answer is `1` because there is no child under `/a.eoj`, so this entry must be a file.

Now consider:

```
2
/a.eoj
/a.eoj/b
```

The answer is `0`. A careless solution that only checks the suffix would count `/a.eoj`, but the second path proves that `/a.eoj` is a directory.

Another case is:

```
2
/a.eoj/b.eoj
/a.eoj
```

The answer is `1`. The path `/a.eoj` is a directory even though it ends with `.eoj`, while `/a.eoj/b.eoj` is a file.

## Approaches

A straightforward solution is to store all paths and, for every path ending with `.eoj`, search the input to check whether another path has it as a prefix followed by a slash. If such a longer path exists, the candidate is a directory. This is correct because every directory must have at least one descendant. However, with 100000 paths this can require comparing every pair of paths. Even ignoring string comparison cost, this gives about 10^10 checks, which is too slow.

The key observation is that we do not need to test every possible ancestor relationship. The only information needed is whether a path has children. A path is a directory exactly when at least one other path starts with that path followed by `/`.

This turns the problem into a prefix problem. If we insert every path into a trie, every node that has children represents a directory. Every leaf node represents a path without descendants, which must be a file. Then we only count leaf nodes whose complete path ends with `.eoj`.

The trie fits naturally because the input is already hierarchical. Shared directory prefixes are stored once, and the total amount of work is proportional to the total number of characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²L) | O(nL) | Too slow |
| Trie | O(S) | O(S) | Accepted |

Here, `L` is the maximum path length and `S` is the total number of characters in all paths.

## Algorithm Walkthrough

1. Split every path into its components and insert the components into a trie. Each trie edge represents moving into one directory or file name component.

The trie stores the parent-child relationship hidden inside the shuffled list. The input order no longer matters because paths automatically connect to their ancestors during insertion.

1. Mark the node representing the end of every complete input path.

Only nodes corresponding to actual entries from the input should be counted. Intermediate trie nodes may exist only because they are ancestors of longer paths.

1. Traverse the trie after construction. For every marked node, check whether it has any children.

A marked node with children represents a directory because another input path continues below it. A marked node without children represents a file because nothing exists below it.

1. For every marked leaf node, rebuild or store its full path name and check whether the final component ends with `.eoj`. Increase the answer if it does.

The suffix belongs only to the final component. A directory name ending in `.eoj` is ignored because it cannot be a leaf.

Why it works:

The invariant is that every trie node with children corresponds to a path that has at least one longer input path beneath it. Since directories cannot exist without files inside them, such nodes must be directories. Conversely, a marked node without children has no descendant in the input, so it cannot be a directory and must be a file. The algorithm counts exactly the leaf entries with the required extension, which matches the definition of the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("children", "terminal", "name")

    def __init__(self, name=""):
        self.children = {}
        self.terminal = False
        self.name = name

def solve():
    n = int(input())
    root = Node()

    for _ in range(n):
        path = input().strip()
        parts = path.split("/")[1:]
        cur = root
        for part in parts:
            if part not in cur.children:
                cur.children[part] = Node(part)
            cur = cur.children[part]
        cur.terminal = True

    ans = 0

    def dfs(node):
        nonlocal ans
        if node.terminal and not node.children and node.name.endswith(".eoj"):
            ans += 1
        for child in node.children.values():
            dfs(child)

    dfs(root)
    print(ans)

if __name__ == "__main__":
    solve()
```

The insertion phase creates one trie node for each unique path component under its parent. The first component is inserted below the root because the leading slash is not a meaningful directory name.

The `terminal` flag separates paths that actually appeared in the input from nodes created only as ancestors. This matters because a directory can be present as a listed entry, but an intermediate node alone does not represent a file or directory in the answer.

During DFS, the condition `not node.children` identifies leaves. The suffix check is applied only after confirming the node is a file candidate. Python integers have arbitrary precision, so no overflow handling is needed for the answer count.

## Worked Examples

For the first sample:

```
/secret/eoj
/secret
/secret.eoj
```

The trie state after insertion is:

| Path node | Has children | Terminal | Counted |
| --- | --- | --- | --- |
| secret | yes | yes | no |
| secret/eoj | no | yes | no |
| secret.eoj | no | yes | yes |

The directory `/secret` is rejected because it has a child. The file `/secret/eoj` does not have the required suffix. Only `/secret.eoj` contributes to the answer, so the result is `1`.

For the second sample:

```
/cuber.eoj/qq.eoj
/cuber.eoj
```

The trie state is:

| Path node | Has children | Terminal | Counted |
| --- | --- | --- | --- |
| cuber.eoj | yes | yes | no |
| cuber.eoj/qq.eoj | no | yes | yes |

Although `/cuber.eoj` ends with `.eoj`, it has a child and is a directory. The leaf `/cuber.eoj/qq.eoj` is the only file counted, giving answer `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S) | Every character is inserted once and every trie node is visited once |
| Space | O(S) | The trie stores the path structure |

The total input length is at most 1000000 characters, so a linear solution comfortably fits the constraints. The trie avoids repeated prefix comparisons and uses the filesystem structure directly.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline

    class Node:
        def __init__(self, name=""):
            self.children = {}
            self.terminal = False
            self.name = name

    n = int(data())
    root = Node()

    for _ in range(n):
        parts = data().strip().split("/")[1:]
        cur = root
        for p in parts:
            if p not in cur.children:
                cur.children[p] = Node(p)
            cur = cur.children[p]
        cur.terminal = True

    ans = 0

    def dfs(x):
        nonlocal ans
        if x.terminal and not x.children and x.name.endswith(".eoj"):
            ans += 1
        for y in x.children.values():
            dfs(y)

    dfs(root)
    sys.stdin = old
    return str(ans) + "\n"

assert run("""3
/secret/eoj
/secret
/secret.eoj
""") == "1\n", "sample 1"

assert run("""2
/cuber.eoj/qq.eoj
/cuber.eoj
""") == "1\n", "sample 2"

assert run("""1
/a.eoj
""") == "1\n", "single file"

assert run("""2
/a.eoj
/a.eoj/b
""") == "0\n", "directory with eoj suffix"

assert run("""4
/a.eoj/b.eoj
/a.eoj
/x
/y.eoj
""") == "2\n", "mixed files and directories"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `/a.eoj` | `1` | A single suffix-matching file |
| `/a.eoj` and `/a.eoj/b` | `0` | A directory whose name ends with `.eoj` |
| Mixed tree | `2` | Multiple independent branches |

## Edge Cases

A suffix check alone fails when a directory has a name ending in `.eoj`.

Input:

```
2
/a.eoj
/a.eoj/b
```

During trie construction, `/a.eoj` gets a child node `b`. The DFS sees that `/a.eoj` is not a leaf, so it is not counted. The result is `0`.

A nested file with a suffix-matching ancestor must not affect the ancestor.

Input:

```
2
/a.eoj/b.eoj
/a.eoj
```

The trie contains a child under `a.eoj`, so that node is treated as a directory. The node for `b.eoj` has no children and ends with `.eoj`, so it contributes one count. The output is `1`.

The shortest valid input contains one path only.

Input:

```
1
/x
```

The trie contains one terminal leaf node. Since `x` does not end with `.eoj`, the DFS returns `0`. This confirms that the algorithm does not count every file, only files with the required extension.

You can further adapt this into a shorter contest editorial format or a more explanatory blog-style version if needed.
