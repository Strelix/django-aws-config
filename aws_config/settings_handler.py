from typing import Literal, Optional, List, NotRequired

from django.core.files.storage import FileSystemStorage
from pydantic import BaseModel, Field, AnyHttpUrl
from storages.backends.s3 import S3Storage

import logging

from typing_extensions import TypedDict

from aws_config._types import (
    AWSSharedSettings,
    AWSSharedSettingsDict,
    AWSConfig,
    AWSConfigDict,
)

logger = logging.getLogger(__name__)

AWSHandler: "AWSHandlerBase"


class AWSHandlerBase(BaseModel):
    """
    Handler for AWS settings.

    :param shared: Shared AWS configuration settings.
    :param credentials: List of AWS configurations.
    """

    shared: AWSSharedSettings | AWSSharedSettingsDict = Field(
        default_factory=AWSSharedSettings, description="Shared AWS configuration settings"
    )
    configs: List[AWSConfig] = Field(default_factory=list, description="List of AWS configurations")
    storages: dict = Field(default_factory=dict, description="AWS storages")
    storage_classes: dict = Field(default_factory=dict, description="AWS storage classes")

    def _get_option(self, option: Literal["static", "media_private", "media_public"]) -> AWSConfig | None:
        """
        Get the AWS configuration option for a specific storage type.

        :param option: Type of storage option ("static", "media_private", or "media_public").
        :return: AWS configuration option or None if not found.
        """
        options = {config.option: config for config in self.configs}
        return options.get(option)

    def _get_existing_storage_class(self, option: Literal["static", "media_private", "media_public"]) -> S3Storage | None:
        return self.storage_classes.get(option)

    def _get_storage_class(self, option: AWSConfig) -> type:
        """
        Get the storage class for a given AWS configuration.

        :param option: AWS configuration option.
        :return: S3Storage class instance.
        """
        if not isinstance(option, AWSConfig):
            logger.error("Invalid option: %s", option)
            raise ValueError("Invalid option")

        if existing_class := self.storage_classes.get(option.option):
            return existing_class

        custom_class = type(
            f"AWSHandler.get_{option.option}()",
            (S3Storage,),
            {
                "location": option.path_prefix,
                "default_acl": option.default_acl or self.shared.default_acl,
                "custom_domain": option.custom_cdn_domain or self.shared.custom_cdn_domain,
                "region_name": option.region_name or self.shared.region_name,
                "access_key": option.access_key_id or self.shared.access_key_id,
                "secret_key": option.access_key or self.shared.access_key,
                "bucket_name": option.bucket_name,
                "endpoint_url": option.endpoint_url,
                "cloudfront_key": option.cloudfront_key,
                "cloudfront_key_id": option.cloudfront_key_id,
            },
        )

        self.storage_classes[option.option] = custom_class

        return custom_class

        # class CustomStorage(S3Storage):
        #     location = option.path_prefix
        #     default_acl = option.default_acl or self.shared.default_acl
        #     custom_domain = option.custom_cdn_domain or self.shared.custom_cdn_domain
        #     region_name = option.region_name or self.shared.region_name
        #     access_key = option.access_key_id or self.shared.access_key_id
        #     secret_key = option.access_key or self.shared.access_key
        #     bucket_name = option.bucket_name
        #     endpoint_url = option.endpoint_url
        #     cloudfront_key = option.cloudfront_key
        #     cloudfront_key_id = option.cloudfront_key_id
        #
        # custom_class = CustomStorage()
        #
        # self.storage_classes[option.option] = CustomStorage
        #
        # return custom_class

    def get_storage(self, option_type: Literal["static", "media_private", "media_public"]) -> FileSystemStorage | S3Storage:
        """
        Get the storage instance for a specific storage type.

        :param option_type: Type of storage option ("static", "media_private", or "media_public").
        :return: FileSystemStorage or S3Storage instance.
        """
        option_obj = self._get_option(option_type)

        if not option_obj:
            return FileSystemStorage()

        return self._get_storage_class(option_obj)

    def get_media_public(self):
        """
        Get the storage instance for public media files.
        """
        return self.get_storage("media_public")

    def get_media_private(self):
        """
        Get the storage instance for private media files.
        """
        return self.get_storage("media_private")

    def get_static(self):
        """
        Get the storage instance for static files.
        """
        return self.get_storage("static")

    def _get_storages_dict(self) -> dict:
        """
        Get a dictionary of configured storages. Used for django's "STORAGES" variable

        :return: Dictionary containing configured storage options.
        """
        storages: dict = self.storages

        static_storage = self.get_storage("static")
        if static_storage:
            storages["staticfiles"] = {"BACKEND": "aws_config.settings_handler.AWSHandler.get_static"}

        for option in ["media_private", "media_public"]:
            storage = self.get_storage(option)  # type: ignore
            if storage:
                storages[option] = {"BACKEND": f"aws_config.settings_handler.AWSHandler.get_{option}"}

        return storages

    def set_shared(self, config: AWSSharedSettings | AWSSharedSettingsDict) -> None:
        """
        Set the shared AWS configuration settings.

        :param config: Shared AWS configuration settings.
        """
        if not isinstance(config, AWSSharedSettings) and not isinstance(config, dict):
            return None

        self.shared = config

    def set_static(self, config: AWSConfig | AWSConfigDict) -> None:
        """
        Set the AWS configuration for static files storage.

        :param config: AWS configuration for static files storage.
        """
        if isinstance(config, dict):
            config = AWSConfig(**config)
        if not isinstance(config, AWSConfig):
            return None

        if self.get_storage("static"):
            self.configs.remove(self._get_option("static"))
        self.configs.append(config)

    def set_configs(self, configs: List[AWSConfig | AWSConfigDict]) -> None:
        """
        Set the list of AWS configurations.

        :param configs: List of AWS configurations.
        """
        if not isinstance(configs, list):
            return None

        new_configs = []

        for config in configs:
            if isinstance(config, dict):
                config = AWSConfig(**config)
            if not isinstance(config, AWSConfig):
                logger.error("Invalid config: %s", config)
                continue
            new_configs.append(config)

        self.configs = new_configs


AWSHandler = AWSHandlerBase()

# Example usage:
settings = AWSHandlerBase(
    shared=AWSSharedSettings(
        region_name="eu-west-2",
        custom_cdn_domain="cdn.example.com",
        path_prefix="/my_site/",
    ),
    configs=[
        AWSConfig(
            option="static",
            access_key_id="AWS_ACCESS_KEY_ID",
            access_key="AWS_SECRET_ACCESS_KEY",
            region_name="eu-west-2",
            custom_cdn_domain="static.example.com",
            bucket_name="static_files_bucket",
        )
    ],
)
