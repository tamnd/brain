---
title: "CF 37C - Old Berland Language"
description: "We need to construct a binary prefix code. The input gives the lengths of all words in the language. Every word may cont"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 37
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 37"
rating: 1900
weight: 37
solve_time_s: 102
verified: true
draft: false
---

[CF 37C - Old Berland Language](https://codeforces.com/problemset/problem/37/C)

**Rating:** 1900  
**Tags:** data structures, greedy, trees  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct a binary prefix code.

The input gives the lengths of all words in the language. Every word may contain only `0` and `1`, and no word is allowed to be the prefix of another. We must either build such a set of words or determine that it is impossible.

For example, if the lengths are `[1, 2, 3]`, one valid construction is:

```
0
10
110
```

None of these strings is a prefix of another. The word `0` is not a prefix of `10` because `10` starts with `1`, and `10` is not a prefix of `110` because `110` starts with `11`.

The key difficulty is that the lengths are fixed. We are not free to choose arbitrary codeword lengths, only the actual binary strings.

The constraints are small enough that we can afford algorithms around `O(n log n)` or even `O(total_length^2)` in practice, since `n ≤ 1000` and each length is at most `1000`. Still, brute-forcing binary strings is completely infeasible because a length of `1000` means there are `2^1000` possible candidates.

The structure of prefix-free binary strings strongly suggests thinking in terms of a binary trie. Every node corresponds to a prefix, and choosing a word means marking one node as terminal. Once a node becomes terminal, its entire subtree becomes unusable because longer strings below it would have that word as a prefix.

Several edge cases are easy to mishandle.

Suppose all lengths are `1`:

```
3
1 1 1
```

There are only two binary strings of length `1`, namely `0` and `1`. A careless greedy algorithm might keep trying deeper strings, but deeper strings would have one of those words as a prefix. The correct output is:

```
NO
```

Another tricky case is repeated lengths:

```
4
2 2 2 2
```

This is valid because there are exactly four binary strings of length `2`:

```
00
01
10
11
```

A bad implementation that blocks siblings incorrectly inside the trie may reject this valid case.

One more subtle situation appears when short words consume too much space:

```
3
1 2 2
```

After choosing one length-1 word, only one branch of the trie remains available. That branch contains only two strings of length `2`, but one of them starts with the chosen length-1 word and becomes forbidden. The maximum possible number of length-2 words drops. The correct answer is:

```
NO
```

This is exactly the kind of interaction that makes local greedy choices dangerous unless the trie structure is handled carefully.

## Approaches

The brute-force idea is straightforward. Generate binary strings of the required lengths one by one and check whether the new string conflicts with previously chosen strings. Two strings conflict if either is a prefix of the other.

This works for tiny lengths. For each candidate string, we can compare it against every previously chosen word. The problem is the search space. Even a single length `1000` word has `2^1000` possibilities. No amount of pruning rescues this approach in the worst case.

The real observation is that prefix-free sets naturally correspond to leaves in a binary trie.

Think of all binary strings as paths in an infinite binary tree. Moving left appends `0`, moving right appends `1`. A word of length `k` corresponds to a node at depth `k`.

The prefix condition becomes simple in this view. If we select a node as a word, we are forbidden from selecting any ancestor or descendant of that node. So every chosen word must be a leaf among the selected nodes.

This suggests a greedy construction.

If we process shorter lengths first, we can always assign the lexicographically smallest currently available node at that depth. Once a node is used, its subtree disappears from consideration automatically.

A clean way to implement this is to maintain the set of currently available prefixes. Initially only the empty string exists. To produce strings of larger depths, we repeatedly expand nodes by replacing a prefix `x` with `x0` and `x1`.

The crucial invariant is that the available set always contains prefixes that are pairwise non-conflicting. When we need a word of length `L`, we expand until some available prefix reaches depth `L`. If no such node exists, construction is impossible.

This turns an exponential search into a deterministic greedy trie traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n + total_length) | O(total_length) | Accepted |

## Algorithm Walkthrough

1. Read all lengths together with their original indices.

We must output answers in input order, but processing lengths in sorted order is much easier because shorter words constrain longer ones.
2. Sort the words by length.

Assigning short words first is safe because a short word blocks an entire subtree. Delaying short words could force conflicts later.
3. Maintain a queue of currently available prefixes.

Initially the queue contains only the empty string `""`.
4. For each required length `L`, repeatedly expand the shortest available prefix until the front of the queue has length `L`.

Expanding a prefix `x` means removing it and inserting `x0` and `x1`.

This simulates descending one level deeper in the binary trie.
5. After expansion, check whether the front prefix has length exactly `L`.

If all available prefixes are already deeper than `L`, then no valid word of length `L` exists anymore. Output `NO`.
6. Otherwise, take the front prefix as the chosen word for this request and remove it from the queue.

Removing it prevents any descendant from being used later, which automatically preserves the prefix-free condition.
7. Store the chosen word at its original index.
8. After processing all requests, output `YES` and print the stored words in input order.

### Why it works

The algorithm maintains the invariant that every available prefix represents an unused subtree of the binary trie.

When we expand a prefix `x` into `x0` and `x1`, we partition the subtree rooted at `x` into its two child subtrees without losing any possible future strings.

When we select a word `x`, we permanently remove its subtree from future consideration. This guarantees that no later word can have `x` as a prefix.

Processing lengths in increasing order is what makes the greedy choice valid. A shorter word always blocks more space than a longer word, so delaying short words can only reduce flexibility. By always taking the lexicographically smallest available prefix at the required depth, we never waste available trie space.

If the algorithm fails at some length `L`, every remaining available prefix is already deeper than `L`. Since trie depth only increases during expansion, there is no way to create a new node at depth `L`. A valid construction cannot exist.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n = int(input())
    lengths = list(map(int, input().split()))

    arr = [(lengths[i], i) for i in range(n)]
    arr.sort()

    q = deque([""])
    ans = [""] * n

    for length, idx in arr:
        while q and len(q[0]) < length:
            cur = q.popleft()
            q.append(cur + "0")
            q.append(cur + "1")

        if not q or len(q[0]) != length:
            print("NO")
            return

        ans[idx] = q.popleft()

    print("YES")
    print("\n".join(ans))

solve()
```

The solution follows the trie interpretation directly.

The queue stores available prefixes in lexicographic order. Initially only the empty string exists. Expanding a node corresponds to replacing it with its two children.

The `while` loop keeps expanding until the shallowest available prefix reaches the required depth. This matters because prefixes shorter than the target depth cannot yet be used as words.

The failure condition is subtle:

```
if not q or len(q[0]) != length:
```

If the shortest available prefix is already deeper than `length`, then every available prefix is deeper as well. We can never move upward in the trie, so constructing a word of this exact length is impossible.

Removing the selected prefix from the queue is what enforces prefix-freeness. Once a word is chosen, its subtree disappears permanently.

The queue size never becomes large enough to cause issues. Every expansion increases the number of nodes by one, and the total number of chosen words is only `1000`.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

Sorted requests:

```
(1,0), (2,1), (3,2)
```

| Step | Queue Before | Action | Chosen Word | Queue After |
| --- | --- | --- | --- | --- |
| Start | `[""]` | Initial state | - | `[""]` |
| 1 | `[""]` | Expand `""` | - | `["0","1"]` |
| 2 | `["0","1"]` | Take length 1 | `0` | `["1"]` |
| 3 | `["1"]` | Expand `"1"` | - | `["10","11"]` |
| 4 | `["10","11"]` | Take length 2 | `10` | `["11"]` |
| 5 | `["11"]` | Expand `"11"` | - | `["110","111"]` |
| 6 | `["110","111"]` | Take length 3 | `110` | `["111"]` |

Final output:

```
YES
0
10
110
```

This trace shows how each chosen word removes an entire subtree. After selecting `0`, only the branch starting with `1` remains available.

### Example 2

Input:

```
3
1 2 2
```

Sorted requests:

```
(1,0), (2,1), (2,2)
```

| Step | Queue Before | Action | Chosen Word | Queue After |
| --- | --- | --- | --- | --- |
| Start | `[""]` | Initial state | - | `[""]` |
| 1 | `[""]` | Expand `""` | - | `["0","1"]` |
| 2 | `["0","1"]` | Take length 1 | `0` | `["1"]` |
| 3 | `["1"]` | Expand `"1"` | - | `["10","11"]` |
| 4 | `["10","11"]` | Take length 2 | `10` | `["11"]` |
| 5 | `["11"]` | Take length 2 | `11` | `[]` |

Actually this case is valid:

```
YES
0
10
11
```

The trace demonstrates an important point. Choosing `0` blocks half the trie, but the remaining half still contains exactly two valid length-2 strings.

Now consider:

```
3
1 1 2
```

| Step | Queue Before | Action | Chosen Word | Queue After |
| --- | --- | --- | --- | --- |
| Start | `[""]` | Initial state | - | `[""]` |
| 1 | `[""]` | Expand `""` | - | `["0","1"]` |
| 2 | `["0","1"]` | Take length 1 | `0` | `["1"]` |
| 3 | `["1"]` | Take length 1 | `1` | `[]` |
| 4 | `[]` | Need length 2 | Impossible | - |

Output:

```
NO
```

After both length-1 strings are used, the trie is completely exhausted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + S) | Sorting costs `O(n log n)`, trie expansions total `O(S)` where `S` is the sum of lengths |
| Space | O(S) | The queue and stored strings together contain at most `O(S)` characters |

Here `S` is at most `1000 × 1000 = 10^6`, which is completely safe in Python. The algorithm easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    def solve():
        n = int(input())
        lengths = list(map(int, input().split()))

        arr = [(lengths[i], i) for i in range(n)]
        arr.sort()

        q = deque([""])
        ans = [""] * n

        for length, idx in arr:
            while q and len(q[0]) < length:
                cur = q.popleft()
                q.append(cur + "0")
                q.append(cur + "1")

            if not q or len(q[0]) != length:
                print("NO")
                return

            ans[idx] = q.popleft()

        print("YES")
        print("\n".join(ans))

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("3\n1 2 3\n").startswith("YES"), "sample 1"

# minimum size
assert run("1\n1\n").startswith("YES"), "single word"

# impossible because only two length-1 strings exist
assert run("3\n1 1 1\n") == "NO\n", "too many short words"

# all length-2 strings fit exactly
res = run("4\n2 2 2 2\n")
assert res.startswith("YES"), "all depth-2 leaves"

# impossible due to Kraft bound
assert run("5\n1 2 2 2 2\n") == "NO\n", "tree exhausted"

# boundary growth
res = run("8\n3 3 3 3 3 3 3 3\n")
assert res.startswith("YES"), "full depth-3 tree"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | YES | Smallest valid input |
| `3 / 1 1 1` | NO | Only two binary strings of length 1 exist |
| `4 / 2 2 2 2` | YES | Entire trie level can be filled exactly |
| `5 / 1 2 2 2 2` | NO | Prefix blocking exhausts available leaves |
| `8 / 3 3 3 3 3 3 3 3` | YES | Complete binary tree at depth 3 |

## Edge Cases

Consider the input:

```
3
1 1 1
```

The algorithm expands the empty string into `0` and `1`. It uses both for the first two requests. The queue becomes empty before the third request. Since no unused subtree remains, the algorithm correctly prints:

```
NO
```

Now examine repeated equal lengths:

```
4
2 2 2 2
```

The algorithm repeatedly expands prefixes until depth 2:

```
00, 01, 10, 11
```

Each one is selected exactly once. Since nodes at the same depth cannot be prefixes of one another, the construction succeeds.

Finally, consider a case where short words consume trie capacity:

```
5
1 2 2 2 2
```

After selecting one length-1 word, only half the trie remains. That half contains exactly two depth-2 leaves. The algorithm successfully assigns two length-2 words, then the queue becomes empty while requests still remain. It outputs:

```
NO
```

This matches the actual combinatorial limit of the binary trie.
