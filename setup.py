#!/usr/bin/python
from distutils.core import setup

if __name__ == "__main__":
   setup(
       name="nfs-diag" ,
       version="1.0",
       author="Matthew Mowens",
       author_email="mowens@redhat.com",
       url="",
       description='''
         Script finds NFS servers to run tcpdump on. By default the script runs in 
         manual mode allowing the user to select which server the user would like
         to run on. All output of script will be archived and stored in users current
         directory.''',
       license="GPLv2",
       packages=[],
       scripts=["nfs-diag"],
       package_dir={"":"lib",}
   )
