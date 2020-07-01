#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Luzilla Capital GmbH
# BSD-2-Clause license (see https://opensource.org/licenses/BSD-2-Clause)

import os.path

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec

DOCUMENTATION = '''
---
module: loki_download
short_description: Download loki, promtail, logcli, ... from Github, with a token.
'''

EXAMPLES = '''
- name: Download all the things...
  loki_download:
    name: "{{ item }}"
    version: "v1.2.0"
    github_oauth_token: "..."
  register: result
  with_items:
    - loki
    - promtail
    - logcli
'''


class LokiDownloadException(Exception):
  pass


def _get_download_path(name, version, os, arch):
  return "/tmp/%s-%s_%s-%s.zip" % (name, version, os, arch)


def _download_exists(download):
  if os.path.isfile(download):
    return True

  return False


def _github_api_headers(token):
  return {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'token %s' % (token)
  }


def _github_release_url(version):
  return "https://api.github.com/repos/%s/%s/releases/tags/%s" % ("grafana", "loki", version)


def _github_release_zip(module, version, headers):
  r, info = fetch_url(module, _github_release_url(params['version']), headers=headers, method='GET')
  if info['status'] == 200:
      try:
          release = json.loads(to_text(r.read()))
          return settings['zipball_url']
      except UnicodeError as e:
          raise LokiDownloadException('Unable to decode version string to Unicode')
      except Exception as e:
          raise LokiDownloadException(e)
  else:
      raise LokiDownloadException('Unable to get the release, HTTP status: %s' % info)


def loki_download_present(module, params):
  download = _get_download_path(params['name'], params['version'], params['os'], params['arch'])
  if _download_exists(download):
    return False, {'path': download}

  headers = _github_api_headers(params['github_oauth_token'])

  # get the release
  asset_url = _github_release_zip(module, params['version'], headers)

  r, info = fetch_url(module, asset_url, headers=headers, method='GET')
  if info['status'] != 200:
    raise LokiDownloadException('Could not download release: %s' % info)

  with open(download, 'w+') as f:
    f.write(r.read())

  return True, {
    'name': params['name'],
    'path': download,
    'version': params['version']
  }


def loki_download_absent(module, params):
  download = _get_download_path(params['name'], params['version'], params['os'], params['arch'])
  if _download_exists(download) is False
    return False, {}

  os.remove(download)
  return True, {}


def main():
  choice_map = {
    "present": loki_download_present,
    "absent": loki_download_absent, 
  }

  fields = {
    "name": {"required": True, "type": "str" },
    "version": {"required": True},
    "os": {"default": "linux", "required": True, "type": "str"},
    "arch": {"default": "amd64", "required": True, "type": "str"},
    "github_oauth_token": {"required": True, "type": "str"},
    "state": {
      "default": "present", 
      "choices": ['present', 'absent'],  
      "type": 'str' 
    },
	}

  module = AnsibleModule(argument_spec=fields)

  has_changed, result = choice_map.get(module.params['state'])(module, module.params)
  module.exit_json(changed=has_changed, meta=result)

if __name__ == '__main__':
    main()
