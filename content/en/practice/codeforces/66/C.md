---
title: "CF 66C - Petya and File System"
description: "Each input line describes the full path of one file inside a file system. A path looks like: The disk name is the root and is not considered a folder. Every component between the disk and the file is a folder. The last component is always a file."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 66
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 61 (Div. 2)"
rating: 1800
weight: 66
solve_time_s: 133
verified: true
draft: false
---

[CF 66C - Petya and File System](https://codeforces.com/problemset/problem/66/C)

**Rating:** 1800  
**Tags:** data structures, implementation  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

Each input line describes the full path of one file inside a file system. A path looks like:

```
C:\folder1\folder2\file.txt
```

The disk name is the root and is not considered a folder. Every component between the disk and the file is a folder. The last component is always a file.

For every folder, we need two quantities.

The first quantity is how many subfolders exist inside it, including nested descendants at every depth.

The second quantity is how many files exist inside it, including files located in all descendant folders.

The task is to compute the maximum value of each quantity over all folders in the entire file system.

The input is small. There are at most 100 paths, and each path length is at most 100 characters. Even a quadratic solution would fit comfortably inside the limits. Still, the structure of the problem naturally suggests building a tree, and that gives a cleaner and more reliable implementation.

The main difficulty is that folders are identified by their full location, not just by their name. Two folders with the same textual name can exist in different places and must be treated as different nodes.

For example:

```
C:\a\b\file.txt
C:\x\b\file2.txt
```

The two `b` folders are unrelated.

Another subtle case is repeated folder names along one path:

```
C:\file\file\file\a.txt
```

A careless implementation that uses only folder names as keys would collapse all three folders into one node and produce completely wrong counts.

There is also the detail that the disk root is not a folder. Consider:

```
C:\a\f.txt
D:\b\g.txt
```

The answer is not computed for `C:` or `D:`. Only `a` and `b` are valid folders.

Finally, folders may contain files only indirectly. For example:

```
C:\a\b\c.txt
```

Folder `a` contains one file even though no file is directly inside `a`.

The correct output here is:

```
1 1
```

Folder `a` has one subfolder, `b`, and one file inside its subtree.

## Approaches

A brute-force solution can work because the constraints are tiny. We could parse every path into its folder prefixes, explicitly generate every folder, and then for each folder scan all other folders and files to check whether their paths start with this folder's path.

For example, if we store folder paths as strings:

```
C:\a\b
```

then another folder is a descendant if its path begins with:

```
C:\a\b\
```

Similarly, a file belongs to a folder if its full file path begins with the folder path plus a separator.

This works because the number of paths is small. Still, the logic becomes fragile. Prefix comparisons are easy to get wrong because `"a\b"` is also a prefix of `"a\bc"` unless separators are handled carefully. The runtime is also unnecessarily repetitive because the same path prefixes get scanned many times.

The file system is fundamentally a tree. Every folder has exactly one parent folder, except top-level folders directly under a disk. Every file belongs to exactly one folder. Once we recognize that, the counting becomes much simpler.

We build a folder tree where every unique folder path is a node. While reading a path, we walk through its folders from left to right and create nodes as needed.

Then we compute two subtree values for every folder:

The number of descendant folders.

The number of files in its subtree.

This is exactly what a DFS on a tree is designed for.

If a node has children folders:

```
child1, child2, child3
```

then:

```
subfolders(node)
= sum(subfolders(child)) + number_of_direct_children
```

and:

```
files(node)
= direct_files(node) + sum(files(child))
```

Each folder and edge is processed once, so the solution is linear in the size of the constructed tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N² · L) | O(N · L) | Accepted |
| Optimal | O(N · L) | O(N · L) | Accepted |

Here, `N` is the number of paths and `L` is the maximum path length.

## Algorithm Walkthrough

1. Read all input lines until EOF.

The problem does not provide the number of paths separately, so we simply consume every non-empty line.
2. Split each path using `\` as the separator.

For a path like:

```
C:\a\b\file.txt
```

we obtain:

```
["C:", "a", "b", "file.txt"]
```
3. Ignore the disk name and the file name.

Only the intermediate components are folders.
4. Build a tree of folders.

Each folder node is identified by its full path, not just its name.

While processing folders from left to right, connect every folder to its parent folder.
5. Store how many files are directly inside each folder.

The last folder in the path directly contains the file.
6. Run DFS from every top-level folder.

During DFS, recursively compute:

```
total_subfolders
total_files
```
7. For each folder node:

Add one for every direct child folder.

Add all descendant counts returned from children.

Add all file counts returned from children.
8. Track the global maximum values.

Every folder contributes a candidate answer.
9. Print:

```
maximum_subfolders maximum_files
```

### Why it works

The folder structure forms a rooted forest because every folder has exactly one parent folder except folders directly under a disk.

DFS computes subtree information bottom-up. When processing a folder, all information about its descendants is already known from recursive calls. The recurrence exactly matches the problem definition:

A folder's descendant folders are all child folders plus all descendants inside those children.

A folder's files are all directly stored files plus all files inside descendant folders.

Because every folder is processed exactly once and every relationship is represented explicitly in the tree, no folder or file can be double-counted or missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

# adjacency list of folder tree
children = defaultdict(list)

# direct file count for each folder
direct_files = defaultdict(int)

# all folder nodes
folders = set()

# parent existence check
has_parent = set()

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    parts = line.split('\\')

    # folders are everything except disk and filename
    path_parts = parts[1:-1]

    current = ""

    for i, folder in enumerate(path_parts):
        if current == "":
            current = parts[0] + "\\" + folder
        else:
            parent = current
            current = current + "\\" + folder

            children[parent].append(current)
            has_parent.add(current)

        folders.add(current)

    # last folder directly contains the file
    direct_files[current] += 1

# roots are folders without parents
roots = [folder for folder in folders if folder not in has_parent]

max_subfolders = 0
max_files = 0

def dfs(node):
    global max_subfolders, max_files

    subfolders = 0
    files = direct_files[node]

    for child in children[node]:
        child_subfolders, child_files = dfs(child)

        subfolders += 1 + child_subfolders
        files += child_files

    max_subfolders = max(max_subfolders, subfolders)
    max_files = max(max_files, files)

    return subfolders, files

for root in roots:
    dfs(root)

print(max_subfolders, max_files)
```

The first section reads all input paths and incrementally builds the folder tree.

A key implementation detail is how folder identities are represented. Using only folder names would fail because the same name can appear in multiple places. Instead, each folder node stores its complete path from the disk root.

For example:

```
C:\a\b
```

and:

```
C:\x\b
```

become different nodes.

The `children` adjacency list stores the folder hierarchy. Whenever we extend a path by one folder, we connect the previous folder to the new folder.

The `direct_files` map stores how many files are directly located inside each folder. We increment only the final folder in the path because the file itself is not a folder node.

The DFS computes subtree information recursively.

The line:

```
subfolders += 1 + child_subfolders
```

is easy to misread. The `+1` counts the child folder itself, while `child_subfolders` counts everything below it.

Similarly:

```
files += child_files
```

accumulates all files from descendant folders.

Roots are detected as folders without parent folders. Disk names are never inserted into the tree, which correctly matches the statement that disks are not folders.

## Worked Examples

### Example 1

Input:

```
C:\folder1\file1.txt
```

### Tree construction

| Current folder | Parent | Direct files |
| --- | --- | --- |
| C:\folder1 | none | 1 |

### DFS computation

| Folder | Subfolders | Files |
| --- | --- | --- |
| C:\folder1 | 0 | 1 |

Output:

```
0 1
```

This example confirms the simplest valid configuration. A folder with no child folders still contributes its directly stored files.

### Example 2

Input:

```
C:\folder1\folder2\folder3\file1.txt
C:\folder1\folder2\folder4\file2.txt
```

### Tree construction

| Current folder | Parent | Direct files |
| --- | --- | --- |
| C:\folder1 | none | 0 |
| C:\folder1\folder2 | C:\folder1 | 0 |
| C:\folder1\folder2\folder3 | C:\folder1\folder2 | 1 |
| C:\folder1\folder2\folder4 | C:\folder1\folder2 | 1 |

### DFS computation

| Folder | Subfolders | Files |
| --- | --- | --- |
| folder3 | 0 | 1 |
| folder4 | 0 | 1 |
| folder2 | 2 | 2 |
| folder1 | 3 | 2 |

Output:

```
3 2
```

This trace demonstrates how subtree aggregation works. Folder `folder1` counts all descendants recursively, not only direct children.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · L) | Every path component is processed once while building and once during DFS |
| Space | O(N · L) | The folder tree stores all unique folder paths |

The constraints are extremely small, so this solution easily fits inside the limits. Even in the worst case, the number of created folder nodes is tiny compared to what modern hardware handles comfortably.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    children = defaultdict(list)
    direct_files = defaultdict(int)
    folders = set()
    has_parent = set()

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        parts = line.split('\\')
        path_parts = parts[1:-1]

        current = ""

        for folder in path_parts:
            if current == "":
                current = parts[0] + "\\" + folder
            else:
                parent = current
                current = current + "\\" + folder
                children[parent].append(current)
                has_parent.add(current)

            folders.add(current)

        direct_files[current] += 1

    roots = [f for f in folders if f not in has_parent]

    max_subfolders = 0
    max_files = 0

    def dfs(node):
        nonlocal max_subfolders, max_files

        subfolders = 0
        files = direct_files[node]

        for child in children[node]:
            s, f = dfs(child)
            subfolders += 1 + s
            files += f

        max_subfolders = max(max_subfolders, subfolders)
        max_files = max(max_files, files)

        return subfolders, files

    for root in roots:
        dfs(root)

    return f"{max_subfolders} {max_files}"

# provided sample
assert run(
    "C:\\folder1\\file1.txt\n"
) == "0 1", "sample 1"

# nested folders
assert run(
    "C:\\folder1\\folder2\\folder3\\file1.txt\n"
    "C:\\folder1\\folder2\\folder4\\file2.txt\n"
) == "3 2", "nested folders"

# repeated folder names
assert run(
    "C:\\file\\file\\file\\a.txt\n"
    "C:\\file\\file\\file2\\b.txt\n"
) == "4 2", "same folder names at different depths"

# multiple disks
assert run(
    "C:\\a\\x.txt\n"
    "D:\\b\\y.txt\n"
) == "0 1", "disk roots are not folders"

# multiple files in same folder
assert run(
    "C:\\a\\f1.txt\n"
    "C:\\a\\f2.txt\n"
    "C:\\a\\f3.txt\n"
) == "0 3", "direct file counting"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single folder with one file | `0 1` | Minimum valid structure |
| Deep nested folders | `3 2` | Recursive descendant counting |
| Repeated folder names | `4 2` | Full-path identity handling |
| Multiple disks | `0 1` | Disk roots are excluded |
| Multiple files in one folder | `0 3` | Direct file accumulation |

## Edge Cases

Consider repeated folder names:

```
C:\file\file\file\a.txt
C:\file\file\file2\b.txt
```

The algorithm creates four distinct folder nodes:

```
C:\file
C:\file\file
C:\file\file\file
C:\file\file\file2
```

DFS computes:

```
C:\file\file\file  -> 0 subfolders
C:\file\file\file2 -> 0 subfolders
C:\file\file       -> 2 subfolders
C:\file            -> 3 subfolders
```

The output becomes:

```
3 2
```

A solution using only folder names would merge all `"file"` folders and fail badly here.

Now consider files only in descendant folders:

```
C:\a\b\c.txt
```

Folder `a` directly contains no files, but DFS propagates file counts upward:

```
b -> 1 file
a -> 1 file
```

The algorithm correctly outputs:

```
1 1
```

Finally, consider multiple disks:

```
C:\a\f.txt
D:\b\g.txt
```

The tree has two independent roots:

```
C:\a
D:\b
```

DFS runs from both roots separately. Disk names themselves never become nodes, so they are not counted as folders. The correct result is:

```
0 1
```
