from mock import MagicMock
import docker.errors
from requests.exceptions import ConnectionError
import datetime


class ClientMock():

    def __init__(self):
        def __logs(i, stream=False):
            if stream:
                return ("this is line {}".format(l) for l in xrange(1, 100))
            else:
                return "\n".join(["this is line {}".format(l) for l in xrange(1, 3)])

        self.client_node1 = MagicMock()
        self.client_node1.containers = MagicMock(return_value=self.__containers_cmd_return_node1)
        self.client_node1.inspect_container = MagicMock(side_effect=lambda container_id:
                                                        self.__get_container(self.__inspect_container_cmd_return_node1,
                                                                             container_id))
        self.client_node1.create_container = MagicMock(return_value={'Id': 'eba8bea2600029'})
        self.client_node1.start = MagicMock()
        self.client_node1.logs = MagicMock(side_effect=__logs)

        self.client_node2 = MagicMock()
        self.client_node2.containers = MagicMock(return_value=self.__containers_cmd_return_node2)
        self.client_node2.inspect_container = MagicMock(side_effect=lambda container_id:
                                                        self.__get_container(self.__inspect_container_cmd_return_node2,
                                                                             container_id))
        self.client_node2.logs = MagicMock(side_effect=__logs)

        self.client_node3 = MagicMock()
        self.client_node3.containers = MagicMock(side_effect=ConnectionError())
        self.client_node3.inspect_container = MagicMock(side_effect=ConnectionError())
        self.client_node3.logs = MagicMock(side_effect=__logs)

    def mock_two_docker_nodes(self, docker_client):
        docker_client.side_effect = self.__side_effect
        return self.client_node1, self.client_node2, self.client_node3

    def __side_effect(self, base_url, version, timeout):
        if "node-1" in base_url:
            return self.client_node1

        if "node-2" in base_url:
            return self.client_node2

        if "node-3" in base_url:
            return self.client_node3

        raise Exception("{} not mocked".format(base_url))

    def __get_container(self, data, container_id):
        try:
            return data[container_id]
        except KeyError as e:
            raise docker.errors.APIError(e, "dummy", explanation="No such container: {}".format(container_id))

    __containers_cmd_return_node1 = [
        {u'Command': u'/runner/init start web',
            u'Created': 1408697397,
            u'Id': u'656ca7c307d178',
            u'Image': u'hmrc/slugrunner:latest',
            u'Names': [u'/ers-checking-frontend-27'],
            u'Ports': [{u'IP': u'0.0.0.0',
                        u'PrivatePort': 8080,
                        u'PublicPort': 9225,
                        u'Type': u'tcp'}],
            u'Status': u'Up 40 minutes'},
        {u'Command': u'/runner/init start web',
            u'Created': 1408696448,
            u'Id': u'eba8bea2600029',
            u'Image': u'hmrc/slugrunner:latest',
            u'Names': [u'/paye_216'],
            u'Ports': [{u'IP': u'0.0.0.0',
                        u'PrivatePort': 8080,
                        u'PublicPort': 9317,
                        u'Type': u'tcp'}],
            u'Status': u'Up 56 minutes'},
        {u'Command': u'/runner/init start web',
            u'Created': 1406886169,
            u'Id': u'381587e2978216',
            u'Image': u'hmrc/slugrunner:latest',
            u'Names': [u'/ers_5'],
            u'Ports': [],
            u'Status': u'Exited (127) 4 weeks ago'},
        # Weird edge case when docker doesn't fill in the container status
        {u'Command': u'/runner/init start web',
            u'Created': 1406886169,
            u'Id': u'3815178hgdasf6',
            u'Image': u'hmrc/slugrunner:latest',
            u'Names': [u'/ers_5'],
            u'Ports': [],
            u'Status': u''}]

    __containers_cmd_return_node2 = [
        {u'Command': u'/runner/init start web',
            u'Created': 1408687834,
            u'Id': u'80be2a9e62ba00',
            u'Image': u'hmrc/slugrunner:latest',
            u'Names': [u'/paye_216_8020e407-e40a-478e-9f31-a43bb50d8410'],
            u'Ports': [{u'IP': u'0.0.0.0',
                        u'PrivatePort': 8080,
                        u'PublicPort': 9317,
                        u'Type': u'tcp'}],
            u'Status': u'Up 19 minutes'},
        {u'Command': u'/runner/init start web',
            u'Created': 1408696448,
            u'Id': u'jh23899fg00029',
            u'Image': u'hmrc/slugrunner:latest',
            u'Names': [u'/noport_216'],
            u'Ports': [],
            u'Status': u'Up 56 minutes'},
        {u'Command': u'/runner/init start web',
            u'Created': 1408696448,
            u'Id': u'oiwq569fg00029',
            u'Image': u'hmrc/slugrunner:latest',
            u'Names': [u'/wrongport_216'],
            u'Ports': [{u'IP': u'0.0.0.0',
                        u'PrivatePort': 1234,
                        u'PublicPort': 9317,
                        u'Type': u'tcp'}],
            u'Status': u'Up 56 minutes'},
        {u'Command': u'/runner/init start web',
            u'Created': 1409767240,
            u'Id': u'389821jsv78216',
            u'Image': u'hmrc/slugrunner:latest',
            u'Names': [u'/myservice_10'],
            u'Ports': [],
            u'Status': u'Exited (127) 21 hours ago'}]

    __inspect_container_cmd_return_node1 = {
        "381587e2978216": {
            u'Args': [u'start', u'web'],
            u'Config': {u'AttachStderr': False,
                        u'AttachStdin': False,
                        u'AttachStdout': False,
                        u'Cmd': [u'start', u'web'],
                        u'CpuShares': 2,
                        u'Cpuset': u'',
                        u'Domainname': u'',
                        u'Entrypoint': [u'/runner/init'],
                        u'Env': [u'HMRC_CONFIG=-Dapplication.secret=H7dVw$PlJiD)^U,oa4TA1pa]pT:4ETLqbL&2P=n6T~p,A*}^.Y46@PQOV~9(B09Hc]t7-hsf~&@w=zH -Dapplication.log=INFO -Dlogger.resource=/application-json-logger.xml -Dhttp.port=8080 -Dgovuk-tax.Prod.google-analytics.token=UA-00000000-0 -Drun.mode=Prod -Dsession.secure=true -Dsession.httpOnly=true -Dcookie.encryption.key=fqpLDZ4smuDsekHkrEBlCA==',
                                 u'JAVA_OPTS=-Xmx256m -Xms256m',
                                 u'SLUG_URL=https://host/ers-checking-frontend_27.tgz',
                                 u'PORT=8080',
                                 u'HOME=/',
                                 u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'],
                        u'ExposedPorts': {u'8080/tcp': {}},
                        u'Hostname': u'656ca7c307d1',
                        u'Image': u'hmrc/slugrunner',
                        u'Memory': 0,
                        u'MemorySwap': 0,
                        u'NetworkDisabled': False,
                        u'OnBuild': None,
                        u'OpenStdin': False,
                        u'PortSpecs': None,
                        u'StdinOnce': False,
                        u'Tty': False,
                        u'User': u'',
                        u'Volumes': None,
                        u'WorkingDir': u''},
            u'Created': u'2014-08-22T08:49:57.80805632Z',
            u'Driver': u'aufs',
            u'ExecDriver': u'native-0.2',
            u'HostConfig': {u'Binds': None,
                            u'ContainerIDFile': u'',
                            u'Dns': None,
                            u'DnsSearch': None,
                            u'Links': None,
                            u'LxcConf': [],
                            u'NetworkMode': u'bridge',
                            u'PortBindings': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                             u'HostPort': u'9225'}]},
                            u'Privileged': False,
                            u'PublishAllPorts': False,
                            u'VolumesFrom': None},
            u'HostnamePath': u'/var/lib/docker/containers/381587e2978216/hostname',
            u'HostsPath': u'/var/lib/docker/containers/381587e2978216/hosts',
            u'Id': u'381587e2978216',
            u'Image': u'c0cd53268e0c7c42bac84b6bf4f51561720c33f5239aa809f1135cc69cc73a2a',
            u'MountLabel': u'',
            u'Name': u'/ers-checking-frontend-27',
            u'NetworkSettings': {u'Bridge': u'docker0',
                                 u'Gateway': u'172.17.42.1',
                                 u'IPAddress': u'172.17.3.224',
                                 u'IPPrefixLen': 16,
                                 u'PortMapping': None,
                                 u'Ports': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                           u'HostPort': u'9225'}]}},
            u'Path': u'/runner/init',
            u'ProcessLabel': u'',
            u'ResolvConfPath': u'/etc/resolv.conf',
            u'State': {u'ExitCode': 127,
                       # This date format tests the fact that datetime wants microseconds but docker returns a higher granularity.
                       u'FinishedAt': "{}1234Z".format((datetime.datetime.now() - datetime.timedelta(days=1, minutes=10)).strftime('%Y-%m-%dT%H:%M:%S.%f')),
                       u'Paused': False,
                       u'Pid': 35327,
                       u'Running': False,
                       u'StartedAt': u'2014-09-02T08:49:57.906207449Z'},
            u'Volumes': {},
            u'VolumesRW': {}},
        "3815178hgdasf6": {
            u'Args': [u'start', u'web'],
            u'Config': {u'AttachStderr': False,
                        u'AttachStdin': False,
                        u'AttachStdout': False,
                        u'Cmd': [u'start', u'web'],
                        u'CpuShares': 2,
                        u'Cpuset': u'',
                        u'Domainname': u'',
                        u'Entrypoint': [u'/runner/init'],
                        u'Env': [u'HMRC_CONFIG=-Dapplication.secret=H7dVw$PlJiD)^U,oa4TA1pa]pT:4ETLqbL&2P=n6T~p,A*}^.Y46@PQOV~9(B09Hc]t7-hsf~&@w=zH -Dapplication.log=INFO -Dlogger.resource=/application-json-logger.xml -Dhttp.port=8080 -Dgovuk-tax.Prod.google-analytics.token=UA-00000000-0 -Drun.mode=Prod -Dsession.secure=true -Dsession.httpOnly=true -Dcookie.encryption.key=fqpLDZ4smuDsekHkrEBlCA==',
                                 u'JAVA_OPTS=-Xmx256m -Xms256m',
                                 u'SLUG_URL=https://host/ers-checking-frontend_27.tgz',
                                 u'PORT=8080',
                                 u'HOME=/',
                                 u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'],
                        u'ExposedPorts': {u'8080/tcp': {}},
                        u'Hostname': u'656ca7c307d1',
                        u'Image': u'hmrc/slugrunner',
                        u'Memory': 0,
                        u'MemorySwap': 0,
                        u'NetworkDisabled': False,
                        u'OnBuild': None,
                        u'OpenStdin': False,
                        u'PortSpecs': None,
                        u'StdinOnce': False,
                        u'Tty': False,
                        u'User': u'',
                        u'Volumes': None,
                        u'WorkingDir': u''},
            u'Created': u'2014-08-22T08:49:57.80805632Z',
            u'Driver': u'aufs',
            u'ExecDriver': u'native-0.2',
            u'HostConfig': {u'Binds': None,
                            u'ContainerIDFile': u'',
                            u'Dns': None,
                            u'DnsSearch': None,
                            u'Links': None,
                            u'LxcConf': [],
                            u'NetworkMode': u'bridge',
                            u'PortBindings': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                             u'HostPort': u'9225'}]},
                            u'Privileged': False,
                            u'PublishAllPorts': False,
                            u'VolumesFrom': None},
            u'HostnamePath': u'/var/lib/docker/containers/3815178hgdasf6/hostname',
            u'HostsPath': u'/var/lib/docker/containers/3815178hgdasf6/hosts',
            u'Id': u'3815178hgdasf6',
            u'Image': u'c0cd53268e0c7c42bac84b6bf4f51561720c33f5239aa809f1135cc69cc73a2a',
            u'MountLabel': u'',
            u'Name': u'/ers-checking-frontend-27',
            u'NetworkSettings': {u'Bridge': u'docker0',
                                 u'Gateway': u'172.17.42.1',
                                 u'IPAddress': u'172.17.3.224',
                                 u'IPPrefixLen': 16,
                                 u'PortMapping': None,
                                 u'Ports': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                           u'HostPort': u'9225'}]}},
            u'Path': u'/runner/init',
            u'ProcessLabel': u'',
            u'ResolvConfPath': u'/etc/resolv.conf',
            u'State': {u'ExitCode': 127,
                       # This date format tests the fact that datetime wants microseconds but docker returns a higher granularity.
                       u'FinishedAt': "{}1234Z".format((datetime.datetime.now() - datetime.timedelta(days=1, minutes=10)).strftime('%Y-%m-%dT%H:%M:%S.%f')),
                       u'Paused': False,
                       u'Pid': 35327,
                       u'Running': False,
                       u'StartedAt': u'2014-09-02T08:49:57.906207449Z'},
            u'Volumes': {},
            u'VolumesRW': {}},
        "656ca7c307d178": {
            u'Args': [u'start', u'web'],
            u'Config': {u'AttachStderr': False,
                        u'AttachStdin': False,
                        u'AttachStdout': False,
                        u'Cmd': [u'start', u'web'],
                        u'CpuShares': 2,
                        u'Cpuset': u'',
                        u'Domainname': u'',
                        u'Entrypoint': [u'/runner/init'],
                        u'Env': [u'HMRC_CONFIG=-Dapplication.secret=H7dVw$PlJiD)^U,oa4TA1pa]pT:4ETLqbL&2P=n6T~p,A*}^.Y46@PQOV~9(B09Hc]t7-hsf~&@w=zH -Dapplication.log=INFO -Dlogger.resource=/application-json-logger.xml -Dhttp.port=8080 -Dgovuk-tax.Prod.google-analytics.token=UA-00000000-0 -Drun.mode=Prod -Dsession.secure=true -Dsession.httpOnly=true -Dcookie.encryption.key=fqpLDZ4smuDsekHkrEBlCA==',
                                 u'JAVA_OPTS=-Xmx256m -Xms256m',
                                 u'SLUG_URL=https://host/ers-checking-frontend_27.tgz',
                                 u'PORT=8080',
                                 u'HOME=/',
                                 u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'],
                        u'ExposedPorts': {u'8080/tcp': {}},
                        u'Hostname': u'656ca7c307d1',
                        u'Image': u'hmrc/slugrunner',
                        u'Memory': 0,
                        u'MemorySwap': 0,
                        u'NetworkDisabled': False,
                        u'OnBuild': None,
                        u'OpenStdin': False,
                        u'PortSpecs': None,
                        u'StdinOnce': False,
                        u'Tty': False,
                        u'User': u'',
                        u'Volumes': None,
                        u'WorkingDir': u''},
            u'Created': u'2014-08-22T08:49:57.80805632Z',
            u'Driver': u'aufs',
            u'ExecDriver': u'native-0.2',
            u'HostConfig': {u'Binds': None,
                            u'ContainerIDFile': u'',
                            u'Dns': None,
                            u'DnsSearch': None,
                            u'Links': None,
                            u'LxcConf': [],
                            u'NetworkMode': u'bridge',
                            u'PortBindings': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                             u'HostPort': u'9225'}]},
                            u'Privileged': False,
                            u'PublishAllPorts': False,
                            u'VolumesFrom': None},
            u'HostnamePath': u'/var/lib/docker/containers/656ca7c307d178/hostname',
            u'HostsPath': u'/var/lib/docker/containers/656ca7c307d178/hosts',
            u'Id': u'656ca7c307d178',
            u'Image': u'c0cd53268e0c7c42bac84b6bf4f51561720c33f5239aa809f1135cc69cc73a2a',
            u'MountLabel': u'',
            u'Name': u'/ers-checking-frontend-27',
            u'NetworkSettings': {u'Bridge': u'docker0',
                                 u'Gateway': u'172.17.42.1',
                                 u'IPAddress': u'172.17.3.224',
                                 u'IPPrefixLen': 16,
                                 u'PortMapping': None,
                                 u'Ports': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                           u'HostPort': u'9225'}]}},
            u'Path': u'/runner/init',
            u'ProcessLabel': u'',
            u'ResolvConfPath': u'/etc/resolv.conf',
            u'State': {u'ExitCode': 0,
                       u'FinishedAt': u'0001-01-01T00:00:00Z',
                       u'Paused': False,
                       u'Pid': 35327,
                       u'Running': True,
                       u'StartedAt': u'2014-08-22T08:49:57.906207449Z'},
            u'Volumes': {},
            u'VolumesRW': {}},
        "eba8bea2600029": {
            u'Args': [u'start', u'web'],
            u'Config': {u'AttachStderr': False,
                        u'AttachStdin': False,
                        u'AttachStdout': False,
                        u'Cmd': [u'start', u'web'],
                        u'CpuShares': 2,
                        u'Cpuset': u'',
                        u'Domainname': u'',
                        u'Entrypoint': [u'/runner/init'],
                        u'Env': [u'HMRC_CONFIG=-Dapplication.log=INFO -Drun.mode=Prod -Dlogger.resource=/application-json-logger.xml -Dhttp.port=8080',
                                 u'JAVA_OPTS=-Xmx256m -Xms256m',
                                 u'SLUG_URL=https://host/paye_216.tgz',
                                 u'PORT=8080',
                                 u'HOME=/',
                                 u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'],
                        u'ExposedPorts': {u'8080/tcp': {}},
                        u'Hostname': u'eba8bea26000',
                        u'Image': u'hmrc/slugrunner',
                        u'Memory': 0,
                        u'MemorySwap': 0,
                        u'NetworkDisabled': False,
                        u'OnBuild': None,
                        u'OpenStdin': False,
                        u'PortSpecs': None,
                        u'StdinOnce': False,
                        u'Tty': False,
                        u'User': u'',
                        u'Volumes': None,
                        u'WorkingDir': u''},
            u'Created': u'2014-08-22T08:34:08.134031634Z',
            u'Driver': u'aufs',
            u'ExecDriver': u'native-0.2',
            u'HostConfig': {u'Binds': None,
                            u'ContainerIDFile': u'',
                            u'Dns': None,
                            u'DnsSearch': None,
                            u'Links': None,
                            u'LxcConf': [],
                            u'NetworkMode': u'bridge',
                            u'PortBindings': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                             u'HostPort': u'9317'}]},
                            u'Privileged': False,
                            u'PublishAllPorts': False,
                            u'VolumesFrom': None},
            u'HostnamePath': u'/var/lib/docker/containers/eba8bea2600029/hostname',
            u'HostsPath': u'/var/lib/docker/containers/eba8bea2600029/hosts',
            u'Id': u'eba8bea2600029',
            u'Image': u'c0cd53268e0c7c42bac84b6bf4f51561720c33f5239aa809f1135cc69cc73a2a',
            u'MountLabel': u'',
            u'Name': u'/paye_216',
            u'NetworkSettings': {u'Bridge': u'docker0',
                                 u'Gateway': u'172.17.42.1',
                                 u'IPAddress': u'172.17.3.221',
                                 u'IPPrefixLen': 16,
                                 u'PortMapping': None,
                                 u'Ports': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                           u'HostPort': u'9317'}]}},
            u'Path': u'/runner/init',
            u'ProcessLabel': u'',
            u'ResolvConfPath': u'/etc/resolv.conf',
            u'State': {u'ExitCode': 0,
                       u'FinishedAt': u'0001-01-01T00:00:00Z',
                       u'Paused': False,
                       u'Pid': 30996,
                       u'Running': True,
                       u'StartedAt': u'2014-08-22T08:34:08.260419303Z'},
            u'Volumes': {},
            u'VolumesRW': {}}
    }

    __inspect_container_cmd_return_node2 = {
        "389821jsv78216": {
            u'Args': [u'start', u'web'],
            u'Config': {u'AttachStderr': False,
                        u'AttachStdin': False,
                        u'AttachStdout': False,
                        u'Cmd': [u'start', u'web'],
                        u'CpuShares': 2,
                        u'Cpuset': u'',
                        u'Domainname': u'',
                        u'Entrypoint': [u'/runner/init'],
                        u'Env': [u'HMRC_CONFIG=-Dapplication.secret=H7dVw$PlJiD)^U,oa4TA1pa]pT:4ETLqbL&2P=n6T~p,A*}^.Y46@PQOV~9(B09Hc]t7-hsf~&@w=zH -Dapplication.log=INFO -Dlogger.resource=/application-json-logger.xml -Dhttp.port=8080 -Dgovuk-tax.Prod.google-analytics.token=UA-00000000-0 -Drun.mode=Prod -Dsession.secure=true -Dsession.httpOnly=true -Dcookie.encryption.key=fqpLDZ4smuDsekHkrEBlCA==',
                                 u'JAVA_OPTS=-Xmx256m -Xms256m',
                                 u'SLUG_URL=https://host/ers-checking-frontend_27.tgz',
                                 u'PORT=8080',
                                 u'HOME=/',
                                 u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'],
                        u'ExposedPorts': {u'8080/tcp': {}},
                        u'Hostname': u'656ca7c307d1',
                        u'Image': u'hmrc/slugrunner',
                        u'Memory': 0,
                        u'MemorySwap': 0,
                        u'NetworkDisabled': False,
                        u'OnBuild': None,
                        u'OpenStdin': False,
                        u'PortSpecs': None,
                        u'StdinOnce': False,
                        u'Tty': False,
                        u'User': u'',
                        u'Volumes': None,
                        u'WorkingDir': u''},
            u'Created': u'2014-08-22T08:49:57.80805632Z',
            u'Driver': u'aufs',
            u'ExecDriver': u'native-0.2',
            u'HostConfig': {u'Binds': None,
                            u'ContainerIDFile': u'',
                            u'Dns': None,
                            u'DnsSearch': None,
                            u'Links': None,
                            u'LxcConf': [],
                            u'NetworkMode': u'bridge',
                            u'PortBindings': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                             u'HostPort': u'9225'}]},
                            u'Privileged': False,
                            u'PublishAllPorts': False,
                            u'VolumesFrom': None},
            u'HostnamePath': u'/var/lib/docker/containers/389821jsv78216/hostname',
            u'HostsPath': u'/var/lib/docker/containers/389821jsv78216/hosts',
            u'Id': u'389821jsv78216',
            u'Image': u'c0cd53268e0c7c42bac84b6bf4f51561720c33f5239aa809f1135cc69cc73a2a',
            u'MountLabel': u'',
            u'Name': u'/ers-checking-frontend-27',
            u'NetworkSettings': {u'Bridge': u'docker0',
                                 u'Gateway': u'172.17.42.1',
                                 u'IPAddress': u'172.17.3.224',
                                 u'IPPrefixLen': 16,
                                 u'PortMapping': None,
                                 u'Ports': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                           u'HostPort': u'9225'}]}},
            u'Path': u'/runner/init',
            u'ProcessLabel': u'',
            u'ResolvConfPath': u'/etc/resolv.conf',
            u'State': {u'ExitCode': 127,
                       u'FinishedAt': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                       u'Paused': False,
                       u'Pid': 35327,
                       u'Running': False,
                       u'StartedAt': u'2014-09-03T17:49:57.906207449Z'},
            u'Volumes': {},
            u'VolumesRW': {}},
        "80be2a9e62ba00": {
            u'Args': [u'start', u'web'],
            u'Config': {u'AttachStderr': False,
                        u'AttachStdin': False,
                        u'AttachStdout': False,
                        u'Cmd': [u'start', u'web'],
                        u'CpuShares': 2,
                        u'Cpuset': u'',
                        u'Domainname': u'',
                        u'Entrypoint': [u'/runner/init'],
                        u'Env': [u'HMRC_CONFIG=-Dapplication.log=INFO -Drun.mode=Prod -Dlogger.resource=/application-json-logger.xml -Dhttp.port=8080',
                                 u'JAVA_OPTS=-Xmx256m -Xms256m',
                                 u'SLUG_URL=http://example.com/paye/paye_216.tgz',
                                 u'PORT=8080',
                                 u'HOME=/',
                                 u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'],
                        u'ExposedPorts': {u'8080/tcp': {}},
                        u'Hostname': u'80be2a9e62ba',
                        u'Image': u'hmrc/slugrunner',
                        u'Memory': 0,
                        u'MemorySwap': 0,
                        u'NetworkDisabled': False,
                        u'OnBuild': None,
                        u'OpenStdin': False,
                        u'PortSpecs': None,
                        u'StdinOnce': False,
                        u'Tty': False,
                        u'User': u'',
                        u'Volumes': None,
                        u'WorkingDir': u''},
            u'Created': u'2014-08-22T08:33:11.343161034Z',
            u'Driver': u'aufs',
            u'ExecDriver': u'native-0.2',
            u'HostConfig': {u'Binds': None,
                            u'ContainerIDFile': u'',
                            u'Dns': None,
                            u'DnsSearch': None,
                            u'Links': None,
                            u'LxcConf': [],
                            u'NetworkMode': u'bridge',
                            u'PortBindings': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                             u'HostPort': u'9317'}]},
                            u'Privileged': False,
                            u'PublishAllPorts': False,
                            u'VolumesFrom': None},
            u'HostnamePath': u'/var/lib/docker/containers/80be2a9e62ba00/hostname',
            u'HostsPath': u'/var/lib/docker/containers/80be2a9e62ba00/hosts',
            u'Id': u'80be2a9e62ba00',
            u'Image': u'c0cd53268e0c7c42bac84b6bf4f51561720c33f5239aa809f1135cc69cc73a2a',
            u'MountLabel': u'',
            u'Name': u'/paye_216_8020e407-e40a-478e-9f31-a43bb50d8410',
            u'NetworkSettings': {u'Bridge': u'docker0',
                                 u'Gateway': u'172.17.42.1',
                                 u'IPAddress': u'172.17.3.221',
                                 u'IPPrefixLen': 16,
                                 u'PortMapping': None,
                                 u'Ports': {u'8080/tcp': [{u'HostIp': u'0.0.0.0',
                                                           u'HostPort': u'9317'}]}},
            u'Path': u'/runner/init',
            u'ProcessLabel': u'',
            u'ResolvConfPath': u'/etc/resolv.conf',
            u'State': {u'ExitCode': 0,
                       u'FinishedAt': u'0001-01-01T00:00:00Z',
                       u'Paused': False,
                       u'Pid': 30996,
                       u'Running': True,
                       u'StartedAt': u'2014-08-22T08:33:39.241960303Z'},
            u'Volumes': {},
            u'VolumesRW': {}}
    }
