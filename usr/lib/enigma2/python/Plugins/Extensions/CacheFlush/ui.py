#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import _

from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Components.config import (
    ConfigInteger,
    config,
    getConfigListEntry,
    ConfigYesNo,
    ConfigSelection,
)
from Screens.Screen import Screen
from enigma import (eTimer, getDesktop)
from os import system
import os

VERSION = "2.0_r4"
HD = False
screenwidth = getDesktop(0).size()
if screenwidth.width() >= 1280:
    HD = True

config.plugins.CacheFlush.enable = ConfigYesNo(default=False)
config.plugins.CacheFlush.type = ConfigSelection(default="3", choices=[("1", _("pagecache")), ("2", ("dentries and inodes")), ("3", ("pagecache, dentries and inodes"))])
config.plugins.CacheFlush.sync = ConfigYesNo(default=False)

global NGETTEXT
NGETTEXT = False
ngettext = ''
try:   # can be used ngettext ?
    ngettext("%d minute", "%d minutes", 5)
    NGETTEXT = True
except Exception as e:
    print("[CacheFlush] ngettext is not supported:", e)

choicelist = []
for i in range(5, 151, 5):
    if NGETTEXT:
        choicelist.append(("%d" % i, ngettext("%d minute", "%d minutes", i) % i))
    else:
        choicelist.append(("%d" % i))
config.plugins.CacheFlush.timeout = ConfigSelection(default="30", choices=choicelist)
config.plugins.CacheFlush.scrinfo = ConfigYesNo(default=False)
choicelist = []
for i in range(1, 11):
    if NGETTEXT:
        choicelist.append(("%d" % i, ngettext("%d second", "%d seconds", i) % i))
    else:
        choicelist.append(("%d" % i))
config.plugins.CacheFlush.timescrinfo = ConfigSelection(default="10", choices=choicelist)
choicelist = [("0", _("Default"))]
for i in range(1, 21):
    choicelist.append(("%d" % i, "%d kB" % (1024*i)))
config.plugins.CacheFlush.uncached = ConfigSelection(default="1", choices=choicelist)
config.plugins.CacheFlush.free_default = ConfigInteger(default=0, limits=(0, 9999999999))
cfg = config.plugins.CacheFlush

# display mem, used, free and progressbar
ALL = 0x17


def dropCache():
    if cfg.sync.value:
        system("sync")
        print("[CacheFlush] sync")
    if cfg.type.value == "1":    # free pagecache
        system("echo 1 > /proc/sys/vm/drop_caches")
        print("[CacheFlush] free pagecache")
    elif cfg.type.value == "2":  # free dentries and inodes
        system("echo 2 > /proc/sys/vm/drop_caches")
        print("[CacheFlush] free dentries and inodes")
    elif cfg.type.value == "3":  # free pagecache, dentries and inodes
        system("echo 3 > /proc/sys/vm/drop_caches")
        print("[CacheFlush] free pagecache, dentries and inodes")

def getMinFreeKbytes():
    for line in open('/proc/sys/vm/min_free_kbytes', 'r'):
        line = line.strip()
    print("[CacheFlush] min_free_kbytes is %s kB" % line)
    return line


def setMinFreeKbytes(size):
    system("echo %d > /proc/sys/vm/min_free_kbytes" % (size))
    print("[CacheFlush] set min_free_kbytes to %d kB" % size)


class CacheFlushSetupMenu(Screen, ConfigListScreen):
    if HD:
        skin = """
            <screen name="CacheFlush" position="center,center" size="1200,900" title="" backgroundColor="#31000000">
                <widget name="config" position="13,15" size="1170,542" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                <ePixmap pixmap="skin_default/div-h.png" position="1,578" zPosition="2" size="1200,6" />
                <widget name="min_free_kb" font="Regular; 30" position="15,600" size="1160,60" zPosition="2" valign="center" backgroundColor="#31000000" transparent="1" />
                <widget name="memory" position="15,670" zPosition="2" size="1160,60" valign="center" halign="left" font="Regular; 28" transparent="1" foregroundColor="white" />
                <widget name="slide" position="15,740" zPosition="2" borderWidth="1" size="1160,50" backgroundColor="dark" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,799" zPosition="2" size="1200,6" />
                <widget name="key_red" position="73,820" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="317,820" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="green" />
                <widget name="key_yellow" position="563,820" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="yellow" />
                <widget name="key_blue" position="807,820" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="blue" />
            </screen>"""
    else:
        skin = """
            <screen name="CacheFlush" position="center,center" size="1000,715" title="" backgroundColor="#31000000">
                <widget name="config" position="13,15" size="980,442" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                <ePixmap pixmap="skin_default/div-h.png" position="1,473" zPosition="2" size="1000,4" />
                <widget name="min_free_kb" font="Regular; 28" position="10,485" size="980,45" zPosition="2" valign="center" backgroundColor="#31000000" transparent="1" />
                <widget name="memory" position="10,535" zPosition="2" size="980,44" valign="center" halign="left" font="Regular; 28" transparent="1" foregroundColor="white" />
                <widget name="slide" position="10,585" zPosition="2" borderWidth="1" size="980,30" backgroundColor="dark" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,619" zPosition="2" size="1000,4" />
                <widget name="key_red" position="25,632" zPosition="2" size="220,50" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="268,632" zPosition="2" size="220,50" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="green" />
                <widget name="key_yellow" position="510,632" zPosition="2" size="220,50" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="yellow" />
                <widget name="key_blue" position="743,632" zPosition="2" size="220,50" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="blue" />
            </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=session, on_change=self.changedEntry)
        self.setup_title = _("Setup CacheFlush")
        self["actions"] = ActionMap(["SetupActions", "ColorActions"],
                                    {
                                        "cancel": self.keyCancel,
                                        "green": self.keySave,
                                        "ok": self.keySave,
                                        "red": self.keyCancel,
                                        "blue": self.freeMemory,
                                        "yellow": self.memoryInfo,
                                    }, -2)

        self["key_green"] = Label(_("Save"))
        self["key_red"] = Label(_("Cancel"))
        self["key_blue"] = Label(_("Clear Now"))
        self["key_yellow"] = Label(_("Info"))

        self["slide"] = ProgressBar()
        self["slide"].setValue(100)
        self["slide"].hide()
        self["memory"] = Label()
        self["min_free_kb"] = Label(_("Uncached memory: %s kB,   ( default: %s kB )") % (getMinFreeKbytes(), str(cfg.free_default.value)))

        self.runSetup()
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(_("Setup CacheFlush") + "  " + VERSION)
        self["memory"].setText(self.getMemory(ALL))

    def runSetup(self):
        self.list = [getConfigListEntry(_("Enable CacheFlush"), cfg.enable)]
        if cfg.enable.value:
            autotext = _("Auto timeout")
            timetext = _("Time of info message")
            if not NGETTEXT:
                autotext = _("Auto timeout (5-150min)")
                timetext = _("Time of info message (1-10sec)")
            self.list.extend((
                getConfigListEntry(_("Cache drop type"), cfg.type),
                getConfigListEntry(_("Clean \"dirty\" cache too"), cfg.sync),
                getConfigListEntry(autotext, cfg.timeout),
                getConfigListEntry(_("Show info on screen"), cfg.scrinfo),
                getConfigListEntry(timetext, cfg.timescrinfo),
                getConfigListEntry(_("Display plugin in"), cfg.where),
            ))
        self.list.extend((getConfigListEntry(_("Uncached memory size"), cfg.uncached),))
        self["config"].list = self.list
        self["config"].setList(self.list)

    def keySave(self):
        for x in self["config"].list:
            x[1].save()
        # configfile.save()
        self.setUncachedMemory()
        self.close()

    def keyCancel(self):
        for x in self["config"].list:
            x[1].cancel()
        self.close()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        if self["config"].getCurrent()[1] == cfg.enable:
            self.runSetup()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        if self["config"].getCurrent()[1] == cfg.enable:
            self.runSetup()

    def changedEntry(self):
        for x in self.onChangedEntry:
            x()

    def freeMemory(self):
        dropCache()
        self["memory"].setText(self.getMemory(ALL))

    def getMemory(self, par=0x01):
        try:
            mm = mu = mf = 0
            for line in open('/proc/meminfo', 'r'):
                line = line.strip()
                if "MemTotal:" in line:
                    line = line.split()
                    mm = int(line[1])
                if "MemFree:" in line:
                    line = line.split()
                    mf = int(line[1])
                    break
            mu = mm - mf
            self["memory"].setText("")
            self["slide"].hide()
            memory = ""
            if par&0x01:
                memory += "".join((_("Memory:"), " %d " % (mm/1024), _("MB"), "  "))
            if par&0x02:
                memory += "".join((_("Used:"), " %.2f%s" % (100.*mu/mm, '%'), "  "))
            if par&0x04:
                memory += "".join((_("Free:"), " %.2f%s" % (100.*mf/mm, '%')))
            if par&0x10:
                self["slide"].setValue(int(100.0*mu/mm+0.25))
                self["slide"].show()
            return memory
        except Exception as e:
            print("[CacheFlush] getMemory FAIL:", e)
            return ""

    def memoryInfo(self):
        self.session.openWithCallback(self.afterInfo, CacheFlushInfoScreen)

    def afterInfo(self, answer=False):
        self["memory"].setText(self.getMemory(ALL))

    def setUncachedMemory(self):
        if cfg.uncached.value == "0":
            setMinFreeKbytes(cfg.free_default.value)
        else:
            setMinFreeKbytes(int(cfg.uncached.value)*1024)


class CacheFlushAutoMain():
    def __init__(self):
        self.dialog = None
        if cfg.free_default.value == 0:
            cfg.free_default.value = int(getMinFreeKbytes())
            cfg.free_default.save()

    def startCacheFlush(self, session):
        self.dialog = session.instantiateDialog(CacheFlushAutoScreen)
        self.makeShow()

    def makeShow(self):
        try:
            if cfg.scrinfo.value:
                self.dialog.show()
            else:
                self.dialog.hide()
        except Exception as e:
            print(e)


CacheFlushAuto = CacheFlushAutoMain()


class CacheFlushAutoScreen(Screen):
    if HD:
        skin = """<screen name="CacheFlushAutoScreen" position="0,0" zPosition="10" size="650,60" title="CacheFlush Status" backgroundColor="#31000000">
                <widget name="message_label" font="Regular; 26" position="25,5" zPosition="2" valign="center" halign="center" size="600,50" backgroundColor="#31000000" transparent="1" />
            </screen>"""
    else:
        skin = """<screen name="CacheFlushAutoScreen" position="0,10" zPosition="10" size="400,20" title="CacheFlush Status" backgroundColor="#31000000">
                <widget name="message_label" font="Regular;16" position="10,0" zPosition="2" valign="center" halign="center" size="380,20" backgroundColor="#31000000" transparent="1" />
            </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skin = CacheFlushAutoScreen.skin
        self['message_label'] = Label(_("Starting"))
        self.CacheFlushTimer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.CacheFlushTimer_conn = self.CacheFlushTimer.timeout.connect(self.__makeWhatYouNeed)
        else:
            self.CacheFlushTimer.callback.append(self.__makeWhatYouNeed)
        # self.CacheFlushTimer.timeout.get().append(self.__makeWhatYouNeed)
        self.showTimer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.showTimer_conn = self.showTimer.timeout.connect(self.__endShow)
        else:
            self.showTimer.callback.append(self.__endShow)
        # self.showTimer.timeout.get().append(self.__endShow)
        self.state = None
        self.onLayoutFinish.append(self.__chckState)
        self.onShow.append(self.__startsuspend)
        self.__setUncachedMemory()

    def __startsuspend(self):
        self.setTitle(_("CacheFlush Status"))
        # if self.showTimer.isActive():
            # self.showTimer.stop()
        self.showTimer.start(int(cfg.timescrinfo.value) * 1000)

    def __chckState(self):
        if self.instance and self.state is None:
            if cfg.enable.value:
                self['message_label'].setText(_("Started"))
            else:
                self['message_label'].setText(_("Stopped"))
            self.state = cfg.enable.value
            if cfg.scrinfo.value and CacheFlushAuto.dialog is not None:
                CacheFlushAuto.dialog.show()
        self.CacheFlushTimer.start(int(cfg.timeout.value)*60000)

    def __makeWhatYouNeed(self):
        try:
            self.__chckState()
            if cfg.enable.value:
                dropCache()
                if self.instance:
                    self['message_label'].setText(_("Mem cleared"))
                    if cfg.scrinfo.value and CacheFlushAuto.dialog is not None:
                        CacheFlushAuto.dialog.show()
        except Exception as e:
            print(e)

    def __endShow(self):
        CacheFlushAuto.dialog.hide()

    def __setUncachedMemory(self):
        if cfg.uncached.value != "0":
            setMinFreeKbytes(int(cfg.uncached.value)*1024)


class CacheFlushInfoScreen(Screen):
    if HD:
        skin = """<screen name="CacheFlushInfoScreen" position="center,center" zPosition="2" size="1500,950" title="CacheFlush Info" backgroundColor="#31000000">
                <widget name="lmemtext" font="Regular; 24" position="10,10" size="320,820" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="lmemvalue" font="Regular; 24" position="335,10" size="320,820" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemtext" font="Regular; 24" position="839,10" size="320,820" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemvalue" font="Regular; 24" position="1165,10" size="320,820" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="pfree" position="626,160" size="100,50" font="Regular; 20" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="pused" position="631,506" size="100,50" font="Regular; 22" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="slide" position="740,14" size="50,811" render="Progress" zPosition="3" borderWidth="1" orientation="orBottomToTop" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,844" zPosition="2" size="1500,6" />
                <widget name="key_red" position="22,860" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 30" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="621,860" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 30" transparent="1" foregroundColor="green" />
                <widget name="key_blue" position="1239,860" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 30" transparent="1" foregroundColor="blue" />
            </screen>"""
    else:
        skin = """<screen name="CacheFlushInfoScreen" position="center,50" zPosition="2" size="540,500" title="CacheFlush Info" backgroundColor="#31000000" >
                <widget name="lmemtext" font="Regular;16" position="10,10" size="120,500" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="lmemvalue" font="Regular;16" position="130,10" size="80,500" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemtext" font="Regular;16" position="330,10" size="120,500" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemvalue" font="Regular;16" position="450,10" size="80,500" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="pfree" position="200,100" size="70,20" font="Regular;14" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="pused" position="200,370" size="70,20" font="Regular;14" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="slide" position="280,10" size="18,445" render="Progress" zPosition="3" borderWidth="1" orientation="orBottomToTop" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,465" zPosition="2" size="540,2" />
                <widget name="key_red" position="10,472" zPosition="2" size="130,28" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="130,472" zPosition="2" size="130,28" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="green" />
                <widget name="key_blue" position="390,472" zPosition="2" size="130,28" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="blue" />
            </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.setup_title = _("CacheFlush Info")
        self["actions"] = ActionMap(["SetupActions", "ColorActions"],
                                    {
                                      "cancel": self.cancel,
                                      "blue": self.freeMemory,
                                      "green": self.getMemInfo,
                                    }, -2)

        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Refresh"))
        self["key_blue"] = Label(_("Clear Now"))

        self['lmemtext'] = Label()
        self['lmemvalue'] = Label()
        self['rmemtext'] = Label()
        self['rmemvalue'] = Label()
        self['pfree'] = Label()
        self['pused'] = Label()

        self["slide"] = ProgressBar()
        self["slide"].setValue(100)

        self.setTitle(_("CacheFlush Info v.%s") % VERSION)
        self.onLayoutFinish.append(self.getMemInfo)

    def getMemInfo(self):
        try:
            ltext = rtext = ""
            lvalue = rvalue = ""
            mem = 0
            free = 0
            i = 0
            for line in open('/proc/meminfo', 'r'):
                (name, size, units) = line.strip().split()
                if name.find("MemTotal") != -1:
                    mem = int(size)
                if name.find("MemFree") != -1:
                    free = int(size)
                if i < 28:
                    ltext += "".join((name, "\n"))
                    lvalue += "".join((size, " ", units, "\n"))
                else:
                    rtext += "".join((name, "\n"))
                    rvalue += "".join((size, " ", units, "\n"))
                i += 1
            self['lmemtext'].setText(ltext)
            self['lmemvalue'].setText(lvalue)
            self['rmemtext'].setText(rtext)
            self['rmemvalue'].setText(rvalue)

            self["slide"].setValue(int(100.0*(mem-free)/mem+0.25))
            self['pfree'].setText("%.1f %s" % (100.*free/mem, '%'))
            self['pused'].setText("%.1f %s" % (100.*(mem-free)/mem, '%'))

        except Exception as e:
            print("[CacheFlush] getMemory FAIL:", e)

    def freeMemory(self):
        dropCache()
        self.getMemInfo()

    def cancel(self):
        self.close()
