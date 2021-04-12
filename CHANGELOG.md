# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).

## Unreleased

### New

### Changes

### Fixes

### Breaks

## 1.1.1 - (2021-04-12)

### Changes

* linting code
* cleanup code and documentation
* fix typos

## 1.1.0 - (2021-03-30)

### New

* introduce `CollectorBase` class to derive new collectors from
* added cache module with timed lru cache
* add netdev collector for network information and statistics

### Changes

* reduce docker image size
* we switched base image from python:3-slim to alpine

## 1.0.0 - (2021-03-22)

### New

* now it is simplier to add new collectors. You have to simply follow the naming convention
* add loadavg collector as a real life example

### Breaks

* change load and registration behavior for collectors

## 0.1.0 - (2021-03-04)

### Changes

* move collector to sub module

### Fixes

* signal handling print now clean log messages instead of exceptions
