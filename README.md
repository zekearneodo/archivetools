# archivetools
Scripts and functions to archive and keep track of data

Typically:

check_list, check_ok = compress_folder(source_folder, tmp_folder, dest_name, mode='w:xz')

compresses the contents of source_folder into a triad:

- dest_name.tar.xz (tar archive with the contents of the source_folder)
- dest_name.mdl (csv list list of name, md5checksum of all the contents)
- dest_name.md5 (just the md5checksum of the .tar.xz archive)

return values:

- check_list: list of lists [name, md5 checksum]
- check_ok is: True if the md5checksum of all the files in the archive (computed post-hoc) coincide with the ones in check_list
