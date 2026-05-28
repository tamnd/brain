---
title: "CF 20A - BerOS file system"
description: "We are given a filesystem path as a string. In this operating system, multiple consecutive '/' characters are treated ex"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 20
codeforces_index: "A"
codeforces_contest_name: "Codeforces Alpha Round 20 (Codeforces format)"
rating: 1700
weight: 20
solve_time_s: 80
verified: true
draft: false
---

[CF 20A - BerOS file system](https://codeforces.com/problemset/problem/20/A)

**Rating:** 1700  
**Tags:** implementation  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a filesystem path as a string. In this operating system, multiple consecutive `'/'` characters are treated exactly the same as a single `'/'`. That means paths like `///home//user///docs` and `/home/user/docs` refer to the same location.

The task is to convert the path into its normalized form. A normalized path keeps only one `'/'` between directory names. The only exception is the root directory itself, which must remain exactly `"/"`.

The input length is at most 100 characters, which is extremely small. Even quadratic solutions would run comfortably within the limits. A linear scan is still the cleanest approach because the problem naturally asks us to process characters one by one and decide whether each slash should be kept or discarded.

The tricky part is handling trailing slashes correctly. A path like:

```
/usr/local///
```

must become:

```
/usr/local
```

A careless implementation that only compresses consecutive slashes would incorrectly produce:

```
/usr/local/
```

Another edge case is the root directory itself. For example:

```
////
```

should normalize to:

```
/
```

If we blindly remove all repeated slashes and then remove trailing slashes, we could accidentally produce an empty string instead of the required root path.

One more subtle case is when slashes appear in the middle:

```
/a////b///c
```

The correct output is:

```
/a/b/c
```

Each group of consecutive slashes must collapse into exactly one slash, not zero.

## Approaches

A brute-force strategy would repeatedly search the string for occurrences of `"//"` and replace them with `"/"` until no double slashes remain. After that, we could remove a trailing slash if the resulting path has length greater than one.

This works because every replacement shortens the string, and eventually no consecutive slashes remain. With a string length of only 100, even repeated replacements are fast enough.

The weakness is that repeated string reconstruction is inefficient in principle. Suppose the string length were much larger, say `10^5`. Each replacement could take linear time because strings are immutable, and we might perform many replacements. In the worst case, something like:

```
//////////////////////////////////////////////////
```

would repeatedly shrink one character at a time, leading to quadratic behavior.

The better observation is that we never actually need to revisit earlier characters. While scanning from left to right, the only thing that matters is whether the previous character we kept was `'/'`.

If the current character is not `'/'`, we always keep it.

If the current character is `'/'`, we keep it only when the previously kept character was not `'/'`.

This turns the problem into a single linear pass over the string.

After building the compressed path, we still need to handle trailing slashes. Any trailing slash should be removed unless the entire path is just `"/"`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input path string.
2. Create an empty list that will store the normalized characters.
3. Iterate through the path character by character.
4. If the current character is not `'/'`, append it directly to the result.

Directory names and letters must always remain unchanged.
5. If the current character is `'/'`, check the last character already stored in the result.

If the result is empty or the last stored character is not `'/'`, append the slash.

Otherwise skip it, because consecutive slashes are equivalent to one slash.
6. Convert the collected characters back into a string.
7. Remove trailing slashes while the string length is greater than one.

The condition `length > 1` protects the root directory path `"/"` from becoming empty.
8. Print the final normalized path.

### Why it works

The algorithm maintains a simple invariant during the scan: the partially built result never contains two consecutive slashes.

Whenever we encounter a slash, we append it only if the previous kept character was not a slash. That guarantees every maximal block of slashes in the original string becomes exactly one slash in the result.

All non-slash characters are copied unchanged and in order, so directory names remain intact.

Finally, removing trailing slashes while keeping at least one character guarantees that paths like `"/usr///"` become `"/usr"` while paths representing the root directory remain exactly `"/"`.

## Python Solution

```python
import sys
input = sys.stdin.readline

path = input().strip()

result = []

for ch in path:
    if ch != '/':
        result.append(ch)
    else:
        if not result or result[-1] != '/':
            result.append('/')

ans = ''.join(result)

while len(ans) > 1 and ans[-1] == '/':
    ans = ans[:-1]

print(ans)
```

The first part of the code performs the linear scan. The `result` list acts as a mutable string builder, which is more efficient than repeatedly concatenating strings.

The condition:

```
if not result or result[-1] != '/':
```

is the key step. It decides whether the current slash begins a new separator block or belongs to an already existing one.

Using a list instead of string concatenation avoids unnecessary rebuilding of intermediate strings. With such a small constraint this is not mandatory, but it is good competitive-programming practice.

The final `while` loop removes trailing slashes carefully:

```
while len(ans) > 1 and ans[-1] == '/':
```

The `len(ans) > 1` condition is critical. Without it, the input:

```
////
```

would incorrectly become an empty string instead of `"/"`.

## Worked Examples

### Example 1

Input:

```
//usr///local//nginx/sbin
```

| Current character | Result before | Action | Result after |
| --- | --- | --- | --- |
| `/` | `""` | keep slash | `/` |
| `/` | `/` | skip slash | `/` |
| `u` | `/` | keep char | `/u` |
| `s` | `/u` | keep char | `/us` |
| `r` | `/us` | keep char | `/usr` |
| `/` | `/usr` | keep slash | `/usr/` |
| `/` | `/usr/` | skip slash | `/usr/` |
| `/` | `/usr/` | skip slash | `/usr/` |
| `l` | `/usr/` | keep char | `/usr/l` |

The same process continues for the remaining characters. Every slash block collapses into one slash.

Final output:

```
/usr/local/nginx/sbin
```

This trace demonstrates the invariant that the constructed result never contains consecutive slashes.

### Example 2

Input:

```
/////
```

| Current character | Result before | Action | Result after |
| --- | --- | --- | --- |
| `/` | `""` | keep slash | `/` |
| `/` | `/` | skip slash | `/` |
| `/` | `/` | skip slash | `/` |
| `/` | `/` | skip slash | `/` |
| `/` | `/` | skip slash | `/` |

After scanning, the intermediate result is:

```
/
```

The trailing-slash cleanup does nothing because the string length is already `1`.

Final output:

```
/
```

This example verifies that the root directory is preserved correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(n) | The result list stores the normalized path |

The maximum input length is only 100 characters, so the algorithm easily fits within the time and memory limits. Even slower approaches would pass, but the linear scan is the cleanest and most scalable solution.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    path = input().strip()

    result = []

    for ch in path:
        if ch != '/':
            result.append(ch)
        else:
            if not result or result[-1] != '/':
                result.append('/')

    ans = ''.join(result)

    while len(ans) > 1 and ans[-1] == '/':
        ans = ans[:-1]

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("//usr///local//nginx/sbin\n") == "/usr/local/nginx/sbin", "sample 1"

# minimum-size input
assert run("/\n") == "/", "single root slash"

# multiple slashes representing root
assert run("//////\n") == "/", "root normalization"

# trailing slash removal
assert run("/usr/local///\n") == "/usr/local", "remove trailing slashes"

# consecutive middle slashes
assert run("/a////b///c\n") == "/a/b/c", "compress middle slashes"

# already normalized path
assert run("/home/user/docs\n") == "/home/user/docs", "unchanged normalized path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `/` | `/` | Minimum valid input |
| `//////` | `/` | Root directory preservation |
| `/usr/local///` | `/usr/local` | Trailing slash cleanup |
| `/a////b///c` | `/a/b/c` | Compression of internal slash blocks |
| `/home/user/docs` | `/home/user/docs` | Already normalized paths remain unchanged |

## Edge Cases

Consider the input:

```
/usr/local///
```

During the scan, the algorithm compresses the final `///` into a single trailing slash, producing:

```
/usr/local/
```

The cleanup loop then removes the trailing slash because the string length is greater than one. The final answer becomes:

```
/ usr/local
```

without the space:

```
/usr/local
```

This confirms that non-root paths never end with unnecessary slashes.

Now consider:

```
////
```

The scan keeps only the first slash and skips all remaining ones. The intermediate result is:

```
/
```

The cleanup loop checks:

```
len(ans) > 1
```

Since the length equals `1`, nothing is removed. The root directory remains valid.

Finally, consider:

```
/a////b///c
```

The scan processes each slash group independently. Every maximal consecutive block becomes one slash, giving:

```
/ a / b / c
```

without spaces:

```
/ a/b/c
```

and finally:

```
/a/b/c
```

This confirms that the algorithm preserves directory structure while eliminating redundant separators.
