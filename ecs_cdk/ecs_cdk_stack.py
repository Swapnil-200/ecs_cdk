from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
)
from constructs import Construct


class EcsCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            "Test_VPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            nat_gateways=1,
            max_azs=2,
        )
        # Iterate the private subnets
        selection = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)

        # for subnet in selection.subnets:
        #   pass

        cluster = ecs.Cluster(self, "testcluster", vpc=vpc)

        # added task defination
        fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDef", cpu=256)
        
        # added container to task defination
        container = fargate_task_definition.add_container("WebContainer",  
        # Used an image from DockerHub
        image=ecs.ContainerImage.from_registry("atharvab/flask_image"),
        # added port mapping
        port_mappings=[ecs.PortMapping(container_port=1532)],
        )

        # ECS service
        service = ecs.FargateService( self, "Service", cluster=cluster, task_definition=fargate_task_definition,
        desired_count=2,)

        service.connections.allow_from_any_ipv4(
            ec2.Port.tcp(1532), "Allow inbound on port 1532"
        )

        lb = elbv2.ApplicationLoadBalancer(
            self, "LoadBalancer", vpc=vpc, internet_facing=True
        )
        listener = lb.add_listener("Listener", port=80)
        target_group1 = listener.add_targets("ECS1", port=80, targets=[service])
