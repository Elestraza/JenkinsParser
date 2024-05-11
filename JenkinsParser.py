import time
from jenkinsapi import jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
from Config import Config

class JenkinsParser:
    def __init__(self, uname, passwd, jenkins_host):
        self.__username = uname
        self.__password = passwd
        self.__jenkins_host = jenkins_host
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

            return(f"Статус сборки {jobName}: {last_build.get_status()}. Номер сборки: {last_build.get_number()}")
        except Exception as e:
            return f"Ошибка: {e}"

    async def createJob(self, jobName, parameters=None, description=""): # Создать задачу
        try:
            configJk = Config()
            config = self.__jenkins.create_job(jobName, configJk.createConfig(self.__jenkins, jobName=jobName, parameters=parameters))
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
Данная версия Программного обеспечения пренадлежит АО "КАЛУГА АСТРАЛ". АО "КАЛУГА АСТРАЛ" имеет полное право на изменение, использование и выпуск 
Программного продукта в любых целях, кроме создания ЯДЕРНОГО ОРУЖИЯ и захвата мира при помощи ИИ! 
'''
# TODO: Научить бота команде VPN, которая будет дергать job VPN. DONE
# TODO: Прикрутить связку Developers-Jobs в БД
# TODO: Настроить отправку данных из БД и в БД
# TODO: Вынести логин и пароль в отдельный файл и читать его
# TODO: Настроить ветки GIT
# TODO: Прикрутить Docker. Образ должен сам собирать все для питона. В Dockerfile указать команду и src для requirements.txt