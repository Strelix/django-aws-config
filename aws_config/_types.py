import re
from typing import Optional, NotRequired, TypedDict, Literal

from pydantic import Field, AnyHttpUrl, BaseModel

AWS_REGIONS = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "af-south-1",
    "ap-east-1",
    "ap-south-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ap-south-1",
    "ap-northeast-3",
    "ap-northeast-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "ca-west-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-south-1",
    "eu-west-3",
    "eu-south-2",
    "eu-north-1",
    "eu-central-2",
    "il-central-1",
    "me-south-1",
    "me-central-1",
    "sa-east-1",
    "us-gov-east-1",
    "us-gov-west-1",
]

BucketName: str = Field(description="Bucket name")
AccessKeyId: str = Field(description="AWS secret access key")
AccessKey: str = Field(description="AWS access key ID")
SignUrls: bool = Field(default=False, description="Sign S3/Cloudfront URLs")
OptionalAccessKey: str | None = Field(default=None, description="AWS access key ID")
OptionalAccessKeyId: str | None = Field(default=None, description="AWS secret access key")
OptionalCloudfrontKey = Field(default=None, description="Cloudfront key")
OptionalCloudfrontKeyId = Field(default=None, description="Cloudfront key ID")
OptionalRegionName: str = Field(
    default="eu-west-1", description="Region name", pattern=rf"({'|'.join(re.escape(region) for region in AWS_REGIONS)})"
)
OptionalCustomCDNDomain: str | None = Field(
    default=None,
    description="Custom Cloudfront domain to use when generating URLs",
    pattern=r"^[^:\/][a-zA-Z0-9-_]+(?:[\.\-][a-zA-Z0-9-_]+)*$",
)
OptionalEndPointUrl: AnyHttpUrl | None = Field(default=None, description="Custom S3 URL to use when connecting to S3, including scheme")
OptionalDefaultACL: str = Field(default="private", description="Default ACL")
OptionalPathPrefix: str = Field(default="", description="Path prefix to add to every file. Do NOT start with a slash.")
VerifyConnection: bool = Field(default=True, description="Verify AWS connection")

class AWSSharedSettings(BaseModel):
    """
    Settings shared across AWS configurations.
    """

    sign_urls: bool | None = SignUrls
    region_name: str | None = OptionalRegionName
    custom_cdn_domain: str | None = OptionalCustomCDNDomain
    path_prefix: str | None = OptionalPathPrefix
    default_acl: str | None = OptionalDefaultACL
    access_key_id: str | None = OptionalAccessKeyId
    access_key: str | None = OptionalAccessKey
    verify_connection: bool | None = VerifyConnection


class AWSSharedSettingsDict(TypedDict):
    sign_urls: NotRequired[bool]
    region_name: NotRequired[str]
    custom_cdn_domain: NotRequired[AnyHttpUrl]
    path_prefix: NotRequired[str]
    access_key_id: NotRequired[str]
    access_key: NotRequired[str]
    default_acl: NotRequired[str]
    verify_connection: NotRequired[bool]


class AWSConfigDict(TypedDict, AWSSharedSettingsDict):
    option: Literal["static", "media_private", "media_public"]
    bucket_name: str
    cloudfront_key: NotRequired[str]
    cloudfront_key_id: NotRequired[str]
    endpoint_url: NotRequired[AnyHttpUrl]


class AWSConfig(AWSSharedSettings):
    """
    AWS S3 configuration settings.
    """

    option: Literal["static", "media_private", "media_public"] = Field(
        default="static",
        description="S3 option",
        example=["static", "media_private", "media_public"],
    )
    bucket_name: str = BucketName
    cloudfront_key: str | None = OptionalCloudfrontKey
    cloudfront_key_id: str | None = OptionalCloudfrontKeyId
    endpoint_url: AnyHttpUrl | None = OptionalEndPointUrl
