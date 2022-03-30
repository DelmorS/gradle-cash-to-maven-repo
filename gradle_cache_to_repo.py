# File name: gradle_cache_to_repo.py
# Author by: ksh (sinsongdev@gmail.com)
# History: 
# [2019/05/31 11:27 AM] Created.
# [2020/12/25 10:22 AM] "Cannot create a file when that file already exists" error fix.
# [2022/03/30 07:58 PM] By Delmor_S. Replaced .gradle path with dynamic one
#
# Function: Converts .gradle cache into local maven repository.
#           This local maven repository can be used in gradle offline build directly instead of gradle cache.

from pathlib import Path
import os
from shutil import copyfile

logging = False
home = str(Path.home())

src = home + "\\.gradle\\caches\\modules-2\\files-2.1\\"
dst = "C:\\gradle_local_repo\\"

group_count = 0
artifact_count = 0

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return

def processGroup(group):
    global group_count
    group_count = group_count + 1
    group_dir = group.replace(".", "/")
    if (logging):
        print(group_dir)
    makedirs(dst + group_dir)

    artifacts = os.listdir(src + group)
    for artifact in artifacts:
        processArtifact(group, group_dir, artifact)
    return

def processArtifact(group, group_dir, artifact):
    global artifact_count
    artifact_count = artifact_count + 1
    artifact_dir = dst + group_dir + "/" + artifact
    makedirs(artifact_dir)
    if (logging):
        print(artifact)

    src_artifact_dir = src + group + "/" + artifact
    versions = os.listdir(src_artifact_dir)
    for version in versions:
        processVersion(group, artifact, artifact_dir, version)
    return

def processVersion(group, artifact, artifact_dir, version):
    version_dir = artifact_dir + "/" + version
    makedirs(version_dir)
    if (logging):
        print(version)

    src_version_dir = src + group + "/" + artifact + "/" + version
    hashs = os.listdir(src_version_dir)
    for hash in hashs:
        hash_dir = src_version_dir + "/" + hash
        files = os.listdir(hash_dir)
        
        for file in files:
            src_file_path = hash_dir + "/" + file
            dst_file_path = version_dir + "/" + file
            copyfile(src_file_path, dst_file_path)
    return

groups = os.listdir(src)
for group in groups:
    processGroup(group)

print("Done!")
print(f'Total {group_count} groups')
print(f'Total {artifact_count} artifacts')