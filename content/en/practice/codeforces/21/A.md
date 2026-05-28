---
title: "CF 21A - Jabber ID"
description: "We need to validate whether a string follows the exact syntax of a Jabber ID."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 21
codeforces_index: "A"
codeforces_contest_name: "Codeforces Alpha Round 21 (Codeforces format)"
rating: 1900
weight: 21
solve_time_s: 97
verified: false
draft: false
---
[CF 21A - Jabber ID](https://codeforces.com/problemset/problem/21/A)

**Rating:** 1900  
**Tags:** implementation, strings  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We need to validate whether a string follows the exact syntax of a Jabber ID.

A valid ID has three possible pieces:

`username@hostname`

or

`username@hostname/resource`

The username and resource follow the same rules. They may contain only English letters, digits, and underscores. Their lengths must be between 1 and 16.

The hostname is slightly different. It is split into parts separated by dots. Every part must satisfy the same rules as the username, meaning each part must contain only letters, digits, and underscores and have length between 1 and 16. The entire hostname length must be between 1 and 32.

The input is a single string, and we must print `YES` if every rule is satisfied, otherwise `NO`.

The input length is at most 100, so performance is not a concern. Even quadratic parsing would easily fit. The challenge is correctness. Most wrong submissions fail because they parse separators incorrectly or forget one of the length conditions.

Several edge cases are easy to mishandle.

A hostname may contain multiple dot-separated words:

```
a@b.c.d
```

This is valid because each segment is non-empty and legal.

A hostname with empty segments is invalid:

```
a@b..c
```

The correct answer is `NO` because the substring between the two dots is empty. A careless split-based implementation sometimes forgets to reject empty pieces.

The resource part is optional, but if `/` exists then the resource cannot be empty:

```
a@b/
```

The answer is `NO`.

The same applies to the username:

```
@abc
```

This is invalid because the username length must be at least 1.

A common parsing mistake is allowing multiple `@` symbols:

```
a@b@c
```

This must be rejected because the structure allows exactly one username and one hostname.

Another subtle case is hostname length. Even if every segment is valid individually, the whole hostname must still be at most 32 characters.

```
a@abcdefghij.abcdefghij.abcdefghijx
```

Each piece length is fine, but the total hostname exceeds 32, so the answer is `NO`.

## Approaches

The most direct brute-force solution is to try every possible split position for `@` and `/`, then check whether the resulting substrings satisfy all rules.

For example, we can iterate over every possible `@` position, then every possible `/` position after it, and verify all pieces manually. Since the string length is at most 100, this still runs instantly. The worst case is roughly a few thousand substring checks.

The weakness of this approach is not speed, but complexity of implementation. Once multiple separators are involved, brute-force parsing becomes error-prone. It is easy to accidentally accept malformed structures such as multiple `@` characters or empty hostname segments.

The cleaner approach is to parse the string according to its grammar.

The structure is rigid:

1. There must be exactly one `@`.
2. Everything before `@` is the username.
3. Everything after `@` is either:

- just a hostname
- or hostname/resource

Once the string is separated into these logical components, validation becomes local. Each piece can be checked independently.

The key observation is that all atomic words share the same validation rule: only letters, digits, and underscores, with length between 1 and 16. That means we can write one reusable validator function and apply it everywhere.

For the hostname, we additionally split by dots and validate every segment individually.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Check that the string contains exactly one `@`.

Without this restriction, malformed inputs like `a@b@c` could be parsed ambiguously.
3. Split the string into `username` and `rest` using the `@`.
4. Validate the username.

The username must:

- have length between 1 and 16
- contain only letters, digits, or underscores
5. Check whether `rest` contains a `/`.

If it does, split into `hostname` and `resource`.

If it does not, then the entire `rest` is the hostname and there is no resource.
6. If a resource exists, validate it using the same rules as the username.

An empty resource is invalid.
7. Validate the hostname length.

The whole hostname must have length between 1 and 32.
8. Split the hostname by dots.
9. Validate every hostname segment.

Every segment must:

- be non-empty
- have length between 1 and 16
- contain only letters, digits, or underscores
10. If every check succeeds, print `YES`. Otherwise print `NO`.

### Why it works

The algorithm mirrors the exact formal structure of a valid Jabber ID.

The `@` split guarantees that there is exactly one username and one hostname section. The optional `/` split isolates the resource if it exists. Every remaining atomic component is checked against the character and length rules.

The hostname validation is correct because splitting by dots produces exactly the hostname words described in the specification. Rejecting empty segments prevents invalid forms like consecutive dots or leading/trailing dots.

Since every rule from the specification is checked directly and independently, the algorithm accepts all valid IDs and rejects all invalid ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

def valid_word(s):
    if not (1 <= len(s) <= 16):
        return False

    for ch in s:
        if not (ch.isalnum() or ch == '_'):
            return False

    return True

def solve():
    s = input().strip()

    if s.count('@') != 1:
        print("NO")
        return

    username, rest = s.split('@')

    if not valid_word(username):
        print("NO")
        return

    if rest.count('/') > 1:
        print("NO")
        return

    if '/' in rest:
        hostname, resource = rest.split('/')

        if not valid_word(resource):
            print("NO")
            return
    else:
        hostname = rest

    if not (1 <= len(hostname) <= 32):
        print("NO")
        return

    parts = hostname.split('.')

    for part in parts:
        if not valid_word(part):
            print("NO")
            return

    print("YES")

solve()
```

The solution revolves around one reusable helper, `valid_word`. This function implements the shared validation logic used by usernames, resources, and hostname segments.

The first structural check is counting `@`. Using `count('@') != 1` immediately rejects malformed inputs before any deeper parsing happens.

The resource parsing deserves careful handling. We first check whether more than one `/` exists inside the hostname-resource section. Inputs like:

```
a@b/c/d
```

must be rejected.

Hostname validation happens in two layers. First we validate the total hostname length, since the statement imposes a separate limit of 32 characters. Then we split by dots and validate each segment individually.

The split behavior naturally catches empty components. For example:

```
"ab..cd".split('.')
```

produces:

```
["ab", "", "cd"]
```

The empty string fails `valid_word`, which correctly rejects the hostname.

## Worked Examples

### Example 1

Input:

```
[email protected]
```

| Step | Variable | Value |
| --- | --- | --- |
| Read input | s | `codeforces@tests` |
| Split by @ | username | `codeforces` |
| Split by @ | rest | `tests` |
| Validate username | result | valid |
| Check / | found | no |
| Hostname | hostname | `tests` |
| Split hostname | parts | `["tests"]` |
| Validate parts | result | valid |
| Final answer | output | `YES` |

This example shows the simplest valid structure without a resource part. Every component satisfies the allowed-character and length rules.

### Example 2

Input:

```
a@b..c
```

| Step | Variable | Value |
| --- | --- | --- |
| Read input | s | `a@b..c` |
| Split by @ | username | `a` |
| Split by @ | rest | `b..c` |
| Validate username | result | valid |
| Hostname | hostname | `b..c` |
| Split hostname | parts | `["b", "", "c"]` |
| Validate empty part | result | invalid |
| Final answer | output | `NO` |

This trace demonstrates why empty hostname segments must be rejected. Consecutive dots create an empty substring between them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed a constant number of times |
| Space | O(n) | Splitting the string creates substring arrays |

The input length is at most 100, so the solution easily fits within the limits. Even inefficient implementations would pass comfortably, but the linear parser is cleaner and easier to reason about.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    s = input().strip()

    def valid_word(x):
        if not (1 <= len(x) <= 16):
            return False

        for ch in x:
            if not (ch.isalnum() or ch == '_'):
                return False

        return True

    if s.count('@') != 1:
        print("NO")
        return

    username, rest = s.split('@')

    if not valid_word(username):
        print("NO")
        return

    if rest.count('/') > 1:
        print("NO")
        return

    if '/' in rest:
        hostname, resource = rest.split('/')

        if not valid_word(resource):
            print("NO")
            return
    else:
        hostname = rest

    if not (1 <= len(hostname) <= 32):
        print("NO")
        return

    for part in hostname.split('.'):
        if not valid_word(part):
            print("NO")
            return

    print("YES")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("[email protected]\n") == "YES", "sample 1"

# custom cases
assert run("a@b\n") == "YES", "minimum valid case"

assert run("@b\n") == "NO", "empty username"

assert run("a@b..c\n") == "NO", "empty hostname segment"

assert run("abcdefghijklmnopq@abc\n") == "NO", "username exceeds 16 chars"

assert run("a@abc/\n") == "NO", "empty resource"

assert run("a@b/c/d\n") == "NO", "multiple slashes"

assert run("a_b@c_d.e_f/resource_1\n") == "YES", "underscores allowed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a@b` | `YES` | Smallest valid structure |
| `@b` | `NO` | Username cannot be empty |
| `a@b..c` | `NO` | Empty hostname segments are invalid |
| `abcdefghijklmnopq@abc` | `NO` | Username length upper bound |
| `a@abc/` | `NO` | Resource cannot be empty |
| `a@b/c/d` | `NO` | Only one optional slash allowed |
| `a_b@c_d.e_f/resource_1` | `YES` | Underscores are legal everywhere |

## Edge Cases

Consider the input:

```
a@b..c
```

The algorithm splits the hostname into:

```
["b", "", "c"]
```

The empty middle segment fails `valid_word` because its length is 0. The algorithm correctly prints `NO`.

Now consider:

```
a@b/
```

The parser detects `/` and splits into:

```
hostname = "b"
resource = ""
```

The empty resource fails validation immediately, so the answer is `NO`.

For multiple `@` symbols:

```
a@b@c
```

The first check counts the number of `@` characters. Since the count is not exactly 1, the string is rejected before any further parsing.

For a hostname exceeding 32 characters:

```
a@abcdefghij.abcdefghij.abcdefghijx
```

The total hostname length becomes 33. Even though every individual segment is valid, the separate hostname-length condition fails, so the algorithm outputs `NO`.

Finally, consider a valid complex example:

```
abc_DEF@host_1.server_2/resource_3
```

The username, every hostname segment, and the resource all satisfy the shared validation rule. The hostname length is within 32. The algorithm reaches the end without triggering any rejection and prints `YES`.
