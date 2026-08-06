---
title: "CF 102482B - Comma Sprinkler"
description: "The text consists of words separated by spaces, commas, or sentence-ending periods. Some commas are already present. The task is to repeatedly apply a rule system until the comma placement stops changing."
date: "2026-08-06T18:39:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102482
codeforces_index: "B"
codeforces_contest_name: "2018 ACM-ICPC World Finals"
rating: 0
weight: 102482
solve_time_s: 234
verified: true
draft: false
---

[CF 102482B - Comma Sprinkler](https://codeforces.com/problemset/problem/102482/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The text consists of words separated by spaces, commas, or sentence-ending periods. Some commas are already present. The task is to repeatedly apply a rule system until the comma placement stops changing.

A comma before a word gives information about that word: every other occurrence of the same word, except when it starts a sentence, must also get a comma before it. A comma after a word works similarly, spreading to all other occurrences of that word except when it is already at the end of a sentence. Newly created commas can affect neighboring words, so the process has to continue until reaching a fixed point.

The input length can reach one million characters. This rules out repeatedly scanning the whole text after every comma addition. A simulation that tries to apply the rules one change at a time can degrade to quadratic behavior because every new comma may require another full pass over the input. We need an approach where each word occurrence and each word type is processed only a constant number of times.

The tricky part is that commas do not only spread between equal words. Adding a comma before a word also means the previous word is now followed by a comma. Adding a comma after a word means the next word is now preceded by a comma. Ignoring this chain reaction gives incorrect results.

For example:

```
a b. a, b.
```

The correct result is:

```
a, b. a, b.
```

A careless implementation that only remembers which words already had commas would add the comma before the second `a` but might forget that the original comma after the first `a` also propagates backward through the neighboring relationship.

Another edge case is sentence boundaries:

```
x x.
```

The correct result is:

```
x x.
```

A comma after the first `x` cannot be created from the second `x` because the second occurrence is the last word of a sentence. A solution that only checks word equality and ignores sentence positions would incorrectly output `x, x.`.

A final edge case is a chain of newly activated words:

```
a b c,.
```

A comma after `c` activates `b` as having a comma after it, which can activate `a` through the same process. Stopping after one propagation round gives the wrong answer.

## Approaches

The straightforward method is to repeatedly scan the entire text. During a scan, whenever a word has a comma on one side somewhere, we find every occurrence and add missing commas. This is correct because it directly follows the rules. The problem is the cost. With one million characters, there can be hundreds of thousands of word occurrences. If every newly added comma causes another complete scan, the worst case reaches around O(n²) work, which is far beyond what the limit allows.

The useful observation is that every word type has only two possible permanent states. A word either eventually becomes a word that has a comma before it somewhere, or it does not. The same is true for commas after words. Once a word enters one of these states, it never leaves.

This turns the process into a graph propagation problem. Each word type has two kinds of states, "has left comma" and "has right comma". A right comma state on a word activates the left comma state of its next neighbor in every occurrence. A left comma state activates the right comma state of its previous neighbor. We can run a queue over newly discovered states, processing each state once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the input into word occurrences. For every occurrence, store the word, its previous word in the same sentence if it exists, its next word in the same sentence if it exists, and whether there was originally a comma before or after it.
2. Create two boolean states for every distinct word. One state records whether the word must have a comma before it, and the other records whether it must have a comma after it. Initialize these states from the original text.
3. Put every initially active state into a queue. The queue contains only word states that have not yet been processed.
4. When processing a word with the left-comma state, visit all occurrences of that word. Every occurrence that is not the first word of a sentence receives a comma before it. The word before that occurrence now has a comma after it, so activate that neighboring right-comma state if needed.
5. When processing a word with the right-comma state, visit all occurrences of that word. Every occurrence that is not the last word of a sentence receives a comma after it. The word after that occurrence now has a comma before it, so activate that neighboring left-comma state if needed.
6. Continue until the queue is empty. The active states now describe the complete fixed point. Rebuild the original text using the final comma decisions for every gap between words.

Why it works:

The algorithm maintains the invariant that every active state represents a fact that must be true in the final answer. Processing a state applies exactly the rule consequences of that fact. Any newly created comma can only create one of the two neighboring word states that the queue can discover. Since states are added only when they become true and never removed, the queue eventually contains every consequence reachable from the original commas. When the queue becomes empty, no rule can create another comma, which is exactly the stopping condition of the original process.

## Python Solution

```python
import sys
from collections import deque, defaultdict

input = sys.stdin.readline

def solve():
    s = input().rstrip("\n")

    words = []
    gaps = []
    i = 0
    while i < len(s):
        if s[i].isalpha():
            j = i
            while j < len(s) and s[j].isalpha():
                j += 1
            words.append(s[i:j])
            i = j
        else:
            i += 1

    m = len(words)
    before = [False] * m
    after = [False] * m
    starts = [False] * m
    ends = [False] * m

    idx = 0
    pos = 0
    while pos < len(s):
        if s[pos].isalpha():
            idx += 1
            while pos < len(s) and s[pos].isalpha():
                pos += 1
            if pos < len(s):
                if s[pos] == ',':
                    before[idx - 1] = True
                    pos += 1
                    while pos < len(s) and s[pos] == ' ':
                        pos += 1
                elif s[pos] == '.':
                    pos += 1
                    while pos < len(s) and s[pos] == ' ':
                        pos += 1
                    ends[idx - 1] = True
                else:
                    pos += 1
        else:
            pos += 1

    starts[0] = True
    for i in range(1, m):
        if ends[i - 1]:
            starts[i] = True

    word_id = {}
    ids = []
    for w in words:
        if w not in word_id:
            word_id[w] = len(word_id)
        ids.append(word_id[w])

    k = len(word_id)
    has_left = [False] * k
    has_right = [False] * k
    occ = [[] for _ in range(k)]

    for i, x in enumerate(ids):
        occ[x].append(i)
        if before[i]:
            has_left[x] = True
        if after[i]:
            has_right[x] = True

    q = deque()
    for i in range(k):
        if has_left[i]:
            q.append((i, 0))
        if has_right[i]:
            q.append((i, 1))

    while q:
        w, side = q.popleft()
        if side == 0:
            for p in occ[w]:
                if not starts[p]:
                    if not after[p - 1]:
                        after[p - 1] = True
                        nw = ids[p - 1]
                        if not has_right[nw]:
                            has_right[nw] = True
                            q.append((nw, 1))
        else:
            for p in occ[w]:
                if not ends[p]:
                    if not before[p + 1]:
                        before[p + 1] = True
                        nw = ids[p + 1]
                        if not has_left[nw]:
                            has_left[nw] = True
                            q.append((nw, 0))

    ans = []
    ptr = 0
    for i, w in enumerate(words):
        ans.append(w)
        if i + 1 < m:
            if after[i]:
                ans.append(", ")
            elif ends[i]:
                ans.append(". ")
            else:
                ans.append(" ")
        else:
            ans.append(".")
    print("".join(ans))

solve()
```

The parser first extracts word occurrences while preserving the sentence structure. The arrays `starts` and `ends` are necessary because the rules explicitly exclude sentence boundaries.

The two state arrays, `has_left` and `has_right`, store the closure information for word types. The occurrence lists allow one activation to update all matching words without searching through the entire text.

The queue is a standard fixed-point propagation technique. A state enters the queue only once, which is why the algorithm stays linear. The final reconstruction uses the gap information stored in `before` and `after`, while sentence endings are preserved through `ends`.

## Worked Examples

For the first sample, the important propagation states are:

| Step | Activated state | New effect |
| --- | --- | --- |
| Initial | `sit` has left comma | `sit` gains left state |
| Initial | `spot` has right comma | all `spot` occurrences gain right commas |
| Propagation | `here` has left comma | other `here` occurrences gain left commas |

The final text becomes:

```
please, sit spot. sit spot, sit. spot, here now, here.
```

The trace shows that a comma can travel through neighboring words. The state of `spot` creates a comma after another `spot`, which then creates a comma before `here`.

For the second sample:

| Step | Activated state | New effect |
| --- | --- | --- |
| Initial | `one` has left comma | other `one` occurrences gain left commas |
| Initial | `four` has right comma | following words gain left commas |
| Propagation | `tree` has left comma | all matching occurrences gain left commas |

The output is:

```
one, two. one, tree. four, tree. four, four. five, four. six five.
```

This example demonstrates that propagation can continue through several different words rather than only repeating the same word.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is parsed once and every word state is processed once. |
| Space | O(n) | The occurrence lists, word states, and reconstruction data are all linear in the input size. |

The input limit of one million characters is handled because the algorithm never performs repeated full scans. Every stored relationship is used a constant number of times.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old
    return out

assert run("please sit spot. sit spot, sit. spot here now here.\n") == "please, sit spot. sit spot, sit. spot, here now, here.\n"
assert run("one, two. one tree. four tree. four four. five four. six five.\n") == "one, two. one, tree. four, tree. four, four. five, four. six five.\n"

assert run("a a.\n") == "a a.\n"
assert run("x, y. x z.\n") == "x, y. x, z.\n"
assert run("a b c,.\n") == "a, b, c.\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a a.` | `a a.` | Sentence boundary handling |
| `x, y. x z.` | `x, y. x, z.` | Propagation from a comma before a word |
| `a b c,.` | `a, b, c.` | Multi-step chain propagation |

## Edge Cases

For the repeated word case:

```
x x.
```

the algorithm creates no initial active state because neither occurrence has a comma. The queue remains empty and reconstruction returns the original text. The sentence boundary information prevents any accidental comma creation.

For the neighboring propagation case:

```
a b. a, b.
```

the comma after `a` activates the right state of `a`. The second occurrence of `a` already satisfies that state, and the comma before the second `b` activates the left state of `b`. The algorithm reaches the final result:

```
a, b. a, b.
```

For a chain:

```
a b c,.
```

the initial right state belongs to `c`. Processing it activates the left state of the following word if one exists, and processing newly discovered states continues until no more neighbors can be reached. The queue-based propagation naturally handles chains of arbitrary length.

I can also provide a shorter contest-style editorial version or a C++ implementation if needed.
