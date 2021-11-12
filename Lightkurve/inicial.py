from lightkurve import search_targetpixelfile

pixelfile = search_targetpixelfile("KIC 8462852", quarter=16).download();