---
title: "CF 102284D - \u041a\u0440\u0430\u0441\u0438\u0432\u044b\u0435 \u043c\u0435\u043b\u043e\u0434\u0438\u0438"
description: "We have an array of (n) note frequencies. We may choose any nonempty subsequence, so the chosen positions have to remain in their original order, but positions may be skipped."
date: "2026-08-13T08:47:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102284
codeforces_index: "D"
codeforces_contest_name: "\u041b\u041a\u0428 2019, \u0418\u044e\u043b\u044c, \u041c\u0438\u043a\u0441 \u0441\u0442\u0430\u0440\u0448\u0435\u0439 \u0438 \u043c\u043b\u0430\u0434\u0448\u0435\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434"
rating: 0
weight: 102284
solve_time_s: 300
verified: true
draft: false
---

[CF 102284D - \u041a\u0440\u0430\u0441\u0438\u0432\u044b\u0435 \u043c\u0435\u043b\u043e\u0434\u0438\u0438](https://codeforces.com/problemset/problem/102284/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of (n) note frequencies. We may choose any nonempty subsequence, so the chosen positions have to remain in their original order, but positions may be skipped. The subsequence is beautiful when the absolute difference between every two neighboring chosen frequencies is prime.

The task is not merely to count such subsequences. We have to sort all beautiful subsequences lexicographically by their frequency sequences and output the (k)-th one. If the same frequency sequence can be obtained from several different choices of positions, every such occurrence contributes separately to the ordering.

The constraints make a direct enumeration impossible. With (n=1000), there can be (2^{1000}-1) nonempty subsequences, so even generating them would be hopeless. The official statement gives a 2 second time limit and 512 MB memory limit. The useful target is consequently around (O(n^2)), which is about one million array-level operations before accounting for the primality preprocessing.

The value bound of (100000) is large enough that testing primality independently for every pair would be wasteful, but small enough for a sieve. The largest possible difference is also below (100000), so one sieve answers every compatibility query.

There are several edge cases that can silently break an otherwise reasonable solution. The first is the smallest possible array.

For

```
1 1
5
```

the only beautiful subsequence is ((5)), so the output is

```
1
5
```

A solution that includes the empty subsequence in its counting will return the wrong rank, because the problem considers only nonempty subsequences.

Repeated values create another trap. For

```
3 2
7 7 7
```

the only beautiful subsequences are the three singleton occurrences, because a difference of zero is not prime. The second one is therefore

```
1
7
```

A careless implementation that treats zero as a valid prime difference, or one that counts only distinct frequency sequences instead of occurrences, gives a different answer.

The lexicographic treatment of duplicate prefixes is also essential. Consider

```
3 4
1 3 1
```

Both (1)'s can form a singleton, and the difference between (1) and (3) is prime. The ordered list is

[
(1), (1), (1,3), (1,3,1), (3), (3,1).
]

Thus the fourth answer is

```
3
1 3 1
```

A solution that groups equal first values by their first occurrence will incorrectly put ((1,3)) before the second singleton ((1)).

Finally, a difference of one must not be accepted. For

```
2 2
1 2
```

neither pair can be extended, so the answer is

```
1
2
```

The two singleton subsequences are the only beautiful ones. This catches implementations that check only that the two frequencies differ.

## Approaches

The brute-force approach is straightforward. Generate every nonempty subsequence of the array, check whether every neighboring difference is prime, store the beautiful ones, sort them lexicographically, and take the (k)-th element. There are (2^n-1) subsequences, and checking one can take (O(n)), so the worst-case work is (O(n2^n)). For (n=1000), this is far beyond any practical limit.

Dynamic programming immediately gives us a useful counting primitive. For every position (i), let (ways[i]) be the number of beautiful subsequences whose first selected position is exactly (i). The singleton consisting only of (a_i) contributes one. Every later position (j) with a prime difference can be the next selected position, after which there are (ways[j]) possible continuations. Thus

1+
\sum_{\substack{j>i\ |a_i-a_j|\text{ is prime}}}
ways[j].
]

This recurrence can be evaluated from right to left in (O(n^2)).

The remaining difficulty is lexicographic unranking. It is tempting to use (ways[i]) directly and choose a starting position, but that is wrong when several positions contain the same frequency. For example, in ((1,3,1)), the two singleton ((1))'s must both appear before ((1,3)). Lexicographic order groups by frequency, not by the position used to obtain that frequency.

The key observation is that after we have fixed a prefix, every embedding of that prefix ends with the same frequency, namely the last frequency of the prefix. We can keep the number of embeddings ending at every position in an array (weight).

Suppose the current prefix has been fixed and (weight[i]) is the number of its embeddings ending at position (i). Then the number of occurrences of the prefix itself is simply

[
\sum_i weight[i].
]

Because a sequence is lexicographically smaller than any proper extension of itself, this entire block has to be considered before looking at another next frequency.

Now consider extending the prefix by the value (v). For a position (j) with (a_j=v), the number of embeddings of the extended prefix ending at (j) is

\sum_{\substack{i<j\ |a_i-v|\text{ is prime}}}
weight[i].
]

The number of complete beautiful subsequences using this position as the newly selected element is then

[
newWeight[j]\cdot ways[j].
]

We need these counts grouped by (v), because all sequences whose next frequency is the same belong to one lexicographic block.

There is a crucial simplification. All nonzero (weight[i]) belong to positions having the current prefix's last frequency (c). Consequently, when scanning positions from left to right, the sum needed for a future position (j) is just the cumulative weight of earlier positions, provided (|c-a_j|) is prime. One scan of the array therefore computes the counts for every possible next frequency at once.

After choosing the next frequency, the same scan has already computed the new weights for all positions containing that frequency. We can discard all other positions and continue.

The brute-force method works because every subsequence is considered explicitly, but fails because their number is exponential. The observation that all embeddings of the current prefix have one common last frequency lets us aggregate them into position weights and update all lexicographic blocks in one linear scan. The resulting unranking takes (O(n)) per output element and there can be at most (n) elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(n2^n)) if all subsequences are stored | Too slow |
| Optimal | (O(n^2)) | (O(n+V)) | Accepted |

Here (V\le 100000) is the maximum frequency difference relevant to the sieve.

## Algorithm Walkthrough

1. Build a sieve of Eratosthenes up to the largest possible frequency difference. After this preprocessing, `prime[d]` tells us in (O(1)) time whether (d) is prime.
2. Compute `ways[i]` from right to left. Initially every position contributes its singleton, so `ways[i]` starts at one. For every later position (j), add `ways[j]` when the frequency difference is prime. Values can be capped at (k), because counts larger than (k) are indistinguishable for rank selection.
3. Before constructing any prefix, group all beautiful subsequences by their first frequency. Every position (i) contributes `ways[i]` sequences to the block whose first value is `a[i]`. Sort the distinct frequencies and subtract whole blocks until the block containing rank (k) is found.
4. Set `weight[i]` to one for every position whose value is the selected first frequency, and zero elsewhere. At this point `weight[i]` means exactly the number of embeddings of the current prefix ending at position (i).
5. For the current prefix, first compute `exact = sum(weight)`. These are all occurrences of the prefix itself. If (k\le exact), the prefix is the required answer, because a string is lexicographically smaller than every proper extension of itself.
6. If the prefix itself is not the answer, subtract `exact` from (k). The remaining rank belongs to a proper extension.
7. Scan the array from left to right. Maintain `pref`, the total weight of positions before the current position. For every position (j), if the difference between the current prefix value and `a[j]` is prime, then `pref` is exactly the number of embeddings of the current prefix that can be extended through (j). Add `pref * ways[j]` to the lexicographic block belonging to `a[j]`.
8. During the same scan, store `pref` as the new weight of position (j) whenever the transition is valid. Once the selected next value (v) is known, all positions whose value is not (v) are discarded. The remaining weights describe every embedding of the new prefix.
9. Repeat the previous three steps until the current prefix itself contains the required rank. Since a subsequence uses strictly increasing positions, its length never exceeds (n).

### Why it works

The invariant is that after constructing a prefix (P), `weight[i]` equals the number of embeddings of (P) whose last selected position is (i). Summing these weights therefore counts every occurrence of (P), including duplicate frequency sequences produced by different positions.

For any possible next position (j), the scan computes exactly the number of embeddings of (P) that can reach (j). Multiplying this by `ways[j]` counts every beautiful completion beginning with that choice exactly once. Grouping these values by `a[j]` gives the exact size of every lexicographic next-value block.

The blocks are examined in increasing frequency order, so skipping a whole block preserves the rank of the desired sequence. When a block is selected, its corresponding `newWeight` array represents precisely all embeddings inside that block. Thus the invariant is preserved after every chosen frequency, and when the rank falls inside the exact-prefix block, the current prefix is exactly the required subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, k, a):
    max_diff = max(a) - min(a)

    prime = bytearray(b'\x01') * (max_diff + 1)
    if max_diff >= 0:
        prime[0] = 0
    if max_diff >= 1:
        prime[1] = 0

    p = 2
    while p * p <= max_diff:
        if prime[p]:
            start = p * p
            cnt = (max_diff - start) // p + 1
            prime[start:max_diff + 1:p] = b'\x00' * cnt
        p += 1

    cap = k

    ways = [1] * n

    for i in range(n - 1, -1, -1):
        total = 1
        ai = a[i]

        for j in range(i + 1, n):
            if prime[abs(ai - a[j])]:
                total += ways[j]
                if total >= cap:
                    total = cap
                    break

        ways[i] = total

    values = sorted(set(a))

    first_count = {}
    for i, v in enumerate(a):
        old = first_count.get(v, 0)
        cur = old + ways[i]
        first_count[v] = cap if cur >= cap else cur

    for v in values:
        cnt = first_count.get(v, 0)
        if k > cnt:
            k -= cnt
        else:
            first_value = v
            break

    answer = [first_value]

    weight = [0] * n
    for i in range(n):
        if a[i] == first_value:
            weight[i] = 1

    current = first_value

    while True:
        exact = sum(weight)

        if k <= exact:
            break

        k -= exact

        group = {}
        new_weight = [0] * n
        pref = 0

        for j in range(n):
            aj = a[j]

            if pref and prime[abs(current - aj)]:
                new_weight[j] = pref

                add = pref * ways[j]
                old = group.get(aj, 0)
                cur = old + add
                group[aj] = cap if cur >= cap else cur

            if weight[j]:
                pref += weight[j]
                if pref >= cap:
                    pref = cap

        chosen = None

        for v in values:
            cnt = group.get(v, 0)
            if k > cnt:
                k -= cnt
            else:
                chosen = v
                break

        answer.append(chosen)
        current = chosen

        for i in range(n):
            if a[i] == chosen:
                weight[i] = new_weight[i]
            else:
                weight[i] = 0

    return answer

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    answer = solve_case(n, k, a)

    print(len(answer))
    print(*answer)

if __name__ == "__main__":
    main()
```

The sieve is built only up to the largest difference that can actually occur. The `bytearray` representation keeps the primality table compact and makes the slicing-based sieve fast enough for Python.

The `ways` recurrence follows the right-to-left dynamic programming step. Breaking once the count reaches `k` is safe because all later additions are nonnegative, so the exact value no longer matters for unranking.

The first-frequency calculation is separate from the main reconstruction because there is no previous frequency at the root. Every position can independently be the first selected position, so the block for value (v) is the sum of `ways[i]` over all positions containing (v).

Once the first value is fixed, `weight[i]` represents embeddings of the complete current prefix, not merely positions where that prefix can occur. This distinction is what correctly handles duplicate subsequences.

Inside the reconstruction scan, `pref` is updated only after processing position (j). A subsequence must use an earlier position before (j), so including `weight[j]` too early would introduce an invalid self-transition. The difference is checked before the new weight is added for exactly the same reason.

The expression `pref * ways[j]` counts all completions through (j). `ways[j]` already includes the option of stopping at (j), which is necessary because the current prefix itself must appear before its extensions in lexicographic order.

Python integers do not overflow. Capping counts at `k` additionally prevents unnecessary growth and lets the algorithm ignore distinctions between counts that are both already large enough to contain the requested rank.

## Worked Examples

### Sample 1

The array is (1,3,6,1). The number of beautiful subsequences beginning at each position is

[
ways=[7,4,2,1].
]

The first-value blocks therefore contain 9 sequences beginning with (1), 4 beginning with (3), and 1 beginning with (6).

| Stage | Current prefix | Exact prefix count | Rank before decision | Decision |
| --- | --- | --- | --- | --- |
| Root | empty | not applicable | 2 | choose 1, its block has 9 |
| 1 | (1) | 2 | 2 | stop |

The two occurrences of the prefix ((1)) are both counted by `weight`: position 0 has weight 1 and position 3 has weight 1. Since the requested rank is exactly 2, the prefix itself is the answer.

The result is

```
1
1
```

This example demonstrates why duplicate embeddings must be counted before considering longer extensions.

### Sample 2

The first-value block counts are again (9,4,1) for values (1,3,6).

| Stage | Current prefix | Exact count | Rank entering stage | Extension blocks | Chosen value |
| --- | --- | --- | --- | --- | --- |
| Root | empty | not applicable | 6 | (1:9,\ 3:4,\ 6:1) | 1 |
| 1 | (1) | 2 | 6 | (3:4,\ 6:2) | 3 |
| 2 | (1,3) | 1 | 3 | (1:1,\ 6:2) | 6 |
| 3 | (1,3,6) | 1 | 2 | (1:1) | 1 |
| 4 | (1,3,6,1) | 1 | 1 | none needed | stop |

After choosing the first (1), the two singleton occurrences occupy the first two ranks of its block, so the residual rank is (6-2=4). The next-value block for (3) has size 4, so (3) is selected.

For the prefix ((1,3)), the prefix itself occupies one position in the ordering. Its remaining rank is 3, and the extension blocks have sizes 1 for the next value (1) and 2 for the next value (6). The third rank inside this subtree is consequently ((1,3,6)).

The same argument selects the final (1), giving

```
4
1 3 6 1
```

The trace demonstrates the central invariant: the rank is always measured inside the subtree represented by the current prefix, while `weight` keeps all its possible embeddings simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2 + V\log\log V)) | The DP takes (O(n^2)), and reconstruction scans the (n)-element array at most (n) times. The sieve handles differences up to (V\le100000). |
| Space | (O(n+V)) | The main arrays have size (O(n)), while the primality table has size (O(V)). |

The dominant term is (O(n^2)), about one million position-level operations for (n=1000). The valid input also guarantees that (k) does not exceed the number of available subsequences, which is at most (2^{1000}-1), so the relevant counts require only about 1000 bits despite the much larger syntactic upper bound on (k).

## Test Cases

```python
import sys
import io

# Paste the solve_case function from the solution above before running these tests.

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        ans = solve_case(n, k, a)
        return str(len(ans)) + "\n" + " ".join(map(str, ans)) + "\n"
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("""4 2
1 3 6 1
""") == """1
1
""", "sample 1"

assert run("""4 6
1 3 6 1
""") == """4
1 3 6 1
""", "sample 2"

# Minimum-size input
assert run("""1 1
5
""") == """1
5
""", "minimum size"

# Maximum-size input, all equal values.
# No pair can be adjacent because the difference is zero.
max_input = "1000 1000\n" + " ".join(["7"] * 1000) + "\n"
assert run(max_input) == """1
7
""", "maximum size and all equal"

# Difference 1 is not prime.
assert run("""2 2
1 2
""") == """1
2
""", "non-prime boundary"

# Duplicate prefixes and exact-prefix ordering.
assert run("""3 4
1 3 1
""") == """3
1 3 1
""", "duplicate prefix ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5` | `1 / 5` | The smallest possible array and exclusion of the empty subsequence |
| `1000 1000 / 7 ... 7` | `1 / 7` | Maximum (n), repeated equal values, and zero not being prime |
| `2 2 / 1 2` | `1 / 2` | Difference one must be rejected |
| `3 4 / 1 3 1` | `3 / 1 3 1` | Duplicate singleton occurrences and prefix-before-extension ordering |

## Edge Cases

For the one-element input

```
1 1
5
```

the initial block for value (5) has size one because `ways[0] = 1`. The first value is selected, `weight[0] = 1`, and the exact-prefix count is one. Since (k=1), reconstruction stops immediately and outputs ((5)). There is never any transition attempt, so the boundary at the end of the array is handled naturally.

For

```
3 2
7 7 7
```

the sieve marks zero as non-prime. Consequently `ways[i] = 1` at every position. The first-value block for (7) has size three, because each position gives one separate singleton subsequence. After choosing (7), the weight array contains three ones. The exact-prefix count is therefore three, so rank two stops at the singleton. No transition with difference zero is ever accepted.

For

```
3 4
1 3 1
```

the first-value block for (1) contains four subsequences: two singleton occurrences, ((1,3)), and ((1,3,1)). Rank four therefore enters the (1)-subtree. The current prefix has exact count two, corresponding to the two positions containing (1), so those two ranks are skipped. The only next value is (3), and its extension block contains two sequences, ((1,3)) and ((1,3,1)). Rank two inside that block selects (3), after which the exact prefix ((1,3)) consumes one rank and the final (1) consumes the remaining one. The output is ((1,3,1)). This is precisely the case where tracking only the earliest matching position would fail.

For

```
2 2
1 2
```

the difference is one, which the sieve marks as composite. Each `ways` value is one, so the initial blocks are (1:1) and (2:1). Rank two skips the entire block beginning with (1) and selects (2). The resulting singleton has exact count one, so the algorithm terminates with ((2)). This confirms that the prime test is applied to the actual absolute difference rather than merely checking that the frequencies are distinct.
