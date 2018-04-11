#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import random
from xml.etree.ElementTree import ElementTree, Element, SubElement

from PyQt4.QtGui import QMessageBox, QApplication, QWidget, QInputDialog, QLineEdit


class rrJob(object):
    def __init__(self):
        self.version = ""
        self.software = ""
        self.renderer = ""
        self.RequiredLicenses = ""
        self.sceneName = ""
        self.sceneDatabaseDir = ""
        self.seqStart = 0
        self.seqEnd = 100
        self.seqStep = 1
        self.seqFileOffset = 0
        self.seqFrameSet = ""
        self.imageWidth = 99
        self.imageHeight = 99
        self.imageDir = ""
        self.imageFileName = ""
        self.imageFramePadding = 4
        self.imageExtension = ""
        self.imagePreNumberLetter = ""
        self.imageSingleOutput = False
        self.imageStereoR = ""
        self.imageStereoL = ""
        self.sceneOS = ""
        self.camera = ""
        self.layer = ""
        self.channel = ""
        self.maxChannels = 0
        self.channelFileName = []
        self.channelExtension = []
        self.isActive = False
        self.sendAppBit = ""
        self.preID = ""
        self.waitForPreID = ""
        self.CustomA = ""
        self.CustomB = ""
        self.CustomC = ""
        self.CustomVarianceFrames = ""
        self.LocalTexturesFile = ""
        self.rrSubmitVersion = "%rrVersion%"
        self.packageSize = ""
        self.threadCount = ""
        self.renderNode = ""
        self.rendererVersionName = ""
        self.rendererVersion = ""
        self.SubmitterParameter = ""

    # from infix.se (Filip Solomonsson)
    def indent(self, elem, level=0):
        i = "\n" + level * ' '
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + " "
            for e in elem:
                self.indent(e, level + 1)
                if not e.tail or not e.tail.strip():
                    e.tail = i + " "
            if not e.tail or not e.tail.strip():
                e.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
        return True

    def subE(self, parent, tag, text):
        sub = SubElement(parent, tag)
        if (type(text) == unicode):
            sub.text = text.encode('utf8')
        else:
            sub.text = str(text).decode("utf8")
        return sub

    def writeToXMLstart(self, submitOptions):
        rootElement = Element("rrJob_submitFile")
        rootElement.attrib["syntax_version"] = "6.0"
        self.subE(rootElement, "DeleteXML", "0")
        self.subE(rootElement, "SubmitterParameter", submitOptions)
        # YOU CAN ADD OTHER NOT SCENE-INFORMATION PARAMETERS USING THIS FORMAT:
        # self.subE(jobElement,"SubmitterParameter","PARAMETERNAME=" + PARAMETERVALUE_AS_STRING)
        return rootElement

    def writeToXMLJob(self, rootElement):

        jobElement = self.subE(rootElement, "Job", "")
        self.subE(jobElement, "Software", self.software)
        self.subE(jobElement, "Renderer", self.renderer)
        self.subE(jobElement, "RequiredLicenses", self.RequiredLicenses)
        self.subE(jobElement, "Version", self.version)
        if (len(self.rendererVersionName) > 0):
            self.subE(jobElement, "customRenVer_" + self.rendererVersionName, self.rendererVersion)
        self.subE(jobElement, "SceneName", self.sceneName)
        self.subE(jobElement, "SceneDatabaseDir", self.sceneDatabaseDir)
        self.subE(jobElement, "IsActive", self.isActive)
        self.subE(jobElement, "SeqStart", self.seqStart)
        self.subE(jobElement, "SeqEnd", self.seqEnd)
        self.subE(jobElement, "SeqStep", self.seqStep)
        self.subE(jobElement, "SeqFileOffset", self.seqFileOffset)
        self.subE(jobElement, "SeqFrameSet", self.seqFrameSet)
        self.subE(jobElement, "ImageWidth", int(self.imageWidth))
        self.subE(jobElement, "ImageHeight", int(self.imageHeight))
        self.subE(jobElement, "ImageDir", self.imageDir)
        self.subE(jobElement, "ImageFilename", self.imageFileName)
        self.subE(jobElement, "ImageFramePadding", self.imageFramePadding)
        self.subE(jobElement, "ImageExtension", self.imageExtension)
        self.subE(jobElement, "ImageSingleOutput", self.imageSingleOutput)
        self.subE(jobElement, "ImagePreNumberLetter", self.imagePreNumberLetter)
        self.subE(jobElement, "ImageStereoR", self.imageStereoR)
        self.subE(jobElement, "ImageStereoL", self.imageStereoL)
        self.subE(jobElement, "SceneOS", self.sceneOS)
        self.subE(jobElement, "Camera", self.camera)
        self.subE(jobElement, "Layer", self.layer)
        self.subE(jobElement, "Channel", self.channel)
        self.subE(jobElement, "SendAppBit", self.sendAppBit)
        self.subE(jobElement, "PreID", self.preID)
        self.subE(jobElement, "WaitForPreID", self.waitForPreID)
        self.subE(jobElement, "CustomDenoiseFlags", self.CustomA)
        self.subE(jobElement, "CustomB", self.CustomB)
        self.subE(jobElement, "CustomVarianceFrames", self.CustomVarianceFrames)
        self.subE(jobElement, "CustomC", self.CustomC)
        self.subE(jobElement, "rrSubmitVersion", self.rrSubmitVersion)
        self.subE(jobElement, "LocalTexturesFile", self.LocalTexturesFile)
        self.subE(jobElement, "SubmitterParameter", self.SubmitterParameter)


        self.subE(jobElement, "PackageSize", self.packageSize)
        self.subE(jobElement, "ThreadCount", self.threadCount)
        self.subE(jobElement, "Rendernode", self.renderNode)

        for c in range(0, self.maxChannels):
            self.subE(jobElement, "ChannelFilename", self.channelFileName[c])
            self.subE(jobElement, "ChannelExtension", self.channelExtension[c])
        return True

    def writeToXMLEnd(self, f, rootElement):
        xml = ElementTree(rootElement)
        self.indent(xml.getroot())

        if not f == None:
            xml.write(f)
            f.close()
        else:
            print("No valid file has been passed to the function")
            try:
                f.close()
            except:
                pass
            return False
        return True


def getOSString():
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        return "win"
    elif (sys.platform.lower() == "darwin"):
        return "osx"
    else:
        return "lx"


################################################################################
# global functions
# from rrSubmit_Nuke_5.py (Copyright (c) Holger Schoenberger - Binary Alchemy)


def getRR_Root():
    if os.environ.has_key('RR_ROOT'):
        return os.environ['RR_ROOT']
    HCPath = "%"
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        HCPath = "%RRLocationWin%"
    elif (sys.platform.lower() == "darwin"):
        HCPath = "%RRLocationMac%"
    else:
        HCPath = "%RRLocationLx%"
    if HCPath[0] != "%":
        return HCPath
    writeError("This plugin was not installed via rrWorkstationInstaller!")


def getRRSubmitterPath():
    ''' returns the rrSubmitter filename '''
    rrRoot = getRR_Root()
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        rrSubmitter = rrRoot + "\\win__rrSubmitter.bat"
    elif (sys.platform.lower() == "darwin"):
        rrSubmitter = rrRoot + "/bin/mac64/rrSubmitter.app/Contents/MacOS/rrSubmitter"
    else:
        rrSubmitter = rrRoot + "/lx__rrSubmitter.sh"
    return rrSubmitter

# generate a tempfile
def getNewTempFileName(filedir, filename):
    random.seed(time.time())
    num = str(random.randrange(1000, 10000, 1))
    name = 'rrSubmit_%s_%s.xml' % (filename, num)
    name = os.path.join(filedir, name)
    print name
    return name


def wrn(msg, buttons=[QMessageBox.Ok]):
    app = QApplication(sys.argv)
    wdg = QWidget()
    result = QMessageBox.question(wdg, 'Warning', msg, buttons, QMessageBox.No)
    return result


def submit_denoise(variance_files, prefix='split_'):
    """
    submit the files given in sys.argv to royal render / prman denoiser
    @variance_files : sequence of exr images used to guide the denoise process
                      in our case we fetch this from sys.argv
    @prefix : a prefix for the beauty filesequence can be assigned
              in our case this defaults to 'split_'

    note : per now the script expects the following files to exist:
        <filename>_<FN>_variance.exr - the input file sequence that guides the process
        <prefix><filename>_<FN>.exr - the file sequence that will be denoised
        no checking will be done if the beauty does not exist!
    """

    if len(variance_files) < 1:
        wrn('No input selected', QMessageBox.Yes)

    else:
        # fetch sequence info
        file_str = ' '.join(variance_files)
        frames = sorted(map(int, sorted(re.findall(r'\d{4}', file_str))))
        missing = sorted(set(range(frames[0], frames[-1] + 1)).difference(frames))

    # wrn when missing frames
    if missing:
        result = wrn('Missing frames:\n{}\n\nSubmit anyway?'.format(missing), QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.No:
            return

    # commandline arg user input
    app = QApplication(sys.argv)
    wdg = QWidget()
    denoise_cmd = 'denoise'
    default_args = '--override filterLayersIndependently true --'
    denoise_args, ok_pressed = QInputDialog.getText(wdg, "Denoise arguments","", QLineEdit.Normal, default_args)
    if ok_pressed is False:
        print "Aborted by user"
        return

    # fetch pathes
    path, input_file = os.path.split(variance_files[0])
    file_name = '_'.join(input_file.split('_')[0:3]) # + '_####_filtered.exr'
    variance_input = os.path.join(path, '{}_{{<SeqFrameList+-1>}}_variance.exr'.format(file_name))
    beauty_input = os.path.join(path, '{}{}_{}.exr'.format(prefix, file_name, frames[0]))
    output_file = os.path.join(path, '{}{}__filtered####.exr'.format(prefix, file_name))
    rr_xml = os

    # open job xml
    job_path = getNewTempFileName(path, '{}_denoise'.format(file_name))
    job_file = open(job_path, 'w')

    # set job options
    job = rrJob()
    job.software = 'prmanDenoise'
    #  job.renderer = 'ChunkAble'
    job.layer = 'prmanDenoise'
    job.sceneName = beauty_input
    job.CustomVarianceFrames = variance_input
    job.seqStart = frames[0]
    job.seqEnd = frames[-1]
    job.imageFileName = output_file
    job.SubmitterParameter = '\"COfilterLayers=0~1\"'
    job.IsActive = 1
    job.imageFramePadding = 4

    # wirte job xml
    root = job.writeToXMLstart(None)
    job_tag = job.writeToXMLJob(root)
    job.writeToXMLEnd(job_file, root)

    # launch submitter
    os.system(getRRSubmitterPath() + "  \"" + job_path + "\"")


if __name__ == '__main__':
    # entry point

    os.environ['RMANTREE'] = '/bigfoot/ratatoskr/software/applications/renderman/Linux/RenderManProServer-21.4_Linux/'
    os.environ['RR_ROOT'] = '/medianet/renderfarm/_RR6'
    submit_denoise(sys.argv[1:])
