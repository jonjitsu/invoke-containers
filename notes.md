
# -r / --search-root is not like make -C
With `make -C examples/simple` make changes CWD to the value of -C.

-r / --search-root only looks for tasks in that directory.

It is possible to discover the value of search-root with
`cwd = self.context.config._project_prefix`

Likely this should not be relied upon and using this value would create inconsistent behaviour between tasks using the @container decorator and not.