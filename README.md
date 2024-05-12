# JenkinsParser
Это парсер Jenkins написаный на Python с использованием библиотеки JenkinsAPI.
Данная версия программы написана глупым студентом во время прохождения практики и по этому поставляется в соответствии с лицензией MIT

Используемые библиотеки:
    jenkinsapi
    jenkinsapi.utils.crumb_requester (является частью jenkinsapi, необходима для правильной аунтитификации)
    xml.etree.ElementTree
    psycopg2
    asyncio
    
Параметры класса Config задаются в стиле
    'bool_param': {'type': 'Boolean', 'description': 'Boolean параметр', 'defaultValue': 'true'},
    'string_param': {'type': 'String', 'description': 'String параметр', 'defaultValue': 'default_value'}

Функции парсера:
    getJobStatus(self, jobName) - получить статус сбоки
    buildJob(self, jobName) - собрать сборку
    createJob(self, jobName, parameters, description) - создать сборку
    deleteJob(self, jobName) - удалить сборку
    updateConfig(self, jobName, parameters) - обновить xml конфиг файл сборки
    vpn(sekf) - запускиет сборку VPN
