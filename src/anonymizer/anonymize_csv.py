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

import csv
from datetime import datetime
import os
import re
import sys


class CSVScrubber(object):
    '''
    Given a .csv file, scrubs it clean of identifying information 
    including  zip codes, phone numbers, and email addresses. 
    Writes output to new csv file.
    '''


    def __init__(self, input_file, output_file):

        self.infile_name = input_file
        self.outfile_name = output_file

        # columns to ignore when scrubbing
        self.ignore_cols = set([1, 2])


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

    def prune_numbers(self, text):
        '''
        Prunes phone numbers from a given string and returns the string with
        phone numbers replaced by <phoneRedac>

        :param text: text field
        :type text: String
        :returns: text with all phone number-like substrings replaced by <phoneRedac>
        :rtype: String
        '''
        #re from stackoverflow. seems to do an awesome job at capturing all phone nos :)
        s = '((?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?)'
        match = re.findall(s, text)
        for phoneMatchHit in match:
            text = text.replace(phoneMatchHit[0],"<phoneRedac>")
        return text

    def prune_zipcode(self, text):
        '''
        Prunes the zipcodes from a given string and returns the string with zipcode
        replaced by <zipRedac>.

        :param text: text field
        :type text: String
        :returns: text with all zipcode substrings replaced by <zipRedac>
        :rtype: String
        '''
        s = '\d{5}(?:[-\s]\d{4})?'
        match = re.findall(s, text)
        for zipcodeMatchHit in match:
            text = text.replace(zipcodeMatchHit,"<zipRedac>")
        return text

    def prune_emails(self, text):
        '''
        Prunes email addresses from a given string and returns the string with emails
        replaced by <emailRedac>.

        :param text: text field
        :type text: String
        :returns: text with all email substrings replaced by <emailRedac>
        :rtype: String
        '''

        # Pattern for email id - strings of alphabets/numbers/dots/hyphens followed
        # by an @ or at followed by combinations of dot/. followed by the edu/com
        # also, allow for spaces
        emailPattern = '(.*)\s+([a-zA-Z0-9\(\.\-]+)[@]([a-zA-Z0-9\.]+)(.)(edu|com)\\s*(.*)'
        #emailPattern='(.*)\\s+([a-zA-Z0-9\\.]+)\\s*(\\(f.*b.*)?(@)\\s*([a-zA-Z0-9\\.\\s;]+)\\s*(\\.)\\s*(edu|com)\\s+(.*)'
        compiledEmailPattern = re.compile(emailPattern);

        if compiledEmailPattern.match(text) is not None:
            #print 'BODY before EMAIL STRIPING %posterNamePart \n'%(body);
            match = re.findall(emailPattern, text)
            new_text = " "
            for emailMatchHit in match:
                new_text += emailMatchHit[0] + " <emailRedac> " + emailMatchHit[-1] 
                #print 'NEW BODY AFTER EMAIL STRIPING %posterNamePart \n'%(new_body);
            return new_text

        return text

    def trimnames(self, text):
        '''
        Removes all person names from the given string. We currently return the text 
        unchanged, because we found that too many names match regular English words.
        :param text: text field
        :type text: String
        :returns: text with all name substrings replaced by <nameRedac>
        :rtype: String
        '''
        return text

    def anonymize_text(self, text):
        '''
        Anonymize text. The following is done:
            - Anything that looks like a phone number is replaced by <phoneRedac>
            - Anything that looks like a zipcode is replaced by <zipRedac>
            - Occurrence of email addresses are replaced by <emailRedac>
        :param text: text field
        :type text: String
        '''

        text = self.prune_numbers(text)
        text = self.prune_zipcode(text)
        text = self.prune_emails(text)

        # Trim names from post. This method currently does nothing, b/c
        # some of the names people give are very common English words. 
        # (Implementation removes too much)
        text = self.trimnames(text)

        return text


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print('Please pass both input and output csv file names')
        sys.exit()

    # ignores parameters after first two
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    scrubber = CSVScrubber(input_file, output_file)
    scrubber.anonymize()