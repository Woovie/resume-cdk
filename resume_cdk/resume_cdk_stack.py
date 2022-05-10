"""
AWS CDK stack generator
"""
from os import getenv

from aws_cdk import (
    Stack,
    CfnOutput
)

from constructs import Construct

from resume_cdk.constructor import ResumeConstructor

from resume_cdk.domain_details import DomainDetails

class ResumeCdkStack(Stack):
    """
    Subclass defining the overall scope of my CDK stack for a basic static site resume deployment
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        props: dict,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        site = ResumeConstructor(
            f"{props['namespace']}-construct",
            domain_details=DomainDetails(
                zone_id=props[getenv("CDK_STAGE")]["hosted_zone_id"],
                zone_name=props[getenv("CDK_STAGE")]["hosted_zone_name"],
                site_domain_name=props[getenv("CDK_STAGE")]["domain_name"],
                custom_header_parameter_name=props[getenv("CDK_STAGE")]["custom_header_parameter_name"]
            ),

        )

        CfnOutput(
            self,
            "SiteBucketName",
            value=site.bucket.bucket_name,
        )
        CfnOutput(
            self,
            "DistributionId",
            value=site.distribution.distribution_id,
        )
        CfnOutput(
            self,
            "CertificateArn",
            value=site.certificate.certificate_arn,
        )
