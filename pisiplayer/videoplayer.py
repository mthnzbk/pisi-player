#
#
#  Copyright 2016 Metehan Özbek <mthnzbk@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer, pyqtSignal, QFile
from .settings import settings
from .downloadmanager import DownloadManager
import os

class Player(QGraphicsVideoItem):

    isSubtitle = pyqtSignal(bool)
    subtitlePos = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.player = QMediaPlayer()
        self.player.setVolume(int(settings().value("Player/volume") or 100))
        self.player.setVideoOutput(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerPos)

        self.player.currentMediaChanged.connect(self.signalStart)
        self.player.currentMediaChanged.connect(self.parent.subtitleitem.subtitleControl)
        self.player.currentMediaChanged.connect(self.videoConfigure)
        """self.player.mediaStatusChanged.connect(self.metadata)

    def metadata(self, data):
        if data and self.player.isMetaDataAvailable():
            print(self.player.metaData("VideoCodec"))"""

    def videoConfigure(self, media):
        video_name = os.path.basename(media.canonicalUrl().toLocalFile())
        videos = settings().value("Player/video_names") or []
        videos_time = settings().value("Player/videos_time") or []
        try:
            self.player.setPosition(int(videos_time[videos.index(video_name)]))
        except ValueError:
            pass

    def timerStart(self):
        self.timer.start(200)

    def signalStart(self, content):
        srt = content.canonicalUrl().toLocalFile().split(".")
        srt.pop(-1)
        srt.append("srt")
        srt = ".".join(srt)
        if QFile.exists(srt):
            self.isSubtitle.emit(True)
            self.timer.start(100)
        else:
            self.isSubtitle.emit(False)
            self.timer.stop()

    def timerPos(self):
        self.subtitlePos.emit(self.player.position())

    def playerPlayOrOpen(self, arg=None):
        if type(arg) == list and len(arg) > 1:
            content = QMediaContent(QUrl.fromLocalFile(arg[1]))
            self.player.setMedia(content)
            self.play()

    def addVideo(self, video):
        content = QMediaContent(QUrl.fromLocalFile(video))
        self.player.setMedia(content)
        self.play()

    def addYoutubeVideo(self, video):
        dm = DownloadManager(self)

        content = QMediaContent(dm.addUrl(video))
        self.player.setMedia(content)
        self.play()

    def sliderChanged(self, pos):
        self.player.setPosition(pos)

    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()

    def setMuted(self, mute):
        self.player.setMuted(mute)

    def mutedState(self):
        if self.player.isMuted():
            self.setMuted(False)
        else:
            self.setMuted(True)

    def isMuted(self):
        return  self.player.isMuted()

    def setVolume(self, value):
        self.player.setVolume(value)

    def volume(self):
        return self.player.volume()