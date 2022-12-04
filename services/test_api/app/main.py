#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticapm
from elasticapm.base import Client as APMClient
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from elasticapm.utils.disttracing import TraceParent
from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from app.config import config_from_envvar
from app.utils import is_service_running, print_msg

config = config_from_envvar()
app = FastAPI(
    title=config.SERVICE_NAME,
    version="0.0.1",
    root_path=config.ROOT_PATH,
    openapi_url='/api/openapi.json',
    docs_url='/api/docs',
    redoc_url='/api/redoc',
)

print_msg(f'{config.ROOT_PATH=}')

if config.APM_ENABLED and is_service_running(host=config.APM_SERVER_HOST,
                                             port=config.APM_SERVER_PORT):
    apm: APMClient = make_apm_client({
        'SERVICE_NAME': config.SERVICE_NAME,
        'SERVER_URL': config.APM_SERVER_URL,
        'LOG_LEVEL': config.APM_LOG_LEVEL,
        'ENABLED': config.APM_ENABLED,
    })
    app.add_middleware(ElasticAPM, client=apm)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

router = APIRouter()


def get_trace(request: Request) -> TraceParent:
    """
    Create a TraceParent object from HTTP headers
    """
    return elasticapm.trace_parent_from_headers(request.headers)


@router.get(
    '/test',
    tags=['Test endpoints'],
    status_code=HTTP_200_OK,
)
async def test_endpoint(request: Request, trace: TraceParent = Depends(get_trace)):
    """
    Test endpoint
    """
    try:
        print_msg(f'{request.headers["traceparent"]=}')
        print_msg(f'{trace.trace_id=}')
        print_msg(f'{trace.span_id=}')
        print_msg(f'{trace.version=}')
        return {'traceparent': request.headers["traceparent"], 'trace_id': trace.trace_id}
    except Exception as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail=f"ERROR: {error}") from error


@router.get(
    '/test/{fake_id}',
    tags=['Test endpoints'],
    status_code=HTTP_200_OK,
)
async def test_endpoint_2(request: Request, fake_id: str, trace: TraceParent = Depends(get_trace)):
    """
    Test endpoint with path parameter
    """
    try:
        print_msg(f'{request.headers["traceparent"]=}')
        print_msg(f'{trace.trace_id=}')
        print_msg(f'{trace.span_id=}')
        print_msg(f'{trace.version=}')
        print_msg(f'{fake_id=}')
        return {'traceparent': request.headers["traceparent"], 'trace_id': trace.trace_id}
    except Exception as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail=f"ERROR: {error}") from error


app.include_router(router)
