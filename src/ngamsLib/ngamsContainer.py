#
#    ICRAR - International Centre for Radio Astronomy Research
#    (c) UWA - The University of Western Australia, 2015
#    Copyright by UWA (in the framework of the ICRAR)
#    All rights reserved
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#    MA 02111-1307  USA
#
'''
Contains classes related to the handling of Containers in ngams

@author: rtobar
'''

class ngamsContainer(object):
    """
    A class representing a container.

    A container represents a collection of files, and are tagged
    with a name and an ID. Container IDs are globally unique.
    Containers can also contain other containers, allowing for a hierarchical
    structure of any necessary depth. Containers that are children
    to other containers have a reference to their parent container's ID
    """

    def __init__(self, containerName):
        self._files = []
        self._containers = []
        self._containerName = containerName
        self._parentContainer = None
        self._containerId = None

    def addFile(self, fileName):
        self._files.append(fileName)

    def addContainer(self, container):
        self._containers.append(container)
        container.setParentContainer(self)

    def setParentContainer(self, parentContainer):
        self._parentContainer = parentContainer

    def getFiles(self):
        return self._files[:]

    def getContainers(self):
        return self._containers[:]

    def getContainerName(self):
        return self._containerName

    def setContainerId(self, containerId):
        self._containerId = containerId

    def getContainerId(self):
        return self._containerId

    def getParentContainer(self):
        return self._parentContainer

    def toStr(self, tab):
        spaces = ''.join(' ' for _ in range(tab))
        buf = spaces + self._containerName
        if self._containerId:
            buf += '(id=' + str(self._containerId) + ')'
        buf += ':\n'
        for cont in self._containers:
            buf += spaces + cont.toStr(tab+4) + '\n'
        for filename in self._files:
            buf += spaces + ' - '  + filename + '\n'
        return buf

    def __str__(self, *args, **kwargs):
        return self.toStr(0)
