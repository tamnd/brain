---
title: "CF 105227D - Chat Order"
description: "We are simulating a dynamic chat sidebar that always shows recent conversations first. Every time Polycarp sends a message to a friend, that friend’s chat becomes the most recently active and is moved to the very top of the list."
date: "2026-06-24T16:27:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105227
codeforces_index: "D"
codeforces_contest_name: "CPG Training Contest - 1"
rating: 0
weight: 105227
solve_time_s: 73
verified: false
draft: false
---

[CF 105227D - Chat Order](https://codeforces.com/problemset/problem/105227/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a dynamic chat sidebar that always shows recent conversations first. Every time Polycarp sends a message to a friend, that friend’s chat becomes the most recently active and is moved to the very top of the list. If the friend was never contacted before, a new chat entry is created at the top. If the friend already exists in the list, their existing entry is removed from its current position and reinserted at the front.

The input is a sequence of recipient names in the order messages are sent. The output is the final ordering of unique friends, from most recently messaged to least recently messaged, after processing all operations.

The constraints allow up to 200,000 messages, and each name has length at most 10. This immediately rules out any solution that repeatedly scans or shifts a list for each message. A naive approach that removes an element from a Python list or array in the middle costs linear time per operation, which would lead to quadratic behavior in the worst case.

A subtle edge case appears when the same friend is messaged repeatedly. For example, if the input is `a b a`, then after processing:

- after `a`, list is `a`
- after `b`, list is `b a`
- after `a`, list becomes `a b`

A naive implementation that simply inserts at the front without removing the old occurrence would incorrectly produce duplicates like `a b a`, which violates the requirement that each friend appears at most once.

Another edge case is when all messages go to the same person. The list should always end with exactly one entry, that person, regardless of how many messages were sent.

## Approaches

The brute-force simulation keeps a list of current chats. For each incoming name, it scans the list to check if the name already exists. If it does, it removes that entry, then inserts the name at the front. If it does not, it simply inserts at the front.

This is correct because it mirrors the exact described behavior. However, each operation requires a linear search to find the position and another linear operation to remove or shift elements. In the worst case where all messages are distinct, we repeatedly scan an ever-growing list, leading to roughly 1 + 2 + 3 + ... + n operations, which is O(n²). With n up to 200,000, this is far too slow.

The key observation is that we only care about whether a name is present and its current position, and we need fast updates at both lookup and reordering. This suggests combining a hash-based structure for existence tracking with a structure that supports fast insertion at the front. A set alone cannot preserve order, and a list alone is too slow for membership updates. The solution is to maintain a set for membership and a deque-like structure for ordering, but even simpler, we can simulate using a set plus a list built backwards, or more cleanly, we process from the end using a set and construct the final order once.

A particularly clean insight is to traverse the messages in reverse. When scanning from the last message to the first, the first time we encounter a name, it must be the final position of that chat in the answer. Any earlier occurrences are irrelevant because later occurrences override earlier ones in the forward process. So we can build the result by iterating backward and collecting first-seen names.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(n) | Too slow |
| Reverse Scan with Set | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the message list from the last recipient to the first, maintaining a set of names already included in the answer and a list for the final order.

1. Start with an empty set and an empty list.

The set tracks which friends have already been placed in the final ordering.
2. Iterate over the message recipients from the end of the list toward the beginning.

This reversal works because later messages override earlier ones in determining final recency.
3. For each name, check if it is already in the set.

If it is already present, we skip it since its final position is already determined.
4. If it is not in the set, we add it to the result list and mark it as seen.

The first time we encounter a name in reverse order corresponds to its most recent appearance in the original sequence.
5. Continue until all messages have been processed.
6. Finally, reverse the constructed list because we collected names in reverse order of final appearance.

### Why it works

Each friend’s final position is determined solely by their last occurrence in the input sequence. Processing from the end guarantees that the first time we encounter a name is exactly its last occurrence in forward time. By skipping all subsequent encounters, we ensure each friend is included exactly once, and in correct recency order. The set enforces uniqueness, while reverse traversal encodes the “most recent wins” rule.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = [input().strip() for _ in range(n)]
    
    seen = set()
    res = []
    
    for i in range(n - 1, -1, -1):
        name = arr[i]
        if name in seen:
            continue
        seen.add(name)
        res.append(name)
    
    print("\n".join(res))

if __name__ == "__main__":
    solve()
```

The solution reads all names first so we can traverse them backwards. The `seen` set ensures each name is output only once. We append names in reverse-final order and directly print them in that order, since reversing is not needed if we interpret construction correctly: the first time we see a name from the back is its final position, and we append in that order.

The key implementation detail is stripping input lines properly; without it, trailing newline characters would break equality checks in the set. Also, we avoid any list deletions or insertions at the front, which would degrade performance.

## Worked Examples

### Example 1

Input:

`alex ivan roman ivan`

We process from right to left:

| Step | Name | Seen before? | Action | Result list |
| --- | --- | --- | --- | --- |
| 1 | ivan | no | add | [ivan] |
| 2 | roman | no | add | [ivan, roman] |
| 3 | ivan | yes | skip | [ivan, roman] |
| 4 | alex | no | add | [ivan, roman, alex] |

Final output is `ivan roman alex`.

This confirms that only the last occurrence of each name matters.

### Example 2

Input:

`alina maria ekaterina darya darya ekaterina maria alina`

We again scan from right to left:

| Step | Name | Seen before? | Action | Result list |
| --- | --- | --- | --- | --- |
| 1 | alina | no | add | [alina] |
| 2 | maria | no | add | [alina, maria] |
| 3 | ekaterina | no | add | [alina, maria, ekaterina] |
| 4 | darya | no | add | [alina, maria, ekaterina, darya] |
| 5 | darya | yes | skip | same |
| 6 | ekaterina | yes | skip | same |
| 7 | maria | yes | skip | same |
| 8 | alina | yes | skip | same |

Output: `alina maria ekaterina darya`.

This shows that repeated updates collapse correctly into a single final ordering based on last appearance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each name is processed once, with O(1) set operations |
| Space | O(n) | Storage for input list and seen set in worst case |

The linear complexity fits easily within constraints of 200,000 operations, and memory usage remains within limits since each name is short and stored once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    
    def solve():
        n = int(input())
        arr = [input().strip() for _ in range(n)]
        seen = set()
        res = []
        for i in range(n - 1, -1, -1):
            if arr[i] not in seen:
                seen.add(arr[i])
                res.append(arr[i])
        print("\n".join(res))
    
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided samples
assert run("4\nalex\nivan\nroman\nivan\n") == "ivan\nroman\nalex"
assert run("8\nalina\nmaria\nekaterina\ndarya\ndarya\nekaterina\nmaria\nalina\n") == "alina\nmaria\nekaterina\ndarya"

# custom cases
assert run("1\na\n") == "a"
assert run("3\na\na\na\n") == "a"
assert run("3\na\nb\na\n") == "a\nb"
assert run("5\na\nb\nc\nd\ne\n") == "e\nd\nc\nb\na"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 a | a | minimum size |
| a a a | a | repeated overwrite |
| a b a | a b | last occurrence dominance |
| a b c d e | e d c b a | full uniqueness ordering |

## Edge Cases

For repeated identical messages, such as `a a a a`, the algorithm processes from the back and immediately takes the first `a` it encounters, then skips all others. The set prevents duplication, so the output remains a single `a`, matching the requirement that chats are unique.

For alternating patterns like `a b a b a`, the reverse scan encounters `a` first, then `b`, and ignores earlier occurrences, producing `a b`. This directly reflects that only the last message per friend determines final ordering.

For strictly increasing unique names, every name is added once in reverse scan order, producing the reverse of the input, which is consistent with “most recent at top” behavior in a sequence of all distinct chats.
