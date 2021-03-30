import netifaces

from p3exporter.collector import CollectorBase, CollectorConfig
from prometheus_client.core import CounterMetricFamily, InfoMetricFamily


class NetdevCollector(CollectorBase):

    def __init__(self, config: CollectorConfig):
        """Instanciate a NetdevCollector object."""

        super(NetdevCollector, self).__init__(config)

        self.whitelist = self.opts.pop("whitelist", [])
        self.blacklist = self.opts.pop("blacklist", [])
        self.ifaces = []
        self.iface_stats = {}

    def collect(self):
        """Collect netdev metrics.

        Returns several info, couter and gauge metrics for interfaces.
        """

        self.ifaces = netifaces.interfaces()
        self.iface_stats = _get_iface_stats()

        for iface in self.ifaces:

            if (self.whitelist and iface in self.whitelist) or \
               (self.blacklist and iface not in self.blacklist):

                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    for addr_id, addr in enumerate(addrs[netifaces.AF_INET]):
                        addr['iface'] = iface
                        addr['addr_id'] = str(addr_id)
                        net_dev_v4 = InfoMetricFamily("network_v4", "Network interface information", labels=addr.keys())
                        net_dev_v4.add_metric(labels=addr.keys(), value=addr)
                        yield net_dev_v4

                if netifaces.AF_INET6 in addrs:
                    for addr_id, addr in enumerate(addrs[netifaces.AF_INET6]):
                        addr['iface'] = iface
                        addr['addr_id'] = str(addr_id)
                        net_dev_v6 = InfoMetricFamily("network_v6", "Network interface information", labels=addr.keys())
                        net_dev_v6.add_metric(labels=addr.keys(), value=addr)
                        yield net_dev_v6

                for d in 'tx', 'rx':
                    for k, v in self.iface_stats[iface][d].items():
                        metric_name = "network_{0}_{1}".format(d, k)
                        metric_desc = "{0} {1} interface statistic for {2}".format(d, k, iface)
                        label_names = ['iface']
                        label_values = [iface]
                        iface_stat = CounterMetricFamily(metric_name, metric_desc, labels=label_names)
                        iface_stat.add_metric(labels=label_values, value=v)
                        yield iface_stat


# found on https://git.io/JYeaI
# thanks https://github.com/racerxdl for that fine code.
# has been adapted by us to meet our requirements
def _get_iface_stats():
    """Get interface statistics from proc fs.

    Get interface statistics from proc filesystem and transform it to a dictionary.

    :return: Returns a dict of dicts. One dict for each interface and one key value pair for each interface statistic in the inner dict.
    :rtype: dict
    """

    ifaces = {}
    f = open("/proc/net/dev")
    data = f.read()
    f.close()
    data = data.split("\n")[2:]
    for i in data:
        if len(i.strip()) > 0:
            x = i.split()
            k = {
                x[0][:len( x[0])-1]: {
                    "tx"        :   {
                        "bytes"         :   int(x[1]),
                        "packets"       :   int(x[2]),
                        "errs"          :   int(x[3]),
                        "drop"          :   int(x[4]),
                        "fifo"          :   int(x[5]),
                        "frame"         :   int(x[6]),
                        "compressed"    :   int(x[7]),
                        "multicast"     :   int(x[8])
                    },
                    "rx"        :   {
                        "bytes"         :   int(x[9]),
                        "packets"       :   int(x[10]),
                        "errs"          :   int(x[11]),
                        "drop"          :   int(x[12]),
                        "fifo"          :   int(x[13]),
                        "frame"         :   int(x[14]),
                        "compressed"    :   int(x[15]),
                        "multicast"     :   int(x[16])
                    }
                }
            }
            ifaces.update(k)
    return ifaces
