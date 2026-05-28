---
title: "CF 70B - Text Messaging"
description: "We are given the maximum length of a single SMS message and one complete text consisting of sentences separated by spaces. A sentence always ends with one of ., ?, or !. Words contain only letters."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "expression-parsing", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 70
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 64"
rating: 1600
weight: 70
solve_time_s: 99
verified: true
draft: false
---

[CF 70B - Text Messaging](https://codeforces.com/problemset/problem/70/B)

**Rating:** 1600  
**Tags:** expression parsing, greedy, strings  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the maximum length of a single SMS message and one complete text consisting of sentences separated by spaces. A sentence always ends with one of `.`, `?`, or `!`. Words contain only letters.

The task is to split the text into the minimum possible number of messages such that no sentence is broken across messages. A message may contain several consecutive sentences if they fit within the length limit. When two consecutive sentences are placed into different messages, the separating space disappears because Fangy simply does not type it.

This detail about spaces is the entire trick of the problem. Inside one message, the original spaces must stay. Between two different messages, the separating space can be omitted.

The text length is at most `10^4`, which is small enough for linear or quadratic processing. Since the message limit `n` is at most `255`, checking sentence lengths is trivial. A cubic solution would already be risky because repeatedly rebuilding substrings or recomputing lengths could push the operation count into tens or hundreds of millions. A clean greedy or dynamic programming solution is more appropriate.

The first important edge case is when a single sentence is already longer than the message limit.

Input:

```
5
Hello!
```

The sentence `"Hello!"` has length `6`, so no valid split exists.

Correct output:

```
Impossible
```

A careless implementation might only check combined message lengths and forget to validate individual sentences.

Another subtle case is the disappearing space between messages.

Input:

```
7
Hi. Bye.
```

The whole text has length `8`, but it can still be sent in two messages:

`"Hi."` and `"Bye."`

Correct output:

```
2
```

An implementation that always counts spaces between sentences would incorrectly think this is impossible.

One more tricky situation appears when several short sentences together exceed the limit by exactly one separating space.

Input:

```
10
Hi. Hello.
```

`"Hi. Hello."` has length `10`, so it fits into one message.

If the limit were `9`, we would need two messages because the internal space must remain when both sentences stay together.

Correct output for `n = 9`:

```
2
```

This distinction between internal spaces and removed boundary spaces is where many off-by-one bugs happen.

## Approaches

The brute-force idea is straightforward. First split the text into sentences. Then try every possible grouping of consecutive sentences into messages and compute the minimum number of messages with dynamic programming.

Suppose there are `k` sentences. A naive DP could define `dp[i]` as the minimum number of messages needed for the first `i` sentences. For every `i`, we try every previous position `j` and check whether sentences `j...i-1` fit into one message.

The expensive part is repeatedly computing the length of a group. If we rebuild substrings or recount spaces every time, each transition may cost `O(k)`, producing an `O(k^3)` solution. With around `10^4` characters, the number of sentences can also be large enough for this to become too slow.

The key observation is that sentence lengths are all we actually need. Once the text is parsed into sentence lengths, checking whether several consecutive sentences fit together becomes a simple arithmetic expression.

Assume the sentence lengths are:

```
len[0], len[1], ..., len[k-1]
```

If we place sentences `l...r` into one message, the total length becomes:

```
sum(len[l...r]) + (r - l)
```

The extra `(r - l)` comes from spaces between consecutive sentences inside the same message. Spaces between different messages disappear and are not counted.

Now the problem becomes much simpler. We only need to partition the sequence into the fewest groups such that each group's total length does not exceed `n`.

At this point, greedy becomes natural. Starting from the current sentence, we should pack as many consecutive sentences as possible into the current message. Leaving unused space can never help later because all future sentences must still be placed somewhere. Taking the maximal valid prefix minimizes the number of groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k³) | O(k) | Too slow |
| Optimal | O( | text | ) |

## Algorithm Walkthrough

1. Parse the text and extract every sentence length.

We scan the string character by character. Every time we encounter `.`, `?`, or `!`, we finish one sentence. The sentence length includes every character from its beginning up to and including the punctuation mark.
2. Check whether any individual sentence length exceeds `n`.

If even one sentence is too large, no valid arrangement exists because sentences cannot be split across messages.
3. Start building messages greedily.

Maintain the current message length and the number of messages used so far.
4. Place the first sentence into the current message.

Since we already verified that every sentence individually fits, this is always possible.
5. For each next sentence, determine whether it can join the current message.

If the current message already contains something, adding another sentence requires one extra space. So the added cost becomes:

```
1 + next_sentence_length
```
6. If the new total does not exceed `n`, append the sentence to the current message.

This keeps the number of messages unchanged while maximizing usage of the current one.
7. Otherwise, start a new message with this sentence.

The separating space disappears because the sentences are now in different messages.
8. After processing all sentences, output the number of messages used.

### Why it works

The greedy choice is optimal because messages contain only consecutive sentences. Suppose the current message can still fit another sentence. Splitting earlier instead of adding that sentence only wastes available space and cannot create additional future opportunities. Every later sentence must still appear after the current one, so delaying the split never increases the required number of messages.

The algorithm maintains the invariant that the current message contains the maximum possible number of consecutive sentences that fit within the limit. Because each message is maximally packed, the total number of messages is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    text = input().rstrip()

    sentences = []

    start = 0

    for i, ch in enumerate(text):
        if ch in ".?!":
            sentences.append(i - start + 1)

            if i + 1 < len(text):
                start = i + 2

    for length in sentences:
        if length > n:
            print("Impossible")
            return

    messages = 1
    current = sentences[0]

    for length in sentences[1:]:
        if current + 1 + length <= n:
            current += 1 + length
        else:
            messages += 1
            current = length

    print(messages)

solve()
```

The first part scans the text and extracts sentence lengths. The variable `start` stores the index where the current sentence begins. Whenever punctuation is found, the sentence length is simply:

```
i - start + 1
```

After a sentence ends, the next sentence starts two positions later because the grammar guarantees exactly one separating space between consecutive sentences.

The second loop checks feasibility. This must happen before the greedy packing phase because a single oversized sentence immediately makes the task impossible.

The greedy construction keeps only the current message length. When appending another sentence, we add one extra character for the internal space:

```
current + 1 + length
```

This space is counted only when two sentences stay inside the same message. Starting a new message resets the length to the new sentence alone.

One subtle boundary condition is the initialization:

```
messages = 1
current = sentences[0]
```

The text is guaranteed to contain at least one sentence, so this is always safe.

## Worked Examples

### Example 1

Input:

```
25
Hello. I am a little walrus.
```

Extracted sentence lengths:

```
[6, 21]
```

| Step | Current Sentence Length | Current Message Length | Action | Messages |
| --- | --- | --- | --- | --- |
| Start | 6 | 6 | Begin first message | 1 |
| Next | 21 | 6 | `6 + 1 + 21 = 28 > 25`, start new message | 2 |

Final answer:

```
2
```

This trace shows why the separating space matters. The combined length becomes `28` because both sentences would require one internal space if kept together.

### Example 2

Input:

```
7
Hi. Bye.
```

Extracted sentence lengths:

```
[3, 4]
```

| Step | Current Sentence Length | Current Message Length | Action | Messages |
| --- | --- | --- | --- | --- |
| Start | 3 | 3 | Begin first message | 1 |
| Next | 4 | 3 | `3 + 1 + 4 = 8 > 7`, start new message | 2 |

Final answer:

```
2
```

This example demonstrates the rule that spaces vanish between messages. Although the original text length is `8`, two separate messages are valid because the separating space is omitted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | text |
| Space | O(k) | Stores sentence lengths for `k` sentences |

The input length is at most `10^4`, so a linear scan is extremely fast. Memory usage is also tiny because we only store one integer per sentence.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    text = input().rstrip()

    sentences = []

    start = 0

    for i, ch in enumerate(text):
        if ch in ".?!":
            sentences.append(i - start + 1)

            if i + 1 < len(text):
                start = i + 2

    for length in sentences:
        if length > n:
            return "Impossible"

    messages = 1
    current = sentences[0]

    for length in sentences[1:]:
        if current + 1 + length <= n:
            current += 1 + length
        else:
            messages += 1
            current = length

    return str(messages)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("25\nHello. I am a little walrus.\n") == "2", "sample 1"

# impossible because one sentence is too long
assert run("5\nHello!\n") == "Impossible", "single oversized sentence"

# exactly fits into one message
assert run("10\nHi. Hello.\n") == "1", "boundary fit"

# requires split because of one extra space
assert run("9\nHi. Hello.\n") == "2", "space handling"

# minimum size style case
assert run("2\nA.\n") == "1", "smallest valid sentence"

# many short sentences
assert run("3\nA. B. C.\n") == "3", "every sentence isolated"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 / Hello!` | `Impossible` | Detects oversized sentence |
| `10 / Hi. Hello.` | `1` | Exact boundary fit |
| `9 / Hi. Hello.` | `2` | Internal spaces counted correctly |
| `2 / A.` | `1` | Smallest valid input |
| `3 / A. B. C.` | `3` | Frequent message splitting |

## Edge Cases

Consider the impossible case:

```
5
Hello!
```

The parser extracts one sentence of length `6`. Since `6 > 5`, the algorithm immediately prints:

```
Impossible
```

No greedy packing happens because the input is already invalid.

Now consider the disappearing-space scenario:

```
7
Hi. Bye.
```

The extracted sentence lengths are `[3, 4]`.

The algorithm first places `"Hi."` into the current message. When trying to append `"Bye."`, the required length becomes:

```
3 + 1 + 4 = 8
```

This exceeds the limit, so a new message is started. The separating space between messages is not counted anymore, producing exactly two valid messages.

Finally, examine the boundary condition:

```
10
Hi. Hello.
```

The lengths are `[3, 6]`.

Appending the second sentence gives:

```
3 + 1 + 6 = 10
```

Since equality is allowed, both sentences stay together in one message. This confirms that the algorithm handles exact fits correctly without off-by-one mistakes.
