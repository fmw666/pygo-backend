from typing import List, Generator

import time
import random

from grpc import (StatusCode, RpcError, UnaryStreamClientInterceptor,
                  UnaryUnaryClientInterceptor, ClientCallDetails)


class RetryInterceptor(UnaryUnaryClientInterceptor,
                       UnaryStreamClientInterceptor):

    def __init__(self,
                 max_retries: int = 3,
                 retry_codes: None | List[StatusCode] = None,
                 retry_timeout_ms=100,
                 retry_jitter_ms=20) -> None:
        """
        :param max_retries: The maximum number of retries to allow.
        :param retry_codes: The set of status codes that should be retried.
        :param retry_timeout_ms: The base timeout in milliseconds to wait
            between retries.
        :param retry_jitter_ms: The jitter in milliseconds to add or subtract
            from the retry timeout.
        :return: None
        """
        if retry_codes is None:
            retry_codes = [StatusCode.UNAVAILABLE,
                           StatusCode.DEADLINE_EXCEEDED]
        self.max_retries = max_retries
        self.retry_codes = retry_codes
        self.retry_timeout_ms = retry_timeout_ms
        self.retry_jitter_ms = retry_jitter_ms

        if self.retry_jitter_ms > self.retry_timeout_ms:
            raise ValueError("retry_jitter_ms cannot be greater than " +
                             "retry_timeout_ms")

    def _next_retry_timeout_seconds(self) -> float:
        """
        Returns the next timeout in seconds to wait before retrying.
        :return: The timeout in seconds.
        """
        ms_timeout = self.retry_timeout_ms + \
            (random.randint(-1, 1) * self.retry_jitter_ms)
        s_timeout = ms_timeout / 1000
        return s_timeout

    def intercept_unary_unary(self,
                              continuation: UnaryUnaryClientInterceptor,
                              client_call_details: ClientCallDetails,
                              request: object) -> None:
        """
        Intercepts a unary-unary invocation asynchronously.
        :param continuation: The continuation function for the intercepted
            invocation.
        :param client_call_details: The client call details.
        :param request: The request value for the invocation.
        :return: None
        """
        retry_count = 0
        while True:
            try:
                response = continuation(client_call_details, request)
                return response
            except RpcError as e:
                if (e.code() not in self.retry_codes or
                   retry_count >= self.max_retries):
                    raise e
                retry_count += 1
                time.sleep(self._next_retry_timeout_seconds())

    def intercept_unary_stream(self,
                               continuation: UnaryStreamClientInterceptor,
                               client_call_details: ClientCallDetails,
                               request: object) -> Generator:
        """
        Intercepts a unary-stream invocation asynchronously.
        :param continuation: The continuation function for the intercepted
            invocation.
        :param client_call_details: The client call details.
        :param request: The request value for the invocation.
        :return: None
        """
        def intercept(continuation: UnaryStreamClientInterceptor,
                      client_call_details: ClientCallDetails,
                      request: object) -> Generator:
            def iterator_wrapper(gen: Generator):
                retry_count = 0
                has_started = False
                while True:
                    try:
                        val = next(gen)
                        has_started = True
                        yield val
                    except RpcError as e:
                        if has_started:
                            raise e
                        if (e.code() not in self.retry_codes or
                           retry_count >= self.max_retries):
                            raise e

                        retry_count += 1
                        timeout = self._next_retry_timeout_seconds()
                        time.sleep(timeout)

                        gen = continuation(client_call_details, request)
                    except StopIteration:
                        return
            return iterator_wrapper(continuation(client_call_details, request))
        return intercept(continuation, client_call_details, request)
