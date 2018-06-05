# MiniBioKit
A mini Biochemistry toolkit developed in Python 3 with some degree of Python 2 compatibility.

Originally developed to provide some aid in primer design, it provide more functionalities that may eventually become a general purpose library.

Currently under active development.

Major modules:

 - BioChemTool: Collection of utilities to deal with different file formats
  - commonUtil: Utilities to define some data types for easier processing through other utils.

 - BioChemData:
  - Nucleotide: Provide functionalities for nucleotide sequence processing
  - Protein: Provide functionalities for peptide sequence processing

## File Format Compatibility

The most commonly used format in this library is the so-called "PSV" file.

PSV file is a dialect of CSV that use Pipe "|" as the separator. As the pipe
symbol does not commonly appear in data, it can save a lot of hassle when dealing
with quotations and escape sequences.

The special point regarding the PSV processor here is that it would treat all lines
starting with a pound/hash "#" symbol as comment. This design would allow users to
include some comments as well as headers to the data without messing up with data.
