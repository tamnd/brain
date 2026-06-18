---
problem: 963D
contest_id: 963
problem_index: D
name: "Frequency of String"
contest_name: "Tinkoff Internship Warmup Round 2018 and Codeforces Round 475 (Div. 1)"
rating: 2500
tags: ["hashing", "string suffix structures", "strings"]
answer: passed_samples
verified: true
solve_time_s: 109
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a33a36d-603c-83ec-9659-5838d7876b75
---

# CF 963D - Frequency of String

**Rating:** 2500  
**Tags:** hashing, string suffix structures, strings  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 49s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a33a36d-603c-83ec-9659-5838d7876b75  

---

## Solution

## Problem Understanding

We are given a fixed text string and then many independent pattern queries. Each query gives a pattern string and a required frequency. For each query we need to look at all substrings of the main string that contain the pattern often enough, and among those substrings choose the shortest one. If the pattern does not appear in the main string enough times globally, the answer is impossible.

The key object is not just whether a pattern occurs, but where its occurrences lie inside the main string. Once we know all starting positions of a pattern, every valid substring is determined by choosing a consecutive block of occurrences and stretching a window from the first occurrence in the block to the last occurrence in the block. The answer is the smallest possible span that still contains at least k occurrences.

The constraints force a global preprocessing strategy. The sum of pattern lengths is at most 10^5, and there are up to 10^5 queries, so recomputing pattern matches per query would exceed both time and memory. Any solution that scans the main string per query leads to O(n^2) in the worst case and fails immediately.

A subtle edge case appears when the pattern is long but appears in overlapping ways, for example in a string like "aaaaa". The occurrences of "aaa" overlap heavily, and the minimal window depends on how overlaps are counted as distinct occurrences. Another issue arises when k is 1, where the answer is simply the pattern length if it exists at all, but naive approaches that assume disjoint occurrences may still overcount or misplace boundaries.

## Approaches

A direct solution would process each query separately by scanning the main string and collecting all occurrences of the pattern. For each pattern we then take its occurrence positions and compute the minimum window covering k consecutive occurrences. This is correct, since any substring containing k occurrences must include some k consecutive ones in occurrence order. The problem is cost: scanning the full string per query gives O(|s| * n) in the worst case, which is around 10^10 operations and infeasible.

The key observation is that all patterns are known in advance, and their total length is small. This suggests building a global structure that can answer “where does this pattern occur in s” for many patterns at once. A suffix automaton or suffix array with LCP would work, but the most natural fit here is a suffix automaton augmented with end-position tracking.

A suffix automaton compactly represents all substrings of s and allows us to locate the state corresponding to any pattern in O(|pattern|). Each state represents a set of occurrences of substrings, and by propagating end positions through suffix links we can collect all occurrence indices for each matched pattern. Once we have all occurrences, we only need to compute the best window covering k consecutive sorted positions, which is a simple sliding window minimum over a sorted list.

Thus the solution becomes: build SAM, feed each query string through it, retrieve all end positions of that state, sort them, and compute the minimal span covering k consecutive occurrences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force scanning per query | O( | s | · n) |
| Suffix automaton + occurrence lists | O( | s | + Σ |

## Algorithm Walkthrough

We construct a suffix automaton over the main string. Each state stores transitions by character, suffix link, and length. Additionally, each state stores a list of end positions where substrings of that state occur. We populate these lists during construction by marking the terminal state of each prefix and propagating occurrences in decreasing order of state length.

For each query pattern, we walk the automaton character by character. If at any step we cannot follow a transition, the pattern does not exist and the answer is -1.

If we successfully reach a state, that state represents all occurrences of the pattern. We extract its occurrence list, which contains ending positions of all matches in the string. From each end position we derive the start position of the pattern occurrence.

We sort these start positions. We then scan a window of size k over this sorted list. For each window, we compute the substring span from the first occurrence start to the last occurrence end. The best answer is the minimum such span over all windows.

Finally, we output this minimum length or -1 if there are fewer than k occurrences.

### Why it works

Any substring containing k occurrences of a pattern induces k occurrence start positions inside it, and these must appear in increasing order. The tightest substring covering k occurrences is always defined by some consecutive block of k occurrences in sorted order, since skipping an occurrence only increases the span. The automaton guarantees we enumerate all occurrences correctly, and the sliding window guarantees we test all optimal consecutive groups without missing any configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SAM:
    def __init__(self, n):
        self.next = [dict()]
        self.link = [-1]
        self.length = [0]
        self.pos = [[]]
        self.last = 0

    def extend(self, c, idx):
        cur = len(self.next)
        self.next.append({})
        self.length.append(self.length[self.last] + 1)
        self.link.append(0)
        self.pos.append([idx])

        p = self.last
        while p != -1 and c not in self.next[p]:
            self.next[p][c] = cur
            p = self.link[p]

        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][c]
            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q
            else:
                clone = len(self.next)
                self.next.append(self.next[q].copy())
                self.length.append(self.length[p] + 1)
                self.link.append(self.link[q])
                self.pos.append([])

                while p != -1 and self.next[p].get(c) == q:
                    self.next[p][c] = clone
                    p = self.link[p]

                self.link[q] = self.link[cur] = clone

        self.last = cur

    def build(self, s):
        for i, ch in enumerate(s):
            self.extend(ch, i)

    def propagate(self):
        order = sorted(range(len(self.next)), key=lambda x: self.length[x], reverse=True)
        for v in order:
            if self.link[v] != -1:
                self.pos[self.link[v]].extend(self.pos[v])

    def match(self, t):
        v = 0
        for ch in t:
            if ch not in self.next[v]:
                return None
            v = self.next[v][ch]
        return v

s = input().strip()
sam = SAM(len(s))
sam.build(s)
sam.propagate()

q = int(input())
for _ in range(q):
    k, m = input().split()
    k = int(k)

    v = sam.match(m)
    if v is None:
        print(-1)
        continue

    occ = sam.pos[v]
    if len(occ) < k:
        print(-1)
        continue

    starts = [p - len(m) + 1 for p in occ]
    starts.sort()

    ans = 10**18
    for i in range(len(starts) - k + 1):
        l = starts[i]
        r = starts[i + k - 1] + len(m) - 1
        ans = min(ans, r - l + 1)

    print(ans)
```

The suffix automaton is built incrementally over the string, with each state recording one end position for every time it is created. After construction, occurrence lists are propagated along suffix links so that every state accumulates all terminal positions of substrings it represents. The match function walks transitions to locate the state corresponding to the pattern.

A subtle implementation detail is that propagation must occur in decreasing length order, otherwise suffix link aggregation loses correctness because shorter states depend on longer ones. Another important detail is converting end positions into start positions carefully with `p - len(m) + 1`, since SAM stores end indices.

The final window computation assumes occurrences are sorted; since SAM propagation does not guarantee order, explicit sorting is required.

## Worked Examples

Consider the sample string `aaaaa` and query pattern `aaa` with k = 2.

After propagation, occurrence end positions are `[2, 3, 4]`.

| Window | Occurrences (end) | Start positions | Span |
| --- | --- | --- | --- |
| [2,3] | 2,3 | 0,1 | 3 |
| [3,4] | 3, |  |  |