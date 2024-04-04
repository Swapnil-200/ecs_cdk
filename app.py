#!/usr/bin/env python3
import os

import yaml

import aws_cdk as cdk


from ecs_cdk.ecs_cdk_stack import EcsCdkStack


app = cdk.App()

with open('repo.yaml', 'r') as envfile:
    yaml_environment = yaml.safe_load(envfile)


for i in range(len(yaml_environment['clusters'])):
    clusterr = yaml_environment['clusters'][i]['name']
    service = yaml_environment['services'][i]['name']
    VPC = yaml_environment['info'][i]['vpc']
    VPC_ID = yaml_environment['info'][i]['vpc_id']
    container= yaml_environment['containers'][i]['name']
    


EcsCdkStack(app,f"EcsCdkStack-{i}",clusterr, service, VPC,VPC_ID,container,
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

   # env=cdk.Environment(account=os.getenv('679104321736'), region=os.getenv('ap-south-1')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */  

    env=cdk.Environment(account='679104321736', region='ap-south-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
