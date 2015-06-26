#
#    ICRAR - International Centre for Radio Astronomy Research
#    (c) UWA - The University of Western Australia, 2012
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
#******************************************************************************
#
# Who       When        What
# --------  ----------  -------------------------------------------------------
# cwu      26/March/2015  Created

"""
plot the file size distribution
"""
import psycopg2 as dbdrv
import sys, getpass, os, datetime

import numpy as np
import pylab
from pylab import median, mean, where
import matplotlib.pyplot as plt

DB = {'Pawsey':'146.118.87.250', 'MIT':'ngas.mit.edu'}

def queryDb(db='Pawsey', limit=None, saveToCSV=None):
    """
    Return the query result as a numpy array

    saveToCSV:  csv file name (string)
    """
    if (not DB.has_key(db)):
        raise Exception("Unknown db name {0}".format(db))
    # don't want to use group by to relief the database
    if (limit is None):
        sl = ""
    else:
        sl = " limit {0}".format(limit)
    hsql = "select file_size from ngas_files {}".format(sl)
    try:
        t = dbpass
    except NameError:
        dbpass = getpass.getpass('%s DB password: ' % db)
        print "Connecting to DB"
        dbconn = dbdrv.connect(database="ngas", user="ngas_ro",
                             password=dbpass, host=DB[db])

    cur = dbconn.cursor()
    print "Executing query '{0}'".format(hsql)
    cur.execute(hsql)
    r = cur.fetchall()
    dbconn.close()
    del(dbconn)
    res = pylab.array(r)
    ll = len(res)
    res = res[:,0].reshape(ll)
    if (not (saveToCSV is None)):
        f = open(saveToCSV, 'wb')
        for li in res:
            #print "--{0}:{1}".format(int(li), type(int(li)))
            f.write("{0}\n".format(li))

    return res # get the first (only) column from all rows

def queryCSV(csvfile):
    with open(csvfile) as f:
        print "loading records from {0}".format(csvfile)
        re = f.readlines()
        return pylab.array(re)

def plotIt(x, db='Pawsey'):

    x = np.int64(x)
    ttsize = np.sum(x) / 1024.0 ** 5
    ttlen = len(x)
    """
    for xi in x:
        print "{0}:{1}".format(xi, type(xi))
    """
    x[where(x == np.NaN)] = 1
    x[where(x == 0)] = 1
    x = np.log10(x)
    print "caculating the histogram..."
    hist, bins = np.histogram(x, bins=60)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    y2 = hist.astype('float')
    y2 = y2 / np.sum(y2) * 100
    fig = plt.figure()
    dt = datetime.datetime.now()
    timestr = dt.strftime('%Y-%m-%dT%H:%M:%S')
    fig.suptitle("MWA LTA {0} at {3}, # of files: {1}, total size: {2:.2f} PB".format(db,
                                                                                        ttlen,
                                                                                        round(ttsize, 2),
                                                                                        timestr),
                 fontsize=14)
    ax = fig.add_subplot(111)
    ax.set_ylabel('Frequency')
    ax.set_xlabel('log(file size [B])')
    ax.set_yscale('log')
    plt.xticks(np.arange(int(min(center)), int(max(center)) + 1, 1))
    plt.bar(center, hist, align='center', width=width)
    ax2 = ax.twinx()
    ax2.set_ylabel('Frequency %')
    ax2.set_yscale('log')
    ax2.plot(center, y2, color = 'r', linestyle = ':', label = 'percentage')

    ymax = ax.get_ylim()[1]
    ax.vlines(3, 0, ymax, colors = 'k', linestyles=':')
    ax.vlines(6, 0, ymax, colors = 'k', linestyles=':')
    ax.vlines(9, 0, ymax, colors = 'k', linestyles=':')

    ax.text(3, ymax + 100, 'K')
    ax.text(6, ymax + 100, 'M')
    ax.text(9, ymax + 100, 'G')


    plt.show()

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        x = queryDb()
    else:
        csvfile = sys.argv[1]
        if (os.path.exists(csvfile)):
            x = queryCSV(csvfile)
        else:
            x = queryDb(saveToCSV=csvfile)
    plotIt(x)
    raw_input('Press ENTER to continue....')


