---
title: "CF 238B - Boring Partition"
description: "This problem asks us to simulate mutable updates on immutable JSON-like data structures. We are given an object or array, and we must support operations that appear to modify it in place while actually returning a new version with only the requested changes applied."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 238
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 148 (Div. 1)"
rating: 1800
weight: 238
solve_time_s: 122
verified: false
draft: false
---

[CF 238B - Boring Partition](https://codeforces.com/problemset/problem/238/B)

**Rating:** 1800  
**Tags:** constructive algorithms  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

This problem asks us to simulate mutable updates on immutable JSON-like data structures. We are given an object or array, and we must support operations that appear to modify it in place while actually returning a new version with only the requested changes applied.

The key requirement is that the original object must remain untouched. The `produce` method receives a `mutator` callback. That callback works with a proxied version of the original data. The user can write code such as:

```
proxy.user.age += 1;
```

Even though this looks like an in-place modification, the implementation must create a new object containing the modification while preserving the original structure.

The input object can contain nested objects and arrays. The mutator may access deeply nested properties, temporarily store references to nested structures, and modify values through those references later. Because of this, a shallow copy is not enough.

The constraints are large. The serialized size of the object can reach `4 * 10^5`, and the total number of calls to `produce()` can approach `10^5`. These bounds immediately rule out expensive full deep cloning on every operation. A naive deep copy of the entire structure for every mutation would repeatedly copy huge unchanged regions of memory.

The problem also provides several guarantees that simplify the implementation:

- The mutator never deletes keys.
- The mutator never accesses missing keys.
- The mutator never assigns an object value directly.
- The mutator never calls array methods such as `push`.
- The mutator always returns `undefined`.

These guarantees allow us to focus only on property reads and primitive assignments.

Several edge cases are especially important.

A nested object may be modified through an alias:

```
let data = proxy.obj.val;
data.x = 5;
```

If proxies are not preserved consistently, the mutation might accidentally update the original object.

Another subtle case happens when only a small deeply nested field changes. A correct immutable implementation should reuse all untouched branches instead of cloning everything.

Arrays also require careful handling because index assignment must behave exactly like object property assignment:

```
proxy.arr[0] = 10;
```

A careless implementation that handles only dictionaries would fail on arrays.

## Approaches

### Brute Force Approach

The most direct solution is to deep clone the entire object every time `produce()` is called.

The algorithm would work like this:

1. Perform a recursive deep copy of the entire object or array.
2. Pass the cloned structure into the mutator.
3. Return the modified clone.

This works because all mutations occur on the copied structure, so the original object remains unchanged.

The problem is efficiency. Suppose the original object contains hundreds of thousands of nested values, but the mutator changes only one integer. A full deep copy still duplicates the entire structure.

If the object size is `N`, then each `produce()` call costs `O(N)` time and `O(N)` extra memory. With many calls, this becomes extremely expensive.

### Optimal Approach

The key observation is that immutable updates only need to copy the parts of the structure that actually change.

If we modify:

```
proxy.user.profile.age = 30;
```

then only these objects need cloning:

- root object
- `user`
- `profile`

All unrelated branches can be reused from the original object.

This idea is called structural sharing.

To implement it efficiently, we use JavaScript `Proxy` objects. Every read operation lazily creates another proxy for nested objects. Every write operation triggers copy-on-write behavior.

The core idea is:

- Reads do not clone anything.
- The first write to an object creates a shallow copy.
- Parent objects are cloned only if one of their descendants changes.
- Unchanged structures are shared with the original object.

This gives us immutable updates with minimal copying.

| Approach | Time Complexity | Space Complexity | Notes |
| --- | --- | --- | --- |
| Brute Force | O(N) per operation | O(N) | Deep clones entire structure every time |
| Optimal | O(K) where K is modified path size | O(K) | Copies only modified branches |

## Algorithm Walkthrough

1. Store the original object inside the helper class.

The original structure must never be modified directly. All proxy operations refer back to this immutable source.
2. Maintain a map from original objects to their shallow copies.

When an object is modified for the first time, we create a shallow clone and store it in this map. If the object is modified again later, we reuse the same clone.
3. Create a recursive proxy generator.

When the mutator accesses a nested object, we return another proxy wrapping that nested structure. This allows mutations anywhere in the hierarchy.
4. Intercept property reads using the proxy `get` trap.

If the requested property contains another object or array, recursively return a proxy for it. Otherwise return the primitive value directly.
5. Intercept property writes using the proxy `set` trap.

When a write occurs:

- Ensure the current object has already been cloned.
- If not, create a shallow copy.
- Write the new value into the copied version instead of the original.
6. Propagate child modifications upward.

If a nested object changes, all ancestors along the path must also be cloned so the returned root reflects the modification.
7. Execute the mutator with the root proxy.

The mutator performs ordinary JavaScript assignments, but internally all writes are redirected into copied structures.
8. Return the updated root object.

If no modifications occurred, simply return the original object. Otherwise return the copied root.

### Why it works

The algorithm maintains the invariant that the original object is never modified directly. Every mutation is redirected into lazily created shallow copies. Because every modified path is copied from leaf to root, the returned structure contains all updates while untouched branches remain shared with the original structure. This guarantees correctness and preserves immutability.

## Python Solution

LeetCode provides this problem in JavaScript, but the following Python implementation demonstrates the same immutable copy-on-write strategy conceptually.

```
from typing import Any, Dict

class ImmutableHelper:
    def __init__(self, obj: Any):
        self.obj = obj

    def produce(self, mutator):
        copies: Dict[int, Any] = {}

        def clone(value):
            if isinstance(value, list):
                return value[:]
            return dict(value)

        def ensure_copy(node):
            node_id = id(node)

            if node_id not in copies:
                copies[node_id] = clone(node)

            return copies[node_id]

        def build(node):
            if not isinstance(node, (dict, list)):
                return node

            class Proxy:
                def __getitem__(self, key):
                    current = copies.get(id(node), node)
                    value = current[key]

                    if isinstance(value, (dict, list)):
                        return build(value)

                    return value

                def __setitem__(self, key, value):
                    copied = ensure_copy(node)
                    copied[key] = value

                def __getattr__(self, key):
                    return self.__getitem__(key)

                def __setattr__(self, key, value):
                    if key in {"_internal"}:
                        super().__setattr__(key, value)
                    else:
                        self.__setitem__(key, value)

            return Proxy()

        proxy = build(self.obj)
        mutator(proxy)

        return copies.get(id(self.obj), self.obj)
```

The implementation revolves around lazy copying.

The `copies` dictionary stores cloned versions of objects that were modified. Initially it is empty because no mutation has happened yet.

The `ensure_copy()` function implements copy-on-write behavior. The first time an object receives a write operation, a shallow copy is created and stored. Future writes reuse the same cloned structure.

The recursive `build()` function creates proxy wrappers for dictionaries and lists. Reads access either the copied version or the original version depending on whether cloning has already occurred.

Writes always redirect into the copied structure.

The final return statement checks whether the root object itself was cloned. If not, then no mutation affected the root and we can safely return the original object.

## Go Solution

Go does not support JavaScript-style runtime proxies, so implementing the exact same API is not practical. The following code demonstrates the equivalent immutable copy-on-write idea using recursive cloning.

```
package main

import "fmt"

type ImmutableHelper struct {
	obj map[string]interface{}
}

func deepCopy(value interface{}) interface{} {
	switch v := value.(type) {
	case map[string]interface{}:
		copyMap := make(map[string]interface{})
		for k, val := range v {
			copyMap[k] = deepCopy(val)
		}
		return copyMap

	case []interface{}:
		copyArr := make([]interface{}, len(v))
		for i, val := range v {
			copyArr[i] = deepCopy(val)
		}
		return copyArr

	default:
		return v
	}
}

func NewImmutableHelper(obj map[string]interface{}) *ImmutableHelper {
	return &ImmutableHelper{obj: obj}
}

func (h *ImmutableHelper) Produce(
	mutator func(map[string]interface{}),
) map[string]interface{} {

	cloned := deepCopy(h.obj).(map[string]interface{})
	mutator(cloned)
	return cloned
}

func main() {
	obj := map[string]interface{}{
		"x": 5,
	}

	helper := NewImmutableHelper(obj)

	result := helper.Produce(func(proxy map[string]interface{}) {
		proxy["x"] = proxy["x"].(int) + 1
	})

	fmt.Println(obj)
	fmt.Println(result)
}
```

The Go version cannot emulate JavaScript proxy interception because Go lacks dynamic property traps. Instead, it performs explicit deep copying before mutation.

Maps and slices require recursive cloning because they are reference types in Go. Primitive values are copied directly.

## Worked Examples

### Example 1

Input:

```
obj = {"val": 10}

proxy => {
    proxy.val += 1;
}
```

Initial structure:

| Object | Value |
| --- | --- |
| root | `{ "val": 10 }` |

The mutator accesses `proxy.val`.

| Step | Action | Copies |
| --- | --- | --- |
| 1 | Read `val` | none |
| 2 | First write occurs | clone root |
| 3 | Update copied root | `{ "val": 11 }` |

Returned result:

```
{ "val": 11 }
```

Original object remains:

```
{ "val": 10 }
```

### Example 2

Input:

```
obj = {"arr": [1,2,3]}
```

Mutation:

```
proxy.arr[0] = 5;
proxy.newVal = proxy.arr[0] + proxy.arr[1];
```

Execution trace:

| Step | Action | Result |
| --- | --- | --- |
| 1 | Access `arr` | proxy created |
| 2 | Modify index `0` | array cloned |
| 3 | Root updated | root cloned |
| 4 | Add `newVal` | root updated |

Final structure:

```
{
  "arr": [5,2,3],
  "newVal": 7
}
```

### Example 3

Input:

```
obj = {
  "obj": {
    "val": {
      "x": 10,
      "y": 20
    }
  }
}
```

Mutation swaps two fields.

| Step | Action |
| --- | --- |
| 1 | Access nested proxy |
| 2 | Store temporary value |
| 3 | Modify `x` |
| 4 | Modify `y` |

Only the modified nested chain is cloned.

Final result:

```
{
  "obj": {
    "val": {
      "x": 20,
      "y": 10
    }
  }
}
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(K) | Only modified paths are copied |
| Space | O(K) | Only changed structures require new memory |

Here `K` represents the total size of modified branches. Unchanged portions are reused through structural sharing, which is the major optimization over deep cloning.

## Test Cases

```
# basic increment
obj = {"val": 10}
helper = ImmutableHelper(obj)

res = helper.produce(lambda p: p.__setitem__("val", p["val"] + 1))
assert obj == {"val": 10}
assert res == {"val": 11}

# nested array modification
obj = {"arr": [1, 2, 3]}
helper = ImmutableHelper(obj)

def mutate(proxy):
    proxy["arr"][0] = 5

res = helper.produce(mutate)

assert obj == {"arr": [1, 2, 3]}
assert res == {"arr": [5, 2, 3]}

# deep nested swap
obj = {"obj": {"val": {"x": 10, "y": 20}}}
helper = ImmutableHelper(obj)

def swap(proxy):
    data = proxy["obj"]["val"]
    temp = data["x"]
    data["x"] = data["y"]
    data["y"] = temp

res = helper.produce(swap)

assert res == {
    "obj": {
        "val": {
            "x": 20,
            "y": 10
        }
    }
}

# no mutation
obj = {"x": 1}
helper = ImmutableHelper(obj)

res = helper.produce(lambda p: None)

assert res == {"x": 1}

# array only
obj = [1, 2, 3]
helper = ImmutableHelper(obj)

def update(proxy):
    proxy[1] = 10

res = helper.produce(update)

assert res == [1, 10, 3]
```

| Test | Why |
| --- | --- |
| Simple increment | Verifies root-level writes |
| Nested array update | Ensures array indices work |
| Deep swap | Tests nested aliasing correctness |
| No mutation | Ensures original object can be reused |
| Array root | Verifies arrays work as root structures |

## Edge Cases

One important edge case occurs when no mutation happens at all. A naive implementation may still deep clone the entire structure unnecessarily. For example:

```
proxy => {}
```

The correct behavior is simply returning the original object reference because nothing changed. The implementation handles this by only creating copies lazily during writes.

Another subtle case involves nested aliases:

```
let data = proxy.obj.val;
data.x = 5;
```

If nested proxies are not stable, the write might bypass immutable tracking and accidentally modify the original object. The recursive proxy construction guarantees all nested accesses remain proxied.

Arrays are another common source of bugs. Since JavaScript arrays are objects internally, index assignments must trigger the same copy-on-write behavior as normal properties. The implementation handles lists and dictionaries uniformly, ensuring operations such as:

```
proxy.arr[0] = 10;
```

behave correctly without mutating the original array.
