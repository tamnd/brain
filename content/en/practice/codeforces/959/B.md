---
problem: 959B
contest_id: 959
problem_index: B
name: "Mahmoud and Ehab and the message"
contest_name: "Codeforces Round 473 (Div. 2)"
rating: 1200
tags: ["dsu", "greedy", "implementation"]
answer: passed_samples
verified: true
solve_time_s: 67
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a327fbf-b66c-83ec-981d-3b18ee9546df
---

# CF 959B - Mahmoud and Ehab and the message

**Rating:** 1200  
**Tags:** dsu, greedy, implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 7s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a327fbf-b66c-83ec-981d-3b18ee9546df  

---

## Solution

## Problem Understanding

We are given a vocabulary where each word has a fixed cost of sending, and some words are grouped together because they share the same meaning. Within a group, any word can be replaced by any other word in that same group without changing the meaning of the message.

A message is a sequence of words. For each word in the message, we are allowed to either send it as it is or replace it with another word from its equivalence group. The cost we pay for that position is simply the cost of the word we choose to send.

The goal is to minimize the total cost of sending the full message.

The important structure is that each word belongs to exactly one group, and replacement is only allowed within that group. This turns the problem into choosing, for each message word, the cheapest representative inside its group.

The constraints go up to 100,000 words, groups, and message length. This immediately rules out any solution that tries to explore replacements per word using nested searches over group members. A naive per-word scan of its group is already too slow if groups are large, since the total work could degrade toward quadratic behavior.

A subtle failure case appears when a group contains a very expensive word and a very cheap word. If we mistakenly assume we should always keep the original word, we miss improvements. For example, if a group is `{A(cost 100), B(cost 1)}` and the message contains `A`, the optimal answer uses `B` instead. Any solution that does not precompute minimum costs per group will fail here.

Another edge case arises when groups are singletons. In that case, replacement is impossible, so the original cost must be used directly. This should not break the logic, but it is easy to mishandle if group processing assumes at least two elements.

## Approaches

A brute-force approach would process each message word independently. For every word in the message, we locate its group and scan all words in that group to find the minimum cost. If we assume worst-case grouping where almost all words belong to one large group, each query could cost O(n), and with m queries this leads to O(nm), which is too large for 10^5 constraints.

The key observation is that the message cost depends only on the minimum cost inside each group, not on the structure of replacements. Once we know the cheapest word in each equivalence class, every occurrence of any word in that class can be replaced by that cheapest word.

This reduces the problem to a preprocessing step: compute, for every group, the minimum cost among its members. Then map each word to its group minimum cost, and sum over the message.

We can implement this efficiently using a hash map from word to index, an array mapping index to group id, and an array storing group minimum costs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O(n + m + n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all words and assign each word an index.

This allows constant-time lookup from message strings to their cost and group.
2. Read the cost array and associate each cost with its word index.

Now every word knows its sending cost.
3. Build a mapping from each word index to its group id.

Since each word belongs to exactly one group, this is a direct assignment.
4. For each group, compute the minimum cost among all words in that group.

We scan group members once and maintain a running minimum.
5. For each word in the message, convert it to its index, then replace its cost by the precomputed group minimum cost.

This models the best possible substitution allowed.
6. Sum these minimum costs over all message words and output the result.

### Why it works

Each message word is independent in terms of replacement choices. The only constraint is that replacements stay inside the same group. Since there are no interactions between positions in the message, optimizing each position independently is globally optimal. Within a group, choosing anything other than the minimum cost word can only increase cost, so the minimum is always optimal for every occurrence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, m = map(int, input().split())
    
    words = input().split()
    cost = list(map(int, input().split()))
    
    idx = {w: i for i, w in enumerate(words)}
    
    group = [-1] * n
    group_min = [10**18] * k
    
    for gid in range(k):
        data = list(map(int, input().split()))
        x = data[0]
        members = data[1:]
        for v in members:
            v -= 1
            group[v] = gid
            group_min[gid] = min(group_min[gid], cost[v])
    
    msg = input().split()
    
    ans = 0
    for w in msg:
        i = idx[w]
        g = group[i]
        ans += group_min[g]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution builds a dictionary from words to indices so message lookup is constant time. It then assigns each word to a group while simultaneously computing the minimum cost for that group. The final loop over the message simply translates each word into its group id and accumulates the corresponding minimum cost. The subtraction of 1 from indices is necessary because input groups are 1-based.

A common pitfall is recomputing group minima during query time instead of preprocessing. That would turn each message lookup into a scan over a group, which is unnecessary and too slow.

## Worked Examples

### Example 1

Input:

```
5 4 4
i loser am the second
100 1 1 5 10
1 1
1 3
2 2 5
1 4
i am the second
```

| word | index | group | group min cost | used cost |
| --- | --- | --- | --- | --- |
| i | 0 | 0 | 100 | 100 |
| am | 2 | 1 | 1 | 1 |
| the | 3 | 3 | 5 | 5 |
| second | 4 | 2 | 1 | 1 |

Total is 107.

This trace shows that even though "second" is expensive, it is replaced by the cheapest word in its group, which is "loser".

### Example 2

Input:

```
3 2 3
a b c
10 20 30
1 1
2 2 3
a b c
```

| word | index | group | group min cost | used cost |
| --- | --- | --- | --- | --- |
| a | 0 | 0 | 10 | 10 |
| b | 1 | 1 | 20 | 20 |
| c | 2 | 1 | 20 | 20 |

Total is 50.

This confirms that within a group containing multiple words, all occurrences use the same cheapest representative.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k + m) | Each word, group membership, and message token is processed once |
| Space | O(n) | Arrays for word mapping, group assignment, and group minima |

The solution fits easily within limits since all operations are linear in the input size, and dictionary lookups are constant time on average.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins
    return main(inp) if False else solve_capture(inp)

def solve_capture(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k, m = map(int, input().split())
    words = input().split()
    cost = list(map(int, input().split()))
    idx = {w: i for i, w in enumerate(words)}

    group = [-1] * n
    group_min = [10**18] * k

    for gid in range(k):
        data = list(map(int, input().split()))
        x = data[0]
        members = data[1:]
        for v in members:
            v -= 1
            group[v] = gid
            group_min[gid] = min(group_min[gid], cost[v])

    msg = input().split()

    ans = 0
    for w in msg:
        ans += group_min[group[idx[w]]]

    return str(ans)

# provided sample
assert solve_capture("""5 4 4
i loser am the second
100 1 1 5 10
1 1
1 3
2 2 5
1 4
i am the second
""") == "107"

# singleton groups
assert solve_capture("""3 3 3
a b c
5 1 10
1 1
1 2
1 3
a b c
""") == "16"

# all in one group
assert solve_capture("""3 1 3
a b c
10 5 7
3 1 2 3
a b c
""") == "15"

# already optimal
assert solve_capture("""2 2 2
x y
3 4
1 1
1 2
x y
""") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 107 | basic correctness |
| singleton groups | 16 | no replacement possible |
| all in one group | 15 | global minimum propagation |
| already optimal | 7 | no unnecessary replacement |

## Edge Cases

A singleton group such as `1 1` ensures that the word has no alternatives. The algorithm assigns its own cost as the group minimum, so queries correctly use the original value.

A large group containing all words tests whether the preprocessing correctly propagates a single minimum across all message positions. The algorithm computes one global minimum and applies it consistently.

A message repeating the same word multiple times checks that lookup is stable and does not recompute or mutate state. Each occurrence independently fetches the same precomputed group minimum, preserving correctness.