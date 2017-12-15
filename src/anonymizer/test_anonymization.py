'''
Created on Dec 14, 2017

@author: paepcke
'''
from tempfile import NamedTemporaryFile
import unittest

from anonymize_txt import TextScrubber
from anonymize_csv import CSVScrubber


TEST_ALL = True
#TEST_ALL = False

class TestAnonymization(unittest.TestCase):

    #-----------------------------
    # setUp 
    #-----------------------    
    
    def setUp(self):
        '''
        Before each test.
        '''
        unittest.TestCase.setUp(self)
        self.txt_tst_lines = self.create_txt_test_file()
        self.csv_tst_lines = self.create_csv_test_file()

        self.tst_outfile_fd = NamedTemporaryFile(prefix='anonymization_tst',
                                                 suffix='.txt',
                                                 dir='/tmp',
                                                 delete=True)
        
    #-----------------------------
    # testTxt
    #-----------------------    

    @unittest.skipIf(not TEST_ALL, "Temporarily disabled")
    def testTxt(self):
        anonymizer = TextScrubber(self.tst_txt_infile, self.tst_outfile_fd.name)
        anonymizer.anonymize()
        
        truth = iter(self.redacted_lines_txt)
        for redacted_line in self.tst_outfile_fd:
            #print(redacted_line)
            self.assertEqual(redacted_line.rstrip(), truth.next())

    #-----------------------------
    # testCsvAllColumns
    #-----------------------    

    @unittest.skipIf(not TEST_ALL, "Temporarily disabled")
    def testCsvAllColumns(self):
        anonymizer = CSVScrubber(self.tst_csv_infile, self.tst_outfile_fd.name)
        anonymizer.anonymize()
        
        truth = iter(self.redacted_lines_all_columns_csv)
        for redacted_row in self.tst_outfile_fd:
            #print(redacted_row.rstrip())
            self.assertEqual(redacted_row.rstrip(), truth.next())

    #-----------------------------
    # testCsvAllNotAllColumns
    #-----------------------    

    @unittest.skipIf(not TEST_ALL, "Temporarily disabled")
    def testCsvNotAllColumns(self):
        anonymizer = CSVScrubber(self.tst_csv_infile, 
                                 self.tst_outfile_fd.name,
                                 ignore_cols=[0])
        anonymizer.anonymize()
        
        truth = iter(self.redacted_lines_not_column_0_csv)
        for redacted_row in self.tst_outfile_fd:
            #print(redacted_row.rstrip())
            self.assertEqual(redacted_row.rstrip(), truth.next())

    #--------------------------- Utilities ---------------------
    
    #-----------------------------
    # create_txt_test_file
    #-----------------------    
      
    def create_txt_test_file(self):
        
        lines_txt = [
                      'First line',
                      'A zipcode is 94025',
                      'A zip+4 is 94025-3412',
                      'A US phone number is 650-327-7398',
                      'A German phone number is 049-721-1234567',
                      'An Indian phone number is 011-91-1234567890',
                      'An email address foo@gmail.com'
                      ]

        self.redacted_lines_txt = [
                                    'First line',
                                    'A zipcode is <zipRedac>',
                                    'A zip+4 is <zipRedac>',
                                    'A US phone number is <phoneRedac>',
                                    'A German phone number is 049-<phoneRedac>567',
                                    'An Indian phone number is 011-91-1<phoneRedac>90',
                                    'An email address <emailRedac>'
                                    ]

        
        self.tst_txt_infile = 'tst_file_txt.txt'
        
        with open(self.tst_txt_infile, 'w') as fd:
            for line in lines_txt:
                fd.write(line + '\n')
            fd.close()
                    
        return lines_txt
            
    #-----------------------------
    # create_csv_test_file
    #-----------------------    
      
    def create_csv_test_file(self):
        
        lines_csv = [
                      'First 94025 line,94025,last column', 
                      'First line,A zip+4 is 94025-3412,last column',
                      '650-327-7398,A US phone number is 650-327-7398,last 650-327-7398 column',
                      'First line,A German phone number is 049-721-1234567,last column',
                      'First line,An Indian phone number is 011-91-1234567890,last column',
                      'First line,An email address foo@gmail.com,last john.doe@stanford.edu'
                      ]

        self.redacted_lines_all_columns_csv = [
                      'First <zipRedac> line,<zipRedac>,last column',
                      'First line,A zip+4 is <zipRedac>,last column',
                      '<phoneRedac>,A US phone number is <phoneRedac>,last <phoneRedac> column',
                      'First line,A German phone number is 049-<phoneRedac>567,last column',
                      'First line,An Indian phone number is 011-91-1<phoneRedac>90,last column',
                      'First line,An email address <emailRedac> ,last <emailRedac>'
                      ]

        self.redacted_lines_not_column_0_csv = [
                      'First 94025 line,<zipRedac>,last column',
                      'First line,A zip+4 is <zipRedac>,last column',
                      '650-327-7398,A US phone number is <phoneRedac>,last <phoneRedac> column',
                      'First line,A German phone number is 049-<phoneRedac>567,last column',
                      'First line,An Indian phone number is 011-91-1<phoneRedac>90,last column',
                      'First line,An email address <emailRedac> ,last <emailRedac>'
                      ]
        
        self.redacted_lines_not_column_0And2_csv = [
                      'First 94025 line,<zipRedac>,last column',
                      'First line,A zip+4 is <zipRedac>,last column',
                      '650-327-7398,A US phone number is 650-327-7398,last 650-327-7398 column',
                      'First line,A German phone number is 049-<phoneRedac>567,last column',
                      'First line,An Indian phone number is 011-91-1<phoneRedac>90,last column',
                      'First line,An email address <emailRedac>,last john.doe@stanford.edu'
                      ]
        
        
        self.tst_csv_infile = 'tst_file_csv.txt'
        
        with open(self.tst_csv_infile, 'w') as fd:
            for line in lines_csv:
                fd.write(line + '\n')
            fd.close()
                    
        return lines_csv
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()