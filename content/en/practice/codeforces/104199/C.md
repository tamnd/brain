---
title: "CF 104199C - \u0411\u0435\u0437\u043b\u044e\u0434\u043d\u044b\u0439 \u043e\u0442\u0435\u043b\u044c"
description: "We are given a word written as a sequence of lowercase Latin letters. A token starts on the first character and moves according to a deterministic rule that depends entirely on how many times the current character appears in the word."
date: "2026-07-02T00:01:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104199
codeforces_index: "C"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u043d\u0430 \u0412\u041a\u041e\u0428\u041f.Junior 18-02-23"
rating: 0
weight: 104199
solve_time_s: 84
verified: true
draft: false
---

[CF 104199C - \u0411\u0435\u0437\u043b\u044e\u0434\u043d\u044b\u0439 \u043e\u0442\u0435\u043b\u044c](https://codeforces.com/problemset/problem/104199/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a word written as a sequence of lowercase Latin letters. A token starts on the first character and moves according to a deterministic rule that depends entirely on how many times the current character appears in the word.

If the character under the token occurs more than once in the string, the token is allowed to jump to any other occurrence of the same character. If the character occurs exactly once, the token is forced to move one step to the right. If it is already at the last position and the character is unique, the process ends.

The question is whether this process always terminates or whether it can be made to continue forever by choosing jumps between equal characters.

The constraint n up to 100000 implies that any simulation that explores transitions step by step is unsafe if it can cycle through states repeatedly. The process can revisit positions many times because repeated letters allow arbitrary jumps, so the state space is effectively a graph with up to 100000 nodes and many edges induced by identical characters. A naive simulation that runs until termination or cycle detection could degrade to quadratic behavior in the worst case due to repeated revisits.

A subtle edge case appears when all characters are identical. For example, in a string like "aaa", the token never advances deterministically and can always jump back and forth, producing an infinite loop. On the other hand, in a string like "abc", every character is unique, so the token always moves right and terminates immediately.

The key difficulty is recognizing when the jump structure creates a cycle rather than actually simulating the process.

## Approaches

A brute force interpretation treats each position as a state. From a position i, if the current character appears more than once, we consider transitions to all other indices with the same character. Otherwise, we move to i + 1. We continue this process until we either fall off the string or revisit a previously seen position in a configuration that guarantees repetition.

This works conceptually because the process is deterministic once we fix a choice of jumps, but the problem allows arbitrary choices among equal letters, meaning the process is not a single path but a branching system. A direct simulation would need to explore all possible choices or maintain a visited set over an implicit graph of states. In the worst case, every position could connect to many others with the same character, and repeated revisits can create exponential or quadratic blowup.

The key observation is that the only way to make progress is via characters that appear exactly once in the entire suffix behavior of the process. If at any moment the token is on a character that appears multiple times, we can always choose to jump to an earlier occurrence and recreate a previously seen situation. This ability to return to a previous state implies that the system is cyclic unless forced progress dominates.

Thus the problem reduces to checking whether the process can reach a point where every character we land on is unique within the remaining reachable structure in a way that forces deterministic rightward movement until termination. This collapses to a structural condition on frequencies: if there exists any character with frequency at least 2, it is always possible to construct a loop by bouncing between occurrences of that character, because nothing in the rules prevents returning to earlier indices indefinitely.

Therefore, termination happens if and only if all characters are distinct in the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute simulation of transitions | O(n²) worst case | O(n) | Too slow |
| Frequency check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

The solution is based on counting occurrences of each character and checking whether any character appears more than once.

1. Count the frequency of every character in the string. This is done in a single pass over the input, maintaining a fixed array of size 26 since only lowercase Latin letters are used. This step captures all structural ambiguity in the process.
2. Scan through the frequency table and check whether any character has frequency greater than 1. The presence of such a character means there exists at least one position where the token can always choose a jump back to another identical character.
3. If any frequency exceeds 1, conclude that the process can be made infinite and output NO. Otherwise, if all frequencies are exactly 1, the token always moves right until it exits the string, so output YES.

### Why it works

The process only becomes non-deterministic at characters that appear multiple times. At such a character, the token gains freedom to jump to another identical position, which always preserves the ability to revisit previous configurations. Since positions are finite, repeated revisits under this freedom form a cycle. If no character repeats, every move is forced to the next index, and the state strictly progresses until termination.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    freq = [0] * 26
    for ch in s:
        freq[ord(ch) - ord('a')] += 1

    for c in freq:
        if c > 1:
            print("NO")
            return

    print("YES")

if __name__ == "__main__":
    solve()
```

The solution begins by reading the length and string. The frequency array tracks occurrences of each character in constant space. The scan for duplicates is the decisive step: it does not attempt to simulate movement, because the only property that matters is whether branching exists at any position.

The check `c > 1` is sufficient because even a single repeated character introduces a reversible transition mechanism, allowing the token to loop indefinitely by alternating between occurrences.

## Worked Examples

### Example 1: "letovo"

We track frequencies first.

| character | count |
| --- | --- |
| l | 1 |
| e | 1 |
| t | 1 |
| o | 2 |
| v | 1 |

Since 'o' appears twice, the algorithm immediately decides that a cycle is possible and outputs NO.

This matches the intuitive behavior where the token can bounce between the two 'o' positions indefinitely.

### Example 2: "abc"

| character | count |
| --- | --- |
| a | 1 |
| b | 1 |
| c | 1 |

All counts are 1, so the token always moves right deterministically: 0 → 1 → 2 → exit. The output is YES.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass to compute frequencies and scan alphabet |
| Space | O(1) | fixed 26-length frequency array |

The input size up to 100000 is easily handled since the solution performs only linear scanning with constant auxiliary memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("6\nletovo\n") == "NO"
assert run("3\nabc\n") == "YES"
assert run("3\naaa\n") == "NO"

# custom cases
assert run("1\na\n") == "YES"          # single character
assert run("2\nab\n") == "YES"         # minimal distinct
assert run("2\naa\n") == "NO"          # immediate repeat
assert run("5\nabcde\n") == "YES"      # all unique longer
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 a | YES | smallest case |
| aa | NO | immediate repetition |
| abcde | YES | general distinct case |
| aaa | NO | full repetition cycle |

## Edge Cases

A minimal single-character string like "a" starts with a unique character, so the token immediately moves out of bounds and terminates. The frequency check sees no repetition and returns YES.

A string like "aa" demonstrates immediate non-termination: both positions share the same character, so even though the token can move, it always has an alternative occurrence to jump to, allowing an infinite loop between the two indices. The algorithm correctly flags frequency 2 and returns NO.

A string like "abcde" contains no duplicates, so every step is forced rightward with no branching, guaranteeing termination at the end of the string.
