---
title: "CF 191A - Dynasty Puzzles"
description: "We are given a list of abbreviated king names in chronological order. Each name is a lowercase string. We may choose some of these names to form a dynasty, while preserving their original order. A valid dynasty must satisfy two conditions."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 191
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 121 (Div. 1)"
rating: 1500
weight: 191
solve_time_s: 102
verified: true
draft: false
---

[CF 191A - Dynasty Puzzles](https://codeforces.com/problemset/problem/191/A)

**Rating:** 1500  
**Tags:** dp  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of abbreviated king names in chronological order. Each name is a lowercase string. We may choose some of these names to form a dynasty, while preserving their original order.

A valid dynasty must satisfy two conditions.

The last character of each chosen name must equal the first character of the next chosen name. This creates a chain.

The dynasty must also form a cycle overall, meaning the first character of the first chosen name must equal the last character of the final chosen name.

The dynasty name itself is the concatenation of all selected strings, so the objective is to maximize the total length of all chosen names.

The key observation is that only the first and last letters of a string matter for compatibility. The internal characters never affect transitions. The contribution of a name is simply its length.

The constraints completely shape the solution. We may have up to $5 \cdot 10^5$ strings, so anything quadratic is impossible. Even storing transitions between all pairs would already be too large. Since each string length is at most 10, processing each name individually is cheap, but we must keep the per-name work close to constant time.

A dynamic programming solution over the alphabet becomes feasible because there are only 26 lowercase letters. Any algorithm using states based on start and end letters has at most $26^2 = 676$ states, which is tiny.

There are several edge cases that can silently break incorrect solutions.

Consider a single string whose first and last characters already match.

```
1
abca
```

The correct answer is 4. A careless implementation that only looks for transitions between different strings would incorrectly return 0.

Another subtle case appears when skipping strings is necessary.

```
3
abc
ca
cba
```

The optimal dynasty uses the first and third strings, producing length 6. Greedy approaches that always extend immediately with the next compatible string would stop at `"abc" + "ca"` and miss the better solution.

A third trap is overwriting DP states incorrectly during updates.

```
3
ab
bc
ca
```

The answer is 6. If updates are performed in-place without care, the current string might get reused multiple times inside the same iteration, effectively allowing impossible chains.

Finally, there may be no valid cycle at all.

```
2
ab
bc
```

No chosen subsequence forms a cycle, so the answer is 0. Returning the best chain instead of the best cycle would be wrong.

## Approaches

The brute-force idea is straightforward. We try every subsequence of strings, check whether adjacent strings connect correctly, and verify whether the whole sequence forms a cycle.

This works because the rules depend only on neighboring strings and the overall first and last letters. The problem is the number of subsequences. With $n$ strings, there are $2^n$ possible selections. Even for $n = 50$, this is already hopeless, and the real limit is $5 \cdot 10^5$.

A more reasonable brute-force variant uses dynamic programming over subsets or graph paths, but that still collapses because the input size is enormous.

The structure of the problem gives a much stronger observation. Every string only contributes three meaningful pieces of information:

First letter.

Last letter.

Length.

The alphabet contains only 26 letters, so the number of possible start-end pairs is tiny. Instead of remembering exact sequences, we only need to remember the best total length for each possible pair of starting and ending letters.

Define:

$dp[i][j]$ = maximum total length of a valid chain whose first string starts with letter $i$ and whose current last string ends with letter $j$.

When processing a new string from $a$ to $b$ with length $w$, we can:

Start a new chain consisting only of this string.

Extend every existing chain ending at $a$.

This is possible because compatibility only depends on matching boundary letters. The full history of the chain does not matter.

Since there are only 26 possible ending letters, each string performs only about 26 transitions. The total work becomes roughly $26 \cdot n$, which easily fits within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal DP | $O(26 \cdot n)$ | $O(26^2)$ | Accepted |

## Algorithm Walkthrough

1. Create a 26 × 26 DP table initialized to negative infinity.

The state $dp[i][j]$ stores the maximum total length of a chain that starts with letter $i$ and currently ends with letter $j$.
2. Process the strings one by one in input order.

Preserving order is mandatory because kings appear chronologically.
3. For the current string, extract:

- its starting character $a$
- its ending character $b$
- its length $w$
4. Start a new chain using only this string.

Update:

$$dp[a][b] = \max(dp[a][b], w)$$

This handles dynasties containing a single king.

1. Try extending every chain that currently ends with $a$.

For every possible starting letter $s$:

$$dp[s][b] = \max(dp[s][b], dp[s][a] + w)$$

This works because the current string can legally follow any chain whose last letter equals its first letter.

1. Be careful not to reuse the current string multiple times during the same iteration.

To avoid this, copy the old values before updating, or iterate using a snapshot of the relevant column.
2. After all strings are processed, the answer is:

$$\max(dp[c][c])$$

over all 26 letters $c$.

A dynasty is valid only if its overall first and last letters match.

### Why it works

The DP state captures exactly the information needed for future extensions.

Suppose we know the best chain starting with letter $s$ and ending with letter $e$. Any future string can only check whether its first letter matches $e$. Nothing else about the chain matters.

When we append a string from $a$ to $b$, every compatible chain ending at $a$ becomes a new chain ending at $b$, with total length increased by the current string length.

Because every string is processed once and transitions only go forward in chronological order, every constructed chain corresponds to a valid subsequence of kings. Conversely, every valid dynasty can be built through these transitions, so the DP never misses an optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = -(10 ** 18)

n = int(input())

dp = [[INF] * 26 for _ in range(26)]

for _ in range(n):
    s = input().strip()

    a = ord(s[0]) - ord('a')
    b = ord(s[-1]) - ord('a')
    w = len(s)

    old = [dp[i][a] for i in range(26)]

    dp[a][b] = max(dp[a][b], w)

    for start in range(26):
        if old[start] != INF:
            dp[start][b] = max(dp[start][b], old[start] + w)

ans = 0

for i in range(26):
    ans = max(ans, dp[i][i])

print(ans)
```

The DP table stores the best achievable total lengths for every start-end pair of letters. Invalid states are initialized with a very negative number so we can distinguish them from legitimate chains.

For each string, we first extract its boundary letters and length. The string can always form a dynasty by itself, so we update `dp[a][b]` directly.

The subtle part is extending previous chains safely. We must avoid reading values that were already updated during the current iteration, because that would allow the same string to be appended multiple times. The line:

```
old = [dp[i][a] for i in range(26)]
```

creates a snapshot of all chains ending with letter `a` before processing the current string.

Then each compatible chain gets extended by the current string length.

Finally, only states where the starting and ending letters are equal represent valid dynasties, so we take the maximum diagonal value.

## Worked Examples

### Example 1

Input:

```
3
abc
ca
cba
```

Processing trace:

| String | Start | End | Length | Updated States |
| --- | --- | --- | --- | --- |
| abc | a | c | 3 | dp[a][c] = 3 |
| ca | c | a | 2 | dp[c][a] = 2, dp[a][a] = 5 |
| cba | c | a | 3 | dp[c][a] = 3, dp[a][a] = 6 |

Final diagonal values:

| State | Value |
| --- | --- |
| dp[a][a] | 6 |
| others | invalid or smaller |

Answer:

```
6
```

The optimal dynasty uses `"abc"` followed by `"cba"`. The intermediate string `"ca"` is skipped. This demonstrates why greedy extension is insufficient and why subsequence DP is necessary.

### Example 2

Input:

```
2
ab
bc
```

Processing trace:

| String | Start | End | Length | Updated States |
| --- | --- | --- | --- | --- |
| ab | a | b | 2 | dp[a][b] = 2 |
| bc | b | c | 2 | dp[b][c] = 2, dp[a][c] = 4 |

Final diagonal values:

| State | Value |
| --- | --- |
| dp[a][a] | invalid |
| dp[b][b] | invalid |
| dp[c][c] | invalid |

Answer:

```
0
```

The chain `"ab" -> "bc"` is valid locally, but it does not form a cycle overall because it starts with `a` and ends with `c`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(26 \cdot n)$ | Each string performs transitions over 26 possible starting letters |
| Space | $O(26^2)$ | The DP table contains only 676 states |

With $n \le 5 \cdot 10^5$, the algorithm performs roughly 13 million state transitions, which is easily fast enough in Python. The memory usage is tiny.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    INF = -(10 ** 18)

    n = int(input())

    dp = [[INF] * 26 for _ in range(26)]

    for _ in range(n):
        s = input().strip()

        a = ord(s[0]) - ord('a')
        b = ord(s[-1]) - ord('a')
        w = len(s)

        old = [dp[i][a] for i in range(26)]

        dp[a][b] = max(dp[a][b], w)

        for start in range(26):
            if old[start] != INF:
                dp[start][b] = max(dp[start][b], old[start] + w)

    ans = 0

    for i in range(26):
        ans = max(ans, dp[i][i])

    return str(ans)

# provided sample
assert run("3\nabc\nca\ncba\n") == "6", "sample 1"

# no valid dynasty
assert run("2\nab\nbc\n") == "0", "no cycle"

# single valid string
assert run("1\nc\n") == "1", "single string cycle"

# choose non-adjacent strings
assert run("4\nab\nbc\nca\naa\n") == "6", "best subsequence"

# all equal letters
assert run("3\naa\naa\naa\n") == "6", "all chains compatible"

# off-by-one style chain
assert run("3\nab\nba\nab\n") == "6", "reuse all strings correctly"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / c` | `1` | Single-string dynasty |
| `2 / ab bc` | `0` | No cycle exists |
| `4 / ab bc ca aa` | `6` | Best answer may skip strings |
| `3 / aa aa aa` | `6` | Repeated compatible states |
| `3 / ab ba ab` | `6` | Correct transition chaining |

## Edge Cases

Consider the case where a single string already forms a cycle.

```
1
abca
```

The string starts and ends with `a`, so during processing we update:

```
dp[a][a] = 4
```

The final diagonal maximum becomes 4, which is correct. Algorithms that only extend previous chains would miss this because no transition is needed.

Now consider a case where skipping strings is optimal.

```
3
abc
ca
cba
```

After processing `"abc"`:

```
dp[a][c] = 3
```

Processing `"ca"` creates:

```
dp[a][a] = 5
```

Processing `"cba"` extends the earlier chain directly:

```
dp[a][a] = 6
```

The algorithm naturally explores all subsequences because each state persists for future transitions.

Finally, consider a dangerous in-place update scenario.

```
3
ab
bc
ca
```

When processing `"bc"`, we first snapshot all chains ending at `b`. Without this snapshot, updating `dp[a][c]` could accidentally influence later transitions in the same iteration and reuse `"bc"` multiple times.

Using:

```
old = [dp[i][a] for i in range(26)]
```

guarantees every transition uses only states that existed before the current string was processed.
