import pulumi
import pulumi_aws as aws

ecr = aws.ecr.Repository("nexttrain", image_tag_mutability="MUTABLE")


