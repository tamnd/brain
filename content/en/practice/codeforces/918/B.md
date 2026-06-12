---
title: "CF 918B - Radio Station"
description: "We are given a small registry of servers, where each server is identified by a unique IP address and also has a human-readable name. After that, we are given a list of configuration commands, and each command references a server only through its IP."
date: "2026-06-13T02:29:03+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 918
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 459 (Div. 2)"
rating: 900
weight: 918
solve_time_s: 563
verified: true
draft: false
---

[CF 918B - Radio Station](https://codeforces.com/problemset/problem/918/B)

**Rating:** 900  
**Tags:** implementation, strings  
**Solve time:** 9m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small registry of servers, where each server is identified by a unique IP address and also has a human-readable name. After that, we are given a list of configuration commands, and each command references a server only through its IP.

The task is to enrich each command line by appending a comment containing the corresponding server name. Concretely, whenever a command contains an IP address, we must replace that line by the same line followed by `#name`, where `name` is the server whose IP matches.

The structure of the input makes the intent very direct: first build a mapping from IP address to server name, then use that mapping to translate each command line.

The constraints are small, with at most 1000 servers and 1000 commands. This means even a straightforward approach that performs linear searches is already within acceptable limits, since a worst-case scan of all servers per command gives about 1,000,000 comparisons, which is trivial in Python under a 2-second limit. Still, the structure of IP lookup strongly suggests a dictionary-based solution.

A subtle point is that server names are not guaranteed to be unique, but IP addresses are. This is important because the correct key for lookup is strictly the IP, not the name. Another detail is parsing: the IP appears in the command line with a trailing semicolon, so it must be stripped carefully before lookup.

No tricky edge cases arise beyond correct string handling and mapping, but a careless solution might fail in a few ways. One is forgetting to remove the trailing semicolon, leading to failed dictionary lookups. Another is splitting the command incorrectly if multiple spaces or formatting variations are assumed. Since the format is consistent, splitting by spaces and trimming the semicolon is sufficient.

## Approaches

The most direct solution is to, for each command line, scan all known servers and find the one whose IP matches the queried IP. This works because the dataset is small, and each lookup is independent. However, this approach repeats the same comparisons for every query. With 1000 commands and 1000 servers, it performs up to one million string comparisons, which is still acceptable but unnecessary.

The key observation is that the relationship between IP and server name is static. Once we read the server list, we can precompute a dictionary that maps each IP string directly to its name. This reduces each query to a single hash table lookup instead of a linear scan.

The transformation becomes purely mechanical: build a map, parse each command, extract the IP, look up the name, and append it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan per Query | O(nm) | O(1) | Accepted but unnecessary |
| Hash Map Lookup | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We separate the solution into preprocessing and query handling.

1. Read all server entries and store them in a dictionary keyed by IP address. Each entry maps the IP string directly to the server name. This ensures constant-time retrieval later.
2. Iterate through each configuration command line. Each line contains a command word, an IP, and a trailing semicolon.
3. Split the line into tokens using whitespace. The second token contains the IP with a semicolon attached.
4. Remove the semicolon from the IP token. This is necessary because dictionary keys are stored as pure IP strings without punctuation.
5. Use the cleaned IP to retrieve the corresponding server name from the dictionary.
6. Construct the output line by concatenating the original command, the original IP-with-semicolon token, and the comment `#name`.

The key design choice is that we never try to reinterpret or reformat the IP beyond stripping the semicolon. We preserve the original formatting of the command line and only append the comment.

### Why it works

The dictionary stores a complete bijection from IPs to names, and every query IP is guaranteed to exist in this mapping. Each command line is independent, and the transformation depends only on this fixed mapping. Since the parsing step always extracts the exact IP string (after removing `;`), the lookup is exact and unambiguous, ensuring every command is annotated with the correct server name.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    mp = {}

    for _ in range(n):
        name, ip = input().split()
        mp[ip] = name

    out = []
    for _ in range(m):
        parts = input().split()
        command = parts[0]
        ip_with_semicolon = parts[1]

        ip = ip_with_semicolon[:-1]
        name = mp[ip]

        out.append(f"{command} {ip_with_semicolon} #{name}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The core idea in the code is the dictionary `mp`, which provides direct translation from IP to server name. The parsing logic relies on the fixed structure of each command line, so we safely split into two tokens and strip exactly one trailing character from the IP token. Output formatting preserves the original command formatting and only appends the required comment.

A common mistake is attempting to parse the IP more aggressively, such as splitting on dots or semicolons unnecessarily. That is not required and only increases risk of formatting bugs.

## Worked Examples

We use the provided sample input to illustrate execution.

### Example trace

Input servers:

```
main -> 192.168.0.2
replica -> 192.168.0.1
```

Commands:

```
block 192.168.0.1;
proxy 192.168.0.2;
```

| Step | Input line | Parsed IP | Lookup result | Output |
| --- | --- | --- | --- | --- |
| 1 | block 192.168.0.1; | 192.168.0.1 | replica | block 192.168.0.1; #replica |
| 2 | proxy 192.168.0.2; | 192.168.0.2 | main | proxy 192.168.0.2; #main |

This confirms that each line is independently transformed using the same fixed mapping.

A second small example helps verify robustness.

Input:

```
1 2
alpha 1.1.1.1
ping 1.1.1.1;
pong 1.1.1.1;
```

Both commands map to the same server, showing that multiple queries can share the same IP without any issue since dictionary lookup is stateless.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One pass to build the dictionary, one pass to process commands with O(1) average lookup per command |
| Space | O(n) | Stores one mapping entry per server |

The constraints cap both n and m at 1000, so this solution runs comfortably within limits. Even in Python, dictionary operations at this scale are instantaneous.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    mp = {}

    for _ in range(n):
        name, ip = input().split()
        mp[ip] = name

    res = []
    for _ in range(m):
        parts = input().split()
        cmd = parts[0]
        ip_semicolon = parts[1]
        ip = ip_semicolon[:-1]
        res.append(f"{cmd} {ip_semicolon} #{mp[ip]}")

    return "\n".join(res)

# provided sample
assert run("""2 2
main 192.168.0.2
replica 192.168.0.1
block 192.168.0.1;
proxy 192.168.0.2;
""") == """block 192.168.0.1; #replica
proxy 192.168.0.2; #main"""

# single server reused
assert run("""1 2
alpha 1.1.1.1
ping 1.1.1.1;
pong 1.1.1.1;
""") == """ping 1.1.1.1; #alpha
pong 1.1.1.1; #alpha"""

# minimal case
assert run("""1 1
x 0.0.0.0
cmd 0.0.0.0;
""") == "cmd 0.0.0.0; #x"

# multiple distinct mappings
assert run("""3 3
a 1.1.1.1
b 2.2.2.2
c 3.3.3.3
x 3.3.3.3;
y 1.1.1.1;
z 2.2.2.2;
""") == """x 3.3.3.3; #c
y 1.1.1.1; #a
z 2.2.2.2; #b"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single server reused | repeated lookup correctness | repeated IP queries |
| minimal case | single mapping correctness | boundary handling |
| multiple mappings | full permutation correctness | dictionary correctness across entries |

## Edge Cases

One subtle edge case is when multiple commands reference the same IP. Since the mapping is purely associative and not consumed or modified, repeated lookups always return the same name. The algorithm naturally handles this because dictionary access does not change state.

Another potential pitfall is incorrect IP extraction. If one forgets to strip the semicolon, the lookup key becomes `192.168.0.1;`, which does not exist in the dictionary. This leads to runtime errors. The fix is consistently removing exactly the last character of the second token, which is guaranteed to be `;` by the input format.

A final edge case is assuming names are unique or using them as keys. Since names may repeat, using IP as the sole key is necessary. The dictionary design avoids ambiguity entirely because IP uniqueness is guaranteed.
