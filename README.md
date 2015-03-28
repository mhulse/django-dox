# Django Dox

### Yet another Django flat pages app on steroids.

The built-in flat pages app of Django is cool, but it does have its limitations. This app is based on [Django's flat pages app](https://docs.djangoproject.com/en/dev/ref/contrib/flatpages/), but its got a bunch more (useful) fields and a few other goodies.

This is app perfect for managing template shells and for quick prototyping.

Tested and working with Djago 1.3.

---

#### INSTALLATION

Install using [`pip`](http://www.pip-installer.org/):

```bash
$ sudo pip install -e git+https://github.com/registerguard/django-dox.git#egg=django-dox
```

Add `'dox',` to your `installed_apps` setting.

Put this in your URLs:

```python
(r'^pages/', include('dox.urls')),
```

Run:

```bash
$ sudo service apache2 restart
```

... or:

```bash
$ touch apache/django.wsgi
```

... or whatever you need to do to reload things.

Lastly:

```bash
$ python manage.py syncdb
```

Next, load the fixture for statii:

```bash
$ python manage.py loaddata dox/fixtures/dox_initial_data.json
```

OR, manaully add statii:

1. "Open", live.
2. "Closed", not live.

... and you're ready to go (maybe do another `touch`?)!

Enjoy your **Django Dox** app _today!_

---

#### LEGAL

Copyright © 2013 [Micky Hulse](http://hulse.me)/[The Register-Guard](http://registerguard.com)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in compliance with the License. You may obtain a copy of the License in the LICENSE file, or at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.