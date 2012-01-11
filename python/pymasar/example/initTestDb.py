'''
Created on Jan 3, 2012

@author: shengb
'''

import os

import sqlite3
from pymasar.pvgroup.pvgroup import (savePvGroup)
from pymasar.pvgroup.pv import (saveGroupPvs)
from pymasar.service.service import (saveService)
from pymasar.service.serviceconfig import (saveServiceConfig, saveServicePvGroup, retrieveServiceConfigPVs)
from pymasar.service.serviceevent import (saveServiceEvent)
from pymasar.utils import (save)
from pymasar.masardata.masardata import (saveMasar)

conn = sqlite3.connect('masar.db')

# pvgroup name: (pv list file, description)
pvgroups= {
    'ltbd1':        ('ltbd1.txt' , 'linac to beam dump 1 all pvs') , 
    'ltbd1_bpm':    ('ltbd1_bpm.txt' , 'linac to beam dump 1 all bpm related pvs'),
    'ltbd1_quad':   ('ltbd1_quad.txt' , 'linac to beam dump 1 all quad related pvs'),
    'ltbd2':        ('ltbd2.txt' , 'linac to beam dump 2 all pvs'),
    'ltbd2_bpm':    ('ltbd2_bpm.txt' , 'linac to beam dump 1 all bpm related pvs'),
    'ltbd2_quad':   ('ltbd2_quad.txt' , 'linac to beam dump 1 all quad related pvs'),
    'sr':           ('sr.txt' , 'storage ring all pvs'),
    'sr_bpm':       ('sr_bpm.txt' , 'storage ring all bpm pvs'),
    'sr_bpm_x':     ('sr_bpm_x.txt' , 'storage ring horizontal orbit'),
    'sr_bpm_y':     ('sr_bpm_y.txt' , 'storage ring vertical orbit'),
    'sr_hcor':      ('sr_hcor.txt' , 'storage ring horizontal slow corrector'),
    'sr_hfcor':     ('sr_hfcor.txt' , 'storage ring horizontal fast corrector'),
    'sr_qs':        ('sr_qs.txt' , 'storage ring quad and sext pvs'),
    'sr_quad':      ('sr_quad.txt' , 'storage ring quad pvs'),
    'sr_sext':      ('sr_sext.txt' , 'storage ring sext pvs'),
    'sr_vcor':      ('sr_vcor.txt' , 'storage ring vertical slow corrector'),
    'sr_vfcor':     ('sr_vfcor.txt' , 'storage ring vertical fast corrector')
}

# dict format
# configname: (config desc, system)
masarconfigs= {
    'ltbd1':        ('linac to beam dump 1 whole machine', 'bd1'), 
    'ltbd1_bpm':    ('linac to beam dump 1 all bpm', 'bd1'),
    'ltbd1_quad':   ('linac to beam dump 1 all quad', 'bd1'),
    'ltbd2':        ('linac to beam dump 2 whole machine', 'bd2'),
    'ltbd2_bpm':    ('linac to beam dump 1 all bpm', 'bd2'),
    'ltbd2_quad':   ('linac to beam dump 1 all quad', 'bd2'),
    'sr':           ('storage ring whole machine', 'sr'),
    'sr_bpm':       ('storage ring all bpm', 'sr'),
    'sr_bpm_x':     ('storage ring horizontal orbit', 'sr'),
    'sr_bpm_y':     ('storage ring vertical orbit', 'sr'),
    'sr_hcor':      ('storage ring horizontal slow corrector', 'sr'),
    'sr_hfcor':     ('storage ring horizontal fast corrector', 'sr'),
    'sr_qs':        ('storage ring quad and sext', 'sr'),
    'sr_quad':      ('storage ring quads', 'sr'),
    'sr_sext':      ('storage ring sexts', 'sr'),
    'sr_vcor':      ('storage ring vertical slow corrector', 'sr'),
    'sr_vfcor':     ('storage ring vertical fast corrector', 'sr')
}

# service config: [pvgroup,]
pvg2config= {
    'ltbd1':     ['ltbd1'],
    'ltbd1_bpm': ['ltbd1_bpm'],
    'ltbd1_quad':['ltbd1_quad'],
    'ltbd2':     ['ltbd2'],
    'ltbd2_bpm': ['ltbd2_bpm'],
    'ltbd2_quad':['ltbd2_quad'],
    'sr':        ['sr'],
    'sr_bpm':    ['sr_bpm_x', 'sr_bpm_y'],
    'sr_bpm_x':  ['sr_bpm_x'],
    'sr_bpm_y':  ['sr_bpm_y'],
    'sr_hcor':   ['sr_hcor'],
    'sr_hfcor':  ['sr_hfcor'],
    'sr_qs':     ['sr_quad', 'sr_sext'],
    'sr_quad':   ['sr_quad'],
    'sr_sext':   ['sr_sext'],
    'sr_vcor':   ['sr_vcor'],
    'sr_vfcor':  ['sr_vfcor']
}

#saveServiceEvent(conn, servicename, configname, comment=None):
# service config: [comment]
event4conf = {
    'ltbd1':     ['masar event for ltbd1 section'],
    'ltbd1_bpm': ['masar event for bpm in ltbd1 section'],
    'ltbd1_quad':['masar event for quad in ltbd1 section'],
    'ltbd2':     ['masar event for ltbd2 section'],
    'ltbd2_bpm': ['masar event for bpm in ltbd2 section'],
    'ltbd2_quad':['masar event for quad in ltbd2 section'],
    'sr':        ['masar event for storage ring'],
    'sr_bpm':    ['masar event for storage ring bpms'],
    'sr_bpm_x':  ['masar event for storage ring horizontal bpms'],
    'sr_bpm_y':  ['masar event for storage ring vertical bpms'],
    'sr_hcor':   ['masar event for storage ring horizontal corrector'],
    'sr_hfcor':  ['masar event for storage ring horizontal fast corrector'],
    'sr_qs':     ['masar event for storage ring both quad and sext'],
    'sr_quad':   ['masar event for storage ring quad'],
    'sr_sext':   ['masar event for storage ring sext'],
    'sr_vcor':   ['masar event for storage ring vertical corrector'],
    'sr_vfcor':  ['masar event for storage ring vertical fast corrector']              
              }

__servicename='masar'
__configname='orbit C01', 

def initPvGroups():        
    for k,v in sorted(pvgroups.items()):
        __file = '/'.join((os.path.abspath(os.path.dirname(__file__)), 'pvs', v[0]))
        if os.path.exists(__file): 
            if os.path.isfile(__file):
                pvlist = None
                try:
                    f = open(__file, 'r')
                    pvlist = f.read()
                    pvlist = pvlist.split('\n')
                    if len(pvlist[len(pvlist)-1]) == 0:
                        pvlist = pvlist[:-1]
                    savePvGroup(conn, k, func=v[1])
                    saveGroupPvs(conn, k, pvlist)
#                    results = retrieveGroupPvs(conn, pvgroup_id[0])
                finally:
                    if f:
                        f.close()
                print ('finished saving {0}'.format(v[0]))
            else:
                print ("""pv list file ({0}) is not a file.""".format(v[0]))
        else:
            print ("""pv list file ({0}) does not exist.""".format(v[0]))

def initService():
    saveService(conn, 'masar', desc='machine snapshot, archiving, and retrieve service')
    saveService(conn, 'archive', desc='machine archiving service')

def initServiceConfig():
    for k, v in sorted(masarconfigs.items()):
        saveServiceConfig(conn, __servicename, k, configdesc = v[0], system=v[1])
        try:
            pvg = pvg2config[k]
            saveServicePvGroup(conn, k, pvg)
        except:
            pass

def dummyServiceEventNoData():
    for k, v in sorted(event4conf.items()):
        saveServiceEvent(conn, __servicename, k, comment=v[0])

def dummyServiceEventData():
    for k, v in sorted(event4conf.items()):
        pvlist = retrieveServiceConfigPVs(conn, k, servicename=__servicename)
        data = []
        
        import random
        # data from ioc
        # [(pv_name, value, status, severity, ioc_timestamp, ioc_timestamp_nano), ]
        for pv in pvlist:
            data.append((pv, str(random.uniform(-5.0e-2, 5.0e-2)), '0', '0', str(random.randrange(1e9, 5e9)), str(random.randrange(1e6, 5e6))))
        saveMasar(conn, data, servicename=__servicename, configname=k, comment=v[0])
        
if __name__ == '__main__':
#    initPvGroups()
#    initService()
#    initServiceConfig()
#    dummyServiceEventNoData
    dummyServiceEventData()
    save(conn)
    conn.close()