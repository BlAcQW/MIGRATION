import boto3

# Set up AWS credentials
aws_access_key_id = "your_access_key_id"
aws_secret_access_key = "your_secret_access_key"
aws_session_token = "your_session_token"

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

# Create an EC2 client
ec2 = session.client('ec2')

# Get the AWS VM ID
vm_id = "your_vm_id"

# Get the AWS VM details
response = ec2.describe_instances(InstanceIds=[vm_id])
vm_details = response['Reservations'][0]['Instances'][0]

# Create an Azure VM
resource_group_name = "MyResourceGroup"
location = "westus"
vm_name = "MyAzureVM"

azure_client = boto3.client('azure')

response = azure_client.create_or_update_vm(
    resource_group_name=resource_group_name,
    location=location,
    vm_name=vm_name,
    vm_size="Standard_A1",
    image_reference=vm_details['ImageId'],
    storage_account_type="Standard_LRS",
    os_type="Linux",
    admin_username="admin",
    admin_password="your_password",
    network_interface_ids=["your_network_interface_id"]
)

# Start the migration process
migration_task_id = response['migrationTaskId']

while True:
    response = azure_client.get_migration_task(
        resource_group_name=resource_group_name,
        migration_task_id=migration_task_id
    )

    if response['status'] == 'Succeeded':
        break
    else:
        print(f"Migration task status: {response['status']}")
        time.sleep(5)

# Delete the AWS VM
ec2.terminate_instances(InstanceIds=[vm_id])