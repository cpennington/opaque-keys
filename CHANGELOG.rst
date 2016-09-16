# Unreleased

# 0.4

* Enforce the property that serialized keys are equal if and only if the parsed
  keys are equal. In particular, this means that OpaqueKey parsing is now case-sensitive.

# 0.3.4

* Update the regular expression for a course key and locators which use course
  keys so that a string with a trailing newline will no longer be accepted as a
  valid key.

# 0.3.3

* Revert of caching optmizations introduced in 0.3.2, due to a bug that can
  occur where course keys can be parsed with trailing newlines, and those parsed
  values can be serialized into the database.

# 0.3.2

* Simple optimizations to reduce the number of OpaqueKey objects
  created, and to speed up hashing and equality checks.

-----

-No changelog was maintained before 0.3.2.
