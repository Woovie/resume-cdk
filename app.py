#!/usr/bin/env python3
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
ResumeCdkStack(
    app,
    "ResumeCdkStack",
    env=cdk.Environment(
        account=getenv(envvars[getenv("CDK_STAGE")]["account"]),
        region=getenv(envvars[getenv("CDK_STAGE")]["region"]),
    ),
)

app.synth()
