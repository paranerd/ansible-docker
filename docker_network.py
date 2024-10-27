#!/usr/bin/python

import subprocess
from ansible.module_utils.basic import AnsibleModule

def exists(name):
  try:
    cmd = 'docker network ls -f name={} --format json'.format(name)
    result = subprocess.run([cmd], shell=True, check=True, capture_output=True)
    return result.stdout.decode('utf-8').strip() != ''
  except subprocess.CalledProcessError as err:
    raise Exception('Error dumping: {} STDOUT: {})'.format(err.stderr.decode('utf-8'), err.stdout.decode('utf-8'))) from err
  
def create(name, subnet=None):
  try:
    subnet_arg = '--subnet {}'.format(subnet) if subnet else ''
    cmd = 'docker network create {} {}'.format(subnet_arg, name)
    result = subprocess.run([cmd], shell=True, check=True, capture_output=True)
    return result.stdout.decode('utf-8')
  except subprocess.CalledProcessError as err:
    raise Exception('Error dumping: {} STDOUT: {})'.format(err.stderr.decode('utf-8'), err.stdout.decode('utf-8'))) from err
  
def remove(name):
  try:
    cmd = 'docker network rm {}'.format(name)
    result = subprocess.run([cmd], shell=True, check=True, capture_output=True)
    return result.stdout.decode('utf-8')
  except subprocess.CalledProcessError as err:
    raise Exception('Error dumping: {} STDOUT: {})'.format(err.stderr.decode('utf-8'), err.stdout.decode('utf-8'))) from err

def main():
  module_args = dict(
    name=dict(type='str', required=True),
    subnet=dict(type='str', required=False, default=None),
    state=dict(type='str', required=False, default='present', choices=['present', 'absent'])
  )

  result = dict(
    changed=False,
    message=''
  )

  module = AnsibleModule(argument_spec=module_args)

  try:
    does_exist = exists(module.params['name'])

    if module.params['state'] == 'present' and not does_exist:
      create(module.params['name'], module.params['subnet'])
      result['changed'] = True
    elif module.params['state'] == 'absent' and does_exist:
      remove(module.params['name'])
      result['changed'] = True

    module.exit_json(**result)
  except Exception as err:
    module.fail_json(msg=err, **result)


if __name__ == '__main__':
  main()
