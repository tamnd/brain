---
title: "CF 158C - Cd and pwd commands"
description: "We need to simulate a tiny shell that supports only two commands. The command cd path changes the current directory. The path may be absolute, meaning it starts from the root /, or relative, meaning it starts from the current directory. Inside a path, the token .."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 158
codeforces_index: "C"
codeforces_contest_name: "VK Cup 2012 Qualification Round 1"
rating: 1400
weight: 158
solve_time_s: 105
verified: true
draft: false
---

[CF 158C - Cd and pwd commands](https://codeforces.com/problemset/problem/158/C)

**Rating:** 1400  
**Tags:** *special, data structures, implementation  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to simulate a tiny shell that supports only two commands.

The command `cd path` changes the current directory. The path may be absolute, meaning it starts from the root `/`, or relative, meaning it starts from the current directory. Inside a path, the token `..` means “go to the parent directory”.

The command `pwd` prints the full absolute path of the current directory, always ending with a trailing slash.

The filesystem itself does not need to be constructed as a tree. The problem guarantees that every referenced directory exists, and directory names are just labels. What actually matters is the sequence of directory names from the root to the current location.

The number of commands is at most 50, and each path length is at most 200 characters. These limits are extremely small. Even rebuilding paths repeatedly or splitting strings many times is completely safe. Any solution close to linear in the total input size will pass comfortably.

The tricky part is handling path semantics correctly.

Consider this input:

```
3
cd /a/b
cd ..
pwd
```

The correct output is:

```
/a/
```

A careless implementation might remove the last character instead of the last directory and accidentally produce `/a/b`.

Another common mistake happens with absolute paths.

```
3
cd /a/b
cd /x
pwd
```

The correct output is:

```
/x/
```

When the path starts with `/`, we must discard the old current directory completely. If we incorrectly append the new path onto the existing one, we would get `/a/b/x/`.

Relative paths with mixed directory names and `..` also cause bugs:

```
2
cd a/b/../c
pwd
```

The correct output is:

```
/a/c/
```

The path must be processed component by component in order. We cannot simply remove every `..` blindly because each one only affects the immediately preceding directory.

The root directory is another edge case.

```
3
cd /
pwd
cd ..
```

The output is:

```text`

/

```

The statement guarantees we never move above the root, but our implementation still needs to keep the root represented correctly as an empty path stack or equivalent structure.

## Approaches

The most direct idea is to treat the current directory as a string and literally manipulate it every time a command appears.

For a `cd`, we could concatenate strings, repeatedly search for slashes, manually erase parent directories when seeing `..`, and rebuild the result. This works because paths are short. Even if every command processes a 200-character string several times, the total work remains tiny.

The weakness of this approach is not performance, but complexity. String slicing and manual parsing become error-prone very quickly. Handling cases like `/`, trailing slashes, or consecutive parent operations becomes awkward.

The cleaner observation is that a filesystem path naturally behaves like a stack.

For example:

```text
/home/vasya/docs
```

can be represented as:

```
["home", "vasya", "docs"]
```

Entering a directory means pushing onto the stack. Going to the parent directory means popping from the stack. Printing the current path means joining the stack with slashes.

This matches the semantics of the shell exactly.

When processing a `cd` command:

If the path starts with `/`, we reset the stack because absolute paths begin from the root.

Then we split the path by `/` and process each component.

If the component is empty, we ignore it. This mainly happens because absolute paths begin with `/`.

If the component is `..`, we pop one directory.

Otherwise, we push the directory name.

The brute-force string manipulation solution is acceptable under these constraints, but the stack representation is simpler, safer, and mirrors the actual filesystem logic directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force string manipulation | O(n × L²) | O(L) | Accepted |
| Stack-based simulation | O(n × L) | O(L) | Accepted |

Here, `L` is the maximum path length.

## Algorithm Walkthrough

1. Store the current directory as a list of directory names.

For example, `/home/vasya/` becomes `["home", "vasya"]`.
2. Read each command one by one.

The shell state changes sequentially, so processing commands in order exactly matches the problem behavior.
3. If the command is `pwd`, print the current path.

Join all directory names with `/`, prepend a leading slash, and append a trailing slash.

If the stack is empty, the result is simply `/`.
4. If the command is `cd path`, first determine whether the path is absolute or relative.

If the path starts with `/`, clear the current stack because absolute paths begin from the root.
5. Split the path using `/` as the separator.

This converts something like `vasya/../petya` into components we can process independently.
6. Process each component from left to right.

If the component is empty, ignore it.

This occurs for leading slashes in absolute paths.
7. If the component is `..`, remove the last directory from the stack.

This simulates moving to the parent directory.
8. Otherwise, append the component to the stack.

This simulates entering a child directory.

### Why it works

The stack always stores the exact sequence of directories from the root to the current location.

Every valid filesystem movement changes only the end of this sequence. Entering a directory adds one element, while moving to the parent removes one element. Absolute paths restart the sequence from the root.

Because each path component is processed in the same order the shell would interpret it, the stack after processing a command always matches the true current directory.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    current = []
    
    for _ in range(n):
        parts = input().strip().split()
        
        if parts[0] == "pwd":
            print("/" + "/".join(current) + "/")
        else:
            path = parts[1]
            
            if path[0] == "/":
                current = []
            
            components = path.split("/")
            
            for comp in components:
                if comp == "" or comp == ".":
                    continue
                
                if comp == "..":
                    current.pop()
                else:
                    current.append(comp)

solve()
```

The solution stores the current path as a list named `current`. Each element is one directory name.

For `pwd`, the implementation reconstructs the absolute path by joining the directory names with `/`. The expression:

```
"/" + "/".join(current) + "/"
```

works even for the root directory. If `current` is empty, `"".join(current)` becomes an empty string, so the final result is simply `//`. Since the format already includes both leading and trailing slashes, this actually produces `//`, which is incorrect for root.

To avoid this subtle bug, many people prefer a conditional approach. However, in this specific implementation, the empty join produces an empty middle section, resulting in exactly `//`. We should correct this.

The proper implementation is:

```python
if not current:
    print("/")
else:
    print("/" + "/".join(current) + "/")
```

Here is the corrected final version:

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    current = []
    
    for _ in range(n):
        parts = input().strip().split()
        
        if parts[0] == "pwd":
            if not current:
                print("/")
            else:
                print("/" + "/".join(current) + "/")
        else:
            path = parts[1]
            
            if path[0] == "/":
                current = []
            
            for comp in path.split("/"):
                if comp == "":
                    continue
                
                if comp == "..":
                    current.pop()
                else:
                    current.append(comp)

solve()
```

The absolute-path reset is another subtle point. We must clear the stack before processing components. If we clear it afterward, relative navigation inside the same path would behave incorrectly.

The problem guarantees we never move above the root, so `current.pop()` is always safe.

## Worked Examples

### Example 1

Input:

```
7
pwd
cd /home/vasya
pwd
cd ..
pwd
cd vasya/../petya
pwd
```

| Command | Components Processed | Current Stack | Output |
| --- | --- | --- | --- |
| pwd | - | [] | / |
| cd /home/vasya | home, vasya | [home, vasya] | - |
| pwd | - | [home, vasya] | /home/vasya/ |
| cd .. | .. | [home] | - |
| pwd | - | [home] | /home/ |
| cd vasya/../petya | vasya, .., petya | [home, petya] | - |
| pwd | - | [home, petya] | /home/petya/ |

This trace shows why the stack model is natural. Every directory entry pushes once, and every `..` removes exactly the most recent directory.

### Example 2

Input:

```
6
cd /a/b/c
pwd
cd ../../x
pwd
cd /z
pwd
```

| Command | Components Processed | Current Stack | Output |
| --- | --- | --- | --- |
| cd /a/b/c | a, b, c | [a, b, c] | - |
| pwd | - | [a, b, c] | /a/b/c/ |
| cd ../../x | .., .., x | [a, x] | - |
| pwd | - | [a, x] | /a/x/ |
| cd /z | z | [z] | - |
| pwd | - | [z] | /z/ |

This example demonstrates the difference between relative and absolute paths. The command `../../x` starts from the current directory, while `/z` discards the previous location entirely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × L) | Each command processes its path linearly |
| Space | O(L) | The stack stores at most all directories in the current path |

The limits are extremely small, so this solution runs comfortably within the time and memory constraints. Even in the worst case, the total number of processed characters is only a few thousand.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    
    out = io.StringIO()
    sys.stdout = out
    
    current = []
    
    n = int(input())
    
    for _ in range(n):
        parts = input().strip().split()
        
        if parts[0] == "pwd":
            if not current:
                print("/")
            else:
                print("/" + "/".join(current) + "/")
        else:
            path = parts[1]
            
            if path[0] == "/":
                current = []
            
            for comp in path.split("/"):
                if comp == "":
                    continue
                
                if comp == "..":
                    current.pop()
                else:
                    current.append(comp)
    
    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run(
"""7
pwd
cd /home/vasya
pwd
cd ..
pwd
cd vasya/../petya
pwd
"""
) == """/
/home/vasya/
/home/
/home/petya/
"""

# minimum case
assert run(
"""1
pwd
"""
) == """/
"""

# absolute path reset
assert run(
"""4
cd /a/b
cd /x
pwd
pwd
"""
) == """/x/
/x/
"""

# relative navigation
assert run(
"""4
cd /a/b/c
cd ../../d
pwd
pwd
"""
) == """/a/d/
/a/d/
"""

# repeated parent operations
assert run(
"""5
cd /a/b/c
cd ../..
pwd
pwd
"""
) == """/a/
/a/
"""

# mixed navigation
assert run(
"""5
cd /a
cd b/../c
pwd
cd ..
pwd
"""
) == """/a/c/
/a/
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 pwd` | `/` | Correct handling of root |
| `/a/b` then `/x` | `/x/` | Absolute paths reset state |
| `../../d` | `/a/d/` | Multiple parent traversals |
| `../..` from deep path | `/a/` | Consecutive pops |
| `b/../c` | `/a/c/` | Mixed relative navigation |

## Edge Cases

Consider the case where the current directory is replaced by an absolute path.

Input:

```
4
cd /a/b
cd /x/y
pwd
pwd
```

Execution:

After `cd /a/b`, the stack becomes `[a, b]`.

The next command starts with `/`, so the algorithm clears the stack before processing components. Then it appends `x` and `y`.

The final stack is `[x, y]`, producing:

```
/x/y/
```

If we forgot to clear the stack, we would incorrectly get `/a/b/x/y/`.

Now consider repeated parent navigation.

Input:

```
3
cd /a/b/c
cd ../..
pwd
```

The stack after the first command is `[a, b, c]`.

Processing `..` pops `c`.

Processing the second `..` pops `b`.

The remaining stack is `[a]`, so the output is:

```
/a/
```

This confirms that each `..` affects only the immediately previous directory.

Finally, consider mixed relative movement.

Input:

```
2
cd a/b/../c
pwd
```

The algorithm processes components in order:

`a` → `[a]`

`b` → `[a, b]`

`..` → `[a]`

`c` → `[a, c]`

The printed path becomes:

```
/a/c/
```

This demonstrates why component-by-component simulation is necessary. A shortcut string replacement approach can easily mishandle nested parent references.
