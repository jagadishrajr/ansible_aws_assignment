#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ec2_serial_console

short_description: Modify EC2 serial console access for an account

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: Using this module, you can enable or disable EC2 serial console access. 

options:
    state:
        description: The target state of the EC2 serial console access. Must be either of 'enabled' or 'disabled'.
        required: true
        type: str

extends_documentation_fragment:
    - amazon.aws.boto3
    - amazon.aws.common.modules
    - amazon.aws.region.modules

author:
    - Jagadish Raj (@jagadishrajr)
'''

EXAMPLES = r'''
- name: Enabling Serial Console
  amazon.aws.ec2_serial_console:
    state: enabled

# fail the module
- name: Test failure of the module
  amazon.aws.ec2_serial_console:
    state: fail me
'''

RETURN = r'''
changed:
    description: Whether the original status was changed or not
    type: bool
    returned: always
    sample: true
account_id:
    description: The account id where the serial console change has taken effect.
    type: str
    returned: always
    sample: '123456789123'
serial_console_status:
    description: The current state of the seria console, enabled or disabled.
    type: str
    returned: always
    sample: 'enabled'
'''


from ansible_collections.amazon.aws.plugins.module_utils.modules import AnsibleAWSModule
try:
    import botocore
except ImportError:
    pass  # handled by AnsibleAWSModule

def change_serial_console():
    module_args = dict(
        state=dict(type='str', required=True, choices=["enabled", "disabled"]),
    )

    result = dict(
        changed=False,
        account_id='',
        serial_console_status=''
    )

    module = AnsibleAWSModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    ec2_client = module.client("ec2")
    sts_client = module.client("sts")

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    
    try: 
        caller_identity = sts_client.get_caller_identity()
        current_serial_console_access = ec2_client.get_serial_console_access_status()

        # Do not modify if the current environment state is the same as that of supplied state
        serial_console_status = "enabled" if current_serial_console_access["SerialConsoleAccessEnabled"] else "disabled"
        if (serial_console_status != module.params['state']):
            if (module.params['state'] == 'enabled'):
                current_serial_console_access = ec2_client.enable_serial_console_access()
            elif (module.params['state'] == 'disabled'):
                current_serial_console_access = ec2_client.disable_serial_console_access()
            result['changed']=True
    except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
        module.fail_json_aws("e")
    
    result['account_id'] = caller_identity["Account"]
    result['serial_console_status'] = "enabled" if current_serial_console_access["SerialConsoleAccessEnabled"] else "disabled"

    module.exit_json(**result)


def main():
    change_serial_console()


if __name__ == '__main__':
    main()
