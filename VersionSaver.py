import os, pathlib, time, shutil

'''
Written by:     Chad Curkendall
Use:            Specifiy the file(s) to be archived in the DefaultFiles.txt file in this same directory
'''


def _archive_exists(path):
    '''
    Checks whether path\archive exists
    '''
    
    # Force path to be a pathlib.Path object:
    path = pathlib.Path( str(path) )
    
    # Set path to folder if it points to a file
    if path.is_file():
        path = pathlib.Path( str(path.resolve().parent) )
    
    # Check whether an achive folder exists:
    if 'archive' in os.listdir( str(path) ):
        return True
    else:
        return False
        

def _create_archive(path):
    '''
    Creates path\archive
    '''
    # Force path to be a pathlib.Path object:
    path = pathlib.Path( str(path), 'archive' )
    os.mkdir( str(path) )

def _get_date_string():
    # Get the current time info:
    year, month, day, hour, min, sec = time.localtime()[0:6]
    
    # Convert numbers <10 from # to 0# and return a string
    def dbl_dgt(num):
        if num <= 9:
            num = '0' + str(num)
        return num
    month   = dbl_dgt(month)
    day     = dbl_dgt(day)
    hour    = dbl_dgt(hour)
    min     = dbl_dgt(min)
    sec     = dbl_dgt(sec)
    return '{0}-{1}-{2} - {3}.{4}.{5} - '.format(year, month, day, hour, min, sec)
    

def archive_file(file = None):
    # The assumption here is that the time stamp is unique for each 
    # call to this function, otherwise there will be filename collisions
    
    if file == None:
        raise Exception("No file specified")
        return
    

    # Target File to archive:
    filePath = pathlib.Path(file)
    
    # Assert the file exists:
    if not filePath.exists():
        raise Exception("{0}\ndoes not exist").format(str(filePath))
    
    # Assert .\archive exists:
    if not _archive_exists(filePath.parent):
        _create_archive(filePath.parent)
    
    # Path Construction:
    sourceFile = filePath
    destFile = pathlib.Path(str(filePath.parent), 'archive')
    
    # Copy file to archive (.copy2 retains metadata):
    shutil.copy2(str(sourceFile), str(destFile))
    
    # Rename archived file with date stamp:
    os.rename(  str(pathlib.Path(str(destFile), filePath.name)), 
                str(pathlib.Path(str(destFile), _get_date_string() + filePath.name)))
    
def create_defaults(defaults):
    '''
    Create the DefaultFiles.txt to populate with files to archive
    '''
    defaults.touch()
    comment = '# This is a comment in the data file\n'
    rootDir = '\\path\\to\\some\\directory\n'
    filesToArchive = '\tSomeFileToArchive.ftw\n'
    pathlib.Path(str(defaults.parent), 'SomeFileToArchive.ftw').touch()
    defaults.write_text(comment + rootDir + filesToArchive)

def get_defaults():
    defaults = pathlib.Path(str(pathlib.Path.cwd()), 'DefaultFiles.txt')
    
    # archive_file(defaults)
    if not defaults.exists():
        create_defaults(defaults)






    

if __name__ == '__main__':
    
    # This is where the routine should read from a data file to get the 
    # file names to archive. -> get_defaults()
    
    filenames = {'SearchViewController.py'}

    for name in filenames:
        file = pathlib.Path(str(pathlib.Path.cwd()), 'src', name)
        if file.exists():
            archive_file(file)
        
#     # archive_file(defaults)
#     if not defaults.exists():
#         pass
    
    
#     pass
    

# #
#   Original Code:
#
    # # Get the current time info:
    # curtime = time.localtime()
    # year = curtime[0]
    # month = curtime[1]
    # day = curtime[2]
    # hour = curtime[3]
    # min = curtime[4]
    # sec = curtime[5]
    # 
    # # Create the date string to prefix to the archived file:
    # dateStr = '{0}-{1}-{2} - {3}.{4}.{5} - '.format(year, month, day, hour, min, sec)

   ##   # Target File to archive:
    # CDS_CurrentProjects = r'Current projects.cds'
    # 
    # # File Locations:
    # domain_settings = pathlib.Path(r'\\Esm8\engr\Program Files\Oasys\DomainSettings')
    # archive = pathlib.Path(str(domain_settings), 'archive')
    # 
    # # Path Construction:
    # sourceFile = pathlib.Path(str(domain_settings), CDS_CurrentProjects)
    # destFile = pathlib.Path(str(archive))
    # 
    # # Copy file to archive (.copy2 retains metadata):
    # shutil.copy2(str(sourceFile), str(destFile))
    # 
    # # Rename file with date:
    # os.rename(  str(pathlib.Path(str(destFile), CDS_CurrentProjects)), 
    #             str(pathlib.Path(str(destFile), dateStr + CDS_CurrentProjects)))
    # 