"""
zxcloudsecurity_stack.py
AWS CDK Stack for zxcloudsecurity.co.uk
"""

from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_ssm as ssm,
)
from constructs import Construct


class ZxCloudsecurityStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        domain_name = "zxcloudsecurity.co.uk"
        www_domain = f"www.{domain_name}"

        # ── SSL Certificate (already issued, just reference it) ───────────────
        certificate = acm.Certificate.from_certificate_arn(
            self,
            "SiteCertificate",
            "arn:aws:acm:us-east-1:917117230191:certificate/6f6a670f-afd9-4f49-8af8-c335f1a7709b",
        )

        # ── S3 bucket for site content ────────────────────────────────────────
        site_bucket = s3.Bucket.from_bucket_name(
            self,
            "SiteBucket",
            "zxcloudsecurity-site",
        )

        # ── S3 bucket for CloudFront logs ─────────────────────────────────────
        logs_bucket = s3.Bucket.from_bucket_name(
            self,
            "LogsBucket",
            "zxcloudsecurity-cf-logs",
        )

        # ── CloudFront distribution ───────────────────────────────────────────
        distribution = cloudfront.Distribution(
            self,
            "Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(site_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                compress=True,
                function_associations=[
                    cloudfront.FunctionAssociation(
                        function=cloudfront.Function.from_function_attributes(
                            self, "UrlRewrite",
                            function_arn="arn:aws:cloudfront::917117230191:function/zxcloudsecurity-url-rewrite",
                            function_name="zxcloudsecurity-url-rewrite",
                        ),
                        event_type=cloudfront.FunctionEventType.VIEWER_REQUEST,
                    )
                ],
            ),
            domain_names=[domain_name, www_domain],
            certificate=certificate,
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=404,
                    response_page_path="/404.html",
                ),
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=404,
                    response_page_path="/404.html",
                ),
            ],
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
            comment=f"{domain_name} static site",
            enable_logging=True,
            log_bucket=logs_bucket,
            log_file_prefix="cloudfront/",
        )

        # ── SSM Parameter — distribution ID for GitHub Actions ───────────────
        ssm.StringParameter(
            self,
            "DistributionIdParam",
            parameter_name="/zxcloudsecurity/cloudfront-distribution-id",
            string_value=distribution.distribution_id,
            description="CloudFront distribution ID for zxcloudsecurity.co.uk",
        )

        # ── Outputs ───────────────────────────────────────────────────────────
        CfnOutput(self, "SiteBucketName", value=site_bucket.bucket_name)
        CfnOutput(self, "DistributionId", value=distribution.distribution_id)
        CfnOutput(self, "DistributionDomain", value=distribution.distribution_domain_name)
