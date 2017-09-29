# example of usage of archive tools to compress a folder and create list of files and md5 hashes.
import shutil
from archivetools import tar as tt
import os
import glob

import logging
logging.basicConfig(filename='backup.log', level=logging.DEBUG)
dest_name = 'B957'

source_folder = os.path.abspath(os.path.join('/home/gentnerbackup/cube_link/raw_data/', dest_name))
tmp_folder = os.path.abspath('/tmp/scratch/')
dest_folder = os.path.abspath(os.path.join('/home/gentnerbackup/archive/raw_data/ibon/', dest_name))
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)
    
if not os.path.exists(tmp_folder):
	os.makedirs(tmp_folder)
	
#  compress the contents of source_folder into a triad:
#  - session.tar.xz (tar archive with the contents of the session folder)
#  - session.mdl (csv list list of name, md5checksum of all the contents)
#  - session.md5 (just the md5checksum of the .tar.xz archive)
# located in tmp_folder/session

dest_file, md5_arch, md_list = tt.compress_folder(source_folder, tmp_folder, dest_name, mode='w:xz')

# check_list is a list of lists [name, md5 checksum]
# check_ok is True if the md5checksum of all the files in the archive
# (computed post-hoc) coincide with the ones in check_list
check_list, check_ok = tt.check_tar_archive(dest_file, md_list)

# Mind that all the files are read (chunked) several times,
# hence you want to do the compression/check in a local scratchpad
# rather than over a samba share.

# If everything checks, move the archive from tmp to its final dest.
assert (check_ok), "There were errors compressing the file"
arc_files = glob.glob(os.path.join(tmp_folder, '*.*'))
for f in arc_files:
    shutil.move(f, dest_folder)

# and If dared, actually remove the uncompressed data
#shutil.rmtree(source_folder)
