---
title: Hash Tables
subtitle: Expected constant-time lookups, and what happens when keys collide
---

A hash table maps each key to a bucket, so inserts and lookups take expected $O(1)$ time. When two keys land in the same bucket, separate chaining keeps a list in each bucket, while linear probing moves on to the next free slot. Deleting from a probing table needs tombstones, so later lookups still find the keys stored past the deleted one.

<iframe src="/embed/hashing.html" title="Hash Table Visualizer"></iframe>
