import pulumi
import pulumi_aws as aws
import misc

alb = aws.lb.LoadBalancer(
    "jeffreytao-xyz",
    internal=False,
    load_balancer_type="application",
    security_groups=[misc.sg_default.id],
    subnets=misc.subnets.ids,
    enable_deletion_protection=True,
)
