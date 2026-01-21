# JenkinsParser
<br>Это парсер Jenkins написаный на Python с использованием библиотеки JenkinsAPI.
<br>Данная версия программы написана глупым студентом во время прохождения практики и по этому поставляется в соответствии с лицензией MIT

Используемые библиотеки:
    <br>jenkinsapi
    <br>jenkinsapi.utils.crumb_requester (является частью jenkinsapi, необходима для правильной аунтитификации)
    <br>xml.etree.ElementTree
    <br>psycopg2
    <br>asyncio
    
Параметры класса Config задаются в стиле
    <br>'bool_param': {'type': 'Boolean', 'description': 'Boolean параметр', 'defaultValue': 'true'},
    <br>'string_param': {'type': 'String', 'description': 'String параметр', 'defaultValue': 'default_value'}

Функции парсера:
    <br>getJobStatus(self, jobName) - получить статус сбоки
    <br>buildJob(self, jobName) - собрать сборку
    <br>createJob(self, jobName, parameters, description) - создать сборку
    <br>deleteJob(self, jobName) - удалить сборку
    <br>updateConfig(self, jobName, parameters) - обновить xml конфиг файл сборки
    <br>vpn(sekf) - запускиет сборку VPN
