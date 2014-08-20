from rucio.client.dq2client import DQ2Client
import rucio.client.client as client
#print dq2.listDatasetsByNameInSite('RUCIO-DPM01_TWGRIDSCRATCHDISK')
#print dq2.listDatasetsByNameInSite('TW-EOS00_TWGRIDSCRATCHDISK')
#print dq2.listDatasetsByNameInSite('TW-DPM01_AMS02DATADISK')
def lDBNIS(site, complete=None, name=None, p=None, rpp=None, group=None):
        """
        List datasets at site

        @param site: is the location to be searched for.
        @param complete: is the location state of the dataset at a site and may have
            the following values: None: in which case the
            location state is ignore; LocationState.COMPLETE: lists only datasets
            fully present at the site (no files missing);
            LocationState.INCOMPLETE: lists only datasets partially present at the
            site (some files missing).
        @param page: is the page to be displayed.
        @param rpp: are the results per page.
        @param group: Not used

        B{Exceptions:}
            - RSENotFound is raised in case the site doesn't exist.

        @return: Tuple of dataset.
            ('dsn1', 'dsn2'... )
        """
        result = []
        pattern = None
        if name:
            pattern = string.replace(name, '*', '.*')
        for did in client.get_dataset_locks_by_rse(site):
            scope = did['scope']
            dsn = did['name']
            state = did['state']
            if pattern:
                if re.match(pattern, dsn):
                    match = True
                else:
                    match = False
            else:
                match = True
            if complete == 1:
                if state == 'OK' and match:
                    result.append('%s:%s' % (scope, dsn))
            elif complete == 0:
                if state != 'OK' and match:
                    result.append('%s:%s' % (scope, dsn))
            elif match:
                result.append('%s:%s' % (scope, dsn))
        return tuple(result)


site = 'TW-DPM01_AMS02DATADISK'
DQ2Client.listDatasetsByNameInSite = lDBNIS
dq2 = DQ2Client()
print dq2.listDatasetsByNameInSite(site)
