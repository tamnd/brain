
### 1. Core data structures and operations (320)

This layer defines the primitives you will use everywhere else. The emphasis is on memory layout, constant factors, and basic invariants. Each structure should be understood at the level of implementation, not just usage.

### 1.1 Arrays and dynamic arrays (35)

| index | slug                     | name                   | description                                           |
| ----- | ------------------------ | ---------------------- | ----------------------------------------------------- |
| 1     | static-array             | Static Array           | Fixed-size contiguous memory block with O(1) indexing |
| 2     | dynamic-array            | Dynamic Array          | Resizable array with amortized O(1) append            |
| 3     | vector-resize-strategy   | Resize Strategy        | Doubling, golden ratio growth, shrink policies        |
| 4     | circular-array           | Circular Array         | Wrap-around indexing for bounded buffers              |
| 5     | multidimensional-array   | Multidimensional Array | Row-major and column-major layouts                    |
| 6     | jagged-array             | Jagged Array           | Array of arrays with uneven lengths                   |
| 7     | array-slicing            | Array Slicing          | Views vs copies and memory implications               |
| 8     | array-rotation           | Array Rotation         | In-place rotation algorithms                          |
| 9     | prefix-sum-array         | Prefix Sum Array       | Precomputed cumulative sums                           |
| 10    | difference-array         | Difference Array       | Efficient range updates                               |
| 11    | sliding-window-array     | Sliding Window         | Fixed/variable window techniques                      |
| 12    | sparse-array             | Sparse Array           | Space-efficient representation                        |
| 13    | bit-packed-array         | Bit Packed Array       | Compact storage using bit fields                      |
| 14    | dynamic-reserve          | Capacity Reservation   | Preallocation strategies                              |
| 15    | amortized-analysis-array | Amortized Analysis     | Cost model for resizing                               |
| 16    | array-partition          | Partitioning           | In-place partition operations                         |
| 17    | array-stable-partition   | Stable Partition       | Order-preserving partition                            |
| 18    | array-reversal           | Reversal               | In-place reversal                                     |
| 19    | array-shuffle            | Shuffle                | Uniform random permutation                            |
| 20    | array-scan               | Linear Scan            | Basic iteration patterns                              |
| 21    | array-compaction         | Compaction             | Remove elements in-place                              |
| 22    | array-deduplication      | Deduplication          | Remove duplicates                                     |
| 23    | array-merge              | Merge                  | Merge sorted arrays                                   |
| 24    | array-intersection       | Intersection           | Compute common elements                               |
| 25    | array-union              | Union                  | Combine unique elements                               |
| 26    | array-binary-layout      | Memory Layout          | Alignment and cache effects                           |
| 27    | array-copying            | Copy Strategies        | Deep vs shallow copy                                  |
| 28    | array-buffering          | Buffering              | Temporary buffer usage                                |
| 29    | array-index-mapping      | Index Mapping          | Logical to physical mapping                           |
| 30    | array-bounds-check       | Bounds Checking        | Safe vs unsafe access                                 |
| 31    | array-stride-access      | Stride Access          | Cache-friendly traversal                              |
| 32    | array-blocking           | Blocking               | Cache blocking techniques                             |
| 33    | array-tiling             | Tiling                 | Subdivision for locality                              |
| 34    | array-vectorization      | Vectorization          | SIMD-friendly layout                                  |
| 35    | array-alignment          | Alignment              | Memory alignment constraints                          |


### 1.2 Linked lists (35)

| index | slug                 | name                 | description                   |
| ----- | -------------------- | -------------------- | ----------------------------- |
| 1     | singly-linked-list   | Singly Linked List   | Nodes with single pointer     |
| 2     | doubly-linked-list   | Doubly Linked List   | Bidirectional traversal       |
| 3     | circular-linked-list | Circular Linked List | Last node points to head      |
| 4     | sentinel-list        | Sentinel List        | Dummy nodes to simplify logic |
| 5     | intrusive-list       | Intrusive List       | Node embedded in data         |
| 6     | skip-pointer-list    | Skip Pointer List    | Fast traversal shortcuts      |
| 7     | list-insertion       | Insertion            | Insert at head, tail, middle  |
| 8     | list-deletion        | Deletion             | Remove nodes safely           |
| 9     | list-reversal        | Reversal             | Iterative and recursive       |
| 10    | list-cycle-detection | Cycle Detection      | Floyd algorithm               |
| 11    | list-merge           | Merge                | Merge sorted lists            |
| 12    | list-split           | Split                | Divide list                   |
| 13    | list-concatenation   | Concatenation        | Join lists                    |
| 14    | list-length          | Length               | Count nodes                   |
| 15    | list-middle          | Find Middle          | Fast/slow pointer             |
| 16    | list-kth-element     | Kth Element          | Index access                  |
| 17    | list-copy            | Copy                 | Deep copy                     |
| 18    | list-clone-random    | Clone Random         | Copy with random pointers     |
| 19    | list-sort            | List Sort            | Merge sort on list            |
| 20    | list-partition       | Partition            | Split around pivot            |
| 21    | list-rotation        | Rotation             | Rotate list                   |
| 22    | list-palindrome      | Palindrome Check     | Symmetry detection            |
| 23    | list-flatten         | Flatten              | Nested list flatten           |
| 24    | list-intersection    | Intersection         | Shared nodes                  |
| 25    | list-union           | Union                | Combine lists                 |
| 26    | list-deduplication   | Deduplication        | Remove duplicates             |
| 27    | list-queue-emulation | Queue via List       | FIFO behavior                 |
| 28    | list-stack-emulation | Stack via List       | LIFO behavior                 |
| 29    | list-memory-pool     | Memory Pool          | Node reuse                    |
| 30    | list-pointer-safety  | Pointer Safety       | Null handling                 |
| 31    | list-lazy-deletion   | Lazy Deletion        | Mark instead of remove        |
| 32    | list-indexing        | Indexing             | Simulated indexing            |
| 33    | list-splice          | Splice               | Move segments                 |
| 34    | list-iterator        | Iterator             | Traversal abstraction         |
| 35    | list-locking         | Locking              | Thread-safe variants          |


### 1.3 Stacks (25)

| index | slug                | name               | description          |
| ----- | ------------------- | ------------------ | -------------------- |
| 1     | array-stack         | Array Stack        | Stack using array    |
| 2     | linked-stack        | Linked Stack       | Stack using list     |
| 3     | dynamic-stack       | Dynamic Stack      | Resizable stack      |
| 4     | stack-push-pop      | Push Pop           | Core operations      |
| 5     | stack-min           | Min Stack          | Track minimum        |
| 6     | stack-max           | Max Stack          | Track maximum        |
| 7     | stack-two-in-one    | Two Stacks         | Share array          |
| 8     | stack-k-in-one      | K Stacks           | Multiple stacks      |
| 9     | stack-using-queue   | Stack via Queue    | Simulation           |
| 10    | stack-recursion     | Recursion Stack    | Implicit stack       |
| 11    | stack-call-frame    | Call Stack         | Function frames      |
| 12    | stack-evaluation    | Expression Eval    | RPN evaluation       |
| 13    | stack-parentheses   | Parentheses Check  | Balance checking     |
| 14    | stack-monotonic     | Monotonic Stack    | Next greater/smaller |
| 15    | stack-span          | Stock Span         | Range queries        |
| 16    | stack-histogram     | Histogram          | Largest rectangle    |
| 17    | stack-backtracking  | Backtracking       | DFS support          |
| 18    | stack-undo          | Undo Stack         | History tracking     |
| 19    | stack-iterator      | Iterator           | Traversal            |
| 20    | stack-bounded       | Bounded Stack      | Fixed capacity       |
| 21    | stack-overflow      | Overflow Handling  | Limits               |
| 22    | stack-underflow     | Underflow Handling | Empty cases          |
| 23    | stack-memory-layout | Layout             | Memory structure     |
| 24    | stack-thread-safe   | Thread Safe        | Synchronization      |
| 25    | stack-lock-free     | Lock Free Stack    | CAS-based            |


### 1.4 Queues and deques (35)

| index | slug                  | name                 | description         |
| ----- | --------------------- | -------------------- | ------------------- |
| 1     | array-queue           | Array Queue          | FIFO array          |
| 2     | circular-queue        | Circular Queue       | Wrap-around queue   |
| 3     | linked-queue          | Linked Queue         | Node-based queue    |
| 4     | deque                 | Deque                | Double-ended queue  |
| 5     | priority-queue-basic  | Basic Priority Queue | Ordered removal     |
| 6     | queue-enqueue-dequeue | Enqueue Dequeue      | Core ops            |
| 7     | queue-two-stacks      | Queue via Stacks     | Simulation          |
| 8     | deque-array           | Array Deque          | Circular buffer     |
| 9     | deque-linked          | Linked Deque         | List-based          |
| 10    | monotonic-queue       | Monotonic Queue      | Sliding window      |
| 11    | blocking-queue        | Blocking Queue       | Thread sync         |
| 12    | lock-free-queue       | Lock Free Queue      | Non-blocking        |
| 13    | queue-buffer          | Buffer Queue         | Streaming           |
| 14    | queue-scheduler       | Scheduler Queue      | Task ordering       |
| 15    | queue-bfs             | BFS Queue            | Graph traversal     |
| 16    | queue-rotation        | Rotation             | Cyclic shift        |
| 17    | queue-partition       | Partition            | Split queue         |
| 18    | queue-merge           | Merge                | Combine queues      |
| 19    | queue-copy            | Copy                 | Duplicate           |
| 20    | queue-bounded         | Bounded Queue        | Capacity limit      |
| 21    | queue-unbounded       | Unbounded Queue      | Dynamic growth      |
| 22    | queue-lazy            | Lazy Queue           | Deferred ops        |
| 23    | queue-iterator        | Iterator             | Traversal           |
| 24    | queue-memory-layout   | Layout               | Memory              |
| 25    | queue-cache           | Cache Queue          | Cache design        |
| 26    | queue-rate-limit      | Rate Limit Queue     | Throttling          |
| 27    | queue-priority-bucket | Bucket Queue         | Discrete priorities |
| 28    | queue-round-robin     | Round Robin          | Scheduling          |
| 29    | queue-multi-level     | Multi-level Queue    | Priority tiers      |
| 30    | queue-delay           | Delay Queue          | Time-based          |
| 31    | queue-event           | Event Queue          | Event systems       |
| 32    | queue-pipeline        | Pipeline Queue       | Streaming           |
| 33    | queue-batch           | Batch Queue          | Bulk ops            |
| 34    | queue-thread-safe     | Thread Safe          | Locks               |
| 35    | queue-lock-free       | Lock Free Deque      | CAS-based           |

### 1.5 Heaps and priority queues (55)

| index | slug                            | name                        | description                                             |
| ----- | ------------------------------- | --------------------------- | ------------------------------------------------------- |
| 1     | binary-heap                     | Binary Heap                 | Array-backed complete binary tree with heap order       |
| 2     | min-heap                        | Min Heap                    | Heap where the minimum element is at the root           |
| 3     | max-heap                        | Max Heap                    | Heap where the maximum element is at the root           |
| 4     | heap-insert                     | Heap Insert                 | Add an element and restore heap order by sift-up        |
| 5     | heap-extract-min                | Extract Minimum             | Remove the minimum element from a min heap              |
| 6     | heap-extract-max                | Extract Maximum             | Remove the maximum element from a max heap              |
| 7     | heap-peek                       | Heap Peek                   | Read the root element without removing it               |
| 8     | heap-sift-up                    | Sift Up                     | Move a node upward until heap order holds               |
| 9     | heap-sift-down                  | Sift Down                   | Move a node downward until heap order holds             |
| 10    | heapify                         | Heapify                     | Convert an array into a heap in linear time             |
| 11    | bottom-up-heap-construction     | Bottom-Up Heap Construction | Build a heap from leaves toward root                    |
| 12    | top-down-heap-construction      | Top-Down Heap Construction  | Build a heap by repeated insertion                      |
| 13    | heap-replace                    | Heap Replace                | Remove root and insert a new item in one operation      |
| 14    | heap-push-pop                   | Heap Push Pop               | Insert then extract while avoiding two full operations  |
| 15    | heap-decrease-key               | Decrease Key                | Lower a key and restore heap order upward               |
| 16    | heap-increase-key               | Increase Key                | Raise a key and restore heap order downward             |
| 17    | heap-delete                     | Heap Delete                 | Remove an arbitrary heap element                        |
| 18    | heap-update-key                 | Update Key                  | Change a key and repair heap position                   |
| 19    | d-ary-heap                      | D-ary Heap                  | Heap where each node has d children                     |
| 20    | ternary-heap                    | Ternary Heap                | D-ary heap with three children per node                 |
| 21    | quaternary-heap                 | Quaternary Heap             | D-ary heap with four children per node                  |
| 22    | binomial-heap                   | Binomial Heap               | Mergeable heap built from binomial trees                |
| 23    | fibonacci-heap                  | Fibonacci Heap              | Lazy mergeable heap with cheap decrease-key             |
| 24    | pairing-heap                    | Pairing Heap                | Simple self-adjusting mergeable heap                    |
| 25    | leftist-heap                    | Leftist Heap                | Mergeable heap biased by null-path length               |
| 26    | skew-heap                       | Skew Heap                   | Self-adjusting mergeable heap                           |
| 27    | rank-pairing-heap               | Rank Pairing Heap           | Fibonacci-like heap with simpler structure              |
| 28    | hollow-heap                     | Hollow Heap                 | Heap using hollow nodes for efficient decrease-key      |
| 29    | soft-heap                       | Soft Heap                   | Approximate heap that permits controlled key corruption |
| 30    | treap-priority-queue            | Treap Priority Queue        | Priority queue represented with randomized priorities   |
| 31    | bucket-priority-queue           | Bucket Priority Queue       | Priority queue for small integer priorities             |
| 32    | radix-heap                      | Radix Heap                  | Integer priority queue for monotone keys                |
| 33    | calendar-queue                  | Calendar Queue              | Bucketed priority queue for event simulation            |
| 34    | indexed-priority-queue          | Indexed Priority Queue      | Priority queue with handles for key updates             |
| 35    | addressable-priority-queue      | Addressable Priority Queue  | Priority queue supporting access to stored items        |
| 36    | meldable-priority-queue         | Meldable Priority Queue     | Priority queue supporting efficient merge               |
| 37    | bounded-priority-queue          | Bounded Priority Queue      | Keeps only the best k elements                          |
| 38    | double-ended-priority-queue     | Double-Ended Priority Queue | Supports finding both minimum and maximum               |
| 39    | min-max-heap                    | Min-Max Heap                | Heap supporting O(1) min and max lookup                 |
| 40    | interval-heap                   | Interval Heap               | Double-ended heap storing intervals in nodes            |
| 41    | median-heap                     | Median Heap                 | Two-heap structure for online median                    |
| 42    | k-way-merge-heap                | K-Way Merge Heap            | Merge many sorted streams with a heap                   |
| 43    | top-k-heap                      | Top K Heap                  | Maintain the largest or smallest k elements             |
| 44    | heap-sort                       | Heap Sort                   | Sort by heap construction and repeated extraction       |
| 45    | partial-heap-sort               | Partial Heap Sort           | Extract only the first k sorted elements                |
| 46    | heap-selection                  | Heap Selection              | Select elements using heap ordering                     |
| 47    | lazy-deletion-heap              | Lazy Deletion Heap          | Mark removed entries and clean them later               |
| 48    | stable-priority-queue           | Stable Priority Queue       | Break equal priorities by insertion order               |
| 49    | priority-queue-with-tie-breaker | Tie-Breaking Priority Queue | Use secondary keys for deterministic order              |
| 50    | concurrent-priority-queue       | Concurrent Priority Queue   | Priority queue safe for multiple threads                |
| 51    | lock-free-priority-queue        | Lock-Free Priority Queue    | Non-blocking priority queue design                      |
| 52    | external-memory-heap            | External Memory Heap        | Heap variant optimized for disk or SSD                  |
| 53    | tournament-tree                 | Tournament Tree             | Tree structure for repeated minimum selection           |
| 54    | loser-tree                      | Loser Tree                  | Tournament structure useful in external merging         |
| 55    | heap-invariant-check            | Heap Invariant Check        | Verify structural and ordering invariants               |

### 1.6 Hash tables and sets (60)

| index | slug                     | name                    | description                                       |
| ----- | ------------------------ | ----------------------- | ------------------------------------------------- |
| 1     | hash-table               | Hash Table              | Key value store with expected O(1) operations     |
| 2     | hash-function            | Hash Function           | Map keys to integer indices                       |
| 3     | universal-hashing        | Universal Hashing       | Family of hash functions with provable guarantees |
| 4     | multiplicative-hashing   | Multiplicative Hashing  | Use multiplication and bit shifts                 |
| 5     | division-hashing         | Division Hashing        | Use modulo table size                             |
| 6     | polynomial-hashing       | Polynomial Hashing      | Rolling hash for strings                          |
| 7     | string-hashing           | String Hashing          | Hash sequences of characters                      |
| 8     | rolling-hash             | Rolling Hash            | Sliding window hash updates                       |
| 9     | cryptographic-hash       | Cryptographic Hash      | Collision-resistant hashing                       |
| 10    | open-addressing          | Open Addressing         | Store elements in array slots                     |
| 11    | linear-probing           | Linear Probing          | Resolve collisions by sequential scan             |
| 12    | quadratic-probing        | Quadratic Probing       | Quadratic step probing                            |
| 13    | double-hashing           | Double Hashing          | Use second hash for probing                       |
| 14    | robin-hood-hashing       | Robin Hood Hashing      | Balance probe lengths                             |
| 15    | hopscotch-hashing        | Hopscotch Hashing       | Neighborhood-based placement                      |
| 16    | cuckoo-hashing           | Cuckoo Hashing          | Two hash functions with relocation                |
| 17    | chained-hashing          | Chained Hashing         | Buckets store lists of elements                   |
| 18    | separate-chaining        | Separate Chaining       | Linked lists per bucket                           |
| 19    | bucket-hashing           | Bucket Hashing          | Fixed-size buckets                                |
| 20    | dynamic-resizing-hash    | Dynamic Resizing        | Grow and shrink table                             |
| 21    | load-factor              | Load Factor             | Ratio of filled slots                             |
| 22    | rehashing                | Rehashing               | Rebuild table with new size                       |
| 23    | incremental-rehashing    | Incremental Rehashing   | Spread rehash over operations                     |
| 24    | hash-table-deletion      | Deletion                | Remove keys safely                                |
| 25    | tombstones               | Tombstones              | Mark deleted slots                                |
| 26    | cache-conscious-hashing  | Cache Conscious Hashing | Improve locality                                  |
| 27    | perfect-hashing          | Perfect Hashing         | No collisions for fixed set                       |
| 28    | minimal-perfect-hashing  | Minimal Perfect Hashing | No collisions with minimal space                  |
| 29    | static-hash-table        | Static Hash Table       | Fixed set of keys                                 |
| 30    | dynamic-hash-table       | Dynamic Hash Table      | Supports insertions and deletions                 |
| 31    | extendible-hashing       | Extendible Hashing      | Directory-based dynamic hashing                   |
| 32    | linear-hashing           | Linear Hashing          | Incremental table growth                          |
| 33    | consistent-hashing       | Consistent Hashing      | Distribute keys across nodes                      |
| 34    | rendezvous-hashing       | Rendezvous Hashing      | Highest random weight hashing                     |
| 35    | hash-set                 | Hash Set                | Store unique keys                                 |
| 36    | hash-map                 | Hash Map                | Map keys to values                                |
| 37    | multi-map                | Multi Map               | Allow duplicate keys                              |
| 38    | multi-set                | Multi Set               | Allow duplicate elements                          |
| 39    | ordered-hash-map         | Ordered Hash Map        | Preserve insertion order                          |
| 40    | linked-hash-map          | Linked Hash Map         | Hash map with linked order                        |
| 41    | lru-cache                | LRU Cache               | Eviction by recency                               |
| 42    | lfu-cache                | LFU Cache               | Eviction by frequency                             |
| 43    | frequency-map            | Frequency Map           | Count occurrences                                 |
| 44    | hash-table-iteration     | Iteration               | Traverse entries                                  |
| 45    | hash-table-serialization | Serialization           | Save and load                                     |
| 46    | hash-table-thread-safe   | Thread Safe Hash Table  | Synchronization mechanisms                        |
| 47    | lock-free-hash-table     | Lock Free Hash Table    | Non-blocking design                               |
| 48    | concurrent-hash-map      | Concurrent Hash Map     | Scalable multi-threaded map                       |
| 49    | sharded-hash-table       | Sharded Hash Table      | Partitioned locks                                 |
| 50    | bloom-filter             | Bloom Filter            | Probabilistic membership                          |
| 51    | counting-bloom-filter    | Counting Bloom Filter   | Support deletions                                 |
| 52    | cuckoo-filter            | Cuckoo Filter           | Improved membership filter                        |
| 53    | quotient-filter          | Quotient Filter         | Compact approximate set                           |
| 54    | xor-filter               | XOR Filter              | Fast compact filter                               |
| 55    | hash-table-attacks       | Hash Attacks            | Adversarial inputs                                |
| 56    | hash-randomization       | Hash Randomization      | Defend against attacks                            |
| 57    | memory-layout-hash       | Memory Layout           | Cache and alignment                               |
| 58    | hash-table-benchmark     | Benchmarking            | Measure performance                               |
| 59    | hash-table-debugging     | Debugging               | Detect issues                                     |
| 60    | hash-table-invariant     | Invariant Check         | Validate structure                                |


### 1.7 Binary search trees (45)

| index | slug                       | name                 | description                             |
| ----- | -------------------------- | -------------------- | --------------------------------------- |
| 1     | binary-search-tree         | Binary Search Tree   | Ordered binary tree with key invariants |
| 2     | bst-insert                 | BST Insert           | Insert a node                           |
| 3     | bst-delete                 | BST Delete           | Remove a node                           |
| 4     | bst-search                 | BST Search           | Lookup operation                        |
| 5     | bst-minimum                | Minimum              | Smallest element                        |
| 6     | bst-maximum                | Maximum              | Largest element                         |
| 7     | bst-predecessor            | Predecessor          | Previous key                            |
| 8     | bst-successor              | Successor            | Next key                                |
| 9     | bst-height                 | Height               | Depth measurement                       |
| 10    | bst-depth                  | Depth                | Node depth                              |
| 11    | bst-traversal-inorder      | Inorder Traversal    | Sorted traversal                        |
| 12    | bst-traversal-preorder     | Preorder Traversal   | Root first                              |
| 13    | bst-traversal-postorder    | Postorder Traversal  | Root last                               |
| 14    | bst-level-order            | Level Order          | Breadth-first                           |
| 15    | bst-iterative-traversal    | Iterative Traversal  | Stack-based                             |
| 16    | bst-recursive-traversal    | Recursive Traversal  | DFS                                     |
| 17    | bst-balance-check          | Balance Check        | Height difference                       |
| 18    | bst-degenerate-case        | Degenerate Tree      | Linked list behavior                    |
| 19    | bst-construction           | Construction         | Build from array                        |
| 20    | bst-from-sorted-array      | Sorted Build         | Balanced tree                           |
| 21    | bst-serialization          | Serialization        | Encode tree                             |
| 22    | bst-deserialization        | Deserialization      | Decode tree                             |
| 23    | bst-range-query            | Range Query          | Find keys in interval                   |
| 24    | bst-kth-smallest           | Kth Smallest         | Order statistic                         |
| 25    | bst-kth-largest            | Kth Largest          | Reverse order                           |
| 26    | bst-lowest-common-ancestor | LCA                  | Common ancestor                         |
| 27    | bst-validate               | Validate BST         | Check invariant                         |
| 28    | bst-merge                  | Merge Trees          | Combine BSTs                            |
| 29    | bst-split                  | Split Tree           | Partition by key                        |
| 30    | bst-rotate-left            | Rotate Left          | Tree rotation                           |
| 31    | bst-rotate-right           | Rotate Right         | Tree rotation                           |
| 32    | bst-join                   | Join Trees           | Combine trees                           |
| 33    | bst-copy                   | Copy Tree            | Deep copy                               |
| 34    | bst-clone                  | Clone Tree           | Duplicate                               |
| 35    | bst-iterator               | Iterator             | Inorder iterator                        |
| 36    | bst-threaded               | Threaded BST         | Pointer reuse                           |
| 37    | bst-augmented              | Augmented BST        | Extra metadata                          |
| 38    | bst-interval-tree          | Interval Tree        | Range overlap                           |
| 39    | bst-order-statistic        | Order Statistic Tree | Rank queries                            |
| 40    | bst-persistent             | Persistent BST       | Versioned                               |
| 41    | bst-concurrent             | Concurrent BST       | Multi-thread                            |
| 42    | bst-lock-free              | Lock Free BST        | Non-blocking                            |
| 43    | bst-cache-aware            | Cache Aware BST      | Memory layout                           |
| 44    | bst-memory-layout          | Memory Layout        | Node storage                            |
| 45    | bst-invariant-check        | Invariant Check      | Validate structure                      |


### 1.8 Basic tree traversals and operations (30)

| index | slug                 | name                   | description                |
| ----- | -------------------- | ---------------------- | -------------------------- |
| 1     | tree-traversal       | Tree Traversal         | General traversal patterns |
| 2     | dfs                  | Depth First Search     | Recursive traversal        |
| 3     | bfs                  | Breadth First Search   | Queue-based traversal      |
| 4     | preorder             | Preorder               | Visit root first           |
| 5     | inorder              | Inorder                | Visit sorted order         |
| 6     | postorder            | Postorder              | Visit root last            |
| 7     | level-order          | Level Order            | Layer traversal            |
| 8     | zigzag-traversal     | Zigzag Traversal       | Alternate levels           |
| 9     | vertical-order       | Vertical Order         | Column-based traversal     |
| 10    | boundary-traversal   | Boundary Traversal     | Outer nodes                |
| 11    | tree-height          | Height                 | Max depth                  |
| 12    | tree-size            | Size                   | Node count                 |
| 13    | tree-diameter        | Diameter               | Longest path               |
| 14    | tree-balance         | Balance                | Height condition           |
| 15    | tree-lca             | Lowest Common Ancestor | Shared ancestor            |
| 16    | tree-path-sum        | Path Sum               | Sum along path             |
| 17    | tree-flatten         | Flatten                | Convert to list            |
| 18    | tree-mirror          | Mirror                 | Reverse tree               |
| 19    | tree-symmetric       | Symmetric Check        | Mirror equality            |
| 20    | tree-serialize       | Serialize              | Encode                     |
| 21    | tree-deserialize     | Deserialize            | Decode                     |
| 22    | tree-prune           | Prune                  | Remove nodes               |
| 23    | tree-merge           | Merge                  | Combine trees              |
| 24    | tree-copy            | Copy                   | Duplicate                  |
| 25    | tree-iterator        | Iterator               | Traversal interface        |
| 26    | tree-recursive       | Recursive Pattern      | DFS pattern                |
| 27    | tree-iterative       | Iterative Pattern      | Stack-based                |
| 28    | tree-threaded        | Threaded Tree          | Pointer reuse              |
| 29    | tree-nary            | N-ary Tree             | Multiple children          |
| 30    | tree-invariant-check | Invariant Check        | Validate structure         |

### 2. Advanced data structures and operations (330)

This layer covers structures that add stronger invariants, faster queries, richer updates, or specialized ordering. The main pattern is augmentation: each structure stores extra information so that expensive work can be avoided later.

### 2.1 Balanced search trees (65)

| index | slug                      | name                      | description                                      |
| ----- | ------------------------- | ------------------------- | ------------------------------------------------ |
| 1     | balanced-search-tree      | Balanced Search Tree      | Ordered tree with height control                 |
| 2     | avl-tree                  | AVL Tree                  | Height-balanced binary search tree               |
| 3     | avl-insert                | AVL Insert                | Insert with rotations                            |
| 4     | avl-delete                | AVL Delete                | Delete with rebalancing                          |
| 5     | avl-rotation              | AVL Rotation              | Restore height balance                           |
| 6     | avl-balance-factor        | Balance Factor            | Track subtree height difference                  |
| 7     | red-black-tree            | Red Black Tree            | Color-balanced binary search tree                |
| 8     | red-black-insert          | Red Black Insert          | Insert with recoloring and rotations             |
| 9     | red-black-delete          | Red Black Delete          | Delete with fix-up cases                         |
| 10    | red-black-properties      | Red Black Properties      | Structural color invariants                      |
| 11    | aa-tree                   | AA Tree                   | Simplified red black tree using levels           |
| 12    | aa-tree-skew              | AA Tree Skew              | Remove left horizontal links                     |
| 13    | aa-tree-split             | AA Tree Split             | Remove consecutive right horizontal links        |
| 14    | treap                     | Treap                     | BST ordered by key and heap ordered by priority  |
| 15    | treap-insert              | Treap Insert              | Insert by key and rotate by priority             |
| 16    | treap-delete              | Treap Delete              | Remove by rotations or split merge               |
| 17    | treap-split               | Treap Split               | Divide by key                                    |
| 18    | treap-merge               | Treap Merge               | Join compatible treaps                           |
| 19    | randomized-bst            | Randomized BST            | Probabilistic balancing                          |
| 20    | splay-tree                | Splay Tree                | Self-adjusting search tree                       |
| 21    | splay-operation           | Splay Operation           | Move accessed node to root                       |
| 22    | zig-rotation              | Zig Rotation              | Single splay step                                |
| 23    | zig-zig-rotation          | Zig Zig Rotation          | Same-direction double step                       |
| 24    | zig-zag-rotation          | Zig Zag Rotation          | Opposite-direction double step                   |
| 25    | scapegoat-tree            | Scapegoat Tree            | Rebuild subtrees after imbalance                 |
| 26    | weight-balanced-tree      | Weight Balanced Tree      | Balance by subtree sizes                         |
| 27    | size-balanced-tree        | Size Balanced Tree        | Maintain balance from subtree counts             |
| 28    | b-tree                    | B Tree                    | Multiway balanced search tree                    |
| 29    | b-tree-search             | B Tree Search             | Search within pages and children                 |
| 30    | b-tree-insert             | B Tree Insert             | Insert with node splitting                       |
| 31    | b-tree-delete             | B Tree Delete             | Delete with borrowing or merging                 |
| 32    | b-tree-split              | B Tree Split              | Divide full node                                 |
| 33    | b-tree-merge              | B Tree Merge              | Combine underfull nodes                          |
| 34    | b-plus-tree               | B Plus Tree               | B tree variant with values in leaves             |
| 35    | b-plus-tree-leaf-chain    | Leaf Chain                | Sequential range scan through linked leaves      |
| 36    | b-star-tree               | B Star Tree               | B tree variant using redistribution before split |
| 37    | two-three-tree            | 2-3 Tree                  | Balanced tree with 2-nodes and 3-nodes           |
| 38    | two-three-four-tree       | 2-3-4 Tree                | Balanced tree equivalent to red black tree       |
| 39    | finger-tree               | Finger Tree               | Sequence tree with efficient end access          |
| 40    | tango-tree                | Tango Tree                | Competitive binary search tree                   |
| 41    | rope-tree                 | Rope Tree                 | Balanced tree for large strings                  |
| 42    | rope-split                | Rope Split                | Divide a rope at an index                        |
| 43    | rope-concat               | Rope Concat               | Join strings without full copy                   |
| 44    | implicit-treap            | Implicit Treap            | Sequence treap indexed by position               |
| 45    | implicit-treap-split      | Implicit Treap Split      | Split by rank                                    |
| 46    | implicit-treap-merge      | Implicit Treap Merge      | Join sequences                                   |
| 47    | order-maintenance-tree    | Order Maintenance Tree    | Maintain relative order under insertions         |
| 48    | join-based-tree           | Join Based Tree           | Define updates using join and split              |
| 49    | split-join-tree           | Split Join Tree           | Tree API based on decomposition                  |
| 50    | persistent-balanced-tree  | Persistent Balanced Tree  | Versioned balanced search tree                   |
| 51    | concurrent-balanced-tree  | Concurrent Balanced Tree  | Balanced tree with synchronization               |
| 52    | lock-free-balanced-tree   | Lock Free Balanced Tree   | Non-blocking balanced tree                       |
| 53    | cache-oblivious-b-tree    | Cache Oblivious B Tree    | Layout for unknown block sizes                   |
| 54    | packed-memory-array       | Packed Memory Array       | Ordered array with gaps                          |
| 55    | van-emde-boas-tree        | Van Emde Boas Tree        | Integer set with fast predecessor queries        |
| 56    | y-fast-trie               | Y Fast Trie               | Integer predecessor structure                    |
| 57    | x-fast-trie               | X Fast Trie               | Hash-based integer predecessor structure         |
| 58    | red-black-invariant-check | Red Black Invariant Check | Validate colors and black height                 |
| 59    | avl-invariant-check       | AVL Invariant Check       | Validate height balance                          |
| 60    | b-tree-invariant-check    | B Tree Invariant Check    | Validate occupancy and ordering                  |
| 61    | tree-rotation-analysis    | Rotation Analysis         | Count and reason about rotations                 |
| 62    | tree-height-bound         | Height Bound              | Prove logarithmic height                         |
| 63    | tree-amortized-analysis   | Amortized Analysis        | Analyze self-adjusting trees                     |
| 64    | tree-cache-layout         | Cache Layout              | Store nodes for locality                         |
| 65    | tree-benchmarking         | Tree Benchmarking         | Compare tree variants under workloads            |

### 2.2 Range query structures (70)

| index | slug                        | name                        | description                                    |
| ----- | --------------------------- | --------------------------- | ---------------------------------------------- |
| 1     | range-query                 | Range Query                 | Query over an interval of positions or keys    |
| 2     | static-range-query          | Static Range Query          | Range query without updates                    |
| 3     | dynamic-range-query         | Dynamic Range Query         | Range query with updates                       |
| 4     | range-sum-query             | Range Sum Query             | Sum values in an interval                      |
| 5     | range-minimum-query         | Range Minimum Query         | Minimum value in an interval                   |
| 6     | range-maximum-query         | Range Maximum Query         | Maximum value in an interval                   |
| 7     | range-count-query           | Range Count Query           | Count elements in an interval                  |
| 8     | range-frequency-query       | Range Frequency Query       | Count occurrences of a value in a range        |
| 9     | range-mode-query            | Range Mode Query            | Most frequent value in a range                 |
| 10    | range-median-query          | Range Median Query          | Median value in a range                        |
| 11    | range-majority-query        | Range Majority Query        | Majority value in a range                      |
| 12    | prefix-sum-query            | Prefix Sum Query            | Answer sums using cumulative values            |
| 13    | prefix-xor-query            | Prefix XOR Query            | Answer xor ranges from prefix xor              |
| 14    | prefix-min-query            | Prefix Min Query            | Prefix-based minimum query                     |
| 15    | difference-query            | Difference Query            | Range update through difference representation |
| 16    | sparse-table                | Sparse Table                | Static idempotent range query table            |
| 17    | sparse-table-build          | Sparse Table Build          | Precompute overlapping power-of-two ranges     |
| 18    | sparse-table-query          | Sparse Table Query          | Answer RMQ in O(1) after preprocessing         |
| 19    | disjoint-sparse-table       | Disjoint Sparse Table       | Static associative range queries               |
| 20    | sqrt-decomposition          | Square Root Decomposition   | Split data into blocks                         |
| 21    | sqrt-range-sum              | Square Root Range Sum       | Range sum with block summaries                 |
| 22    | sqrt-range-min              | Square Root Range Min       | Range minimum with block summaries             |
| 23    | sqrt-range-update           | Square Root Range Update    | Blocked range updates                          |
| 24    | sqrt-lazy-blocks            | Lazy Blocks                 | Delay work within blocks                       |
| 25    | mo-algorithm                | Mo Algorithm                | Offline range queries ordered by block         |
| 26    | mo-with-updates             | Mo With Updates             | Offline range queries with point updates       |
| 27    | hilbert-order-mo            | Hilbert Order Mo            | Cache-friendly ordering for offline queries    |
| 28    | wavelet-tree                | Wavelet Tree                | Range rank, select, and quantile queries       |
| 29    | wavelet-matrix              | Wavelet Matrix              | Compact wavelet variant                        |
| 30    | range-rank-query            | Range Rank Query            | Count values below or equal to a key           |
| 31    | range-select-query          | Range Select Query          | Find kth occurrence in a range                 |
| 32    | range-quantile-query        | Range Quantile Query        | Find kth smallest value in a range             |
| 33    | merge-sort-tree             | Merge Sort Tree             | Segment tree with sorted lists                 |
| 34    | fractional-cascading        | Fractional Cascading        | Speed up related binary searches               |
| 35    | persistent-range-query      | Persistent Range Query      | Query old versions of data                     |
| 36    | persistent-segment-query    | Persistent Segment Query    | Versioned segment tree queries                 |
| 37    | range-tree                  | Range Tree                  | Orthogonal range searching structure           |
| 38    | two-dimensional-range-tree  | 2D Range Tree               | Range search over points in the plane          |
| 39    | kd-tree-range-query         | KD Tree Range Query         | Spatial range search in kd tree                |
| 40    | interval-tree-query         | Interval Tree Query         | Find intervals overlapping a query             |
| 41    | stabbing-query              | Stabbing Query              | Find intervals containing a point              |
| 42    | fenwick-range-query         | Fenwick Range Query         | Prefix-based dynamic range query               |
| 43    | segment-tree-range-query    | Segment Tree Range Query    | General dynamic interval query                 |
| 44    | lazy-range-query            | Lazy Range Query            | Delay range updates until needed               |
| 45    | range-add-query             | Range Add Query             | Add to all elements in an interval             |
| 46    | range-assign-query          | Range Assign Query          | Assign all values in an interval               |
| 47    | range-chmin-query           | Range Chmin Query           | Clamp range values downward                    |
| 48    | range-chmax-query           | Range Chmax Query           | Clamp range values upward                      |
| 49    | range-affine-query          | Range Affine Query          | Apply affine transform over a range            |
| 50    | range-gcd-query             | Range GCD Query             | Greatest common divisor over interval          |
| 51    | range-lcm-query             | Range LCM Query             | Least common multiple over interval            |
| 52    | range-bitwise-and-query     | Range Bitwise AND Query     | Bitwise and over interval                      |
| 53    | range-bitwise-or-query      | Range Bitwise OR Query      | Bitwise or over interval                       |
| 54    | range-bitwise-xor-query     | Range Bitwise XOR Query     | Bitwise xor over interval                      |
| 55    | range-convolution-query     | Range Convolution Query     | Query using convolution-like summaries         |
| 56    | range-hash-query            | Range Hash Query            | Hash substrings or subarrays                   |
| 57    | range-distinct-query        | Range Distinct Query        | Count distinct values in a range               |
| 58    | range-inversion-query       | Range Inversion Query       | Count inversions in a subarray                 |
| 59    | range-next-greater-query    | Range Next Greater Query    | Precomputed nearest-greater relations          |
| 60    | range-nearest-smaller-query | Range Nearest Smaller Query | Precomputed nearest-smaller relations          |
| 61    | cartesian-tree-rmq          | Cartesian Tree RMQ          | Reduce RMQ to LCA                              |
| 62    | euler-tour-rmq              | Euler Tour RMQ              | Use RMQ over tree traversal depths             |
| 63    | lca-range-query             | LCA Range Query             | Lowest common ancestor through RMQ             |
| 64    | block-decomposition-rmq     | Block Decomposition RMQ     | RMQ with micro and macro blocks                |
| 65    | plus-minus-one-rmq          | Plus Minus One RMQ          | Specialized RMQ for depth arrays               |
| 66    | offline-range-query         | Offline Range Query         | Reorder queries to improve complexity          |
| 67    | online-range-query          | Online Range Query          | Answer queries as they arrive                  |
| 68    | range-query-compression     | Coordinate Compression      | Reduce large keys to compact indices           |
| 69    | range-query-invariant-check | Range Query Invariant Check | Validate stored summaries                      |
| 70    | range-query-benchmarking    | Range Query Benchmarking    | Compare structures by workload                 |

### 2.3 Fenwick tree variants (25)

| index | slug                             | name                     | description                                |
| ----- | -------------------------------- | ------------------------ | ------------------------------------------ |
| 1     | fenwick-tree                     | Fenwick Tree             | Binary indexed tree for prefix aggregates  |
| 2     | fenwick-build                    | Fenwick Build            | Construct from array in O(n)               |
| 3     | fenwick-point-update             | Point Update             | Add value at a position                    |
| 4     | fenwick-prefix-query             | Prefix Query             | Query prefix aggregate                     |
| 5     | fenwick-range-query              | Range Query              | Compute range via prefix differences       |
| 6     | fenwick-range-update-point-query | Range Update Point Query | Apply updates over intervals, query points |
| 7     | fenwick-point-update-range-query | Point Update Range Query | Standard BIT mode                          |
| 8     | fenwick-range-update-range-query | Range Update Range Query | Two-tree technique for full support        |
| 9     | fenwick-min-tree                 | Fenwick Min Tree         | Prefix minimum queries                     |
| 10    | fenwick-max-tree                 | Fenwick Max Tree         | Prefix maximum queries                     |
| 11    | fenwick-xor-tree                 | Fenwick XOR Tree         | Prefix xor queries                         |
| 12    | fenwick-gcd-tree                 | Fenwick GCD Tree         | Prefix gcd queries                         |
| 13    | fenwick-2d                       | 2D Fenwick Tree          | Grid-based prefix queries                  |
| 14    | fenwick-3d                       | 3D Fenwick Tree          | Higher dimensional extension               |
| 15    | fenwick-compressed               | Compressed Fenwick Tree  | Coordinate compressed indices              |
| 16    | fenwick-order-statistic          | Fenwick Order Statistic  | Find k-th element via prefix sums          |
| 17    | fenwick-inversion-count          | Fenwick Inversion Count  | Count inversions in O(n log n)             |
| 18    | fenwick-frequency-table          | Frequency Table          | Maintain counts dynamically                |
| 19    | fenwick-weighted-sum             | Weighted Sum             | Prefix weighted aggregation                |
| 20    | fenwick-lower-bound              | Fenwick Lower Bound      | Find smallest index with prefix ≥ target   |
| 21    | fenwick-binary-lifting           | Binary Lifting on BIT    | Jump through implicit tree                 |
| 22    | fenwick-persistent               | Persistent Fenwick Tree  | Versioned BIT                              |
| 23    | fenwick-concurrent               | Concurrent Fenwick Tree  | Thread-safe BIT                            |
| 24    | fenwick-memory-layout            | Memory Layout            | Bitwise index manipulation                 |
| 25    | fenwick-invariant-check          | Fenwick Invariant Check  | Validate structure and sums                |

### 2.4 Segment tree variants (60)

| index | slug                             | name                     | description                          |
| ----- | -------------------------------- | ------------------------ | ------------------------------------ |
| 1     | segment-tree                     | Segment Tree             | Binary tree for interval aggregation |
| 2     | segment-tree-build               | Segment Tree Build       | Construct from array                 |
| 3     | segment-tree-query               | Segment Tree Query       | Query over interval                  |
| 4     | segment-tree-update              | Segment Tree Update      | Point update                         |
| 5     | segment-tree-range-update        | Range Update             | Update interval                      |
| 6     | segment-tree-lazy                | Lazy Propagation         | Defer updates                        |
| 7     | segment-tree-range-sum           | Range Sum                | Sum queries                          |
| 8     | segment-tree-range-min           | Range Min                | Minimum queries                      |
| 9     | segment-tree-range-max           | Range Max                | Maximum queries                      |
| 10    | segment-tree-range-gcd           | Range GCD                | GCD queries                          |
| 11    | segment-tree-range-lcm           | Range LCM                | LCM queries                          |
| 12    | segment-tree-xor                 | Range XOR                | XOR aggregation                      |
| 13    | segment-tree-affine              | Affine Updates           | Linear transform updates             |
| 14    | segment-tree-beats               | Segment Tree Beats       | Advanced lazy propagation            |
| 15    | segment-tree-chmin               | Range Chmin              | Clamp values                         |
| 16    | segment-tree-chmax               | Range Chmax              | Clamp upward                         |
| 17    | segment-tree-assign              | Range Assign             | Set interval values                  |
| 18    | segment-tree-add                 | Range Add                | Add to interval                      |
| 19    | segment-tree-multiply            | Range Multiply           | Multiply interval                    |
| 20    | segment-tree-sum-of-squares      | Sum of Squares           | Maintain squared values              |
| 21    | segment-tree-frequency           | Frequency Tree           | Count values                         |
| 22    | segment-tree-merge-sort          | Merge Sort Tree          | Node stores sorted list              |
| 23    | segment-tree-order-statistic     | Order Statistic Tree     | Kth element queries                  |
| 24    | segment-tree-persistent          | Persistent Segment Tree  | Versioned queries                    |
| 25    | segment-tree-dynamic             | Dynamic Segment Tree     | Sparse coordinates                   |
| 26    | segment-tree-implicit            | Implicit Segment Tree    | Allocate nodes on demand             |
| 27    | segment-tree-2d                  | 2D Segment Tree          | Grid-based                           |
| 28    | segment-tree-3d                  | 3D Segment Tree          | Higher dimensions                    |
| 29    | segment-tree-hash                | Hash Tree                | Store rolling hashes                 |
| 30    | segment-tree-string              | String Segment Tree      | Substring queries                    |
| 31    | segment-tree-range-mode          | Range Mode               | Most frequent element                |
| 32    | segment-tree-range-majority      | Range Majority           | Majority element                     |
| 33    | segment-tree-interval            | Interval Segment Tree    | Overlapping intervals                |
| 34    | segment-tree-kd                  | KD Segment Tree          | Spatial partition                    |
| 35    | segment-tree-hybrid              | Hybrid Tree              | Combine techniques                   |
| 36    | segment-tree-cache-aware         | Cache Aware Tree         | Layout optimization                  |
| 37    | segment-tree-iterative           | Iterative Segment Tree   | Array-based non-recursive            |
| 38    | segment-tree-bottom-up           | Bottom Up Tree           | Iterative build                      |
| 39    | segment-tree-top-down            | Top Down Tree            | Recursive                            |
| 40    | segment-tree-sparse-table-hybrid | Hybrid with Sparse Table | Static optimization                  |
| 41    | segment-tree-fenwick-hybrid      | Fenwick Hybrid           | Combine BIT and segment tree         |
| 42    | segment-tree-wavelet-hybrid      | Wavelet Hybrid           | Combine structures                   |
| 43    | segment-tree-sqrt-hybrid         | Sqrt Hybrid              | Combine block decomposition          |
| 44    | segment-tree-parallel            | Parallel Segment Tree    | Multi-threaded                       |
| 45    | segment-tree-lock-free           | Lock Free Segment Tree   | Non-blocking                         |
| 46    | segment-tree-batched             | Batched Updates          | Bulk operations                      |
| 47    | segment-tree-pipeline            | Pipeline Updates         | Streaming                            |
| 48    | segment-tree-memory-layout       | Memory Layout            | Node storage                         |
| 49    | segment-tree-node-pooling        | Node Pooling             | Memory reuse                         |
| 50    | segment-tree-compression         | Coordinate Compression   | Reduce domain                        |
| 51    | segment-tree-inversion           | Inversion Count          | Count inversions                     |
| 52    | segment-tree-dp                  | DP Optimization          | Use in dynamic programming           |
| 53    | segment-tree-lca                 | LCA Segment Tree         | Tree queries                         |
| 54    | segment-tree-rmq                 | RMQ Segment Tree         | Minimum query                        |
| 55    | segment-tree-range-query-check   | Invariant Check          | Validate correctness                 |
| 56    | segment-tree-benchmarking        | Benchmarking             | Compare variants                     |
| 57    | segment-tree-debugging           | Debugging                | Trace issues                         |
| 58    | segment-tree-visualization       | Visualization            | Tree inspection                      |
| 59    | segment-tree-proof               | Correctness Proof        | Formal guarantees                    |
| 60    | segment-tree-complexity          | Complexity Analysis      | Time and space bounds                |

### 2.5 Disjoint set union variants (35)

| index | slug                       | name                  | description                    |
| ----- | -------------------------- | --------------------- | ------------------------------ |
| 1     | disjoint-set-union         | Disjoint Set Union    | Maintain partition of elements |
| 2     | union-find                 | Union Find            | Equivalent DSU interface       |
| 3     | dsu-make-set               | Make Set              | Initialize singleton           |
| 4     | dsu-find                   | Find                  | Locate representative          |
| 5     | dsu-union                  | Union                 | Merge two sets                 |
| 6     | path-compression           | Path Compression      | Flatten tree during find       |
| 7     | union-by-rank              | Union by Rank         | Attach smaller tree            |
| 8     | union-by-size              | Union by Size         | Attach smaller set             |
| 9     | dsu-rollback               | Rollback DSU          | Undo operations                |
| 10    | dsu-persistent             | Persistent DSU        | Versioned structure            |
| 11    | dsu-parity                 | Parity DSU            | Track bipartite relations      |
| 12    | dsu-weighted               | Weighted DSU          | Maintain differences           |
| 13    | dsu-bipartite-check        | Bipartite Check       | Detect odd cycles              |
| 14    | dsu-component-size         | Component Size        | Track sizes                    |
| 15    | dsu-component-sum          | Component Sum         | Aggregate values               |
| 16    | dsu-on-tree                | DSU on Tree           | Small to large merging         |
| 17    | dsu-offline-query          | Offline Query DSU     | Process queries offline        |
| 18    | dsu-dynamic-connectivity   | Dynamic Connectivity  | Maintain connectivity          |
| 19    | dsu-with-time              | DSU with Time         | Track versions over time       |
| 20    | dsu-edge-removal           | Edge Removal          | Handle deletions offline       |
| 21    | dsu-grid                   | Grid DSU              | 2D connectivity                |
| 22    | dsu-3d                     | 3D DSU                | Higher dimension               |
| 23    | dsu-hash-map               | Map-based DSU         | Sparse keys                    |
| 24    | dsu-linked                 | Linked DSU            | Explicit pointers              |
| 25    | dsu-concurrent             | Concurrent DSU        | Multi-thread safe              |
| 26    | dsu-lock-free              | Lock Free DSU         | Non-blocking                   |
| 27    | dsu-memory-layout          | Memory Layout         | Array structure                |
| 28    | dsu-invariant-check        | Invariant Check       | Validate parents               |
| 29    | dsu-benchmarking           | Benchmarking          | Measure performance            |
| 30    | dsu-debugging              | Debugging             | Trace unions                   |
| 31    | dsu-randomized             | Randomized DSU        | Random union heuristic         |
| 32    | dsu-compressed-path-length | Path Length Analysis  | Measure compression            |
| 33    | dsu-forest-representation  | Forest Representation | Tree structure                 |
| 34    | dsu-graph-application      | Graph Application     | Connectivity problems          |
| 35    | dsu-kruskal                | Kruskal Integration   | MST usage                      |

### 2.6 Tries and prefix structures (45)

| index | slug                        | name                        | description                              |
| ----- | --------------------------- | --------------------------- | ---------------------------------------- |
| 1     | trie                        | Trie                        | Prefix tree for strings or sequences     |
| 2     | trie-insert                 | Trie Insert                 | Add a key character by character         |
| 3     | trie-search                 | Trie Search                 | Lookup an exact key                      |
| 4     | trie-prefix-search          | Prefix Search               | Find keys sharing a prefix               |
| 5     | trie-delete                 | Trie Delete                 | Remove a key and prune unused nodes      |
| 6     | compressed-trie             | Compressed Trie             | Merge single-child paths                 |
| 7     | radix-tree                  | Radix Tree                  | Compact trie over string fragments       |
| 8     | patricia-trie               | Patricia Trie               | Path-compressed binary trie              |
| 9     | crit-bit-tree               | Crit Bit Tree               | Binary trie branching on critical bit    |
| 10    | ternary-search-tree         | Ternary Search Tree         | Trie-like tree with three-way branching  |
| 11    | binary-trie                 | Binary Trie                 | Trie over bit strings                    |
| 12    | xor-trie                    | XOR Trie                    | Binary trie for maximum xor queries      |
| 13    | suffix-trie                 | Suffix Trie                 | Trie containing all suffixes of a string |
| 14    | suffix-tree                 | Suffix Tree                 | Compressed suffix trie                   |
| 15    | suffix-array                | Suffix Array                | Sorted array of suffix positions         |
| 16    | lcp-array                   | LCP Array                   | Longest common prefix between suffixes   |
| 17    | prefix-function             | Prefix Function             | KMP prefix table                         |
| 18    | z-array                     | Z Array                     | Longest prefix match at each position    |
| 19    | aho-corasick-trie           | Aho Corasick Trie           | Multi-pattern matching automaton         |
| 20    | dawg                        | Directed Acyclic Word Graph | Minimal graph for a dictionary           |
| 21    | minimal-dfa                 | Minimal DFA                 | Compact deterministic automaton          |
| 22    | double-array-trie           | Double Array Trie           | Dense array-based trie representation    |
| 23    | succinct-trie               | Succinct Trie               | Bit-compressed trie layout               |
| 24    | burst-trie                  | Burst Trie                  | Cache-conscious string dictionary        |
| 25    | hat-trie                    | HAT Trie                    | Hybrid array hash trie for strings       |
| 26    | hash-array-mapped-trie      | Hash Array Mapped Trie      | Hash trie with bitmap-indexed nodes      |
| 27    | persistent-trie             | Persistent Trie             | Versioned prefix tree                    |
| 28    | immutable-trie              | Immutable Trie              | Functional trie with structural sharing  |
| 29    | concurrent-trie             | Concurrent Trie             | Thread-safe prefix tree                  |
| 30    | lock-free-trie              | Lock Free Trie              | Non-blocking trie design                 |
| 31    | trie-autocomplete           | Autocomplete Trie           | Prefix completion queries                |
| 32    | trie-wildcard-search        | Wildcard Search             | Match keys with wildcard positions       |
| 33    | trie-fuzzy-search           | Fuzzy Search                | Approximate matching over prefixes       |
| 34    | trie-lexicographic-iterator | Lexicographic Iterator      | Visit keys in sorted order               |
| 35    | trie-count-prefix           | Prefix Count                | Count words under a prefix               |
| 36    | trie-frequency              | Frequency Trie              | Store counts at nodes                    |
| 37    | trie-top-k                  | Top K Trie                  | Return most frequent completions         |
| 38    | trie-memory-pool            | Memory Pool                 | Reuse trie nodes efficiently             |
| 39    | trie-array-children         | Array Children              | Fixed child array representation         |
| 40    | trie-map-children           | Map Children                | Sparse child map representation          |
| 41    | trie-bitset-children        | Bitset Children             | Compact child existence mask             |
| 42    | trie-serialization          | Serialization               | Save and load trie structure             |
| 43    | trie-compression            | Trie Compression            | Reduce memory footprint                  |
| 44    | trie-invariant-check        | Trie Invariant Check        | Validate prefix structure                |
| 45    | trie-benchmarking           | Trie Benchmarking           | Compare lookup and memory cost           |

### 2.7 Order statistic structures (30)

| index | slug                            | name                            | description                                |
| ----- | ------------------------------- | ------------------------------- | ------------------------------------------ |
| 1     | order-statistic-tree            | Order Statistic Tree            | Balanced tree augmented with subtree sizes |
| 2     | select-kth                      | Select Kth                      | Find element by rank                       |
| 3     | rank-query                      | Rank Query                      | Count elements smaller than a key          |
| 4     | order-statistic-insert          | Order Statistic Insert          | Insert while maintaining subtree sizes     |
| 5     | order-statistic-delete          | Order Statistic Delete          | Delete while updating ranks                |
| 6     | order-statistic-rotation        | Order Statistic Rotation        | Preserve size metadata during rotations    |
| 7     | indexed-sequence-tree           | Indexed Sequence Tree           | Sequence represented by rank-balanced tree |
| 8     | implicit-treap-order-statistic  | Implicit Treap Order Statistic  | Rank queries over implicit treap positions |
| 9     | wavelet-tree-order-statistic    | Wavelet Tree Order Statistic    | Kth and rank queries in ranges             |
| 10    | fenwick-order-statistic         | Fenwick Order Statistic         | Find kth by prefix counts                  |
| 11    | segment-tree-order-statistic    | Segment Tree Order Statistic    | Select kth using frequency tree            |
| 12    | bitset-rank-select              | Bitset Rank Select              | Rank and select over packed bits           |
| 13    | succinct-rank-select            | Succinct Rank Select            | Space-efficient rank and select support    |
| 14    | dynamic-rank-select             | Dynamic Rank Select             | Rank and select with updates               |
| 15    | range-kth-query                 | Range Kth Query                 | Kth smallest in subarray                   |
| 16    | range-rank-query                | Range Rank Query                | Rank of key inside interval                |
| 17    | quantile-query                  | Quantile Query                  | General percentile or kth statistic        |
| 18    | median-maintenance              | Median Maintenance              | Maintain online median                     |
| 19    | two-heap-median                 | Two Heap Median                 | Median by lower and upper heaps            |
| 20    | indexed-skip-list               | Indexed Skip List               | Skip list with span counts                 |
| 21    | skip-list-rank                  | Skip List Rank                  | Rank query using spans                     |
| 22    | sorted-vector-rank              | Sorted Vector Rank              | Rank by binary search                      |
| 23    | gapped-array-order              | Gapped Array Order              | Maintain order with gaps                   |
| 24    | order-maintenance               | Order Maintenance               | Test relative order under insertions       |
| 25    | packed-memory-order             | Packed Memory Order             | Ordered sequence in packed memory array    |
| 26    | top-k-structure                 | Top K Structure                 | Maintain best k elements                   |
| 27    | bottom-k-structure              | Bottom K Structure              | Maintain smallest k elements               |
| 28    | percentile-sketch               | Percentile Sketch               | Approximate order statistics               |
| 29    | order-statistic-invariant-check | Order Statistic Invariant Check | Validate size and rank metadata            |
| 30    | order-statistic-benchmarking    | Order Statistic Benchmarking    | Compare rank and select workloads          |

### 3. Specialized, persistent, concurrent, and external structures (250)

This layer focuses on memory models, versioning, compression, concurrency, and large-scale data handling. The emphasis shifts from pure asymptotic complexity to system constraints: memory footprint, cache behavior, parallelism, and I/O.

### 3.1 Persistent data structures (45)

| index | slug                           | name                       | description                              |
| ----- | ------------------------------ | -------------------------- | ---------------------------------------- |
| 1     | persistent-data-structure      | Persistent Data Structure  | Preserve previous versions after updates |
| 2     | partial-persistence            | Partial Persistence        | Access all versions, update latest       |
| 3     | full-persistence               | Full Persistence           | Update any version                       |
| 4     | confluent-persistence          | Confluent Persistence      | Merge different versions                 |
| 5     | path-copying                   | Path Copying               | Copy nodes along update path             |
| 6     | fat-node                       | Fat Node                   | Store multiple versions in one node      |
| 7     | persistent-array               | Persistent Array           | Versioned array                          |
| 8     | persistent-segment-tree        | Persistent Segment Tree    | Versioned interval queries               |
| 9     | persistent-fenwick             | Persistent Fenwick Tree    | Versioned prefix queries                 |
| 10    | persistent-bst                 | Persistent BST             | Versioned search tree                    |
| 11    | persistent-treap               | Persistent Treap           | Randomized versioned tree                |
| 12    | persistent-heap                | Persistent Heap            | Versioned priority queue                 |
| 13    | persistent-union-find          | Persistent Union Find      | Versioned DSU                            |
| 14    | persistent-stack               | Persistent Stack           | Functional stack                         |
| 15    | persistent-queue               | Persistent Queue           | Functional queue                         |
| 16    | persistent-deque               | Persistent Deque           | Double-ended versioned queue             |
| 17    | persistent-hash-map            | Persistent Hash Map        | Immutable map with sharing               |
| 18    | persistent-trie                | Persistent Trie            | Versioned prefix tree                    |
| 19    | persistent-rope                | Persistent Rope            | Versioned string                         |
| 20    | persistent-graph               | Persistent Graph           | Versioned graph structure                |
| 21    | version-tree                   | Version Tree               | Track lineage of versions                |
| 22    | snapshot-system                | Snapshot System            | Capture system states                    |
| 23    | undo-redo-structure            | Undo Redo Structure        | Track reversible operations              |
| 24    | structural-sharing             | Structural Sharing         | Reuse unchanged parts                    |
| 25    | copy-on-write                  | Copy On Write              | Delay copying until mutation             |
| 26    | immutable-structure            | Immutable Structure        | No in-place mutation                     |
| 27    | persistent-memory-layout       | Memory Layout              | Node allocation strategies               |
| 28    | persistent-garbage-collection  | Garbage Collection         | Reclaim unused versions                  |
| 29    | persistent-reference-counting  | Reference Counting         | Track shared nodes                       |
| 30    | persistent-diff                | Persistent Diff            | Store changes between versions           |
| 31    | persistent-log-structure       | Log Structured Persistence | Append-only updates                      |
| 32    | persistent-indexing            | Persistent Index           | Index across versions                    |
| 33    | persistent-cache               | Persistent Cache           | Cache across versions                    |
| 34    | persistent-concurrent          | Concurrent Persistence     | Thread-safe versioning                   |
| 35    | persistent-lock-free           | Lock Free Persistence      | Non-blocking versioned structures        |
| 36    | persistent-consistency         | Consistency Model          | Version correctness                      |
| 37    | persistent-rollback            | Rollback                   | Revert to previous version               |
| 38    | persistent-branching           | Branching                  | Fork versions                            |
| 39    | persistent-merge               | Merge Versions             | Combine histories                        |
| 40    | persistent-invariant-check     | Invariant Check            | Validate version correctness             |
| 41    | persistent-benchmarking        | Benchmarking               | Measure overhead                         |
| 42    | persistent-debugging           | Debugging                  | Trace version issues                     |
| 43    | persistent-snapshot-delta      | Snapshot Delta             | Store differences                        |
| 44    | persistent-storage-integration | Storage Integration        | Disk-backed persistence                  |
| 45    | persistent-distributed         | Distributed Persistence    | Versioning across nodes                  |

### 3.2 Functional data structures (35)

| index | slug                           | name                      | description                              |
| ----- | ------------------------------ | ------------------------- | ---------------------------------------- |
| 1     | functional-data-structure      | Functional Data Structure | Immutable structure with pure operations |
| 2     | persistent-list                | Persistent List           | Linked list with sharing                 |
| 3     | functional-stack               | Functional Stack          | Immutable stack                          |
| 4     | functional-queue               | Functional Queue          | Two-list queue                           |
| 5     | banker's-queue                 | Bankers Queue             | Amortized functional queue               |
| 6     | real-time-queue                | Real Time Queue           | Worst-case O(1) queue                    |
| 7     | functional-deque               | Functional Deque          | Double-ended immutable queue             |
| 8     | finger-tree-functional         | Finger Tree               | General-purpose sequence                 |
| 9     | functional-heap                | Functional Heap           | Immutable priority queue                 |
| 10    | binomial-heap-functional       | Functional Binomial Heap  | Persistent mergeable heap                |
| 11    | pairing-heap-functional        | Functional Pairing Heap   | Lazy heap                                |
| 12    | skew-binomial-heap             | Skew Binomial Heap        | Improved insertion                       |
| 13    | functional-set                 | Functional Set            | Immutable set                            |
| 14    | functional-map                 | Functional Map            | Immutable key-value store                |
| 15    | hamt                           | Hash Array Mapped Trie    | Functional hash map                      |
| 16    | functional-trie                | Functional Trie           | Immutable prefix tree                    |
| 17    | functional-bst                 | Functional BST            | Immutable search tree                    |
| 18    | red-black-functional           | Functional Red Black Tree | Balanced immutable tree                  |
| 19    | functional-sequence            | Functional Sequence       | Abstract sequence                        |
| 20    | lazy-evaluation-structure      | Lazy Structure            | Deferred computation                     |
| 21    | stream-structure               | Stream                    | Infinite sequence                        |
| 22    | amortized-functional-analysis  | Amortized Analysis        | Cost over operations                     |
| 23    | worst-case-functional-analysis | Worst Case Analysis       | Strict bounds                            |
| 24    | structural-sharing-functional  | Structural Sharing        | Reuse nodes                              |
| 25    | persistent-functional          | Persistent Functional     | Versioning                               |
| 26    | functional-memory-layout       | Memory Layout             | Allocation patterns                      |
| 27    | functional-garbage-collection  | Garbage Collection        | Reclaim unused                           |
| 28    | functional-concurrency         | Concurrency               | Safe sharing                             |
| 29    | functional-lock-free           | Lock Free                 | Non-blocking                             |
| 30    | functional-invariant-check     | Invariant Check           | Validate immutability                    |
| 31    | functional-benchmarking        | Benchmarking              | Measure performance                      |
| 32    | functional-debugging           | Debugging                 | Trace errors                             |
| 33    | functional-fusion              | Fusion                    | Combine operations                       |
| 34    | functional-deforestation       | Deforestation             | Remove intermediate structures           |
| 35    | functional-composability       | Composability             | Combine operations cleanly               |

### 3.3 Succinct and compressed structures (45)

| index | slug                              | name                     | description                       |
| ----- | --------------------------------- | ------------------------ | --------------------------------- |
| 1     | succinct-data-structure           | Succinct Structure       | Near information-theoretic space  |
| 2     | bit-vector                        | Bit Vector               | Compact bit storage               |
| 3     | rank-select                       | Rank Select              | Count and locate bits             |
| 4     | succinct-rank                     | Succinct Rank            | Efficient rank queries            |
| 5     | succinct-select                   | Succinct Select          | Efficient select queries          |
| 6     | wavelet-tree-succinct             | Succinct Wavelet Tree    | Compressed range queries          |
| 7     | wavelet-matrix-succinct           | Succinct Wavelet Matrix  | Compact variant                   |
| 8     | compressed-trie-succinct          | Succinct Trie            | Bit-packed prefix tree            |
| 9     | compressed-suffix-array           | Compressed Suffix Array  | Reduced memory suffix array       |
| 10    | fm-index                          | FM Index                 | Compressed full-text index        |
| 11    | burrows-wheeler-transform         | BWT                      | Transform for compression         |
| 12    | run-length-encoding               | RLE                      | Compress repeated values          |
| 13    | delta-encoding                    | Delta Encoding           | Store differences                 |
| 14    | gamma-coding                      | Gamma Coding             | Variable-length integer coding    |
| 15    | elias-delta-coding                | Elias Delta Coding       | Efficient integer encoding        |
| 16    | huffman-coding                    | Huffman Coding           | Optimal prefix codes              |
| 17    | arithmetic-coding                 | Arithmetic Coding        | Fractional encoding               |
| 18    | succinct-tree                     | Succinct Tree            | Encode tree topology              |
| 19    | balanced-parentheses              | Balanced Parentheses     | Tree encoding                     |
| 20    | louds                             | LOUDS                    | Level-order unary degree sequence |
| 21    | compressed-graph                  | Compressed Graph         | Compact adjacency                 |
| 22    | adjacency-bitset                  | Adjacency Bitset         | Bit-based graph                   |
| 23    | sparse-bitset                     | Sparse Bitset            | Efficient sparse representation   |
| 24    | roaring-bitmap                    | Roaring Bitmap           | Hybrid compressed bitmap          |
| 25    | succinct-hash                     | Succinct Hash            | Compact hash table                |
| 26    | minimal-perfect-hash-succinct     | Succinct MPH             | Compact mapping                   |
| 27    | compressed-array                  | Compressed Array         | Store values efficiently          |
| 28    | dictionary-encoding               | Dictionary Encoding      | Map values to ids                 |
| 29    | columnar-compression              | Columnar Compression     | Compress columns independently    |
| 30    | vector-compression                | Vector Compression       | SIMD-friendly compression         |
| 31    | cache-compressed-layout           | Cache Layout             | Fit into cache lines              |
| 32    | succinct-index                    | Succinct Index           | Compressed indexing               |
| 33    | compressed-range-query            | Compressed Range Query   | Query on compressed data          |
| 34    | compressed-structure-update       | Update                   | Maintain compressed data          |
| 35    | succinct-memory-layout            | Memory Layout            | Bit-level organization            |
| 36    | succinct-concurrency              | Concurrency              | Thread-safe compressed structures |
| 37    | succinct-lock-free                | Lock Free                | Non-blocking                      |
| 38    | succinct-invariant-check          | Invariant Check          | Validate encoding                 |
| 39    | succinct-benchmarking             | Benchmarking             | Measure space/time                |
| 40    | succinct-debugging                | Debugging                | Inspect compressed state          |
| 41    | compressed-io                     | Compressed IO            | Efficient disk read/write         |
| 42    | compressed-database               | Compressed DB Structures | Storage engine integration        |
| 43    | succinct-graph-traversal          | Graph Traversal          | Operate on compressed graph       |
| 44    | succinct-tree-navigation          | Tree Navigation          | Navigate encoded trees            |
| 45    | succinct-rank-select-optimization | Optimization             | Faster bit operations             |

### 3.4 Geometric data structures (40)

| index | slug                                 | name                         | description                                          |
| ----- | ------------------------------------ | ---------------------------- | ---------------------------------------------------- |
| 1     | geometric-data-structure             | Geometric Data Structure     | Store and query points, ranges, and shapes           |
| 2     | point-set                            | Point Set                    | Collection of points in coordinate space             |
| 3     | line-segment-set                     | Line Segment Set             | Store and query line segments                        |
| 4     | interval-tree-geometric              | Interval Tree                | Query overlapping one-dimensional intervals          |
| 5     | segment-tree-geometric               | Geometric Segment Tree       | Store intervals and support stabbing queries         |
| 6     | range-tree-geometric                 | Range Tree                   | Orthogonal range search                              |
| 7     | two-dimensional-range-tree-geometric | 2D Range Tree                | Range search over planar points                      |
| 8     | kd-tree                              | KD Tree                      | Recursive spatial partition by axis                  |
| 9     | kd-tree-nearest-neighbor             | KD Tree Nearest Neighbor     | Find closest point using pruning                     |
| 10    | ball-tree                            | Ball Tree                    | Partition space using hyperspheres                   |
| 11    | vp-tree                              | Vantage Point Tree           | Metric tree using distances to pivots                |
| 12    | cover-tree                           | Cover Tree                   | Metric tree for nearest-neighbor search              |
| 13    | quadtree                             | Quadtree                     | Recursive partition of 2D space                      |
| 14    | octree                               | Octree                       | Recursive partition of 3D space                      |
| 15    | r-tree                               | R Tree                       | Bounding-box tree for rectangles and spatial objects |
| 16    | r-star-tree                          | R Star Tree                  | R tree variant with improved split heuristics        |
| 17    | hilbert-r-tree                       | Hilbert R Tree               | R tree ordered by Hilbert curve                      |
| 18    | bounding-volume-hierarchy            | Bounding Volume Hierarchy    | Tree of nested bounding volumes                      |
| 19    | spatial-hash                         | Spatial Hash                 | Hash grid for geometric locality                     |
| 20    | uniform-grid                         | Uniform Grid                 | Divide space into equal cells                        |
| 21    | compressed-quadtree                  | Compressed Quadtree          | Quadtree with compressed paths                       |
| 22    | point-location-structure             | Point Location Structure     | Locate region containing a point                     |
| 23    | planar-subdivision                   | Planar Subdivision           | Store faces, edges, and vertices                     |
| 24    | dc-el                                | Doubly Connected Edge List   | Half-edge structure for planar graphs                |
| 25    | half-edge-mesh                       | Half Edge Mesh               | Mesh topology representation                         |
| 26    | winged-edge-structure                | Winged Edge Structure        | Edge-centered mesh structure                         |
| 27    | delaunay-triangulation               | Delaunay Triangulation       | Triangulation maximizing minimum angles              |
| 28    | voronoi-diagram                      | Voronoi Diagram              | Partition plane by nearest site                      |
| 29    | convex-hull-structure                | Convex Hull Structure        | Maintain boundary of points                          |
| 30    | dynamic-convex-hull                  | Dynamic Convex Hull          | Support point insertions and deletions               |
| 31    | nearest-neighbor-index               | Nearest Neighbor Index       | General search index for closest items               |
| 32    | approximate-nearest-neighbor         | Approximate Nearest Neighbor | Trade accuracy for speed                             |
| 33    | locality-sensitive-hashing           | Locality Sensitive Hashing   | Hash similar points into same buckets                |
| 34    | hnsw                                 | HNSW                         | Hierarchical graph for approximate nearest neighbors |
| 35    | range-search-structure               | Range Search Structure       | Query points in a region                             |
| 36    | rectangle-intersection               | Rectangle Intersection       | Detect overlapping rectangles                        |
| 37    | sweep-line-status                    | Sweep Line Status            | Balanced structure for geometric sweeps              |
| 38    | geometric-invariant-check            | Geometric Invariant Check    | Validate spatial partition and ordering              |
| 39    | geometric-memory-layout              | Geometric Memory Layout      | Store coordinates and nodes efficiently              |
| 40    | geometric-benchmarking               | Geometric Benchmarking       | Compare spatial queries and updates                  |

### 3.5 Concurrent and lock-free structures (35)

| index | slug                          | name                          | description                                    |
| ----- | ----------------------------- | ----------------------------- | ---------------------------------------------- |
| 1     | concurrent-data-structure     | Concurrent Data Structure     | Structure safe under simultaneous access       |
| 2     | thread-safe-wrapper           | Thread Safe Wrapper           | Lock-protected wrapper around a structure      |
| 3     | mutex-protected-map           | Mutex Protected Map           | Hash map guarded by a mutex                    |
| 4     | read-write-lock-map           | Read Write Lock Map           | Map optimized for many readers                 |
| 5     | striped-locking               | Striped Locking               | Split one lock into many shard locks           |
| 6     | concurrent-queue              | Concurrent Queue              | Queue for multiple producers and consumers     |
| 7     | mpsc-queue                    | MPSC Queue                    | Multiple producers, single consumer            |
| 8     | spmc-queue                    | SPMC Queue                    | Single producer, multiple consumers            |
| 9     | mpmc-queue                    | MPMC Queue                    | Multiple producers, multiple consumers         |
| 10    | bounded-concurrent-queue      | Bounded Concurrent Queue      | Fixed-capacity concurrent queue                |
| 11    | unbounded-concurrent-queue    | Unbounded Concurrent Queue    | Dynamically growing concurrent queue           |
| 12    | lock-free-stack               | Lock Free Stack               | CAS-based non-blocking stack                   |
| 13    | lock-free-queue               | Lock Free Queue               | CAS-based non-blocking queue                   |
| 14    | lock-free-list                | Lock Free List                | Linked list without blocking locks             |
| 15    | lock-free-hash-table          | Lock Free Hash Table          | Non-blocking hash table                        |
| 16    | lock-free-skip-list           | Lock Free Skip List           | Concurrent ordered set or map                  |
| 17    | wait-free-structure           | Wait Free Structure           | Every operation completes in bounded steps     |
| 18    | obstruction-free-structure    | Obstruction Free Structure    | Progress under solo execution                  |
| 19    | compare-and-swap              | Compare And Swap              | Atomic primitive for lock-free updates         |
| 20    | load-linked-store-conditional | Load Linked Store Conditional | Atomic update primitive                        |
| 21    | aba-problem                   | ABA Problem                   | Hazard caused by reused memory values          |
| 22    | tagged-pointer                | Tagged Pointer                | Add version bits to pointers                   |
| 23    | hazard-pointer                | Hazard Pointer                | Safe memory reclamation method                 |
| 24    | epoch-based-reclamation       | Epoch Based Reclamation       | Reclaim memory after readers exit epochs       |
| 25    | read-copy-update              | Read Copy Update              | Reader-friendly synchronization technique      |
| 26    | memory-ordering               | Memory Ordering               | Rules for atomic visibility                    |
| 27    | linearizability               | Linearizability               | Correctness condition for concurrent objects   |
| 28    | progress-guarantee            | Progress Guarantee            | Blocking, lock-free, wait-free classifications |
| 29    | concurrent-skip-list          | Concurrent Skip List          | Ordered concurrent structure                   |
| 30    | concurrent-bag                | Concurrent Bag                | Unordered concurrent collection                |
| 31    | work-stealing-deque           | Work Stealing Deque           | Deque for task schedulers                      |
| 32    | flat-combining                | Flat Combining                | Batch operations through a combiner            |
| 33    | elimination-backoff-stack     | Elimination Backoff Stack     | Stack using elimination array under contention |
| 34    | concurrent-invariant-check    | Concurrent Invariant Check    | Test thread-safety and structure validity      |
| 35    | concurrent-benchmarking       | Concurrent Benchmarking       | Measure throughput, latency, and contention    |

### 3.6 External-memory and database structures (35)

| index | slug                      | name                      | description                                         |
| ----- | ------------------------- | ------------------------- | --------------------------------------------------- |
| 1     | external-memory-structure | External Memory Structure | Data structure optimized for block I/O              |
| 2     | block-model               | Block Model               | Analyze transfers between disk and memory           |
| 3     | buffer-pool               | Buffer Pool               | Cache disk pages in memory                          |
| 4     | page-cache                | Page Cache                | Operating-system or engine page cache               |
| 5     | slotted-page              | Slotted Page              | Variable-length records inside a fixed page         |
| 6     | heap-file                 | Heap File                 | Unordered collection of records on disk             |
| 7     | sorted-file               | Sorted File               | Disk file maintained in key order                   |
| 8     | clustered-index           | Clustered Index           | Table storage ordered by primary key                |
| 9     | secondary-index           | Secondary Index           | Separate index pointing to base records             |
| 10    | b-tree-index              | B Tree Index              | Disk-oriented balanced tree index                   |
| 11    | b-plus-tree-index         | B Plus Tree Index         | Leaf-linked index for range scans                   |
| 12    | lsm-tree                  | LSM Tree                  | Log-structured merge tree for write-heavy workloads |
| 13    | memtable                  | Memtable                  | In-memory write buffer                              |
| 14    | sstable                   | SSTable                   | Immutable sorted disk table                         |
| 15    | bloom-filter-index        | Bloom Filter Index        | Avoid unnecessary disk reads                        |
| 16    | write-ahead-log           | Write Ahead Log           | Durable append-only recovery log                    |
| 17    | checkpoint                | Checkpoint                | Persist a consistent state for recovery             |
| 18    | compaction                | Compaction                | Merge and rewrite sorted runs                       |
| 19    | leveled-compaction        | Leveled Compaction        | Maintain size-tiered levels                         |
| 20    | tiered-compaction         | Tiered Compaction         | Merge similar-sized runs                            |
| 21    | fractal-tree-index        | Fractal Tree Index        | Buffered tree optimized for writes                  |
| 22    | buffer-tree               | Buffer Tree               | External-memory tree with batched updates           |
| 23    | cache-oblivious-structure | Cache Oblivious Structure | Efficient across unknown block sizes                |
| 24    | log-structured-storage    | Log Structured Storage    | Append updates and compact later                    |
| 25    | append-only-file          | Append Only File          | Sequential write structure                          |
| 26    | columnar-store            | Columnar Store            | Store values by column                              |
| 27    | row-store                 | Row Store                 | Store complete records together                     |
| 28    | zone-map                  | Zone Map                  | Min/max metadata for block pruning                  |
| 29    | bitmap-index              | Bitmap Index              | Bitset-based secondary index                        |
| 30    | inverted-index            | Inverted Index            | Term-to-document index                              |
| 31    | posting-list              | Posting List              | Sorted list of document ids or row ids              |
| 32    | roaring-bitmap-index      | Roaring Bitmap Index      | Compressed bitmap index                             |
| 33    | external-sort             | External Sort             | Sort data larger than memory                        |
| 34    | external-merge            | External Merge            | Merge sorted runs from disk                         |
| 35    | external-invariant-check  | External Invariant Check  | Validate disk layout and index metadata             |

### 3.7 Probabilistic data structures (15)

| index | slug                                | name                          | description                                           |
| ----- | ----------------------------------- | ----------------------------- | ----------------------------------------------------- |
| 1     | probabilistic-data-structure        | Probabilistic Data Structure  | Use randomness or approximation to save space or time |
| 2     | bloom-filter-probabilistic          | Bloom Filter                  | Approximate membership with false positives           |
| 3     | counting-bloom-filter-probabilistic | Counting Bloom Filter         | Bloom filter variant that supports deletions          |
| 4     | cuckoo-filter-probabilistic         | Cuckoo Filter                 | Approximate membership with compact fingerprints      |
| 5     | quotient-filter-probabilistic       | Quotient Filter               | Cache-friendly approximate membership                 |
| 6     | xor-filter-probabilistic            | XOR Filter                    | Static approximate membership with fast lookup        |
| 7     | count-min-sketch                    | Count Min Sketch              | Approximate frequency counting                        |
| 8     | count-sketch                        | Count Sketch                  | Frequency estimates with signed counters              |
| 9     | hyperloglog                         | HyperLogLog                   | Approximate cardinality counting                      |
| 10    | minhash                             | MinHash                       | Estimate set similarity                               |
| 11    | reservoir-sampling                  | Reservoir Sampling            | Maintain random sample from a stream                  |
| 12    | skip-list                           | Skip List                     | Randomized ordered set or map                         |
| 13    | treap-probabilistic                 | Treap                         | Randomized balanced search tree                       |
| 14    | randomized-meldable-heap            | Randomized Meldable Heap      | Priority queue with randomized merging                |
| 15    | probabilistic-invariant-check       | Probabilistic Invariant Check | Validate error bounds and structural assumptions      |

