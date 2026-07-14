import io
import json
import logging
import unittest
import urllib.error
from unittest.mock import Mock

from operations.waef.github_client import GitHubClient


class Response:
    def __init__(self, payload, status=200, headers=None):
        self.payload = json.dumps(payload).encode("utf-8")
        self.status = status
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.payload


def http_error(status, payload=None, headers=None):
    return urllib.error.HTTPError(
        "https://api.github.com/test",
        status,
        "failure",
        headers or {},
        io.BytesIO(json.dumps(payload or {"message": "failure"}).encode("utf-8")),
    )


class GitHubClientTests(unittest.TestCase):
    def test_request_sets_required_headers_and_serializes_json(self):
        opener = Mock(return_value=Response({"ok": True}))
        client = GitHubClient("secret-token", opener=opener, sleep=Mock())

        result = client.request("POST", "/repos/weiandata/WAEF/issues", {"title": "audit"})

        self.assertEqual({"ok": True}, result)
        request = opener.call_args.args[0]
        self.assertEqual("Bearer secret-token", request.get_header("Authorization"))
        self.assertEqual("application/vnd.github+json", request.get_header("Accept"))
        self.assertEqual("2022-11-28", request.get_header("X-github-api-version"))
        self.assertEqual("application/json", request.get_header("Content-type"))
        self.assertEqual({"title": "audit"}, json.loads(request.data))

    def test_retryable_statuses_use_exponential_delays(self):
        opener = Mock(
            side_effect=[
                http_error(502),
                http_error(503),
                http_error(504),
                Response({"ok": True}),
            ]
        )
        sleep = Mock()
        client = GitHubClient("secret-token", opener=opener, sleep=sleep)

        self.assertEqual({"ok": True}, client.request("GET", "/test"))
        self.assertEqual([unittest.mock.call(1), unittest.mock.call(2), unittest.mock.call(4)], sleep.call_args_list)
        self.assertEqual(4, opener.call_count)

    def test_retry_after_header_overrides_exponential_delay(self):
        opener = Mock(side_effect=[http_error(429, headers={"Retry-After": "9"}), Response([])])
        sleep = Mock()
        client = GitHubClient("secret-token", opener=opener, sleep=sleep)

        self.assertEqual([], client.request("GET", "/test"))
        sleep.assert_called_once_with(9)

    def test_client_stops_after_three_retries(self):
        opener = Mock(side_effect=[http_error(503) for _ in range(4)])
        client = GitHubClient("secret-token", opener=opener, sleep=Mock())

        with self.assertRaises(urllib.error.HTTPError):
            client.request("GET", "/test")
        self.assertEqual(4, opener.call_count)

    def test_non_retryable_status_is_not_retried(self):
        for status in (401, 403, 404, 422):
            with self.subTest(status=status):
                opener = Mock(side_effect=http_error(status))
                client = GitHubClient("secret-token", opener=opener, sleep=Mock())
                with self.assertRaises(urllib.error.HTTPError):
                    client.request("GET", "/test")
                self.assertEqual(1, opener.call_count)

    def test_token_is_redacted_from_logs(self):
        stream = io.StringIO()
        logger = logging.getLogger("waef-test-redaction")
        logger.handlers = [logging.StreamHandler(stream)]
        logger.setLevel(logging.DEBUG)
        opener = Mock(side_effect=http_error(401, {"message": "Bearer secret-token invalid"}))
        client = GitHubClient("secret-token", opener=opener, sleep=Mock(), logger=logger)

        with self.assertRaises(urllib.error.HTTPError):
            client.request("GET", "/test")

        self.assertNotIn("secret-token", stream.getvalue())
        self.assertIn("[REDACTED]", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
