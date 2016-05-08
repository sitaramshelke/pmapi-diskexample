import sys
from pcp import pmapi
from cpmapi import PM_TYPE_U32
from cpmapi import PM_ERR_VALUE

class TotalRead():
    """It prints the total read operations, summed for all disks"""
    def __init__(self):
        self.context = None
        self.opts = pmapi.pmOptions()
        self.opts.pmSetShortOptions("V?")
        self.opts.pmSetLongOptionHeader("Options")
        self.opts.pmSetLongOptionVersion()
        self.opts.pmSetLongOptionHelp()
    def execute(self):
        if self.context:
            metrics = ('disk.all.read',)
            pmids = self.context.pmLookupName(metrics)
            # print "PMID: ",pmids
            descs = self.context.pmLookupDescs(pmids)
            # print "Desc: ",descs
            result = self.context.pmFetch(pmids)
            if result.contents.numpmid != len(metrics):
                print "Got error here"
                raise pmapi.pmErr(PM_ERR_VALUE)
            atom = self.context.pmExtractValue(
                    result.contents.get_valfmt(0),
                    result.contents.get_vlist(0,0),
                    descs[0].contents.type,
                    PM_TYPE_U32)
            print "Total Disk Reads: ",atom.ul
            self.context.pmFreeResult(result)

    def connect(self):
        """Establish a PMAPI context Local using args """
        self.context = pmapi.pmContext.fromOptions(self.opts,sys.argv)
        if self.context:
            print "Connection Established"


if __name__ == "__main__":
    try:
        tr = TotalRead()
        tr.connect()
        tr.execute()
    except pmapi.pmErr as error:
        print "Error: ",error.message()
    except pmapi.pmUsageErr as usage:
        usage.message()
