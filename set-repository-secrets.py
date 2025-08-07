#!/usr/bin/env python3


from peaklib import secrets
from pathlib import Path
import os


def set_github_token():
    token = secrets.load_secret('github-token-1')['value']
    os.system(f'gh secret set GH_PAT --body "{token}"')


def set_macbook_air_ssh_keys():
    private_key_fp = '~/.ssh/id_rsa'
    public_key_fp = '~/.ssh/id_rsa.pub'
    # assert Path(public_key_fp).exists()
    # assert Path(private_key_fp).exists()
    os.system(f"""gh secret set MACBOOK_AIR_PVK < {private_key_fp}""")
    os.system(f"""gh secret set MACBOOK_AIR_PK < {public_key_fp}""")


def set_pyramid_host_ip():
    ip_address = secrets.load_secret('server-us-west-4')['host']
    os.system(f"""gh secret set PYRAMID_HOST_IP --body '{ip_address}'""")


def set_surry_secrets():
    fp = secrets.get_secrets_files_from_env()
    assert Path(fp).exists()
    os.system(f"""gh secret set SURRY_SECRETS < {fp}""")


def main():
    set_github_token()
    # set_pyramid_host_ip()
    # set_macbook_air_ssh_keys()
    # set_surry_secrets()


if __name__ == "__main__":
    main()


