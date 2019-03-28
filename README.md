# Nines
usage: nines.py [-h] folder match replace

Finds and replaces all instances of a user Id in a Dolphin user data folder,
file names, as well as .txts, recursively. Will only work with Alphanumeric
Characters. New folder will be named replace-new. ThisThere are three
positional arguments, and this script should be run from the directory which
contains the user folder

positional arguments:
  folder      Required Argument: Folder Name
  match       Required Argument: UserId to match and replace
  replace     Required Argument: Replacement string for match values

optional arguments:
  -h, --help  show this help message and exit

# Replacement Terms
Currently uses a regex map for search and replace terms hard coded into the script.

cases follow

        "ID:"+match: "ID:"+replace,
        "user_id:"+match: "user_id:"+replace,
        "user_ID"+match: "user_ID:"+replace,
        
        #food_log pattern uses 2 of year to avoid issues with count column
        match+"|2018" : replace+"|2018"            

Additional cases can be added via the code, or later on as a arg.
