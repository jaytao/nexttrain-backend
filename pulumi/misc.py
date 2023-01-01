import pulumi
import pulumi_aws as aws

sg_default = aws.ec2.get_security_group(name="default")

subnets = aws.ec2.get_subnets()
