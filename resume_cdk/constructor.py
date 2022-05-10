"""
AWS CDK constructor for stack generation
"""
from aws_cdk import (
    RemovalPolicy,
    aws_s3 as s3,
    aws_certificatemanager as acm,
    aws_route53 as route53,# TODO replace Route 53 with Cloudflare
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_route53_targets as targets,
    aws_ssm as ssm,# TODO I may not use this, but I'd like to implement it regardless
)

from constructs import Construct

from resume_cdk.domain_details import DomainDetails# TODO fix import error, no idea why it has one

class ResumeConstructor(Construct):
    """
    Constructs the CDK construct which is then used in stack generation
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_details: DomainDetails,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = None
        self.certificate = None
        self.distribution = None

        self._site_domain_name = domain_details.site_domain_name
        self.__hosted_zone_name = domain_details.zone_name
        self.__hosted_zone_id = domain_details.zone_id
        self.__domain_certificate_arn = domain_details.certificate_arn

        self._build_site()

    def _create_site_bucket(self):  # Always a private bucket
        self.bucket = s3.Bucket(
            self,
            "resume_bucket",
            bucket_name=self._site_domain_name,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

    def __get_hosted_zone(self):
        return route53.HostedZone.from_hosted_zone_attributes(
            self,
            "resume_zone",
            zone_name=self.__hosted_zone_name,
            hosted_zone_id=self.__hosted_zone_id,
        )

    def __create_certificate(self, hosted_zone: route53.HostedZone):
        if self.__domain_certificate_arn:
            # I don't think I'll hit this logic but, it's there just in case
            self.certificate = acm.Certificate.from_certificate_arn(
                self,
                "resume_certificate",
                certificate_arn=self.__domain_certificate_arn,
            )
        else:
            self.certificate = acm.DnsValidatedCertificate(
                self,
                "resume_certificate",
                domain_name=self._site_domain_name,
                hosted_zone=hosted_zone,
                region="us-east-1",
            )

    def _create_cloudfront_distribution(self):
        self.distribution = cloudfront.Distribution(
            self,
            "resume_cf_distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(self.bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            domain_names=[self._site_domain_name],
            certificate=self.certificate,
            default_root_object="index.html",
        )

    def __create_route53_record(self, hosted_zone: route53.HostedZone):
        route53.ARecord(
            self,
            "resume-address-record",
            record_name=self._site_domain_name,
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(self.distribution)
            ),
        )

    def _build_site(self):
        self._create_site_bucket()

        hosted_zone = self.__get_hosted_zone()

        self.__create_certificate(hosted_zone)
        self._create_cloudfront_distribution()
        self.__create_route53_record(hosted_zone)
