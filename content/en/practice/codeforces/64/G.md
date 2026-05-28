---
title: "CF 64G - Path Canonization"
description: "We are given an absolute Unix-style path. The path is split into components by /, and every component represents either a normal directory or file name, \".\", or \"..\". A normal name means “go into this directory or file”. The component \"."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 64
codeforces_index: "G"
codeforces_contest_name: "Unknown Language Round 1"
rating: 2200
weight: 64
solve_time_s: 102
verified: true
draft: false
---

[CF 64G - Path Canonization](https://codeforces.com/problemset/problem/64/G)

**Rating:** 2200  
**Tags:** *special  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an absolute Unix-style path. The path is split into components by `/`, and every component represents either a normal directory or file name, `"."`, or `".."`.

A normal name means “go into this directory or file”.

The component `"."` means “stay in the current directory”, so it changes nothing.

The component `".."` means “move to the parent directory”.

The task is to simplify the path so that the final result contains no `"."` or `".."` components. If at some point the path tries to move above the root directory, the path is invalid and we must print `-1`.

The path length is at most 1000 characters, which is very small. Even quadratic solutions would probably pass comfortably, but the structure of the problem naturally leads to a linear-time solution. Since every path component is processed independently and only affects the current directory stack, we can solve the problem in one left-to-right pass.

The dangerous cases are not about performance, they are about correctly interpreting special components.

Consider the input:

```
/../../a
```

The first `".."` already tries to leave the root directory. The correct output is:

```
-1
```

A careless implementation might silently ignore extra `".."` operations and incorrectly return `/a`.

Another subtle case is distinguishing `"."` and `".."` from ordinary names containing dots.

For example:

```
/.../..hidden/./x
```

The components `"..."` and `"..hidden"` are ordinary names, not special commands. The correct simplified path is:

```
/.../..hidden/x
```

A buggy implementation that checks only whether a component contains dots would incorrectly treat them as parent-directory operations.

The root directory itself also needs careful handling.

```
/
```

The result must remain exactly `/`. Reconstructing the answer by blindly joining components can accidentally produce an empty string instead.

## Approaches

A brute-force approach would repeatedly search the path for occurrences of `"."` and `".."`, rewrite the string, and continue until no special components remain.

For example, if we see `/a/b/../c`, we can rewrite it into `/a/c`. If we see `/./`, we remove it. This method is conceptually simple because it directly simulates path simplification on the string itself.

The problem is that every rewrite shifts characters in the string. If the path contains many nested directories and many `".."` operations, each rewrite can cost linear time, and we may perform linear many rewrites. With a path length of `n`, this can degrade into `O(n²)` operations.

The key observation is that path canonicalization depends only on the sequence of directory components that are currently active. When we enter a directory, we append it to the current path. When we encounter `".."`, we remove the most recent directory. This behavior is exactly a stack.

That changes the problem from “rewrite strings repeatedly” into “process components once from left to right”.

For each component:

If it is `"."`, we ignore it.

If it is `".."`, we pop one directory from the stack. If the stack is already empty, the path is invalid.

Otherwise, the component is an ordinary name, so we push it onto the stack.

At the end, the stack already contains the canonical path components in order. We simply join them with `/`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted but inefficient |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input path as a string.
2. Split the path by `/`.

Since the path always starts with `/`, the first split component will be an empty string. We simply ignore empty components during processing.
3. Create an empty stack.

The stack represents the current canonical path from root to the current directory.
4. Process each component from left to right.

This matches the real behavior of navigating through a filesystem.
5. If the component is empty or `"."`, skip it.

Empty components appear because the path starts with `/`. The component `"."` means “stay here”, so it changes nothing.
6. If the component is `".."`, try to remove the last directory from the stack.

If the stack is empty, we are already at the root directory, so moving upward is impossible. Print `-1` and stop.
7. Otherwise, the component is a normal directory or file name.

Push it onto the stack.
8. After processing all components, reconstruct the canonical path.

If the stack is empty, the canonical path is simply `/`.

Otherwise, join all stack elements with `/` and prepend one leading slash.

### Why it works

After processing the first `k` components, the stack always represents the exact canonical path corresponding to those `k` components.

Pushing a normal name matches entering a directory. Popping on `".."` matches returning to the parent directory. Ignoring `"."` matches staying in the same directory.

Because every operation updates the stack exactly as the filesystem semantics require, the final stack state is the unique canonical version of the path. The only invalid situation is attempting to pop from an empty stack, which corresponds precisely to moving above the root directory.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    path = input().strip()

    stack = []

    for part in path.split('/'):
        if part == '' or part == '.':
            continue

        if part == '..':
            if not stack:
                print(-1)
                return
            stack.pop()
        else:
            stack.append(part)

    if not stack:
        print('/')
    else:
        print('/' + '/'.join(stack))

solve()
```

The solution follows the stack-based simulation directly.

The call to `split('/')` converts the path into individual components. Because the input path always starts with `/`, the first component becomes an empty string. We ignore such components.

The stack stores the currently active directories. Every ordinary name is appended. Every `".."` removes the most recent directory.

The most important implementation detail is checking whether the stack is empty before calling `pop()`. Forgetting this check would either crash or incorrectly allow movement above the root directory.

Another subtle point is reconstructing the final answer. If the stack becomes empty, the correct canonical path is `/`, not an empty string. That special case must be handled separately.

The condition:

```
if part == '' or part == '.':
```

is also important. Only exact matches to `"."` and `".."` are special. Strings like `"..."` or `"..a"` must remain ordinary path names.

## Worked Examples

### Example 1

Input:

```
/usr/share/mysql/../tomcat6/conf/server.xml
```

| Component | Action | Stack |
| --- | --- | --- |
| `usr` | push | `["usr"]` |
| `share` | push | `["usr", "share"]` |
| `mysql` | push | `["usr", "share", "mysql"]` |
| `..` | pop | `["usr", "share"]` |
| `tomcat6` | push | `["usr", "share", "tomcat6"]` |
| `conf` | push | `["usr", "share", "tomcat6", "conf"]` |
| `server.xml` | push | `["usr", "share", "tomcat6", "conf", "server.xml"]` |

Final output:

```
/usr/share/tomcat6/conf/server.xml
```

This trace demonstrates the core invariant: the stack always stores the canonical path after processing the current prefix of components.

### Example 2

Input:

```
/../../a
```

| Component | Action | Stack |
| --- | --- | --- |
| `..` | invalid pop | `[]` |

Final output:

```
-1
```

This example exercises the only failure condition in the problem. The algorithm immediately detects an attempt to move above the root directory.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each path component is processed once |
| Space | O(n) | The stack may store all components |

Here, `n` is the length of the input string. Since the maximum path length is only 1000, the linear solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    path = input().strip()

    stack = []

    for part in path.split('/'):
        if part == '' or part == '.':
            continue

        if part == '..':
            if not stack:
                print(-1)
                return
            stack.pop()
        else:
            stack.append(part)

    if not stack:
        print('/')
    else:
        print('/' + '/'.join(stack))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("/usr/share/mysql/../tomcat6/conf/server.xml\n") == \
       "/usr/share/tomcat6/conf/server.xml", "sample 1"

# minimum-size input
assert run("/\n") == "/", "root directory"

# invalid upward movement
assert run("/../../a\n") == "-1", "cannot move above root"

# only current-directory operations
assert run("/./././x\n") == "/x", "ignore current directory"

# names containing dots are ordinary names
assert run("/.../..hidden/./x\n") == "/.../..hidden/x", \
       "dot-containing names"

# returns to root exactly
assert run("/a/b/../..\n") == "/", "back to root"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `/` | `/` | Correct handling of root |
| `/../../a` | `-1` | Detecting invalid upward movement |
| `/./././x` | `/x` | Ignoring `"."` components |
| `/.../..hidden/./x` | `/.../..hidden/x` | Distinguishing special names from ordinary names |
| `/a/b/../..` | `/` | Correct reconstruction of empty stack |

## Edge Cases

Consider the invalid upward traversal case:

```
/../../a
```

The algorithm starts with an empty stack. The first component is `".."`. Since the stack is empty, there is no parent directory to return to. The algorithm immediately prints `-1`.

This matches the filesystem semantics exactly. Ignoring this operation would incorrectly allow paths outside the root.

Now consider names containing dots:

```
/.../..hidden/./x
```

The components are:

```
"...", "..hidden", ".", "x"
```

The algorithm only treats exact matches to `"."` and `".."` as special. So `"..."` and `"..hidden"` are pushed normally onto the stack. The `"."` component is ignored, and `"x"` is appended.

The final stack becomes:

```
["...", "..hidden", "x"]
```

which reconstructs into:

```
/../..hidden/x
```

Finally, consider a path that collapses completely back to root:

```
/a/b/../..
```

The stack evolves as:

```
["a"]
["a", "b"]
["a"]
[]
```

At the end, the stack is empty. The algorithm prints `/` instead of an empty string, which is the correct canonical representation of the root directory.
