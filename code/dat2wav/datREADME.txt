The files dat2wav.py and datConvert.py are python code text files to create
WAV format files from the DAT format files produced by NOAA PMEL HaruPhone
(hydrophones using CF2 hardware). The conversion routines are in datConvert.py
and the dat2wav.py code manages the user command line. Either code file is 
suited to modification for other uses.

Python3 is cross-platform; this code has been tested on Redhat Linux and
Windows10 but is expected to run on other flavors of linux or Apple OSX.
To install python3 on windows, open a cmd.exe window and enter python3.
Windows10 will open a microsoft store download page if it is not installed.
On Redhat Linux the install command is   yum install python3

The output from   python3 dat2wav.py --help is shown below.
To convert all the .dat or .DAT files in the current directory to .wav, do
  python3 dat2wav.py *.*

usage: dat2wav.py [-h] [-n NAME] [-D DAT_DIR] [-H HDR_DIR] [-W WAV_DIR]
                  [--datetime] [--no-wav] [-v]
                  file [file ...]

convert .DAT format to .wav format

positional arguments:
  file                  directory, files or filespecs; required

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  prefix for output names, as name_date_time.wav
  -D DAT_DIR, --dat-dir DAT_DIR
                        read .dat files from this directory; default=.
  -H HDR_DIR, --hdr-dir HDR_DIR
                        write .hdr files in this directory; default=no headers
  -W WAV_DIR, --wav-dir WAV_DIR
                        write .wav files in this directory; default=.
  --datetime            print yyyymmdd_hhmmss from .dat header and exit
  --no-wav              do not create wav files (use with --hdr-dir)
  -v, --verbose         increase output text; default=quiet

examples:
  python3 dat2wav.py 00000000.DAT 00000001.DAT    #make 2 .wav files
  python3 dat2wav.py *009[89].DAT 0000010?.DAT    #make 12 .wav files
  python3 dat2wav.py -H headers .    #make .wav here, .hdr in a subdir

advanced hints:
.1 a four hour 138MB .DAT file takes 30 seconds to convert on a low end PC
.2 if the .wav file exists already it is skipped, so converting a lot of files
   will continue if interrupted and restarted
.3 default action is to just make .wav files, but the DAT headers are saved
   if the HDR directory is specified with --hdr-dir option
.4 a DAT file can be recreated from a WAV and a HDR (with the same base name)
.5 --name option is a prefix to the wav filenames, or a complete name spec
   if the NAME argument includes date/time %format (see linux, man date)
