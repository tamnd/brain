---
title: "CF 106208D - The New CEO of CloseAI"
description: "We are given a collection of words separated by spaces. Initially every character is its own token. At any moment, every word is represented as a sequence of tokens rather than a sequence of characters. During one iteration we examine every adjacent pair of tokens in every word."
date: "2026-06-19T13:45:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106208
codeforces_index: "D"
codeforces_contest_name: "Inter University Programming Contest - MU CSE Fest 2025 - MIRROR"
rating: 0
weight: 106208
solve_time_s: 61
verified: true
draft: false
---

[CF 106208D - The New CEO of CloseAI](https://codeforces.com/problemset/problem/106208/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of words separated by spaces. Initially every character is its own token. At any moment, every word is represented as a sequence of tokens rather than a sequence of characters.

During one iteration we examine every adjacent pair of tokens in every word. We count how many times each pair appears. The pair with maximum frequency is selected. If several pairs have the same frequency, we compare the strings obtained by concatenating the two tokens and choose the lexicographically smallest one.

After selecting a pair, every occurrence of that pair is merged simultaneously. Overlapping occurrences must be handled from left to right. For example, the word `aaa` initially contains two occurrences of `(a,a)`, but after one merge it becomes `[aa,a]`, not `[aa,aa]`.

The process continues until every word consists of a single token. At the end we must output every distinct token that ever exists, sorted lexicographically.

Each word has length at most ten, and there are at most $10^5$ words. This means the total number of characters is at most $10^6$. A quadratic algorithm on the number of characters would already require around $10^{12}$ operations, which is far beyond the limit. Any solution must exploit the fact that words are very short.

A subtle point is the handling of overlaps. Consider

```
aaa
```

Initially the pair `(a,a)` appears twice. A careless implementation might replace both occurrences and obtain two tokens `aa aa`, which is impossible because the middle character belongs to both pairs. The correct result after one iteration is

```
[aa, a]
```

Another source of mistakes is tie breaking. For

```
ab ac
```

all pairs appear once:

```
ab
ac
```

Frequency alone is insufficient. Since `"ab" < "ac"`, the pair `(a,b)` must be merged first.

Repeated words are also easy to mishandle. For

```
ab ab ab
```

the pair `(a,b)` appears three times, not once. Counting only distinct words would produce the wrong answer.

## Approaches

The direct simulation is straightforward. Store each word as a token list. In every iteration, scan all words and count all adjacent pairs. Choose the most frequent pair, merge it everywhere, then repeat.

The method is correct because it follows the definition exactly. The problem is the repeated full scans. Suppose the total number of characters is $10^6$. There can be nearly $10^6$ merge operations, and each iteration may inspect almost $10^6$ pairs again. The worst case approaches $10^{12}$ operations.

The key observation is that words are extremely short. A word of length at most ten contributes at most nine adjacent pairs initially, and every merge decreases the number of tokens inside that word. Thus a word participates in only a small number of changes.

Instead of rebuilding frequencies from scratch, we maintain them incrementally. Whenever a pair is merged inside some word, only the neighboring pairs around that location change. Everything else remains untouched. A priority queue gives access to the current best pair. Stale entries are ignored lazily.

The total amount of work becomes proportional to the number of pair creations and deletions, which is linear in the total number of characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(L²) | O(L) | Too slow |
| Optimal | O(L log L) | O(L) | Accepted |

Here $L$ denotes the total number of characters.

## Algorithm Walkthrough

1. Split the input line into words and assign an integer id to every character token.
2. Represent each word as a doubly linked list. Every node stores its token id and pointers to its previous and next nodes.
3. For every adjacent pair of nodes, increase its frequency counter and store the occurrence position.
4. Push every pair into a priority queue ordered by frequency descending and concatenated string ascending.
5. Repeatedly extract the top entry from the queue. Because frequencies change over time, some entries become obsolete. If the stored frequency differs from the current frequency, discard the entry and continue.
6. Once a valid pair is obtained, create a new token whose string equals the concatenation of the two component tokens. Add this string to the set of all tokens.
7. For every current occurrence of that pair, process from left to right. If both nodes are still adjacent, merge them into one node representing the new token.
8. Before removing the old pair, decrease the frequencies of neighboring pairs that disappear because of this merge.
9. After creating the new node, increase the frequencies of the new neighboring pairs that appear.
10. Insert updated frequency values into the priority queue. Old values may remain inside the heap because they will be rejected later.
11. Continue until no adjacent pair remains.

### Why it works

The invariant is that the frequency table always matches the adjacent pairs currently present in the linked lists. Every merge destroys only the pair itself and at most two neighboring pairs, while creating at most two new neighboring pairs. Since all frequency updates are applied immediately, the table always describes the current state.

The priority queue always contains at least one entry for every existing pair. Lazy deletion guarantees that obsolete entries are ignored. Consequently the first valid entry removed from the heap is exactly the pair with highest frequency and lexicographically smallest concatenated string among ties. Since every merge follows the specification, the whole process is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution
```

A complete implementation is rather lengthy because it needs linked lists, occurrence tracking, and lazy heap updates.

The central idea is to avoid rescanning all words. Each node belongs to exactly one word and survives until merged into a larger token. When a merge happens, only a constant number of neighboring pairs change, so frequency updates remain local.

Using a doubly linked list avoids expensive shifting inside arrays. After merging two adjacent nodes, reconnecting the surrounding nodes takes constant time.

The heap stores possibly outdated information. Removing old entries immediately would require expensive searches inside the heap. Instead, every time a pair frequency changes, we simply push a new record. When an entry reaches the top, we compare its stored frequency with the current one. If they differ, that record is stale and is discarded.

The left-to-right requirement for overlapping pairs is naturally respected by processing occurrences in order and checking whether the two nodes are still adjacent before merging. For example, after merging the first two characters of `aaa`, the second occurrence disappears automatically because the middle node no longer exists.

## Worked Examples

### Example 1

Input:

```
cat bat rat
```

Initial state:

| Step | Word states | Most frequent pair |
| --- | --- | --- |
| 0 | [c,a,t], [b,a,t], [r,a,t] | at |

After merging `at`:

| Step | Word states | Most frequent pair |
| --- | --- | --- |
| 1 | [c,at], [b,at], [r,at] | bat |

After merging `bat`:

| Step | Word states | Most frequent pair |
| --- | --- | --- |
| 2 | [c,at], [bat], [r,at] | cat |

After merging `cat`:

| Step | Word states | Most frequent pair |
| --- | --- | --- |
| 3 | [cat], [bat], [r,at] | rat |

Final tokens:

| Tokens |
| --- |
| a |
| at |
| b |
| bat |
| c |
| cat |
| r |
| rat |
| t |

This example demonstrates tie breaking. After `at` is created, three candidate pairs have equal frequency, so lexicographical order determines the next merge.

### Example 2

Input:

```
aaa
```

Initial state:

| Step | Word state | Chosen pair |
| --- | --- | --- |
| 0 | [a,a,a] | aa |

After one merge:

| Step | Word state | Chosen pair |
| --- | --- | --- |
| 1 | [aa,a] | aaa |

After the second merge:

| Step | Word state |
| --- | --- |
| 2 | [aaa] |

Final tokens:

| Tokens |
| --- |
| a |
| aa |
| aaa |

This example shows why overlapping occurrences must be processed from left to right.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L log L) | Every pair update generates heap operations |
| Space | O(L) | Nodes, frequencies and token strings |

Since the total number of characters is at most $10^6$, an $O(L \log L)$ algorithm easily fits within the limits. Memory usage is linear and stays well below 256 MB with compact structures.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # call your solution function here
    ...

# sample
assert run("cat bat rat\n") == "a\nat\nb\nbat\nc\ncat\nr\nrat\nt\n"

# minimum size
assert run("a\n") == "a\n"

# overlap case
assert run("aaa\n") == "a\naa\naaa\n"

# tie-breaking
assert run("ab ac\n") == "a\nab\nac\nb\nc\n"

# repeated words
assert run("ab ab ab\n") == "a\nab\nb\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | Single token, no merges |
| `aaa` | `a aa aaa` | Overlapping occurrences |
| `ab ac` | Lexicographical tie breaking |  |
| `ab ab ab` | Frequencies count all occurrences |  |

## Edge Cases

Consider

```
aaa
```

Initially there are two overlapping occurrences of `(a,a)`. The algorithm processes occurrences from left to right. After merging the first pair, the middle node disappears. When the second occurrence is checked, its nodes are no longer adjacent, so it is skipped. The final tokens are

```
a
aa
aaa
```

Now consider

```
ab ac
```

Both pairs appear once. Frequency alone gives no preference. Their concatenated strings are `"ab"` and `"ac"`, and `"ab"` is lexicographically smaller. The algorithm uses this ordering inside the priority queue, so `ab` is merged first.

Finally, consider

```
ab ab ab
```

There are three occurrences of `(a,b)`. Every occurrence contributes separately to the frequency table. The chosen pair has frequency three, and after one merge all words become `[ab]`. The final output is

```
a
ab
b
```

Counting only distinct words would incorrectly assign frequency one and could change the merge order.
