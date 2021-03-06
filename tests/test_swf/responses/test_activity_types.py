import boto
from boto.swf.exceptions import SWFResponseError
from sure import expect

from moto import mock_swf


# RegisterActivityType endpoint
@mock_swf
def test_register_activity_type():
    conn = boto.connect_swf("the_key", "the_secret")
    conn.register_domain("test-domain", "60")
    conn.register_activity_type("test-domain", "test-activity", "v1.0")

    types = conn.list_activity_types("test-domain", "REGISTERED")
    actype = types["typeInfos"][0]
    actype["activityType"]["name"].should.equal("test-activity")
    actype["activityType"]["version"].should.equal("v1.0")

@mock_swf
def test_register_already_existing_activity_type():
    conn = boto.connect_swf("the_key", "the_secret")
    conn.register_domain("test-domain", "60")
    conn.register_activity_type("test-domain", "test-activity", "v1.0")

    conn.register_activity_type.when.called_with(
        "test-domain", "test-activity", "v1.0"
    ).should.throw(SWFResponseError)

@mock_swf
def test_register_with_wrong_parameter_type():
    conn = boto.connect_swf("the_key", "the_secret")
    conn.register_domain("test-domain", "60")

    conn.register_activity_type.when.called_with(
        "test-domain", "test-activity", 12
    ).should.throw(SWFResponseError)

# ListActivityTypes endpoint
@mock_swf
def test_list_activity_types():
    conn = boto.connect_swf("the_key", "the_secret")
    conn.register_domain("test-domain", "60")
    conn.register_activity_type("test-domain", "b-test-activity", "v1.0")
    conn.register_activity_type("test-domain", "a-test-activity", "v1.0")
    conn.register_activity_type("test-domain", "c-test-activity", "v1.0")

    all_activity_types = conn.list_activity_types("test-domain", "REGISTERED")
    names = [activity_type["activityType"]["name"] for activity_type in all_activity_types["typeInfos"]]
    names.should.equal(["a-test-activity", "b-test-activity", "c-test-activity"])

@mock_swf
def test_list_activity_types_reverse_order():
    conn = boto.connect_swf("the_key", "the_secret")
    conn.register_domain("test-domain", "60")
    conn.register_activity_type("test-domain", "b-test-activity", "v1.0")
    conn.register_activity_type("test-domain", "a-test-activity", "v1.0")
    conn.register_activity_type("test-domain", "c-test-activity", "v1.0")

    all_activity_types = conn.list_activity_types("test-domain", "REGISTERED",
                                                  reverse_order=True)
    names = [activity_type["activityType"]["name"] for activity_type in all_activity_types["typeInfos"]]
    names.should.equal(["c-test-activity", "b-test-activity", "a-test-activity"])


# DeprecateActivityType endpoint
@mock_swf
def test_deprecate_activity_type():
    conn = boto.connect_swf("the_key", "the_secret")
    conn.register_domain("test-domain", "60")
    conn.register_activity_type("test-domain", "test-activity", "v1.0")
    conn.deprecate_activity_type("test-domain", "test-activity", "v1.0")

    actypes = conn.list_activity_types("test-domain", "DEPRECATED")
    actype = actypes["typeInfos"][0]
    actype["activityType"]["name"].should.equal("test-activity")
    actype["activityType"]["version"].should.equal("v1.0")

@mock_swf
def test_deprecate_already_deprecated_activity_type():
    conn = boto.connect_swf("the_key", "the_secret")
    conn.register_domain("test-domain", "60")
    conn.register_activity_type("test-domain", "test-activity", "v1.0")
    conn.deprecate_activity_type("test-domain", "test-activity", "v1.0")

    conn.deprecate_activity_type.when.called_with(
        "test-domain", "test-activity", "v1.0"
    ).should.throw(SWFResponseError)

@mock_swf
def test_deprecate_non_existent_activity_type():
    conn = boto.connect_swf("the_key", "the_secret")
    conn.register_domain("test-domain", "60")

    conn.deprecate_activity_type.when.called_with(
        "test-domain", "non-existent", "v1.0"
    ).should.throw(SWFResponseError)

# DescribeActivityType endpoint
@mock_swf
def test_describe_activity_type():
    conn = boto.connect_swf("the_key", "the_secret")
    conn.register_domain("test-domain", "60")
    conn.register_activity_type("test-domain", "test-activity", "v1.0",
                                task_list="foo", default_task_heartbeat_timeout="32")

    actype = conn.describe_activity_type("test-domain", "test-activity", "v1.0")
    actype["configuration"]["defaultTaskList"]["name"].should.equal("foo")
    infos = actype["typeInfo"]
    infos["activityType"]["name"].should.equal("test-activity")
    infos["activityType"]["version"].should.equal("v1.0")
    infos["status"].should.equal("REGISTERED")

@mock_swf
def test_describe_non_existent_activity_type():
    conn = boto.connect_swf("the_key", "the_secret")
    conn.register_domain("test-domain", "60")

    conn.describe_activity_type.when.called_with(
        "test-domain", "non-existent", "v1.0"
    ).should.throw(SWFResponseError)
