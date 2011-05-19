# coding: utf-8

import os
import re
import sys
import unittest
import subprocess

import mystem

def _run_mystem(args,
                fin=subprocess.PIPE,
                fout=subprocess.PIPE,
                ferr=subprocess.PIPE,
                input_data=None):
    '''\
    Run mystem binary for tests
    '''
    return mystem.mystem(args, fin, fout, ferr, input_data)


class MystemBinaryTests(unittest.TestCase):
    '''\
    Tests for mystem binary
    '''

    def test_mystem_console_interface(self):
        '''\
        Check that mystem supports conole commands
        and returns correct statuses
        '''
        retcode, data_out, data_err = _run_mystem(["-h"])
        self.assertEqual(retcode, 0)
        self.assertEqual(data_out, "")
        self.assertNotEqual(data_err, None)
        self.assertNotEqual(data_err, "")

    def test_mystem_version(self):
        '''\
        Check mystem verion
        '''
        retcode, data_out, data_err = _run_mystem(["-h"])
        self.assertTrue('Version ' in data_err)
        v_list = re.findall(r'Version ([\d\.]+)\.', data_err)
        self.assertTrue(len(v_list) == 1)
        v_major, v_minor = [int(v) for v in v_list[0].split('.')]
        self.assertEqual(2, v_major)
        self.assertEqual(0, v_minor)

    def test_mytem_cmds(self):
        '''\
        Check that all options are supported
        '''
        retcode, data_out, data_err = _run_mystem(["-h"])
        valid_option = ['h', 'c', 'n', 'w', 'l', 'f', 's', 'i', 'g', 'e']
        for opt in valid_option:
            self.assertEqual(len(re.findall(r'    -%s' % opt, data_err)), 1)

    def tests_c_option(self):
        '''\
        Check -c option
        '''
        input_data = '<h1>Мама мыла раму</h1>'
        output_data = '<h1>Мама{мама} мыла{мыло|мыть} раму{рам|рама}</h1>\n'
        retcode, data_out, data_err = _run_mystem(["-c"], input_data=input_data)
        self.assertEqual(data_out, output_data)

    def test_n_option(self):
        '''\
        Check -n option
        '''
        input_data = '<h1>Мама мыла раму</h1>'
        output_data = 'Мама{мама}\nмыла{мыло|мыть}\nраму{рам|рама}\n'
        retcode, data_out, data_err = _run_mystem(["-n"], input_data=input_data)
        self.assertEqual(data_out, output_data)

    def test_nc_option(self):
        '''\
        Check -nc option
        '''
        input_data = '<h1>Мама мыла раму</h1>'
        output_data = '<h1>\nМама{мама}\n_\nмыла{мыло|мыть}\n_\nраму{рам|рама}\n</h1>\\n'
        retcode, data_out, data_err = _run_mystem(["-nc"], input_data=input_data)
        self.assertEqual(data_out, output_data)

    @unittest.skip("-sc i the same as -c?")
    def tets_sc_option(self):
        '''\
        Check -sc option
        '''
        self.fail("don't call")

    @unittest.skip('The behaviour of -w is unknown?')
    def test_w_option(self):
        '''\
        Check -w option
        '''
        self.fail("don't call")

    def test_l_option(self):
        '''\
        Check -l option
        '''
        input_data = '<h1>Мама мыла раму</h1>'
        output_data = '{мама}{мыло|мыть}{рам|рама}'
        retcode, data_out, data_err = _run_mystem(["-l"], input_data=input_data)
        self.assertEqual(data_out, output_data)

    def test_i_option(self):
        '''\
        Check -i option
        '''
        input_data = '<h1>Мама мыла раму</h1>'
        output_data = 'Мама{мама=S,жен,од=им,ед}мыла{мыть=V,несов=прош,ед,изъяв,жен,пе|мыло=S,сред,неод=им,мн|=S,сред,неод=род,ед|=S,сред,неод=вин,мн}раму{рама=S,жен,неод=вин,ед|рам=S,гео,муж,неод=дат,ед}'
        retcode, data_out, data_err = _run_mystem(["-i"], input_data=input_data)
        self.assertEqual(data_out, output_data)

    def test_gi_option(self):
        '''\
        Check -gi option
        '''
        input_data = '<h1>Мама мыла раму</h1>'
        output_data = 'Мама{мама=S,жен,од=им,ед}мыла{мыть=V,несов=прош,ед,изъяв,жен,пе|мыло=S,сред,неод=(им,мн|род,ед|вин,мн)}раму{рама=S,жен,неод=вин,ед|рам=S,гео,муж,неод=дат,ед}'
        retcode, data_out, data_err = _run_mystem(["-gi"], input_data=input_data)
        self.assertEqual(data_out, output_data)

    def test_f_option(self):
        '''\
        Check -f option
        '''
        input_data = '<h1>Мама мыла раму</h1>'
        output_data = 'Мама{мама:313.80}мыла{мыло:16.30|мыть:26.70}раму{рам:0.00|рама:22.50}'
        retcode, data_out, data_err = _run_mystem(["-f"], input_data=input_data)
        self.assertEqual(data_out, output_data)

    def test_inf_option(self):
        '''\
        Run test on dataset
        '''
        test_data_dir = os.path.join(
                           os.path.dirname(os.path.abspath(__file__)),
                           'test_data')

        input_data = open(os.path.join(test_data_dir, 'in.txt')).read()
        output_data = open(os.path.join(test_data_dir, 'out.txt')).read()

        retcode, data_out, data_err = _run_mystem(["-inf"],
                                                  input_data=input_data)
        self.assertEqual(data_out, output_data)



def suite():
    loader = unittest.TestLoader()
    return unittest.TestSuite([
        loader.loadTestsFromTestCase(MystemBinaryTests)
    ])
