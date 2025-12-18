#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import _, __version__

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
from os.path import exists
from sys import version_info

PY3 = version_info[0] == 3

HD = False
WQHD = False
FHD = False
screenwidth = getDesktop(0).size()
if screenwidth.width() >= 2560:
    WQHD = True
elif screenwidth.width() >= 1920:
    FHD = True
elif screenwidth.width() >= 1280:
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
    choicelist.append(("%d" % i, "%d kB" % (1024 * i)))
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
    try:
        with open('/proc/sys/vm/min_free_kbytes', 'r') as f:
            line = f.read().strip()
        print("[CacheFlush] min_free_kbytes is %s kB" % line)
        return line
    except Exception as e:
        print("[CacheFlush] Error reading min_free_kbytes:", e)
        return "0"


def setMinFreeKbytes(size):
    system("echo %d > /proc/sys/vm/min_free_kbytes" % (size))
    print("[CacheFlush] set min_free_kbytes to %d kB" % size)


class CacheFlushSetupMenu(Screen, ConfigListScreen):
    if WQHD:
        skin = """
            <screen name="CacheFlush" position="center,center" size="1800,1100" title="" backgroundColor="#31000000" flags="wfNoBorder">
                <widget name="config" position="20,10" size="1760,750" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" itemHeight="50" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,765" zPosition="2" size="1800,8" />
                <widget name="min_free_kb" font="Regular; 40" position="20,775" size="1760,70" zPosition="2" valign="center" backgroundColor="#31000000" transparent="1" />
                <widget name="memory" position="20,845" zPosition="2" size="1760,80" valign="center" halign="left" font="Regular; 36" transparent="1" foregroundColor="white" />
                <widget name="slide" position="20,930" zPosition="2" borderWidth="2" size="1760,60" backgroundColor="dark" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,995" zPosition="2" size="1800,8" />
                <widget name="key_red" position="100,1005" zPosition="2" size="350,80" valign="center" halign="center" font="Regular; 36" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="500,1005" zPosition="2" size="350,80" valign="center" halign="center" font="Regular; 36" transparent="1" foregroundColor="green" />
                <widget name="key_yellow" position="900,1005" zPosition="2" size="350,80" valign="center" halign="center" font="Regular; 36" transparent="1" foregroundColor="yellow" />
                <widget name="key_blue" position="1300,1005" zPosition="2" size="350,80" valign="center" halign="center" font="Regular; 36" transparent="1" foregroundColor="blue" />
            </screen>"""
    elif FHD:
        skin = """
            <screen name="CacheFlush" position="center,center" size="1600,1000" title="" backgroundColor="#31000000" flags="wfNoBorder">
                <widget name="config" position="20,20" size="1560,600" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" itemHeight="40" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,650" zPosition="2" size="1600,6" />
                <widget name="min_free_kb" font="Regular; 32" position="20,670" size="1560,60" zPosition="2" valign="center" backgroundColor="#31000000" transparent="1" />
                <widget name="memory" position="20,740" zPosition="2" size="1560,60" valign="center" halign="left" font="Regular; 30" transparent="1" foregroundColor="white" />
                <widget name="slide" position="20,820" zPosition="2" borderWidth="1" size="1560,50" backgroundColor="dark" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,890" zPosition="2" size="1600,6" />
                <widget name="key_red" position="80,910" zPosition="2" size="300,60" valign="center" halign="center" font="Regular; 32" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="470,910" zPosition="2" size="300,60" valign="center" halign="center" font="Regular; 32" transparent="1" foregroundColor="green" />
                <widget name="key_yellow" position="860,910" zPosition="2" size="300,60" valign="center" halign="center" font="Regular; 32" transparent="1" foregroundColor="yellow" />
                <widget name="key_blue" position="1250,910" zPosition="2" size="300,60" valign="center" halign="center" font="Regular; 32" transparent="1" foregroundColor="blue" />
            </screen>"""
    elif HD:
        skin = """
            <screen name="CacheFlush" position="center,center" size="1200,715" title="" backgroundColor="#31000000" flags="wfNoBorder">
                <widget name="config" position="15,10" size="1170,440" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                <ePixmap pixmap="skin_default/div-h.png" position="1,453" zPosition="2" size="1200,6" />
                <widget name="min_free_kb" font="Regular; 30" position="15,460" size="1160,60" zPosition="2" valign="center" backgroundColor="#31000000" transparent="1" />
                <widget name="memory" position="15,521" zPosition="2" size="1160,60" valign="center" halign="left" font="Regular; 28" transparent="1" foregroundColor="white" />
                <widget name="slide" position="17,585" zPosition="2" borderWidth="1" size="1160,50" backgroundColor="dark" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,634" zPosition="2" size="1200,6" />
                <widget name="key_red" position="73,642" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="318,640" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="green" />
                <widget name="key_yellow" position="563,640" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="yellow" />
                <widget name="key_blue" position="808,640" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 28" transparent="1" foregroundColor="blue" />
            </screen>"""
    else:
        skin = """
            <screen name="CacheFlush" position="center,center" size="800,600" title="" backgroundColor="#31000000" flags="wfNoBorder">
                <widget name="config" position="13,15" size="775,340" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                <ePixmap pixmap="skin_default/div-h.png" position="11,359" zPosition="2" size="775,4" />
                <widget name="min_free_kb" font="Regular; 28" position="10,370" size="775,45" zPosition="2" valign="center" backgroundColor="#31000000" transparent="1" />
                <widget name="memory" position="10,420" zPosition="2" size="775,44" valign="center" halign="left" font="Regular; 28" transparent="1" foregroundColor="white" />
                <widget name="slide" position="12,468" zPosition="2" borderWidth="1" size="775,30" backgroundColor="dark" />
                <ePixmap pixmap="skin_default/div-h.png" position="10,504" zPosition="2" size="775,4" />
                <widget name="key_red" position="5,537" zPosition="2" size="200,50" valign="center" halign="center" font="Regular; 24" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="208,537" zPosition="2" size="200,50" valign="center" halign="center" font="Regular; 24" transparent="1" foregroundColor="green" />
                <widget name="key_yellow" position="410,537" zPosition="2" size="200,50" valign="center" halign="center" font="Regular; 24" transparent="1" foregroundColor="yellow" />
                <widget name="key_blue" position="613,537" zPosition="2" size="200,50" valign="center" halign="center" font="Regular; 24" transparent="1" foregroundColor="blue" />
            </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=session, on_change=self.changedEntry)
        self.setup_title = _("Setup CacheFlush")
        self["actions"] = ActionMap(["SetupActions", "ColorActions"],
                                    {"cancel": self.keyCancel,
                                     "green": self.keySave,
                                     "ok": self.keySave,
                                     "red": self.keyCancel,
                                     "blue": self.freeMemory,
                                     "yellow": self.memoryInfo}, -2)

        self["key_green"] = Label(_("- - - -"))
        self["key_red"] = Label(_("Cancel"))
        self["key_blue"] = Label(_("Clear Now"))
        self["key_yellow"] = Label(_("Info"))

        self["slide"] = ProgressBar()
        self["slide"].setValue(100)
        self["slide"].hide()
        self["memory"] = Label()
        self["min_free_kb"] = Label(
            _("Uncached memory: %(current)s kB,   ( default: %(default)s kB )") % {
                "current": getMinFreeKbytes(),
                "default": str(cfg.free_default.value),
            }
        )

        self.runSetup()
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(_("Setup CacheFlush") + "  " + __version__)
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
        self['key_green'].instance.setText(_('Save') if self['config'].isChanged() else '- - - -')

    def freeMemory(self):
        dropCache()
        self["memory"].setText(self.getMemory(ALL))

    def getMemory(self, par=0x01):
        try:
            mm = mu = mf = 0
            with open('/proc/meminfo', 'r') as f:
                for line in f:
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
            if par & 0x01:
                memory += "".join((_("Memory:"), " %d " % (mm // 1024), _("MB"), "  "))
            if par & 0x02:
                memory += "".join((_("Used:"), " %.2f%s" % (100. * mu // mm, '%'), "  "))
            if par & 0x04:
                memory += "".join((_("Free:"), " %.2f%s" % (100. * mf // mm, '%')))
            if par & 0x10:
                self["slide"].setValue(int(100.0 * mu // mm + 0.25))
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
            setMinFreeKbytes(int(cfg.uncached.value) * 1024)


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
    if WQHD:
        skin = """<screen name="CacheFlushAutoScreen" position="0,10" zPosition="10" size="900,80" title="CacheFlush Status" backgroundColor="#31000000">
                <widget name="message_label" font="Regular; 36" position="30,10" zPosition="2" valign="center" halign="center" size="840,60" backgroundColor="#31000000" transparent="1" />
            </screen>"""
    elif FHD:
        skin = """<screen name="CacheFlushAutoScreen" position="0,10" zPosition="10" size="800,70" title="CacheFlush Status" backgroundColor="#31000000">
                <widget name="message_label" font="Regular; 32" position="25,10" zPosition="2" valign="center" halign="center" size="750,50" backgroundColor="#31000000" transparent="1" />
            </screen>"""
    elif HD:
        skin = """<screen name="CacheFlushAutoScreen" position="0,10" zPosition="10" size="650,60" title="CacheFlush Status" backgroundColor="#31000000">
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
        if exists('/var/lib/dpkg/info'):
            self.CacheFlushTimer_conn = self.CacheFlushTimer.timeout.connect(self.__makeWhatYouNeed)
        else:
            self.CacheFlushTimer.callback.append(self.__makeWhatYouNeed)
        # self.CacheFlushTimer.timeout.get().append(self.__makeWhatYouNeed)
        self.showTimer = eTimer()
        if exists('/var/lib/dpkg/info'):
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
        self.CacheFlushTimer.start(int(cfg.timeout.value) * 60000)

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
            setMinFreeKbytes(int(cfg.uncached.value) * 1024)


class CacheFlushInfoScreen(Screen):
    if WQHD:
        skin = """<screen name="CacheFlushInfoScreen" position="center,center" zPosition="2" size="2100,1400" title="CacheFlush Info" backgroundColor="#31000000" flags="wfNoBorder">
                <widget name="lmemtext" font="Regular; 32" position="30,30" size="450,1200" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="lmemvalue" font="Regular; 32" position="439,30" size="450,1200" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemtext" font="Regular; 32" position="1140,30" size="450,1200" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemvalue" font="Regular; 32" position="1570,30" size="450,1200" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="pfree" position="850,200" size="150,80" font="Regular; 28" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="pused" position="847,950" size="150,80" font="Regular; 30" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="slide" position="1010,30" size="70,1200" render="Progress" zPosition="3" borderWidth="2" orientation="orBottomToTop" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,1255" zPosition="2" size="2100,8" />
                <widget name="key_red" position="100,1270" zPosition="2" size="400,90" valign="center" halign="center" font="Regular; 36" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="850,1270" zPosition="2" size="400,90" valign="center" halign="center" font="Regular; 36" transparent="1" foregroundColor="green" />
                <widget name="key_blue" position="1600,1270" zPosition="2" size="400,90" valign="center" halign="center" font="Regular; 36" transparent="1" foregroundColor="blue" />
            </screen>"""
    elif FHD:
        skin = """<screen name="CacheFlushInfoScreen" position="center,center" zPosition="2" size="1900,1070" title="CacheFlush Info" backgroundColor="#31000000" flags="wfNoBorder">
                <widget name="lmemtext" font="Regular; 26" position="50,20" size="400,900" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="lmemvalue" font="Regular; 26" position="435,20" size="400,900" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemtext" font="Regular; 26" position="980,20" size="400,900" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemvalue" font="Regular; 26" position="1395,20" size="400,900" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="pfree" position="770,150" size="120,60" font="Regular; 24" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="pused" position="770,750" size="120,60" font="Regular; 26" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="slide" position="900,20" size="50,900" render="Progress" zPosition="3" borderWidth="1" orientation="orBottomToTop" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,955" zPosition="2" size="1800,6" />
                <widget name="key_red" position="80,970" zPosition="2" size="350,80" valign="center" halign="center" font="Regular; 32" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="700,970" zPosition="2" size="350,80" valign="center" halign="center" font="Regular; 32" transparent="1" foregroundColor="green" />
                <widget name="key_blue" position="1320,970" zPosition="2" size="350,80" valign="center" halign="center" font="Regular; 32" transparent="1" foregroundColor="blue" />
            </screen>"""
    elif HD:
        skin = """<screen name="CacheFlushInfoScreen" position="center,center" zPosition="2" size="1280,720" title="CacheFlush Info" backgroundColor="#31000000" flags="wfNoBorder">
                <widget name="lmemtext" font="Regular; 24" position="10,10" size="280,620" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="lmemvalue" font="Regular; 24" position="290,10" size="300,620" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemtext" font="Regular; 24" position="774,10" size="280,620" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemvalue" font="Regular; 24" position="1060,10" size="280,620" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="pfree" position="580,159" size="100,50" font="Regular; 20" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="pused" position="576,506" size="100,50" font="Regular; 22" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="slide" position="685,14" size="50,620" render="Progress" zPosition="3" borderWidth="1" orientation="orBottomToTop" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,634" zPosition="2" size="1280,6" />
                <widget name="key_red" position="22,649" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 30" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="532,650" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 30" transparent="1" foregroundColor="green" />
                <widget name="key_blue" position="1019,646" zPosition="2" size="220,60" valign="center" halign="center" font="Regular; 30" transparent="1" foregroundColor="blue" />
            </screen>"""
    else:
        skin = """<screen name="CacheFlushInfoScreen" position="center,center" zPosition="2" size="540,550" title="CacheFlush Info" backgroundColor="#31000000" flags="wfNoBorder">
                <widget name="lmemtext" font="Regular;16" position="10,10" size="120,450" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="lmemvalue" font="Regular;16" position="130,10" size="80,450" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemtext" font="Regular;16" position="330,5" size="120,450" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                <widget name="rmemvalue" font="Regular;16" position="450,10" size="80,450" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
                <widget name="pfree" position="200,100" size="70,20" font="Regular;14" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="pused" position="200,370" size="70,20" font="Regular;14" zPosition="3" halign="right" backgroundColor="#2890fe" transparent="1" />
                <widget name="slide" position="280,10" size="18,445" render="Progress" zPosition="3" borderWidth="1" orientation="orBottomToTop" />
                <ePixmap pixmap="skin_default/div-h.png" position="0,465" zPosition="2" size="540,2" />
                <widget name="key_red" position="10,497" zPosition="2" size="130,28" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="red" />
                <widget name="key_green" position="230,497" zPosition="2" size="130,28" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="green" />
                <widget name="key_blue" position="390,497" zPosition="2" size="130,28" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="blue" />
            </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.setup_title = _("CacheFlush Info")
        self["actions"] = ActionMap(["SetupActions", "ColorActions"],
                                    {"cancel": self.cancel,
                                     "blue": self.freeMemory,
                                     "green": self.getMemInfo}, -2)

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

        self.setTitle(_("CacheFlush Info v.%s") % __version__)
        self.onLayoutFinish.append(self.getMemInfo)

    def getMemInfo(self):
        try:
            ltext = rtext = ""
            lvalue = rvalue = ""
            mem = 0
            free = 0
            i = 0
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        name = parts[0]
                        size = parts[1]
                        units = parts[2] if len(parts) > 2 else "kB"
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

            if mem > 0:
                self["slide"].setValue(int(100.0 * (mem - free) // mem + 0.25))
                self['pfree'].setText("%.1f %s" % (100. * free // mem, '%'))
                self['pused'].setText("%.1f %s" % (100. * (mem - free) // mem, '%'))

        except Exception as e:
            print("[CacheFlush] getMemory FAIL:", e)

    def freeMemory(self):
        dropCache()
        self.getMemInfo()

    def cancel(self):
        self.close()
