import time
from datetime import datetime
import asyncio
import psycopg2
from jenkinsapi import jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
from Config import Config

class JenkinsParser:
    def __init__(self, uname, passwd, jenkins_host):
        self.__username = uname
        self.__password = passwd
        self.__jenkins_host = jenkins_host
        self.__conn = psycopg2.connect(
            dbname="AstralJEnkins",
            user="postgres",
            password="passwd",
            host="host",
            port="port"
        )
        # crumb requests
        self.__crumb=CrumbRequester(username=self.__username, password=self.__password, baseurl=f"http://{self.__jenkins_host}")
        self.__jenkins = jenkins.Jenkins(f"http://{self.__jenkins_host}", username=self.__username, password=self.__password, requester=self.__crumb)

    async def getJobStatus(self, jobName): # Вывод статуса сборки
        try:
            job = self.__jenkins.get_job(jobName)
            return f"{jobName}: {job.get_last_build().get_status()}. Номер сборки: {job.get_last_build().get_number()}"
        except Exception as e:
            return f"Ошибка при получении статуса задания {jobName}: {e}"

    async def buildJob(self, jobName): # Запуск сборки
        try:
            build = self.__jenkins.get_job(jobName)
            prev_id = build.get_last_buildnumber()
            self.__jenkins.build_job(jobName)

            while True: # Ждем конца сборки
                if prev_id != build.get_last_buildnumber():
                    break
                time.sleep(3)

            last_build = build.get_last_build()
            while last_build.is_running():
                time.sleep(1)

            cur = self.__conn.cursor()

            # Получение developer_id по nickname из таблицы developers
            cur.execute("SELECT id FROM developers WHERE nickname = %s", (self.__username,))
            developer_id = cur.fetchone()[0] 

            # Получение job_id по jobname из таблицы jobs
            cur.execute("SELECT id FROM jobs WHERE jobname = %s", (jobName,))
            job_id = cur.fetchone()[0]

            # Получение status_id по name из таблицы statuses
            cur.execute("SELECT id FROM statuses WHERE name = %s", (asyncio.run(self.buildJob(jobName)),))
            status_id = cur.fetchone()[0]

            build_time = datetime.now()

            cur.execute("INSERT INTO history (developerid, buildtime, job, status) VALUES (%s, %s, %s, %s)",
                (developer_id, build_time, job_id, status_id))
            
            self.__conn.commit()
            cur.close()
            self.__conn.close()

            return(f"Статус сборки {jobName}: {last_build.get_status()}. Номер сборки: {last_build.get_number()}")
        except Exception as e:
            return f"Ошибка: {e}"

    async def createJob(self, jobName, parameters=None, description="Base description"): # Создать задачу
        try:
            configJk = Config()
            config = self.__jenkins.create_job(jobName, configJk.createConfig(self.__jenkins, jobName=jobName, parameters=parameters,  description=description))
            print(config)
            return f"Задача {jobName} успешно создана"
        except Exception as e:
            return f"Ошибка: {e}"
        
    async def deleteJob(self, jobName):
        try:
            self.__jenkins.delete_job(jobName)
            return f"Задача {jobName} успешно удалена"
        except Exception as e:
            return f"Ошибка при удалении задачи {jobName}: {e}"
        
    async def updateConfig(self, jobName, parameters=None):
        configJk = Config()
        job = self.__jenkins.get_job(jobName)
        await job.update_config(configJk.createConfig(jobName=jobName, parameters=parameters), True)
        return job
        
    async def vpn(self):
        return self.buildJob("VPN")


'''
Данная версия Программного обеспечения написана глупым студентом(автором) и пренадлежит АО "КАЛУГА АСТРАЛ". АО "КАЛУГА АСТРАЛ" имеет полное право на изменение, использование и выпуск 
Программного продукта в любых целях, кроме создания ЯДЕРНОГО ОРУЖИЯ и захвата мира при помощи ИИ! 
'''
