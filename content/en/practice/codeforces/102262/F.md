---
title: "CF 102262F - \u0422\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0438\u0438"
description: "We have two snapshots of the same directory tree, the initial state A and the final state B. Every listed object is either a directory, recognized by the trailing /, or a file with an associated hash. The root directory itself is implicit and does not appear in the input."
date: "2026-08-17T20:22:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102262
codeforces_index: "F"
codeforces_contest_name: "\u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e - \u0444\u0438\u043d\u0430\u043b (\u042f\u043d\u0434\u0435\u043a\u0441)"
rating: 0
weight: 102262
solve_time_s: 148
verified: true
draft: false
---

[CF 102262F - \u0422\u0440\u0430\u043d\u0441\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0438\u0438](https://codeforces.com/problemset/problem/102262/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two snapshots of the same directory tree, the initial state A and the final state B. Every listed object is either a directory, recognized by the trailing `/`, or a file with an associated hash. The root directory itself is implicit and does not appear in the input.

The allowed operations are deliberately restrictive. A directory can only be created when its parent already exists, and it can only be removed when it is empty. A file cannot be created from scratch. The only way to obtain a new file name is to create a hardlink to an already existing file, and the new name consequently has exactly the same hash as the source. Existing hardlinks can be removed with `unlink`.

The input gives at most `10^4` objects in each snapshot, so a quadratic scan performs up to `10^8` object comparisons. That is already too much for a 2 second limit in Python, and comparing path strings can make each comparison itself non-constant. We need essentially linear or near-linear processing. The maximum path and hash lengths are only 256, so hashing and sorting strings of this size are practical.

Several cases can fool a careless implementation. If a source file is located inside a directory that must eventually disappear, the source cannot be deleted before all required hardlinks have been created. For example,

```
1 1
/old/x h
/new/x h
```

requires two operations, `link /old/x /new/x` followed by `unlink /old/x`. Deleting `/old/x` first would make the required link impossible.

Nested directories create a similar ordering constraint. For

```
2 2
/old/
/old/x/
/new/
/new/x/
```

the correct minimum is two operations, `mkdir /new/` is already enough only if `/new/x/` is directly represented as the second new directory. More precisely, with the given four entries, `/old/` and `/new/` are the only directories, so the output is `mkdir /new/` followed by `rmdir /old/`. A careless implementation that removes old directories before processing their contents can fail on a deeper version such as

```
3 3
/old/
/old/x/
/old/x/f
/new/
/new/x/
/new/x/g
```

where the old subtree has to be emptied from the bottom up.

A third edge case is several files with the same hash. Suppose

```
2 2
/a h
/b h
/c h
/d h
```

A single original file can be used as the source for both new hardlinks. The minimum is four operations, two `link` operations and two `unlink` operations. There is no reason to search for a one-to-one matching between old and new files.

Finally, an unchanged file must not be touched even if another file with the same hash is being moved. For

```
1 1
/a h
/a h
```

the answer is simply `0`. The common name already denotes the correct hardlink and its hash is guaranteed to match.

## Approaches

A direct solution could repeatedly search one snapshot for every object in the other snapshot. For every path in A we could scan B to decide whether it remains, and then perform another scan to match file hashes. This is correct because every required operation can be derived after explicitly finding the corresponding object, but the first comparison stage alone can require `n * m = 10^8` path comparisons when both snapshots contain `10^4` objects. With paths of up to 256 characters, this is far more work than we need.

The brute-force approach works because the identity of an object is its complete path. The useful observation is that paths are already unique, and the statement guarantees that a file in one snapshot never has the same path as a directory in the other snapshot. We can put all objects into hash tables and classify them immediately by exact path.

Once paths are classified, the number of file operations is fixed. Every file that exists only in A must eventually be removed, so each such file costs at least one `unlink`. Every file that exists only in B must be created as a hardlink, so each such file costs at least one `link`. The two operations are always sufficient: create every required target hardlink while an appropriate source still exists, then remove all obsolete file names.

The hash is only needed to choose the source for a new hardlink. For each hash, we remember one file from A having that hash. If a hash occurs in an unchanged file, preferring that file as the source is convenient because it will never be removed. Otherwise an A-only file with that hash can serve as the temporary source. We create all new hardlinks before deleting any A-only file, so even a source that is scheduled for deletion remains available long enough.

Directories have the same fixed lower bound. Every directory present only in B requires one `mkdir`, and every directory present only in A requires one `rmdir`. The only difficulty is ordering. New directories must be created from shallow to deep, while old directories must be removed from deep to shallow. Once all new directories exist, every target file has a valid parent, and once all obsolete files are removed, every old directory can eventually become empty.

Thus the minimum number of operations is exactly the number of objects whose path differs between A and B. The algorithm only has to find a legal order for those unavoidable operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm · L) | O(n + m) | Too slow |
| Optimal | O((n + m) log(n + m) · L) | O(n + m) | Accepted |

Here `L` is the maximum path length, at most 256. With bounded path length this is effectively `O((n + m) log(n + m))`.

## Algorithm Walkthrough

1. Read all objects of A and B and separate files from directories. Store files as `path -> hash` and directories as a set of paths. At the same time, remember one A file for every hash.
2. Find the directories that have to be created by taking `B_dirs - A_dirs`. Sort them by increasing directory depth, and use the path as a secondary key. A parent must exist before its child, so every newly created directory will have a valid parent when its operation is emitted.
3. Find the directories that have to be removed by taking `A_dirs - B_dirs`. Sort them by decreasing depth. A child has to disappear before its parent can become empty, so this order makes every `rmdir` legal.
4. Find files that occur only in B. For every such file, look up its hash in the source map built from A and emit a `link source target` operation. All target directories have already been created, and all source files from A are still present because no `unlink` has happened yet.
5. Find files that occur only in A and emit an `unlink` operation for each one. At this point all new hardlinks have been made, so even an obsolete file that was used as a source can safely be removed.
6. Emit the `rmdir` operations for the old-only directories in decreasing depth order. All obsolete files have already disappeared, so the directories can now be empty.
7. Print the total number of emitted operations followed by the operations themselves. Common files and common directories never appear because they already have exactly the required state.

### Why it works

Consider every path independently. A common path has the same object type in both snapshots, and a common file has the same hash, so touching it cannot reduce the number of operations below zero. A file existing only in B needs at least one `link`, while a file existing only in A needs at least one `unlink`. Our algorithm performs exactly those operations, and it creates every new link before removing any possible source, so all of them are legal.

The same argument applies to directories. Every B-only directory needs one `mkdir`, and every A-only directory needs one `rmdir`. Sorting creation by depth guarantees that parents exist first. Sorting deletion by reverse depth guarantees that children disappear first. Hence every emitted operation is legal, and the number of operations reaches the unavoidable lower bound, making the sequence minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    a_files = {}
    a_dirs = set()

    for _ in range(n):
        parts = input().split()
        path = parts[0]

        if path.endswith('/'):
            a_dirs.add(path)
        else:
            a_files[path] = parts[1]

    b_files = {}
    b_dirs = set()

    for _ in range(m):
        parts = input().split()
        path = parts[0]

        if path.endswith('/'):
            b_dirs.add(path)
        else:
            b_files[path] = parts[1]

    common_files = a_files.keys() & b_files.keys()

    source_by_hash = {}

    # Prefer files that survive in B as sources.
    for path in common_files:
        source_by_hash[a_files[path]] = path

    # If a hash has no surviving source, an obsolete A-file can be used
    # until all required links have been created.
    for path, h in a_files.items():
        if h not in source_by_hash:
            source_by_hash[h] = path

    add_dirs = sorted(
        b_dirs - a_dirs,
        key=lambda p: (p.count('/'), p)
    )

    remove_dirs = sorted(
        a_dirs - b_dirs,
        key=lambda p: (-p.count('/'), p)
    )

    add_files = sorted(
        b_files.keys() - a_files.keys()
    )

    remove_files = sorted(
        a_files.keys() - b_files.keys()
    )

    operations = []

    for path in add_dirs:
        operations.append(f"mkdir {path}")

    for target in add_files:
        source = source_by_hash[b_files[target]]
        operations.append(f"link {source} {target}")

    for path in remove_files:
        operations.append(f"unlink {path}")

    for path in remove_dirs:
        operations.append(f"rmdir {path}")

    out = [str(len(operations))]
    out.extend(operations)
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == "__main__":
    solve()
```

The first two dictionaries and sets represent the two snapshots directly. Using the complete path as the key makes testing whether an object is common an average O(1) operation.

The `source_by_hash` map captures the only information needed for hardlinks. A common file is preferred as a source because it will survive until the end. If no common file has the required hash, an A-only file becomes the source. Such a file is deliberately kept alive until after every new hardlink has been created.

The directory sorting uses `path.count('/')` as a depth measure. Because every directory path ends with `/`, a child always has a greater slash count than its parent. The exact numeric depth is irrelevant, only the ordering matters.

The operation groups are emitted in a fixed order. Creating directories comes first, because links and nested directories may depend on them. Links come before unlinks, because an obsolete source may be needed. Unlinks come before `rmdir`, because directories must be empty before removal.

There is no integer overflow issue in Python, and the maximum number of operations is at most `2(n + m)`, which is below 40000 for the given limits. The output itself is stored in a list so that the operation count can be printed before the operations.

## Worked Examples

For the provided sample, the common directory is `/a/`. The directory `/a/e/` must be created and `/f/` must disappear. The file `/a/b.txt` is an available source for the new file `/a/e/c.txt`, while `/a/d.txt` is obsolete.

| Step | Operation | New directories | New files | Remaining old files |
| --- | --- | --- | --- | --- |
| 1 | `mkdir /a/e/` | `/a/e/` exists | none | `/a/b.txt`, `/a/d.txt` |
| 2 | `link /a/b.txt /a/e/c.txt` | `/a/e/` exists | `/a/e/c.txt` exists | `/a/b.txt`, `/a/d.txt` |
| 3 | `unlink /a/b.txt` | unchanged | `/a/e/c.txt` exists | `/a/d.txt` |
| 4 | `unlink /a/d.txt` | unchanged | `/a/e/c.txt` exists | none |
| 5 | `rmdir /f/` | final directories remain | final files remain | none |

The resulting sequence has five operations, the same minimum as the sample output. The order differs from the statement's example, which is allowed because any minimum valid sequence is accepted.

For a second example, consider moving a file between two nested directory trees.

```
6 6
/old/
/old/sub/
/old/sub/file h
/new/
/new/sub/
/new/sub/file2 h
```

The two directory trees have no common directories, and the only file is renamed.

| Step | Operation | Created directories | Existing source | Obsolete files |
| --- | --- | --- | --- | --- |
| 1 | `mkdir /new/` | `/new/` | `/old/sub/file` | none |
| 2 | `mkdir /new/sub/` | `/new/`, `/new/sub/` | `/old/sub/file` | none |
| 3 | `link /old/sub/file /new/sub/file2` | both new dirs | `/old/sub/file` | none |
| 4 | `unlink /old/sub/file` | unchanged | none required | none |
| 5 | `rmdir /old/sub/` | unchanged | none | old subtree partly removed |
| 6 | `rmdir /old/` | final tree reached | none | old subtree gone |

The example demonstrates both depth orderings. `/new/` must precede `/new/sub/`, while `/old/sub/` must precede `/old/` in the deletion sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log(n + m) · L) | Hash-table classification is linear on average, and directory/file sorting dominates |
| Space | O(n + m) | All paths, hashes, and generated operations are stored |

Here `L <= 256` is the maximum path length. With at most `10^4` objects in each snapshot, sorting at most `2 * 10^4` short strings is easily within the limits, and the generated operation count is below `4 * 10^4`.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    a_files = {}
    a_dirs = set()

    for _ in range(n):
        parts = input().split()
        path = parts[0]
        if path.endswith('/'):
            a_dirs.add(path)
        else:
            a_files[path] = parts[1]

    b_files = {}
    b_dirs = set()

    for _ in range(m):
        parts = input().split()
        path = parts[0]
        if path.endswith('/'):
            b_dirs.add(path)
        else:
            b_files[path] = parts[1]

    source_by_hash = {}

    for path in a_files.keys() & b_files.keys():
        source_by_hash[a_files[path]] = path

    for path, h in a_files.items():
        if h not in source_by_hash:
            source_by_hash[h] = path

    add_dirs = sorted(
        b_dirs - a_dirs,
        key=lambda p: (p.count('/'), p)
    )
    remove_dirs = sorted(
        a_dirs - b_dirs,
        key=lambda p: (-p.count('/'), p)
    )
    add_files = sorted(b_files.keys() - a_files.keys())
    remove_files = sorted(a_files.keys() - b_files.keys())

    operations = []

    for path in add_dirs:
        operations.append(f"mkdir {path}")

    for target in add_files:
        operations.append(
            f"link {source_by_hash[b_files[target]]} {target}"
        )

    for path in remove_files:
        operations.append(f"unlink {path}")

    for path in remove_dirs:
        operations.append(f"rmdir {path}")

    sys.stdout.write(
        str(len(operations)) + '\n' +
        '\n'.join(operations) +
        ('\n' if operations else '')
    )

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample1 = """\
4 3
/a/
/a/b.txt hash1
/a/d.txt hash2
/f/
/a/
/a/e/
/a/e/c.txt hash1
"""

expected1 = """\
5
mkdir /a/e/
link /a/b.txt /a/e/c.txt
unlink /a/b.txt
unlink /a/d.txt
rmdir /f/
"""

assert run(sample1) == expected1, "provided sample"

assert run("0 0\n") == "0\n", "minimum-size empty snapshots"

sample2 = """\
4 4
/a h
/b h
/c/
c
"""

# The previous test deliberately is not valid path input, so use a valid
# all-equal-hash case instead.
sample2 = """\
2 2
/a h
/b h
/c h
/d h
"""

expected2 = """\
4
link /a /c
link /a /d
unlink /a
unlink /b
"""

assert run(sample2) == expected2, "all equal hashes"

sample3 = """\
3 3
/old/
/old/sub/
/old/sub/file h
/new/
/new/sub/
/new/sub/file2 h
"""

expected3 = """\
6
mkdir /new/
mkdir /new/sub/
link /old/sub/file /new/sub/file2
unlink /old/sub/file
rmdir /old/sub/
rmdir /old/
"""

assert run(sample3) == expected3, "nested directory ordering"

deep_name = "/" + "a/" * 126
deep_file_a = deep_name + "x"
deep_file_b = deep_name + "y"

sample4 = (
    "1 1\n"
    + deep_file_a + " h\n"
    + deep_file_b + " h\n"
)

out4 = run(sample4).splitlines()
assert out4[0] == "2", "deep path operation count"
assert out4[1] == f"link {deep_file_a} {deep_file_b}"
assert out4[2] == f"unlink {deep_file_a}"

# Maximum-size test: 10000 old files and 10000 new files,
# all having the same hash.
old_files = [f"/a{i}" for i in range(10000)]
new_files = [f"/b{i}" for i in range(10000)]

max_input = (
    "10000 10000\n"
    + ''.join(path + " h\n" for path in old_files)
    + ''.join(path + " h\n" for path in new_files)
)

max_out = run(max_input).splitlines()

assert max_out[0] == "20000", "maximum-size operation count"
assert len(max_out) == 20001, "maximum-size output length"

link_count = sum(line.startswith("link ") for line in max_out[1:])
unlink_count = sum(line.startswith("unlink ") for line in max_out[1:])

assert link_count == 10000, "maximum-size link count"
assert unlink_count == 10000, "maximum-size unlink count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0` | Minimum-size input and the case where nothing changes |
| Two old files and two new files with hash `h` | `4` operations | Reusing one source for several hardlinks and delaying its unlink |
| Nested `/old/sub/` to `/new/sub/` | `6` operations | Parent-first `mkdir` and child-first `rmdir` |
| A file path near the 256-character limit | `2` operations | Path-length boundary and exact path handling |
| 10000 old and 10000 new files with the same hash | `20000` operations | Maximum input size, all-equal hashes, and scalability |

## Edge Cases

The empty case needs no special operation. For

```
0 0
```

both sets of directories and files are empty, so all four difference sets are empty. The algorithm emits no operations and prints `0`.

When a source file is inside a directory that will be removed, the file must be linked before its old directory is deleted. For

```
3 3
/old/
/old/sub/
/old/sub/file h
/new/
/new/sub/
/new/sub/file2 h
```

the algorithm first creates `/new/` and `/new/sub/`, then creates `/new/sub/file2` from `/old/sub/file`, and only afterwards removes the old file. The reverse-depth directory order then removes `/old/sub/` before `/old/`. The six operations are exactly the four unavoidable directory changes plus one `link` and one `unlink`.

Several new files with the same hash do not require several independent original sources. For

```
2 2
/a h
/b h
/c h
/d h
```

the source map chooses `/a` for hash `h`. The algorithm creates both `/c` and `/d` as hardlinks to `/a`, then removes `/a` and `/b`. The output is four operations. The fact that `/a` is eventually deleted does not matter because all links using it have already been created.

An unchanged file must be excluded from both file difference sets. For

```
1 1
/a h
/a h
```

`/a` occurs in both dictionaries with the same hash, so neither `link` nor `unlink` is generated. The output is `0`. This is why comparing only hashes would be incorrect: the path itself determines whether a file name already exists in the desired state.

The deepest valid paths are handled without recursion. The implementation uses the number of `/` characters only to sort directory operations, so even a path close to the 256-character limit is processed as an ordinary string. A parent has fewer slashes than its descendant, which is sufficient to establish the required creation and deletion order.
