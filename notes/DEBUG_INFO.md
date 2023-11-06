# Debug Info

```
jordanz@Jordans-MBP-2:~/Coding/qnap_exporter (convert-to-prom-metrics * u+2)$ docker compose logs qnap_exporter
qnap_exporter  | [2023-11-06 07:53:00 +0000] [7] [INFO] Starting gunicorn 20.1.0
qnap_exporter  | [2023-11-06 07:53:00 +0000] [7] [INFO] Listening at: http://0.0.0.0:1996 (7)
qnap_exporter  | [2023-11-06 07:53:00 +0000] [7] [INFO] Using worker: sync
qnap_exporter  | [2023-11-06 07:53:00 +0000] [9] [INFO] Booting worker with pid: 9
qnap_exporter  | [2023-11-06 07:53:00 +0000] [10] [INFO] Booting worker with pid: 10
qnap_exporter  | [2023-11-06 07:53:00,333] INFO in __init__: registering with SQLALCHEMY_DATABASE_URI: sqlite:////qnap_exporter/app/app.db?check_same_thread=False
qnap_exporter  | [2023-11-06 07:53:00,375] INFO in __init__: registering with SQLALCHEMY_DATABASE_URI: sqlite:////qnap_exporter/app/app.db?check_same_thread=False
qnap_exporter  | [2023-11-06 07:53:02,183] INFO in debug_router: handle debug print route
qnap_exporter  | [2023-11-06 07:53:04,750] INFO in debug_router: system_stats: {'system': {'name': 'SolarisStorage', 'model': 'TS-653D', 'serial_number': 'Q21BI087473', 'temp_c': 38, 'temp_f': 100, 'timezone': '(GMT-08:00) Pacific Time(US &amp; Canada); Tijuana'}, 'firmware': {'version': '5.1.2', 'build': '20230926', 'patch': '0', 'build_time': '2023/09/26'}, 'uptime': {'days': 2, 'hours': 10, 'minutes': 12, 'seconds': 47}, 'cpu': {'model': 'Intel(R) Celeron(R) J4125 CPU @ 2.00GHz', 'usage_percent': 1.6, 'temp_c': 47, 'temp_f': 116}, 'memory': {'total': 7792.0, 'free': 5657.2}, 'nics': {'eth0': {'link_status': 'Up', 'max_speed': 2500, 'ip': '10.0.1.62', 'mask': '255.255.255.0', 'mac': '24:5e:be:6a:7a:81', 'usage': 'DHCP', 'rx_packets': 9148064, 'tx_packets': 5263356, 'err_packets': 0}, 'eth1': {'link_status': 'Down', 'max_speed': 2500, 'ip': '0.0.0.0', 'mask': '0.0.0.0', 'mac': '24:5e:be:6a:7a:82', 'usage': 'DHCP', 'rx_packets': 0, 'tx_packets': 0, 'err_packets': 0}}, 'dns': ['10.0.1.4']}
qnap_exporter  | {'cpu': {'model': 'Intel(R) Celeron(R) J4125 CPU @ 2.00GHz',
qnap_exporter  |          'temp_c': 47,
qnap_exporter  |          'temp_f': 116,
qnap_exporter  |          'usage_percent': 1.6},
qnap_exporter  |  'dns': ['10.0.1.4'],
qnap_exporter  |  'firmware': {'build': '20230926',
qnap_exporter  |               'build_time': '2023/09/26',
qnap_exporter  |               'patch': '0',
qnap_exporter  |               'version': '5.1.2'},
qnap_exporter  |  'memory': {'free': 5657.2, 'total': 7792.0},
qnap_exporter  |  'nics': {'eth0': {'err_packets': 0,
qnap_exporter  |                    'ip': '10.0.1.62',
qnap_exporter  |                    'link_status': 'Up',
qnap_exporter  |                    'mac': '24:5e:be:6a:7a:81',
qnap_exporter  |                    'mask': '255.255.255.0',
qnap_exporter  |                    'max_speed': 2500,
qnap_exporter  |                    'rx_packets': 9148064,
qnap_exporter  |                    'tx_packets': 5263356,
qnap_exporter  |                    'usage': 'DHCP'},
qnap_exporter  |           'eth1': {'err_packets': 0,
qnap_exporter  |                    'ip': '0.0.0.0',
qnap_exporter  |                    'link_status': 'Down',
qnap_exporter  |                    'mac': '24:5e:be:6a:7a:82',
qnap_exporter  |                    'mask': '0.0.0.0',
qnap_exporter  |                    'max_speed': 2500,
qnap_exporter  |                    'rx_packets': 0,
qnap_exporter  |                    'tx_packets': 0,
qnap_exporter  |                    'usage': 'DHCP'}},
qnap_exporter  |  'system': {'model': 'TS-653D',
qnap_exporter  |             'name': 'SolarisStorage',
qnap_exporter  |             'serial_number': 'Q21BI087473',
qnap_exporter  |             'temp_c': 38,
qnap_exporter  |             'temp_f': 100,
qnap_exporter  |             'timezone': '(GMT-08:00) Pacific Time(US &amp; Canada); Tijuana'},
qnap_exporter  |  'uptime': {'days': 2, 'hours': 10, 'minutes': 12, 'seconds': 47}}
qnap_exporter  | [2023-11-06 07:53:05,569] INFO in debug_router: system_health: warning
qnap_exporter  | 'warning'
qnap_exporter  | [2023-11-06 07:53:05,744] INFO in debug_router: bandwidth: {'eth0': {'name': 'Adapter 1', 'rx': 1160, 'tx': 116, 'is_default': False}, 'eth1': {'name': 'Adapter 2', 'rx': 0, 'tx': 0, 'is_default': False}}
qnap_exporter  | {'eth0': {'is_default': False, 'name': 'Adapter 1', 'rx': 1160, 'tx': 116},
qnap_exporter  |  'eth1': {'is_default': False, 'name': 'Adapter 2', 'rx': 0, 'tx': 0}}
qnap_exporter  | [2023-11-06 07:53:06,589] INFO in debug_router: volumes: {'DataVol1': {'id': '1', 'label': 'DataVol1', 'free_size': 531079839744, 'total_size': 1089217155072, 'folders': [{'sharename': 'Public', 'used_size': 8450048}, {'sharename': 'AlphaTest', 'used_size': 519412658176}, {'sharename': 'Multimedia', 'used_size': 2109440}, {'sharename': 'Container', 'used_size': 511930368}, {'sharename': 'Browser Station', 'used_size': 24576}, {'sharename': 'System Reserved', 'used_size': 38292750336}]}, 'MirrorV1': {'id': '2', 'label': 'MirrorV1', 'free_size': 1445745127424, 'total_size': 33814631309312, 'folders': [{'sharename': 'Media', 'used_size': 32366573592576}, {'sharename': 'System Reserved', 'used_size': 40960}]}, 'IvansChildhoodV1': {'id': '3', 'label': 'IvansChildhoodV1', 'free_size': 332002488320, 'total_size': 2188650659840, 'folders': [{'sharename': 'LegacyDrobo', 'used_size': 1247344844800}, {'sharename': 'LeftoverHardDrives', 'used_size': 610179112960}, {'sharename': 'System Reserved', 'used_size': 40960}]}}
qnap_exporter  | {'DataVol1': {'folders': [{'sharename': 'Public', 'used_size': 8450048},
qnap_exporter  |                           {'sharename': 'AlphaTest', 'used_size': 519412658176},
qnap_exporter  |                           {'sharename': 'Multimedia', 'used_size': 2109440},
qnap_exporter  |                           {'sharename': 'Container', 'used_size': 511930368},
qnap_exporter  |                           {'sharename': 'Browser Station', 'used_size': 24576},
qnap_exporter  |                           {'sharename': 'System Reserved',
qnap_exporter  |                            'used_size': 38292750336}],
qnap_exporter  |               'free_size': 531079839744,
qnap_exporter  |               'id': '1',
qnap_exporter  |               'label': 'DataVol1',
qnap_exporter  |               'total_size': 1089217155072},
qnap_exporter  |  'IvansChildhoodV1': {'folders': [{'sharename': 'LegacyDrobo',
qnap_exporter  |                                    'used_size': 1247344844800},
qnap_exporter  |                                   {'sharename': 'LeftoverHardDrives',
qnap_exporter  |                                    'used_size': 610179112960},
qnap_exporter  |                                   {'sharename': 'System Reserved',
qnap_exporter  |                                    'used_size': 40960}],
qnap_exporter  |                       'free_size': 332002488320,
qnap_exporter  |                       'id': '3',
qnap_exporter  |                       'label': 'IvansChildhoodV1',
qnap_exporter  |                       'total_size': 2188650659840},
qnap_exporter  |  'MirrorV1': {'folders': [{'sharename': 'Media', 'used_size': 32366573592576},
qnap_exporter  |                           {'sharename': 'System Reserved', 'used_size': 40960}],
qnap_exporter  |               'free_size': 1445745127424,
qnap_exporter  |               'id': '2',
qnap_exporter  |               'label': 'MirrorV1',
qnap_exporter  |               'total_size': 33814631309312}}
qnap_exporter  | [2023-11-06 07:53:07,074] INFO in debug_router: smart_disk_health: {'0:1': {'drive_number': '0:1', 'health': 'OK', 'temp_c': 49, 'temp_f': 120, 'capacity': '9.10 TB', 'model': 'WD101EFBX-68B0AN0', 'serial': 'VCHYAXMP', 'type': 'hdd'}, '0:2': {'drive_number': '0:2', 'health': 'OK', 'temp_c': 47, 'temp_f': 116, 'capacity': '9.10 TB', 'model': 'WD102KFBX-68M95N0', 'serial': 'VHGBERXM', 'type': 'hdd'}, '0:3': {'drive_number': '0:3', 'health': 'OK', 'temp_c': 39, 'temp_f': 102, 'capacity': '9.10 TB', 'model': 'ST10000VN0008-2PJ103', 'serial': 'ZS50ZTA1', 'type': 'hdd'}, '0:4': {'drive_number': '0:4', 'health': 'OK', 'temp_c': 39, 'temp_f': 102, 'capacity': '9.10 TB', 'model': 'ST10000VN0008-2PJ103', 'serial': 'ZS50ZT60', 'type': 'hdd'}, '0:5': {'drive_number': '0:5', 'health': 'OK', 'temp_c': 39, 'temp_f': 102, 'capacity': '9.10 TB', 'model': 'ST10000NE0004-1ZF101', 'serial': 'ZA28ZSW2', 'type': 'hdd'}, '0:6': {'drive_number': '0:6', 'health': 'OK', 'temp_c': 47, 'temp_f': 116, 'capacity': '9.10 TB', 'model': 'WD101EFAX-68LDBN0', 'serial': 'VCG7DRJN', 'type': 'hdd'}}
qnap_exporter  | {'0:1': {'capacity': '9.10 TB',
qnap_exporter  |          'drive_number': '0:1',
qnap_exporter  |          'health': 'OK',
qnap_exporter  |          'model': 'WD101EFBX-68B0AN0',
qnap_exporter  |          'serial': 'VCHYAXMP',
qnap_exporter  |          'temp_c': 49,
qnap_exporter  |          'temp_f': 120,
qnap_exporter  |          'type': 'hdd'},
qnap_exporter  |  '0:2': {'capacity': '9.10 TB',
qnap_exporter  |          'drive_number': '0:2',
qnap_exporter  |          'health': 'OK',
qnap_exporter  |          'model': 'WD102KFBX-68M95N0',
qnap_exporter  |          'serial': 'VHGBERXM',
qnap_exporter  |          'temp_c': 47,
qnap_exporter  |          'temp_f': 116,
qnap_exporter  |          'type': 'hdd'},
qnap_exporter  |  '0:3': {'capacity': '9.10 TB',
qnap_exporter  |          'drive_number': '0:3',
qnap_exporter  |          'health': 'OK',
qnap_exporter  |          'model': 'ST10000VN0008-2PJ103',
qnap_exporter  |          'serial': 'ZS50ZTA1',
qnap_exporter  |          'temp_c': 39,
qnap_exporter  |          'temp_f': 102,
qnap_exporter  |          'type': 'hdd'},
qnap_exporter  |  '0:4': {'capacity': '9.10 TB',
qnap_exporter  |          'drive_number': '0:4',
qnap_exporter  |          'health': 'OK',
qnap_exporter  |          'model': 'ST10000VN0008-2PJ103',
qnap_exporter  |          'serial': 'ZS50ZT60',
qnap_exporter  |          'temp_c': 39,
qnap_exporter  |          'temp_f': 102,
qnap_exporter  |          'type': 'hdd'},
qnap_exporter  |  '0:5': {'capacity': '9.10 TB',
qnap_exporter  |          'drive_number': '0:5',
qnap_exporter  |          'health': 'OK',
qnap_exporter  |          'model': 'ST10000NE0004-1ZF101',
qnap_exporter  |          'serial': 'ZA28ZSW2',
qnap_exporter  |          'temp_c': 39,
qnap_exporter  |          'temp_f': 102,
qnap_exporter  |          'type': 'hdd'},
qnap_exporter  |  '0:6': {'capacity': '9.10 TB',
qnap_exporter  |          'drive_number': '0:6',
qnap_exporter  |          'health': 'OK',
qnap_exporter  |          'model': 'WD101EFAX-68LDBN0',
qnap_exporter  |          'serial': 'VCG7DRJN',
qnap_exporter  |          'temp_c': 47,
qnap_exporter  |          'temp_f': 116,
qnap_exporter  |          'type': 'hdd'}}
```