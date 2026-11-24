class MockLlmSkills:

    def __init__(self, requests, responses):
        if len(requests) != len(responses):
            raise ValueError(
                f"requests/responses length mismatch: "
                f"{len(requests)} != {len(responses)}"
            )
        self._requests = list(requests)
        self._responses = list(responses)
        self._calls = []
        self._index = 0

    def invoke(self, **kwargs):
        self._calls.append(kwargs)

        if self._index >= len(self._requests):
            raise AssertionError(
                f"unexpected extra call #{len(self._calls)} "
                f"to FakeSkill with {kwargs!r}; no more expected requests"
            )

        expected = self._requests[self._index]
        if kwargs != expected:
            raise AssertionError(
                f"call #{len(self._calls)} argument mismatch:\n"
                f"  expected: {expected!r}\n"
                f"  actual:   {kwargs!r}"
            )

        response = self._responses[self._index]
        self._index += 1
        return response

    __call__ = invoke

    @property
    def calls(self):
        return list(self._calls)

    @property
    def remaining(self):
        return len(self._requests) - self._index

    def assert_all_called(self):
        if self._index != len(self._requests):
            raise AssertionError(
                f"only {self._index} of {len(self._requests)} expected calls were made; "
                f"remaining requests: {self._requests[self._index:]!r}"
            )
