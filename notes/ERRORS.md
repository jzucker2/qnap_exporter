# Errors

## To Do

- [ ] simple retry (with `tenacity`)
- [ ] network timeouts
- [ ] invalid JSON
- [ ] reset metrics to 0 when failing to get data (so graphs can dip appropriately)

## Debug Data

```
qnap_exporter  | [2023-11-10 01:20:00,022] INFO in exporter: fetching all domains stats for last_updated: 2023-11-10 01:20:00.022104
qnap_exporter  | [2023-11-10 01:20:04,929] INFO in exporter: updating metrics for domain: Domains.SYSTEM_STATS
qnap_exporter  | [2023-11-10 01:20:04,929] INFO in exporter: updating metrics for domain: Domains.BANDWIDTH
qnap_exporter  | [2023-11-10 01:20:04,930] INFO in exporter: updating metrics for domain: Domains.VOLUMES
qnap_exporter  | [2023-11-10 01:20:04,930] INFO in exporter: updating metrics for domain: Domains.SMART_DISK_HEALTH
qnap_exporter  | [2023-11-10 01:20:04,931] INFO in exporter: updating metrics for domain: Domains.SYSTEM_HEALTH
qnap_exporter  | [2023-11-10 01:21:00,008] INFO in exporter: fetching all domains stats for last_updated: 2023-11-10 01:21:00.008892
qnap_exporter  | [2023-11-10 01:21:04,887] INFO in exporter: updating metrics for domain: Domains.SYSTEM_STATS
qnap_exporter  | [2023-11-10 01:21:04,890] INFO in exporter: updating metrics for domain: Domains.BANDWIDTH
qnap_exporter  | [2023-11-10 01:21:04,890] INFO in exporter: updating metrics for domain: Domains.VOLUMES
qnap_exporter  | [2023-11-10 01:21:04,891] INFO in exporter: updating metrics for domain: Domains.SMART_DISK_HEALTH
qnap_exporter  | [2023-11-10 01:21:04,892] INFO in exporter: updating metrics for domain: Domains.SYSTEM_HEALTH
qnap_exporter  | [2023-11-10 01:22:00,056] INFO in exporter: fetching all domains stats for last_updated: 2023-11-10 01:22:00.052559
qnap_exporter  | Job "perform_qnap_metrics_update (trigger: interval[0:01:00], next run at: 2023-11-10 01:23:00 UTC)" raised an exception
qnap_exporter  | Traceback (most recent call last):
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connection.py", line 174, in _new_conn
qnap_exporter  |     conn = connection.create_connection(
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/util/connection.py", line 95, in create_connection
qnap_exporter  |     raise err
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/util/connection.py", line 85, in create_connection
qnap_exporter  |     sock.connect(sa)
qnap_exporter  | TimeoutError: timed out
qnap_exporter  | 
qnap_exporter  | During handling of the above exception, another exception occurred:
qnap_exporter  | 
qnap_exporter  | Traceback (most recent call last):
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 703, in urlopen
qnap_exporter  |     httplib_response = self._make_request(
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 398, in _make_request
qnap_exporter  |     conn.request(method, url, **httplib_request_kw)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connection.py", line 239, in request
qnap_exporter  |     super(HTTPConnection, self).request(method, url, body=body, headers=headers)
qnap_exporter  |   File "/usr/local/lib/python3.10/http/client.py", line 1283, in request
qnap_exporter  |     self._send_request(method, url, body, headers, encode_chunked)
qnap_exporter  |   File "/usr/local/lib/python3.10/http/client.py", line 1329, in _send_request
qnap_exporter  |     self.endheaders(body, encode_chunked=encode_chunked)
qnap_exporter  |   File "/usr/local/lib/python3.10/http/client.py", line 1278, in endheaders
qnap_exporter  |     self._send_output(message_body, encode_chunked=encode_chunked)
qnap_exporter  |   File "/usr/local/lib/python3.10/http/client.py", line 1038, in _send_output
qnap_exporter  |     self.send(msg)
qnap_exporter  |   File "/usr/local/lib/python3.10/http/client.py", line 976, in send
qnap_exporter  |     self.connect()
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connection.py", line 205, in connect
qnap_exporter  |     conn = self._new_conn()
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connection.py", line 179, in _new_conn
qnap_exporter  |     raise ConnectTimeoutError(
qnap_exporter  | urllib3.exceptions.ConnectTimeoutError: (<urllib3.connection.HTTPConnection object at 0xffff8b579ab0>, 'Connection to 10.0.1.1 timed out. (connect timeout=5)')
qnap_exporter  | 
qnap_exporter  | During handling of the above exception, another exception occurred:
qnap_exporter  | 
qnap_exporter  | Traceback (most recent call last):
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/requests/adapters.py", line 489, in send
qnap_exporter  |     resp = conn.urlopen(
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 787, in urlopen
qnap_exporter  |     retries = retries.increment(
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/util/retry.py", line 592, in increment
qnap_exporter  |     raise MaxRetryError(_pool, url, error or ResponseError(cause))
qnap_exporter  | urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='10.0.1.1', port=8080): Max retries exceeded with url: /cgi-bin/authLogin.cgi (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0xffff8b579ab0>, 'Connection to 10.0.1.1 timed out. (connect timeout=5)'))
qnap_exporter  | 
qnap_exporter  | During handling of the above exception, another exception occurred:
qnap_exporter  | 
qnap_exporter  | Traceback (most recent call last):
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/apscheduler/executors/base.py", line 125, in run_job
qnap_exporter  |     retval = job.func(*job.args, **job.kwargs)
qnap_exporter  |   File "/qnap_exporter/app/tasks/qnap.py", line 37, in perform_qnap_metrics_update
qnap_exporter  |     response = router.handle_exporter_metrics_update_route_response()
qnap_exporter  |   File "<decorator-gen-2>", line 2, in handle_exporter_metrics_update_route_response
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/prometheus_client/context_managers.py", line 81, in wrapped
qnap_exporter  |     return func(*args, **kwargs)
qnap_exporter  |   File "/qnap_exporter/app/routers/exporter_router.py", line 40, in handle_exporter_metrics_update_route_response
qnap_exporter  |     self.exporter.fetch_all_domains_stats()
qnap_exporter  |   File "/qnap_exporter/app/clients/exporter.py", line 82, in fetch_all_domains_stats
qnap_exporter  |     domain_stats.update_stats(last_updated=last_updated)
qnap_exporter  |   File "/qnap_exporter/app/clients/domain_stats.py", line 74, in update_stats
qnap_exporter  |     updated_stats = self._domain_func()
qnap_exporter  |   File "/qnap_exporter/app/clients/qnap_client.py", line 46, in get_system_stats
qnap_exporter  |     return self.client.get_system_stats()
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/qnapstats/qnap_stats.py", line 217, in get_system_stats
qnap_exporter  |     resp = self._get_url(
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/qnapstats/qnap_stats.py", line 74, in _get_url
qnap_exporter  |     self._init_session()
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/qnapstats/qnap_stats.py", line 50, in _init_session
qnap_exporter  |     if self._login() is False:
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/qnapstats/qnap_stats.py", line 58, in _login
qnap_exporter  |     result = self._execute_post_url("authLogin.cgi", data, False)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/qnapstats/qnap_stats.py", line 104, in _execute_post_url
qnap_exporter  |     resp = self._session.post(url, data, timeout=self._timeout, verify=self._verify_ssl)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/requests/sessions.py", line 635, in post
qnap_exporter  |     return self.request("POST", url, data=data, json=json, **kwargs)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/requests/sessions.py", line 587, in request
qnap_exporter  |     resp = self.send(prep, **send_kwargs)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/requests/sessions.py", line 701, in send
qnap_exporter  |     r = adapter.send(request, **kwargs)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/requests/adapters.py", line 553, in send
qnap_exporter  |     raise ConnectTimeout(e, request=request)
qnap_exporter  | requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='10.0.1.1', port=8080): Max retries exceeded with url: /cgi-bin/authLogin.cgi (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0xffff8b579ab0>, 'Connection to 10.0.1.1 timed out. (connect timeout=5)'))
qnap_exporter  | [2023-11-10 01:23:00,008] INFO in exporter: fetching all domains stats for last_updated: 2023-11-10 01:23:00.008062
qnap_exporter  | Job "perform_qnap_metrics_update (trigger: interval[0:01:00], next run at: 2023-11-10 01:24:00 UTC)" raised an exception
qnap_exporter  | Traceback (most recent call last):
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connection.py", line 174, in _new_conn
qnap_exporter  |     conn = connection.create_connection(
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/util/connection.py", line 95, in create_connection
qnap_exporter  |     raise err
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/util/connection.py", line 85, in create_connection
qnap_exporter  |     sock.connect(sa)
qnap_exporter  | TimeoutError: timed out
qnap_exporter  | 
qnap_exporter  | During handling of the above exception, another exception occurred:
qnap_exporter  | 
qnap_exporter  | Traceback (most recent call last):
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 703, in urlopen
qnap_exporter  |     httplib_response = self._make_request(
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 398, in _make_request
qnap_exporter  |     conn.request(method, url, **httplib_request_kw)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connection.py", line 239, in request
qnap_exporter  |     super(HTTPConnection, self).request(method, url, body=body, headers=headers)
qnap_exporter  |   File "/usr/local/lib/python3.10/http/client.py", line 1283, in request
qnap_exporter  |     self._send_request(method, url, body, headers, encode_chunked)
qnap_exporter  |   File "/usr/local/lib/python3.10/http/client.py", line 1329, in _send_request
qnap_exporter  |     self.endheaders(body, encode_chunked=encode_chunked)
qnap_exporter  |   File "/usr/local/lib/python3.10/http/client.py", line 1278, in endheaders
qnap_exporter  |     self._send_output(message_body, encode_chunked=encode_chunked)
qnap_exporter  |   File "/usr/local/lib/python3.10/http/client.py", line 1038, in _send_output
qnap_exporter  |     self.send(msg)
qnap_exporter  |   File "/usr/local/lib/python3.10/http/client.py", line 976, in send
qnap_exporter  |     self.connect()
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connection.py", line 205, in connect
qnap_exporter  |     conn = self._new_conn()
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connection.py", line 179, in _new_conn
qnap_exporter  |     raise ConnectTimeoutError(
qnap_exporter  | urllib3.exceptions.ConnectTimeoutError: (<urllib3.connection.HTTPConnection object at 0xffff8b5792d0>, 'Connection to 10.0.1.1 timed out. (connect timeout=5)')
qnap_exporter  | 
qnap_exporter  | During handling of the above exception, another exception occurred:
qnap_exporter  | 
qnap_exporter  | Traceback (most recent call last):
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/requests/adapters.py", line 489, in send
qnap_exporter  |     resp = conn.urlopen(
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/connectionpool.py", line 787, in urlopen
qnap_exporter  |     retries = retries.increment(
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/urllib3/util/retry.py", line 592, in increment
qnap_exporter  |     raise MaxRetryError(_pool, url, error or ResponseError(cause))
qnap_exporter  | urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='10.0.1.1', port=8080): Max retries exceeded with url: /cgi-bin/authLogin.cgi (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0xffff8b5792d0>, 'Connection to 10.0.1.1 timed out. (connect timeout=5)'))
qnap_exporter  | 
qnap_exporter  | During handling of the above exception, another exception occurred:
qnap_exporter  | 
qnap_exporter  | Traceback (most recent call last):
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/apscheduler/executors/base.py", line 125, in run_job
qnap_exporter  |     retval = job.func(*job.args, **job.kwargs)
qnap_exporter  |   File "/qnap_exporter/app/tasks/qnap.py", line 37, in perform_qnap_metrics_update
qnap_exporter  |     response = router.handle_exporter_metrics_update_route_response()
qnap_exporter  |   File "<decorator-gen-2>", line 2, in handle_exporter_metrics_update_route_response
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/prometheus_client/context_managers.py", line 81, in wrapped
qnap_exporter  |     return func(*args, **kwargs)
qnap_exporter  |   File "/qnap_exporter/app/routers/exporter_router.py", line 40, in handle_exporter_metrics_update_route_response
qnap_exporter  |     self.exporter.fetch_all_domains_stats()
qnap_exporter  |   File "/qnap_exporter/app/clients/exporter.py", line 82, in fetch_all_domains_stats
qnap_exporter  |     domain_stats.update_stats(last_updated=last_updated)
qnap_exporter  |   File "/qnap_exporter/app/clients/domain_stats.py", line 74, in update_stats
qnap_exporter  |     updated_stats = self._domain_func()
qnap_exporter  |   File "/qnap_exporter/app/clients/qnap_client.py", line 46, in get_system_stats
qnap_exporter  |     return self.client.get_system_stats()
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/qnapstats/qnap_stats.py", line 217, in get_system_stats
qnap_exporter  |     resp = self._get_url(
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/qnapstats/qnap_stats.py", line 74, in _get_url
qnap_exporter  |     self._init_session()
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/qnapstats/qnap_stats.py", line 50, in _init_session
qnap_exporter  |     if self._login() is False:
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/qnapstats/qnap_stats.py", line 58, in _login
qnap_exporter  |     result = self._execute_post_url("authLogin.cgi", data, False)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/qnapstats/qnap_stats.py", line 104, in _execute_post_url
qnap_exporter  |     resp = self._session.post(url, data, timeout=self._timeout, verify=self._verify_ssl)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/requests/sessions.py", line 635, in post
qnap_exporter  |     return self.request("POST", url, data=data, json=json, **kwargs)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/requests/sessions.py", line 587, in request
qnap_exporter  |     resp = self.send(prep, **send_kwargs)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/requests/sessions.py", line 701, in send
qnap_exporter  |     r = adapter.send(request, **kwargs)
qnap_exporter  |   File "/usr/local/lib/python3.10/site-packages/requests/adapters.py", line 553, in send
qnap_exporter  |     raise ConnectTimeout(e, request=request)
qnap_exporter  | requests.exceptions.ConnectTimeout: HTTPConnectionPool(host='10.0.1.1', port=8080): Max retries exceeded with url: /cgi-bin/authLogin.cgi (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0xffff8b5792d0>, 'Connection to 10.0.1.1 timed out. (connect timeout=5)'))
```
