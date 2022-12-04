#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from pydantic import BaseModel


class BaseConfig(BaseModel):
    """Base configuration"""
    # API
    SERVICE_NAME: str
    ROOT_PATH: str = ''

    # CORS
    ALLOWED_HOSTS: list = ['localhost', '127.0.0.1']

    # APM
    APM_SERVER_HOST: str
    APM_SERVER_PORT: int
    APM_SERVER_URL: str | None = None
    APM_LOG_LEVEL: str = 'off'
    APM_ENABLED: bool = False

    def calculate_apm_server_url(self) -> None:
        """
        Concatinate parameters to get correct APM_SERVER_URL
        """
        if self.APM_SERVER_URL is None:
            self.APM_SERVER_URL = f'http://{self.APM_SERVER_HOST}:{self.APM_SERVER_PORT}'


def config_from_envvar() -> BaseConfig:
    """Get configuration class from environment variable"""
    loaded_config: BaseConfig = BaseConfig(**os.environ)
    loaded_config.calculate_apm_server_url()
    return loaded_config
