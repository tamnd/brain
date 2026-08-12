---
title: "CF 102375K - <<\u041a\u043e\u043d\u0442\u0430\u043a\u0442>> \u0434\u043b\u044f \u0434\u0432\u043e\u0438\u0445"
description: "We have a dictionary of known words. For every query, one dictionary entry is chosen as the secret word (S), and an integer (K) determines how many unsuccessful guesses the second player may make before another letter of (S) is revealed."
date: "2026-08-12T22:43:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "K"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 457
verified: true
draft: false
---

[CF 102375K - <<\u041a\u043e\u043d\u0442\u0430\u043a\u0442>> \u0434\u043b\u044f \u0434\u0432\u043e\u0438\u0445](https://codeforces.com/problemset/problem/102375/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a dictionary of known words. For every query, one dictionary entry is chosen as the secret word (S), and an integer (K) determines how many unsuccessful guesses the second player may make before another letter of (S) is revealed.

At any moment the player knows a prefix of (S). They may name any previously unused dictionary word having that prefix. The secret word itself is also in the dictionary, and identical spellings are still different dictionary entries, so every occurrence must be counted separately.

Valera wants to make the game last as long as possible. For a query ((w,K)), the required answer is the largest possible number of guesses, including the successful guess if the player eventually guesses the secret word.

The total length of all dictionary words is at most (2\cdot10^5), and there can be (2\cdot10^5) queries. This rules out doing work proportional to the whole dictionary for every query. Even a solution that preprocesses prefix counts but then walks the entire secret word for every query can reach about (2\cdot10^{10}) operations when many queries refer to a long word. The solution must make the preprocessing essentially linear in the total input size and keep each query logarithmic or close to it.

There are several edge cases that are easy to mishandle. First, the secret word may be the only word with its first letter. For example,

```
1
a
1
1 1
```

has answer `1`. There are no wrong guesses, so the player immediately names the secret word. A formula that counts only unsuccessful guesses would incorrectly return zero.

Second, duplicate dictionary entries matter. Consider

```
3
aa
ab
ab
2
2 2
```

The answer is `3`. With (K=2), the player can first name `aa` and the other occurrence of `ab`, then the first player reveals that the whole word is `ab`. Treating the dictionary as a set would lose one available guess and produce the wrong result.

Third, previously named words cannot be reused. For example,

```
4
abc
abd
abe
abf
2
1 2
```

has answer `4`. During the first round, two of `abd`, `abe`, `abf` must be named. Only one wrong word remains when the prefix becomes `ab`, so the second round consists of that wrong guess followed by the successful guess `abc`. Counting the number of words under every prefix independently would incorrectly assume that the same words can be used again.

## Approaches

The most direct approach is to simulate the game. For each query, we could inspect all dictionary words that match the currently known prefix, choose suitable wrong words, remove them from consideration, reveal the next letter after (K) guesses, and continue. This is correct because the only strategic choice is which unused matching words to spend as wrong guesses.

A literal implementation that scans all (N) dictionary words at every prefix costs (O(N|S|)) for one query. Under the given bounds this can reach roughly (2\cdot10^{15}) elementary checks over all queries in a construction with many queries and a long secret word, so it is unusable.

A natural improvement is to build a trie and store how many dictionary entries pass through every prefix. Then a query can inspect only the prefixes of its secret word. This reduces one query to (O(|S|)), but (2\cdot10^5) queries can still require (O(Q\cdot |S|)) work, which is too large.

The key observation is to stop thinking about individual words and instead assign every wrong dictionary word a deadline. For a wrong word (T), let (d) be the length of the longest common prefix of (T) and the secret word (S). The word can be guessed during rounds (1,\ldots,d), but after the (d)-th letter is revealed it is no longer a valid guess.

Every round needs exactly (K) wrong guesses if the game is to continue. Thus the problem becomes a scheduling problem: each wrong word is a job with deadline (d), and every round has (K) slots. The player should use words with earlier deadlines first, because those words will disappear sooner.

Let (C_d) be the number of wrong dictionary entries whose longest common prefix with (S) has length at least (d). In trie terminology, this is simply the number of dictionary entries having the first (d) letters of (S), minus the secret entry itself.

Suppose we want to complete (r) full rounds. Consider the last (r-d+1) rounds, from (d) through (r). Every guess placed there must use a word whose deadline is at least (d), and there are (K(r-d+1)) required guesses. Hence we need

[
C_d \ge K(r-d+1)
]

for every (d\le r).

This condition is also sufficient. The sets of words with deadline at least (d) are nested, so the usual greedy scheduling argument applies: always use an available word with the smallest deadline. The suffix inequalities are exactly the capacity conditions required by that greedy schedule.

Rearranging the inequality gives

[
r \le d-1+\left\lfloor\frac{C_d}{K}\right\rfloor.
]

Consequently the maximum number of complete rounds is

[
r=\min_d\left(d-1+\left\lfloor\frac{C_d}{K}\right\rfloor\right).
]

The expression inside the minimum has an especially useful form:

\left\lfloor\frac{C_d+K(d-1)}{K}\right\rfloor.
]

For a fixed secret word, every depth (d) thus contributes a line

[
f_d(x)=C_d+(d-1)x,
]

and a query asks for the minimum value of these lines at (x=K). This is exactly a lower convex hull trick problem. We build the hull once for every dictionary word and answer each query with a binary search on that hull.

After (r) complete rounds, if (r) is smaller than the secret length, the next round cannot contain (K) wrong guesses. Let (W=N-1) be the total number of wrong dictionary entries. At that point the number of still usable wrong words is

[
R=\min(C_{r+1}, W-rK).
]

The player names those (R) words and then names the secret word successfully, so the final answer is

[
rK+R+1.
]

If (r) equals the secret length, all rounds have completed and the first player reveals the entire word, so the answer is simply (rK).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Literal simulation | (O(QN | S | )) in the worst case | (O(N)) | Too slow |
| Trie plus simulation | (O(\sum | S | +Q | S | )) | (O(\sum | S | )) | Too slow |
| Trie plus convex hulls | (O(L+Q\log L)), where (L) is total word length | (O(L)) | Accepted |

## Algorithm Walkthrough

1. Build a trie containing every dictionary word. Each trie node stores how many dictionary entries pass through it. Equal words are inserted separately, so their multiplicity is preserved automatically.
2. For every dictionary word (S), walk through its path in the trie. For every prefix length (d), store

[
C_d=\text{count(prefix of length }d)-1.
]

The subtraction removes the particular dictionary entry chosen as the secret word. Other identical entries remain counted, which is exactly what the game requires.

1. Interpret every wrong word as a job whose deadline is its longest common prefix length with (S). A word with deadline (d) can be guessed during any of the first (d) rounds. The value (C_d) is precisely the number of jobs whose deadline is at least (d).
2. For every prefix length (d), create the line

[
y=C_d+(d-1)x.
]

For a query value (K), the minimum line value divided by (K) gives the maximum number of complete rounds:

[
r=\min\left(|S|,\left\lfloor\frac{\min_d(C_d+K(d-1))}{K}\right\rfloor\right).
]

The convex hull stores only lines that can be optimal, so the minimum can be found in logarithmic time.

1. If (r=|S|), the game survives every round. After (K) guesses in the final round, all letters have been revealed, so the answer is (rK).
2. Otherwise the next known prefix has length (r+1). There are (C_{r+1}) wrong dictionary entries under that prefix, but some of the (rK) earlier guesses may have come from this same subtree. The minimum possible number of remaining usable wrong words is

[
R=\min(C_{r+1},N-1-rK).
]

The player can name all (R) of them and then must name the secret word, so the answer is (rK+R+1).

1. Repeat the hull query for every requested pair ((w,K)). The preprocessing for a word is independent of every other word, so duplicate query pairs require no additional work.

Why it works

The central invariant is that every wrong word is characterized only by the last round in which it can still be named, namely its longest common prefix length with the secret word. To complete (r) rounds, the last (r-d+1) rounds require (K(r-d+1)) words with deadline at least (d). The inequalities (C_d\ge K(r-d+1)) are necessary, and because the eligible sets are nested, they are sufficient for the greedy strategy that always spends the earliest-deadline available words first. The convex hull computes the largest (r) satisfying all these inequalities. Once that many complete rounds have been made, the formula for (R) counts exactly how many usable wrong words can remain, after which the secret word is necessarily the next guess if the game has not already ended.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_hull(values):
    hull = []

    for slope, intercept in enumerate(values):
        while len(hull) >= 2:
            m1, b1 = hull[-2]
            m2, b2 = hull[-1]
            m3, b3 = slope, intercept

            # l2 is redundant if the intersection of l1,l2
            # is not to the right of the intersection of l2,l3.
            if (b1 - b2) * (m3 - m2) <= (b2 - b3) * (m2 - m1):
                hull.pop()
            else:
                break

        hull.append((slope, intercept))

    return hull

def query_hull(hull, x):
    lo = 0
    hi = len(hull) - 1

    while lo < hi:
        mid = (lo + hi) // 2

        m1, b1 = hull[mid]
        m2, b2 = hull[mid + 1]

        if m1 * x + b1 <= m2 * x + b2:
            hi = mid
        else:
            lo = mid + 1

    m, b = hull[lo]
    return m * x + b

def solve():
    n = int(input())
    words = [input().strip() for _ in range(n)]

    children = [{}]
    count = [0]

    # Build the trie and count how many dictionary entries
    # pass through every node.
    for word in words:
        node = 0
        for ch in word:
            nxt = children[node].get(ch)
            if nxt is None:
                nxt = len(children)
                children[node][ch] = nxt
                children.append({})
                count.append(0)

            node = nxt
            count[node] += 1

    hulls = [None] * n
    prefix_counts = [None] * n

    # For every possible secret word, prepare C_d and its
    # lower hull of lines C_d + (d-1) * x.
    for idx, word in enumerate(words):
        node = 0
        values = []

        for ch in word:
            node = children[node][ch]
            values.append(count[node] - 1)

        prefix_counts[idx] = values
        hulls[idx] = build_hull(values)

    q = int(input())
    total_wrong = n - 1
    out = []

    for _ in range(q):
        w, k = map(int, input().split())
        w -= 1

        values = prefix_counts[w]
        length = len(values)
        hull = hulls[w]

        minimum = query_hull(hull, k)
        rounds = minimum // k

        if rounds > length:
            rounds = length

        completed = rounds * k

        if rounds == length:
            out.append(str(completed))
            continue

        remaining = min(values[rounds], total_wrong - completed)
        answer = completed + remaining + 1
        out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The trie construction follows the first part of the walkthrough. Every occurrence of a word increments the counters on its complete prefix path, so two identical spellings contribute two separate entries.

For each word, `values[d]` stores (C_{d+1}). The word itself is subtracted exactly once by `count[node] - 1`, while other dictionary entries with the same spelling remain present.

`build_hull` receives lines whose slopes are (0,1,2,\ldots). The cross-product comparison avoids floating-point intersection coordinates. Since all values are integers and can be as large as roughly (K|S|), integer arithmetic is also naturally sufficient. Python integers have no overflow issue.

`query_hull` compares two adjacent hull lines. The lower hull makes the line values ordered around their minimum, so binary search finds the optimal line in (O(\log |S|)).

The expression returned by the hull is

[
M=\min_d(C_d+K(d-1)).
]

Dividing it by (K) with integer division gives the maximum number of complete rounds. The `rounds > length` guard handles the theoretical case where the minimum expression would exceed the number of letters.

The final calculation uses `values[rounds]`, because `rounds` complete rounds mean the next known prefix has length `rounds + 1`, corresponding to zero-based index `rounds`. The `+1` in the final answer is the successful guess of the secret word when the game stops before all letters have been revealed.

## Worked Examples

### Sample 1

Consider the first dictionary word `asassin`. Its relevant wrong-word counts along the secret path are

[
C_1=5,\qquad C_2=2,\qquad C_3=0.
]

The later prefix counts are also zero, so they can never improve the hull minimum.

For (K=1), the three relevant lines are (5), (2+x), and (2x). Their minimum at (x=1) is (2), so two complete rounds are possible. The next prefix has no wrong word, hence the secret word itself is guessed on the third attempt.

| Prefix length (d) | (C_d) | Line (C_d+(d-1)K), (K=1) |
| --- | --- | --- |
| 1 | 5 | 5 |
| 2 | 2 | 3 |
| 3 | 0 | 2 |

Thus (r=2), and the answer is (2\cdot1+0+1=3).

For (K=2), the line values are (5,4,4). The minimum is (4), giving (r=2). There are again no remaining wrong words under the third prefix, so the answer is (4+1=5).

For (K=3), the line values are (5,5,6). The minimum is (5), giving (r=1). After three guesses in the first round, two usable wrong words remain under the second prefix. The player names those two and then guesses the secret word.

| (K) | Hull minimum | Complete rounds (r) | Remaining wrong guesses | Final answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 0 | 3 |
| 2 | 4 | 2 | 0 | 5 |
| 3 | 5 | 1 | 2 | 6 |

This trace demonstrates why previously used words must be treated as scheduled jobs rather than independently counted at every prefix. For (K=3), the first round consumes some words that would otherwise belong to the deeper prefix.

### Sample 2

Take dictionary entry 2, `ab`, as the secret word. There are two other dictionary entries under prefix `a`: `aa` and the second occurrence of `ab`. Thus (C_1=2). Under the full prefix `ab`, only the other occurrence of `ab` remains, so (C_2=1).

For (K=1), the lines have values (2) and (2). Two complete rounds are possible.

| Prefix length (d) | (C_d) | Line (C_d+(d-1)K), (K=1) |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | 1 | 2 |

The player first names `aa`, then the first player reveals `b`. The player next names the other `ab`, and the first player ends the game because the entire word has been revealed. The answer is `2`.

For (K=2), the line values are (2) and (3), so only one complete round is possible. After the two guesses in that round, no wrong `ab` entry remains, and the secret word is guessed successfully.

| (K) | Hull minimum | Complete rounds (r) | Remaining wrong guesses | Final answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 0 | 2 |
| 2 | 2 | 1 | 0 | 3 |

The second query demonstrates why duplicate spellings must remain separate dictionary entries. The second `ab` is a legitimate wrong guess even though its spelling is identical to the secret word.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(L+Q\log L)) | Trie construction and all hull construction take (O(L)), where (L) is the total length of all words. Each query performs one hull binary search. |
| Space | (O(L)) | The trie, prefix-count arrays, convex hulls, and stored words contain (O(L)) total information. |

Here (L\le2\cdot10^5), and (Q\le2\cdot10^5). The preprocessing is linear in the actual input size, while each query touches only the hull belonging to its requested word. The largest hull is bounded by the length of that word, so the logarithmic query bound remains small.

## Test Cases

```python
import sys
import io

def build_hull(values):
    hull = []

    for slope, intercept in enumerate(values):
        while len(hull) >= 2:
            m1, b1 = hull[-2]
            m2, b2 = hull[-1]
            m3, b3 = slope, intercept

            if (b1 - b2) * (m3 - m2) <= (b2 - b3) * (m2 - m1):
                hull.pop()
            else:
                break

        hull.append((slope, intercept))

    return hull

def query_hull(hull, x):
    lo = 0
    hi = len(hull) - 1

    while lo < hi:
        mid = (lo + hi) // 2

        m1, b1 = hull[mid]
        m2, b2 = hull[mid + 1]

        if m1 * x + b1 <= m2 * x + b2:
            hi = mid
        else:
            lo = mid + 1

    m, b = hull[lo]
    return m * x + b

def solve_stream(stream):
    input = stream.readline

    n = int(input())
    words = [input().strip() for _ in range(n)]

    children = [{}]
    count = [0]

    for word in words:
        node = 0

        for ch in word:
            nxt = children[node].get(ch)

            if nxt is None:
                nxt = len(children)
                children[node][ch] = nxt
                children.append({})
                count.append(0)

            node = nxt
            count[node] += 1

    hulls = [None] * n
    prefix_counts = [None] * n

    for idx, word in enumerate(words):
        node = 0
        values = []

        for ch in word:
            node = children[node][ch]
            values.append(count[node] - 1)

        prefix_counts[idx] = values
        hulls[idx] = build_hull(values)

    q = int(input())
    total_wrong = n - 1
    answer = []

    for _ in range(q):
        w, k = map(int, input().split())
        w -= 1

        values = prefix_counts[w]
        length = len(values)

        rounds = query_hull(hulls[w], k) // k
        rounds = min(rounds, length)

        completed = rounds * k

        if rounds == length:
            answer.append(str(completed))
        else:
            remaining = min(values[rounds], total_wrong - completed)
            answer.append(str(completed + remaining + 1))

    return "\n".join(answer)

def run(inp: str) -> str:
    return solve_stream(io.StringIO(inp)).strip()

# Provided sample 1
assert run("""\
6
asassin
assistant
astronaut
abrakadabra
abbey
automaton
9
1 1
1 2
1 3
4 1
4 2
4 3
6 1
6 2
6 3
""") == """\
3
5
6
3
4
5
2
3
4
""", "sample 1"

# Provided sample 2
assert run("""\
3
aa
ab
ab
6
1 1
2 1
1 2
3 2
2 2
3 1
""") == """\
2
2
3
3
3
2
""", "sample 2"

# Provided sample 3
assert run("""\
7
pit
pitbul
piter
pitstop
pitlane
petroleum
pistol
6
1 2
1 3
6 4
7 2
7 3
5 1
""") == """\
6
7
5
5
7
4
""", "sample 3"

# Minimum-size dictionary.
assert run("""\
1
a
1
1 1
""") == "1", "only word is the secret"

# Duplicate spellings and K at the boundary.
assert run("""\
3
aa
ab
ab
2
2 2
2 1
""") == """\
3
2
""", "duplicates must remain distinct"

# Previously used words cannot be reused.
assert run("""\
4
abc
abd
abe
abf
2
1 2
1 1
""") == """\
4
3
""", "reuse of guesses"

# Maximum-size construction: 200000 identical one-letter words.
maximum_case = (
    "200000\n"
    + "a\n" * 200000
    + "2\n"
    + "1 1\n"
    + "1 200000\n"
)

assert run(maximum_case) == """\
1
200000
""", "maximum N and duplicate count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a / 1 / 1 1` | `1` | Minimum dictionary and immediate successful guess |
| Three entries `aa, ab, ab` | `3, 2` | Duplicate dictionary entries and (K) boundary behavior |
| `abc, abd, abe, abf` | `4, 3` | Previously used words must not be counted again |
| 200000 copies of `a` | `1, 200000` | Maximum (N), maximum (K), and large multiplicities |

## Edge Cases

For the single-word case

```
1
a
1
1 1
```

the trie contains one node for prefix `a`, whose dictionary count is one. After subtracting the secret entry, (C_1=0). The hull contains the line (y=0), so (r=0). There are zero remaining wrong words, and the answer is (0+0+1=1). The algorithm correctly counts the successful guess.

For duplicate spellings,

```
3
aa
ab
ab
1
2 2
```

the trie count for `a` is three, so (C_1=2). The count for `ab` is two, so (C_2=1). With (K=2), the hull values are (2) and (3), giving (r=1). After the first two guesses, no wrong `ab` entry remains, so the secret word is guessed next. The result is (2+0+1=3). The duplicate occurrence is preserved throughout preprocessing.

For the no-reuse case,

```
4
abc
abd
abe
abf
1
1 2
```

there are three wrong words and all have the same deadline (2). Thus (C_1=3) and (C_2=3). For (K=2), the hull gives

[
\min(3,3+2)=3,
]

so (r=1). The first round consumes two wrong words. At prefix `ab`, only one wrong word remains, so the second round has one wrong guess followed by the successful guess `abc`. The answer is (4). The hull model captures the fact that two of the three words have already been consumed.

For the maximum duplicate case, there are (200000) copies of `a`. For (K=1), the secret word can be postponed by one wrong guess, but the word is already fully revealed after that round, giving answer `1`. For (K=200000), there are (199999) wrong occurrences and then the secret occurrence itself can be named, giving exactly `200000`. The algorithm stores multiplicities rather than deduplicating the dictionary, so both boundary cases are handled correctly.
