#!/usr/bin/env python

# Copyright (c) 2014, Stanford University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import csv
import os
import sys

from anonymize_txt import TextScrubber


class CSVScrubber(TextScrubber):
    '''
    Given a .csv file, scrubs it clean of identifying information 
    including  zip codes, phone numbers, and email addresses. 
    Writes output to new csv file.
    '''


    def __init__(self, input_file=None, output_file=None, ignore_cols=[]):
        
        TextScrubber.__init__(self, input_file, output_file)

        # Columns to ignore when scrubbing
        self.ignore_cols = set(ignore_cols)


    def anonymize(self):
        '''
        Do the actual work. We don't call this method from __init__()
        so that unittests can create a CSVScrubber instance without
        doing the actual work. Instead, unittests call individual methods.
        '''

        with open(self.infile_name, 'rU') as infile:
            with open(self.outfile_name, 'w') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                for row in reader:
                    row = [self.anonymize_text(t) if i not in self.ignore_cols else t for i, t in enumerate(row)]
                    writer.writerow(row)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--infile',
                        action='store',
                        help="File containing text to scrub; default is STDIN",
                        default=None
                        )
    parser.add_argument('-o', '--outfile',
                        action='store',
                        help="File to which scrubbed content is to be written; default is STDOUT",
                        default=None
                        )
    parser.add_argument('-c', '--ignorecol',
                        action='store',
                        nargs='*',
                        help="Use this option for each CSV column to ignore (origin 1); default: scrub all columns.",
                        default=[]
                        )
    
    args = parser.parse_args();

    scrubber = CSVScrubber(input_file=args.infile, output_file=args.outfile, ignore_cols=args.ignorecol)
    scrubber.anonymize()