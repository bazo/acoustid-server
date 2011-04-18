# Copyright (C) 2011 Lukas Lalinsky
# Distributed under the MIT license, see the LICENSE file for details.

from nose.tools import *
from tests import (prepare_database, with_database, assert_json_equals,
    TEST_1_LENGTH,
    TEST_1_FP,
    TEST_1_FP_RAW,
    TEST_2_LENGTH,
    TEST_2_FP,
    TEST_2_FP_RAW,
)
from werkzeug.wrappers import Request
from werkzeug.test import EnvironBuilder
from werkzeug.datastructures import MultiDict
from acoustid.api import errors
from acoustid.api.v1 import (
    LookupHandlerParams,
    SubmitHandlerParams,
    APIHandler,
)


def test_ok():
    handler = APIHandler()
    resp = handler._ok({'tracks': [{'id': 1, 'name': 'Track 1'}]})
    assert_equals('text/xml', resp.content_type)
    expected = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<response status="ok"><tracks><track><id>1</id><name>Track 1</name></track></tracks></response>'
    assert_equals(expected, resp.data)
    assert_equals('200 OK', resp.status)


def test_error():
    handler = APIHandler()
    resp = handler._error(123, 'something is wrong')
    assert_equals('text/xml', resp.content_type)
    expected = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<response status="error"><error>something is wrong</error></response>'
    assert_equals(expected, resp.data)
    assert_equals('400 BAD REQUEST', resp.status)
    resp = handler._error(234, 'oops', status=500)
    assert_equals('text/xml', resp.content_type)
    expected = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<response status="error"><error>oops</error></response>'
    assert_equals(expected, resp.data)
    assert_equals('500 INTERNAL SERVER ERROR', resp.status)


@with_database
def test_lookup_handler_params(conn):
    # missing client
    values = MultiDict({})
    params = LookupHandlerParams()
    assert_raises(errors.MissingParameterError, params.parse, values, conn)
    # invalid client
    values = MultiDict({'client': 'N/A'})
    params = LookupHandlerParams()
    assert_raises(errors.InvalidAPIKeyError, params.parse, values, conn)
    # missing length
    values = MultiDict({'client': 'app1key'})
    params = LookupHandlerParams()
    assert_raises(errors.MissingParameterError, params.parse, values, conn)
    # missing fingerprint
    values = MultiDict({'client': 'app1key', 'length': str(TEST_1_LENGTH)})
    params = LookupHandlerParams()
    assert_raises(errors.MissingParameterError, params.parse, values, conn)
    # invalid fingerprint
    values = MultiDict({'client': 'app1key', 'length': str(TEST_1_LENGTH), 'fingerprint': '...'})
    params = LookupHandlerParams()
    assert_raises(errors.InvalidFingerprintError, params.parse, values, conn)
    # all ok
    values = MultiDict({'client': 'app1key', 'length': str(TEST_1_LENGTH), 'fingerprint': TEST_1_FP})
    params = LookupHandlerParams()
    params.parse(values, conn)
    assert_equals(1, params.application_id)
    assert_equals(TEST_1_LENGTH, params.duration)
    assert_equals(TEST_1_FP_RAW, params.fingerprint)


@with_database
def test_submit_handler_params(conn):
    # missing client
    values = MultiDict({})
    params = SubmitHandlerParams()
    assert_raises(errors.MissingParameterError, params.parse, values, conn)
    # invalid client
    values = MultiDict({'client': 'N/A'})
    params = SubmitHandlerParams()
    assert_raises(errors.InvalidAPIKeyError, params.parse, values, conn)
    # missing user
    values = MultiDict({'client': 'app1key'})
    params = SubmitHandlerParams()
    assert_raises(errors.MissingParameterError, params.parse, values, conn)
    # invalid user
    values = MultiDict({'client': 'app1key', 'user': 'N/A'})
    params = SubmitHandlerParams()
    assert_raises(errors.InvalidUserAPIKeyError, params.parse, values, conn)
    # missing fingerprint
    values = MultiDict({'client': 'app1key', 'user': 'user1key'})
    params = SubmitHandlerParams()
    assert_raises(errors.MissingParameterError, params.parse, values, conn)
    # all ok (single submission)
    values = MultiDict({'client': 'app1key', 'user': 'user1key',
        'mbid': ['4d814cb1-20ec-494f-996f-f31ca8a49784', '66c0f5cc-67b6-4f51-80cd-ab26b5aaa6ea'],
        'puid': '4e823498-c77d-4bfb-b6cc-85b05c2783cf',
        'length': str(TEST_1_LENGTH),
        'fingerprint': TEST_1_FP,
        'bitrate': '192',
        'format': 'MP3'
    })
    params = SubmitHandlerParams()
    params.parse(values, conn)
    assert_equals(1, len(params.submissions))
    assert_equals(['4d814cb1-20ec-494f-996f-f31ca8a49784', '66c0f5cc-67b6-4f51-80cd-ab26b5aaa6ea'], params.submissions[0]['mbids'])
    assert_equals('4e823498-c77d-4bfb-b6cc-85b05c2783cf', params.submissions[0]['puid'])
    assert_equals(TEST_1_LENGTH, params.submissions[0]['duration'])
    assert_equals(TEST_1_FP_RAW, params.submissions[0]['fingerprint'])
    assert_equals(192, params.submissions[0]['bitrate'])
    assert_equals('MP3', params.submissions[0]['format'])
    # all ok (single submission)
    values = MultiDict({'client': 'app1key', 'user': 'user1key',
        'mbid.0': '4d814cb1-20ec-494f-996f-f31ca8a49784',
        'puid.0': '4e823498-c77d-4bfb-b6cc-85b05c2783cf',
        'length.0': str(TEST_1_LENGTH),
        'fingerprint.0': TEST_1_FP,
        'bitrate.0': '192',
        'format.0': 'MP3',
        'mbid.1': '66c0f5cc-67b6-4f51-80cd-ab26b5aaa6ea',
        'puid.1': '57b202a3-242b-4896-a79c-cac34bbca0b6',
        'length.1': str(TEST_2_LENGTH),
        'fingerprint.1': TEST_2_FP,
        'bitrate.1': '500',
        'format.1': 'FLAC',
    })
    params = SubmitHandlerParams()
    params.parse(values, conn)
    assert_equals(2, len(params.submissions))
    assert_equals(['4d814cb1-20ec-494f-996f-f31ca8a49784'], params.submissions[0]['mbids'])
    assert_equals('4e823498-c77d-4bfb-b6cc-85b05c2783cf', params.submissions[0]['puid'])
    assert_equals(TEST_1_LENGTH, params.submissions[0]['duration'])
    assert_equals(TEST_1_FP_RAW, params.submissions[0]['fingerprint'])
    assert_equals(192, params.submissions[0]['bitrate'])
    assert_equals('MP3', params.submissions[0]['format'])
    assert_equals(['66c0f5cc-67b6-4f51-80cd-ab26b5aaa6ea'], params.submissions[1]['mbids'])
    assert_equals('57b202a3-242b-4896-a79c-cac34bbca0b6', params.submissions[1]['puid'])
    assert_equals(TEST_2_LENGTH, params.submissions[1]['duration'])
    assert_equals(TEST_2_FP_RAW, params.submissions[1]['fingerprint'])
    assert_equals(500, params.submissions[1]['bitrate'])
    assert_equals('FLAC', params.submissions[1]['format'])
