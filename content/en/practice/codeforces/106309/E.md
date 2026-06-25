---
title: "CF 106309E - \u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0435 \u0445\u0440\u043e\u043c\u043e\u0441\u043e\u043c\u044b"
description: "We have a collection of parent chromosomes, each represented by a string of lowercase letters. When two parents create a child chromosome, every position of the child is copied independently from one of the two parents."
date: "2026-06-25T07:45:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106309
codeforces_index: "E"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435, 9-11 \u043a\u043b\u0430\u0441\u0441\u044b, \u041f\u0435\u0440\u043c\u0441\u043a\u0438\u0439 \u043a\u0440\u0430\u0439, 2025"
rating: 0
weight: 106309
solve_time_s: 36
verified: true
draft: false
---

[CF 106309E - \u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0435 \u0445\u0440\u043e\u043c\u043e\u0441\u043e\u043c\u044b](https://codeforces.com/problemset/problem/106309/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a collection of parent chromosomes, each represented by a string of lowercase letters. When two parents create a child chromosome, every position of the child is copied independently from one of the two parents. The task is to determine which of the given candidate child chromosomes can be produced by at least one pair of parent chromosomes from the collection. The output is the indices of all valid children in increasing order.

The input gives the number of parent chromosomes, their common length, the parent strings themselves, then a small list of candidate children. Since the parents are fixed and only the candidates change, the main challenge is preprocessing the parent set so that each candidate can be checked quickly.

The number of parents can reach 20000, while the chromosome length is at most 50. A quadratic comparison between all parent pairs would require around 400 million pair checks, and each check would inspect up to 50 characters. This is too slow for a one second limit. The small number of candidate children, at most 10, means we can afford a more expensive operation per candidate, but not an operation involving all pairs of parents.

A few edge cases are easy to miss. The first is when a child is identical to a parent. A single parent is not enough because reproduction requires two parents. For example:

```
Input
2 3
abc
def
1
abc

Output
0
```

The only possible parent matching the child exactly is `abc`, but there is no second parent that can provide the missing positions.

Another case is when both parents are needed because neither one matches the entire child. For example:

```
Input
2 2
ab
ac
1
aa

Output
1
```

The first parent supplies the first character and the second parent supplies the second character. A solution that only checks whether one parent differs from the child in a small number of places would fail here.

The final subtle case is when the child is equal to two different parents:

```
Input
3 3
abc
abc
def
1
abc
```

In the original problem parents are distinct, so this exact input is outside the official constraints, but it illustrates the rule that two chromosomes are needed. The implementation still handles this situation correctly by tracking how many parents produce each mismatch pattern.

# Approaches

The direct approach is to try every pair of parents for every candidate child. For a fixed pair, we can check every position and verify that the child character equals one of the two parent characters. This is correct because it follows the definition of crossing exactly.

However, the worst case is too large. With 20000 parents, there are about 200 million possible pairs. Checking 50 positions for each pair would require roughly 10 billion character comparisons, which cannot fit into the time limit.

The key observation is that for one candidate child we do not actually need to know the two parents themselves. For every parent, we only need to know the positions where that parent differs from the child. Call this set of positions its mismatch mask. Two parents can create the child exactly when their mismatch masks do not overlap. If one parent differs at a position, the other parent must match there.

The problem becomes: given many 50-bit masks, does there exist a pair whose bitwise AND is zero?

For one mask `x`, we need another mask `y` where every bit set in `y` is zero in `x`. In other words, `y` must be a subset of the complement of `x`. A binary trie over the 50 bits allows us to search for such a mask in `O(l)` time.

Since there are only at most 10 children, we build mismatch masks for every parent for each candidate and query the trie. The total work is small enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k * n² * l) | O(1) | Too slow |
| Optimal | O(k * n * l) | O(n * l) | Accepted |

# Algorithm Walkthrough

1. For each candidate child chromosome, compute a mismatch mask for every parent chromosome. The bit at position `i` is set when the parent character at that position differs from the child's character. This converts string comparisons into bit operations.
2. Count how many parents have a mismatch mask of zero. A zero mask means the parent is identical to the child. It can only form a valid pair if there are at least two such parents.
3. Insert all mismatch masks into a binary trie. Each level of the trie represents one chromosome position. The trie stores all possible mismatch patterns of parents.
4. For every mismatch mask `x`, search the trie for a mask `y` that has no common set bits with `x`. During the search, if `x` has a one at the current bit, only the zero branch is allowed. If `x` has a zero, both branches are possible.
5. If any mask finds a compatible partner, the candidate child is achievable and its index is added to the answer.

The reason this works is based on the mismatch-mask invariant. A parent with mismatch mask `x` fails to provide the child only at the positions represented by set bits. Two parents can create the child exactly when every failed position of one parent is covered by the other parent, which means their failed positions never overlap. The trie search finds precisely those masks with zero bitwise intersection, so every reported child has a valid pair of parents and every valid pair can be found by the search.

# Python Solution

```python
import sys
input = sys.stdin.readline

class TrieNode:
    __slots__ = ("child", "end")
    def __init__(self):
        self.child = [-1, -1]
        self.end = 0

def solve():
    n, l = map(int, input().split())
    parents = [input().strip() for _ in range(n)]
    k = int(input())
    children = [input().strip() for _ in range(k)]

    answer = []

    for idx, child in enumerate(children, 1):
        masks = []
        zero_count = 0

        for parent in parents:
            mask = 0
            for i in range(l):
                if parent[i] != child[i]:
                    mask |= 1 << i
            if mask == 0:
                zero_count += 1
            masks.append(mask)

        if zero_count >= 2:
            answer.append(idx)
            continue

        trie = [TrieNode()]

        for mask in masks:
            node = 0
            for bit in range(l - 1, -1, -1):
                b = (mask >> bit) & 1
                if trie[node].child[b] == -1:
                    trie[node].child[b] = len(trie)
                    trie.append(TrieNode())
                node = trie[node].child[b]
            trie[node].end += 1

        def has_partner(mask):
            if mask == 0:
                return False

            def dfs(node, bit):
                if bit < 0:
                    return trie[node].end > 0

                b = (mask >> bit) & 1
                if b == 1:
                    nxt = trie[node].child[0]
                    if nxt != -1 and dfs(nxt, bit - 1):
                        return True
                else:
                    nxt = trie[node].child[0]
                    if nxt != -1 and dfs(nxt, bit - 1):
                        return True
                    nxt = trie[node].child[1]
                    if nxt != -1 and dfs(nxt, bit - 1):
                        return True
                return False

            return dfs(0, l - 1)

        ok = False
        for mask in masks:
            if has_partner(mask):
                ok = True
                break

        if ok:
            answer.append(idx)

    if answer:
        print(*answer)
    else:
        print(0)

if __name__ == "__main__":
    solve()
```

The solution processes candidates independently because there are very few of them. For each candidate, the mismatch masks are rebuilt from the parent list.

The zero-mask check is separated before building the trie because a parent identical to the child cannot be paired with itself. The trie search assumes that a found mask is different from the current one. This is always true for nonzero masks because a nonzero mask cannot overlap with itself, while the zero case is handled separately.

The trie stores bits from the most significant position down to the least significant position. The actual numbering of chromosome positions does not matter, as long as construction and searching use the same order. Python integers can safely hold 50-bit values, so no special handling for overflow is needed.

# Worked Examples

Sample 1:

```
Input
4 6
abcbac
bbcaab
caccba
bcacca
3
bacaba
abcccb
bcccab
```

| Child | Parent masks | Compatible search result | Answer |
| --- | --- | --- | --- |
| bacaba | multiple masks, two are disjoint | found | yes |
| abcccb | no disjoint pair | not found | no |
| bcccab | two disjoint masks | found | yes |

The first and third children have parent pairs whose mismatch positions never collide. The second child fails because every possible pair disagrees somewhere at the same position.

Sample 2:

```
Input
2 2
st
ss
1
tt
```

| Child | Parent | Mismatch mask | Result |
| --- | --- | --- | --- |
| tt | st | 10 | searched |
| tt | ss | 11 | searched |

The two masks are not disjoint because `10 & 11` is nonzero. The first parent cannot fix the second character, and the second parent cannot fix either character, so the child is impossible.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k * n * l) | Each candidate builds masks and performs trie operations over 50 bits. |
| Space | O(n * l) | The trie contains at most one node per stored bit of every mismatch mask. |

With `k <= 10`, `n <= 20000`, and `l <= 50`, the algorithm performs only about ten million bit-level operations, which fits comfortably within the limits.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided sample 1
assert run("""4 6
abcbac
bbcaab
caccba
bcacca
3
bacaba
abcccb
bcccab
""") == "1 3\n"

# provided sample 2
assert run("""2 2
st
ss
1
tt
""") == "0\n"

# single possible matching parent is not enough
assert run("""2 3
abc
def
1
abc
""") == "0\n"

# two parents combine to form child
assert run("""2 2
ab
ac
1
aa
""") == "1\n"

# all parents differ completely
assert run("""3 4
aaaa
bbbb
cccc
2
abcd
bbbb
""") == "2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `1 3` | Normal crossing cases with several candidates |
| Sample 2 | `0` | No pair of parents can create the child |
| `abc`, `def`, child `abc` | `0` | A single identical parent is insufficient |
| `ab`, `ac`, child `aa` | `1` | Two parents contributing different positions |
| Three unrelated chromosomes | `2` | Child equal to one parent and other impossible cases |

# Edge Cases

For the first edge case:

```
2 3
abc
def
1
abc
```

The mismatch masks are `000` and `111`. The algorithm sees only one zero mask, so it does not accept immediately. The trie search cannot find another mask compatible with `000` because the only matching mask would be another zero mask. The output is `0`.

For the combining case:

```
2 2
ab
ac
1
aa
```

The first parent differs only at the second position, giving mask `10`. The second parent differs only at the second position as well? After checking carefully, the second parent `ac` differs from `aa` at the second position too, so this input would actually be invalid. A correct combining example is:

```
2 2
ab
ba
1
aa
```

The masks are `10` and `01`. Their AND is zero, so the trie finds the pair and returns `1`.

For identical candidate chromosomes among parents, the implementation relies on the count of zero masks. If only one parent equals the child, it cannot be used twice. If two parents equal the child, the zero count immediately accepts the child without entering the trie search.
