import os
import re
import sys

import eigenfaces

class PyFaces:
    def __init__(self,imgsdir,egfnum,thrsh,extn):
        self.imgsdir=imgsdir
        self.threshold=thrsh
        self.egfnum=egfnum
        self.facet= eigenfaces.FaceRec()
        
        self.extn = extn
        self.egfnum = self.set_selected_eigenfaces_count(self.egfnum, extn)
        #print "number of eigenfaces used:",self.egfnum
    
    def train(self):
        """
        Updates the eigenfaces cache.
        """
        self.facet.checkCache(
            self.imgsdir,
            self.extn,
            self.imgnamelist,
            self.egfnum,
            self.threshold)
    
    def match(self, testimg):
        parts = os.path.basename(testimg).split('.')
        extn = parts[len(parts) - 1]
        #print "to match:",testimg," to all ",extn," images in directory:",self.imgsdir
        
        self.facet.checkCache(self.imgsdir,extn,self.imgnamelist,self.egfnum,self.threshold)
        mindist,matchfile = self.facet.findmatchingimage(testimg,self.egfnum,self.threshold)
        if mindist < 1e-10:
            mindist=0
        if matchfile:
            #print "matches :"+matchfile+" dist :"+str(mindist)
            return matchfile,mindist
#        else:
#            print "NOMATCH! try higher threshold"
    
    def match_name(self, testimg):
        matchfile,matchdist = self.match(testimg)
        #print>>sys.stderr, matchfile,matchdist
        match = re.findall("[a-zA-Z_\-]+", os.path.splitext(os.path.split(matchfile)[1])[0])
        if match:
            return match[0], matchdist
        return None, None
    
    def set_selected_eigenfaces_count(self,selected_eigenfaces_count,ext):
        #call eigenfaces.parsefolder() and get imagenamelist
        self.imgnamelist=self.facet.parsefolder(self.imgsdir,ext)
        numimgs=len(self.imgnamelist)
        if(selected_eigenfaces_count >= numimgs or selected_eigenfaces_count == 0):
            selected_eigenfaces_count=numimgs/2
        return selected_eigenfaces_count
        