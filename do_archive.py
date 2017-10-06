# example of usage of archive tools to compress a folder and create list of files and md5 hashes.
import shutil
from archivetools import tar as tt
import os
import glob
import argparse
import logging

logger = logging.getLogger()


def mkdir_p(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def get_args():
    parser = argparse.ArgumentParser(description='Compress a whole folder and check the md5 hash of each file')

    parser.add_argument('folder_name', type=str,
                        help='Name of the folder to compress')
    parser.add_argument('source', type=str,
                        help='location of the folder in the source filesystem')
    parser.add_argument('dest', type=str,
                        help='location of the folder in the dest filesystem')
    parser.add_argument('tmp', default='~/tmp', type=str,
                        help='temporary directory (scratchpad for computing the md5 hash')
    return parser.parse_args()


def main():
    #  compress the contents of source_folder into a triad:
    #  - session.tar.xz (tar archive with the contents of the session folder)
    #  - session.mdl (csv list list of name, md5checksum of all the contents)
    #  - session.md5 (just the md5checksum of the .tar.xz archive)
    # located in tmp_folder/session

    args = get_args()

    dest_name = args.folder_name
    source_folder = os.path.abspath(os.path.join(args.source, dest_name))
    dest_folder = os.path.abspath(os.path.join(args.dest, dest_name))
    tmp_folder = os.path.abspath(os.path.join(args.tmp, dest_name))
    log_path = os.path.join(args.source, '{}_bkp.log'.format(dest_name))

    print('Will compress {}'.format(source_folder))
    print('Logging to {}'.format(log_path))

    # handler = logging.StreamHandler()
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # logger.setLevel(logging.DEBUG)
    # logger.info('logger created')
    # Create the log file
    fh = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

    mkdir_p(dest_folder)
    mkdir_p(tmp_folder)

    logger.info('Created folders, beginning compression')
    # Do the compression
    dest_file, md5_arch, md_list = tt.compress_folder(source_folder,
                                                      tmp_folder,
                                                      dest_name,
                                                      mode='w:xz')

    # check_list is a list of lists [name, md5 checksum]
    # check_ok is True if the md5checksum of all the files in the archive
    # (computed post-hoc) coincide with the ones in check_list
    check_list, check_ok = tt.check_tar_archive(dest_file, md_list)

    # Mind that all the files are read (chunked) several times,
    # hence you want to do the compression/check in a local scratchpad
    # rather than over a samba share.

    # If everything checks, move the archive from tmp to its final dest.
    assert check_ok, "There were errors compressing the file"
    logger.info('Compressed and check OK, moving to final destination')
    arc_files = glob.glob(os.path.join(tmp_folder, '*.*'))
    for f in arc_files:
        shutil.move(f, dest_folder)

    # and If dared, actually remove the uncompressed data
    #shutil.rmtree(source_folder)

if __name__ == '__main__':
    main()