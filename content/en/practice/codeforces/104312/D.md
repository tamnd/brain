---
title: "CF 104312D - Love is War"
description: "We are given a collection of short text messages, each independent from the others. For every message, we need to decide whether it represents a “battle” or just casual conversation."
date: "2026-07-01T19:52:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104312
codeforces_index: "D"
codeforces_contest_name: "UTPC Spring 2023 Contest (HS)"
rating: 0
weight: 104312
solve_time_s: 65
verified: true
draft: false
---

[CF 104312D - Love is War](https://codeforces.com/problemset/problem/104312/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of short text messages, each independent from the others. For every message, we need to decide whether it represents a “battle” or just casual conversation.

A message is considered a battle if it contains a contiguous sequence of at least three characters that are all the letter ‘a’, and case does not matter. This means we treat uppercase and lowercase versions of letters as identical, so sequences like “aaa”, “Aaa”, or “aAAa” all qualify as long as there is a run of length at least three consecutive ‘a’-like letters in the text.

Each line of input is checked separately, and we output a fixed phrase depending on whether such a substring exists.

The constraints are small: each message has length at most 100 characters, and even if the number of messages is large, the total work per message is constant bounded. This immediately rules out anything heavier than linear scanning per string, and even quadratic behavior per string would be acceptable but unnecessary. A single pass per message is enough.

The main subtlety is in defining “consecutive a’s” correctly under case-insensitivity and ensuring we reset counts correctly whenever a non-‘a’ character appears.

A common mistake comes from only checking exact lowercase 'a' without normalization. For example, “AAA” should be a battle, but a case-sensitive check would incorrectly reject it.

Another subtle edge case is forgetting to reset the streak across spaces or punctuation. For example, “aa a aaaa” contains a valid run of four consecutive a’s at the end, but if a programmer mistakenly resets on every space incorrectly or merges non-contiguous segments, they might miscount.

## Approaches

The brute-force idea is straightforward: for each position in the string, try to expand a window and check whether we can find a run of at least three consecutive characters that are all ‘a’ after normalizing case. For each starting index, scanning forward to detect a run takes O(n), and doing this for every index gives O(n²) per message. With up to 100 characters, this still works comfortably, but it is unnecessary overkill.

The key observation is that we do not need to restart scanning from every position. We only care about contiguous runs of the same character category. If we maintain a running count of consecutive ‘a’-type characters while scanning from left to right, we can decide in one pass whether any run reaches length three. This transforms the problem into a simple streaming check: accumulate streaks, reset when broken, and track the maximum streak length.

The structure of the problem is fundamentally run-length based, so collapsing the string into consecutive segments is optimal. Each character is processed exactly once, and state is constant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) per message | O(1) | Accepted but unnecessary |
| Optimal | O(n) per message | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert the entire message to lowercase so that case differences do not affect comparisons. This ensures uniform handling of ‘A’ and ‘a’ without extra conditional logic during scanning.
2. Initialize a counter `streak = 0` to track the current number of consecutive ‘a’ characters.
3. Scan the string from left to right, processing one character at a time. Each character contributes either to continuing a streak or breaking it.
4. If the current character is ‘a’, increment `streak` by one. This extends the current contiguous segment of valid characters.
5. If the current character is not ‘a’, reset `streak` to zero because the contiguity requirement is broken.
6. After updating `streak`, check whether it has reached 3 or more. If it has, we can immediately classify the message as a battle and stop scanning early.
7. If we finish scanning without ever reaching a streak of 3, classify the message as not a battle.

The early stopping is optional but aligns with the fact that once a valid segment is found, further processing cannot change the answer.

### Why it works

At any position in the string, `streak` represents exactly the length of the current suffix of consecutive ‘a’ characters ending at that position. Because we reset it immediately when a non-‘a’ character appears, it always encodes a valid contiguous segment ending at the current index. Any valid substring of length at least 3 must end at some index where `streak >= 3`, so detecting such a state is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    for _ in range(n):
        s = input().rstrip("\n").lower()
        
        streak = 0
        found = False
        
        for ch in s:
            if ch == 'a':
                streak += 1
                if streak >= 3:
                    found = True
                    break
            else:
                streak = 0
        
        if found:
            print("Love is war!")
        else:
            print("Just friends <3")

if __name__ == "__main__":
    solve()
```

The solution reads each message, normalizes it using `.lower()`, and maintains a single integer counter. The `found` flag allows early termination once a valid run is discovered. Resetting `streak` on any non-‘a’ character preserves contiguity, which is the core requirement.

A subtle implementation detail is stripping only the newline character. We avoid stripping spaces because spaces are meaningful characters that break runs. Another important point is performing `.lower()` once per string instead of per character, which keeps the per-character loop minimal and efficient.

## Worked Examples

Consider the sample input:

```
THIS MEANS WAAAAAARRRRRRRRRR
```

We track the scan:

| Index | Char | Lower | Streak | Found |
| --- | --- | --- | --- | --- |
| 0 | T | t | 0 | no |
| ... | ... | ... | 0 | no |
| 11 | W | w | 0 | no |
| 12 | A | a | 1 | no |
| 13 | A | a | 2 | no |
| 14 | A | a | 3 | yes |

At index 14, streak reaches 3, so we immediately classify it as a battle. This demonstrates that only contiguous runs matter, not total counts.

Now consider:

```
LlLmmAAaOoo that's soooo funnnyyy
```

| Index | Char | Lower | Streak | Found |
| --- | --- | --- | --- | --- |
| ... | l | l | 0 | no |
| ... | m | m | 0 | no |
| ... | A | a | 1 | no |
| ... | A | a | 2 | no |
| ... | a | a | 3 | yes |

Even though letters are separated by other characters later, the run of “AAA” appears locally and triggers the condition.

This confirms that the algorithm correctly isolates contiguous segments and ignores irrelevant parts of the string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total characters across all messages) | Each character is visited once and processed in constant time |
| Space | O(1) | Only a few counters and flags are used |

Given that each message is at most 100 characters, the total workload is extremely small, well within limits even for large n. The algorithm is effectively linear in input size with minimal constant overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    n = int(sys.stdin.readline())
    for _ in range(n):
        s = sys.stdin.readline().rstrip("\n").lower()
        streak = 0
        found = False
        for ch in s:
            if ch == 'a':
                streak += 1
                if streak >= 3:
                    found = True
                    break
            else:
                streak = 0
        
        output.append("Love is war!" if found else "Just friends <3")
    
    return "\n".join(output)

# provided samples
assert run("""5
How are you doing Kaguya?
THIS MEANS WAAAAAARRRRRRRRRR
oops sorry wrong person
LlLmmAAaOoo that's soooo funnnyyy
what is a aardvark
""") == """Just friends <3
Love is war!
Just friends <3
Love is war!
Just friends <3"""

# custom cases
assert run("1\naaa") == "Love is war!"
assert run("1\nAaA") == "Love is war!"
assert run("1\naa a aa") == "Just friends <3"
assert run("1\nbbbbbaaa") == "Love is war!"
assert run("1\nababa") == "Just friends <3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `aaa` | Love is war! | minimum valid streak |
| `AaA` | Love is war! | case insensitivity |
| `aa a aa` | Just friends <3 | non-contiguous reset |
| `bbbbbaaa` | Love is war! | detection at end |
| `ababa` | Just friends <3 | no valid segment |

## Edge Cases

One important edge case is when the string contains mixed case letters forming a valid run only after normalization. For example, input “AaAaA” becomes “aaaaa” after lowering, producing a valid streak of 5. The algorithm handles this because normalization happens before scanning, so the streak count is computed on a uniform representation.

Another case is when valid characters are separated by spaces or punctuation. For example, “aa aaaa” should be a battle because of the trailing run of four ‘a’s. During scanning, the space resets the streak to zero, and the final segment correctly rebuilds the streak, reaching 4 and triggering the condition.

A third case is strings with no ‘a’ at all, such as “hello world”. The streak remains zero throughout, and no early termination occurs, correctly producing a non-battle classification.
