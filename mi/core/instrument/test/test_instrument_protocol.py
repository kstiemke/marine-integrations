#!/usr/bin/env python

"""
@package mi.core.instrument.test.test_instrument_protocol
@file mi/core/instrument/test/test_instrument_protocol.py
@author Steve Foley
@brief Test cases for the base instrument protocol module
"""

__author__ = 'Steve Foley'
__license__ = 'Apache 2.0'

import logging
from nose.plugins.attrib import attr
from mi.core.log import get_logger ; log = get_logger()
from mi.core.instrument.instrument_protocol import InstrumentProtocol
#from mi.core.instrument.data_particle import DataParticle
from mi.instrument.satlantic.par_ser_600m.driver import SAMPLE_REGEX
from mi.instrument.satlantic.par_ser_600m.driver import SatlanticPARDataParticle
from pyon.util.unit_test import IonUnitTestCase
from mi.core.exceptions import InstrumentParameterException

@attr('UNIT', group='mi')
class TestUnitInstrumentProtocol(IonUnitTestCase):
    """
    Test cases for instrument protocol class. Functions in this class provide
    instrument protocol unit tests and provide a tutorial on use of
    the protocol interface.
    """ 
    def setUp(self):
        """
        """
        self.callback_result = None
        
        def protocol_callback(self, arg):
            callback_result = arg
            
        self.protocol = InstrumentProtocol(protocol_callback)
    
    def test_extraction(self):
        sample_line = "SATPAR0229,10.01,2206748544,234"
        result = self.protocol._extract_sample(SatlanticPARDataParticle,
                                               SAMPLE_REGEX,
                                               sample_line,
                                               publish=False)
    
        self.assertTrue(result['parsed'])
        self.assertTrue(result['raw'])

        # Test the format of the result in the individual driver tests. Here,
        # just tests that the result is there.
        
    def test_publish_raw(self):
        """
        Tests to see if raw data is appropriately published back out to
        the InstrumentAgent via the event callback.
        """
        # build a packet
        # have it published by the protocol (force state if needed)
        # delay?
        # catch it in the  callback
        # confirm it came back
        # compare response to original packet
        
        self.assertTrue(False)
    
    def test_publish_parsed_data(self):
        """
        Tests to see if parsed data is appropriately published back to the
        InstrumentAgent via the event callback.
        """
        # similar to above
        self.assertTrue(False)

    def test_publish_engineering_data(self):
        """
        Tests to see if engineering data is appropriately published back to the
        InstrumentAgent via the event callback.
        """
        # similar to above
        self.assertTrue(False)
        
    def test_get_running_config(self):
        """
        Checks to see that one can successfully get the running config from an
        instrument protocol.
        """
        # set some values
        log.debug("first param_dict: %s", self.protocol._param_dict.get_config())
        self.protocol._param_dict.add("foo", r'foo=(.*)',
                             lambda match : int(match.group(1)),
                             lambda x : str(x),
                             direct_access=True,
                             default_value=10)
        self.protocol._param_dict.set_default("foo") # test hack to set w/o fetch
        self.protocol._param_dict.add("bar", r'bar=(.*)',
                             lambda match : int(match.group(1)),
                             lambda x : str(x),
                             direct_access=False,
                             default_value=15)
        self.protocol._param_dict.set_default("bar")
                
        self.assertEquals(self.protocol._param_dict.get("foo"), 10)
        self.assertEquals(self.protocol._param_dict.get("bar"), 15)
        result = self.protocol.get_running_config()
        self.assertEquals(result['foo'], 10)
        self.assertEquals(result['bar'], 15)

        self.protocol._param_dict.update("bar=20")
        result = self.protocol.get_running_config()
        self.assertEquals(result['foo'], 10)
        self.assertEquals(result['bar'], 20)
        self.assertEquals(self.protocol._param_dict.get("bar"), 20)
        
        # get and check the running config
        result = self.protocol.get_running_config()
        self.assertTrue(isinstance(result, dict))
        self.assertEquals(result['foo'], 10)
        self.assertEquals(result['bar'], 20)

    def test_init_values(self):
        """
        Test getting and setting the initialization value for a parameter
        """
        # set an additional value for test
        self.protocol._param_dict.add("foo", r'foo=(.*)',
                             lambda match : int(match.group(1)),
                             lambda x : str(x),
                             direct_access=True,
                             startup_param=True,
                             default_value=10)
        self.protocol._param_dict.add("bar", r'bar=(.*)',
                             lambda match : int(match.group(1)),
                             lambda x : str(x),
                             direct_access=False,
                             startup_param=True,
                             default_value=15)
        self.protocol._param_dict.add("baz", r'baz=(.*)',
                             lambda match : int(match.group(1)),
                             lambda x : str(x),
                             direct_access=True,
                             default_value=20)
        self.protocol._param_dict.add("bat", r'bat=(.*)',
                             lambda match : int(match.group(1)),
                             lambda x : str(x),
                             startup_param=False,
                             default_value=20)
        self.protocol._param_dict.add("qux", r'qux=(.*)',
                             lambda match : int(match.group(1)),
                             lambda x : str(x),
                             startup_param=True)
        self.protocol._param_dict.update("qux=6666")
        
        # mark init params
        self.assertRaises(InstrumentParameterException,
                          self.protocol.set_init_params, [])
        self.protocol.set_init_params({"foo": 1111, "baz":2222})
        
        # get new startup config
        result = self.protocol.get_startup_config()
        
        self.assertEquals(len(result), 3)
        self.assertEquals(result["foo"], 1111) # init param
        self.assertEquals(result["bar"], 15)   # default param
        self.assertEquals(result["qux"], 6666) # set param
        
        