# INSTALL
run on Centos8 or Fedora 30-32:
```shell
dnf copr enable vorona/aliyun-python-sdk
dnf install python3-ansible_alicloud
```

# BUILD
On any COPR do `New build` and paste urls to `From URLs`:
```text
# added provides python3dist(aliyun-python-sdk-core-v3)
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-core/python-aliyun-python-sdk-core.spec

# aliyun-python-sdk-core Requires python3dist(jmespath) < 1.0.0 and python3dist(jmespath) >= 0.9.3
# C8 contains only v0.9.0, Fedora ok with v0.9.4
# it is 0.10.0 version:
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/jmespath/python-jmespath.spec

# added BuildRequires:  gcc for Fedora
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/pycryptodome/python-pycryptodome.spec


https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-alidns/python-aliyun-python-sdk-alidns.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-ecs/python-aliyun-python-sdk-ecs.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-ess/python-aliyun-python-sdk-ess.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-kms/python-aliyun-python-sdk-kms.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-market/python-aliyun-python-sdk-market.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-oos/python-aliyun-python-sdk-oos.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-ram/python-aliyun-python-sdk-ram.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-rds/python-aliyun-python-sdk-rds.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-ros/python-aliyun-python-sdk-ros.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-slb/python-aliyun-python-sdk-slb.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-sts/python-aliyun-python-sdk-sts.spec
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-aliyun-python-sdk-vpc/python-aliyun-python-sdk-vpc.spec


# deleted tests and debugpkg
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/crcmod/python-crcmod.spec

# deleted tests and fixed setup.py
https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/oss2/python-oss2.spec

https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/footmark/python-footmark.spec

https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/master/python-ansible_alicloud/python-ansible_alicloud.spec
```

Rebuild broken builds.