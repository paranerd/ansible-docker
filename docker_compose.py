#!/usr/bin/python

import subprocess
from ansible.module_utils.basic import AnsibleModule

def is_running(project_src):
  try:
    cmd = 'docker compose ps --services'
    result = subprocess.run([cmd], shell=True, check=True, capture_output=True, cwd=project_src)
    return result.stdout.decode('utf-8').strip() != ''
  except subprocess.CalledProcessError as err:
    raise Exception('Error dumping: {} STDOUT: {})'.format(err.stderr.decode('utf-8'), err.stdout.decode('utf-8'))) from err
  
def start(project_src):
  try:
    cmd = 'docker compose up -d'
    result = subprocess.run([cmd], shell=True, check=True, capture_output=True, cwd=project_src)
    return result.stdout.decode('utf-8')
  except subprocess.CalledProcessError as err:
    raise Exception('Error dumping: {} STDOUT: {})'.format(err.stderr.decode('utf-8'), err.stdout.decode('utf-8'))) from err
  
def stop(project_src):
  try:
    cmd = 'docker compose down'
    result = subprocess.run([cmd], shell=True, check=True, capture_output=True, cwd=project_src)
    return result.stdout.decode('utf-8')
  except subprocess.CalledProcessError as err:
    raise Exception('Error dumping: {} STDOUT: {})'.format(err.stderr.decode('utf-8'), err.stdout.decode('utf-8'))) from err

def main():
  module_args = dict(
    project_src=dict(type='str', required=True),
    state=dict(type='str', required=False, default='present', choices=['present', 'absent'])
  )

  result = dict(
    changed=False,
    message=''
  )

  module = AnsibleModule(argument_spec=module_args)

  try:
    running = is_running(module.params['project_src'])

    if module.params['state'] == 'present' and not running:
      start(module.params['project_src'])
      result['changed'] = True
    elif module.params['state'] == 'absent' and running:
      stop(module.params['project_src'])
      result['changed'] = True

    module.exit_json(**result)
  except Exception as err:
    module.fail_json(msg=err, **result)


if __name__ == '__main__':
  main()
