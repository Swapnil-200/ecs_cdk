from variables import (
    LB,
    image, 
    port,
    #inbound,
    listener_port,
    cpu
)
 
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,

)

from constructs import Construct


class EcsCdkStack(Stack):

    """
    A class representing a stack for creating EC2 instances and associated resources.

    Attributes:
    - scope: Construct: The parent of this construct (scope).
    - construct_id: str: The identifier for the construct.
    """

    def __init__(self, scope: Construct, construct_id: str,clusterr, service,VPC,VPC_ID,container,**kwargs) -> None:

        """
        Initializes a new EcsCdkStack Cluster.

        Args:
        - scope (Construct): The parent of this construct (scope).
        - construct_id (str): The identifier for the construct.
        - **kwargs: Additional keyword arguments for the Stack constructor.
        """
        super().__init__(scope, construct_id, **kwargs)


        # Creating vpc 
        vpc = ec2.Vpc.from_lookup( self, id=f"{VPC}" , vpc_id=VPC_ID, 
        is_default=False
        )
        # Iterate the private subnets
        selection = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)

        cluster = ecs.Cluster(self, id=f"{clusterr}", vpc=vpc)

        # added task defination
        fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDef", cpu=cpu)
        
        # added container to task defination
        container = fargate_task_definition.add_container(id=f"container",  
        # Used an image from DockerHub
        image=ecs.ContainerImage.from_registry(image),
        # added port mapping
        port_mappings=[ecs.PortMapping(port)]
        )

        # ECS service
        service = ecs.FargateService( self, id=f"{service}", cluster=cluster, task_definition=fargate_task_definition,
        desired_count=2,)

        service.connections.allow_from_any_ipv4(
            ec2.Port.tcp(port), "Allow inbound on port 1532"
        )

        lb = elbv2.ApplicationLoadBalancer(
            self,LB, vpc=vpc, internet_facing=True
        )
        listener = lb.add_listener("Listener", port=listener_port)
        target_group1 = listener.add_targets("ECS1", port=listener_port, targets=[service]) 