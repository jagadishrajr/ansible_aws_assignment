# Ansible module to modify ec2 serial console access

This module can be used to enable or disable ec2 serial console access for an AWS account. You can refer more details about serial console access at this [AWS documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configure-access-to-serial-console.html).

## Pre-requisites

To run the library you will need ansible and python installed locally. You will also need boto3 and botocore libraries. You will also need an AWS account (free tier).

### Versions

| Software | Version  |
| -------- | -------- |
| Python   | >=3.6    |
| Ansible  | >=2.9    |
| boto3    | >=1.22.0 |
| botocore | >=1.25.0 |

### AWS Credentials

Create an IAM user with minimum below policy attached to it.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:GetSerialConsoleAccessStatus",
        "ec2:EnableSerialConsoleAccess",
        "ec2:DisableSerialConsoleAccess"
      ],
      "Resource": "*"
    }
  ]
}
```

Enable programatic access for this user and get AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY generated. You will also need the AWS Region where you want to set ec2 serial console access.

Set below environment variables for ansible to connect to your AWS account.

```bash
export AWS_ACCESS_KEY_ID=''
export AWS_SECRET_ACCESS_KEY=''
export AWS_DEFAULT_REGION=''
```

You may also pass the AWS credentials via other methods as referenced in Ansible AWS module documentation.

### Install dependencies

Optionally, you can install all the required dependencies using below command.

```bash
pip install -r requirements.txt
```

## Run the module

Clone this repo to your local. The module is kept inside the library folder. Use the example_playbook.yml as reference to run the module. You may modify the state to enabled|disabled to see different actions.

```yaml
---
- name: Test Playbook
  hosts: localhost
  connection: local
  tasks:
    - name: Enabling Serial Console
      ec2_serial_console:
        state: disabled
      register: r
    - name: Debugging
      debug:
        msg: "The state of the serial console for account {{ r.account_id }} is {{ r.serial_console_status }}"
```

### Run playbook

```bash
ansible-playbook example_playbook.yml
```

### View ansible doc

```bash
ansible-doc -M ./library -t module ec2_serial_console
```
