TOP=../..

include $(TOP)/configure/CONFIG

PROD_HOST += gatherV3Data
gatherV3Data_SRCS += gatherV3Data.cpp
#gatherV3Data_LIBS += Com pvData nt pvAccess
gatherV3Data_LIBS += gather nt pvAccess pvData Com
gatherV3Data_LIBS += $(PYTHON)

PROD_HOST += gatherV3DataTest
gatherV3DataTest_SRCS += gatherV3DataTest.cpp
#gatherV3DataTest_LIBS += nt pvAccess pvData Com
gatherV3DataTest_LIBS += gather nt pvAccess pvData Com
gatherV3DataTest_LIBS += $(PYTHON)

PROD_HOST += gatherV3DataExample
gatherV3DataExample_SRCS += gatherV3DataExample.cpp
#gatherV3DataExample_LIBS += nt pvAccess pvData Com
gatherV3DataExample_LIBS += gather nt pvAccess pvData Com
gatherV3DataExample_LIBS += $(PYTHON)

PROD_HOST += gatherV3DataPut
gatherV3DataPut_SRCS += gatherV3DataPut.cpp
#gatherV3DataPut_LIBS += nt pvAccess pvData Com
gatherV3DataPut_LIBS += gather nt pvAccess pvData Com
gatherV3DataPut_LIBS += $(PYTHON)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

