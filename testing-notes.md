# Testing notes

These are notes about testing.

## `pytest`
We are using `pytest` as a test runner and `unittest` code for tests. Technically speaking, `pytest` isn't needed to run the unit tests. However, `pytest` is the most popular test runner in the Travis CI documentation and also offers a number of interesting test running features. It is completely compataible with unittest tests.

## Performance profiling

If some of the tests--regression tests inparticular--start running slowly, the test suite can be eecuted with the following command `pytest` command:

```
pytest -vv --durations=0 test/
```

Which will display verbose timing information about test execution.
