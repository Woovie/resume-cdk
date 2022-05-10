#!/usr/bin/env python3
"""
Here's a docstring so you be quiet
"""
from os import getenv

import aws_cdk as cdk

from resume_cdk.resume_cdk_stack import ResumeCdkStack

envvars = {
    "production": {
        "account": "CDK_PRODUCTION_ACCOUNT",
        "region": "CDK_PRODUCTION_REGION",
    },
    "staging": {
        "account": "CDK_STAGING_ACCOUNT", "region": "CDK_STAGING_REGION"
    },
    None: {# This is only a little dangerous. As long as I don't use JSON I'm okay
        "account": "CDK_DEFAULT_ACCOUNT", "region": "CDK_DEFAULT_REGION"
    }
}


app = cdk.App()

props = {
    "namespace": app.node.try_get_context("namespace"),
    "domain_name": app.node.try_get_context("domain_name"),
    "sub_domain_name": app.node.try_get_context("sub_domain_name"),
    "domain_certificate_arn": app.node.try_get_context(
        "domain_certificate_arn"
    ),
    "enable_s3_website_endpoint": app.node.try_get_context(
        "enable_s3_website_endpoint"
    ),
    "origin_custom_header_parameter_name": app.node.try_get_context(
        "origin_custom_header_parameter_name"
    ),
    "hosted_zone_id": app.node.try_get_context("hosted_zone_id"),
    "hosted_zone_name": app.node.try_get_context("hosted_zone_name"),
    "environments": app.node.try_get_context("environments")
}

ResumeCdkStack(
    app,
    "ResumeCdkStack",
    env=cdk.Environment(
        account=getenv(envvars[getenv("CDK_STAGE")]["account"]),
        region=getenv(envvars[getenv("CDK_STAGE")]["region"]),
    ),
    props=props
)

app.synth()
