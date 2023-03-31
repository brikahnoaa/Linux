#!/usr/bin/python3 -B
# convert .dat to .wav format
# this file just does the command line arg processing and error checks
# the dat conversion functions are in the imported module datConvert
###
import sys
from os import mkdir, listdir
from os.path import isfile, isdir, join, splitext, expanduser
from glob import glob
import argparse
import datConvert
#
me = 'dat2wav.py'
wavFmtDefault = '%Y%m%d_%H%M%S'
#
def cmdLineArgs():
  """parse command line
  rets: clargs=command line arguments namespace
  """
  parser = argparse.ArgumentParser(
    prog=me, add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="convert .DAT format to .wav format",
    epilog="examples:\n\
  python3 %s 00000000.DAT 00000001.DAT    #make 2 .wav files\n\
  python3 %s *009[89].DAT 0000010?.DAT    #make 12 .wav files\n\
  python3 %s -H headers .    #make .wav here, .hdr in a subdir\
    " % (me, me, me),
    )
  parser.add_argument('file', nargs='+',
    help="directory, files or filespecs; required")
  parser.add_argument('-n', dest='name', 
    help="prefix for output names, as name_date_time.wav")
  parser.add_argument('-d', dest='dat_dir', default='.',
    help="read .dat files from this directory; default=.")
  parser.add_argument('-h', dest='hdr_dir', 
    help="write .hdr files in this directory; default=no headers")
  parser.add_argument('-w', dest='wav_dir', default='.',
    help="write .wav files in this directory; default=.")
  parser.add_argument('--datetime', action='store_true', 
    help="print yyyymmdd_hhmmss from .dat header and exit")
  parser.add_argument('--help', action='help',
    help="print help message and exit") 
  parser.add_argument('--no-wav', action='store_true',
    help="do not create wav files (use with HDR_DIR)")
  parser.add_argument('-v', '--verbose', action='count', default=0,
    help="increase output text; default=quiet")
  #clargs = argparse.Namespace(usageStr=parser.format_usage())
  clargs = argparse.Namespace()
  parser.parse_args(namespace=clargs)
  return(clargs, parser)

def go():
  """parse cmd line, take actions
  """
  clargs, parser = cmdLineArgs()
  v = clargs.verbose
  if v>1: print(clargs)
  # name format
  wavFmt = wavFmtDefault
  if clargs.name: 
    if '%' in clargs.name:
      # % means it must be a full strftime format string
      wavFmt = clargs.name
    else:
      # must be a prefix
      wavFmt = clargs.name+'_'+wavFmt
  #[ file names: make a list of .DAT filenames 
  # works on PC or linux
  files = clargs.file
  # is the input directory not curdir?
  datD = expanduser(clargs.dat_dir)
  if not isdir(datD):
    print("%s is not a directory" % datD)
    parser.print_usage()
    exit(1)
  # expand single directory to a list of file names
  x = join(datD, files[0])
  if isdir(x):
    if len(files)==1:
      datD = x
      files = listdir(x)
    else:
      print("%s is a directory, so it should be the only argument" % x)
      print(*sys.argv)
      parser.print_help()
      exit(1)
  # add datD, expand filespecs to names using unix style glob pattern match
  x = []
  for f in files:
    # look for glob chars in filename
    if [ c for c in '*?[]' if c in f ]:
      x.extend(glob(join(datD, f)))
    else:
      x.append(join(datD, f))
  files = x
  # use filename if it exists and ends in .dat .DAT 
  files = [ x for x in files if isfile(x) and
          '.dat'==splitext(x)[1].lower() ]
  if v>1:
    print("files: ", *files)
  # must have filenames
  if len(files)<1:
    print("No dat files")
    print(*sys.argv)
    parser.print_help()
    exit(1)
  #] file names
  ## do things
  if clargs.datetime:
    # print yyyymmdd_hhmmss from .dat header and exit
    if len(files)==1:
      print(datConvert.datDateStr(files[0], wavFmt=wavFmt))
    else: 
      for f in files:
        print(f, datConvert.datDateStr(f, wavFmt=wavFmt))
    exit(0)
  # output dirs # create output dirs if needed
  hdrD = wavD = None
  if clargs.hdr_dir:
    hdrD = expanduser(clargs.hdr_dir)
    if not isdir(hdrD):
      mkdir(hdrD)
  if clargs.wav_dir and not clargs.no_wav:
    wavD = expanduser(clargs.wav_dir)
    if not isdir(wavD):
      mkdir(wavD)
  # process dat files
  if v>0:
    if datD: print("Reading dat files in %s" % datD)
    if hdrD: print("Writing hdr files in %s" % hdrD)
    if wavD: print("Writing wav files in %s" % wavD)
  for f in files:
    w = datConvert.dat2wav(f, hdrD=hdrD, wavD=wavD, wavFmt=wavFmt, v=v)
    if v>0: print(f,w)
  exit(0)

go()

### notes
# v1.0 blk works
# v1.1 refined cmdline
# v2.0 blk release
# v2.1 blk v=verbose, no overwrite more efficient
#
# os.path.join(path, abspath)->abspath  # pretty smart!
# flat_list = [item for sublist in l for item in sublist]
