Dionysos
========

A server for managing sensors and actuators in a aquaponics setup. Written in Python using the Django framework

Roadmap
========

_Planned releases and their featureset (subject to change). When a version number is in front of the feature, it was implemented in that version. Documentation will probably lag behind_

API
---
A RESTfull JSON API which can be used to create endpoints for measurements to be sent to by other devices (Arduino, for example)

* 0.1 DataPoints API [doc](https://github.com/todorus/dionysos/wiki/API-documentation#datapoints)
* Measurements API
* Images

Admin client
---
Admin webapp for sensor data collecting endpoints

* DataPoints admin
* Measurements admin
* Arduino code generator
* Reporting

Deployment
---
* Easy deployment on Google App Engine
* Easy deployment on Raspberry PI
* Easy deployment on Ubuntu

Triggers
---
* Send Emails
* Send Push notifications
* Send custom messages to actuators
