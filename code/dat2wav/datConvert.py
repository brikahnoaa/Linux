#! python3
# functions to translate between .dat and .wav formats
# see notes at end of file
###
import os
import wave
from datetime import timedelta, datetime
from struct import unpack_from, pack_into
# 
wavFmtDefault='%Y%m%d_%H%M%S'
#
def datDatetime(datH, round=True):
  """ extract date and time from dat header
  uses: datHdr:bytes, round=bool (else truncate)
  rets: datetime
  """
  # dat file year is after 1900, so 114 means 2014
  datYear=int( unpack_from("3s", datH, 90)[0] )+1900
  datDayOfYear=int( unpack_from("3s", datH, 94)[0] )
  # 1<=dayOfYear<=365, so convert to date as year/Jan/1 + dayOfYear
  datDT=datetime(datYear, 1, 1) 
  datDT+=timedelta(days=datDayOfYear-1)
  # "hour:minute:second:milli" 
  # unpack, split, map to int; add timedelta
  h, m, s, u=map(int, unpack_from("12s", datH, 98)[0].split(b':'))
  datDT+=timedelta(hours=h, minutes=m, seconds=s, microseconds=u*1000)
  if round: # round to nearest second
    datDT+=timedelta(seconds=0.5)
  return datDT
#
def dat2wav(datF, hdrD=None, wavD=None, wavFmt=wavFmtDefault, v=0):
  """ convert .dat file to .wav file and .hdr file in curdir
  read dat header, dat data; hdr datetime; convert data; save [.hdr] .wav
  note: does not overwrite existing files
  glob: wavFmtDefault=yyyymmdd_hhmmss
  uses: datF=filename of input dat file
  rets: wavF
  outs: datetime.wav, datetime.hdr
  """
  datHdrSz=256
  datSampRate=5000
  # small header, large data
  with open(datF, "rb") as f:
    datH=f.read(datHdrSz)
    outF=datDatetime(datH).strftime(wavFmt)
    if hdrD:
      # save .hdr 
      hdrName = os.path.join(hdrD, outF+".hdr")
      if os.path.isfile(hdrName): # do not overwrite
        if v>0: print(hdrName, "exists, no overwrite")
      else:
        with open(hdrName, "wb") as h:
          h.write(datH) 
    if wavD:
      # rest of file is data
      wavName = os.path.join(wavD, outF+".wav")
      if os.path.isfile(wavName): # do not overwrite
        if v>0: print(wavName, "exists, no overwrite")
        return("")
      if v>1: print("reading")
      data=bytearray(f.read())
      ## 2do: QC: expect 1 channel, 16 bit data; unsigned big-endian
      # convert data: 16bit unsigned bigend -> 16bit signed little
      if v>1: print("converting")
      for i in range(0, len(data), 2):
        x=unpack_from(">H", data, i)[0]-32768
        pack_into("<h", data, i, x)
      ## datChannels=unpack_from(">H", datH, 194)[0]
      if v>1: print("writing")
      with wave.open(wavName, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(datSampRate)
        w.writeframes(data)
  return(outF)
#
def wav2dat(wavF, datF):
  """ convert .wav file + .hdr file to .dat file
  read .hdr, .wav data; convert data.
  uses: wav hdr [path]file, dat [path]file
  outs: datF.dat
  reqs: .hdr matching .wav in curdir or subdir "hdr"
  """
  wavHdrSz=44
  # validate
  # look for hdr locally or in subdir "hdr"
  curD=os.curdir
  with open(wavF+'.hdr', "rb") as f:
    datH=f.read()
  with open(wavF+'.wav', "rb") as f:
    f.seek(wavHdrSz)
    data=bytearray(f.read())
  # convert data: 16bit signed little -> 16bit unsigned bigend
  for i in range(0, len(data), 2):
    x=unpack_from("<h", data, i)[0]+32768
    pack_into(">H", data, i, x)
  # save dat
  with open(datF+".dat", "wb") as f:
    f.write(datH)
    f.write(data)
#
def datDateStr(path, wavFmt=wavFmtDefault):
  """date and time of a DAT file
  path=datFilename.DAT
  glob wavFmt=yyyymmdd_hhmmss
  """
  datHdrSz=256
  with open(path, "rb") as f:
    datH=f.read(datHdrSz)
  return datDatetime(datH).strftime(wavFmt)
#
###
# notes
# v1.0 blk works
# v1.1 refined cmdline
# v2.0 blk release
# v2.1 blk v=verbose, no overwrite more efficient
#
# This code uses the date, time from DAT header (v3)
# all NRS data have samprate of (about) 5000, 16bit 0-2.5volt
# most of the hdr is ignored, this is why we save hdr separate
# NRS data has a bad value (2) for channels from 2014-2015
# 
