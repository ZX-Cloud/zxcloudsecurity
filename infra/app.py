import aws_cdk as cdk
from infra.zxcloudsecurity_stack import ZxCloudsecurityStack

app = cdk.App()
ZxCloudsecurityStack(
    app,
    "ZxCloudsecurityStack",
    env=cdk.Environment(region="eu-west-2"),
)
app.synth()