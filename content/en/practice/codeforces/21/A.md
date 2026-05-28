---
title: "CF 21A - Jabber ID"
description: "We are given a string that is supposed to represent a Jabber ID on a fictional service. A Jabber ID is structured as <us"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 21
codeforces_index: "A"
codeforces_contest_name: "Codeforces Alpha Round 21 (Codeforces format)"
rating: 1900
weight: 21
solve_time_s: 99
verified: false
draft: false
---

[CF 21A - Jabber ID](https://codeforces.com/problemset/problem/21/A)

**Rating:** 1900  
**Tags:** implementation, strings  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string that is supposed to represent a Jabber ID on a fictional service. A Jabber ID is structured as `<username>@<hostname>[/<resource>]`, where the `resource` part is optional. The username must be a string of letters, digits, or underscores, and its length is limited to 1-16 characters. The hostname is a dot-separated sequence of “words” with the same character restrictions and length between 1 and 16 per word, and the total hostname cannot exceed 32 characters. The resource, if present, also follows the same character rules with a 1-16 length limit.

The input string can be any sequence of 1 to 100 ASCII characters. Our goal is to validate whether the string is a correctly formatted Jabber ID and print `YES` if it is, or `NO` otherwise.

The constraints are tight on character sets and lengths but loose on overall string length. Since the input is at most 100 characters, a linear scan of the string is fast enough, so our algorithm can iterate over the string several times without performance issues.

Non-obvious edge cases include strings missing the `@` symbol, usernames or hostnames that are empty, hostnames with empty segments like `host..com`, usernames or hostname words that exceed the length limit, and incorrect resource lengths. A careless implementation might, for example, accept `user@host..com` because it splits on `@` and `.` without checking for empty words, but the correct output is `NO`.

## Approaches

A naive approach would be to attempt parsing the string manually by scanning characters one by one, validating each segment against character sets and lengths. This works because the rules are explicit, but it is verbose and prone to off-by-one errors. Conceptually, you could split on `@` and then on `/`, then check each segment. The operation count is linear in string length, which is acceptable here because the string length is capped at 100.

The key insight for a cleaner solution is to leverage Python’s string splitting and iteration while enforcing length and character constraints. We first separate the optional resource from the rest of the ID, then split on `@` to extract the username and hostname. Splitting the hostname on `.` gives us the hostname words. Each component is then validated for allowed characters and length. This method simplifies the brute-force scanning while remaining linear in the length of the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N) | O(N) | Accepted |
| Split and Validate | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Check if the string contains a `/`. If it does, split it into `main_part` and `resource`. If it does not, treat the entire string as `main_part` and set `resource` to `None`.
2. If `resource` exists, verify its length is between 1 and 16 and that all characters are letters, digits, or underscores. If any check fails, print `NO`.
3. Split `main_part` on `@`. If it does not produce exactly two segments, print `NO` because there must be exactly one `@`.
4. Assign the segments to `username` and `hostname`. Validate that `username` has length 1-16 and contains only allowed characters. If not, print `NO`.
5. Split `hostname` on `.`. Each word must be 1-16 characters and contain only letters, digits, or underscores. Additionally, the total hostname length must not exceed 32 characters. If any of these checks fail, print `NO`.
6. If all checks pass, print `YES`.

Why it works: By splitting on `/` and `@` carefully, we isolate the three components of a Jabber ID. Each validation step enforces the explicit constraints given in the problem. Since every possible invalid pattern is rejected by at least one check, the algorithm cannot falsely accept a malformed ID.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_valid_component(s, min_len, max_len):
    if not (min_len <= len(s) <= max_len):
        return False
    for c in s:
        if not (c.isalnum() or c == '_'):
            return False
    return True

def main():
    s = input().strip()
    
    if '/' in s:
        main_part, resource = s.split('/', 1)
        if not is_valid_component(resource, 1, 16):
            print("NO")
            return
    else:
        main_part = s

    if main_part.count('@') != 1:
        print("NO")
        return

    username, hostname = main_part.split('@')
    if not is_valid_component(username, 1, 16):
        print("NO")
        return
    
    if not (1 <= len(hostname) <= 32):
        print("NO")
        return

    hostname_parts = hostname.split('.')
    for part in hostname_parts:
        if not is_valid_component(part, 1, 16):
            print("NO")
            return

    print("YES")

if __name__ == "__main__":
    main()
```

The function `is_valid_component` centralizes the character and length checks to avoid repeating code. We carefully split only once on `/` to avoid accidentally splitting resource segments containing `/`. The username, hostname, and resource are checked independently. Hostname segments are split on `.` and validated individually, ensuring no empty segments are accepted.

## Worked Examples

### Example 1

Input: `[email protected]`

| Variable | Value |
| --- | --- |
| s | `[email protected]` |
| main_part | `[email protected]` |
| resource | None |
| username | `user` |
| hostname | `host` |
| hostname_parts | `['host']` |

The username is valid, hostname has one word with valid characters and length, no resource is present. Output: `YES`.

### Example 2

Input: `[email protected]/contest`

| Variable | Value |
| --- | --- |
| s | `[email protected]/contest` |
| main_part | `[email protected]` |
| resource | `contest` |
| username | `user` |
| hostname | `host.com` |
| hostname_parts | `['host', 'com']` |

All components meet character and length rules. Output: `YES`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each split and validation iterates over the string once, N ≤ 100 |
| Space | O(N) | Splitting produces lists of at most O(N) size |

Linear complexity relative to string length is efficient because N is small. Memory usage is negligible compared to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("[email protected]") == "YES", "sample 1"
assert run("[email protected]/contest") == "YES", "sample 2"

# Custom cases
assert run("a@b") == "YES", "minimum valid input"
assert run("user_with_16char@host_with_16char") == "YES", "max username and hostname word length"
assert run("user@host..com") == "NO", "empty hostname word"
assert run("user@host.com/") == "NO", "empty resource"
assert run("toolongusernameeeee@host") == "NO", "username too long"
assert run("user@toolonghostnameeeeeeeeeeeeeeeeeeeeeeeeeee") == "NO", "hostname too long"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a@b` | YES | minimal valid Jabber ID |
| `user_with_16char@host_with_16char` | YES | maximum allowed word lengths |
| `user@host..com` | NO | empty hostname segment |
| `user@host.com/` | NO | empty resource after slash |
| `toolongusernameeeee@host` | NO | username exceeds length limit |
| `user@toolonghostnameeeeeeeeeeeeeeeeeeeeeeeeeee` | NO | hostname exceeds length limit |

## Edge Cases

An empty hostname segment like `user@host..com` triggers a split resulting in an empty string. Our loop over hostname words checks for length ≥1, so it correctly rejects this input. A resource of length 0, e.g., `user@host/`, fails the `is_valid_component` check for minimum length 1. Multiple `@` symbols, such as `user@host@domain`, are rejected by counting `@` in `main_part` and ensuring there is exactly one. Each edge case is handled systematically by the combination of splitting and component validation.
