"""
Basic helper module to simplify constructor variable input by grouping commonly used values into a
dataclass
"""

from dataclasses import dataclass
from aws_cdk import aws_certificatemanager as acm

@dataclass
class DomainDetails:
    """
    Simple helper class
    """
    zone_id: str
    zone_name: str
    site_domain_name: str
    custom_header_parameter_name: str
    certificate_arn: acm.DnsValidatedCertificate = None
